# 확인용 도구: 가짜 공유 저장소를 붙여 실제 브라우저에서 플래너를 연다.
import json, os, re, time
from playwright.sync_api import sync_playwright
BASE='/home/claude/planner'
NPM=BASE+'/tools/npm/node_modules'
PAGE='file://'+BASE+'/study-room-planner.html'
FONT_PKG={'Nanum Pen Script':('nanum-pen-script','index.css'),'Gaegu':('gaegu','700.css'),'Jua':('jua','index.css'),'Gowun Batang':('gowun-batang','700.css')}

MOCK = r"""
(function(){
  const T=(function(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');})();
  const dayAdd=(s,n)=>{const a=s.split('-');const d=new Date(+a[0],+a[1]-1,+a[2]);d.setDate(d.getDate()+n);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
  const Y=dayAdd(T,-1),now=Date.now();
  const items=['개념 정리','교과서와 프린트 복습','문제집 풀이','기출 풀이','오답 정리'].map((l,i)=>({id:'i'+(i+1),label:l}));
  const names=['화법과 언어','미적분Ⅰ','확률과 통계','영어 비평적 읽기와 쓰기','화학 반응의 세계','세포와 물질대사','생물의 유전','생명과학 실험'];
  const store={'meta/config':{roster:[{id:'m1',name:'민준'},{id:'m2',name:'서연'},{id:'m3',name:'도윤'},{id:'m4',name:'하준'},{id:'m5',name:'지호'}],penalties:['매점 간식 사기','아침에 물 떠오기','칠판 지우기'],certHour:26}};
  names.forEach((n,i)=>store['subjects/s'+(i+1)]={name:n,order:i+1,items});
  let gi=0;const g=(t,s,d)=>({id:'g'+(gi++),text:t,sid:s,done:d});
  store['days/m1_'+Y]={goals:[g('문제집 풀이 20문제','s2',true),g('개념 정리 1단원','s6',true),g('기출 풀이 1회','s3',false)],mins:{s2:90,s6:60},certAt:Y+'T13:10:00.000Z',in:Y+'T08:00:00.000Z'};
  store['days/m2_'+Y]={goals:[g('오답 정리','s2',true),g('개념 정리','s5',true),g('암기 30분','s7',true)],mins:{s2:120,s5:90},certAt:Y+'T12:40:00.000Z',in:Y+'T07:00:00.000Z'};
  store['days/m1_'+T]={goals:[g('문제집 풀이 20문제 (3단원 유형)','s2',true),g('개념 정리','s6',false),g('기출 풀이 1회','s3',false)],mins:{s2:95,s6:40},manual:{s1:30},in:T+'T00:20:00.000Z'};
  store['days/m2_'+T]={goals:[g('문제집 풀이 30문제','s2',true),g('개념 정리 2단원','s5',true)],mins:{s2:80,s5:45},in:T+'T00:10:00.000Z'};
  store['days/m5_'+T]={goals:[g('암기','s7',true),g('교과서와 프린트 복습','s1',true),g('문제집 풀이 20문제','s3',true)],mins:{s7:60,s1:30},manual:{s3:90},certAt:T+'T05:00:00.000Z',in:T+'T00:30:00.000Z'};
  store['live/m2']={sid:'s2',start:now-37*60000,flushed:now-4*60000};
  store['events/e1']={mid:'m1',date:dayAdd(T,7),title:'화학 반응의 세계 수행평가 (실험 보고서)',shared:false};
  store['events/e2']={mid:'m3',date:dayAdd(T,9),title:'확률과 통계 수행평가',shared:true};
  store['progress/m2']={checks:{'s2__i1':true,'s2__i2':true},skip:{s8:true},now:{id:'n2',at:now-300000}};
  store['songs/n1']={mid:'m2',title:'집중용 로파이',url:'https://music.youtube.com/playlist?list=abc123',mood:'집중',at:now-86400000};
  store['songs/n2']={mid:'m5',title:'빗소리 3시간',url:'https://www.youtube.com/watch?v=rain',mood:'잔잔한',at:now-3600000};
  store['songs/n3']={mid:'m1',title:'시험기간 클래식 모음',url:'',mood:'가사 없음',at:now-7200000};
  store['songs/n4']={mid:'m3',title:'아침에 듣는 신나는 노래',url:'https://open.spotify.com/playlist/xyz',mood:'잠 깰 때',at:now-1800000};
  store['progress/m5']={liked:{n1:true},now:{id:'n1',at:now-600000}};
  store['progress/m3']={liked:{n1:true,n2:true}};
  store['msgs/x1']={from:'m2',to:'all',text:'오늘 다들 몇 시까지 해?',at:now-50*60000};
  store['msgs/x2']={from:'m5',to:'all',text:'나는 11시까지 할 듯',at:now-48*60000};
  store['msgs/x2b']={from:'m5',to:'all',stk:'basic-07',text:'',at:now-47*60000};
  store['msgs/x3']={from:'m2',to:'m1',text:'미적분 3단원 프린트 있어?',at:now-20*60000};
  store['msgs/x3b']={from:'m1',to:'m2',text:'응 있어. 내일 가져갈게',at:now-19*60000};
  store['msgs/x3c']={from:'m2',to:'m1',stk:'basic-06',text:'',at:now-18*60000};
  store['msgs/x3d']={from:'m2',to:'m1',pic:true,text:'이 부분이야',at:now-17*60000};
  store['pics/x3d']={data:window.__SAMPLE_PIC||''};
  store['msgs/x4']={from:'m3',to:'m5',text:'둘만 보는 메시지',at:now-10*60000};
  // 대결: 예전 방식(메시지에 대결 번호 없음)으로 온 신청 하나, 어제 시작한 진행 중 대결 하나
  store['duels/dOld']={a:'m5',b:'m1',stake:'음료수 사기',status:'pending',at:now-9*60000};
  store['msgs/xd1']={from:'m5',to:'m1',text:'1:1 대결을 신청했습니다. 도전 화면에서 수락해 주세요.',go:'play',at:now-9*60000+3};
  store['duels/dOn']={a:'m1',b:'m2',stake:'',status:'on',start:Y,at:now-2*86400000};
  const subs=[];const fire=()=>subs.forEach(f=>f());
  const snapDoc=p=>({id:p.split('/').pop(),exists:p in store,data:()=>store[p]});
  const db={doc(p){return{get:async()=>snapDoc(p),set:async d=>{store[p]=JSON.parse(JSON.stringify(d));if(!p.startsWith('pics/'))fire();},delete:async()=>{delete store[p];if(!p.startsWith('pics/'))fire();},onSnapshot(cb){const f=()=>cb(snapDoc(p));subs.push(f);setTimeout(f,0);return()=>{};}}},
    collection(c){const q={limit(){return q;},orderBy(){return q;},onSnapshot(cb){const f=()=>cb({docs:Object.keys(store).filter(k=>k.startsWith(c+'/')).map(snapDoc)});subs.push(f);setTimeout(f,0);return()=>{};}};return q;}};
  window.__store=store;window.__fire=fire;
  window.claude={use:async n=>n==='db'?db:{can:async()=>null}};
})();
"""

