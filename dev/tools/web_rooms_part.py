# ---------------------------------------------------------------- 웹 판: 참여 코드로 방 들어가기, 새 방 만들기, 방 바꾸기
# build_web.py 안에서 exec 된다 (s, sub 를 같이 쓴다).
ROOMS_JS = open(BASE + '/src/rooms.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", ROOMS_JS + "\n/* ---------- 공부방 ---------- */")

# 1) 기기 저장: 방마다 따로 기억해야 하는 값(누구로 들어왔는지, 비밀번호 확인, 읽음 표시 등)은 방 id를 붙여 저장한다.
#    예전 판에서 쓰던 방은 붙이지 않은 값도 이어서 읽는다.
sub("function lsGet(k){try{return localStorage.getItem(k);}catch(e){return null;}}\nfunction lsSet(k,v){try{if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,v);}catch(e){}}",
    r"""var LS_ROOM=(function(){
  try{
    var h=new URLSearchParams(String(location.hash||'').slice(1)),sv=JSON.parse(localStorage.getItem('gbb_remote')||'null');
    if(localStorage.getItem('gbb_legacy_room')==null)localStorage.setItem('gbb_legacy_room',sv&&sv.room?sv.room:'-');
    if(h.get('db'))return h.get('room')||'';
    if(h.get('join'))return '';
    return sv&&sv.room?String(sv.room):'';
  }catch(e){return '';}
})();
var LS_SCOPED={gbb_me:1,gbb_auth:1,gbb_pinask:1,gbb_read:1,gbb_badges:1,gbb_drafts:1,gbb_ahead:1,gbb_due:1};
function lsKey(k){return LS_SCOPED[k]&&LS_ROOM?k+'@'+LS_ROOM:k;}
function lsGet(k){try{var sk=lsKey(k),v=localStorage.getItem(sk);if(v==null&&sk!==k&&localStorage.getItem('gbb_legacy_room')===LS_ROOM)v=localStorage.getItem(k);return v;}catch(e){return null;}}
function lsSet(k,v){try{k=lsKey(k);if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,v);}catch(e){}}""")

# 2) 주소창: #db=..&room=..(예전 초대 링크), #join=..(참여 링크), #j=..(평소)
cut("function remoteConfig(){", "function validRemote(r){", r"""function remoteConfig(){
  var h=null,sv=null,r=null;
  try{h=new URLSearchParams(String(location.hash||'').slice(1));}catch(e){}
  try{sv=JSON.parse(lsGet('gbb_remote')||'null');}catch(e){}
  if(h&&h.get('db')){r={url:String(h.get('db')).replace(/\/+$/,''),room:h.get('room')||''};if(validRemote(r))lsSet('gbb_remote',JSON.stringify(r));}
  else if(h&&(h.get('join')||h.get('j'))){
    var ju=dbFromToken(h.get('join')||h.get('j'));if(!ju)return null;
    if(!h.get('join')&&sv&&String(sv.url).replace(/\/+$/,'')===ju&&validRemote(sv))r=sv;
    else return {join:true,url:ju};
  }
  else r=sv;
  if(r&&r.url)r.url=String(r.url).replace(/\/+$/,'');
  return validRemote(r)?r:null;
}
""")
sub("""    var rc=remoteConfig();
    if(!rc||!window.EventSource||!window.fetch){S.setup=true;S.ready=true;render();return;}
    S.remote=rc;S.net=firebaseNet(rc.url,rc.room);
    try{if(!location.hash)history.replaceState(null,'',inviteLink(rc));}catch(e){}""",
    """    var rc=remoteConfig();
    if(rc&&rc.join&&window.fetch){S.join={url:rc.url};S.ready=true;render();return;}
    if(!rc||!window.EventSource||!window.fetch){S.setup=true;S.ready=true;render();return;}
    S.remote=rc;S.net=firebaseNet(rc.url,rc.room);
    try{syncAddr();}catch(e){}""")
sub("  var gate=S.setup||(S.ready&&!V.me);\n  paintBanner();", "  var gate=S.setup||!!S.join||(S.ready&&!V.me);\n  paintBanner();")
sub("  else if(S.setup)h=viewSetup();", "  else if(S.join)h=viewJoin();\n  else if(S.setup)h=viewSetup();")
sub("S.setup=false;S.setupErr='';S.remote=null;S.importMsg='';",
    "S.setup=false;S.setupErr='';S.remote=null;S.importMsg='';S.join=null;S.jst={err:'',busy:false,fails:0,until:0};S.roomInfo=null;S.nrSubj=true;S.nrBusy=false;S.codeTried=false;")
# 데이터를 받을 때마다 방 정보를 챙긴다
sub("  S.config=c&&typeof c==='object'?c:null;\n  COLLS.forEach(function(k){S[k]=obj(tree[k]);});\n  S.ready=true;render();\n}",
    "  S.config=c&&typeof c==='object'?c:null;\n  S.roomInfo=obj(obj(tree.meta).room);\n  COLLS.forEach(function(k){S[k]=obj(tree[k]);});\n  S.ready=true;render();\n  try{roomTick();}catch(e){}\n}")

# 처음 연결할 때도 방 id가 정해진 상태로 다시 열어서, 방마다 따로 저장하는 값이 처음부터 제자리에 들어가게 한다
sub("""function connect(rc){
  lsSet('gbb_remote',JSON.stringify(rc));
  try{history.replaceState(null,'',inviteLink(rc));}catch(e){}
  S.setup=false;S.setupErr='';S.ready=false;S.readOnly=false;S.remote=rc;S.net=firebaseNet(rc.url,rc.room);render();S.net.start();
}""", """function connect(rc){
  lsSet('gbb_remote',JSON.stringify(rc));roomsRemember({url:rc.url,room:rc.room});
  try{history.replaceState(null,'',inviteLink(rc));}catch(e){}
  location.reload();
}""")
# 3) 첫 화면(연결 화면) 안내와 참여 링크 붙여넣기
sub("<h1>공부방 플래너 연결</h1><p class=\"hint\" style=\"margin-top:6px\">초대 링크를 받았다면 그 링크로 열거나 아래에 붙여넣으세요. 처음 만드는 사람은 Firebase 데이터베이스 주소를 붙여넣으세요. 주소는 처음 한 번만 넣고, 내 다른 기기와 친구들은 초대 링크로 들어옵니다.</p>",
    "<h1>공부방 플래너 연결</h1><p class=\"hint\" style=\"margin-top:6px\">초대 메시지를 받았다면 메시지의 링크를 눌러 열고 참여 코드를 넣으세요. 링크를 아래에 붙여넣어도 됩니다. 처음 만드는 사람만 Firebase 데이터베이스 주소를 붙여넣습니다.</p>")
sub("placeholder=\"https://...firebasedatabase.app\" aria-label=\"초대 링크 또는 데이터베이스 주소\"", "placeholder=\"초대 링크 또는 https://...firebasedatabase.app\" aria-label=\"초대 링크 또는 데이터베이스 주소\"")
sub("""    case 'setup-go':{
      var rcx=parseRemote(S.draft.setupIn);""", """    case 'setup-go':{
      var jtk=/#(?:join|j)=([^&\\s]+)/.exec(String(S.draft.setupIn||''));
      if(jtk&&dbFromToken(jtk[1])){S.setup=false;S.setupErr='';S.join={url:dbFromToken(jtk[1])};S.jst.err='';try{history.replaceState(null,'',siteBase()+'#join='+jtk[1]);}catch(e){}break;}
      var rcx=parseRemote(S.draft.setupIn);""")

# 4) 설정: 맨 위에 방 칸, 저장 위치의 긴 초대 링크는 빼기
sub("""  var dis=canWrite()?'':' disabled',b='<div class="fld"><h3>이 기기에서 누구로 기록할까요</h3><div class="chips">';""",
    """  var dis=canWrite()?'':' disabled',b=roomSec(V)+'<div class="fld"><h3>이 기기에서 누구로 기록할까요</h3><div class="chips">';""")
sub("firebase:'공유 저장소에 연결되어 있습니다. 링크를 가진 참여 인원 모두가 실시간으로 같이 봅니다.'",
    "firebase:'공유 저장소에 연결되어 있습니다. 참여 코드로 들어온 사람 모두가 실시간으로 같이 봅니다.'")
sub("""'<div class="invite"><small>초대 링크</small><p class="url" id="invUrl">'+esc(inviteLink(S.remote))+'</p></div><div class="row" style="margin-top:10px"><button class="btn small primary" data-act="copy-invite">초대 링크 복사</button>""",
    """'<div class="row" style="margin-top:10px">""")
sub("'이 기기 연결 끊기')", "'이 기기에서 이 방 나가기')")
sub("'한 번 더 누르면 연결을 끊습니다'", "'한 번 더 누르면 이 방에서 나갑니다'")
sub("esc(S.importMsg||'초대 링크를 친구들과 내 다른 기기에 보내세요. 기록 가져오기는 처음 연결한 뒤 한 번만 하면 됩니다.')",
    "esc(S.importMsg||'친구와 내 다른 기기는 위의 친구 초대하기로 들어옵니다. 기록 가져오기는 처음 연결한 뒤 한 번만 하면 됩니다.')")
sub("""      lsSet('gbb_remote',null);try{history.replaceState(null,'',String(location.href).split('#')[0]);}catch(e){}""",
    """      if(S.remote){roomsSave(roomsList().filter(function(x){return !(x.url===S.remote.url&&x.room===S.remote.room);}));}
      lsSet('gbb_remote',null);try{history.replaceState(null,'',String(location.href).split('#')[0]);}catch(e){}""")

# 5) 창 열기
sub("  if(type!=='settings'&&type!=='pic'&&!V.me)return;", "  if(type!=='settings'&&type!=='pic'&&type!=='rooms'&&type!=='invite'&&type!=='a2hs'&&!V.me)return;")
sub("  if(type==='plan'){S.pl=newPlan();S.draft.plNote='';}",
    "  if(type==='rooms'){S.jst.err='';S.draft.joinCode='';S.draft.rmRename='';S.nrBusy=false;if(!S.draft.nrPeople&&V.me&&V.byId[V.me])S.draft.nrPeople=V.byId[V.me].name;}\n  if(type==='plan'){S.pl=newPlan();S.draft.plNote='';}")
sub("  if(t==='settings')return modalSettings(V);", "  if(t==='settings')return modalSettings(V);\n  if(t==='rooms')return modalRooms(V);\n  if(t==='invite')return modalInvite(V);\n  if(t==='a2hs')return modalA2HS(V);")
# 처음 안내는 한 번만: 닫으면 표시를 지운다. 그린 뒤마다 띄울 때인지 본다
sub("  if(S.modal.type==='pin')S.autoReward=null;", "  if(S.modal.type==='pin')S.autoReward=null;\n  if(S.modal.type==='a2hs')lsSet('gbb_a2hs',null);")
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);", "  try{a2hsTick();}catch(e){}\n  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);")


