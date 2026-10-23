/* ---------- 잠금 화면, 알림창에 공부 시간 (켜고 끄는 설정, 이 기기에만) ---------- */
// 영상처럼 '지금 재생 중' 칸에 과목과 시간을 띄운다. 그러려면 타이머가 도는 동안 소리 없는 소리를 틀어야 해서
// 아이폰, 아이패드에서는 음악 앱이 멈춘다. 그래서 기본은 꺼 두고 원하는 사람만 켠다.
var LK={a:null,showing:false,userPaused:false,key:'',pos:0,start:0};window.__lk=LK;
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
  a.addEventListener('pause',function(){if(LK.showing){LK.showing=false;lockClear();}});
  LK.a=a;
  try{
    var ms=navigator.mediaSession;
    ms.setActionHandler('play',function(){LK.userPaused=false;lockStart();});
    ms.setActionHandler('pause',function(){LK.userPaused=true;lockStop();});
    ['seekbackward','seekforward','seekto','previoustrack','nexttrack'].forEach(function(k){try{ms.setActionHandler(k,null);}catch(e){}});
  }catch(e){}
  return a;
}
function lockLive(){var V=view();return V&&V.me?liveOf(V,V.me):null;}
function lockStart(){
  if(!lockOn())return;var L=lockLive();if(!L)return;
  var a=lockAudio();LK.key='';
  try{var pr=a.play();if(pr&&pr.then)pr.then(function(){LK.showing=true;lockMeta(true);}).catch(function(){});else{LK.showing=true;lockMeta(true);}}catch(e){}
}
function lockClear(){try{navigator.mediaSession.metadata=null;navigator.mediaSession.playbackState='none';}catch(e){}LK.key='';}
function lockStop(){LK.showing=false;if(LK.a){try{LK.a.pause();}catch(e){}}lockClear();}
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
/* 그림: 오늘 공부한 시간(돌고 있는 타이머 포함)과 하루 목표 대비 링. 목표가 없으면 링은 이번 1시간 안에서 돈다 */
function lockToday(V,L,now){
  var day=dayOf(V,V.me,today()),tot=sumMins(day.mins)+sumMins(day.manual);
  if(L){var o=lv(L,now);tot+=Math.max(0,Math.floor(o.focus/60000)-credited(L));}
  return tot;
}
function lockArt(V,L,now){
  var tot=lockToday(V,L,now),gm=+obj(V.progress[V.me]).goalMins||0,col=L&&L.sid&&V.subName[L.sid]?subCol(V,L.sid):'#2B63E6';
  var key=tot+'|'+gm+'|'+col;if(LK.artKey===key&&LK.art)return LK.art;
  try{
    var c=document.createElement('canvas');c.width=c.height=512;var x=c.getContext('2d'),F="-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif";
    var p=gm?Math.min(1,tot/gm):(tot%60)/60;
    x.fillStyle='#F4F6FB';x.fillRect(0,0,512,512);
    x.lineCap='round';x.lineWidth=44;x.strokeStyle='#DDE3EF';x.beginPath();x.arc(256,256,180,0,Math.PI*2);x.stroke();
    if(p>0.002){x.strokeStyle=col;x.beginPath();x.arc(256,256,180,-Math.PI/2,-Math.PI/2+p*Math.PI*2);x.stroke();}
    x.fillStyle='#141B2E';x.textAlign='center';x.textBaseline='alphabetic';x.font='800 124px '+F;
    x.fillText(Math.floor(tot/60)+':'+String(tot%60).padStart(2,'0'),256,284);
    x.fillStyle='#5A6377';x.font='700 32px '+F;
    x.fillText(gm?(tot>=gm?'오늘 목표 채움':'오늘 / 목표 '+fmtMins(gm)):'오늘 공부',256,344);
    LK.art=c.toDataURL('image/png');LK.artKey=key;
  }catch(e){LK.art='';}
  return LK.art;
}
function lockMeta(force){
  var V=view(),L=V&&V.me?liveOf(V,V.me):null;if(!L){lockStop();return;}
  var now=Date.now(),st=lockState(V,L,now),art=lockArt(V,L,now),key=st.title+'|'+st.artist+'|'+st.dur+'|'+LK.artKey;
  try{
    var ms=navigator.mediaSession;
    if(force||key!==LK.key){
      var aw=art?[{src:art,sizes:'512x512',type:'image/png'}]:[];
      ms.metadata=new MediaMetadata({title:st.title,artist:st.artist,album:'공부방',artwork:aw});LK.key=key;force=true;
    }
    ms.playbackState='playing';
    if(ms.setPositionState&&(force||Math.abs(st.pos-LK.pos-(Date.now()-LK.start)/1000)>3)){
      ms.setPositionState({duration:st.dur,playbackRate:1,position:Math.min(st.dur,st.pos)});LK.pos=st.pos;LK.start=Date.now();
    }
  }catch(e){}
}
function lockTick(){
  if(!LK.showing)return;
  if(!lockOn()||!lockLive()){lockStop();return;}
  lockMeta(false);
}
// 타이머를 켜는 누름(또는 설정을 켜는 누름) 바로 뒤에 소리를 시작해야 해서, 앱의 누름 처리 뒤에 붙인다
function lockGesture(){
  if(!lockOn()){if(LK.showing)lockStop();return;}
  var L=lockLive();
  if(!L){if(LK.showing)lockStop();return;}
  if(+L.start!==LK.lastStart){LK.lastStart=+L.start;LK.userPaused=false;}
  if(!LK.showing&&!LK.userPaused)lockStart();
}
setTimeout(function(){document.addEventListener('click',lockGesture);},0);
function lockRow(L){
  if(!lockOk())return '';
  var on=lockOn();
  return '<div class="lockrow"><button class="lockbtn" data-act="lock-toggle" aria-pressed="'+(on?'true':'false')+'"><i aria-hidden="true"></i><span><b>잠금 화면에 공부 시간 보이기</b><small>'+(on?(L&&!LK.showing&&LK.userPaused?'잠금 화면에서 멈췄습니다. 다음에 타이머를 켜면 다시 보입니다.':'켜짐. 타이머가 도는 동안 음악 앱이 멈춥니다.'):'켜면 영상처럼 잠금 화면과 알림창에 과목과 시간이 나옵니다. 그동안 음악 앱은 멈춥니다.')+'</small></span></button></div>';
}
