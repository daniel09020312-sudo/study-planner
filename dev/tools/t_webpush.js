// 웹 푸시 암호화가 맞는지: 받는 쪽 키로 다시 풀어 본다(RFC 8291), VAPID 서명이 검증되는지
const WP = require('../src/webpush.js');
const C = require('crypto').webcrypto;
(async () => {
  const ua = await C.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
  const uaPub = new Uint8Array(await C.subtle.exportKey('raw', ua.publicKey));
  const auth = C.getRandomValues(new Uint8Array(16));
  const msg = JSON.stringify({ t: '민준 님이 찔렀습니다', b: '눌러서 답장하기' });
  const body = await WP.encrypt(uaPub, auth, msg);
  // 풀기
  const salt = body.slice(0, 16), rs = (body[16] << 24) | (body[17] << 16) | (body[18] << 8) | body[19], idlen = body[20], asPub = body.slice(21, 21 + idlen), ct = body.slice(21 + idlen);
  const asKey = await C.subtle.importKey('raw', asPub, { name: 'ECDH', namedCurve: 'P-256' }, false, []);
  const secret = new Uint8Array(await C.subtle.deriveBits({ name: 'ECDH', public: asKey }, ua.privateKey, 256));
  const E = new TextEncoder();
  const prkKey = await WP.hmac(auth, secret);
  const ikm = await WP.hmac(prkKey, WP.cat(E.encode('WebPush: info\0'), uaPub, asPub, new Uint8Array([1])));
  const prk = await WP.hmac(salt, ikm);
  const cek = (await WP.hmac(prk, WP.cat(E.encode('Content-Encoding: aes128gcm\0'), new Uint8Array([1])))).slice(0, 16);
  const nonce = (await WP.hmac(prk, WP.cat(E.encode('Content-Encoding: nonce\0'), new Uint8Array([1])))).slice(0, 12);
  const k = await C.subtle.importKey('raw', cek, { name: 'AES-GCM' }, false, ['decrypt']);
  const pt = new Uint8Array(await C.subtle.decrypt({ name: 'AES-GCM', iv: nonce }, k, ct));
  const text = new TextDecoder().decode(pt.slice(0, pt.length - 1));
  console.log('rs', rs, 'idlen', idlen, 'delim', pt[pt.length - 1], 'roundtrip', text === msg);
  // VAPID
  const v = await WP.genVapid();
  const t = await WP.jwt('https://fcm.googleapis.com', 'https://study-planner-2tk.pages.dev', v.jwk);
  const [h, c, s] = t.split('.');
  const pub = await C.subtle.importKey('raw', WP.ub64(v.pub), { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
  const okSig = await C.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, pub, WP.ub64(s), E.encode(h + '.' + c));
  console.log('pub len', WP.ub64(v.pub).length, 'jwt verify', okSig, 'claims', Buffer.from(c, 'base64').toString());
  const req = await WP.build({ endpoint: 'https://fcm.googleapis.com/fcm/send/abc', p256dh: WP.b64u(uaPub), auth: WP.b64u(auth) }, msg, v, 'https://study-planner-2tk.pages.dev');
  console.log('headers', Object.keys(req.headers).join(','), 'bodylen', WP.ub64(req.body).length);
})();
// RFC 8291 부록 A 예제와 똑같이 나오는지
(async () => {
  const asPubB = WP.ub64('BP4z9KsN6nGRTbVYI_c7VJSPQTBtkgcy27mlmlMoZIIgDll6e3vCYLocInmYWAmS6TlzAC8wEqKK6PBru3jl7A8');
  const jwk = { kty: 'EC', crv: 'P-256', d: 'yfWPiYE-n46HLnH0KqZOF1fJJU3MYrct3AELtAQ-oRw', x: WP.b64u(asPubB.slice(1, 33)), y: WP.b64u(asPubB.slice(33, 65)) };
  const priv = await C.subtle.importKey('jwk', jwk, { name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
  const pub = await C.subtle.importKey('raw', asPubB, { name: 'ECDH', namedCurve: 'P-256' }, true, []);
  const body = await WP.encrypt(WP.ub64('BCVxsr7N_eNgVRqvHtD0zTZsEc6-VV-JvLexhqUzORcxaOzi6-AYWXvTBHm4bjyPjs7Vd8pZGH6SRpkNtoIAiw4'), WP.ub64('BTBZMqHH6r4Tts7J_aSIgg'), 'When I grow up, I want to be a watermelon', WP.ub64('DGv6ra1nlYgDCS1FRnbzlw'), { privateKey: priv, publicKey: pub });
  const want = 'DGv6ra1nlYgDCS1FRnbzlwAAEABBBP4z9KsN6nGRTbVYI_c7VJSPQTBtkgcy27mlmlMoZIIgDll6e3vCYLocInmYWAmS6TlzAC8wEqKK6PBru3jl7A_yl95bQpu6cVPTpK4Mqgkf1CXztLVBSt2Ks3oZwbuwXPXLWyouBWLVWGNWQexSgSxsj_Qulcy4a-fN';
  console.log('RFC 8291 vector', WP.b64u(body) === want ? 'MATCH' : 'MISMATCH ' + WP.b64u(body));
})();
