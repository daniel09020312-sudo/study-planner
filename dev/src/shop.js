/* ---------- 상점: 공부 10분마다 잉크 한 방울, 잉크로 모양만 바꾸는 것을 산다 ---------- */
// 잉크는 이 방에서 공부한 시간(타이머 + 직접 넣은 시간은 하루 RULE.manualMax까지)으로 계산하고, 산 것만 progress.shop.own[물건]=값 으로 적는다.
// 남은 잉크 = 모은 잉크 - 산 값의 합. 상점이 생기기 전에 이 기기에서 쓰던 컨셉, 대표 색, 타이머 모양은 처음 한 번 그냥 준다(shop.gf).
// 이모티콘은 기본만 처음부터 쓰고, 장난과 감정은 팩으로 산다. 모양은 이 기기에 저장되고(예전과 같음), 산 것만 고를 수 있다.
var INK_MIN=10;
var SHOP_CATS=[['look','방 꾸미기'],['color','대표 색'],['timer','타이머'],['stk','이모티콘']];
var SHOP_LOOK={grid:[100,'공책 모눈 위에 손글씨'],board:[100,'초록 칠판과 분필 글씨'],pop:[100,'동글동글 말랑한 버튼'],line:[100,'얇은 검은 선으로 또렷하게'],glass:[100,'뒤가 비치는 유리 카드'],night:[100,'별이 뜬 밤하늘'],paper:[100,'따뜻한 크라프트 종이와 스티치'],news:[100,'흑백 신문 지면과 명조 제목'],sunset:[100,'노을빛 그러데이션 하늘']};
var SHOP_TIMER={digits:[50,'큰 숫자만 깔끔하게'],bar:[50,'숫자 아래 줄어드는 막대'],pie:[50,'시간이 줄어드는 원판'],flip:[50,'넘어가는 넘김 시계'],analog:[50,'눈금과 바늘이 있는 아날로그 시계'],orbit:[50,'분과 초가 함께 도는 두 겹 고리']};
var SHOP_STK={playful:[50,'어쩔~, 메롱, 뇌 정지 같은 장난'],emotions:[50,'신난다!, 부끄러워, 감동이야 같은 마음'],cat:[100,'출석!, 멘탈 바사삭, 오늘도 수고했어. 움직이는 까만 고양이'],dog:[100,'개힘듦, 할 게 산더미, 간식 필요. 움직이는 하얀 강아지'],nyang:[150,'고양이와 강아지가 같이 공부합니다. 움직이는 둘']};
// 숨은 팩: 앞의 팩을 모두 사야 무엇인지 보이고 살 수 있다
var SHOP_HIDE={nyang:['cat','dog']};
var INK_SVG='<svg class="inkd" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8c3.2 4 6.2 7.6 6.2 11.2a6.2 6.2 0 0 1-12.4 0c0-3.6 3-7.2 6.2-11.2z"/><path class="hl" d="M9.4 14.6a2.8 2.8 0 0 0 2.4 2.7"/></svg>';
var SHOP_GF=false;
// 모든 방 잉크(웹 판): wallet.js가 채운다. on이면 지갑의 다른 방 합계와 산 것을 더한다
var WAL={on:false,id:'',key:'',own:{},rm:{},rk:{},unl:false},WALH={buy:null,adm:null,revoke:null};
var GIFT_AMTS=[10,30,50,100];
function shopItems(){
  if(shopItems.c)return shopItems.c;var a=[];
  CONCEPTS.forEach(function(x){var m=SHOP_LOOK[x.id];a.push({id:'c:'+x.id,v:x.id,cat:'look',name:x.name,price:m?m[0]:0,desc:m?m[1]:'처음 모양',free:x.id==='basic'});});
  ACCENTS.forEach(function(x){a.push({id:'a:'+x.id,v:x.id,cat:'color',name:x.name,price:0,desc:x.g==='p'?'파스텔, 무료':'대표 색, 무료',free:true,ac:x});});
  TSTYLES.forEach(function(x){var m=SHOP_TIMER[x[0]];a.push({id:'t:'+x[0],v:x[0],cat:'timer',name:x[1],price:m?m[0]:0,desc:m?m[1]:'처음 모양',free:x[0]==='ring'});});
  STK_PACKS.forEach(function(x){var m=SHOP_STK[x[0]];a.push({id:'k:'+x[0],v:x[0],cat:'stk',name:x[1]+' 팩',price:m?m[0]:120,desc:m?m[1]:(x[0]==='basic'?'처음부터 쓰는 이모티콘':'새 이모티콘'),free:x[0]==='basic'});});
  return shopItems.c=a;
}
function shopItem(id){return shopItems().filter(function(x){return x.id===id;})[0]||null;}
function shopOwn(V){return obj(obj(obj(V.progress[V.me]).shop).own);}
function shopShown(V,id){var it=shopItem(id),req=it&&it.cat==='stk'?SHOP_HIDE[it.v]:null;if(!req)return true;return shopOwns(V,id)||req.every(function(p){return shopOwns(V,'k:'+p);});}
function stkHid(V,pack){return !shopShown(V,'k:'+pack);}
function stkHidNote(pack){var req=SHOP_HIDE[pack]||[];return req.map(function(p){var it=shopItem('k:'+p);return it?it.name:p;}).join('과 ')+'을 모두 사면 무엇인지 보이고 살 수 있습니다.';}
function stkHidPrev(){return '<span class="shpv shstk shq" aria-hidden="true"><i>?</i><i>?</i><i>?</i><i>?</i></span>';}
function walOwn(){return WAL.on?obj(WAL.own):{};}
/* 관리자가 되돌린 것: 지갑 rk에 적혀 있으면 다른 방 기록에 남은 것도 산 것으로 치지 않는다 */
function shopRk(id){return WAL.on&&obj(WAL.rk)[id]!=null;}
function shopOwnLive(V){var o=shopOwn(V),r={};Object.keys(o).forEach(function(k){if(!shopRk(k))r[k]=o[k];});return r;}
function shopOwns(V,id){var it=shopItem(id);if(!it)return false;if(it.free)return true;return V&&V.me?(shopOwnLive(V)[id]!=null||walOwn()[id]!=null):false;}
function inkMins(V,mid,date){
  var pre=mid+'_',m=0;
  Object.keys(V.days).forEach(function(k){if(k.indexOf(pre)!==0)return;if(date&&k!==pre+date)return;var d=obj(V.days[k]);m+=sumMins(d.mins)+Math.min(sumMins(d.manual),RULE.manualMax);});
  return m;
}
/* 이 방에서: 공부한 분, 받은 선물, 보낸 선물 */
function inkLocal(V){
  var e=inkMins(V,V.me),gi=0,go=0,g=obj(V.gifts);
  Object.keys(g).forEach(function(k){var x=obj(g[k]),n=Math.max(0,Math.floor(+x.n||0));if(x.to===V.me)gi+=n;if(x.from===V.me)go+=n;});
  return {e:e,gi:gi,go:go};
}
/* 남은 잉크 = (공부한 분/10 + 받은 선물) - (산 값 + 보낸 선물). 지갑이 있으면 다른 방 것도 더한다 */
function inkOf(V){
  if(!V||!V.me)return {got:0,spent:0,bal:0,today:0,gi:0,unl:false,rooms:1};
  if(V._ink)return V._ink;
  var L=inkLocal(V),m=L.e,gi=L.gi,go=L.go,own=Object.assign({},shopOwnLive(V),walOwn()),spent=0,n=1;
  if(WAL.on)Object.keys(obj(WAL.rm)).forEach(function(k){if(k===WAL.key)return;var r=obj(WAL.rm[k]);m+=Math.max(0,+r.e||0);gi+=Math.max(0,+r.gi||0);go+=Math.max(0,+r.go||0);n++;});
  Object.keys(own).forEach(function(k){spent+=Math.max(0,+own[k]||0);});
  var got=Math.floor(m/INK_MIN)+gi+(WAL.on?Math.floor(+WAL.adj||0):0);spent+=go;
  return V._ink={got:got,spent:spent,bal:WAL.unl?Infinity:Math.max(0,got-spent),today:Math.floor(inkMins(V,V.me,today())/INK_MIN),gi:gi,unl:!!WAL.unl,rooms:n};
}
function roJ(w){w=String(w||'');var c=w.charCodeAt(w.length-1);if(!(c>=0xAC00&&c<=0xD7A3))return w+'로';var f=(c-0xAC00)%28;return w+(f&&f!==8?'으로':'로');}
function inkTag(n){return '<span class="inkt">'+INK_SVG+'<b>'+n+'</b></span>';}
function shopInUse(id){
  var it=shopItem(id);if(!it)return false;
  if(it.cat==='look')return conceptPref().id===it.v;
  if(it.cat==='color')return accentPref().id===it.v;
  if(it.cat==='timer')return tstyle()===it.v;
  return false;
}
function shopUse(id){
  var it=shopItem(id);if(!it)return;
  if(it.cat==='look'){lsSet('gbb_concept',it.v);applyLook();}
  else if(it.cat==='color'){lsSet('gbb_accent',it.v);applyLook();}
  else if(it.cat==='timer'){S.tstyle=it.v;lsSet('gbb_tstyle',it.v);}
  else if(it.cat==='stk'){S.stkPack=it.v;}
}
/* 상점이 생기기 전에 쓰던 모양은 한 번 그냥 준다 */
function shopGf(){
  if(SHOP_GF||!netFresh())return;var V=view();
  if(!S.ready||!V||!V.me||!canWrite())return;
  SHOP_GF=true;
  if(obj(obj(V.progress[V.me]).shop).gf)return;
  var give=[],c=conceptPref().id,a=accentPref().id,t=tstyle();
  if(c!=='basic')give.push('c:'+c);if(a!=='blue')give.push('a:'+a);if(t!=='ring')give.push('t:'+t);
  editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);give.forEach(function(k){if(sh.own[k]==null)sh.own[k]=0;});sh.gf=1;});
}
/* 미리 보기 */
function shopPrev(it){
  if(it.cat==='look')return '<span class="cvp cvp-'+it.v+' shpv" aria-hidden="true"><i></i><i></i><i></i></span>';
  if(it.cat==='color')return '<span class="shpv shcol" style="--a:'+it.ac.l.a+';--b:'+it.ac.d.a+';--s:'+it.ac.l.soft+'" aria-hidden="true"><i></i><u>공부 시작</u></span>';
  if(it.cat==='timer')return '<span class="tsp tsp-'+it.v+' shpv" aria-hidden="true">'+TSPREV[it.v]+'</span>';
  var ids=STK.filter(function(x){return x[0].indexOf(it.v+'-')===0;}).slice(0,4);
  return '<span class="shpv shstk" aria-hidden="true">'+ids.map(function(x){return stkImg(x[0]);}).join('')+'</span>';
}
function shopBtn(V,it,ink){
  var own=shopOwns(V,it.id),use=shopInUse(it.id);
  if(own){
    if(it.cat==='stk')return '<span class="shst">'+(it.free?'기본':'가지고 있음')+'</span>';
    return use?'<span class="shst on">쓰는 중</span>':'<button class="btn small" data-act="shop-use" data-id="'+esc(it.id)+'">쓰기</button>';
  }
  var lack=it.price-ink.bal,cf=S.confirm==='buy:'+it.id;
  if(lack>0)return '<button class="shbuy" disabled aria-label="'+esc(it.name)+', 잉크 '+it.price+'방울, '+lack+'방울 모자람">'+inkTag(it.price)+'</button><small class="shlack">'+lack+'방울 더</small>';
  return '<button class="shbuy'+(cf?' cf':'')+'" data-act="shop-buy" data-id="'+esc(it.id)+'" aria-label="'+esc(it.name)+' 사기, 잉크 '+it.price+'방울">'+(cf?'한 번 더 누르면 삽니다':inkTag(it.price))+'</button>';
}
function modalShop(V){
  var ink=inkOf(V),cat=S.shopCat||'look',items=shopItems().filter(function(x){return x.cat===cat;});
  var b='<div class="wallet'+(ink.unl?' unl':'')+'"><div class="wl">'+INK_SVG+'<div><small>내 잉크'+(ink.rooms>1?' · 방 '+ink.rooms+'개 합계':'')+'</small><b>'+(ink.unl?'무제한':ink.bal+'<em>방울</em>')+'</b></div></div>';
  b+='<p class="wr">공부 10분마다 잉크 한 방울'+(ink.today?'<span class="wtd">오늘 +'+ink.today+'</span>':'')+'<small>'+(ink.unl?'관리자는 잉크를 쓰지 않고 사고 선물합니다':'모은 잉크 '+ink.got+(ink.gi?' (받은 선물 '+ink.gi+')':'')+' · 쓴 잉크 '+ink.spent)+'</small><span class="wbtns">'+(WAL.on&&WALH.link?'<button class="btn small gfbtn" data-act="wal-open" aria-expanded="'+(S.walLinkOpen?'true':'false')+'">다른 방과 같이 쓰기</button>':'')+'<button class="btn small gfbtn" data-act="gift-open" aria-expanded="'+(S.giftOpen?'true':'false')+'">'+(S.giftOpen?'선물 닫기':'잉크 선물하기')+'</button></span></p></div>';
  if(S.walLinkOpen&&WAL.on)b+=walPanel(V,ink);
  if(S.giftOpen)b+=giftPanel(V,ink);
  b+='<div class="seg mini shcats" style="--i:'+SHOP_CATS.map(function(x){return x[0];}).indexOf(cat)+';--n:'+SHOP_CATS.length+'" role="group" aria-label="상품 종류">'+SHOP_CATS.map(function(x){return '<button data-act="shop-cat" data-v="'+x[0]+'" aria-pressed="'+(cat===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  b+='<div class="shgrid'+(cat==='stk'?' wide':'')+'" id="shg-'+cat+'">';
  items.forEach(function(it){
    var foc=S.shopFocus===it.id,peek=cat==='stk'&&S.shopPeek===it.id;
    if(!shopShown(V,it.id)){
      var hreq=SHOP_HIDE[it.v]||[],hgot=hreq.filter(function(p){return shopOwns(V,'k:'+p);}).length;
      b+='<div class="shi hid'+(foc?' foc':'')+'" id="shi-'+esc(it.id.replace(':','-'))+'">'+stkHidPrev()+'<div class="shn"><b>비밀 팩</b><small>'+esc(stkHidNote(it.v))+'</small></div><div class="sha"><span class="shst"><svg class="lki" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg>'+hreq.length+'개 중 '+hgot+'개 샀음</span></div></div>';
      return;
    }
    var fresh=SHOP_HIDE[it.v]&&!shopOwns(V,it.id);
    b+='<div class="shi'+(foc?' foc':'')+(shopOwns(V,it.id)?' own':'')+'" id="shi-'+esc(it.id.replace(':','-'))+'">'+shopPrev(it)+'<div class="shn"><b>'+esc(it.name)+(fresh?'<em class="shnew">새로 열림</em>':'')+'</b><small>'+esc(it.desc)+'</small></div><div class="sha">'+shopBtn(V,it,ink)+'</div>';
    if(cat==='stk'){
      b+='<button class="shpeek" data-act="shop-peek" data-id="'+esc(it.id)+'" aria-expanded="'+(peek?'true':'false')+'">'+(peek?'미리 보기 접기':'전체 미리 보기')+'</button>';
      if(peek)b+='<div class="shall">'+STK.filter(function(x){return x[0].indexOf(it.v+'-')===0;}).map(function(x){return '<span class="stk" data-m="'+esc(x[2])+'">'+stkImg(x[0])+'<small>'+esc(x[1])+'</small></span>';}).join('')+'</div>';
    }
    b+='</div>';
  });
  b+='</div><p class="hint" style="margin-top:14px">'+(WAL.on?'잉크와 산 것은 내가 들어간 모든 방에서 같이 씁니다. ':'산 것은 이 방에서 계속 쓸 수 있습니다. ')+'모양만 바뀌고 기능과 점수는 그대로입니다. 고른 모양은 이 기기에 저장됩니다.</p>';
  var admHave=false;try{admHave=!!localStorage.getItem('gbb_adm');}catch(e){}
  if(WAL.on&&WALH.unlOff&&ink.unl)b+='<div class="admrow"><button class="btn small soft" data-act="adm-off">'+(S.confirm==='admoff'?'한 번 더 누르면 무제한을 끕니다':'잉크 무제한 끄기')+'</button></div>';
  else if(WAL.on&&WALH.adm&&!ink.unl&&admHave)b+='<div class="admrow"><button class="btn small soft" data-act="adm-on">잉크 무제한 다시 켜기</button></div>';
  else if(WAL.on&&WALH.adm&&!ink.unl)b+=S.admOpen?'<div class="admrow"><input type="text" class="admin-secret" id="admCode" data-draft="admCode" data-enter="adm-go" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="관리자 코드" aria-label="관리자 코드"><button class="btn small" data-act="adm-go">확인</button></div>':'<button class="linkbtn admlink" data-act="adm-open">관리자 코드</button>';
  if(WAL.on&&WALH.addInk&&(ink.unl||admHave))b+='<div class="admrow"><input type="number" inputmode="numeric" id="admInk" data-draft="admInk" value="'+esc(String(S.draft.admInk||''))+'" placeholder="더할 잉크(빼려면 -)" aria-label="내 잉크에 더할 방울"><button class="btn small" data-act="adm-ink">'+(S.confirm==='admink'?'한 번 더 누르면 적용':'관리자: 내 잉크 더하기')+'</button></div>'+(+WAL.adj?'<p class="hint">관리자가 더한 잉크 '+Math.floor(+WAL.adj)+'방울</p>':'');
  if(ink.unl||admHave){var rva=shopItems().filter(function(x){return !x.free&&shopOwns(V,x.id);});
    if(rva.length){b+='<button class="linkbtn admlink" data-act="adm-rvlist" aria-expanded="'+(S.admRv?'true':'false')+'">관리자: 산 물건 되돌리기 ('+rva.length+'개)</button>';
      if(S.admRv)b+='<div class="chips admrv">'+rva.map(function(x){var cf=S.confirm==='rv1:'+x.id;return '<button class="chip" data-act="adm-rv1" data-id="'+esc(x.id)+'">'+(cf?'한 번 더 누르면 되돌림':esc(x.name)+' 되돌리기')+'</button>';}).join('')+'</div>';}}
  if(ink.unl){var rvn=shopRevokeList(V).length;if(rvn)b+='<button class="linkbtn admlink" data-act="adm-revoke">'+(S.confirm==='admrv'?'한 번 더 누르면 산 이모티콘 팩 '+rvn+'개를 되돌립니다':'관리자: 산 이모티콘 팩 되돌리기')+'</button>';}
  return dlg('wide',{id:'shop',t:'상점'},b);
}
/* 관리자: 산 물건 하나 되돌리기(낸 잉크는 돌아옴). 쓰고 있던 모양이면 기본으로 */
function shopRevokeOne(V,id){
  var it=shopItem(id);if(!it||it.free||!shopOwns(V,id))return false;
  editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);delete sh.own[id];});
  if(WALH.revoke)WALH.revoke([id]);
  if(shopInUse(id)){if(it.cat==='look'){lsSet('gbb_concept','basic');applyLook();}else if(it.cat==='timer'){S.tstyle='ring';lsSet('gbb_tstyle','ring');}}
  if(it.cat==='stk'){if(S.stkPack===it.v)S.stkPack='basic';Object.keys(SHOP_HIDE).forEach(function(pk){if(pk===it.v||SHOP_HIDE[pk].indexOf(it.v)>=0)lsSet('gbb_rv_'+pk,null);});}
  S.shopPeek=null;S.shopFocus=null;return true;
}
/* 관리자: 산 이모티콘 팩을 되돌려 다시 살 수 있게(숨은 팩 연출도 다시 나오게) */
function shopRevokeList(V){return shopItems().filter(function(x){return x.cat==='stk'&&!x.free&&shopOwns(V,x.id);}).map(function(x){return x.id;});}
function shopRevokeStk(V){
  var ids=shopRevokeList(V);if(!ids.length)return 0;
  editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);ids.forEach(function(k){delete sh.own[k];});});
  if(WALH.revoke)WALH.revoke(ids);
  Object.keys(SHOP_HIDE).forEach(function(pk){lsSet('gbb_rv_'+pk,null);});
  if(ids.indexOf('k:'+S.stkPack)>=0)S.stkPack='basic';
  S.shopPeek=null;S.shopFocus=null;
  return ids.length;
}
/* 다른 방과 잉크 같이 쓰기(웹 판): 연동 코드를 만들어 다른 방에서 넣는다 */
function walPanel(V,ink){
  var names=Object.keys(obj(WAL.rm)).map(function(k){return String(obj(WAL.rm[k]).n||'');}).filter(Boolean);
  var b='<div class="gift wlink" id="walLink"><h3>다른 방과 잉크 같이 쓰기</h3><p class="hint">한 방에서 연동 코드를 만들고, 다른 방 상점에서 그 코드를 넣으면 두 방의 잉크와 산 것이 합쳐집니다. 코드를 아는 사람만 연동할 수 있습니다.</p>';
  if(names.length)b+='<p class="wlrooms"><small>같이 쓰는 방</small>'+names.map(function(n){return '<span class="tag">'+esc(n)+'</span>';}).join('')+'</p>';
  b+=S.walCode?'<div class="wlcode"><b id="walCodeT">'+esc(S.walCode)+'</b><button class="btn small" data-act="wal-copy">복사</button></div><p class="hint">이 코드는 지금만 보입니다. 다시 만들면 예전 코드는 쓸 수 없습니다.</p>':'<div class="row"><button class="btn small" data-act="wal-code">연동 코드 만들기</button></div>';
  b+='<div class="admrow"><input type="text" id="walLinkIn" data-draft="walLink" data-enter="wal-link" maxlength="9" autocomplete="off" autocapitalize="characters" placeholder="다른 방에서 만든 코드" aria-label="연동 코드"><button class="btn small primary" data-act="wal-link">연동</button></div>';
  if(names.length>1)b+='<button class="del" data-act="wal-unlink">'+(S.confirm==='walun'?'한 번 더 누르면 이 방만 떼어 냅니다':'이 방만 떼어 내기')+'</button>';
  return b+'</div>';
}
/* 잉크 선물: 받는 사람, 얼마, 한마디 */
function giftPanel(V,ink){
  var to=S.giftTo&&V.byId[S.giftTo]&&S.giftTo!==V.me?S.giftTo:'',n=Math.floor(+S.draft.giftN||0),others=V.roster.filter(function(m){return m.id!==V.me;});
  var b='<div class="gift" id="giftPanel"><h3>잉크 선물하기</h3>';
  if(!others.length)return b+'<p class="hint">이 방에 선물할 사람이 없습니다.</p></div>';
  b+='<div class="chips" role="group" aria-label="받는 사람">'+others.map(function(m){return '<button class="chip" data-act="gift-to" data-id="'+esc(m.id)+'" aria-pressed="'+(to===m.id?'true':'false')+'">'+esc(m.name)+'</button>';}).join('')+'</div>';
  b+='<div class="chips gfamt" role="group" aria-label="보낼 잉크">'+GIFT_AMTS.map(function(a){return '<button class="chip" data-act="gift-amt" data-v="'+a+'" aria-pressed="'+(n===a?'true':'false')+'"'+(!ink.unl&&a>ink.bal?' disabled':'')+'>'+inkTag(a)+'</button>';}).join('')+'<input type="number" inputmode="numeric" min="1" id="giftN" data-draft="giftN" data-live="1" placeholder="직접" aria-label="보낼 잉크 직접 적기"></div>';
  b+='<input type="text" id="giftMsg" data-draft="giftMsg" maxlength="60" placeholder="한마디 (없어도 됩니다)" aria-label="선물과 함께 보낼 말">';
  var ok=to&&n>0&&(ink.unl||n<=ink.bal)&&n<=99999,cf=S.confirm==='gift';
  b+='<div class="row"><button class="btn primary" data-act="gift-send"'+(ok?'':' disabled')+'>'+(ok?(cf?'한 번 더 누르면 보냅니다':esc(V.byId[to].name)+' 님에게 '+n+'방울 보내기'):(n>0&&!ink.unl&&n>ink.bal?'잉크가 모자랍니다':'받는 사람과 잉크를 고르세요'))+'</button></div>';
  return b+'<p class="hint">보낸 잉크는 받는 사람의 잉크가 되고, 1:1 메시지로 알려 줍니다.</p></div>';
}
/* 설정 화면: 안 산 것은 자물쇠와 값, 누르면 상점으로 */
function shopLock(V,id){var it=shopItem(id);return it&&!shopOwns(V,id)?it:null;}
function shopLockTag(it){return '<em class="lkp">'+inkTag(it.price)+'</em>';}
/* 숨은 팩이 열릴 때: 어두운 막 위로 금빛 선이 원을 그리고, 봉인된 카드가 빛을 한 번 받은 뒤 뒤집혀 이모티콘 넷이 차례로 드러난다.
   상점을 보고 있을 때(사자마자, 또는 다른 방에서 사서 상점을 열었을 때) 이 기기에서 한 번만 */
