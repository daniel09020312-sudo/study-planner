import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
SEED="""()=>{const S=window.__store,d0=new Date();const f=n=>{const d=new Date(d0);d.setDate(d.getDate()+n);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
const L=[[1,'s5','수행평가 (실험 보고서)'],[1,'s3','수행평가 (탐구 프로젝트 발표)'],[1,'s4','수행평가 (에세이)'],[1,'s1','수행평가 (문법 탐구)'],[2,'s2','수행평가 (서술형)'],[3,'s6','수행평가 (모형 만들기)'],[3,'s5','발표 (반응 속도)'],[5,'s7','제출 (가계도 분석)'],[6,'s8','수행평가 (실험 보고서 2)'],[6,'s3','퀴즈'],[8,'s4','수행평가 (토론)'],[9,'s1','수행평가 (보고서)']];
L.forEach((x,i)=>{const nm=['화법과 언어','미적분Ⅰ','확률과 통계','영어 비평적 읽기와 쓰기','화학 반응의 세계','세포와 물질대사','생물의 유전','생명과학 실험'][+x[1].slice(1)-1];S['events/z'+i]={mid:'m1',date:f(x[0]),title:nm+' '+x[2],shared:i%3===0,kind:'수행평가',sid:x[1]};});
S['events/zz']={mid:'m1',date:f(4),title:'11월 모의고사',shared:false,kind:'시험',sid:''};
window.__fire();}"""
R=Rig()
for w,h in ((1180,820),(390,844)):
    p=R.open(w,h,ls={'gbb_note':'9999999999999'});close_dlg(p);p.evaluate(SEED);p.wait_for_timeout(700)
    print(w,'legend:',st(p,"(document.querySelector('.calleg')||{}).innerText"))
    print(w,'cell chips:',st(p,"[...document.querySelectorAll('.cell')].filter(c=>c.querySelector('.sevs')).slice(0,4).map(c=>c.querySelector('.dn').textContent+':'+[...c.querySelectorAll('.sev')].map(i=>i.textContent).join(',')).join(' | ')"))
    print(w,'overflow:',st(p,"document.documentElement.scrollWidth>innerWidth+1"),'| chip overflow',st(p,"[...document.querySelectorAll('.cell')].some(c=>c.scrollWidth>c.clientWidth+1)"))
    p.screenshot(path=SH+'v23_cal_%d.png'%w,full_page=(w==390))
    d1=st(p,"(()=>{const d=new Date();d.setDate(d.getDate()+1);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()")
    p.evaluate("(d)=>document.querySelector('.cell[data-d=\"'+d+'\"]').click()",d1);p.wait_for_timeout(600)
    print(w,'day panel:',st(p,"[...document.querySelectorAll('#c-day .evrow')].map(e=>e.innerText.split(String.fromCharCode(10)).join(' ')).join(' | ')"))
    if w==1180:p.locator('#c-day').screenshot(path=SH+'v23_day.png')
print('errors',R.errors)
R.close()
