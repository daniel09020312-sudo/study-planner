# ---------------------------------------------------------------- 할 일 점수 바꾸기, 지난 날 할 일 지키기, 내 할 일 숨기기
# 1) 점수: NEWRULE부터 할 일 하나당 점수는 없고, 3개 이상 모두 끝내고 인증하면 크게 준다
sub("var RULE={goal:10,goalMax:5,clear:10,", "var NEWRULE='2026-10-21';\nvar RULE={allCert:50,allLate:20,goal:10,goalMax:5,clear:10,")
sub("goal:RULE.goal*Math.min(RULE.goalMax,done),clear:(g.length>=3&&done===g.length)?RULE.clear:0,",
    "goal:d<NEWRULE?RULE.goal*Math.min(RULE.goalMax,done):0,clear:d<NEWRULE?((g.length>=3&&done===g.length)?RULE.clear:0):((g.length>=3&&done===g.length&&x.certAt)?(isLate(V,d,x.certAt)?RULE.allLate:RULE.allCert):0),")
sub("  ['할 일 완료','1개당 10점, 하루 5개까지 반영'],\n  ['모두 완료','할 일을 3개 이상 세우고 전부 끝내면 10점'],",
    "  ['모두 끝내고 인증','할 일을 3개 이상 세우고 모두 끝낸 뒤 인증하면 50점, 마감 뒤에 인증하면 20점. 할 일 하나하나에는 점수가 없습니다 (10월 20일까지는 1개당 10점)'],")
sub("['출석',r.att],['할 일 완료',r.goal],['모두 완료',r.clear],", "['출석',r.att]].concat(t<NEWRULE?[['할 일 완료',r.goal],['모두 완료',r.clear]]:[['모두 끝내고 인증',r.clear]]).concat([")
sub("['문제, 풀이, 답변',r.quiz]];\n    b+='<ul class=\"brk\">'", "['문제, 풀이, 답변',r.quiz]]);\n    b+='<ul class=\"brk\">'")
sub("""    b+='<ul class="brk">'+rows.map(""", """    if(t>=NEWRULE&&!r.clear){var dd0=dayOf(V,V.me,t),gn0=dd0.goals.length,gd0=dd0.goals.filter(isDone).length;b+='<p class="hint" style="margin-bottom:10px">'+(gn0<3?'할 일을 3개 이상 세우고 모두 끝낸 뒤 인증하면 '+RULE.allCert+'점을 더 받습니다.':gd0<gn0?'할 일 '+(gn0-gd0)+'개를 마저 끝내고 인증하면 '+RULE.allCert+'점을 더 받습니다.':'할 일을 모두 끝냈습니다. 인증하면 '+RULE.allCert+'점을 더 받습니다.')+'</p>';}
    b+='<ul class="brk">'+rows.map(""")

# 인증 칸 안내
sub("(late?'마감 뒤 인증이라 3점입니다.':'마감 전 인증으로 10점을 받았습니다.')", "(late?'마감 뒤 인증이라 3점입니다.':'마감 전 인증으로 10점을 받았습니다.')+clearHint(V,date,day,late,true)")
sub("(past?'마감이 지나 지금 인증하면 3점입니다.':esc(hour)+'까지 인증하면 10점입니다.')", "(past?'마감이 지나 지금 인증하면 3점입니다.':esc(hour)+'까지 인증하면 10점입니다.')+clearHint(V,date,day,past,false)")
sub("function goalRow(V,date,mode,day,x,isT){", r"""function clearHint(V,date,day,late,certed){
  if(date<NEWRULE)return '';
  var g=day.goals,n=g.length,dn=g.filter(isDone).length,pt=late?RULE.allLate:RULE.allCert;
  if(n>=3&&dn===n)return certed?' 할 일을 모두 끝내서 '+pt+'점을 더 받았습니다.':' 할 일을 모두 끝냈으니 인증하면 '+pt+'점이 더 붙습니다.';
  if(n<3)return ' 할 일을 3개 이상 세우고 모두 끝내면 '+pt+'점을 더 받습니다.';
  return ' 할 일 '+(n-dn)+'개를 마저 끝내면 '+pt+'점을 더 받습니다.';
}
/* 지난 날의 할 일: 지우거나 이름을 바꿀 수 없고, 인증 마감 뒤에는 완료 표시도 바꿀 수 없다.
   다른 날로 옮기면 그날에는 '다른 날로 옮김'으로 남아서 모두 끝낸 날이 되지 않는다. */
function dayLocked(V,date){return date<today()&&Date.now()>certEnd(V,date).getTime();}
function guardDay(path,data){
  var m=/^days\/(.+)_(\d{4}-\d{2}-\d{2})$/.exec(path);
  if(!m||!data||typeof data!=='object'||m[2]>=today())return data;
  var V=view(),old=dayOf(V,m[1],m[2]),open=!dayLocked(V,m[2]),og=arr(old.goals),ng=arr(data.goals),byOld={},byNew={},out=[];
  og.forEach(function(g){if(g&&g.id)byOld[g.id]=g;});ng.forEach(function(g){if(g&&g.id)byNew[g.id]=g;});
  ng.forEach(function(g){
    var o=byOld[g.id];
    if(!o){if(open)out.push(g);return;}
    var c=clone(g);c.text=o.text;c.sid=o.sid||'';
    if(o.mv&&!g.mv){delete c.mv;c.done=false;}
    else if(!open)c.done=!!o.done;
    out.push(c);
  });
  og.forEach(function(o){if(o.id&&!byNew[o.id]){var c=clone(o);if(!c.done)c.mv=1;out.push(c);}});
  return Object.assign({},data,{goals:out});
}
function goalRow(V,date,mode,day,x,isT){
  if(x.mv)return '<li class="goal mv" id="g-'+esc(x.id)+'-mv"><span class="chk ghost" aria-hidden="true"><span></span></span><div class="gt">'+(x.sid&&V.subName[x.sid]&&S.gGroup!=='sub'?subTag(V,x):'')+'<span>'+esc(x.text)+'</span><em class="tag">다른 날로 옮김</em></div><span></span></li>';""")
