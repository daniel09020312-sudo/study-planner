# ---------------------------------------------------------------- v35: 잉크 선물, 관리자 무제한(웹 판 지갑은 web_wallet_part.py)
# 선물 기록은 방 기록 gifts/<id> = {from, to, n, at}, 받는 사람에게 1:1 메시지 {gift:n}로 알린다
sub("var COLLS=['subjects','days','progress','quiz','events','live','replies','msgs','songs','duels','spins','locks','flags','plans'];",
    "var COLLS=['subjects','days','progress','quiz','events','live','replies','msgs','songs','duels','spins','locks','flags','plans','gifts'];")
sub("plans:merged('plans'),", "plans:merged('plans'),gifts:merged('gifts'),")
sub("S.plans={};", "S.plans={};S.gifts={};")

# 사기: 관리자는 0방울, 지갑에도 적기
sub("editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);sh.own[id]=sbi.price;});",
    "var sbp=sbk.unl?0:sbi.price;editProg(function(p){var sh=p.shop=obj(p.shop);sh.own=obj(sh.own);sh.own[id]=sbp;});if(canWrite()&&WALH.buy)WALH.buy(id,sbp);")
sub("flash(jos(sbi.name,'을','를')+' 샀습니다. 잉크 '+sbi.price+'방울을 썼습니다.'",
    "flash(jos(sbi.name,'을','를')+' 샀습니다.'+(sbk.unl?'':' 잉크 '+sbi.price+'방울을 썼습니다.')")

# 선물, 관리자 코드 동작
sub("    case 'shop-cat':", r"""    case 'gift-open':S.giftOpen=!S.giftOpen;S.giftTo=null;S.draft.giftN='';S.draft.giftMsg='';S.sync=true;break;
    case 'gift-to':S.giftTo=id;break;
    case 'gift-amt':S.draft.giftN=String(+el.getAttribute('data-v')||'');S.sync=true;break;
    case 'gift-send':{
      var Vgf=view(),gto=S.giftTo,gn=Math.floor(+S.draft.giftN||0),gk=inkOf(Vgf);
      if(!Vgf.me||!gto||gto===Vgf.me||!Vgf.byId[gto]||!(gn>0)||gn>99999||!need())break;
      if(!gk.unl&&gn>gk.bal){flash('잉크가 '+(gn-gk.bal)+'방울 모자랍니다.');break;}
      if(prev!=='gift'){S.confirm='gift';break;}
      var gat=Date.now(),gmsg=String(S.draft.giftMsg||'').trim().slice(0,60);
      save('gifts/'+rid('g'),{from:Vgf.me,to:gto,n:gn,at:gat});
      save('msgs/'+rid('x'),{from:Vgf.me,to:gto,text:gmsg,gift:gn,at:gat});
      if(!canWrite())break;
      S.giftOpen=false;S.giftTo=null;S.draft.giftN='';S.draft.giftMsg='';S.sync=true;
      flash(Vgf.byId[gto].name+' 님에게 잉크 '+gn+'방울을 선물했습니다.');break;
    }
    case 'adm-open':S.admOpen=true;S.focusAfter='admCode';break;
    case 'adm-go':{var acd=String(S.draft.admCode||'').trim();S.draft.admCode='';S.sync=true;if(acd&&WALH.adm)WALH.adm(acd);break;}
    case 'shop-cat':""")
sub("  if(type==='shop'){var snx=S.shopNext;", "  if(type==='shop'){S.giftOpen=false;S.admOpen=false;S.draft.admCode='';}\n  if(type==='shop'){var snx=S.shopNext;")

# 메시지: 선물 말풍선, 미리 보기 글
sub("    if(x.stk)body='<span class=\"stk\"", "    if(x.gift)body='<div class=\"bb gift\"'+pick+'><span class=\"gfi\">'+INK_SVG+'<b>잉크 '+(+x.gift||0)+'방울</b> 선물</span>'+(x.text?'<span class=\"gft\">'+esc(x.text)+'</span>':'')+'</div>';\n    else if(x.stk)body='<span class=\"stk\"")
sub("(x.stk?'':'<button class=\"btn small\" data-act=\"msg-edit\"", "(x.stk||x.gift?'':'<button class=\"btn small\" data-act=\"msg-edit\"")
sub("function msgPreview(x){\n  if(x.poke)return '찌르기';", "function msgPreview(x){\n  if(x.poke)return '찌르기';\n  if(x.gift)return '잉크 '+(+x.gift||0)+'방울 선물'+(x.text?', '+cut(x.text,14):'');")
