# ---------------------------------------------------------------- 처음 열 때 잠깐 보이는 화면
# 앱 아이콘 안의 그림(달력 테두리, 머리줄, 고리, 체크)을 붓글씨 획순대로 한 획씩 써 나간다.
# ㅁ 쓰는 순서: 왼쪽 세로 -> 위와 오른쪽(ㄱ) -> 아래. 그다음 머리줄, 고리 둘, 마지막에 체크.
# 납작붓처럼 지나가는 방향에 따라 굵기가 바뀌고, 처음엔 눌러 시작해 끝은 가늘게 뺀다.
# 그림은 앱이 준비되는 동안 계속 그려지고, 다 그린 뒤 준비가 끝나면 사라진다. 누르면 바로 넘어간다.
_SP_HTML = """<div id="splash" role="status" aria-label="공부방을 여는 중"><div class="spin"><svg class="spdraw" viewBox="84 70 344 352" aria-hidden="true"><defs><clipPath id="sp-cc"><rect x="112" y="132" width="288" height="270" rx="58"/></clipPath><filter id="sp-rough" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="6" xChannelSelector="R" yChannelSelector="G"/></filter></defs><g clip-path="url(#sp-cc)"><rect class="spwash" x="112" y="132" width="288" height="80"/></g><g class="spink" filter="url(#sp-rough)"></g></svg><b class="spt">공부방</b></div></div>
<script>
(function(){
window.__sp0=Date.now();
var sp=document.getElementById('splash');if(!sp)return;
var svg=sp.querySelector('.spdraw'),ink=sp.querySelector('.spink'),wash=sp.querySelector('.spwash'),txt=sp.querySelector('.spt'),NS='http://www.w3.org/2000/svg';
var red=false;try{red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
sp.addEventListener('click',function(){if(window.__spGo)window.__spGo();});
function out(t){return 1-Math.pow(1-t,3);}
function sine(t){return .5-.5*Math.cos(Math.PI*t);}
function io(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
function seg(t,a,b){var x=(t-a)/(b-a);return x<0?0:x>1?1:x;}
function press(a,inn,o,end){return function(t){return t<inn?a+(1-a)*out(t/inn):t>1-o?1-(1-end)*sine((t-(1-o))/o):1;};}
function brush(d,o){
  var g=document.createElementNS(NS,'path');g.setAttribute('d',d);g.setAttribute('fill','none');ink.appendChild(g);
  var L=g.getTotalLength(),N=Math.max(12,Math.ceil(L/2.5)),phi=(o.phi==null?35:o.phi)*Math.PI/180,mn=o.min||.34,pr=o.p||press(.55,.14,.2,.45),C=[],T=[],W=[],Ws=[],Lp=[],Rp=[],i,k;
  for(i=0;i<=N;i++){var s=L*i/N,a=g.getPointAtLength(Math.max(0,s-1.5)),b=g.getPointAtLength(Math.min(L,s+1.5)),c=g.getPointAtLength(s),tx=b.x-a.x,ty=b.y-a.y,m=Math.sqrt(tx*tx+ty*ty)||1;tx/=m;ty/=m;C.push([c.x,c.y]);T.push([tx,ty]);W.push(o.w*(mn+(1-mn)*Math.abs(Math.sin(Math.atan2(ty,tx)-phi))));}
  for(i=0;i<=N;i++){var sum=0,n=0;for(k=-3;k<=3;k++){if(i+k>=0&&i+k<=N){sum+=W[i+k];n++;}}Ws.push(sum/n*pr(i/N)/2);}
  for(i=0;i<=N;i++){var nx=-T[i][1],ny=T[i][0];Lp.push([C[i][0]+nx*Ws[i],C[i][1]+ny*Ws[i]]);Rp.push([C[i][0]-nx*Ws[i],C[i][1]-ny*Ws[i]]);}
  ink.removeChild(g);
  var sh=document.createElementNS(NS,'path');if(o.cls)sh.setAttribute('class',o.cls);ink.appendChild(sh);
  function f(q){return q[0].toFixed(1)+' '+q[1].toFixed(1);}
  return {L:L,draw:function(u){
    if(u<=0){sh.setAttribute('d','');return;}
    var m=Math.max(1,Math.round(u*N)),r=Ws[m].toFixed(1),r0=Ws[0].toFixed(1),dd='M'+f(Lp[0]),i;
    for(i=1;i<=m;i++)dd+='L'+f(Lp[i]);
    dd+='A'+r+' '+r+' 0 0 0 '+f(Rp[m]);
    for(i=m-1;i>=0;i--)dd+='L'+f(Rp[i]);
    sh.setAttribute('d',dd+'A'+r0+' '+r0+' 0 0 0 '+f(Lp[0])+'Z');
  }};
}
try{
  var D=[
    {d:'M129 149 A58 58 0 0 0 112 190 L112 344',w:27},
    {d:'M129 149 A58 58 0 0 1 170 132 L342 132 A58 58 0 0 1 400 190 L400 350',w:27},
    {d:'M112 344 A58 58 0 0 0 170 402 L342 402 A58 58 0 0 0 400 344',w:27},
    {d:'M120 212 L392 212',w:20,p:press(.5,.12,.25,.35)},
    {d:'M191 100 L191 170',w:32,p:press(.7,.2,.35,.4)},
    {d:'M321 100 L321 170',w:32,p:press(.7,.2,.35,.4)},
    {d:'M186 300 L236 346 L328 252',w:40,phi:0,min:.45,p:press(.6,.12,.4,.1),cls:'spck'}
  ];
  var B=D.map(function(x){return brush(x.d,x);}),t=70,S=B.map(function(b){var s={a:t,b:t+50+b.L/2.8};t=s.b+35;return s;}),T1=t-35,TOTAL=T1+460;
  var frame=function(n){
    for(var i=0;i<B.length;i++)B[i].draw(sine(seg(n,S[i].a,S[i].b)));
    var w=seg(n,T1-60,T1+320);wash.style.opacity=(.9*out(w)).toFixed(3);wash.setAttribute('transform','translate(112 0) scale('+(.2+.8*out(w)).toFixed(4)+' 1) translate(-112 0)');
    var k=seg(n,T1,T1+420);svg.style.transform='scale('+(1+.035*Math.sin(Math.PI*k)).toFixed(4)+')';
    var x=seg(n,T1-80,T1+420);txt.style.opacity=x>.03?1:0;txt.style.clipPath='inset(-30% '+(100-100*io(x)).toFixed(1)+'% -30% 0)';
  };
  if(red){frame(TOTAL);window.__spEnd=0;return;}
  frame(0);window.__spEnd=Date.now()+TOTAL+400;
  var t0=null;
  var step=function(now){if(t0===null){t0=now;window.__spEnd=Date.now()+TOTAL;}var n=now-t0;frame(Math.min(n,TOTAL));if(n<TOTAL)requestAnimationFrame(step);};
  requestAnimationFrame(step);
}catch(e){window.__spEnd=0;txt.style.opacity=1;}
})();
</script>"""
sub("<body>", "<body>\n" + _SP_HTML)
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);", """  if(S.ready||S.setup||S.join)splashDone();
  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);""")
sub("/* ---------- 공부방 ---------- */", r"""/* ---------- 처음 화면 ---------- */
// 붓글씨 그림이 끝날 때(__spEnd)까지 기다렸다가 사라진다. 준비된 뒤에는 화면을 누르면 바로 넘어간다
function splashDone(){
  var sp=document.getElementById('splash');if(!sp||sp.getAttribute('data-out'))return;
  sp.setAttribute('data-out','1');
  var go=function(){if(sp.classList.contains('out'))return;sp.classList.add('out');setTimeout(function(){if(sp.parentNode)sp.parentNode.removeChild(sp);},reduced?0:520);};
  window.__spGo=go;
  setTimeout(go,reduced?0:Math.max(0,(window.__spEnd||0)-Date.now())+220);
}
setTimeout(function(){var sp=document.getElementById('splash');if(sp&&!sp.getAttribute('data-out'))splashDone();},8000);
/* ---------- 공부방 ---------- */""")
sub("</style>", """#splash{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:var(--bg);transition:opacity .45s ease,visibility .45s;-webkit-tap-highlight-color:transparent}
#splash.out{opacity:0;visibility:hidden}
#splash .spin{display:flex;flex-direction:column;align-items:center;gap:8px;transition:transform .5s cubic-bezier(.3,1.4,.5,1)}
#splash.out .spin{transform:scale(1.06)}
.spdraw{display:block;width:118px;height:121px;overflow:visible;transform-origin:50% 55%}
.spink path{fill:var(--ink);fill:color-mix(in srgb,var(--accent) 30%,var(--ink))}
.spink path.spck{fill:var(--accent)}
.spwash{fill:var(--accent-soft);opacity:0}
.spt{font-size:17px;font-weight:800;letter-spacing:.08em;color:var(--ink);opacity:0}
@media (prefers-reduced-motion:reduce){#splash,#splash .spin{transition:none}}
</style>""")
