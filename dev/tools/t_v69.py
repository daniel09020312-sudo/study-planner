# v70: 달력 할 일 목록에서 옆으로 밀면 다음/이전 주, 달력은 달
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
_nc=R.browser.new_context
R.browser.new_context=lambda **k:_nc(has_touch=True,**k)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now='2026-11-01T22:00:00+09:00');close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',600);click(p,'[data-act="cal-mode"][data-id="list"]',800)
def title():return ev(p,"(document.querySelector('#view-cal h1')||{}).textContent")
SW="""(a)=>{const v=document.querySelector('#view-cal .card')||document.getElementById('view-cal');const r=v.getBoundingClientRect();const y=r.top+Math.min(300,r.height/2),x0=r.left+r.width/2;
const mk=(x)=>new Touch({identifier:1,target:v,clientX:x,clientY:y});
v.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[mk(x0)],changedTouches:[mk(x0)]}));
v.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[mk(x0+a)]}));}"""
t0=title();p.evaluate(SW,-200);p.wait_for_timeout(700);t1=title()
check('swipe left -> next week',t1!=t0,(t0,t1))
p.evaluate(SW,200);p.wait_for_timeout(700);t2=title()
check('swipe right -> back',t2==t0,(t2,t0))
p.evaluate(SW,-30);p.wait_for_timeout(500)
check('short move ignored',title()==t0)
click(p,'[data-act="cal-mode"][data-id="cal"]',800)
m0=title();p.evaluate(SW,-200);p.wait_for_timeout(700)
check('month swipe',title()!=m0,(m0,title()))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
