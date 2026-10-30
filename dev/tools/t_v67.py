# v67: 공부 항목은 사람마다. 같은 이름은 하나만, 남이 만든 새 항목은 안 보임, 예전 항목 빼기는 나에게서만
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
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['meta/config'].migItems2=1;S['subjects/s2'].items=[{id:'a',label:'개념'},{id:'b',label:'고쟁이'},{id:'c',label:'고쟁이'},{id:'d',label:'고쟁이'},{id:'e',label:'쎈'},{id:'f',label:'블랙라벨',by:'m2'}];S['progress/m2']=Object.assign({},S['progress/m2']||{},{checks:{'s2__c':true}});clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(1000)
click(p,'[data-act="tab"][data-tab="prog"]',700);click(p,'[data-act="prog-mode"][data-id="me"]',700)
def labels():return ev(p,"(()=>{const c=[...document.querySelectorAll('.card')].find(e=>e.textContent.includes('미적분Ⅰ'));return c?[...c.querySelectorAll('.uck')].map(b=>b.textContent.trim()):[]})()")
L=labels()
check('dedupe and hide others new item',L.count('고쟁이')==1 and '블랙라벨' not in L and '개념' in L and '쎈' in L,L)
# 쎈 빼기(예전 항목 -> 나에게서만)
click(p,'[data-act="prog-edit"]',600)
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='item-del';b.dataset.id='s2';b.dataset.item='e';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(600)
check('legacy item hidden only for me',any(i['id']=='e' for i in store(p,'subjects/s2')['items']) and (store(p,'progress/m1') or {}).get('ihide',{}).get('s2__e')==True)
# 새 항목 추가 -> by m1, 같은 이름은 막음
p.evaluate("()=>{}")
click(p,'[data-act="prog-edit"]',600)
click(p,'[data-act="tab"][data-tab="prog"]',500)
click(p,'[data-act="prog-edit"]',600)
p.evaluate("()=>{const b=document.querySelector('[data-act=\"prog-toggle\"][data-id=\"s2\"]');if(b&&b.getAttribute('aria-expanded')!=='true')b.click();}");p.wait_for_timeout(600)
inp=ev(p,"!!document.querySelector('[data-draft=\"item:s2\"]')")
if inp:
    p.fill('[data-draft="item:s2"]','마플');p.wait_for_timeout(200)
    p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='item-add';b.dataset.id='s2';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(600)
    it=[i for i in store(p,'subjects/s2')['items'] if i['label']=='마플']
    check('new item owned by me',len(it)==1 and it[0].get('by')=='m1',it)
    p.fill('[data-draft="item:s2"]','고쟁이');p.wait_for_timeout(200)
    p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='item-add';b.dataset.id='s2';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(600)
    check('no duplicate add',len([i for i in store(p,'subjects/s2')['items'] if i['label']=='고쟁이'])==3)
else: check('item input found',False)
# 내가 만든 항목 삭제 -> 문서에서 지움
mid=[i for i in store(p,'subjects/s2')['items'] if i['label']=='마플'][0]['id']
p.evaluate("(m)=>{const b=document.createElement('button');b.dataset.act='item-del';b.dataset.id='s2';b.dataset.item=m;document.body.appendChild(b);b.click();b.remove();}",mid);p.wait_for_timeout(600)
check('own item deleted',not any(i['label']=='마플' for i in store(p,'subjects/s2')['items']))
# 기본 항목으로
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='item-reset';b.dataset.id='s2';document.body.appendChild(b);b.click();b.click();b.remove();}");p.wait_for_timeout(800)
click(p,'[data-act="prog-edit"]',600)
click(p,'[data-act="prog-mode"][data-id="me"]',600)
L2=labels()
hd=(store(p,'progress/m1') or {}).get('ihide',{})
check('reset to default items',len(L2)==5 and all(hd.get('s2__'+k) for k in 'abcde'),(L2,hd))
check('friends items untouched',sum(1 for i in store(p,'subjects/s2')['items'] if i['label']=='고쟁이')==3 and any(i['label']=='블랙라벨' for i in store(p,'subjects/s2')['items']))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
