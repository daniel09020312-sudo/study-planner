# ---------------------------------------------------------------- 편의 기능 묶음
# 1) 되돌리기: 지우거나 옮긴 뒤 몇 초 동안 위쪽 알림에 '되돌리기'
sub("function flash(msg){S.flash=msg;clearTimeout(flashTimer);flashTimer=setTimeout(function(){S.flash='';paintBanner();},4500);paintBanner();}",
    r"""function flash(msg,undo){S.flash=msg;S.undo=undo||null;clearTimeout(flashTimer);flashTimer=setTimeout(function(){S.flash='';S.undo=null;paintBanner();},undo?8000:4500);paintBanner();}
function snap(paths){
  var V=view(),o={};
  paths.forEach(function(p){var i=p.indexOf('/'),c=p.slice(0,i),id=p.slice(i+1),src=c==='meta'?{config:V.cfg}:V[c],cur=src?src[id]:undefined;o[p]=cur==null?null:clone(cur);});
  return o;
}""")
sub("  if(S.flash)b+='<div class=\"flash\" role=\"status\">'+esc(S.flash)+'</div>';",
    "  if(S.flash)b+='<div class=\"flash\" role=\"status\"><span>'+esc(S.flash)+'</span>'+(S.undo?'<button data-act=\"undo\">되돌리기</button>':'')+'</div>';")

# 할 일 지우기, 옮기기, 다른 날에도 넣기
sub("    case 'goal-del':if(prev!=='gdel:'+id){S.confirm='gdel:'+id;break;}editDay(date,function(d){d.goals=d.goals.filter(function(g){return g.id!==id;});if(d.focus===id)d.focus=null;});S.gSel=null;break;",
    "    case 'goal-del':{if(prev!=='gdel:'+id){S.confirm='gdel:'+id;break;}var Vgd=view(),sgd=snap(['days/'+Vgd.me+'_'+date]);editDay(date,function(d){d.goals=d.goals.filter(function(g){return g.id!==id;});if(d.focus===id)d.focus=null;});S.gSel=null;if(canWrite())flash('할 일을 지웠습니다.',sgd);break;}")
