# 웹 판(실제 동기화 경로)에서 50명 기록으로 view() 계산 시간과, 메시지 하나가 들어올 때 다시 그리기 시간
import os, sys, json, datetime, time
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
def closepin(pg):
    pg.wait_for_timeout(300)
    if ev(pg, "!!document.querySelector('#dlg-pin')"): pg.evaluate("()=>{const b=document.querySelector('#dlg-pin [data-act=\"modal-close\"],#dlg-pin [data-act=\"pin-skip\"]');if(b)b.click();}"); pg.wait_for_timeout(300)
T = datetime.date(2026, 11, 25)
NOWMS = lambda: int(datetime.datetime(2026, 11, 25, 12, 0, 0).timestamp() * 1000)
R = 'perfroomabcdef12'
N = 50
ros = [{'id': 'm%d' % i, 'name': '학생%02d' % i} for i in range(1, N + 1)]
days = {}
for i in range(1, N + 1):
    for k in range(45):
        d = (T - datetime.timedelta(days=k)).isoformat()
        days['m%d_%s' % (i, d)] = {'goals': [{'id': 'g%d' % g, 'text': '할 일 %d' % g, 'sid': 's%d' % (1 + (i + g + k) % 2), 'done': (i + g + k) % 3 != 0} for g in range(4)], 'mins': {'s1': 30 + (i * k) % 120, 's2': 20}, 'in': d + 'T00:10:00.000Z'}
msgs = {'z%d' % k: {'from': 'm%d' % (1 + k % N), 'to': 'all', 'text': '메시지 %d' % k, 'at': NOWMS() - k * 60000} for k in range(600)}
STORE['rooms'] = {R: {'d': {'meta': {'config': {'certHour': 29, 'migCert5': 1, 'migHum': 1, 'roster': ros}, 'room': {'name': '성능 방', 'code': '999111'}},
    'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'i1', 'label': '개념'}]}, 's2': {'name': '영어', 'order': 2, 'items': [{'id': 'i1', 'label': '단어'}]}},
    'days': days, 'msgs': msgs}}, 'joincode-999111': {'r': R, 'n': '성능 방'}}
def b36(n):
    s = ''
    while n: s = '0123456789abcdefghijklmnopqrstuvwxyz'[n % 36] + s; n //= 36
    return s
def tok(): return b36(NOWMS()) + '.t%03d' % (NOWMS() % 1000)
def server_set(path, val):
    with LOCK:
        set_at('/rooms/' + R + '/d/' + path, val)
        set_at('/rooms/' + R + '/x/' + path.replace('/', '|'), tok())
LS = {'gbb_remote': json.dumps({'url': DB, 'room': R}), 'gbb_legacy_room': '-', 'gbb_rooms': json.dumps([{'url': DB, 'room': R, 'name': '성능 방', 'code': '999111'}]),
      'gbb_me@' + R: 'm1', 'gbb_test': '1', 'gbb_pinask@' + R: json.dumps({m['id']: 1 for m in ros})}
cb, B = newpage(w=1180, h=820, ls=LS)
B.emulate_media(reduced_motion='reduce')
B.add_init_script('(()=>{const O=Date,off=%d-O.now();class D extends O{constructor(...a){if(a.length)super(...a);else super(O.now()+off);}static now(){return O.now()+off;}};window.Date=D;})()' % NOWMS())
B.goto(SITE + '#j=' + TOK, wait_until='commit'); B.wait_for_timeout(6000); closepin(B)
print('ready', ev(B, "__gbb.S.ready"))
t = lambda e: B.evaluate("()=>{const a=performance.now();%s;return performance.now()-a}" % e)
print('days', ev(B,"Object.keys(__gbb.view().days).length"), 'roster', ev(B,"__gbb.view().roster.length"), 'today', ev(B,"__gbb.today()"), 'sc m2 days', ev(B,"Object.keys(__gbb.view().sc.m2||{}).length"))
print('view() #1 %.1f ms' % t("__gbb.view()"))
print('view() #2 %.1f ms' % t("__gbb.view()"))
print('view() #3 %.1f ms' % t("__gbb.view()"))
for tab in ['chat', 'cal']:
    B.evaluate("(t)=>document.querySelector('[data-act=\"tab\"][data-tab=\"'+t+'\"]').click()", tab); B.wait_for_timeout(500)
    B.evaluate("()=>{window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(e.duration))).observe({entryTypes:['longtask']});}")
    for i in range(3):
        server_set('msgs/new%s%d' % (tab, i), {'from': 'm2', 'to': 'all', 'text': '새 메시지', 'at': NOWMS()}); B.wait_for_timeout(1500)
    print('incoming on', tab, 'long tasks ms:', [round(x) for x in ev(B, "window.__lt")])
print('errors', errors)
