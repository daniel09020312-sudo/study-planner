# ---------------------------------------------------------------- 과목별 진도: 각자 단원을 정하고 단원별 진도 보기
UNITS_JS = open(BASE + '/src/units.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", UNITS_JS + "\n/* ---------- 공부방 ---------- */")
# 예전 표는 '과목과 항목 편집' 때만 쓴다
sub("function viewProg(V){", r"""function viewProg(V){
  if(S.edit)return viewProgEdit(V);
  var mode=S.progMode==='all'||!V.me?'all':'me';
  var h='<div class="view" id="view-prog"><header class="vhead"><div><h1>과목별 진도</h1><p>'+(mode==='me'?'내 시험 범위의 단원을 적고 단원별로 끝낸 공부를 표시하세요. 단원은 사람마다 따로 정합니다.':'과목마다 각자 얼마나 했는지 봅니다. 과목을 누르면 단원별로 보입니다.')+'</p></div><div class="vacts"><div class="seg mini pmode" role="group" aria-label="보기">'+[['me','내 진도'],['all','모두 보기']].map(function(x){return '<button data-act="prog-mode" data-id="'+x[0]+'" aria-pressed="'+(mode===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div><button class="btn small" data-act="prog-edit">과목과 항목 편집</button></div></header>';
  h+='<div class="vbody'+(S.vbDir?' side':'')+'" id="vb-prog-'+mode+'" style="--vd:'+S.vbDir+'"><div class="ustack">'+(mode==='me'?viewProgMine(V):viewProgAll(V))+'</div></div>';
  return h+'</div>';
}
function viewProgEdit(V){""")
sub("<h1>과목별 진도</h1><p>과목을 누르면 항목이 열립니다. 끝낸 공부는 내 칸에 표시하세요.</p>", "<h1>과목과 항목 편집</h1><p>과목과 공부 항목은 모두에게 똑같이 보입니다. 단원은 내 진도에서 각자 정합니다.</p>")
sub("    case 'prog-edit':S.edit=!S.edit;break;", r"""    case 'prog-edit':S.edit=!S.edit;break;
    case 'prog-mode':{var pm0=S.progMode==='all'?'all':'me',pm1=id==='all'?'all':'me';if(pm0!==pm1){S.progMode=pm1;S.vbDir=pm1==='all'?1:-1;}break;}
    case 'unit-edit':S.uEdit=S.uEdit===id?null:id;break;
    case 'unit-add':{
      var unames=String(S.draft['unit:'+id]||'').split(/[,\n]+/).map(function(x){return x.trim().slice(0,40);}).filter(Boolean),ufull=false;if(!unames.length)break;
      editProg(function(p){p.units=obj(p.units);var l=arr(p.units[id]);unames.forEach(function(nm){if(l.length>=UNIT_MAX){ufull=true;return;}l.push({id:rid('u'),n:nm});});p.units[id]=l;});
      if(ufull)flash('단원은 과목마다 '+UNIT_MAX+'개까지 적을 수 있습니다.');
      if(canWrite()){S.draft['unit:'+id]='';S.sync=true;}break;
    }
    case 'unit-del':{
      var udl=el.getAttribute('data-u');if(prev!=='udel:'+udl){S.confirm='udel:'+udl;break;}
      editProg(function(p){p.units=obj(p.units);p.units[id]=arr(p.units[id]).filter(function(u){return u.id!==udl;});Object.keys(p.checks).forEach(function(k){if(k.indexOf(id+'__'+udl+'__')===0)delete p.checks[k];});});break;
    }
    case 'unit-mv':{
      var umv=el.getAttribute('data-u'),udd=+el.getAttribute('data-d');
      editProg(function(p){p.units=obj(p.units);var l=arr(p.units[id]),i=l.map(function(u){return u.id;}).indexOf(umv),j=i+udd;if(i<0||j<0||j>=l.length)return;var x=l[i];l[i]=l[j];l[j]=x;p.units[id]=l;});break;
    }
    case 'ucheck':{var ukey=id+'__'+el.getAttribute('data-u')+'__'+el.getAttribute('data-item');editProg(function(p){if(p.checks[ukey])delete p.checks[ukey];else p.checks[ukey]=true;});break;}""")
