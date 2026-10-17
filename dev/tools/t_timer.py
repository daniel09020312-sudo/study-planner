import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
CLOCK="(function(){const R=Date.now.bind(Date);window.__off=0;Date.now=()=>R()+window.__off;})();"
R=Rig();p=R.open(ls={'gbb_note':'1'},pre=CLOCK);close_dlg(p)
st=lambda expr:p.evaluate('()=>'+expr)
def adv(mins,wait=1400):
    p.evaluate("m=>{window.__off+=m*60000;}",mins);p.wait_for_timeout(wait)
mins=lambda sid='s1': st("(window.__store['days/m1_'+(d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'))(new Date())].mins||{})['%s']||0"%sid)
live=lambda: st("JSON.stringify((l=>l&&Object.assign({},l,{start:'t',flushed:'t',run:l.run?'t':undefined}))(window.__store['live/m1']||null))")
ring=lambda: st("(e=>e?e.className+' | '+e.querySelector('.rg-in').innerText.replace(/\\n/g,' / '):'(no ring)')(document.querySelector('#c-timer .ring'))")
flash=lambda: st("(document.querySelector('.flash')||{}).textContent||''")
me_line=lambda: st("(e=>e?e.textContent:'')([...document.querySelectorAll('#c-people .fr')].filter(e=>e.textContent.includes('민준'))[0].querySelector('small.live'))")
click(p,'[data-tab="room"]',900)
print('idle sw    :',st("document.querySelector('#c-timer .tt').textContent"),'| seg:',st("[...document.querySelectorAll('.tseg button')].map(b=>b.textContent+(b.getAttribute('aria-pressed')==='true'?'*':'')).join(' ')"))
p.screenshot(path=SH+'t_00_sw_idle.png')
# 뽀모도로 설정
click(p,'[data-act="tmode"][data-v="pomo"]',300);print('pomo idle  :',ring())
click(p,'[data-act="pomo-custom"]',250);click(p,'[data-act="pomo-adj"][data-k="f"][data-d="5"]',150);click(p,'[data-act="pomo-adj"][data-k="b"][data-d="-1"]',150)
print('custom     :',ring(),'| stored',st("localStorage.getItem('gbb_pomo')"))
p.screenshot(path=SH+'t_01_pomo_custom.png')
click(p,'[data-act="pomo-set"][data-f="25"]',250);print('preset     :',ring())
p.screenshot(path=SH+'t_02_pomo_idle.png')
# 시작
click(p,'[data-act="timer-start"]',500);print('started    :',live(),'|',ring(),'| seg gone:',st("!document.querySelector('.tseg')"))
adv(12);print('+12m       : mins',mins(),'|',ring(),'|',live())
p.screenshot(path=SH+'t_03_pomo_focus.png')
adv(13.5);print('+25.5m rest: mins',mins(),'|',ring(),'| flash:',flash(),'| me:',me_line(),'| header:',st("document.querySelector('#c-people .ct small').textContent"))
p.screenshot(path=SH+'t_04_pomo_rest.png')
adv(4.7);print('+30.2m     : mins',mins(),'|',ring(),'| flash:',flash(),'| me:',me_line())
adv(25);print('+55.2m rest: mins',mins(),'|',ring())
click(p,'[data-act="pomo-skip"]',500);print('skip       :',live(),'|',ring())
adv(3.2);
# 크게 보기
click(p,'[data-act="focus-open"]',500);print('big view   :',st("(e=>e?e.querySelector('.rg-in').innerText.replace(/\\n/g,' / ')+' | '+[...e.querySelectorAll('button')].map(b=>b.textContent).join(', '):'(none)')(document.querySelector('.fview'))"),'| layer:',st("document.getElementById('layer')?document.getElementById('layer').className:document.querySelector('.layer').className"))
p.screenshot(path=SH+'t_05_big_pomo.png')
click(p,'.fview [data-act="timer-stop"]',500);print('stop in big: mins',mins(),'| live',live(),'| modal',st("!!document.querySelector('.fview')"))
# 목표 시간
click(p,'[data-act="tmode"][data-v="goal"]',300);print('goal idle  :',ring())
click(p,'[data-act="goal-custom"]',200);click(p,'[data-act="goal-adj"][data-d="10"]',150);print('goal custom:',ring())
click(p,'[data-act="goal-set"][data-v="30"]',250);p.screenshot(path=SH+'t_06_goal_idle.png')
m0=mins();click(p,'[data-act="timer-start"]',500);adv(20);print('goal +20m  : mins +',mins()-m0,'|',ring(),'| me:',me_line())
p.screenshot(path=SH+'t_07_goal_run.png')
adv(10.2);print('goal done  : mins +',mins()-m0,'| live',live(),'| flash:',flash(),'|',ring())
# 스톱워치
click(p,'[data-act="tmode"][data-v="sw"]',300);m0=mins();click(p,'[data-act="timer-start"]',500);print('sw doc     :',live())
adv(12);print('sw +12m    : mins +',mins()-m0,'|',live(),'| clock',st("document.querySelector('#c-timer .tt').textContent"),'| me:',me_line())
click(p,'[data-act="focus-open"]',500);p.screenshot(path=SH+'t_08_big_sw.png');click(p,'.fview [data-act="modal-close"]',500)
adv(1.6);click(p,'#c-timer [data-act="timer-stop"]',500);print('sw stop    : mins +',mins()-m0,'| live',live())
# 예전 방식 기록(cm 없음)으로 켜져 있던 타이머
p.evaluate("()=>{const n=Date.now();window.__store['live/m1']={sid:'s1',start:n-37*60000,flushed:n-4*60000};window.__fire();}");p.wait_for_timeout(500)
m0=mins();click(p,'#c-timer [data-act="timer-stop"]',500);print('legacy stop: mins +',mins()-m0)
# 다른 사람 상태
p.evaluate("()=>{const n=Date.now();window.__store['live/m3']={sid:'s3',mode:'pomo',f:25,b:5,start:n-27*60000,flushed:n,cm:25};window.__store['live/m4']={sid:'s5',mode:'goal',g:30,start:n-40*60000,flushed:n,cm:0};window.__store['live/m5']={sid:'s7',mode:'goal',g:60,start:n-10*60000,flushed:n,cm:0};window.__fire();}");p.wait_for_timeout(600)
print('others     :',st("[...document.querySelectorAll('#c-people .fr')].map(e=>e.querySelector('b').textContent+': '+((e.querySelector('small.live')||{}).textContent||'(꺼짐)')).join(' | ')"),'|',st("document.querySelector('#c-people .ct small').textContent"))
p.evaluate("()=>document.getElementById('c-people').scrollIntoView()");p.wait_for_timeout(300);p.screenshot(path=SH+'t_09_people.png')
# 5시간 상한 (뽀모도로)
click(p,'[data-act="tmode"][data-v="pomo"]',300);m0=mins();click(p,'[data-act="timer-start"]',500)
adv(301,2000);print('pomo cap   : mins +',mins()-m0,'| live',live(),'| flash:',flash(),'| flags:',st("JSON.stringify(Object.keys(window.__store).filter(k=>k.startsWith('flags/')).map(k=>window.__store[k].why))"))
# 달력 홈
click(p,'[data-act="tmode"][data-v="pomo"]',300);click(p,'[data-act="timer-start"]',400);adv(26)
click(p,'[data-tab="cal"]',900);print('home card  :',st("(document.querySelector('#c-now .what')||{}).textContent"))
print('errors:',R.errors);R.close()