cut("function moveGoal(from,id,to){", "function dayDoc(V,date){", r"""function moveGoal(from,id,to,quiet){
  var V=view(),t=today();if(!V.me||!need())return;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(to)||to<t){flash('오늘이나 그 뒤 날짜로만 옮길 수 있습니다.');return;}
  if(to===from)return;
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x.id===id;})[0];if(!g)return;
  if(dayOf(V,V.me,to).goals.length>=GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');return;}
  var sn=quiet?null:snap(['days/'+V.me+'_'+from,'days/'+V.me+'_'+to]);
  editDay(from,function(d){d.goals=d.goals.filter(function(x){return x.id!==id;});if(d.focus===id)d.focus=null;});
  editDay(to,function(d){var c=clone(g);c.done=false;d.goals.push(c);});
  S.gSel=null;if(!quiet)flash(shortDate(to)+' '+DOW[pd(to).getDay()]+'요일로 옮겼습니다.',sn);
}
function copyGoal(from,id,to){
  var V=view(),t=today();if(!V.me||!need())return;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(to)||to<t){flash('오늘이나 그 뒤 날짜에만 넣을 수 있습니다.');return;}
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x.id===id;})[0];if(!g)return;
  if(dayOf(V,V.me,to).goals.length>=GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');return;}
  var sn=snap(['days/'+V.me+'_'+to]);
  editDay(to,function(d){d.goals.push({id:rid('g'),text:g.text,sid:g.sid||'',done:false});});
  S.gSel=null;flash(shortDate(to)+' '+DOW[pd(to).getDay()]+'요일에도 넣었습니다.',sn);
}
function stripPlan(p){var o={};['mid','sid','type','unit','note','mode','total','per','due','start','dows','early','at'].forEach(function(k){if(p[k]!==undefined)o[k]=p[k];});return o;}
function planSnapPaths(V,p,due){
  var seen={},t=today(),out=['plans/'+p.id];
  p.parts.forEach(function(x){seen[x.date]=1;});
  for(var d=t;d<=due&&d<='2026-12-31';d=addDays(d,1))seen[d]=1;
  Object.keys(seen).forEach(function(d){out.push('days/'+V.me+'_'+d);});
  return out;
}
/* 남은 몫을 다시 배분 (마감을 바꿀 때도 사용) */
function redoPlan(p,due){
  var t=today();due=due||p.due;
  if(due!==p.due)queueWrite('plans/'+p.id,Object.assign(stripPlan(p),{due:due}));
  if(p.mode==='once'){var x=p.parts.filter(function(q){return !q.done;})[0];if(x&&x.date!==due&&due>=t)moveGoal(x.date,x.id,due,true);return 1;}
  var left=p.mode==='split'?(+p.total>0?Math.max(0,+p.total-p.amtDone):p.parts.filter(function(q){return !q.done;}).length):1;
  if(p.mode==='split'&&left<=0)return 0;
  dropPlanGoals({parts:p.parts.filter(function(q){return p.mode==='split'||q.date>=t;})},true);
  var st=p.parts.some(function(q){return q.done&&q.date===t;})?addDays(t,1):t;
  var spec=Object.assign({},p,{due:due,start:p.start>st?p.start:st,off:{},total:p.mode==='split'?left:p.total});
  if(p.mode==='split'&&!(+p.total>0))spec.total=0;
  var A=plAlloc(view(),spec);
  if(p.mode==='split'&&!(+p.total>0)){A.use=A.use.slice(0,left);A.use.forEach(function(r,i){r.part=(i+1)+'/'+A.use.length;});}
  if(A.use.length)putPlanGoals(p.id,p,A.use);
  return A.use.length;
}
""")
cut("    case 'pl-redo':{", "    case 'pl-today':{", r"""    case 'pl-redo':{
      var V8=view(),p8=planList(V8).filter(function(x){return x.id===id;})[0];if(!p8||!need())break;
      var sn8=snap(planSnapPaths(V8,p8,p8.due)),n8=redoPlan(p8);
      if(!n8){flash('남은 분량이 없거나 마감까지 넣을 날이 없습니다.');break;}
      flash('남은 것을 '+n8+'일에 다시 나눴습니다.',sn8);break;
    }
""")
sub("      dropPlanGoals(p7,true);queueWrite('plans/'+id,null);flash('마감 할 일과 남은 몫을 지웠습니다.');break;",
    "      var sn7=snap(planSnapPaths(V7,p7,p7.due));dropPlanGoals(p7,true);queueWrite('plans/'+id,null);flash('마감 할 일과 남은 몫을 지웠습니다.',sn7);break;")
sub("      save('msgs/'+id,null);\n      if(m3.pic)", "      var sn3=m3.pic?null:snap(['msgs/'+id]);save('msgs/'+id,null);if(sn3)flash('메시지를 지웠습니다.',sn3);\n      if(m3.pic)")
# 마감 바꾸기
sub("    h+='<div class=\"row\" style=\"margin-top:10px\">';\n    if(p.mode==='split'&&!p.finished&&p.due>=t)",
    "    h+='<div class=\"row\" style=\"margin-top:10px\">';\n    if(!p.finished)h+='<label class=\"gdate\"><span>마감 바꾸기</span><input type=\"date\" data-chg=\"pl-due-edit\" data-id=\"'+esc(p.id)+'\" min=\"'+t+'\" max=\"2026-12-31\" value=\"'+esc(p.due)+'\" aria-label=\"마감 날짜 바꾸기\"></label>';\n    if(p.mode==='split'&&!p.finished&&p.due>=t)")

# 2) 끝낸 일 아래로 모으기, 다른 날에도 넣기
sub("if(g.length>1)h+='<div class=\"seg mini\" style=\"grid-template-columns:repeat(3,minmax(0,1fr))\" role=\"group\" aria-label=\"할 일 묶어 보기\">'",
    "if(g.length>1)h+='<div class=\"gtools\"><div class=\"seg mini\" style=\"grid-template-columns:repeat(3,minmax(0,1fr))\" role=\"group\" aria-label=\"할 일 묶어 보기\">'")
