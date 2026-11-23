# v106: 할 일 목록에서 할 일을 눌러도 달력으로 안 넘어가고 고치기 창이 열림
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=datetime.datetime(2026,11,23,15,0,0));close_dlg(p);p.wait_for_timeout(800)
p.evaluate("()=>{const S=window.__store;S['days/m1_2026-11-24']={goals:[{id:'gx',text:'수학 문제집 20문제',sid:'s2',done:false}],mins:{}};S['days/m1_2026-11-20']={goals:[{id:'gp',text:'지난 할 일',sid:'s2',done:false}],mins:{}};window.__fire();}");p.wait_for_timeout(600)
check('list mode',ev(p,"!!document.getElementById('wkScroll')"))
click(p,'#wi-gx .wkt',700)
check('still list (no calendar)',ev(p,"!!document.getElementById('wkScroll')"))
check('edit window open',ev(p,"!!document.querySelector('#dlg-compose')"))
check('filled with goal',ev(p,"(document.querySelector('#dlg-compose')||{}).textContent||''").find('수학')>=0 or ev(p,"[...document.querySelectorAll('#dlg-compose input')].some(i=>i.value.includes('20'))"))
p.keyboard.press('Escape');p.wait_for_timeout(500)
if ev(p,"!!document.querySelector('#dlg-compose')"):click(p,'[data-act="modal-close"]',500)
p.evaluate("()=>{const w=document.getElementById('wkScroll');const c=document.getElementById('wc-2026-11-20');if(w&&c)w.scrollLeft=c.offsetLeft-20;}");p.wait_for_timeout(500)
if ev(p,"!!document.querySelector('#wi-gp .wkt')"):
    click(p,'#wi-gp .wkt',600)
    check('past: still list, no window',ev(p,"!!document.getElementById('wkScroll')") and not ev(p,"!!document.querySelector('#dlg-compose')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
