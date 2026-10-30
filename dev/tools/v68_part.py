# ---------------------------------------------------------------- v68: 과목마다 '기본 항목으로'(나에게만): 기본 항목(DEFAULT_ITEMS)만 남기고 나머지는 빼기(내가 만든 것은 지움, 예전 항목은 ihide)
sub("h+='<div class=\"row\"><button class=\"btn small\" data-act=\"skip\" data-id=\"'+esc(s.id)+'\">'+(mySkip?",
    "h+='<div class=\"row\"><button class=\"btn small soft\" data-act=\"item-reset\" data-id=\"'+esc(s.id)+'\">'+(S.confirm==='ireset:'+s.id?'한 번 더 누르면 기본 항목만 남깁니다':'기본 항목으로')+'</button><button class=\"btn small\" data-act=\"skip\" data-id=\"'+esc(s.id)+'\">'+(mySkip?")
sub("    case 'item-del':{", r"""    case 'item-reset':{
      if(prev!=='ireset:'+id){S.confirm='ireset:'+id;break;}
      var Vir=view(),sir=Vir.subById[id];if(!sir||!Vir.me||!need())break;
      var norm=function(x){return String(x||'').replace(/\s+/g,'');},defs=DEFAULT_ITEMS.map(norm),all=sir.all||sir.items,add=[],del={};
      editProg(function(p){p.ihide=obj(p.ihide);
        all.forEach(function(it){var k=id+'__'+it.id;if(it.by&&it.by!==Vir.me)return;if(defs.indexOf(norm(it.label))>=0)delete p.ihide[k];else if(it.by===Vir.me)del[it.id]=1;else p.ihide[k]=true;});
      });
      DEFAULT_ITEMS.forEach(function(l){if(!all.some(function(it){return norm(it.label)===norm(l)&&!(it.by&&it.by!==Vir.me);}))add.push({id:rid('i'),label:l,by:Vir.me});});
      if(add.length||Object.keys(del).length)editSub(id,function(s){s.items=s.items.filter(function(it){return it&&!del[it.id];}).concat(add);});
      flash(jos(sir.name,'은','는')+' 기본 항목만 남겼습니다. 친구들 항목은 그대로입니다.');break;
    }
    case 'item-del':{""")
