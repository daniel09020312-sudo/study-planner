/* ---------- 과목별 진도: 각자 단원을 정하고 단원마다 진도 표시 ---------- */
// progress/<나>.units = {과목id: [{id, n}]}, 체크는 checks['과목__단원__항목']
// 단원을 아직 안 정한 과목은 예전처럼 과목 전체에 체크(checks['과목__항목'])
var UNIT_MAX=20;
function unitsOf(V,mid,sid){return arr(obj(obj(V.progress[mid]).units)[sid]).filter(function(u){return u&&u.id&&u.n;});}
function shortItem(l){l=String(l||'');var w=l.split(/\s+/)[0].replace(/(와|과)$/,'');return w.length>5?w.slice(0,5):w;}
function unitStat(V,mid,s){
  var ck=obj(obj(V.progress[mid]).checks),us=unitsOf(V,mid,s.id),n=s.items.length,d=0,t;
  if(!n)return {d:0,t:0,pct:0,us:us};
  if(!us.length){d=s.items.filter(function(it){return ck[s.id+'__'+it.id];}).length;t=n;}
  else{t=us.length*n;us.forEach(function(u){s.items.forEach(function(it){if(ck[s.id+'__'+u.id+'__'+it.id])d++;});});}
  return {d:d,t:t,pct:t?Math.round(d/t*100):0,us:us};
}
function unitRow(V,s,u,ck,edit,i,len){
  var key=u?s.id+'__'+u.id+'__':s.id+'__',dn=s.items.filter(function(it){return ck[key+it.id];}).length;
  var h='<div class="urow'+(dn===s.items.length&&dn?' full':'')+'" id="ur-'+esc(s.id+'-'+(u?u.id:'all'))+'"><div class="un"><b>'+esc(u?u.n:'과목 전체')+'</b><small>'+dn+' / '+s.items.length+'</small></div><div class="uchks">';
  s.items.forEach(function(it){var on=!!ck[key+it.id];h+='<button class="uck'+(on?' on':'')+'" data-act="'+(u?'ucheck':'check')+'" data-id="'+esc(s.id)+'"'+(u?' data-u="'+esc(u.id)+'"':'')+' data-item="'+esc(it.id)+'" aria-pressed="'+(on?'true':'false')+'" aria-label="'+esc((u?u.n+' ':'')+it.label)+' 완료 표시" title="'+esc(it.label)+'">'+esc(shortItem(it.label))+'</button>';});
  h+='</div>';
  if(edit&&u)h+='<div class="uedit"><button class="btn small" data-act="unit-mv" data-id="'+esc(s.id)+'" data-u="'+esc(u.id)+'" data-d="-1"'+(i===0?' disabled':'')+' aria-label="위로">위로</button><button class="btn small" data-act="unit-mv" data-id="'+esc(s.id)+'" data-u="'+esc(u.id)+'" data-d="1"'+(i===len-1?' disabled':'')+' aria-label="아래로">아래로</button><button class="del" data-act="unit-del" data-id="'+esc(s.id)+'" data-u="'+esc(u.id)+'">'+(S.confirm==='udel:'+u.id?'한 번 더 누르면 삭제':'삭제')+'</button></div>';
  return h+'</div>';
}
function viewProgMine(V){
  var p=obj(V.progress[V.me]),ck=obj(p.checks),skip=obj(p.skip),mine=V.subs.filter(function(s){return !skip[s.id];}),off=V.subs.filter(function(s){return skip[s.id];}),h='';
  if(!V.subs.length)return '<section class="card" style="--k:0"><p class="empty">아직 과목이 없습니다.</p>'+(canWrite()?'<div class="row" style="margin-top:10px"><button class="btn primary" data-act="seed">기본 과목 8개 넣기</button><button class="btn" data-act="prog-edit">직접 추가하기</button></div>':'')+'</section>';
  var tot=0,dn=0;mine.forEach(function(s){var u=unitStat(V,V.me,s);tot+=u.t;dn+=u.d;});
  h+='<section class="card usum" id="c-usum" style="--k:0"><div class="usumrow"><div><small>내 전체 진도</small><b>'+(tot?Math.round(dn/tot*100):0)+'%</b></div><p class="hint">과목 '+mine.length+'개, 단원 '+mine.reduce(function(a,s){return a+unitsOf(V,V.me,s.id).length;},0)+'개, 표시한 칸 '+dn+' / '+tot+'</p></div></section>';
  mine.forEach(function(s,k){
    var st=unitStat(V,V.me,s),us=st.us,edit=S.uEdit===s.id,col=subCol(V,s.id);
    h+='<section class="card usub" id="us-'+esc(s.id)+'" style="--k:'+Math.min(k+1,6)+';--sc:'+col+'"><div class="ct"><h2><i class="sdot"></i>'+esc(s.name)+'<small>'+(us.length?'단원 '+us.length+'개':'단원 없음')+'</small></h2><b class="upct">'+st.pct+'%</b></div><div class="ubar" aria-hidden="true"><i style="width:'+st.pct+'%"></i></div>';
    if(us.length)us.forEach(function(u,i){h+=unitRow(V,s,u,ck,edit,i,us.length);});
    else h+=unitRow(V,s,null,ck,false,0,1)+'<p class="hint" style="margin-top:6px">아래에 단원을 적으면 단원마다 따로 표시할 수 있습니다.</p>';
    h+='<div class="uadd"><input type="text" data-draft="unit:'+esc(s.id)+'" data-enter="unit-add" data-id="'+esc(s.id)+'" maxlength="80" placeholder="예: 1. 지수와 로그, 2. 삼각함수" aria-label="'+esc(s.name)+' 단원 추가"><button class="btn small" data-act="unit-add" data-id="'+esc(s.id)+'">단원 추가</button></div>';
    h+='<div class="row ufoot">'+(us.length?'<button class="btn small" data-act="unit-edit" data-id="'+esc(s.id)+'" aria-pressed="'+(edit?'true':'false')+'">'+(edit?'고치기 끝':'단원 순서, 삭제')+'</button>':'')+'<button class="btn small" data-act="skip" data-id="'+esc(s.id)+'">안 듣는 과목이면 빼기</button></div></section>';
  });
  if(off.length)h+='<section class="card" id="c-uoff" style="--k:6"><div class="ct"><h2>뺀 과목</h2></div><div class="chips">'+off.map(function(s){return '<button class="chip" data-act="skip" data-id="'+esc(s.id)+'">'+esc(s.name)+' 다시 넣기</button>';}).join('')+'</div></section>';
  return h;
}
function viewProgAll(V){
  var R=V.roster,n=R.length||1;
  var h='<section class="card tbl" id="c-tbl" style="--k:0;--n:'+n+(n>6?';--cw:46px':'')+'"><div class="orow ohead"><span class="olabel">과목</span>';
  R.forEach(function(m){h+='<span class="ocell'+(m.id===V.me?' me':'')+'">'+esc(shortName(V.byId[m.id].name))+'</span>';});
  h+='</div>';
  V.subs.forEach(function(s){
    var open=!!S.open[s.id];
    h+='<button class="orow osum" id="os-'+esc(s.id)+'" data-act="prog-toggle" data-id="'+esc(s.id)+'" aria-expanded="'+(open?'true':'false')+'"><span class="olabel"><b>'+esc(s.name)+'</b><span class="chev">'+(open?'접기':'단원 보기')+'</span></span>';
    R.forEach(function(m){
      var skip=obj(obj(V.progress[m.id]).skip)[s.id],u=unitStat(V,m.id,s);
      h+='<span class="ocell'+(m.id===V.me?' me':'')+'">'+(skip?'<span class="skip">제외</span>':'<span class="frac">'+u.pct+'%</span><span class="obar" aria-hidden="true"><i style="width:'+u.pct+'%"></i></span>')+'</span>';
    });
    h+='</button>';
    if(!open)return;
    h+='<div class="ounits" id="ou-'+esc(s.id)+'">';
    R.forEach(function(m){
      var skip=obj(obj(V.progress[m.id]).skip)[s.id];if(skip)return;
      var ck=obj(obj(V.progress[m.id]).checks),us=unitsOf(V,m.id,s.id);
      h+='<div class="oup"><b>'+esc(V.byId[m.id].name)+'</b><span>'+(us.length?us.map(function(u){var d=s.items.filter(function(it){return ck[s.id+'__'+u.id+'__'+it.id];}).length;return '<em class="ut'+(d===s.items.length&&d?' full':'')+'">'+esc(cut(u.n,14))+' '+d+'/'+s.items.length+'</em>';}).join(''):'<em class="ut">단원을 정하지 않음</em>')+'</span></div>';
    });
    h+='</div>';
  });
  return h+'</section>';
}
