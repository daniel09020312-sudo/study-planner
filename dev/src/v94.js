/* ---------- v94: (1) 노동요 방장 보기: 사람별로 들은 곡(progress.sp)·좋아요(progress.liked)와 곡마다 들은 사람·좋아요 누른 사람(S.songAdm)
   (2) 최종 결과는 END가 지나고 방장이 승인해야 공개(cfg.finalOk={at,by}). 공개되면 처음 열 때 한 번 3D 연출(finPlay, src/finrev3d.js, 이 기기 gbb_finrv=승인 시각). 결과 화면에서 다시 보기 ---------- */
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
function finRevTick(V){
  try{var f=finOk(V);if(!f||!V.me||S.modal||today()<=END)return;if(lsGet('gbb_finrv')===String(f.at))return;lsSet('gbb_finrv',String(f.at));finPlay(V);}catch(e){}
}
function finAdminCard(V){
  if(adminId(V)!==V.me||today()<=END||finOk(V))return '';
  var fs=finalStandings(V);
  return '<section class="card fin" id="c-fin-ok" style="--k:0"><div class="ct"><h2>최종 결과 공개 승인<small>방장만 보입니다</small></h2></div><p class="hint">승인하면 모두에게 공개 연출과 함께 순위가 공개됩니다. 승인 전에는 아무에게도 보이지 않습니다.</p><div class="row" style="margin:10px 0"><button class="btn primary" data-act="fin-ok">'+(S.confirm==='finok'?'한 번 더 누르면 공개합니다':'승인하고 공개하기')+'</button></div><details class="finpre"><summary>미리 보기 (방장만)</summary>'+fs.map(function(x,i){return '<div class="frr"><b>'+(i+1)+'등</b><span>'+esc(x.p.name)+'</span><em>'+fmtN(x.total)+'점</em></div>';}).join('')+'</details></section>';
}
