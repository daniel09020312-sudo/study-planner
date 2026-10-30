// 공부방 플래너: 웹 푸시 보내기 중계. 브라우저는 푸시 서버로 바로 보낼 수 없어서(CORS) 여기서 대신 보낸다.
// 받는 쪽은 알려진 푸시 서버만, 머리글은 정해진 것만 넘긴다. 암호화와 서명은 보내는 앱이 이미 해서 온다.
const HOSTS = /(^|\.)(fcm\.googleapis\.com|push\.services\.mozilla\.com|push\.apple\.com|notify\.windows\.com)$/;
const PASS = ['Authorization', 'Content-Encoding', 'TTL', 'Urgency', 'Topic'];
function ub64(s) {
  s = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (s.length % 4) s += '=';
  const r = atob(s), o = new Uint8Array(r.length);
  for (let i = 0; i < r.length; i++) o[i] = r.charCodeAt(i);
  return o;
}
export async function onRequestPost({ request }) {
  let j;
  try { j = await request.json(); } catch (e) { return new Response('bad json', { status: 400 }); }
  let u;
  try { u = new URL(j.endpoint); } catch (e) { return new Response('bad endpoint', { status: 400 }); }
  if (u.protocol !== 'https:' || !HOSTS.test(u.hostname)) return new Response('host not allowed', { status: 403 });
  const body = ub64(j.body || '');
  if (body.length > 4200) return new Response('too large', { status: 413 });
  const h = {};
  PASS.forEach(k => { if (j.headers && typeof j.headers[k] === 'string') h[k] = j.headers[k].slice(0, 2000); });
  h['Content-Type'] = 'application/octet-stream';
  const r = await fetch(u.toString(), { method: 'POST', headers: h, body });
  return new Response(JSON.stringify({ status: r.status }), { status: 200, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}
export async function onRequestGet() {
  return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } });
}