# 6) 이름 고르는 화면에 방 이름
sub("""var h='<div class="view" id="view-gate"><div class="gatebox"><div><h1>누구로 들어갈까요?</h1>""",
    """var h='<div class="view" id="view-gate"><div class="gatebox"><div>'+(S.roomInfo&&S.roomInfo.name?'<p class="gaterm">'+esc(S.roomInfo.name)+'</p>':'')+'<h1>누구로 들어갈까요?</h1>""")

# 7) 동작
sub("    case 'copy-rules':", r"""    case 'join-go':joinGo();return;
    case 'room-open':{var roe=roomsList().filter(function(x){return x.room===id;})[0];if(roe)goRoom(roe);return;}
    case 'room-forget':{if(prev!=='rmf:'+id){S.confirm='rmf:'+id;break;}roomsSave(roomsList().filter(function(x){return x.room!==id;}));break;}
    case 'room-invite':if(S.roomInfo&&S.roomInfo.code&&S.remote)copyText(inviteMsg(),'초대 메시지를 복사했습니다. 카카오톡에 붙여넣으세요.',document.getElementById('invMsg'));break;
    case 'nr-subj':S.nrSubj=!S.nrSubj;break;
    case 'nr-make':makeRoom();break;
    case 'room-rename':{
      var Vrn=view(),rnm=String(S.draft.rmRename||'').trim().slice(0,16),rri=S.roomInfo||{};
      if(!rnm||!rri.code||adminId(Vrn)!==Vrn.me||!need())break;
      var nri={name:rnm,code:rri.code,at:rri.at||Date.now()};S.roomInfo=nri;S.draft.rmRename='';S.sync=true;
      S.net.write('meta/room',nri).catch(function(){});
      fbRaw(S.remote.url,'joincode-'+rri.code,'PUT',{r:S.remote.room,n:rnm,at:Date.now()}).catch(function(){});
      roomsRemember({url:S.remote.url,room:S.remote.room,name:rnm,code:rri.code});
      flash('방 이름을 바꿨습니다.');break;
    }
    case 'room-recode':{
      var Vrc=view();if(adminId(Vrc)!==Vrc.me||!need())break;
      if(prev!=='recode'){S.confirm='recode';break;}
      makeCode(true);break;
    }
    case 'copy-rules':""")

