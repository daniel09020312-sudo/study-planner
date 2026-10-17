# ---------------------------------------------------------------- 타이머 종류 (스톱워치, 뽀모도로, 목표 시간)
sub("function isStale(L){return Date.now()-(+L.start||0)>MAXRUN;}", r"""function runStart(L){return +L.run||+L.start||0;}
function isStale(L){return Date.now()-runStart(L)>MAXRUN;}
function clampN(v,lo,hi,d){v=Math.round(+v);return v>=lo&&v<=hi?v:d;}
var RING=565.49,TMODES=[['sw','스톱워치'],['pomo','뽀모도로'],['goal','목표 시간']],POMOS=[[25,5],[50,10]],GOALS=[30,50,60,90,120];
/* 지금 타이머 상태: 종류, 쉬는 중인지, 남은 시간, 집중한 시간 */
function lv(L,now){
  var s=+L.start||now,e=Math.max(0,Math.min(now,runStart(L)+MAXRUN)-s),o={mode:'sw',rest:false,over:false,e:e,focus:e,left:0,frac:0,n:0};
  if(L.mode==='pomo'&&+L.f>0&&+L.b>0){
    var f=L.f*60000,c=f+L.b*60000,k=Math.floor(e/c),w=e-k*c;
    o.mode='pomo';o.n=(+L.n0||0)+k+1;o.rest=w>=f;o.left=o.rest?c-w:f-w;o.frac=o.rest?(w-f)/(c-f):w/f;o.focus=k*f+Math.min(w,f);
  }else if(L.mode==='goal'&&+L.g>0){
    var g=L.g*60000;o.mode='goal';o.left=Math.max(0,g-e);o.frac=Math.min(1,e/g);o.over=e>=g;o.focus=Math.min(e,g);
  }
  return o;
}
function fmtLeft(ms){var s=Math.max(0,Math.ceil(ms/1000)),h=Math.floor(s/3600),m=Math.floor(s%3600/60);return (h?h+':':'')+String(m).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
function lvText(o){return o.mode==='sw'?fmtElapsed(o.e):fmtLeft(o.left);}
function credited(L){return L.cm!=null?(+L.cm||0):Math.max(0,Math.floor(((+L.flushed||+L.start)-(+L.start))/60000));}
function liveLine(V,mid,L,o){
  var c='<span data-lv="'+esc(mid)+'">'+lvText(o)+'</span>',sl=esc(subLabel(V,L.sid));
  if(o.mode==='pomo')return o.rest?'쉬는 중, '+c+' 남음':c+' 남음, '+sl+' '+o.n+'번째 집중';
  if(o.mode==='goal')return c+' 남음, '+sl+' 공부 중';
  return c+' '+sl+' 공부 중';
}
var TSTYLES=[['ring','링'],['digits','숫자'],['bar','막대'],['pie','원판'],['flip','넘김 시계']];
function tstyle(){var t=S.tstyle;return TSTYLES.some(function(x){return x[0]===t;})?t:'ring';}
/* 모양에 보여줄 비율: 카운트다운은 남은 비율, 스톱워치는 이번 1시간 중 지난 비율 */
function lvShow(o){return o.mode==='sw'?(o.e%3600000)/3600000:Math.max(0,Math.min(1,1-o.frac));}
function lvPie(L,o){if(o.mode==='sw')return (o.e%3600000)/3600000;var tot=o.mode==='pomo'?(o.rest?+L.b:+L.f):+L.g;return Math.max(0,Math.min(1,o.left/(Math.max(60,tot||60)*60000)));}
function piePath(p){
  p=Math.max(0,Math.min(1,+p||0));if(p<=0.0005)return 'M100,100 Z';
  if(p>=0.9995)return 'M100,22 A78,78 0 1,1 100,178 A78,78 0 1,1 100,22 Z';
  var a=p*2*Math.PI,x=100+78*Math.sin(a),y=100-78*Math.cos(a);
  return 'M100,100 L100,22 A78,78 0 '+(p>.5?1:0)+',1 '+x.toFixed(2)+','+y.toFixed(2)+' Z';
}
var PIE_TICKS=(function(){var t='';for(var i=0;i<60;i++){var a=i*Math.PI/30,b=i%5===0,r1=b?83:87;t+='<line'+(b?' class="bg"':'')+' x1="'+(100+r1*Math.sin(a)).toFixed(1)+'" y1="'+(100-r1*Math.cos(a)).toFixed(1)+'" x2="'+(100+93*Math.sin(a)).toFixed(1)+'" y2="'+(100-93*Math.cos(a)).toFixed(1)+'"/>';}return t;})();
function flipHtml(t){return String(t).split('').map(function(c){return c===':'?'<em>:</em>':'<i>'+c+'</i>';}).join('');}
function setFlip(el,t){
  var old=el.getAttribute('data-t')||'';if(old===t)return;
  el.setAttribute('data-t',t);el.classList.toggle('long',t.length>=7);
  if(old.length!==t.length||el.children.length!==t.length){el.innerHTML=flipHtml(t);return;}
  for(var i=0;i<t.length;i++){var c=el.children[i];if(t[i]!==old[i]&&c){c.textContent=t[i];if(!reduced){c.classList.remove('chg');void c.offsetWidth;c.classList.add('chg');}}}
}
function faceInfo(V,L,o){
  var sl=esc(subLabel(V,L.sid)),f={text:lvText(o),pie:lvPie(L,o)};
  if(o.mode==='pomo'){f.top=o.rest?'쉬는 시간':o.n+'번째 집중';f.sub=o.rest?'다음은 '+(o.n+1)+'번째 집중':sl;}
  else if(o.mode==='goal'){f.top='목표 '+fmtMins(L.g);f.sub=sl;}
  else{f.top='공부 중';f.sub=sl;}
  return f;
}
function faceIdle(m,p,g){
  if(m==='pomo')return {idle:true,text:fmtLeft(p.f*60000),top:'집중 '+p.f+'분, 쉬기 '+p.b+'분',sub:'시작 전',pie:p.f/Math.max(60,p.f)};
  if(m==='goal')return {idle:true,text:fmtLeft(g*60000),top:'목표 '+fmtMins(g),sub:'시작 전',pie:g/Math.max(60,g)};
  return {idle:true,text:'00:00:00',top:'스톱워치',sub:'시작 전',pie:0};
}
function faceHtml(st,mid,o,f){
  var a=mid?' data-lv="'+esc(mid)+'"':'',pa=mid?' data-lvp="'+esc(mid)+'"':'',cls=(o.rest?' rest':'')+(f.idle?' idle':'')+(o.mode==='sw'?' swm':'');
  var show=f.idle?(o.mode==='sw'?0:1):lvShow(o),lg=f.text.length>=7?' long':'',lab='<small>'+f.top+'</small>',sub='<span>'+f.sub+'</span>';
  var txt=st==='flip'?'<b class="tt flip'+lg+'"'+(mid?' data-lvf="'+esc(mid)+'"':'')+' data-t="'+esc(f.text)+'">'+flipHtml(f.text)+'</b>':'<b class="tt'+lg+'"'+a+'>'+f.text+'</b>';
  if(st==='ring')return '<div class="tf ring'+cls+'"><svg viewBox="0 0 200 200" aria-hidden="true"><circle class="rg-t" cx="100" cy="100" r="90"/><circle class="rg-p"'+pa+' data-k="ring" cx="100" cy="100" r="90" style="stroke-dashoffset:'+(RING*(1-show)).toFixed(1)+'"/></svg><div class="rg-in">'+lab+txt+sub+'</div></div>';
  if(st==='pie')return '<div class="tf pie'+cls+'"><svg viewBox="0 0 200 200" aria-hidden="true"><circle class="pf" cx="100" cy="100" r="97"/><path class="pw"'+pa+' data-k="pie" d="'+piePath(f.pie)+'"/><g class="pt">'+PIE_TICKS+'</g><circle class="pk" cx="100" cy="100" r="7"/></svg><div class="ptx">'+lab+txt+sub+'</div></div>';
  if(st==='bar')return '<div class="tf bar'+cls+'">'+lab+txt+'<div class="bbar" aria-hidden="true"><i'+pa+' data-k="bar" style="width:'+(show*100).toFixed(2)+'%"></i></div>'+sub+'</div>';
  return '<div class="tf '+(st==='flip'?'flipf':'digits')+cls+'">'+lab+txt+sub+'</div>';
}
function timerActs(o){return '<div class="tacts">'+(o.rest?'<button class="btn xl soft" data-act="pomo-skip">쉬는 시간 건너뛰기</button>':'')+'<button class="btn xl" data-act="timer-stop">끝내고 기록하기</button></div>';}
function timerBody(V,L,sel,subs){
  var now=Date.now(),o=L?lv(L,now):null,m=o?o.mode:S.tmode,p=S.pomo,g=S.goal,h='';
  if(!L)h+='<div class="seg tseg" role="group" aria-label="타이머 종류">'+TMODES.map(function(x){return '<button data-act="tmode" data-v="'+x[0]+'" aria-pressed="'+(m===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  h+='<div class="chips scroll">';
  subs.forEach(function(s){h+='<button class="chip" data-act="time-pick" data-id="'+esc(s.id)+'" aria-pressed="'+(sel===s.id?'true':'false')+'">'+esc(s.name)+'</button>';});
  h+='<button class="chip" data-act="time-pick" data-id="etc" aria-pressed="'+(sel==='etc'?'true':'false')+'">기타</button></div>';
  if(!L&&m==='pomo'){
    var pc=S.pomoCustom||!POMOS.some(function(x){return x[0]===p.f&&x[1]===p.b;});
    h+='<div class="tset" id="tset-pomo"><div class="chips">'+POMOS.map(function(x){return '<button class="chip" data-act="pomo-set" data-f="'+x[0]+'" data-b="'+x[1]+'" aria-pressed="'+(!pc&&p.f===x[0]&&p.b===x[1]?'true':'false')+'">'+x[0]+'분 집중, '+x[1]+'분 쉬기</button>';}).join('')+'<button class="chip" data-act="pomo-custom" aria-pressed="'+(pc?'true':'false')+'">직접 설정</button></div>';
    if(pc)h+='<div class="trow"><span>집중</span><div class="amt"><button data-act="pomo-adj" data-k="f" data-d="-5" aria-label="집중 5분 줄이기">-5</button><b>'+p.f+'분</b><button data-act="pomo-adj" data-k="f" data-d="5" aria-label="집중 5분 늘리기">+5</button></div></div><div class="trow"><span>쉬기</span><div class="amt"><button data-act="pomo-adj" data-k="b" data-d="-1" aria-label="쉬기 1분 줄이기">-1</button><b>'+p.b+'분</b><button data-act="pomo-adj" data-k="b" data-d="1" aria-label="쉬기 1분 늘리기">+1</button></div></div>';
    h+='</div>';
  }
  if(!L&&m==='goal'){
    var gc=S.goalCustom||GOALS.indexOf(g)<0;
    h+='<div class="tset" id="tset-goal"><div class="chips">'+GOALS.map(function(x){return '<button class="chip" data-act="goal-set" data-v="'+x+'" aria-pressed="'+(!gc&&g===x?'true':'false')+'">'+fmtMins(x)+'</button>';}).join('')+'<button class="chip" data-act="goal-custom" aria-pressed="'+(gc?'true':'false')+'">직접 설정</button></div>';
    if(gc)h+='<div class="trow"><span>목표</span><div class="amt"><button data-act="goal-adj" data-d="-10" aria-label="10분 줄이기">-10</button><b>'+fmtMins(g)+'</b><button data-act="goal-adj" data-d="10" aria-label="10분 늘리기">+10</button></div></div>';
    h+='</div>';
  }
  if(L){
    h+=faceHtml(tstyle(),V.me,o,faceInfo(V,L,o));
    h+=timerActs(o);
  }else{
    h+=faceHtml(tstyle(),'',{mode:m,rest:false,frac:0,e:0},faceIdle(m,p,g));
    h+='<button class="btn xl primary" data-act="timer-start">'+esc(subLabel(V,sel))+' 공부 시작</button>';
  }
  h+='<p class="hint" style="margin-top:12px">'+(m==='pomo'?'집중한 시간만 기록되고 쉬는 시간은 기록되지 않습니다. 끝내기를 누를 때까지 반복하고, 5시간이 넘으면 자동으로 끝납니다.':m==='goal'?'목표 시간이 되면 자동으로 끝나고 기록됩니다. 먼저 끝내도 그때까지 한 만큼 기록됩니다.':'끝내기를 누르면 기록됩니다. 한 번에 5시간까지 기록되고, 5시간이 넘으면 자동으로 끝납니다.')+'</p>';
  if(m!=='sw')h+='<div class="tsnd"><span class="hint">'+(m==='pomo'?'집중과 쉬는 시간이 바뀔 때':'목표 시간이 끝날 때')+' 소리 알림: '+(S.sound?'켜짐':'꺼짐')+'</span><button class="del" data-act="sound">'+(S.sound?'끄기':'켜기')+'</button></div>';
  return h;
}
function modalFocus(V){
  var L=liveOf(V,V.me),o=lv(L,Date.now()),b;
  b=faceHtml(tstyle(),V.me,o,faceInfo(V,L,o));
  return '<div class="fview" id="dlg-focus" role="dialog" aria-modal="true" aria-label="타이머 크게 보기" tabindex="-1">'+b+timerActs(o).replace('</div>','<button class="btn xl soft" data-act="modal-close">작게 보기</button></div>')+'</div>';
}
function endFocus(){if(S.modal&&S.modal.type==='focus'){S.modal=null;S.closing=false;}lock(false);S.myPh=null;}""")

