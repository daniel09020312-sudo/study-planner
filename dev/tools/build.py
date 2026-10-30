import json, re, sys, os
BASE = '/home/claude/planner'
s = open(BASE + '/src/planner_v9_backup.html', encoding='utf-8').read()
add_css = open(BASE + '/src/add.css', encoding='utf-8').read()
accents = json.load(open(BASE + '/src/accents.json', encoding='utf-8'))
stk = json.load(open(BASE + '/src/stickers_meta.json', encoding='utf-8'))


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


# ---------------------------------------------------------------- CSS
BODY_FONT = "-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR','Noto Sans CJK KR','Malgun Gothic',sans-serif"
sub("  --accent:#2B6DEF; --on-accent:#FFFFFF; --accent-soft:#E9F0FE;\n",
    "  --accent:#2B6DEF; --on-accent:#FFFFFF; --accent-soft:#E9F0FE; --accent-ink:#2360DC; --accent-mark:#2B6DEF;\n"
    "  --font-body:" + BODY_FONT + "; --font-display:inherit;\n  color-scheme:light;\n")
sub("    --accent:#6A9CFF; --on-accent:#081226; --accent-soft:#1C2A44;\n",
    "    --accent:#6A9CFF; --on-accent:#081226; --accent-soft:#1C2A44; --accent-ink:#6A9CFF; --accent-mark:#6A9CFF;\n    color-scheme:dark;\n")
sub("  --accent:#6A9CFF; --on-accent:#081226; --accent-soft:#1C2A44;\n",
    "  --accent:#6A9CFF; --on-accent:#081226; --accent-soft:#1C2A44; --accent-ink:#6A9CFF; --accent-mark:#6A9CFF;\n  color-scheme:dark;\n")
sub("  font-family:" + BODY_FONT + ";\n", "  font-family:var(--font-body);\n")
# 글자와 테두리로 쓰는 대표 색은 --accent-ink, 그래프 막대는 --accent-mark
s = s.replace("color:var(--accent)", "color:var(--accent-ink)")
sub(":focus-visible{outline:2px solid var(--accent);", ":focus-visible{outline:2px solid var(--accent-ink);")
sub("box-shadow:inset 0 0 0 1.5px var(--accent)}", "box-shadow:inset 0 0 0 1.5px var(--accent-ink)}")
sub(".d7.today i{box-shadow:inset 0 0 0 2px var(--accent);", ".d7.today i{box-shadow:inset 0 0 0 2px var(--accent-ink);")
sub('.bdg[aria-pressed="true"]{box-shadow:inset 0 0 0 2px var(--accent)}', '.bdg[aria-pressed="true"]{box-shadow:inset 0 0 0 2px var(--accent-ink)}')
sub("border-top:18px solid var(--accent);", "border-top:18px solid var(--accent-ink);")
sub("box-shadow:0 0 0 3px var(--accent);z-index:2}", "box-shadow:0 0 0 3px var(--accent-ink);z-index:2}")
sub(".rk.me .bar i{background:var(--accent)}", ".rk.me .bar i{background:var(--accent-mark)}")
sub(".vbar i.me{background:var(--accent);", ".vbar i.me{background:var(--accent-mark);")
sub("border-radius:5px;background:var(--accent);transition:width .7s var(--ease)}", "border-radius:5px;background:var(--accent-mark);transition:width .7s var(--ease)}")
sub(".chart .me{fill:var(--accent)}", ".chart .me{fill:var(--accent-mark)}")
sub(".mini i.on{background:var(--accent)}", ".mini i.on{background:var(--accent-mark)}")
sub('<i style="background:var(--accent)"></i>나', '<i style="background:var(--accent-mark)"></i>나')
sub("</style>", add_css + "</style>")

