# v78: 잉크 뿌리기 새 방식(행운 봉투·퀴즈·마감 추첨·모여라·공부왕), 결과는 열어 볼 때까지 숨김
import sys,json,time
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
def gifts(p):return {k[6:]:v for k,v in json.loads(ev(p,"JSON.stringify(window.__store)")).items() if k.startswith('gifts/')}
def ink(p):
    p.evaluate("()=>document.getElementById('shopBtn').click()");p.wait_for_timeout(600)
    t=ev(p,"(document.querySelector('.wallet .wl b')||{}).textContent||''");p.evaluate("()=>{const b=document.querySelector('#dlg-shop [data-act=\"modal-close\"]');if(b)b.click();}");p.wait_for_timeout(300)
    import re;m=re.search(r'(\d+)',t);return int(m.group(1)) if m else -1
p=R.open(1180,900,ls={'gbb_note':'9999999999999'});close_dlg(p);p.wait_for_timeout(600)
p.evaluate("()=>{const S=window.__store;S['days/m1_'+new Date().toISOString().slice(0,10)]=Object.assign({},S['days/m1_'+new Date().toISOString().slice(0,10)]||{},{mins:{s2:3000}});window.__fire();}");p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="chat"]',600)
def post(g,n,k=None,dl=None,q=None,a=None):
    click(p,'#msgLot',500);click(p,'[data-act="lot-set2"][data-k="g"][data-v="%s"]'%g,300)
    if k:click(p,'[data-act="lot-set2"][data-k="k"][data-v="%d"]'%k,200)
    if dl:click(p,'[data-act="lot-set2"][data-k="dl"][data-v="%d"]'%dl,200)
    if q:p.fill('[data-draft="lotQ"]',q);p.fill('[data-draft="lotA"]',a)
    p.fill('[data-draft="lotN"]',str(n));p.wait_for_timeout(250);click(p,'[data-act="lot-add2"]',800)
    return [x for x in gifts(p).items() if x[1].get('g')==g][-1]
