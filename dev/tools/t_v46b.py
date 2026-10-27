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
pre="""window.__nt=[];window.Notification=function(t,o){window.__nt.push([t,o&&o.body]);};Notification.permission='granted';Notification.requestPermission=function(){return Promise.resolve('granted');};"""
p=R.open(390,844,ls={'gbb_note':str(int(NOW.timestamp()*1000)-86400000*30),'gbb_pokenote':'1'},now=NOW,pre=pre);close_dlg(p)
check('hide-ms extended',st(p,"window.__SSE_HIDE_MS")==15*60000,st(p,"window.__SSE_HIDE_MS"))
p.evaluate("()=>{Object.defineProperty(document,'visibilityState',{get:()=>'hidden',configurable:true});const S=window.__store;S['msgs/pk1']={from:'m2',to:'m1',poke:true,text:'',at:Date.now()};window.__fire();}");p.wait_for_timeout(800)
n=st(p,"window.__nt")
check('notification fired on poke',len(n)==1 and '찔렀' in n[0][0],n)
p.evaluate("()=>{Object.defineProperty(document,'visibilityState',{get:()=>'visible',configurable:true});const S=window.__store;S['msgs/pk2']={from:'m3',to:'m1',poke:true,text:'',at:Date.now()};window.__fire();}");p.wait_for_timeout(800)
check('no system notification while visible',len(st(p,"window.__nt"))==1)
click(p,'#meBtn',600)
check('settings toggle',st(p,"!!document.querySelector('[data-act=\"pn-toggle\"]')"))
click(p,'[data-act="pn-toggle"]',400)
check('toggle off',st(p,"localStorage.getItem('gbb_pokenote')")is None,st(p,"localStorage.getItem('gbb_pokenote')"))
print('errors',R.errors);check('no errors',not R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
