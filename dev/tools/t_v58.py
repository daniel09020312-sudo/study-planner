# v55: 잉크 선물 게임
import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def allk(p,pre):return json.loads(st(p,"JSON.stringify(Object.fromEntries(Object.entries(window.__store).filter(e=>e[0].startsWith('%s')).map(e=>[e[0].slice(%d),e[1]])))"%(pre,len(pre))))
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,30,15,0,0)
R=Rig()
p=R.open(1180,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("()=>{const S=window.__store;Object.keys(S).filter(k=>k.startsWith('gifts/')).forEach(k=>delete S[k]);window.__fire();}");p.wait_for_timeout(300)
def ink():
    click(p,'#shopBtn',800);v=st(p,"(document.querySelector('.wallet .wl b')||{}).textContent");return int(''.join(ch for ch in (v or '0') if ch.isdigit()) or 0)
i0=ink()
# 1) 퀴즈 선물 보내기
click(p,'[data-act="gift-open"]',500)
p.locator('[data-act="gift-to"]').first.click();p.wait_for_timeout(200)
click(p,'[data-act="gift-amt"][data-v="10"]',300)
click(p,'[data-act="gg-type"][data-v="quiz"]',300)
check('send disabled until quiz filled',st(p,"document.querySelector('[data-act=gift-send]').disabled"))
p.fill('input[data-draft="ggQ"]','2 더하기 2는?');p.fill('input[data-draft="ggA"]','4');p.wait_for_timeout(300)
click(p,'[data-act="gift-open"]',100) if False else None
p.evaluate("()=>{document.querySelector('input[data-draft=ggA]').dispatchEvent(new Event('input',{bubbles:true}))}");p.wait_for_timeout(300)
click(p,'[data-act="gift-send"]',300);click(p,'[data-act="gift-send"]',700)
gs=allk(p,'gifts/');g=list(gs.values())[0] if gs else {}
check('quiz gift saved',g.get('g')=='quiz' and g.get('st')=='wait' and g.get('q')=='2 더하기 2는?' and 'h' in g and 'a' not in g,g)
close_dlg(p);i1=ink()
check('sender ink reserved -10',i0-i1==10,(i0,i1))
close_dlg(p)
# 2) 받는 사람으로: 상자 / 가위바위보 / 퀴즈 (m2가 m1에게)
seed="""()=>{const S=window.__store,n=Date.now();
S['gifts/bx']={from:'m2',to:'m1',n:20,at:n,g:'box',st:'wait',r:14};S['msgs/mbx']={from:'m2',to:'m1',text:'열어 봐',gift:20,gg:'bx',at:n};
S['gifts/qz']={from:'m2',to:'m1',n:9,at:n,g:'quiz',st:'wait',q:'수도는?',h:'%s',tries:0};S['msgs/mqz']={from:'m2',to:'m1',text:'',gift:9,gg:'qz',at:n+1};
S['gifts/rp']={from:'m2',to:'m1',n:10,at:n,g:'rps',st:'wait',h:'%s'};S['msgs/mrp']={from:'m2',to:'m1',text:'',gift:10,gg:'rp',at:n+2};
window.__fire();}"""
def h(i,s):
    t=i+'|'+s;x=5381
    for ch in t: x=((x<<5)+x+ord(ch))&0xffffffff
    if x>=2**31: x-=2**32
    x&=0xffffffff
    a='0123456789abcdefghijklmnopqrstuvwxyz';o=''
    while x: o=a[x%36]+o;x//=36
    return o or '0'
p.evaluate(seed%(h('qz','서울'),h('rp','s')));p.wait_for_timeout(500)
i2=ink();close_dlg(p)
click(p,'[data-act="tab"][data-tab="chat"]',700);click(p,'[data-act="chan"][data-id="m2"]',700)
check('play buttons in bubbles',st(p,"document.querySelectorAll('[data-act=gg-play]').length")==3)
click(p,'[data-act="gg-play"][data-id="bx"]',500);click(p,'[data-act="gg-box"]',300)
check('box opening anim',st(p,"!!document.querySelector('.ggbox.opening')"))
p.wait_for_timeout(1600)
check('box result 14',st(p,"(document.querySelector('.ggwin b')||{}).textContent")=='14')
close_dlg(p)
click(p,'[data-act="gg-play"][data-id="qz"]',500)
p.fill('input[data-draft="ggTry"]','부산');click(p,'[data-act="gg-ans"]',500)
check('wrong answer counts try',(store(p,'gifts/qz') or {}).get('tries')==1)
p.fill('input[data-draft="ggTry"]','서 울');click(p,'[data-act="gg-ans"]',600)
q=store(p,'gifts/qz');check('quiz 2nd try = 2/3 -> 6',q.get('st')=='done' and q.get('got')==6,q)
close_dlg(p)
click(p,'[data-act="gg-play"][data-id="rp"]',500);click(p,'[data-act="gg-rps"][data-v="r"]',600)
r=store(p,'gifts/rp');check('rps rock beats scissors -> 10',r.get('got')==10,r)
close_dlg(p)
i3=ink();check('receiver ink +30',i3-i2==30,(i2,i3));close_dlg(p)
check('result DMs to sender',sum(1 for m in allk(p,'msgs/').values() if m.get('to')=='m2' and '결과' in (m.get('text') or ''))==3)
# 3) 보낸 사람 회수
gid=list(gs.keys())[0]
click(p,'[data-act="chan"][data-id="%s"]'%g['to'],600)
click(p,'[data-act="gg-back"][data-id="%s"]'%gid,300);click(p,'[data-act="gg-back"][data-id="%s"]'%gid,600)
check('sender cancels',store(p,'gifts/'+gid).get('st')=='back')
i4=ink();check('reserved ink returned',i4-i3==10,(i3,i4));close_dlg(p)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