# 8) 모양
sub("</style>", """.jcode{font:700 30px/1.2 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace !important;letter-spacing:.32em;text-align:center;padding:14px 10px !important;font-variant-numeric:tabular-nums}
.jcode::placeholder{color:var(--ink-3);opacity:.45}
.jcode.sm{font-size:18px !important;letter-spacing:.18em;padding:10px !important}
#c-joincode{display:flex;flex-direction:column;gap:10px}
#c-joincode .btn{width:100%}
.gaterm{font-size:13px;font-weight:700;color:var(--accent-ink);margin-bottom:4px}
.rmbox{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rmbox>div{min-width:0;padding:10px 12px;border-radius:12px;background:var(--fill)}
.rmbox small,.invbig small{display:block;font-size:12px;color:var(--ink-3);margin-bottom:2px}
.rmbox b{display:block;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rmcode{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:.06em;font-variant-numeric:tabular-nums}
.invbig{margin:0 0 14px;padding:16px 12px;border-radius:14px;background:var(--accent-soft);text-align:center}
.invbig b{display:block;font:800 36px/1.15 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:.1em;color:var(--accent-ink);font-variant-numeric:tabular-nums}
.invsteps{margin:0 0 12px;padding-left:20px;font-size:14px;color:var(--ink-2);display:grid;gap:4px}
.invmsg{margin:0;padding:10px 12px;border-radius:12px;background:var(--fill);font:12.5px/1.55 inherit;font-family:inherit;white-space:pre-wrap;word-break:break-all;-webkit-user-select:all;user-select:all;color:var(--ink-2)}
.rmlist{display:grid;gap:8px}
.rmrow{display:flex;align-items:center;flex-wrap:wrap;gap:8px;padding:10px 12px;border-radius:12px;background:var(--fill)}
.rmrow.on{background:var(--accent-soft)}
.rmn{flex:1;min-width:120px}
.rmn b{display:block;font-size:15px}
.rmn small{font-size:12px;color:var(--ink-3)}
#c-newroom .lb:first-of-type{margin-top:0}
.a2steps{margin:0 0 12px;padding-left:22px;display:grid;gap:10px;font-size:16px;line-height:1.45}
.a2steps b{color:var(--accent-ink)}
.jinapp{margin:0;font-size:13.5px}
.jcode.sm::placeholder{letter-spacing:normal;font:500 15px/1.2 var(--font-body)}
.rmsec{border-top:0;padding-top:0}
.nrchk{display:flex;align-items:center;gap:10px;margin-top:12px;padding:4px 0;border:0;background:none;font-size:14px;color:var(--ink-2);cursor:pointer;text-align:left}
.nrchk i{position:relative;flex:none;width:20px;height:20px;border-radius:6px;box-shadow:inset 0 0 0 2px var(--line);transition:background .15s,box-shadow .15s}
.nrchk[aria-pressed="true"] i{background:var(--accent);box-shadow:none}
.nrchk[aria-pressed="true"] i::after{content:'';position:absolute;left:7px;top:3px;width:5px;height:10px;border:solid var(--on-accent);border-width:0 2px 2px 0;transform:rotate(45deg)}
</style>""")
