# v54: 반 전체 목표, 같이 공부하기, 공부 잔디, 요즘 안 보이는 사람
import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,11,4,15,0,0)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
# 지난주(10/26~11/1)에 모두 합쳐 많이 공부 -> 목표 달성 -> 잉크 20
seed="""()=>{const S=window.__store;['m1','m2','m3','m4','m5'].forEach(m=>{['2026-10-26','2026-10-27','2026-10-28','2026-10-29'].forEach(d=>{S['days/'+m+'_'+d]={in:d+'T00:10:00.000Z',mins:{s2:600},goals:[]};});});
S['days/m1_2026-11-03']={in:'2026-11-03T00:10:00.000Z',mins:{s2:120},goals:[]};S['days/m2_2026-11-04']={in:'2026-11-04T00:10:00.000Z',mins:{s2:60},goals:[]};window.__fire();}"""
p.evaluate(seed);p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="room"]',800)
check('class goal card',st(p,"!!document.querySelector('#c-cg')"))
t=st(p,"document.querySelector('#c-cg').innerText")
check('goal default 50h for 5 people',('/ 50시간' in t),t.replace('\n',' ')[:160])
check('last week achieved',('지난주 달성' in t))
def ink():
    click(p,'#shopBtn',800);v=st(p,"(document.querySelector('.wallet .wl b')||{}).textContent");close_dlg(p);return int(''.join(ch for ch in (v or '0') if ch.isdigit()) or 0)
ink1=ink()
p.evaluate("()=>{const S=window.__store;S['meta/config'].cgoal={hist:{'2026-10-26':5000}};window.__fire();}");p.wait_for_timeout(400)
ink0=ink()
p.evaluate("()=>{const S=window.__store;delete S['meta/config'].cgoal;window.__fire();}");p.wait_for_timeout(400)
check('ink bonus 20 for achieved week',ink1-ink0==20,(ink0,ink1))
# 방장(m1)이 목표 바꾸기
click(p,'#c-cg [data-act="cg-edit"]',400);click(p,'#c-cg [data-act="cg-set"][data-v="200"]',500)
cg=json.loads(st(p,"JSON.stringify(window.__store['meta/config'].cgoal||null)"))
check('target saved for this week',cg and cg['hist'].get('2026-11-02')==200,cg)
t=st(p,"document.querySelector('#c-cg').innerText")
check('this week shows 200',('/ 200시간' in t))
# 같이 공부하기: 지금 공부 중 + 약속
p.evaluate("()=>{const S=window.__store;S['live/m3']={sid:'s2',start:Date.now()-20*60000,flushed:Date.now()-20*60000,cm:0};window.__fire();}");p.wait_for_timeout(500)
check('live list',st(p,"document.querySelectorAll('#c-tg .tgp').length")>=1)
click(p,'#c-tg [data-act="meet-form"]',400)
p.fill('#c-tg input[data-draft="meetT"]','21:50');p.fill('#c-tg input[data-draft="meetN"]','저녁 집중');p.wait_for_timeout(200)
click(p,'#c-tg [data-act="meet-add"]',600)
meet=json.loads(st(p,"JSON.stringify(window.__store['meta/config'].meet||{})"))
check('meet created',len(meet)==1 and list(meet.values())[0]['t']=='저녁 집중',meet)
mid=list(meet.keys())[0]
check('creator joined',(store(p,'progress/m1') or {}).get('mj',{}).get(mid)==1)
click(p,'#mt-%s [data-act="meet-join"]'%mid,500)
check('leave meet',not (store(p,'progress/m1') or {}).get('mj',{}).get(mid))
click(p,'#mt-%s [data-act="meet-del"]'%mid,300);click(p,'#mt-%s [data-act="meet-del"]'%mid,600)
check('meet deleted',not json.loads(st(p,"JSON.stringify(window.__store['meta/config'].meet||{})")))
# 요즘 안 보이는 사람(방장): m4, m5는 10/29 뒤로 출석 없음
check('quiet card',st(p,"!!document.querySelector('#c-quiet')") and ('m' or True),st(p,"(document.querySelector('#c-quiet')||{}).innerText"))
# 잔디
click(p,'[data-act="tab"][data-tab="report"]',800)
check('grass card',st(p,"document.querySelectorAll('#c-grass .ggrid i').length")>=30)
click(p,'#c-grass [data-act="grass-m"]',500)
check('grass prev month',('10월' in st(p,"document.querySelector('#c-grass').innerText")))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