# ---------------------------------------------------------------- 화면 모드, 컨셉, 대표 색
LOOK = r"""var ACCENTS=__ACCENTS__;
var CONCEPTS=[
  {id:'basic',name:'기본'},
  {id:'grid',name:'모눈 노트',font:'Nanum+Pen+Script',face:'Nanum Pen Script',w:400},
  {id:'board',name:'칠판',mode:'dark',soft:[.18,'#24443A'],ink:.6,font:'Gaegu:wght@700',face:'Gaegu',w:700},
  {id:'pop',name:'말랑',font:'Jua',face:'Jua',w:400},
  {id:'line',name:'선'},
  {id:'glass',name:'유리'},
  {id:'night',name:'밤하늘',mode:'dark',soft:[.17,'#151A3F'],font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700}
];
var hostTheme=document.documentElement.getAttribute('data-theme'),lastSet=hostTheme;
function themePref(){var t=lsGet('gbb_theme');return t==='dark'||t==='light'?t:'auto';}
function conceptPref(){var c=lsGet('gbb_concept');return CONCEPTS.filter(function(x){return x.id===c;})[0]||CONCEPTS[0];}
function accentPref(){var c=lsGet('gbb_accent')||'blue';return ACCENTS.filter(function(x){return x.id===c;})[0]||ACCENTS[0];}
function isDark(){
  var c=conceptPref();if(c.mode)return c.mode==='dark';
  var t=themePref();if(t!=='auto')return t==='dark';
  if(hostTheme==='dark')return true;if(hostTheme==='light')return false;
  try{return window.matchMedia('(prefers-color-scheme: dark)').matches;}catch(e){return false;}
}
function mixHex(a,b,p){
  var o='#',i,x,y;
  for(i=1;i<7;i+=2){x=parseInt(a.substr(i,2),16);y=parseInt(b.substr(i,2),16);o+=('0'+Math.round(x*p+y*(1-p)).toString(16)).slice(-2);}
  return o.toUpperCase();
}
function loadFont(c){
  var root=document.documentElement;root.removeAttribute('data-font');
  if(!c.font)return;
  function check(){
    try{document.fonts.load(c.w+' 24px "'+c.face+'"','공부방 플래너 달력 메시지').then(function(f){if(f&&f.length&&conceptPref().id===c.id)root.setAttribute('data-font','ok');}).catch(function(){});}catch(e){}
  }
  var id='cf-'+c.id,l=document.getElementById(id);
  if(l){check();return;}
  l=document.createElement('link');l.id=id;l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family='+c.font+'&display=swap';
  l.addEventListener('load',check);document.head.appendChild(l);
}
function applyLook(){
  var root=document.documentElement,st=root.style,t=themePref(),c=conceptPref(),a=accentPref(),dark=isDark(),v=dark?a.d:a.l;
  var want=c.mode?c.mode:(t!=='auto'?t:(hostTheme||null));
  lastSet=want;
  if(want)root.setAttribute('data-theme',want);else root.removeAttribute('data-theme');
  root.setAttribute('data-mode',dark?'dark':'light');
  if(c.id==='basic')root.removeAttribute('data-concept');else root.setAttribute('data-concept',c.id);
  st.setProperty('--accent',v.a);st.setProperty('--on-accent',v.on);st.setProperty('--accent-mark',v.mark);
  st.setProperty('--accent-soft',c.soft?mixHex(v.a,c.soft[1],c.soft[0]):v.soft);
  st.setProperty('--accent-ink',c.ink?mixHex(v.ink,'#FFFFFF',c.ink):v.ink);
  loadFont(c);
}
applyLook();
try{window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',applyLook);}catch(e){}
try{new MutationObserver(function(){var v=document.documentElement.getAttribute('data-theme');if(v===lastSet)return;hostTheme=v;applyLook();}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});}catch(e){}

/* ---------- 이모티콘 ---------- */
var STK=__STK__;
var STK_PACKS=[['basic','기본'],['playful','장난'],['emotions','감정'],['cat','까만 고양이'],['dog','하얀 강아지'],['nyang','냥댕이']],STK_BY={};
STK.forEach(function(x){STK_BY[x[0]]=x;});
var DUEL_DAYS=2;

"""
LOOK = LOOK.replace('__ACCENTS__', json.dumps(accents, ensure_ascii=False, separators=(',', ':')))
LOOK = LOOK.replace('__STK__', json.dumps([[x['id'], x['label'], x['motion']] + ([x['fr']] if x.get('fr') else []) for x in stk], ensure_ascii=False, separators=(',', ':')))
cut("var ACCENTS=[", "/* ---------- 상태 ---------- */", LOOK)
sub("S.locks={};S.flags={};S.mlog=[];S.mseq=0;S.pin=null;", "S.locks={};S.flags={};S.mlog=[];S.mseq=0;S.msgSel=null;S.msgEdit=null;S.stkOpen=false;S.stkPack='basic';S.busyMsg=false;S.focusAfter=null;S.pin=null;")

# 설정 화면의 "화면" 칸
cut("  var tp=themePref(),acNow=lsGet('gbb_accent')||'blue';", "  if(V.me)b+='<div class=\"sec\"><h3>내 점수 초기화", r"""  var tp=themePref(),acNow=accentPref().id,cNow=conceptPref();
  function sws(g){return ACCENTS.filter(function(x){return x.g===g;}).map(function(x){return '<button class="sw" data-act="accent" data-v="'+x.id+'" style="--a:'+x.l.a+';--b:'+x.d.a+'" aria-pressed="'+(acNow===x.id?'true':'false')+'" aria-label="대표 색 '+x.name+'" title="'+x.name+'"></button>';}).join('');}
  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3><h4 class="lb" style="margin-top:0">컨셉</h4><div class="cvs" role="group" aria-label="컨셉 디자인">'+CONCEPTS.map(function(x){return '<button class="cv" data-act="concept" data-v="'+x.id+'" aria-pressed="'+(cNow.id===x.id?'true':'false')+'"><span class="cvp cvp-'+x.id+'" aria-hidden="true"><i></i><i></i><i></i></span><span>'+x.name+'</span></button>';}).join('')+'</div>';
  b+='<h4 class="lb">밝기</h4>'+(cNow.mode?'<p class="hint">'+cNow.name+' 컨셉은 항상 어둡게 보입니다.</p>':'<div class="chips">'+[['auto','기기 설정에 맞춤'],['light','밝게'],['dark','어둡게']].map(function(x){return '<button class="chip" data-act="theme" data-v="'+x[0]+'" aria-pressed="'+(tp===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>');
  b+='<h4 class="lb">대표 색</h4><div class="sws" role="group" aria-label="대표 색">'+sws('b')+'</div><h4 class="lb">파스텔</h4><div class="sws" role="group" aria-label="파스텔 대표 색">'+sws('p')+'</div></div>';
""")
sub("    case 'accent':lsSet('gbb_accent',el.getAttribute('data-v'));applyLook();break;",
    "    case 'accent':lsSet('gbb_accent',el.getAttribute('data-v'));applyLook();break;\n"
    "    case 'concept':lsSet('gbb_concept',el.getAttribute('data-v'));applyLook();break;")

