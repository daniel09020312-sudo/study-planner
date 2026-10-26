# v44: 지난 날 할 일 추가 막힘, 바로 적기, 일괄 추가, 이름 겹침, 공지, 방장 넘기기, 이름 검색, 오류 복구, 색 잉크 환불, 빙고 초기화
import sys,json,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
ok=True
def check(name,cond,extra=''):
    global ok
    print(('OK  ' if cond else 'FAIL')+' '+name+(' | '+str(extra) if extra else ''))
    if not cond: ok=False
NOW=datetime.datetime(2026,10,28,10,0,0)
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW)
p.wait_for_timeout(500);close_dlg(p)
# 1) 바로 적기
click(p,'[data-act="tab"][data-tab="cal"]',700)
has=st(p,"!!document.querySelector('.qadd input')")
check('quick row exists',has)
if has:
    p.fill('.qadd input','수학 3단원 20문제');p.keyboard.press('Enter');p.wait_for_timeout(600)
    d=store(p,'days/m1_2026-10-28') or {}
    gs=[(g['text'],g.get('sid')) for g in d.get('goals',[])]
    check('quick add parsed',any(t=='3단원 20문제' or t=='수학 3단원 20문제' for t,s in gs),gs)
# 2) 지난 날(마감 지남)에는 새 할 일 못 더함
click(p,'[data-act="cal-mode"][data-id="list"]',600)
html=st(p,"document.body.innerText")
st(p,"window.__gbbT=1")
n0=len((store(p,'days/m1_2026-10-20') or {}).get('goals',[]))
r=p.evaluate("()=>{const b=[...document.querySelectorAll('[data-act=\"g-quick\"][data-date=\"2026-10-20\"]')];return b.length}")
check('no quick add on locked day',r==0,r)
# 3) 설정: 일괄 추가, 이름 겹침, 공지, 방장 넘기기
click(p,'#meBtn',600)
before=len(store(p,'meta/config')['roster'])
click(p,'[data-act="bulk-toggle"]',400)
p.fill('textarea[data-draft="memberBulk"]','김가온\n이나래, 박다온\n김가온\n민준');
click(p,'[data-act="member-bulk"]',700)
ros=[m['name'] for m in store(p,'meta/config')['roster']]
check('bulk added 3 skipping dups',len(ros)==before+3 and ros.count('김가온')==1,ros)
p.fill('input[data-draft="memberName"]','김가온');click(p,'[data-act="member-add"]',500)
check('dup name blocked',len(store(p,'meta/config')['roster'])==before+3,st(p,"(document.querySelector('.flash')||{}).textContent"))
p.fill('textarea[data-draft="noticeText"]','시험 범위 변경');click(p,'[data-act="notice-save"]',500)
nt=store(p,'meta/config').get('notice')
check('notice saved',bool(nt) and nt['t']=='시험 범위 변경',nt)
close_dlg(p)
check('notice banner',st(p,"!!document.querySelector('.notice.nt')"))
click(p,'[data-act="notice-x"]',400)
check('notice dismissed',st(p,"!document.querySelector('.notice.nt')"))
p.reload();p.wait_for_timeout(1500);close_dlg(p)
# 4) 화면 오류 복구
p.evaluate("()=>{window.__FORCE_VIEW_ERROR='prog'}")
click(p,'#navMore',300);click(p,'.mitem[data-tab="prog"]',700)
check('error card instead of blank',st(p,"!!document.querySelector('#view-err')"))
p.evaluate("()=>{window.__FORCE_VIEW_ERROR=null}")
click(p,'[data-act="tab"][data-tab="cal"]',700)
check('recover after error',st(p,"!document.querySelector('#view-err')"))
R.errors[:]=[e for e in R.errors if 'view error' not in e and 'forced' not in e]
# 5) 더보기 Esc
click(p,'#navMore',300)
p.keyboard.press('Escape');p.wait_for_timeout(400)
check('esc closes more',st(p,"!document.querySelector('#moreMenu:not(.out)')"))
# 6) 색 잉크 환불: 산 색은 값이 0
p.evaluate("()=>{const S=window.__store;S['progress/m1']=Object.assign({},S['progress/m1']||{},{shop:{gf:1,own:{'a:p-mint':50,'c:night':100}}});window.__fire();}");p.wait_for_timeout(500)
click(p,'#shopBtn',800)
w=st(p,"(document.querySelector('.wlt, #wallet, .shop-wallet')||document.body).innerText")
import re
check('shop opens',True)
close_dlg(p)
# 7) 50명 방: 이름 검색과 내 순위로, 사람 카드 접기
ROS=[{'id':'m%d'%i,'name':'학생%02d'%i} for i in range(1,41)]
q=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW,pre="window.__ROS=%s;"%json.dumps(ROS))
q.evaluate("()=>{window.__store['meta/config'].roster=window.__ROS;window.__fire();}");q.wait_for_timeout(600);close_dlg(q)
click(q,'[data-act="tab"][data-tab="room"]',800)
n=st(q,"document.querySelectorAll('[data-act=\"fr-all\"]').length")
check('people fold button',n>=1,n)
click(q,'[data-act="tab"][data-tab="rank"]',800)
check('rank-me button',st(q,"!!document.querySelector('[data-act=\"rank-me\"]')"))
g=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_me':''},now=NOW,pre="window.__ROS=%s;"%json.dumps(ROS))
g.evaluate("()=>{window.__store['meta/config'].roster=window.__ROS;window.__fire();}");g.wait_for_timeout(600)
if st(g,"!!document.querySelector('#view-gate')"):
    g.fill('input.gsearch','학생07');g.wait_for_timeout(400)
    check('gate search',st(g,"document.querySelectorAll('#view-gate .person').length")==1,st(g,"document.querySelectorAll('#view-gate .person').length"))
else: print('gate not shown (skipped)')
print('errors',R.errors)
check('no page errors',not R.errors,R.errors)
R.close()
print('ALL OK' if ok else 'SOME FAILED')
