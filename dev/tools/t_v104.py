# v104: 기존 꾸미기의 히든 상품
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
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre());close_dlg(p);p.wait_for_timeout(400)
shop(p,'look');check('look hidden locked',ev(p,"!!document.querySelector('#shi-c-aurora.hid2')"))
click(p,'[data-act="shop-cat"][data-v="color"]',400);check('color hidden locked',ev(p,"!!document.querySelector('#shi-a-hgold.hid2')"))
click(p,'[data-act="shop-cat"][data-v="timer"]',400);check('timer hidden locked',ev(p,"!!document.querySelector('#shi-t-neon.hid2')"))
check('hint count',ev(p,"(document.querySelector('.shdeco')||{}).textContent||''").startswith('히든 0 / 4'))
R.close()
# 하루 10시간 -> 네온 링 열림, 산 것으로 두고 쓰기
seed="S['days/m1_2026-11-18']={mins:{s1:400,s2:250},in:'2026-11-18T09:00:00+09:00',goals:[]};var p=S['progress/m1']||{};p.shop={own:{'t:neon':80},gf:1};S['progress/m1']=p;"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre(seed));close_dlg(p);p.wait_for_timeout(400)
shop(p,'timer')
check('neon opened',ev(p,"!!document.querySelector('#shi-t-neon')&&!document.querySelector('#shi-t-neon.hid2')"))
click(p,'#shi-t-neon [data-act="shop-use"]',500);click(p,'[data-act="modal-close"]',400)
click(p,'[data-tab="room"]',800)
check('neon timer face',ev(p,"!!document.querySelector('.tf.tv-neon.ring')"))
R.close()
# 누적 60시간 -> 오로라 방 꾸미기, 쓰면 data-concept
seed="['2026-11-03','2026-11-04','2026-11-05','2026-11-06','2026-11-07','2026-11-08','2026-11-09','2026-11-10','2026-11-11','2026-11-12','2026-11-13','2026-11-14'].forEach(function(d){S['days/m1_'+d]={mins:{s1:310},in:d+'T09:00:00+09:00',goals:[]};});var p=S['progress/m1']||{};p.shop={own:{'c:aurora':150},gf:1};S['progress/m1']=p;"
R=Rig();p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre(seed));close_dlg(p);p.wait_for_timeout(400)
shop(p,'look')
check('aurora opened',ev(p,"!!document.querySelector('#shi-c-aurora [data-act=\"shop-use\"]')"))
click(p,'#shi-c-aurora [data-act="shop-use"]',500)
check('concept applied',ev(p,"document.documentElement.getAttribute('data-concept')")=='aurora' and ev(p,"document.documentElement.getAttribute('data-mode')")=='dark')
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/aurora.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