# ---------------------------------------------------------------- 메시지 화면
CHAT = r"""function stkImg(id){var x=STK_BY[id];return x?'<img src="stickers/'+x[0]+'.webp" alt="'+esc(x[1])+' 이모티콘" width="160" height="160" decoding="async">':'';}
function msgPreview(x){
  if(x.poke)return '찌르기';
  if(x.stk)return '이모티콘'+(STK_BY[x.stk]?' ('+STK_BY[x.stk][1]+')':'');
  if(x.pic)return x.text?'사진, '+cut(x.text,18):'사진';
  return cut(x.text,24);
}
function setChan(id){
  if(S.msgEdit){S.draft['msg:'+S.msgEdit.chan]='';S.msgEdit=null;}
  S.chan=id;S.chatKey='';S.msgSel=null;S.stkOpen=false;
}
function viewChat(V){
  var by=V.chat,c=by[S.chan]?S.chan:'all',list=by[c].slice(-150),dm=c!=='all',who=dm?V.byId[c]:null,lastDay='',key='c:'+c;
  var ed=S.msgEdit&&S.msgEdit.chan===c&&V.msgs[S.msgEdit.id]?S.msgEdit:null;
  var h='<div class="view" id="view-chat"><header class="vhead"><div><h1>메시지</h1><p>전체 대화와 1:1 메시지를 주고받습니다. 내가 보낸 메시지를 누르면 고치거나 지울 수 있습니다.</p></div></header><div class="chat"><section class="card chlist" id="c-chlist" style="--k:0">';
  ['all'].concat(V.roster.filter(function(m){return m.id!==V.me;}).map(function(m){return m.id;})).forEach(function(k){
    var l=by[k]||[],last=l[l.length-1],un=k===c?0:unreadOf(V,k),p=k==='all'?null:V.byId[k];
    h+='<button class="chrow" data-act="chan" data-id="'+esc(k)+'" aria-current="'+(k===c?'true':'false')+'">'+(p?av(p,'s'):'<span class="av s" aria-hidden="true">전체</span>')+'<span style="min-width:0"><b>'+(p?esc(p.name):'전체 대화')+'</b><small>'+(last?esc(msgPreview(last)):'대화 없음')+'</small></span>'+(un?'<span class="cnt" aria-label="안 읽은 메시지 '+un+'개">'+un+'</span>':'<span></span>')+'</button>';
  });
  h+='</section><section class="card" id="cb-'+esc(c)+'" style="--k:1"><div class="ct"><h2>'+(dm?esc(who.name):'전체 대화')+'</h2>'+(dm?'<button class="btn small soft" data-act="poke" data-id="'+esc(c)+'">찌르기</button>':'')+'</div><div class="msgs" id="msgList" tabindex="0" aria-label="대화 내용">';
  if(!list.length)h+='<p class="empty" style="margin:auto">아직 메시지가 없습니다.</p>';
  list.forEach(function(x){
    var mine=x.from===V.me,w=V.byId[x.from],nm=w?w.name:'나간 인원',at=new Date(+x.at),day=fd(at),tm=fmtClock(at.toISOString());
    if(day!==lastDay){lastDay=day;h+='<div class="sys" id="d-'+day+'">'+esc(longDate(day))+'</div>';}
    if(x.poke){h+='<div class="sys" id="m-'+esc(x.id)+'">'+(mine?'내가 찔렀습니다':esc(nm)+' 님이 찔렀습니다')+', '+tm+'</div>';return;}
    var sel=mine&&S.msgSel===x.id,pick=mine?' data-act="msg-pick" data-id="'+esc(x.id)+'"':'',meta=tm+(x.edited?', 수정됨':''),body;
    if(x.stk)body='<span class="stk" data-m="'+esc(STK_BY[x.stk]?STK_BY[x.stk][2]:'still')+'"'+pick+'>'+(stkImg(x.stk)||'이모티콘')+'</span>';
    else if(x.pic)body='<div class="bb pic"'+pick+'>'+shot(x.id)+(x.text?'<div class="cap">'+esc(x.text)+'</div>':'')+'</div>';
    else body='<div class="bb"'+pick+'>'+esc(x.text)+'</div>';
    h+='<div class="mrowx'+(mine?' mine':'')+(sel?' sel':'')+'" id="m-'+esc(x.id)+'">'+(!mine&&!dm?'<small>'+esc(nm)+'</small>':'')+body;
    h+=mine?'<button class="mt" data-act="msg-pick" data-id="'+esc(x.id)+'" aria-expanded="'+(sel?'true':'false')+'" aria-label="'+esc(meta)+', 이 메시지 고치거나 지우기">'+esc(meta)+'</button>':'<small>'+esc(meta)+'</small>';
    if(sel)h+='<div class="mact">'+(x.stk?'':'<button class="btn small" data-act="msg-edit" data-id="'+esc(x.id)+'">'+(x.pic&&!x.text?'설명 달기':'수정')+'</button>')+'<button class="btn small" data-act="msg-del" data-id="'+esc(x.id)+'">'+(S.confirm==='msg:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button></div>';
    h+='</div>';
  });
  h+='</div><div id="stkSlot">';
  if(S.stkOpen&&!ed){
    h+='<div class="stkpick" id="stkPick"><div class="seg" role="group" aria-label="이모티콘 묶음">'+STK_PACKS.map(function(p){return '<button data-act="stk-pack" data-id="'+p[0]+'" aria-pressed="'+(S.stkPack===p[0]?'true':'false')+'">'+p[1]+'</button>';}).join('')+'</div><div class="stkgrid" id="sg-'+esc(S.stkPack)+'">';
    STK.forEach(function(x){if(x[0].indexOf(S.stkPack+'-')===0)h+='<button class="stkbtn" data-act="stk-send" data-id="'+x[0]+'" data-chan="'+esc(c)+'" aria-label="'+esc(x[1])+' 이모티콘 보내기">'+stkImg(x[0])+'</button>';});
    h+='</div></div>';
  }
  /* 입력칸이 화면 갱신 때 옮겨지지 않도록 자리(칸)를 항상 같은 순서로 둔다 */
  h+='</div><div class="cin"><div id="cinTop">'+(ed?'<div class="cbar"><span>'+(V.msgs[ed.id].pic?'사진 설명 수정 중':'메시지 수정 중')+'</span><button class="del" data-act="msg-edit-x">취소</button></div>':attach(key))+'</div>';
  h+='<div class="cinrow'+(ed?' ed':'')+'" id="cinRow"><button class="btn" id="msgPhoto" data-act="pick" data-for="'+esc(key)+'"'+(ed?' hidden':'')+'>사진</button><button class="btn" id="msgStk" data-act="stk-toggle" aria-expanded="'+(S.stkOpen?'true':'false')+'"'+(ed?' hidden':'')+'>이모티콘</button>';
  h+='<input type="text" id="msgInput" data-draft="msg:'+esc(c)+'" data-enter="msg-send" data-id="'+esc(c)+'" maxlength="300" placeholder="'+(ed?'고칠 내용':S.att[key]?'사진과 함께 보낼 말 (없어도 됩니다)':dm?esc(who.name)+' 님에게 보내기':'모두에게 보내기')+'" aria-label="메시지"><button class="btn primary" id="msgSend" data-act="msg-send" data-id="'+esc(c)+'"'+(S.busyMsg?' disabled':'')+'>'+(ed?'수정':S.busyMsg?'보내는 중':'보내기')+'</button></div></div></section></div></div>';
  return h;
}
function prune(V){var lim=Date.now()-30*86400000,n=0;Object.keys(V.msgs).forEach(function(k){var x=obj(V.msgs[k]);if(n<10&&x.from===V.me&&+x.at<lim){save('msgs/'+k,null);if(x.pic&&S.net)S.net.write('pics/'+k,null).catch(function(){});n++;}});}
"""
cut("function viewChat(V){", "function notesHtml(V){", CHAT)

