# ---------------------------------------------------------------- v69: 미적분Ⅰ·확률과 통계 항목을 모두에게 기본 항목으로(한 번, meta/config migItems2), 교양 과목(lib: 후마니타스 등)은 진도·퍼센트 없이 이름만
sub("try{humMig();}catch(e){}", "try{humMig();}catch(e){}\n  try{itemMig();}catch(e){}")
sub("function progRows(V){\n  return mySubs(V).map(", r"""/* 교양 과목: 과목 문서 lib가 true이거나, 정하지 않았으면 이름이 후마니타스 */
function isLib(V,sid){var o=obj(V.subjects[sid]);if(o.lib===true)return true;if(o.lib===false)return false;return /후마니타스/.test(String(o.name||''));}
var ITEM_MIG=false;
function itemMig(){
  if(ITEM_MIG||!netFresh())return;var V=view();
  if(!S.ready||!V||!V.me||!canWrite())return;
  ITEM_MIG=true;if(obj(V.cfg).migItems2)return;
  var norm=function(x){return String(x||'').replace(/\s+/g,'');},kept=[];
  V.subs.forEach(function(s){
    var n=norm(s.name);if(!/^미적분(Ⅰ|I|1)?$/.test(n)&&n!=='확률과통계')return;
    var raw=arr(obj(V.subjects[s.id]).items).filter(function(it){return it&&it.id;});
    var list=DEFAULT_ITEMS.map(function(l){
      var hit=raw.filter(function(it){return norm(it.label)===norm(l)&&!it.by;})[0]||raw.filter(function(it){return norm(it.label)===norm(l);})[0];
      if(hit){kept.push(s.id+'__'+hit.id);return {id:String(hit.id),label:l};}
      return {id:rid('i'),label:l};
    });
    editSub(s.id,function(x){x.items=list;});
  });
  editProg(function(p){if(p.ihide)kept.forEach(function(k){delete p.ihide[k];});});
  editCfg(function(c){c.migItems2=1;});
}
function progRows(V){
  return mySubs(V).filter(function(s){return !isLib(V,s.id);}).map(""")
sub("mine.forEach(function(s){var u=unitStat(V,V.me,s);tot+=u.t;dn+=u.d;});", "mine.forEach(function(s){if(isLib(V,s.id))return;var u=unitStat(V,V.me,s);tot+=u.t;dn+=u.d;});")
sub("  mine.forEach(function(s,k){\n    var st=unitStat(V,V.me,s),", """  mine.forEach(function(s,k){
    if(isLib(V,s.id)){var lc=subCol(V,s.id);h+='<section class="card usub ulib" id="us-'+esc(s.id)+'" style="--k:'+Math.min(k+1,6)+';--sc:'+lc+';--fg:'+fgOn(lc)+'"><div class="ct"><h2><i class="sdot"></i>'+esc(s.name)+'<small>교양 과목, 시험 없음</small></h2></div><div class="row ufoot"><button class="btn small" data-act="skip" data-id="'+esc(s.id)+'">안 듣는 과목이면 빼기</button></div></section>';return;}
    var st=unitStat(V,V.me,s),""")
sub("  if(!rows.length)h+='<p class=\"empty\">아직 과목이 없습니다.</p>';", "  if(!rows.length)h+='<p class=\"empty\">아직 과목이 없습니다.</p>';\n  var libs=mySubs(V).filter(function(s){return isLib(V,s.id);});if(libs.length)h+='<p class=\"hint\" style=\"margin:4px 0 8px\">교양 과목(진도 없음): '+libs.map(function(s){return esc(s.name);}).join(', ')+'</p>';")
sub("    var open=!!S.open[s.id],mySkip=!!skipOf(V,V.me)[s.id];\n", """    var open=!!S.open[s.id],mySkip=!!skipOf(V,V.me)[s.id];
    if(isLib(V,s.id)){h+='<div class="orow osum olib" id="os-'+esc(s.id)+'"><span class="olabel"><b>'+esc(s.name)+'</b><small class="hint">교양 과목, 시험 없음</small></span></div><div class="ofoot" id="of-'+esc(s.id)+'"><div class="row"><button class="btn small soft" data-act="sub-lib" data-id="'+esc(s.id)+'">시험 보는 과목으로</button><button class="btn small" data-act="skip" data-id="'+esc(s.id)+'">'+(mySkip?'내 과목에 다시 넣기':'내가 안 듣는 과목이면 빼기')+'</button>'+(S.edit?'<button class="btn small" data-act="sub-del" data-id="'+esc(s.id)+'">'+(S.confirm==='sub:'+s.id?'한 번 더 누르면 삭제':'과목 삭제')+'</button>':'')+'</div></div>';return;}
""")
sub("<button class=\"btn small soft\" data-act=\"item-reset\" data-id=\"'+esc(s.id)+'\">", "<button class=\"btn small soft\" data-act=\"sub-lib\" data-id=\"'+esc(s.id)+'\">교양 과목으로(시험 없음)</button><button class=\"btn small soft\" data-act=\"item-reset\" data-id=\"'+esc(s.id)+'\">")
sub("과목과 항목은 참여 인원 모두에게 똑같이 보입니다.", "과목은 각자 정하고, 같은 이름 과목은 함께 씁니다. 교양 과목은 진도 없이 이름만 보입니다.")
sub("var mys=V.subs.filter(function(x){return !skip[x.id];});", "var mys=V.subs.filter(function(x){return !skip[x.id]&&!isLib(V,x.id);});")
sub("    case 'item-del':{", "    case 'sub-lib':{var Vlb=view();if(!Vlb.subjects[id]||!need())break;var lbOn=!isLib(Vlb,id);editSub(id,function(s){s.lib=lbOn;});flash(lbOn?'교양 과목으로 바꿨습니다. 진도 없이 이름만 보입니다.':'시험 보는 과목으로 바꿨습니다.');break;}\n    case 'item-del':{")
