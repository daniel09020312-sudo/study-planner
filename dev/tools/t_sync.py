# 바뀐 것만 받기: 두 기기 동기화, 다시 열 때 전체를 받지 않는지, 예전 판 쓰기, 표 정리, 오프라인, 받은 양, 새 판 다시 읽기
import os, sys, json, datetime, time
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
def closepin(pg):
    pg.wait_for_timeout(300)
    if ev(pg, "!!document.querySelector('#dlg-pin')"): pg.evaluate("()=>{const b=document.querySelector('#dlg-pin [data-act=\"modal-close\"],#dlg-pin [data-act=\"pin-skip\"]');if(b)b.click();}"); pg.wait_for_timeout(300)

T = datetime.date.today().isoformat()
R = 'syncroomabcdef12'
STORE['rooms'] = {R: {'d': {
    'meta': {'config': {'certHour': 26, 'roster': [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}]}, 'room': {'name': '동기화 방', 'code': '555666'}},
    'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'i1', 'label': '문제집 풀이'}]}},
    'days': {'m1_' + T: {'goals': [{'id': 'g1', 'text': '처음 할 일', 'sid': 's1', 'done': False}], 'mid': 'm1', 'date': T}},
    'msgs': {('x%03d' % i): {'from': 'm2', 'text': '예전 메시지 %d' % i, 'at': 1792700000000 + i} for i in range(40)}}},
  'joincode-555666': {'r': R, 'n': '동기화 방'}}
def X(): return get_at('/rooms/' + R + '/x') or {}
def logs(since): return [(m, p) for m, p in LOG[since:] if p.startswith('/rooms/' + R)]
BASE_LS = {'gbb_remote': json.dumps({'url': DB, 'room': R}), 'gbb_legacy_room': '-', 'gbb_rooms': json.dumps([{'url': DB, 'room': R, 'name': '동기화 방', 'code': '555666'}])}
def cache(pg):
    return json.loads(ev(pg, "localStorage.getItem('gbb_cache@%s')||'null'" % R) or 'null')
def open_dev(me, w=390):
    ls = dict(BASE_LS); ls['gbb_me@' + R] = me; ls['gbb_pinask@' + R] = json.dumps({'m1': 1, 'm2': 1})
    cx, pg = newpage(w=w, h=844, ls=ls)
    pg.goto(SITE + '#j=' + TOK, wait_until='commit'); pg.wait_for_timeout(2600); closepin(pg)
    return cx, pg

# ---- A 처음 열기: 저장된 기록이 없으니 전체 한 번
n0 = len(LOG)
ca, A = open_dev('m1')
L = logs(n0)
print('A first       : full GET', ('GET', '/rooms/' + R + '/d') in L, '| x stream', ('GET', '/rooms/' + R + '/x') in L)
# ---- A가 할 일 추가 -> 기록과 표가 같이
click(A, '[data-act="tab"][data-tab="cal"]', 600)
A.evaluate("()=>{const b=document.querySelector('#c-goals [data-act=\"open\"][data-modal=\"compose\"]');b.click();}"); A.wait_for_timeout(700)
A.fill('.dialog input[data-draft="cmpNote"]', 'A가 새로 적은 일'); A.wait_for_timeout(200)
click(A, '.dialog [data-act="cmp-add"]:not([data-more])', 1200)
day = get_at('/rooms/' + R + '/d/days/m1_' + T) or {}
print('A write       :', [g['text'] for g in day.get('goals', [])], '| x token', 'days|m1_' + T in X(), '| mid/date gone', 'mid' not in day and 'date' not in day)
print('A methods     :', sorted(set(m for m, p in logs(n0) if m != 'GET')))
# ---- B 열기 (처음): A가 쓴 것 보임
cb, B = open_dev('m2')
B.wait_for_timeout(2500)
cbB = cache(B)
print('B sees A      :', 'A가 새로 적은 일' in json.dumps(cbB, ensure_ascii=False), '| cache has x', bool(cbB and cbB.get('x')))
# ---- A가 하나 더: B는 그 자리만 다시 받음
n1 = len(LOG)
A.evaluate("()=>{const b=document.querySelector('#c-goals [data-act=\"open\"][data-modal=\"compose\"]');b.click();}"); A.wait_for_timeout(700)
A.fill('.dialog input[data-draft="cmpNote"]', '두 번째 일'); A.wait_for_timeout(200)
click(A, '.dialog [data-act="cmp-add"]:not([data-more])', 1200)
B.wait_for_timeout(3000)
LB = [x for x in logs(n1) if x[0] == 'GET' and '/d' in x[1]]
print('B live        :', '두 번째 일' in json.dumps(cache(B), ensure_ascii=False), '| B GET paths', sorted(set(p.split('/d/')[-1] if '/d/' in p else p for m, p in LB))[:4])
# ---- B 다시 열기: 저장해 둔 기록으로, 전체 받기 없음
n2 = len(LOG)
B.reload(); B.wait_for_timeout(3000); closepin(B)
L2 = logs(n2)
print('B reopen      : full GET', ('GET', '/rooms/' + R + '/d') in L2, '| requests', len(L2), '| shows goal', ev(B, "document.body.innerText.includes('서연')"))
# ---- 예전 판(표 없이 PUT)이 쓴 것: 바로는 안 보이고, 전체 받기 때 보임
with LOCK:
    set_at('/rooms/' + R + '/d/days/m2_' + T, {'goals': [{'id': 'go', 'text': '예전 판이 쓴 일', 'sid': 's1', 'done': False}]})
