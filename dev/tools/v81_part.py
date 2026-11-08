# ---------------------------------------------------------------- v81: 순서 정리 창에서 여러 개 골라 할 일 모음으로 거둬들이기(지난 날 못 끝낸 것 포함), 모음에서 골고루 나누기 (src/v81.js)
V81_JS = open(BASE + '/src/v81.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V81_JS + "\n/* ---------- 공부방 ---------- */")
# 모음 한도 60 -> 150
sub("function ibItems(V){", "var IB_MAX=150;\nfunction ibItems(V){")
sub("Object.keys(d.items).length>=60", "Object.keys(d.items).length>=IB_MAX")
sub("'할 일 모음은 60개까지", "'할 일 모음은 '+IB_MAX+'개까지")
# 순서 정리: '지난 못한 일' 범위, 지난 날 못 끝낸 일도 고르기·옮기기
sub("var GORD_R=[['today','오늘'],['week','이번 주'],['next','앞으로 2주'],['all','전체']];", "var GORD_R=[['past','지난 못한 일'],['today','오늘'],['week','이번 주'],['next','앞으로 2주'],['all','전체']];")
sub("if(r==='today'){a=t;b=t;}", "if(r==='past'){a=[CAL_MIN,addDays(t,-30)].sort().pop();b=addDays(t,-1);}else if(r==='today'){a=t;b=t;}")
sub("var g=dayOf(V,V.me,d).goals,live=g.filter(function(x){return x&&!x.mv;}),shown=G.left?", "var g=dayOf(V,V.me,d).goals,live=g.filter(function(x){return x&&!x.mv;}),shown=G.left||G.r==='past'?")
sub("+(lock?'<i class=\"sdot\"></i>':'<button class=\"gck", "+(lock&&x.done?'<i class=\"sdot\"></i>':'<button class=\"gck")
sub("if(g&&!dayLocked(V,x[0])||g&&x[0]===to)", "if(g&&(!dayLocked(V,x[0])||!g.done||x[0]===to))")
sub("<button class=\"btn small soft\" data-act=\"go-top\">고른 것 맨 위로</button>", "<button class=\"btn small primary\" data-act=\"go-collect\">모음으로 거둬들이기</button><button class=\"btn small soft\" data-act=\"go-top\">고른 것 맨 위로</button>")
sub("b+='<div class=\"row gorda\">", "b+='<div class=\"row gorda\"><button class=\"btn small soft\" data-act=\"go-selall\">보이는 남은 일 모두 고르기</button>")
sub("    case 'go-clr':", r"""    case 'go-collect':gordCollect();break;
    case 'go-selall':{var Vsa=view();S.gsel=S.gsel||{};gordDays().forEach(function(d){dayOf(Vsa,Vsa.me,d).goals.forEach(function(q){if(q&&!q.mv&&!q.done)S.gsel[d+'|'+q.id]=1;});});break;}
    case 'ib-start':if(S.ib)S.ib.start=el.getAttribute('data-v');break;
    case 'ib-n':if(S.ib)S.ib.spread=Math.max(1,Math.min(14,+el.getAttribute('data-v')||3));break;
    case 'ib-spread':ibSpread();break;
    case 'ib-selsub':{if(!S.ib)break;var Vis=view(),isid=el.getAttribute('data-v');ibItems(Vis).forEach(function(x){if((x.sid||'')===isid)S.ib.sel[x.id]=1;});break;}
    case 'go-clr':""")
# 모음: 과목별로 한 번에 고르기, 원래 날짜 표시, 골고루 나누기
sub("b+='</ul>';\n  }\n  var f='';", "b+='</ul>';\n    var isubs={};list.forEach(function(x){isubs[x.sid||'']=1;});var iks=Object.keys(isubs);if(iks.length>1)b+='<div class=\"chips ibsubs\"><small>과목별 고르기</small>'+iks.map(function(k){return chipBtn('ib-selsub','sid',k,k&&V.subName[k]?V.subName[k]:'과목 없음',false);}).join('')+'</div>';\n  }\n  var f='';")
sub("'<b>'+esc(x.t)+'</b></span></button>", "'<b>'+esc(x.t)+'</b>'+(x.od?'<small class=\"ibod\">'+(+x.od.slice(5,7))+'/'+(+x.od.slice(8))+'에서</small>':'')+'</span></button>")
sub("f+='</div><p class=\"hint\">'+(nsel?", "f+='</div>'+ibSpreadHtml(V,nsel)+'<p class=\"hint\">'+(nsel?")
