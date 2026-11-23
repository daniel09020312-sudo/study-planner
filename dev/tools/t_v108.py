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
for ls in [{'gbb_note':'9999999999999','gbb_me':'m2'},{'gbb_note':'9999999999999'}]:
    q=R.open(1180,900,ls=ls,now=datetime.datetime(2026,11,23,15,0,0));close_dlg(q);q.wait_for_timeout(500)
    click(q,'[data-act="tab"][data-tab="rank"]',700);click(q,'[data-act="range"][data-id="all"]',800)
    check('hidden without code '+ls.get('gbb_me','m1'),ev(q,"!document.getElementById('c-fin-anon')"))
    R.close();R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_me':'m2','gbb_adm':'x'},now=datetime.datetime(2026,11,23,15,0,0));close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="rank"]',700);click(p,'[data-act="range"][data-id="all"]',800)
check('card shown',ev(p,"!!document.getElementById('c-fin-anon')"))
names=ev(p,"(JSON.parse(JSON.stringify(window.__store['meta/config'])).roster||[]).map(m=>m.name)")
txt=ev(p,"document.getElementById('c-fin-anon').textContent")
n=ev(p,"document.querySelectorAll('#c-fin-anon .fanr').length")
check('one row per person',n==len(names),(n,len(names)))
check('no names in card',not any(nm in txt for nm in names),[nm for nm in names if nm in txt])
check('no me mark',ev(p,"!document.querySelector('#fan-me')&&!document.querySelector('#c-fin-anon .fanr.me')"))
check('has score and time',ev(p,"!!document.querySelector('#c-fin-anon .fanr strong')&&!!document.querySelector('#c-fin-anon .fant')"))
el=p.query_selector('#c-fin-anon');el.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/fanon.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
# 50명도 한 카드에 모두(안쪽 스크롤 없음)
R=Rig()
pre="(function(){var t=setInterval(function(){var S=window.__store;if(!S||!S['meta/config'])return;var c=S['meta/config'];for(var i=0;i<45;i++)c.roster.push({id:'z'+i,name:'가짜'+i});clearInterval(t);},2);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_me':'m2','gbb_adm':'x'},now=datetime.datetime(2026,11,23,15,0,0),pre=pre);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="rank"]',700);click(p,'[data-act="range"][data-id="all"]',800)
tot=ev(p,"(JSON.parse(JSON.stringify(window.__store['meta/config'])).roster||[]).length")
n=ev(p,"document.querySelectorAll('#c-fin-anon .fanr').length")
check('all members (50)',n==tot and tot>=50,(n,tot))
check('no inner scroll',ev(p,"(function(e){return e.scrollHeight<=e.clientHeight+1})(document.querySelector('#c-fin-anon .fanl'))"))
check('no names (50)',not ev(p,"document.getElementById('c-fin-anon').textContent.includes('가짜')"))
p.query_selector('#c-fin-anon').screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/fanon50.png')
R.close();print('ALL OK' if ok else 'SOME FAILED')
