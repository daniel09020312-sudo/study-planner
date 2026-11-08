# v82: 할 일 모음 과목별 정리
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
T='2026-11-08'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['inbox/m1']={items:{i1:{t:'가',sid:'s3',at:1},i2:{t:'나',sid:'s1',at:2},i3:{t:'다',at:3},i4:{t:'라',sid:'s3',at:4},i5:{t:'마',sid:'s1',at:5}}};clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=T+'T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',700);click(p,'[data-act="open"][data-modal="inbox"]',700)
rows=lambda:ev(p,"[...document.querySelectorAll('#dlg-inbox .iblist > li')].map(e=>e.classList.contains('ibgrp')?'#'+e.querySelector('b').textContent:e.querySelector('.ibpick b').textContent)")
r=rows();print(r)
check('grouped by subject order, no-subject last',[x for x in r if not x.startswith('#')]==['나','마','가','라','다'] and r[-2]=='#과목 없음',r)
check('no chip row in grouped mode',ev(p,"!document.querySelector('#dlg-inbox .ibsubs')"))
click(p,'#dlg-inbox .ibgrp:nth-child(4) [data-act="ib-selsub"]',400)
check('select group',ev(p,"document.querySelectorAll('#dlg-inbox .ibrow.on').length")==2)
check('group button turns to 풀기',ev(p,"document.querySelector('#dlg-inbox .ibgrp:nth-child(4) .linkbtn').textContent")=='풀기')
click(p,'#dlg-inbox .ibgrp:nth-child(4) [data-act="ib-selsub"]',400)
check('unselect group',ev(p,"document.querySelectorAll('#dlg-inbox .ibrow.on').length")==0)
click(p,'[data-act="ib-view"][data-v="at"]',400)
check('written order view',[x for x in rows()]==['가','나','다','라','마'],rows())
check('pref saved',ev(p,"localStorage.getItem('gbb_ibview')")=='at')
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/ib_at.png')
click(p,'[data-act="ib-view"][data-v="sub"]',400)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/ib_sub.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
