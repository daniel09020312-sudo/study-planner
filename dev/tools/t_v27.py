# 점수 규칙: 묶음별(매일, 매주, 시험 끝나고) 항목과 점수
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
for w,h,tag in [(1180,820,'pc'),(390,844,'phone')]:
    p=R.open(w,h,ls={'gbb_note':'9999999999999'});close_dlg(p)
    p.wait_for_timeout(1500)
    click(p,'[data-act="tab"][data-tab="rank"]',900)
    print(tag,'groups',p.evaluate("()=>[...document.querySelectorAll('#c-rules .rlg h4')].map(e=>e.textContent).join(',')"),'| rows',p.evaluate("()=>document.querySelectorAll('#c-rules .rlg li').length"),'| overflow',p.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1"))
    print(tag,'first',p.evaluate("()=>[...document.querySelectorAll('#c-rules .rlg li')].slice(0,3).map(e=>e.innerText.replace(/\\n/g,' / ')).join(' | ')"))
    p.evaluate("()=>document.getElementById('c-rules').scrollIntoView()");p.wait_for_timeout(300)
    p.locator('#c-rules').screenshot(path=SH+'v27_rules_%s.png'%tag)
    click(p,'#meBtn',700)
    print(tag,'settings rules',p.evaluate("()=>document.querySelectorAll('.dialog .rlz li').length"))
print('errors',R.errors)
R.close()