b0=ink(p);print('ink start',b0)
check('8 modes in composer',(click(p,'#msgLot',500) or True) and ev(p,"document.querySelectorAll('[data-act=\"lot-set2\"][data-k=\"g\"]').length")==8)
p.evaluate("()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();}");p.wait_for_timeout(300)
# 행운 봉투
rid,rg=post('rand',30,k=3)
check('rand amounts sum',sum(rg['amts'])==30 and len(rg['amts'])==3 and min(rg['amts'])>=1,rg['amts'])
check('ink reserved',ink(p)==b0-30,ink(p))
p.evaluate("(id)=>{const S=window.__store,t=Date.now();['m2','m3','m4'].forEach((m,i)=>{S['progress/'+m]=Object.assign({},S['progress/'+m]||{},{lc:{[id]:t+i}});});window.__fire();}",rid);p.wait_for_timeout(600)
txt=ev(p,"[...document.querySelectorAll('.lot2')].map(e=>e.textContent).join(' | ')")
check('rand settled hidden until open','누가 얼마 받았나 보기' in txt and '%d방울'%rg['amts'][0] not in txt.split('누가')[0][-30:],txt[:200])
check('sender pays all 30',ink(p)==b0-30)
# 퀴즈
qid,qg=post('quiz',20,k=2,q='1+1은?',a='2')
check('quiz stored hashed',qg.get('h') and '2' not in json.dumps({k:v for k,v in qg.items() if k=='q'}) and qg.get('q')=='1+1은?')
# 뽑기: 올린 사람도 열기 전에는 결과 못 봄
wid,wg=post('wheel',10)
txt=ev(p,"[...document.querySelectorAll('.lot2')].map(e=>e.textContent).join(' | ')")
check('wheel result hidden','열어 봐야' in txt and not ev(p,"!!document.getElementById('dlg-lot')"),txt[-160:])
click(p,'[data-act="lot-open"][data-id="%s"]'%wid,800)
check('open shows wheel',ev(p,"!!document.querySelector('#dlg-lot .lwheel')"))
p.evaluate("()=>{const b=document.querySelector('#dlg-lot [data-act=\"modal-close\"]');if(b)b.click();}");p.wait_for_timeout(400)
# 마감 추첨: 마감 지난 것처럼 만들기
did,dg=post('draw',40,k=1,dl=10)
check('draw has end',dg.get('end',0)>time.time()*1000)
p.evaluate("(id)=>{const S=window.__store,t=Date.now();['m2','m3'].forEach((m,i)=>{const pr=S['progress/'+m]=Object.assign({},S['progress/'+m]||{});pr.lj=Object.assign({},pr.lj||{},{[id]:t+i});});S['gifts/'+id].end=t+5;window.__fire();}",did);p.wait_for_timeout(1500)
txt=ev(p,"[...document.querySelectorAll('.lot2')].map(e=>e.textContent).join(' | ')")
check('draw hidden after end','마감되었습니다' in txt,txt[-120:])
click(p,'[data-act="lot-open"][data-id="%s"]'%did,800)
check('draw wheel modal',ev(p,"!!document.querySelector('#dlg-lot .lwheel')"))
p.evaluate("()=>{const b=document.querySelector('#dlg-lot [data-act=\"modal-close\"]');if(b)b.click();}");p.wait_for_timeout(300)
# 모여라: 아무도 안 오면 돌아옴
pid,pg=post('pot',30,dl=10)
p.evaluate("(id)=>{const S=window.__store;S['gifts/'+id].end=Date.now()-1;window.__fire();}",pid);p.wait_for_timeout(1200)
# 공부왕: m2가 오늘 가장 많이
bid,bg=post('best',25,dl=10)
p.evaluate("(id)=>{const S=window.__store,d=S['gifts/'+id].day;S['days/m2_'+d]={mins:{s2:300}};S['days/m3_'+d]={mins:{s2:100}};S['gifts/'+id].end=Date.now()-1;window.__fire();}",bid);p.wait_for_timeout(2500)
check('best winner written',(store(p,'gifts/'+bid) or {}).get('win')=={'m2':25},(store(p,'gifts/'+bid) or {}).get('win'))
# 잉크: 봉투 30 + 퀴즈 20(아직) + 뽑기 10 + 추첨 40 + 모여라 0(돌아옴) + 공부왕 25
check('ink accounting',ink(p)==b0-30-20-10-40-25,(ink(p),b0))
# 퀴즈 거두기
click(p,'[data-act="lot-back"][data-id="%s"]'%qid,200);click(p,'[data-act="lot-back"][data-id="%s"]'%qid,600)
check('quiz take back refunds',ink(p)==b0-30-10-40-25)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
# 받는 쪽(m2): 퀴즈 맞히기, 봉투 열기
q=R.open(1180,900,ls={'gbb_note':'9999999999999'},me='m2');close_dlg(q);q.wait_for_timeout(500)
q.evaluate("()=>{const S=window.__store,t=Date.now();S['gifts/gq1']={from:'m1',to:'all',n:20,at:t,g:'quiz',k:2,st:'open',q:'수도는?',h:'%s'};S['msgs/qq1']={from:'m1',to:'all',text:'',gift:20,lot:'gq1',at:t};S['gifts/gr1']={from:'m1',to:'all',n:30,at:t,g:'rand',k:3,st:'open',amts:[5,15,10]};S['msgs/qr1']={from:'m1',to:'all',text:'',gift:30,lot:'gr1',at:t+1};window.__fire();}"%q.evaluate("()=>{var t='gq1|서울',h=5381;for(var i=0;i<t.length;i++)h=((h<<5)+h+t.charCodeAt(i))|0;return (h>>>0).toString(36);}"))
q.wait_for_timeout(600);click(q,'[data-act="tab"][data-tab="chat"]',700)
q.fill('[data-draft="lq:gq1"]','부산');click(q,'[data-act="lot-ans"][data-id="gq1"]',500)
check('wrong answer no claim',not ((store(q,'progress/m2') or {}).get('lq') or {}).get('gq1'))
q.fill('[data-draft="lq:gq1"]',' 서 울 ');click(q,'[data-act="lot-ans"][data-id="gq1"]',600)
check('right answer claims',bool(((store(q,'progress/m2') or {}).get('lq') or {}).get('gq1')))
click(q,'[data-act="lot-env"][data-id="gr1"]',600)
fl=ev(q,"(document.querySelector('.flash span')||{}).textContent||''")
check('envelope shows my amount','5방울' in fl,fl)
print('errors',R.errors);check('no errors 2',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