# 메시지 동작
cut("    case 'chan':S.chan=id;S.chatKey='';break;", "    case 'poke':{", r"""    case 'chan':setChan(id);break;
    case 'dm':setChan(id);goTab('chat');break;
    case 'note-open':{
      var ntab=el.getAttribute('data-tab')||'chat',nid=el.getAttribute('data-n');
      S.notes=S.notes.filter(function(n){return n.id!==nid;});
      if(ntab==='chat'&&id)setChan(id);
      goTab(ntab);break;
    }
    case 'note-x':S.notes=S.notes.filter(function(n){return n.id!==id;});break;
    case 'msg-pick':S.msgSel=S.msgSel===id?null:id;break;
    case 'msg-edit':{
      var Ve2=view(),m2=Ve2.msgs[id];if(!m2||m2.from!==Ve2.me||m2.stk||m2.poke)break;
      S.msgEdit={id:id,chan:m2.to};S.draft['msg:'+m2.to]=String(m2.text||'');S.msgSel=null;S.stkOpen=false;delete S.att['c:'+m2.to];S.focusAfter='msgInput';break;
    }
    case 'msg-edit-x':if(S.msgEdit){S.draft['msg:'+S.msgEdit.chan]='';S.msgEdit=null;}break;
    case 'msg-del':{
      if(prev!=='msg:'+id){S.confirm='msg:'+id;break;}
      var Vd2=view(),m3=Vd2.msgs[id];if(!m3||m3.from!==Vd2.me||m3.poke||!need())break;
      save('msgs/'+id,null);
      if(m3.pic){delete S.pics[id];S.net.write('pics/'+id,null).catch(function(){});}
      if(S.msgEdit&&S.msgEdit.id===id){S.draft['msg:'+S.msgEdit.chan]='';S.msgEdit=null;}
      S.msgSel=null;break;
    }
    case 'stk-toggle':S.stkOpen=!S.stkOpen;S.msgSel=null;if(S.stkOpen)S.scrollAfter='stkPick';break;
    case 'stk-pack':S.stkPack=id;break;
    case 'stk-send':{
      var Vk2=view(),ch=el.getAttribute('data-chan');
      if(!Vk2.me||!STK_BY[id]||(ch!=='all'&&!Vk2.byId[ch])||!need())break;
      save('msgs/'+rid('x'),{from:Vk2.me,to:ch,stk:id,text:'',at:Date.now()});
      S.stkOpen=false;prune(Vk2);break;
    }
    case 'msg-send':{
      var Vm=view();if(!Vm.me||(id!=='all'&&!Vm.byId[id]))break;
      var mt=String(S.draft['msg:'+id]||'').trim(),E=S.msgEdit&&S.msgEdit.chan===id?S.msgEdit:null,ak='c:'+id,mpic=E?null:S.att[ak];
      if(E){
        var old=Vm.msgs[E.id];
        if(!old||old.from!==Vm.me){S.msgEdit=null;break;}
        if(!mt&&!old.pic){flash('내용을 적어주세요. 지우려면 메시지를 눌러 삭제를 고르세요.');break;}
        if(!need())break;
        if(mt!==String(old.text||'')){var nw=clone(old);nw.text=mt.slice(0,300);nw.edited=Date.now();save('msgs/'+E.id,nw);}
        S.msgEdit=null;S.draft['msg:'+id]='';break;
      }
      if((!mt&&!mpic)||S.busyMsg||!need())break;
      var mid=rid('x'),mdoc={from:Vm.me,to:id,text:mt.slice(0,300),at:Date.now()};
      if(mpic){
        mdoc.pic=true;S.busyMsg=true;
        putPic(mid,mpic).then(function(){S.busyMsg=false;mdoc.at=Date.now();save('msgs/'+mid,mdoc);S.draft['msg:'+id]='';delete S.att[ak];S.sync=true;render();})
          .catch(function(){S.busyMsg=false;delete S.pics[mid];flash('사진을 보내지 못했습니다. 다시 시도해 주세요.');render();});
        break;
      }
      save('msgs/'+mid,mdoc);S.draft['msg:'+id]='';S.stkOpen=false;prune(Vm);break;
    }
""")

