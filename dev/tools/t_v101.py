# v101: 노동요 칸 정리(더 보기, 펼치기), 댓글
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
songs={'q%d'%i:{'mid':'m%d'%(2+i%3),'title':'곡%02d'%i,'url':'https://youtu.be/abcdef%05d'%i if i%2==0 else '','at':NOW-i*3600000} for i in range(20)}
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;Object.keys(S).filter(k=>k.startsWith('songs/')).forEach(k=>delete S[k]);var sg=%s;for(var k in sg)S['songs/'+k]=sg[k];var p=S['progress/m3']||{};p.scm={x1:{s:'q0',t:'남의 댓글',at:%d}};S['progress/m3']=p;clearInterval(t);},5);})();"%(json.dumps(songs),NOW-60000)
p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',800)
n=lambda:ev(p,"document.querySelectorAll('#c-songs .song').length")
check('first page 6',n()==6,n())
click(p,'[data-act="song-lim"][data-id="more"]',400)
check('more shows 16',n()==16,n())
click(p,'[data-act="song-lim"][data-id="more"]',400)
check('all 20, no more button',n()==20 and not ev(p,"!!document.querySelector('[data-act=\"song-lim\"][data-id=\"more\"]')"))
click(p,'[data-act="song-lim"][data-id="less"]',400)
check('fold back to 6',n()==6,n())
first=ev(p,"document.querySelector('#c-songs .song').id.slice(3)")
check('comment count on row',ev(p,"document.querySelector('#sg-q0 .sgc span')?.textContent")=='1')
click(p,'#sg-q0 [data-act="song-x"]',400)
check('expanded shows comment','남의 댓글' in ev(p,"document.querySelector('#sg-q0 .sgcm').textContent"))
p.fill('#sg-q0 .sgcin input','좋아요 이 곡');p.keyboard.press('Enter');p.wait_for_timeout(500)
scm=json.loads(ev(p,"JSON.stringify((window.__store['progress/m1']||{}).scm||{})"))
check('comment saved in my progress',any(v.get('s')=='q0' and v.get('t')=='좋아요 이 곡' for v in scm.values()),scm)
check('comment shown, input cleared','좋아요 이 곡' in ev(p,"document.querySelector('#sg-q0 .sgcm').textContent") and ev(p,"document.querySelector('#sg-q0 .sgcin input').value")=='')
check('count 2',ev(p,"document.querySelector('#sg-q0 .sgc span').textContent")=='2')
# 방장(m1)은 남의 댓글도 지울 수 있음
click(p,'#sg-q0 [data-act="song-cdel"][data-id="m3|x1"]',300);click(p,'#sg-q0 [data-act="song-cdel"][data-id="m3|x1"]',500)
check('admin deleted other comment',not ev(p,"!!((window.__store['progress/m3']||{}).scm||{}).x1"))
cid=[k for k in scm][0]
click(p,'#sg-q0 [data-act="song-cdel"][data-id="m1|%s"]'%cid,300);click(p,'#sg-q0 [data-act="song-cdel"][data-id="m1|%s"]'%cid,500)
check('own comment deleted',not ev(p,"Object.keys((window.__store['progress/m1']||{}).scm||{}).length"))
# 방장 아닌 사람은 남의 댓글 지우기 단추 없음
R.close()
R=Rig();p=R.open(390,900,ls={'gbb_note':'9999999999999','gbb_me':'m2'},pre=PRE);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-tab="room"]',800)
click(p,'#sg-q0 [data-act="song-x"]',400)
check('member: no delete for others',not ev(p,"!!document.querySelector('#sg-q0 [data-act=\"song-cdel\"]')"))
check('member: no admin button',not ev(p,"!!document.querySelector('[data-act=\"song-adm\"]')"))
check('mobile no overflow',ev(p,"document.getElementById('c-songs').scrollWidth<=document.getElementById('c-songs').clientWidth+1"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
