# v88: 할 일 모음 크게 보기
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
items={}
k=0
for s,n in [('s1',6),('s2',4),('s3',7),('s4',3),('s5',5),('',2)]:
    for i in range(n):
        k+=1;items['i%d'%k]={'t':'할 일 %s-%d 문제집 풀기'%(s or '없음',i+1),'at':k}
        if s: items['i%d'%k]['sid']=s
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['inbox/m1']={items:%s};clearInterval(t);},5);})();"%json.dumps(items)
p=R.open(1366,1024,ls={'gbb_note':'9999999999999'},now='2026-11-14T10:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="cal"]',600);click(p,'[data-act="open"][data-modal="inbox"]',600)
check('small by default',not ev(p,"document.getElementById('dlg-inbox').classList.contains('ibbig')"))
click(p,'[data-act="ib-big"]',600)
check('big class',ev(p,"document.getElementById('dlg-inbox').classList.contains('ibbig')"))
w=ev(p,"document.getElementById('dlg-inbox').getBoundingClientRect().width")
check('full width',w>1300,w)
check('6 columns',ev(p,"document.querySelectorAll('#dlg-inbox .ibcol').length")==6)
check('all rows',ev(p,"document.querySelectorAll('#dlg-inbox .ibrow').length")==27)
cols=ev(p,"new Set([...document.querySelectorAll('#dlg-inbox .ibcol')].map(e=>Math.round(e.getBoundingClientRect().top))).size")
check('columns side by side',cols<=2,cols)
check('pref saved',ev(p,"localStorage.getItem('gbb_ibbig')")=='1')
click(p,'#dlg-inbox .ibcol:nth-child(3) [data-act="ib-selsub"]',400)
check('select subject in column',ev(p,"document.querySelectorAll('#dlg-inbox .ibrow.on').length")==7)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/ibbig.png')
click(p,'[data-act="ib-view"][data-v="at"]',400)
check('flow grid when by time',ev(p,"!!document.querySelector('#dlg-inbox .iblist.ibflow')"))
click(p,'[data-act="ib-view"][data-v="sub"]',400)
click(p,'[data-act="ib-big"]',500)
check('back to small',not ev(p,"document.getElementById('dlg-inbox').classList.contains('ibbig')") and not ev(p,"!!document.querySelector('#dlg-inbox .ibcols')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close()
# 휴대폰
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_ibbig':'1'},now='2026-11-14T10:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(500)
ev(p,"(()=>{var b=document.createElement('button');b.dataset.act='open';b.dataset.modal='inbox';document.body.appendChild(b);b.click();return 1})()");p.wait_for_timeout(700)
check('phone big one column',ev(p,"new Set([...document.querySelectorAll('#dlg-inbox .ibcol')].map(e=>Math.round(e.getBoundingClientRect().left))).size")==1)
check('no horizontal overflow',ev(p,"document.querySelector('#dlg-inbox .db').scrollWidth<=document.querySelector('#dlg-inbox .db').clientWidth+1"))
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/ibbig_phone.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