# 달력 홈의 오늘 점수 카드
cut("  if(L)h+='<div class=\"what\"><b>'+esc(subLabel(V,L.sid))+' 공부 중</b>", "  else h+='<div class=\"what\"><b>오늘 공부 '",
    "  if(L){var lo=lv(L,Date.now());h+='<div class=\"what\"><b>'+(lo.rest?'쉬는 중':esc(subLabel(V,L.sid))+' 공부 중')+'</b><span class=\"hint\"><span data-lv=\"'+esc(V.me)+'\">'+lvText(lo)+'</span>'+(lo.mode==='sw'?'':' 남음')+'</span></div><button class=\"btn small\" data-act=\"timer-stop\">끝내기</button>';}\n")
# 참여 인원 목록
sub("  list.forEach(function(x){x.on=x.L&&!isStale(x.L);});", "  list.forEach(function(x){x.o=x.L?lv(x.L,now):null;x.on=!!x.L&&!isStale(x.L)&&!x.o.over;});")
sub("var onN=list.filter(function(x){return x.on;}).length,flagged={};", "var onN=list.filter(function(x){return x.on&&!x.o.rest;}).length,flagged={};")
sub("    if(x.on)st='<small class=\"live\"><span data-since=\"'+(+x.L.start)+'\">'+fmtElapsed(now-x.L.start)+'</span> '+esc(subLabel(V,x.L.sid))+' 공부 중</small>';",
    "    if(x.on)st='<small class=\"live'+(x.o.rest?' rest':'')+'\">'+liveLine(V,x.p.id,x.L,x.o)+'</small>';")
