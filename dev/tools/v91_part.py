# ---------------------------------------------------------------- v91: 노동요 태그 직접 만들기. 곡마다 태그 3개까지(songs.tags={태그:1}, mood는 첫 태그), 기본 태그 MOODS 5개 + 글로 적는 태그(songTagClean, 10자),
# 올릴 때 고르기·적기(S.songMoods), 올린 사람은 '태그'로 고치기(S.songTagEdit), 거르기 칩은 쓰인 태그 모두 #과 곡 수
sub("var MOODS=['집중','잔잔한','신나는','가사 없음','잠 깰 때'];", r"""var MOODS=['집중','잔잔한','신나는','가사 없음','잠 깰 때'];
var SONG_TAG_MAX=3;
function songTagClean(t){return String(t||'').replace(/^#+/,'').replace(/[.#$\[\]\/]/g,'').replace(/\s+/g,' ').trim().slice(0,10);}
function songTagOrder(list){return list.slice().sort(function(a,b){var i=MOODS.indexOf(a),j=MOODS.indexOf(b);return (i<0?99:i)-(j<0?99:j);});}
function songTags(x){var o={};if(x&&x.mood)o[x.mood]=1;var t=obj(x&&x.tags);for(var k in t)if(t[k])o[k]=1;return songTagOrder(Object.keys(o));}
function songMoodSel(){var s=obj(S.songMoods);return songTagOrder(Object.keys(s).filter(function(k){return s[k];}));}
function songTagChips(act,id,cur){
  var all=MOODS.concat(cur.filter(function(m){return MOODS.indexOf(m)<0;}));
  return all.map(function(m){return '<button class="chip" data-act="'+act+'"'+(id?' data-id="'+esc(id)+'"':' data-id="'+esc(m)+'"')+' data-v="'+esc(m)+'" aria-pressed="'+(cur.indexOf(m)>=0?'true':'false')+'">#'+esc(m)+'</button>';}).join('');
}
function songTagInput(key,act,id){return '<span class="stagin"><input type="text" data-draft="'+esc(key)+'" data-enter="'+act+'"'+(id?' data-id="'+esc(id)+'"':'')+' maxlength="12" placeholder="태그 직접 적기" aria-label="태그 직접 적기"><button class="btn small" data-act="'+act+'"'+(id?' data-id="'+esc(id)+'"':'')+'>추가</button></span>';}""")
sub("var moods=MOODS.filter(function(m){return all.some(function(x){return x.mood===m;});}),", "var tcnt={};all.forEach(function(x){songTags(x).forEach(function(m){tcnt[m]=(tcnt[m]||0)+1;});});var moods=Object.keys(tcnt).sort(function(a,b){var i=MOODS.indexOf(a),j=MOODS.indexOf(b);if(i>=0||j>=0)return (i<0?99:i)-(j<0?99:j);return tcnt[b]-tcnt[a];}),")
sub("f?all.filter(function(x){return x.mood===f;}):all", "f?all.filter(function(x){return songTags(x).indexOf(f)>=0;}):all")
sub("aria-pressed=\"'+(f===m?'true':'false')+'\">'+(m||'전체')+'</button>';", "aria-pressed=\"'+(f===m?'true':'false')+'\">'+(m?'#'+esc(m)+' <small>'+tcnt[m]+'</small>':'전체 <small>'+all.length+'</small>')+'</button>';")
sub("aria-label=\"분위기로 고르기\">", "aria-label=\"태그로 고르기\">")
sub("<div class=\"chips\">'+MOODS.map(function(m){return '<button class=\"chip\" data-act=\"song-mood\" data-id=\"'+m+'\" aria-pressed=\"'+(S.songMood===m?'true':'false')+'\">'+m+'</button>';}).join('')+'</div>", "<div class=\"chips\">'+songTagChips('song-mood','',songMoodSel())+songTagInput('songTagIn','song-tagnew','')+'</div>")
sub("(x.mood?'<em class=\"tag\">'+esc(x.mood)+'</em>':'')", "songTags(x).map(function(m){return '<em class=\"tag stg\">#'+esc(m)+'</em>';}).join('')")
sub("if(x.note)h+='<p class=\"snote\">'+esc(x.note)+'</p>';", "if(x.note)h+='<p class=\"snote\">'+esc(x.note)+'</p>';\n    if(S.songTagEdit===x.id&&x.mid===V.me)h+='<div class=\"chips stedit\">'+songTagChips('song-tagset',x.id,songTags(x))+songTagInput('songTagE:'+x.id,'song-tagset',x.id)+'<button class=\"btn small\" data-act=\"song-tagedit\" data-id=\"'+esc(x.id)+'\">다 했어요</button></div>';")
sub("(x.mid===V.me?'<button class=\"del\" data-act=\"song-del\"", "(x.mid===V.me?'<button class=\"del\" data-act=\"song-tagedit\" data-id=\"'+esc(x.id)+'\">태그</button>':'')+(x.mid===V.me?'<button class=\"del\" data-act=\"song-del\"")
sub("    case 'song-mood':S.songMood=S.songMood===id?'':id;break;", r"""    case 'song-mood':case 'song-tagnew':{
      var tg=name==='song-tagnew'?songTagClean(S.draft.songTagIn):el.getAttribute('data-v');if(!tg)break;
      S.songMoods=obj(S.songMoods);
      if(S.songMoods[tg]&&name==='song-mood')delete S.songMoods[tg];
      else if(!S.songMoods[tg]){if(songMoodSel().length>=SONG_TAG_MAX){flash('태그는 '+SONG_TAG_MAX+'개까지 달 수 있습니다.');break;}S.songMoods[tg]=1;}
      if(name==='song-tagnew'){S.draft.songTagIn='';var tin=el.tagName==='INPUT'?el:(el.parentNode&&el.parentNode.querySelector&&el.parentNode.querySelector('input'));if(tin)tin.value='';}
      S.songMood=songMoodSel()[0]||'';break;
    }
    case 'song-tagedit':S.songTagEdit=S.songTagEdit===id?null:id;break;
    case 'song-tagset':{
      var Vt=view(),so=obj(Vt.songs[id]),typed=el.tagName==='INPUT'||!el.getAttribute('data-v'),tv=typed?songTagClean(S.draft['songTagE:'+id]):el.getAttribute('data-v');
      if(!tv||!so.title||so.mid!==Vt.me||!need())break;
      var cur=songTags(so),on=cur.indexOf(tv)<0;if(!on&&typed){S.draft['songTagE:'+id]='';break;}
      if(on&&cur.length>=SONG_TAG_MAX){flash('태그는 '+SONG_TAG_MAX+'개까지 달 수 있습니다.');break;}
      cur=on?cur.concat([tv]):cur.filter(function(m){return m!==tv;});cur=songTagOrder(cur);
      var ns=clone(so);ns.mood=cur[0]||'';ns.tags={};cur.forEach(function(m){ns.tags[m]=1;});if(!cur.length)delete ns.tags;
      if(typed){S.draft['songTagE:'+id]='';var tin=el.tagName==='INPUT'?el:(el.parentNode&&el.parentNode.querySelector&&el.parentNode.querySelector('input'));if(tin)tin.value='';}
      save('songs/'+id,ns);break;
    }""")
sub("mood:MOODS.indexOf(S.songMood)>=0?S.songMood:'',note:", "mood:songMoodSel()[0]||'',tags:(function(){var o={};songMoodSel().forEach(function(m){o[m]=1;});return o;})(),note:")
sub("S.draft.songNote='';S.draft.songIn='';S.draft.songUrl='';S.songMood='';", "S.draft.songNote='';S.draft.songIn='';S.draft.songUrl='';S.songMood='';S.songMoods={};S.draft.songTagIn='';")
