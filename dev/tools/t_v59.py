# v56: 전체 대화방 잉크 뿌리기(돌림판, 사다리)
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
i0=ink()
click(p,'[data-act="tab"][data-tab="chat"]',700);click(p,'[data-act="chan"][data-id="all"]',600)
check('ink button in all chat',st(p,"!!document.getElementById('msgLot')"))
click(p,'#msgLot',500)
click(p,'[data-act="lot-amt"][data-v="30"]',300)
p.fill('input[data-draft="lotMsg"]','수고했어');click(p,'[data-act="lot-add"]',700)
gs=allk(p,'gifts/');gid=list(gs.keys())[0] if gs else ''
check('wheel lot created',gs and gs[gid]['g']=='wheel' and gs[gid]['st']=='open' and gs[gid]['to']=='all',gs)
i1=ink();check("reserved 30",i0-i1==30,(i0,i1))
click(p,'[data-act="tab"][data-tab="chat"]',600)
check('start disabled (<2)',st(p,"document.querySelector('[data-act=lot-go]').disabled"))
p.evaluate("(id)=>{const S=window.__store;['m2','m3','m4'].forEach(m=>{S['progress/'+m]=Object.assign({},S['progress/'+m]||{},{lj:{[id]:1}});});window.__fire();}",gid);p.wait_for_timeout(500)
check('3 joined shown',('참여 3명' in st(p,"document.querySelector('.bb.lot').innerText")))
click(p,'[data-act="lot-go"]',800)
g=store(p,'gifts/'+gid);w=g.get('win',{})
check("wheel done: 1 winner gets 30",g["st"]=="done" and len(w)==1 and list(w.values())[0]==30 and list(w.keys())[0] in ['m2','m3','m4'],g)
check('wheel modal',st(p,"!!document.querySelector('#dlg-lot .lwh')"));p.wait_for_timeout(4300);p.screenshot(path='/home/claude/planner/shots/v56_wheel.png')
close_dlg(p);i2=ink();check('sender ink stays -30',i2==i1,(i1,i2))
# 사다리 2명 당첨
click(p,'[data-act="tab"][data-tab="chat"]',600)
click(p,'#msgLot',500);click(p,'[data-act="lot-set"][data-k="g"][data-v="ladder"]',300);click(p,'[data-act="lot-set"][data-k="k"][data-v="2"]',300)
click(p,'[data-act="lot-amt"][data-v="10"]',300);click(p,'[data-act="lot-add"]',700)
gs=allk(p,'gifts/');lid=[k for k,v in gs.items() if v.get('g')=='ladder'][0]
p.evaluate("(id)=>{const S=window.__store;['m2','m3','m4','m5'].forEach(m=>{S['progress/'+m]=Object.assign({},S['progress/'+m]||{},{lj:{[id]:1}});});window.__fire();}",lid);p.wait_for_timeout(500)
click(p,'[data-act="lot-go"][data-id="%s"]'%lid,800)
g=store(p,'gifts/'+lid);w=g.get('win',{})
check('ladder 2 winners 5 each',len(w)==2 and sorted(w.values())==[5,5],w)
check('ladder svg',st(p,"document.querySelectorAll('#dlg-lot .lp').length")==4 and st(p,"document.querySelectorAll('#dlg-lot .lpz.on').length")==2)
p.wait_for_timeout(3000);p.screenshot(path='/home/claude/planner/shots/v56_ladder.png');check('winning paths count 2',st(p,"document.querySelectorAll('#dlg-lot .lp.win').length")==2)
close_dlg(p)
# 받는 사람 쪽: m1이 당첨된 다른 사람의 뿌리기
p.evaluate("()=>{const S=window.__store,n=Date.now();S['gifts/zz']={from:'m2',to:'all',n:30,at:n,g:'wheel',k:1,st:'done',who:['m1','m3'],seed:5,win:{m1:30}};S['msgs/zz']={from:'m2',to:'all',text:'',gift:30,lot:'zz',at:n};window.__fire();}");p.wait_for_timeout(500)
i3=ink();check('winner ink +30 (after spending 10 on ladder)',i3-i2==20,(i2,i3))
# 취소
click(p,'[data-act="tab"][data-tab="chat"]',600)
click(p,'#msgLot',500);click(p,'[data-act="lot-amt"][data-v="10"]',300);click(p,'[data-act="lot-add"]',700)
i4=ink();click(p,'[data-act="tab"][data-tab="chat"]',600)
bid=[k for k,v in allk(p,'gifts/').items() if v.get('st')=='open'][0]
click(p,'[data-act="lot-back"][data-id="%s"]'%bid,300);click(p,'[data-act="lot-back"][data-id="%s"]'%bid,600)
i5=ink();check('cancel refunds',i5-i4==10,(i4,i5))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
