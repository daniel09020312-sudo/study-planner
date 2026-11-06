# v79: 할 일 순서 정리 창
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
T='2026-11-04';T2='2026-11-06'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_%s']={goals:[{id:'a',text:'생물',sid:'s7',done:true},{id:'b',text:'국어',sid:'s1',done:false},{id:'m',text:'옮김',sid:'s2',done:false,mv:1},{id:'c',text:'미적',sid:'s2',done:false}]};S['days/m1_%s']={goals:[{id:'x',text:'확통',sid:'s3',done:false},{id:'y',text:'국어2',sid:'s1',done:false}]};clearInterval(t);},5);})();"%(T,T2)
p=R.open(1180,900,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=T+'T20:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(800)
click(p,'[data-act="tab"][data-tab="cal"]',700)
click(p,'#c-wk [data-act="open"][data-modal="gorder"]',700)
secs=ev(p,"[...document.querySelectorAll('#dlg-gorder .gordd')].map(s=>s.id)")
check('shows several days',secs==['go-'+T,'go-'+T2],secs)
check('moved goal hidden',ev(p,"document.querySelectorAll('#go-%s .gordi').length"%T)==3)
def ids(d):return [g['id'] for g in store(p,'days/m1_'+d)['goals']]
click(p,'[data-act="go-mv"][data-date="%s"][data-id="c"][data-v="-1"]'%T,500)
check('move up skips moved slot',ids(T)==['a','c','m','b'],ids(T))
click(p,'[data-act="go-sort"][data-k="done"][data-date="%s"]'%T,500)
check('done last keeps mv slot',ids(T)==['c','b','m','a'],ids(T))
click(p,'[data-act="go-sort"][data-k="sub"][data-date="all"]',700)
check('all days subject order',ids(T)==['b','c','m','a'] and ids(T2)==['y','x'],(ids(T),ids(T2)))
click(p,'[data-act="go-r"][data-v="today"]',500)
check('range today',ev(p,"[...document.querySelectorAll('#dlg-gorder .gordd')].map(s=>s.id)")==['go-'+T])
click(p,'[data-act="go-left"]',500)
check('left only hides done',ev(p,"document.querySelectorAll('#go-%s .gordi.done').length"%T)==0)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