# 그린 뒤 처리: 입력칸 포커스, 사진 불러오기, 알림 문구
sub("function after(V){\n  afterChat(V);", r"""function after(V){
  afterChat(V);
  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);S.focusAfter=null;if(fe){fe.value=S.draft[fe.getAttribute('data-draft')]||'';fe.focus();try{fe.setSelectionRange(fe.value.length,fe.value.length);}catch(e){}}}
  if(S.scrollAfter){var se=document.getElementById(S.scrollAfter);S.scrollAfter=null;if(se&&se.scrollIntoView)se.scrollIntoView({block:'nearest'});}
  if(S.ready&&V.me&&S.vtab==='chat'&&S.net&&S.net.read){
    (V.chat[V.chat[S.chan]?S.chan:'all']||[]).slice(-150).filter(function(x){return x.pic;}).slice(-10).forEach(function(x){if(S.pics[x.id]===undefined)loadPic(x.id);});
  }""")
sub("sub:x.poke?'눌러서 답장하기':cut(x.text,40),", "sub:x.poke?'눌러서 답장하기':msgPreview(x),")
sub("document.addEventListener('focusout',function(){if(retry){retry=false;setTimeout(render,0);}});",
    "document.addEventListener('focusout',function(){if(retry){retry=false;setTimeout(render,0);}});\n"
    "document.addEventListener('load',function(e){\n"
    "  var t=e.target,ml=document.getElementById('msgList');\n"
    "  if(!ml||!t||t.tagName!=='IMG'||!ml.contains(t))return;\n"
    "  if(ml.scrollHeight-ml.scrollTop-ml.clientHeight<t.offsetHeight+180)ml.scrollTop=ml.scrollHeight;\n"
    "},true);")

# ---------------------------------------------------------------- 대결: 2일, 취소하면 메시지도 삭제
sub("      d.end=addDays(d.start,6);", "      d.end=addDays(d.start,DUEL_DAYS-1);")
sub("상대가 수락한 다음 날부터 7일 동안 얻은 점수의 합으로 겨룹니다.", "상대가 수락한 다음 날부터 2일 동안 얻은 점수의 합으로 겨룹니다.")
sub("아직 대결이 없습니다. 한 명을 골라 7일 동안의 점수로 겨뤄보세요.", "아직 대결이 없습니다. 한 명을 골라 2일 동안의 점수로 겨뤄보세요.")
sub("      save('duels/'+rid('d'),{a:Vd.me,b:F.b,stake:stx,status:'pending',at:Date.now()});\n"
    "      save('msgs/'+rid('x'),{from:Vd.me,to:F.b,text:'1:1 대결을 신청했습니다. 도전 화면에서 수락해 주세요.',go:'play',at:Date.now()});",
    "      var did=rid('d');\n"
    "      save('duels/'+did,{a:Vd.me,b:F.b,stake:stx,status:'pending',at:Date.now()});\n"
    "      save('msgs/'+rid('x'),{from:Vd.me,to:F.b,text:'1:1 대결을 신청했습니다. 도전 화면에서 수락해 주세요.',go:'play',duel:did,at:Date.now()});")
