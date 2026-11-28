/* 한 입 화학: 인터넷이 없어도 열리게. 파일을 바꾸면 V를 올린다. */
var V = 'hanip-chem-21';
var FILES = ['./', 'index.html', 'app.css?v=21', 'mol.js?v=21', 'fig.js?v=21', 'data.js?v=21', 'ws.js?v=21', 'ppt.js?v=21', 'redox.js?v=21', 'trip.js?v=21', 'app.js?v=21', 'font.woff2', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'icon-maskable.png'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(V).then(function (c) { return c.addAll(FILES); }));
  self.skipWaiting();
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k.indexOf('hanip-chem-') === 0 && k !== V; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var r = e.request;
  if (r.method !== 'GET') return;
  var u = new URL(r.url);
  if (u.origin !== location.origin) return;
  if (/\/(icon|splash|apple-touch)[^/]*\.png$/.test(u.pathname)) return; // 아이콘·시작 이미지는 늘 인터넷에서(아이폰이 홈 화면에 추가할 때)
  if (r.mode === 'navigate') {
    // 화면: 인터넷에서 새 것을 먼저(3초 넘으면 저장해 둔 것), 안 되면 저장해 둔 것
    e.respondWith(caches.open(V).then(function (c) {
      var net = fetch(r).then(function (res) { if (res.ok && !res.redirected) c.put('./', res.clone()); return res; });
      var slow = new Promise(function (ok) { setTimeout(ok, 3000); }).then(function () { return c.match('./'); });
      return Promise.race([net.catch(function () { return c.match('./'); }), slow.then(function (m) { return m || net; })]);
    }));
    return;
  }
  e.respondWith(caches.match(r).then(function (m) {
    return m || fetch(r).then(function (res) {
      if (res.ok && u.pathname.indexOf('/chem/') >= 0) { var cp = res.clone(); caches.open(V).then(function (c) { c.put(r, cp); }); }
      return res;
    });
  }));
});
