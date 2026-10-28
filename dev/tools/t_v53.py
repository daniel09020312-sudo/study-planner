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
NOW=datetime.datetime(2026,10,28,21,30,0)
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
# 1) 타이머 30분 -> hh 기록
p.evaluate("()=>{const S=window.__store;S['live/m1']={sid:'s2',start:Date.now()-30*60000,flushed:Date.now()-30*60000,cm:0};window.__fire();}");p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="room"]',800)
click(p,'[data-act="timer-stop"]',900)
d=store(p,'days/m1_2026-10-28') or {}
hh=d.get('hh') or {}
tot=sum(v for o in hh.values() for v in o.values())
check('hh recorded 30 min',tot==30 and d['mins'].get('s2')>=30,(hh,d.get('mins')))
check('hours 21 only (21:00-21:30)',set(hh.keys())<= {'h20','h21'},list(hh.keys()))
# 2) 시간 빼기: hh도 같이 줄어듦
click(p,'[data-modal="trim"]',500)
p.locator('#dlg-trim [data-k="n"][data-v="10"]').click();p.wait_for_timeout(200)
click(p,'[data-act="trim-go"]',700)
d=store(p,'days/m1_2026-10-28') or {}
tot2=sum(v for o in (d.get('hh') or {}).values() for v in o.values())
check('hh reduced by trim',tot2==20,tot2)
# 3) 다른 편집(할 일 완료)에도 hh 유지
p.evaluate("()=>{const S=window.__store;const k='days/m1_2026-10-28';S[k].goals=[{id:'q1',text:'z',sid:'s2',done:false}];window.__fire();}");p.wait_for_timeout(300)
click(p,'[data-act="tab"][data-tab="cal"]',700)
p.evaluate("()=>{const b=document.querySelector('.chk[data-id=\"q1\"]');if(b)b.click();}");p.wait_for_timeout(700)
d=store(p,'days/m1_2026-10-28') or {}
check('hh kept after other edit',sum(v for o in (d.get('hh') or {}).values() for v in o.values())==20,d.get('hh'))
# 4) 리포트 카드
p.evaluate("()=>{const S=window.__store;S['days/m1_2026-10-27']={in:'2026-10-27T00:10:00.000Z',mins:{s2:90,s3:45},hh:{h19:{s2:60},h20:{s2:30,s3:45}},goals:[]};window.__fire();}");p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="report"]',900)
check('grid card',st(p,"!!document.querySelector('#c-rgrid-this .rgrid')") and st(p,"document.querySelectorAll('#c-rgrid-this tbody tr').length")>=3)
check('hour chart',st(p,"document.querySelectorAll('#c-rhour-this .hc').length")==24,st(p,"(document.querySelector('#c-rhour-this .hint')||{}).innerText"))
check('peak text',st(p,"document.querySelector('#c-rhour-this').innerText.includes('가장 오래 공부한 시간')"))
click(p,'[data-act="rep-week"][data-id="last"]',700)
check('last week empty note',st(p,"document.querySelector('#c-rhour-last').innerText.includes('아직 시간대 기록이 없습니다')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
