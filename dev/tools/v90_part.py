# ---------------------------------------------------------------- v90: 노동요 기능 더하기(src/v90.js): 정렬·검색·새 곡·들은 횟수·한마디·앱 안에서 듣기, 공부 타이머 아래 노동요 줄, 공부방 오른쪽 맨 위로
V90_JS = open(BASE + '/src/v90.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V90_JS + "\n/* ---------- 공부방 ---------- */")
sub("var list=f?all.filter(function(x){return x.mood===f;}):all,top=", "var list=songSorted(V,f?all.filter(function(x){return x.mood===f;}):all,likes),pls=songPlays(V),top=")
sub("  if(!all.length)h+='<p class=\"empty\">공부할 때 듣는 음악을 올려보세요.", "  if(!pv)h+=songTools(V,all.length);\n  if(all.length&&!list.length)h+='<p class=\"empty\">'+(S.songSort==='mine'&&!String(S.draft.songQ||'').trim()?'아직 좋아요를 누른 곡이 없습니다.':'찾는 곡이 없습니다.')+'</p>';\n  if(!all.length)h+='<p class=\"empty\">공부할 때 듣는 음악을 올려보세요.")
sub("(x.mood?'<em class=\"tag\">'+esc(x.mood)+'</em>':'')", "(Date.now()-(+x.at||0)<3*86400000?'<em class=\"tag snew\">새 곡</em>':'')+(x.mood?'<em class=\"tag\">'+esc(x.mood)+'</em>':'')")
sub("esc(w?w.name:'나간 인원')+'</small></div>';", "esc(w?w.name:'나간 인원')+(pls[x.id]?', '+pls[x.id]+'번 들음':'')+'</small></div>';\n    if(x.note)h+='<p class=\"snote\">'+esc(x.note)+'</p>';")
sub("    if(S.songShow[x.id]&&ok)h+='<small class=\"url\">'+esc(x.url)+'</small>';", "    if(S.songShow[x.id]&&ok)h+='<small class=\"url\">'+esc(x.url)+'</small>';\n    var emb=ok?songEmbed(x.url):null;")
sub("h+='</div><div class=\"acts\"><button class=\"btn small'+(mine[x.id]", "h+='</div><div class=\"acts\">'+(emb?'<button class=\"btn small soft\" data-act=\"song-play\" data-id=\"'+esc(x.id)+'\" aria-pressed=\"'+(S.songPlay===x.id?'true':'false')+'\">'+(S.songPlay===x.id?'플레이어 닫기':'여기서 듣기')+'</button>':'')+'<button class=\"btn small'+(mine[x.id]")
sub("aria-pressed=\"'+(S.songMood===m?'true':'false')+'\">'+m+'</button>';}).join('')+'</div></div>';", "aria-pressed=\"'+(S.songMood===m?'true':'false')+'\">'+m+'</button>';}).join('')+'</div><input type=\"text\" class=\"snotein\" data-draft=\"songNote\" maxlength=\"60\" placeholder=\"한마디 (선택, 예: 수학 풀 때 최고)\" aria-label=\"한마디\"></div>';")
sub("mood:MOODS.indexOf(S.songMood)>=0?S.songMood:'',at:Date.now()});\n      S.draft.songIn='';", "mood:MOODS.indexOf(S.songMood)>=0?S.songMood:'',note:String(S.draft.songNote||'').trim().slice(0,60),at:Date.now()});\n      S.draft.songNote='';S.draft.songIn='';")
sub("    case 'song-open':setTimeout(function(){if(canWrite()&&view().me){editProg(function(p){p.now={id:id,at:Date.now()};});render();}},60);return;",
    r"""    case 'song-open':setTimeout(function(){songListen(id);render();},60);return;
    case 'song-play':{var spOff=S.songPlay;if(!id||S.songPlay===id){S.songPlay=null;if(spOff&&canWrite()&&view().me)editProg(function(p){if(obj(p.now).id===spOff)delete p.now;});}else{songListen(id);S.songPlay=id;S.songMin=false;}break;}
    case 'song-dockmin':S.songMin=!S.songMin;break;
    case 'song-sort':S.songSort=id;S.songRoll=null;break;
    case 'song-pick':{if(S.tab!=='room')break;rollSong();setTimeout(function(){var e=document.getElementById('songBar');if(e&&e.scrollIntoView)e.scrollIntoView({block:'nearest'});},50);return;}
    case 'song-goto':{var sc=document.getElementById('c-songs');if(sc&&sc.scrollIntoView)sc.scrollIntoView({behavior:reduced?'auto':'smooth',block:'start'});var si=document.getElementById(Object.keys(view().songs).length?'songIn':'songIn');if(si&&!Object.keys(view().songs).length)setTimeout(function(){try{si.focus();}catch(e){}},300);return;}""")
sub("return h+'</section>'+cgCard(V,1)+togetherCard(V,2)+'</div><div class=\"stack\">'+quietCard(V,1)+peopleCard(V,t,1)+flagCard(V,2)+songsCard(V,3)+'</div></div></div>';",
    "return h+'</section>'+cgCard(V,1)+togetherCard(V,2)+'</div><div class=\"stack\">'+songsCard(V,1)+peopleCard(V,t,2)+flagCard(V,3)+quietCard(V,4)+'</div></div></div>';")
sub("  h+='<p class=\"hint\" style=\"margin-top:12px\">'+(m==='pomo'?'집중한 시간만", "  h+=songBar(V);\n  h+='<p class=\"hint\" style=\"margin-top:12px\">'+(m==='pomo'?'집중한 시간만")
sub("try{paintMore();pruneOnce(V);eggTick(V);cgTick(V);meetTick(V);", "try{songDock();}catch(e){}\n  try{paintMore();pruneOnce(V);eggTick(V);cgTick(V);meetTick(V);")