# 공부방 타이머 카드
cut("  h+='<section class=\"card\" id=\"c-timer\" style=\"--k:0\">", "  h+='<div class=\"sec\"><h3>직접 입력",
    "  h+='<section class=\"card\" id=\"c-timer\" style=\"--k:0\"><div class=\"ct\"><h2>공부 타이머<small>오늘 '+fmtMins(total)+'</small></h2>'+(L?'<button class=\"btn small soft\" data-act=\"focus-open\">크게 보기</button>':'')+'</div>';\n"
    "  h+=timerBody(V,L,sel,subs);\n")
assert 'data-since' not in s.split('/* ---------- 타이머와 집중 확인')[0]

# 기록 계산
cut("function flushLive(L,now){", "function dawnMins(s,e){", r"""function flushLive(L,now){
  var o=lv(L,now),cm=credited(L),mins=Math.floor(o.focus/60000)-cm,n=clone(L);
  if(mins>0){editDay(today(),function(d){d.mins[L.sid]=Math.min(1200,(+d.mins[L.sid]||0)+mins);});cm+=mins;}
  n.cm=cm;n.flushed=o.mode==='sw'?+L.start+cm*60000:now;
  return n;
}
""")
sub("  var st=+L.start,why=[];if(!st)return;", "  var st=runStart(L),why=[];if(!st)return;")
cut("function startTimer(){", "function confirmCheck(){", r"""function startTimer(){
  var V=view();if(!V.me||!need()||liveOf(V,V.me))return;
  var subs=mySubs(V),sid=S.draft.timeSub||(subs[0]?subs[0].id:'etc'),now=Date.now(),d={sid:sid,start:now,flushed:now,cm:0};
  if(S.tmode==='pomo'){d.mode='pomo';d.f=S.pomo.f;d.b=S.pomo.b;}
  else if(S.tmode==='goal'){d.mode='goal';d.g=S.goal;}
  if(d.mode&&S.sound)primeAudio();
  S.myPh=null;save('live/'+V.me,d);
}
function stopTimer(){
  var V=view(),L=V.me&&liveOf(V,V.me);if(!L||!need())return;
  flagSession(V,L,Date.now());flushLive(L,Date.now());save('live/'+V.me,null);S.check=null;endFocus();
}
function skipRest(){
  var V=view(),L=V.me&&liveOf(V,V.me);if(!L||L.mode!=='pomo'||!need())return;
  var now=Date.now(),o=lv(L,now);if(!o.rest)return;
  flushLive(L,now);S.myPh=null;
  save('live/'+V.me,{sid:L.sid,mode:'pomo',f:L.f,b:L.b,start:now,flushed:now,cm:0,run:runStart(L),n0:o.n});
}
""")
sub("  var now=Date.now(),fl=flushLive(L,now);\n  save('live/'+V.me,{sid:L.sid,start:+L.start,last:now,flushed:fl,next:nextCheck(V)});",
    "  var now=Date.now(),nl=flushLive(L,now);nl.last=now;nl.next=nextCheck(V);\n  save('live/'+V.me,nl);")
