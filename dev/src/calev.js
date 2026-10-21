/* ---------- 달력 칸: 일정은 과목 줄임말 색 칩으로만, 자세한 내용은 날짜를 누르면 ---------- */
var SUB_ABBR={'생물의 유전':'유전','확률과 통계':'확통','화법과 언어':'화언','화법과 작문':'화작','언어와 매체':'언매','생명과학 실험':'생실','미적분Ⅰ':'미적','미적분Ⅱ':'미적2','미적분':'미적'};
function subShort(name){name=String(name||'').trim();if(SUB_ABBR[name])return SUB_ABBR[name];var w=name.split(/\s+/)[0].replace(/(의|과|와)$/,'');return w.length>2?w.slice(0,2):w;}
function subAbbr(V,sid){var c=String(obj(obj(V.progress[V.me]).abbr)[sid]||'').trim();return c||subShort(V.subName[sid]);}
function evSid(V,e){
  if(e.sid&&V.subName[e.sid])return e.sid;
  var t=String(e.title||''),best='',bl=0;
  V.subs.forEach(function(s){if(t.indexOf(s.name)===0&&s.name.length>bl){best=s.id;bl=s.name.length;}});
  return best;
}
function evRest(V,e,sid){var t=String(e.title||'');if(sid&&t.indexOf(V.subName[sid])===0)t=t.slice(V.subName[sid].length).trim();return t;}
function cellChips(V,mine){
  var chips=[],seen={};
  mine.forEach(function(e){
    var sid=evSid(V,e),k=sid||('t:'+e.title);
    if(seen[k]){seen[k].n++;return;}
    var c={sid:sid,grp:e.grp,n:1,t:sid?subAbbr(V,sid):(e.kind==='시험'||e.kind==='행사'||e.kind==='발표'||e.kind==='제출'||e.kind==='퀴즈')?e.kind:cut(String(e.title).replace(/\s+/g,''),3)};
    seen[k]=c;chips.push(c);
  });
  return chips;
}
function chipHtml(V,c){return '<i class="sev'+(c.grp==='exam'?' ex':'')+'" style="--sc:'+(c.sid?subCol(V,c.sid):c.grp==='exam'?'var(--accent)':SGRAY)+'">'+esc(c.t)+(c.n>1?'<b>'+c.n+'</b>':'')+'</i>';}
function monthLegend(V,ym){
  var cnt={},order=[];
  Object.keys(V.evByDate).forEach(function(d){if(d.slice(0,7)!==ym)return;V.evByDate[d].forEach(function(e){if(e.grp!=='task')return;var sid=evSid(V,e),k=sid||'_';if(!cnt[k]){cnt[k]=0;order.push(k);}cnt[k]++;});});
  if(!order.length)return '';
  order.sort(function(a,b){return cnt[b]-cnt[a];});
  return '<div class="calleg"><small>이번 달 수행평가</small>'+order.map(function(k){var nm=k==='_'?'기타':V.subName[k];return '<span class="lg" style="--sc:'+(k==='_'?SGRAY:subCol(V,k))+'">'+(k==='_'?'<i></i>':'<em class="sev">'+esc(subAbbr(V,k))+'</em>')+esc(nm)+' '+cnt[k]+'</span>';}).join('')+(V.me?'<button class="btn small lgbtn" data-act="abbr-open">줄임말 바꾸기</button>':'')+'</div>';
}
document.addEventListener('change',function(e){
  var t=e.target;if(!t||!t.classList||!t.classList.contains('abin-in'))return;
  var v=String(t.value||'').trim().slice(0,3),id=t.getAttribute('data-id');
  setTimeout(function(){var V=view();if(!V.subName[id])return;editProg(function(p){var a=obj(p.abbr);if(v&&v!==subShort(V.subName[id]))a[id]=v;else delete a[id];p.abbr=a;});render();},0);
});
