import sys,datetime
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
p.evaluate("()=>{const S=window.__store;S['msgs/y1']={from:'m2',to:'all',text:'남이 쓴 글',at:Date.now()-1000};S['msgs/y2']={from:'m2',to:'m1',text:'귓속말',at:Date.now()-900};window.__fire();}")
click(p,'[data-act="tab"][data-tab="chat"]',800)
t=st(p,"(document.querySelector('#m-y1 .urd')||{}).textContent")
check('other msg unread count (roster-2)',t=='3',t)
click(p,'[data-act="chan"][data-id="m2"]',600)
check('dm from other: none',not st(p,"!!document.querySelector('#m-y2 .urd')"))
# 패드: 폭 650, 터치
q=R.open(650,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(q)
q.evaluate("()=>document.documentElement.classList.add('pad')");q.wait_for_timeout(200)
vis=st(q,"[...document.querySelectorAll('.navs > button')].filter(b=>getComputedStyle(b).display!=='none').map(b=>b.dataset.tab||b.id)")
check('pad shows all tabs, no more',len(vis)==8 and 'navMore' not in vis,vis)
r=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(r)
vis=st(r,"[...document.querySelectorAll('.navs > button')].filter(b=>getComputedStyle(b).display!=='none').map(b=>b.dataset.tab||b.id)")
check('phone keeps more',vis==['cal','room','chat','navMore'],vis)
print('errors',R.errors);check('no errors',not R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
