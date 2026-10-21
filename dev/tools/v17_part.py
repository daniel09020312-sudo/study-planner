# ---------------------------------------------------------------- 게시판: 공부 타임랩스
LAPSE_JS = open(BASE + '/src/lapse.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", LAPSE_JS + "\n/* ---------- 공부방 ---------- */")

# 글 목록에 타임랩스도 넣고, 문제 점수와 집계에서는 뺀다
sub(".filter(function(q){return q.q||q.pic;})", ".filter(function(q){return q.q||q.pic||q.vid;})")
assert s.count("q.kind!=='ask'") == 4
s = s.replace("q.kind!=='ask'", "q.kind!=='ask'&&q.kind!=='lapse'")
sub("function postCard(V,q,k){", """function boardShow(q){if(S.filter==='all')return true;if(S.filter==='lapse')return q.kind==='lapse';return q.kind!=='lapse'&&(S.filter==='ask')===(q.kind==='ask');}
function postCard(V,q,k){""")
assert s.count("S.filter==='all'||(S.filter==='ask')===(q.kind==='ask')") == 2
s = s.replace("function(q){return S.filter==='all'||(S.filter==='ask')===(q.kind==='ask');}", "boardShow")

# 게시판 머리
sub("<h1>게시판</h1><p>문제를 내거나 모르는 것을 물어보세요. 사진을 찍어 올릴 수 있습니다.</p>",
    "<h1>게시판</h1><p>문제를 내거나 모르는 것을 물어보세요. 공부하는 모습을 타임랩스로 올릴 수도 있습니다.</p>")
sub("  [['all','전체'],['quiz','문제'],['ask','질문']].forEach(function(r){h+='<button data-act=\"filter\"",
    "  [['all','전체'],['quiz','문제'],['ask','질문'],['lapse','타임랩스']].forEach(function(r){h+='<button data-act=\"filter\"")
sub("<button class=\"btn small soft\" data-act=\"open\" data-modal=\"post\" data-kind=\"ask\">질문하기</button>",
    "<button class=\"btn small soft\" data-act=\"open\" data-modal=\"post\" data-kind=\"ask\">질문하기</button><button class=\"btn small soft\" data-act=\"open\" data-modal=\"lapse\">타임랩스 올리기</button>")
sub("<p class=\"empty\">'+(S.filter==='ask'?'아직 질문이 없습니다.'",
    "<p class=\"empty\">'+(S.filter==='lapse'?'아직 올라온 타임랩스가 없습니다. 휴대폰 카메라의 타임랩스로 공부하는 모습을 찍어 올려 보세요.':S.filter==='ask'?'아직 질문이 없습니다.'")
sub("""    h+='<li>'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><small>문제 '+c+', 답변 '+r+'</small></li>';""",
    """    var lpc=V.posts.filter(function(q){return q.mid===m.id&&q.kind==='lapse'&&(+q.at||0)>=monT;}).length;
    h+='<li>'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><small>문제 '+c+', 답변 '+r+(lpc?', 타임랩스 '+lpc:'')+'</small></li>';""")

# 글 카드: 타임랩스는 재생기, 문제용 단추는 뺀다
sub("  var a=V.byId[q.mid],ask=q.kind==='ask',shown=!!S.reveal[q.id],own=q.mid===V.me,reps=V.repBy[q.id]||[];",
    "  var a=V.byId[q.mid],ask=q.kind==='ask',lp=q.kind==='lapse',shown=!!S.reveal[q.id],own=q.mid===V.me,reps=V.repBy[q.id]||[];")
sub("<span class=\"tag'+(ask?' a':'')+'\">'+(ask?'질문':'문제')+'</span>",
    "<span class=\"tag'+(ask?' a':lp?' lp':'')+'\">'+(lp?'타임랩스':ask?'질문':'문제')+'</span>")
sub("  if(q.pic)h+=shot(q.id);\n  if(!ask&&shown)", "  if(lp)h+=lapseBox(q);else if(q.pic)h+=shot(q.id);\n  if(!ask&&!lp&&shown)")
sub("  if(!ask)qa+='<button class=\"btn small\" data-act=\"quiz-reveal\"", "  if(!ask&&!lp)qa+='<button class=\"btn small\" data-act=\"quiz-reveal\"")
sub("  if(!ask&&!own)qa+='<button class=\"btn small'+(mine?' soft':'')+'\" data-act=\"quiz-solved\"", "  if(!ask&&!lp&&!own)qa+='<button class=\"btn small'+(mine?' soft':'')+'\" data-act=\"quiz-solved\"")

# 지울 때 장면 묶음도 지운다
sub("save('quiz/'+id,null);if(q7.pic)S.net.write('pics/'+id,null).catch(function(){});",
    "save('quiz/'+id,null);if(q7.pic)S.net.write('pics/'+id,null).catch(function(){});if(q7.vid){for(var lci=0;lci<(+q7.vid.c||0);lci++)S.net.write('pics/'+id+'_c'+lci,null).catch(function(){});}lapseStop(id);delete S.lapse[id];")

# 창
sub("  if(t==='score')return modalScore(V);", "  if(t==='score')return modalScore(V);\n  if(t==='lapse')return modalLapse(V);")
sub("  if(type==='plan'){S.pl=newPlan();S.draft.plNote='';}", "  if(type==='lapse'){lapseStop('_new');delete S.lapse._new;S.lup={frames:[],busy:false};S.draft.lapseCap='';}\n  if(type==='plan'){S.pl=newPlan();S.draft.plNote='';}")
sub("  if(S.modal.type==='focus')lock(false);\n  S.closing=true;render();", "  if(S.modal.type==='focus')lock(false);\n  if(S.modal.type==='lapse')lapseStop('_new');\n  S.closing=true;render();")

# 동작
sub("    case 'pic-load':loadPic(id);break;", r"""    case 'pic-load':loadPic(id);break;
    case 'lapse-pick':lapsePick();return;
    case 'lapse-up':lapseUpload();return;
    case 'lapse-sid':{if(S.lup){var lsv=el.getAttribute('data-v');S.lup.sid=S.lup.sid===lsv?'':lsv;}break;}
    case 'lapse-tap':{var LP=S.lapse[id];if(LP&&LP.frames){if(LP.on)lapseStop(id);else lapsePlay(id);}else if(id!=='_new')lapseLoad(id);break;}""")
