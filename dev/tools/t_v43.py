# v43: 점수 조정, 색 무료·새 꾸미기, 타임랩스 없음, 할 일 모음, 지난 날 할 일, 메시지 읽음 숫자, 리포트·진도, 모바일 더보기, 새 타이머 모양
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
SEED="""()=>{const S=window.__store;
S['days/m1_2026-10-25']={goals:[{id:'pa',text:'기출 1회',sid:'s2',done:false},{id:'pb',text:'오답',sid:'s3',done:true}],mins:{s2:60}};
S['inbox/m1']={items:{a1:{t:'쎈 3단원',sid:'s2',at:1},a2:{t:'단어 100개',sid:'s4',at:2}}};
S['days/m2_2026-10-28']=Object.assign({},S['days/m2_2026-10-28'],{in:'2026-10-28T00:10:00.000Z'});
S['days/m2_2026-10-20']={in:'2026-10-20T00:10:00.000Z',goals:[]};
window.__fire();}"""
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW)
p.evaluate(SEED);p.wait_for_timeout(500);close_dlg(p)
# 1) 점수: 출석 3~5점(10/27부터), 예전 날은 그대로
sc=st(p,"(()=>{const V=window.__gbbV||null;return null})()")
click(p,'#navMore',400);click(p,'.mitem[data-tab="rank"]',800)
rules=st(p,"document.querySelector('.rlz')?document.querySelector('.rlz').innerText:''")
check('rules text',('3~5점' in rules) and ('1줄 20점' in rules) and ('문제 내기\n문제를 올린 날\n5점' in rules or '5점' in rules),rules[:200].replace('\n',' / '))
# 2) 모바일 아래 메뉴
vis=st(p,"[...document.querySelectorAll('.navs > button')].filter(b=>getComputedStyle(b).display!=='none').map(b=>b.dataset.tab||b.id)")
check('mobile nav items',vis==['cal','room','chat','navMore'],vis)
click(p,'#navMore',400)
check('more menu 5',st(p,"document.querySelectorAll('#moreMenu .mitem').length")==5)
click(p,'.mitem[data-tab="board"]',800)
check('more menu closes and goes',st(p,"!document.querySelector('#moreMenu:not(.out)')")and st(p,"document.querySelector('#navMore').getAttribute('aria-current')")=='page')
check('no timelapse in board',not st(p,"document.querySelector('#view-board').innerText.includes('타임랩스')"))
# 3) 지난 날 할 일 (오늘 화면)
click(p,'[data-act="tab"][data-tab="cal"]',700)
check('past card',st(p,"!!document.querySelector('#c-past #pd-2026-10-25')"))
click(p,'#c-past .chk[data-id="pa"]',600)
click(p,'#pd-2026-10-25 [data-act="cert"]',600)
d=store(p,'days/m1_2026-10-25')
check('past done+cert',d['goals'][0]['done'] and bool(d.get('certAt')),d)
# 4) 할 일 모음
click(p,'[data-act="cal-mode"][data-id="list"]',600)
click(p,'[data-act="open"][data-modal="inbox"]',700)
p.fill('#ibText','기출 2회');click(p,'[data-act="ib-add"]',500)
check('inbox add',len(store(p,'inbox/m1')['items'])==3)
click(p,'[data-act="ib-all"]',300);click(p,'[data-act="ib-put"][data-d="2026-10-30"]',700)
g=[x['text'] for x in store(p,'days/m1_2026-10-30')['goals']]
check('inbox assign',g==['쎈 3단원','단어 100개','기출 2회'] and not store(p,'inbox/m1')['items'],g)
check('past day disabled',st(p,"document.querySelector('[data-act=\"ib-put\"][data-d=\"2026-10-26\"]')===null||document.querySelector('[data-act=\"ib-put\"][data-d=\"2026-10-26\"]').disabled"))
close_dlg(p)
# 5) 메시지 읽음 숫자
click(p,'[data-act="tab"][data-tab="chat"]',700);click(p,'[data-act="chan"][data-id="m2"]',600)
p.evaluate("()=>{const S=window.__store;S['msgs/y1']={from:'m1',to:'m2',text:'봤어?',at:Date.now()};window.__fire();}");p.wait_for_timeout(500)
check('dm unread 1',st(p,"(document.querySelector('#m-y1 .urd')||{}).textContent")=='1')
p.evaluate("()=>{const S=window.__store;S['reads/m2']={m1:Date.now()+1000};window.__fire();}");p.wait_for_timeout(500)
check('dm read clears',st(p,"!document.querySelector('#m-y1 .urd')"))
check('my reads written',bool((store(p,'reads/m1') or {}).get('m2')))
click(p,'[data-act="chan"][data-id="all"]',600)
p.evaluate("()=>{const S=window.__store;S['msgs/y2']={from:'m1',to:'all',text:'모두',at:Date.now()};S['reads/m3']={all:Date.now()+5000};window.__fire();}");p.wait_for_timeout(500)
check('all unread = roster-2',st(p,"(document.querySelector('#m-y2 .urd')||{}).textContent")=='3')
# 6) 상점: 색 무료, 새 꾸미기
click(p,'#shopBtn',800)
click(p,'[data-act="shop-cat"][data-v="color"]',500)
check('colors free',st(p,"document.querySelectorAll('#shg-color .shbuy').length")==0)
click(p,'[data-act="shop-cat"][data-v="look"]',500)
names=st(p,"[...document.querySelectorAll('#shg-look .shn b')].map(e=>e.textContent)")
check('new looks',all(n in ' '.join(names) for n in ['크라프트지','신문','노을','숲','벚꽃']),names)
prices=st(p,"[...document.querySelectorAll('#shg-look .shbuy b')].map(e=>+e.textContent)")
check('look prices lower',max(prices)<=200,prices)
click(p,'[data-act="shop-cat"][data-v="timer"]',500)
check('new timers',st(p,"!!document.querySelector('#shi-t-analog')&&!!document.querySelector('#shi-t-orbit')"))
close_dlg(p)
# 7) 진도 모두 보기
click(p,'#navMore',400);click(p,'.mitem[data-tab="prog"]',700);click(p,'[data-act="prog-mode"][data-id="all"]',600)
check('prog rows',st(p,"document.querySelectorAll('.prow').length")==st(p,"document.querySelectorAll('.prow').length")>0)
click(p,'[data-act="prog-sort"][data-id="avg"]',500)
check('prog sort',st(p,"document.querySelector('[data-act=\"prog-sort\"][data-id=\"avg\"]').getAttribute('aria-pressed')")=='true')
# 8) 리포트
click(p,'#navMore',400);click(p,'.mitem[data-tab="report"]',700)
check('report more',st(p,"document.querySelectorAll('.rmore .card').length")==4)
print('errors',R.errors)
check('no page errors',not R.errors,R.errors)
# 9) 새 타이머 모양
for t in ['analog','orbit']:
    q=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_tstyle':t},now=NOW)
    q.evaluate("()=>{const S=window.__store;S['progress/m1']=Object.assign({},S['progress/m1']||{},{shop:{gf:1,own:{'t:%s':0}}});S['live/m1']={sid:'s2',start:Date.now()-600000,flushed:Date.now(),cm:0};window.__fire();}"%t);q.wait_for_timeout(500);close_dlg(q)
    click(q,'[data-act="tab"][data-tab="room"]',800)
    a=st(q,"(document.querySelector('.ansec,.ob-p')||{}).outerHTML||''");q.wait_for_timeout(2100)
    b=st(q,"(document.querySelector('.ansec,.ob-p')||{}).outerHTML||''")
    check(t+' face ticks',bool(a) and a!=b)
print('errors',R.errors)
R.close()
print('ALL OK' if ok else 'SOME FAILED')
