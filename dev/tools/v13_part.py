# ---------------------------------------------------------------- 날짜별 할 일 (주간 달력)
# 달력 화면 위쪽에서 '달력 / 할 일 / 시간표'를 바꿔 본다. 할 일은 한 주를 달력처럼 7칸으로 놓고 날짜 밑에 적어 둔 모양.

# 상태
sub("S.gDoneLast=lsGet('gbb_donelast')==='1';S.undo=null;",
    "S.gDoneLast=lsGet('gbb_donelast')==='1';S.undo=null;\n"
    "S.calMode=(function(m){return m==='list'||m==='tt'?m:'cal';})(lsGet('gbb_calmode'));S.alWeek=null;S.alLeft=lsGet('gbb_alleft')==='1';S.scrollTo=S.calMode==='list'?{id:'wc-'+today(),inline:'start',quiet:1}:null;S.vbDir=0;")

# 달력 머리에 보기 방식 전환, 달력 본문에도 전환 연출
sub("  h+='</div><div class=\"vacts\">';\n  if(ph&&wk<=8)h+='<span class=\"pill\">'+wk+'주차<b>'+esc(ph.name)+'</b></span>';",
    "  h+='</div><div class=\"vacts\">'+calModeSeg();\n  if(ph&&wk<=8)h+='<span class=\"pill\">'+wk+'주차<b>'+esc(ph.name)+'</b></span>';")
sub("  h+='</div></header><div class=\"calwrap\"><section class=\"card calcard\"",
    "  h+='</div></header><div class=\"calwrap vbody'+(S.vbDir?' side':'')+'\" id=\"vb-cal-'+ym+'\" style=\"--vd:'+S.vbDir+'\"><section class=\"card calcard\"")
sub("function viewCal(V){\n",
    "function viewCal(V){\n  if(S.calMode==='list')return viewAgenda(V);\n  if(S.calMode==='tt')return viewTT(V);\n")

