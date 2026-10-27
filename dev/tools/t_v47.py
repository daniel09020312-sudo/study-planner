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
NOW=datetime.datetime(2026,10,28,10,0,0)
T='2026-10-28'
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("(T)=>{const S=window.__store;S['days/m1_'+T]=Object.assign({},S['days/m1_'+T]||{},{goals:[],mins:{s2:120,s3:30}});window.__fire();}",T);p.wait_for_timeout(400)
click(p,'[data-act="tab"][data-tab="room"]',800)
# 1) 멈춘 뒤 빼기
click(p,'[data-modal="trim"]',500)
check('modal opens',st(p,"!!document.querySelector('#dlg-trim')"))
p.locator('#dlg-trim [data-k="sid"][data-v="s2"]').click();p.wait_for_timeout(200)
p.locator('#dlg-trim [data-k="n"][data-v="60"]').click();p.wait_for_timeout(200)
click(p,'[data-act="trim-go"]',600)
d=store(p,'days/m1_'+T)
check('s2 120 -> 60',d['mins'].get('s2')==60 and d['mins'].get('s3')==30,d['mins'])
# 2) 직접 입력, 초과는 막힘
click(p,'[data-modal="trim"]',500)
p.locator('#dlg-trim [data-k="sid"][data-v="s3"]').click();p.wait_for_timeout(200)
p.fill('#dlg-trim input[data-draft="trimN"]','99');p.wait_for_timeout(300)
check('over max disabled',st(p,"document.querySelector('[data-act=\"trim-go\"]').disabled"))
p.fill('#dlg-trim input[data-draft="trimN"]','30');p.wait_for_timeout(300)
click(p,'[data-act="trim-go"]',600)
d=store(p,'days/m1_'+T)
check('s3 removed at 0',('s3' not in d['mins']) and d['mins'].get('s2')==60,d['mins'])
# 3) 타이머 켠 채 빼고 끝내기
p.evaluate("()=>{const S=window.__store;S['live/m1']={sid:'s2',start:Date.now()-90*60000,flushed:Date.now()-90*60000,cm:0};window.__fire();}");p.wait_for_timeout(600)
check('stop+trim button',st(p,"!!document.querySelector('[data-act=\"open\"][data-modal=\"trim\"][data-stop=\"1\"]')"))
click(p,'[data-act="open"][data-modal="trim"][data-stop="1"]',500)
p.locator('#dlg-trim [data-k="n"][data-v="60"]').click();p.wait_for_timeout(200)
click(p,'[data-act="trim-go"]',900)
d=store(p,'days/m1_'+T)
check('timer stopped and 90-60 added',(store(p,'live/m1') is None) and d['mins'].get('s2')==60+30,(d['mins'],store(p,'live/m1')))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
