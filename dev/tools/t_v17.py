import sys,json,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
SEED=open('/home/claude/planner/tools/t_v13.py').read().split('SEED=r"""')[1].split('"""')[0]
# 일요일(주의 마지막 날)로 고정
_t=datetime.datetime.now();SUN=(_t+datetime.timedelta(days=(6-_t.weekday())%7)).replace(hour=15,minute=0,second=0,microsecond=0)
EXTRA="""()=>{const S=window.__store,d=new Date(),k='days/m1_'+d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
S[k]={goals:[{id:'z1',text:'일요일 할 일 하나',sid:'s3',done:false},{id:'z2',text:'일요일 할 일 둘',sid:'s4',done:false}]};window.__fire();}"""
def title(p):return st(p,"document.querySelector('.wkt').textContent")
def edges(p):return st(p,"[...document.querySelectorAll('.wkedge')].map(e=>(e.classList.contains('r')?'R':'L')+(e.classList.contains('on')?'on':'off'))")
def center(p,sel):
    b=p.locator(sel).bounding_box();return b['x']+b['width']/2,b['y']+b['height']/2
def drag_flip(p,src,edge,drop,label):
    x,y=center(p,src);p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+10,y+4,steps=2)
    print(label,'edges at start :',edges(p))
    ex,ey=center(p,'.wkedge.'+edge+'.on');p.mouse.move(ex,ey,steps=8);p.wait_for_timeout(200)
    p.screenshot(path=SH+'v17_'+label+'.png')
    print(label,'armed          :',st(p,"!!document.querySelector('.wkedge.arm')"),'| ph',st(p,"!!document.querySelector('.wkph')"))
    p.wait_for_timeout(600)
    print(label,'week now       :',title(p))
    dx,dy=center(p,drop);p.mouse.move(dx,dy-10,steps=8);p.wait_for_timeout(150)
    print(label,'over           :',st(p,"(document.querySelector('.wkc.over')||{}).id"))
    p.mouse.up();p.wait_for_timeout(700)
    print(label,'flash          :',st(p,"(document.querySelector('.flash span')||{}).textContent"),'| edges left',st(p,"document.querySelectorAll('.wkedge').length"))

R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=SUN);close_dlg(p)
T=p.evaluate(SEED);p.evaluate(EXTRA);p.wait_for_timeout(700)
add=lambda n: st(p,"(()=>{const d=new Date();d.setDate(d.getDate()+%d);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()"%n)
T1=add(1);ids=lambda d:[g['id'] for g in (store(p,'days/m1_'+d) or {}).get('goals',[])]
print('today',T,'| week',title(p),'| hint',st(p,"(document.querySelector('.wkhint')||{}).textContent"))
# 1) 일요일 할 일 -> 다음 주 월요일
drag_flip(p,'#wi-z1','r','#wc-%s'%T1,'next')
print('after          : today',ids(T),'| mon',ids(T1),'| week',title(p))
# 2) 다음 주 월요일 -> 이전 주로 돌아가 오늘(일요일)로
drag_flip(p,'#wi-z1','l','#wc-%s'%T,'back')
print('after          : today',ids(T),'| mon',ids(T1),'| week',title(p))
# 3) 이번 주에서는 왼쪽(이전 주, 모두 지난 날)이 안 나옴 -> drag_flip의 edges at start에서 Loff 확인
# 4) 되돌리기
print('errors',R.errors)
# 5) 휴대폰 폭: 가로로 끝까지 밀린 다음 다음 주로
q=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=SUN);close_dlg(q);q.evaluate(SEED);q.evaluate(EXTRA);q.wait_for_timeout(900)
print('phone scroll   :',q.evaluate("()=>{const s=document.querySelector('.wkscroll');return [s.scrollLeft,s.scrollWidth-s.clientWidth]}"))
x,y=center(q,'#wi-z2');q.mouse.move(x,y);q.mouse.down();q.mouse.move(x+10,y+4,steps=2)
print('phone edges    :',edges(q))
q.mouse.move(380,y,steps=6);q.wait_for_timeout(1400)
print('phone edges 2  :',edges(q),'| week',title(q))
q.screenshot(path=SH+'v17_phone.png')
q.wait_for_timeout(900)
print('phone week     :',title(q))
c=q.evaluate("()=>{const e=document.getElementById('wc-%s');if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+40]}"%T1)
print('mon cell       :',c)
if c:
    q.mouse.move(c[0],c[1],steps=8);q.wait_for_timeout(150);q.mouse.up();q.wait_for_timeout(700)
print('phone after    : mon',[g['id'] for g in (json.loads(q.evaluate("()=>JSON.stringify(window.__store['days/m1_%s']||null)"%T1)) or {}).get('goals',[])])
print('phone overflow',q.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1"))
print('errors',R.errors)
R.close()
