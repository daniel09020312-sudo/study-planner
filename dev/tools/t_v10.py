import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
CLOCK="(function(){const R=Date.now.bind(Date);window.__off=0;Date.now=()=>R()+window.__off;})();"
def st(p,e):return p.evaluate('()=>'+e)
def lines(p,sel):
    return st(p,"[...document.querySelectorAll('%s')].map(e=>{const cs=getComputedStyle(e),fs=parseFloat(cs.fontSize);return e.textContent+' '+Math.round(fs)+'px h'+Math.round(e.getBoundingClientRect().height)+(e.getBoundingClientRect().height>fs*1.8?' WRAP':'')+(e.scrollWidth>e.clientWidth+1?' OVER':'')}).join(' | ')"%sel)
STY=['ring','digits','bar','pie','flip']
R=Rig()
for w,h,sc,tag in [(1180,820,1,'L'),(390,800,2,'P')]:
    for sty in STY:
        p=R.open(w=w,h=h,scale=sc,ls={'gbb_note':'9999999999999','gbb_tstyle':sty,'gbb_tmode':'goal','gbb_goal':'90'},pre=CLOCK);close_dlg(p)
        click(p,'[data-tab="room"]',800)
        idle=lines(p,'#c-timer .tt')
        click(p,'[data-act="timer-start"]',600)
        p.evaluate("()=>{window.__off+=3*60000+20000}");p.wait_for_timeout(1300)
        run=lines(p,'#c-timer .tt')
        p.evaluate("()=>document.getElementById('c-timer').scrollIntoView()");p.wait_for_timeout(200)
        p.screenshot(path=SH+'v_%s_%s_goal.png'%(tag,sty))
        click(p,'[data-act="focus-open"]',600)
        big=lines(p,'.fview .tt')
        p.screenshot(path=SH+'v_%s_%s_big.png'%(tag,sty))
        click(p,'.fview [data-act="timer-stop"]',500)
        # 스톱워치
        click(p,'[data-act="tmode"][data-v="sw"]',300);click(p,'[data-act="timer-start"]',500)
        p.evaluate("()=>{window.__off+=72*60000}");p.wait_for_timeout(1300)
        sw=lines(p,'#c-timer .tt')
        p.screenshot(path=SH+'v_%s_%s_sw.png'%(tag,sty))
        click(p,'#c-timer [data-act="timer-stop"]',400)
        # 뽀모도로 쉬는 시간
        click(p,'[data-act="tmode"][data-v="pomo"]',300);click(p,'[data-act="timer-start"]',500)
        p.evaluate("()=>{window.__off+=26*60000}");p.wait_for_timeout(1300)
        pr=lines(p,'#c-timer .tt')
        prog=st(p,"(e=>e?(e.getAttribute('d')||e.style.width||e.style.strokeDashoffset):'-')(document.querySelector('#c-timer [data-lvp]'))")
        p.screenshot(path=SH+'v_%s_%s_rest.png'%(tag,sty))
        click(p,'#c-timer [data-act="timer-stop"]',400)
        print(tag,sty,'\n  idle:',idle,'\n  goal:',run,'\n  big :',big,'\n  sw  :',sw,'\n  rest:',pr,'| prog',str(prog)[:40],'| errors',R.errors)
        p.context.close()
R.close()