cut("function tick(){", "  if(S.check){", r"""function tick(){
  var now=Date.now(),V=V0,els=document.querySelectorAll('[data-lv],[data-lvp],[data-lvf]'),memo={},key='',i,k;
  for(i=0;i<els.length;i++){
    var el=els[i],mid=el.getAttribute('data-lv')||el.getAttribute('data-lvp')||el.getAttribute('data-lvf'),Lx=V&&V.live[mid];if(!Lx||!Lx.start)continue;
    var ox=memo[mid]||(memo[mid]=lv(Lx,now));
    if(el.hasAttribute('data-lvp')){var pk=el.getAttribute('data-k');if(pk==='ring')el.style.strokeDashoffset=(RING*(1-lvShow(ox))).toFixed(1);else if(pk==='bar')el.style.width=(lvShow(ox)*100).toFixed(2)+'%';else if(pk==='pie')el.setAttribute('d',piePath(lvPie(Lx,ox)));}
    else if(el.hasAttribute('data-lvf'))setFlip(el,lvText(ox));
    else{var tx=lvText(ox);if(el.textContent!==tx){el.textContent=tx;if(el.classList.contains('tt'))el.classList.toggle('long',tx.length>=7);}}
  }
  if(S.ready&&V){for(k in V.live){var Lk=V.live[k];if(Lk&&Lk.start&&Lk.mode){var ok=memo[k]||lv(Lk,now);key+=k+(ok.rest?'r':'f')+(ok.over?'o':'')+ok.n+';';}}}
  if(S.ready&&V&&V.me&&canWrite()){
    var L=liveOf(V,V.me);
    if(L){
      var o=memo[V.me]||lv(L,now),pend=Math.floor(o.focus/60000)-credited(L);
      if(now-runStart(L)>MAXRUN){flagSession(V,L,now);flushLive(L,now);save('live/'+V.me,null);endFocus();flash('타이머가 5시간을 넘어 자동으로 끝났습니다.');render();}
      else if(o.over){flagSession(V,L,now);flushLive(L,now);save('live/'+V.me,null);endFocus();beep();flash('목표한 '+fmtMins(L.g)+'을 채웠습니다. 공부 시간에 기록했습니다.');render();}
      else{
        if(S.myPh&&S.myPh.s===+L.start&&S.myPh.rest!==o.rest){beep();flash(o.rest?'집중 '+L.f+'분이 끝났습니다. '+L.b+'분 쉬세요.':'쉬는 시간이 끝났습니다. '+o.n+'번째 집중을 시작합니다.');}
        S.myPh={s:+L.start,rest:o.rest};
        if(pend>=10||(pend>0&&o.rest)){save('live/'+V.me,flushLive(L,now));render();}
      }
    }else S.myPh=null;
  }
  if(key!==S.phKey){var firstKey=S.phKey==null;S.phKey=key;if(!firstKey)render();}
""")

