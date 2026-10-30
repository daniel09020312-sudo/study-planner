# ---------------------------------------------------------------- v60: 과목은 사람마다. 새로 만든 과목은 만든 사람(by)만 갖고, 다른 사람은 '다른 사람 과목'에서 골라 넣음(progress.<나>.suse)
# skipOf(V,mid): 그 사람이 안 갖는 과목 = skip에 있거나, 다른 사람이 만든(by) 과목인데 suse에 없음. 비교(진도 반 평균 등)는 그 과목을 가진 사람끼리
sub("function mySubs(V){var sk=obj(obj(V.progress[V.me]).skip);return V.subs.filter(function(s){return !sk[s.id];});}",
r"""function skipOf(V,mid){
  V._sk=V._sk||{};if(V._sk[mid])return V._sk[mid];
  var p=obj(V.progress[mid]),sk=obj(p.skip),use=obj(p.suse),o={};
  V.subs.forEach(function(s){var by=obj(V.subjects[s.id]).by;if(sk[s.id]||(by&&by!==mid&&!use[s.id]))o[s.id]=true;});
  return (V._sk[mid]=o);
}
function hasSub(V,mid,sid){return !skipOf(V,mid)[sid];}
function mySubs(V){if(!V.me)return V.subs;var sk=skipOf(V,V.me);return V.subs.filter(function(s){return !sk[s.id];});}""")
sub("var p=obj(V.progress[V.me]),ck=obj(p.checks),skip=obj(p.skip),mine=", "var p=obj(V.progress[V.me]),ck=obj(p.checks),skip=skipOf(V,V.me),mine=")
sub("<h2>뺀 과목</h2>", "<h2>뺀 과목, 다른 사람 과목<small>눌러서 내 과목에 넣기</small></h2>")
sub("function progRows(V){\n  return V.subs.map(function(s){\n    var per=[],skipN=0;\n    V.roster.forEach(function(m){\n      if(obj(obj(V.progress[m.id]).skip)[s.id]){skipN++;return;}",
    "function progRows(V){\n  return mySubs(V).map(function(s){\n    var per=[],skipN=0;\n    V.roster.forEach(function(m){\n      if(skipOf(V,m.id)[s.id]){skipN++;return;}")
sub("var allOpen=V.subs.length>0&&V.subs.every(function(s){return S.open[s.id];});", "var allOpen=mySubs(V).length>0&&mySubs(V).every(function(s){return S.open[s.id];});")
sub("과목과 공부 항목은 모두에게 똑같이 보입니다. 단원은 내 진도에서 각자 정합니다.", "과목은 각자 정합니다. 같은 이름 과목은 같이 쓰고, 그 과목의 항목은 함께 바뀝니다. 다른 사람 과목은 내 진도의 아래에서 넣을 수 있습니다.")
sub("  V.subs.forEach(function(s){\n    var open=!!S.open[s.id],mySkip=!!obj(obj(V.progress[V.me]).skip)[s.id];", "  mySubs(V).forEach(function(s){\n    var open=!!S.open[s.id],mySkip=!!skipOf(V,V.me)[s.id];")
sub("var p=obj(V.progress[m.id]),ck=obj(p.checks),skip=obj(p.skip)[s.id],c=", "var p=obj(V.progress[m.id]),ck=obj(p.checks),skip=skipOf(V,m.id)[s.id],c=")
sub("var p=obj(V.progress[m.id]),on=!!obj(p.checks)[s.id+'__'+it.id],skip=!!obj(p.skip)[s.id],nm=", "var p=obj(V.progress[m.id]),on=!!obj(p.checks)[s.id+'__'+it.id],skip=!!skipOf(V,m.id)[s.id],nm=")
sub("rows=V.sc[mid]||{},skip=obj(obj(V.progress[mid]).skip),subj={},k;", "rows=V.sc[mid]||{},skip=skipOf(V,mid),subj={},k;")
sub("    V.subs.forEach(function(s){\n      var cur=subCol(V,s.id),open=S.scolOpen===s.id", "    mySubs(V).forEach(function(s){\n      var cur=subCol(V,s.id),open=S.scolOpen===s.id")
# 빼기/넣기
sub("case 'skip':editProg(function(p){if(p.skip[id])delete p.skip[id];else p.skip[id]=true;});break;",
    "case 'skip':{var Vk=view(),kon=!!skipOf(Vk,Vk.me)[id];editProg(function(p){p.suse=obj(p.suse);if(kon){delete p.skip[id];p.suse[id]=true;}else{p.skip[id]=true;delete p.suse[id];}});break;}")
# 과목 추가: 같은 이름이 있으면 그 과목을 내 과목에 넣고, 없으면 만든 사람(by)을 적어 만든다
sub("      var V2=view(),ord=V2.subs.reduce(function(a,s){return Math.max(a,s.order);},0)+1,sid=rid('s');\n      save('subjects/'+sid,{name:sn.slice(0,24),order:ord,items:itemsOf(DEFAULT_ITEMS)});",
    "      var V2=view(),ord=V2.subs.reduce(function(a,s){return Math.max(a,s.order);},0)+1,sid=rid('s'),snk=sn.slice(0,24).replace(/\\s+/g,'').toLowerCase();\n      var same=V2.subs.filter(function(s){return s.name.replace(/\\s+/g,'').toLowerCase()===snk;})[0];\n      if(same){if(V2.me){editProg(function(p){p.suse=obj(p.suse);delete p.skip[same.id];p.suse[same.id]=true;});flash('같은 이름 과목이 있어 내 과목에 넣었습니다.');}S.draft.subName='';S.open[same.id]=true;break;}\n      var nsub={name:sn.slice(0,24),order:ord,items:itemsOf(DEFAULT_ITEMS)};if(V2.me)nsub.by=V2.me;\n      save('subjects/'+sid,nsub);")
# 과목 삭제: 다른 사람도 가진 과목이면 내 과목에서만 뺀다
sub("case 'sub-del':if(prev==='sub:'+id){if(need())save('subjects/'+id,null);}else S.confirm='sub:'+id;break;",
    "case 'sub-del':if(prev==='sub:'+id){if(need()){var Vd=view(),oth=Vd.roster.filter(function(m){return m.id!==Vd.me&&hasSub(Vd,m.id,id);}).length;if(oth&&Vd.me){editProg(function(p){p.suse=obj(p.suse);p.skip[id]=true;delete p.suse[id];});flash('다른 사람('+oth+'명)도 듣는 과목이라 내 과목에서만 뺐습니다.');}else save('subjects/'+id,null);}}else S.confirm='sub:'+id;break;")
