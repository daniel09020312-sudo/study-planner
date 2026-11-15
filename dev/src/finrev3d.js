/* ---------- v95: 최종 결과 3D 공개 연출 (FR3). three.js r128을 열 때만 불러옴(같은 사이트 vendor/three-r128.min.js, 안 되면 cdnjs).
   FR3.play(data, {onClose, onFail}) data={title, period, cut, people:[{name,total,me}](점수 높은 순), prizes:['1등 상품','2등','3등']}
   막: 0 시작(멀리서 곡선으로 날아옴, 3·2·1) -> 1 막대가 솟고 100점 라인 -> 2 꼴찌부터 4등까지 카메라가 하나씩 -> 3·4·5 스포트라이트가 찾고 3·2·1등이 곡선으로 시상대에 -> 6 전체 ---------- */
var FR3=(function(){
  var SRC=['vendor/three-r128.min.js','https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'];
  var FONT='"Pretendard","Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",system-ui,sans-serif';
  function loadThree(cb){
    if(window.THREE)return cb(true);
    var i=0;
    (function next(){
      if(i>=SRC.length)return cb(false);
      var s=document.createElement('script'),done=false,src=SRC[i++];
      var to=setTimeout(function(){if(done)return;done=true;try{s.parentNode.removeChild(s);}catch(e){}next();},12000);
      s.onload=function(){if(done)return;done=true;clearTimeout(to);if(window.THREE)cb(true);else next();};
      s.onerror=function(){if(done)return;done=true;clearTimeout(to);try{s.parentNode.removeChild(s);}catch(e){}next();};
      s.src=src;s.async=true;document.head.appendChild(s);
    })();
  }
  function webgl(){try{var c=document.createElement('canvas');return !!(window.WebGLRenderingContext&&(c.getContext('webgl')||c.getContext('experimental-webgl')));}catch(e){return false;}}
  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function fmt(n){return Math.round(+n||0).toLocaleString('ko-KR');}
  var E={
    lin:function(t){return t;},
    out:function(t){return 1-Math.pow(1-t,3);},
    io:function(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;},
    back:function(t){var c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2);},
    el:function(t){if(t===0||t===1)return t;return Math.pow(2,-10*t)*Math.sin((t*10-.75)*(2*Math.PI/3))+1;},
    bounce:function(t){var n=7.5625,d=2.75;if(t<1/d)return n*t*t;if(t<2/d)return n*(t-=1.5/d)*t+.75;if(t<2.5/d)return n*(t-=2.25/d)*t+.9375;return n*(t-=2.625/d)*t+.984375;}
  };
  function play(data,opt){
    opt=opt||{};
    var root=document.createElement('div');root.className='f3';root.setAttribute('role','dialog');root.setAttribute('aria-modal','true');root.setAttribute('aria-label','최종 결과 발표');
    root.innerHTML='<div class="f3load"><i></i><span>무대를 준비하는 중</span></div>';
    document.body.appendChild(root);document.documentElement.classList.add('f3on');
    var closed=false;
    function fail(){if(closed)return;closed=true;try{root.parentNode.removeChild(root);}catch(e){}document.documentElement.classList.remove('f3on');if(opt.onFail)opt.onFail();}
    if(!webgl())return fail();
    loadThree(function(ok){
      if(closed)return;
      if(!ok||!window.THREE)return fail();
      try{run(root,data,opt,function(){closed=true;});}catch(e){try{console.error(e);}catch(x){}fail();}
    });
    return {close:function(){if(root._close)root._close();else fail();}};
  }
  function run(root,data,opt,markClosed){
    var T3=window.THREE,people=(data.people||[]).filter(function(x){return x&&x.total>0;}),N=people.length,CUT=+data.cut||100;
    people.forEach(function(p,i){p.rank=i+1;});
    var W=innerWidth,H=innerHeight,mobile=Math.min(W,H)<700;
    root.innerHTML='<canvas class="f3c"></canvas><div class="f3ui"><div class="f3flash"></div><div class="f3vig"></div><div class="f3top"></div><div class="f3mid"></div><div class="f3side"></div><div class="f3bot"><button class="f3next" hidden></button><button class="f3skip">건너뛰기</button></div></div>';
    var cv=root.querySelector('.f3c'),ui={top:root.querySelector('.f3top'),mid:root.querySelector('.f3mid'),side:root.querySelector('.f3side'),flash:root.querySelector('.f3flash'),next:root.querySelector('.f3next'),skip:root.querySelector('.f3skip')};
    var R=new T3.WebGLRenderer({canvas:cv,antialias:true,powerPreference:'high-performance'});
    R.setPixelRatio(Math.min(devicePixelRatio||1,mobile?1.6:2));R.setSize(W,H);
    R.outputEncoding=T3.sRGBEncoding;R.toneMapping=T3.ACESFilmicToneMapping;R.toneMappingExposure=1.05;
    var scene=new T3.Scene();scene.background=new T3.Color(0x05060f);scene.fog=new T3.FogExp2(0x05060f,mobile?0.010:0.008);
    var camera=new T3.PerspectiveCamera(mobile&&W<H?62:48,W/H,0.1,2000);
    var cam={pos:new T3.Vector3(0,80,300),look:new T3.Vector3(0,30,-60),shake:0};
    /* ---- 텍스처 ---- */
    function dotTex(){var c=document.createElement('canvas');c.width=c.height=64;var x=c.getContext('2d'),g=x.createRadialGradient(32,32,0,32,32,32);g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.25,'rgba(255,255,255,.85)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,64,64);var t=new T3.CanvasTexture(c);return t;}
    function vGrad(a,b){var c=document.createElement('canvas');c.width=4;c.height=256;var x=c.getContext('2d'),g=x.createLinearGradient(0,0,0,256);g.addColorStop(0,a);g.addColorStop(1,b);x.fillStyle=g;x.fillRect(0,0,4,256);return new T3.CanvasTexture(c);}
    function nebTex(col){var c=document.createElement('canvas');c.width=c.height=256;var x=c.getContext('2d'),g=x.createRadialGradient(128,128,0,128,128,128);g.addColorStop(0,col);g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,256,256);return new T3.CanvasTexture(c);}
    var DOT=dotTex();
    function label(lines,o){
      o=o||{};var c=document.createElement('canvas'),x=c.getContext('2d'),w=1024,big=o.big||96,small=o.small||60,h=lines.length>1?big+small+110:big+90;
      c.width=w;c.height=h;
      var col=o.col||'#ffffff',bd=o.bd||'rgba(160,200,255,.55)';
      x.fillStyle=o.bg||'rgba(8,10,28,.78)';var r=h/2.6;x.beginPath();x.moveTo(r,8);x.lineTo(w-r,8);x.quadraticCurveTo(w-8,8,w-8,r);x.lineTo(w-8,h-r);x.quadraticCurveTo(w-8,h-8,w-r,h-8);x.lineTo(r,h-8);x.quadraticCurveTo(8,h-8,8,h-r);x.lineTo(8,r);x.quadraticCurveTo(8,8,r,8);x.closePath();x.fill();
      x.lineWidth=6;x.strokeStyle=bd;x.stroke();
      x.textAlign='center';x.textBaseline='middle';
      x.font='800 '+big+'px '+FONT;x.fillStyle=col;x.shadowColor=o.glow||'rgba(120,180,255,.6)';x.shadowBlur=24;
      x.fillText(lines[0],w/2,lines.length>1?big/2+44:h/2,w-60);
      if(lines.length>1){x.font='600 '+small+'px '+FONT;x.fillStyle=o.col2||'rgba(255,255,255,.82)';x.shadowBlur=0;x.fillText(lines[1],w/2,big+small/2+64,w-60);}
      var t=new T3.CanvasTexture(c);t.encoding=T3.sRGBEncoding;t.anisotropy=4;
      var m=new T3.SpriteMaterial({map:t,transparent:true,depthWrite:false,depthTest:false,opacity:0});
      var s=new T3.Sprite(m);var sc=o.scale||3.2;s.scale.set(sc,sc*h/w,1);s.renderOrder=20;s.userData.sc=sc;s.userData.ar=h/w;return s;
    }
    /* ---- 무대 ---- */
    var amb=new T3.AmbientLight(0x6070b0,.55);scene.add(amb);
    var hemi=new T3.HemisphereLight(0x8aa0ff,0x100818,.5);scene.add(hemi);
    var key=new T3.DirectionalLight(0xffffff,.9);key.position.set(10,30,25);scene.add(key);
    var pls=[0xff4fa3,0x3fd0ff,0xffc94a].map(function(c,i){var l=new T3.PointLight(c,1.4,90,1.6);l.position.set(Math.cos(i*2.1)*20,8,Math.sin(i*2.1)*20);scene.add(l);return l;});
    var Rr=Math.max(12,0.62*N+7),MAXH=mobile?14:16;
    var floor=new T3.Mesh(new T3.CircleGeometry(220,96),new T3.MeshStandardMaterial({color:0x080a1a,metalness:.75,roughness:.32}));floor.rotation.x=-Math.PI/2;scene.add(floor);
    var grid=new T3.PolarGridHelper(Rr+30,36,14,96,0x2c3a8a,0x1a2250);grid.material.transparent=true;grid.material.opacity=.45;grid.position.y=.01;scene.add(grid);
    function ring(r,col,op,y){var m=new T3.Mesh(new T3.RingGeometry(r-.12,r,160),new T3.MeshBasicMaterial({color:col,transparent:true,opacity:op,blending:T3.AdditiveBlending,side:T3.DoubleSide,depthWrite:false}));m.rotation.x=-Math.PI/2;m.position.y=y||.03;scene.add(m);return m;}
    var rings=[ring(Rr+3,0x4fb8ff,.7),ring(Rr+3.8,0xb46bff,.35),ring(7.5,0xffd36a,.0),ring(9,0xff7ab6,.0)];
    /* 별, 성운 */
    (function(){var n=mobile?1800:3200,g=new T3.BufferGeometry(),p=new Float32Array(n*3),c=new Float32Array(n*3);
      for(var i=0;i<n;i++){var r=250+Math.random()*500,th=Math.random()*Math.PI*2,ph=Math.acos(Math.random()*.95);p[i*3]=r*Math.sin(ph)*Math.cos(th);p[i*3+1]=r*Math.cos(ph)*.9+10;p[i*3+2]=r*Math.sin(ph)*Math.sin(th);var k=.6+Math.random()*.4,h=Math.random();c[i*3]=k*(h<.2?1:.8);c[i*3+1]=k*.85;c[i*3+2]=k;}
      g.setAttribute('position',new T3.BufferAttribute(p,3));g.setAttribute('color',new T3.BufferAttribute(c,3));
      var st=new T3.Points(g,new T3.PointsMaterial({size:2.2,map:DOT,vertexColors:true,transparent:true,depthWrite:false,blending:T3.AdditiveBlending,fog:false}));st.name='stars';scene.add(st);
      ['rgba(120,60,255,.55)','rgba(255,60,160,.35)','rgba(40,160,255,.4)'].forEach(function(col,i){var s=new T3.Sprite(new T3.SpriteMaterial({map:nebTex(col),transparent:true,depthWrite:false,blending:T3.AdditiveBlending,fog:false}));s.position.set((i-1)*180,90+i*30,-380);s.scale.set(420,420,1);scene.add(s);});
    })();
    /* 떠다니는 먼지 */
    var dust=(function(){var n=mobile?260:500,g=new T3.BufferGeometry(),p=new Float32Array(n*3);for(var i=0;i<n;i++){p[i*3]=(Math.random()-.5)*Rr*3;p[i*3+1]=Math.random()*30;p[i*3+2]=(Math.random()-.5)*Rr*3;}g.setAttribute('position',new T3.BufferAttribute(p,3));var m=new T3.Points(g,new T3.PointsMaterial({size:.22,map:DOT,color:0x9fc8ff,transparent:true,opacity:.55,depthWrite:false,blending:T3.AdditiveBlending}));scene.add(m);return m;})();
    /* ---- 막대 ---- */
    var maxS=Math.max.apply(null,people.map(function(p){return p.total;}).concat([1]));
    function hOf(s){return .6+MAXH*s/maxS;}
    var hCut=CUT<=maxS?hOf(CUT):null,capH=Math.max(hCut?hCut*1.18:0,MAXH*.42);
    var order=people.slice();for(var i=order.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=order[i];order[i]=order[j];order[j]=t;}
    var span=Math.min(Math.PI*1.15,Math.max(Math.PI*.6,N*0.16)),bars=[];
    var BOX=new T3.BoxGeometry(1.3,1,1.3);BOX.translate(0,.5,0);var EDG=new T3.EdgesGeometry(BOX);
    order.forEach(function(p,i){
      var a=N>1?-span/2+span*i/(N-1):0,x=Math.sin(a)*Rr,z=-Math.cos(a)*Rr*.9;
      var hue=.55+.32*(i/Math.max(1,N-1)),col=new T3.Color().setHSL(hue,.82,.5);
      var g=new T3.Group();g.position.set(x,0,z);g.lookAt(0,0,6);
      var mat=new T3.MeshStandardMaterial({color:col,metalness:.35,roughness:.28,emissive:col,emissiveIntensity:.16,transparent:true,opacity:.96});
      var mesh=new T3.Mesh(BOX,mat);mesh.scale.y=.001;g.add(mesh);
      var em=new T3.LineBasicMaterial({color:p.me?0x7cf0ff:0xaedcff,transparent:true,opacity:.7,blending:T3.AdditiveBlending,depthWrite:false});var edges=new T3.LineSegments(EDG,em);edges.scale.y=.001;g.add(edges);
      var cap=new T3.Sprite(new T3.SpriteMaterial({map:DOT,color:col,transparent:true,blending:T3.AdditiveBlending,depthWrite:false,opacity:.0}));cap.scale.set(3,3,1);g.add(cap);
      scene.add(g);
      var b={p:p,g:g,mesh:mesh,mat:mat,edges:edges,em:em,cap:cap,col:col,h:hOf(p.total),cur:.001,home:new T3.Vector3(x,0,z),label:null,lift:0};
      b.set=function(h){b.cur=Math.max(.001,h);mesh.scale.y=b.cur;edges.scale.y=b.cur;cap.position.y=b.cur+.05;if(b.label)b.label.position.y=b.cur+b.lift+b.label.scale.y/2+.6;};
      bars.push(b);
    });
    function barOf(rank){for(var i=0;i<bars.length;i++)if(bars[i].p.rank===rank)return bars[i];return null;}
    function setLabel(b,lines,o){if(b.label){b.g.remove(b.label);b.label.material.map.dispose();b.label.material.dispose();}b.label=label(lines,o);b.g.add(b.label);b.set(b.cur);return b.label;}
    /* 100점 라인 */
    var cutPlane=null,cutLab=null;
    if(hCut){cutPlane=new T3.Group();var cp=new T3.Mesh(new T3.CircleGeometry(Rr+4,96),new T3.MeshBasicMaterial({color:0x58d6ff,transparent:true,opacity:.0,blending:T3.AdditiveBlending,depthWrite:false,side:T3.DoubleSide}));cp.rotation.x=-Math.PI/2;cutPlane.add(cp);var ce=new T3.Mesh(new T3.RingGeometry(Rr+3.8,Rr+4,160),new T3.MeshBasicMaterial({color:0x9ff0ff,transparent:true,opacity:.0,blending:T3.AdditiveBlending,depthWrite:false,side:T3.DoubleSide}));ce.rotation.x=-Math.PI/2;cutPlane.add(ce);cutPlane.userData={a:cp,b:ce};cutPlane.position.y=0;scene.add(cutPlane);
      cutLab=label([CUT+'점 라인'],{scale:4,col:'#9ff0ff',bd:'rgba(159,240,255,.7)'});cutLab.position.set(0,0,-Rr*.9-2);scene.add(cutLab);}
    /* 스포트라이트 빔 */
    var BEAM_L=60,beamTex=vGrad('rgba(255,255,255,.0)','rgba(255,255,255,.55)');
    function beam(col,rb){var g=new T3.CylinderGeometry(.2,rb||2.3,BEAM_L,40,1,true);g.translate(0,-BEAM_L/2,0);var m=new T3.Mesh(g,new T3.MeshBasicMaterial({map:beamTex,color:col,transparent:true,opacity:0,blending:T3.AdditiveBlending,depthWrite:false,side:T3.DoubleSide}));var o=new T3.Group();o.add(m);o.userData={m:m,tgt:new T3.Vector3(),cur:new T3.Vector3()};scene.add(o);return o;}
    var beams=[beam(0xfff1c2),beam(0xc8e4ff),beam(0xffd0ec)];
    beams.forEach(function(b,i){b.position.set((i-1)*16,BEAM_L-6,4);});
    function aimBeam(b,v){var d=new T3.Vector3().subVectors(v,b.position);var len=d.length();d.normalize();b.quaternion.setFromUnitVectors(new T3.Vector3(0,-1,0),d);b.scale.set(1,len/BEAM_L,1);}
    var spot=new T3.SpotLight(0xffffff,0,90,.32,.55,1.2);spot.position.set(0,40,10);scene.add(spot);scene.add(spot.target);
    /* 금빛 기둥, 충격파, 왕관, 시상대 */
    var pillar=new T3.Mesh(new T3.CylinderGeometry(2.6,2.6,90,48,1,true),new T3.MeshBasicMaterial({map:vGrad('rgba(255,210,90,0)','rgba(255,225,140,.9)'),color:0xffd36a,transparent:true,opacity:0,blending:T3.AdditiveBlending,depthWrite:false,side:T3.DoubleSide}));pillar.position.set(0,45,4);pillar.scale.y=.001;scene.add(pillar);
    var PODIUM={1:new T3.Vector3(0,0,5),2:new T3.Vector3(-4.6,0,6.2),3:new T3.Vector3(4.6,0,6.2)},PH={1:1.6,2:1.1,3:.75},MED={1:0xffcf4a,2:0xd9e4f2,3:0xd98a4a};
    var pods={};[1,2,3].forEach(function(k){if(!barOf(k))return;var m=new T3.Mesh(new T3.BoxGeometry(3.4,1,3.4),new T3.MeshStandardMaterial({color:0x151a35,metalness:.6,roughness:.3,emissive:MED[k],emissiveIntensity:.0}));m.geometry.translate(0,.5,0);m.position.copy(PODIUM[k]);m.scale.y=.001;scene.add(m);var n=label([String(k)],{big:150,scale:1.6,col:'#'+MED[k].toString(16),bd:'rgba(255,255,255,.2)',bg:'rgba(0,0,0,0)'});n.position.set(PODIUM[k].x,.5,PODIUM[k].z+1.75);scene.add(n);pods[k]={m:m,n:n};});
    var crown=(function(){var g=new T3.Group(),gold=new T3.MeshStandardMaterial({color:0xffcf4a,metalness:1,roughness:.18,emissive:0x664400,emissiveIntensity:.6});var band=new T3.Mesh(new T3.CylinderGeometry(1,1.1,.55,32,1,true),gold);band.material.side=T3.DoubleSide;g.add(band);for(var i=0;i<6;i++){var a=i/6*Math.PI*2,sp=new T3.Mesh(new T3.ConeGeometry(.22,.75,12),gold);sp.position.set(Math.cos(a)*1.02,.62,Math.sin(a)*1.02);g.add(sp);var gem=new T3.Mesh(new T3.SphereGeometry(.13,12,12),new T3.MeshStandardMaterial({color:[0xff3b6b,0x3bc6ff,0x7dff7a][i%3],emissive:[0xff3b6b,0x3bc6ff,0x7dff7a][i%3],emissiveIntensity:.8,metalness:.2,roughness:.1}));gem.position.set(Math.cos(a)*1.08,.05,Math.sin(a)*1.08);g.add(gem);}g.visible=false;scene.add(g);return g;})();
    /* ---- 파티클 ---- */
    var bursts=[];
    function burst(pos,col,n,spd,life,size,grav){
      n=Math.round(n*(mobile?.65:1));var g=new T3.BufferGeometry(),p=new Float32Array(n*3),v=new Float32Array(n*3);
      for(var i=0;i<n;i++){p[i*3]=pos.x;p[i*3+1]=pos.y;p[i*3+2]=pos.z;var th=Math.random()*Math.PI*2,ph=Math.acos(2*Math.random()-1),s=spd*(.45+Math.random()*.55);v[i*3]=s*Math.sin(ph)*Math.cos(th);v[i*3+1]=s*Math.cos(ph);v[i*3+2]=s*Math.sin(ph)*Math.sin(th);}
      g.setAttribute('position',new T3.BufferAttribute(p,3));
      var m=new T3.PointsMaterial({size:size||.5,map:DOT,color:col,transparent:true,opacity:1,depthWrite:false,blending:T3.AdditiveBlending});
      var pt=new T3.Points(g,m);scene.add(pt);bursts.push({pt:pt,v:v,n:n,t:0,life:life||1.6,grav:grav==null?5:grav});
    }
    function stepBursts(dt){for(var i=bursts.length-1;i>=0;i--){var b=bursts[i],a=b.pt.geometry.attributes.position.array;b.t+=dt;var k=Math.pow(.985,dt*60);for(var j=0;j<b.n;j++){b.v[j*3]*=k;b.v[j*3+1]=b.v[j*3+1]*k-b.grav*dt;b.v[j*3+2]*=k;a[j*3]+=b.v[j*3]*dt;a[j*3+1]+=b.v[j*3+1]*dt;a[j*3+2]+=b.v[j*3+2]*dt;}b.pt.geometry.attributes.position.needsUpdate=true;b.pt.material.opacity=Math.max(0,1-b.t/b.life);if(b.t>=b.life){scene.remove(b.pt);b.pt.geometry.dispose();b.pt.material.dispose();bursts.splice(i,1);}}}
    var waves=[];
    function wave(pos,col,maxS,dur){var m=new T3.Mesh(new T3.RingGeometry(.8,1,128),new T3.MeshBasicMaterial({color:col,transparent:true,opacity:.95,blending:T3.AdditiveBlending,depthWrite:false,side:T3.DoubleSide}));m.rotation.x=-Math.PI/2;m.position.set(pos.x,.06,pos.z);scene.add(m);waves.push({m:m,t:0,d:dur||1.4,s:maxS||22});}
    function stepWaves(dt){for(var i=waves.length-1;i>=0;i--){var w=waves[i];w.t+=dt;var k=w.t/w.d,s=1+E.out(Math.min(1,k))*w.s;w.m.scale.set(s,s,s);w.m.material.opacity=Math.max(0,.95*(1-k));if(k>=1){scene.remove(w.m);w.m.geometry.dispose();w.m.material.dispose();waves.splice(i,1);}}}
    /* 색종이 */
    var CN=mobile?260:520,conf=new T3.InstancedMesh(new T3.PlaneGeometry(.22,.36),new T3.MeshBasicMaterial({side:T3.DoubleSide,transparent:true}),CN),cd=[],dum=new T3.Object3D(),confOn=0;
    var CC=[0xffcf4a,0xff5fa8,0x5fd4ff,0x8dff8a,0xffffff,0xb98cff];
    for(var ci=0;ci<CN;ci++){cd.push({p:new T3.Vector3(0,-50,0),v:new T3.Vector3(),r:new T3.Vector3(Math.random()*6,Math.random()*6,Math.random()*6),rs:new T3.Vector3(Math.random()*6-3,Math.random()*6-3,Math.random()*6-3),ph:Math.random()*6,live:false});conf.setColorAt(ci,new T3.Color(CC[ci%CC.length]));}
    conf.instanceColor.needsUpdate=true;conf.frustumCulled=false;scene.add(conf);
    function confSpawn(n,cx,cz,wide){var c=0;for(var i=0;i<CN&&c<n;i++){var d=cd[i];if(d.live)continue;d.live=true;c++;d.p.set(cx+(Math.random()-.5)*wide,22+Math.random()*16,cz+(Math.random()-.5)*wide*.7);d.v.set((Math.random()-.5)*1.5,-(2.2+Math.random()*2.2),(Math.random()-.5)*1.5);}}
    function stepConf(dt,t){for(var i=0;i<CN;i++){var d=cd[i];if(d.live){d.p.addScaledVector(d.v,dt);d.p.x+=Math.sin(t*2+d.ph)*dt*.9;d.r.addScaledVector(d.rs,dt);if(d.p.y<0){d.live=false;d.p.y=-50;}}dum.position.copy(d.p);dum.rotation.set(d.r.x,d.r.y,d.r.z);dum.updateMatrix();conf.setMatrixAt(i,dum.matrix);}conf.instanceMatrix.needsUpdate=true;}
    var fireworks=0,fwNext=0;
    /* ---- 시간표 ---- */
    var T=0,tws=[],evs=[];
    function tw(delay,dur,fn,ease){tws.push({s:T+delay,d:Math.max(.0001,dur),fn:fn,e:E[ease||'io']||E.io,started:false});}
    function at(delay,fn){evs.push({s:T+delay,fn:fn});}
    function stepTime(){for(var i=tws.length-1;i>=0;i--){var w=tws[i];if(T<w.s)continue;var k=Math.min(1,(T-w.s)/w.d);if(!w.started){w.started=true;if(w.fn.init)w.fn.init();}w.fn(w.e(k),k);if(k>=1)tws.splice(i,1);}for(var j=evs.length-1;j>=0;j--){if(T>=evs[j].s){var f=evs[j].fn;evs.splice(j,1);f();}}}
    function camTo(delay,dur,pts,lookTo,ease){
      var P,L0,c;var f=function(e){cam.pos.copy(c.getPoint(e));cam.look.lerpVectors(L0,lookTo,e);};
      f.init=function(){P=[cam.pos.clone()].concat(typeof pts==='function'?pts():pts);c=new T3.CatmullRomCurve3(P,false,'centripetal');L0=cam.look.clone();};
      tw(delay,dur,f,ease||'io');
    }
    function fadeMat(m,to,delay,dur){var a;var f=function(e){m.opacity=a+(to-a)*e;};f.init=function(){a=m.opacity;};tw(delay,dur,f,'out');}
    function growBar(b,h,delay,dur,ease){var a;var f=function(e){b.set(a+(h-a)*e);};f.init=function(){a=b.cur;};tw(delay,dur,f,ease||'back');}
    function popLabel(s,delay){var sc=s.userData.sc,ar=s.userData.ar;tw(delay,.55,function(e){s.material.opacity=Math.min(1,e*1.4);var k=.3+.7*e;s.scale.set(sc*k,sc*ar*k,1);},'back');}
    function dimBar(b,op,emi,delay){var a,c;var f=function(e){b.mat.opacity=a+(op-a)*e;b.mat.emissiveIntensity=c+(emi-c)*e;b.em.opacity=.7*b.mat.opacity;};f.init=function(){a=b.mat.opacity;c=b.mat.emissiveIntensity;};tw(delay||0,.8,f,'out');}
    function lightTo(v,delay,dur){var a;var f=function(e){amb.intensity=a+(v-a)*e;hemi.intensity=(a+(v-a)*e)*.9;key.intensity=(a+(v-a)*e)*1.6;};f.init=function(){a=amb.intensity;};tw(delay,dur||.8,f,'io');}
    function flash(ms,col){ui.flash.style.background=col||'#fff';ui.flash.classList.remove('on');void ui.flash.offsetWidth;ui.flash.style.animationDuration=(ms||600)+'ms';ui.flash.classList.add('on');}
    function shake(a){cam.shake=Math.max(cam.shake,a);}
    function html(el,h){el.innerHTML=h;}
    /* ---- 막 ---- */
    var front=new T3.Vector3(0,4,0),act=-1,actEnd=0,busy=false,nextLabel='';
    function showNext(txt){nextLabel=txt;ui.next.textContent=txt;ui.next.hidden=false;ui.next.classList.remove('in');void ui.next.offsetWidth;ui.next.classList.add('in');}
    function hideNext(){ui.next.hidden=true;}
    var revealed={};
    function act0(){
      html(ui.top,'');html(ui.mid,'<div class="f3title"><small>'+esc(data.period||'')+'</small><h1>'+esc(data.title||'최종 결과 발표')+'</h1><p>'+N+'명의 기록을 모두 더했습니다</p></div>');
      cam.pos.set(0,90,320);cam.look.set(0,40,-80);
      var far=mobile&&W<H?1.6:1;
      camTo(0,7.2,[new T3.Vector3(150,55,170),new T3.Vector3(70,24,80*far),new T3.Vector3(0,13,(Rr+26)*far)],new T3.Vector3(0,5,0),'io');
      at(4.1,function(){html(ui.mid,'<div class="f3count"><b style="--i:0">3</b><b style="--i:1">2</b><b style="--i:2">1</b></div>');});
      at(6.6,function(){flash(500,'rgba(160,210,255,.9)');burst(new T3.Vector3(0,6,0),0x9fd8ff,260,22,1.4,.4,0);wave(new T3.Vector3(0,0,0),0x7fd0ff,30,1.6);shake(.5);html(ui.mid,'');});
      return 7.2;
    }
    function act1(){
      var gap=Math.min(.09,2.6/Math.max(1,N));
      bars.forEach(function(b,i){growBar(b,Math.min(b.h,capH),.2+i*gap,1.6,'back');tw(.2+i*gap,.6,function(e){b.cap.material.opacity=.55*e;},'out');});
      var far=mobile&&W<H?1.6:1;
      camTo(0,5.2,[new T3.Vector3(-Rr*1.05,9,Rr*.75*far),new T3.Vector3(0,11,(Rr+18)*far),new T3.Vector3(Rr*1.05,12,Rr*.75*far)],new T3.Vector3(0,4,-Rr*.3),'io');
      html(ui.top,'<div class="f3tag">모두의 기록</div>');
      var cutters=bars.filter(function(b){return b.p.total>=CUT;});
      var t0=2.4+N*gap;
      if(cutPlane){
        at(t0,function(){html(ui.top,'<div class="f3tag hot">'+CUT+'점 라인</div>');});
        tw(t0,1.8,function(e){cutPlane.position.y=hCut*e;cutPlane.userData.a.material.opacity=.13*Math.min(1,e*3);cutPlane.userData.b.material.opacity=.9*Math.min(1,e*3);cutLab.position.y=hCut*e+1.4;cutLab.material.opacity=Math.min(1,e*3);},'io');
        cutters.forEach(function(b,i){at(t0+1.9+i*.14,function(){b.em.color.set(0xffd36a);b.em.opacity=1;b.cap.material.color.set(0xffd36a);b.cap.material.opacity=1;burst(new T3.Vector3(b.home.x,b.cur,b.home.z),0xffd36a,70,7,1.1,.35,3);setLabel(b,[b.p.name],{scale:2.8,col:'#ffe7a3',bd:'rgba(255,211,106,.8)',glow:'rgba(255,200,80,.7)'});popLabel(b.label,0);});});
        bars.forEach(function(b){if(b.p.total<CUT)dimBar(b,.55,.08,t0+1.9);});
      }
      var tEnd=(cutPlane?t0+2.4+cutters.length*.14:t0+.5);
      camTo(Math.max(5.3,tEnd-1.8),2.2,[new T3.Vector3(0,(hCut||8)+9,(Rr+20)*far)],new T3.Vector3(0,(hCut||6)*.6,-2),'io');
      at(tEnd+.3,function(){
        var names=cutters.map(function(b){return b.p.name;}).sort(function(a,b){return a.localeCompare(b);});
        html(ui.side,'<div class="f3panel in"><h2>'+CUT+'점 넘긴 사람<small>'+names.length+'명 · 이름순</small></h2><div class="f3chips">'+(names.length?names.map(function(n,i){return '<span style="--i:'+i+'">'+esc(n)+'</span>';}).join(''):'<p>'+CUT+'점을 넘긴 사람이 없습니다</p>')+'</div><p class="f3note">등수는 곧 공개됩니다</p></div>');
      });
      return Math.max(7.6,tEnd+1.6);
    }
    function act2(){
      html(ui.side,'');var rest=bars.filter(function(b){return b.p.rank>3;}).sort(function(a,b){return b.p.rank-a.p.rank;});
      if(!rest.length)return 0;
      html(ui.top,'<div class="f3tag">'+(rest.length>1?rest[0].p.rank+'등부터 4등까지':'4등')+'</div>');
      html(ui.side,'<div class="f3tick"></div>');
      var per=rest.length<=8?1.5:rest.length<=20?.95:.55,far=mobile&&W<H?1.5:1;
      bars.forEach(function(b){if(b.p.rank<=3&&b.label){b.label.material.opacity=0;}});
      rest.forEach(function(b,j){
        var d=new T3.Vector3(b.home.x,0,b.home.z),dir=d.clone().normalize(),h=b.h;
        var cp=new T3.Vector3(b.home.x*.42-dir.x*2,h*.55+3.2,b.home.z*.42+7*far);
        camTo(j*per,per*.95,function(){var mid=cp.clone().lerp(cam.pos,.5);mid.y+=3;return [mid,cp];},new T3.Vector3(b.home.x,h*.65,b.home.z),'io');
        at(j*per+per*.35,function(){
          dimBar(b,.97,.32,0);growBar(b,h,0,.7,'back');
          setLabel(b,[b.p.rank+'등 '+b.p.name,fmt(b.p.total)+'점'+(b.p.me?' · 나':'')],{scale:N<=20?4.2:3.4,col:b.p.me?'#9ff4ff':'#ffffff'});popLabel(b.label,.35);
          burst(new T3.Vector3(b.home.x,h,b.home.z),b.col.getHex(),90,6,1.2,.38,2.5);
          var tk=ui.side.querySelector('.f3tick');if(tk){var r=document.createElement('div');r.className='f3row'+(b.p.me?' me':'');r.innerHTML='<b>'+b.p.rank+'등</b><span>'+esc(b.p.name)+'</span><em>'+fmt(b.p.total)+'점</em>';tk.insertBefore(r,tk.firstChild);}
        });
        at(j*per+per*.95,function(){dimBar(b,.8,.16,0);});
      });
      var tEnd=rest.length*per;
      camTo(tEnd,2.4,[new T3.Vector3(0,14,(Rr+22)*far)],new T3.Vector3(0,5,0),'io');
      at(tEnd+.6,function(){bars.forEach(function(b){if(b.p.rank<=3){setLabel(b,['?'],{scale:2.8,big:150,col:'#ffd36a',bd:'rgba(255,211,106,.8)'});popLabel(b.label,0);b.em.color.set(0xffd36a);}});html(ui.top,'<div class="f3tag hot">남은 세 사람</div>');});
      return tEnd+3;
    }
    function podiumAct(k){
      var b=barOf(k);if(!b)return 0;
      html(ui.side,'');var far=mobile&&W<H?1.45:1,big=k===1;
      var cand=bars.filter(function(x){return x.p.rank<=3&&!revealed[x.p.rank];});
      html(ui.top,'');html(ui.mid,'<div class="f3drum'+(big?' big':'')+'"><small>두 구 두 구 두 구</small><b>'+k+'등은</b></div>');
      lightTo(big?.04:.18,0,big?1.2:.8);bars.forEach(function(x){if(!revealed[x.p.rank]&&x.p.rank>3)dimBar(x,.25,.04,0);});
      pls.forEach(function(l){tw(0,.8,function(e){l.intensity=1.4*(1-e*.7);},'out');});
      var t0=big?2.4:0;
      if(big){at(.3,function(){root.classList.add('beat');});at(2.3,function(){root.classList.remove('beat');});camTo(0,2.4,[new T3.Vector3(0,22,(Rr+30)*far)],new T3.Vector3(0,4,0),'io');}
      /* 빔이 후보를 훑음 */
      var sweep=big?3.4:2.6;
      beams.forEach(function(bm,i){
        fadeMat(bm.userData.m.material,.5,t0,.4);
        var pick=function(){var c=cand[Math.floor(Math.random()*cand.length)]||b;return new T3.Vector3(c.g.position.x+(Math.random()-.5)*3,0,c.g.position.z+(Math.random()-.5)*3);};
        var steps=big?6:4;for(var s=0;s<steps;s++)(function(s){var A,B;var f=function(e){bm.userData.cur.lerpVectors(A,B,e);aimBeam(bm,bm.userData.cur);};f.init=function(){A=bm.userData.cur.lengthSq()?bm.userData.cur.clone():pick();B=s===steps-1?new T3.Vector3(b.g.position.x,b.cur,b.g.position.z):pick();};tw(t0+s*sweep/steps,sweep/steps,f,'io');})(s);
      });
      camTo(t0,sweep,[new T3.Vector3(Math.sin(k)*8,12,(Rr+14)*far)],new T3.Vector3(b.g.position.x*.4,4,b.g.position.z*.4),'io');
      var tLock=t0+sweep;
      at(tLock,function(){flash(220,'rgba(255,255,255,.5)');shake(.25);spot.intensity=big?6:4;spot.target.position.copy(b.g.position);spot.position.set(b.g.position.x,40,b.g.position.z+8);});
      /* 시상대가 솟고 막대가 곡선으로 날아옴 */
      var pod=pods[k],P=PODIUM[k],ph=PH[k];
      tw(tLock,.9,function(e){pod.m.scale.y=Math.max(.001,ph*e);pod.m.material.emissiveIntensity=.35*e;pod.n.material.opacity=e;},'back');
      var flyD=big?2:1.6;
      (function(){var C;var f=function(e){var p=C.getPoint(e);b.g.position.copy(p);b.g.lookAt(cam.pos.x,p.y,cam.pos.z);};f.init=function(){var s=b.g.position.clone();C=new T3.CatmullRomCurve3([s,new T3.Vector3(s.x*.55,9+k*2,s.z*.4+3),new T3.Vector3(P.x*.6,6,P.z+2),new T3.Vector3(P.x,ph,P.z)],false,'centripetal');};tw(tLock+.3,flyD,f,'io');})();
      dimBar(b,1,.45,tLock+.3);growBar(b,b.h,tLock+.4,flyD+.2,'out');
      at(tLock+.3,function(){if(b.label){b.label.material.opacity=0;}});
      beams.forEach(function(bm){var A;var f=function(e){var tg=new T3.Vector3(b.g.position.x,b.cur*.6+b.g.position.y,b.g.position.z);bm.userData.cur.copy(tg);aimBeam(bm,tg);};tw(tLock+.3,flyD+.2,f,'lin');});
      var hTop=ph+b.h,fx=new T3.Vector3(P.x,0,P.z);
      camTo(tLock+.3,flyD+.3,[new T3.Vector3(P.x+(k===2?-6:k===3?6:0)*.6,hTop*.7+5,P.z+(14+hTop*.8)*far),new T3.Vector3(P.x*.8,hTop*.5+3,P.z+(10+hTop*1.0)*far)],new T3.Vector3(P.x,hTop*.56,P.z),'io');
      var tHit=tLock+.3+flyD;
      at(tHit,function(){
        b.em.color.set(MED[k]);b.cap.material.color.set(MED[k]);b.cap.material.opacity=1;b.cap.scale.set(5,5,1);
        burst(new T3.Vector3(P.x,hTop,P.z),MED[k],big?420:260,big?18:13,big?2.2:1.8,big?.55:.45,4);
        burst(new T3.Vector3(P.x,hTop,P.z),0xffffff,big?160:90,big?10:7,1.2,.3,1);
        wave(fx,MED[k],big?40:24,big?2:1.5);if(big)wave(fx,0xffffff,60,2.6);
        shake(big?1.2:.6);flash(big?900:420,big?'rgba(255,240,200,.95)':'rgba(255,255,255,.6)');
        b.lift=0;setLabel(b,[k+'등 '+b.p.name,fmt(b.p.total)+'점'],{scale:big?5:4,big:110,col:'#'+MED[k].toString(16),bd:'rgba(255,255,255,.75)',glow:big?'rgba(255,200,80,.95)':'rgba(255,255,255,.6)'});popLabel(b.label,.15);
        b.label.position.y=b.cur+b.label.scale.y/2+(big?2.4:.8);
        revealed[k]=true;
        var pz=(data.prizes||[])[k-1];
        html(ui.mid,'<div class="f3card k'+k+'"><span class="f3med">'+k+'</span><small>'+(big?'최종 1등':k+'등')+'</small><h2>'+esc(b.p.name)+'</h2><em>'+fmt(b.p.total)+'점</em>'+(pz?'<p>상품 · '+esc(pz)+'</p>':'')+'</div>');
        rings[2].material.opacity=big?.8:.5;rings[2].material.color.set(MED[k]);
        lightTo(big?.35:.45,.4,1.2);
      });
      beams.forEach(function(bm){fadeMat(bm.userData.m.material,big?.0:.25,tHit+.6,1.4);});
      if(big){
        tw(tHit-.15,.5,function(e){pillar.material.opacity=.85*e;pillar.scale.y=Math.max(.001,e);pillar.position.y=90-45*e;},'out');
        tw(tHit+1.6,2.4,function(e){pillar.material.opacity=.85-.55*e;},'io');
        at(tHit,function(){crown.visible=true;crown.position.set(P.x,hTop+14,P.z);fireworks=9;confOn=10;confSpawn(CN*.6,0,4,34);});
        tw(tHit+.2,1.8,function(e){crown.position.y=hTop+14-(14-1.25)*e;},'bounce');
        var orb=function(e){var a=Math.PI/2+e*Math.PI*2,r=(11+hTop*.75)*far;cam.pos.set(P.x+Math.cos(a)*r,hTop*.35+2+(hTop*.45+3)*Math.sin(e*Math.PI),P.z+Math.sin(a)*r);cam.look.set(P.x,hTop*.55,P.z);};
        var orbT=0;tw(tHit+1.4,6.5,orb,'io');
        camTo(tHit+8,2.2,[new T3.Vector3(0,hTop*.55+5,P.z+(14+hTop*1.05)*far)],new T3.Vector3(P.x,hTop*.55,P.z),'io');
      }
      return big?tHit+10.4:tHit+2.6;
    }
    function act6(){
      html(ui.mid,'');html(ui.top,'<div class="f3tag">최종 순위</div>');
      var far=mobile&&W<H?1.6:1;
      lightTo(.55,0,1.2);pls.forEach(function(l){tw(0,1.2,function(e){l.intensity=.4+1*e;},'out');});
      bars.forEach(function(b){dimBar(b,.97,b.p.rank<=3?.45:.22,0);if(b.cur<b.h-.01)growBar(b,b.h,.2,1,'out');if(b.p.rank>3&&(!b.label||b.label.material.opacity<.5)){setLabel(b,[b.p.rank+'등 '+b.p.name,fmt(b.p.total)+'점'],{scale:3.3});popLabel(b.label,.4);}});
      camTo(0,4.2,[new T3.Vector3(-Rr*.6,18,(Rr+28)*far),new T3.Vector3(0,22+MAXH*.4,(Rr+40)*far)],new T3.Vector3(0,6,-2),'io');
      confOn=Math.max(confOn,4);
      at(1.5,function(){
        var h='<div class="f3panel f3final in"><h2>최종 순위<small>'+esc(data.period||'')+'</small></h2><div class="f3pod">';
        [2,1,3].forEach(function(k){var x=people[k-1];if(x)h+='<div class="k'+k+'"><b>'+esc(x.name)+'</b><small>'+fmt(x.total)+'점</small><span>'+k+'</span></div>';});
        h+='</div><div class="f3list">'+people.map(function(x){return '<div class="f3row'+(x.me?' me':'')+(x.total>=CUT?' cut':'')+'"><b>'+x.rank+'등</b><span>'+esc(x.name)+'</span><em>'+fmt(x.total)+'점</em></div>';}).join('')+'</div></div>';
        html(ui.side,h);
      });
      return 4.4;
    }
    var ACTS=[act0,act1,act2,function(){return podiumAct(3);},function(){return podiumAct(2);},function(){return podiumAct(1);},act6];
    var NEXT=['','','4등부터 공개','3등 공개','2등 공개','1등 공개','전체 순위 보기'];
    function startAct(i){
      act=i;hideNext();var d=ACTS[i]();
      if(!d&&i<ACTS.length-1){return startAct(i+1);}
      actEnd=T+(d||0);busy=true;
    }
    function onActEnd(){
      busy=false;
      if(act===0)return startAct(1);
      if(act>=ACTS.length-1){ui.skip.hidden=true;ui.next.textContent='닫기';ui.next.hidden=false;ui.next.classList.add('in','close');showClose();return;}
      var nx=act+1;
      if(nx===2&&!bars.some(function(b){return b.p.rank>3;}))nx=3;
      while(nx>=3&&nx<=5&&!barOf(6-nx))nx++;
      showNext(NEXT[nx]||'다음');ui.next.dataset.go=nx;
    }
    function showClose(){var h=ui.side.querySelector('.f3final');if(h&&!h.querySelector('.f3again')){var a=document.createElement('div');a.className='f3again';a.innerHTML='<button class="f3re">다시 보기</button>';h.appendChild(a);a.querySelector('.f3re').onclick=function(){close();if(opt.onReplay)opt.onReplay();};}}
    ui.next.onclick=function(){if(ui.next.classList.contains('close')){close();return;}if(busy)return;startAct(+ui.next.dataset.go||act+1);};
    ui.skip.onclick=function(){skipAll();};
    function skipAll(){
      tws.length=0;evs.length=0;beams.forEach(function(bm){bm.userData.m.material.opacity=0;});html(ui.mid,'');
      [1,2,3].forEach(function(k){var b=barOf(k);if(!b)return;var P=PODIUM[k];b.g.position.set(P.x,PH[k],P.z);b.g.lookAt(0,PH[k],40);pods[k].m.scale.y=PH[k];pods[k].m.material.emissiveIntensity=.35;pods[k].n.material.opacity=1;b.em.color.set(MED[k]);setLabel(b,[k+'등 '+b.p.name,fmt(b.p.total)+'점'],{scale:4,col:'#'+MED[k].toString(16)});b.label.material.opacity=1;revealed[k]=true;});
      var b1=barOf(1);if(b1){crown.visible=true;crown.position.set(PODIUM[1].x,PH[1]+b1.h+1.25,PODIUM[1].z);}
      if(cutPlane){cutPlane.position.y=hCut;cutPlane.userData.a.material.opacity=.13;cutPlane.userData.b.material.opacity=.9;cutLab.position.y=hCut+1.4;cutLab.material.opacity=1;}
      bars.forEach(function(b){b.set(b.h);b.cap.material.opacity=.6;});
      startAct(ACTS.length-1);
    }
    /* ---- 그리기 ---- */
    var last=performance.now()/1000,raf=0,alive=true,shk=new T3.Vector3();
    function frame(){
      if(!alive)return;raf=requestAnimationFrame(frame);
      var now=performance.now()/1000,dt=Math.min(.05,now-last);last=now;if(document.hidden)return;tick(dt);
    }
    function tick(dt){
      T+=dt;
      stepTime();stepBursts(dt);stepWaves(dt);stepConf(dt,T);
      if(confOn>0){confOn-=dt;if(Math.random()<dt*6)confSpawn(Math.round(10+Math.random()*16),0,4,40);}
      if(fireworks>0){fireworks-=dt;fwNext-=dt;if(fwNext<=0){fwNext=.22+Math.random()*.35;var col=[0xffcf4a,0xff5fa8,0x5fd4ff,0x8dff8a,0xffffff,0xb98cff][Math.floor(Math.random()*6)];var p=new T3.Vector3((Math.random()-.5)*Rr*1.6,14+Math.random()*16,-Rr*.4+(Math.random()-.5)*Rr*.8);burst(p,col,mobile?120:200,10+Math.random()*6,2,.42,3.5);if(Math.random()<.5)burst(p,0xffffff,40,4,1,.3,1);}}
      if(busy&&T>=actEnd)onActEnd();
      var st=scene.getObjectByName('stars');if(st)st.rotation.y+=dt*.01;
      dust.rotation.y+=dt*.03;
      rings[0].rotation.z+=dt*.08;rings[1].rotation.z-=dt*.05;rings[2].rotation.z+=dt*.2;rings[3].rotation.z-=dt*.15;
      pls.forEach(function(l,i){var a=T*.35+i*2.1;l.position.set(Math.cos(a)*(Rr*.8),7+Math.sin(T*.7+i)*3,Math.sin(a)*(Rr*.8));});
      if(crown.visible)crown.rotation.y+=dt*1.2;
      bars.forEach(function(b){if(b.label&&b.p.rank<=3&&b.label.material.map&&!revealed[b.p.rank]&&act>=2){var s=1+Math.sin(T*4)*.06;b.label.scale.set(b.label.userData.sc*s,b.label.userData.sc*b.label.userData.ar*s,1);}});
      cam.shake*=Math.pow(.04,dt);shk.set((Math.random()-.5),(Math.random()-.5),(Math.random()-.5)).multiplyScalar(cam.shake);
      camera.position.copy(cam.pos).add(shk);camera.lookAt(cam.look);
      R.render(scene,camera);
    }
    function resize(){W=innerWidth;H=innerHeight;camera.aspect=W/H;camera.updateProjectionMatrix();R.setSize(W,H);}
    addEventListener('resize',resize);
    function onKey(e){if(e.key==='Escape')close();else if((e.key==='Enter'||e.key===' ')&&!ui.next.hidden){e.preventDefault();ui.next.click();}}
    addEventListener('keydown',onKey);
    function close(){
      if(!alive)return;alive=false;cancelAnimationFrame(raf);removeEventListener('resize',resize);removeEventListener('keydown',onKey);
      root.classList.add('out');
      setTimeout(function(){try{scene.traverse(function(o){if(o.geometry)o.geometry.dispose();if(o.material){[].concat(o.material).forEach(function(m){if(m.map)m.map.dispose();m.dispose();});}});R.dispose();}catch(e){}try{root.parentNode.removeChild(root);}catch(e){}document.documentElement.classList.remove('f3on');markClosed();if(opt.onClose)opt.onClose();},450);
    }
    root._close=close;
    root.__fr3={tick:function(dt){tick(dt);},dbg:function(){return {cam:[cam.pos.x,cam.pos.y,cam.pos.z],look:[cam.look.x,cam.look.y,cam.look.z],bars:bars.filter(function(b){return b.p.rank<=3;}).map(function(b){return {r:b.p.rank,p:[b.g.position.x,b.g.position.y,b.g.position.z],h:b.cur,op:b.mat.opacity,vis:b.g.visible};})};},skip:skipAll,next:function(){ui.next.click();},state:function(){return {act:act,busy:busy,T:T,next:ui.next.hidden?'':ui.next.textContent};}};
    if(opt.manual){startAct(0);tick(0);}else{frame();startAct(0);}
  }
  return {play:play,webgl:webgl,load:loadThree};
})();