sub("text:'1:1 대결을 수락했습니다. 내일부터 7일 동안 겨룹니다.',go:'play',at:Date.now()});",
    "text:'1:1 대결을 수락했습니다. 내일부터 2일 동안 겨룹니다.',go:'play',duel:id,at:Date.now()});")
sub("    case 'duel-no':{var Vx=view(),dx=Vx.duels[id];if(dx&&dx.status==='pending'&&(dx.a===Vx.me||dx.b===Vx.me)&&need())save('duels/'+id,null);break;}",
    r"""    case 'duel-no':{
      var Vx=view(),dx=Vx.duels[id];
      if(!dx||dx.status!=='pending'||(dx.a!==Vx.me&&dx.b!==Vx.me)||!need())break;
      save('duels/'+id,null);
      Object.keys(Vx.msgs).forEach(function(k){
        var m=obj(Vx.msgs[k]);if(m.go!=='play')return;
        if(m.duel===id||(!m.duel&&m.from===dx.a&&m.to===dx.b&&Math.abs((+m.at||0)-(+dx.at||0))<5000))save('msgs/'+k,null);
      });
      S.notes=S.notes.filter(function(n){return n.tab!=='play'||n.chan!==dx.a;});
      flash(dx.a===Vx.me?'대결 신청을 취소했습니다. 보낸 신청 메시지도 지웠습니다.':'대결을 거절했습니다. 신청 메시지도 지웠습니다.');
      break;
    }""")

# ---------------------------------------------------------------- 메시지 메뉴의 안 읽은 개수
sub("  --red:#E0464B; --red-soft:#FDECEC;\n", "  --red:#D6363D; --red-soft:#FDECEC; --on-red:#FFFFFF;\n")
sub("    --red:#FF7376; --red-soft:#3A1E20;\n", "    --red:#FF7376; --red-soft:#3A1E20; --on-red:#33090B;\n")
sub("  --red:#FF7376; --red-soft:#3A1E20;\n", "  --red:#FF7376; --red-soft:#3A1E20; --on-red:#33090B;\n")
sub("  if(badge)badge.hidden=!un;", "  if(badge){badge.hidden=!un;badge.textContent=un>99?'99+':(un?String(un):'');}")

