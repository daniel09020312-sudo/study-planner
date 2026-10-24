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
# 움직이는 이모티콘: 아이폰(Safari)은 움직이는 webp를 아주 느리게 돌리므로, 장면을 옆으로 이어 붙인 한 장(STK의 4번째 값=장면마다 ms)을
# object-fit:cover로 한 칸만 보이게 하고 object-position을 장면 시간대로 옮긴다(@keyframes는 처음 쓸 때 만든다)
sub(""" decoding="async">':'';}""", """ decoding="async"'+stkSa(x)+'>':'';}
var STK_SA={},STK_SAN=0;
function stkSa(x){
  var f=x&&x[3];if(!f||!f.length)return '';
  var key=f.join('_'),a=STK_SA[key];
  if(!a){
    var n=f.length,tot=0,t=0,kf='';f.forEach(function(v){tot+=+v||0;});if(!tot)return '';
    for(var i=0;i<n;i++){kf+=(Math.round(t/tot*10000)/100)+'%{object-position:'+(n>1?Math.round(i/(n-1)*10000)/100:0)+'% 0}';t+=+f[i]||0;}
    a=STK_SA[key]={nm:'stkSa'+(STK_SAN++),d:tot};
    try{var st=document.createElement('style');st.textContent='@keyframes '+a.nm+'{'+kf+'100%{object-position:100% 0}}';document.head.appendChild(st);}catch(e){}
  }
  return ' class="sa" style="animation:'+a.nm+' '+a.d+'ms step-end infinite"';
}""")
# 숨은 팩이 열리는 순간 연출(stkReveal): 사자마자, 그리고 상점을 볼 때 매초 확인
sub("+(sbi.cat==='stk'?' 메시지의 이모티콘에서 쓸 수 있습니다.':' 바로 바꿨습니다.'));break;",
    "+(sbi.cat==='stk'?' 메시지의 이모티콘에서 쓸 수 있습니다.':' 바로 바꿨습니다.'));setTimeout(stkRevealTick,500);break;")
sub("  try{humMig();}catch(e){}\n", "  try{humMig();}catch(e){}\n  try{stkRevealTick();}catch(e){}\n")