# 주간 달력
sub("/* ---------- 공부방 ---------- */", r"""var CMODES=[['cal','달력'],['list','할 일'],['tt','시간표']];
function calModeSeg(){
  var i=0;CMODES.forEach(function(x,j){if(x[0]===S.calMode)i=j;});
  return '<div class="seg mini cmode" style="--i:'+i+';--n:'+CMODES.length+'" role="group" aria-label="보기 방식">'+CMODES.map(function(x){return '<button data-act="cal-mode" data-id="'+x[0]+'" aria-pressed="'+(S.calMode===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
}
function setCalMode(m){
  var a=-1,b=-1;CMODES.forEach(function(x,j){if(x[0]===S.calMode)a=j;if(x[0]===m)b=j;});if(b<0||a===b)return;
  S.vbDir=b>a?1:-1;S.calMode=m;lsSet('gbb_calmode',m==='cal'?null:m);
  if(m==='list'){S.alWeek=wkStart(S.date||today());if(S.alWeek===wkStart(today()))S.scrollTo={id:'wc-'+today(),inline:'start',quiet:1};}
  if(m==='tt')ttEnter();
}
function wkStart(d){return addDays(d,-((pd(d).getDay()+6)%7));}
var AL_MIN=wkStart(MONTHS[0]+'-01'),AL_MAX=(function(){var m=MONTHS[MONTHS.length-1];return wkStart(m+'-'+String(new Date(+m.slice(0,4),+m.slice(5),0).getDate()).padStart(2,'0'));})();
function alClamp(d){return d<AL_MIN?AL_MIN:d>AL_MAX?AL_MAX:d;}
function wkTitle(ws,n){n=n||7;var a=pd(ws),b=pd(addDays(ws,n-1));return (a.getMonth()+1)+'월 '+a.getDate()+'일 ~ '+(a.getMonth()===b.getMonth()?'':(b.getMonth()+1)+'월 ')+b.getDate()+'일';}
function wkItem(V,d,mode,x,t){
  var sub=x.sid&&V.subName[x.sid],late=!x.done&&d<t,p=x.pid&&V.plans[x.pid]?obj(V.plans[x.pid]):null,meta=[];
  if(sub)meta.push(esc(sub));
  if(x.ts!=null&&x.te>x.ts)meta.push(fmtHM(x.ts));
  if(p)meta.push(esc(shortDate(p.due))+' 마감'+(x.part?' '+esc(x.part):''));
  var h='<div class="wki'+(x.done?' done':'')+(late?' late':'')+'" id="wi-'+esc(x.id)+'" style="--sc:'+goalCol(V,x)+'">';
  h+='<button class="wkchk'+(x.done?' on':'')+'" data-act="goal-toggle" data-date="'+d+'" data-id="'+esc(x.id)+'" aria-pressed="'+(x.done?'true':'false')+'" aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'?' disabled':'')+'><span></span></button>';
  h+='<button class="wkt" data-act="al-goal" data-d="'+d+'" data-id="'+esc(x.id)+'" aria-label="'+esc(x.text)+', 달력에서 열어 고치기"><span class="t">'+esc(x.text)+'</span>'+(meta.length||late?'<small>'+meta.join(' · ')+(late?'<em>못 끝냄</em>':'')+'</small>':'')+'</button>';
  return h+'</div>';
}
function wkCell(V,d,t){
  var day=dayOf(V,V.me,d),g=day.goals,mode=modeOf(d),done=g.filter(isDone).length;
  var list=S.alLeft?g.filter(function(x){return !x.done;}):(S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g);
  var h='<div class="wkc'+(d===t?' today':'')+(d<t?' past':'')+'" id="wc-'+d+'">';
  if(g.length)h+='<div class="wkbar" role="img" aria-label="'+g.length+'개 중 '+done+'개 완료"><i style="width:'+Math.round(done*100/g.length)+'%"></i></div>';
  (dueMap(V)[d]||[]).forEach(function(p){h+='<p class="wkdue">마감 · '+esc(p.label)+'</p>';});
  list.forEach(function(x){h+=wkItem(V,d,mode,x,t);});
  if(g.length&&!list.length)h+='<p class="wke">모두 끝냄</p>';
  if(mode!=='view'&&g.length<GMAX)h+='<button class="wkadd" data-act="open" data-modal="compose" data-date="'+d+'" aria-label="'+esc(longDate(d))+'에 할 일 추가">+ 추가</button>';
  return h+'</div>';
}
function viewAgenda(V){
  var t=today(),cur=wkStart(t),ws=alClamp(S.alWeek||wkStart(S.date||t)),dd=diffDays(t,EXAM[0]),ph=phaseOf(ws),wk=weekNo(ws);
  S.alWeek=ws;
  var h='<div class="view" id="view-cal"><header class="vhead"><div class="mnav"><button class="ib" data-act="al-week" data-d="-1" aria-label="이전 주"'+(ws<=AL_MIN?' disabled':'')+'>&lsaquo;</button><h1 class="wkt">'+wkTitle(ws)+'</h1><button class="ib" data-act="al-week" data-d="1" aria-label="다음 주"'+(ws>=AL_MAX?' disabled':'')+'>&rsaquo;</button>';
  if(ws!==cur)h+='<button class="btn small" data-act="al-week" data-d="0" style="margin-left:6px">이번 주</button>';
  h+='</div><div class="vacts">'+calModeSeg();
  if(ph&&wk>=1)h+='<span class="pill">'+wk+'주차<b>'+esc(ph.name)+'</b></span>';
  if(dd>0)h+='<span class="pill">2차 시험<b>D-'+dd+'</b></span>';
  h+='</div></header>';
  var days=[],tot=0,dn=0,late=0;
  for(var i=0;i<7;i++){var d=addDays(ws,i),g=dayOf(V,V.me,d).goals,c=g.filter(isDone).length;days.push(d);tot+=g.length;dn+=c;if(d<t)late+=g.length-c;}
  h+='<div class="vbody'+(S.vbDir?' side':'')+'" id="vb-list-'+ws+'" style="--vd:'+S.vbDir+'"><section class="card wkcard" id="c-wk" style="--k:0"><div class="ct"><h2>할 일'+(tot?'<small>'+dn+'/'+tot+'</small>':'')+'</h2><div class="acts">'+(late?'<span class="wklate">지난 날 못 끝낸 일 '+late+'개</span>':'')+'<button class="chip" data-act="al-left" aria-pressed="'+(S.alLeft?'true':'false')+'">남은 일만</button></div></div>';
  h+='<div class="wkscroll" id="wkScroll"><div class="wk">';
  days.forEach(function(d){var dt=pd(d),off=dt.getDay()===0||(EVENTS[d]&&EVENTS[d].off),g=dayOf(V,V.me,d).goals,c=g.filter(isDone).length;
    h+='<button class="wkh'+(d===t?' today':'')+(off?' sun':'')+(d<t?' past':'')+'" data-act="al-open" data-d="'+d+'" aria-label="'+esc(longDate(d))+', 달력에서 열기"><small>'+DOW[dt.getDay()]+'</small><b>'+dt.getDate()+'</b>'+(g.length?'<em class="'+(c===g.length?'all':'')+'">'+c+'/'+g.length+'</em>':'<em></em>')+'</button>';});
  days.forEach(function(d){h+=wkCell(V,d,t);});
  h+='</div></div>';
  if(!tot)h+='<p class="hint wkhint">이 주에는 적은 할 일이 없습니다. 날짜 칸의 추가를 눌러 적어 보세요.</p>';
  return h+'</section></div></div>';
}

/* ---------- 공부방 ---------- */""")

