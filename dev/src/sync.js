/* ---------- 바뀐 것만 받기 (웹 판) ---------- */
// 방 기록(rooms/<방>/d)은 예전과 같고, 쓸 때마다 rooms/<방>/x/<자리> 에 새 표(token)를 같이 적는다(PATCH 한 번으로 함께).
// 열 때: 이 기기에 저장해 둔 기록으로 바로 보여 주고, x만 실시간으로 받아 표가 달라진 자리만 다시 받는다.
// 이 기기 저장이 없거나, 이틀 넘게 못 받았거나, 마지막 전체 받기가 오래됐으면(48시간, 바꾼 첫 며칠은 1시간: 예전 판이 x 없이 쓴 것을 놓치지 않게) 방 전체를 한 번 받는다.
// x는 3일 지난 표를 지운다. 사진(p)은 예전처럼 따로 둔다.
var SYNC_KEEP=3*86400000,SYNC_FULL=48*3600000,SYNC_FULL_EARLY=3600000,SYNC_EARLY_UNTIL=Date.parse('2026-10-26T00:00:00+09:00');
function xKey(path){return String(path).replace(/\//g,'|');}
function xPath(k){return String(k).replace(/\|/g,'/');}
function xTok(){return Date.now().toString(36)+'.'+Math.random().toString(36).slice(2,6);}
function xAge(tok){var t=parseInt(String(tok||'').split('.')[0],36);return isFinite(t)&&t>0?Date.now()-t:0;}
function u8len(s){s=String(s||'');try{return new TextEncoder().encode(s).length;}catch(e){return s.length;}}
/* 이 기기에서 이번 달 받은 기록 양 */
function dlAdd(n){
  if(!(n>0))return;var m=today().slice(0,7),o=null;
  try{o=JSON.parse(localStorage.getItem('gbb_dl')||'null');}catch(e){}
  if(!o||o.m!==m)o={m:m,b:0};o.b+=n;
  try{localStorage.setItem('gbb_dl',JSON.stringify(o));}catch(e){}
}
function dlMonth(){var o=null;try{o=JSON.parse(localStorage.getItem('gbb_dl')||'null');}catch(e){}return o&&o.m===today().slice(0,7)?+o.b||0:0;}
function fmtBytes(n){n=+n||0;if(n<1024)return n+'B';if(n<1048576)return Math.round(n/1024)+'KB';if(n<1073741824)return (n/1048576).toFixed(n<10485760?1:0)+'MB';return (n/1073741824).toFixed(2)+'GB';}
function firebaseNet(base,room){
  var rm=base.replace(/\/+$/,'')+'/rooms/'+encodeURIComponent(room),tree={},X={},L={},full=0,syncAt=0,sizeT=0,sizeV=0,paintT=null,fresh=false,live=false;
  function paintSoon(){if(paintT)return;paintT=setTimeout(function(){paintT=null;fromTree(tree);},60);}
  function url(path){return path.indexOf('pics/')===0?rm+'/p/'+path.slice(5)+'.json':rm+'/d/'+path+'.json';}
  function chk(r){if(!r.ok){var e=new Error('http '+r.status);e.code=(r.status===401||r.status===403)?'not_granted':'unavailable';throw e;}return r;}
  function getText(u){return fetch(u).then(chk).then(function(r){return r.text();}).then(function(t){dlAdd(u8len(t));return t;});}
  // 날마다 기록에 같이 들어가던 mid, date는 열쇠에 이미 있으므로 빼고 저장한다
  function slim(path,d){if(d&&typeof d==='object'&&path.indexOf('days/')===0&&(d.mid!==undefined||d.date!==undefined)){d=Object.assign({},d);delete d.mid;delete d.date;}return d;}
  // 기록과 표를 함께 쓴다. 성공하면 이 기기의 기록에도 바로 반영
  function send(path,d){
    d=slim(path,d===undefined?null:d);
    var tok=xTok(),k=xKey(path),body={};body['d/'+path]=d;body['x/'+k]=tok;
    function done(r,logged){if(r.ok){tree=setAt(tree,path,d===null?null:clone(d));if(logged){X[k]=tok;if(L[k]===undefined)L[k]=tok;}paintSoon();}return r;}
    return fetch(rm+'.json',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){
      // 저장소가 함께 쓰기를 받지 않으면(400) 예전처럼 기록만 쓴다. 다른 기기는 전체 받기 때 받는다
      if(r.status===400)return fetch(url(path),{method:d===null?'DELETE':'PUT',headers:{'Content-Type':'application/json'},body:d===null?undefined:JSON.stringify(d)}).then(function(r2){return done(r2,false);});
      return done(r,true);
    });
  }
  // 바뀐 칸만 쓴다: d/<문서>/<칸>들과 문서의 표를 PATCH 한 번으로. 다른 기기는 표를 보고 문서 전체를 다시 받는다
  function docOf(path){return String(path).split('/').slice(0,2).join('/');}
  function sendPatch(path,ops){
    // 이 기기가 그 문서의 마지막 판을 갖고 있었고(실시간 연결 중), 보내는 동안 다른 쓰기가 오지 않았을 때만 '최신'으로 친다. 아니면 표를 보고 다시 받는다
    var tok=xTok(),k=xKey(docOf(path)),body={},l0=L[k],cur=live&&X[k]===l0;
    Object.keys(ops).forEach(function(r){body['d/'+path+'/'+r]=ops[r]===undefined?null:ops[r];});body['x/'+k]=tok;
    function done(r,logged){
      if(r.ok){Object.keys(ops).forEach(function(r2){tree=setAt(tree,path+'/'+r2,ops[r2]==null?null:clone(ops[r2]));});if(logged&&cur&&L[k]===l0){X[k]=tok;if(L[k]===undefined)L[k]=tok;}paintSoon();}
      return r;
    }
    return fetch(rm+'.json',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){
      if(r.status===400)return fetch(url(path),{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(ops)}).then(function(r2){return done(r2,false);});
      return done(r,true);
    });
  }
  function getAt(path){var o=tree,a=String(path).split('/').filter(Boolean);for(var i=0;i<a.length;i++){if(!o||typeof o!=='object')return undefined;o=o[a[i]];}return o===undefined?undefined:clone(o);}
  return {mode:'firebase',
    send:send,
    sendPatch:sendPatch,
    peek:getAt,
    fresh:function(){return fresh;},
    patch:function(path,ops){
      function off(){var e=new Error('offline');e.code='offline';return e;}
      if(navigator.onLine===false||obHas(path)){obQueueOps(path,ops);if(navigator.onLine!==false)obFlush();return Promise.resolve();}
      return sendPatch(path,ops).then(chk).then(function(){})
        .catch(function(e){if(e&&e.code)throw e;obQueueOps(path,ops);});
    },
    meta:function(){return {x:X,full:full,sy:syncAt};},
    size:function(){var n=Date.now();if(n-sizeT>8000){sizeT=n;try{sizeV=u8len(JSON.stringify(tree));}catch(e){sizeV=0;}}return sizeV;},
    write:function(path,d){
      var pic=path.indexOf('pics/')===0;
      function off(){var e=new Error('offline');e.code='offline';return e;}
      if(navigator.onLine===false){if(pic)return Promise.reject(off());obQueue(path,d);return Promise.resolve();}
      if(pic)return fetch(url(path),{method:d===null?'DELETE':'PUT',headers:{'Content-Type':'application/json'},body:d===null?undefined:JSON.stringify(d)})
        .then(chk).then(function(){}).catch(function(e){if(e&&e.code)throw e;throw off();});
      return send(path,d).then(chk).then(function(){obDrop(path);})
        .catch(function(e){if(e&&e.code)throw e;obQueue(path,d);});
    },
    read:function(path){return getText(url(path)).then(function(t){return JSON.parse(t);});},
    start:function(){
      var es=null,first=true,pend={},fullBusy=false,snapped=false;
      function chkFresh(){if(!fresh&&snapped&&!fullBusy&&!Object.keys(pend).length){fresh=true;paintSoon();}}
      var c=cacheGet(),now=Date.now();
      if(c&&c.t&&c.x&&typeof c.x==='object'){tree=clone(c.t);X=clone(c.x);full=+c.full||0;syncAt=+c.sy||0;}
      var fullEvery=function(){return Date.now()<SYNC_EARLY_UNTIL?SYNC_FULL_EARLY:SYNC_FULL;};
      var needFull=!(c&&c.t&&c.x)||now-full>fullEvery();
      function fetchPath(k){
        if(pend[k]){pend[k].again=true;return;}
        var want=L[k];pend[k]={again:false};
        getText(rm+'/d/'+xPath(k)+'.json').then(function(t){
          var d=JSON.parse(t),p=pend[k];delete pend[k];
          tree=setAt(tree,xPath(k),d===null?null:d);X[k]=want;paintSoon();
          if(p&&p.again&&L[k]!==X[k])fetchPath(k);
          chkFresh();
        }).catch(function(){delete pend[k];setTimeout(function(){if(L[k]!==undefined&&L[k]!==X[k])fetchPath(k);},4000);});
      }
      function diff(keys){keys.forEach(function(k){if(L[k]!==undefined&&L[k]!==X[k]&&!fullBusy)fetchPath(k);});}
      function doFull(){
        if(fullBusy)return;fullBusy=true;var x0=clone(L);
        getText(rm+'/d.json').then(function(t){
          fullBusy=false;tree=obj(JSON.parse(t));X=x0;full=Date.now();syncAt=full;fromTree(tree);diff(Object.keys(L));chkFresh();
        }).catch(function(){fullBusy=false;if(!S.ready){S.ready=true;render();}});
      }
      function prune(){
        var old=Object.keys(L).filter(function(k){return xAge(L[k])>SYNC_KEEP;}).slice(0,400);
        if(!old.length||Math.random()>0.3)return;
        var body={};old.forEach(function(k){body[k]=null;});
        fetch(rm+'/x.json',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).catch(function(){});
      }
      function onSnap(data){
        L=obj(clone(data||{}));
        var stale=Date.now()-syncAt>SYNC_KEEP-86400000;
        if((first&&needFull)||stale||!Object.keys(tree).length)doFull();
        else{if(first)fromTree(tree);diff(Object.keys(L));syncAt=Date.now();}
        first=false;snapped=true;chkFresh();prune();
      }
      function onKey(k,v){
        if(!k)return;
        if(v===null||v===undefined){delete L[k];delete X[k];return;}
        L[k]=v;syncAt=Date.now();diff([k]);
      }
      // 앱이 가려진 지 2분이 지나면 실시간 연결을 끊는다(무료 Firebase는 동시 연결이 100개까지라서, 학급 전체가 켜 둔 채 두면 모자란다).
      // 돌아오면 다시 연결하고, 그동안 바뀐 자리는 표(x)를 비교해 받아 온다.
      var hideT=null;
      document.addEventListener('visibilitychange',function(){
        if(document.visibilityState==='hidden'){
          clearTimeout(hideT);
          hideT=setTimeout(function(){hideT=null;if(document.visibilityState==='hidden'&&es){try{es.close();}catch(e){}live=false;}},window.__SSE_HIDE_MS||120000);
        }else{
          clearTimeout(hideT);hideT=null;
          if(es&&es.readyState===2)open();
        }
      });
      setInterval(function(){if(document.visibilityState==='visible'&&!fullBusy&&full&&Date.now()-full>fullEvery())doFull();},30*60000);
      open();
      function open(){
      es=new EventSource(rm+'/x.json');
      es.addEventListener('put',function(ev){dlAdd(u8len(ev.data));var m=JSON.parse(ev.data);if(m.path==='/'||!m.path)onSnap(m.data);else onKey(String(m.path).replace(/^\//,''),m.data);});
      es.addEventListener('patch',function(ev){dlAdd(u8len(ev.data));var m=JSON.parse(ev.data),pre=String(m.path||'/').replace(/^\//,'');Object.keys(obj(m.data)).forEach(function(k){onKey(pre?pre+'/'+k:k,m.data[k]);});});
      es.addEventListener('keep-alive',function(){syncAt=Date.now();});
      es.addEventListener('cancel',function(){S.readOnly=true;S.ready=true;render();});
      es.addEventListener('auth_revoked',function(){S.readOnly=true;S.ready=true;render();});
      es.onopen=function(){live=true;clearTimeout(S.sseT);S.sseT=null;if(S.sseDown){S.sseDown=false;paintBanner();}obFlush();};
      es.onerror=function(){live=false;if(!S.sseT)S.sseT=setTimeout(function(){S.sseT=null;if(!es||es.readyState!==1){S.sseDown=true;paintBanner();}},4000);if(!S.ready){S.ready=true;if(navigator.onLine!==false)flash('공유 저장소에 연결하지 못했습니다. 인터넷 연결을 확인하세요.');render();}};
      }
    }};
}
