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
/* 모두 보기: 과목마다 한 줄. 반 평균 막대 위에 내 위치, 사람 분포. 누르면 사람별 막대와 단원 */
var PSORTS=[['order','과목 순'],['mine','내 진도 낮은 순'],['avg','반 평균 낮은 순']];
function progRows(V){
  return V.subs.map(function(s){
    var per=[],skipN=0;
    V.roster.forEach(function(m){
      if(obj(obj(V.progress[m.id]).skip)[s.id]){skipN++;return;}
      var u=unitStat(V,m.id,s),us=u.us,full=0,ck=obj(obj(V.progress[m.id]).checks);
      us.forEach(function(x){if(s.items.length&&s.items.every(function(it){return ck[s.id+'__'+x.id+'__'+it.id];}))full++;});
      per.push({m:m,pct:u.pct,us:us.length,full:full});
    });
    var avg=per.length?Math.round(per.reduce(function(a,x){return a+x.pct;},0)/per.length):0,mine=per.filter(function(x){return x.m.id===V.me;})[0];
    return {s:s,per:per,avg:avg,mine:mine,skipN:skipN};
  });
}
function viewProgAll(V){
  var so=PSORTS.some(function(x){return x[0]===S.progSort;})?S.progSort:'order',rows=progRows(V);
  if(so==='mine')rows.sort(function(a,b){return (a.mine?a.mine.pct:101)-(b.mine?b.mine.pct:101);});
  else if(so==='avg')rows.sort(function(a,b){return a.avg-b.avg;});
  var h='<section class="card pall" id="c-pall" style="--k:0"><div class="ct"><h2>모두의 진도<small>과목 '+rows.length+'개, '+V.roster.length+'명</small></h2></div>';
  h+='<div class="seg mini psort" style="grid-template-columns:repeat(3,minmax(0,1fr))" role="group" aria-label="정렬">'+PSORTS.map(function(x){return '<button data-act="prog-sort" data-id="'+x[0]+'" aria-pressed="'+(so===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  if(!rows.length)h+='<p class="empty">아직 과목이 없습니다.</p>';
  h+='<div class="prows">';
  rows.forEach(function(r){
    var s=r.s,open=!!S.open[s.id],col=subCol(V,s.id),bins=[0,0,0,0,0];
    r.per.forEach(function(x){bins[Math.min(4,Math.floor(x.pct/20))]++;});
    var bm=Math.max.apply(null,bins.concat([1]));
    h+='<div class="prow'+(open?' open':'')+'" id="pr-'+esc(s.id)+'" style="--sc:'+col+'"><button class="phead" data-act="prog-toggle" data-id="'+esc(s.id)+'" aria-expanded="'+(open?'true':'false')+'">';
    h+='<span class="pnm"><i class="sdot"></i><b>'+esc(s.name)+'</b><small>'+r.per.length+'명'+(r.skipN?', 제외 '+r.skipN+'명':'')+'</small></span>';
    h+='<span class="pmid"><span class="pbar" aria-hidden="true"><i style="width:'+r.avg+'%"></i>'+(r.mine?'<u style="left:'+r.mine.pct+'%"></u>':'')+'</span><span class="pnums"><em>반 평균 <b>'+r.avg+'%</b></em>'+(r.mine?'<em class="me">나 <b>'+r.mine.pct+'%</b></em>':'<em class="me">나 제외</em>')+'</span></span>';
    h+='<span class="pdist" aria-label="진도 분포">'+bins.map(function(n,i){return '<i style="--h:'+Math.round(n/bm*100)+'%" title="'+(i*20)+'~'+(i*20+19)+'%: '+n+'명"></i>';}).join('')+'</span><i class="pchev" aria-hidden="true"></i></button>';
    if(open){
      h+='<div class="pppl" id="pp-'+esc(s.id)+'">';
      r.per.slice().sort(function(a,b){return b.pct-a.pct;}).forEach(function(x,i){
        var me=x.m.id===V.me;
        h+='<div class="pp'+(me?' me':'')+'"><span class="ppr">'+(i+1)+'</span><span class="ppn">'+esc(V.byId[x.m.id].name)+'</span><span class="pbar sm" aria-hidden="true"><i style="width:'+x.pct+'%"></i></span><b>'+x.pct+'%</b><small>'+(x.us?'단원 '+x.full+'/'+x.us:'단원 없음')+'</small></div>';
      });
      h+='</div>';
    }
    h+='</div>';
  });
  return h+'</div></section>';
}
