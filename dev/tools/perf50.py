# 50명 x 45일 기록, 메시지 3000개에서 화면별 그리기 시간을 잰다
import sys, json, datetime
sys.path.insert(0, '/home/claude/planner/tools')
from rig import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
R = Rig()
p = R.open(1180, 820, ls={'gbb_note': '9999999999999'}, now=datetime.datetime(2026, 11, 20, 12, 0, 0))
p.emulate_media(reduced_motion='reduce')
p.evaluate("""(N)=>{
  const S=window.__store;const cfg=S['meta/config'];cfg.roster=[];
  for(let i=1;i<=N;i++)cfg.roster.push({id:'m'+i,name:'학생'+String(i).padStart(2,'0')});
  const subs=['s1','s2','s3','s4','s5','s6','s7','s8'];
  const day=(n)=>{const x=new Date(2026,10,20);x.setDate(x.getDate()-n);return x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')+'-'+String(x.getDate()).padStart(2,'0');};
  for(let i=1;i<=N;i++){
    S['progress/m'+i]={units:{s2:[{id:'u1',n:'1단원'},{id:'u2',n:'2단원'}]},checks:{['s2__u1__i1']:true,['s3__i1']:true},skip:{s8:true}};
    for(let k=0;k<45;k++){const d=day(k);
      S['days/m'+i+'_'+d]={goals:[1,2,3,4].map(g=>({id:'g'+i+'_'+k+'_'+g,text:'할 일 '+g+' 길게 적은 내용 입니다',sid:subs[(i+g+k)%8],done:(i+g+k)%3!==0})),mins:{[subs[i%8]]:30+(i*k)%120,[subs[(i+3)%8]]:20},manual:{s1:10},in:d+'T00:10:00.000Z',certAt:(i+k)%4?d+'T12:00:00.000Z':undefined};
      if(!S['days/m'+i+'_'+d].certAt)delete S['days/m'+i+'_'+d].certAt;}
  }
  for(let k=0;k<3000;k++)S['msgs/z'+k]={from:'m'+(1+k%N),to:'all',text:'메시지 '+k,at:Date.now()-k*60000};
  for(let k=0;k<120;k++)S['quiz/q'+k]={kind:k%3?'quiz':'ask',mid:'m'+(1+k%N),sid:'s2',q:'문제 '+k,a:'정답',at:Date.now()-k*3600000};
  window.__fire();
}""", N)
p.wait_for_timeout(2500)
close_dlg(p)
tabs = ['cal', 'room', 'prog', 'rank', 'report', 'play', 'board', 'chat']
for t in tabs:
    ms = p.evaluate("""(t)=>{const b=document.querySelector('[data-act="tab"][data-tab="'+t+'"]');const a=performance.now();b.dispatchEvent(new MouseEvent('click',{bubbles:true}));return performance.now()-a}""", t)
    p.wait_for_timeout(300)
    print('%-7s %7.1f ms' % (t, ms))
# 진도 모두 보기, 순위 최종, 도전 배지
p.evaluate("()=>document.querySelector('[data-act=\"tab\"][data-tab=\"prog\"]').click()");p.wait_for_timeout(200)
print('prog-all %7.1f ms' % p.evaluate("()=>{const b=document.querySelector('[data-act=\"prog-mode\"][data-id=\"all\"]');const a=performance.now();b.click();return performance.now()-a}"))
p.evaluate("()=>document.querySelector('[data-act=\"tab\"][data-tab=\"play\"]').click()");p.wait_for_timeout(200)
print('badges  %7.1f ms' % p.evaluate("()=>{const b=document.querySelector('[data-act=\"play-tab\"][data-id=\"badge\"]');const a=performance.now();b.click();return performance.now()-a}"))
p.evaluate("()=>document.querySelector('[data-act=\"tab\"][data-tab=\"rank\"]').click()");p.wait_for_timeout(200)
print('final   %7.1f ms' % p.evaluate("()=>{const b=document.querySelector('[data-act=\"range\"][data-id=\"all\"]');const a=performance.now();b.click();return performance.now()-a}"))
# 한 번의 변화(다른 사람의 기록 하나)가 들어올 때 다시 그리기
for t in ['cal','chat']:
    p.evaluate("(t)=>document.querySelector('[data-act=\"tab\"][data-tab=\"'+t+'\"]').click()", t);p.wait_for_timeout(300)
    ms = p.evaluate("()=>{const a=performance.now();window.__store['msgs/zz'+Date.now()]={from:'m2',to:'all',text:'새',at:Date.now()};window.__fire();return performance.now()-a}")
    print('incoming on %-5s %7.1f ms' % (t, ms))
print('errors', R.errors)
R.close()
