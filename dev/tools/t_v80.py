# v84: 진도 다 나가서 자습하는 과목 표시
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
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now='2026-11-10T20:00:00+09:00');close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="prog"]',600)
click(p,'[data-act="prog-mode"][data-id="me"]',500)
sid=ev(p,"document.querySelector('[data-act=\"self-tg\"]').dataset.id")
click(p,'[data-act="self-tg"][data-id="%s"]'%sid,600)
pr=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1']||{})"))
check('saved self',sid in pr.get('self',{}),pr.get('self'))
check('badge on my card',ev(p,"!!document.querySelector('#us-%s .selfb')"%sid))
check('button flips',ev(p,"document.querySelector('[data-act=\"self-tg\"][data-id=\"%s\"]').textContent"%sid)=='자습 끝내기')
click(p,'[data-act="prog-mode"][data-id="all"]',600)
check('all view count',('자습 1명' in ev(p,"document.querySelector('#pr-%s .pnm').textContent"%sid)),ev(p,"document.querySelector('#pr-%s .pnm').textContent"%sid))
click(p,'#pr-%s .phead'%sid,500)
check('person tag',ev(p,"document.querySelectorAll('#pp-%s .selfb').length"%sid)==1)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/self_all.png')
click(p,'[data-act="prog-mode"][data-id="me"]',500)
click(p,'[data-act="self-tg"][data-id="%s"]'%sid,600)
pr=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1']||{})"))
check('off removes',sid not in (pr.get('self') or {}))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
