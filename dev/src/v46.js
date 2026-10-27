/* ---------- v46: 1:1 대결 종류(점수, 공부 시간, 끝낸 할 일, 올 클리어, 인증한 날)와 기간(1·3·7일) ---------- */
var DUEL_KINDS=[
  {id:'score',name:'점수',unit:'점',desc:'기간 동안 얻은 점수의 합',f:function(r){return +r.total||0;}},
  {id:'time',name:'공부 시간',unit:'분',desc:'기간 동안 공부한 시간의 합',f:function(r){return +r.mins||0;}},
  {id:'goals',name:'끝낸 할 일',unit:'개',desc:'기간 동안 끝낸 할 일 개수',f:function(r){return +r.done||0;}},
  {id:'clear',name:'올 클리어',unit:'일',desc:'할 일 3개 이상을 모두 끝낸 날 수',f:function(r){return r.clear>0?1:0;}},
  {id:'cert',name:'인증한 날',unit:'일',desc:'공부 인증을 한 날 수',f:function(r){return r.certed?1:0;}}
],DUEL_LENS=[1,3,7];
function duelKindOf(d){var k=String(d&&d.kind||'score');for(var i=0;i<DUEL_KINDS.length;i++)if(DUEL_KINDS[i].id===k)return DUEL_KINDS[i];return DUEL_KINDS[0];}
function duelLen(d){var n=Math.round(+(d&&d.days));return DUEL_LENS.indexOf(n)>=0?n:DUEL_DAYS;}
function duelVal(d,r){return r?duelKindOf(d).f(r):0;}
function duelNum(d,n){var k=duelKindOf(d);return k.id==='time'?fmtMins(n):n+k.unit;}
function duelDesc(d){return duelKindOf(d).name+' · '+duelLen(d)+'일';}
function duelRecord(V,me){
  var w=0,l=0,e=0;
  duelList(V).forEach(function(d){if(d.state!=='done'||(d.a!==me&&d.b!==me))return;if(!d.win)e++;else if(d.win===me)w++;else l++;});
  return {w:w,l:l,e:e};
}

/* ---------- 찌르기 알림: 앱이 가려져 있어도 살아 있는 동안 화면 알림으로 알려 줌 (이 기기 설정 gbb_pokenote) ---------- */
function pnOn(){try{return typeof Notification!=='undefined'&&Notification.permission==='granted'&&lsGet('gbb_pokenote')==='1';}catch(e){return false;}}
function pnApply(){try{window.__SSE_HIDE_MS=pnOn()?15*60000:0;}catch(e){}}
function sysNotify(title,body,tag){
  if(!pnOn()||document.visibilityState!=='hidden')return;
  var o={body:body||'',tag:tag||'gbb',renotify:true,icon:'icon-192.png',badge:'icon-192.png',lang:'ko'};
  try{
    if(navigator.serviceWorker&&navigator.serviceWorker.getRegistration){
      navigator.serviceWorker.getRegistration().then(function(r){if(r&&r.showNotification)r.showNotification(title,o);else new Notification(title,o);}).catch(function(){try{new Notification(title,o);}catch(e){}});
    }else new Notification(title,o);
  }catch(e){}
}
function pokeSec(){
  var sup=typeof Notification!=='undefined',on=pnOn(),den=sup&&Notification.permission==='denied';
  return '<div class="sec"><h3>찌르기 알림<small>이 기기</small></h3><div class="row"><button class="btn small'+(on?'':' primary')+'" data-act="pn-toggle" aria-pressed="'+(on?'true':'false')+'">'+(on?'알림 끄기':'알림 켜기')+'</button></div><p class="hint">'+(!sup?'이 브라우저는 알림을 지원하지 않습니다. 아이폰은 홈 화면에 추가한 앱(iOS 16.4 이상)에서만 됩니다.':den?'브라우저 설정에서 이 사이트의 알림을 허용해 주세요.':'누가 나를 찌르면 앱이 가려져 있어도 알림으로 알려 줍니다. 앱을 완전히 닫았거나 기기가 앱을 멈춘 뒤에는 받지 못합니다.')+'</p></div>';
}
pnApply();

/* ---------- v46: 사람이 많을 때 끊기지 않게: 점수와 순위 계산을 기록이 바뀔 때만 다시 한다 ---------- */
var SCV=0,GC={st:{},sc:null},GCR=[],ADC={},ADN=0;
var MSV=0,CDK=null,CDV=null;
function scBump(c){if(c==='msgs'||c==='d'||c==='meta')MSV=(MSV|0)+1;if(c!=='msgs'&&c!=='live'&&c!=='reads'&&c!=='inbox'&&c!=='x')SCV=(SCV|0)+1;}
function gcSync(V){
  var r=[SCV,today(),START,END,V.certHour,V.me,V.days,V.progress,V.quiz,V.replies,V.songs,V.events,V.subjects,V.cfg];
  for(var i=0;i<r.length;i++)if(GCR[i]!==r[i]){GCR=r;GC={st:{},sc:null};break;}
  return GC;
}
function buildScores(V){var g=gcSync(V);return g.sc||(g.sc=buildScores0(V));}
function standings(V,from,to){var g=gcSync(V),k=from+'|'+to;return g.st[k]||(g.st[k]=standings0(V,from,to));}
function addDays(s,n){var k=s+'|'+n,v;if(!ADC)ADC={};v=ADC[k];if(v)return v;var d=pd(s);d.setDate(d.getDate()+n);v=fd(d);if(++ADN>20000){ADC={};ADN=0;}return ADC[k]=v;}
function chatData(V){
  var k=[MSV,V.msgs,V.me,V.cfg],same=CDK&&CDK.length===k.length;
  if(same)for(var i=0;i<k.length;i++)if(CDK[i]!==k[i]){same=false;break;}
  if(same)return CDV;
  CDV=chatData0(V);CDK=k;return CDV;
}
