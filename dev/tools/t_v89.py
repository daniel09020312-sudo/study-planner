# v95: 앱에서 방장이 승인하면 3D 연출(FR3)이 열리고, 끝까지 넘기면 닫힘. 3D가 안 되면 예전 연출(t_v88)
import sys,json,time,re
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
THREE=open('/home/claude/planner/vendor/three-r128.min.js','rb').read()
R=Rig();R.browser.close();R.browser=R.pw.chromium.launch(args=['--font-render-hinting=none','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
SEED="(function(){var t=setInterval(function(){var S=window.__store;if(!S||!S['meta/config'])return;var ms=['m1','m2','m3','m4','m5'];var d0=new Date('2026-11-02T12:00:00+09:00').getTime();ms.forEach(function(m,i){for(var k=0;k<(4+i*3)%13+2;k++){var dt=new Date(d0+k*86400000*2),ds=dt.toISOString().slice(0,10);S['days/'+m+'_'+ds]={mins:{s1:60+i*40+k*7},in:dt.getTime(),certAt:dt.getTime()+3600000,goals:[{id:'g1',text:'a',sid:'s1',done:true},{id:'g2',text:'b',sid:'s1',done:true},{id:'g3',text:'c',sid:'s2',done:true}]};}});clearInterval(t);},5);})();"
p=R.open(1280,800,ls={'gbb_note':'9999999999999'},now='2026-12-10T10:00:00+09:00',pre=SEED)
p.context.route(re.compile(r'.*three(-r128)?\.min\.js.*'),lambda r:r.fulfill(status=200,content_type='application/javascript',body=THREE))
close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="rank"]',600);click(p,'[data-act="range"][data-id="all"]',600)
click(p,'[data-act="fin-ok"]',300);click(p,'[data-act="fin-ok"]',600)
p.wait_for_function("()=>document.querySelector('.f3')&&document.querySelector('.f3').__fr3",timeout=40000)
check('3D reveal opened',True)
check('old modal not opened',not ev(p,"!!document.getElementById('dlg-finrev')"))
d=ev(p,"document.querySelector('.f3').__fr3.dbg()");print(d['bars'])
check('top3 present',sorted(b['r'] for b in d['bars'])==[1,2,3])
ev(p,"(document.querySelector('.f3').__fr3.skip(),1)")
t0=time.time()
while time.time()-t0<60:
    s=ev(p,"document.querySelector('.f3').__fr3.state()")
    if not s['busy'] and s['next']=='닫기':break
    time.sleep(.5)
check('skip to final',s['next']=='닫기',s)
txt=ev(p,"document.querySelector('.f3 .f3final').textContent")
check('final list shows names',all(n in txt for n in ['민준','서연','도윤','하준','지호']),txt[:120])
try:p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/app_fr3.png',timeout=90000)
except Exception as e:print('shot skipped',str(e)[:80])
ev(p,"(document.querySelector('.f3next').click(),1)");p.wait_for_timeout(1200)
check('closed',not ev(p,"!!document.querySelector('.f3')") and ev(p,"!!document.getElementById('c-fin')"))
click(p,'[data-act="fr-replay"]',1500)
print('after replay', ev(p,"[!!document.querySelector('.f3'),!!document.getElementById('dlg-finrev'),!!document.querySelector('[data-act=\"fr-replay\"]')]"))
p.wait_for_function("()=>document.querySelector('.f3')&&document.querySelector('.f3').__fr3",timeout=40000)
check('replay opens 3D again',True)
print('errors',R.errors);check('no errors',not [e for e in R.errors if 'WebGL' not in e and 'GPU' not in e],R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
