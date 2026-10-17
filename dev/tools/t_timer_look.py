import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
from PIL import Image
SH='/home/claude/planner/shots/'
CLOCK="(function(){const R=Date.now.bind(Date);window.__off=0;Date.now=()=>R()+window.__off;})();"
def run(name,w,h,scale,ls,scheme='light'):
    R=Rig();base={'gbb_note':'9999999999999','gbb_tmode':'pomo'};base.update(ls)
    p=R.open(w=w,h=h,scale=scale,ls=base,pre=CLOCK,scheme=scheme);close_dlg(p)
    click(p,'[data-tab="room"]',900)
    p.screenshot(path=SH+'tl_%s_idle.png'%name)
    click(p,'[data-act="timer-start"]',400);p.evaluate("()=>{window.__off+=7.3*60000}");p.wait_for_timeout(1500)
    p.screenshot(path=SH+'tl_%s_run.png'%name)
    click(p,'[data-act="focus-open"]',600);p.screenshot(path=SH+'tl_%s_big.png'%name)
    print(name,'overflow:',p.evaluate("()=>document.documentElement.scrollWidth>innerWidth"),'errors:',R.errors);R.close()
run('phone',390,800,2,{})
run('board',1024,768,1,{'gbb_concept':'board','gbb_accent':'p-mint'})
run('pop',1024,768,1,{'gbb_concept':'pop','gbb_accent':'p-pink'})
run('glass',1024,768,1,{'gbb_concept':'glass','gbb_accent':'purple'})
run('night',1024,768,1,{'gbb_concept':'night','gbb_accent':'p-butter'})
run('dark',1024,768,1,{'gbb_theme':'dark'},scheme='dark')
