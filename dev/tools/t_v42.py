# v42: 참여 인원 50명까지, 벌칙 없음, 상품은 1·2·3등
import sys,json,datetime,time
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
ok=True
def check(name,cond,extra=''):
    global ok
    print(('OK  ' if cond else 'FAIL')+' '+name+(' | '+str(extra) if extra else ''))
    if not cond: ok=False
R=Rig()
# 49명 방: 하나 더 넣으면 50명, 그다음은 막힘
ROS=[{'id':'m%d'%i,'name':'학생%02d'%i} for i in range(1,50)]
pre="window.__ROS=%s;"%json.dumps(ROS)
SEED="()=>{const S=window.__store;S['meta/config'].roster=window.__ROS;window.__fire&&window.__fire();}"
p=R.open(1180,820,ls={'gbb_note':'9999999999999'},now=datetime.datetime(2026,10,28,10,0,0),pre=pre)
p.evaluate(SEED);p.wait_for_timeout(600);close_dlg(p)
click(p,'#meBtn',600)
p.fill('input[data-draft="memberName"]','오십번째');click(p,'[data-act="member-add"]',500)
n1=len(store(p,'meta/config')['roster'])
p.fill('input[data-draft="memberName"]','쉰한번째');click(p,'[data-act="member-add"]',500)
n2=len(store(p,'meta/config')['roster'])
check('roster 50 allowed',n1==50,n1)
check('roster 51 blocked',n2==50,(n2,st(p,"(document.querySelector('.flash')||{}).textContent")))
close_dlg(p)
# 50명 진도 표: 옆으로 밀어 보기
click(p,'[data-act="tab"][data-tab="prog"]',800)
click(p,'[data-act="prog-mode"][data-id="all"]',800)
t0=time.time();
info=st(p,"(()=>{const t=document.querySelector('#c-tbl');return {many:t.classList.contains('many'),sw:t.scrollWidth,cw:t.clientWidth,cols:t.querySelectorAll('.ohead .ocell').length}})()")
check('progress table scrolls',info['many'] and info['sw']>info['cw'] and info['cols']==50,info)
p.screenshot(path=SH+'v42_prog50.png')
# 렌더 시간(50명)
click(p,'[data-act="tab"][data-tab="rank"]',800)
rt=st(p,"(()=>{const b=document.querySelector('[data-act=\"range\"][data-id=\"this\"]');const a=performance.now();b.click();return performance.now()-a})()")
print('rank render ms (50명):',round(rt,1))
check('rank render under 300ms',rt<300,rt)
# 최종 결과(공개 전): 상품 1·2·3등, 벌칙 없음
click(p,'[data-act="range"][data-id="all"]',700)
check('prize inputs 3',st(p,"document.querySelectorAll('#c-prize .prz').length")==3)
for i,t in [(1,'기프티콘'),(2,'간식 세트'),(3,'음료수')]:
    p.fill('#c-prize input[data-draft="prizeText%d"]'%i,t);click(p,'[data-act="prize-save"][data-id="%d"]'%i,500)
cfg=store(p,'meta/config')
check('prizes saved',cfg.get('prizes')=={'p1':{'t':'기프티콘','by':'m1'},'p2':{'t':'간식 세트','by':'m1'},'p3':{'t':'음료수','by':'m1'}},cfg.get('prizes'))
check('prize card text',st(p,"document.querySelector('#c-prize').innerText.includes('3등 상품')"))
check('no 벌칙 on page',not st(p,"document.body.innerText.includes('벌칙')"))
p.screenshot(path=SH+'v42_prize_wait.png',full_page=True)
print('errors',R.errors);R.errors.clear()

# 예전 방: cfg.prize만 있으면 1등 상품으로, 시험 끝난 뒤 시상대에 1·2·3등 상품
AFTER=datetime.datetime(2026,12,10,15,0,0)
SEED2="()=>{const S=window.__store;S['meta/config'].prize={t:'예전 1등 선물',by:'m2'};S['meta/config'].penalties=[{t:'매점 간식 사기',by:'m1'}];const ms={m1:[300,240,200],m2:[420,380,300],m3:[120,100,90],m4:[60,30,20],m5:[200,260,240]};Object.keys(ms).forEach(m=>{['2026-11-02','2026-11-03','2026-11-10'].forEach((d,i)=>{S['days/'+m+'_'+d]={in:d+'T00:10:00.000Z',mins:{s2:ms[m][i]},goals:[]};});});window.__fire&&window.__fire();}"
p=R.open(1180,820,ls={'gbb_note':'9999999999999'},now=AFTER)
p.evaluate(SEED2);p.wait_for_timeout(600);close_dlg(p)
click(p,'[data-act="tab"][data-tab="rank"]',800)
click(p,'[data-act="range"][data-id="all"]',800)
check('legacy prize as 1st',st(p,"document.querySelector('#prz-1 b').textContent")=='예전 1등 선물')
p.evaluate("()=>{window.__store['meta/config'].prizes={p2:{t:'간식',by:'m1'},p3:{t:'음료',by:'m3'}};window.__fire();}");p.wait_for_timeout(600)
tags=st(p,"[...document.querySelectorAll('.podium .pd .tag')].map(e=>e.textContent)")
check('podium prizes 1-3',len(tags)==3 and tags[0].startswith('상품: 간식') and '예전 1등 선물' in tags[1],tags)
ranks=st(p,"[...document.querySelectorAll('.fr2 .tag.a')].map(e=>e.textContent).filter(t=>/등$/.test(t))")
check('rank tags 1~3등',ranks==['1등','2등','3등'],ranks)
check('no 벌칙 after final',not st(p,"document.body.innerText.includes('벌칙')"))
check('no prize inputs after final',st(p,"document.querySelectorAll('#c-prize input').length")==0)
p.screenshot(path=SH+'v42_final.png',full_page=True)
click(p,'[data-act="tab"][data-tab="play"]',800)
click(p,'[data-act="play-tab"][data-id="duel"]',600)
check('no 벌칙 in play',not st(p,"document.body.innerText.includes('벌칙')"))
print('errors',R.errors)
check('no page errors',not R.errors,R.errors)
R.close()
print('ALL OK' if ok else 'SOME FAILED')
