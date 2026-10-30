# Claude 밖(GitHub Pages 등)에서 쓰는 한 파일짜리 플래너를 만든다.
# 기본 빌드(study-room-planner.html)를 바탕으로:
#  - morphdom을 파일 안에 넣고, 이모티콘 36개를 파일 안에 넣는다.
#  - 저장소 주소가 없으면 연결 화면을 보여주고, 초대 링크와 기록 가져오기를 넣는다.
import base64, json, os
BASE = '/home/claude/planner'
NPM = BASE + '/tools/npm/node_modules'
s = open(BASE + '/study-room-planner.html', encoding='utf-8').read()


def sub(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, ('count', n, a[:90])
    s = s.replace(a, b)


def cut(a, b, new):
    """a에서 시작해 b 직전까지를 new로 바꾼다."""
    global s
    assert s.count(a) == 1, ('cut start', s.count(a), a[:80])
    i = s.index(a)
    j = s.index(b, i)
    s = s[:i] + new + s[j:]


# 1) morphdom을 파일 안으로
md = open(NPM + '/morphdom/dist/morphdom-umd.min.js', encoding='utf-8').read()
assert '</script' not in md
sub('<script src="https://cdn.jsdelivr.net/npm/morphdom@2.7.4/dist/morphdom-umd.min.js"></script>', '<script>' + md + '</script>')

# 2) 이모티콘을 파일 안으로 (처음 쓸 때 Blob 주소로 바꿔 쓴다)
stk = {}
for f in sorted(os.listdir(BASE + '/stickers')):
    if f.endswith('.webp'):
        stk[f[:-5]] = base64.b64encode(open(BASE + '/stickers/' + f, 'rb').read()).decode('ascii')
assert len(stk) == 72
import sys
LIGHT = '--light' in sys.argv  # 이모티콘을 파일 안에 넣지 않고 stickers 폴더에서 불러오는 가벼운 판
if not LIGHT:
    sub('<script>' + md + '</script>', '<script>' + md + '</script>\n<script>var STK_B64=' + json.dumps(stk, separators=(',', ':')) + ';</script>')
sub("function stkImg(id){var x=STK_BY[id];return x?'<img src=\"stickers/'+x[0]+'.webp\"",
    r"""var STK_URL={};
function stkSrc(id){
  if(STK_URL[id])return STK_URL[id];
  var b=window.STK_B64&&window.STK_B64[id];if(!b)return 'stickers/'+id+'.webp';
  try{var bin=atob(b),u=new Uint8Array(bin.length);for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);STK_URL[id]=URL.createObjectURL(new Blob([u],{type:'image/webp'}));}
  catch(e){STK_URL[id]='data:image/webp;base64,'+b;}
  return STK_URL[id];
}
function stkImg(id){var x=STK_BY[id];return x?'<img src="'+stkSrc(x[0])+'\"""")

# 3) 연결 정보: 주소창의 초대 링크(#db=...&room=...)나 이 기기에 저장한 값
sub("""  if(!/^https:\\/\\/[a-z0-9.-]+\\.(firebaseio\\.com|firebasedatabase\\.app)\\/?$/i.test(r.url||''))return null;
  if(!/^[A-Za-z0-9_-]{1,40}$/.test(r.room||''))return null;
  return r;
}""", r"""  if(r.url)r.url=String(r.url).replace(/\/+$/,'');
  return validRemote(r)?r:null;
}
function validRemote(r){return !!r&&/^https:\/\/[a-z0-9.-]+\.(firebaseio\.com|firebasedatabase\.app)$/i.test(r.url||'')&&/^[A-Za-z0-9_-]{12,40}$/.test(r.room||'');}
function newRoom(){var a='abcdefghijkmnpqrstuvwxyz23456789',o='',b=new Uint8Array(16),i;try{crypto.getRandomValues(b);}catch(e){for(i=0;i<16;i++)b[i]=Math.floor(Math.random()*256);}for(i=0;i<16;i++)o+=a[b[i]%a.length];return o;}
function parseRemote(v){
  v=String(v||'').trim();var i=v.indexOf('#'),r=null,m;
  if(i>=0){try{var h=new URLSearchParams(v.slice(i+1));if(h.get('db'))r={url:h.get('db'),room:h.get('room')||''};}catch(e){}}
  if(!r&&(m=v.match(/https:\/\/[a-z0-9.-]+\.(firebaseio\.com|firebasedatabase\.app)/i)))r={url:m[0],room:''};
  if(!r)return null;
  r.url=String(r.url).replace(/\/+$/,'');if(!r.room)r.room=newRoom();
  return validRemote(r)?r:null;
}
function inviteLink(r){return String(location.href).split('#')[0]+'#db='+encodeURIComponent(r.url)+'&room='+encodeURIComponent(r.room);}
var FB_RULES='{\n  "rules": {\n    ".read": false,\n    ".write": false,\n    "rooms": {\n      "$room": {\n        ".read": "$room.length >= 12",\n        ".write": "$room.length >= 12"\n      }\n    }\n  }\n}';
function connect(rc){
  lsSet('gbb_remote',JSON.stringify(rc));
  try{history.replaceState(null,'',inviteLink(rc));}catch(e){}
  S.setup=false;S.setupErr='';S.ready=false;S.readOnly=false;S.remote=rc;S.net=firebaseNet(rc.url,rc.room);render();S.net.start();
}
function viewSetup(){
  var h='<div class="view" id="view-setup"><div class="gatebox"><div><h1>공부방 플래너 연결</h1><p class="hint" style="margin-top:6px">초대 링크를 받았다면 그 링크로 열거나 아래에 붙여넣으세요. 처음 만드는 사람은 Firebase 데이터베이스 주소를 붙여넣으세요. 주소는 처음 한 번만 넣고, 내 다른 기기와 친구들은 초대 링크로 들어옵니다.</p></div>';
  h+='<section class="card" id="c-setup"><label for="setupIn" class="lb">초대 링크 또는 데이터베이스 주소</label><div class="row"><input type="text" id="setupIn" data-draft="setupIn" data-enter="setup-go" inputmode="url" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="https://...firebasedatabase.app" aria-label="초대 링크 또는 데이터베이스 주소"><button class="btn primary" data-act="setup-go">연결</button></div>'+(S.setupErr?'<p class="hint serr" role="status">'+esc(S.setupErr)+'</p>':'')+'</section>';
  h+='<section class="card" id="c-rules"><h2 class="sh">Firebase 보안 규칙</h2><p class="hint">데이터베이스를 처음 만들 때 Realtime Database의 규칙 탭에 아래 내용을 그대로 붙여넣고 게시하세요. 초대 링크를 아는 사람만 기록을 보고 쓸 수 있게 합니다.</p><pre class="rules" id="fbRules">'+esc(FB_RULES)+'</pre><div class="row"><button class="btn small" data-act="copy-rules">규칙 복사</button></div></section>';
  return h+'</div></div>';
}
function copyText(t,okMsg,el){
  var fail=function(){if(el){try{var r=document.createRange();r.selectNodeContents(el);var sl=window.getSelection();sl.removeAllRanges();sl.addRange(r);}catch(e){}}flash('복사가 막혀 있습니다. 선택된 글자를 길게 눌러 복사하세요.');};
  try{navigator.clipboard.writeText(t).then(function(){flash(okMsg);},fail);}catch(e){fail();}
}
function importData(txt){
  var j=null;try{j=JSON.parse(txt);}catch(e){}
  if(!j||j.app!=='gbb-planner'||!j.d||typeof j.d!=='object'){S.importMsg='공부방 플래너 기록 파일이 아닙니다.';render();return;}
  var ok=COLLS.concat(['meta']),jobs=[];
  Object.keys(j.d).forEach(function(c){if(ok.indexOf(c)<0)return;var col=obj(j.d[c]);Object.keys(col).forEach(function(id){if(/^[A-Za-z0-9_-]{1,80}$/.test(id)&&col[id]&&typeof col[id]==='object')jobs.push([c+'/'+id,col[id]]);});});
  Object.keys(obj(j.p)).forEach(function(id){var p=obj(j.p[id]);if(/^[A-Za-z0-9_-]{1,80}$/.test(id)&&typeof p.data==='string'&&p.data.indexOf('data:image/')===0)jobs.push(['pics/'+id,{data:p.data}]);});
  if(!jobs.length){S.importMsg='가져올 기록이 없습니다.';render();return;}
  var n=0;S.importMsg='가져오는 중입니다. 0/'+jobs.length;render();
  (function next(){
    if(n>=jobs.length){S.importMsg='기록 '+jobs.length+'개를 가져왔습니다.';render();return;}
    var x=jobs[n];
    S.net.write(x[0],x[1]).then(function(){n++;S.importMsg='가져오는 중입니다. '+n+'/'+jobs.length;render();next();})
      .catch(function(){S.importMsg='가져오다가 멈췄습니다. 인터넷 연결과 Firebase 규칙을 확인한 뒤 다시 가져오세요.';render();});
  })();
}""")
sub("""    var rc=remoteConfig();
    S.net=rc&&window.EventSource&&window.fetch?firebaseNet(rc.url,rc.room):localNet();
  }
  try{S.net.start();}catch(e){S.net=localNet();S.net.start();}""",
    """    var rc=remoteConfig();
    if(!rc||!window.EventSource||!window.fetch){S.setup=true;S.ready=true;render();return;}
    S.remote=rc;S.net=firebaseNet(rc.url,rc.room);
    try{if(!location.hash)history.replaceState(null,'',inviteLink(rc));}catch(e){}
  }
  try{S.net.start();}catch(e){S.setup=true;S.ready=true;S.setupErr='연결하지 못했습니다. 주소를 다시 확인하세요.';render();}""")
sub("  var gate=S.ready&&!V.me;\n  paintBanner();", "  var gate=S.setup||(S.ready&&!V.me);\n  paintBanner();")
sub("  else if(gate)h=viewGate(V);", "  else if(S.setup)h=viewSetup();\n  else if(gate)h=viewGate(V);")
sub("  else if(S.readOnly)b+='<div class=\"notice\">보기 전용으로 열려 있습니다. 직접 기록하려면 플래너 주인에게 편집 권한 초대를 요청하세요.</div>';",
    "  else if(S.readOnly)b+='<div class=\"notice\">'+(S.net&&S.net.mode==='firebase'?'저장소가 기록을 받아주지 않습니다. Firebase 규칙이 맞게 게시되었는지, 초대 링크가 맞는지 확인하세요.':'보기 전용으로 열려 있습니다. 직접 기록하려면 플래너 주인에게 편집 권한 초대를 요청하세요.')+'</div>';")
# 설정의 저장 위치에 초대 링크, 기록 가져오기, 연결 끊기
sub("local:'지금은 이 기기에만 저장됩니다. 다른 사람과 같이 보려면 공유 저장소 연결이 필요합니다.'}[S.net.mode]):'연결 중입니다.')+'</p></div>';",
    "local:'지금은 이 기기에만 저장됩니다. 다른 사람과 같이 보려면 공유 저장소 연결이 필요합니다.'}[S.net.mode]):'연결 중입니다.')+'</p>'"
    "+(S.net&&S.net.mode==='firebase'&&S.remote?'<div class=\"invite\"><small>초대 링크</small><p class=\"url\" id=\"invUrl\">'+esc(inviteLink(S.remote))+'</p></div><div class=\"row\" style=\"margin-top:10px\"><button class=\"btn small primary\" data-act=\"copy-invite\">초대 링크 복사</button><button class=\"btn small\" data-act=\"import-pick\">기록 가져오기</button><button class=\"del\" data-act=\"setup-reset\">'+(S.confirm==='disc'?'한 번 더 누르면 연결을 끊습니다':'이 기기 연결 끊기')+'</button></div><p class=\"hint\" style=\"margin-top:8px\">'+esc(S.importMsg||'초대 링크를 친구들과 내 다른 기기에 보내세요. 기록 가져오기는 처음 연결한 뒤 한 번만 하면 됩니다.')+'</p>':'')+'</div>';")
# 아이패드에서 화면을 껐다 켜면 끊긴 실시간 연결을 다시 연다
sub("""    start:function(){
      var es=new EventSource(rm+'/d.json');""", """    start:function(){
      var es=null;
      document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'&&es&&es.readyState===2)open();});
      open();
      function open(){
      es=new EventSource(rm+'/d.json');""")
sub("""      es.onerror=function(){if(!S.ready){S.ready=true;flash('공유 저장소에 연결하지 못했습니다. 인터넷 연결을 확인하세요.');render();}};
    }};""", """      es.onerror=function(){if(!S.ready){S.ready=true;flash('공유 저장소에 연결하지 못했습니다. 인터넷 연결을 확인하세요.');render();}};
      }
    }};""")
# 참여 인원이 아직 없을 때(처음 연결한 주인): 연결 화면에서 바로 기록 가져오기
sub("  else if(!V.roster.length)h+='<p class=\"hint\">연결되면 참여 인원이 표시됩니다.</p>';",
    "  else if(!V.roster.length)h+='<p class=\"hint\">연결되면 참여 인원이 표시됩니다.</p>';\n"
    "  if(!V.roster.length&&S.net&&S.net.mode==='firebase'&&canWrite())h+='<section class=\"card\" id=\"c-import\"><h2 class=\"sh\">Claude에서 쓰던 기록이 있나요?</h2><p class=\"hint\">받아둔 기록 파일(planner-data.json)을 가져오면 참여 인원, 과목, 지금까지의 기록이 그대로 들어옵니다.</p><div class=\"row\" style=\"margin-top:10px\"><button class=\"btn\" data-act=\"import-pick\">기록 가져오기</button></div>'+(S.importMsg?'<p class=\"hint\" style=\"margin-top:8px\" role=\"status\">'+esc(S.importMsg)+'</p>':'')+'</section>';")
# 동작
sub("    case 'open':openModal(el.getAttribute('data-modal'),el);return;", r"""    case 'setup-go':{
      var rcx=parseRemote(S.draft.setupIn);
      if(!rcx){S.setupErr='주소를 알아보지 못했습니다. https://로 시작하는 Firebase 데이터베이스 주소나 초대 링크를 붙여넣으세요.';break;}
      connect(rcx);return;
    }
    case 'copy-rules':copyText(FB_RULES,'규칙을 복사했습니다.',document.getElementById('fbRules'));break;
    case 'copy-invite':if(S.remote)copyText(inviteLink(S.remote),'초대 링크를 복사했습니다.',document.getElementById('invUrl'));break;
    case 'import-pick':{
      if(!S.net||S.net.mode!=='firebase'||!need())break;
      var fi=document.getElementById('importPick');
      if(!fi){fi=document.createElement('input');fi.type='file';fi.id='importPick';fi.accept='.json,application/json';fi.style.display='none';document.body.appendChild(fi);
        fi.addEventListener('change',function(){var f=fi.files&&fi.files[0];if(!f)return;var rd=new FileReader();rd.onload=function(){importData(String(rd.result||''));};rd.readAsText(f);fi.value='';});}
      fi.click();return;
    }
    case 'setup-reset':
      if(prev!=='disc'){S.confirm='disc';break;}
      lsSet('gbb_remote',null);try{history.replaceState(null,'',String(location.href).split('#')[0]);}catch(e){}
      location.reload();return;
    case 'open':openModal(el.getAttribute('data-modal'),el);return;""")
sub("S.songMood='';S.songFilter='';S.songRoll=null;", "S.setup=false;S.setupErr='';S.remote=null;S.importMsg='';\nS.songMood='';S.songFilter='';S.songRoll=null;")
# change 이벤트에서 가져오기 파일 칸은 건너뛴다
sub("  var t=e.target;if(!t.getAttribute||t===filePick)return;", "  var t=e.target;if(!t.getAttribute||t===filePick||t.id==='importPick')return;")
sub("</style>", """#c-setup .row input{min-width:0}
#c-setup .lb{margin-top:0}
.serr{color:var(--red);margin-top:8px}
.sh{font-size:15px;font-weight:700;margin-bottom:6px}
.rules{margin:10px 0;padding:12px 14px;border-radius:12px;background:var(--fill);font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre;overflow-x:auto;-webkit-user-select:all;user-select:all}
.invite{margin-top:10px;padding:10px 12px;border-radius:12px;background:var(--fill)}
.invite small{display:block;font-size:12px;color:var(--ink-3);margin-bottom:2px}
.invite .url{font-size:13px;word-break:break-all;-webkit-user-select:all;user-select:all;color:var(--ink-2)}
</style>""")
# 홈 화면에 추가하면 앱처럼 열리게 (아이콘과 manifest는 같은 폴더에 둠)
sub("<title>공부방 플래너</title>", """<title>공부방 플래너</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="공부방">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#F3F4F6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1114" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">""")
# 기록 파일로 저장 (백업)
sub("<button class=\"btn small\" data-act=\"import-pick\">기록 가져오기</button>",
    "<button class=\"btn small\" data-act=\"import-pick\">기록 가져오기</button><button class=\"btn small\" data-act=\"export-data\">기록 파일로 저장</button>")
sub("    case 'copy-rules':", r"""    case 'export-data':{
      var ex={app:'gbb-planner',v:1,exportedAt:new Date().toISOString(),d:{meta:{config:S.config||{}}},p:{}};
      COLLS.forEach(function(c){ex.d[c]=S[c]||{};});
      try{var bl=new Blob([JSON.stringify(ex)],{type:'application/json'}),bu=URL.createObjectURL(bl),ba=document.createElement('a');ba.href=bu;ba.download='planner-data-'+today()+'.json';document.body.appendChild(ba);ba.click();setTimeout(function(){URL.revokeObjectURL(bu);ba.remove();},1500);flash('기록 파일을 저장했습니다. 사진은 들어가지 않습니다.');}
      catch(e){flash('저장하지 못했습니다.');}
      break;
    }
    case 'copy-rules':""")
# 참여 코드, 새 방, 방 바꾸기
exec(open(BASE + '/tools/web_rooms_part.py', encoding='utf-8').read())
# 오프라인
exec(open(BASE + '/tools/web_offline_part.py', encoding='utf-8').read())
# 바뀐 것만 받기
exec(open(BASE + '/tools/web_sync_part.py', encoding='utf-8').read())
# 모든 방 잉크
exec(open(BASE + '/tools/web_wallet_part.py', encoding='utf-8').read())
# 다른 방에서 내 것 가져오기
exec(open(BASE + '/tools/web_carry_part.py', encoding='utf-8').read())
# 검색 제외
exec(open(BASE + '/tools/web_v44_part.py', encoding='utf-8').read())
# 찌르기 웹 푸시
exec(open(BASE + '/tools/web_push_part.py', encoding='utf-8').read())
OUT = BASE + ('/web-light' if LIGHT else '/web')
os.makedirs(OUT, exist_ok=True)
open(OUT + '/index.html', 'w', encoding='utf-8').write(s)
import re as _re
_vb = _re.search(r"var APP_BUILD='(\d+)';", s)
assert _vb, 'APP_BUILD missing'
open(OUT + '/version.txt', 'w').write(_vb.group(1) + (' force' if os.environ.get('FORCE') == '1' else '') + '\n')
print('web built', len(s.encode('utf-8')))
