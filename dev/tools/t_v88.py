# v94: 노동요 방장 보기, 최종 결과 방장 승인 뒤 공개 연출
import sys,json,time
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
SS='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/'
NOW=int(time.time()*1000)
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['songs/n1']={mid:'m2',title:'로파이',url:'',at:%d};var p=S['progress/m2']||{};p.sp={n1:3};p.liked={n1:true};S['progress/m2']=p;clearInterval(t);},5);})();"%NOW
# 노동요 방장 보기 (m1이 방장)
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',800)
check('admin toggle shown',ev(p,"!!document.querySelector('[data-act=\"song-adm\"]')"))
click(p,'[data-act="song-adm"]',400)
t=ev(p,"document.getElementById('c-songs').textContent")
check('who listened and liked','들음: 로파이 3번' in t and '좋아요: 로파이' in t,t[:300])
check('per song line',ev(p,"(document.querySelector('#sg-n1 .sadmr')||{}).textContent||''").startswith('들은 사람:'))
R.close()
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999','gbb_me':'m2'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',800)
check('not admin: no toggle',ev(p,"(window.__me=document.querySelector('[data-act=\"song-adm\"]'),!window.__me)"),ev(p,"document.querySelector('#meBtn')&&document.querySelector('#meBtn').textContent"))
R.close()
SEEDF="(function(){var t=setInterval(function(){var S=window.__store;if(!S||!S['meta/config'])return;var ms=Object.keys(S['meta/config'].roster||{}).length?S['meta/config'].roster.map(function(m){return m.id;}):['m1','m2','m3','m4','m5'];var d0=new Date('2026-11-02T12:00:00+09:00').getTime();ms.forEach(function(m,i){for(var k=0;k<(4+i*3)%13+2;k++){var dt=new Date(d0+k*86400000*2),ds=dt.toISOString().slice(0,10);S['days/'+m+'_'+ds]={mins:{s1:60+i*40+k*7},in:dt.getTime(),certAt:dt.getTime()+3600000,goals:[{id:'g1',text:'a',sid:'s1',done:true},{id:'g2',text:'b',sid:'s1',done:true},{id:'g3',text:'c',sid:'s2',done:true}]};}});%sclearInterval(t);},5);})();"
# 최종 결과
R=Rig();p=R.open(1280,900,ls={'gbb_note':'9999999999999'},now='2026-12-10T10:00:00+09:00',pre='window.WebGLRenderingContext=undefined;'+SEEDF.replace("%s",""));close_dlg(p);p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="rank"]',600);click(p,'[data-act="range"][data-id="all"]',600)
check('not revealed before approval',not ev(p,"!!document.getElementById('c-fin')") and ev(p,"!!document.getElementById('c-fin-wait')"))
check('admin approve card',ev(p,"!!document.getElementById('c-fin-ok')"))
click(p,'[data-act="fin-ok"]',300);click(p,'[data-act="fin-ok"]',900)
check('approved saved',bool(json.loads(ev(p,"JSON.stringify(window.__store['meta/config'].finalOk||null)"))))
p.wait_for_timeout(1500)
check('no 2D reveal, results shown directly',not ev(p,"!!document.getElementById('dlg-finrev')") and not ev(p,"!!document.querySelector('.f3')") and ev(p,"!!document.getElementById('c-fin')"))
check('results visible after',ev(p,"!!document.getElementById('c-fin')") and ev(p,"!!document.querySelector('.fincut')"))
p.reload();p.wait_for_timeout(1500);close_dlg(p) if False else None
check('not shown again on reload',not ev(p,"!!document.getElementById('dlg-finrev')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close()
R=Rig();p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-12-10T10:00:00+09:00',pre='window.WebGLRenderingContext=undefined;'+SEEDF.replace("%s","S['meta/config'].finalOk={at:1,by:'m1'};"));p.wait_for_timeout(1500)
check('no 2D modal for others either',not ev(p,"!!document.getElementById('dlg-finrev')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
