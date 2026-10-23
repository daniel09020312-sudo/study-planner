# 잠금 화면에 공부 시간: 설정 켜기, 타이머 켜면 소리 없는 소리 + 재생 정보, 끄면 사라짐
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'});close_dlg(p)
click(p,'[data-act="tab"][data-tab="room"]',900)
def ev(js):return p.evaluate('()=>'+js)
print('row          :', ev("(document.querySelector('.lockbtn')||{}).innerText"), '| pressed', ev("(document.querySelector('.lockbtn')||{getAttribute:()=>null}).getAttribute('aria-pressed')"))
p.locator('.lockbtn').click();p.wait_for_timeout(500)
print('toggle on    :', ev("localStorage.getItem('gbb_lock')"), '| pressed', ev("document.querySelector('.lockbtn').getAttribute('aria-pressed')"))
# 타이머 켜기 (실제 누름)
btn=p.locator('[data-act="timer-start"]').first
print('start btn    :', btn.count())
btn.click();p.wait_for_timeout(1500)
print('showing      :', ev("__lk.showing"), '| audio paused', ev("__lk.a?__lk.a.paused:null"), '| meta', ev("navigator.mediaSession.metadata?navigator.mediaSession.metadata.title+' / '+navigator.mediaSession.metadata.artist:null"), '| state', ev("navigator.mediaSession.playbackState"))
p.screenshot(path=SH+'v30_room.png',full_page=True)
p.wait_for_timeout(2500)
print('tick keeps   :', ev("__lk.showing"), '| meta', ev("navigator.mediaSession.metadata&&navigator.mediaSession.metadata.title"))
ev("(()=>{const L=window.__store['live/m1'];if(L){L.start-=83*60000;L.flushed=L.start;L.cm=0;window.__fire();}return 1})()");p.wait_for_timeout(1600)
print('83 min later :', ev("navigator.mediaSession.metadata&&navigator.mediaSession.metadata.title"))
import base64
art=ev("navigator.mediaSession.metadata&&navigator.mediaSession.metadata.artwork[0]&&navigator.mediaSession.metadata.artwork[0].src")
print('artwork      :', (art or '')[:30], len(art or ''))
if art and art.startswith('data:image/png;base64,'):open(SH+'v30_art.png','wb').write(base64.b64decode(art.split(',',1)[1]))
# 잠금 화면의 일시정지 (pause 처리)
ev("(__lk.a.pause(),0)");p.wait_for_timeout(300)
print('lock pause   :', ev("__lk.showing"), '| meta', ev("navigator.mediaSession.metadata"))
# 타이머 끄기
st=p.locator('[data-act="timer-stop"]').first
if st.count():st.click();p.wait_for_timeout(1200)
print('timer off    :', ev("!!(view().live&&view().live[view().me])") if False else ev("__lk.showing"))
# 설정 끄기
p.locator('.lockbtn').click();p.wait_for_timeout(400)
print('toggle off   :', ev("localStorage.getItem('gbb_lock')"))
print('errors',R.errors)
R.close()
