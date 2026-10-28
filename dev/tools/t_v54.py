# v54(v51): 10명 더보기, 1:1 대결 라운드제, 응원, 한마디, 자랑, 할 일 달성률, 아침 출석
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
NOW=datetime.datetime(2026,10,28,12,0,0)
ROS=[{'id':'m%d'%i,'name':'학생%02d'%i} for i in range(1,26)]
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW,pre="window.__ROS=%s;"%json.dumps(ROS))
p.evaluate("()=>{const S=window.__store;S['meta/config'].roster=window.__ROS;Object.keys(S).filter(k=>k.startsWith('duels/')).forEach(k=>delete S[k]);window.__fire();}");p.wait_for_timeout(500);close_dlg(p)
# 1) 10명 더보기 (순위)
click(p,'[data-act="tab"][data-tab="rank"]',800)
check('rank cut to 10',st(p,"document.querySelectorAll('#c-rank-this .rk').length")==10,st(p,"document.querySelectorAll('#c-rank-this .rk').length"))
click(p,'#c-rank-this [data-act="more-list"]',500)
check('rank expands in place',st(p,"document.querySelectorAll('#c-rank-this .rk').length")==25)
click(p,'#c-rank-this [data-act="more-list"]',400)
check('rank collapses',st(p,"document.querySelectorAll('#c-rank-this .rk').length")==10)
# 2) 대결 만들기: 라운드제 + 한마디
click(p,'[data-act="tab"][data-tab="play"]',700);click(p,'[data-act="play-tab"][data-id="duel"]',600)
check('record list cut',st(p,"document.querySelectorAll('#c-duels .sec:last-of-type .brow').length")==10,st(p,"document.querySelectorAll('#c-duels .brow').length"))
click(p,'[data-act="open"][data-modal="duel"]',600)
check('opponent chips cut',st(p,"document.querySelectorAll('.dialog [data-k=\"b\"]').length")==10,st(p,"document.querySelectorAll('.dialog [data-k=\"b\"]').length"))
p.locator('.dialog [data-k="b"]').first.click();p.wait_for_timeout(200)
p.locator('.dialog [data-k="kind"][data-v="goals"]').click();p.wait_for_timeout(200)
p.locator('.dialog [data-k="mode"][data-v="rounds"]').click();p.wait_for_timeout(200)
p.locator('.dialog [data-k="len"][data-v="3"]').click();p.wait_for_timeout(200)
p.fill('.dialog input[data-draft="duelNote"]','이번엔 내가 이긴다')
click(p,'[data-act="duel-add"]',600)
ds=allk(p,'duels/');d=[v for v in ds.values() if v.get('mode')][0];did=[k for k,v in ds.items() if v.get('mode')][0]
check('duel saved rounds+note',d['mode']=='rounds' and d['kind']=='goals' and d['days']==3 and d.get('note')=='이번엔 내가 이긴다',d)
# 3) 진행: 3일 라운드 (10/26~10/28 시작해서 이미 시작한 걸로)
p.evaluate("(a)=>{const S=window.__store;const [id,b]=a;const d=S['duels/'+id];d.status='on';d.start='2026-10-26';d.days=3;const mk=(m,date,done)=>{S['days/'+m+'_'+date]={in:date+'T00:10:00.000Z',goals:Array.from({length:3},(_,i)=>({id:'g'+i,text:'x',sid:'s2',done:i<done})),mins:{s2:30}};};mk(d.a,'2026-10-26',3);mk(d.b,'2026-10-26',1);mk(d.a,'2026-10-27',1);mk(d.b,'2026-10-27',2);mk(d.a,'2026-10-28',3);mk(d.b,'2026-10-28',0);window.__fire();}",[did,d['b']]);p.wait_for_timeout(600)
txt=st(p,"(document.querySelector('#du-%s')||{}).innerText"%did)
check('rounds shown',('라운드' in txt) and ('이번엔 내가 이긴다' in txt) and st(p,"document.querySelectorAll('#du-%s .rdc').length"%did)==3,txt.replace('\n',' | ')[:200])
check('coach line',st(p,"!!document.querySelector('#du-%s .dcoach')"%did))
# 4) 한마디
click(p,'#du-%s [data-act="duel-taunt"]'%did,500)
msgs=allk(p,'msgs/')
check('taunt sent to opponent',any(m.get('duel')==did and m.get('to')==d['b'] and m.get('text') for m in msgs.values()))
# 5) 응원: 제3자 시점(m3 가 아닌 다른 사람으로) -> 응원 단추는 참가자가 아닐 때만
q=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_me':'m20'},me='m20',now=NOW,pre="window.__ROS=%s;"%json.dumps(ROS))
q.evaluate("(a)=>{const S=window.__store;S['meta/config'].roster=window.__ROS;S['duels/'+a[0]]=a[1];window.__fire();}",[did,dict(d,status='on',start='2026-10-26')]);q.wait_for_timeout(500);close_dlg(q)
click(q,'[data-act="tab"][data-tab="play"]',700);click(q,'[data-act="play-tab"][data-id="duel"]',600)
has=st(q,"document.querySelectorAll('#du-%s [data-act=\"duel-cheer\"]').length"%did)
check('cheer buttons for onlooker',has==2,has)
if has==2:
    click(q,'#du-%s [data-act="duel-cheer"][data-side="a"]'%did,500)
    ch=(store(q,'duels/'+did) or {}).get('cheer')
    check('cheer saved',ch=={'m20':'a'},ch)
    click(q,'#du-%s [data-act="duel-cheer"][data-side="a"]'%did,500)
    check('cheer toggled off',not (store(q,'duels/'+did) or {}).get('cheer'))
