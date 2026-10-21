/* ---------- 일정: 학교 행사·시험과 수행평가 따로 보기 ---------- */
var EV_EXAM_KINDS=['시험','행사'];
function evGroupOf(e){
  if(e.kind)return EV_EXAM_KINDS.indexOf(String(e.kind))>=0?'exam':'task';
  return /시험|모의고사|모평|학평|학력평가|수능|행사|축제|대회|방학|개학|휴업|컨퍼런스/.test(String(e.title||''))?'exam':'task';
}
function evSubCol(V,x){
  if(x.sid&&V.subName[x.sid])return subCol(V,x.sid);
  var hit=V.subs.filter(function(s){return String(x.title||'').indexOf(s.name)===0;})[0];
  return hit?subCol(V,hit.id):SGRAY;
}
function evItems(V,grp,past){
  var t=today(),out=[];
  if(grp==='exam')Object.keys(EVENTS).forEach(function(d){out.push({d:d,title:EVENTS[d].l,school:1,exam:!!EVENTS[d].exam,off:!!EVENTS[d].off});});
  Object.keys(V.evByDate).forEach(function(d){V.evByDate[d].forEach(function(e){if(e.grp===grp)out.push({d:d,title:e.title,id:e.id,mid:e.mid,shared:e.shared,kind:e.kind,sid:e.sid});});});
  out=out.filter(function(x){return past?x.d<t:x.d>=t;});
  out.sort(function(a,b){return a.d<b.d?-1:a.d>b.d?1:0;});
  return past?out.reverse():out;
}
function evRow(V,x){
  var own=x.mid===V.me,who=x.mid&&!own&&V.byId[x.mid]?V.byId[x.mid].name:'',n=diffDays(today(),x.d);
  var col=x.school?(x.exam?'var(--accent)':x.off?'var(--red)':SGRAY):(x.kind==='시험'&&!x.sid?'var(--accent)':evSubCol(V,x));
  var tags=(x.school?'<em class="tag">학교</em>':'')+(x.exam?'<em class="tag a">시험</em>':'')+(x.off?'<em class="tag">쉬는 날</em>':'')+(!x.school&&x.kind&&x.kind!=='기타'&&String(x.title).indexOf(x.kind)<0?'<em class="tag">'+esc(x.kind)+'</em>':'')+(!x.school?(x.shared?'<em class="tag">'+(who?esc(who)+' 님이 공유':'모두에게 공유')+'</em>':'<em class="tag">나만 보기</em>'):'');
  var h='<div class="evr'+(n>=0&&n<=3?' soon':'')+'" id="evr-'+esc(x.id||('s'+x.d))+'" style="--sc:'+col+'"><button class="evd" data-act="al-open" data-d="'+x.d+'" aria-label="'+esc(longDate(x.d))+' 달력에서 보기"><b>'+dlabel(x.d)+'</b><small>'+esc(shortDate(x.d))+' '+DOW[pd(x.d).getDay()]+'</small></button><div class="evt"><span>'+esc(x.title)+'</span><div class="evtags">'+tags+'</div></div>';
  if(own&&x.id)h+='<button class="del" data-act="ev-del" data-id="'+esc(x.id)+'">'+(S.confirm==='ev:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button>';
  return h+'</div>';
}
function viewEvents(V){
  var t=today(),dd=diffDays(t,EXAM[0]),past=!!S.evPast;
  var h='<div class="view" id="view-cal"><header class="vhead"><div><h1>일정</h1><p>학교 행사와 시험, 수행평가를 나눠서 봅니다.</p></div><div class="vacts">'+calModeSeg();
  if(dd>0)h+='<span class="pill">2차 시험<b>D-'+dd+'</b></span>';
  h+='</div></header><div class="vbody'+(S.vbDir?' side':'')+'" id="vb-ev-'+(past?'p':'n')+'" style="--vd:'+S.vbDir+'"><div class="cols evcols">';
  [['task','수행평가','수행평가'],['exam','학교 행사와 시험','시험']].forEach(function(g,k){
    var list=evItems(V,g[0],past);
    h+='<section class="card evcard '+g[0]+'" id="c-ev-'+g[0]+'" style="--k:'+k+'"><div class="ct"><h2>'+g[1]+'<small>'+(past?'지난 일정 ':'남은 일정 ')+list.length+'개</small></h2><button class="btn small'+(g[0]==='task'?' primary':' soft')+'" data-act="ev-new" data-k="'+g[2]+'">추가</button></div>';
    if(!list.length)h+='<p class="empty">'+(past?'지난 일정이 없습니다.':g[0]==='task'?'남은 수행평가가 없습니다. 추가를 눌러 날짜와 과목을 적어 두세요.':'남은 행사나 시험이 없습니다.')+'</p>';
    list.forEach(function(x){h+=evRow(V,x);});
    h+='</section>';
  });
  h+='</div><div class="row evmore"><button class="btn small" data-act="ev-past" aria-pressed="'+(past?'true':'false')+'">'+(past?'남은 일정 보기':'지난 일정 보기')+'</button></div></div></div>';
  return h;
}
