# v100: 지금까지 총점은 방장만
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
R=Rig()
adm=None
for me in ['m1','m2']:
    p=R.open(1180,820,ls={'gbb_note':'9999999999999'},me=me,now=NOW);close_dlg(p)
    a=st(p,"(()=>{const c=window.__store['meta/config']||{};return c.admin||((c.roster||[])[0]||{}).id})()")
    click(p,'[data-act="tab"][data-tab="rank"]',700);click(p,'[data-act="range"][data-id="all"]',800)
    has=st(p,"!!document.querySelector('#c-fin-now')")
    n=st(p,"document.querySelectorAll('#c-fin-now .frr').length")
    if me==a: check('admin %s sees totals'%me,has and n>=2,n)
    else: check('member %s does not see totals'%me,not has and st(p,"!!document.querySelector('#c-fin-wait')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
