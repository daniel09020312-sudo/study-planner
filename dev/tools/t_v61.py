# v58: 지난 날에서 옮긴 할 일은 그 날 '모두 끝내고 인증'에서 끝낸 것으로 침(3개 조건에는 셈)
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,29,12,0,0)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
G=lambda i,done,mv=0:"{id:'%s',text:'%s',sid:'s2',done:%s%s}"%(i,i,'true' if done else 'false',',mv:1' if mv else '')
p.evaluate("()=>{const S=window.__store;"
  "S['days/m1_2026-10-26']={in:'2026-10-26T00:10:00.000Z',certAt:'2026-10-26T12:00:00.000Z',goals:[%s,%s,%s]};"
  "S['days/m1_2026-10-27']={in:'2026-10-27T00:10:00.000Z',certAt:'2026-10-27T12:00:00.000Z',goals:[%s,%s,%s]};"
  "S['days/m1_2026-10-28']={in:'2026-10-28T00:10:00.000Z',certAt:'2026-10-28T12:00:00.000Z',goals:[%s,%s]};"
  "window.__fire();}"%(G('a',1),G('b',0,1),G('c',0,1),G('d',0,1),G('e',0,1),G('f',0,1),G('g',1),G('h',1)))
p.wait_for_timeout(700)
click(p,'[data-act="tab"][data-tab="report"]',900)
import re
sc=p.evaluate("()=>[...document.querySelectorAll('#c-rpts-this .hb')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
m=re.search(r'할 일 모두 끝내기\s*(\d+)점',sc)
print(sc[:300])
check('two days with moved goals get all-done points (2 x 50)',bool(m) and int(m.group(1))==100,m and m.group(1))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