var STK_RV=null;
function stkRevealTick(){
  if(STK_RV||!S.ready||!S.modal||S.modal.type!=='shop')return;
  var V=view();if(!V||!V.me)return;
  Object.keys(SHOP_HIDE).some(function(pk){
    var id='k:'+pk;
    // 본 시각을 적어 두고, 관리자가 그 뒤에 되돌렸으면(지갑 rk) 다른 기기에서도 다시 보인다
    var seen=+lsGet('gbb_rv_'+pk)||0,rk=obj(WAL.on?WAL.rk:null);
    if(seen&&[pk].concat(SHOP_HIDE[pk]).some(function(p){return +rk['k:'+p]>seen;}))seen=0;
    if(SHOP_HIDE[pk].every(function(p){return shopOwns(V,'k:'+p);})&&!shopOwns(V,id)&&!seen){lsSet('gbb_rv_'+pk,String(Date.now()));stkReveal(pk);return true;}
    return false;
  });
}
function stkReveal(pk){
  var it=shopItem('k:'+pk);if(!it||STK_RV)return;
  var ids=STK.filter(function(x){return x[0].indexOf(pk+'-')===0;}),pick=[0,5,8,11].map(function(i){return ids[i]||ids[0];});
  var red=false;try{red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  var motes='';for(var i=0;i<18;i++)motes+='<i style="--x:'+(4+Math.random()*92).toFixed(1)+'%;--d:'+(Math.random()*3).toFixed(2)+'s;--t:'+(5+Math.random()*4).toFixed(2)+'s;--s:'+(1.5+Math.random()*2.5).toFixed(1)+'px"></i>';
  var el=document.createElement('div');
  el.className='rv2'+(red?' calm':'');el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');el.setAttribute('aria-label','비밀 팩이 열렸습니다. '+it.name);
  el.innerHTML='<div class="rv2bg"></div><div class="rv2motes" aria-hidden="true">'+motes+'</div>'+
    '<div class="rv2stage" aria-hidden="true"><svg class="rv2ring" viewBox="0 0 200 200"><circle cx="100" cy="100" r="92"/><circle class="in" cx="100" cy="100" r="84"/></svg>'+
    '<div class="rv2card"><div class="rv2face rv2front"><span class="rv2seal">'+INK_SVG+'</span><small>SECRET</small></div><div class="rv2face rv2back">'+pick.map(function(x,n){return '<span class="rv2s" style="--n:'+n+'">'+stkImg(x[0])+'</span>';}).join('')+'</div><i class="rv2sheen"></i></div></div>'+
    '<div class="rv2txt"><small>비밀 팩 해금</small><h2>'+esc(it.name)+'</h2><p>'+esc(it.desc)+'</p><div class="rvbtns"><button class="btn primary" data-rv="go">보러 가기</button><button class="btn" data-rv="x">닫기</button></div></div>';
  document.body.appendChild(el);STK_RV=el;
  function done(go){
    if(!el.parentNode||el.classList.contains('out'))return;
    el.classList.add('out');window.removeEventListener('keydown',key,true);
    setTimeout(function(){if(el.parentNode)el.parentNode.removeChild(el);STK_RV=null;},520);
    if(go){S.shopCat='stk';S.shopFocus='k:'+pk;S.shopPeek='k:'+pk;render();setTimeout(function(){var c=document.getElementById('shi-k-'+pk);if(c&&c.scrollIntoView)c.scrollIntoView({block:'start',behavior:red?'auto':'smooth'});},60);}
  }
  function key(e){if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();done(false);}}
  window.addEventListener('keydown',key,true);
  el.addEventListener('click',function(e){var b=e.target.closest?e.target.closest('[data-rv]'):null;if(!b)return;e.preventDefault();e.stopPropagation();done(b.getAttribute('data-rv')==='go');});
  if(!red)setTimeout(function(){try{if(navigator.vibrate)navigator.vibrate(12);}catch(e){}},2300);
  setTimeout(function(){var b=el.querySelector('[data-rv="go"]');if(b&&el.parentNode)try{b.focus({preventScroll:true});}catch(e){}},red?300:3200);
}
