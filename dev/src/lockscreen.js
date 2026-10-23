/* ---------- 잠금 화면, 알림창에 공부 시간 (켜고 끄는 설정, 이 기기에만) ---------- */
// 영상처럼 '지금 재생 중' 칸에 과목과 시간을 띄운다. 그러려면 타이머가 도는 동안 소리 없는 소리를 틀어야 해서
// 아이폰, 아이패드에서는 음악 앱이 멈춘다. 그래서 기본은 꺼 두고 원하는 사람만 켠다.
// 잠금 화면에서 멈추면 타이머도 멈추고(기록됨), 다시 재생하면 같은 과목, 같은 방식으로 새로 시작한다.
var LK={a:null,showing:false,paused:null,want:false,key:'',pos:0,start:0};window.__lk=LK;
function lockOk(){return 'mediaSession' in navigator&&typeof MediaMetadata!=='undefined';}
function lockOn(){return lockOk()&&lsGet('gbb_lock')==='1';}
function lockWav(){
  // 20초짜리 소리 없는 wav(8kHz, 8비트)를 그 자리에서 만든다
  var sr=8000,n=sr*20,buf=new ArrayBuffer(44+n),v=new DataView(buf),p=0;
  function s4(t){for(var i=0;i<t.length;i++)v.setUint8(p++,t.charCodeAt(i));}
  function u32(x){v.setUint32(p,x,true);p+=4;}
  function u16(x){v.setUint16(p,x,true);p+=2;}
  s4('RIFF');u32(36+n);s4('WAVE');s4('fmt ');u32(16);u16(1);u16(1);u32(sr);u32(sr);u16(1);u16(8);s4('data');u32(n);
  new Uint8Array(buf,44).fill(128);
  return URL.createObjectURL(new Blob([buf],{type:'audio/wav'}));
}
function lockAudio(){
  if(LK.a)return LK.a;
  var a=new Audio();a.src=lockWav();a.loop=true;a.preload='auto';a.setAttribute('playsinline','');
  // 다른 앱 소리, 전화 등으로 끊기면 자리를 비켜 준다(타이머는 그대로). 같은 타이머 동안은 다시 틀지 않는다
  a.addEventListener('pause',function(){if(LK.paused)return;if(LK.showing){LK.showing=false;lockClear();}});
  LK.a=a;
  try{
    var ms=navigator.mediaSession;
    ms.setActionHandler('play',function(){lockResume();});
    ms.setActionHandler('pause',function(){lockPause();});
    try{ms.setActionHandler('stop',function(){lockPause();});}catch(e){}
    ['seekbackward','seekforward','seekto','previoustrack','nexttrack'].forEach(function(k){try{ms.setActionHandler(k,null);}catch(e){}});
  }catch(e){}
  return a;
}
function lockLive(){var V=view();return V&&V.me?liveOf(V,V.me):null;}
function lockStart(){
  if(!lockOn())return;var L=lockLive();if(!L)return;
  var a=lockAudio();LK.key='';LK.paused=null;LK.lastStart=+L.start;
  try{var pr=a.play();if(pr&&pr.then)pr.then(function(){LK.showing=true;lockMeta(true);}).catch(function(){});else{LK.showing=true;lockMeta(true);}}catch(e){}
}
function lockClear(){try{navigator.mediaSession.metadata=null;navigator.mediaSession.playbackState='none';}catch(e){}LK.key='';}
function lockStop(){LK.showing=false;LK.paused=null;if(LK.a){try{LK.a.pause();}catch(e){}}lockClear();}
function lockBtn(){var b=document.createElement('button');return b;}
/* 잠금 화면의 멈춤: 타이머를 끄고(앱의 끄기와 같음) 재생 칸은 '멈춤'으로 남긴다 */
function lockPause(){
  var L=lockLive();
  if(!L){if(!LK.paused)lockStop();else if(LK.a){try{LK.a.pause();}catch(e){}}return;}
  LK.paused={sid:L.sid,mode:L.mode==='pomo'||L.mode==='goal'?L.mode:'sw',f:+L.f||0,b:+L.b||0,g:+L.g||0};
  LK.showing=false;if(LK.a){try{LK.a.pause();}catch(e){}}
  try{act('timer-stop',lockBtn());}catch(e){}
  if(lockLive()){LK.paused=null;lockStart();return;}  // 끌 수 없는 상태(보기 전용 등)면 그대로 둔다
  lockPausedMeta();
}
/* 잠금 화면의 재생: 멈췄던 과목과 방식(스톱워치, 뽀모도로, 목표 시간)으로 새로 시작 */
function lockResume(){
  var P=LK.paused;
  if(P&&!lockLive()&&lockOn()){
    S.draft.timeSub=P.sid;
    if(P.mode==='pomo'&&P.f){S.tmode='pomo';S.pomo={f:P.f,b:P.b||5};}
    else if(P.mode==='goal'&&P.g){S.tmode='goal';S.goal=P.g;}
    else S.tmode='sw';
    try{act('timer-start',lockBtn());}catch(e){}
  }
  if(lockLive())lockStart();
  else if(P)lockPausedMeta();
}
/* 보여 줄 내용: 제목은 과목과 상태, 막대는 지금 구간(스톱워치는 5시간까지, 목표 시간, 뽀모도로는 이번 집중이나 쉬는 시간) */
/* 제목 맨 앞에 시간(1분마다 바뀜): 스톱워치·목표는 공부한 시간, 뽀모도로는 이번 구간 남은 시간 */
function lockMinsDone(ms){var m=Math.floor(ms/60000);return m<1?'방금 시작':fmtMins(m)+'째';}
function lockMinsLeft(ms){var m=Math.ceil(ms/60000);return m<1?'곧 끝':fmtMins(m)+' 남음';}
function lockState(V,L,now){
  var o=lv(L,now),sub=subLabel(V,L.sid),title,artist,dur,pos;
  if(o.mode==='pomo'){
    var f=(+L.f)*60,b=(+L.b)*60,c=f+b,w=(o.e/1000)%c;
    title=o.rest?'쉬는 중 · '+lockMinsLeft(o.left):lockMinsLeft(o.left)+' · '+sub;
    artist=o.rest?sub+' 다음 집중 준비':o.n+'번째 집중 · 뽀모도로 '+L.f+'분';
    dur=o.rest?b:f;pos=o.rest?w-f:w;
  }else if(o.mode==='goal'){
    title=lockMinsDone(o.e)+' · '+sub;
    artist=o.over?'목표 '+fmtMins(+L.g)+' 채움':'목표 '+fmtMins(+L.g)+' · '+lockMinsLeft(o.left);
    dur=(+L.g)*60;pos=Math.min(dur,o.e/1000);
  }else{
    title=lockMinsDone(o.e)+' · '+sub;artist='공부방 스톱워치';dur=MAXRUN/1000;pos=Math.min(dur,o.e/1000);
  }
  return {title:title,artist:artist,dur:Math.max(1,Math.round(dur)),pos:Math.max(0,pos),rest:!!o.rest};
}
/* 오늘 공부한 시간(돌고 있는 타이머 포함) */
function lockToday(V,L,now){
  var day=dayOf(V,V.me,today()),tot=sumMins(day.mins)+sumMins(day.manual);
  if(L){var o=lv(L,now);tot+=Math.max(0,Math.floor(o.focus/60000)-credited(L));}
  return tot;
}
/* 그림: 과목 색 바탕에 오늘 공부 링(하루 목표 대비, 목표가 없으면 이번 1시간 안에서 돎)과 큰 시간.
   밝은 색(파스텔)은 밝은 바탕에 진한 글씨, 나머지는 진한 바탕에 흰 글씨. 멈춤은 색을 눌러 두 막대, 목표를 채우면 체크 */
