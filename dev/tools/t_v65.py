# v62: 순위 보너스 없음(하루, 주간), 순위 기록은 그대로
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now='2026-11-12T12:00:00+09:00');close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="report"]',900)
sc=ev(p,"[...document.querySelectorAll('[id^=\"c-rpts\"] .hb')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
check('no rank bonus row in report','순위 보너스' not in sc,sc[:200])
click(p,'[data-act="tab"][data-tab="rank"]',900)
click(p,'[data-act="range"][data-id="all"]',900)
txt=ev(p,"document.querySelector('#view-rank, .view').innerText")
check('weekly record without points','기록만, 점수 없음' in txt and '1등 100점' not in txt)
check('no week bonus tag','+100' not in txt and '+60' not in txt)
click(p,'#meBtn',600)
rt=ev(p,"(document.querySelector('.rlz')||{innerText:''}).innerText")
print(rt[:400])
check('rules without rank items','하루 순위' not in rt and '주간 순위' not in rt)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
