# ---------------------------------------------------------------- v33: 시간표 잠금 (이 기기 설정 gbb_ttlock)
# 잠그면 끌기, 길이 바꾸기, 빈 곳 눌러 넣기, 할 일 칩 놓기, 빈 시간에 채우기, 창에서 시간 고치기가 막힌다.
# 블록을 누르면 내용은 보이고, 할 일 끝냄 표시는 그대로 할 수 있다.
sub("function ttCommit(kind,from,id,s,e,to){\n", "function ttLocked(){return lsGet('gbb_ttlock')==='1';}\nfunction ttCommit(kind,from,id,s,e,to){\n  if(ttLocked()){S.ttPick=null;render();return;}\n")
sub("function ttFill(){\n  var V=view();if(!V.me||!need())return;", "function ttFill(){\n  var V=view();if(!V.me||ttLocked()||!need())return;")
# 칸마다 잠금 표시(c.lk). 지난 날(c.ro)과 따로: 잠가도 흐리게 하지 않는다
sub("ro:mode==='view',fx:(function(f,sc)", "ro:mode==='view',lk:mode!=='view'&&ttLocked(),fx:(function(f,sc)")
sub("if(!c.ro&&c.d>=t)fillable+=", "if(!c.ro&&!c.lk&&c.d>=t)fillable+=")
sub("""data-act="tt-pick" data-tdrag="q" data-d=""", """'+(c.lk?'aria-disabled="true" ':'data-act="tt-pick" data-tdrag="q" ')+'data-d=""")
sub("if(c.offN&&!c.ro)h+='<button class=\"ttrest\"", "if(c.offN&&!c.ro&&!c.lk)h+='<button class=\"ttrest\"")
sub("""h+='<div class="ttcol'+(c.ro?' ro':'')+(S.ttPick&&!c.ro?' picking':'')+""", """h+='<div class="ttcol'+(c.ro?' ro':'')+(c.lk?' lk':'')+(S.ttPick&&!c.ro&&!c.lk?' picking':'')+""")
sub("""'" id="tc-'+c.d+'" data-act="tt-slot" data-d="'""", """'" id="tc-'+c.d+'" '+(c.lk?'':'data-act="tt-slot" ')+'data-d="'""")
sub("dr=c.ro?'':' data-tdrag=", "dr=c.ro||c.lk?'':' data-tdrag=")
sub("(c.ro?'':'<i class=\"tbr\" aria-hidden=\"true\"></i>')", "(c.ro||c.lk?'':'<i class=\"tbr\" aria-hidden=\"true\"></i>')", 2)
sub("    case 'tt-slot':{\n      if(el.classList.contains('ro'))break;", "    case 'tt-slot':{\n      if(el.classList.contains('ro')||ttLocked())break;")

# 잠금 단추: 시간표 위 도구 줄 맨 앞
LOCK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0'+"'+(ttLocked()?'v2.5':'')+'"+'"/></svg>'
sub("""+'</div><div class="acts">'+(fillable?'<button class="btn small soft" data-act="tt-fill">빈 시간에 채우기</button>':'')""",
    """+'</div><div class="acts"><button class="btn small ttlock" data-act="tt-lock" aria-pressed="'+(ttLocked()?'true':'false')+'" aria-label="시간표 잠금">"""+LOCK_SVG+"""<span>'+(ttLocked()?'잠김':'잠금')+'</span></button>'+(fillable?'<button class="btn small soft" data-act="tt-fill">빈 시간에 채우기</button>':'')""")
sub("""  h+='<p class="hint tthint">빈 곳을 누르면 그 시간에 넣을 할 일을 고를 수 있습니다. 블록을 꾹 눌러 끌면 옮겨지고, 아래 끝을 끌면 길이가 바뀝니다.</p>';""",
    """  h+='<p class="hint tthint">'+(ttLocked()?'시간표가 잠겨 있어 끌거나 눌러도 바뀌지 않습니다. 블록을 누르면 내용만 보입니다. 고치려면 위의 잠김을 눌러 푸세요.':'빈 곳을 누르면 그 시간에 넣을 할 일을 고를 수 있습니다. 블록을 꾹 눌러 끌면 옮겨지고, 아래 끝을 끌면 길이가 바뀝니다.')+'</p>';""")
sub("    case 'tt-fill':ttFill();break;", "    case 'tt-fill':ttFill();break;\n    case 'tt-lock':{var tlk=!ttLocked();lsSet('gbb_ttlock',tlk?'1':null);S.ttPick=null;flash(tlk?'시간표를 잠갔습니다. 끌거나 눌러도 바뀌지 않습니다.':'시간표 잠금을 풀었습니다.');break;}")

# 창: 잠겨 있으면 시간 고치기와 '시간표에서 빼기'를 숨기고 안내
TTLKH = "'<p class=\"hint ttlkh\">시간표가 잠겨 있어 시간을 바꿀 수 없습니다. 시간표 위의 잠김을 누르면 풀립니다.</p>'"
sub("  if(mode!=='view'){\n    b+='<div class=\"fld\"><h3>시간</h3>'+ttTimeRow('ttg-time'", "  if(mode!=='view'&&ttLocked())b+="+TTLKH+";\n  if(mode!=='view'&&!ttLocked()){\n    b+='<div class=\"fld\"><h3>시간</h3>'+ttTimeRow('ttg-time'")
sub("(on&&mode!=='view'?'<button class=\"btn\" data-act=\"ttg-off\">", "(on&&mode!=='view'&&!ttLocked()?'<button class=\"btn\" data-act=\"ttg-off\">")
sub("ro=modeOf(d)==='view',dws=", "ro=modeOf(d)==='view'||ttLocked(),dws=")
sub("ttTimeRow('ttf-time',x.s,x.e,ro,'ttf|'+d+'|'+x.id)+'</div>';", "ttTimeRow('ttf-time',x.s,x.e,ro,'ttf|'+d+'|'+x.id)+'</div>'+(ttLocked()&&modeOf(d)!=='view'?"+TTLKH+":'');")
