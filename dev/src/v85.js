/* ---------- v85: 할 일 모음에서 ≡ 손잡이로 끌어 순서 바꾸기. 순서는 항목의 o(작을수록 위), o가 없으면 적은 시각(at) 순.
   골라 둔 항목을 끌면 골라 둔 것 모두 함께. 과목별 보기에서는 같은 과목 안에서 순서가 바뀐다 ---------- */
var IBD=null;
function ibOrd(x){return x.o!=null&&x.o!==''?+x.o:+x.at||0;}
function ibMove(ids,before){
  var V=view();if(!V.me||!need()||!ids.length)return false;
  var list=ibItems(V),mv=list.filter(function(x){return ids.indexOf(x.id)>=0;});if(!mv.length)return false;
  var rest=list.filter(function(x){return ids.indexOf(x.id)<0;}),at=before?rest.map(function(x){return x.id;}).indexOf(before):-1;
  var out=at<0?rest.concat(mv):rest.slice(0,at).concat(mv,rest.slice(at));
  if(out.map(function(x){return x.id;}).join()===list.map(function(x){return x.id;}).join())return false;
  var sn=snap(['inbox/'+V.me]);
  editInbox(function(d){out.forEach(function(x,i){if(d.items[x.id])d.items[x.id].o=i+1;});});
  flash(mv.length>1?mv.length+'개 순서를 바꿨습니다.':'순서를 바꿨습니다.',sn);
  return true;
}
function ibdClear(){if(!IBD)return;if(IBD.gh&&IBD.gh.parentNode)IBD.gh.parentNode.removeChild(IBD.gh);[].forEach.call(document.querySelectorAll('.ibrow.gdover,.ibrow.gdafter'),function(e){e.classList.remove('gdover','gdafter');});document.documentElement.classList.remove('gdragging');}
function ibdTarget(x,y){
  if(IBD.gh)IBD.gh.style.visibility='hidden';var e=document.elementFromPoint(x,y);if(IBD.gh)IBD.gh.style.visibility='';
  var row=e&&e.closest&&e.closest('.ibrow');if(!row||!row.closest('#dlg-inbox'))return null;
  var r=row.getBoundingClientRect(),after=y>r.top+r.height/2,nx=row;
  if(after){nx=row.nextElementSibling;while(nx&&!(nx.classList&&nx.classList.contains('ibrow')))nx=nx.nextElementSibling;}
  return {before:nx?nx.getAttribute('data-id'):null,row:row,after:after};
}
document.addEventListener('pointerdown',function(e){
  var h=e.target.closest&&e.target.closest('.ibh');if(!h||!S.modal||S.modal.type!=='inbox')return;
  var row=h.closest('.ibrow');if(!row)return;e.preventDefault();
  var id=row.getAttribute('data-id'),sel=Object.keys(obj(S.ib&&S.ib.sel)).filter(function(k){return S.ib.sel[k];}),ids=sel.indexOf(id)>=0?sel:[id];
  var r=row.getBoundingClientRect(),gh=row.cloneNode(true);gh.classList.add('gdghost');gh.style.width=r.width+'px';gh.style.left=r.left+'px';gh.style.top=r.top+'px';
  if(ids.length>1){var bd=document.createElement('em');bd.className='gdn';bd.textContent=ids.length+'개';gh.appendChild(bd);}
  document.body.appendChild(gh);
  IBD={ids:ids,id:id,gh:gh,dy:e.clientY-r.top,dx:e.clientX-r.left,sc:row.closest('.db')||row.closest('.iblist'),pid:e.pointerId,t:null};
  S.drag=true;document.documentElement.classList.add('gdragging');
  try{h.setPointerCapture(e.pointerId);}catch(x){}
},{passive:false});
document.addEventListener('pointermove',function(e){
  if(!IBD||e.pointerId!==IBD.pid)return;e.preventDefault();
  IBD.gh.style.left=(e.clientX-IBD.dx)+'px';IBD.gh.style.top=(e.clientY-IBD.dy)+'px';
  [].forEach.call(document.querySelectorAll('.ibrow.gdover,.ibrow.gdafter'),function(x){x.classList.remove('gdover','gdafter');});
  var t=ibdTarget(e.clientX,e.clientY);IBD.t=t;if(t)t.row.classList.add(t.after?'gdafter':'gdover');
  if(IBD.sc){var sr=IBD.sc.getBoundingClientRect();if(e.clientY<sr.top+50)IBD.sc.scrollTop-=12;else if(e.clientY>sr.bottom-50)IBD.sc.scrollTop+=12;}
},{passive:false});
function ibdEnd(e,cancel){
  if(!IBD||(e&&e.pointerId!==IBD.pid))return;var g=IBD,t=g.t;ibdClear();IBD=null;S.drag=false;
  if(!cancel&&t&&!(g.ids.length===1&&(t.before===g.id)))ibMove(g.ids,t.before);
  S.dragDirty=false;render();
}
document.addEventListener('pointerup',function(e){ibdEnd(e,false);});
document.addEventListener('pointercancel',function(e){ibdEnd(e,true);});
