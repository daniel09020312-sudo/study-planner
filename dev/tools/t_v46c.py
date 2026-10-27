# 점수 캐시가 기록이 바뀔 때 새로 계산되는지(실제 동기화 경로)
import os, sys, json, datetime, time
src = open('/home/claude/planner/tools/perf50w.py', encoding='utf-8').read().split("print('ready'")[0]
exec(src)
ok = True
def check(n, c, x=''):
    global ok
    print(('OK  ' if c else 'FAIL'), n, x)
    if not c: ok = False
TD = '2026-11-25'
def sc(m): return ev(B, "(()=>{const r=__gbb.view().sc['%s']['%s'];return r?[r.total,r.done,r.mins]:null})()" % (m, TD))
a = sc('m2')
# 1) 다른 기기가 m2의 오늘 기록을 바꿈 (제자리 갱신 경로)
server_set('days/m2_' + TD, {'goals': [{'id': 'a', 'text': 'x', 'sid': 's1', 'done': True}] * 1 + [{'id': 'b', 'text': 'y', 'sid': 's1', 'done': True}, {'id': 'c', 'text': 'z', 'sid': 's1', 'done': True}], 'mins': {'s1': 400}, 'in': TD + 'T00:10:00.000Z'})
B.wait_for_timeout(2500)
b = sc('m2')
check('score changes after remote day update', a != b, (a, b))
# 2) 내 이름 바꾸기 -> 명단(설정)이 바뀐 뒤에도 순위 계산 유지
c0 = ev(B, "__gbb.view().roster.length")
server_set('meta/config', {'certHour': 29, 'migCert5': 1, 'migHum': 1, 'roster': ros[:10], 'cfgx': 1})
B.wait_for_timeout(2500)
check('roster shrink seen', ev(B, "__gbb.view().roster.length") == 10, ev(B, "__gbb.view().roster.length"))
check('chat rebuilt for new roster', ev(B, "Object.keys(__gbb.view().chat).length") <= 10, ev(B, "Object.keys(__gbb.view().chat).length"))
# 3) 메시지 들어옴 -> 대화 목록 갱신
n0 = ev(B, "__gbb.view().chat.all.length")
server_set('msgs/zznew', {'from': 'm2', 'to': 'all', 'text': '새 글', 'at': NOWMS()})
B.wait_for_timeout(2000)
check('chat updated', ev(B, "__gbb.view().chat.all.length") == n0 + 1, (n0, ev(B, "__gbb.view().chat.all.length")))
print('errors', errors); check('no errors', not errors)
print('ALL OK' if ok else 'SOME FAILED')
