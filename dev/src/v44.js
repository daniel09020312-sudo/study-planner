/* ---------- v44: 학급 규모(50명) 편의와 안정성 ---------- */

/* 이름 겹침: 같은 이름이 둘이면 목록에서 누가 누군지 알 수 없으므로 막는다 */
function nameKey(n){return String(n||'').replace(/\s+/g,'').toLowerCase();}
function nameTaken(V,nm,exceptId){var k=nameKey(nm);return !!k&&V.roster.some(function(m){return m.id!==exceptId&&nameKey(m.name)===k;});}
var NAME_DUP_MSG='같은 이름이 이미 있습니다. 목록에서 고르거나, 이름 뒤에 구분할 글자를 붙여 주세요. (예: 김민준A)';

/* 여러 명 한꺼번에 추가: 한 줄에 한 명(쉼표도 됨) */
function newMemberIds(n,taken){
  var out=[],used={};Object.keys(taken).forEach(function(k){used[k]=1;});
  while(out.length<n){var id=rid('m')+Math.random().toString(36).slice(2,4);if(!used[id]){used[id]=1;out.push(id);}}
  return out;
}
function bulkAdd(){
  var V=view();if(!V.me||!need())return;
  var names=String(S.draft.memberBulk||'').split(/[\n,，;]+/).map(function(x){return x.trim().slice(0,12);}).filter(Boolean);
  if(!names.length){flash('이름을 한 줄에 한 명씩 적어 주세요.');return;}
  var seen={},dup=0,add=[];
  V.roster.forEach(function(m){seen[nameKey(m.name)]=1;});
  names.forEach(function(n){var k=nameKey(n);if(seen[k]){dup++;return;}seen[k]=1;add.push(n);});
  var room=Math.max(0,ROSTER_MAX-V.roster.length),over=Math.max(0,add.length-room);add=add.slice(0,room);
  if(!add.length){flash(dup?'모두 이미 있는 이름입니다.':'더 추가할 수 없습니다. 인원은 '+ROSTER_MAX+'명까지입니다.');return;}
  var taken={};V.roster.forEach(function(m){taken[m.id]=1;});
  var ids=newMemberIds(add.length,taken);
  editCfg(function(c){add.forEach(function(n,i){if(c.roster.length<ROSTER_MAX)c.roster.push({id:ids[i],name:n});});if(typeof c.certHour!=='number')c.certHour=29;});
  if(!canWrite())return;
  S.draft.memberBulk='';S.bulkOpen=false;S.sync=true;
  flash(add.length+'명을 추가했습니다.'+(dup?' 이미 있는 이름 '+dup+'개는 건너뛰었습니다.':'')+(over?' 한도('+ROSTER_MAX+'명) 때문에 '+over+'명은 넣지 못했습니다.':''));
}
function bulkSec(){
  var h='<div class="bulk"><button class="linkbtn" data-act="bulk-toggle" aria-expanded="'+(S.bulkOpen?'true':'false')+'">'+(S.bulkOpen?'한꺼번에 추가 접기':'여러 명 한꺼번에 추가')+'</button>';
  if(S.bulkOpen)h+='<textarea data-draft="memberBulk" rows="6" maxlength="1500" placeholder="한 줄에 한 명씩 적으세요&#10;예:&#10;김민준&#10;이서연" aria-label="추가할 이름 여러 명"></textarea><div class="row" style="margin-top:8px"><button class="btn primary" data-act="member-bulk">모두 추가</button></div><p class="hint">같은 이름은 건너뛰고, 인원은 '+ROSTER_MAX+'명까지 넣을 수 있습니다.</p>';
  return h+'</div>';
}

/* 이름 고르는 첫 화면: 사람이 많으면 검색 */
function gateList(V){var q=nameKey(S.draft.gateQ);return q?V.roster.filter(function(m){return nameKey(V.byId[m.id].name).indexOf(q)>=0;}):V.roster;}
function gateSearch(V){
  if(V.roster.length<=8)return '';
  return '<input type="text" class="gsearch" data-draft="gateQ" data-live="1" inputmode="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="이름 검색 ('+V.roster.length+'명)" aria-label="이름 검색">'+(gateList(V).length?'':'<p class="hint">찾는 이름이 없습니다. 아래에서 직접 추가할 수 있습니다.</p>');
}