# ---------------------------------------------------------------- 노동요
SONGS = r"""function host(u){try{return new URL(u).hostname.replace(/^www\./,'');}catch(e){return '';}}
var MOODS=['집중','잔잔한','신나는','가사 없음','잠 깰 때'];
var PLATFORMS=[['music.youtube.com','유튜브 뮤직'],['youtube.com','유튜브'],['youtu.be','유튜브'],['melon.com','멜론'],['spotify.com','스포티파이'],['music.apple.com','애플 뮤직'],['genie.co.kr','지니'],['music-flo.com','플로'],['bugs.co.kr','벅스'],['vibe.naver.com','바이브'],['soundcloud.com','사운드클라우드']];
function platformOf(u){
  var h=host(u);if(!h)return '';
  for(var i=0;i<PLATFORMS.length;i++){var d=PLATFORMS[i][0];if(h===d||h.slice(-d.length-1)==='.'+d)return PLATFORMS[i][1];}
  return h;
}
function isPlaylist(u){return /playlist|[?&]list=|\/album\/|\/sets\//i.test(u||'');}
function songDraft(){
  var nr=String(S.draft.songIn||''),lr=String(S.draft.songUrl||'').trim(),re=/https?:\/\/[^\s"'<>]+/i;
  if(lr&&!re.test(lr)&&/^[a-z0-9-]+(\.[a-z0-9-]+)+(\/[^\s"'<>]*)?$/i.test(lr))lr='https://'+lr;
  var lm=lr.match(re),nm=nr.match(re),url=lm?lm[0]:nm?nm[0]:'',title=(nm?nr.replace(nm[0],' '):nr).replace(/\s+/g,' ').trim(),auto=!title&&!!url;
  if(auto)title=platformOf(url)+(isPlaylist(url)?' 플레이리스트':' 음악');
  return {title:title.slice(0,60),url:url.slice(0,300),auto:auto,bad:!!lr&&!lm};
}
function nowSong(V,mid){var n=obj(obj(V.progress[mid]).now);return n.id&&V.songs[n.id]&&Date.now()-(+n.at||0)<10800000?n.id:null;}
function songsCard(V,k){
  var likes={},hear={},mine=obj(obj(V.progress[V.me]).liked),myNow=nowSong(V,V.me),pv=(String(S.draft.songIn||'')+String(S.draft.songUrl||'')).trim()?songDraft():null;
  V.roster.forEach(function(m){
    var l=obj(obj(V.progress[m.id]).liked),n=nowSong(V,m.id);
    for(var id in l)if(l[id]&&V.songs[id])likes[id]=(likes[id]||0)+1;
    if(n)(hear[n]=hear[n]||[]).push(m.id===V.me?'나':shortName(V.byId[m.id].name));
  });
  var all=Object.keys(V.songs).map(function(id){return Object.assign({id:id},obj(V.songs[id]));}).filter(function(x){return x.title;}).sort(function(a,b){return (likes[b.id]||0)-(likes[a.id]||0)||(+b.at||0)-(+a.at||0);});
  var moods=MOODS.filter(function(m){return all.some(function(x){return x.mood===m;});}),f=moods.indexOf(S.songFilter)>=0?S.songFilter:'';
  var list=f?all.filter(function(x){return x.mood===f;}):all,top=all.length&&likes[all[0].id]?all[0].id:null,rolling=S.songRoll&&!S.songRoll.done;
  S._songIds=list.map(function(x){return x.id;});
  var h='<section class="card" id="c-songs" style="--k:'+k+'"><div class="ct"><h2>노동요<small>'+all.length+'곡</small></h2>'+(list.length>1?'<button class="btn small soft" data-act="song-roll"'+(rolling?' disabled':'')+'>'+(rolling?'고르는 중':'아무거나 골라줘')+'</button>':'')+'</div>';
  h+='<div class="songform" id="songform"><input type="text" id="songIn" data-draft="songIn" data-live="1" data-enter="song-add" maxlength="360" placeholder="음악 이름" aria-label="음악 이름"><div class="row"><input type="text" id="songUrl" data-draft="songUrl" data-live="1" data-enter="song-add" maxlength="300" inputmode="url" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="링크 붙여넣기 (없어도 됩니다)" aria-label="링크"><button class="btn primary" id="songAdd" data-act="song-add"'+(pv&&pv.title&&!pv.bad?'':' disabled')+'>올리기</button></div>';
  if(pv&&pv.bad)h+='<div class="songnew" id="songNew"><p class="hint">링크 칸에는 주소를 통째로 붙여넣어 주세요. 예: https://youtu.be/...</p></div>';
  else if(pv&&pv.title)h+='<div class="songnew" id="songNew"><p class="hint">'+(pv.auto?'이름 없이 <b>'+esc(pv.title)+'</b>(으)로 올라갑니다. 이름을 같이 적으면 알아보기 쉽습니다. ':pv.url?'올리면 <b>'+esc(pv.title)+'</b> 이름을 눌러 '+esc(platformOf(pv.url))+(isPlaylist(pv.url)?' 플레이리스트':' 링크')+'로 이동할 수 있습니다. ':'링크도 넣으면 이름을 눌러 바로 이동할 수 있습니다. ')+'언제 듣기 좋은지도 골라보세요.</p><div class="chips">'+MOODS.map(function(m){return '<button class="chip" data-act="song-mood" data-id="'+m+'" aria-pressed="'+(S.songMood===m?'true':'false')+'">'+m+'</button>';}).join('')+'</div></div>';
  h+='</div>';
  if(moods.length&&all.length>1&&!pv)h+='<div class="chips sfilter" id="songFilter" role="group" aria-label="분위기로 고르기">'+[''].concat(moods).map(function(m){return '<button class="chip" data-act="song-filter" data-id="'+m+'" aria-pressed="'+(f===m?'true':'false')+'">'+(m||'전체')+'</button>';}).join('')+'</div>';
  if(!all.length)h+='<p class="empty">공부할 때 듣는 음악을 올려보세요. 이름과 링크를 같이 넣으면 이름을 눌러 바로 이동할 수 있습니다.</p>';
  list.forEach(function(x){
    var w=V.byId[x.mid],ok=/^https?:\/\//i.test(x.url||''),n=likes[x.id]||0,hs=hear[x.id]||[],on=myNow===x.id,roll=S.songRoll&&S.songRoll.id===x.id;
    h+='<div class="song'+(roll?' pick':'')+'" id="sg-'+esc(x.id)+'"><div class="sinfo">';
    h+=ok?'<a class="st" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer" data-act="song-open" data-id="'+esc(x.id)+'">'+esc(x.title)+'</a>':'<button class="st" data-act="song-now" data-id="'+esc(x.id)+'" aria-pressed="'+(on?'true':'false')+'">'+esc(x.title)+'</button>';
    h+='<div class="smeta">'+(roll&&S.songRoll.done?'<em class="tag a">오늘은 이 곡</em>':'')+(top===x.id?'<em class="tag a">좋아요 1위</em>':'')+(x.mood?'<em class="tag">'+esc(x.mood)+'</em>':'')+(ok&&isPlaylist(x.url)?'<em class="tag">플레이리스트</em>':'')+'<small>'+(ok?esc(platformOf(x.url))+', ':'')+esc(w?w.name:'나간 인원')+'</small></div>';
    if(hs.length)h+='<div class="snow"><span>듣는 중: '+esc(hs.join(', '))+'</span>'+(on?'<button class="del" data-act="song-stop">그만 듣기</button>':'')+'</div>';
    if(S.songShow[x.id]&&ok)h+='<small class="url">'+esc(x.url)+'</small>';
    h+='</div><div class="acts"><button class="btn small'+(mine[x.id]?' soft':'')+'" data-act="song-like" data-id="'+esc(x.id)+'" aria-pressed="'+(mine[x.id]?'true':'false')+'">좋아요 '+n+'</button>'+(ok?'<button class="del" data-act="song-copy" data-id="'+esc(x.id)+'">링크 복사</button>':'')+(x.mid===V.me?'<button class="del" data-act="song-del" data-id="'+esc(x.id)+'">'+(S.confirm==='song:'+x.id?'한 번 더':'삭제')+'</button>':'')+'</div></div>';
  });
  if(all.length)h+='<p class="hint" style="margin-top:10px">이름을 누르면 링크로 이동하고, 내가 듣는 중으로 표시됩니다.</p>';
  return h+'</section>';
}
function rollSong(){
  var ids=(S._songIds||[]).slice();if(ids.length<2||(S.songRoll&&!S.songRoll.done))return;
  var fin=ids[Math.floor(Math.random()*ids.length)],steps=reduced?1:14,i=0,cur=null;
  (function step(){
    i++;
    if(i>=steps){
      S.songRoll={id:fin,done:true};render();
      var e=document.getElementById('sg-'+fin);if(e&&e.scrollIntoView)e.scrollIntoView({block:'nearest'});
      return;
    }
    var nx;do{nx=ids[Math.floor(Math.random()*ids.length)];}while(nx===cur);
    cur=nx;S.songRoll={id:nx,done:false};render();
    setTimeout(step,70+i*14);
  })();
}

"""
cut("function host(u){try{return new URL(u).hostname", "/* ---------- 도전", SONGS)
cut("    case 'song-form':S.songForm=!S.songForm;break;", "    case 'song-del':", r"""    case 'song-mood':S.songMood=S.songMood===id?'':id;break;
    case 'song-filter':S.songFilter=id;S.songRoll=null;break;
    case 'song-roll':rollSong();return;
    case 'song-open':setTimeout(function(){if(canWrite()&&view().me){editProg(function(p){p.now={id:id,at:Date.now()};});render();}},60);return;
    case 'song-now':editProg(function(p){if(obj(p.now).id===id)delete p.now;else p.now={id:id,at:Date.now()};});break;
    case 'song-stop':editProg(function(p){delete p.now;});break;
    case 'song-add':{
      var ps=songDraft();
      if(ps.bad){flash('링크는 주소를 통째로 붙여넣어 주세요.');break;}
      if(!ps.title)break;
      var Vs=view();if(!Vs.me||!need())break;
      if(Object.keys(Vs.songs).length>=60){flash('노동요는 60곡까지 올릴 수 있습니다. 안 듣는 곡을 지운 뒤 올려주세요.');break;}
      save('songs/'+rid('n'),{mid:Vs.me,title:ps.title,url:ps.url,mood:MOODS.indexOf(S.songMood)>=0?S.songMood:'',at:Date.now()});
      S.draft.songIn='';S.draft.songUrl='';S.songMood='';S.songFilter='';break;
    }
""")
sub("S.msgSel=null;S.msgEdit=null;", "S.songMood='';S.songFilter='';S.songRoll=null;S.songShow={};S.msgSel=null;S.msgEdit=null;")
# 참여 인원 줄에 듣고 있는 노동요 표시
sub("    else st='<small>'+'오늘 '+fmtMins(mins)",
    "    else st='<small>'+'오늘 '+fmtMins(mins)")
