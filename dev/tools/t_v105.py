# v105: 병맛 히든
import sys,json,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
NOW=datetime.datetime(2026,11,22,15,0,0)
def pre(extra=''):return "(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;%sclearInterval(t);},5);})();"%extra
def shop(p,cat):
    click(p,'#shopBtn',600);click(p,'[data-act="shop-cat"][data-v="%s"]'%cat,500)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999','gbb_me':'m2'},now=NOW,pre=pre());close_dlg(p);p.wait_for_timeout(400)
shop(p,'ring');check('flame locked as bm',ev(p,"!!document.querySelector('#shi-r-flame.hid2.bm')"),ev(p,"(document.querySelector('#shi-r-flame')||{}).textContent"))
check('zzz back',ev(p,"!!document.querySelector('#shi-r-zzz')"))
check('no 병맛 word',('병맛' not in ev(p,"document.querySelector('#dlg-shop').textContent")))
click(p,'[data-act="shop-cat"][data-v="color"]',400);check('neon green removed',not ev(p,"!!document.querySelector('#shi-a-hlime')"))
click(p,'[data-act="shop-cat"][data-v="look"]',400);check('mini02 locked',ev(p,"!!document.querySelector('#shi-c-mini02.hid2')"))
R.close()
seed="['2026-11-17','2026-11-18','2026-11-19'].forEach(function(d){S['days/m2_'+d]={mins:{},in:d+'T09:00:00+09:00',goals:[]};});S['days/m2_2026-11-20']={mins:{s1:71},in:'2026-11-20T09:00:00+09:00',goals:[]};var p=S['progress/m2']||{};p.shop={own:{'r:flame':30,'c:mini02':60},gf:1};S['progress/m2']=p;"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999','gbb_me':'m2'},now=NOW,pre=pre(seed));close_dlg(p);p.wait_for_timeout(400)
shop(p,'ring')
check('flame opened',ev(p,"!!document.querySelector('#shi-r-flame [data-act=\"shop-use\"]')"))
check('bm condition line','히든 · 조건' in ev(p,"(document.querySelector('#shi-r-flame .hidc')||{}).textContent||''"))
click(p,'#shi-r-flame [data-act="shop-use"]',500)
check('flame ring on avatar',ev(p,"!!document.querySelector('.av.rg-flame')"))
click(p,'[data-act="shop-cat"][data-v="look"]',400)
click(p,'#shi-c-mini02 [data-act="shop-use"]',500)
check('mini02 applied',ev(p,"document.documentElement.getAttribute('data-concept')")=='mini02')
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/mini02.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
