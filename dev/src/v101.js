/* ---------- v101: 노동요 칸 정리. 한 줄 목록(처음 SONG_LIM곡, '더 보기'), 줄을 누르면 펼쳐서 한마디·댓글·링크 복사·태그·삭제,
   댓글은 각자 progress.<나>.scm={<댓글 id>:{s:곡 id,t:글,at}}에 적고 모두 모아 보여 줌(곡마다 SCM_MAX개까지 보임),
   방장 보기는 창 'songadm'(사람별·곡별) ---------- */
var SONG_LIM=6,SCM_LEN=120,SCM_KEEP=200;
function songCmts(V){
  if(V._scm)return V._scm;
  var o={};
  V.roster.forEach(function(m){var c=obj(obj(V.progress[m.id]).scm);for(var k in c){var x=obj(c[k]);if(!x.s||!V.songs[x.s]||!x.t)continue;(o[x.s]=o[x.s]||[]).push({id:k,mid:m.id,t:String(x.t),at:+x.at||0});}});
  for(var s in o)o[s].sort(function(a,b){return a.at-b.at;});
  return V._scm=o;
}
function songAgo(ts){
  var d=Date.now()-ts;if(d<60000)return '방금';if(d<3600000)return Math.floor(d/60000)+'분 전';if(d<86400000)return Math.floor(d/3600000)+'시간 전';
  var x=new Date(ts);return (x.getMonth()+1)+'/'+x.getDate();
}
var SG_ICON={play:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg>',stop:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="1.5" fill="currentColor"/></svg>',
  out:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  heart:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="currentColor"/></svg>',
  cmt:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H10l-4 3v-3H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'};
function songsCard(V,k){
  var likes={},hear={},mine=obj(obj(V.progress[V.me]).liked),myNow=nowSong(V,V.me),pv=(String(S.draft.songIn||'')+String(S.draft.songUrl||'')).trim()?songDraft():null,cm=songCmts(V);
  V.roster.forEach(function(m){
    var l=obj(obj(V.progress[m.id]).liked),n=nowSong(V,m.id);
    for(var id in l)if(l[id]&&V.songs[id])likes[id]=(likes[id]||0)+1;
    if(n)(hear[n]=hear[n]||[]).push(m.id===V.me?'나':shortName(V.byId[m.id].name));
  });
  var all=Object.keys(V.songs).map(function(id){return Object.assign({id:id},obj(V.songs[id]));}).filter(function(x){return x.title;}).sort(function(a,b){return (likes[b.id]||0)-(likes[a.id]||0)||(+b.at||0)-(+a.at||0);});
  var tcnt={};all.forEach(function(x){songTags(x).forEach(function(m){tcnt[m]=(tcnt[m]||0)+1;});});var moods=Object.keys(tcnt).sort(function(a,b){var i=MOODS.indexOf(a),j=MOODS.indexOf(b);if(i>=0||j>=0)return (i<0?99:i)-(j<0?99:j);return tcnt[b]-tcnt[a];}),f=moods.indexOf(S.songFilter)>=0?S.songFilter:'';
  var list=songSorted(V,f?all.filter(function(x){return songTags(x).indexOf(f)>=0;}):all,likes),pls=songPlays(V),top=all.length&&likes[all[0].id]?all[0].id:null,rolling=S.songRoll&&!S.songRoll.done;
  S._songIds=list.map(function(x){return x.id;});
  var lim=Math.max(SONG_LIM,+S.songLim||0),q=String(S.draft.songQ||'').trim();
  var show=list.slice(0,lim);
  /* 지금 플레이어·골라 준 곡·펼친 곡은 가려지지 않게 */
  [S.songPlay,S.songRoll&&S.songRoll.id,S.songOpen].forEach(function(id){if(id&&show.every(function(x){return x.id!==id;})){var x=list.filter(function(y){return y.id===id;})[0];if(x)show.push(x);}});
  var h='<section class="card" id="c-songs" style="--k:'+k+'"><div class="ct"><h2>노동요<small>'+all.length+'곡</small></h2><div class="row sghd">'+(list.length>1?'<button class="btn small soft" data-act="song-roll"'+(rolling?' disabled':'')+'>'+(rolling?'고르는 중':'아무거나 골라줘')+'</button>':'')+(adminId(V)===V.me&&all.length?'<button class="btn small soft" data-act="song-adm">누가 들었나 (방장)</button>':'')+'</div></div>';
  h+='<div class="songform" id="songform"><input type="text" id="songIn" data-draft="songIn" data-live="1" data-enter="song-add" maxlength="360" placeholder="음악 이름" aria-label="음악 이름"><div class="row"><input type="text" id="songUrl" data-draft="songUrl" data-live="1" data-enter="song-add" maxlength="300" inputmode="url" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="링크 붙여넣기 (없어도 됩니다)" aria-label="링크"><button class="btn primary" id="songAdd" data-act="song-add"'+(pv&&pv.title&&!pv.bad?'':' disabled')+'>올리기</button></div>';
  if(pv&&pv.bad)h+='<div class="songnew" id="songNew"><p class="hint">링크 칸에는 주소를 통째로 붙여넣어 주세요. 예: https://youtu.be/...</p></div>';
  else if(pv&&pv.title)h+='<div class="songnew" id="songNew"><p class="hint">'+(pv.auto?'이름 없이 <b>'+esc(pv.title)+'</b>(으)로 올라갑니다. 이름을 같이 적으면 알아보기 쉽습니다. ':pv.url?'올리면 <b>'+esc(pv.title)+'</b> 이름을 눌러 '+esc(platformOf(pv.url))+(isPlaylist(pv.url)?' 플레이리스트':' 링크')+'로 이동할 수 있습니다. ':'링크도 넣으면 이름을 눌러 바로 이동할 수 있습니다. ')+'언제 듣기 좋은지도 골라보세요.</p><div class="chips">'+songTagChips('song-mood','',songMoodSel())+songTagInput('songTagIn','song-tagnew','')+'</div><input type="text" class="snotein" data-draft="songNote" maxlength="60" placeholder="한마디 (선택, 예: 수학 풀 때 최고)" aria-label="한마디"></div>';
  h+='</div>';
  if(moods.length&&all.length>1&&!pv)h+='<div class="chips sfilter" id="songFilter" role="group" aria-label="태그로 고르기">'+[''].concat(moods).map(function(m){return '<button class="chip" data-act="song-filter" data-id="'+m+'" aria-pressed="'+(f===m?'true':'false')+'">'+(m?'#'+esc(m)+' <small>'+tcnt[m]+'</small>':'전체 <small>'+all.length+'</small>')+'</button>';}).join('')+'</div>';
  if(!pv)h+=songTools(V,all.length);
  if(all.length&&!list.length)h+='<p class="empty">'+(S.songSort==='mine'&&!q?'아직 좋아요를 누른 곡이 없습니다.':'찾는 곡이 없습니다.')+'</p>';
  if(!all.length)h+='<p class="empty">공부할 때 듣는 음악을 올려보세요. 이름과 링크를 같이 넣으면 이름을 눌러 바로 이동할 수 있습니다.</p>';
  if(show.length)h+='<div class="sglist">';
  show.forEach(function(x){
    var w=V.byId[x.mid],ok=/^https?:\/\//i.test(x.url||''),n=likes[x.id]||0,hs=hear[x.id]||[],on=myNow===x.id,roll=S.songRoll&&S.songRoll.id===x.id,emb=ok?songEmbed(x.url):null,op=S.songOpen===x.id,cs=cm[x.id]||[],pl=S.songPlay===x.id,tg=songTags(x);
    h+='<div class="song sg2'+(roll?' pick':'')+(op?' open':'')+(pl||on?' on':'')+'" id="sg-'+esc(x.id)+'">';
    h+='<div class="sgrow">';
    if(emb)h+='<button class="sgp" data-act="song-play" data-id="'+esc(x.id)+'" aria-pressed="'+(pl?'true':'false')+'" aria-label="'+(pl?'플레이어 닫기':'여기서 듣기')+'" title="'+(pl?'플레이어 닫기':'여기서 듣기')+'">'+(pl?SG_ICON.stop:SG_ICON.play)+'</button>';
    else if(ok)h+='<a class="sgp out" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer" data-act="song-open" data-id="'+esc(x.id)+'" aria-label="링크 열기" title="링크 열기">'+SG_ICON.out+'</a>';
    else h+='<span class="sgp none" aria-hidden="true">'+SG_ICON.play+'</span>';
    h+='<div class="sinfo">';
    h+=ok?'<a class="st" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer" data-act="song-open" data-id="'+esc(x.id)+'">'+esc(x.title)+'</a>':'<button class="st" data-act="song-now" data-id="'+esc(x.id)+'" aria-pressed="'+(on?'true':'false')+'">'+esc(x.title)+'</button>';
    h+='<div class="smeta">'+(roll&&S.songRoll.done?'<em class="tag a">오늘은 이 곡</em>':'')+(top===x.id?'<em class="tag a">좋아요 1위</em>':'')+(Date.now()-(+x.at||0)<3*86400000?'<em class="tag snew">새 곡</em>':'')+tg.slice(0,op?3:2).map(function(m){return '<em class="tag stg">#'+esc(m)+'</em>';}).join('')+(!op&&tg.length>2?'<em class="tag stg">+'+(tg.length-2)+'</em>':'')+'<small>'+esc(w?shortName(w.name):'나간 인원')+(pls[x.id]?' · 모두 '+pls[x.id]+'번 들음':'')+'</small></div>';
    if(x.note&&!op)h+='<p class="snote one">'+esc(x.note)+'</p>';
    if(hs.length)h+='<div class="snow"><span>듣는 중: '+esc(hs.join(', '))+'</span>'+(on?'<button class="del" data-act="song-stop">그만 듣기</button>':'')+'</div>';
    h+='</div><div class="acts">';
    h+='<button class="sgl'+(mine[x.id]?' on':'')+'" data-act="song-like" data-id="'+esc(x.id)+'" aria-pressed="'+(mine[x.id]?'true':'false')+'" aria-label="좋아요 '+n+'">'+SG_ICON.heart+'<span>'+n+'</span></button>';
    h+='<button class="sgc" data-act="song-x" data-id="'+esc(x.id)+'" aria-expanded="'+(op?'true':'false')+'" aria-label="댓글과 더 보기, 댓글 '+cs.length+'개">'+SG_ICON.cmt+'<span>'+cs.length+'</span></button>';
    h+='</div></div>';
    if(op){
      h+='<div class="sdet">';
      if(x.note)h+='<p class="snote">'+esc(x.note)+'</p>';
      if(S.songShow[x.id]&&ok)h+='<small class="url">'+esc(x.url)+'</small>';
      if(S.songTagEdit===x.id&&x.mid===V.me)h+='<div class="chips stedit">'+songTagChips('song-tagset',x.id,songTags(x))+songTagInput('songTagE:'+x.id,'song-tagset',x.id)+'<button class="btn small" data-act="song-tagedit" data-id="'+esc(x.id)+'">다 했어요</button></div>';
      h+='<div class="sgcm"><b class="sgch">댓글 '+cs.length+'</b>';
      if(!cs.length)h+='<p class="hint">아직 댓글이 없습니다. 이 곡 어땠는지 남겨 보세요.</p>';
      cs.forEach(function(c){var cw=V.byId[c.mid];h+='<div class="sgci"><b>'+esc(cw?shortName(cw.name):'나간 인원')+'</b><span>'+esc(c.t)+'</span><time>'+esc(songAgo(c.at))+'</time>'+(c.mid===V.me||adminId(V)===V.me?'<button class="del" data-act="song-cdel" data-id="'+esc(c.mid+'|'+c.id)+'">'+(S.confirm==='scm:'+c.id?'한 번 더':'지우기')+'</button>':'')+'</div>';});
      if(V.me)h+='<div class="sgcin"><input type="text" data-draft="scm:'+esc(x.id)+'" data-enter="song-cadd" data-id="'+esc(x.id)+'" maxlength="'+SCM_LEN+'" placeholder="댓글 달기" aria-label="댓글 달기"><button class="btn small primary" data-act="song-cadd" data-id="'+esc(x.id)+'">남기기</button></div>';
      h+='</div><div class="row sgmore">'+(ok?'<button class="del" data-act="song-copy" data-id="'+esc(x.id)+'">링크 복사</button>':'')+(x.mid===V.me?'<button class="del" data-act="song-tagedit" data-id="'+esc(x.id)+'">태그 고치기</button><button class="del" data-act="song-del" data-id="'+esc(x.id)+'">'+(S.confirm==='song:'+x.id?'한 번 더':'곡 삭제')+'</button>':'')+'<small>'+(+obj(obj(V.progress[V.me]).sp)[x.id]?'내가 '+(+obj(obj(V.progress[V.me]).sp)[x.id])+'번 들음 · ':'')+esc(w?w.name:'나간 인원')+' · '+esc(songAgo(+x.at||0))+' 올림</small></div>';
      h+='</div>';
    }
    h+='</div>';
  });
  if(show.length)h+='</div>';
  var rest=list.length-Math.min(list.length,lim);
  if(rest>0||lim>SONG_LIM)h+='<div class="row sgpage">'+(rest>0?'<button class="btn small soft" data-act="song-lim" data-id="more">'+Math.min(rest,10)+'곡 더 보기 <small>남은 '+rest+'곡</small></button>':'')+(lim>SONG_LIM?'<button class="btn small" data-act="song-lim" data-id="less">접기</button>':'')+'</div>';
  return h+'</section>';
}
function songAdmRow(){return '';}
function songAdmHtml(){return '';}
/* 방장 보기 창 */
function modalSongAdm(V){
  if(adminId(V)!==V.me)return '';
  var tab=S.songAdmTab==='song'?'song':'people',pick=S.songAdmP,ids=Object.keys(V.songs).filter(function(k){return obj(V.songs[k]).title;}),cm=songCmts(V);
  var rows=V.roster.map(function(m){var p=obj(V.progress[m.id]),sp=obj(p.sp),lk=obj(p.liked),pl=Object.keys(sp).filter(function(k){return V.songs[k]&&+sp[k]>0;}).sort(function(a,b){return sp[b]-sp[a];}),li=Object.keys(lk).filter(function(k){return lk[k]&&V.songs[k];}),tot=pl.reduce(function(s,k){return s+(+sp[k]||0);},0),c=0;for(var s in cm)cm[s].forEach(function(x){if(x.mid===m.id)c++;});return {m:m,pl:pl,sp:sp,li:li,tot:tot,c:c,now:nowSong(V,m.id)};}).sort(function(a,b){return b.tot-a.tot||b.li.length-a.li.length;});
  var h='<p class="hint">방장만 보입니다. 사람을 누르면 들은 곡과 좋아요가 펼쳐집니다.</p><div class="seg mini" role="group" aria-label="보기" style="grid-template-columns:1fr 1fr;margin-bottom:12px"><button data-act="songadm-tab" data-id="people" aria-pressed="'+(tab==='people'?'true':'false')+'">사람별</button><button data-act="songadm-tab" data-id="song" aria-pressed="'+(tab==='song'?'true':'false')+'">곡별</button></div>';
  h+='<div class="sadmbody">';
  if(tab==='people'){
    h+='<div class="sadmtbl"><div class="sadmth"><span>이름</span><span>들은 횟수</span><span>곡 수</span><span>좋아요</span><span>댓글</span></div>';
    rows.forEach(function(r){
      var op=pick===r.m.id;
      h+='<button class="sadmtr'+(op?' on':'')+'" data-act="songadm-p" data-id="'+esc(r.m.id)+'" aria-expanded="'+(op?'true':'false')+'"><span><b>'+esc(r.m.name)+'</b>'+(r.now?'<em class="tag a">듣는 중</em>':'')+'</span><span>'+r.tot+'</span><span>'+r.pl.length+'</span><span>'+r.li.length+'</span><span>'+r.c+'</span></button>';
      if(op){
        h+='<div class="sadmdet">';
        if(r.now)h+='<p class="hint">지금 듣는 곡: <b>'+esc(obj(V.songs[r.now]).title)+'</b></p>';
        h+='<h4>들은 곡</h4>'+(r.pl.length?'<ol class="sadml">'+r.pl.map(function(k){return '<li><span>'+esc(obj(V.songs[k]).title)+'</span><em>'+r.sp[k]+'번</em></li>';}).join('')+'</ol>':'<p class="hint">없음</p>');
        h+='<h4>좋아요</h4>'+(r.li.length?'<div class="chips">'+r.li.map(function(k){return '<span class="chip">'+esc(cut(obj(V.songs[k]).title,24))+'</span>';}).join('')+'</div>':'<p class="hint">없음</p>');
        h+='</div>';
      }
    });
    h+='</div>';
  }else{
    var per=ids.map(function(id){var lk=[],pl=[],tot=0;V.roster.forEach(function(m){var p=obj(V.progress[m.id]),n=+obj(p.sp)[id]||0;if(obj(p.liked)[id])lk.push(shortName(m.name));if(n>0){pl.push([shortName(m.name),n]);tot+=n;}});pl.sort(function(a,b){return b[1]-a[1];});return {id:id,x:obj(V.songs[id]),lk:lk,pl:pl,tot:tot,c:(cm[id]||[]).length};}).sort(function(a,b){return b.tot-a.tot||b.lk.length-a.lk.length;});
    per.forEach(function(r){
      var w=V.byId[r.x.mid];
      h+='<div class="sadms"><div class="sadmsh"><b>'+esc(r.x.title)+'</b><small>'+esc(w?shortName(w.name):'나간 인원')+' 올림 · '+r.tot+'번 · 좋아요 '+r.lk.length+' · 댓글 '+r.c+'</small></div>';
      h+='<p>'+(r.pl.length?'들은 사람: '+r.pl.map(function(x){return esc(x[0])+' <em>'+x[1]+'</em>';}).join(', '):'<span class="hint">들은 사람 없음</span>')+'</p>';
      if(r.lk.length)h+='<p>좋아요: '+esc(r.lk.join(', '))+'</p>';
      h+='</div>';
    });
    if(!per.length)h+='<p class="empty">곡이 없습니다.</p>';
  }
  return dlg('wide',{id:'songadm',t:'노동요 기록'},h+'</div>');
}
function songCAdd(id){
  var V=view();if(!V.me||!V.songs[id]||!need())return;
  var k='scm:'+id,t=String(S.draft[k]||'').trim().slice(0,SCM_LEN);if(!t){flash('댓글을 적어 주세요.');return;}
  editProg(function(p){p.scm=obj(p.scm);var ks=Object.keys(p.scm);if(ks.length>=SCM_KEEP){ks.sort(function(a,b){return (+obj(p.scm[a]).at||0)-(+obj(p.scm[b]).at||0);});ks.slice(0,ks.length-SCM_KEEP+1).forEach(function(z){delete p.scm[z];});}p.scm[rid('c')]={s:id,t:t,at:Date.now()};});
  S.draft[k]='';var el=document.querySelector('#sg-'+(window.CSS&&CSS.escape?CSS.escape(id):id)+' .sgcin input');if(el)el.value='';
}
