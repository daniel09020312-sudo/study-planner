# v85: 할 일 모음 끌어서 순서 바꾸기
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['inbox/m1']={items:{i1:{t:'가',sid:'s1',at:1},i2:{t:'나',sid:'s1',at:2},i3:{t:'다',sid:'s1',at:3},i4:{t:'라',sid:'s2',at:4}}};clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_ibview':'at'},now='2026-11-14T10:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="cal"]',600);click(p,'[data-act="open"][data-modal="inbox"]',600)
order=lambda:ev(p,"[...document.querySelectorAll('#dlg-inbox .ibrow .ibpick b')].map(e=>e.textContent)")
def drag(src,dst,after=False):
    a=p.locator('#dlg-inbox .ibrow[data-id="%s"] .ibh'%src).bounding_box();b=p.locator('#dlg-inbox .ibrow[data-id="%s"]'%dst).bounding_box()
    p.mouse.move(a['x']+a['width']/2,a['y']+a['height']/2);p.mouse.down()
    ty=b['y']+(b['height']*0.8 if after else b['height']*0.2)
    for k in range(1,9):p.mouse.move(a['x']+a['width']/2,a['y']+(ty-a['y'])*k/8);p.wait_for_timeout(30)
    p.mouse.up();p.wait_for_timeout(600)
check('initial',order()==['가','나','다','라'],order())
drag('i3','i1')
check('move 다 to top',order()==['다','가','나','라'],order())
drag('i3','i4',True)
check('move 다 to bottom',order()==['가','나','라','다'],order())
st=json.loads(ev(p,"JSON.stringify(window.__store['inbox/m1'].items)"))
check('o saved',[st[k].get('o') for k in ['i1','i2','i4','i3']]==[1,2,3,4],st)
click(p,'[data-act="ib-sel"][data-id="i1"]',300);click(p,'[data-act="ib-sel"][data-id="i2"]',300)
drag('i1','i3',True)
check('multi drag',order()==['라','다','가','나'],order())
# 과목별 보기에서도 같은 과목 안 순서 반영
click(p,'[data-act="ib-view"][data-v="sub"]',400)
check('grouped keeps order',order()==['다','가','나','라'],order())
# 새로 적은 것은 맨 뒤
ev(p,"(()=>{var i=document.getElementById('ibText');i.value='마';i.dispatchEvent(new Event('input',{bubbles:true}));return 1})()")
click(p,'[data-act="ib-add"]',500);click(p,'[data-act="ib-view"][data-v="at"]',400)
check('new item last',order()[-1]=='마',order())
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/ibdrag.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
