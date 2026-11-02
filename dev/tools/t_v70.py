# v71: 할 일 목록이 날짜로 이어지게 옆으로 스크롤
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
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now='2026-11-04T20:00:00+09:00');close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',600);click(p,'[data-act="cal-mode"][data-id="list"]',900)
def st():return ev(p,"(()=>{const s=document.getElementById('wkScroll');const fv=s.dataset.fv;const c=document.getElementById('wc-'+fv);return {title:document.getElementById('alTitle').textContent,fv:fv,n:s.querySelectorAll('.wkh').length,off:Math.round(c.offsetLeft-s.firstElementChild.offsetLeft-s.scrollLeft),cw:c.offsetWidth,vis:Math.round(s.clientWidth/c.offsetWidth)}})()")
a=st();print(a)
check('21 days rendered, 7 visible',a['n']==21 and a['vis']==7 and a['fv']=='2026-11-02' and abs(a['off'])<=1,a)
p.evaluate("()=>{const s=document.getElementById('wkScroll');const c=document.getElementById('wc-2026-11-02');s.scrollLeft+=c.offsetWidth*3;}");p.wait_for_timeout(700)
b=st();print(b)
check('scroll 3 days -> starts Thu',b['fv']=='2026-11-05' and abs(b['off'])<=1 and '11월 5일' in b['title'],b)
for k in range(3):
    p.evaluate("()=>{const s=document.getElementById('wkScroll');const c=s.querySelector('.wkh');s.scrollLeft+=s.querySelector('[id^=wc-]').offsetWidth*5;}");p.wait_for_timeout(700)
c=st();print(c)
check('keeps going across weeks',c['fv']=='2026-11-20' and abs(c['off'])<=1,c)
p.evaluate("()=>{const s=document.getElementById('wkScroll');s.scrollLeft-=s.querySelector('[id^=wc-]').offsetWidth*6;}");p.wait_for_timeout(700)
d=st();print(d)
check('scroll back',d['fv']=='2026-11-14',d)
click(p,'[data-act="al-week"][data-d="0"]',900)
check('this week button',st()['fv']=='2026-11-02',st())
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
