# v102: 노동요 들은 횟수(1분 넘게 들어야, 30분에 한 번), 반 전체 목표 단계별 잉크, 상점 테두리·칭호 장식·히든
import sys,json,time,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
NOW=datetime.datetime(2026,11,20,15,0,0)
songs={'n1':{'mid':'m2','title':'로파이','url':'https://youtu.be/abcDEF12345','at':1},'n2':{'mid':'m3','title':'멜론','url':'https://www.melon.com/x','at':2}}
def pre(extra=''):
    return "window.__SP_MIN=1500;(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('songs/')).forEach(k=>delete S[k]);var sg=%s;for(var k in sg)S['songs/'+k]=sg[k];%sclearInterval(t);},5);})();"%(json.dumps(songs),extra)
sp=lambda p,id:ev(p,"+(((window.__store['progress/m1']||{}).sp||{})['%s']||0)"%id)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre());close_dlg(p);p.wait_for_timeout(400)
click(p,'[data-tab="room"]',800)
click(p,'#c-songs [data-act="song-play"][data-id="n1"]',300)
check('no count right away',sp(p,'n1')==0)
p.wait_for_timeout(1800)
check('count after listening',sp(p,'n1')==1,sp(p,'n1'))
click(p,'#c-songs [data-act="song-play"][data-id="n1"]',300);click(p,'#c-songs [data-act="song-play"][data-id="n1"]',300);p.wait_for_timeout(1800)
check('no double count within 30 min',sp(p,'n1')==1,sp(p,'n1'))
click(p,'#c-songs [data-act="song-play"][data-id="n1"]',300)
# 링크: 잠깐 갔다 오면 안 셈, 오래 있다 오면 셈
def back(p,ms):
    p.evaluate("(ms)=>{const L=window.__lastOpen=Date.now();}",ms)
p.evaluate("()=>{const a=document.querySelector('#c-songs a[data-act=\"song-open\"][data-id=\"n2\"]');a.removeAttribute('href');a.click();}");p.wait_for_timeout(300)
p.evaluate("()=>{Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'visible'});document.dispatchEvent(new Event('visibilitychange'));}");p.wait_for_timeout(300)
check('quick link visit not counted',sp(p,'n2')==0)
p.evaluate("()=>{const a=document.querySelector('#c-songs a[data-act=\"song-open\"][data-id=\"n2\"]');a.removeAttribute('href');a.click();}");p.wait_for_timeout(1800)
p.evaluate("()=>{document.dispatchEvent(new Event('visibilitychange'));}");p.wait_for_timeout(300)
check('long link visit counted',sp(p,'n2')==1,sp(p,'n2'))
check('row shows total label','모두 1번' in ev(p,"document.getElementById('sg-n1').textContent"))
R.close()
# 반 전체 목표: 목표 50시간의 160% -> 45방울 단계
seed="var D=['2026-11-16','2026-11-17','2026-11-18','2026-11-19'];['m2','m3','m4','m5'].forEach(function(m){D.forEach(function(d){S['days/'+m+'_'+d]={mins:{s1:300},in:d+'T08:00:00+09:00',goals:[]};});});"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre(seed));close_dlg(p);p.wait_for_timeout(400)
click(p,'[data-tab="room"]',800)
tag=ev(p,"(document.querySelector('#c-cg .ct .tag')||{}).textContent||''")
check('tier tag shows ink',tag.startswith('지금 +'),tag)
check('tier markers',ev(p,"document.querySelectorAll('#c-cg .cgbar2 b.on').length")>=2,ev(p,"document.getElementById('c-cg').textContent")[:200])
R.close()
# 상점: 테두리 쓰기, 히든 열림
own="var p=S['progress/m1']||{};p.shop={own:{'r:mint':50},gf:1};S['progress/m1']=p;"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre(own));close_dlg(p);p.wait_for_timeout(400)
click(p,'#shopBtn',600);click(p,'[data-act="shop-cat"][data-v="ring"]',500)
check('hidden locked',ev(p,"!!document.querySelector('#shi-r-blaze.hid2')"))
click(p,'#shi-r-mint [data-act="shop-use"]',500)
check('deco saved',ev(p,"((window.__store['progress/m1']||{}).deco||{}).r")=='mint')
check('my avatar ring',ev(p,"!!document.querySelector('.av.rg-mint')"))
R.close()
d12="S['days/m1_2026-11-18']={mins:{s1:400,s2:400},in:'2026-11-18T09:00:00+09:00',goals:[]};"
R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=NOW,pre=pre(d12));close_dlg(p);p.wait_for_timeout(400)
click(p,'#shopBtn',600);click(p,'[data-act="shop-cat"][data-v="ring"]',500)
check('hidden opens after 12h day',ev(p,"!!document.querySelector('#shi-r-blaze')&&!document.querySelector('#shi-r-blaze.hid2')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
