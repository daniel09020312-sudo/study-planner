import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,29,12,0,0)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
# 1) 지난 날: 완료 3개 + 옮긴(mv) 1개 + 마감 뒤 인증 -> 모두 끝내고 인증 점수(늦은 인증 20점)
p.evaluate("()=>{const S=window.__store;S['days/m1_2026-10-27']={in:'2026-10-27T00:10:00.000Z',certAt:'2026-10-29T01:00:00.000Z',mins:{s2:60},goals:[{id:'a',text:'1',sid:'s2',done:true},{id:'b',text:'2',sid:'s2',done:true},{id:'c',text:'3',sid:'s2',done:true},{id:'d',text:'옮긴 것',sid:'s2',done:false,mv:1}]};window.__fire();}");p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="report"]',900)
txt=st(p,"document.body.innerText")
rows=st(p,"[...document.querySelectorAll('#c-rdaily-this tbody tr')].map(r=>r.innerText.replace(/\\s+/g,' ')).join('|')")
print(rows[:300])
# 점수 내역: 모두 끝내기 칸이 20점 이상
import re
sc=st(p,"[...document.querySelectorAll('#c-rpts-this .hb')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
m=re.search(r'할 일 모두 끝내기\s*(\d+)점',sc)
check('moved goal does not block all-done points',bool(m) and int(m.group(1))>=20,sc[:200])
# 2) 대결 화면: 종류 3개, 오른쪽 칸
click(p,'[data-act="tab"][data-tab="play"]',700);click(p,'[data-act="play-tab"][data-id="duel"]',700)
check('side column cards',st(p,"!!document.querySelector('#c-duelriv')&&!!document.querySelector('#c-duelbig')&&!!document.querySelector('#c-duelhall')"))
check('rival rows',st(p,"document.querySelectorAll('#c-duelriv .rival').length")>=1,st(p,"document.querySelectorAll('#c-duelriv .rival').length"))
click(p,'#c-duelriv [data-act="open"][data-modal="duel"]',600)
check('3 kinds',st(p,"document.querySelectorAll('.dialog [data-k=\"kind\"]').length")==3,st(p,"document.querySelectorAll('.dialog [data-k=\"kind\"]').length"))
check('rival preselected',st(p,"!!document.querySelector('.dialog [data-k=\"b\"][aria-pressed=\"true\"]')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
