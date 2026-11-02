# ---------------------------------------------------------------- v74: 할 일 과목순(무지개 순서) 자동 정렬(이 기기 gbb_gsort, 할 일 목록 '과목순' 칩), 다른 날로 옮김 줄은 그제보다 오래되면 숨김
sub("  if(x.mv)return '<li class=\"goal mv\"", "  if(x.mv&&date<addDays(today(),-2))return '';\n  if(x.mv)return '<li class=\"goal mv\"")
sub("  if(x.mv)return '<div class=\"wki mv\"", "  if(x.mv&&d<addDays(today(),-2))return '';\n  if(x.mv)return '<div class=\"wki mv\"")
sub("  var list=S.alLeft?g.filter(function(x){return !x.done;}):(S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g);",
    "  var list=gSortSub(V,S.alLeft?g.filter(function(x){return !x.done;}):(S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g));")
sub("var gl=S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g;", "var gl=gSortSub(V,S.gDoneLast?g.filter(function(x){return !x.done;}).concat(g.filter(isDone)):g);")
sub("<button class=\"chip\" data-act=\"al-left\"", "<button class=\"chip\" data-act=\"al-sort\" aria-pressed=\"'+(gSortOn()?'true':'false')+'\">과목순</button><button class=\"chip\" data-act=\"al-left\"")
sub("    case 'al-left':", "    case 'al-sort':lsSet('gbb_gsort',gSortOn()?null:'1');break;\n    case 'al-left':")
sub("function wkCell(V,d,t){", r"""/* 과목순(과목 색 무지개 순서 = 과목 순서) 정렬: 같은 과목 안에서는 원래 순서, 과목 없는 할 일은 맨 뒤 */
function gSortOn(){return lsGet('gbb_gsort')==='1';}
function gSortSub(V,list){
  if(!gSortOn()||list.length<2)return list;
  var rk=function(x){var s=x&&!isEtcGoal(x)&&V.subById[x.sid];return s?V.subs.indexOf(s):9999;};
  return list.map(function(x,i){return {x:x,i:i,r:rk(x)};}).sort(function(a,b){return a.r-b.r||a.i-b.i;}).map(function(o){return o.x;});
}
function wkCell(V,d,t){""")
