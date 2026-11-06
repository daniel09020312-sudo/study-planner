/* ---------- v79: 할 일 순서 정리 창(여러 날 할 일을 날짜별로 한 번에 보고 위·아래로 옮기기, 과목순·끝낸 일 아래로 자동 정리) ----------
   보기 범위 S.gord.r: today(오늘) week(이번 주) next(앞으로 2주) all(지난 2주부터 앞으로 4주). 다른 날로 옮긴 할 일(mv)은 보이지 않고 자리만 지킨다 */
var GORD_R=[['today','오늘'],['week','이번 주'],['next','앞으로 2주'],['all','전체']];
function gordDays(){
  var t=today(),r=(S.gord&&S.gord.r)||'next',a,b;
  if(r==='today'){a=t;b=t;}else if(r==='week'){a=wkStart(t);b=addDays(a,6);}else if(r==='all'){a=addDays(t,-14);b=addDays(t,28);}else{a=t;b=addDays(t,13);}
  var out=[];for(var d=a;d<=b;d=addDays(d,1))out.push(d);return out;
}
function gordSortRank(V,x,k){if(k==='done')return x.done?1:0;var s=x&&!isEtcGoal(x)&&V.subById[x.sid];return s?V.subs.indexOf(s):9999;}
function gordSort(V,goals,k){
  var keep=goals.map(function(x,i){return {x:x,i:i};}),live=keep.filter(function(o){return !o.x.mv;}),slots=live.map(function(o){return o.i;});
  var sorted=live.slice().sort(function(a,b){return gordSortRank(V,a.x,k)-gordSortRank(V,b.x,k)||a.i-b.i;});
  var out=goals.slice();slots.forEach(function(si,j){out[si]=sorted[j].x;});return out;
}
function modalGOrder(V){
  var G=S.gord||(S.gord={r:'next'}),days=gordDays(),t=today(),n=0,b='';
  b+='<div class="chips gordr">'+GORD_R.map(function(x){return chipBtn('go-r','r',x[0],x[1],G.r===x[0]);}).join('')+'<button class="chip" data-act="go-left" aria-pressed="'+(G.left?'true':'false')+'">남은 일만</button></div>';
  b+='<div class="row gorda"><button class="btn small soft" data-act="go-sort" data-k="sub" data-date="all">보이는 날 모두 과목순</button><button class="btn small soft" data-act="go-sort" data-k="done" data-date="all">모두 끝낸 일 아래로</button></div>';
  days.forEach(function(d){
    var g=dayOf(V,V.me,d).goals,live=g.filter(function(x){return x&&!x.mv;}),shown=G.left?live.filter(function(x){return !x.done;}):live;if(!shown.length)return;n+=shown.length;
    var dt=pd(d),lock=dayLocked(V,d);
    b+='<section class="gordd'+(d===t?' today':'')+'" id="go-'+d+'"><div class="gordh"><b>'+(dt.getMonth()+1)+'월 '+dt.getDate()+'일 '+DOW[dt.getDay()]+'</b><small>'+(d===t?'오늘 · ':'')+live.filter(isDone).length+'/'+live.length+'</small>'+(lock?'':'<span class="gordb"><button class="linkbtn" data-act="go-sort" data-k="sub" data-date="'+d+'">과목순</button><button class="linkbtn" data-act="go-sort" data-k="done" data-date="'+d+'">끝낸 일 아래로</button></span>')+'</div><ol>';
    shown.forEach(function(x,i){
      b+='<li class="gordi'+(x.done?' done':'')+'" style="--sc:'+goalCol(V,x)+'"><i class="sdot"></i><span class="gordt">'+esc(x.text)+(x.sid&&V.subName[x.sid]?'<small>'+esc(V.subName[x.sid])+'</small>':'')+'</span>';
      if(!lock)b+='<button class="ib sm" data-act="go-mv" data-date="'+d+'" data-id="'+esc(x.id)+'" data-v="-1" aria-label="위로"'+(i===0?' disabled':'')+'>&#8593;</button><button class="ib sm" data-act="go-mv" data-date="'+d+'" data-id="'+esc(x.id)+'" data-v="1" aria-label="아래로"'+(i===shown.length-1?' disabled':'')+'>&#8595;</button>';
      b+='</li>';
    });
    b+='</ol></section>';
  });
  if(!n)b+='<p class="empty">이 기간에는 할 일이 없습니다.</p>';
  return dlg('wide',{id:'gorder',t:'할 일 순서 정리'},b,'<div class="df"><span class="hint">마감이 지난 날은 보기만 됩니다.'+(gSortOn()?' 할 일 목록의 과목순 보기가 켜져 있으면 목록에서는 과목순으로 보입니다.':'')+'</span><button class="btn primary" data-act="modal-close">닫기</button></div>');
}