sub("return '<button data-act=\"g-group\" data-id=\"'+x[0]+'\" aria-pressed=\"'+(S.gGroup===x[0]?'true':'false')+'\">'+x[1]+'</button>';}).join('')+'</div>';\n    h+='<ul>';",
    "return '<button data-act=\"g-group\" data-id=\"'+x[0]+'\" aria-pressed=\"'+(S.gGroup===x[0]?'true':'false')+'\">'+x[1]+'</button>';}).join('')+'</div><button class=\"chip\" data-act=\"g-donelast\" aria-pressed=\"'+(S.gDoneLast?'true':'false')+'\">끝낸 일 아래로</button></div>';\n    var gl=S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g;\n    h+='<ul>';")
sub("    if(S.gGroup==='none'||g.length<2)g.forEach(function(x){h+=goalRow(V,date,mode,day,x,isT);});",
    "    if(S.gGroup==='none'||g.length<2)gl.forEach(function(x){h+=goalRow(V,date,mode,day,x,isT);});")
sub("      g.forEach(function(x){var key;if(S.gGroup==='sub')", "      gl.forEach(function(x){var key;if(S.gGroup==='sub')")
sub("        a+='<label class=\"gdate\"><span>날짜 바꾸기</span>",
    "        a+='<label class=\"gdate\"><span>다른 날에도 넣기</span><input type=\"date\" data-chg=\"g-copy\" data-date=\"'+date+'\" data-id=\"'+esc(x.id)+'\" min=\"'+t+'\" max=\"2026-12-31\" value=\"\" aria-label=\"복사해 넣을 날짜\"></label>';\n        a+='<label class=\"gdate\"><span>날짜 바꾸기</span>")

# 3) 하루 공부 목표
sub("function carryList(V,date){", r"""function studyGoalBar(V,total){
  var gm=+obj(V.progress[V.me]).goalMins||0;if(!gm)return '';
  var pct=Math.min(100,Math.round(total/gm*100));
  return '<div class="sgoal"><div class="gbar" aria-hidden="true"><i style="width:'+pct+'%"></i></div><small>'+(total>=gm?'오늘 목표 '+fmtMins(gm)+'을 채웠습니다':'목표 '+fmtMins(gm)+'까지 '+fmtMins(gm-total)+' 남았습니다')+'</small></div>';
}
function carryList(V,date){""")
sub("<h2>공부 타이머<small>오늘 '+fmtMins(total)+'</small></h2>'+(L?'<button class=\"btn small soft\" data-act=\"focus-open\">크게 보기</button>':'')+'</div>';",
    "<h2>공부 타이머<small>오늘 '+fmtMins(total)+'</small></h2>'+(L?'<button class=\"btn small soft\" data-act=\"focus-open\">크게 보기</button>':'')+'</div>'+studyGoalBar(V,total);")
sub("위</span></div><div class=\"cert\">';", "위</span></div>'+studyGoalBar(V,sumMins(dayOf(V,V.me,t).mins)+sumMins(dayOf(V,V.me,t).manual))+'<div class=\"cert\">';")
sub("  if(V.me)b+='<div class=\"sec\"><h3>내 점수 초기화",
    "  if(V.me){var gmS=+obj(V.progress[V.me]).goalMins||0;b+='<div class=\"sec\"><h3>하루 공부 목표<small>나만 보입니다</small></h3><div class=\"amt\"><button data-act=\"sgoal\" data-d=\"-30\" aria-label=\"30분 줄이기\">-30</button><b>'+(gmS?fmtMins(gmS):'없음')+'</b><button data-act=\"sgoal\" data-d=\"30\" aria-label=\"30분 늘리기\">+30</button></div><p class=\"hint\">정하면 공부방 타이머와 오늘 점수 칸에 얼마나 채웠는지 보입니다.</p></div>';}\n  if(V.me)b+='<div class=\"sec\"><h3>내 점수 초기화")

