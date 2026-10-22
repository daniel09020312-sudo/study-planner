import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
SEED=open('/home/claude/planner/tools/t_v13.py').read().split('SEED=r"""')[1].split('"""')[0]
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_calmode':'tt','gbb_ttspan':'7'});close_dlg(p)
T=p.evaluate(SEED);p.wait_for_timeout(500)
# 고정 학교 일정 + 다른 사람(m2)의 학교 시간표
p.evaluate("""()=>{const S=window.__store;const pr=S['progress/m1']||{};pr.tt={b:[{id:'b1',k:'school',t:'학교',sid:'',d:'0111110',s:500,e:990}]};S['progress/m1']=pr;
 const p2=S['progress/m2']||{};p2.tt={sch:{p:[{s:520,e:570},{s:580,e:630},{s:640,e:690},{s:700,e:750},{s:810,e:860},{s:870,e:920},{s:930,e:980}],w:{'1':{p0:{s:'s1'},p1:{s:'s2'},p2:{t:'창체'}},'2':{p0:{s:'s3'}}}}};S['progress/m2']=p2;window.__fire();}""");p.wait_for_timeout(500)
print('toolbar     :',st(p,"[...document.querySelectorAll('.tttools .acts button')].map(b=>b.textContent).join(' | ')"))
click(p,'.tttools [data-modal="school"]',600)
print('modal       :',st(p,"document.querySelector('#dlg-school h2').textContent"),'| rows',st(p,"document.querySelectorAll('#dlg-school table.sch tbody tr').length"),'| who chips',st(p,"[...document.querySelectorAll('#dlg-school .schwho .chip')].map(b=>b.textContent).join(',')"))
# 월 1교시부터 차례로
click(p,'#dlg-school .schc[data-d="1"][data-i="0"]',300)
for sid in ['s1','s2','s3']: click(p,'#dlg-school .chip[data-act="sch-put"][data-v="%s"]'%sid,300);click(p,'#dlg-school [data-act="sch-next"]',300)
print('after 3     :',st(p,"JSON.stringify(window.__store['progress/m1'].tt.sch.w)"),'| sel',st(p,"(document.querySelector('#dlg-school .schc.on')||{}).getAttribute&&document.querySelector('#dlg-school .schc.on').getAttribute('aria-label')"))
click(p,'#dlg-school .chip[data-act="sch-put"][data-t="창체"]',300);click(p,'#dlg-school [data-act="sch-next"]',300)
p.fill('#dlg-school input[data-draft="schT"]','자율');click(p,'#dlg-school [data-act="sch-text"]',300);click(p,'#dlg-school [data-act="sch-next"]',300)
click(p,'#dlg-school .schc[data-d="2"][data-i="0"]',300);click(p,'#dlg-school .chip[data-act="sch-put"][data-v="s5"]',300)
click(p,'#dlg-school .schc[data-d="1"][data-i="3"]',300);click(p,'#dlg-school [data-act="sch-clear"]',300)
print('cells       :',st(p,"[...document.querySelectorAll('#dlg-school tbody tr')].slice(0,5).map(r=>[...r.querySelectorAll('.schc')].map(c=>c.textContent.replace('+','·')).join('/')).join(' || ')"))
p.screenshot(path=SH+'v15_school_edit.png')
click(p,'#dlg-school [data-act="sch-times"]',300)
p.evaluate("()=>{const i=document.querySelector('#dlg-school input[data-chg=\"sch-time\"][data-i=\"0\"][data-k=\"s\"]');i.value='08:30';i.dispatchEvent(new Event('change',{bubbles:true}));}");p.wait_for_timeout(300)
click(p,'#dlg-school [data-act="sch-padd"]',300)
print('periods     :',st(p,"JSON.stringify(window.__store['progress/m1'].tt.sch.p.map(x=>[x.s,x.e]))"))
click(p,'#dlg-school [data-act="sch-fit"]',400)
print('fit         :',st(p,"JSON.stringify(window.__store['progress/m1'].tt.b.map(b=>[b.k,b.s,b.e]))"),'|',st(p,"(document.querySelector('.flash span')||{}).textContent"))
click(p,'#dlg-school [data-act="sch-pdel"]',300)
p.screenshot(path=SH+'v15_school_times.png')
# 다른 사람 시간표 보기, 가져오기는 확인만
click(p,'#dlg-school .schwho .chip[data-id="m2"]',400)
print('m2 view     :',st(p,"document.querySelector('#dlg-school h2').textContent"),'| ro',st(p,"!document.querySelector('#dlg-school button.schc')"),'| copy btn',st(p,"!!document.querySelector('[data-act=\"sch-copy\"]')"))
close_dlg(p);p.wait_for_timeout(400)
# 시간표에 교시 표시
mon=st(p,"[...document.querySelectorAll('.ttcol')].map(c=>c.dataset.d).find(d=>new Date(d+'T00:00').getDay()===1)")
# 학교 시간표가 있는 요일은 고정 '학교' 덩어리 대신 교시마다 칸이 나온다 (v29)
print('mon         :',mon,'| periods',st(p,"[...document.querySelectorAll('#tc-%s .ttsc')].map(e=>e.innerText.replace(/\\n/g,' ')).join(', ')"%mon),'| fixed school hidden',st(p,"!document.getElementById('tb-b1-%s')"%mon))
p.evaluate("()=>{document.getElementById('ttScroll').scrollTop=60}");p.wait_for_timeout(200)
p.screenshot(path=SH+'v15_tt_school.png')
click(p,'#tc-%s .ttsc'%mon,600)
print('opens       :',st(p,"(document.getElementById('dlgT')||{}).textContent"))
close_dlg(p)
# ---- 확인 필요 지우기
now=st(p,"Date.now()")
p.evaluate("""([T,now])=>{const S=window.__store;
 S['days/m1_'+T].mins={s2:420,s6:40};
 S['flags/fA']={mid:'m1',sid:'s2',start:now-6*3600e3,end:now-3600e3,why:['cap'],cd:{[T]:300}};
 S['days/m2_'+T].mins={s2:330,s5:45};
 S['flags/fB']={mid:'m2',sid:'s2',start:now-5*3600e3-60e3,end:now-60e3,why:['cap']};
 window.__fire();}""",[T,now]);p.wait_for_timeout(300)
