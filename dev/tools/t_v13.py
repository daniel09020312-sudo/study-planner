import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
SEED=r"""()=>{
 const S=window.__store,T=(d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'));
 const add=(n)=>{const d=new Date();d.setDate(d.getDate()+n);return T(d);};
 let i=100;const g=(t,s,d,x)=>Object.assign({id:'q'+(i++),text:t,sid:s,done:d},x||{});
 S['plans/pA']={mid:'m1',mode:'split',type:'문제집 풀이',unit:'쪽',total:60,note:'쎈 3단원',due:add(6),start:add(1),dows:'1111111',at:Date.now()};
 S['days/m1_'+add(-5)]={goals:[g('개념 정리 1단원','s2',true),g('영단어 50개','s4',true)]};
 S['days/m1_'+add(-4)]={goals:[g('문제집 풀이 30문제','s3',true),g('오답 정리','s3',false),g('교과서와 프린트 복습','s5',true)]};
 S['days/m1_'+add(-3)]={goals:[g('기출 풀이 1회 (2025 1학기 중간)','s2',true)]};
 S['days/m1_'+add(-2)]={goals:[]};
 for(let k=1;k<=6;k++){const key='days/m1_'+add(k);S[key]={goals:[g('문제집 풀이 10쪽 (쎈 3단원)','s3',false,{pid:'pA',part:k+'/6',amt:10})]};}
 S['days/m1_'+add(1)].goals.push(g('수행평가 준비 (실험 보고서 초안)','s5',false),g('영어 지문 3개 분석','s4',false));
 S['days/m1_'+add(2)].goals.push(g('개념 정리','s6',false));
 S['days/m2_'+add(1)]={goals:[g('오답 정리 20문제','s2',false),g('암기','s7',false)]};
 window.__fire();return add(0);
}"""
R=Rig()
p=R.open(ls={'gbb_note':'9999999999999'});close_dlg(p)
T=p.evaluate(SEED);p.wait_for_timeout(600)
print('today',T)
print('seg in cal   :',st(p,"[...document.querySelectorAll('.cmode button')].map(b=>b.textContent+':'+b.getAttribute('aria-pressed')).join(' ')"))
click(p,'[data-act="cal-mode"][data-id="list"]',700)
print('title        :',st(p,"document.querySelector('.wkt').textContent"),'| ls',st(p,"localStorage.getItem('gbb_calmode')"))
print('strip        :',st(p,"[...document.querySelectorAll('.astrip button')].map(b=>b.textContent).join(' ')"))
print('summary      :',st(p,"document.querySelector('.alsum p').textContent"))
print('days         :',st(p,"[...document.querySelectorAll('.aday')].map(e=>e.querySelector('.ad b').textContent+'['+(e.querySelector('.acnt')||{textContent:'-'}).textContent+']').join(' ')"))
p.screenshot(path=SH+'v13_land_this.png',full_page=True)
# 오늘 할 일 하나 완료
gid=st(p,"(e=>e?e.getAttribute('data-id'):'')(document.querySelector('#ad-%s .arow:not(.done) .chk:not([disabled])'))"%T)
click(p,'#ad-%s .chk[data-id="%s"]'%(T,gid),600)
print('after toggle :',st(p,"document.querySelector('#ad-%s .acnt').textContent"%T),'| store',st(p,"JSON.stringify((window.__store['days/m1_%s'].goals||[]).map(g=>g.done))"%T))
# 다음 주
click(p,'[data-act="al-week"][data-d="1"]',600)
print('next title   :',st(p,"document.querySelector('.wkt').textContent"),'| this-week btn',st(p,"!!document.querySelector('[data-act=\"al-week\"][data-d=\"0\"]')"))
print('next days    :',st(p,"[...document.querySelectorAll('.aday')].map(e=>e.querySelector('.ad b').textContent.split(' ')[1]+'='+e.querySelectorAll('.arow').length+(e.querySelector('.adue')?'+due':'')).join(' ')"))
print('future chk disabled:',st(p,"[...document.querySelectorAll('.aday .chk')].every(b=>b.disabled)"))
p.screenshot(path=SH+'v13_land_next.png',full_page=True)
# 남은 일만
click(p,'[data-act="al-left"]',400)
print('left only    :',st(p,"document.querySelectorAll('.arow.done').length"),'| ls',st(p,"localStorage.getItem('gbb_alleft')"))
click(p,'[data-act="al-left"]',400)
# 다른 사람
click(p,'[data-act="al-who"][data-id="m2"]',500)
print('m2 view      :',st(p,"document.querySelector('.alsum p').textContent"),'| rows',st(p,"document.querySelectorAll('.arow').length"),'| btn chk',st(p,"document.querySelectorAll('.arow button.chk').length"),'| add btns',st(p,"document.querySelectorAll('.afoot').length"))
click(p,'[data-act="al-who"][data-id="m1"]',400)
# 할 일 눌러서 달력으로
rid=st(p,"document.querySelector('.atext[data-act=\"al-goal\"]').getAttribute('data-id')")
rd=st(p,"document.querySelector('.atext[data-act=\"al-goal\"]').getAttribute('data-d')")
click(p,'.atext[data-act="al-goal"][data-id="%s"]'%rid,900)
print('to cal       :',st(p,"!!document.querySelector('.calcard')"),'| sel date',st(p,"(document.querySelector('.cell.sel')||{}).getAttribute&&document.querySelector('.cell.sel').getAttribute('data-d')"),rd,'| acts',st(p,"!!document.getElementById('ga-%s')"%rid))
p.screenshot(path=SH+'v13_back_cal.png')
# 단축키 L
p.keyboard.press('l');p.wait_for_timeout(600)
print('key L        :',st(p,"!!document.querySelector('.agrid')"),'| week',st(p,"document.querySelector('.wkt').textContent"))
p.keyboard.press('l');p.wait_for_timeout(600)
print('key L again  :',st(p,"!!document.querySelector('.calcard')"))
p.keyboard.press('l');p.wait_for_timeout(600)
click(p,'[data-act="al-week"][data-d="0"]',500)
# 추가 버튼 -> 작성 창 날짜
fd=st(p,"(b=>b?b.getAttribute('data-date'):'')(document.querySelector('.afoot [data-modal=\"compose\"]'))")
print('add date     :',fd)
print('errors',R.errors)
for (w,h,n) in [(820,1180,'port'),(390,844,'phone')]:
    q=R.open(w,h,ls={'gbb_note':'9999999999999','gbb_calmode':'list'});close_dlg(q);q.evaluate(SEED);q.wait_for_timeout(700)
    print(n,'overflow',q.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1"),'| cols',q.evaluate("()=>getComputedStyle(document.querySelector('.agrid')).gridTemplateColumns.split(' ').length"))
    q.screenshot(path=SH+'v13_%s.png'%n,full_page=True)
    if n=='phone':
        click(q,'[data-act="al-jump"][data-d="%s"]'%T,900)
        print('jump top     :',q.evaluate("()=>Math.round(document.getElementById('ad-%s').getBoundingClientRect().top)"%T))
        q.screenshot(path=SH+'v13_phone_jump.png')
q=R.open(1180,820,scheme='dark',ls={'gbb_note':'9999999999999','gbb_calmode':'list'});close_dlg(q);q.evaluate(SEED);q.wait_for_timeout(700)
q.screenshot(path=SH+'v13_dark.png')
print('errors',R.errors)
R.close()
