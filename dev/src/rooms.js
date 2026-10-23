/* ---------- 방: 참여 코드, 새 방, 방 바꾸기 (웹 판) ---------- */
// 참여 링크: 사이트주소#join=<저장소 이름>  -> 참여 코드 6자리 -> 이름 고르기
// 코드 연결: rooms/joincode-<코드> = {r:방 id, n:방 이름, at}
// 방 정보:   rooms/<방>/d/meta/room = {name, code, at}
var JOIN_LEN=6;
function siteBase(){return String(location.href).split('#')[0];}
function dbToken(url){
  url=String(url||'');
  var m=/^https:\/\/([a-z0-9-]+)-default-rtdb\.([a-z0-9-]+)\.firebasedatabase\.app$/i.exec(url);if(m)return m[1]+'.'+m[2];
  m=/^https:\/\/([a-z0-9-]+)-default-rtdb\.firebaseio\.com$/i.exec(url);if(m)return m[1];
  return encodeURIComponent(url);
}
function dbFromToken(t){
  t=String(t||'');
  if(/^https/i.test(t)){try{t=decodeURIComponent(t);}catch(e){}t=t.replace(/\/+$/,'');return /^https:\/\/[a-z0-9.-]+\.(firebaseio\.com|firebasedatabase\.app)$/i.test(t)?t:'';}
  if(/^[a-z0-9-]+\.[a-z0-9-]+$/i.test(t)){var p=t.split('.');return 'https://'+p[0]+'-default-rtdb.'+p[1]+'.firebasedatabase.app';}
  if(/^[a-z0-9-]+$/i.test(t))return 'https://'+t+'-default-rtdb.firebaseio.com';
  return '';
}
function joinLink(url){return siteBase()+'#join='+dbToken(url);}
function fmtCode(c){c=String(c||'');return c.length===6?c.slice(0,3)+' '+c.slice(3):c;}
function roomsList(){var a=[];try{a=JSON.parse(lsGet('gbb_rooms')||'[]');}catch(e){}return Array.isArray(a)?a.filter(function(x){return x&&x.url&&x.room;}):[];}
function roomsSave(a){lsSet('gbb_rooms',JSON.stringify(a.slice(0,12)));}
function roomEntry(r){return r?roomsList().filter(function(x){return x.url===r.url&&x.room===r.room;})[0]||null:null;}
function roomsRemember(e){
  var a=roomsList(),i=-1;a.forEach(function(x,j){if(x.url===e.url&&x.room===e.room)i=j;});
  if(i<0){a.unshift({url:e.url,room:e.room,name:e.name||'',code:e.code||''});roomsSave(a);return;}
  var x=a[i],ch=false;
  if(e.name&&x.name!==e.name){x.name=e.name;ch=true;}
  if(e.code&&x.code!==e.code){x.code=e.code;ch=true;}
  if(ch)roomsSave(a);
}
function fbRaw(url,path,method,data){
  return fetch(url.replace(/\/+$/,'')+'/rooms/'+path+'.json',{method:method||'GET',headers:{'Content-Type':'application/json'},body:data===undefined?undefined:JSON.stringify(data)})
    .then(function(r){if(!r.ok)throw new Error('http '+r.status);return r.json();});
}
function codeLookup(url,code){return fbRaw(url,'joincode-'+code);}
function newCode(url){
  var n=0;
  function one(){
    var b=new Uint32Array(1);try{crypto.getRandomValues(b);}catch(e){b[0]=Math.floor(Math.random()*4294967295);}
    var c=String(100000+b[0]%900000);
    return codeLookup(url,c).then(function(m){if(!m)return c;if(++n>=6)throw new Error('busy');return one();});
  }
  return one();
}
function goRoom(e){
  roomsRemember(e);
  lsSet('gbb_remote',JSON.stringify({url:e.url,room:e.room}));
  try{history.replaceState(null,'',siteBase()+'#j='+dbToken(e.url));}catch(x){}
  location.reload();
}
function syncAddr(){
  if(!S.remote)return;
  var ri=S.roomInfo||{},e=roomEntry(S.remote),code=ri.code||(e&&e.code);
  var want=code?siteBase()+'#j='+dbToken(S.remote.url):inviteLink(S.remote);
  if(String(location.href)!==want){try{history.replaceState(null,'',want);}catch(x){}}
}
function makeCode(re){
  if(!S.remote||!S.net||S.net.mode!=='firebase')return;
  var url=S.remote.url,room=S.remote.room,old=(S.roomInfo||{}).code||'';
  return newCode(url).then(function(code){
    return S.net.read('meta/room').then(function(cur){
      cur=obj(cur);
      if(!re&&cur.code)return;
      var name=String(cur.name||(S.roomInfo||{}).name||'공부방'),now=Date.now();
      return fbRaw(url,'joincode-'+code,'PUT',{r:room,n:name,at:now}).then(function(){
        var ni={name:name,code:code,at:now};
        return S.net.write('meta/room',ni).then(function(){
          S.roomInfo=ni;
          if(re&&old&&old!==code)fbRaw(url,'joincode-'+old,'DELETE').catch(function(){});
          roomTick();
          if(re)flash('참여 코드를 '+fmtCode(code)+'(으)로 바꿨습니다.');
          render();
        });
      });
    });
  }).catch(function(){if(re){flash('코드를 바꾸지 못했습니다. 인터넷 연결을 확인해 주세요.');render();}});
}
function roomTick(){
  if(!S.remote||!S.net||S.net.mode!=='firebase')return;
  var ri=S.roomInfo||{};
  roomsRemember({url:S.remote.url,room:S.remote.room,name:ri.name||'',code:ri.code||''});
  syncAddr();
  if(!ri.code&&!S.codeTried&&canWrite()){S.codeTried=true;setTimeout(function(){makeCode(false);},400);}
  if(S.ready){var lf=null;try{lf=sessionStorage.getItem('gbb_left');if(lf)sessionStorage.removeItem('gbb_left');}catch(e){}if(lf)flash("'"+lf+"'에서 나왔습니다. "+jos(roomName(),'으로','로')+' 옮겼습니다.');}
  if(view().me&&!S.modal){
    var f=null;try{f=sessionStorage.getItem('gbb_newroom');}catch(e){}
    if(f&&ri.code){try{sessionStorage.removeItem('gbb_newroom');}catch(e){}setTimeout(function(){if(!S.modal){openModal('invite',null);render();}},350);}
  }
}
function roomName(){return (S.roomInfo&&S.roomInfo.name)||'공부방';}
function inviteMsg(){
  var ri=S.roomInfo||{};
  return '공부방 플래너 \''+roomName()+'\'에 초대합니다.\n1. 링크 열기: '+joinLink(S.remote.url)+'\n2. 참여 코드 넣기: '+ri.code+'\n3. 내 이름 고르기/추가하기';
}

