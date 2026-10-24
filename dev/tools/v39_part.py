# v39: 움직이는 이모티콘 팩(까만 고양이, 하얀 강아지, 냥댕이). 냥댕이는 앞의 두 팩을 모두 사야 보이고 살 수 있다(SHOP_HIDE)
# 메시지 이모티콘 고르기: 숨은 팩은 '비밀' 탭에 물음표만, 그림은 불러오지 않는다
sub("+p[1]+'</button>';}).join('')+'</div>'+(shopOwns(V,'k:'+S.stkPack)?'':(function(it){",
    "+(stkHid(V,p[0])?'비밀':p[1])+'</button>';}).join('')+'</div>'+(shopOwns(V,'k:'+S.stkPack)?'':stkHid(V,S.stkPack)?'<div class=\"stklock\"><span>비밀 팩입니다. '+esc(stkHidNote(S.stkPack))+'</span><button class=\"btn small primary\" data-act=\"shop-open\" data-v=\"k:'+esc(S.stkPack)+'\">상점에서 보기</button></div>':(function(it){")
sub("    var stOwn=shopOwns(V,'k:'+S.stkPack);\n    STK.forEach(function(x){if(x[0].indexOf(S.stkPack+'-')===0)h+=stOwn?",
    "    var stOwn=shopOwns(V,'k:'+S.stkPack),stHid=stkHid(V,S.stkPack);\n    STK.forEach(function(x){if(x[0].indexOf(S.stkPack+'-')===0)h+=stHid?'<span class=\"stkbtn stkq\" aria-hidden=\"true\">?</span>':stOwn?")
# 사기: 숨은 팩은 열리기 전에 살 수 없다
sub("if(!sbi||!Vsb.me||shopOwns(Vsb,id)||!need())break;", "if(!sbi||!Vsb.me||shopOwns(Vsb,id)||!shopShown(Vsb,id)||!need())break;")
# 묶음 탭이 넘치면 옆으로 밀고, 고른 탭이 보이게
sub("    if(ml&&(S.chatKey!==key||!ml.__sc)){",
    "    var sps=document.querySelector('.stkpick .seg');if(sps&&sps.__pk!==S.stkPack){sps.__pk=S.stkPack;var spb=sps.querySelector('[aria-pressed=\"true\"]');if(spb){var spa=spb.getBoundingClientRect(),spr=sps.getBoundingClientRect();if(spa.left<spr.left||spa.right>spr.right)sps.scrollLeft+=spa.left-spr.left-(spr.width-spa.width)/2;}}\n    if(ml&&(S.chatKey!==key||!ml.__sc)){")
