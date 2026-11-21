# v91: 노동요 태그 직접 만들기
import sys,json,time
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
NOW=int(time.time()*1000)
songs={'n1':{'mid':'m2','title':'로파이 집중','url':'','mood':'집중','at':NOW-10*86400000},
       'n2':{'mid':'m1','title':'빗소리','url':'','mood':'신나는','tags':{'신나는':1,'수학':1},'at':NOW-86400000}}
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('songs/')).forEach(k=>delete S[k]);var sg=%s;for(var k in sg)S['songs/'+k]=sg[k];clearInterval(t);},5);})();"%json.dumps(songs)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',900)
chips=lambda:ev(p,"[...document.querySelectorAll('#songFilter .chip')].map(e=>e.textContent)")
check('filter chips incl custom',chips()==['전체 2','#집중 1','#신나는 1','#수학 1'],chips())
click(p,'[data-act="song-filter"][data-id="수학"]',400)
check('filter by custom tag',ev(p,"[...document.querySelectorAll('#c-songs .song .st')].map(e=>e.textContent)")==['빗소리'])
click(p,'[data-act="song-filter"][data-id=""]',300)
p.fill('#songIn','새 곡');p.wait_for_timeout(300)
check('only 5 preset tags',ev(p,"document.querySelectorAll('#songNew [data-act=\"song-mood\"]').length")==5)
click(p,'[data-act="song-mood"][data-id="집중"]',200)
p.fill('#songNew .stagin input','#영어 듣기');p.keyboard.press('Enter');p.wait_for_timeout(300)
check('typed tag added as chip',ev(p,"[...document.querySelectorAll('#songNew [data-act=\"song-mood\"][aria-pressed=\"true\"]')].map(e=>e.textContent)")==['#집중','#영어 듣기'],ev(p,"[...document.querySelectorAll('#songNew [data-act=\"song-mood\"][aria-pressed=\"true\"]')].map(e=>e.textContent)"))
p.fill('#songNew .stagin input','밤');click(p,'#songNew .stagin [data-act="song-tagnew"]',300)
p.fill('#songNew .stagin input','넷째');p.keyboard.press('Enter');p.wait_for_timeout(300)
check('max 3',ev(p,"document.querySelectorAll('#songNew [data-act=\"song-mood\"][aria-pressed=\"true\"]').length")==3)
p.focus('#songIn');p.keyboard.press('Enter');p.wait_for_timeout(500)
nw=json.loads(ev(p,"JSON.stringify(Object.values(window.__store).filter(x=>x&&x.title==='새 곡')[0])"))
check('saved custom tags',sorted(nw.get('tags',{}).keys())==sorted(['영어 듣기','밤','집중']) and nw['mood']=='집중',nw)
click(p,'#sg-n2 [data-act="song-x"]',400)
click(p,'#sg-n2 [data-act="song-tagedit"]',400)
click(p,'#sg-n2 [data-act="song-tagset"][data-v="수학"]',400)
p.fill('#sg-n2 .stagin input','새벽 공부');p.keyboard.press('Enter');p.wait_for_timeout(400)
n2=json.loads(ev(p,"JSON.stringify(window.__store['songs/n2'])"))
check('edit input cleared',ev(p,"document.querySelector('#sg-n2 .stagin input').value")=='')
check('edit: remove and add custom',sorted(n2.get('tags',{}).keys())==['새벽 공부','신나는'],n2)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/tags2.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
