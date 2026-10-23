# 잠금 화면에 공부 시간: 설정 켜기, 타이머 켜면 소리 없는 소리 + 재생 정보,
# 잠금 화면에서 멈추면 타이머도 끄고 기록, 재생하면 같은 과목/방식으로 다시 시작, 다른 소리에 끊기면 비켜 줌
import sys,json,base64
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
# 잠금 화면 단추를 시험에서 누를 수 있게 등록된 처리를 모아 둔다
PRE="(function(){try{var ms=navigator.mediaSession,o=ms.setActionHandler.bind(ms);window.__msh={};ms.setActionHandler=function(k,f){window.__msh[k]=f;try{o(k,f);}catch(e){}};}catch(e){}})();"
p=R.open(390,844,ls={'gbb_note':'9999999999999'},pre=PRE,now='2026-10-21T19:00:00+09:00');close_dlg(p)
click(p,'[data-act="tab"][data-tab="room"]',900)
def ev(js):return p.evaluate('()=>'+js)
def meta():return ev("navigator.mediaSession.metadata?navigator.mediaSession.metadata.title+' / '+navigator.mediaSession.metadata.artist:null")
def live():return json.loads(ev("JSON.stringify(window.__store['live/m1']||null)"))
def mins():
    d=json.loads(ev("JSON.stringify(window.__store['days/m1_2026-10-21']||null)")) or {}
    return d.get('mins')
def save_art(name):
    art=ev("navigator.mediaSession.metadata&&navigator.mediaSession.metadata.artwork[0]&&navigator.mediaSession.metadata.artwork[0].src")
    if art and art.startswith('data:image/png;base64,'):open(SH+name,'wb').write(base64.b64decode(art.split(',',1)[1]))
    return len(art or '')
print('row          :', ev("(document.querySelector('.lockbtn')||{}).innerText"))
p.locator('.lockbtn').click();p.wait_for_timeout(500)
print('toggle on    :', ev("localStorage.getItem('gbb_lock')"), '| pressed', ev("document.querySelector('.lockbtn').getAttribute('aria-pressed')"))
p.locator('[data-act="timer-start"]').first.click();p.wait_for_timeout(1500)
print('showing      :', ev("__lk.showing"), '| audio paused', ev("__lk.a?__lk.a.paused:null"), '| meta', meta(), '| state', ev("navigator.mediaSession.playbackState"))
print('handlers     :', ev("Object.keys(window.__msh).filter(k=>window.__msh[k]).join(',')"))
ev("(()=>{const L=window.__store['live/m1'];if(L){L.start-=83*60000;L.flushed=L.start;L.cm=0;window.__fire();}return 1})()");p.wait_for_timeout(1600)
print('83 min later :', meta())
print('artwork      :', save_art('v30_art.png'))
sid0=live()['sid'];before=mins()
# 잠금 화면에서 멈춤
ev("(window.__msh.pause(),0)");p.wait_for_timeout(800)
print('lock pause   : live', live(), '| mins', before, '->', mins())
print('  paused meta:', meta(), '| state', ev("navigator.mediaSession.playbackState"), '| audio paused', ev("__lk.a.paused"), '| showing', ev("__lk.showing"))
print('  app button :', ev("!!document.querySelector('[data-act=\"timer-start\"]')"), '| row', ev("document.querySelector('.lockbtn small').textContent"))
save_art('v30_art_paused.png')
p.wait_for_timeout(2500)
print('  after ticks:', meta())
# 아무 데나 눌러도 멈춤 유지
click(p,'[data-act="tab"][data-tab="room"]',600)
print('  after tap  :', meta(), '| live', live())
# 잠금 화면에서 재생 -> 같은 과목으로 새로 시작
ev("(window.__msh.play(),0)");p.wait_for_timeout(1200)
L=live();print('lock play    : live sid same', L and L['sid']==sid0, '| mode', L and L.get('mode'), '| showing', ev("__lk.showing"), '| meta', meta(), '| state', ev("navigator.mediaSession.playbackState"))
# 뽀모도로로 바꿔서 같은 흐름
click(p,'[data-act="timer-stop"]',900)
print('app stop     : showing', ev("__lk.showing"), '| meta', meta())
mp=p.locator('[data-act="tmode"][data-v="pomo"]')
if mp.count():mp.first.click();p.wait_for_timeout(500)
p.locator('[data-act="timer-start"]').first.click();p.wait_for_timeout(1200)
print('pomo start   :', live() and {k:live()[k] for k in ('mode','f','b')}, '| meta', meta())
ev("(window.__msh.pause(),0)");p.wait_for_timeout(600)
print('pomo pause   : live', live(), '| meta', meta())
ev("(window.__msh.play(),0)");p.wait_for_timeout(1000)
print('pomo resume  :', live() and {k:live()[k] for k in ('mode','f','b')}, '| meta', meta())
# 다른 소리에 끊김: 비켜 주고, 같은 타이머 동안은 눌러도 다시 틀지 않음
ev("(__lk.a.pause(),0)");p.wait_for_timeout(400)
print('interrupted  : showing', ev("__lk.showing"), '| meta', meta(), '| live kept', bool(live()))
click(p,'[data-act="tab"][data-tab="room"]',500)
print('  after tap  : showing', ev("__lk.showing"), '| audio paused', ev("__lk.a.paused"))
click(p,'[data-act="timer-stop"]',900)
# 미리 보기 그림 여러 개
for nm,sid in (('v30_art_s1.png',None),):pass
p.screenshot(path=SH+'v30_room.png',full_page=True)
p.locator('.lockbtn').click();p.wait_for_timeout(400)
print('toggle off   :', ev("localStorage.getItem('gbb_lock')"), '| meta', meta())
print('errors',R.errors)
R.close()
