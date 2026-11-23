# v108: 전체 순위(이름 없이) 카드
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_me':'m2'},now=datetime.datetime(2026,11,23,15,0,0));close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="rank"]',700);click(p,'[data-act="range"][data-id="all"]',800)
check('card shown',ev(p,"!!document.getElementById('c-fin-anon')"))
names=ev(p,"(JSON.parse(JSON.stringify(window.__store['meta/config'])).roster||[]).map(m=>m.name)")
txt=ev(p,"document.getElementById('c-fin-anon').textContent")
n=ev(p,"document.querySelectorAll('#c-fin-anon .fanr').length")
check('one row per person',n==len(names),(n,len(names)))
check('no names in card',not any(nm in txt for nm in names),[nm for nm in names if nm in txt])
check('my row marked',ev(p,"!!document.querySelector('#fan-me .tag')"))
check('has score and time',ev(p,"!!document.querySelector('#c-fin-anon .fanr strong')&&!!document.querySelector('#c-fin-anon .fant')"))
el=p.query_selector('#c-fin-anon');el.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/fanon.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
