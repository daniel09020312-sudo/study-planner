# ---------------------------------------------------------------- v44: 학급 규모(50명) 편의와 안정성, 오류 고치기 (JS는 src/v44.js, CSS는 src/v44.css)
V44_JS = open(BASE + '/src/v44.js', encoding='utf-8').read()
V44_CSS = open(BASE + '/src/v44.css', encoding='utf-8').read()
# 예전 prune(보관 30일)은 v44.js의 것으로 바꾼다
cut("function prune(V){", "function notesHtml(V){", "")
sub("/* ---------- 공부방 ---------- */", V44_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V44_CSS + "</style>")

# ---- 1) 오류 고치기
# 빙고 점수가 20점이 된 뒤에도 점수 초기화가 줄마다 10점만 빼던 것
sub("bingo(Vr,mondayOf(tr)).per[Vr.me].lines*10:0;", "bingo(Vr,mondayOf(tr)).per[Vr.me].lines*bingoLine(mondayOf(tr)):0;")
# 인증 마감이 지난 날에는 할 일을 더할 수 없는데 단추는 보이고, 눌러도 아무 말 없이 버려지던 것
sub("  if(mode!=='view')h+=ibBtn(V);\n  if(mode!=='view')h+='<button class=\"btn small primary\" data-act=\"open\" data-modal=\"compose\"",
    "  if(canAddTo(V,date))h+=ibBtn(V);\n  if(canAddTo(V,date))h+='<button class=\"btn small primary\" data-act=\"open\" data-modal=\"compose\"")
sub("  h+='</div></div>';\n  if(g.length){\n    if(g.length>1)h+='<div class=\"gtools\">",
    "  h+='</div></div>';\n  if(canAddTo(V,date)&&g.length<GMAX)h+=quickAddRow(V,date);\n  else if(mode!=='view'&&dayLocked(V,date))h+='<p class=\"hint\">인증 마감이 지나 새 할 일을 더할 수 없습니다. 완료 표시와 인증은 할 수 있습니다.</p>';\n  if(g.length){\n    if(g.length>1)h+='<div class=\"gtools\">")
sub("  }else if(mode==='view'){\n    h+='<p class=\"empty\">이날은 할 일을 적지 않았습니다.</p>';", "  }else if(mode==='view'||dayLocked(V,date)){\n    h+='<p class=\"empty\">이날은 할 일을 적지 않았습니다.</p>';")
sub("  if(mode!=='view'&&g.length<GMAX)h+='<button class=\"wkadd\"", "  if(canAddTo(V,d)&&g.length<GMAX)h+='<button class=\"wkadd\"")
# 지난 날 보호가 새 할 일을 버릴 때 알려 준다
sub("    if(!o){if(open)out.push(g);return;}", "    if(!o){if(open)out.push(g);else S.gdRej=true;return;}")
sub("  return Object.assign({},data,{goals:out});", "  if(S.gdRej){S.gdRej=false;flash('인증 마감이 지나 이 날에는 새 할 일을 더할 수 없습니다.');}\n  return Object.assign({},data,{goals:out});")
# 창으로도 막는다(단축키 N, 시간표 빈 칸, 오래 열어 둔 창)
sub("function openModal(type,el){\n  var V=view();S.ttPend=null;",
    "function openModal(type,el){\n  var V=view();S.ttPend=null;\n  if(type==='compose'&&V.me){var cdt=(el&&el.getAttribute('data-date'))||today();if(dayLocked(V,cdt)){flash('인증 마감이 지나 이 날에는 새 할 일을 더할 수 없습니다.');return;}}")

# 색은 무료가 됐으므로 예전에 색을 사느라 쓴 잉크는 돌려준다. 이제 없는 물건(없어진 컨셉)에 쓴 잉크도 돌려준다
sub("  Object.keys(own).forEach(function(k){spent+=Math.max(0,+own[k]||0);});",
    "  Object.keys(own).forEach(function(k){var si=shopItem(k);if(!si||si.free)return;spent+=Math.max(0,+own[k]||0);});")

# 점수 초기화 안내 같은 안내 문구
# ---- 2) 학급 규모 편의
# 이름 겹침 막기
sub("var nn=String(S.draft.newName||'').trim();if(!nn||!need())break;", "var nn=String(S.draft.newName||'').trim();if(!nn||!need())break;\n      if(nameTaken(view(),nn.slice(0,12))){flash(NAME_DUP_MSG);break;}")
sub("var mn=String(S.draft.memberName||'').trim();if(!mn)break;", "var mn=String(S.draft.memberName||'').trim();if(!mn)break;\n      if(nameTaken(view(),mn.slice(0,12))){flash(NAME_DUP_MSG);break;}")
sub("if(kind==='member-name'){var Vc0=view();if(!v||!Vc0.me||(id!==Vc0.me&&adminId(Vc0)!==Vc0.me))return;",
    "if(kind==='member-name'){var Vc0=view();if(!v||!Vc0.me||(id!==Vc0.me&&adminId(Vc0)!==Vc0.me))return;\n    if(nameTaken(Vc0,v.slice(0,12),id)){flash(NAME_DUP_MSG);render();return;}")
