/* ---------- v70: 달력 화면에서 옆으로 밀어 넘기기 (할 일 목록은 주, 달력은 달). 옆으로 밀리는 칸이 있으면 그 끝에 닿아 있을 때만 ---------- */
var SWP=null;
function swpScroller(el,stop){
  for(var e=el;e&&e!==stop&&e!==document.body;e=e.parentElement){
    if(e.scrollWidth>e.clientWidth+2){var ox=getComputedStyle(e).overflowX;if(ox==='auto'||ox==='scroll')return e;}
  }
  return null;
}
document.addEventListener('touchstart',function(e){
  SWP=null;if(!e.touches||e.touches.length!==1||S.modal)return;
  var v=document.getElementById('view-cal'),t=e.target;if(!v||!v.contains(t))return;
  if(S.calMode!=='list'&&S.calMode!=='cal'&&S.calMode)return;
  if(t.closest&&t.closest('input,textarea,select,[contenteditable],.noswipe'))return;
  var sc=swpScroller(t,v),p=e.touches[0];
  SWP={x:p.clientX,y:p.clientY,t:Date.now(),sc:sc,s0:sc?sc.scrollLeft<=1:true,e0:sc?sc.scrollLeft+sc.clientWidth>=sc.scrollWidth-1:true};
},{passive:true});
document.addEventListener('touchend',function(e){
  var s=SWP;SWP=null;if(!s||!e.changedTouches||!e.changedTouches.length)return;
  var p=e.changedTouches[0],dx=p.clientX-s.x,dy=p.clientY-s.y,dt=Date.now()-s.t;
  if(S.drag||(window.__ttDragEnd&&Date.now()-window.__ttDragEnd<500)||(typeof WD!=='undefined'&&WD))return;
  if(dt>800||Math.abs(dx)<70||Math.abs(dx)<Math.abs(dy)*2)return;
  var d=dx<0?1:-1;if(d>0&&!s.e0)return;if(d<0&&!s.s0)return;
  var name=S.calMode==='list'?'al-week':'month';
  act(name,{getAttribute:function(k){return k==='data-d'?String(d):null;}});
},{passive:true});
document.addEventListener('touchcancel',function(){SWP=null;},{passive:true});
