/* ---------- v110: 할 순서 정하기. 하루 할 일 카드에서 '할 순서 정하기'를 켜고 하고 싶은 순서대로 누르면 그 순서로 줄을 바꾸고(day.ord=1), 남은 할 일 앞에 1, 2, 3 번호 ---------- */
S.gNum=null;S.gNumPick=[];
function gNumList(day){return day.goals.filter(function(x){return x&&!x.done&&!x.mv;});}
/* 번호: 남은 할 일 중 몇 번째 */
function gOrdNo(day,x){if(!day.ord||x.done||x.mv)return 0;var l=gNumList(day);for(var i=0;i<l.length;i++)if(l[i].id===x.id)return i+1;return 0;}
function goalRowNum(V,date,day,x){
  if(x.done||x.mv)return '';
  var i=S.gNumPick.indexOf(x.id),sub=x.sid&&V.subName[x.sid];
  return '<li class="goal gnrow'+(i>=0?' on':'')+'" id="g-'+esc(x.id)+'"><button class="gnb'+(i>=0?' on':'')+'" data-act="g-numpick" data-date="'+date+'" data-id="'+esc(x.id)+'" aria-label="'+esc(x.text)+(i>=0?' '+(i+1)+'번째, 누르면 빼기':' 다음 순서로')+'">'+(i>=0?(i+1):'')+'</button><button class="gt gnt" data-act="g-numpick" data-date="'+date+'" data-id="'+esc(x.id)+'" tabindex="-1">'+(sub?subTag(V,x):'')+'<span>'+esc(x.text)+'</span></button><span></span></li>';
}
function gNumBar(V,date,day){
  var n=gNumList(day).length,k=S.gNumPick.length;
  return '<div class="gnbar"><div><b>할 순서 정하기</b><small>'+(k?k+' / '+n+'개 골랐습니다. 남은 것은 그 뒤로 갑니다.':'먼저 할 일부터 차례로 누르세요.')+'</small></div><div class="row"><button class="btn small" data-act="g-numx">취소</button>'+(k?'<button class="btn small" data-act="g-numreset">다시</button>':'')+(day.ord&&!k?'<button class="btn small" data-act="g-numoff">번호 없애기</button>':'')+'<button class="btn small primary" data-act="g-numsave"'+(k?'':' disabled')+'>저장</button></div></div>';
}
function gNumSave(date){
  var V=view(),day=dayOf(V,V.me,date),pick=S.gNumPick.slice();
  if(!pick.length){S.gNum=null;return;}
  var sn=snap(['days/'+V.me+'_'+date]);
  editDay(date,function(d){
    var by={};d.goals.forEach(function(x){if(x&&x.id)by[x.id]=x;});
    var first=pick.map(function(id){return by[id];}).filter(function(x){return x&&!x.done&&!x.mv;}),used={};first.forEach(function(x){used[x.id]=1;});
    var rest=d.goals.filter(function(x){return !(x&&used[x.id])&&x&&!x.done&&!x.mv;}),tail=d.goals.filter(function(x){return !(x&&used[x.id])&&!(x&&!x.done&&!x.mv);});
    d.goals=first.concat(rest,tail);d.ord=1;
  });
  var gs=gSortOn();if(gs)lsSet('gbb_gsort',null);
  S.gNum=null;S.gNumPick=[];
  flash('할 순서를 정했습니다.'+(gs?' 과목순 자동 정렬은 껐습니다.':''),sn);
}
