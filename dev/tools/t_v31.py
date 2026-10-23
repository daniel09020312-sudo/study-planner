# v31: 시간 고칠 때 시작과 끝 따로(끝을 같이 밀지 않음), 학원 등 고정 일정에 과목 여러 개
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
T='2026-10-21'
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T15:00:00+09:00');close_dlg(p)
def ev(js):return p.evaluate('()=>'+js)
def store(k):return json.loads(ev("JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def setv(sel,v):
    p.evaluate("([s,v])=>{const i=document.querySelector(s);i.value=v;i.dispatchEvent(new Event('change',{bubbles:true}));}",[sel,v]);p.wait_for_timeout(450)
def vals(sel):return ev("[...document.querySelectorAll(%s)].map(i=>i.value).join('~')"%json.dumps(sel))
def hint(sel):return ev("(document.querySelector(%s)||{textContent:''}).textContent"%json.dumps(sel))
ev("(()=>{const k='days/m1_%s',d=window.__store[k]||{goals:[]};d.goals=(d.goals||[]).concat([{id:'gx',text:'수학 문제집',sid:'s2',done:false,ts:600,te:660},{id:'gy',text:'영어 단어',sid:'s3',done:false}]);window.__store[k]=d;window.__fire();return 1})()"%T)
p.wait_for_timeout(500)
click(p,'[data-act="cal-mode"][data-id="tt"]',900)
# ---- 할 일 시간: 시작만 바꾸면 끝은 그대로
click(p,'#tb-gx',600)
print('ttg open     :', vals('#dlg-ttg .ttime input'))
setv('#dlg-ttg .ttime input[data-k="s"]','09:30')
g=[x for x in store('days/m1_'+T)['goals'] if x['id']=='gx'][0]
print('start 09:30  :', vals('#dlg-ttg .ttime input'), '| saved', g['ts'], g['te'], '(570, 660)')
setv('#dlg-ttg .ttime input[data-k="s"]','13:00')
g=[x for x in store('days/m1_'+T)['goals'] if x['id']=='gx'][0]
print('start 13:00  :', vals('#dlg-ttg .ttime input'), '| saved', g['ts'], g['te'], '| hint', hint('#dlg-ttg .ttpend'))
p.screenshot(path=SH+'v31_pend.png')
setv('#dlg-ttg .ttime input[data-k="e"]','14:20')
g=[x for x in store('days/m1_'+T)['goals'] if x['id']=='gx'][0]
print('end 14:20    :', vals('#dlg-ttg .ttime input'), '| saved', g['ts'], g['te'], '(780, 860) | hint', repr(hint('#dlg-ttg .ttpend')))
setv('#dlg-ttg .ttime input[data-k="e"]','15:00')
g=[x for x in store('days/m1_'+T)['goals'] if x['id']=='gx'][0]
print('end 15:00    :', g['ts'], g['te'], '(start kept 780)')
close_dlg(p)
# 시간표에 아직 안 넣은 할 일: 시작만 적으면 기다렸다가 길이 고르면 저장
ev("(()=>{window.__store['days/m1_%s'].goals.forEach(g=>{if(g.id==='gy'){g.ts=1200;g.te=1260;}});window.__fire();return 1})()"%T);p.wait_for_timeout(500)
click(p,'#tb-gy',600)
click(p,'#dlg-ttg [data-act="ttg-off"]',700)
ev("(()=>{window.__S_open=1;return 1})()")
# ---- 고정 일정: 학원, 과목 두 개
click(p,'.tttools [data-modal="ttset"]',600)
click(p,'#dlg-ttset [data-act="tt-new"][data-v="academy"]',400)
print('subject hint :', hint('#dlg-ttset .fld:last-child h3 small') or ev("[...document.querySelectorAll('#dlg-ttset h3 small')].map(e=>e.textContent).join(' | ')"))
click(p,'#dlg-ttset [data-act="tt-ed-dow"][data-v="3"]',250)
click(p,'#dlg-ttset [data-act="tt-ed-set"][data-k="sid"][data-v="s2"]',250)
click(p,'#dlg-ttset [data-act="tt-ed-set"][data-k="sid"][data-v="s3"]',250)
print('picked       :', ev("[...document.querySelectorAll('#dlg-ttset [data-k=\"sid\"][aria-pressed=\"true\"]')].map(e=>e.textContent).join(',')"))
# 설정 창 안 시간: 시작만 바꿔도 끝 그대로
setv('#dlg-ttset .ttime input[data-k="s"]','17:00')
print('ed times     :', vals('#dlg-ttset .ttime input'))
p.screenshot(path=SH+'v31_ed.png')
click(p,'#dlg-ttset [data-act="tt-ed-save"]',600)
tt=store('progress/m1')['tt'];ac=[b for b in tt['b'] if b['k']=='academy'][-1]
print('saved block  :', {k:ac.get(k) for k in ('sid','sids','s','e','d')})
print('list row     :', ev("[...document.querySelectorAll('#dlg-ttset .ttrow small')].map(e=>e.textContent).join(' | ')"), '| --sc', ev("(document.querySelector('#dlg-ttset .ttrow.k-academy')||{style:{getPropertyValue:()=>''}}).style.getPropertyValue('--sc').slice(0,40)"))
p.screenshot(path=SH+'v31_list.png')
# 한 과목 빼기 -> sids 지워짐
click(p,'#dlg-ttset .ttrow.k-academy',500)
click(p,'#dlg-ttset [data-act="tt-ed-set"][data-k="sid"][data-v="s2"]',250)
click(p,'#dlg-ttset [data-act="tt-ed-save"]',600)
ac=[b for b in store('progress/m1')['tt']['b'] if b['k']=='academy'][-1];print('one subject  :', {k:ac.get(k) for k in ('sid','sids')})
click(p,'#dlg-ttset .ttrow.k-academy',500)
click(p,'#dlg-ttset [data-act="tt-ed-set"][data-k="sid"][data-v="s2"]',250)
click(p,'#dlg-ttset [data-act="tt-ed-save"]',600)
ac=[b for b in store('progress/m1')['tt']['b'] if b['k']=='academy'][-1];print('two again    :', {k:ac.get(k) for k in ('sid','sids')})
close_dlg(p)
fid=ac['id'];sel='#tb-%s-%s'%(fid,T)
print('tt block     :', ev("(()=>{const b=document.querySelector(%s);if(!b)return null;return b.className+' | '+b.innerText.replace(/\\n/g,' / ')+' | scg '+getComputedStyle(b,'::before').backgroundImage.slice(0,30)})()"%json.dumps(sel)))
ev("(()=>{const b=document.querySelector(%s),sc=document.getElementById('ttScroll');if(b&&sc)sc.scrollTop=Math.max(0,b.offsetTop-120);return 1})()"%json.dumps(sel));p.wait_for_timeout(300)
p.screenshot(path=SH+'v31_tt.png')
# 그 날 고정 일정 시간: 시작만 바꾸기
click(p,sel,600)
print('ttf open     :', vals('#dlg-ttf .ttime input'), '| sum', hint('#dlg-ttf .ttsum small'))
setv('#dlg-ttf .ttime input[data-k="s"]','17:30')
ov=store('progress/m1')['tt'].get('ov',{}).get(T,{}).get(fid);print('ttf start    :', vals('#dlg-ttf .ttime input'), '| ov', ov, '(1050, 1260)')
setv('#dlg-ttf .ttime input[data-k="s"]','22:00')
ov=store('progress/m1')['tt'].get('ov',{}).get(T,{}).get(fid);print('ttf bad      :', vals('#dlg-ttf .ttime input'), '| ov kept', ov, '| hint', hint('#dlg-ttf .ttpend'))
setv('#dlg-ttf .ttime input[data-k="e"]','23:30')
ov=store('progress/m1')['tt'].get('ov',{}).get(T,{}).get(fid);print('ttf fixed    :', ov, '(1320, 1410)')
close_dlg(p)
# ---- 학교 교시 시간
click(p,'#meBtn',700);click(p,'.dialog [data-modal="school"]',700)
click(p,'[data-act="sch-times"]',400)
setv('.schtimes input[data-i="0"][data-k="s"]','08:40')
print('sch start    :', vals('.schtimes .schtr:first-child input'), '| saved', store('progress/m1')['tt'].get('sch',{}).get('p',[None])[0])
setv('.schtimes input[data-i="0"][data-k="s"]','09:30')
print('sch bad      :', vals('.schtimes .schtr:first-child input'), '| hint', hint('.schtimes .ttpend'))
setv('.schtimes input[data-i="0"][data-k="e"]','10:10')
print('sch fixed    :', store('progress/m1')['tt']['sch']['p'][0], '| hint gone', not hint('.schtimes .ttpend'))
close_dlg(p)
print('errors',R.errors)
R.close()
