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
NOW=datetime.datetime(2026,10,28,12,0,0)
T='2026-10-28'
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
seed="""(T)=>{const S=window.__store,n=Date.now();
S['days/m1_'+T]=Object.assign({},S['days/m1_'+T]||{},{goals:[],mins:{s2:300},hh:{h8:{s2:60},h9:{s2:60},h10:{s2:60},h11:{s2:60},h7:{s2:60}}});
S['flags/f1']={mid:'m1',sid:'s2',start:n-6*3600000,end:n-3600000,why:['cap'],cd:{[T]:300}};
S['flags/f2']={mid:'m1',sid:'s2',start:n-30*3600000,end:n-25*3600000,why:['cap'],cd:{[T]:300}};
window.__fire();}"""
p.evaluate(seed,T);p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="room"]',900)
check('flag card shows',st(p,"!!document.querySelector('#fl-f1')"))
click(p,'#fl-f1 [data-act="flag-open"]',400)
check('panel opens',st(p,"!!document.querySelector('#fl-f1 [data-act=flag-fix]')"))
p.locator('#fl-f1 [data-k="n"][data-v="120"]').click();p.wait_for_timeout(250)
check('preview',('3시간' in st(p,"document.querySelector('#fl-f1 .flfix').innerText")),st(p,"document.querySelector('#fl-f1 .flfix').innerText").replace('\n',' ')[:160])
click(p,'#fl-f1 [data-act="flag-fix"]',700)
d=store(p,'days/m1_'+T);f=store(p,'flags/f1')
check('minutes reduced 300->180',d['mins']['s2']==180,d['mins'])
check('hours reduced too',sum(v for o in d['hh'].values() for v in o.values())==180,d.get('hh'))
check('flag resolved',bool(f.get('cut')) and f.get('cutMins')==120,f)
check('card gone',st(p,"!document.querySelector('#fl-f1')"))
# 그대로 확인
click(p,'#fl-f2 [data-act="flag-open"]',400)
p.fill('#fl-f2 input[data-draft="flagN"]','0');p.wait_for_timeout(300)
check('button says keep',('그대로 확인' in st(p,"document.querySelector('#fl-f2 [data-act=flag-fix]').innerText")))
click(p,'#fl-f2 [data-act="flag-fix"]',700)
d=store(p,'days/m1_'+T)
check('kept minutes, flag cleared',d['mins']['s2']==180 and not st(p,"!!document.querySelector('#fl-f2')"),d['mins'])
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
