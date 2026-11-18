import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
R=Rig()
for (h,m,exp) in [(2,30,'2026-11-19'),(4,59,'2026-11-19'),(5,0,'2026-11-20'),(23,50,'2026-11-20')]:
    p=R.open(1280,900,ls={'gbb_note':'9999999999999','gbb_test':'1'},now=datetime.datetime(2026,11,20,h,m,0));close_dlg(p)
    t=st(p,"__gbb.today()")
    check('today at %02d:%02d'%(h,m),t==exp,t)
# 새벽 2시에 공부한 시간은 전날 기록
p=R.open(1280,900,ls={'gbb_note':'9999999999999','gbb_test':'1'},now=datetime.datetime(2026,11,20,2,0,0));close_dlg(p)
G="(d)=>+((window.__store['days/m1_'+d]||{}).mins||{}).s2||0"
b19=p.evaluate(G,'2026-11-19');b20=p.evaluate(G,'2026-11-20')
p.evaluate("()=>{__gbb.editDay(__gbb.today(),function(d){d.mins.s2=(+d.mins.s2||0)+30;});}");p.wait_for_timeout(800)
a19=p.evaluate(G,'2026-11-19');a20=p.evaluate(G,'2026-11-20')
check('2am minutes go to previous day',a19-b19==30 and a20==b20,(b19,a19,b20,a20))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