/* 참여 코드 넣는 화면 */
function viewJoin(){
  var J=S.join,st=S.jst,mine=roomsList();
  var h='<div class="view" id="view-join"><div class="gatebox"><div><h1>공부방 들어가기</h1><p class="hint" style="margin-top:6px">초대 메시지에 있는 참여 코드 6자리를 넣으세요.</p></div>';
  if(a2hsKind()==='inapp')h+='<p class="notice jinapp">'+inappName()+' 안에서 열렸습니다. 앱으로 쓰려면 메뉴에서 <b>다른 브라우저로 열기</b>를 먼저 누르세요.</p>';
  else if(a2hsKind()==='ios-inapp')h+='<div class="notice jinapp jgo"><p>'+inappName()+' 안에서 열렸습니다. 앱으로 쓰려면 <b>구글 앱</b>에서 여세요. 링크를 복사해 구글 앱 검색창에 붙여넣으면 됩니다.</p><button class="btn small primary" data-act="kakao-copy">링크 복사</button></div>';
  h+='<section class="card" id="c-joincode"><input id="joinCode" class="jcode" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" maxlength="7" data-draft="joinCode" data-enter="join-go" placeholder="000000" aria-label="참여 코드 6자리"'+(st.busy?' disabled':'')+'><button class="btn primary" data-act="join-go"'+(st.busy?' disabled':'')+'>'+(st.busy?'확인하는 중':'들어가기')+'</button>'+(st.err?'<p class="hint serr" role="status">'+esc(st.err)+'</p>':'')+'</section>';
  if(mine.length){
    h+='<section class="card"><h2 class="sh">이 기기에서 들어갔던 방</h2><div class="people">';
    mine.forEach(function(x){h+='<button class="person" data-act="room-open" data-id="'+esc(x.room)+'"><span style="flex:1">'+esc(x.name||'공부방')+'</span><em class="tag">열기</em></button>';});
    h+='</div></section>';
  }
  return h+'</div></div>';
}
function joinFail(msg){S.jst.busy=false;S.jst.err=msg;S.draft.joinCode='';S.sync=true;render();var e=document.getElementById('joinCode')||document.getElementById('rmCode');if(e)try{e.focus();}catch(x){}}
function joinGo(){
  var st=S.jst,url=S.join?S.join.url:(S.remote&&S.remote.url);
  if(!url||st.busy)return;
  var code=String(S.draft.joinCode||'').replace(/\D/g,'');
  if(Date.now()<st.until){st.err='여러 번 틀려서 잠시 막혔습니다. 30초 뒤에 다시 넣어 주세요.';render();return;}
  if(code.length!==JOIN_LEN){st.err='참여 코드는 숫자 6자리입니다.';render();return;}
  st.busy=true;st.err='';render();
  codeLookup(url,code).then(function(m){
    if(!m||!m.r||!/^[A-Za-z0-9_-]{12,40}$/.test(m.r)){
      st.fails=(st.fails||0)+1;if(st.fails>=5){st.fails=0;st.until=Date.now()+30000;}
      joinFail('맞는 방이 없습니다. 코드를 다시 확인해 주세요.');return;
    }
    if(S.remote&&S.remote.url===url&&S.remote.room===m.r){st.busy=false;S.draft.joinCode='';closeModal();flash('이미 이 방에 있습니다.');render();return;}
    lsSet('gbb_a2hs','1');
    goRoom({url:url,room:m.r,name:String(m.n||''),code:code});
  }).catch(function(){joinFail('확인하지 못했습니다. 인터넷 연결을 확인해 주세요.');});
}
document.addEventListener('input',function(e){
  var t=e.target;if(!t||!t.classList||!t.classList.contains('jcode'))return;
  var d=String(t.value||'').replace(/\D/g,'');
  if(d!==t.value&&d.length<=JOIN_LEN){t.value=d;}
  S.draft.joinCode=d;
  if(d.length===JOIN_LEN&&!S.jst.busy)joinGo();
});

