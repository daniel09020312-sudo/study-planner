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
shop(p,'ring');check('potato locked as bm',ev(p,"!!document.querySelector('#shi-r-potato.hid2.bm')"),ev(p,"(document.querySelector('#shi-r-potato')||{}).textContent"))
click(p,'[data-act="shop-cat"][data-v="look"]',400);check('banana locked',ev(p,"!!document.querySelector('#shi-c-banana.hid2')"))
R.close()
seed="['2026-11-17','2026-11-18','2026-11-19'].forEach(function(d){S['days/m2_'+d]={mins:{},in:d+'T09:00:00+09:00',goals:[]};});S['days/m2_2026-11-20']={mins:{s1:71},in:'2026-11-20T09:00:00+09:00',goals:[]};var p=S['progress/m2']||{};p.shop={own:{'r:potato':30,'c:banana':60},gf:1};S['progress/m2']=p;"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999','gbb_me':'m2'},now=NOW,pre=pre(seed));close_dlg(p);p.wait_for_timeout(400)
shop(p,'ring')
check('potato opened',ev(p,"!!document.querySelector('#shi-r-potato [data-act=\"shop-use\"]')"))
check('bm condition line','병맛 히든 · 조건' in ev(p,"(document.querySelector('#shi-r-potato .hidc')||{}).textContent||''"))
click(p,'#shi-r-potato [data-act="shop-use"]',500)
check('potato ring on avatar',ev(p,"!!document.querySelector('.av.rg-potato')"))
click(p,'[data-act="shop-cat"][data-v="look"]',400)
click(p,'#shi-c-banana [data-act="shop-use"]',500)
check('banana applied',ev(p,"document.documentElement.getAttribute('data-concept')")=='banana')
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/banana.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