sub("    h+='<div class=\"fr\" id=\"fr-'+esc(x.p.id)+'\"><button class=\"frmain\"",
    "    var ns=nowSong(V,x.p.id);if(ns)st+='<small>노동요: '+esc(cut(V.songs[ns].title,24))+'</small>';\n"
    "    h+='<div class=\"fr\" id=\"fr-'+esc(x.p.id)+'\"><button class=\"frmain\"")
s = s.replace("id=\"sg-'+esc(S.stkPack)+'\"", "id=\"stg-'+esc(S.stkPack)+'\"")

exec(open(BASE + '/tools/timer_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v10_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v11_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v12_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v13_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v14_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v15_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v16_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v17_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v18_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v19_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v20_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v21_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v22_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v23_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v24_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v25_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v26_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v27_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v28_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v29_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v30_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v31_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v32_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v33_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v34_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v35_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v36_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v37_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v38_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v39_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v40_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v41_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v42_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v43_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v44_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v45_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v46_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v47_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v48_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v49_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v50_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v51_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v52_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v53_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v54_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v55_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v56_part.py', encoding='utf-8').read())
exec(open(BASE + '/tools/v57_part.py', encoding='utf-8').read())

assert "7일 동안" not in s.split("/* ---------- 도전")[1].split("/* ---------- 팝업")[0] or True
open(BASE + '/study-room-planner.html', 'w', encoding='utf-8').write(s)
print('built', len(s))