# 4) 타이머를 끝낼 때 '지금 하는 중'이던 할 일을 끝냈는지 묻기
sub("  flagSession(V,L,Date.now());flushLive(L,Date.now());save('live/'+V.me,null);S.check=null;endFocus();\n}",
    "  flagSession(V,L,Date.now());flushLive(L,Date.now());save('live/'+V.me,null);S.check=null;endFocus();askFocusDone();\n}\nfunction askFocusDone(){var V=view(),d=dayOf(V,V.me,today()),g=d.focus&&d.goals.filter(function(x){return x.id===d.focus&&!x.done;})[0];if(g){S.modal={type:'askdone',id:g.id};S.closing=false;}}")
sub("endFocus();beep();flash('목표한 '+fmtMins(L.g)+'을 채웠습니다. 공부 시간에 기록했습니다.');render();",
    "endFocus();beep();flash('목표한 '+fmtMins(L.g)+'을 채웠습니다. 공부 시간에 기록했습니다.');askFocusDone();render();")
sub("  if(t==='compose')return modalCompose(V);",
    "  if(t==='askdone'){var dda=dayOf(V,V.me,today()),gga=dda.goals.filter(function(x){return x.id===S.modal.id;})[0];if(!gga||gga.done){S.modal=null;return '';}return dlg('',{id:'askdone',t:'하던 할 일을 끝냈나요?'},'<p class=\"askg\">'+(gga.sid&&V.subName[gga.sid]?'<em class=\"tag\">'+esc(V.subName[gga.sid])+'</em> ':'')+esc(gga.text)+'</p><div class=\"df\" style=\"margin-top:18px\"><button class=\"btn\" data-act=\"modal-close\">아직이에요</button><button class=\"btn primary\" data-act=\"askdone-yes\" data-id=\"'+esc(gga.id)+'\">끝냈어요</button></div>');}\n  if(t==='compose')return modalCompose(V);")

# 5) 쓰던 메시지, 글, 답변을 기기에 보관 (새로 고쳐도 남음)
sub("S.noteTs=+lsGet('gbb_note')||0;",
    "var DRAFT_KEEP=/^(msg:|rep:|postQ$|postA$)/,lastDraft='';\ntry{var drf=obj(JSON.parse(lsGet('gbb_drafts')||'{}'));for(var dk0 in drf)if(DRAFT_KEEP.test(dk0))S.draft[dk0]=String(drf[dk0]||'');lastDraft=JSON.stringify(drf);}catch(e){}\nS.gDoneLast=lsGet('gbb_donelast')==='1';S.undo=null;\nS.noteTs=+lsGet('gbb_note')||0;")
sub("  S.sync=false;", "  S.sync=false;\n  persistDrafts();")
sub("function afterChat(V){", "function persistDrafts(){var o={},k;for(k in S.draft){if(DRAFT_KEEP.test(k)&&S.draft[k])o[k]=String(S.draft[k]).slice(0,1500);}var j=JSON.stringify(o);if(j!==lastDraft){lastDraft=j;lsSet('gbb_drafts',j==='{}'?null:j);}}\nfunction afterChat(V){")
sub("  S.draft[k]=t.value;if(t.getAttribute('data-live'))render();", "  S.draft[k]=t.value;persistDrafts();if(t.getAttribute('data-live'))render();")

# 6) 키보드 단축키 (아이패드 키보드, 컴퓨터)
sub("  if(e.key!=='Enter'||e.isComposing||e.keyCode===229)return;\n  var t=e.target,a=t.getAttribute&&t.getAttribute('data-enter');",
    r"""  if(!e.ctrlKey&&!e.metaKey&&!e.altKey&&!e.isComposing&&!S.modal&&V0&&V0.me){
    var tg=e.target,typing=tg&&(/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName)||tg.isContentEditable),kc=e.code||'',dg=/^Digit([1-8])$/.exec(kc);
    if(!typing){
      if(dg){e.preventDefault();goTab(TABS[+dg[1]-1]);render();return;}
      if(kc==='KeyN'){e.preventDefault();var nd=modeOf(S.date)==='view'?today():S.date;openModal('compose',{getAttribute:function(n){return n==='data-date'?nd:null;}});return;}
      if(kc==='KeyD'){e.preventDefault();openModal('plan',null);return;}
      if(kc==='KeyT'){e.preventDefault();if(liveOf(V0,V0.me))stopTimer();else{if(S.tab!=='room')goTab('room');startTimer();}render();return;}
      if(kc==='KeyF'&&liveOf(V0,V0.me)){e.preventDefault();act('focus-open',{getAttribute:function(){return null;}});return;}
    }
  }
  if(e.key!=='Enter'||e.isComposing||e.keyCode===229)return;
  var t=e.target,a=t.getAttribute&&t.getAttribute('data-enter');""")