# 동작
sub("    case 'cal-today':",
    r"""    case 'cal-mode':setCalMode(id==='list'||id==='tt'?id:'cal');break;
    case 'al-week':{var aw=+el.getAttribute('data-d')||0,ow=S.alWeek||wkStart(today());S.alWeek=alClamp(aw===0?wkStart(today()):addDays(ow,7*aw));S.vbDir=S.alWeek>ow?1:S.alWeek<ow?-1:0;if(S.alWeek===wkStart(today()))S.scrollTo={id:'wc-'+today(),inline:'start',quiet:1};break;}
    case 'al-left':S.alLeft=!S.alLeft;lsSet('gbb_alleft',S.alLeft?'1':null);break;
    case 'al-open':case 'al-goal':{
      var ad=el.getAttribute('data-d');S.vbDir=-1;S.calMode='cal';lsSet('gbb_calmode',null);S.date=ad;if(MONTHS.indexOf(ad.slice(0,7))>=0)S.month=ad.slice(0,7);
      if(name==='al-goal'){S.gSel=ad+'|'+id;S.gEdit=null;S.scrollTo={id:'g-'+id,block:'center'};}else S.scrollTo={id:'c-goals',block:'start'};
      break;
    }
    case 'cal-today':""")
sub("    case 'month':{var mi=MONTHS.indexOf(S.month)+(+el.getAttribute('data-d')||0);if(MONTHS[mi])S.month=MONTHS[mi];break;}",
    "    case 'month':{var md=+el.getAttribute('data-d')||0,mi=MONTHS.indexOf(S.month)+md;if(MONTHS[mi]){S.month=MONTHS[mi];S.vbDir=md>0?1:-1;}break;}")

# 그린 뒤 스크롤
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);",
    "  if(S.scrollTo&&(S.ready||!S.scrollTo.quiet)){var sa=S.scrollTo;S.scrollTo=null;setTimeout(function(){var se=document.getElementById(sa.id);if(!se||!se.scrollIntoView)return;"
    "if(sa.inline){var sc=se.closest('.wkscroll');if(sc&&sc.scrollWidth>sc.clientWidth+2)sc.scrollTo({left:se.offsetLeft-sc.firstElementChild.offsetLeft,behavior:sa.quiet||reduced?'auto':'smooth'});return;}"
    "se.scrollIntoView({block:sa.block||'start',behavior:reduced?'auto':'smooth'});},30);}\n"
    "  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);")

# 단축키 L: 달력 -> 할 일 -> 시간표
sub("      if(kc==='KeyD'){e.preventDefault();openModal('plan',null);return;}",
    "      if(kc==='KeyD'){e.preventDefault();openModal('plan',null);return;}\n"
    "      if(kc==='KeyL'){e.preventDefault();if(S.tab!=='cal'){goTab('cal');}else{var ci=0;CMODES.forEach(function(x,j){if(x[0]===S.calMode)ci=j;});setCalMode(CMODES[(ci+1)%CMODES.length][0]);}render();return;}")
sub("['D','마감 있는 할 일 추가'],", "['D','마감 있는 할 일 추가'],['L','달력, 할 일, 시간표 차례로 바꿔 보기'],")
