/* ---------- v94: (1) 노동요 방장 보기: 사람별로 들은 곡(progress.sp)·좋아요(progress.liked)와 곡마다 들은 사람·좋아요 누른 사람(S.songAdm)
   (2) 최종 결과는 END가 지나고 방장이 승인해야 공개(cfg.finalOk={at,by}). 공개되면 처음 열 때 한 번 큰 연출(창 'finrev', 이 기기 gbb_finrv=승인 시각):
   시작 -> 100점 넘긴 사람 명단 -> 4등부터 꼴찌까지(아래에서 위로) -> 3등 -> 2등 -> 1등 -> 전체 순위. 결과 화면에서 다시 보기 ---------- */
var FIN_CUT=100;
function finOk(V){var f=obj(obj((V||V0||{}).cfg).finalOk);return f.at?f:null;}
function finalOpen(){return today()>END&&!!finOk(V0);}
function songAdmHtml(V){
  if(adminId(V)!==V.me||!S.songAdm)return '';
  var h='<div class="sadm"><h3>사람별 노동요<small>방장만 보입니다</small></h3>';
  V.roster.forEach(function(m){
    var p=obj(V.progress[m.id]),sp=obj(p.sp),lk=obj(p.liked),pl=Object.keys(sp).filter(function(k){return V.songs[k]&&+sp[k]>0;}).sort(function(a,b){return sp[b]-sp[a];}),li=Object.keys(lk).filter(function(k){return lk[k]&&V.songs[k];});
    if(!pl.length&&!li.length)return;
    h+='<div class="sadmp"><b>'+esc(V.byId[m.id].name)+'</b>'+(pl.length?'<span>들음: '+pl.map(function(k){return esc(cut(obj(V.songs[k]).title,18))+' '+sp[k]+'번';}).join(', ')+'</span>':'')+(li.length?'<span>좋아요: '+li.map(function(k){return esc(cut(obj(V.songs[k]).title,18));}).join(', ')+'</span>':'')+'</div>';
  });
  return h+'</div>';
}
function songAdmRow(V,id){
  if(adminId(V)!==V.me||!S.songAdm)return '';
  var lk=[],pl=[];V.roster.forEach(function(m){var p=obj(V.progress[m.id]),n=+obj(p.sp)[id]||0,nm=V.byId[m.id].name;if(obj(p.liked)[id])lk.push(nm);if(n>0)pl.push(nm+' '+n+'번');});
  return '<p class="sadmr">'+(pl.length?'들은 사람: '+esc(pl.join(', ')):'들은 사람 없음')+' · '+(lk.length?'좋아요: '+esc(lk.join(', ')):'좋아요 없음')+'</p>';
}
/* 공개 연출 */
var FR_STEPS=['intro','cut','rest','p3','p2','p1','all'];
function finConfetti(n,cls){var h='<div class="frconf '+(cls||'')+'" aria-hidden="true">';for(var i=0;i<n;i++){h+='<i style="--x:'+((i*37)%100)+';--d:'+((i*53)%23/10)+'s;--r:'+((i*71)%360)+'deg;--c:'+(i%5)+'"></i>';}return h+'</div>';}
function modalFinRev(V){
  var fs=finalStandings(V).filter(function(x){return x.total>0;}),st=S.fr||{s:0},step=FR_STEPS[st.s]||'all',h='';
  var top=fs.slice(0,3),rest=fs.slice(3),cutL=fs.filter(function(x){return x.total>=FIN_CUT;});
  h+='<div class="frv s-'+step+'" id="dlg-finrev" role="dialog" aria-modal="true" aria-label="최종 결과 발표" tabindex="-1"><div class="frbg" aria-hidden="true"></div>';
  if(step==='intro')h+='<div class="frin"><small>'+esc(shortDate(TALLY)+' ~ '+shortDate(END))+'</small><h2>최종 결과 발표</h2><p>'+fs.length+'명의 기록을 모두 더했습니다</p><div class="frcount"><b>3</b><b>2</b><b>1</b></div></div>';
  else if(step==='cut')h+='<div class="frsec"><h2>'+FIN_CUT+'점 넘긴 사람<small>'+cutL.length+'명</small></h2><div class="frcut">'+(cutL.length?cutL.slice().sort(function(a,b){return a.p.name.localeCompare(b.p.name);}).map(function(x,i){return '<span style="--i:'+i+'">'+esc(x.p.name)+'</span>';}).join(''):'<p class="hint">'+FIN_CUT+'점을 넘긴 사람이 없습니다</p>')+'</div><p class="frnote">순서는 이름순입니다. 등수는 곧 공개됩니다</p></div>';
  else if(step==='rest')h+='<div class="frsec"><h2>'+(rest.length?'4등부터':'등수 공개')+'</h2><div class="frrest">'+(rest.length?rest.map(function(x,i){return {x:x,i:i};}).reverse().map(function(o,j){return '<div class="frr'+(o.x.p.id===V.me?' me':'')+'" style="--i:'+j+'"><b>'+(o.i+4)+'등</b><span>'+esc(o.x.p.name)+'</span><em>'+fmtN(o.x.total)+'점</em></div>';}).join(''):'<p class="hint">이제 1, 2, 3등만 남았습니다</p>')+'</div></div>';
  else if(step==='p3'||step==='p2'||step==='p1'){
    var k=+step.slice(1),x=top[k-1],pz=prizeOf(V,k);
    h+='<div class="frpod k'+k+'"><div class="frdrum"><small>두구두구</small><b>'+k+'등은</b></div>'+(x?'<div class="frcard"><span class="frmed">'+k+'</span><b class="frname">'+esc(x.p.name)+'</b><em>'+fmtN(x.total)+'점</em>'+(pz.t?'<small class="frprize">상품: '+esc(pz.t)+'</small>':'')+'</div>':'<div class="frcard"><b class="frname">없음</b></div>')+(k===1?finConfetti(70,'big')+'<div class="frrays" aria-hidden="true"></div>':finConfetti(k===2?30:20,''))+'</div>';
  }else{
    h+='<div class="frsec frall"><h2>최종 순위</h2><div class="frpodium">'+[1,0,2].map(function(i){var x=top[i];return x?'<div class="frp p'+(i+1)+'"><b>'+esc(x.p.name)+'</b><small>'+fmtN(x.total)+'점</small><span>'+(i+1)+'</span></div>':'';}).join('')+'</div><div class="frlist">'+fs.map(function(x,i){return '<div class="frr'+(x.p.id===V.me?' me':'')+(x.total>=FIN_CUT?' cut':'')+'"><b>'+(i+1)+'등</b><span>'+esc(x.p.name)+'</span><em>'+fmtN(x.total)+'점</em></div>';}).join('')+'</div></div>';
  }
  var last=st.s>=FR_STEPS.length-1;
  h+='<div class="frnav">'+(last?'<button class="btn xl primary" data-act="fr-close">닫기</button>':'<button class="btn xl primary" data-act="fr-next">'+(step==='intro'?'시작':step==='p1'?'전체 순위 보기':'다음')+'</button><button class="linkbtn frskip" data-act="fr-skip">건너뛰기</button>')+'</div></div>';
  return h;
}
function finRevTick(V){
  try{var f=finOk(V);if(!f||!V.me||S.modal||today()<=END)return;if(lsGet('gbb_finrv')===String(f.at))return;lsSet('gbb_finrv',String(f.at));S.fr={s:0};openModal('finrev');}catch(e){}
}
function finAdminCard(V){
  if(adminId(V)!==V.me||today()<=END||finOk(V))return '';
  var fs=finalStandings(V);
  return '<section class="card fin" id="c-fin-ok" style="--k:0"><div class="ct"><h2>최종 결과 공개 승인<small>방장만 보입니다</small></h2></div><p class="hint">승인하면 모두에게 공개 연출과 함께 순위가 공개됩니다. 승인 전에는 아무에게도 보이지 않습니다.</p><div class="row" style="margin:10px 0"><button class="btn primary" data-act="fin-ok">'+(S.confirm==='finok'?'한 번 더 누르면 공개합니다':'승인하고 공개하기')+'</button></div><details class="finpre"><summary>미리 보기 (방장만)</summary>'+fs.map(function(x,i){return '<div class="frr"><b>'+(i+1)+'등</b><span>'+esc(x.p.name)+'</span><em>'+fmtN(x.total)+'점</em></div>';}).join('')+'</details></section>';
}