/* 설정의 방 칸 */
function roomSec(V){
  if(!S.net||S.net.mode!=='firebase'||!S.remote)return '';
  var ri=S.roomInfo||{},isAdm=!!(V.me&&adminId(V)===V.me);
  var h='<div class="sec rmsec"><h3>방</h3><div class="rmbox"><div><small>지금 방</small><b>'+esc(roomName())+'</b></div><div><small>참여 코드</small><b class="rmcode">'+(ri.code?fmtCode(ri.code):'만드는 중')+'</b></div></div>';
  if(S.net.size)h+='<p class="hint rmsz">이 방 기록 '+fmtBytes(S.net.size())+' · 이 기기가 이번 달 받은 양 '+fmtBytes(dlMonth())+'</p>';
  h+='<div class="row" style="margin-top:10px"><button class="btn small primary" data-act="open" data-modal="invite"'+(ri.code?'':' disabled')+'>친구 초대하기</button>'+(isAdm&&ri.code?'<button class="btn small" data-act="open" data-modal="roomadm">방 이름, 코드 바꾸기</button>':'')+(isStandalone()?'':'<button class="btn small" data-act="open" data-modal="a2hs">앱으로 추가하기</button>')+'</div>';
  h+='<div class="rmacts"><button class="rmact mv" data-act="open" data-modal="rooms"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 8h13M13 4l4 4-4 4M20 16H7M11 12l-4 4 4 4"/></svg></i><span><b>방 옮기기</b><small>다른 방으로 가기</small></span></button>';
  h+='<button class="rmact nw" data-act="open" data-modal="newroom"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></i><span><b>새로운 방 만들기</b><small>기록은 새로 시작</small></span></button></div></div>';
  return h;
}
function modalInvite(V){
  var ri=S.roomInfo||{};
  if(!ri.code||!S.remote)return dlg('',{id:'invite',t:'친구 초대하기'},'<p class="hint">참여 코드를 만드는 중입니다. 잠시 뒤에 다시 열어 주세요.</p>');
  var b='<div class="invbig"><small>'+esc(roomName())+' 참여 코드</small><b>'+fmtCode(ri.code)+'</b></div>';
  b+='<ol class="invsteps"><li>초대 메시지를 카카오톡에 붙여넣기</li><li>친구가 링크를 열고 참여 코드 6자리 넣기</li><li>자기 이름 고르기 (없으면 직접 추가)</li></ol>';
  b+='<pre class="invmsg" id="invMsg">'+esc(inviteMsg())+'</pre>';
  b+='<div class="row" style="margin-top:12px"><button class="btn primary" data-act="room-invite">초대 메시지 복사</button></div>';
  return dlg('',{id:'invite',t:'친구 초대하기'},b);
}
function modalRooms(V){
  var cur=S.remote,list=roomsList(),st=S.jst;
  list.sort(function(a,b){var ac=cur&&a.room===cur.room?0:1,bc=cur&&b.room===cur.room?0:1;return ac-bc;});
  var b='<div class="sec" style="margin-top:0"><h3>이 기기에서 들어간 방</h3><div class="rmlist">';
  list.forEach(function(x){
    var on=!!(cur&&x.room===cur.room&&x.url===cur.url);
    b+='<div class="rmrow'+(on?' on':'')+'"><div class="rmn"><b>'+esc(on?roomName():(x.name||'공부방'))+'</b><small>'+(on?'지금 방':(x.code?'참여 코드 '+fmtCode(x.code):''))+'</small></div>';
    if(!on)b+='<button class="btn small" data-act="room-open" data-id="'+esc(x.room)+'">이 방으로</button><button class="del" data-act="room-forget" data-id="'+esc(x.room)+'">'+(S.confirm==='rmf:'+x.room?'한 번 더 누르면 뺍니다':'목록에서 빼기')+'</button>';
    b+='</div>';
  });
  b+='</div>'+(list.length<2?'<p class="hint" style="margin-top:6px">다른 방에 들어가 본 적이 없습니다. 친구에게 받은 참여 코드를 아래에 넣으세요.</p>':'')+'</div>';
  b+='<div class="sec"><h3>참여 코드로 다른 방 들어가기</h3><div class="row"><input id="rmCode" class="jcode sm" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" maxlength="7" data-draft="joinCode" data-enter="join-go" placeholder="참여 코드 6자리" aria-label="참여 코드 6자리"><button class="btn" data-act="join-go"'+(st.busy?' disabled':'')+'>들어가기</button></div>'+(st.err?'<p class="hint serr" role="status">'+esc(st.err)+'</p>':'')+'</div>';
  b+='<p class="hint rmswap">방을 새로 만들려면 <button class="linkbtn" data-act="open" data-modal="newroom">새로운 방 만들기</button></p>';
  return dlg('',{id:'rooms',t:'방 옮기기'},b);
}
function modalNewRoom(V){
  var b='<div class="sec" id="c-newroom" style="margin-top:0"><p class="hint" style="margin:0 0 10px">지금 방은 그대로 두고, 기록이 비어 있는 방을 하나 더 만듭니다. 만든 뒤 바로 그 방으로 옮겨 갑니다.</p>';
  b+='<label class="lb" for="nrName">방 이름</label><input id="nrName" type="text" maxlength="16" data-draft="nrName" placeholder="예: 2학년 공부방">';
  b+='<label class="lb" for="nrPeople">참여할 사람</label><textarea id="nrPeople" rows="4" data-draft="nrPeople" placeholder="한 줄에 한 명씩 적으세요. 맨 위가 방장입니다."></textarea>';
  b+='<p class="hint" style="margin-top:6px">비워 두어도 됩니다. 들어온 친구가 자기 이름을 직접 추가할 수 있습니다.</p>';
  b+='<button class="nrchk" data-act="nr-subj" aria-pressed="'+(S.nrSubj?'true':'false')+'"><i aria-hidden="true"></i>지금 방의 과목 목록 그대로 쓰기</button>';
  b+='<div class="row" style="margin-top:12px"><button class="btn primary" data-act="nr-make"'+(S.nrBusy?' disabled':'')+'>'+(S.nrBusy?'만드는 중':'새로운 방 만들기')+'</button></div></div>';
  return dlg('',{id:'newroom',t:'새로운 방 만들기'},b);
}
function modalRoomAdm(V){
  var ri=S.roomInfo||{};
  if(!(V.me&&adminId(V)===V.me&&ri.code))return dlg('',{id:'roomadm',t:'방 이름, 코드 바꾸기'},'<p class="hint">방장만 바꿀 수 있습니다.</p>');
  var b='<div class="sec" style="margin-top:0"><label class="lb" for="rmRename" style="margin-top:0">방 이름</label><div class="row"><input id="rmRename" type="text" maxlength="16" data-draft="rmRename" data-enter="room-rename" placeholder="'+esc(roomName())+'"><button class="btn small" data-act="room-rename">이름 바꾸기</button></div></div>';
  b+='<div class="sec"><h3>참여 코드<small>지금 '+fmtCode(ri.code)+'</small></h3><div class="row"><button class="btn small'+(S.confirm==='recode'?' warn':'')+'" data-act="room-recode">'+(S.confirm==='recode'?'한 번 더 누르면 코드를 바꿉니다':'참여 코드 바꾸기')+'</button></div><p class="hint" style="margin-top:6px">코드를 바꾸면 예전 코드로는 들어올 수 없습니다. 이미 들어온 사람은 그대로입니다.</p></div>';
  return dlg('',{id:'roomadm',t:'방 이름, 코드 바꾸기'},b);
}
function makeRoom(){
  if(!S.remote||!S.net||S.nrBusy)return;
  var nm=String(S.draft.nrName||'').trim().slice(0,16)||'새 공부방',seen={};
  var ppl=String(S.draft.nrPeople||'').split(/[\n,]+/).map(function(x){return x.trim().slice(0,12);}).filter(function(x){if(!x||seen[x])return false;seen[x]=1;return true;}).slice(0,12);
  var url=S.remote.url,room=newRoom(),cfg=clone(obj(S.config)),subs=S.nrSubj?clone(obj(S.subjects)):{};
  delete cfg.roster;delete cfg.admin;
  cfg.roster=ppl.map(function(n,i){return {id:'m'+(i+1),name:n};});
  if(typeof cfg.certHour!=='number')cfg.certHour=26;
  S.nrBusy=true;render();
  newCode(url).then(function(code){
    var now=Date.now(),jobs=[[room+'/d/meta/config',cfg],[room+'/d/meta/room',{name:nm,code:code,at:now}]];
    Object.keys(subs).forEach(function(k){if(/^[A-Za-z0-9_-]{1,80}$/.test(k)&&subs[k]&&typeof subs[k]==='object')jobs.push([room+'/d/subjects/'+k,subs[k]]);});
    jobs.push(['joincode-'+code,{r:room,n:nm,at:now}]);
    var i=0;
    function next(){if(i>=jobs.length)return Promise.resolve();var j=jobs[i++];return fbRaw(url,j[0],'PUT',j[1]).then(next);}
    return next().then(function(){
      if(ppl.length){try{localStorage.setItem('gbb_me@'+room,'m1');localStorage.setItem('gbb_pinask@'+room,JSON.stringify({m1:1}));}catch(e){}}
      try{sessionStorage.setItem('gbb_newroom','1');}catch(e){}
      S.draft.nrName='';S.draft.nrPeople='';persistDrafts();
      goRoom({url:url,room:room,name:nm,code:code});
    });
  }).catch(function(){S.nrBusy=false;flash('방을 만들지 못했습니다. 인터넷 연결을 확인해 주세요.');render();});
}

