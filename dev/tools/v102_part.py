# ---------------------------------------------------------------- v102: 노동요 들은 횟수 정리, 반 전체 목표 단계별 잉크, 상점 프로필 테두리·칭호 장식·히든 상품 (src/v102.js, v102.css)
V102_JS = open(BASE + '/src/v102.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V102_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", open(BASE + '/src/v102.css', encoding='utf-8').read() + "</style>")
# 링크로 듣기는 다녀온 시간으로 셈
sub("setTimeout(function(){songListen(id);render();},60)", "setTimeout(function(){songListen(id,true);render();},60)")
# 상점
sub("var SHOP_CATS=[['look','방 꾸미기'],['color','대표 색'],['timer','타이머'],['stk','이모티콘']];", "var SHOP_CATS=[['look','방 꾸미기'],['color','대표 색'],['timer','타이머'],['stk','이모티콘'],['ring','테두리'],['ttag','칭호']];")
sub("  return shopItems.c=a;", "  DECO_ITEMS.forEach(function(x){a.push(x);});\n  return shopItems.c=a;")
sub("function shopShown(V,id){var it=shopItem(id),req=", "function shopShown0(V,id){var it=shopItem(id),req=")
sub("    if(!shopShown(V,it.id)){", "    if(it.hid&&!shopShown(V,it.id)){b+=decoHidCard(V,it,foc);return;}\n    if(!shopShown(V,it.id)){")
sub("var fresh=SHOP_HIDE[it.v]&&!shopOwns(V,it.id);", "var fresh=(it.hid||SHOP_HIDE[it.v])&&!shopOwns(V,it.id);")
sub("b+='<div class=\"shgrid'+(cat==='stk'?' wide':'')+'\" id=\"shg-'+cat+'\">';", "if(cat==='ring'||cat==='ttag'){var dhc=decoHidCount(V,cat);b+='<p class=\"hint shdeco\">'+(cat==='ring'?'내 이름 동그라미에 두르는 테두리입니다.':'배지 칭호를 꾸밉니다.')+' 모든 사람에게 보입니다. 히든 '+dhc[0]+' / '+dhc[1]+' 열림</p>';}\n  b+='<div class=\"shgrid'+(cat==='stk'?' wide':'')+'\" id=\"shg-'+cat+'\">';")
sub("function shopPrev(it){\n", "function shopPrev(it){\n  if(it.cat==='ring'||it.cat==='ttag')return decoPrev(it);\n")
sub("function shopInUse(id){\n  var it=shopItem(id);if(!it)return false;\n", "function shopInUse(id){\n  var it=shopItem(id);if(!it)return false;\n  if(it.cat==='ring'||it.cat==='ttag'){var dv=view(),dd=obj(obj(dv.progress[dv.me]).deco),cur=(it.cat==='ring'?dd.r:dd.g)||'none';return cur===it.v;}\n")
sub("function shopUse(id){\n  var it=shopItem(id);if(!it)return;\n", "function shopUse(id){\n  var it=shopItem(id);if(!it)return;\n  if(it.cat==='ring'||it.cat==='ttag'){if(canWrite()&&view().me)editProg(function(p){p.deco=obj(p.deco);p.deco[it.cat==='ring'?'r':'g']=it.v;});return;}\n")
# 모두에게 보이는 꾸미기
sub("function av(p,cls){return '<span class=\"av'+(p.me?' me':'')+(cls?' '+cls:'')+'\"", "function av(p,cls){return '<span class=\"av'+(p.me?' me':'')+(cls?' '+cls:'')+decoRingCls(p.id)+'\"")
sub("return b?'<em class=\"tag tt-'+b.tier+'\">'", "return b?'<em class=\"tag tt-'+b.tier+decoTagCls(mid)+'\">'")