# 동작
sub("    case 'timer-stop':stopTimer();break;", r"""    case 'timer-stop':stopTimer();break;
    case 'tmode':{var tmv=el.getAttribute('data-v');S.tmode=tmv==='pomo'||tmv==='goal'?tmv:'sw';lsSet('gbb_tmode',S.tmode);break;}
    case 'pomo-set':S.pomo={f:clampN(el.getAttribute('data-f'),10,90,25),b:clampN(el.getAttribute('data-b'),3,30,5)};S.pomoCustom=false;lsSet('gbb_pomo',JSON.stringify(S.pomo));break;
    case 'pomo-custom':S.pomoCustom=true;break;
    case 'pomo-adj':{
      var tpk=el.getAttribute('data-k'),tpd=+el.getAttribute('data-d')||0;
      if(tpk==='f')S.pomo.f=Math.max(10,Math.min(90,S.pomo.f+tpd));else S.pomo.b=Math.max(3,Math.min(30,S.pomo.b+tpd));
      S.pomoCustom=true;lsSet('gbb_pomo',JSON.stringify(S.pomo));break;
    }
    case 'goal-set':S.goal=clampN(el.getAttribute('data-v'),10,240,60);S.goalCustom=false;lsSet('gbb_goal',String(S.goal));break;
    case 'goal-custom':S.goalCustom=true;break;
    case 'goal-adj':S.goal=Math.max(10,Math.min(240,S.goal+(+el.getAttribute('data-d')||0)));S.goalCustom=true;lsSet('gbb_goal',String(S.goal));break;
    case 'pomo-skip':skipRest();break;
    case 'focus-open':{
      if(!liveOf(view(),view().me))break;
      lock(true);S.modal={type:'focus'};S.closing=false;S.sync=true;render();
      var fvw=layer.querySelector('.fview');if(fvw)fvw.focus({preventScroll:true});
      return;
    }""")
