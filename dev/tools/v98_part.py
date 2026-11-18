# ---------------------------------------------------------------- v98: 히든 칭호 '인간 아님'(하루 18시간). 받기 전에는 배지 목록에 안 보이고 점수는 없음 (src/v98.js, v98.css)
V98_JS = open(BASE + '/src/v98.js', encoding='utf-8').read()
V98_CSS = open(BASE + '/src/v98.css', encoding='utf-8').read()
sub("var TIERS={b:['동',10],s:['은',30],g:['금',60],l:['전설',100]};", "var TIERS={b:['동',10],s:['은',30],g:['금',60],l:['전설',100],h:['히든',0]};")
sub("  {id:'d12',cat:'time',tier:'l',name:'하루 12시간',title:'시간의 지배자',desc:'하루 12시간 넘게 공부하기',max:1,f:function(s){return s.d12;}},",
    "  {id:'d12',cat:'time',tier:'l',name:'하루 12시간',title:'시간의 지배자',desc:'하루 12시간 넘게 공부하기',max:1,f:function(s){return s.d12;}},\n  {id:'d18',cat:'time',tier:'h',hid:1,name:'하루 18시간',title:'인간 아님',desc:'하루 18시간 넘게 공부하기',max:1,f:function(s){return s.d18;}},")
sub("early:0,win:0,d6:0,d8:0,d10:0,d12:0,", "early:0,win:0,d6:0,d8:0,d10:0,d12:0,d18:0,")
sub("if(dm>=720)s.d12++;", "if(dm>=720)s.d12++;if(dm>=1080)s.d18++;")
# 숨은 배지는 받은 사람에게만 목록에 들어감
sub("  return V._bl[mid]=BADGES.map(function(b){", "  return V._bl[mid]=BADGES.filter(function(b){return !b.hid||(Math.max(0,+b.f(s)||0)>=b.max);}).map(function(b){")
sub("/* ---------- 공부방 ---------- */", V98_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V98_CSS + "</style>")
sub("  if(t==='egg7')return modalEgg(V);", "  if(t==='egg7')return modalEgg(V);\n  if(t==='h18')return modalH18(V);")
sub("    case 'egg-x':eggClose();break;", "    case 'egg-x':eggClose();break;\n    case 'h18-x':h18Close(false);break;\n    case 'h18-use':h18Close(true);flash('칭호 \\'인간 아님\\'를 달았습니다.');break;")
# 히든 칭호는 따로 창으로 알리므로 '새 배지' 알림은 하지 않음
sub("earned.forEach(function(b){if(pb.ids.indexOf(b.id)<0)addNote(", "earned.forEach(function(b){if(b.tier!=='h'&&pb.ids.indexOf(b.id)<0)addNote(")