# 설정: 여러 명 한꺼번에, 방장 넘기기, 공지, 사용법
sub("""<button class="btn" data-act="member-add"'+dis+'>인원 추가</button></div></div>';""",
    """<button class="btn" data-act="member-add"'+dis+'>인원 추가</button></div>'+(canWrite()?bulkSec():'')+'</div>';""")
sub("+(V.me&&m.id!==V.me&&(isAdm||m.id!==adm)?'<button class=\"btn small'",
    "+(isAdm&&m.id!==V.me&&canWrite()?'<button class=\"del\" data-act=\"admin-give\" data-id=\"'+esc(m.id)+'\">'+(S.confirm==='give:'+m.id?'한 번 더 누르면 방장을 넘깁니다':'방장 넘기기')+'</button>':'')+(V.me&&m.id!==V.me&&(isAdm||m.id!==adm)?'<button class=\"btn small'")
sub("b+='</div><div class=\"sec\"><h3>키보드 단축키<small>", "b+='</div>'+noticeSec(V)+'<div class=\"sec\"><h3>사용법</h3><div class=\"row\"><button class=\"btn small\" data-act=\"open\" data-modal=\"help\">사용법 보기</button></div></div><div class=\"sec\"><h3>키보드 단축키<small>")
sub("  if(t==='settings')return modalSettings(V);", "  if(t==='settings')return modalSettings(V);\n  if(t==='help')return modalHelp(V);")

# 첫 화면 이름 검색
sub("    h+='<div class=\"people\">';\n    V.roster.forEach(function(m){h+='<button class=\"person\" data-act=\"who\"",
    "    h+=gateSearch(V)+'<div class=\"people\">';\n    gateList(V).forEach(function(m){h+='<button class=\"person\" data-act=\"who\"")
# 공지와 오래된 브라우저 알림
sub("  try{b+=schNowHtml(V0);}catch(e){}", "  try{b+=oldBrowserHtml();b+=noticeHtml(V0);b+=schNowHtml(V0);}catch(e){}")
# 순위: 내 순위로
sub("' 순위<small>'+esc(shortDate(from)+' ~ '+shortDate(to))+'</small></h2></div>';",
    "' 순위<small>'+esc(shortDate(from)+' ~ '+shortDate(to))+'</small></h2>'+(V.me&&st.length>8&&any?'<button class=\"btn small soft\" data-act=\"rank-me\">내 순위로</button>':'')+'</div>';")
# 메시지 목록: 최근 대화 순
sub("['all'].concat(V.roster.filter(function(m){return m.id!==V.me;}).map(function(m){return m.id;})).forEach(function(k){", "['all'].concat(dmOrder(V)).forEach(function(k){")
# 참여 인원 카드: 앞의 12명과 나
sub("  list.forEach(function(x){\n    var g=x.day.goals,done=g.filter(isDone).length,man=sumMins(x.day.manual)", "  var shown=frShown(V,list);\n  shown.forEach(function(x){\n    var g=x.day.goals,done=g.filter(isDone).length,man=sumMins(x.day.manual)")
sub("  return h+'</section>';\n}\nfunction flagList(V){",
    "  if(list.length>14)h+='<button class=\"plfin\" data-act=\"fr-all\" aria-expanded=\"'+(S.frAll?'true':'false')+'\">'+(S.frAll?'접기':'나머지 '+(list.length-shown.length)+'명 보기')+'</button>';\n  return h+'</section>';\n}\nfunction flagList(V){")

