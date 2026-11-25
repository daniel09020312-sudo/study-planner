# ---------------------------------------------------------------- v110: 할 순서 정하기(하루 할 일 카드 '할 순서 정하기', 누른 순서로 줄 바꿈, day.ord=1이면 남은 할 일 앞 번호) (src/v110.js)
sub("  if(d.hh)r0.hh=obj(d.hh);\n  return r0;", "  if(d.hh)r0.hh=obj(d.hh);\n  if(d.ord)r0.ord=1;\n  return r0;")
sub("/* ---------- 공부방 ---------- */", open(BASE + '/src/v110.js', encoding='utf-8').read() + "\n/* ---------- 공부방 ---------- */")
sub("function goalRow(V,date,mode,day,x,isT){\n", "function goalRow(V,date,mode,day,x,isT){\n  if(S.gNum===date)return goalRowNum(V,date,day,x);\n")
# 번호 표시(적은 순서 보기에서만)
sub("  else h+='<div class=\"gt\">'+(sub&&S.gGroup!=='sub'?subTag(V,x):'')+'<span>'+esc(x.text)+'</span>'",
    "  else h+='<div class=\"gt\">'+(function(n){return n&&S.gGroup==='none'&&!gSortOn()?'<b class=\"gno'+(n===1?' n1':'')+'\" title=\"할 순서\">'+n+'</b>':'';})(gOrdNo(day,x))+(sub&&S.gGroup!=='sub'?subTag(V,x):'')+'<span>'+esc(x.text)+'</span>'")
sub("<button class=\"chip\" data-act=\"open\" data-modal=\"gall\">전체 할 일</button><button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button><button class=\"chip\" data-act=\"g-donelast\"",
    "'+(mode!=='view'&&!doneLocked(V,date)&&undone>=2&&S.gNum!==date?'<button class=\"chip\" data-act=\"g-num\" data-date=\"'+date+'\">'+(day.ord?'할 순서 다시 정하기':'할 순서 정하기')+'</button>':'')+'<button class=\"chip\" data-act=\"open\" data-modal=\"gall\">전체 할 일</button><button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button><button class=\"chip\" data-act=\"g-donelast\"")
sub("    var gl=gSortSub(V,S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g);\n    h+='<ul>';\n    if(S.gGroup==='none'||g.length<2)",
    "    var gl=S.gNum===date?g:gSortSub(V,S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g);\n    if(S.gNum===date)h+=gNumBar(V,date,day);\n    h+='<ul>';\n    if(S.gGroup==='none'||g.length<2||S.gNum===date)")
sub("    case 'g-donelast':", """    case 'g-num':if(!need())break;S.gNum=date;S.gNumPick=[];S.gSel=null;S.gEdit=null;break;
    case 'g-numx':S.gNum=null;S.gNumPick=[];break;
    case 'g-numreset':S.gNumPick=[];break;
    case 'g-numpick':{var pi=S.gNumPick.indexOf(id);if(pi>=0)S.gNumPick.splice(pi,1);else S.gNumPick.push(id);
      var Vp=view(),dp=dayOf(Vp,Vp.me,date);if(S.gNumPick.length>=gNumList(dp).length)gNumSave(date);break;}
    case 'g-numsave':gNumSave(S.gNum||date);break;
    case 'g-numoff':{var sno=snap(['days/'+view().me+'_'+date]);editDay(date,function(d){delete d.ord;});S.gNum=null;S.gNumPick=[];flash('할 순서 번호를 없앴습니다.',sno);break;}
    case 'g-donelast':""")
sub("</style>", open(BASE + '/src/v110.css', encoding='utf-8').read() + "</style>")
