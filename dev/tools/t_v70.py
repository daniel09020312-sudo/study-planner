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
def st():return ev(p,"(()=>{const s=document.getElementById('wkScroll');const fv=s.dataset.fv;const c=document.getElementById('wc-'+fv);return {title:fv,fv:fv,n:s.querySelectorAll('.wkh').length,off:Math.round(c.offsetLeft-s.firstElementChild.offsetLeft-s.scrollLeft),cw:c.offsetWidth,vis:Math.round(s.clientWidth/c.offsetWidth)}})()")
a=st();print(a)
check('21 days rendered, 7 visible',a['n']==21 and a['vis']==7 and a['fv']=='2026-11-02' and abs(a['off'])<=1,a)
p.evaluate("()=>{const h=document.getElementById('wh-2026-11-04');h.__tag=1;window.__swaps=0;new MutationObserver(m=>m.forEach(r=>{if(r.attributeName==='class'&&r.target.classList.contains('wkh'))window.__swaps++;})).observe(document.getElementById('wkScroll'),{attributes:true,subtree:true,attributeFilter:['class']});}")
p.evaluate("()=>{const s=document.getElementById('wkScroll');const c=document.getElementById('wc-2026-11-02');s.scrollLeft+=c.offsetWidth*3;}");p.wait_for_timeout(700)
b=st();print(b)
check('today header kept (no flicker)',ev(p,"(()=>{const h=document.getElementById('wh-2026-11-04');return !!(h&&h.__tag&&h.classList.contains('today'))&&window.__swaps===0})()"),ev(p,"window.__swaps"))
check('scroll 3 days -> starts Thu',b['fv']=='2026-11-05' and abs(b['off'])<=1 ,b)
for k in range(3):
    p.evaluate("()=>{const s=document.getElementById('wkScroll');const c=s.querySelector('.wkh');s.scrollLeft+=s.querySelector('[id^=wc-]').offsetWidth*4;}");p.wait_for_timeout(700)
c=st();print(c)
check('keeps going across weeks',c['fv']=='2026-11-17' and abs(c['off'])<=1,c)
p.evaluate("()=>{const s=document.getElementById('wkScroll');s.scrollLeft-=s.querySelector('[id^=wc-]').offsetWidth*6;}");p.wait_for_timeout(700)
d=st();print(d)
check('scroll back',d['fv']=='2026-11-11',d)
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='al-week';b.dataset.d='0';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(900)
check('this week button',st()['fv']=='2026-11-02',st())
check('no date title',ev(p,"!document.getElementById('alTitle')&&!document.querySelector('#view-cal .mnav h1')"))
# 오늘로 단추: 오늘이 안 보이면 나타남
p.evaluate("()=>{const s=document.getElementById('wkScroll');s.scrollLeft+=s.querySelector('[id^=wc-]').offsetWidth*6;}");p.wait_for_timeout(700)
check('today button when today hidden',ev(p,"!!document.querySelector('#view-cal .mnav [data-act=\"al-week\"]')"))
# 끄는 동안 옆 스크롤 막기
check('drag locks scroll',ev(p,"(()=>{document.documentElement.classList.add('wkdragging');const o=getComputedStyle(document.getElementById('wkScroll')).overflowX;document.documentElement.classList.remove('wkdragging');return o})()")=='hidden')
# 알림줄은 위에 떠서 본문을 밀지 않음
y0=ev(p,"document.getElementById('main').getBoundingClientRect().top")
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='al-left';document.body.appendChild(b);b.click();b.remove();}")
p.evaluate("()=>{document.getElementById('banner').innerHTML='<div class=\"flash\" role=\"status\"><span>시험 알림</span><button data-act=\"undo\">되돌리기</button></div>';}");p.wait_for_timeout(200)
y1=ev(p,"document.getElementById('main').getBoundingClientRect().top")
check('banner overlays (main not pushed)',abs(y0-y1)<1 and ev(p,"getComputedStyle(document.getElementById('banner')).position")=='absolute',(y0,y1))
# 휴대폰: 옆으로 넘겨도 세로 위치 그대로
PRE2="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;for(var i=0;i<20;i++){var d=new Date(2026,10,1+i),k=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');S['days/m1_'+k]={goals:Array.from({length:20},(_, j)=>({id:'g'+i+'_'+j,text:'할 일 '+j,sid:'s2',done:false}))};}clearInterval(t);},5);})();"
q=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now='2026-11-04T20:00:00+09:00',pre=PRE2);close_dlg(q);q.wait_for_timeout(1000)
q.evaluate("()=>{const b=document.querySelector('[data-act=\"tab\"][data-tab=\"cal\"]');if(b)b.click();}");q.wait_for_timeout(800)
q.evaluate("()=>{document.getElementById('main').scrollTop=300;}");q.wait_for_timeout(200)
for k in range(5):
    q.evaluate("()=>{const s=document.getElementById('wkScroll');s.scrollLeft+=128*2;}");q.wait_for_timeout(500)
check('phone keeps vertical position',q.evaluate("()=>document.getElementById('main').scrollTop")==300,q.evaluate("()=>[document.getElementById('main').scrollTop,document.getElementById('wkScroll').dataset.fv]"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
