/* ---------- v90: 노동요 더하기. 정렬(인기·최신·많이 들은·내 좋아요), 이름 검색, 새 곡 표시, 들은 횟수(progress.<나>.sp={곡:횟수}),
   한마디(songs/<id>.note), 유튜브·스포티파이는 앱 안에서 바로 듣기(S.songPlay), 공부 타이머 아래 노동요 줄(songBar) ---------- */
var SONG_SORTS=[['top','인기'],['new','최신'],['play','많이 들은'],['mine','내 좋아요']];
function songPlays(V){var o={};V.roster.forEach(function(m){var sp=obj(obj(V.progress[m.id]).sp);for(var k in sp)if(V.songs[k])o[k]=(o[k]||0)+(+sp[k]||0);});return o;}
function songEmbed(u){
  u=String(u||'');var m,h=host(u),q=function(k){var r=u.match(new RegExp('[?&]'+k+'=([\\w-]+)'));return r?r[1]:'';},ok=function(x){return /^[\w-]{6,}$/.test(x||'');};
  if(/(^|\.)youtube\.com$|^youtu\.be$/.test(h)){
    var id='',list=q('list');
    if(h==='youtu.be'){m=u.match(/youtu\.be\/([\w-]+)/);id=m?m[1]:'';}
    else{id=q('v');if(!id){m=u.match(/\/(?:shorts|live|embed)\/([\w-]+)/);id=m?m[1]:'';}}
    if(ok(id))return {k:'yt',src:'https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0'+(ok(list)?'&list='+list:'')};
    if(ok(list))return {k:'yt',src:'https://www.youtube-nocookie.com/embed/videoseries?list='+list+'&autoplay=1&rel=0'};
    return null;
  }
  if(/(^|\.)spotify\.com$/.test(h)){m=u.match(/spotify\.com\/(?:intl-[a-z]+\/)?(track|playlist|album|episode|show)\/([A-Za-z0-9]+)/);if(m)return {k:'sp',src:'https://open.spotify.com/embed/'+m[1]+'/'+m[2]};}
  return null;
}
function songSorted(V,all,likes){
  var so=SONG_SORTS.some(function(x){return x[0]===S.songSort;})?S.songSort:'top',pl=songPlays(V),mine=obj(obj(V.progress[V.me]).liked),q=String(S.draft.songQ||'').trim().toLowerCase();
  var l=all.slice();
  if(q)l=l.filter(function(x){return (String(x.title)+' '+String(x.note||'')+' '+String(x.mood||'')).toLowerCase().indexOf(q)>=0;});
  if(so==='mine')l=l.filter(function(x){return mine[x.id];});
  if(so==='new')l.sort(function(a,b){return (+b.at||0)-(+a.at||0);});
  else if(so==='play')l.sort(function(a,b){return (pl[b.id]||0)-(pl[a.id]||0)||(likes[b.id]||0)-(likes[a.id]||0);});
  return l;
}
function songTools(V,n){
  var so=SONG_SORTS.some(function(x){return x[0]===S.songSort;})?S.songSort:'top';
  if(!n)return '';
  var h='<div class="stools"><div class="seg mini ssort" role="group" aria-label="노동요 정렬" style="grid-template-columns:repeat(4,minmax(0,1fr))">'+SONG_SORTS.map(function(x){return '<button data-act="song-sort" data-id="'+x[0]+'" aria-pressed="'+(so===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  if(n>=6)h+='<input type="text" class="ssearch" data-draft="songQ" data-live="1" inputmode="search" autocomplete="off" spellcheck="false" placeholder="노동요 찾기 (이름, 한마디)" aria-label="노동요 찾기">';
  return h+'</div>';
}
/* 공부 타이머 아래 노동요 줄: 지금 듣는 곡, 함께 듣는 사람 수, 아무거나 골라줘, 노동요 칸으로 */
function songBar(V){
  if(!V.me)return '';
  var ids=Object.keys(V.songs).filter(function(k){return obj(V.songs[k]).title;});
  var my=nowSong(V,V.me),cnt=0;V.roster.forEach(function(m){if(m.id!==V.me&&nowSong(V,m.id))cnt++;});
  var pick=S.songRoll&&S.songRoll.done&&V.songs[S.songRoll.id]?S.songRoll.id:null,cur=my||pick,x=cur?obj(V.songs[cur]):null;
  var h='<div class="sbar" id="songBar"><span class="sbl">노동요</span>';
  if(x)h+='<span class="sbt">'+(my?'듣는 중 ':'오늘은 ')+'<b>'+esc(cut(x.title,28))+'</b></span>';
  else h+='<span class="sbt">'+(ids.length?ids.length+'곡 있음':'아직 올린 곡이 없습니다')+'</span>';
  if(cnt)h+='<em class="tag">'+cnt+'명 듣는 중</em>';
  h+='<span class="sbb">';
  if(x&&/^https?:\/\//i.test(x.url||''))h+=(songEmbed(x.url)?'<button class="btn small soft" data-act="song-play" data-id="'+esc(cur)+'">'+(S.songPlay===cur&&S.songPlayW==='bar'?'플레이어 닫기':'여기서 듣기')+'</button>':'<a class="btn small soft" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer" data-act="song-open" data-id="'+esc(cur)+'">열기</a>');
  if(ids.length>1)h+='<button class="btn small soft" data-act="song-pick">아무거나 골라줘</button>';
  h+='<button class="btn small" data-act="song-goto">'+(ids.length?'노동요 보기':'노동요 올리기')+'</button></span>';
  if(S.songPlay&&S.songPlay===cur&&S.songPlayW==='bar'&&x){var e=songEmbed(x.url);if(e)h+=songFrame(e,'bar');}
  return h+'</div>';
}
function songFrame(e,w){return '<div class="sply '+e.k+'" id="sply-'+w+'"><iframe src="'+esc(e.src)+'" title="노동요 플레이어" loading="lazy" allow="autoplay; encrypted-media; clipboard-write; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>';}
function songListen(id){if(canWrite()&&view().me)editProg(function(p){p.now={id:id,at:Date.now()};p.sp=obj(p.sp);p.sp[id]=(+p.sp[id]||0)+1;});}
