/* ---------- v109: 다 같이 쓰는 손글씨 화이트보드. 획 하나가 문서 하나: wb/<id>={by,c,w,k:'p'|'h',p:'x,y,x,y..',at} ---------- */
var WB_W=12800,WB_H=8000,WB_MAX=8000,WB_PTS=1500;
var WB_COLORS=['#1F2328','#E5484D','#F76B15','#E8B500','#30A46C','#0090FF','#6E56CF','#D6409F','#8D6E63'];
/* 굵기는 화면에서 보이는 굵기(px). 저장은 그때 배율로 나눈 판 굵기 */
var WB_SIZES=[['s',2.5,'가늘게'],['m',5,'보통'],['l',10,'굵게']];
var WB={open:false,tool:'p',color:WB_COLORS[0],size:'m',cam:null,undo:[],seen:null,ref:null,penSeen:false,clr:0};
function wbList(V){
  var o=obj(V.wb),a=[];
  for(var k in o){var s=o[k];if(s&&typeof s.p==='string'&&s.p)a.push({id:k,by:s.by,c:s.c,w:+s.w||6,k:s.k,p:s.p,at:+s.at||0});}
  return a.sort(function(x,y){return x.at-y.at||(x.id<y.id?-1:1);});
}
function wbPts(s){if(s._pts)return s._pts;var a=s.p.split(','),r=[];for(var i=0;i+1<a.length;i+=2)r.push([+a[i],+a[i+1]]);var bx=[1e9,1e9,-1e9,-1e9];r.forEach(function(q){if(q[0]<bx[0])bx[0]=q[0];if(q[1]<bx[1])bx[1]=q[1];if(q[0]>bx[2])bx[2]=q[0];if(q[1]>bx[3])bx[3]=q[1];});s._bx=bx;return s._pts=r;}
function wbPath(ctx,pts,tr){
  ctx.beginPath();var p0=tr(pts[0]);ctx.moveTo(p0[0],p0[1]);
  if(pts.length===1){ctx.lineTo(p0[0]+.01,p0[1]);return;}
  if(pts.length===2){var p1=tr(pts[1]);ctx.lineTo(p1[0],p1[1]);return;}
  for(var i=1;i<pts.length-1;i++){var a=tr(pts[i]),b=tr(pts[i+1]);ctx.quadraticCurveTo(a[0],a[1],(a[0]+b[0])/2,(a[1]+b[1])/2);}
  var e=tr(pts[pts.length-1]);ctx.lineTo(e[0],e[1]);
}
function wbStroke(ctx,s,z,tr){
  var pts=wbPts(s);if(!pts.length)return;
  ctx.save();ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=s.c||'#1F2328';
  if(s.k==='h'){ctx.globalAlpha=.32;ctx.lineCap='butt';ctx.lineWidth=Math.max(1,s.w*2.6*z);}else ctx.lineWidth=Math.max(.6,s.w*z);
  wbPath(ctx,pts,tr);ctx.stroke();ctx.restore();
}
/* 게시판 카드: 작은 미리 보기(바뀔 때만 다시 그린 그림) */
var WBP={key:'',url:''};
function wbPreview(V){
  var l=wbList(V),key=l.length+'|'+(l.length?l[l.length-1].id+l[0].id:'');
  if(WBP.key===key)return WBP.url;
  try{
    var c=document.createElement('canvas'),W=480,H=300;c.width=W;c.height=H;var x=c.getContext('2d');
    x.fillStyle='#FFFFFF';x.fillRect(0,0,W,H);
    var ll=l.slice(-600),bb=wbBox(ll);if(bb){var z=Math.min(W/bb[2],H/bb[3],.5),ox=bb[0]-(W/z-bb[2])/2,oy=bb[1]-(H/z-bb[3])/2;
    ll.forEach(function(s){wbStroke(x,s,z*1.3,function(q){return [(q[0]-ox)*z,(q[1]-oy)*z];});});}
    WBP.url=c.toDataURL('image/png');
  }catch(e){WBP.url='';}
  WBP.key=key;return WBP.url;
}
/* 쓴 곳 범위 [x,y,w,h](여백 포함) */
function wbBox(l){if(!l.length)return null;var b=[1e9,1e9,-1e9,-1e9];l.forEach(function(s){wbPts(s);var q=s._bx;b[0]=Math.min(b[0],q[0]);b[1]=Math.min(b[1],q[1]);b[2]=Math.max(b[2],q[2]);b[3]=Math.max(b[3],q[3]);});var pad=150;return [b[0]-pad,b[1]-pad,Math.max(600,b[2]-b[0]+pad*2),Math.max(400,b[3]-b[1]+pad*2)];}
function wbCard(V,k){
  if(!V.me)return '';
  var l=wbList(V),who={};l.forEach(function(s){if(s.by)who[s.by]=1;});
  var last=l.length?l[l.length-1]:null,url=wbPreview(V);
  var h='<section class="card wbc" id="c-wb" style="--k:'+(k||1)+'"><div class="ct"><h2>화이트보드<small>모두 같이 손글씨로 쓰는 넓은 판</small></h2>'+(l.length?'<span class="tag">'+Object.keys(who).length+'명</span>':'')+'</div>';
  h+='<button class="wbprev" data-act="wb-open" aria-label="화이트보드 열기">'+(url?'<img src="'+url+'" alt="" width="480" height="300">':'')+(l.length?'':'<span>아직 아무도 쓰지 않았습니다. 눌러서 먼저 써 보세요.</span>')+'</button>';
  h+='<div class="row wbrow"><small class="muted">'+(last?'마지막: '+esc((V.byId[last.by]||{name:'누군가'}).name)+' · '+esc(agoLabel(last.at)):'펜, 형광펜, 지우개')+'</small><button class="btn small primary" data-act="wb-open">열기</button></div></section>';
  return h;
}
function agoLabel(t){var m=Math.round((Date.now()-t)/60000);if(m<1)return '방금';if(m<60)return m+'분 전';var hh=Math.round(m/60);if(hh<24)return hh+'시간 전';return Math.round(hh/24)+'일 전';}
/* 화면 가득 여는 판: body에 붙은 #wbDock, 앱 render와 따로 그림 */
function wbOpen(){
  if(WB.open)return;var V=view();if(!V.me)return;
  WB.open=true;WB.undo=[];WB.seen=null;WB.ref=null;
  var d=document.createElement('div');d.id='wbDock';d.setAttribute('role','dialog');d.setAttribute('aria-label','화이트보드');
  var cs=WB_COLORS.map(function(c){return '<button class="wbsw" data-w="color" data-v="'+c+'" style="--c:'+c+'" aria-label="색 '+c+'"></button>';}).join('');
  var sz=WB_SIZES.map(function(x){return '<button class="wbsz" data-w="size" data-v="'+x[0]+'" aria-label="'+x[2]+'"><i style="width:'+(x[1]+3)+'px;height:'+(x[1]+3)+'px"></i></button>';}).join('');
  var tl=[['p','펜','<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>'],['h','형광펜','<path d="M5 19h6"/><path d="M8 16l-2-2 9-9 4 4-9 9z"/>'],['e','지우개','<path d="M7 20h12"/><path d="M5 15l8-8 5 5-6 6H8z"/>'],['m','이동','<path d="M12 3v18M3 12h18"/><path d="M9 6l3-3 3 3M9 18l3 3 3-3M6 9l-3 3 3 3M18 9l3 3-3 3"/>']]
    .map(function(t){return '<button class="wbt" data-w="tool" data-v="'+t[0]+'" aria-label="'+t[1]+'" title="'+t[1]+'"><svg viewBox="0 0 24 24" aria-hidden="true">'+t[2]+'</svg><span>'+t[1]+'</span></button>';}).join('');
  d.innerHTML='<div class="wbtop"><b>화이트보드</b><small id="wbInfo"></small><span class="wbsp"></span><button class="btn small" data-w="undo">되돌리기</button><button class="btn small" data-w="fit">쓴 곳 보기</button><button class="btn small wball" data-w="all">판 전체</button><span class="wbzoom"><button class="btn small" data-w="zout" aria-label="작게">-</button><small id="wbZ">100%</small><button class="btn small" data-w="zin" aria-label="크게">+</button></span>'+(adminId(V)===V.me?'<button class="btn small danger" data-w="clear" id="wbClr">모두 지우기</button>':'')+'<button class="btn small primary" data-w="close">닫기</button></div>'+
    '<div class="wbstage" id="wbStage"><canvas id="wbBase"></canvas><canvas id="wbLive"></canvas><div id="wbTags"></div></div>'+
    '<div class="wbbar"><div class="wbtools">'+tl+'</div><div class="wbcols">'+cs+'</div><div class="wbsizes">'+sz+'</div></div>';
  document.body.appendChild(d);document.documentElement.classList.add('wbon');
  d.addEventListener('click',wbClick);
  var st=document.getElementById('wbStage');
  st.addEventListener('pointerdown',wbDown);st.addEventListener('pointermove',wbMove);st.addEventListener('pointerup',wbUp);st.addEventListener('pointercancel',wbUp);
  st.addEventListener('wheel',wbWheel,{passive:false});
  addEventListener('keydown',wbKey,true);addEventListener('resize',wbResize);
  wbResize();wbFit(true);wbUi();wbSync(true);
}
function wbClose(){
  var d=document.getElementById('wbDock');if(d)d.parentNode.removeChild(d);
  WB.open=false;WB.cur=null;WB.ptr={};document.documentElement.classList.remove('wbon');
  removeEventListener('keydown',wbKey,true);removeEventListener('resize',wbResize);render();
}
function wbKey(e){
  if(!WB.open)return;
  if(e.key==='Escape'){e.preventDefault();e.stopPropagation();wbClose();return;}
  if((e.ctrlKey||e.metaKey)&&(e.key==='z'||e.key==='Z')){e.preventDefault();e.stopPropagation();wbUndo();return;}
  var tg=e.target;if(tg&&/^(INPUT|TEXTAREA)$/.test(tg.tagName))return;
  e.stopPropagation();
}
function wbUi(){
  var d=document.getElementById('wbDock');if(!d)return;
  d.querySelectorAll('[data-w="tool"]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-v')===WB.tool?'true':'false');});
  d.querySelectorAll('[data-w="color"]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-v')===WB.color?'true':'false');});
  d.querySelectorAll('[data-w="size"]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-v')===WB.size?'true':'false');});
  d.className=WB.tool==='e'?'erase':WB.tool==='m'?'move':'';
  var z=document.getElementById('wbZ');if(z&&WB.cam)z.textContent=Math.round(WB.cam.z*100)+'%';
  var c=document.getElementById('wbClr');if(c)c.textContent=WB.clr&&Date.now()-WB.clr<4000?'한 번 더 누르면 모두 지움':'모두 지우기';
}
function wbClick(e){
  var b=e.target.closest&&e.target.closest('[data-w]');if(!b)return;e.stopPropagation();
  var w=b.getAttribute('data-w'),v=b.getAttribute('data-v');
  if(w==='tool')WB.tool=v;
  else if(w==='color'){WB.color=v;if(WB.tool==='e'||WB.tool==='m')WB.tool='p';}
  else if(w==='size'){WB.size=v;if(WB.tool==='e'||WB.tool==='m')WB.tool='p';}
  else if(w==='undo')wbUndo();
  else if(w==='fit'){wbFit(true);wbDraw();}
  else if(w==='all'){wbFit();wbDraw();}
  else if(w==='zin'||w==='zout'){var st=document.getElementById('wbStage');wbZoomAt(st.clientWidth/2,st.clientHeight/2,w==='zin'?1.25:.8);}
  else if(w==='clear')wbClear();
  else if(w==='close'){wbClose();return;}
  wbUi();
}
function wbResize(){
  var st=document.getElementById('wbStage');if(!st)return;
  var r=window.devicePixelRatio||1,W=st.clientWidth,H=st.clientHeight;WB.dpr=r;
  ['wbBase','wbLive'].forEach(function(id){var c=document.getElementById(id);c.width=Math.round(W*r);c.height=Math.round(H*r);c.style.width=W+'px';c.style.height=H+'px';});
  var fz=Math.min(W/WB_W,H/WB_H);WB.fitZ=fz;if(WB.cam)wbClamp();
  wbDraw();
}
function wbFit(first){var st=document.getElementById('wbStage');if(!st)return;var W=st.clientWidth,H=st.clientHeight,z=Math.min(W/WB_W,H/WB_H);WB.fitZ=z;WB.cam={z:z,x:-(W/z-WB_W)/2,y:-(H/z-WB_H)/2};
  /* 세로 화면은 처음에 판 높이를 채워 왼쪽부터(옆으로 밀어 봄) */
  /* 처음 열 때는 쓴 곳(없으면 판 가운데)을 알맞은 배율로 */
  if(first){var bb=wbBox(wbList(V0||view()));if(!bb)bb=[WB_W/2-W/1.2,WB_H/2-H/1.2,W/.6,H/.6];var zz=Math.max(z,Math.min(W/bb[2],H/bb[3],1));WB.cam={z:zz,x:bb[0]+bb[2]/2-W/zz/2,y:bb[1]+bb[3]/2-H/zz/2};wbClamp();}wbUi();}
