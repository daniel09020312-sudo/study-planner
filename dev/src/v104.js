/* ---------- v104: 기존 꾸미기(방 꾸미기·대표 색·타이머)에도 히든 상품. 조건을 채워야 상점에 보이고 살 수 있음 ---------- */
CONCEPTS.push(
  {id:'aurora',name:'오로라',mode:'dark',soft:[.2,'#10243A'],hid:1},
  {id:'library',name:'밤의 도서관',mode:'dark',soft:[.2,'#2A2019'],font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700,hid:1},
  {id:'ocean',name:'깊은 바다',mode:'dark',soft:[.2,'#0A2233'],hid:1},
  {id:'royal',name:'황금 서재',mode:'light',soft:[.25,'#F3E6C4'],font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700,hid:1}
);
ACCENTS.push(
  {id:'hgold',name:'금',g:'h',l:{a:'#B8860B',on:'#FFFFFF',soft:'#FBF1D6',ink:'#946C08',mark:'#B8860B'},d:{a:'#E8C259',on:'#2A1E00',soft:'#3A2F12',ink:'#E8C259',mark:'#E8C259'}},
  {id:'hneon',name:'네온 핑크',g:'h',l:{a:'#E0168A',on:'#FFFFFF',soft:'#FDE4F2',ink:'#C21277',mark:'#E0168A'},d:{a:'#FF4FB8',on:'#2A0019',soft:'#3D1530',ink:'#FF4FB8',mark:'#FF4FB8'}},
  {id:'hink',name:'먹',g:'h',l:{a:'#1C1C1E',on:'#FFFFFF',soft:'#ECECEE',ink:'#1C1C1E',mark:'#1C1C1E'},d:{a:'#E8E8EA',on:'#111113',soft:'#2A2A2E',ink:'#E8E8EA',mark:'#E8E8EA'}}
);
/* 타이머 변형: 바탕 모양(TVAR)을 그대로 그리고 색만 바꿈 */
var TVAR={neon:'ring',aurora:'orbit',goldan:'analog',pixel:'digits'};
TSTYLES.push(['neon','네온 링'],['aurora','오로라 고리'],['goldan','황금 시계'],['pixel','픽셀 숫자']);
for(var tv in TVAR)TSPREV[tv]=TSPREV[TVAR[tv]];
SHOP_LOOK.aurora=[150,'초록과 보라 빛이 흐르는 밤'];SHOP_LOOK.library=[150,'나무 책장과 따뜻한 등불'];SHOP_LOOK.ocean=[150,'빛이 내려오는 깊은 바다'];SHOP_LOOK.royal=[150,'크림색 종이와 금빛 테두리'];
SHOP_TIMER.neon=[80,'빛나는 네온 고리'];SHOP_TIMER.aurora=[100,'두 겹 고리에 오로라 빛'];SHOP_TIMER.goldan=[100,'금빛 아날로그 시계'];SHOP_TIMER.pixel=[80,'오래된 게임기 같은 초록 숫자'];
/* id: [조건 글, 조건 함수, 값(색은 따로)] */
var HID_EXTRA={
  'c:aurora':['누적 공부 60시간',function(s){return s.mins>=3600;}],
  'c:library':['14일 연속 출석',function(s){return s.maxStreak>=14;}],
  'c:ocean':['1:1 대결 3승',function(s){return s.duelWins>=3;}],
  'c:royal':['배지 8개 모으기',function(s,V){return badgeList(V,V.me).filter(function(b){return b.on;}).length>=8;}],
  'a:hgold':['하루 1등 6번',function(s){return s.dayWins>=6;},40],
  'a:hneon':['아침 7시 전 출석 15번',function(s){return s.early>=15;},40],
  'a:hink':['문제 10개 올리기',function(s){return s.posts>=10;},40],
  't:neon':['하루 10시간 넘게 공부',function(s){return s.d10>=1;}],
  't:aurora':['빙고 5줄',function(s){return s.lines>=5;}],
  't:goldan':['완벽한 한 주',function(s){return s.perfect>=1;}],
  't:pixel':['모두 끝내고 인증 14일',function(s){return s.clrCert>=14;}]
};
function hidExtraMark(a){a.forEach(function(x){var h=HID_EXTRA[x.id];if(!h)return;x.hid=h[0];x.cond=h[1];x.free=false;if(h[2])x.price=h[2];x.desc=x.desc.replace(/, 무료$/,'');});}
function faceHtml(st,mid,o,f){var b=TVAR[st];if(!b)return faceHtml0(st,mid,o,f);return faceHtml0(b,mid,o,f).replace('<div class="tf ','<div class="tf tv-'+st+' ');}
function hidCatName(cat){return {ring:'테두리',ttag:'칭호 장식',look:'방 꾸미기',color:'대표 색',timer:'타이머'}[cat]||'상품';}
try{applyLook();}catch(e){}
function decoHidCount(V,cat){var l=shopItems().filter(function(x){return x.hid&&x.cat===cat;});return [l.filter(function(x){return shopShown(V,x.id);}).length,l.length];}
/* 열린 히든은 조건을 계속 보여 주고, 방장은 조건과 상관없이 모든 히든을 볼 수 있고 살 수 있음 */
function hidAdm(V){return !!(V&&V.me&&adminId(V)===V.me);}
function shopShown(V,id){var it=shopItem(id);if(it&&it.hid)return shopOwns(V,id)||hidAdm(V)||decoOk(V,it);return shopShown0(V,id);}
function hidLine(V,it){if(!it.hid)return '';var met=decoOk(V,it);return '<small class="hidc'+(met?' met':'')+'">히든 · 조건: '+esc(it.hid)+(met?' (채움)':hidAdm(V)?' (방장이라 열림)':'')+'</small>';}
