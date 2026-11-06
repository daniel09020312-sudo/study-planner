/* ---------- v80: 순서 정리 창에서 손잡이로 끌어 옮기기(같은 날 순서, 다른 날로), 여러 개 골라 한 번에 옮기기 ----------
   고른 할 일: S.gsel={'<날짜>|<id>':1}. 끌 때 잡은 할 일이 골라 둔 것 중 하나면 골라 둔 것 모두 함께 옮긴다 */
var GD=null;
function gselKeys(){return Object.keys(S.gsel||{}).filter(function(k){return S.gsel[k];});}
/* items=[[날짜,id]...]를 to 날짜의 before(id, 없으면 맨 뒤) 앞으로. 지난 날로는 못 옮기고, 다른 날로 가면 완료 표시·시간은 지운다 */
function gordMove(items,to,before){
  var V=view();if(!V.me||!need()||!items.length)return false;
  if(dayLocked(V,to)){flash('마감이 지난 날로는 옮길 수 없습니다.');return false;}
  var cross=items.filter(function(x){return x[0]!==to;});
  if(cross.length&&to<today()){flash('지난 날로는 옮길 수 없습니다.');return false;}
  var tgo=dayOf(V,V.me,to).goals;if(tgo.length+cross.length>GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');return false;}
  var picked=[],paths={};paths['days/'+V.me+'_'+to]=1;
  items.forEach(function(x){var g=dayOf(V,V.me,x[0]).goals.filter(function(q){return q&&q.id===x[1]&&!q.mv;})[0];if(g&&!dayLocked(V,x[0])||g&&x[0]===to){picked.push([x[0],g]);paths['days/'+V.me+'_'+x[0]]=1;}});
  if(!picked.length)return false;
  picked.sort(function(a,b){if(a[0]!==b[0])return a[0]<b[0]?-1:1;var gl=dayOf(V,V.me,a[0]).goals;return gl.indexOf(a[1])-gl.indexOf(b[1]);});
  var sn=snap(Object.keys(paths)),ids=picked.map(function(p){return p[1].id;}),froms={};
  picked.forEach(function(p){if(p[0]!==to)froms[p[0]]=1;});
  Object.keys(froms).forEach(function(d){editDay(d,function(dd){dd.goals=dd.goals.filter(function(q){return !(q&&ids.indexOf(q.id)>=0&&!q.mv);});if(ids.indexOf(dd.focus)>=0)dd.focus=null;});});
  editDay(to,function(dd){
    var keep=dd.goals.filter(function(q){return !(q&&ids.indexOf(q.id)>=0&&!q.mv);});
    var ins=picked.map(function(p){var c=clone(p[1]);if(p[0]!==to){c.done=false;delete c.ts;delete c.te;}return c;});
    var at=before?keep.map(function(q){return q&&q.id;}).indexOf(before):-1;
    if(at<0)keep=keep.concat(ins);else keep=keep.slice(0,at).concat(ins,keep.slice(at));
    dd.goals=keep;
  });
  var n=picked.length,moved=Object.keys(froms).length;
  flash(moved?n+'개를 '+shortDate(to)+'로 옮겼습니다.':'순서를 바꿨습니다.',sn);
  S.gsel={};return true;
}
function gdClear(){if(!GD)return;if(GD.gh&&GD.gh.parentNode)GD.gh.parentNode.removeChild(GD.gh);[].forEach.call(document.querySelectorAll('.gordi.gdover,.gordi.gdafter,.gordd.gdend'),function(e){e.classList.remove('gdover','gdafter','gdend');});document.documentElement.classList.remove('gdragging');}
function gdTarget(x,y){
  if(GD.gh)GD.gh.style.visibility='hidden';var e=document.elementFromPoint(x,y);if(GD.gh)GD.gh.style.visibility='';
  var row=e&&e.closest&&e.closest('.gordi'),sec=e&&e.closest&&e.closest('.gordd');
  if(row){var r=row.getBoundingClientRect(),after=y>r.top+r.height/2,nx=after?row.nextElementSibling:row;return {d:row.getAttribute('data-date'),before:nx&&nx.getAttribute?nx.getAttribute('data-id'):null,row:row,after:after};}
  if(sec)return {d:sec.getAttribute('data-d'),before:null,sec:sec};
  return null;
}
document.addEventListener('pointerdown',function(e){
  var h=e.target.closest&&e.target.closest('.gdh');if(!h||!S.modal||S.modal.type!=='gorder')return;
  var row=h.closest('.gordi');if(!row)return;e.preventDefault();
  var d=row.getAttribute('data-date'),id=row.getAttribute('data-id'),k=d+'|'+id,sel=gselKeys(),items=sel.indexOf(k)>=0?sel.map(function(s){var i=s.indexOf('|');return [s.slice(0,i),s.slice(i+1)];}):[[d,id]];
  var r=row.getBoundingClientRect(),gh=row.cloneNode(true);gh.classList.add('gdghost');gh.style.width=r.width+'px';gh.style.left=r.left+'px';gh.style.top=r.top+'px';
  if(items.length>1){var bd=document.createElement('em');bd.className='gdn';bd.textContent=items.length+'개';gh.appendChild(bd);}
  document.body.appendChild(gh);
  GD={items:items,gh:gh,dy:e.clientY-r.top,dx:e.clientX-r.left,sc:row.closest('.db'),pid:e.pointerId,t:null};
  S.drag=true;document.documentElement.classList.add('gdragging');
  try{h.setPointerCapture(e.pointerId);}catch(x){}
},{passive:false});
document.addEventListener('pointermove',function(e){
  if(!GD||e.pointerId!==GD.pid)return;e.preventDefault();
  GD.gh.style.left=(e.clientX-GD.dx)+'px';GD.gh.style.top=(e.clientY-GD.dy)+'px';
  [].forEach.call(document.querySelectorAll('.gordi.gdover,.gordi.gdafter,.gordd.gdend'),function(x){x.classList.remove('gdover','gdafter','gdend');});
  var t=gdTarget(e.clientX,e.clientY);GD.t=t;
  if(t&&t.row)t.row.classList.add(t.after?'gdafter':'gdover');else if(t&&t.sec)t.sec.classList.add('gdend');
  if(GD.sc){var sr=GD.sc.getBoundingClientRect();if(e.clientY<sr.top+50)GD.sc.scrollTop-=12;else if(e.clientY>sr.bottom-50)GD.sc.scrollTop+=12;}
},{passive:false});
function gdEnd(e,cancel){
  if(!GD||(e&&e.pointerId!==GD.pid))return;var g=GD,t=g.t;gdClear();GD=null;S.drag=false;
  if(!cancel&&t&&t.d){var same=g.items.length===1&&g.items[0][1]===t.before;if(!same)gordMove(g.items,t.d,t.before);}
  S.dragDirty=false;render();
}
document.addEventListener('pointerup',function(e){gdEnd(e,false);});
document.addEventListener('pointercancel',function(e){gdEnd(e,true);});