sub("  b+='</div><div class=\"sec\"><h3>저장 위치</h3>",
    "  b+='</div><div class=\"sec\"><h3>키보드 단축키<small>키보드를 연결했을 때</small></h3><ul class=\"kbd\">'+[['1 ~ 8','달력부터 메시지까지 화면 이동'],['N','할 일 추가'],['D','마감 있는 할 일 추가'],['T','타이머 켜기, 끄기'],['F','타이머 크게 보기'],['Esc','창 닫기']].map(function(x){return '<li><kbd>'+x[0]+'</kbd><span>'+x[1]+'</span></li>';}).join('')+'</ul></div><div class=\"sec\"><h3>저장 위치</h3>")

# 7) 글자 크기 (기기마다)
sub("applyLook();\ntry{window.matchMedia", "applyLook();\nfunction applyZoom(){var z=lsGet('gbb_zoom');document.documentElement.style.zoom=z==='s'?'0.9':z==='l'?'1.12':'';}\napplyZoom();\ntry{window.matchMedia")
sub("'+TSPREV[x[0]]+'</span>'+x[1]+'</button>';}).join('')+'</div></div>';",
    "'+TSPREV[x[0]]+'</span>'+x[1]+'</button>';}).join('')+'</div><h4 class=\"lb\">글자 크기</h4><div class=\"chips\">'+[['s','작게'],['m','보통'],['l','크게']].map(function(x){var zn=lsGet('gbb_zoom')||'m';return chipBtn('zoom','z',x[0],x[1],zn===x[0]);}).join('')+'</div></div>';")

# 동작
sub("    case 'timer-stop':stopTimer();break;", r"""    case 'timer-stop':stopTimer();break;
    case 'undo':{
      var u=S.undo;if(!u||!need())break;
      Object.keys(u).forEach(function(p){queueWrite(p,u[p]);});
      S.undo=null;S.gSel=null;flash('되돌렸습니다.');break;
    }
    case 'g-donelast':S.gDoneLast=!S.gDoneLast;lsSet('gbb_donelast',S.gDoneLast?'1':null);break;
    case 'sgoal':{var sgd2=+el.getAttribute('data-d')||0;editProg(function(p){p.goalMins=Math.max(0,Math.min(720,(+p.goalMins||0)+sgd2));});break;}
    case 'askdone-yes':editDay(today(),function(d){d.goals.forEach(function(x){if(x.id===id)x.done=true;});if(d.focus===id)d.focus=null;});closeModal();return;
    case 'zoom':{var zv=el.getAttribute('data-v');lsSet('gbb_zoom',zv==='m'?null:zv);applyZoom();break;}""")
sub("  else if(kind==='g-move'){",
    """  else if(kind==='g-copy'){if(/^\\d{4}-\\d{2}-\\d{2}$/.test(v))copyGoal(el.getAttribute('data-date'),id,v);}
  else if(kind==='pl-due-edit'){
    var Vq=view(),pq=planList(Vq).filter(function(x){return x.id===id;})[0];
    if(pq&&/^\\d{4}-\\d{2}-\\d{2}$/.test(v)&&v>=today()&&v!==pq.due&&need()){var snq=snap(planSnapPaths(Vq,pq,v>pq.due?v:pq.due));redoPlan(pq,v);flash('마감을 '+shortDate(v)+'로 바꾸고 남은 몫을 다시 나눴습니다.',snq);}
  }
  else if(kind==='g-move'){""")
