/* ---------- 웹 판: 찌르기를 앱 밖 알림(웹 푸시)으로 ----------
   열쇠(VAPID)는 저장소 rooms/webpush-vapid={pub, jwk}에 하나(처음 켠 기기가 만든다). 내 구독은 progress.<나>.ps={e,p,a,at}.
   찌를 때 상대 구독으로 암호화한 알림을 만들어 이 사이트의 api/push(Cloudflare Pages 함수)가 푸시 서버로 넘긴다 */
var PUSH={v:null,busy:false,tried:false};
function pushOk(){try{return 'serviceWorker' in navigator&&'PushManager' in window&&typeof Notification!=='undefined'&&!!(window.crypto&&crypto.subtle)&&!!S.remote;}catch(e){return false;}}
function pushVapid(){
  if(PUSH.v)return Promise.resolve(PUSH.v);
  var url=S.remote.url;
  return fbRaw(url,'webpush-vapid').then(function(v){
    if(v&&v.pub&&v.jwk&&v.jwk.d)return v;
    return WP.genVapid().then(function(nv){return fbRaw(url,'webpush-vapid','PUT',nv).then(function(){return fbRaw(url,'webpush-vapid');});});
  }).then(function(v){PUSH.v=v;return v;});
}
function pushSame(a,b){a=new Uint8Array(a||[]);if(a.length!==b.length)return false;for(var i=0;i<a.length;i++)if(a[i]!==b[i])return false;return true;}
function pushSubscribe(){
  if(!pushOk()||PUSH.busy)return Promise.resolve(false);
  PUSH.busy=true;
  return pushVapid().then(function(v){
    var key=WP.ub64(v.pub);
    return navigator.serviceWorker.ready.then(function(reg){
      return reg.pushManager.getSubscription().then(function(old){
        if(old&&old.options&&old.options.applicationServerKey&&!pushSame(old.options.applicationServerKey,key))return old.unsubscribe().then(function(){return null;});
        return old;
      }).then(function(sub){return sub||reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:key});});
    });
  }).then(function(sub){
    var j=sub.toJSON(),k=obj(j.keys);
    editProg(function(p){p.ps={e:j.endpoint,p:k.p256dh,a:k.auth,at:Date.now()};});
    PUSH.busy=false;return true;
  }).catch(function(){PUSH.busy=false;return false;});
}
function pushUnsub(){
  try{navigator.serviceWorker.ready.then(function(reg){return reg.pushManager.getSubscription();}).then(function(s){if(s)s.unsubscribe();}).catch(function(){});}catch(e){}
  editProg(function(p){delete p.ps;});
}
function pushSend(V,mid,msg){
  try{
    var ps=obj(obj(V.progress[mid]).ps);if(!ps.e||!ps.p||!ps.a||!(window.crypto&&crypto.subtle)||!S.remote)return;
    pushVapid().then(function(v){return WP.build({endpoint:ps.e,p256dh:ps.p,auth:ps.a},JSON.stringify(msg),v,location.origin);})
      .then(function(req){return fetch('api/push',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(req)});})
      .catch(function(){});
  }catch(e){}
}
/* 알림을 켜 둔 기기인데 이 방에 구독이 없으면 한 번 맞춘다 */
function pushEnsure(V){
  if(PUSH.tried||!V||!V.me||!S.ready||!pnOn()||!pushOk()||!netFresh())return;
  PUSH.tried=true;
  if(!obj(obj(V.progress[V.me]).ps).e)pushSubscribe();
}
/* 나 찌르기: 내 기기로 시험 알림(메시지는 남기지 않음) */
function pushSelf(){
  var V=view();if(!V.me)return;
  if(!pnOn()){flash('설정 > 찌르기 알림을 먼저 켜 주세요.');return;}
  if(!pushOk()){flash('이 브라우저는 앱 밖 알림을 받을 수 없습니다. 아이폰은 홈 화면에 추가한 앱에서만 됩니다.');return;}
  var go=function(){pushSend(view(),V.me,{t:'나를 찔렀습니다',b:'찌르기 알림 시험입니다',tag:'poke-self'});flash('나에게 알림을 보냈습니다. 몇 초 안에 알림이 오면 됩니다.');};
  if(obj(obj(V.progress[V.me]).ps).e)go();
  else{flash('알림을 받을 준비를 하는 중입니다.');pushSubscribe().then(function(ok){if(ok)go();else flash('알림 준비에 실패했습니다. 알림을 껐다 켜 보세요.');});}
}
