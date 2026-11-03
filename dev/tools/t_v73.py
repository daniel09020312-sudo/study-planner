# v75: 다른 기기에서 읽은 메시지는 이 기기에서도 안 읽은 수에서 빠짐(reads/<나>)
import sys,json,time
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
p=R.open(1180,900,ls={'gbb_note':'9999999999999'});close_dlg(p);p.wait_for_timeout(800)
p.evaluate("()=>{const S=window.__store,t=Date.now();S['msgs/x1']={from:'m2',to:'m1',text:'안녕',at:t-60000};S['msgs/x2']={from:'m2',to:'m1',text:'뭐해',at:t-30000};S['msgs/x3']={from:'m3',to:'all',text:'전체',at:t-20000};window.__fire();}");p.wait_for_timeout(700)
def badge():return ev(p,"(()=>{const b=document.getElementById('chatBadge');return b&&!b.hidden?b.textContent:''})()")
b0=badge();print('before',b0)
check('unread before',b0 not in ('','0'),b0)
p.evaluate("()=>{const S=window.__store,t=Date.now();S['reads/m1']={m2:t+1000,m3:t+1000,m4:t+1000,m5:t+1000,all:t+1000};window.__fire();}");p.wait_for_timeout(700)
b1=badge();print('after',b1)
check('read on other device clears badge',b1=='',b1)
p.evaluate("()=>{const S=window.__store,t=Date.now();S['msgs/x4']={from:'m2',to:'m1',text:'새 글',at:t+5000};window.__fire();}");p.wait_for_timeout(700)
check('newer message counts again',badge()=='1',badge())
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