B.wait_for_timeout(2500)
print('old client    : seen now', '예전 판이 쓴 일' in json.dumps(cache(B), ensure_ascii=False))
B.evaluate("()=>{const k='gbb_cache@%s',c=JSON.parse(localStorage.getItem(k));c.full=Date.now()-2*3600000;localStorage.setItem(k,JSON.stringify(c));}" % R)
n3 = len(LOG)
B.reload(); B.wait_for_timeout(3500); closepin(B)
print('old client    : after reopen (full 2h ago) full GET', ('GET', '/rooms/' + R + '/d') in logs(n3), '| seen', '예전 판이 쓴 일' in json.dumps(cache(B), ensure_ascii=False))
# ---- 예전 형식 저장(x 없음) -> 전체 한 번
B.evaluate("()=>{const k='gbb_cache@%s',c=JSON.parse(localStorage.getItem(k));delete c.x;delete c.full;delete c.sy;localStorage.setItem(k,JSON.stringify(c));}" % R)
n4 = len(LOG)
B.reload(); B.wait_for_timeout(3000); closepin(B)
print('old cache     : full GET', ('GET', '/rooms/' + R + '/d') in logs(n4))
# ---- 오래된 표 정리
old = (int((time.time() - 5 * 86400) * 1000))
def b36(n):
    s = ''
    while n: s = '0123456789abcdefghijklmnopqrstuvwxyz'[n % 36] + s; n //= 36
    return s
with LOCK:
    for i in range(5): set_at('/rooms/' + R + '/x/msgs|old%d' % i, b36(old) + '.zz%02d' % i)
A.wait_for_timeout(6000)
print('prune         : old left', len([k for k in X() if k.startswith('msgs|old')]), '| total x', len(X()))
# ---- 오프라인에서 쓰기 -> 연결되면 표와 함께
cb.set_offline(True); B.wait_for_timeout(300)
B.evaluate("()=>window.dispatchEvent(new Event('offline'))")
click(B, '[data-act="tab"][data-tab="cal"]', 600)
B.evaluate("()=>{const b=document.querySelector('#c-goals [data-act=\"open\"][data-modal=\"compose\"]');b.click();}"); B.wait_for_timeout(700)
B.fill('.dialog input[data-draft="cmpNote"]', '오프라인 일'); B.wait_for_timeout(200)
click(B, '.dialog [data-act="cmp-add"]:not([data-more])', 1000)
print('offline       : outbox', ev(B, "(JSON.parse(localStorage.getItem('gbb_outbox@%s')||'[]')).length" % R))
cb.set_offline(False); B.evaluate("()=>window.dispatchEvent(new Event('online'))"); B.wait_for_timeout(2500)
d2 = get_at('/rooms/' + R + '/d/days/m2_' + T) or {}
print('online        :', [g['text'] for g in d2.get('goals', [])], '| x', 'days|m2_' + T in X(), '| outbox', ev(B, "(JSON.parse(localStorage.getItem('gbb_outbox@%s')||'[]')).length" % R))
A.wait_for_timeout(2500)
print('A sees B      :', '오프라인 일' in json.dumps(cache(A), ensure_ascii=False))
# ---- 받은 양 표시
click(B, '#meBtn', 700)
print('usage         :', ev(B, "(document.querySelector('.rmsz')||{}).textContent"))
B.evaluate("()=>{const b=document.querySelector('[data-act=\"modal-close\"]');if(b)b.click();}"); B.wait_for_timeout(400)
# ---- 새 판: 보는 중에는 다시 읽지 않고, 돌아올 때 다시 읽음
build = int(open(WEB + '/version.txt').read().split()[0])
open(BASE + '/site/version.txt', 'w').write(str(build + 1) + '\n')
B.evaluate("()=>{window.__mark=1;}")
B.wait_for_timeout(6500)
print('new build     : still same page', ev(B, "window.__mark===1"))
B.evaluate("()=>{Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'visible'});document.dispatchEvent(new Event('visibilitychange'));}")
B.wait_for_timeout(3000)
print('came back     : reloaded', ev(B, "window.__mark!==1"))
open(BASE + '/site/version.txt', 'w').write(str(build) + '\n')
print('errors', errors)
br.close(); pw.stop()
