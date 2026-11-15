# 3D 최종 결과 연출 예시를 프레임마다 찍어 영상으로(가상 시간: 3D는 tick, CSS 애니메이션은 currentTime을 같이 넘김)
import sys,os,time,threading,http.server,functools,socketserver,subprocess,shutil
from playwright.sync_api import sync_playwright
BASE='/home/claude/planner/web-light'
OUT=sys.argv[1];W=int(sys.argv[2]);H=int(sys.argv[3]);FPS=int(sys.argv[4]) if len(sys.argv)>4 else 24
FR=OUT+'_frames';shutil.rmtree(FR,ignore_errors=True);os.makedirs(FR)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
srv=socketserver.TCPServer(('127.0.0.1',0),functools.partial(Q,directory=BASE));port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
VT="""window.__vt=function(ms){document.getAnimations().forEach(function(a){if(!a.__vt){a.__vt=1;try{a.pause();}catch(e){}}else{try{a.currentTime=(a.currentTime||0)+ms;}catch(e){}}});};"""
n=0
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    p=b.new_page(viewport={'width':W,'height':H},device_scale_factor=1)
    p.add_init_script(VT)
    p.goto('http://127.0.0.1:%d/final-demo.html#rec'%port)
    p.wait_for_function("()=>document.querySelector('.f3')&&document.querySelector('.f3').__fr3",timeout=60000)
    dt=1.0/FPS;wait=0;done_after=None
    while True:
        s=p.evaluate("(dt)=>{var f=document.querySelector('.f3').__fr3;f.tick(dt);window.__vt(dt*1000);return f.state();}",dt)
        p.screenshot(path='%s/%05d.jpg'%(FR,n),type='jpeg',quality=88);n+=1
        if not s['busy'] and s['next']:
            wait+=1
            if s['next']=='닫기':
                if wait>FPS*5:break
            elif wait>FPS*1.6:
                p.evaluate("()=>document.querySelector('.f3').__fr3.next()");wait=0
        if n>FPS*200:break
        if n%240==0:print('frames',n,s,flush=True)
    b.close()
srv.shutdown()
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',FR+'/%05d.jpg','-vf','scale=trunc(iw/2)*2:trunc(ih/2)*2','-c:v','libx264','-pix_fmt','yuv420p','-crf','23','-preset','medium','-movflags','+faststart',OUT],check=True)
print('video',OUT,n,'frames')
