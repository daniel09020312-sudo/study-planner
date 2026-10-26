import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
for w,h in [(915,412),(800,360),(1180,820)]:
    p=R.open(w,h,ls={'gbb_note':'9999999999999'});close_dlg(p)
    r=p.evaluate("()=>{const e=document.querySelector('.rail');e.scrollTop=9999;const m=document.getElementById('meBtn').getBoundingClientRect();return {sh:e.scrollHeight,ch:e.clientHeight,st:e.scrollTop,meBottom:Math.round(m.bottom),vh:innerHeight}}")
    print(w,h,r, 'me reachable', r['meBottom']<=r['vh'])
print('errors',R.errors);R.close()