def font_css(family):
    pkg,cssf=FONT_PKG[family]
    css=open(f'{NPM}/@fontsource/{pkg}/{cssf}',encoding='utf-8').read()
    return css.replace('url(./files/',f'url(https://fonts.gstatic.com/fs/{pkg}/files/')

def route(route_, request):
    u=request.url
    if 'morphdom' in u:
        return route_.fulfill(status=200,content_type='application/javascript',body=open(NPM+'/morphdom/dist/morphdom-umd.min.js',encoding='utf-8').read())
    if u.startswith('https://fonts.googleapis.com/'):
        m=re.search(r'family=([^:&]+)',u);fam=m.group(1).replace('+',' ') if m else ''
        if fam in FONT_PKG and os.environ.get('NOFONT')!='1': return route_.fulfill(status=200,content_type='text/css',body=font_css(fam))
        return route_.fulfill(status=200,content_type='text/css',body='')
    if u.startswith('https://fonts.gstatic.com/fs/'):
        p=NPM+'/@fontsource/'+u.split('/fs/')[1]
        if os.path.exists(p): return route_.fulfill(status=200,content_type='font/woff2',body=open(p,'rb').read())
        return route_.abort()
    return route_.abort()

class Rig:
    def __init__(self):
        self.pw=sync_playwright().start()
        self.browser=self.pw.chromium.launch(args=['--font-render-hinting=none'])
        self.errors=[]
    def open(self,w=1180,h=820,scale=1,scheme='light',ls=None,me='m1',sample_pic=None,mock=True,pre=None,now=None):
        ctx=self.browser.new_context(viewport={'width':w,'height':h},device_scale_factor=scale,color_scheme=scheme)
        if now: ctx.clock.set_system_time(now)  # 요일에 따라 달라지는 시험은 날짜를 고정해서 돌린다
        ctx.route(re.compile(r'^https?://'),route)
        page=ctx.new_page()
        page.on('pageerror',lambda e:self.errors.append('pageerror: '+str(e)))
        page.on('console',lambda m:self.errors.append('console: '+m.text) if m.type=='error' and 'net::ERR' not in m.text else None)
        init={'gbb_pinask':json.dumps({'m1':1,'m2':1,'m3':1})}
        if me: init['gbb_me']=me
        init.update(ls or {})
        page.add_init_script("try{var o=%s;if(!sessionStorage.getItem('__i')){for(var k in o)localStorage.setItem(k,o[k]);sessionStorage.setItem('__i','1');}}catch(e){}"%json.dumps(init))
        if sample_pic: page.add_init_script('window.__SAMPLE_PIC=%s;'%json.dumps(sample_pic))
        if pre: page.add_init_script(pre)
        if mock: page.add_init_script(MOCK)
        page.goto(PAGE);page.wait_for_timeout(1500)
        return page
    def close(self):
        self.browser.close();self.pw.stop()

def click(page,sel,wait=220):
    ok=page.evaluate("""s=>{const e=document.querySelector(s);if(!e)return false;const r=e.getBoundingClientRect();e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+r.width/2,clientY:r.top+r.height/2}));return true;}""",sel)
    if not ok: raise Exception('missing '+sel)
    page.wait_for_timeout(wait)
def close_dlg(page):
    page.evaluate("()=>{const e=document.querySelector('.dialog [data-act=\"modal-close\"]');if(e)e.click();}");page.wait_for_timeout(450)
