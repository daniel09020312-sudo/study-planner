# ---------------------------------------------------------------- 일정: 학교 행사·시험과 수행평가 따로 보기
EV_JS = open(BASE + '/src/evview.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", EV_JS + "\n/* ---------- 공부방 ---------- */")

# 일정 종류에 시험, 행사를 더하고, 종류와 과목도 저장한다
sub("var EV_KINDS=['수행평가','발표','제출','퀴즈','기타'];", "var EV_KINDS=['수행평가','발표','제출','퀴즈','시험','행사','기타'];")
sub("  if(e.kind&&e.kind!=='기타')parts.push(e.kind);", "  if(e.kind&&e.kind!=='기타'&&!((e.kind==='행사'||e.kind==='시험')&&note&&!parts.length))parts.push(e.kind);")
sub("save('events/'+rid('e'),{mid:Ve.me,date:S.evd.date,title:title.slice(0,60),shared:!!S.evd.shared});",
    "save('events/'+rid('e'),{mid:Ve.me,date:S.evd.date,title:title.slice(0,60),shared:!!S.evd.shared,kind:String(S.evd.kind||''),sid:String(S.evd.sid||'')});")
sub("(V.evByDate[e.date]=V.evByDate[e.date]||[]).push({id:id,title:String(e.title),mid:e.mid,shared:!!e.shared,date:e.date});",
    "(V.evByDate[e.date]=V.evByDate[e.date]||[]).push({id:id,title:String(e.title),mid:e.mid,shared:!!e.shared,date:e.date,kind:String(e.kind||''),sid:String(e.sid||''),grp:evGroupOf(e)});")

# 일정 추가 창: 날짜 고르기
sub("""  var e=S.evd,title=evTitle(V),b='<p class="hint">'+esc(longDate(e.date))+'에 추가합니다. 수행평가처럼 사람마다 다른 일정은 내 달력에만 보입니다.</p>';""",
    """  var e=S.evd,title=evTitle(V),b='<p class="hint">'+esc(longDate(e.date))+'에 추가합니다. 수행평가처럼 사람마다 다른 일정은 내 달력에만 보입니다.</p>';
  if(e.pickDate)b+='<div class="fld"><h3>날짜</h3><input type="date" class="evdate" value="'+esc(e.date)+'" data-chg="ev-date" aria-label="일정 날짜"></div>';""")
sub("  else if(kind==='g-copy'){", "  else if(kind==='ev-date'){if(S.evd&&/^\\d{4}-\\d{2}-\\d{2}$/.test(v))S.evd.date=v;}\n  else if(kind==='g-copy'){")

# 달력 보기 방식에 '일정' 더하기
sub("var CMODES=[['cal','달력'],['list','할 일'],['tt','시간표']];", "var CMODES=[['cal','달력'],['list','할 일'],['tt','시간표'],['ev','일정']];")
sub("S.calMode=(function(m){return m==='list'||m==='tt'?m:'cal';})(lsGet('gbb_calmode'));", "S.calMode=(function(m){return m==='list'||m==='tt'||m==='ev'?m:'cal';})(lsGet('gbb_calmode'));S.evPast=false;S.upF='all';")
sub("    case 'cal-mode':setCalMode(id==='list'||id==='tt'?id:'cal');break;", "    case 'cal-mode':setCalMode(id==='list'||id==='tt'||id==='ev'?id:'cal');break;")
sub("  if(S.calMode==='tt')return viewTT(V);", "  if(S.calMode==='tt')return viewTT(V);\n  if(S.calMode==='ev')return viewEvents(V);")

# 달력의 '다가오는 일정'에 종류 나눠 보기
sub("""  Object.keys(EVENTS).forEach(function(d){if(d>=t)up.push({d:d,title:EVENTS[d].l});});
  Object.keys(V.evByDate).forEach(function(d){if(d>=t)V.evByDate[d].forEach(function(e){up.push({d:d,title:e.title,mine:1});});});""",
    """  Object.keys(EVENTS).forEach(function(d){if(d>=t)up.push({d:d,title:EVENTS[d].l,g:'exam'});});
  Object.keys(V.evByDate).forEach(function(d){if(d>=t)V.evByDate[d].forEach(function(e){up.push({d:d,title:e.title,mine:1,g:e.grp,sid:e.sid});});});""")
sub("""up.push({d:d,title:'마감 · '+p.label,mine:1});""", """up.push({d:d,title:'마감 · '+p.label,mine:1,g:'due'});""")
sub("""  h+='<div class="col upcol">'+plansCard(V,2)+'<section class="card upcard" id="c-up" style="--k:3"><div class="ct"><h2>다가오는 일정</h2></div>';
  if(!up.length)h+='<p class="empty">남은 일정이 없습니다.</p>';
  up.slice(0,6).forEach(function(u){h+='<button class="uprow" data-act="pick-date" data-d="'+u.d+'">""",
    """  var upF=S.upF==='exam'||S.upF==='task'?S.upF:'all';up=up.filter(function(u){return upF==='all'||u.g===upF;});
  h+='<div class="col upcol">'+plansCard(V,2)+'<section class="card upcard" id="c-up" style="--k:3"><div class="ct"><h2>다가오는 일정</h2><div class="seg mini upf" role="group" aria-label="일정 종류">'+[['all','전체'],['exam','행사·시험'],['task','수행평가']].map(function(x){return '<button data-act="up-f" data-id="'+x[0]+'" aria-pressed="'+(upF===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div></div>';
  if(!up.length)h+='<p class="empty">'+(upF==='task'?'남은 수행평가가 없습니다.':upF==='exam'?'남은 행사나 시험이 없습니다.':'남은 일정이 없습니다.')+'</p>';
  up.slice(0,6).forEach(function(u){h+='<button class="uprow g-'+(u.g||'exam')+'" style="--sc:'+(u.g==='task'?evSubCol(V,u):u.g==='due'?SGRAY:'var(--accent)')+'" data-act="pick-date" data-d="'+u.d+'">""")
sub("""+DOW[pd(u.d).getDay()]+'</small></button>';});
  return h+'</section></div></div></div>';
}""", """+DOW[pd(u.d).getDay()]+'</small></button>';});
  if(up.length>6)h+='<button class="btn small upall" data-act="cal-mode" data-id="ev">일정 모두 보기</button>';
  return h+'</section></div></div></div>';
}""")

# 동작
sub("    case 'pick-date':", r"""    case 'up-f':S.upF=id;break;
    case 'ev-past':S.evPast=!S.evPast;S.vbDir=S.evPast?-1:1;break;
    case 'ev-new':{openModal('event',el);if(S.evd){S.evd.kind=el.getAttribute('data-k')||'수행평가';S.evd.pickDate=true;if(S.evd.date<today())S.evd.date=today();}render();return;}
    case 'pick-date':""")
