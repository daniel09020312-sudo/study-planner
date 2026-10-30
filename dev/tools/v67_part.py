# ---------------------------------------------------------------- v67: 공부 항목은 사람마다. 새 항목은 만든 사람(by)만 보고, 예전 항목은 모두 보되 '빼기'는 나에게서만(progress.ihide). 같은 이름 항목은 하나만 보임
sub("items:arr(s.items).filter(function(it){return it&&it.id;}).map(function(it){return {id:String(it.id),label:String(it.label||'')};})};",
    "items:arr(s.items).filter(function(it){return it&&it.id;}).map(function(it){var o={id:String(it.id),label:String(it.label||'')};if(it.by)o.by=String(it.by);return o;})};")
sub("V.subs.forEach(function(s){V.subById[s.id]=s;V.subName[s.id]=s.name;});",
    "V.subs.forEach(function(s){V.subById[s.id]=s;V.subName[s.id]=s.name;s.all=s.items;s.items=itemsFor(V,V.me,s);});")
sub("function unitStat(V,mid,s){\n", r"""/* 그 사람이 보는 항목: 다른 사람이 만든 항목(by)은 빼고, 내가 뺀 항목(ihide)도 빼고, 같은 이름은 하나만(내가 체크한 것을 먼저) */
function itemsFor(V,mid,s){
  var all=s.all||s.items,p=obj(V.progress[mid]),hd=obj(p.ihide),ck=obj(p.checks),seen={},out=[];
  var mine=function(it){var t='__'+it.id;for(var k in ck){if(ck[k]&&k.indexOf(s.id+'__')===0&&k.slice(-t.length)===t)return true;}return false;};
  var vis=all.filter(function(it){return !(it.by&&it.by!==mid)&&!hd[s.id+'__'+it.id];});
  vis.filter(mine).concat(vis).forEach(function(it){var l=it.label.replace(/\s+/g,'');if(seen[l])return;seen[l]=1;out.push(it);});
  return all.filter(function(it){return out.indexOf(it)>=0;});
}
function subFor(V,mid,s){if(mid===V.me||!s.all)return s;return Object.assign({},s,{items:itemsFor(V,mid,s)});}
function unitStat(V,mid,s){
  s=subFor(V,mid,s);
""")
sub("us.forEach(function(x){if(s.items.length&&s.items.every(function(it){return ck[s.id+'__'+x.id+'__'+it.id];}))full++;",
    "var sit=subFor(V,m.id,s).items;us.forEach(function(x){if(sit.length&&sit.every(function(it){return ck[s.id+'__'+x.id+'__'+it.id];}))full++;")
sub("skip=skipOf(V,m.id)[s.id],c=s.items.filter(function(it){return ck[s.id+'__'+it.id];}).length;",
    "skip=skipOf(V,m.id)[s.id],sim=subFor(V,m.id,s).items,c=sim.filter(function(it){return ck[s.id+'__'+it.id];}).length;")
sub("'<span class=\"frac\">'+c+'/'+s.items.length+'</span>'", "'<span class=\"frac\">'+c+'/'+sim.length+'</span>'")
sub("editSub(id,function(s){if(s.items.length<12)s.items.push({id:rid('i'),label:label.slice(0,30)});else flash('항목은 과목당 12개까지입니다.');});",
    r"""var Vit=view(),sit0=Vit.subById[id],lk=label.slice(0,30).replace(/\s+/g,'');
      var have=sit0?sit0.items.filter(function(it){return it.label.replace(/\s+/g,'')===lk;})[0]:null;
      var hid=sit0?(sit0.all||[]).filter(function(it){return it.label.replace(/\s+/g,'')===lk&&!(it.by&&it.by!==Vit.me);})[0]:null;
      if(have){flash('이미 있는 항목입니다.');}
      else if(hid&&Vit.me){editProg(function(p){p.ihide=obj(p.ihide);delete p.ihide[id+'__'+hid.id];});}
      else if(sit0&&sit0.items.length>=12){flash('항목은 과목당 12개까지입니다.');}
      else editSub(id,function(s){if(s.items.length<60){var ni={id:rid('i'),label:label.slice(0,30)};if(Vit.me)ni.by=Vit.me;s.items.push(ni);}});""")
sub("case 'item-del':{var iid=el.getAttribute('data-item');editSub(id,function(s){s.items=s.items.filter(function(it){return it&&it.id!==iid;});});break;}",
    "case 'item-del':{var iid=el.getAttribute('data-item'),Vid=view(),sid0=Vid.subById[id],it0=sid0&&(sid0.all||[]).filter(function(it){return it.id===iid;})[0];if(it0&&it0.by&&it0.by===Vid.me)editSub(id,function(s){s.items=s.items.filter(function(it){return it&&it.id!==iid;});});else if(Vid.me)editProg(function(p){p.ihide=obj(p.ihide);p.ihide[id+'__'+iid]=true;});break;}")
sub("같은 이름 과목은 같이 쓰고, 그 과목의 항목은 함께 바뀝니다.", "같은 이름 과목은 같이 쓰고, 공부 항목은 각자 정합니다(예전 항목은 빼면 나에게서만 빠집니다).")
