# v95: 3D 최종 결과 연출 예시 페이지를 브라우저로 돌려 막마다 사진(SHOTS=폴더)
import sys,os,time,subprocess,threading,http.server,functools,socketserver
from playwright.sync_api import sync_playwright
BASE='/home/claude/planner/web-light'
OUT=os.environ.get('SHOTS','/tmp/fr3shots');os.makedirs(OUT,exist_ok=True)
W=int(os.environ.get('W','1280'));H=int(os.environ.get('H','800'))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
srv=socketserver.TCPServer(('127.0.0.1',0),functools.partial(Q,directory=BASE));port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--enable-unsafe-swiftshader'])
    ctx=b.new_context(viewport={'width':W,'height':H},device_scale_factor=1,record_video_dir=os.environ.get('VIDEO') or None,record_video_size={'width':W,'height':H} if os.environ.get('VIDEO') else None)
    p=ctx.new_page();errs=[]
    p.on('pageerror',lambda e:errs.append(str(e)));p.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    p.goto('http://127.0.0.1:%d/final-demo.html#auto'%port);
    p.wait_for_function("()=>document.querySelector('.f3')&&document.querySelector('.f3').__fr3",timeout=30000)
    st=lambda:p.evaluate("()=>document.querySelector('.f3').__fr3.state()")
    shots=[];k=0
    def snap(tag):
        global k
        k+=1;path='%s/%02d_%s.png'%(OUT,k,tag);p.screenshot(path=path);shots.append(path)
    def wait_ready(maxs=60):
        t0=time.time()
        while time.time()-t0<maxs:
            s=st()
            if not s['busy'] and s['next']:return s
            time.sleep(.5)
        return st()
    # 0 intro
    time.sleep(2.5);snap('intro_fly');time.sleep(2.4);snap('countdown')
    s=wait_ready();snap('cut_line');print(s)
    acts=[]
    while True:
        s=st();acts.append(s['act'])
        if s['next']=='닫기':break
        lab=s['next'];p.evaluate("()=>document.querySelector('.f3').__fr3.next()")
        time.sleep(1.0);snap('a%d_start'%(s['act']+1))
        if lab in ('1등 공개',):
            time.sleep(5.2);snap('p1_hit');time.sleep(2.5);snap('p1_orbit');time.sleep(3);snap('p1_end')
        elif lab in ('3등 공개','2등 공개'):
            time.sleep(4);snap('podium')
        elif lab=='4등부터 공개':
            time.sleep(3);snap('rest_mid')
        s=wait_ready();snap('a%d_end'%s['act'])
    print('acts',acts)
    check('reached final',st()['next']=='닫기',st())
    check('no errors',not errs,errs[:5])
    p.evaluate("()=>document.querySelector('.f3next').click()");time.sleep(1)
    check('closed',p.evaluate("()=>!document.querySelector('.f3')"))
    ctx.close();b.close()
srv.shutdown()
print('ALL OK' if ok else 'SOME FAILED')
