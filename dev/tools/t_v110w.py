# v109 화이트보드 웹 판 두 기기: A가 쓰면 B에 보이고, B가 쓰면 A 판에 이름표 (LIGHT=1, site/index.html)
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


ca, A = open_dev('m1', 1180)
cb, B = open_dev('m2')
click(A, '[data-act="tab"][data-tab="room"]', 600)
click(A, '#c-wb .btn[data-act="wb-open"]', 700)
st = A.query_selector('#wbStage').bounding_box()
A.mouse.move(st['x']+200, st['y']+200); A.mouse.down()
for i in range(1, 11): A.mouse.move(st['x']+200+30*i, st['y']+200+10*i)
A.mouse.up(); A.wait_for_timeout(2500)
wb = get_at('/rooms/' + R + '/d/wb') or {}
print('A wrote stroke:', len(wb))
click(B, '[data-act="tab"][data-tab="room"]', 600)
B.evaluate("()=>document.getElementById('c-wb').scrollIntoView()"); B.wait_for_timeout(300)
print('B sees:', ev(B, "!!document.querySelector('#c-wb .wbprev img')"), ev(B, "document.getElementById('c-wb').textContent.includes('민준')"))
click(B, '#c-wb .btn[data-act="wb-open"]', 700)
print('B info:', ev(B, "document.getElementById('wbInfo')?document.getElementById('wbInfo').textContent:''"))
# B가 쓰면 A 판에 이름표
st2 = B.query_selector('#wbStage').bounding_box()
B.mouse.move(st2['x']+50, st2['y']+300); B.mouse.down(); B.mouse.move(st2['x']+150, st2['y']+350); B.mouse.move(st2['x']+250, st2['y']+330); B.mouse.up(); B.wait_for_timeout(3000)
print('A info after B:', ev(A, "document.getElementById('wbInfo').textContent"), 'tag', ev(A, "document.querySelectorAll('.wbtag').length"))
print('ERR', ERRS if 'ERRS' in dir() else '')
print('fb count', len(get_at('/rooms/' + R + '/d/wb') or {}))
A.wait_for_timeout(4000)
print('A info later:', ev(A, "document.getElementById('wbInfo').textContent"))
print('B info later:', ev(B, "document.getElementById('wbInfo').textContent"))
c=cache(A); print('A cache wb', list(((c or {}).get('t') or {}).get('wb',{}).keys()), 'x', [k for k in ((c or {}).get('x') or {}) if k.startswith('wb')])
print('A card text', ev(A,"document.getElementById('c-wb')?document.getElementById('c-wb').textContent:''")[:80])
click(A,'[data-w="close"]',800)
print('A card after close', ev(A,"document.getElementById('c-wb').textContent")[:80])
