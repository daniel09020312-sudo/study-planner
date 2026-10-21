/* ---------- 오프라인: 마지막으로 받은 기록으로 열고, 내 기록은 모아 두었다가 연결되면 올린다 (웹 판) ---------- */
var OB=null,OB_BUSY=false,CACHE_T=null;
function obLoad(){if(OB)return OB;try{OB=JSON.parse(lsGet('gbb_outbox')||'[]');}catch(e){OB=[];}if(!Array.isArray(OB))OB=[];return OB;}
function obSave(){try{lsSet('gbb_outbox',OB.length?JSON.stringify(OB):null);}catch(e){}}
function obCount(){return obLoad().length;}
function obQueue(path,d){obLoad();OB=OB.filter(function(x){return x.p!==path;});OB.push({p:path,d:d===undefined?null:d});obSave();paintBanner();}
function obDrop(path){obLoad();var n=OB.length;OB=OB.filter(function(x){return x.p!==path;});if(OB.length!==n)obSave();}
function isOffline(){return navigator.onLine===false||!!S.sseDown;}
function obApply(){
  obLoad().forEach(function(x){
    var p=x.p,i=p.indexOf('/'),c=p.slice(0,i),id=p.slice(i+1);
    if(c==='pics')return;
    if(p==='meta/config'){S.config=x.d;return;}
    if(p==='meta/room'){S.roomInfo=obj(x.d);return;}
    if(COLLS.indexOf(c)<0)return;
    var m=Object.assign({},obj(S[c]));if(x.d===null)delete m[id];else m[id]=x.d;S[c]=m;
  });
}
function obFlush(){
  if(OB_BUSY||!obCount()||navigator.onLine===false||!S.remote)return;
  OB_BUSY=true;var sent=0,base=S.remote.url.replace(/\/+$/,'')+'/rooms/'+encodeURIComponent(S.remote.room)+'/d/';
  (function next(){
    var x=obLoad()[0];
    if(!x){OB_BUSY=false;if(sent){flash('인터넷이 다시 연결되어 모아 둔 기록 '+sent+'개를 올렸습니다.');}paintBanner();return;}
    fetch(base+x.p+'.json',{method:x.d===null?'DELETE':'PUT',headers:{'Content-Type':'application/json'},body:x.d===null?undefined:JSON.stringify(x.d)})
      .then(function(r){
        if(r.status===401||r.status===403){obDrop(x.p);S.readOnly=true;next();return;}
        if(!r.ok)throw new Error('http');
        obDrop(x.p);sent++;next();
      })
      .catch(function(){OB_BUSY=false;paintBanner();});
  })();
}
var CACHE_TREE=null;
function cacheSave(tree){
  CACHE_TREE=tree;if(CACHE_T)return;
  CACHE_T=setTimeout(function(){CACHE_T=null;try{lsSet('gbb_cache',JSON.stringify({at:Date.now(),t:CACHE_TREE}));}catch(e){try{lsSet('gbb_cache',null);}catch(e2){}}},1500);
}
function cacheBoot(){
  var c=null;try{c=JSON.parse(lsGet('gbb_cache')||'null');}catch(e){}
  if(!c||!c.t||typeof c.t!=='object')return;
  S.cacheAt=+c.at||0;S.booting=true;fromTree(c.t);S.booting=false;
}
window.addEventListener('online',function(){paintBanner();obFlush();});
window.addEventListener('offline',function(){paintBanner();});
setInterval(function(){if(obCount()&&!OB_BUSY&&navigator.onLine!==false)obFlush();},20000);
