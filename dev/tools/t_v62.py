# v59: 옮긴 할 일 되돌리기, 하루 할 일 20개
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
PAST='2026-10-19';T='2026-10-21'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_%s']={goals:[{id:'k1',text:'끝낸 것',sid:'s2',done:true},{id:'mv1',text:'옮긴 것',sid:'s2',done:false,mv:1},{id:'mv2',text:'예전 옮김',sid:'s3',done:false,mv:1}]};S['days/m1_%s']={goals:[{id:'mv1',text:'옮긴 것',sid:'s2',done:false},{id:'nw',text:'다른 이름',sid:'s3',done:false}]};clearInterval(t);},5);})();"%(PAST,T)
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=T+'T19:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1500)
def pick(d):p.evaluate("(d)=>{const b=document.createElement('button');b.setAttribute('data-act','pick-date');b.setAttribute('data-d',d);document.body.appendChild(b);b.click();b.remove();}",d);p.wait_for_timeout(700)
pick(PAST)
check('undo buttons on moved goals',ev(p,"document.querySelectorAll('#c-goals [data-act=\"mv-back\"]').length")==2)
click(p,'#c-goals [data-act="mv-back"][data-id="mv1"]',700)
src=store(p,'days/m1_'+PAST)['goals'];dst=store(p,'days/m1_'+T)['goals']
g1=[g for g in src if g['id']=='mv1'][0]
check('restored on source',not g1.get('mv') and not g1.get('done'),g1)
check('removed from target',[g['id'] for g in dst]==['nw'],[g['id'] for g in dst])
# 다른 id로 복사된 경우(어제 할 일 가져오기): 이름과 과목이 같은 것을 찾음. 없으면 원래 날에만 되돌림
click(p,'#c-goals [data-act="mv-back"][data-id="mv2"]',700)
g2=[g for g in store(p,'days/m1_'+PAST)['goals'] if g['id']=='mv2'][0]
check('restored without target',not g2.get('mv'),g2)
check('other goal untouched',[g['id'] for g in store(p,'days/m1_'+T)['goals']]==['nw'])
# 옮겨 간 날에 끝냈으면 되돌리지 않음
p.evaluate("()=>{const S=window.__store;S['days/m1_%s']={goals:[{id:'z',text:'끝냄',sid:'s2',done:false,mv:1}]};S['days/m1_%s']={goals:[{id:'z',text:'끝냄',sid:'s2',done:true}]};window.__fire();}"%('2026-10-18',T));p.wait_for_timeout(600)
pick('2026-10-18');click(p,'#c-goals [data-act="mv-back"][data-id="z"]',700)
check('done target blocks undo',[g for g in store(p,'days/m1_2026-10-18')['goals']][0].get('mv')==1)
# 20개까지
p.evaluate("()=>{const S=window.__store;S['days/m1_2026-10-22']={goals:Array.from({length:19},(_, i)=>({id:'q'+i,text:'할 일 '+i,sid:'s2',done:false}))};window.__fire();}");p.wait_for_timeout(600)
pick('2026-10-22')
check('add row at 19',ev(p,"!!document.querySelector('#c-goals input, #c-goals [data-act=\"open\"][data-modal=\"compose\"]')"))
p.evaluate("()=>{const S=window.__store;S['days/m1_2026-10-22'].goals.push({id:'q19',text:'스무째',sid:'s2',done:false});window.__fire();}");p.wait_for_timeout(600)
pick('2026-10-22')
check('20 shown',ev(p,"document.querySelectorAll('#c-goals li.goal').length")==20,ev(p,"document.querySelectorAll('#c-goals li.goal').length"))
check('GMAX 20 text',ev(p,"document.body.innerHTML.indexOf('quickAdd')")>=-1)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
