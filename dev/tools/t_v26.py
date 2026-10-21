# 처음 화면: 붓글씨로 아이콘 안 그림을 한 획씩 그린 뒤 사라지는지
import sys,json,re
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
from PIL import Image
SH='/home/claude/planner/shots/'
R=Rig()
def openc(scheme='light',ls=None,motion='no-preference',w=390,h=844):
    ctx=R.browser.new_context(viewport={'width':w,'height':h},device_scale_factor=2,color_scheme=scheme,reduced_motion=motion)
    ctx.route(re.compile(r'^https?://'),route)
    pg=ctx.new_page()
    pg.on('pageerror',lambda e:R.errors.append('pageerror: '+str(e)))
    pg.on('console',lambda m:R.errors.append('console: '+m.text) if m.type=='error' and 'net::ERR' not in m.text else None)
    init={'gbb_pinask':json.dumps({'m1':1,'m2':1,'m3':1}),'gbb_me':'m1','gbb_note':'9999999999999'};init.update(ls or {})
    pg.add_init_script("try{var o=%s;for(var k in o)localStorage.setItem(k,o[k]);}catch(e){}"%json.dumps(init))
    pg.add_init_script(MOCK)
    pg.clock.install()
    pg.goto(PAGE,wait_until='domcontentloaded')
    return pg
def sheet(name,frames,bg):
    ims=[Image.open(f) for f in frames];w=max(i.size[0] for i in ims);h=max(i.size[1] for i in ims)
    s=Image.new('RGB',(w*len(ims),h),bg)
    for i,im in enumerate(ims):s.paste(im,(i*w,0))
    s.save(SH+name)
for scheme,ls,tag,bg in [('light',None,'light','#F3F4F6'),('dark',None,'dark','#0F1114'),('light',{'gbb_concept':'board'},'board','#1E3A2F')]:
    pg=openc(scheme,ls)
    fr=[];t=0
    for ms in [150,250,250,250,250,250,200,150,150,150,150,150]:
        pg.clock.run_for(ms);t+=ms
        p=SH+'v26_%s_%d.png'%(tag,t)
        pg.screenshot(path=p,animations='allow');fr.append(p)
    ims=[Image.open(f).resize((195,422)) for f in fr]
    s2=Image.new('RGB',(195*len(ims),422),bg)
    for i,im in enumerate(ims):s2.paste(im,(i*195,0))
    s2.save(SH+'v26_%s.png'%tag)
    st=pg.evaluate("JSON.stringify(window.__sp&&{done:window.__sp.done,ready:window.__sp.ready})")
    pg.clock.run_for(2500)
    print(tag,'| state',st,'| splash gone',pg.evaluate("!document.getElementById('splash')"),'| app shown',pg.evaluate("!!document.querySelector('.view')"))
# 준비 전에 사라지지 않는지, 누르면 넘어가는지
pg=openc()
pg.clock.run_for(400)
print('early tap     | still there', pg.evaluate("!!document.getElementById('splash')"))
pg.evaluate("document.getElementById('splash').click()");pg.clock.run_for(1400)
print('after tap     | gone', pg.evaluate("!document.getElementById('splash')"))
# 동작 줄이기: 바로 완성된 그림, 바로 사라짐
pg=openc(motion='reduce')
pg.clock.run_for(50)
print('reduced       | splash', pg.evaluate("!!document.getElementById('splash')"))
pg.clock.run_for(1500)
print('reduced       | gone', pg.evaluate("!document.getElementById('splash')"))
# 다른 앱에 갔다가 돌아오기: 5분 넘으면 다시 그림, 짧으면 그대로
def away(pg,ms):
    pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
    pg.clock.fast_forward(ms)
    pg.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))")
pg=openc()
pg.clock.run_for(4000)
print('first gone    |', pg.evaluate("!document.getElementById('splash')"))
away(pg,60000);pg.clock.run_for(100)
print('back 1 min    | splash', pg.evaluate("!!document.getElementById('splash')"))
away(pg,360000);pg.clock.run_for(600)
print('back 6 min    | splash', pg.evaluate("!!document.getElementById('splash')"), '| strokes', pg.evaluate("document.querySelectorAll('#splash .spink path[d]').length"))
pg.screenshot(path=SH+'v26_again.png')
pg.clock.run_for(3000)
print('back 6 min    | gone after', pg.evaluate("!document.getElementById('splash')"), '| app', pg.evaluate("!!document.querySelector('.view')"))
print('errors',R.errors)
R.close()
