# v56: 전체 대화방 잉크 뿌리기: 선착순, 뽑기(전체), 사다리타기(전체)
import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def allk(p,pre):return json.loads(st(p,"JSON.stringify(Object.fromEntries(Object.entries(window.__store).filter(e=>e[0].startsWith('%s')).map(e=>[e[0].slice(%d),e[1]])))"%(pre,len(pre))))
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,30,15,0,0)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("()=>{const S=window.__store;Object.keys(S).filter(k=>k.startsWith('gifts/')).forEach(k=>delete S[k]);['2026-10-19','2026-10-20','2026-10-21'].forEach(d=>{S['days/m1_'+d]={mins:{s2:600},goals:[]};});window.__fire();}");p.wait_for_timeout(300)
def ink():
    click(p,'#shopBtn',800);v=st(p,"(document.querySelector('.wallet .wl b')||{}).textContent");close_dlg(p);return int(''.join(ch for ch in (v or '0') if ch.isdigit()) or 0)
def newlot(g,k,amt):
    click(p,'[data-act="tab"][data-tab="chat"]',600);click(p,'[data-act="chan"][data-id="all"]',500);click(p,'#msgLot',500)
    click(p,'[data-act="lot-set"][data-k="g"][data-v="%s"]'%g,300)
    if k: click(p,'[data-act="lot-set"][data-k="k"][data-v="%d"]'%k,300)
    click(p,'[data-act="lot-amt"][data-v="%d"]'%amt,300);click(p,'[data-act="lot-add"]',900)
i0=ink()
# 1) 뽑기(전체): 올리자마자 결과
newlot('wheel',0,30)
gs=allk(p,'gifts/');g=[v for v in gs.values() if v['g']=='wheel'][0]
check('draw done at once over all members',g['st']=='done' and len(g['who'])==4 and sum(g['win'].values())==30 and len(g['win'])==1,g)
check('result modal opens',st(p,"!!document.querySelector('#dlg-lot .lwh')"))
close_dlg(p)
# 2) 사다리(전체) 2명
newlot('ladder',2,10)
g=[v for v in allk(p,'gifts/').values() if v['g']=='ladder'][0]
check('ladder 2 winners 5 each',g['st']=='done' and sorted(g['win'].values())==[5,5],g['win'])
check('ladder 4 paths',st(p,"document.querySelectorAll('#dlg-lot .lp').length")==4)
close_dlg(p)
i1=ink();check('spent 40',i0-i1==40,(i0,i1))
# 3) 선착순 2명, 30방울 -> 15씩
newlot('first',2,30)
fid=[k for k,v in allk(p,'gifts/').items() if v['g']=='first'][0]
i2=ink();check('first-come reserves 30',i1-i2==30,(i1,i2))
p.evaluate("(id)=>{const S=window.__store,n=Date.now();S['progress/m3']=Object.assign({},S['progress/m3']||{},{lc:{[id]:n-5000}});S['progress/m2']=Object.assign({},S['progress/m2']||{},{lc:{[id]:n-3000}});S['progress/m4']=Object.assign({},S['progress/m4']||{},{lc:{[id]:n-1000}});window.__fire();}",fid);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="chat"]',600)
t=st(p,"[...document.querySelectorAll('.bb.lot')].map(e=>e.innerText).join('|')")
check('first two shown, full',('(2/2)' in t),t[:200])
i3=ink();check('sender pays 30 total (2x15)',i2==i3,(i2,i3))
# 4) 받는 쪽: 다른 사람이 올린 선착순에서 m1이 받기
p.evaluate("()=>{const S=window.__store,n=Date.now();S['gifts/ff']={from:'m2',to:'all',n:20,at:n,g:'first',k:2,st:'open'};S['msgs/ff']={from:'m2',to:'all',text:'',gift:20,lot:'ff',at:n};window.__fire();}");p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="chat"]',600)
click(p,'[data-act="lot-claim"][data-id="ff"]',700)
check('claimed recorded',bool(((store(p,'progress/m1') or {}).get('lc') or {}).get('ff')))
i4=ink();check('receiver +10',i4-i3==10,(i3,i4))
# 5) 선착순 남은 잉크 거두기
newlot('first',3,30)
bid=[k for k,v in allk(p,'gifts/').items() if v['g']=='first' and v['from']=='m1' and k!=fid][0]
p.evaluate("(id)=>{const S=window.__store;S['progress/m5']=Object.assign({},S['progress/m5']||{},{lc:{[id]:Date.now()}});window.__fire();}",bid);p.wait_for_timeout(400)
i5=ink()
click(p,'[data-act="tab"][data-tab="chat"]',600)
click(p,'[data-act="lot-back"][data-id="%s"]'%bid,300);click(p,'[data-act="lot-back"][data-id="%s"]'%bid,600)
i6=ink();check('take back unclaimed 20 (one took 10)',i6-i5==20,(i5,i6))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
