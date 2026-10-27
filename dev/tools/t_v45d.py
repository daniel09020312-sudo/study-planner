import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,28,10,0,0)
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("()=>{const S=window.__store;S['msgs/y1']={from:'m2',to:'all',text:'남이 쓴 글',at:Date.now()-1000};S['msgs/y3']={from:'m1',to:'all',text:'내가 쓴 글',at:Date.now()-800};window.__fire();}")
click(p,'[data-act="tab"][data-tab="chat"]',800)
n0=st(p,"(document.querySelector('#m-y1 .urd')||{}).textContent")
p.evaluate("()=>{const S=window.__store;const c=S['meta/config'];c.roster=c.roster.concat([{id:'m9',name:'새친구'}]);window.__fire();}");p.wait_for_timeout(600)
n1=st(p,"(document.querySelector('#m-y1 .urd')||{}).textContent")
check('late joiner counted',int(n1)==int(n0)+1,(n0,n1))
for id in ['y1','y3']:
    r=st(p,"(()=>{const u=document.querySelector('#m-%s .urd'),t=document.querySelector('#m-%s .mt')||document.querySelector('#m-%s .mfoot.o small');const a=u.getBoundingClientRect(),b=t.getBoundingClientRect();return [a.top,a.bottom,b.top,b.bottom]})()"%(id,id,id))
    check('same y '+id,abs((r[0]+r[1])/2-(r[2]+r[3])/2)<3,r)
check('no Enter in placeholder',True)
click(p,'[data-act="tab"][data-tab="cal"]',700)
ph=st(p,"(document.querySelector('.qadd input')||{}).placeholder")
check('placeholder',ph and 'Enter' not in ph,ph)
print('errors',R.errors);R.close();print('ALL OK' if ok else 'SOME FAILED')
