# v91: 노동요 해시태그
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
       'n2':{'mid':'m1','title':'빗소리','url':'','mood':'신나는','tags':{'신나는':1,'새벽':1},'at':NOW-86400000}}
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('songs/')).forEach(k=>delete S[k]);var sg=%s;for(var k in sg)S['songs/'+k]=sg[k];clearInterval(t);},5);})();"%json.dumps(songs)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',900)
chips=lambda:ev(p,"[...document.querySelectorAll('#songFilter .chip')].map(e=>e.textContent)")
check('filter chips with # and counts',chips()==['전체 2','#집중 1','#신나는 1','#새벽 1'],chips())
click(p,'[data-act="song-filter"][data-id="새벽"]',400)
check('filter by extra tag',ev(p,"[...document.querySelectorAll('#c-songs .song .st')].map(e=>e.textContent)")==['빗소리'])
click(p,'[data-act="song-filter"][data-id=""]',300)
check('tags shown on song',ev(p,"[...document.querySelectorAll('#sg-n2 .stg')].map(e=>e.textContent)")==['#신나는','#새벽'])
# 올릴 때 여러 개
p.fill('#songIn','새 곡');p.wait_for_timeout(300)
check('many tag choices',ev(p,"document.querySelectorAll('#songNew [data-act=\"song-mood\"]').length")>=20)
for m in ['로파이','피아노','시험 직전','재즈']:click(p,'[data-act="song-mood"][data-id="%s"]'%m,200)
check('max 3 picked',ev(p,"document.querySelectorAll('#songNew [data-act=\"song-mood\"][aria-pressed=\"true\"]').length")==3)
p.focus('#songIn');p.keyboard.press('Enter');p.wait_for_timeout(500)
nw=json.loads(ev(p,"JSON.stringify(Object.values(window.__store).filter(x=>x&&x.title==='새 곡')[0])"))
check('saved tags',nw.get('mood')=='시험 직전' and sorted(nw.get('tags',{}).keys())==sorted(['로파이','피아노','시험 직전']),nw)
# 내 곡 태그 고치기
click(p,'#sg-n2 [data-act="song-tagedit"]',400)
click(p,'#sg-n2 [data-act="song-tagset"][data-v="새벽"]',400)
click(p,'#sg-n2 [data-act="song-tagset"][data-v="K-팝"]',400)
n2=json.loads(ev(p,"JSON.stringify(window.__store['songs/n2'])"))
check('edit tags',sorted(n2.get('tags',{}).keys())==['K-팝','신나는'] and n2['mood']=='신나는',n2)
check('no tag edit on others song',not ev(p,"!!document.querySelector('#sg-n1 [data-act=\"song-tagedit\"]')"))
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/tags.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
