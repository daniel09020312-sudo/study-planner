# v109 화이트보드: 쓰기, 다른 사람에게 보임, 지우개, 되돌리기, 방장 모두 지우기
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
SC='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/'
NOW=datetime.datetime(2026,11,24,15,0,0)
R=Rig();p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="board"]',700)
check('card',ev(p,"!!document.getElementById('c-wb')"))
click(p,'#c-wb .btn[data-act="wb-open"]',600)
check('dock open',ev(p,"!!document.getElementById('wbDock')"))
st=p.query_selector('#wbStage').bounding_box()
def line(x0,y0,x1,y1,n=12):
    p.mouse.move(st['x']+x0,st['y']+y0);p.mouse.down()
    for i in range(1,n+1):p.mouse.move(st['x']+x0+(x1-x0)*i/n,st['y']+y0+(y1-y0)*i/n)
    p.mouse.up();p.wait_for_timeout(250)
def cnt():return ev(p,"Object.keys(window.__store).filter(k=>k.indexOf('wb/')===0&&window.__store[k]).length")
line(100,100,400,200)
click(p,'[data-w="color"][data-v="#E5484D"]',100);line(100,300,500,320)
click(p,'[data-w="tool"][data-v="h"]',100);line(150,400,600,400)
p.wait_for_timeout(600)
check('3 strokes saved',cnt()==3,cnt())
d=ev(p,"Object.keys(window.__store).filter(k=>k.indexOf('wb/')===0).map(k=>window.__store[k])")
check('stroke data',all(x.get('by')=='m1' and len(x['p'].split(','))>=4 for x in d),d[0])
check('highlighter kind',any(x.get('k')=='h' for x in d))
p.screenshot(path=SC+'wb1.png')
click(p,'[data-w="undo"]',500);check('undo removes',cnt()==2,cnt())
click(p,'[data-w="tool"][data-v="e"]',100);line(300,290,300,340,4);p.wait_for_timeout(500)
check('eraser removes red',cnt()==1,cnt())
click(p,'[data-w="undo"]',500);check('undo erase restores',cnt()==2,cnt())
# 확대, 전체 보기
z0=ev(p,"document.getElementById('wbZ').textContent");click(p,'[data-w="zin"]',300)
check('zoom in',ev(p,"document.getElementById('wbZ').textContent")!=z0)
click(p,'[data-w="all"]',200);za=ev(p,"document.getElementById('wbZ').textContent");check('whole board small',int(za[:-1])<20,za)
click(p,'[data-w="fit"]',200);check('fit content',ev(p,"document.getElementById('wbZ').textContent")!=za)
# 숫자 키가 탭을 바꾸지 않음
p.keyboard.press("Digit1");p.wait_for_timeout(300);check("keys blocked",ev(p,"!!document.getElementById('wbDock')&&!!document.querySelector('[data-tab=board][aria-current]')"))
# 방장 모두 지우기(두 번)
click(p,'[data-w="clear"]',200);check('clear needs twice',cnt()==2)
click(p,'[data-w="clear"]',600);check('cleared',cnt()==0,cnt())
p.keyboard.press('Escape');p.wait_for_timeout(300);check('esc closes',ev(p,"!document.getElementById('wbDock')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close()
# 다른 사람(m2) 판에 m1이 쓴 획이 보이고, m2는 모두 지우기 없음, 지우개로 지움
pre="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['wb/wa1']={by:'m1',c:'#0090FF',w:6,k:'p',p:'200,200,900,600,1500,300',at:Date.now()-5000};clearInterval(t);},2);})();"
R=Rig();p=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_me':'m2'},now=NOW,pre=pre);close_dlg(p);p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="board"]',700)
p.evaluate("()=>document.getElementById('c-wb').scrollIntoView()");p.wait_for_timeout(300)
check('preview img',ev(p,"!!document.querySelector('#c-wb .wbprev img')"))
check('card names drawer',ev(p,"document.getElementById('c-wb').textContent.includes('마지막')"))
click(p,'#c-wb .btn[data-act="wb-open"]',600)
check('no clear for non-owner',ev(p,"!document.querySelector('[data-w=clear]')"))
check('info 1 stroke',ev(p,"document.getElementById('wbInfo').textContent").find('1획')>=0)
p.screenshot(path=SC+'wb2.png')
print('errors',R.errors);check('no errors 2',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
