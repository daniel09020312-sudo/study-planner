# ---------------------------------------------------------------- v34: 상점 (src/shop.js), 메시지는 가장 최근 대화로
SHOP_JS = open(BASE + '/src/shop.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", SHOP_JS + "\n/* ---------- 공부방 ---------- */")

# 1) 왼쪽(아래) 줄: 설정 바로 위에 상점
sub('    <button class="mebtn" id="meBtn" data-act="open" data-modal="settings" aria-label="설정 열기"></button>',
    '    <button class="shopbtn" id="shopBtn" data-act="open" data-modal="shop" aria-label="상점 열기"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.5 8.5h13l-1 11a1.5 1.5 0 0 1-1.5 1.4H8a1.5 1.5 0 0 1-1.5-1.4z"/><path d="M9 10.5V7a3 3 0 0 1 6 0v3.5"/></svg><span>상점</span></button>\n'
    '    <button class="mebtn" id="meBtn" data-act="open" data-modal="settings" aria-label="설정 열기"></button>')

# 2) 창
sub("function openModal(type,el){\n  var V=view();S.ttPend=null;",
    "function shopGo(id){var it=shopItem(id);S.shopNext=it?{cat:it.cat,focus:it.id}:null;openModal('shop',null);}\n"
    "function openModal(type,el){\n  var V=view();S.ttPend=null;\n"
    "  if(type==='shop'){var snx=S.shopNext;S.shopNext=null;S.shopCat=snx?snx.cat:(S.shopCat||'look');S.shopFocus=snx?snx.focus:null;S.shopPeek=snx&&snx.cat==='stk'?snx.focus:null;}")
sub("  if(t==='settings')return modalSettings(V);", "  if(t==='settings')return modalSettings(V);\n  if(t==='shop')return modalShop(V);")

# 3) 동작
sub("    case 'stk-send':{", r"""    case 'shop-cat':S.shopCat=el.getAttribute('data-v')||'look';S.shopFocus=null;S.shopPeek=null;break;
    case 'shop-peek':S.shopPeek=S.shopPeek===id?null:id;break;
    case 'shop-open':shopGo(el.getAttribute('data-v'));return;
    case 'shop-use':{var Vsu=view();if(shopOwns(Vsu,id)){shopUse(id);var siu=shopItem(id);flash(roJ(siu.name)+' 바꿨습니다.');}break;}
    case 'shop-buy':{
      var Vsb=view(),sbi=shopItem(id);if(!sbi||!Vsb.me||shopOwns(Vsb,id)||!need())break;
      var sbk=inkOf(Vsb);if(sbk.bal<sbi.price){flash('잉크가 '+(sbi.price-sbk.bal)+'방울 모자랍니다.');break;}
      if(prev!=='buy:'+id){S.confirm='buy:'+id;break;}
      editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);sh.own[id]=sbi.price;});
      if(!canWrite())break;
      shopUse(id);S.shopFocus=id;flash(jos(sbi.name,'을','를')+' 샀습니다. 잉크 '+sbi.price+'방울을 썼습니다.'+(sbi.cat==='stk'?' 메시지의 이모티콘에서 쓸 수 있습니다.':' 바로 바꿨습니다.'));break;
    }
    case 'stk-send':{""")
sub("      if(!Vk2.me||!STK_BY[id]||", "      if(!Vk2.me||!STK_BY[id]||!shopOwns(Vk2,'k:'+String(id).split('-')[0])||")
sub("    case 'accent':lsSet('gbb_accent',el.getAttribute('data-v'));applyLook();break;",
    "    case 'accent':{var acv=el.getAttribute('data-v');if(!shopOwns(view(),'a:'+acv)){shopGo('a:'+acv);return;}lsSet('gbb_accent',acv);applyLook();break;}")
sub("    case 'concept':lsSet('gbb_concept',el.getAttribute('data-v'));applyLook();break;",
    "    case 'concept':{var cov=el.getAttribute('data-v');if(!shopOwns(view(),'c:'+cov)){shopGo('c:'+cov);return;}lsSet('gbb_concept',cov);applyLook();break;}")
sub("    case 'tstyle':{var tsv=el.getAttribute('data-v');if(TSTYLES.some(function(x){return x[0]===tsv;})){",
    "    case 'tstyle':{var tsv=el.getAttribute('data-v');if(!shopOwns(view(),'t:'+tsv)){shopGo('t:'+tsv);return;}if(TSTYLES.some(function(x){return x[0]===tsv;})){")

# 4) 설정 > 화면: 안 산 것은 자물쇠와 값, 누르면 상점
sub("""'<button class="cv" data-act="concept" data-v="'+x.id+'" aria-pressed="'+(cNow.id===x.id?'true':'false')+'"><span class="cvp cvp-'+x.id+'" aria-hidden="true"><i></i><i></i><i></i></span><span>'+x.name+'</span></button>'""",
    """(function(lk){return '<button class="cv'+(lk?' lk':'')+'" data-act="'+(lk?'shop-open':'concept')+'" data-v="'+(lk?'c:':'')+x.id+'" aria-pressed="'+(cNow.id===x.id?'true':'false')+'"'+(lk?' aria-label="'+esc(x.name)+', 상점에서 잉크 '+lk.price+'방울"':'')+'><span class="cvp cvp-'+x.id+'" aria-hidden="true"><i></i><i></i><i></i></span><span>'+x.name+'</span>'+(lk?shopLockTag(lk):'')+'</button>';})(shopLock(V,'c:'+x.id))""")
sub("""return '<button class="sw" data-act="accent" data-v="'+x.id+'" style="--a:'+x.l.a+';--b:'+x.d.a+'" aria-pressed="'+(acNow===x.id?'true':'false')+'" aria-label="대표 색 '+x.name+'" title="'+x.name+'"></button>';""",
    """var lk=shopLock(V,'a:'+x.id);return '<button class="sw'+(lk?' lk':'')+'" data-act="'+(lk?'shop-open':'accent')+'" data-v="'+(lk?'a:':'')+x.id+'" style="--a:'+x.l.a+';--b:'+x.d.a+'" aria-pressed="'+(acNow===x.id?'true':'false')+'" aria-label="대표 색 '+x.name+(lk?', 상점에서 잉크 '+lk.price+'방울':'')+'" title="'+x.name+'"></button>';""")
sub("""'<button class="cv" data-act="tstyle" data-v="'+x[0]+'" aria-pressed="'+(tstyle()===x[0]?'true':'false')+'"><span class="tsp tsp-'+x[0]+'" aria-hidden="true">'+TSPREV[x[0]]+'</span>'+x[1]+'</button>'""",
    """(function(lk){return '<button class="cv'+(lk?' lk':'')+'" data-act="'+(lk?'shop-open':'tstyle')+'" data-v="'+(lk?'t:':'')+x[0]+'" aria-pressed="'+(tstyle()===x[0]?'true':'false')+'"><span class="tsp tsp-'+x[0]+'" aria-hidden="true">'+TSPREV[x[0]]+'</span>'+x[1]+(lk?shopLockTag(lk):'')+'</button>';})(shopLock(V,'t:'+x[0]))""")
sub("""  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3>""",
    """  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3><div class="shrow"><span>'+INK_SVG+'자물쇠가 있는 것은 상점에서 잉크로 삽니다</span><button class="btn small" data-act="open" data-modal="shop">상점</button></div>""")

# 5) 메시지 이모티콘: 안 산 팩은 미리 보기와 상점 안내
sub("""STK_PACKS.map(function(p){return '<button data-act="stk-pack" data-id="'+p[0]+'" aria-pressed="'+(S.stkPack===p[0]?'true':'false')+'">'+p[1]+'</button>';}).join('')+'</div><div class="stkgrid" id="stg-'+esc(S.stkPack)+'">';""",
    """STK_PACKS.map(function(p){var plk=!shopOwns(V,'k:'+p[0]);return '<button data-act="stk-pack" data-id="'+p[0]+'" aria-pressed="'+(S.stkPack===p[0]?'true':'false')+'">'+(plk?'<svg class="lki" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg>':'')+p[1]+'</button>';}).join('')+'</div>'+(shopOwns(V,'k:'+S.stkPack)?'':(function(it){return '<div class="stklock"><span>'+esc(it.name)+'은 상점에서 잉크 '+it.price+'방울에 살 수 있습니다. 아래는 미리 보기입니다.</span><button class="btn small primary" data-act="shop-open" data-v="'+esc(it.id)+'">상점에서 보기</button></div>';})(shopItem('k:'+S.stkPack)))+'<div class="stkgrid'+(shopOwns(V,'k:'+S.stkPack)?'':' lockd')+'" id="stg-'+esc(S.stkPack)+'">';""")
sub("""    STK.forEach(function(x){if(x[0].indexOf(S.stkPack+'-')===0)h+='<button class="stkbtn" data-act="stk-send" data-id="'+x[0]+'" data-chan="'+esc(c)+'" aria-label="'+esc(x[1])+' 이모티콘 보내기">'+stkImg(x[0])+'</button>';});""",
    """    var stOwn=shopOwns(V,'k:'+S.stkPack);
    STK.forEach(function(x){if(x[0].indexOf(S.stkPack+'-')===0)h+=stOwn?'<button class="stkbtn" data-act="stk-send" data-id="'+x[0]+'" data-chan="'+esc(c)+'" aria-label="'+esc(x[1])+' 이모티콘 보내기">'+stkImg(x[0])+'</button>':'<span class="stkbtn stk" data-m="'+esc(x[2])+'" title="'+esc(x[1])+'">'+stkImg(x[0])+'</span>';});""")

# 6) 처음 한 번: 쓰던 모양은 그냥 주기
sub("  try{humMig();}catch(e){}\n", "  try{humMig();}catch(e){}\n  try{shopGf();}catch(e){}\n")

# 7) 메시지 탭에 들어오면 가장 최근 대화로 (다시 들어와 목록이 새로 그려졌을 때도, 이모티콘 그림이 늦게 떠도)
sub("    if(ml&&S.chatKey!==key){S.chatKey=key;ml.scrollTop=ml.scrollHeight;}",
    "    if(ml&&(S.chatKey!==key||!ml.__sc)){S.chatKey=key;ml.__sc=1;ml.scrollTop=ml.scrollHeight;[].forEach.call(ml.querySelectorAll('img'),function(im){if(!im.complete)im.addEventListener('load',function(){if(ml.scrollHeight-ml.scrollTop-ml.clientHeight<320)ml.scrollTop=ml.scrollHeight;},{once:true});});}")