sub("S.songMood='';S.songFilter='';S.songRoll=null;",
    "S.tmode=(function(m){return m==='pomo'||m==='goal'?m:'sw';})(lsGet('gbb_tmode'));\n"
    "S.pomo=(function(){var p=null;try{p=JSON.parse(lsGet('gbb_pomo')||'null');}catch(e){}p=p&&typeof p==='object'?p:{};return {f:clampN(p.f,10,90,25),b:clampN(p.b,3,30,5)};})();\n"
    "S.goal=clampN(lsGet('gbb_goal'),10,240,60);S.tstyle=lsGet('gbb_tstyle')||'ring';S.pomoCustom=false;S.goalCustom=false;S.myPh=null;S.phKey=null;\n"
    "S.songMood='';S.songFilter='';S.songRoll=null;")
# 크게 보기
sub("  if(t==='pin')return S.pin?modalPin(V):'';", "  if(t==='pin')return S.pin?modalPin(V):'';\n  if(t==='focus'){if(!V.me||!liveOf(V,V.me)){S.modal=null;lock(false);return '';}return modalFocus(V);}")
sub("  layer.className='layer'+(S.closing?' closing':'');", "  layer.className='layer'+(S.closing?' closing':'')+(S.modal&&S.modal.type==='focus'&&!S.check&&!S.missed?' fullv':'');")
sub("  if(S.modal.type==='pin')S.autoReward=null;", "  if(S.modal.type==='pin')S.autoReward=null;\n  if(S.modal.type==='focus')lock(false);")
sub("  if(document.visibilityState!=='visible')return;\n  tick();", "  if(document.visibilityState!=='visible')return;\n  if(S.modal&&S.modal.type==='focus')lock(true);\n  tick();")
