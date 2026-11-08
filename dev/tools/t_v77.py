# v81: 할 일 거둬들이기(지난 날 못 끝낸 것 포함)와 모음에서 골고루 나누기
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
T='2026-11-08';P='2026-11-03'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('days/m1_')).forEach(k=>delete S[k]);S['days/m1_%s']={goals:[{id:'p1',text:'옛일1',sid:'s1',done:false},{id:'p2',text:'옛일2',sid:'s2',done:true},{id:'p3',text:'옛일3',sid:'s3',done:false}]};S['days/m1_%s']={goals:[{id:'a',text:'오늘1',sid:'s1',done:false},{id:'b',text:'오늘2',sid:'s2',done:false}]};S['days/m1_2026-11-09']={goals:[{id:'c',text:'내일1',sid:'s4',done:false}]};clearInterval(t);},5);})();"%(P,T)
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=T+'T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',700);click(p,'#c-wk [data-act="open"][data-modal="gorder"]',700)
click(p,'[data-act="go-r"][data-v="past"]',500)
rows=ev(p,"[...document.querySelectorAll('#dlg-gorder .gordi')].map(e=>e.dataset.id)")
check('past range shows undone only',rows==['p1','p3'],rows)
click(p,'[data-act="go-selall"]',400)
click(p,'[data-act="go-r"][data-v="next"]',400)
click(p,'[data-act="go-sel"][data-id="b"]',300);click(p,'[data-act="go-sel"][data-id="c"]',300)
check('4 selected',('4개' in ev(p,"document.querySelector('.gselbar').textContent")))
click(p,'[data-act="go-collect"]',900)
ib=(store(p,'inbox/m1') or {}).get('items',{})
check('collected to inbox',sorted(x['t'] for x in ib.values())==['내일1','옛일1','옛일3','오늘2'],[x['t'] for x in ib.values()])
pg=[g for g in store(p,'days/m1_'+P)['goals']]
check('past day keeps moved marks',[g.get('mv') for g in pg if g['id'] in ('p1','p3')]==[1,1],pg)
check('today removed',[g['id'] for g in store(p,'days/m1_'+T)['goals']]==['a'])
check('inbox opened with selection',ev(p,"!!document.getElementById('dlg-inbox')") and ev(p,"document.querySelectorAll('#dlg-inbox .ibrow.on').length")==4)
check('origin date shown',ev(p,"document.querySelectorAll('#dlg-inbox .ibod').length")==4)
click(p,'[data-act="ib-n"][data-v="3"]',300);click(p,'[data-act="ib-spread"]',900)
cnt={d:len(store(p,'days/m1_'+d)['goals']) for d in [T,'2026-11-09','2026-11-10']}
check('spread evenly over 3 days (fewest first)',cnt=={T:2,'2026-11-09':2,'2026-11-10':1} or cnt=={T:2,'2026-11-09':1,'2026-11-10':2},cnt)
check('inbox emptied',not (store(p,'inbox/m1') or {}).get('items'))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
