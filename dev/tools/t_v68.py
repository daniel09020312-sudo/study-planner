# v69: 미적분Ⅰ·확률과 통계 항목을 모두 기본으로(한 번), 교양 과목은 진도·퍼센트 없이
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
def store(p,k):return json.loads(ev(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['subjects/s2'].items=[{id:'a',label:'개념'},{id:'b',label:'고쟁이'},{id:'k',label:'개념 정리',by:'m1'},{id:'f',label:'블랙라벨',by:'m2'}];S['subjects/s3'].items=[{id:'x',label:'올포고'},{id:'i3',label:'문제집 풀이'}];S['progress/m1']=Object.assign({},S['progress/m1']||{},{checks:{'s2__k':true,'s3__i3':true},ihide:{'s2__a':true}});clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(2500)
DEF=['개념 정리','교과서와 프린트 복습','문제집 풀이','기출 풀이','오답 정리']
i2=store(p,'subjects/s2')['items'];i3=store(p,'subjects/s3')['items']
check('calc items reset for all',[i['label'] for i in i2]==DEF and i2[0]['id']=='k' and not any(i.get('by') for i in i2),i2)
check('prob items reset, kept checked id',[i['label'] for i in i3]==DEF and i3[2]['id']=='i3',i3)
check('migration flag',(store(p,'meta/config') or {}).get('migItems2')==1)
# 교양 과목
click(p,'[data-act="tab"][data-tab="prog"]',700);click(p,'[data-act="prog-mode"][data-id="me"]',700)
lib=ev(p,"(()=>{const c=document.querySelector('.usub.ulib');return c?c.innerText:''})()")
check('humanities card without percent','후마니타스' in lib and '시험 없음' in lib and '%' not in lib,lib)
click(p,'[data-act="prog-mode"][data-id="all"]',700)
rows=ev(p,"[...document.querySelectorAll('.prow .pnm b')].map(e=>e.textContent)")
check('no humanities row in compare','후마니타스' not in rows and '교양 과목' in ev(p,"document.querySelector('#c-pall').innerText"),rows)
# 다른 과목을 교양으로
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='sub-lib';b.dataset.id='s8';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(600)
check('toggle lib',store(p,'subjects/s8').get('lib')==True)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
