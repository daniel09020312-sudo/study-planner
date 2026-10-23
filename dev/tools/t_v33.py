# v33: 시간표 잠금 - 잠그면 끌기, 길이, 빈 곳 누르기, 칩 놓기, 채우기, 창에서 시간 고치기가 막힘
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig();T='2026-10-21'
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T15:00:00+09:00');close_dlg(p)
def ev(js):return p.evaluate('()=>'+js)
def store(k):return json.loads(ev("JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def goal(i):return [x for x in store('days/m1_'+T)['goals'] if x['id']==i][0]
ev("""(()=>{const S=window.__store,k='days/m1_%s',d=S[k];d.goals=d.goals.concat([{id:'gx',text:'수학 문제집',sid:'s2',done:false,ts:960,te:1020}]);
const pr=S['progress/m1']=S['progress/m1']||{};pr.tt={b:[{id:'ba',k:'academy',t:'수학 학원',sid:'s2',d:'0101010',s:1080,e:1200}]};window.__fire();return 1})()"""%T)
p.wait_for_timeout(500)
click(p,'[data-act="cal-mode"][data-id="tt"]',900)
click(p,'[data-act="tt-span"][data-v="1"]',700)
print('lock btn     :', ev("(b=>b.innerText+' '+b.getAttribute('aria-pressed'))(document.querySelector('[data-act=\"tt-lock\"]'))"), '| fill', ev("!!document.querySelector('[data-act=\"tt-fill\"]')"))
click(p,'[data-act="tt-lock"]',600)
print('locked       :', ev("localStorage.getItem('gbb_ttlock')"), '|', ev("(b=>b.innerText+' '+b.getAttribute('aria-pressed'))(document.querySelector('[data-act=\"tt-lock\"]'))"), '| flash', ev("(document.querySelector('.flash span')||{}).textContent"))
print('  col slot   :', ev("document.getElementById('tc-%s').getAttribute('data-act')"%T), '| drag attrs', ev("document.querySelectorAll('.ttb[data-tdrag]').length"), '| resize', ev("document.querySelectorAll('.ttb .tbr').length"), '| chips', ev("[...document.querySelectorAll('.ttchip')].map(c=>c.getAttribute('data-act')+'/'+c.getAttribute('aria-disabled')).join(',')"), '| fill', ev("!!document.querySelector('[data-act=\"tt-fill\"]')"))
print('  hint       :', ev("document.querySelector('.tthint').textContent"))
# 끌어 보기
ev("(()=>{const sc=document.getElementById('ttScroll'),t=document.getElementById('tb-gx');document.getElementById('c-tt').scrollIntoView({block:'start'});sc.scrollTop=t.offsetTop-120;return 1})()");p.wait_for_timeout(200)
b=p.locator('#tb-gx').bounding_box()
p.mouse.move(b['x']+30,b['y']+12);p.mouse.down();p.mouse.move(b['x']+32,b['y']+20,steps=2);p.mouse.move(b['x']+30,b['y']+150,steps=8);p.mouse.up();p.wait_for_timeout(700)
g=goal('gx');print('  drag       :', g['ts'], g['te'], '(960 1020 그대로) | modal', ev("(document.getElementById('dlgT')||{}).textContent||null"))
close_dlg(p)
# 빈 곳 누르기
r=p.locator('#tc-%s'%T).bounding_box()
p.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:x,clientY:y}));}",[r['x']+r['width']/2,b['y']-60]);p.wait_for_timeout(600)
print('  slot tap   : modal', ev("(document.getElementById('dlgT')||{}).textContent||null"))
# 블록 누르면 내용만
click(p,'#tb-gx',600)
print('  ttg modal  :', ev("document.getElementById('dlgT').textContent"), '| times', ev("document.querySelectorAll('#dlg-ttg .ttime input').length"), '| off btn', ev("!!document.querySelector('[data-act=\"ttg-off\"]')"), '| hint', ev("(document.querySelector('#dlg-ttg .ttlkh')||{}).textContent"))
p.screenshot(path=SH+'v33_ttg.png')
close_dlg(p)
click(p,'#tb-ba-%s'%T,600)
print('  ttf modal  : disabled', ev("[...document.querySelectorAll('#dlg-ttf .ttime input')].map(i=>i.disabled).join(',')"), '| hint', bool(ev("(document.querySelector('#dlg-ttf .ttlkh')||{}).textContent")), '| btns', ev("[...document.querySelectorAll('#dlg-ttf .df .btn')].map(b=>b.textContent).join(',')"))
close_dlg(p)
# 끝냄 표시는 됨
ck=p.locator('#tb-gx .ttbchk')
if ck.count():ck.click();p.wait_for_timeout(600);print('  check      :', goal('gx')['done'])
ev("(()=>{const sc=document.getElementById('ttScroll'),t=document.getElementById('tb-gx');sc.scrollTop=t.offsetTop-120;return 1})()");p.wait_for_timeout(200)
p.screenshot(path=SH+'v33_locked.png')
# 다시 열어도 잠김 유지
p.reload();p.wait_for_timeout(2200);close_dlg(p)
click(p,'[data-act="cal-mode"][data-id="tt"]',900)
print('reload       :', ev("document.querySelector('[data-act=\"tt-lock\"]').getAttribute('aria-pressed')"))
# 풀기 -> 끌기 됨
ev("""(()=>{const S=window.__store,k='days/m1_%s',d=S[k];d.goals=d.goals.concat([{id:'gx',text:'수학 문제집',sid:'s2',done:false,ts:960,te:1020}]);window.__fire();return 1})()"""%T);p.wait_for_timeout(500)
click(p,'[data-act="tt-lock"]',600)
print('unlocked     :', ev("localStorage.getItem('gbb_ttlock')"), '| drag attrs', ev("document.querySelectorAll('.ttb[data-tdrag]').length"), '| slot', ev("document.getElementById('tc-%s').getAttribute('data-act')"%T))
print('errors',R.errors)
R.close()
