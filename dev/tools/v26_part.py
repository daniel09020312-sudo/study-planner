# ---------------------------------------------------------------- 처음 열 때 잠깐 보이는 화면
# 앱 아이콘 안의 그림(달력 테두리, 머리줄, 고리, 체크)을 붓글씨 획순대로 한 획씩 써 나간다.
# ㅁ 쓰는 순서: 왼쪽 세로 -> 위와 오른쪽(ㄱ) -> 아래. 그다음 머리줄, 고리 둘, 마지막에 체크.
# 납작붓처럼 지나가는 방향에 따라 굵기가 바뀌고, 처음엔 눌러 시작해 끝은 가늘게 뺀다.
# 다 그리고 앱도 준비되면, 달력 테두리 안쪽이 뚫리며 앱 화면이 보이고 그림이 커지면서 화면 전체로 열린다.
# 화면 전체를 덮는 막(spcur)에 달력 안쪽 모양의 구멍이 있고, 그림과 막을 같이 키운다.
_HOLE = 'M176 138 H336 A58 58 0 0 1 394 196 V338 A58 58 0 0 1 336 396 H176 A58 58 0 0 1 118 338 V196 A58 58 0 0 1 176 138 Z'
_SP_HTML = """<div id="splash" role="status" aria-label="공부방을 여는 중"><svg class="spcv" aria-hidden="true"><defs><clipPath id="sp-cc"><rect x="112" y="132" width="288" height="270" rx="58"/></clipPath><filter id="sp-rough" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="6" xChannelSelector="R" yChannelSelector="G"/></filter></defs><g class="spg"><path class="spcur" fill-rule="evenodd" d="M-30000 -30000H30000V30000H-30000Z HOLE"/><path class="sphole" d="HOLE"/><g clip-path="url(#sp-cc)"><rect class="spwash" x="112" y="132" width="288" height="80"/></g><g class="spink" filter="url(#sp-rough)"></g></g></svg><small class="spw">불러오는 중</small></div>
<script>
(function(){
var sp0=document.getElementById('splash');if(!sp0)return;
var TPL=sp0.outerHTML,NS='http://www.w3.org/2000/svg';
var red=false;try{red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
function out(t){return 1-Math.pow(1-t,3);}
function sine(t){return .5-.5*Math.cos(Math.PI*t);}
function seg(t,a,b){var x=(t-a)/(b-a);return x<0?0:x>1?1:x;}
function press(a,inn,o,end){return function(t){return t<inn?a+(1-a)*out(t/inn):t>1-o?1-(1-end)*sine((t-(1-o))/o):1;};}
function run(sp,again){
var st=window.__sp={done:false,ready:!!again};
var svg=sp.querySelector('.spcv'),g=sp.querySelector('.spg'),ink=sp.querySelector('.spink'),wash=sp.querySelector('.spwash'),hole=sp.querySelector('.sphole');
var S0=.36,CX=256,CY=262;
var DIM=null;function dims(){var r=svg.getBoundingClientRect();DIM=[r.width||window.innerWidth,r.height||window.innerHeight];}
var onR=function(){DIM=null;};window.addEventListener('resize',onR);
function place(z){if(!DIM)dims();var w=DIM[0],h=DIM[1];g.setAttribute('transform','translate('+(w/2).toFixed(1)+' '+(h/2).toFixed(1)+') scale('+(S0*z).toFixed(5)+') translate('+(-CX)+' '+(-CY)+')');return [w,h];}
function kill(){st.done=true;st.ready=true;window.removeEventListener('resize',onR);if(sp.parentNode)sp.parentNode.removeChild(sp);}
st.reveal=kill;st.go=function(){if(st.ready)kill();};
place(1);
function brush(d,o){
  var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('fill','none');ink.appendChild(p);
  var L=p.getTotalLength(),N=Math.max(12,Math.ceil(L/2.5)),phi=(o.phi==null?35:o.phi)*Math.PI/180,mn=o.min||.34,pr=o.p||press(.55,.14,.2,.45),C=[],T=[],W=[],Ws=[],Lp=[],Rp=[],i,k;
  for(i=0;i<=N;i++){var s=L*i/N,a=p.getPointAtLength(Math.max(0,s-1.5)),b=p.getPointAtLength(Math.min(L,s+1.5)),c=p.getPointAtLength(s),tx=b.x-a.x,ty=b.y-a.y,m=Math.sqrt(tx*tx+ty*ty)||1;tx/=m;ty/=m;C.push([c.x,c.y]);T.push([tx,ty]);W.push(o.w*(mn+(1-mn)*Math.abs(Math.sin(Math.atan2(ty,tx)-phi))));}
  for(i=0;i<=N;i++){var sum=0,n=0;for(k=-3;k<=3;k++){if(i+k>=0&&i+k<=N){sum+=W[i+k];n++;}}Ws.push(sum/n*pr(i/N)/2);}
  for(i=0;i<=N;i++){var nx=-T[i][1],ny=T[i][0];Lp.push([C[i][0]+nx*Ws[i],C[i][1]+ny*Ws[i]]);Rp.push([C[i][0]-nx*Ws[i],C[i][1]-ny*Ws[i]]);}
  ink.removeChild(p);
  var sh=document.createElementNS(NS,'path');if(o.cls)sh.setAttribute('class',o.cls);ink.appendChild(sh);
  function f(q){return q[0].toFixed(1)+' '+q[1].toFixed(1);}
  return {L:L,el:sh,draw:function(u){
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
  var B=D.map(function(x){return brush(x.d,x);}),t=70,S=B.map(function(b){var s={a:t,b:t+50+b.L/2.8};t=s.b+35;return s;}),T1=t-35,DRAW=T1+380,REV=900,ck=B[6].el;
  var frame=function(n){
    for(var i=0;i<B.length;i++)B[i].draw(sine(seg(n,S[i].a,S[i].b)));
    var w=seg(n,T1-60,T1+320);wash.style.opacity=(.9*out(w)).toFixed(3);wash.setAttribute('transform','translate(112 0) scale('+(.2+.8*out(w)).toFixed(4)+' 1) translate(-112 0)');
    place(1+.03*Math.sin(Math.PI*seg(n,T1,T1+380)));
  };
  // 열기: 달력 안쪽이 먼저 비치고(구멍을 덮던 막이 옅어짐), 그림과 막이 함께 커지며 화면 전체가 드러난다
  var reveal=function(r){
    var q=place(1),zEnd=Math.max(q[0]/(276*S0),q[1]/(258*S0))*1.6+1,u=seg(r,140,REV);
    place(Math.pow(zEnd,u*u));
    hole.style.opacity=(1-out(seg(r,0,300))).toFixed(3);
    wash.style.opacity=(.9*(1-seg(r,0,220))).toFixed(3);ck.style.opacity=(1-seg(r,0,220)).toFixed(3);
    ink.style.opacity=(1-seg(r,REV*.45,REV*.85)).toFixed(3);
  };
  if(red){frame(DRAW);st.done=true;st.reveal=kill;return;}
  frame(0);
  var n=0,r=0,last=null,phase='draw';
  var loop=function(now){
    if(last===null)last=now;var dt=now-last;last=now;dt=dt<0?0:dt>50?50:dt;
    if(phase==='draw'){
      n+=dt;frame(Math.min(n,DRAW));
      if(n>=DRAW){st.done=true;if(st.ready){phase='rev';ink.removeAttribute('filter');}else{phase='idle';setTimeout(function(){if(phase==='idle')sp.classList.add('wait');},1500);return;}}
    }else if(phase==='rev'){r+=dt;reveal(r);if(r>=REV){kill();return;}}
    requestAnimationFrame(loop);
  };
  st.reveal=function(){st.ready=true;if(phase==='idle'){phase='rev';ink.removeAttribute('filter');sp.classList.remove('wait');last=null;requestAnimationFrame(loop);}};
  st.go=function(){if(!st.ready)return;if(phase==='draw')n=DRAW;else st.reveal();};
  sp.addEventListener('click',function(){st.go();});
  // 앱 코드가 다 읽힌 뒤(DOMContentLoaded) 그리기 시작. 화면이 멈춘 동안은 그림도 멈춰서 건너뛰지 않는다
  var start=function(){requestAnimationFrame(loop);};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(start,0);});else start();
}catch(e){st.done=true;st.reveal=kill;if(again)kill();}
}
run(sp0,false);
// 다른 앱에 5분 넘게 있다가 돌아오면(홈 화면 앱은 다시 읽지 않고 이어서 열림) 그림을 한 번 더 그리고 지금 화면을 연다
if(!red){var hidAt=0;document.addEventListener('visibilitychange',function(){
  if(document.hidden){hidAt=Date.now();return;}
  var away=hidAt?Date.now()-hidAt:0;hidAt=0;if(away<300000||document.getElementById('splash'))return;
  var ae=document.activeElement;if(ae&&/^(INPUT|TEXTAREA|SELECT)$/.test(ae.tagName))return;
  var box=document.createElement('div');box.innerHTML=TPL;var el=box.firstChild;el.setAttribute('data-out','1');document.body.insertBefore(el,document.body.firstChild);run(el,true);
});}
})();
</script>""".replace('HOLE', _HOLE)
sub("<body>", "<body>\n" + _SP_HTML)
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);", """  if(S.ready||S.setup||S.join)splashDone();
  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);""")
sub("/* ---------- 공부방 ---------- */", r"""/* ---------- 처음 화면 ---------- */
// 앱이 준비되면 알린다. 그림이 아직이면 다 그린 뒤에 열리고, 그림이 먼저 끝났으면 바로 열린다
function splashDone(){
  var sp=document.getElementById('splash'),st=window.__sp;if(!sp||sp.getAttribute('data-out'))return;
  sp.setAttribute('data-out','1');
  if(!st||!st.reveal){if(sp.parentNode)sp.parentNode.removeChild(sp);return;}
  st.ready=true;
  if(st.done)st.reveal();
  setTimeout(function(){if(sp.parentNode)sp.parentNode.removeChild(sp);},7000);
}
setTimeout(function(){var sp=document.getElementById('splash');if(sp&&!sp.getAttribute('data-out'))splashDone();},15000);
/* ---------- 공부방 ---------- */""")
sub("</style>", """#splash{position:fixed;inset:0;z-index:200;overflow:hidden;-webkit-tap-highlight-color:transparent}
.spcv{position:absolute;inset:0;display:block;width:100%;height:100%;overflow:visible}
.spcur,.sphole{fill:var(--bg)}
.spink path{fill:var(--ink)}
@supports (color:color-mix(in srgb,red 50%,blue)){.spink path{fill:color-mix(in srgb,var(--accent) 30%,var(--ink))}}
.spink path.spck{fill:var(--accent)}
.spwash{fill:var(--accent-soft);opacity:0}
.spw{position:absolute;left:0;right:0;top:calc(50% + 74px);text-align:center;font-size:12.5px;color:var(--ink-3);opacity:0;transition:opacity .3s}
#splash.wait .spw{opacity:1;animation:spBreath 1.4s ease-in-out .3s infinite}
@keyframes spBreath{0%,100%{opacity:1}50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){#splash.wait .spw{animation:none}}
</style>""")
# 설정 맨 아래에 이 판을 만든 시각: 휴대폰이 새 판을 받았는지 확인할 때 본다
import datetime as _dt
_ver = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=9))).strftime('%-m월 %-d일 %H:%M')
sub("  return dlg('wide',{id:'settings',t:'설정'},b);", "  b+='<p class=\"hint appver\">앱 버전 " + _ver + "</p>';\n  return dlg('wide',{id:'settings',t:'설정'},b);")
sub("</style>", ".appver{margin-top:18px;text-align:center;font-size:12px;color:var(--ink-3);font-variant-numeric:tabular-nums}\n</style>")
