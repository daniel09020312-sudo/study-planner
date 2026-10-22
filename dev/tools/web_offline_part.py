# ---------------------------------------------------------------- 웹 판: 오프라인에서도 내 기록 쓰기, 오프라인 표시, 앱 화면 저장(sw.js)
OFF_JS = open(BASE + '/src/offline.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", OFF_JS + "\n/* ---------- 공부방 ---------- */")
sub("var LS_SCOPED={gbb_me:1,", "var LS_SCOPED={gbb_outbox:1,gbb_cache:1,gbb_me:1,")
# 쓰기: 인터넷이 없으면 모아 두고, 사진은 연결된 뒤에
sub("""    write:function(path,d){return fetch(url(path),{method:d===null?'DELETE':'PUT',headers:{'Content-Type':'application/json'},body:d===null?undefined:JSON.stringify(d)}).then(chk).then(function(){});},""",
    """    write:function(path,d){
      var pic=path.indexOf('pics/')===0;
      function off(){var e=new Error('offline');e.code='offline';return e;}
      if(navigator.onLine===false){if(pic)return Promise.reject(off());obQueue(path,d);return Promise.resolve();}
      return fetch(url(path),{method:d===null?'DELETE':'PUT',headers:{'Content-Type':'application/json'},body:d===null?undefined:JSON.stringify(d)})
        .then(chk).then(function(){obDrop(path);})
        .catch(function(e){if(e&&e.code)throw e;if(pic)throw off();obQueue(path,d);});
    },""")
sub("  else if(code==='quota_exceeded'){", "  else if(code==='offline'){flash('오프라인이라 사진과 영상은 올릴 수 없습니다. 인터넷이 연결되면 다시 올려 주세요.');}\n  else if(code==='quota_exceeded'){")
# 받은 기록: 모아 둔 내 기록을 덮어 보이게 하고, 이 기기에 저장해 둔다
sub("  COLLS.forEach(function(k){S[k]=obj(tree[k]);});\n  S.ready=true;render();\n  try{roomTick();}catch(e){}",
    "  COLLS.forEach(function(k){S[k]=obj(tree[k]);});\n  try{obApply();}catch(e){}\n  if(!S.booting)cacheSave(tree);\n  S.ready=true;render();\n  try{roomTick();}catch(e){}")
# 처음 열 때: 저장해 둔 기록으로 바로 보여 주고, 연결되면 새로 받는다
sub("    S.remote=rc;S.net=firebaseNet(rc.url,rc.room);\n    try{syncAddr();}catch(e){}",
    "    S.remote=rc;S.net=firebaseNet(rc.url,rc.room);\n    try{syncAddr();}catch(e){}\n    try{cacheBoot();}catch(e){}")
# 연결 상태
sub("      es.onerror=function(){if(!S.ready){S.ready=true;flash('공유 저장소에 연결하지 못했습니다. 인터넷 연결을 확인하세요.');render();}};",
    "      es.onopen=function(){clearTimeout(S.sseT);S.sseT=null;if(S.sseDown){S.sseDown=false;paintBanner();}obFlush();};\n"
    "      es.onerror=function(){if(!S.sseT)S.sseT=setTimeout(function(){S.sseT=null;if(!es||es.readyState!==1){S.sseDown=true;paintBanner();}},4000);if(!S.ready){S.ready=true;if(navigator.onLine!==false)flash('공유 저장소에 연결하지 못했습니다. 인터넷 연결을 확인하세요.');render();}};")
sub("function paintBanner(){\n  var b='';", "function paintBanner(){\n  var b='';\n  if(S.net&&S.net.mode==='firebase'&&isOffline()){var obn=obCount();b+='<div class=\"notice offn\"><b>오프라인</b> 내 일정과 할 일은 지금처럼 쓰면 됩니다. 이 기기에 모아 두었다가 연결되면 올립니다'+(obn?' (올릴 기록 '+obn+'개)':'')+'. 친구들 기록은 연결된 뒤에 새로 보입니다.</div>';}")
# 앱 화면 저장
assert s.count("init();\n})();") == 1
s = s.replace("init();\n})();", "init();\nif('serviceWorker' in navigator&&location.protocol==='https:'){try{navigator.serviceWorker.register('sw.js').catch(function(){});}catch(e){}}\n})();")
sub("</style>", ".notice.offn{background:color-mix(in srgb,var(--ink) 88%,transparent);color:var(--bg)}\n.notice.offn b{margin-right:6px}\n</style>")
# 새 판이 올라오면 저절로 다시 읽기: 홈 화면 앱은 껐다 켜지 않으면 예전 화면이 계속 돌아가서
# version.txt(빌드할 때 같이 만듦)의 번호가 지금 화면의 APP_BUILD와 다르면, 창이나 입력 중이 아닐 때 다시 읽는다
assert s.count("init();\nif('serviceWorker' in navigator") == 1
s = s.replace("init();\nif('serviceWorker' in navigator", r"""init();
(function(){
  var want=false,busy=false;
  function check(){
    if(busy||want||navigator.onLine===false||location.protocol!=='https:'||typeof APP_BUILD==='undefined')return;busy=true;
    fetch('version.txt?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.text():'';}).then(function(t){busy=false;t=String(t||'').trim();if(/^\d+$/.test(t)&&+t>+APP_BUILD){var done='';try{done=sessionStorage.getItem('gbb_upd')||'';}catch(e){}if(done===t)return;want=t;tryReload();}}).catch(function(){busy=false;});
  }
  function tryReload(){
    if(!want)return;
    var ae=document.activeElement,typing=ae&&/^(INPUT|TEXTAREA|SELECT)$/.test(ae.tagName);
    if(S.modal||typing||S.drag||S.check||document.getElementById('splash'))return;
    try{if(obCount())return;}catch(e){}
    try{sessionStorage.setItem('gbb_upd',String(want));}catch(e){}
    location.reload();
  }
  setTimeout(check,4000);
  document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'){check();tryReload();}});
  setInterval(function(){if(document.visibilityState==='visible')check();},10*60000);
  setInterval(tryReload,4000);
})();
if('serviceWorker' in navigator""")
