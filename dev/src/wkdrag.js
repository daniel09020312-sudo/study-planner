/* ---------- 할 일(주간 달력)에서 끌어 옮기기 ---------- */
var WD=null;
function wdOk(){return S.vtab==='cal'&&S.calMode==='list'&&!S.modal;}
function wkMove(from,id,to,beforeId){
  var V=view(),t=today();if(!V.me||!need())return;
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x.id===id;})[0];if(!g)return;
  function put(list,item){var j=beforeId?list.map(function(x){return x.id;}).indexOf(beforeId):-1;if(j<0)list.push(item);else list.splice(j,0,item);}
  if(from===to){
    editDay(from,function(d){var i=d.goals.map(function(x){return x.id;}).indexOf(id);if(i<0)return;var it=d.goals.splice(i,1)[0];put(d.goals,it);});
    return;
  }
  if(to<t){flash('지난 날로는 옮길 수 없습니다.');return;}
  if(dayOf(V,V.me,to).goals.length>=GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');return;}
  var sn=snap(['days/'+V.me+'_'+from,'days/'+V.me+'_'+to]);
  editDay(from,function(d){d.goals=d.goals.filter(function(x){return x.id!==id;});if(d.focus===id)d.focus=null;});
  editDay(to,function(d){var c=clone(g);c.done=false;delete c.ts;delete c.te;put(d.goals,c);});
  flash(shortDate(to)+' '+DOW[pd(to).getDay()]+'요일로 옮겼습니다.',sn);
}
function wdCancel(){if(!WD)return;clearTimeout(WD.timer);clearTimeout(WD.pt);if(WD.src)WD.src.classList.remove('press');WD=null;}
function wdEnd(){
  if(!WD)return;cancelAnimationFrame(WD.raf);clearTimeout(WD.timer);clearTimeout(WD.pt);
  if(WD.gh)WD.gh.remove();if(WD.ph)WD.ph.remove();
  if(WD.edges){WD.edges[-1].remove();WD.edges[1].remove();WD.edges=null;WD.er=null;}
  if(WD.src)WD.src.classList.remove('lifting','press');
  var cs=document.querySelectorAll('.wkc.over,.wkc.no');for(var i=0;i<cs.length;i++)cs[i].classList.remove('over','no');
  document.documentElement.classList.remove('wkdragging');
  S.drag=false;window.__ttDragEnd=Date.now();
}
function wdMarkPast(){
  var t=today(),cs=document.querySelectorAll('.wkc[data-d]');
  for(var i=0;i<cs.length;i++){var cd=cs[i].getAttribute('data-d');if(cd<t&&cd!==WD.d)cs[i].classList.add('no');}
}
/* 끄는 중에 주 바꾸기: 달력 양쪽 끝에 잠깐 대고 있으면 이전 주, 다음 주로 넘어간다 */
var WD_DWELL=520;
function wdCanFlip(dir){
  var ws=S.alWeek,nw=alClamp(addDays(ws,7*dir));
  if(nw===ws)return false;
  if(dir<0&&addDays(nw,6)<today())return false;
  return true;
}
function wdEdges(){
  WD.edges={};WD.er={};
  [-1,1].forEach(function(dir){
    var e=document.createElement('div');e.className='wkedge '+(dir>0?'r':'l');e.setAttribute('aria-hidden','true');
    e.innerHTML=dir>0?'<span>다음 주</span><b>&rsaquo;</b>':'<b>&lsaquo;</b><span>이전 주</span>';
    document.body.appendChild(e);WD.edges[dir]=e;
  });
  wdEdgeUpdate();
}
function wdEdgeUpdate(){
  if(!WD||!WD.edges)return;
  var sc=WD.sc||document.querySelector('.wkscroll'),W=window.innerWidth||1000,H=window.innerHeight||800;
  [-1,1].forEach(function(dir){
    var e=WD.edges[dir],show=false,r=null;
    if(sc&&document.body.contains(sc)&&wdCanFlip(dir)){
      var b=sc.getBoundingClientRect(),can=sc.scrollWidth>sc.clientWidth+2;
      var atEnd=!can||(dir>0?sc.scrollLeft+sc.clientWidth>=sc.scrollWidth-2:sc.scrollLeft<=1);
      var top=Math.max(b.top,8),bot=Math.min(b.bottom,H-8);
      if(atEnd&&bot-top>40){
        if(bot-top<140){var mid=(top+bot)/2;top=Math.max(8,mid-70);bot=Math.min(H-8,mid+70);}
        var left=dir>0?Math.min(b.right,W)-44:Math.max(b.left,0);
        r={l:left,t:top,r:left+44,b:bot};show=true;
      }
    }
    WD.er[dir]=r;
    if(show){e.style.left=r.l+'px';e.style.top=r.t+'px';e.style.height=(r.b-r.t)+'px';}
    if(e.classList.contains('on')!==show)e.classList.toggle('on',show);
    if(!show)e.classList.remove('arm');
  });
}
function wdInEdge(){
  if(!WD||!WD.er)return 0;
  for(var k=-1;k<=1;k+=2){var r=WD.er[k];if(r&&WD.x>=r.l-6&&WD.x<=r.r+6&&WD.y>=r.t&&WD.y<=r.b)return k;}
  return 0;
}
function wdFlip(dir){
  var ow=S.alWeek,nw=alClamp(addDays(ow,7*dir));if(nw===ow)return;
  if(WD.ph&&WD.ph.parentNode)WD.ph.remove();
  var prev=document.querySelector('.wkc.over');if(prev)prev.classList.remove('over');
  S.alWeek=nw;S.vbDir=dir;S.drag=false;render();S.drag=true;
  var sc=document.querySelector('.wkscroll');WD.sc=sc;
  if(sc&&sc.scrollWidth>sc.clientWidth+2)sc.scrollLeft=dir>0?0:sc.scrollWidth;
  var s2=document.getElementById('wi-'+WD.id);
  if(s2&&s2.getAttribute('data-d')===WD.d){WD.src=s2;s2.classList.add('lifting');}
  wdMarkPast();WD.tgt=null;
  if(navigator.vibrate)try{navigator.vibrate(8);}catch(e){}
}
function wdStart(){
  var src=WD.src;clearTimeout(WD.timer);clearTimeout(WD.pt);src.classList.remove('press');
  if(!document.body.contains(src)){WD=null;return;}
  WD.on=true;S.drag=true;document.documentElement.classList.add('wkdragging');
  WD.d=src.getAttribute('data-d');WD.id=src.getAttribute('data-id');WD.sc=src.closest('.wkscroll');
  var r=src.getBoundingClientRect(),gh=src.cloneNode(true);
  gh.removeAttribute('id');gh.classList.add('wkghost');gh.style.width=r.width+'px';gh.style.left=r.left+'px';gh.style.top=r.top+'px';
  document.body.appendChild(gh);WD.gh=gh;WD.h=r.height;
  var ph=document.createElement('div');ph.className='wkph';ph.style.height=r.height+'px';WD.ph=ph;
  src.classList.add('lifting');
  wdMarkPast();wdEdges();
  requestAnimationFrame(function(){if(WD&&WD.gh)WD.gh.classList.add('up');});
  wdAuto();wdMove();
}
function wdMove(){
  if(!WD||!WD.on)return;
  WD.gh.style.transform='translate3d('+(WD.x-WD.x0)+'px,'+(WD.y-WD.y0)+'px,0)';
  var cell=null,els=document.elementsFromPoint?document.elementsFromPoint(WD.x,WD.y):[];
  for(var i=0;i<els.length;i++){var c=els[i].closest&&els[i].closest('.wkc[data-d]');if(c){cell=c;break;}}
  if(cell&&cell.classList.contains('no'))cell=null;
  if(wdInEdge())cell=null;
  var prev=document.querySelector('.wkc.over');if(prev&&prev!==cell)prev.classList.remove('over');
  if(!cell){if(WD.ph.parentNode)WD.ph.remove();WD.tgt=null;return;}
  cell.classList.add('over');
  var items=[].slice.call(cell.querySelectorAll('.wki[data-id]')).filter(function(e){return e!==WD.src;}),before=null;
  for(var j=0;j<items.length;j++){var rr=items[j].getBoundingClientRect();if(WD.y<rr.top+rr.height/2){before=items[j];break;}}
  var anchor=before||cell.querySelector('.wkadd')||null;
  if(anchor){if(WD.ph.nextSibling!==anchor||WD.ph.parentNode!==cell)cell.insertBefore(WD.ph,anchor);}
  else if(WD.ph.parentNode!==cell||WD.ph.nextSibling)cell.appendChild(WD.ph);
  WD.tgt={d:cell.getAttribute('data-d'),before:before?before.getAttribute('data-id'):null};
}
function wdAuto(){
  if(!WD||!WD.on)return;
  var E=70,dy=0,dx=0,H=window.innerHeight||800;
  if(WD.y<E)dy=-Math.min(18,Math.ceil((E-WD.y)/4));else if(WD.y>H-E)dy=Math.min(18,Math.ceil((WD.y-(H-E))/4));
  if(dy&&main){var y0=main.scrollTop;main.scrollTop+=dy;if(main.scrollTop!==y0)wdMove();}
  var sc=WD.sc;
  if(sc&&sc.scrollWidth>sc.clientWidth+2){var r=sc.getBoundingClientRect();
    if(WD.x<r.left+40)dx=-Math.min(16,Math.ceil((r.left+40-WD.x)/3));else if(WD.x>r.right-40)dx=Math.min(16,Math.ceil((WD.x-(r.right-40))/3));
    if(dx){var x0=sc.scrollLeft;sc.scrollLeft+=dx;if(sc.scrollLeft!==x0)wdMove();}}
  wdEdgeUpdate();
  var ed=wdInEdge(),now=Date.now();
  if(ed&&now>(WD.cool||0)){
    if(!WD.fz||WD.fz.dir!==ed){if(WD.fz&&WD.edges[WD.fz.dir])WD.edges[WD.fz.dir].classList.remove('arm');WD.fz={dir:ed,t:now};WD.edges[ed].classList.add('arm');wdMove();}
    else if(now-WD.fz.t>=WD_DWELL){WD.edges[ed].classList.remove('arm');WD.fz=null;WD.cool=now+380;wdFlip(ed);wdEdgeUpdate();wdMove();}
  }else if(!ed&&WD.fz){if(WD.edges[WD.fz.dir])WD.edges[WD.fz.dir].classList.remove('arm');WD.fz=null;}
  WD.raf=requestAnimationFrame(wdAuto);
}
function wdDrop(){
  var R=WD,tg=R.tgt;wdEnd();WD=null;
  if(!tg){render();return;}
  if(tg.d===R.d&&tg.before===R.next){render();return;}
  wkMove(R.d,R.id,tg.d,tg.before);render();
}
document.addEventListener('pointerdown',function(e){
  if(WD||!wdOk()||e.button>0||e.isPrimary===false)return;
  var tg=e.target;if(!tg||!tg.closest)return;
  var src=tg.closest('.wki[data-wdrag]');if(!src||tg.closest('.wkchk'))return;
  var touch=e.pointerType==='touch',nx=src.nextElementSibling;
  WD={src:src,quick:!touch,id0:e.pointerId,x0:e.clientX,y0:e.clientY,x:e.clientX,y:e.clientY,on:false,next:nx&&nx.classList.contains('wki')?nx.getAttribute('data-id'):null};
  if(touch){WD.timer=setTimeout(function(){if(WD&&!WD.on)wdStart();},320);WD.pt=setTimeout(function(){if(WD&&!WD.on&&WD.src)WD.src.classList.add('press');},130);}
});
document.addEventListener('pointermove',function(e){
  if(!WD||e.pointerId!==WD.id0)return;
  WD.x=e.clientX;WD.y=e.clientY;
  if(!WD.on){
    var dist=Math.abs(WD.x-WD.x0)+Math.abs(WD.y-WD.y0);
    if(!WD.quick){if(dist>12)wdCancel();return;}
    if(dist<7)return;
    wdStart();
  }
  if(WD&&WD.on){e.preventDefault();wdMove();}
},{passive:false});
document.addEventListener('pointerup',function(e){if(!WD||e.pointerId!==WD.id0)return;if(WD.on)wdDrop();else wdCancel();});
document.addEventListener('pointercancel',function(e){if(!WD||e.pointerId!==WD.id0)return;if(WD.on){wdEnd();WD=null;render();}else wdCancel();});
document.addEventListener('touchmove',function(e){if(WD&&WD.on)e.preventDefault();},{passive:false});
document.addEventListener('contextmenu',function(e){if(WD)e.preventDefault();});
