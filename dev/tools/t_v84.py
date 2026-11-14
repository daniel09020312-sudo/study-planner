# v90: 노동요 기능 더하기
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
songs={'n1':{'mid':'m2','title':'로파이 집중','url':'https://youtu.be/abcDEF12345','mood':'집중','at':NOW-10*86400000},
       'n2':{'mid':'m3','title':'빗소리','url':'https://open.spotify.com/playlist/37i9dQZF1DX','at':NOW-86400000},
       'n3':{'mid':'m1','title':'멜론 차트','url':'https://www.melon.com/chart','at':NOW-5*86400000},
       'n4':{'mid':'m2','title':'피아노','url':'','at':NOW-4*86400000},
       'n5':{'mid':'m3','title':'재즈 카페','url':'https://www.youtube.com/watch?v=zzzYYY11111&list=PLabcdef123','at':NOW-6*86400000},
       'n6':{'mid':'m4','title':'백색소음','url':'','at':NOW-7*86400000}}
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('songs/')).forEach(k=>delete S[k]);var sg=%s;for(var k in sg)S['songs/'+k]=sg[k];var p=S['progress/m3']||{};p.sp={n3:5};p.liked={n4:true};S['progress/m3']=p;clearInterval(t);},5);})();"%json.dumps(songs)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',900)
check('song bar under timer',ev(p,"!!document.querySelector('#c-timer #songBar')"))
check('songs card first in right stack',ev(p,"(()=>{var s=document.getElementById('c-songs');return s&&s.parentElement.querySelector('.card:not(#c-quiet)')===s})()"))
titles=lambda:ev(p,"[...document.querySelectorAll('#c-songs .song .st')].map(e=>e.textContent)")
click(p,'[data-act="song-sort"][data-id="new"]',400)
check('newest first',titles()[0]=='빗소리',titles())
check('new tag only for recent',ev(p,"document.querySelectorAll('#c-songs .snew').length")==1)
click(p,'[data-act="song-sort"][data-id="play"]',400)
check('most played first',titles()[0]=='멜론 차트' and '5번 들음' in ev(p,"document.querySelector('#c-songs .song .smeta small').textContent"),titles())
p.fill('#c-songs .ssearch','재즈');p.wait_for_timeout(400)
check('search',titles()==['재즈 카페'],titles())
p.fill('#c-songs .ssearch','');p.wait_for_timeout(300)
click(p,'[data-act="song-sort"][data-id="top"]',300)
check('embed buttons for yt and spotify only',ev(p,"document.querySelectorAll('#c-songs [data-act=\"song-play\"]').length")==3)
click(p,'#c-songs [data-act="song-play"][data-id="n5"]',600)
src=ev(p,"(document.querySelector('#sply-n5 iframe')||{}).src||''")
check('youtube embed with list',src.startswith('https://www.youtube-nocookie.com/embed/zzzYYY11111') and 'list=PLabcdef123' in src,src)
pr=json.loads(ev(p,"JSON.stringify(window.__store['progress/m1'])"))
check('play counted and now set',pr.get('sp',{}).get('n5')==1 and pr.get('now',{}).get('id')=='n5',pr.get('sp'))
check('bar shows now playing','재즈 카페' in ev(p,"document.getElementById('songBar').textContent"))
click(p,'#c-songs [data-act="song-play"][data-id="n2"]',600)
check('spotify embed',ev(p,"(document.querySelector('#sply-n2 iframe')||{}).src||''")=='https://open.spotify.com/embed/playlist/37i9dQZF1DX')
check('only one player',ev(p,"document.querySelectorAll('.sply iframe').length")==1)
click(p,'#songBar [data-act="song-play"]',500)
check('bar player moves (still one)',ev(p,"document.querySelectorAll('.sply iframe').length")==1 and ev(p,"!!document.querySelector('#songBar .sply iframe')"))
click(p,'#songBar [data-act="song-play"]',400)
check('bar player closed',ev(p,"document.querySelectorAll('.sply iframe').length")==0)
click(p,'[data-act="song-sort"][data-id="mine"]',300)
check('my likes empty msg','좋아요' in ev(p,"document.querySelector('#c-songs .empty').textContent"))
click(p,'[data-act="song-sort"][data-id="top"]',300)
# 한마디와 올리기
p.fill('#songIn','새 노래');p.wait_for_timeout(300)
p.fill('#c-songs .snotein','영어 지문 읽을 때');p.focus('#songIn');p.keyboard.press('Enter');p.wait_for_timeout(500)
nw=ev(p,"JSON.stringify(Object.values(window.__store).filter(x=>x&&x.title==='새 노래')[0])")
check('note saved','영어 지문 읽을 때' in nw,nw)
check('note shown',ev(p,"[...document.querySelectorAll('#c-songs .snote')].some(e=>e.textContent.includes('영어 지문'))"))
click(p,'#songBar [data-act="song-pick"]',3500)
check('pick from bar','오늘은' in ev(p,"document.getElementById('songBar').textContent") or '듣는 중' in ev(p,"document.getElementById('songBar').textContent"),ev(p,"document.getElementById('songBar').textContent"))
# 타이머가 도는 동안 플레이어가 다시 만들어지지 않음
click(p,'[data-act="timer-start"]',800)
click(p,'#songBar [data-act="song-play"]',600)
ev(p,"(document.querySelector('#songBar .sply iframe').__keep=1,1)");p.wait_for_timeout(3500)
check('player kept while timer runs',ev(p,"!!(document.querySelector('#songBar .sply iframe')||{}).__keep"))
ev(p,"(document.getElementById('c-timer').scrollIntoView(),1)");p.wait_for_timeout(300)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/song1.png')
ev(p,"(document.getElementById('c-songs').scrollIntoView(),1)");p.wait_for_timeout(300)
p.screenshot(path='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/song2.png')
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
