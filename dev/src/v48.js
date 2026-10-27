/* ---------- v48: 숨은 이스터에그: 7일 연속 매일 공부 시간이 7시간대(7시간 이상 8시간 미만) ---------- */
function eggRun(V){
  var g=gcSync(V);if(g.egg!==undefined)return g.egg;
  var t=today(),run=0,res='',rows=V.sc[V.me]||{};
  for(var d=START;d<t&&d<=END;d=addDays(d,1)){
    var m=rows[d]?+rows[d].mins||0:0;
    if(m>=420&&m<480){run++;if(run>=7){res=d;break;}}else run=0;
  }
  return g.egg=res;
}
function eggTick(V){
  if(!V||!V.me||!S.ready||S.modal||S.check||S.missed||!canWrite()||!netFresh())return;
  var e=eggRun(V);if(!e||lsGet('gbb_egg7')===e)return;
  S.modal={type:'egg7',id:e};S.closing=false;render();
}
function eggClose(){
  var m=S.modal;if(m&&m.type==='egg7'){var e=m.id;lsSet('gbb_egg7',e);try{editProg(function(p){p.egg7=e;});}catch(x){}}
  closeModal();
}
function modalEgg(V){
  var reel='';for(var i=0;i<3;i++)reel+='<div class="eggr" style="--i:'+i+'"><div class="eggs"><b>3</b><b>9</b><b>5</b><b>1</b><b>7</b></div></div>';
  return '<div class="scrim" data-act="egg-x"></div><div class="dialog egg" id="dlg-egg" role="dialog" aria-modal="true" aria-label="숨은 업적" tabindex="-1"><div class="eggbg" aria-hidden="true"></div>'+
    '<div class="eggh">숨은 업적</div><div class="eggreels" aria-label="7 7 7">'+reel+'</div>'+
    '<h2 class="eggt">럭키 세븐</h2><p class="eggp">일주일 내내, 매일 7시간대로 공부했습니다.<br>이런 꾸준함은 우연이 아닙니다.</p>'+
    '<div class="eggs7" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'+
    '<button class="btn primary" data-act="egg-x">고맙습니다</button></div>';
}
