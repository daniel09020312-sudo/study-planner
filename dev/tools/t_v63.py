# v60: 과목은 사람마다. 다른 사람이 만든 과목은 내게 안 생김, 같은 이름이면 함께 씀, 비교는 그 과목 가진 사람끼리
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
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['subjects/s9']={name:'일본어',order:9,by:'m2',items:[{id:'i1',label:'개념'}]};clearInterval(t);},5);})();"
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(1000)
def goprog(mode):
    click(p,'[data-act="tab"][data-tab="prog"]',700);click(p,'[data-act="prog-mode"][data-id="%s"]'%mode,700)
goprog('me')
txt=ev(p,"document.querySelector('#view-prog').innerText")
check('other person subject not in my list',('일본어 다시 넣기' in txt or '일본어' in ev(p,"[...document.querySelectorAll('#c-uoff .chip')].map(e=>e.textContent).join(',')")) and '일본어' not in ev(p,"[...document.querySelectorAll('#view-prog section.card:not(#c-uoff) h2')].map(e=>e.textContent).join(',')"))
goprog('all')
rows=ev(p,"[...document.querySelectorAll('.prow .pnm b')].map(e=>e.textContent)")
check('compare rows only my subjects',('일본어' not in rows) and '미적분Ⅰ' in rows,rows)
# 다른 사람이 과목을 빼면 그 과목 비교에서 빠짐
p.evaluate("()=>{const S=window.__store;S['progress/m3']=Object.assign({},S['progress/m3']||{},{skip:{s2:true}});window.__fire();}");p.wait_for_timeout(600)
goprog('all')
cnt=ev(p,"(()=>{const r=[...document.querySelectorAll('.prow')].find(e=>e.querySelector('.pnm b').textContent==='미적분Ⅰ');return r?r.querySelector('.pnm small').textContent:''})()")
check('compare excludes people without the subject','4명' in cnt and '제외 1명' in cnt,cnt)
# 같은 이름으로 추가하면 그 과목을 함께 씀
click(p,'[data-act="prog-edit"]',600)
p.fill('[data-draft="subName"]','일본어');p.wait_for_timeout(200);click(p,'[data-act="sub-add"]',700)
check('join same-name subject',(store(p,'progress/m1') or {}).get('suse',{}).get('s9')==True and len([1 for k,v in json.loads(ev(p,"JSON.stringify(window.__store)")).items() if k.startswith('subjects/') and (v or {}).get('name')=='일본어'])==1,store(p,'progress/m1'))
# 새 이름은 만든 사람(by) 적어 만들고, 다른 사람에게는 안 보임
p.fill('[data-draft="subName"]','중국어');p.wait_for_timeout(200);click(p,'[data-act="sub-add"]',700)
new=[ (k,v) for k,v in json.loads(ev(p,"JSON.stringify(window.__store)")).items() if k.startswith('subjects/') and (v or {}).get('name')=='중국어']
check('new subject has by=m1',len(new)==1 and new[0][1].get('by')=='m1',new)
# 모두가 가진 예전 과목 삭제 -> 내 과목에서만 빠짐
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='sub-del';b.dataset.id='s8';document.body.appendChild(b);b.click();b.click();b.remove();}");p.wait_for_timeout(700)
check('shared subject kept, skipped for me',store(p,'subjects/s8') is not None and (store(p,'progress/m1') or {}).get('skip',{}).get('s8')==True)
# 나만 가진 과목 삭제 -> 지워짐
sid=new[0][0].split('/')[1]
p.evaluate("(id)=>{const b=document.createElement('button');b.dataset.act='sub-del';b.dataset.id=id;document.body.appendChild(b);b.click();b.click();b.remove();}",sid);p.wait_for_timeout(700)
check('own-only subject deleted',store(p,'subjects/'+sid) is None)
# 다시 넣기
click(p,'[data-act="prog-edit"]',600)
goprog('me')
click(p,'#c-uoff [data-act="skip"][data-id="s8"]',600)
check('re-add',not (store(p,'progress/m1') or {}).get('skip',{}).get('s8') and (store(p,'progress/m1') or {}).get('suse',{}).get('s8')==True)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
