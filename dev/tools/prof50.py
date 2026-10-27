# 50명 방에서 새 메시지 하나가 들어올 때 어느 함수가 오래 걸리는지 (CDP 프로파일러)
import sys, json, datetime, collections
sys.path.insert(0, '/home/claude/planner/tools')
src = open('/home/claude/planner/tools/perf50.py', encoding='utf-8').read().split("tabs = ['cal'")[0]
exec(src)
tab = sys.argv[2] if len(sys.argv) > 2 else 'chat'
p.evaluate("(t)=>document.querySelector('[data-act=\"tab\"][data-tab=\"'+t+'\"]').click()", tab); p.wait_for_timeout(500)
c = p.context.new_cdp_session(p)
c.send('Profiler.enable'); c.send('Profiler.setSamplingInterval', {'interval': 200}); c.send('Profiler.start')
for i in range(3):
    p.evaluate("()=>{window.__store['msgs/zz'+Date.now()]={from:'m2',to:'all',text:'새',at:Date.now()};window.__fire();}"); p.wait_for_timeout(200)
prof = c.send('Profiler.stop')['profile']
nodes = {n['id']: n for n in prof['nodes']}
self_t = collections.Counter()
dt = prof['timeDeltas']
for sid, d in zip(prof['samples'], dt):
    cf = nodes[sid]['callFrame']; self_t[(cf['functionName'] or '(anon)') + ':' + str(cf['lineNumber'])] += d
tot = sum(self_t.values())
print('total ms', tot / 1000)
for k, v in self_t.most_common(14): print('%8.1f ms  %s' % (v / 1000, k))
R.close()
