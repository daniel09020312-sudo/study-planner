# v74: 할 일 과목순 정렬, 오래된 '다른 날로 옮김' 숨김
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
T='2026-11-04'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_%s']={goals:[{id:'a',text:'생물',sid:'s7',done:false},{id:'b',text:'메모',sid:'',done:false},{id:'c',text:'국어',sid:'s1',done:false},{id:'d',text:'미적',sid:'s2',done:false},{id:'e',text:'국어2',sid:'s1',done:false}]};S['days/m1_2026-11-01']={goals:[{id:'o1',text:'옛날 옮김',sid:'s2',done:false,mv:1}]};S['days/m1_2026-11-02']={goals:[{id:'o2',text:'그제 옮김',sid:'s2',done:false,mv:1}]};clearInterval(t);},5);})();"%T
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=T+'T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1000)
click(p,'[data-act="tab"][data-tab="cal"]',800)
def order():return ev(p,"[...document.querySelectorAll('#wc-%s .wki .t')].map(e=>e.textContent)"%T)
print(order())
check('original order',order()==['생물','메모','국어','미적','국어2'],order())
click(p,'[data-act="al-sort"]',700)
check('subject order',order()==['국어','국어2','미적','생물','메모'],order())
check('old moved hidden',ev(p,"!document.getElementById('wi-o1-mv')"))
check('two-day-old moved shown',ev(p,"!!document.getElementById('wi-o2-mv')"))
click(p,'[data-act="al-sort"]',700)
check('toggle off',order()==['생물','메모','국어','미적','국어2'],order())
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
