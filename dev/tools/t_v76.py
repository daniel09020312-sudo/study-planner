# v80: 순서 정리 창 끌어 옮기기, 여러 개 골라 옮기기
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
def store(p,k):return json.loads(ev(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
T='2026-11-04';T2='2026-11-05';P='2026-11-01'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_%s']={goals:[{id:'a',text:'A',sid:'s1',done:false},{id:'b',text:'B',sid:'s2',done:true},{id:'c',text:'C',sid:'s3',done:false},{id:'d',text:'D',sid:'s4',done:false}]};S['days/m1_%s']={goals:[{id:'x',text:'X',sid:'s1',done:false}]};clearInterval(t);},5);})();"%(T,T2)
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=T+'T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',700);click(p,'#c-wk [data-act="open"][data-modal="gorder"]',700)
def ids(d):return [g['id'] for g in (store(p,'days/m1_'+d) or {}).get('goals',[])]
def box(sel):return p.evaluate("(s)=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.height]}",sel)
def drag(src,dst,after=False):
    x,y,_=box('.gordi[data-id="%s"] .gdh'%src);tx,ty,h=box(dst)
    ty=ty+h*0.3 if after else ty-h*0.3
    p.mouse.move(x,y);p.mouse.down();p.mouse.move(x,y+5,steps=2);p.mouse.move(tx,ty,steps=8);p.wait_for_timeout(100);p.mouse.up();p.wait_for_timeout(600)
drag('d','.gordi[data-id="a"]')
check('drag to top same day',ids(T)==['d','a','b','c'],ids(T))
drag('a','.gordi[data-id="x"]',after=True)
check('drag to other day',ids(T)==['d','b','c'] and ids(T2)==['x','a'],(ids(T),ids(T2)))
check('moved goal reset done',[g for g in store(p,'days/m1_'+T2)['goals'] if g['id']=='a'][0].get('done')==False)
# 여러 개 고르기
click(p,'[data-act="go-sel"][data-id="b"]',300);click(p,'[data-act="go-sel"][data-id="c"]',300)
check('select bar',ev(p,"!!document.querySelector('.gselbar')") and '2개' in ev(p,"document.querySelector('.gselbar').textContent"))
click(p,'.gselbar [data-act="go-to"][data-date="%s"]'%T2,700)
check('multi move to date',ids(T)==['d'] and ids(T2)==['x','a','b','c'],(ids(T),ids(T2)))
click(p,'[data-act="go-sel"][data-id="c"]',300);click(p,'[data-act="go-sel"][data-id="a"]',300)
x,y,_=box('.gordi[data-id="a"] .gdh');tx,ty,h=box('.gordi[data-id="d"]')
p.mouse.move(x,y);p.mouse.down();p.mouse.move(x,y+5,steps=2);p.mouse.move(tx,ty-h*0.3,steps=8);p.wait_for_timeout(100);p.mouse.up();p.wait_for_timeout(700)
check('multi drag keeps order',ids(T)==['a','c','d'] and ids(T2)==['x','b'],(ids(T),ids(T2)))
check('selection cleared',not ev(p,"!!document.querySelector('.gselbar')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
