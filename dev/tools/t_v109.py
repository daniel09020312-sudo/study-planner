# v109: 술 취한 숫자 타이머가 돌아가는 동안 화면(스크롤)이 저절로 밀리지 않음
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
R=Rig();p=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_tstyle':'drunk'},now=datetime.datetime(2026,11,23,15,0,0));close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="room"]',700);click(p,'.btn.xl[data-act="timer-start"]',800)
p.mouse.wheel(0,300);p.wait_for_timeout(500)
a=p.evaluate("()=>document.querySelector('#main').scrollTop");p.wait_for_timeout(12000)
b=p.evaluate("()=>document.querySelector('#main').scrollTop")
print(('OK  ' if a==b else 'FAIL'),'scroll stays',a,b);ok=a==b
print('errors',R.errors);ok=ok and not R.errors
R.close();print('ALL OK' if ok else 'SOME FAILED')