click(p,'[data-act="cal-mode"][data-id="cal"]',300);p.evaluate("()=>{}")
click(p,'.navs [data-tab="room"]',900)
print('flags       :',st(p,"[...document.querySelectorAll('#c-flags .flag')].map(e=>e.textContent).join(' || ')"))
p.evaluate("()=>document.getElementById('c-flags').scrollIntoView()");p.wait_for_timeout(200)
p.screenshot(path=SH+'v15_flags.png')
sc0=st(p,"document.querySelector('#rk-m1, .fr#fr-m1 .fp b') ? document.querySelector('#fr-m1 .fp b').textContent : ''")
click(p,'[data-act="flag-cut"][data-id="fA"]',300)
print('confirm     :',st(p,"document.querySelector('[data-act=\"flag-cut\"][data-id=\"fA\"]').textContent"))
click(p,'[data-act="flag-cut"][data-id="fA"]',700)
print('m1 mins     :',json.dumps(store(p,'days/m1_'+T)['mins']),'| flag cut',bool(store(p,'flags/fA').get('cut')),'| score',sc0,'->',st(p,"document.querySelector('#fr-m1 .fp b').textContent"),'| flash',st(p,"(document.querySelector('.flash span')||{}).textContent"))
click(p,'.flash [data-act="undo"]',700)
print('undo        :',json.dumps(store(p,'days/m1_'+T)['mins']),'| flag cut',bool(store(p,'flags/fA').get('cut')))
# 방장(m1)이 m2 것도 지울 수 있음 (cd 없는 예전 기록)
click(p,'[data-act="flag-cut"][data-id="fB"]',300);click(p,'[data-act="flag-cut"][data-id="fB"]',700)
print('m2 mins     :',json.dumps(store(p,'days/m2_'+T)['mins']),'| flags left',st(p,"document.querySelectorAll('#c-flags .flag').length"))
print('errors',R.errors)
# m3(방장 아님) 시점: 남의 기록에는 버튼 없음
q=R.open(1180,820,me='m3',ls={'gbb_note':'9999999999999'});close_dlg(q);q.evaluate(SEED)
q.evaluate("""([T,now])=>{const S=window.__store;S['days/m1_'+T].mins={s2:420};S['flags/fA']={mid:'m1',sid:'s2',start:now-6*3600e3,end:now-3600e3,why:['cap'],cd:{[T]:300}};window.__fire();}""",[T,now]);q.wait_for_timeout(300)
click(q,'.navs [data-tab="room"]',900)
print('m3 sees     :',st(q,"document.querySelectorAll('#c-flags .flag').length"),'| buttons',st(q,"document.querySelectorAll('#c-flags [data-act=\"flag-cut\"]').length"))
# 타이머 기록 추적: 6시간 전에 켠 타이머가 자동으로 끝나면 cd가 기록된 확인 필요가 생김
r=R.open(1180,820,ls={'gbb_note':'9999999999999'});close_dlg(r);r.evaluate(SEED)
r.evaluate("()=>{const S=window.__store,n=Date.now();S['live/m1']={sid:'s3',start:n-2*3600e3,flushed:n-2*3600e3,cm:0};window.__fire();}");r.wait_for_timeout(1500)
r.evaluate("()=>{const S=window.__store,L=S['live/m1'];if(L){L.start-=4*3600e3;L.flushed-=4*3600e3;if(L.cm!=null){} }window.__fire();}");r.wait_for_timeout(2500)
fl=[v for k,v in r.evaluate("()=>Object.entries(window.__store).filter(([k])=>k.startsWith('flags/'))")]
print('auto flag   :',json.dumps(fl)[:300])
print('live left   :',r.evaluate("()=>!!window.__store['live/m1']"),'| mins',json.dumps(store(r,'days/m1_'+T)['mins']))
print('errors',R.errors)
R.close()