function wbClamp(){var st=document.getElementById('wbStage'),c=WB.cam;if(!st||!c)return;var mn=WB.fitZ*.8,mx=4;c.z=Math.max(mn,Math.min(mx,c.z));var vw=st.clientWidth/c.z,vh=st.clientHeight/c.z,m=200;
  c.x=vw>=WB_W?-(vw-WB_W)/2:Math.max(-m,Math.min(WB_W+m-vw,c.x));c.y=vh>=WB_H?-(vh-WB_H)/2:Math.max(-m,Math.min(WB_H+m-vh,c.y));}
function wbZoomAt(sx,sy,f){var c=WB.cam,bx=sx/c.z+c.x,by=sy/c.z+c.y;c.z*=f;wbClamp();c.x=bx-sx/c.z;c.y=by-sy/c.z;wbClamp();wbDraw();wbUi();}
function wbTr(){var c=WB.cam,r=WB.dpr||1;return function(q){return [(q[0]-c.x)*c.z*r,(q[1]-c.y)*c.z*r];};}
function wbDraw(){
  if(!WB.open||!WB.cam)return;if(WB.raf)return;
  WB.raf=requestAnimationFrame(function(){WB.raf=0;wbDrawNow();});
}
function wbDrawNow(){
  var cv=document.getElementById('wbBase');if(!cv||!WB.cam)return;
  var x=cv.getContext('2d'),c=WB.cam,r=WB.dpr||1,z=c.z*r,tr=wbTr();
  x.setTransform(1,0,0,1,0,0);x.fillStyle='#E9EAEE';x.fillRect(0,0,cv.width,cv.height);
  var o=tr([0,0]);x.fillStyle='#FFFFFF';x.shadowColor='rgba(0,0,0,.12)';x.shadowBlur=12*r;x.fillRect(o[0],o[1],WB_W*z,WB_H*z);x.shadowBlur=0;
  var g=25;while(g*z<26*r)g*=2;x.fillStyle='rgba(30,35,45,.13)';var dr=Math.max(.8,1.1*r);
  var vx0=Math.max(0,c.x),vy0=Math.max(0,c.y),vx1=Math.min(WB_W,c.x+cv.width/z),vy1=Math.min(WB_H,c.y+cv.height/z);
  for(var gx=Math.ceil(vx0/g)*g;gx<=vx1;gx+=g)for(var gy=Math.ceil(vy0/g)*g;gy<=vy1;gy+=g){var p=tr([gx,gy]);x.fillRect(p[0]-dr/2,p[1]-dr/2,dr,dr);}
  (WB.list||[]).forEach(function(s){wbPts(s);var b=s._bx,pad=s.w*3;if(b[2]+pad<c.x||b[0]-pad>c.x+cv.width/z||b[3]+pad<c.y||b[1]-pad>c.y+cv.height/z)return;wbStroke(x,s,z,tr);});
  wbLiveDraw();
}
function wbLiveDraw(){
  var cv=document.getElementById('wbLive');if(!cv)return;var x=cv.getContext('2d');x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,cv.width,cv.height);
  if(WB.cur&&WB.cur.pts.length)wbStroke(x,{c:WB.cur.c,w:WB.cur.w,k:WB.cur.k,_pts:WB.cur.pts,_bx:[0,0,0,0]},WB.cam.z*(WB.dpr||1),wbTr());
  if(WB.er){var p=WB.er,rr=wbErR()*WB.cam.z*(WB.dpr||1);x.beginPath();x.arc(p[0]*(WB.dpr||1),p[1]*(WB.dpr||1),rr,0,7);x.strokeStyle='rgba(0,0,0,.35)';x.lineWidth=1.2*(WB.dpr||1);x.stroke();}
}
/* 앱 render 뒤: 기록이 바뀌었을 때만 다시 그림 */
function wbSync(force){
  if(!WB.open)return;var V=V0||view();
  /* 받은 기록은 같은 묶음을 고쳐 쓰기도 해서, 묶음이 같아도 열쇠 목록으로 바뀜을 봄 */
  var o=obj(V.wb),key=Object.keys(o).join(',');
  if(!force&&o===WB.ref&&key===WB.key)return;WB.ref=o;WB.key=key;
  var old={};(WB.list||[]).forEach(function(s){old[s.id]=s;});
  var l=wbList(V);l.forEach(function(s,i){var o=old[s.id];if(o&&o.p===s.p){o.at=s.at;l[i]=o;}});
  var fresh=[];if(WB.seen){l.forEach(function(s){if(!WB.seen[s.id]&&s.by&&s.by!==V.me&&Date.now()-s.at<30000)fresh.push(s);});}
  WB.seen={};l.forEach(function(s){WB.seen[s.id]=1;});
  WB.list=l;wbDraw();
  var who={};l.forEach(function(s){if(s.by)who[s.by]=1;});
  var inf=document.getElementById('wbInfo');if(inf)inf.textContent=l.length?Object.keys(who).length+'명 · '+l.length+'획':'첫 글씨를 써 보세요';
  fresh.slice(-4).forEach(function(s){wbTag(s,V);});
}
function wbTag(s,V){
  var box=document.getElementById('wbTags');if(!box||!WB.cam)return;var pts=wbPts(s),q=pts[pts.length-1],c=WB.cam;
  var t=document.createElement('span');t.className='wbtag';t.textContent=(V.byId[s.by]||{name:'누군가'}).name;
  t.style.left=((q[0]-c.x)*c.z)+'px';t.style.top=((q[1]-c.y)*c.z)+'px';t.style.setProperty('--c',s.c||'#333');box.appendChild(t);
  setTimeout(function(){t.classList.add('out');},2600);setTimeout(function(){if(t.parentNode)t.parentNode.removeChild(t);},3200);
}
function wbPt(e){var st=document.getElementById('wbStage').getBoundingClientRect();return [e.clientX-st.left,e.clientY-st.top];}
function wbB(p){var c=WB.cam;return [p[0]/c.z+c.x,p[1]/c.z+c.y];}
function wbErR(){return 14/WB.cam.z;}
WB.ptr={};
function wbDown(e){
  if(!WB.cam)return;
  if(e.pointerType==='pen')WB.penSeen=true;
  try{e.currentTarget.setPointerCapture(e.pointerId);}catch(x){}
  WB.ptr[e.pointerId]={p:wbPt(e),t:e.pointerType};
  var n=Object.keys(WB.ptr).length;
  if(n>=2){if(WB.cur&&WB.cur.t==='touch')WB.cur=null;WB.er=null;wbGestureStart();wbLiveDraw();return;}
  var draw=(WB.tool!=='m')&&e.button===0&&!(WB.penSeen&&e.pointerType==='touch');
  if(!draw){WB.pan={p:wbPt(e),x:WB.cam.x,y:WB.cam.y};return;}
  e.preventDefault();
  if(WB.tool==='e'){WB.er=wbPt(e);WB.erasing=true;wbErase(wbB(WB.er));wbLiveDraw();return;}
  var V=view();if(!need())return;
  if((WB.list||[]).length>=WB_MAX){flash('화이트보드가 가득 찼습니다(획 '+WB_MAX+'개). 지우개로 정리해 주세요.');return;}
  var sz=WB_SIZES.filter(function(x){return x[0]===WB.size;})[0]||WB_SIZES[1];
  var b=wbB(wbPt(e));WB.cur={id:e.pointerId,t:e.pointerType,c:WB.color,w:Math.round(sz[1]/WB.cam.z*100)/100,k:WB.tool==='h'?'h':'p',pts:[wbQ(b)]};
  wbLiveDraw();
}
/* 점 저장: 크게 볼 때는 소수 한 자리 */
function wbQ(b){var k=WB.cam&&WB.cam.z>1.2?10:1;return [Math.round(b[0]*k)/k,Math.round(b[1]*k)/k];}
function wbGestureStart(){var ks=Object.keys(WB.ptr).slice(0,2),a=WB.ptr[ks[0]].p,b=WB.ptr[ks[1]].p;WB.pan=null;WB.gs={d:Math.hypot(a[0]-b[0],a[1]-b[1])||1,m:[(a[0]+b[0])/2,(a[1]+b[1])/2],cam:{x:WB.cam.x,y:WB.cam.y,z:WB.cam.z}};}
function wbMove(e){
  var P=WB.ptr[e.pointerId];if(P)P.p=wbPt(e);
  if(WB.gs&&Object.keys(WB.ptr).length>=2){
    var ks=Object.keys(WB.ptr).slice(0,2),a=WB.ptr[ks[0]].p,b=WB.ptr[ks[1]].p,g=WB.gs,d=Math.hypot(a[0]-b[0],a[1]-b[1])||1,m=[(a[0]+b[0])/2,(a[1]+b[1])/2];
    var bx=g.m[0]/g.cam.z+g.cam.x,by=g.m[1]/g.cam.z+g.cam.y,c=WB.cam;c.z=g.cam.z*d/g.d;wbClamp();c.x=bx-m[0]/c.z;c.y=by-m[1]/c.z;wbClamp();wbDraw();wbUi();return;
  }
  if(WB.pan&&P){var c2=WB.cam;c2.x=WB.pan.x-(P.p[0]-WB.pan.p[0])/c2.z;c2.y=WB.pan.y-(P.p[1]-WB.pan.p[1])/c2.z;wbClamp();wbDraw();return;}
  if(WB.tool==='e'&&e.pointerType!=='touch'||WB.erasing){WB.er=wbPt(e);if(WB.erasing&&P)wbErase(wbB(WB.er));wbLiveDraw();return;}
  var cur=WB.cur;if(!cur||cur.id!==e.pointerId)return;e.preventDefault();
  var evs=e.getCoalescedEvents?e.getCoalescedEvents():[e];if(!evs.length)evs=[e];
  evs.forEach(function(ev){var b=wbB(wbPt(ev)),l=cur.pts[cur.pts.length-1],q=wbQ(b);if((Math.abs(q[0]-l[0])+Math.abs(q[1]-l[1]))*WB.cam.z>=1.6&&cur.pts.length<WB_PTS)cur.pts.push(q);});
  wbLiveDraw();
}
function wbUp(e){
  delete WB.ptr[e.pointerId];
  if(WB.gs){if(Object.keys(WB.ptr).length<2)WB.gs=null;WB.pan=null;return;}
  if(WB.pan){WB.pan=null;return;}
  if(WB.erasing){WB.erasing=false;if(e.pointerType==='touch')WB.er=null;wbLiveDraw();return;}
  var cur=WB.cur;if(!cur||cur.id!==e.pointerId)return;WB.cur=null;
  var V=view(),id=rid('w'),s={by:V.me,c:cur.c,w:cur.w,k:cur.k,p:cur.pts.map(function(q){return Math.max(-200,Math.min(WB_W+200,q[0]))+','+Math.max(-200,Math.min(WB_H+200,q[1]));}).join(','),at:Date.now()};
  var ls={id:id,by:s.by,c:s.c,w:s.w,k:s.k,p:s.p,at:s.at};WB.list=(WB.list||[]).concat([ls]);if(WB.seen)WB.seen[id]=1;
  wbDrawNow();WB.undo.push({a:'add',id:id});if(WB.undo.length>200)WB.undo.shift();
  save('wb/'+id,s);
}
function wbErase(b){
  var r=wbErR(),hit=[];
  (WB.list||[]).forEach(function(s){var pts=wbPts(s),bx=s._bx,pad=r+s.w*(s.k==='h'?1.3:.5);if(b[0]<bx[0]-pad||b[0]>bx[2]+pad||b[1]<bx[1]-pad||b[1]>bx[3]+pad)return;
    for(var i=0;i<pts.length;i++){var p=pts[i],q=pts[i+1]||p,dx=q[0]-p[0],dy=q[1]-p[1],L=dx*dx+dy*dy,t=L?Math.max(0,Math.min(1,((b[0]-p[0])*dx+(b[1]-p[1])*dy)/L)):0,ex=p[0]+t*dx-b[0],ey=p[1]+t*dy-b[1];if(ex*ex+ey*ey<=pad*pad){hit.push(s);return;}}});
  if(!hit.length||!need())return;
  var ids={};hit.forEach(function(s){ids[s.id]=1;WB.undo.push({a:'del',id:s.id,d:{by:s.by,c:s.c,w:s.w,k:s.k,p:s.p,at:s.at}});save('wb/'+s.id,null);});
  WB.list=WB.list.filter(function(s){return !ids[s.id];});wbDrawNow();
}
function wbUndo(){
  var u=WB.undo.pop();if(!u){flash('되돌릴 것이 없습니다.');return;}if(!need())return;
  if(u.a==='add'){save('wb/'+u.id,null);WB.list=(WB.list||[]).filter(function(s){return s.id!==u.id;});}
  else{save('wb/'+u.id,u.d);WB.list=(WB.list||[]).concat([Object.assign({id:u.id},u.d)]).sort(function(x,y){return x.at-y.at;});}
  wbDrawNow();
}
function wbClear(){
  var V=view();if(adminId(V)!==V.me||!need())return;
  if(!WB.clr||Date.now()-WB.clr>4000){WB.clr=Date.now();setTimeout(wbUi,4100);return;}
  WB.clr=0;var l=wbList(V);l.forEach(function(s){save('wb/'+s.id,null);});WB.undo=[];WB.list=[];wbDrawNow();flash('화이트보드를 모두 지웠습니다.');
}
function wbWheel(e){
  if(!WB.cam)return;e.preventDefault();var p=wbPt(e);
  if(e.ctrlKey||e.metaKey){wbZoomAt(p[0],p[1],Math.exp(-e.deltaY*.0025));return;}
  var c=WB.cam;c.x+=(e.shiftKey?e.deltaY:e.deltaX)/c.z;if(!e.shiftKey)c.y+=e.deltaY/c.z;wbClamp();wbDraw();
}
