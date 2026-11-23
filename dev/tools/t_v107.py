# v107: 할 일을 꾹 누르고 가만히 있으면 화면이 저절로 스크롤되지 않음(아래쪽 할 일도)
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from playwright.sync_api import sync_playwright
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
R=Rig()
_nc=R.browser.new_context
R.browser.new_context=lambda **k:_nc(has_touch=True,**k)
p=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=datetime.datetime(2026,11,23,15,0,0))
close_dlg(p);p.wait_for_timeout(600)
p.evaluate("()=>{const S=window.__store;['2026-11-23','2026-11-22','2026-11-21','2026-11-24'].forEach(d=>S['days/m1_'+d]={goals:Array.from({length:4},(_,i)=>({id:'g'+i,text:'할 일 '+i,sid:'s2',done:false})),mins:{}});window.__fire();}");p.wait_for_timeout(700)
# 화면 아래쪽(가장자리 60px 안)에 있는 할 일 찾기
box=p.evaluate("()=>{const sc=document.getElementById('wkScroll').getBoundingClientRect();let best=null;document.querySelectorAll('.wkc .wki[data-wdrag] .wkt').forEach(e=>{const r=e.getBoundingClientRect();if(!best&&r.left>=sc.left-1&&r.left<sc.left+60&&r.top>0&&r.bottom<innerHeight)best=[r.left+12,r.top+r.height/2];});return best}")
check('found item at left edge of list',box is not None,box)
if box:
    cdp=p.context.new_cdp_session(p)
    y0=p.evaluate("()=>[document.getElementById('main').scrollTop,document.getElementById('wkScroll').scrollLeft]")
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box[0],'y':box[1]}]})
    p.wait_for_timeout(1500)
    lifted=p.evaluate("()=>document.documentElement.classList.contains('wkdragging')")
    y1=p.evaluate("()=>[document.getElementById('main').scrollTop,document.getElementById('wkScroll').scrollLeft]")
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    p.wait_for_timeout(400)
    check('long press lifts item',lifted)
    check('no auto scroll while holding still',y1==y0,(y0,y1))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