/* 방장 공지: meta/config.notice = {t, at, by}. 이 기기에서 닫으면 새 공지가 올라올 때까지 숨김 */
function noticeOf(V){var n=obj(V.cfg.notice);return n.t?{t:String(n.t).slice(0,300),at:+n.at||0,by:n.by||''}:null;}
function noticeHtml(V){
  if(!V||!V.me)return '';
  var n=noticeOf(V);if(!n||lsGet('gbb_notice')===String(n.at))return '';
  var who=n.by&&V.byId[n.by]?V.byId[n.by].name:'';
  return '<div class="notice nt" role="status"><span class="ntl">공지</span><span class="ntt">'+esc(n.t)+'</span>'+(who?'<small>'+esc(who)+'</small>':'')+'<button data-act="notice-x" aria-label="공지 닫기">닫기</button></div>';
}
function noticeSec(V){
  if(!V.me||adminId(V)!==V.me)return '';
  var cur=noticeOf(V);
  return '<div class="sec"><h3>공지<small>방장만 올릴 수 있습니다</small></h3><textarea data-draft="noticeText" rows="3" maxlength="200" placeholder="예: 11월 3일 시험 범위가 바뀌었습니다" aria-label="공지 내용"></textarea><div class="row" style="margin-top:8px"><button class="btn small primary" data-act="notice-save">올리기</button>'+(cur?'<button class="btn small" data-act="notice-off">내리기</button>':'')+'</div>'+(cur?'<p class="hint">지금 공지: '+esc(cur.t)+'</p>':'<p class="hint">올리면 모두의 화면 위에 한 줄로 나옵니다. 각자 닫을 수 있습니다.</p>')+'</div>';
}

/* 메시지 목록: 최근에 대화한 사람이 위(왼쪽)로 */
function dmOrder(V){
  var ids=V.roster.filter(function(m){return m.id!==V.me;}).map(function(m){return m.id;}),last={};
  ids.forEach(function(k){var l=V.chat[k]||[];last[k]=l.length?+l[l.length-1].at||0:0;});
  return ids.map(function(k,i){return {k:k,i:i};}).sort(function(a,b){return (last[b.k]-last[a.k])||(a.i-b.i);}).map(function(x){return x.k;});
}

/* 참여 인원 카드: 많으면 앞의 12명과 나만 보이고 나머지는 펼치기 */
function frShown(V,list){
  if(S.frAll||list.length<=14)return list;
  var top=list.slice(0,12),me=list.filter(function(x){return x.p.me;})[0];
  if(me&&top.indexOf(me)<0)top.push(me);
  return top;
}

/* 할 일 바로 적기: 과목 이름이나 줄임말로 시작하면 그 과목으로 */
function quickParse(V,text){
  text=String(text||'').trim();if(!text)return null;
  var best=null;
  mySubs(V).forEach(function(s){[s.name,subAbbr(V,s.id)].forEach(function(c){c=String(c||'').trim();if(c&&text.indexOf(c)===0&&(!best||c.length>best.len))best={sid:s.id,len:c.length};});});
  if(best){var rest=text.slice(best.len).replace(/^[\s,:·\-]+/,'');return {sid:best.sid,text:rest||text};}
  return {sid:'',text:text};
}
function canAddTo(V,d){return modeOf(d)!=='view'&&!dayLocked(V,d);}
function quickAddRow(V,date){
  return '<div class="qadd"><input type="text" id="qadd-'+date+'" data-draft="qadd:'+date+'" data-enter="g-quick" data-date="'+date+'" maxlength="90" placeholder="할 일을 바로 적고 Enter (예: 미적 3단원 20문제)" aria-label="할 일 바로 적기"><button class="btn small" data-act="g-quick" data-date="'+date+'">넣기</button></div>';
}

/* 오래된 메시지는 지운다(보관 14일). 한 사람이 자기 것만, 한 번에 40개까지. 앱을 열고 한 번, 메시지를 보낼 때마다 */
var MSG_KEEP_DAYS=14;
function prune(V){
  var lim=Date.now()-MSG_KEEP_DAYS*86400000,n=0;
  Object.keys(V.msgs).forEach(function(k){
    var x=obj(V.msgs[k]);
    if(n<40&&x.from===V.me&&+x.at<lim){save('msgs/'+k,null);if(x.pic&&S.net)S.net.write('pics/'+k,null).catch(function(){});n++;}
  });
}
function pruneOnce(V){
  if(S.pruned||!S.ready||!V||!V.me||!canWrite()||!netFresh())return;
  S.pruned=true;setTimeout(function(){try{prune(view());}catch(e){}},5000);
}

