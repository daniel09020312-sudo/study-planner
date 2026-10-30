/* 웹 푸시 보내기용 암호화(RFC 8291 aes128gcm)와 VAPID 서명(RFC 8292). 브라우저와 Node 시험에서 같이 쓴다 */
var WP=(function(){
  var C=typeof crypto!=='undefined'&&crypto.subtle?crypto:(typeof require==='function'?require('crypto').webcrypto:null),E=new TextEncoder();
  function b64u(b){b=new Uint8Array(b);var s='';for(var i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
  function ub64(s){s=String(s).replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';var r=atob(s),o=new Uint8Array(r.length);for(var i=0;i<r.length;i++)o[i]=r.charCodeAt(i);return o;}
  function cat(){var n=0,i,a=[].slice.call(arguments);a.forEach(function(x){n+=x.length;});var o=new Uint8Array(n),p=0;a.forEach(function(x){o.set(x,p);p+=x.length;});return o;}
  async function hmac(key,data){var k=await C.subtle.importKey('raw',key,{name:'HMAC',hash:'SHA-256'},false,['sign']);return new Uint8Array(await C.subtle.sign('HMAC',k,data));}
  async function genVapid(){
    var kp=await C.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']);
    return {pub:b64u(await C.subtle.exportKey('raw',kp.publicKey)),jwk:await C.subtle.exportKey('jwk',kp.privateKey)};
  }
  async function jwt(aud,sub,jwk){
    var data=b64u(E.encode(JSON.stringify({typ:'JWT',alg:'ES256'})))+'.'+b64u(E.encode(JSON.stringify({aud:aud,exp:Math.floor(Date.now()/1000)+12*3600,sub:sub})));
    var key=await C.subtle.importKey('jwk',{kty:jwk.kty,crv:jwk.crv,x:jwk.x,y:jwk.y,d:jwk.d},{name:'ECDSA',namedCurve:'P-256'},false,['sign']);
    return data+'.'+b64u(await C.subtle.sign({name:'ECDSA',hash:'SHA-256'},key,E.encode(data)));
  }
  async function encrypt(uaPub,auth,text,salt,asKp){
    asKp=asKp||await C.subtle.generateKey({name:'ECDH',namedCurve:'P-256'},true,['deriveBits']);
    var asPub=new Uint8Array(await C.subtle.exportKey('raw',asKp.publicKey));
    var uaKey=await C.subtle.importKey('raw',uaPub,{name:'ECDH',namedCurve:'P-256'},false,[]);
    var secret=new Uint8Array(await C.subtle.deriveBits({name:'ECDH',public:uaKey},asKp.privateKey,256));
    var prkKey=await hmac(auth,secret);
    var ikm=await hmac(prkKey,cat(E.encode('WebPush: info\0'),uaPub,asPub,new Uint8Array([1])));
    salt=salt||C.getRandomValues(new Uint8Array(16));
    var prk=await hmac(salt,ikm);
    var cek=(await hmac(prk,cat(E.encode('Content-Encoding: aes128gcm\0'),new Uint8Array([1])))).slice(0,16);
    var nonce=(await hmac(prk,cat(E.encode('Content-Encoding: nonce\0'),new Uint8Array([1])))).slice(0,12);
    var key=await C.subtle.importKey('raw',cek,{name:'AES-GCM'},false,['encrypt']);
    var ct=new Uint8Array(await C.subtle.encrypt({name:'AES-GCM',iv:nonce},key,cat(E.encode(text),new Uint8Array([2]))));
    var rs=new Uint8Array([0,0,16,0]);
    return cat(salt,rs,new Uint8Array([asPub.length]),asPub,ct);
  }
  async function build(sub,text,vapid,subject){
    var aud=new URL(sub.endpoint).origin,t=await jwt(aud,subject,vapid.jwk);
    var body=await encrypt(ub64(sub.p256dh),ub64(sub.auth),text);
    return {endpoint:sub.endpoint,headers:{Authorization:'vapid t='+t+', k='+vapid.pub,'Content-Encoding':'aes128gcm',TTL:'86400',Urgency:'high'},body:b64u(body)};
  }
  return {b64u:b64u,ub64:ub64,genVapid:genVapid,jwt:jwt,encrypt:encrypt,build:build,hmac:hmac,cat:cat};
})();
if(typeof module!=='undefined')module.exports=WP;
