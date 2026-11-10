# v84: 학교 시간표 자습 수업 표시
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
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;var p=S['progress/m1']||{};p.tt=p.tt||{};p.tt.sch={w:{2:{p0:{s:'s1'},p1:{s:'s1'},p2:{t:'체육'}},3:{p3:{s:'s1'}}}};S['progress/m1']=p;clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now='2026-11-10T08:05:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(500)
ev(p,"(()=>{var b=document.createElement('button');b.id='xo';b.dataset.act='open';b.dataset.modal='school';document.body.appendChild(b);b.click();return 1})()");p.wait_for_timeout(600)
click(p,'[data-act="sch-sel"][data-d="2"][data-i="0"]',500)
click(p,'[data-act="sch-sj"]',600)
sch=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'].tt.sch)"))
check('saved sj',list((sch.get('sj') or {}).keys())==['s:s1'],sch.get('sj'))
check('all periods of subject marked',ev(p,"document.querySelectorAll('#dlg-school .schc.sj').length")==3,ev(p,"document.querySelectorAll('#dlg-school .schc.sj').length"))
check('summary line',('자습 수업' in ev(p,"document.querySelector('#dlg-school .sjlist').textContent")))
check('button flips',ev(p,"document.querySelector('[data-act=\"sch-sj\"]').textContent")=='자습 표시 끄기')
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/sj_modal.png')
close_dlg(p);p.wait_for_timeout(400)
check('class alert shows 자습',('자습' in ev(p,"(document.querySelector('.schnow')||{}).textContent||''")),ev(p,"(document.querySelector('.schnow')||{}).textContent||''"))
ev(p,"(()=>{var b=document.createElement('button');b.dataset.act='open';b.dataset.modal='school';document.body.appendChild(b);b.click();return 1})()");p.wait_for_timeout(500)
click(p,'[data-act="sch-sel"][data-d="2"][data-i="0"]',500);click(p,'[data-act="sch-sj"]',600)
sch=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'].tt.sch)"))
check('off',not sch.get('sj'),sch.get('sj'))
# 같은 과목 두 선생님: 선생님마다 따로
ev(p,"(()=>{var S=window.__store;var x=S['progress/m1'];x.tt.sch.w={2:{p0:{s:'s1',tc:'김'},p1:{s:'s1',tc:'김'},p4:{s:'s1',tc:'이'}},4:{p2:{s:'s1',tc:'이'}}};x.tt.sch.sj={};window.__fire&&window.__fire();return 1})()");p.wait_for_timeout(600)
click(p,'[data-act="sch-sel"][data-d="2"][data-i="4"]',500)
check('label names teacher','(이)' in ev(p,"document.querySelector('[data-act=\"sch-sj\"]').textContent"),ev(p,"document.querySelector('[data-act=\"sch-sj\"]').textContent"))
click(p,'[data-act="sch-sj"]',600)
sch=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'].tt.sch)"))
check('per-teacher key',list(sch.get('sj',{}).keys())==['s:s1|이'],sch.get('sj'))
check('only 이 periods marked',ev(p,"document.querySelectorAll('#dlg-school .schc.sj').length")==2,ev(p,"document.querySelectorAll('#dlg-school .schc.sj').length"))
check('summary shows teacher','(이)' in ev(p,"document.querySelector('#dlg-school .sjlist').textContent"))
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/sj_tc.png')
click(p,'[data-act="sch-sj"]',600)
sch=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'].tt.sch)"))
check('per-teacher off',not sch.get('sj'),sch.get('sj'))
# 예전처럼 과목 전체로 표시된 것을 한 선생님만 끄면 다른 선생님은 남음
ev(p,"(()=>{var x=window.__store['progress/m1'];x.tt.sch.sj={'s:s1':'2026-11-10'};window.__fire&&window.__fire();return 1})()");p.wait_for_timeout(600)
click(p,'[data-act="sch-sel"][data-d="2"][data-i="1"]',500)
click(p,'[data-act="sch-sj"]',600)
sch=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'].tt.sch)"))
check('whole -> other teacher kept',list(sch.get('sj',{}).keys())==['s:s1|이'],sch.get('sj'))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