# ---- 3) 저장과 안정성
# 읽음과 모음은 바뀐 칸만 저장(같은 사람의 두 기기가 서로 덮어쓰지 않게)
sub("  var d=clone(cur);d[c]=at;save('reads/'+V.me,d);", "  var d=clone(cur);d[c]=at;savePatch('reads/'+V.me,cur,d);")
sub("  var d=clone(obj(V.inbox[V.me]));d.items=obj(d.items);fn(d);\n  save('inbox/'+V.me,d);", "  var b0=clone(obj(V.inbox[V.me])),d=clone(b0);d.items=obj(d.items);fn(d);\n  savePatch('inbox/'+V.me,b0,d);")
# 오래된 읽음 숫자는 세지 않는다(3일)
sub("  if(x.from!==V.me||+x.at<READS_SINCE)return 0;", "  if(x.from!==V.me||+x.at<READS_SINCE||Date.now()-(+x.at)>3*86400000)return 0;")
# 화면 오류 복구
sub("  else h=({cal:viewCal,room:viewRoom,prog:viewProg,rank:viewRank,report:viewReport,play:viewPlay,board:viewBoard,chat:viewChat}[S.vtab]||viewCal)(V);", "  else h=safeView(V);")
sub("  paint(layer,S.ready?modalHtml(V):'');\n  after(V);\n}", "  paint(layer,S.ready?safeModal(V):'');\n  try{after(V);}catch(e){try{console.error('after error',e);}catch(x){}}\n}")
sub("try{paintMore();}catch(e){}", "try{paintMore();pruneOnce(V);}catch(e){}")
# view()가 복사를 덜 하게: 덮어쓴 값이 없으면 그대로 돌려준다(50명 학급에서 한 번에 수천 건을 복사하던 것)
sub("""function merged(name){
  var out=Object.assign({},S[name]),pre=name+'/';
  for(var p in O){if(p.indexOf(pre)===0){var id=p.slice(pre.length);if(O[p]===null)delete out[id];else out[id]=O[p];}}
  return out;
}""", """function merged(name){
  var out=null,pre=name+'/';
  for(var p in O){if(p.indexOf(pre)===0){if(!out)out=Object.assign({},S[name]);var id=p.slice(pre.length);if(O[p]===null)delete out[id];else out[id]=O[p];}}
  return out||S[name];
}""")

# ---- 4) 동작
sub("    case 'more-open':", r"""    case 'reload':location.reload();return;
    case 'old-x':lsSet('gbb_old','1');break;
    case 'notice-x':{var Vnx=view(),nnx=noticeOf(Vnx);if(nnx)lsSet('gbb_notice',String(nnx.at));break;}
    case 'notice-save':{
      var nst=String(S.draft.noticeText||'').trim().slice(0,200),Vns=view();
      if(!nst){flash('공지 내용을 적어 주세요.');break;}
      if(!Vns.me||adminId(Vns)!==Vns.me||!need())break;
      editCfg(function(c){c.notice={t:nst,at:Date.now(),by:Vns.me};});
      if(canWrite()){S.draft.noticeText='';S.sync=true;flash('공지를 올렸습니다.');}
      break;
    }
    case 'notice-off':{var Vnf=view();if(!Vnf.me||adminId(Vnf)!==Vnf.me||!need())break;editCfg(function(c){delete c.notice;});if(canWrite())flash('공지를 내렸습니다.');break;}
    case 'bulk-toggle':S.bulkOpen=!S.bulkOpen;S.sync=true;break;
    case 'member-bulk':bulkAdd();break;
    case 'admin-give':{
      var Vag=view();if(!Vag.me||adminId(Vag)!==Vag.me||!Vag.byId[id]||id===Vag.me)break;
      if(prev!=='give:'+id){S.confirm='give:'+id;break;}
      if(!need())break;
      editCfg(function(c){c.admin=id;});
      if(canWrite())flash(Vag.byId[id].name+' 님에게 방장을 넘겼습니다.');
      break;
    }
    case 'rank-me':{var Vrm=view();if(Vrm.me)S.scrollTo={id:'rk-'+Vrm.me,block:'center'};break;}
    case 'fr-all':S.frAll=!S.frAll;break;
    case 'g-quick':{
      var Vgq=view(),qkey='qadd:'+date,qp=quickParse(Vgq,S.draft[qkey]);
      if(!qp||!Vgq.me||!need())break;
      if(!canAddTo(Vgq,date)){flash('이 날에는 새 할 일을 더할 수 없습니다.');break;}
      var qfull=false;
      editDay(date,function(d){if(d.goals.length>=GMAX){qfull=true;return;}d.goals.push({id:rid('g'),text:qp.text.slice(0,90),sid:qp.sid,done:false});});
      if(qfull){flash('할 일은 하루 '+GMAX+'개까지 넣을 수 있습니다.');break;}
      if(canWrite()){S.draft[qkey]='';S.sync=true;S.focusAfter='qadd-'+date;}
      break;
    }
    case 'more-open':""")
# 더보기 메뉴는 다른 동작을 하면 닫는다
sub("prev=S.confirm,before=myGrand(V0);\n  S.confirm=null;", "prev=S.confirm,before=myGrand(V0);\n  S.confirm=null;if(name!=='more-open'&&name!=='more-x')S.moreOpen=false;")
sub("S.inbox={};S.reads={};S.ib=null;", "S.inbox={};S.reads={};S.ib=null;S.bulkOpen=false;S.frAll=false;S.pruned=false;S.gdRej=false;")
