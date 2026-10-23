/* ---------- 상점: 공부 10분마다 잉크 한 방울, 잉크로 모양만 바꾸는 것을 산다 ---------- */
// 잉크는 이 방에서 공부한 시간(타이머 + 직접 넣은 시간은 하루 RULE.manualMax까지)으로 계산하고, 산 것만 progress.shop.own[물건]=값 으로 적는다.
// 남은 잉크 = 모은 잉크 - 산 값의 합. 상점이 생기기 전에 이 기기에서 쓰던 컨셉, 대표 색, 타이머 모양은 처음 한 번 그냥 준다(shop.gf).
// 이모티콘은 기본만 처음부터 쓰고, 장난과 감정은 팩으로 산다. 모양은 이 기기에 저장되고(예전과 같음), 산 것만 고를 수 있다.
var INK_MIN=10;
var SHOP_CATS=[['look','방 꾸미기'],['color','대표 색'],['timer','타이머'],['stk','이모티콘']];
var SHOP_LOOK={grid:[150,'공책 모눈 위에 손글씨'],board:[200,'초록 칠판과 분필 글씨'],pop:[150,'동글동글 말랑한 버튼'],line:[100,'얇은 검은 선으로 또렷하게'],glass:[200,'뒤가 비치는 유리 카드'],night:[250,'별이 뜬 밤하늘']};
var SHOP_TIMER={digits:[60,'큰 숫자만 깔끔하게'],bar:[60,'숫자 아래 줄어드는 막대'],pie:[80,'시간이 줄어드는 원판'],flip:[100,'넘어가는 넘김 시계']};
var SHOP_STK={playful:[120,'어쩔~, 메롱, 뇌 정지 같은 장난'],emotions:[120,'신난다!, 부끄러워, 감동이야 같은 마음']};
var INK_SVG='<svg class="inkd" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8c3.2 4 6.2 7.6 6.2 11.2a6.2 6.2 0 0 1-12.4 0c0-3.6 3-7.2 6.2-11.2z"/><path class="hl" d="M9.4 14.6a2.8 2.8 0 0 0 2.4 2.7"/></svg>';
var SHOP_GF=false;
function shopItems(){
  if(shopItems.c)return shopItems.c;var a=[];
  CONCEPTS.forEach(function(x){var m=SHOP_LOOK[x.id];a.push({id:'c:'+x.id,v:x.id,cat:'look',name:x.name,price:m?m[0]:0,desc:m?m[1]:'처음 모양',free:x.id==='basic'});});
  ACCENTS.forEach(function(x){a.push({id:'a:'+x.id,v:x.id,cat:'color',name:x.name,price:x.g==='p'?50:40,desc:x.g==='p'?'파스텔':'대표 색',free:x.id==='blue',ac:x});});
  TSTYLES.forEach(function(x){var m=SHOP_TIMER[x[0]];a.push({id:'t:'+x[0],v:x[0],cat:'timer',name:x[1],price:m?m[0]:0,desc:m?m[1]:'처음 모양',free:x[0]==='ring'});});
  STK_PACKS.forEach(function(x){var m=SHOP_STK[x[0]];a.push({id:'k:'+x[0],v:x[0],cat:'stk',name:x[1]+' 팩',price:m?m[0]:120,desc:m?m[1]:(x[0]==='basic'?'처음부터 쓰는 이모티콘':'새 이모티콘'),free:x[0]==='basic'});});
  return shopItems.c=a;
}
function shopItem(id){return shopItems().filter(function(x){return x.id===id;})[0]||null;}
function shopOwn(V){return obj(obj(obj(V.progress[V.me]).shop).own);}
function shopOwns(V,id){var it=shopItem(id);if(!it)return false;if(it.free)return true;return V&&V.me?shopOwn(V)[id]!=null:false;}
function inkMins(V,mid,date){
  var pre=mid+'_',m=0;
  Object.keys(V.days).forEach(function(k){if(k.indexOf(pre)!==0)return;if(date&&k!==pre+date)return;var d=obj(V.days[k]);m+=sumMins(d.mins)+Math.min(sumMins(d.manual),RULE.manualMax);});
  return m;
}
function inkOf(V){
  if(!V||!V.me)return {got:0,spent:0,bal:0,today:0};
  if(V._ink)return V._ink;
  var got=Math.floor(inkMins(V,V.me)/INK_MIN),own=shopOwn(V),spent=0;
  Object.keys(own).forEach(function(k){spent+=Math.max(0,+own[k]||0);});
  return V._ink={got:got,spent:spent,bal:Math.max(0,got-spent),today:Math.floor(inkMins(V,V.me,today())/INK_MIN)};
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
  if(SHOP_GF)return;var V=view();
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
  var b='<div class="wallet"><div class="wl">'+INK_SVG+'<div><small>내 잉크</small><b>'+ink.bal+'<em>방울</em></b></div></div>';
  b+='<p class="wr">공부 10분마다 잉크 한 방울'+(ink.today?'<span class="wt">오늘 +'+ink.today+'</span>':'')+'<small>모은 잉크 '+ink.got+' · 쓴 잉크 '+ink.spent+'</small></p></div>';
  b+='<div class="seg mini shcats" style="--i:'+SHOP_CATS.map(function(x){return x[0];}).indexOf(cat)+';--n:'+SHOP_CATS.length+'" role="group" aria-label="상품 종류">'+SHOP_CATS.map(function(x){return '<button data-act="shop-cat" data-v="'+x[0]+'" aria-pressed="'+(cat===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  b+='<div class="shgrid'+(cat==='stk'?' wide':'')+'" id="shg-'+cat+'">';
  items.forEach(function(it){
    var foc=S.shopFocus===it.id,peek=cat==='stk'&&S.shopPeek===it.id;
    b+='<div class="shi'+(foc?' foc':'')+(shopOwns(V,it.id)?' own':'')+'" id="shi-'+esc(it.id.replace(':','-'))+'">'+shopPrev(it)+'<div class="shn"><b>'+esc(it.name)+'</b><small>'+esc(it.desc)+'</small></div><div class="sha">'+shopBtn(V,it,ink)+'</div>';
    if(cat==='stk'){
      b+='<button class="shpeek" data-act="shop-peek" data-id="'+esc(it.id)+'" aria-expanded="'+(peek?'true':'false')+'">'+(peek?'미리 보기 접기':'전체 미리 보기')+'</button>';
      if(peek)b+='<div class="shall">'+STK.filter(function(x){return x[0].indexOf(it.v+'-')===0;}).map(function(x){return '<span class="stk" data-m="'+esc(x[2])+'">'+stkImg(x[0])+'<small>'+esc(x[1])+'</small></span>';}).join('')+'</div>';
    }
    b+='</div>';
  });
  b+='</div><p class="hint" style="margin-top:14px">산 것은 이 방에서 계속 쓸 수 있습니다. 모양만 바뀌고 기능과 점수는 그대로입니다. 고른 모양은 이 기기에 저장됩니다.</p>';
  return dlg('wide',{id:'shop',t:'상점'},b);
}
/* 설정 화면: 안 산 것은 자물쇠와 값, 누르면 상점으로 */
function shopLock(V,id){var it=shopItem(id);return it&&!shopOwns(V,id)?it:null;}
function shopLockTag(it){return '<em class="lkp">'+inkTag(it.price)+'</em>';}