function lockArt(V,sid,tot,paused){
  var gm=+obj(V.progress[V.me]).goalMins||0,col=sid&&V.subName[sid]?subCol(V,sid):'#2B63E6';
  var key=tot+'|'+gm+'|'+col+'|'+(paused?1:0);if(LK.artKey===key&&LK.art)return LK.art;
  try{
    var c=document.createElement('canvas');c.width=c.height=512;var x=c.getContext('2d'),F="-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif";
    x.fillStyle='#2B63E6';x.fillStyle=col;var hx=/^#[0-9a-f]{6}$/i.test(x.fillStyle)?x.fillStyle:'#2B63E6';
    var rgb=function(h){var n=parseInt(h.slice(1),16);return [n>>16,n>>8&255,n&255];},
        lum=function(a){return (0.2126*a[0]+0.7152*a[1]+0.0722*a[2])/255;},
        mix=function(a,b,t){return [0,1,2].map(function(i){return Math.round(a[i]+(b[i]-a[i])*t);});},
        css=function(a){return 'rgb('+a.join(',')+')';};
    var base=rgb(hx),light=lum(base)>0.62,W=[255,255,255];
    if(paused)base=mix(base,light?[200,204,214]:[70,74,86],0.55);
    var inkC=light?mix(base,[16,18,30],0.78):W,ink=css(inkC),inkA=function(a){return 'rgba('+inkC.join(',')+','+a+')';};
    var g=x.createLinearGradient(0,0,512,512);
    if(light){g.addColorStop(0,css(mix(base,W,0.45)));g.addColorStop(1,css(mix(base,W,0.05)));}
    else{g.addColorStop(0,css(mix(base,W,0.16)));g.addColorStop(1,css(mix(base,[8,10,24],0.38)));}
    x.fillStyle=g;x.fillRect(0,0,512,512);
    var hl=x.createRadialGradient(96,40,0,96,40,440);hl.addColorStop(0,'rgba(255,255,255,'+(light?0.45:0.22)+')');hl.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=hl;x.fillRect(0,0,512,512);
    var cx=256,cy=256,R=170,lw=22,p=gm?Math.min(1,tot/gm):(tot%60)/60,a0=-Math.PI/2,a1=a0+p*Math.PI*2;
    x.lineCap='round';x.lineWidth=lw;x.strokeStyle=inkA(light?0.12:0.2);x.beginPath();x.arc(cx,cy,R,0,Math.PI*2);x.stroke();
    if(p>0.004){x.strokeStyle=inkA(light?0.88:0.96);x.beginPath();x.arc(cx,cy,R,a0,a1);x.stroke();}
    if(p<1){
      var kx=cx+R*Math.cos(a1),ky=cy+R*Math.sin(a1);
      x.save();x.shadowColor='rgba(0,0,0,.22)';x.shadowBlur=10;x.shadowOffsetY=2;x.fillStyle=light?ink:'#fff';x.beginPath();x.arc(kx,ky,lw*0.82,0,Math.PI*2);x.fill();x.restore();
      x.fillStyle=light?css(mix(base,W,0.3)):css(base);x.beginPath();x.arc(kx,ky,lw*0.32,0,Math.PI*2);x.fill();
    }
    x.textAlign='center';x.textBaseline='alphabetic';x.fillStyle=ink;
    var t=Math.floor(tot/60)+':'+String(tot%60).padStart(2,'0'),fs=118;x.font='800 '+fs+'px '+F;
    while(x.measureText(t).width>232&&fs>70){fs-=4;x.font='800 '+fs+'px '+F;}
    x.fillText(t,cx,cy+fs*0.30);
    var done=!paused&&gm&&tot>=gm;
    var lab=paused?'멈춤 · 오늘 공부':gm?(done?'오늘 목표 채움':'목표 '+fmtMins(gm)+' · '+Math.floor(tot/gm*100)+'%'):'오늘 공부';
    x.font='700 25px '+F;x.fillStyle=inkA(0.78);x.fillText(lab,cx,cy+fs*0.30+48);
    var iy=cy-fs*0.62-26;x.fillStyle=inkA(0.92);x.strokeStyle=inkA(0.92);
    if(paused){[cx-10,cx+10].forEach(function(bx){x.beginPath();if(x.roundRect)x.roundRect(bx-4.5,iy-14,9,28,4);else x.rect(bx-4.5,iy-14,9,28);x.fill();});}
    else if(done){x.lineWidth=7;x.lineJoin='round';x.beginPath();x.moveTo(cx-15,iy);x.lineTo(cx-4,iy+11);x.lineTo(cx+17,iy-11);x.stroke();}
    LK.art=c.toDataURL('image/png');LK.artKey=key;
  }catch(e){LK.art='';}
  return LK.art;
}
function lockSet(title,artist,art){
  navigator.mediaSession.metadata=new MediaMetadata({title:title,artist:artist,album:'공부방',artwork:art?[{src:art,sizes:'512x512',type:'image/png'}]:[]});
}
function lockMeta(force){
  var V=view(),L=V&&V.me?liveOf(V,V.me):null;
  if(!L){if(LK.paused)lockPausedMeta();else lockStop();return;}
  var now=Date.now(),st=lockState(V,L,now),art=lockArt(V,L.sid,lockToday(V,L,now),false),key=st.title+'|'+st.artist+'|'+st.dur+'|'+LK.artKey;
  try{
    var ms=navigator.mediaSession;
    if(force||key!==LK.key){lockSet(st.title,st.artist,art);LK.key=key;force=true;}
    ms.playbackState='playing';
    if(ms.setPositionState&&(force||Math.abs(st.pos-LK.pos-(Date.now()-LK.start)/1000)>3)){
      ms.setPositionState({duration:st.dur,playbackRate:1,position:Math.min(st.dur,st.pos)});LK.pos=st.pos;LK.start=Date.now();
    }
  }catch(e){}
}
function lockPausedMeta(){
  var P=LK.paused,V=view();if(!P||!V||!V.me)return;
  var tot=lockToday(V,null,Date.now()),art=lockArt(V,P.sid,tot,true);
  try{
    var ms=navigator.mediaSession;
    lockSet('멈춤 · '+subLabel(V,P.sid),'오늘 '+fmtMins(tot)+' · 재생을 누르면 다시 시작',art);LK.key='';
    ms.playbackState='paused';
  }catch(e){}
}
function lockTick(){
  if(LK.paused){
    if(!lockOn()){lockStop();return;}
    if(lockLive()&&!LK.showing){LK.paused=null;lockClear();}  // 다른 곳에서 타이머를 켬: 앱을 누르면 다시 보임
    return;
  }
  if(!LK.showing)return;
  if(!lockOn()||!lockLive()){lockStop();return;}
  lockMeta(false);
}
// 타이머를 켜는 누름(또는 설정을 켜는 누름) 바로 뒤에 소리를 시작해야 해서, 앱의 누름 처리 뒤에 붙인다
function lockGesture(){
  if(!lockOn()){if(LK.showing||LK.paused)lockStop();return;}
  var L=lockLive();
  if(!L){if(LK.showing)lockStop();return;}
  if(LK.showing)return;
  if(+L.start!==LK.lastStart||LK.want||LK.paused){LK.want=false;lockStart();}
}
setTimeout(function(){document.addEventListener('click',lockGesture);},0);
function lockRow(L){
  if(!lockOk())return '';
  var on=lockOn(),msg;
  if(!on)msg='켜면 영상처럼 잠금 화면과 알림창에 과목과 시간이 나옵니다. 그동안 음악 앱은 멈춥니다.';
  else if(!L&&LK.paused)msg='잠금 화면에서 멈췄습니다. 거기서 재생을 누르면 같은 과목으로 다시 시작합니다.';
  else msg='켜짐. 잠금 화면에서 멈추면 타이머도 멈추고 기록됩니다. 타이머가 도는 동안 음악 앱은 멈춥니다.';
  return '<div class="lockrow"><button class="lockbtn" data-act="lock-toggle" aria-pressed="'+(on?'true':'false')+'"><i aria-hidden="true"></i><span><b>잠금 화면에 공부 시간 보이기</b><small>'+msg+'</small></span></button></div>';
}
