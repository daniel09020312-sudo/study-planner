import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999'});close_dlg(p)
h=lambda:st(p,"document.querySelector('#view-cal h1').textContent")
click(p,'[data-act="month"][data-d="-1"]',500)
print('back         :',h(),'| prev disabled',st(p,"document.querySelector('[data-act=month][data-d=\"-1\"]').disabled"))
seen=[]
for i in range(20):
    if st(p,"document.querySelector('[data-act=month][data-d=\"1\"]').disabled"):break
    click(p,'[data-act="month"][data-d="1"]',250);seen.append(h())
print('forward      :',seen[0],'...',seen[-1],'| steps',len(seen),'| next disabled',st(p,"document.querySelector('[data-act=month][data-d=\"1\"]').disabled"))
p.screenshot(path=SH+'v22_dec2027.png')
click(p,'[data-act="cal-today"]',500);print('today        :',h())
# 할 일 주간 달력도 9월까지, 2027년 12월까지
click(p,'[data-act="cal-mode"][data-id="list"]',600)
n=0
while not st(p,"document.querySelector('[data-act=al-week][data-d=\"-1\"]').disabled") and n<20:
    click(p,'[data-act="al-week"][data-d="-1"]',200);n+=1
print('week first   :',st(p,"document.querySelector('.wkt').textContent"),'| steps back',n)
# 날짜 고르기 최대값
click(p,'[data-act="cal-mode"][data-id="cal"]',500)
print('date max     :',st(p,"[...new Set([...document.querySelectorAll('input[type=date]')].map(i=>i.max))].join(',')") or '(no inputs on screen)')
click(p,'[data-act="open"][data-modal="plan"]',600)
print('plan max     :',st(p,"[...new Set([...document.querySelectorAll('#dlg-plan input[type=date]')].map(i=>i.max))].join(',')"))
print('errors',R.errors)
R.close()
