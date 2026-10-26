# ---------------------------------------------------------------- v43: 점수 조정, 상점(색 무료, 새 꾸미기), 타임랩스 없애기, 할 일 모음,
# 메시지 읽음 숫자, 리포트·진도 새로, 모바일 아래 메뉴, 해금 연출·배지·타이머 모양 (JS는 src/v43.js, CSS는 src/v43.css)
V43_JS = open(BASE + '/src/v43.js', encoding='utf-8').read()
V43_CSS = open(BASE + '/src/v43.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V43_JS + "\n/* ---------- 공부방 ---------- */")

# 1) 점수: RULE3(10/27)부터 출석 3~5점(7일째 +5), 문제 내기 5점, 풀이와 답변 6점. 빙고는 그 주(10/26 주)부터 1줄 20점
sub("function attReward(n){return Math.min(10,4+n)+(n%7===0?10:0);}",
    "var RULE3='2026-10-27';\nfunction attReward(n,d){if((d||today())>=RULE3)return Math.min(5,2+n)+(n%7===0?5:0);return Math.min(10,4+n)+(n%7===0?10:0);}\nfunction bingoLine(mon){return mon>=mondayOf(RULE3)?20:10;}")
sub("certOn:10,certLate:3,quiz:10,help:3,helpMax:3,", "certOn:10,certLate:3,quiz:5,help:6,helpMax:3,")
sub("att:x.in?attReward(streak):0,", "att:x.in?attReward(streak,d):0,")
sub("quiz:(posts[m.id+'_'+d]?RULE.quiz:0)+RULE.help*Math.min(RULE.helpMax,hk),",
    "quiz:(posts[m.id+'_'+d]?(d<RULE3?10:RULE.quiz):0)+(d<RULE3?3:RULE.help)*Math.min(RULE.helpMax,hk),")
sub(".length,pts=lines*10,rs=obj(obj(V.progress[m.id]).reset);", ".length,pts=lines*bingoLine(mon),rs=obj(obj(V.progress[m.id]).reset);")
sub("문제를 올린 날 10점, 다른 사람 문제를 풀거나 질문에 답하면 1개당 3점입니다.",
    "문제를 올린 날 '+RULE.quiz+'점, 다른 사람 문제를 풀거나 질문에 답하면 1개당 '+RULE.help+'점(하루 '+RULE.helpMax+'개까지)입니다.")
sub("'문제를 올린 날 10점을 받습니다.'", "'문제를 올린 날 '+RULE.quiz+'점을 받습니다. 다른 사람이 풀어 주면 푼 사람이 '+RULE.help+'점을 받습니다.'")
sub("한 줄을 채울 때마다 주간 점수에 10점이 더해집니다.", "한 줄을 채울 때마다 주간 점수에 '+bingoLine(mon)+'점이 더해집니다.")
sub("7일째에는 10점을 더 받습니다.", "7일째에는 5점을 더 받습니다.")

# 2) 꾸미기: 새 컨셉 5개 (색 토큰은 그대로, 면·선·글꼴만)
sub("  {id:'night',name:'밤하늘',mode:'dark',soft:[.17,'#151A3F'],font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700}\n];",
    "  {id:'night',name:'밤하늘',mode:'dark',soft:[.17,'#151A3F'],font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700},\n"
    "  {id:'paper',name:'크라프트지',font:'Gaegu:wght@700',face:'Gaegu',w:700},\n"
    "  {id:'news',name:'신문',font:'Gowun+Batang:wght@700',face:'Gowun Batang',w:700},\n"
    "  {id:'sunset',name:'노을'}\n];")

# 5) 타임랩스 없애기: 게시판 종류, 올리기 단추, 배지에서 빼고 예전 글도 보이지 않게 (기록은 지우지 않음)
sub(".filter(function(q){return q.q||q.pic||q.vid;})", ".filter(function(q){return q.kind!=='lapse'&&(q.q||q.pic);})")
sub("[['all','전체'],['quiz','문제'],['ask','질문'],['lapse','타임랩스']]", "[['all','전체'],['quiz','문제'],['ask','질문']]")
sub("<button class=\"btn small soft\" data-act=\"open\" data-modal=\"lapse\">타임랩스 올리기</button>", "")
sub("문제를 내거나 모르는 것을 물어보세요. 공부하는 모습을 타임랩스로 올릴 수도 있습니다.", "문제를 내거나 모르는 것을 물어보세요. 사진을 찍어 올릴 수 있습니다.")
cut("  {id:'lapse3',cat:'board'", "  {id:'bingo5',cat:'play'", "")
sub("  if(t==='lapse')return modalLapse(V);\n", "")

sub("</style>", V43_CSS + "</style>")

# 3) 할 일 모음(inbox), 메시지 읽음(reads): 새 모음
s = s.replace("'plans','gifts'];", "'plans','gifts','inbox','reads'];")
assert s.count("'plans','gifts','inbox','reads'];") == 1
sub("gifts:merged('gifts'),", "gifts:merged('gifts'),inbox:merged('inbox'),reads:merged('reads'),")
sub("S.plans={};S.gifts={};", "S.plans={};S.gifts={};S.inbox={};S.reads={};S.ib=null;S.pastOpen=false;S.moreOpen=false;")
sub("if(t==='shop')return modalShop(V);", "if(t==='shop')return modalShop(V);\n  if(t==='inbox'&&S.ib)return modalInbox(V);")
sub("  if(type==='shop'){S.giftOpen", "  if(type==='inbox'){S.ib={sel:{},week:wkStart(today()),sid:''};S.draft.ibText='';}\n  if(type==='shop'){S.giftOpen")
# 할 일 주간 보기, 날짜 칸의 할 일, 할 일 추가 창에서 모음으로
sub("<button class=\"chip\" data-act=\"al-left\"", "'+ibBtn(V,'soft')+'<button class=\"chip\" data-act=\"al-left\"")
sub("if(mode!=='view')h+='<button class=\"btn small primary\" data-act=\"open\" data-modal=\"compose\"",
    "if(mode!=='view')h+=ibBtn(V);\n  if(mode!=='view')h+='<button class=\"btn small primary\" data-act=\"open\" data-modal=\"compose\"")
sub("else f+='<div class=\"df\"><button class=\"btn\" data-act=\"cmp-add\" data-more=\"1\"", "else f+='<div class=\"df\"><button class=\"btn\" data-act=\"cmp-inbox\"'+(text?'':' disabled')+'>모음에 넣기</button><button class=\"btn\" data-act=\"cmp-add\" data-more=\"1\"")
# 오늘 화면: 지난 날 할 일
sub("if(isT)h+=todayCard(V,3);", "if(isT)h+=pastCard(V,3)+todayCard(V,4);")
# 메시지 읽음
sub("if(lastAt>(+S.read[c]||0)){S.read[c]=lastAt;lsSet('gbb_read',JSON.stringify(S.read));}",
    "if(lastAt>(+S.read[c]||0)){S.read[c]=lastAt;lsSet('gbb_read',JSON.stringify(S.read));}\n    readsMark(V,c,lastAt);")
sub("    h+=mine?'<button class=\"mt\"", "    h+=mine?'<span class=\"mfoot\">'+unreadTag(V,c,x)+'<button class=\"mt\"")
sub("+esc(meta)+'</button>':'<small>'", "+esc(meta)+'</button></span>':'<small>'")
# 주간 리포트 더 보기
sub("return h+'</tbody></table></div></section></div></div></div>';", "return h+'</tbody></table></div></section></div></div>'+reportMore(V,from,Wk,Pv)+'</div>';")
# 모바일 더보기
sub('<span>메시지</span><i class="badge" id="chatBadge" hidden></i></button>',
    '<span>메시지</span><i class="badge" id="chatBadge" hidden></i></button>\n      <button class="navmore" id="navMore" data-act="more-open" aria-haspopup="menu" aria-expanded="false"><span>더보기</span></button>')
sub("case 'tab':goTab", "case 'tab':S.moreOpen=false;goTab")
sub("function after(V){\n  afterChat(V);", "function after(V){\n  afterChat(V);\n  try{paintMore();}catch(e){}")
sub("    case 'cmp-add':{", r"""    case 'more-open':S.moreOpen=!S.moreOpen;break;
    case 'more-x':S.moreOpen=false;break;
    case 'past-more':S.pastOpen=!S.pastOpen;break;
    case 'cmp-inbox':{
      var cib=S.cmp,tib=cmpText();if(!cib||!tib)break;
      var nib=String(S.draft.cmpNote||'').trim(),itb={t:tib.slice(0,90),sid:cib.sid||''};if(cib.type)itb.ct=cib.type;if(cib.amt>0){itb.ca=+cib.amt;itb.cu=cib.unit||'문제';}if(nib)itb.cn=nib;
      if(!ibAdd(itb)||!canWrite())break;
      S.draft.cmpNote='';closeModal();flash('할 일 모음에 넣었습니다. 할 일 모음에서 요일을 골라 넣으세요.');return;
    }
    case 'ib-sid':{if(S.ib){var ibs=el.getAttribute('data-v');S.ib.sid=S.ib.sid===ibs?'':ibs;}break;}
    case 'ib-add':{
      var ibt=String(S.draft.ibText||'').trim();if(!S.ib||!ibt)break;
      if(ibAdd({t:ibt.slice(0,90),sid:S.ib.sid||''})&&canWrite()){S.draft.ibText='';S.sync=true;S.focusAfter='ibText';}
      break;
    }
    case 'ib-sel':if(S.ib){S.ib.sel[id]=!S.ib.sel[id];}break;
    case 'ib-all':{if(!S.ib)break;var ibl=ibItems(view()),iba=ibl.every(function(x){return S.ib.sel[x.id];});S.ib.sel={};if(!iba)ibl.forEach(function(x){S.ib.sel[x.id]=true;});break;}
    case 'ib-del':{if(prev!=='ibdel:'+id){S.confirm='ibdel:'+id;break;}editInbox(function(d){delete d.items[id];});if(S.ib)delete S.ib.sel[id];break;}
    case 'ib-week':{if(!S.ib)break;var ibw=addDays(S.ib.week,7*(+el.getAttribute('data-d')||0));S.ib.week=ibw<wkStart(today())?wkStart(today()):alClamp(ibw);break;}
    case 'ib-put':ibAssign(el.getAttribute('data-d'));break;
    case 'cmp-add':{""")
# 진도 모두 보기 정렬
sub("    case 'prog-mode':{", "    case 'prog-sort':S.progSort=id;break;\n    case 'prog-mode':{")

# 7) 타이머 모양: 아날로그 시계, 두 겹 고리 더하기. 링·원판에 눈금
sub("var TSTYLES=[['ring','링'],['digits','숫자'],['bar','막대'],['pie','원판'],['flip','넘김 시계']];",
    "var TSTYLES=[['ring','링'],['digits','숫자'],['bar','막대'],['pie','원판'],['flip','넘김 시계'],['analog','아날로그'],['orbit','두 겹 고리']];")
sub("var TSPREV={", "var TSPREV={analog:'<svg viewBox=\"0 0 48 48\"><circle class=\"f\" cx=\"24\" cy=\"24\" r=\"19\"/><path class=\"w\" d=\"M24,24 L24,8 A16,16 0 0,1 38,16 Z\"/><path class=\"h\" d=\"M24 24 L36 17\"/><path class=\"s\" d=\"M24 27 L24 9\"/><circle class=\"n\" cx=\"24\" cy=\"24\" r=\"2.2\"/></svg>',orbit:'<svg viewBox=\"0 0 48 48\"><circle class=\"k\" cx=\"24\" cy=\"24\" r=\"18\"/><path class=\"a\" d=\"M24,6 A18,18 0 1,1 6,24\"/><circle class=\"k\" cx=\"24\" cy=\"24\" r=\"12\"/><path class=\"b\" d=\"M24,12 A12,12 0 0,1 36,24\"/></svg>',")
sub("  if(st==='ring')return '<div class=\"tf ring'+cls+'\">", r"""  if(st==='analog'){
    var an=anAngles(mid?V0&&V0.live[mid]:null,o,f);
    return '<div class="tf analog'+cls+'"><svg viewBox="0 0 200 200" aria-hidden="true"><circle class="anb" cx="100" cy="100" r="97"/><circle class="anf" cx="100" cy="100" r="88"/><g class="pt">'+AN_TICKS+'</g>'+AN_NUMS+'<g'+pa+' data-k="an"><path class="ans" d="'+piePath(f.pie)+'"/><line class="anm" x1="100" y1="108" x2="100" y2="34" transform="rotate('+an.m+' 100 100)"/><line class="ansec" x1="100" y1="116" x2="100" y2="26" transform="rotate('+an.s+' 100 100)"/></g><circle class="anc" cx="100" cy="100" r="5.5"/><circle class="anc2" cx="100" cy="100" r="2"/></svg><div class="ptx">'+lab+txt+sub+'</div></div>';
  }
  if(st==='orbit'){
    var so=f.idle?0:(o.e%60000)/60000;
    return '<div class="tf orbit ring'+cls+'"><svg viewBox="0 0 200 200" aria-hidden="true"><g class="pt ot">'+RING_TICKS+'</g><circle class="rg-t" cx="100" cy="100" r="90"/><circle class="rg-p"'+pa+' data-k="ring" cx="100" cy="100" r="90" style="stroke-dashoffset:'+(RING*(1-show)).toFixed(1)+'"/><circle class="ob-t" cx="100" cy="100" r="74"/><circle class="ob-p"'+(mid?' data-lvp="'+esc(mid)+'"':'')+' data-k="orbs" cx="100" cy="100" r="74" style="stroke-dashoffset:'+(ORB*(1-so)).toFixed(1)+'"/></svg><div class="rg-in">'+lab+txt+sub+'</div></div>';
  }
  if(st==='ring')return '<div class="tf ring'+cls+'">""")
# 링: 눈금
sub("""<svg viewBox="0 0 200 200" aria-hidden="true"><circle class="rg-t" cx="100" cy="100" r="90"/>""",
    """<svg viewBox="0 0 200 200" aria-hidden="true"><g class="pt rt">'+RING_TICKS+'</g><circle class="rg-t" cx="100" cy="100" r="90"/>""")
# 원판: 숫자
sub("""<g class="pt">'+PIE_TICKS+'</g><circle class="pk" cx="100" cy="100" r="7"/>""",
    """<g class="pt">'+PIE_TICKS+'</g>'+PIE_NUMS+'<circle class="pk" cx="100" cy="100" r="7"/>""")
# 매초 바꾸기
sub("else if(pk==='pie')el.setAttribute('d',piePath(lvPie(Lx,ox)));",
    "else if(pk==='pie')el.setAttribute('d',piePath(lvPie(Lx,ox)));else if(pk==='an')anSet(el,Lx,ox);else if(pk==='orbs')el.style.strokeDashoffset=(ORB*(1-(ox.e%60000)/60000)).toFixed(1);")
