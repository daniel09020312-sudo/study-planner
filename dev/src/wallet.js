/* ---------- 모든 방 잉크 (웹 판) ---------- */
// 사람마다 지갑 하나: rooms/wallet-<id> = {name, own:{물건:값}, rm:{<방>_<mid>:{e:공부한 분, gi:받은 선물, go:보낸 선물, n:방 이름, at}}, unl:관리자 서명, to:합쳐진 지갑}
// 방마다 progress.<me>.wal = 지갑 id. 이 기기의 지갑(gbb_wallet={id,name})과 이름이 같으면 저절로 이어 붙인다.
// 같은 사람이 지갑 두 개를 갖게 되면(다른 기기에서 따로 만든 경우) 이 기기에서 만날 때 하나로 합치고, 옛 지갑에 to를 남긴다.
// 관리자: 관리자 코드(ECDSA 비밀 열쇠)로 지갑 id에 서명해 unl에 두면, 누구나 공개 열쇠로 확인해 무제한으로 본다.
var ADM_PUB={kty:'EC',crv:'P-256',x:'vfzTJmmFW0USLkZF7xdyTcjlcOdr8HSkQjarXt0A8b4',y:'-_jKn2V1W8NOJsDkdfJVQzY09uPf05MsAB99oTFx_uY'};
var WALS={busy:false,loadAt:0,syncAt:0,tick:0,unlFor:'',unlChk:{}};
function walUrl(id,p){return S.remote.url.replace(/\/+$/,'')+'/rooms/wallet-'+id+(p?'/'+p:'')+'.json';}
function walGet(id){return fetch(walUrl(id)).then(function(r){if(!r.ok)throw new Error('http');return r.text();}).then(function(t){try{dlAdd(u8len(t));}catch(e){}return obj(JSON.parse(t));});}
function walPatch(id,body){return fetch(walUrl(id),{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw new Error('http');});}
function walDev(){try{var o=JSON.parse(localStorage.getItem('gbb_wallet')||'null');return o&&o.id?o:null;}catch(e){return null;}}
function walDevSet(o){try{localStorage.setItem('gbb_wallet',JSON.stringify(o));}catch(e){}}
function walNm(s){return String(s||'').replace(/\s+/g,'');}
function walNew(){var a='abcdefghijkmnpqrstuvwxyz23456789',o='',b=new Uint8Array(16),i;try{crypto.getRandomValues(b);}catch(e){for(i=0;i<16;i++)b[i]=Math.floor(Math.random()*256);}for(i=0;i<16;i++)o+=a[b[i]%a.length];return o;}
function b64u(buf){var s='',a=new Uint8Array(buf);for(var i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function unb64u(t){t=String(t||'').replace(/-/g,'+').replace(/_/g,'/');while(t.length%4)t+='=';var s=atob(t),a=new Uint8Array(s.length);for(var i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a;}
function walMsg(id){return new TextEncoder().encode('gbb-wallet:'+id);}
function walVerify(id,sig){
  try{if(!sig||!crypto.subtle)return Promise.resolve(false);
    return crypto.subtle.importKey('jwk',ADM_PUB,{name:'ECDSA',namedCurve:'P-256'},false,['verify'])
      .then(function(k){return crypto.subtle.verify({name:'ECDSA',hash:'SHA-256'},k,unb64u(sig),walMsg(id));}).catch(function(){return false;});
  }catch(e){return Promise.resolve(false);}
}
function walSign(id,d){
  return crypto.subtle.importKey('jwk',Object.assign({},ADM_PUB,{d:String(d||'').trim(),ext:true}),{name:'ECDSA',namedCurve:'P-256'},false,['sign'])
    .then(function(k){return crypto.subtle.sign({name:'ECDSA',hash:'SHA-256'},k,walMsg(id));}).then(b64u);
}
/* 받아 온 지갑을 화면에 반영 (관리자 서명은 확인한 뒤에) */
function walSet(id,w,key){
  WAL.on=true;WAL.id=id;WAL.key=key;WAL.own=obj(w.own);WAL.rm=obj(w.rm);WAL.name=String(w.name||'');
  var sig=String(w.unl||'');
  if(!sig){WAL.unl=false;}
  else if(WALS.unlChk[id+'|'+sig]!==undefined){WAL.unl=WALS.unlChk[id+'|'+sig];}
  else walVerify(id,sig).then(function(ok){WALS.unlChk[id+'|'+sig]=ok;if(WAL.id===id){WAL.unl=ok;render();}});
  render();
}
/* 지갑 찾기: 방에 적힌 지갑, 없으면 이 기기 지갑(이름이 같을 때), 그것도 없으면 새로 */
function walFind(V){
  var me=V.me,nm=V.byId[me].name,p=obj(V.progress[me]),dev=walDev();
  if(p.wal)return Promise.resolve(String(p.wal));
  if(dev&&walNm(dev.name)===walNm(nm)){editProg(function(q){q.wal=dev.id;});return Promise.resolve(dev.id);}
  var id=walNew();
  return walPatch(id,{name:nm,at:Date.now(),own:obj(obj(p.shop).own)}).then(function(){
    editProg(function(q){q.wal=id;});if(!dev)walDevSet({id:id,name:nm});return id;
  });
}
/* 지갑 받기: 합쳐진 지갑이면 따라가고, 이 기기의 같은 이름 다른 지갑이면 하나로 합친다 */
function walLoad(V,id,depth){
  depth=depth||0;var key=S.remote.room+'_'+V.me,nm=V.byId[V.me].name;
  return walGet(id).then(function(w){
    if(w.to&&depth<4){editProg(function(q){q.wal=String(w.to);});var dv=walDev();if(dv&&dv.id===id)walDevSet({id:String(w.to),name:dv.name});return walLoad(V,String(w.to),depth+1);}
    var dev=walDev();
    if(dev&&dev.id!==id&&walNm(dev.name)===walNm(nm)){
      return walGet(dev.id).then(function(o){
        if(o.to)return w;
        var body={};
        Object.keys(obj(o.own)).forEach(function(k){if(obj(w.own)[k]==null)body['own/'+k]=o.own[k];});
        Object.keys(obj(o.rm)).forEach(function(k){if(obj(w.rm)[k]==null)body['rm/'+k]=o.rm[k];});
        return (Object.keys(body).length?walPatch(id,body):Promise.resolve()).then(function(){return walPatch(dev.id,{to:id});}).then(function(){
          walDevSet({id:id,name:nm});return walGet(id);
        });
      }).catch(function(){return w;});
    }
    if(!dev)walDevSet({id:id,name:nm});
    return w;
  }).then(function(w){walSet(id,w,key);WALS.loadAt=Date.now();return w;});
}
/* 이 방 합계를 지갑에 적고, 이 방에서 산 것을 지갑에도 넣는다 */
function walSync(V){
  if(!WAL.on||!WAL.id||Date.now()-WALS.syncAt<20000)return;
  var L=inkLocal(V),cur=obj(WAL.rm[WAL.key]),body={};
  if((+cur.e||0)!==L.e||(+cur.gi||0)!==L.gi||(+cur.go||0)!==L.go||String(cur.n||'')!==roomName())body['rm/'+WAL.key]={e:L.e,gi:L.gi,go:L.go,n:roomName(),at:Date.now()};
  var own=obj(obj(obj(V.progress[V.me]).shop).own);Object.keys(own).forEach(function(k){if(WAL.own[k]==null)body['own/'+k]=+own[k]||0;});
  if(!Object.keys(body).length)return;
  WALS.syncAt=Date.now();
  walPatch(WAL.id,body).then(function(){Object.keys(body).forEach(function(k){var a=k.split('/');if(a[0]==='rm')WAL.rm[a[1]]=body[k];else WAL.own[a[1]]=body[k];});}).catch(function(){WALS.syncAt=0;});
}
/* 관리자 열쇠가 이 기기에 있으면 내 지갑에 서명해 둔다 */
function walAutoAdm(){
  var d=null;try{d=localStorage.getItem('gbb_adm');}catch(e){}
  var dev=walDev();
  if(!d||!WAL.on||WAL.unl||!dev||dev.id!==WAL.id||WALS.unlFor===WAL.id)return;
  WALS.unlFor=WAL.id;
  walSign(WAL.id,d).then(function(sig){return walVerify(WAL.id,sig).then(function(ok){if(!ok)return;return walPatch(WAL.id,{unl:sig}).then(function(){WALS.unlChk[WAL.id+'|'+sig]=true;WAL.unl=true;render();});});}).catch(function(){});
}
function walTick(){
  if(!S.remote||!S.ready||!S.net||S.net.mode!=='firebase'||WALS.busy)return;
  if(++WALS.tick%3)return;
  var V=view();if(!V.me||!V.byId[V.me]||!canWrite()||navigator.onLine===false)return;
  var key=S.remote.room+'_'+V.me,pw=String(obj(V.progress[V.me]).wal||'');
  if(WAL.on&&WAL.key===key&&(!pw||pw===WAL.id)&&Date.now()-WALS.loadAt<5*60000){walSync(V);walAutoAdm();return;}
  WALS.busy=true;
  walFind(V).then(function(id){return walLoad(V,id);}).then(function(){WALS.busy=false;walSync(view());}).catch(function(){WALS.busy=false;WALS.loadAt=Date.now()-4*60000;});
}
WALH.buy=function(id,price){if(!WAL.on||!WAL.id)return;WAL.own[id]=price;var b={};b['own/'+id]=price;walPatch(WAL.id,b).catch(function(){});};
WALH.adm=function(code){
  if(!WAL.on||!WAL.id||!code)return;
  walSign(WAL.id,code).then(function(sig){return walVerify(WAL.id,sig).then(function(ok){
    if(!ok)throw new Error('bad');
    return walPatch(WAL.id,{unl:sig}).then(function(){
      WALS.unlChk[WAL.id+'|'+sig]=true;WAL.unl=true;S.admOpen=false;
      try{localStorage.setItem('gbb_adm',code);}catch(e){}
      walDevSet({id:WAL.id,name:WAL.name||walDev()&&walDev().name||''});
      flash('관리자 코드를 확인했습니다. 잉크를 무제한으로 쓰고 선물할 수 있습니다.');render();
    });
  });}).catch(function(){flash('관리자 코드가 맞지 않습니다.');});
};
