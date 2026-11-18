/* ---------- v98: 숨은 칭호 '잠들지 않는 자' (하루 18시간 넘게 공부한 날이 있으면). 받기 전에는 배지 목록에 안 보임 ---------- */
var H18_MIN=1080;
function h18Day(V,mid){
  var t=today(),last=t<END?t:END,res='';
  for(var d=TALLY;d<=last;d=addDays(d,1)){var x=dayOf(V,mid,d);if(sumMins(x.mins)+sumMins(x.manual)>=H18_MIN){res=d;break;}}
  return res;
}
function h18Tick(V){
  if(!V||!V.me||!S.ready||S.modal||S.check||S.missed||!canWrite()||!netFresh())return;
  var b=badgeList(V,V.me).filter(function(x){return x.id==='d18'&&x.on;})[0];if(!b)return;
  var d=h18Day(V,V.me)||'1';if(lsGet('gbb_h18')===d)return;
  S.modal={type:'h18',id:d};S.closing=false;render();
}
function h18Close(use){
  var m=S.modal;if(m&&m.type==='h18'){lsSet('gbb_h18',m.id);if(use){try{editProg(function(p){p.title='d18';});}catch(x){}}}
  closeModal();
}
function modalH18(V){
  var st='';for(var i=0;i<24;i++)st+='<i style="--x:'+((i*37)%100)+'%;--y:'+((i*61)%70)+'%;--d:'+((i*13)%30)/10+'s"></i>';
  var ring='';for(var j=0;j<24;j++)ring+='<b class="'+(j<18?'on':'')+'" style="--j:'+j+'"></b>';
  return '<div class="scrim" data-act="h18-x"></div><div class="dialog h18" id="dlg-h18" role="dialog" aria-modal="true" aria-label="숨은 칭호" tabindex="-1"><div class="h18sky" aria-hidden="true">'+st+'</div>'+
    '<div class="h18h">숨은 칭호</div><div class="h18clock" aria-hidden="true">'+ring+'<span>18<small>시간</small></span></div>'+
    '<h2 class="h18t">잠들지 않는 자</h2><p class="h18p">하루에 18시간 넘게 공부했습니다.<br>목록에 없던 칭호가 열렸습니다.</p>'+
    '<div class="h18b"><button class="btn primary" data-act="h18-use">칭호 달기</button><button class="btn" data-act="h18-x">닫기</button></div></div>';
}
/* 화면을 그린 뒤 도는 eggTick에 붙여 확인 */
eggTick=(function(f){return function(V){f(V);try{h18Tick(V);}catch(e){}};})(eggTick);