/* 화면 하나가 그려지다 실패해도 앱 전체가 멈추지 않게 */
function safeView(V){
  try{if(window.__FORCE_VIEW_ERROR===S.vtab)throw new Error('forced view error');return ({cal:viewCal,room:viewRoom,prog:viewProg,rank:viewRank,report:viewReport,play:viewPlay,board:viewBoard,chat:viewChat}[S.vtab]||viewCal)(V);}
  catch(e){
    try{console.error('view error',S.vtab,e);}catch(x){}
    return '<div class="view" id="view-err"><section class="card errcard"><div class="ct"><h2>이 화면을 그리지 못했습니다</h2></div><p class="hint">일시적인 문제일 수 있습니다. 다른 화면으로 가거나 새로고침해 보세요. 기록은 그대로 저장되어 있습니다.</p><div class="row" style="margin-top:12px"><button class="btn primary" data-act="reload">새로고침</button><button class="btn" data-act="tab" data-tab="cal">달력으로</button></div></section></div>';
  }
}
function safeModal(V){
  try{return modalHtml(V);}
  catch(e){try{console.error('modal error',S.modal&&S.modal.type,e);}catch(x){}S.modal=null;S.closing=false;return '';}
}

/* 오래된 브라우저(color-mix를 모름): 화면이 조금 다르게 보일 수 있다고 한 번 알린다 */
var OLD_BROWSER=(function(){try{return !(window.CSS&&CSS.supports&&CSS.supports('color','color-mix(in srgb, red 50%, blue)'));}catch(e){return false;}})();
function oldBrowserHtml(){
  if(!OLD_BROWSER||lsGet('gbb_old')==='1')return '';
  return '<div class="notice old" role="status"><span>이 기기의 브라우저가 오래되어 화면이 조금 다르게 보일 수 있습니다. 아이폰과 아이패드는 iOS 16.4 이상으로 업데이트하면 가장 잘 보입니다.</span><button data-act="old-x">닫기</button></div>';
}

/* 사용법 */
function modalHelp(V){
  var items=[
    ['하루 시작','공부방에서 타이머를 켜면 모두에게 공부 중으로 보입니다. 오늘 출석을 누르면 출석 점수를 받고, 하루가 끝나면 인증하세요.'],
    ['할 일 적기','달력에서 날짜를 고르면 할 일 칸 위에 입력칸이 있습니다. 적고 Enter를 누르면 바로 들어가고, 과목 이름이나 줄임말로 시작하면 그 과목으로 들어갑니다. 요일을 아직 못 정한 일은 할 일 모음에 적어 두고 요일을 눌러 나눠 넣으세요.'],
    ['마감 있는 할 일','시험이나 수행평가처럼 며칠까지 끝낼 일은 마감 있는 할 일로 정하면 날짜별로 나눠서 그날 할 일에 넣어 줍니다.'],
    ['지난 날','인증 마감(다음 날 새벽 5시)이 지나도 지난 날의 할 일은 완료 표시하고 인증할 수 있습니다. 늦은 인증 점수가 적용되고, 새 할 일을 더하거나 고칠 수는 없습니다.'],
    ['점수','출석, 공부 시간, 모두 끝내고 인증, 문제 내기와 풀이, 하루 순위, 빙고로 점수가 쌓입니다. 자세한 점수표는 아래 단추에서 볼 수 있습니다.'],
    ['문제가 생길 때','화면이 이상하면 새로고침하세요. 인터넷이 끊겨도 내 기록은 이 기기에 모아 두었다가 연결되면 올라갑니다. 친구 기록은 연결된 뒤에 새로 보입니다.']
  ];
  var b='<div class="helplist">'+items.map(function(x){return '<section><h3>'+x[0]+'</h3><p>'+esc(x[1])+'</p></section>';}).join('')+'</div>';
  b+='<div class="row" style="margin-top:12px"><button class="btn small" data-act="open" data-modal="score">점수표 보기</button>'+(typeof modalA2HS==='function'?'<button class="btn small" data-act="open" data-modal="a2hs">앱으로 추가하기</button>':'')+'</div>';
  return dlg('wide',{id:'help',t:'사용법'},b);
}

/* 더보기 메뉴: Esc로 닫기, 화면이 넓어지면(패드, 가로) 닫기 */
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&S.moreOpen&&!S.modal){S.moreOpen=false;render();}});
window.addEventListener('resize',function(){if(S.moreOpen&&window.innerWidth>=700){S.moreOpen=false;render();}});