sub("function save(path,data){\n  if(!canWrite())return;", "function save(path,data){\n  if(!canWrite())return;\n  data=guardDay(path,data);")
sub("function queueWrite(path,data){\n  if(!canWrite())return;", "function queueWrite(path,data){\n  if(!canWrite())return;\n  data=guardDay(path,data);")

# 지난 날 할 일: 수정, 삭제 단추는 빼고, 마감 뒤에는 완료 표시도 막는다
sub("""aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'?' disabled':'')+'><span></span></button>';
  if(ed)""", """aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'||dayLocked(V,date)?' disabled':'')+'><span></span></button>';
  if(ed)""")
sub("""      a+='<button class="btn small" data-act="g-edit" data-date="'+date+'" data-id="'+esc(x.id)+'">수정</button>';""",
    """      if(date>=t)a+='<button class="btn small" data-act="g-edit" data-date="'+date+'" data-id="'+esc(x.id)+'">수정</button>';""")
sub("""      a+='<button class="del" data-act="goal-del" data-date="'+date+'" data-id="'+esc(x.id)+'">'+(S.confirm==='gdel:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button>';""",
    """      if(date>=t)a+='<button class="del" data-act="goal-del" data-date="'+date+'" data-id="'+esc(x.id)+'">'+(S.confirm==='gdel:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button>';
      else a+='<span class="hint gpast">지난 날의 할 일은 지우거나 고칠 수 없습니다.</span>';""")
sub("    case 'goal-del':{if(prev!=='gdel:'+id){", "    case 'goal-del':{if(date<today()){flash('지난 날의 할 일은 지울 수 없습니다.');break;}if(prev!=='gdel:'+id){")
sub("    case 'goal-toggle':editDay(date,", "    case 'goal-toggle':if(dayLocked(view(),date)){flash('인증 마감이 지나 완료 표시를 바꿀 수 없습니다.');break;}editDay(date,")
# 주간 할 일 칸
sub("function wkItem(V,d,mode,x,t){", """function wkItem(V,d,mode,x,t){
  if(x.mv)return '<div class="wki mv" id="wi-'+esc(x.id)+'-mv" style="--sc:'+goalCol(V,x)+'"><span class="wkchk ghost" aria-hidden="true"><span></span></span><span class="wkt"><span class="t">'+esc(x.text)+'</span><small>다른 날로 옮김</small></span></div>';""")
sub("""aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'?' disabled':'')+'><span></span></button>';
  h+='<button class="wkt\"""", """aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'||dayLocked(V,d)?' disabled':'')+'><span></span></button>';
  h+='<button class="wkt\"""")
sub("if(d<t)late+=g.length-c;", "if(d<t)late+=g.filter(function(x){return !x.done&&!x.mv;}).length;")
sub("var prev=dayOf(V,V.me,addDays(date,-1)).goals.filter(function(g){return !g.done;})", "var prev=dayOf(V,V.me,addDays(date,-1)).goals.filter(function(g){return !g.done&&!g.mv;})")
sub("arr(obj(V.days[k]).goals).forEach(function(g){if(g&&g.pid)(parts[g.pid]", "arr(obj(V.days[k]).goals).forEach(function(g){if(g&&g.pid&&!g.mv)(parts[g.pid]")

# 3) 내 할 일 숨기기
sub("      if(g.length){h+='<ul class=\"fgoals\" id=\"fg-'+esc(x.p.id)+'\">';",
    "      if(g.length&&!x.p.me&&obj(V.progress[x.p.id]).hideGoals)h+='<p class=\"fgoals hint\" id=\"fg-'+esc(x.p.id)+'\">할 일을 비공개로 해 두었습니다. '+g.length+'개 중 '+done+'개를 끝냈습니다.</p>';\n      else if(g.length){h+='<ul class=\"fgoals\" id=\"fg-'+esc(x.p.id)+'\">';")
sub("""  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3>""",
    """  if(V.me){var hg=!!obj(V.progress[V.me]).hideGoals;b+='<div class="fld"><h3>내 할 일 공개<small>다른 사람이 볼 수 있는 범위</small></h3><div class="chips"><button class="chip" data-act="hide-goals" data-v="0" aria-pressed="'+(hg?'false':'true')+'">내용까지 보이기</button><button class="chip" data-act="hide-goals" data-v="1" aria-pressed="'+(hg?'true':'false')+'">개수만 보이기</button></div><p class="hint" style="margin-top:6px">'+(hg?'다른 사람에게는 할 일 개수와 끝낸 개수만 보입니다.':'참여 인원 목록에서 내 할 일 내용이 보입니다.')+'</p></div>';}
  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3>""")
sub("    case 'pick-date':", "    case 'hide-goals':{var hgv=el.getAttribute('data-v')==='1';editProg(function(p){if(hgv)p.hideGoals=true;else delete p.hideGoals;});break;}\n    case 'pick-date':")
