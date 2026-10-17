import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
SEED=open('/home/claude/planner/tools/t_v13.py').read().split('SEED=r"""')[1].split('"""')[0]
import datetime
_t=datetime.datetime.now();WED=(_t+datetime.timedelta(days=(2-_t.weekday())%7)).replace(hour=15,minute=0,second=0,microsecond=0)  # 한 주 안에 어제·내일·모레가 다 보이는 수요일로 고정
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=WED);close_dlg(p)
T=p.evaluate(SEED);p.wait_for_timeout(700)
add=lambda n: st(p,"(()=>{const d=new Date();d.setDate(d.getDate()+%d);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()"%n)
T1,T2=add(1),add(2)
texts=lambda d: [g['text'][:12] for g in (store(p,'days/m1_'+d) or {}).get('goals',[])]
print('today',T,'| T1',texts(T1),'| T2',texts(T2))
print('draggable   :',st(p,"document.querySelectorAll('.wki[data-wdrag]').length"),'| hint',st(p,"(document.querySelector('.wkhint')||{}).textContent"))
# 1) T1의 첫 할 일을 T2 맨 위로 끌기
gid=st(p,"document.querySelector('#wc-%s .wki[data-wdrag]').dataset.id"%T1)
b=p.locator('#wi-%s'%gid).bounding_box();c=p.locator('#wc-%s .wki'%T2).first.bounding_box()
p.mouse.move(b['x']+b['width']/2,b['y']+b['height']/2);p.mouse.down()
p.mouse.move(b['x']+b['width']/2+10,b['y']+b['height']/2+4,steps=2)
p.mouse.move(c['x']+c['width']/2,c['y']+6,steps=10);p.wait_for_timeout(150)
print('placeholder :',st(p,"(e=>e?e.parentNode.id+' before '+(e.nextElementSibling&&e.nextElementSibling.id):'none')(document.querySelector('.wkph'))"),'| over',st(p,"(document.querySelector('.wkc.over')||{}).id"),'| ghost',st(p,"!!document.querySelector('.wkghost')"))
p.screenshot(path=SH+'v16_drag.png')
p.mouse.up();p.wait_for_timeout(700)
print('after move  : T1',texts(T1),'| T2',texts(T2),'| flash',st(p,"(document.querySelector('.flash span')||{}).textContent"))
# 2) 같은 날 순서 바꾸기: T2 마지막 것을 맨 위로
ids=st(p,"[...document.querySelectorAll('#wc-%s .wki')].map(e=>e.dataset.id)"%T2)
last=ids[-1];b=p.locator('#wi-%s'%last).bounding_box();c=p.locator('#wi-%s'%ids[0]).bounding_box()
p.mouse.move(b['x']+30,b['y']+b['height']/2);p.mouse.down();p.mouse.move(b['x']+38,b['y']+b['height']/2-4,steps=2);p.mouse.move(c['x']+30,c['y']+4,steps=8);p.mouse.up();p.wait_for_timeout(600)
print('reorder     : T2',texts(T2))
# 3) 지난 날로는 안 됨
past=add(-1)
b=p.locator('#wc-%s .wki[data-wdrag]'%T2).first.bounding_box();c=p.locator('#wc-%s'%past).bounding_box()
p.mouse.move(b['x']+30,b['y']+10);p.mouse.down();p.mouse.move(b['x']+40,b['y']+14,steps=2);p.mouse.move(c['x']+c['width']/2,c['y']+60,steps=8)
print('past blocked:',st(p,"document.getElementById('wc-%s').classList.contains('no')"%past),'| ph',st(p,"!!document.querySelector('.wkph')"))
p.mouse.up();p.wait_for_timeout(500)
print('unchanged   : T2',texts(T2),'| past',texts(past))
# 4) 짧게 누르면 그대로 달력으로 열림
gid2=st(p,"document.querySelector('#wc-%s .wki[data-wdrag]').dataset.id"%T2)
p.wait_for_timeout(500)
p.locator('#wi-%s .wkt'%gid2).click();p.wait_for_timeout(700)
print('tap opens   :',st(p,"!!document.querySelector('.calcard')"),'| sel',st(p,"!!document.getElementById('ga-%s')"%gid2))
# 5) 터치 꾹 눌러 끌기
click(p,'[data-act="cal-mode"][data-id="list"]',800)
gid3=st(p,"document.querySelector('#wc-%s .wki[data-wdrag]').dataset.id"%T2)
r=p.evaluate("(id)=>{const e=document.getElementById('wi-'+id).getBoundingClientRect(),c=document.getElementById('wc-%s').getBoundingClientRect();return [e.left+e.width/2,e.top+e.height/2,c.left+c.width/2,c.top+60];}"%T,gid3)
ev="(a)=>{const [type,x,y]=a;const t=document.elementFromPoint(x,y)||document.body;t.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,button:0}));}"
p.evaluate(ev,['pointerdown',r[0],r[1]]);p.wait_for_timeout(450)
for k in range(1,11): p.evaluate(ev,['pointermove',r[0]+(r[2]-r[0])*k/10,r[1]+(r[3]-r[1])*k/10]);p.wait_for_timeout(25)
p.evaluate(ev,['pointerup',r[2],r[3]]);p.wait_for_timeout(700)
print('touch move  : today has',gid3 in [g['id'] for g in store(p,'days/m1_'+T)['goals']])
print('errors',R.errors)
q=R.open(390,844,ls={'gbb_note':'9999999999999','gbb_calmode':'list'},now=WED);close_dlg(q);q.evaluate(SEED);q.wait_for_timeout(800)
print('phone overflow',q.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1"))
print('errors',R.errors)
R.close()
