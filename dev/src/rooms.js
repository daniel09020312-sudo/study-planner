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
  if(view().me&&!S.modal){
    var f=null;try{f=sessionStorage.getItem('gbb_newroom');}catch(e){}
    if(f&&ri.code){try{sessionStorage.removeItem('gbb_newroom');}catch(e){}setTimeout(function(){if(!S.modal){openModal('invite',null);render();}},350);}
  }
}
function roomName(){return (S.roomInfo&&S.roomInfo.name)||'공부방';}
function inviteMsg(){
  var ri=S.roomInfo||{};
  return '공부방 플래너 \''+roomName()+'\'에 초대합니다.\n1. 링크 열기: '+joinLink(S.remote.url)+'\n2. 참여 코드 넣기: '+ri.code+'\n3. 내 이름 고르기';
}

/* 참여 코드 넣는 화면 */
function viewJoin(){
  var J=S.join,st=S.jst,mine=roomsList();
  var h='<div class="view" id="view-join"><div class="gatebox"><div><h1>공부방 들어가기</h1><p class="hint" style="margin-top:6px">초대 메시지에 있는 참여 코드 6자리를 넣으세요.</p></div>';
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
  var ri=S.roomInfo||{};
  var h='<div class="sec rmsec"><h3>방</h3><div class="rmbox"><div><small>지금 방</small><b>'+esc(roomName())+'</b></div><div><small>참여 코드</small><b class="rmcode">'+(ri.code?fmtCode(ri.code):'만드는 중')+'</b></div></div>';
  h+='<div class="row" style="margin-top:10px"><button class="btn small primary" data-act="open" data-modal="invite"'+(ri.code?'':' disabled')+'>친구 초대하기</button><button class="btn small" data-act="open" data-modal="rooms">다른 방, 새 방 만들기</button></div></div>';
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
  var cur=S.remote,list=roomsList(),ri=S.roomInfo||{},isAdm=!!(V.me&&adminId(V)===V.me),st=S.jst;
  list.sort(function(a,b){var ac=cur&&a.room===cur.room?0:1,bc=cur&&b.room===cur.room?0:1;return ac-bc;});
  var b='<div class="sec" style="margin-top:0"><h3>이 기기에서 들어간 방</h3><div class="rmlist">';
  list.forEach(function(x){
    var on=!!(cur&&x.room===cur.room&&x.url===cur.url);
    b+='<div class="rmrow'+(on?' on':'')+'"><div class="rmn"><b>'+esc(on?roomName():(x.name||'공부방'))+'</b><small>'+(on?'지금 방':(x.code?'참여 코드 '+fmtCode(x.code):''))+'</small></div>';
    if(!on)b+='<button class="btn small" data-act="room-open" data-id="'+esc(x.room)+'">열기</button><button class="del" data-act="room-forget" data-id="'+esc(x.room)+'">'+(S.confirm==='rmf:'+x.room?'한 번 더 누르면 뺍니다':'목록에서 빼기')+'</button>';
    b+='</div>';
  });
  b+='</div></div>';
  b+='<div class="sec"><h3>참여 코드로 다른 방 들어가기</h3><div class="row"><input id="rmCode" class="jcode sm" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" maxlength="7" data-draft="joinCode" data-enter="join-go" placeholder="참여 코드 6자리" aria-label="참여 코드 6자리"><button class="btn" data-act="join-go"'+(st.busy?' disabled':'')+'>들어가기</button></div>'+(st.err?'<p class="hint serr" role="status">'+esc(st.err)+'</p>':'')+'</div>';
  b+='<div class="sec" id="c-newroom"><h3>새 방 만들기<small>기록은 새로 시작합니다</small></h3>';
  b+='<label class="lb" for="nrName">방 이름</label><input id="nrName" type="text" maxlength="16" data-draft="nrName" placeholder="예: 2학년 공부방">';
  b+='<label class="lb" for="nrPeople">참여할 사람</label><textarea id="nrPeople" rows="4" data-draft="nrPeople" placeholder="한 줄에 한 명씩 적으세요. 맨 위가 방장입니다."></textarea>';
  b+='<p class="hint" style="margin-top:6px">비워 두어도 됩니다. 들어온 친구가 자기 이름을 직접 추가할 수 있습니다.</p>';
  b+='<button class="nrchk" data-act="nr-subj" aria-pressed="'+(S.nrSubj?'true':'false')+'"><i aria-hidden="true"></i>지금 방의 과목 목록 그대로 쓰기</button>';
  b+='<div class="row" style="margin-top:12px"><button class="btn primary" data-act="nr-make"'+(S.nrBusy?' disabled':'')+'>'+(S.nrBusy?'만드는 중':'새 방 만들기')+'</button></div></div>';
  if(isAdm&&ri.code){
    b+='<div class="sec"><h3>이 방 관리<small>방장만</small></h3><label class="lb" for="rmRename">방 이름</label><div class="row"><input id="rmRename" type="text" maxlength="16" data-draft="rmRename" data-enter="room-rename" placeholder="'+esc(roomName())+'"><button class="btn small" data-act="room-rename">이름 바꾸기</button></div>';
    b+='<div class="row" style="margin-top:10px"><button class="btn small'+(S.confirm==='recode'?' warn':'')+'" data-act="room-recode">'+(S.confirm==='recode'?'한 번 더 누르면 코드를 바꿉니다':'참여 코드 바꾸기')+'</button></div><p class="hint" style="margin-top:6px">코드를 바꾸면 예전 코드로는 들어올 수 없습니다. 이미 들어온 사람은 그대로입니다.</p></div>';
  }
  return dlg('',{id:'rooms',t:'방'},b);
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
