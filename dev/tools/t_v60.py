# v57: 설정 > 시작 연출 끄기 -> 다음에 새로 켤 때 연출 없이 바로 열림
import os, json
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
R = 'splashroomabcd12'
STORE['rooms'] = {R: {'d': {'meta': {'config': {'certHour': 29, 'migCert5': 1, 'migHum': 1, 'roster': [{'id': 'm1', 'name': '민준'}]}, 'room': {'name': '연출 방', 'code': '343434'}}}}, 'joincode-343434': {'r': R, 'n': '연출 방'}}
ok = True
def check(n, c, x=''):
    global ok
    print(('OK  ' if c else 'FAIL'), n, x)
    if not c: ok = False
LS = {'gbb_remote': json.dumps({'url': DB, 'room': R}), 'gbb_legacy_room': '-', 'gbb_rooms': json.dumps([{'url': DB, 'room': R, 'name': '연출 방', 'code': '343434'}]), 'gbb_me@' + R: 'm1', 'gbb_pinask@' + R: json.dumps({'m1': 1})}
U = SITE + '#j=fake-planner.asia-southeast1'
cb, A = newpage(w=390, h=844, ls=LS)
A.goto(U, wait_until='commit'); A.wait_for_timeout(200)
check('splash on first open', ev(A, "!!document.getElementById('splash')"))
A.wait_for_timeout(4000)
A.evaluate("()=>{document.querySelector('#meBtn').click();}"); A.wait_for_timeout(600)
check('setting shown', ev(A, "!!document.querySelector('[data-act=\"sp-toggle\"]')"))
A.evaluate("()=>document.querySelector('[data-act=\"sp-toggle\"]').click()"); A.wait_for_timeout(400)
check('stored', ev(A, "localStorage.getItem('gbb_nosplash')") == '1')
check('label', '켜기' in ev(A, "document.querySelector('[data-act=\"sp-toggle\"]').textContent"))
# 새로 켜기: 새 탭(새 sessionStorage), 같은 localStorage
B = cb.new_page()
B.add_init_script("window.__sp0=null;document.addEventListener('readystatechange',()=>{if(window.__sp0===null)window.__sp0=!!document.getElementById('splash');});")
B.goto(U, wait_until='commit'); B.wait_for_timeout(300)
check('no splash next open', ev(B, "!document.getElementById('splash') && window.__sp0===false"), ev(B, "window.__sp0"))
B.wait_for_timeout(2500)
check('app opened', ev(B, "!!document.querySelector('#meBtn')"))
B.evaluate("()=>{document.querySelector('#meBtn').click();}"); B.wait_for_timeout(600)
B.evaluate("()=>document.querySelector('[data-act=\"sp-toggle\"]').click()"); B.wait_for_timeout(300)
check('turned back on', ev(B, "localStorage.getItem('gbb_nosplash')") is None)
C = cb.new_page(); C.goto(U, wait_until='commit'); C.wait_for_timeout(200)
check('splash again', ev(C, "!!document.getElementById('splash')"))
print('ALL OK' if ok else 'SOME FAILED')
