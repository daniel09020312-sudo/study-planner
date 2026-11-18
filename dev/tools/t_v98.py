import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,11,20,12,0,0)
SEED="(m)=>{const S=window.__store;S['days/m1_2026-11-10']={goals:[],mins:{s2:m},in:'2026-11-10T00:10:00.000Z'};window.__fire();}"
def HAS(p):
    p.evaluate("()=>{const b=document.querySelector('[data-act=\"tab\"][data-tab=\"play\"]');if(b)b.click();}");p.wait_for_timeout(500)
    p.evaluate("()=>{const b=document.querySelector('[data-act=\"play-tab\"][data-id=\"badge\"]');if(b)b.click();}");p.wait_for_timeout(600)
    return st(p,"!!document.querySelector('#c-badges')&&document.querySelector('#c-badges').textContent.includes('하루 18시간')")
R=Rig()
p=R.open(1280,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate(SEED,1000);p.wait_for_timeout(1500)
check('17h: no modal',not st(p,"!!document.querySelector('#dlg-h18')"))
check('17h: hidden badge not listed',HAS(p) is False and st(p,"!!document.querySelector('#c-badges')"))
q=R.open(1280,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(q)
q.evaluate(SEED,1090);q.wait_for_timeout(1800)
check('18h: modal shows',st(q,"!!document.querySelector('#dlg-h18')"))
click(q,'#dlg-h18 [data-act="h18-use"]',900)
check('closed and remembered',st(q,"!document.querySelector('#dlg-h18')") and st(q,"!!localStorage.getItem('gbb_h18')"))
check('title set',st(q,"window.__store['progress/m1']&&window.__store['progress/m1'].title")=='d18',st(q,"JSON.stringify(window.__store['progress/m1']||{}).slice(0,200)"))
check('18h: badge listed',HAS(q) is True)
check('title in use',st(q,"document.querySelector('#c-badges').textContent.includes('칭호 사용 중')"))
check('no points',st(q,"document.querySelector('#c-badges .bdg.t-h').textContent.includes('+0점')"))
q.wait_for_timeout(1200)
check('not shown again',st(q,"!document.querySelector('#dlg-h18')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
