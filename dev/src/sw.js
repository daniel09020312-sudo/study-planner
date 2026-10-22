/* 공부방 플래너: 인터넷이 없어도 앱 화면이 열리게 (화면은 새 버전 먼저, 안 되면 저장해 둔 것) */
var C='gbb-shell-v1';
self.addEventListener('install',function(e){
  e.waitUntil(caches.open(C).then(function(c){return c.addAll(['./','manifest.webmanifest','icon-180.png','icon-192.png','icon-512.png']);}).catch(function(){}));
  self.skipWaiting();
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==C;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));
});
self.addEventListener('fetch',function(e){
  var r=e.request;if(r.method!=='GET')return;
  var u=new URL(r.url);if(u.origin!==location.origin)return;
  if(/\/version\.txt$/.test(u.pathname))return; // 새 판 확인은 늘 인터넷에서
  if(r.mode==='navigate'){
    e.respondWith(fetch(r).then(function(res){if(res.ok&&!res.redirected){var cp=res.clone();caches.open(C).then(function(c){c.put('./',cp);});}return res;}).catch(function(){return caches.match('./');}));
    return;
  }
  e.respondWith(caches.match(r).then(function(m){
    var net=fetch(r).then(function(res){if(res.ok){var cp=res.clone();caches.open(C).then(function(c){c.put(r,cp);});}return res;});
    return m||net;
  }));
});
