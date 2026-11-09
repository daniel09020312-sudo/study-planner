# v83: 찌르기 알림 기본 켜짐, 처음 누를 때 한 번 허용 묻기, 끄면 gbb_pnoff
import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
PRE="(function(){var perm='default';window.__asked=0;function N(t,o){};Object.defineProperty(N,'permission',{get:function(){return perm;}});N.requestPermission=function(){window.__asked++;perm='granted';return Promise.resolve('granted');};window.Notification=N;})();"
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-11-09T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="cal"]',600)
check('asked once on first tap',ev(p,"window.__asked")==1,ev(p,"window.__asked"))
click(p,'[data-act="tab"][data-tab="prog"]',400)
check('not asked again',ev(p,"window.__asked")==1)
click(p,'#meBtn',600)
check('on by default: settings shows 끄기',ev(p,"document.querySelector('[data-act=\"pn-toggle\"]').textContent")=='알림 끄기')
click(p,'[data-act="pn-toggle"]',500)
check('off sets pnoff',ev(p,"localStorage.getItem('gbb_pnoff')") =='1' and ev(p,"document.querySelector('[data-act=\"pn-toggle\"]').textContent")=='알림 켜기')
click(p,'[data-act="pn-toggle"]',500)
check('on again',ev(p,"localStorage.getItem('gbb_pnoff')") is None and ev(p,"document.querySelector('[data-act=\"pn-toggle\"]').textContent")=='알림 끄기')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