# 6) 끝난 대결: 승자(a) 자랑하기
p.evaluate("(id)=>{const S=window.__store;S['duels/'+id].start='2026-10-20';window.__fire();}",did);p.wait_for_timeout(500)
w=st(p,"(document.querySelector('#du-%s .dwin')||{}).innerText"%did)
check('result banner',('승리' in w) or ('무승부' in w),w)
if '민준' in w or '학생01' in w:
    click(p,'#du-%s [data-act="duel-brag"]'%did,500)
    check('brag posted',any('이겼습니다' in (m.get('text') or '') for m in allk(p,'msgs/').values()))
p.evaluate("(a)=>{const S=window.__store;const d=S['duels/'+a[0]];d.kind='goals';d.mode='rounds';d.start='2026-10-20';['2026-10-20','2026-10-21','2026-10-22'].forEach(x=>{S['days/'+d.a+'_'+x]={in:x+'T00:10:00.000Z',goals:[1,2,3].map(i=>({id:'k'+i,text:'x',sid:'s2',done:true})),mins:{s2:30}};S['days/'+d.b+'_'+x]={in:x+'T00:10:00.000Z',goals:[1,2,3].map(i=>({id:'k'+i,text:'x',sid:'s2',done:i<2})),mins:{s2:30}};});window.__fire();}",[did]);p.wait_for_timeout(500)
click(p,'#du-%s [data-act="duel-brag"]'%did,600)
check('brag posted to all',any('이겼습니다' in (m.get('text') or '') and m.get('to')=='all' for m in allk(p,'msgs/').values()))
check('brag button gone',not st(p,"!!document.querySelector('#du-%s [data-act=duel-brag]')"%did))
p.screenshot(path='/home/claude/planner/shots/v51_duel.png')
# 7) 달성률/아침 출석 종류 계산이 에러 없이
for kind in ['rate','early','time','score']:
    p.evaluate("(a)=>{const S=window.__store;S['duels/'+a[0]].kind=a[1];S['duels/'+a[0]].start='2026-10-26';window.__fire();}",[did,kind]);p.wait_for_timeout(300)
    check('kind %s renders'%kind,st(p,"!!document.querySelector('#du-%s .vs .p')"%did))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
