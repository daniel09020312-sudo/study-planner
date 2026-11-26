/* 한 입 화학: 인터넷이 없어도 열리게. 파일을 바꾸면 V를 올린다. */
var V = 'hanip-chem-2';
var FILES = ['./', 'index.html', 'app.css?v=2', 'mol.js?v=2', 'fig.js?v=2', 'data.js?v=2', 'ws.js?v=2', 'trip.js?v=2', 'app.js?v=2', 'font.woff2', 'manifest.webmanifest', 'icon.svg', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'icon-maskable.png'];
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
  if (r.mode === 'navigate') {
    // 화면: 저장해 둔 것으로 바로 열고, 뒤에서 새 것을 받아 둔다
    e.respondWith(caches.open(V).then(function (c) {
      return c.match('./').then(function (m) {
        var net = fetch(r).then(function (res) { if (res.ok && !res.redirected) c.put('./', res.clone()); return res; }).catch(function () { return m; });
        return m || net;
      });
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