/* 처음 방에 들어온 사람에게: 홈 화면에 앱으로 추가하는 법 (기기에 맞는 것만) */
function isStandalone(){try{return window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;}catch(e){return false;}}
/* 링크를 연 앱 이름 (주소창 없는 앱 안 브라우저). 디스코드처럼 사파리나 크롬 화면을 그대로 쓰는 앱은 구분되지 않는다 */
function inappName(){
  var ua=navigator.userAgent||'';
  if(/KAKAOTALK/i.test(ua))return '카톡';
  if(/Instagram/i.test(ua))return '인스타그램';
  if(/FBAN|FBAV|FB_IAB/i.test(ua))return '페이스북';
  if(/NAVER\(/i.test(ua))return '네이버 앱';
  if(/Line\//i.test(ua))return '라인';
  if(/Everytimeapp/i.test(ua))return '에브리타임';
  if(/Twitter|TwitterAndroid/i.test(ua))return 'X';
  return '';
}
function a2hsKind(){
  var ua=navigator.userAgent||'',ios=/iPhone|iPad|iPod/.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  // 카톡, 인스타그램 같은 앱 안에서 열린 경우: 아이폰, 아이패드는 구글 앱으로, 안드로이드는 다른 브라우저로
  if(inappName())return ios?'ios-inapp':'inapp';
  if(ios)return /GSA\//.test(ua)?'ios-google':/CriOS/.test(ua)?'ios-chrome':'ios-safari';
  if(/Android/.test(ua))return 'android';
  return 'pc';
}
/* 휴대폰 화면의 단추 모양을 본뜬 그림 */
var A2IC={
  link:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2"/></svg>',
  search:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/></svg>',
  share:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 9.5H7a2 2 0 0 0-2 2v7.5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7.5a2 2 0 0 0-2-2h-1.5"/><path d="M12 14.5V3"/><path d="M8.3 6.6 12 3l3.7 3.6"/></svg>',
  more:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 9.5 12 15l5.5-5.5"/></svg>',
  plus:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><path d="M12 8v8M8 12h8"/></svg>',
  dots:'<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5.5" r="1.9"/><circle cx="12" cy="12" r="1.9"/><circle cx="12" cy="18.5" r="1.9"/></svg>',
  hdots:'<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5.5" cy="12" r="1.9"/><circle cx="12" cy="12" r="1.9"/><circle cx="18.5" cy="12" r="1.9"/></svg>',
  install:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8"/><path d="M12 7.5v6M9.3 10.8 12 13.5l2.7-2.7"/></svg>',
  open:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/></svg>'
};
function a2Pic(k){
  if(k==='share')return '<span class="a2ic">'+A2IC.share+'</span>';
  if(k==='more')return '<span class="a2ic circ"><span class="a2c">'+A2IC.more+'</span><small>더 보기</small></span>';
  if(k==='addrow')return '<span class="a2ic row">'+A2IC.plus+'<span>홈 화면에 추가</span></span>';
  if(k==='add')return '<span class="a2ic pill">추가</span>';
  if(k==='install')return '<span class="a2ic pill">설치</span>';
  if(k==='dots')return '<span class="a2ic">'+A2IC.dots+'</span>';
  if(k==='pcinstall')return '<span class="a2ic">'+A2IC.install+'</span>';
  if(k==='menu')return '<span class="a2ic">'+A2IC.hdots+'</span>';
  if(k==='openrow')return '<span class="a2ic row">'+A2IC.open+'<span>다른 브라우저로 열기</span></span>';
  if(k==='copylink')return '<span class="a2ic row">'+A2IC.link+'<span>링크 복사</span></span>';
  if(k==='paste')return '<span class="a2ic sbar">'+A2IC.search+'<span>붙여넣기</span></span>';
  return '';
}
function a2hsSteps(k){
  return {
    'inapp':[['menu','오른쪽 아래나 위의 <b>메뉴</b> 누르기'],['openrow','<b>다른 브라우저로 열기</b> 누르기'],['code','열린 화면에서 <b>참여 코드</b> 다시 넣기']],
    'ios-inapp':[['copylink','아래 <b>링크 복사</b> 누르기'],['gapp','<b>구글 앱</b> 열기'],['paste','검색창에 <b>붙여넣기</b>'],['code','열린 화면에서 <b>참여 코드</b> 다시 넣기']],
    'ios-google':[['share','<b>공유 버튼</b> 누르기'],['more','<b>더 보기</b> 누르기'],['addrow','<b>홈 화면에 추가</b> 누르기'],['add','오른쪽 위 <b>추가</b> 누르기']],
    'ios-chrome':[['share','주소창 오른쪽 <b>공유 버튼</b> 누르기'],['more','<b>더 보기</b> 누르기'],['addrow','<b>홈 화면에 추가</b> 누르기'],['add','오른쪽 위 <b>추가</b> 누르기']],
    'ios-safari':[['share','<b>공유 버튼</b> 누르기'],['more','<b>더 보기</b> 누르기'],['addrow','<b>홈 화면에 추가</b> 누르기'],['add','오른쪽 위 <b>추가</b> 누르기']],
    'android':[['dots','오른쪽 위 <b>점 세 개</b> 누르기'],['addrow','<b>홈 화면에 추가</b>(또는 앱 설치) 누르기'],['install','<b>설치</b> 누르기']],
    'pc':[['pcinstall','주소창 오른쪽 <b>설치 아이콘</b> 누르기'],['install','<b>설치</b> 누르기']]
  }[k];
}
function modalA2HS(V){
  var k=a2hsKind(),st=a2hsSteps(k),ios=k.indexOf('ios')===0;
  var b='<ol class="a2steps">'+st.map(function(x,i){var pic=a2Pic(x[0]);return '<li><span class="a2n">'+(i+1)+'</span>'+pic+'<span class="a2t'+(pic?'':' wide')+'">'+x[1]+'</span></li>';}).join('')+'</ol>';
  if(k==='inapp')b='<p class="hint" style="margin-bottom:12px">'+inappName()+' 안에서는 앱으로 추가할 수 없습니다.</p>'+b;
  else if(k==='ios-google')b='<p class="hint" style="margin-bottom:12px">구글 앱에서는 이 순서로 눌러야 합니다.</p>'+b;
  else if(k==='ios-safari')b='<p class="hint" style="margin-bottom:12px">공유 버튼이 안 보이면 주소창 옆 <b>점 세 개</b>를 먼저 누르세요.</p>'+b;
  else if(k==='ios-inapp')b='<p class="hint" style="margin-bottom:12px">'+inappName()+' 대신 구글 앱에서 열어야 앱으로 추가할 수 있습니다.</p>'+b;
  if(k!=='inapp'&&k!=='ios-inapp')b+='<p class="hint">'+(ios?'이제 홈 화면의 공부방 아이콘으로 여세요. 처음 열 때 참여 코드를 한 번 더 넣습니다.':'이제 홈 화면의 공부방 아이콘으로 여세요.')+'</p>';
  if(k==='ios-inapp')b+='<p class="kklink" id="kkLink">'+esc(kakaoLink())+'</p><p class="hint">구글 앱에서 들어오면 앱으로 추가하는 방법이 다시 나옵니다.</p>';
  b+='<div class="row" style="margin-top:14px">'+(k==='ios-inapp'?'<button class="btn primary" data-act="kakao-copy">링크 복사</button><button class="btn" data-act="modal-close">닫기</button>':'<button class="btn primary" data-act="modal-close">확인</button>')+'</div>';
  return dlg('',{id:'a2hs',t:k==='inapp'?'다른 브라우저로 열어 주세요':k==='ios-inapp'?'구글 앱에서 열어 주세요':'앱으로 추가하기'},b);
}
/* 카톡 같은 앱에서 연 링크를 구글 앱에서 열 수 있게 복사 */
function kakaoLink(){var u=(S.remote&&S.remote.url)||(S.join&&S.join.url);return u?joinLink(u):String(location.href);}
function kakaoCopy(){copyText(kakaoLink(),'링크를 복사했습니다. 구글 앱 검색창에 붙여넣으세요.',document.getElementById('kkLink'));
}
function a2hsTick(){
  if(!lsGet('gbb_a2hs'))return;
  if(isStandalone()){lsSet('gbb_a2hs',null);return;}
  var V=V0;if(!S.ready||!V||!V.me||S.modal||S.check||S.missed||S.a2hsT)return;
  S.a2hsT=setTimeout(function(){S.a2hsT=null;if(!S.modal&&!S.check&&!S.missed&&lsGet('gbb_a2hs')&&V0&&V0.me){openModal('a2hs',null);render();}},1500);
}
