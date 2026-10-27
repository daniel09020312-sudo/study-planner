# ---------------------------------------------------------------- v46: 1:1 대결 종류와 기간, 전적, 다시 붙기 (JS는 src/v46.js)
V46_JS = open(BASE + '/src/v46.js', encoding='utf-8').read()
# ---- 성능: 점수·순위 계산 캐시, 날짜 계산 캐시
sub("function addDays(s,n){var d=pd(s);d.setDate(d.getDate()+n);return fd(d);}\n", "")
sub("function buildScores(V){", "function buildScores0(V){")
sub("function standings(V,from,to){", "function standings0(V,from,to){")
sub("function chatData(V){", "function chatData0(V){")
sub("function setAt(tree,path,val){\n  var segs=String(path).split('/').filter(Boolean);\n", "function setAt(tree,path,val){\n  var segs=String(path).split('/').filter(Boolean);\n  scBump(segs[0]);\n")
sub("function commit(path,d){\n  var i=path.indexOf('/'),c=path.slice(0,i),id=path.slice(i+1);\n", "function commit(path,d){\n  var i=path.indexOf('/'),c=path.slice(0,i),id=path.slice(i+1);\n  scBump(c);\n")
sub("function fromTree(tree){\n", "function fromTree(tree){\n  scBump('d');\n")

sub("/* ---------- 공부방 ---------- */", V46_JS + "\n/* ---------- 공부방 ---------- */")
# 계산: 종류별 값, 기간은 대결마다
sub("d.end=addDays(d.start,DUEL_DAYS-1);", "d.end=addDays(d.start,duelLen(d)-1);")
sub("d.pa+=ra?ra.total:0;d.pb+=rb?rb.total:0;", "d.pa+=duelVal(d,ra);d.pb+=duelVal(d,rb);")
# 줄 보여주기
sub("님에게 신청</span><span class=\"tag\">수락 대기</span>", "님에게 신청 <small>'+esc(duelDesc(d))+'</small></span><span class=\"tag\">수락 대기</span>")
sub("+lab+'</em><span class=\"r\"><b>'+esc(B.name)+'</b></span></div>';", "+lab+'</em><span class=\"r\"><b>'+esc(B.name)+'</b></span></div><p class=\"duk\">'+esc(duelDesc(d))+'</p>';")
sub("h+='<div class=\"vs\"><span class=\"p\">'+d.pa+'</span><em>점</em><span class=\"p r\">'+d.pb+'</span></div>';",
    "h+='<div class=\"vs\"><span class=\"p\">'+esc(duelNum(d,d.pa))+'</span><em>'+esc(duelKindOf(d).name)+'</em><span class=\"p r\">'+esc(duelNum(d,d.pb))+'</span></div>';")
sub("  if(d.state==='done')h+='<p style=\"margin-top:8px\"><b>'+(d.win?esc(V.byId[d.win].name)+' 님 승리':'무승부')+'</b></p>';",
    "  if(d.state==='done'){h+='<p style=\"margin-top:8px\"><b>'+(d.win?esc(V.byId[d.win].name)+' 님 승리':'무승부')+'</b></p>';if(d.a===V.me||d.b===V.me)h+='<div class=\"row\" style=\"margin-top:8px\"><button class=\"btn small\" data-act=\"open\" data-modal=\"duel\" data-b=\"'+esc(d.a===V.me?d.b:d.a)+'\" data-kind=\"'+esc(duelKindOf(d).id)+'\" data-len=\"'+duelLen(d)+'\">다시 붙기</button></div>';}")
# 신청 창
sub("var f=S.duelF,b='<p class=\"hint\">상대가 수락한 다음 날부터 2일 동안 얻은 점수의 합으로 겨룹니다.</p><div class=\"fld\"><h3>상대</h3><div class=\"chips\">';",
    "var f=S.duelF,fk=duelKindOf({kind:f.kind}),b='<p class=\"hint\">상대가 수락한 다음 날부터 '+duelLen({days:f.len})+'일 동안, '+esc(fk.desc)+'로 겨룹니다.</p><div class=\"fld\"><h3>상대</h3><div class=\"chips\">';")
sub("  b+='</div></div>';\n  return dlg('wide',{id:'duel',t:'1:1 대결 신청'}",
    "  b+='</div></div><div class=\"fld\"><h3>종류</h3><div class=\"chips\">';\n  DUEL_KINDS.forEach(function(k){b+=chipBtn('duel-set','kind',k.id,k.name,f.kind===k.id);});\n  b+='</div></div><div class=\"fld\"><h3>기간</h3><div class=\"chips\">';\n  DUEL_LENS.forEach(function(n){b+=chipBtn('duel-set','len',String(n),n===1?'하루':n+'일',+f.len===n);});\n  b+='</div></div>';\n  return dlg('wide',{id:'duel',t:'1:1 대결 신청'}")
sub("S.duelF={b:'',stake:'roul'};", "S.duelF={b:(el&&el.getAttribute('data-b'))||'',kind:(el&&el.getAttribute('data-kind'))||'score',len:+(el&&el.getAttribute('data-len'))||DUEL_DAYS,stake:'roul'};")
sub("if(dk2==='b')S.duelF.b=S.duelF.b===dv2?'':dv2;else S.duelF.stake=dv2==='text'?'text':'roul';",
    "if(dk2==='b')S.duelF.b=S.duelF.b===dv2?'':dv2;else if(dk2==='kind'){if(DUEL_KINDS.some(function(k){return k.id===dv2;}))S.duelF.kind=dv2;}else if(dk2==='len'){if(DUEL_LENS.indexOf(+dv2)>=0)S.duelF.len=+dv2;}else S.duelF.stake=dv2==='text'?'text':'roul';")
sub("save('duels/'+did,{a:Vd.me,b:F.b,stake:stx,status:'pending',at:Date.now()});", "save('duels/'+did,{a:Vd.me,b:F.b,stake:stx,kind:F.kind||'score',days:duelLen({days:F.len}),status:'pending',at:Date.now()});")
sub("text:'1:1 대결을 신청했습니다. 도전 화면에서 수락해 주세요.'", "text:'1:1 대결을 신청했습니다('+duelDesc({kind:F.kind,days:F.len})+'). 도전 화면에서 수락해 주세요.'")
sub("text:'1:1 대결을 수락했습니다. 내일부터 2일 동안 겨룹니다.'", "text:'1:1 대결을 수락했습니다. 내일부터 '+duelLen(dd0)+'일 동안 '+duelKindOf(dd0).name+' 기준으로 겨룹니다.'")
# 도전 > 1:1 대결 화면: 안내, 내 전적, 승무패
sub("<p class=\"empty\">아직 대결이 없습니다. 한 명을 골라 2일 동안의 점수로 겨뤄보세요.</p>", "<p class=\"empty\">아직 대결이 없습니다. 한 명을 골라 점수, 공부 시간, 끝낸 할 일 중 하나로 겨뤄보세요.</p>")
sub("    h+='<div class=\"sec\"><h3>대결 전적</h3>';\n    V.roster.forEach(function(m){h+='<div class=\"brow\">'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><span></span><small>'+(wins[m.id]||0)+'승</small></div>';});",
    "    var rc=duelRecord(V,V.me);\n    h+='<div class=\"sec\"><h3>대결 전적'+(V.me?'<small>나 '+rc.w+'승 '+rc.e+'무 '+rc.l+'패</small>':'')+'</h3>';\n    V.roster.slice().sort(function(a,b){return (wins[b.id]||0)-(wins[a.id]||0);}).slice(0,12).forEach(function(m){h+='<div class=\"brow\">'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><span></span><small>'+(wins[m.id]||0)+'승</small></div>';});")
sub("</style>", ".duk{font-size:12px;color:var(--ink-3);margin:2px 0 0;text-align:center}.duel .pl small{color:var(--ink-3);margin-left:4px}</style>")

# ---- 배지: 시험까지 40일 남짓 동안 할 수 있게 다시 구성(id는 그대로). 출석 전설은 11/2~12/2 한 달 매일 출석
BADGES_NEW = r"""var BADGES=[
  {id:'att7',cat:'att',tier:'b',name:'7일 연속 출석',title:'개근',desc:'7일 연속 출석',max:7,f:function(s){return s.maxStreak;}},
  {id:'att21',cat:'att',tier:'s',name:'14일 연속 출석',title:'출석왕',desc:'14일 연속 출석',max:14,f:function(s){return s.maxStreak;}},
  {id:'att42',cat:'att',tier:'g',name:'21일 연속 출석',title:'철인',desc:'21일 연속 출석',max:21,f:function(s){return s.maxStreak;}},
  {id:'att58',cat:'att',tier:'l',name:'한 달 개근',title:'불멸의 출석',desc:'11/2부터 12/2까지 31일 매일 출석',max:31,f:function(s){return s.win;}},
  {id:'early5',cat:'att',tier:'b',name:'아침 출석 5번',title:'아침형',desc:'오전 7시 전에 출석 5번',max:5,f:function(s){return s.early;}},
  {id:'early20',cat:'att',tier:'s',name:'아침 출석 15번',title:'새벽의 학자',desc:'오전 7시 전에 출석 15번',max:15,f:function(s){return s.early;}},
  {id:'h30',cat:'time',tier:'b',name:'누적 20시간',title:'시동 걸림',desc:'누적 공부 20시간',max:1200,u:'m',f:function(s){return s.mins;}},
  {id:'h80',cat:'time',tier:'s',name:'누적 50시간',title:'꾸준함',desc:'누적 공부 50시간',max:3000,u:'m',f:function(s){return s.mins;}},
  {id:'h150',cat:'time',tier:'g',name:'누적 100시간',title:'공부 기계',desc:'누적 공부 100시간',max:6000,u:'m',f:function(s){return s.mins;}},
  {id:'h250',cat:'time',tier:'l',name:'누적 160시간',title:'전설의 끈기',desc:'누적 공부 160시간',max:9600,u:'m',f:function(s){return s.mins;}},
  {id:'d6',cat:'time',tier:'b',name:'6시간 넘은 날 4일',title:'몰입',desc:'하루 6시간 넘게 공부한 날 4일',max:4,f:function(s){return s.d6;}},
  {id:'d8',cat:'time',tier:'s',name:'8시간 넘은 날 4일',title:'몰입 장인',desc:'하루 8시간 넘게 공부한 날 4일',max:4,f:function(s){return s.d8;}},
  {id:'d10',cat:'time',tier:'g',name:'10시간 넘은 날 2일',title:'한계 돌파',desc:'하루 10시간 넘게 공부한 날 2일',max:2,f:function(s){return s.d10;}},
  {id:'d12',cat:'time',tier:'l',name:'하루 12시간',title:'시간의 지배자',desc:'하루 12시간 넘게 공부하기',max:1,f:function(s){return s.d12;}},
  {id:'bal5',cat:'time',tier:'s',name:'전 과목 3시간씩',title:'균형 잡힌',desc:'내 과목 모두 각각 3시간 넘게',max:180,u:'m',f:function(s){return s.balMin;}},
  {id:'bal15',cat:'time',tier:'g',name:'전 과목 8시간씩',title:'빈틈 없음',desc:'내 과목 모두 각각 8시간 넘게',max:480,u:'m',f:function(s){return s.balMin;}},
  {id:'clr7',cat:'plan',tier:'b',name:'모두 끝내고 인증 5일',title:'약속 지킴이',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 5일',max:5,f:function(s){return s.clrCert;}},
  {id:'clr21',cat:'plan',tier:'s',name:'모두 끝내고 인증 14일',title:'계획의 달인',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 14일',max:14,f:function(s){return s.clrCert;}},
  {id:'clr40',cat:'plan',tier:'g',name:'모두 끝내고 인증 28일',title:'완벽주의자',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 28일',max:28,f:function(s){return s.clrCert;}},
  {id:'pw1',cat:'plan',tier:'g',name:'완벽한 한 주',title:'흠잡을 데 없음',desc:'한 주 7일 모두 출석, 마감 전 인증, 할 일 3개 이상 모두 완료',max:1,f:function(s){return s.perfect;}},
  {id:'pw3',cat:'plan',tier:'l',name:'완벽한 한 주 2번',title:'무결점',desc:'완벽한 한 주를 2번',max:2,f:function(s){return s.perfect;}},
  {id:'day3',cat:'rank',tier:'b',name:'하루 1등 2번',title:'오늘의 1등',desc:'하루 순위 1등 2번',max:2,f:function(s){return s.dayWins;}},
  {id:'day10',cat:'rank',tier:'s',name:'하루 1등 6번',title:'연승 행진',desc:'하루 순위 1등 6번',max:6,f:function(s){return s.dayWins;}},
  {id:'day20',cat:'rank',tier:'g',name:'하루 1등 12번',title:'독주',desc:'하루 순위 1등 12번',max:12,f:function(s){return s.dayWins;}},
  {id:'wk1',cat:'rank',tier:'s',name:'주간 1등',title:'주간 챔피언',desc:'끝난 주에 1등 하기',max:1,f:function(s){return s.weekWins;}},
  {id:'wk3',cat:'rank',tier:'g',name:'주간 1등 2번',title:'왕좌',desc:'주간 1등 2번',max:2,f:function(s){return s.weekWins;}},
  {id:'wk5',cat:'rank',tier:'l',name:'주간 1등 3번',title:'절대 강자',desc:'주간 1등 3번',max:3,f:function(s){return s.weekWins;}},
  {id:'quiz5',cat:'board',tier:'b',name:'문제 3개',title:'출제 위원',desc:'문제 3개 올리기',max:3,f:function(s){return s.posts;}},
  {id:'quiz20',cat:'board',tier:'s',name:'문제 10개',title:'문제 은행',desc:'문제 10개 올리기',max:10,f:function(s){return s.posts;}},
  {id:'help10',cat:'board',tier:'b',name:'풀이와 답변 6개',title:'해결사',desc:'다른 사람 문제 풀이나 질문 답변 6개',max:6,f:function(s){return s.helps;}},
  {id:'help30',cat:'board',tier:'s',name:'풀이와 답변 15개',title:'모두의 과외 선생',desc:'다른 사람 문제 풀이나 질문 답변 15개',max:15,f:function(s){return s.helps;}},
  {id:'bingo5',cat:'play',tier:'b',name:'빙고 3줄',title:'빙고 장인',desc:'빙고 줄을 모두 합쳐 3개',max:3,f:function(s){return s.lines;}},
  {id:'bingo15',cat:'play',tier:'g',name:'빙고 8줄',title:'빙고 마스터',desc:'빙고 줄을 모두 합쳐 8개',max:8,f:function(s){return s.lines;}},
  {id:'duel3',cat:'play',tier:'b',name:'대결 2승',title:'승부사',desc:'1:1 대결에서 2번 이기기',max:2,f:function(s){return s.duelWins;}},
  {id:'duel10',cat:'play',tier:'g',name:'대결 5승',title:'무패의 검',desc:'1:1 대결에서 5번 이기기',max:5,f:function(s){return s.duelWins;}}
"""
cut("var BADGES=[", "];", BADGES_NEW)
sub("lines:0,duelWins:0,early:0,d6:0,", "lines:0,duelWins:0,early:0,win:0,d6:0,")
sub("    if(x.in&&new Date(x.in).getHours()<7)s.early++;\n", "    if(x.in&&new Date(x.in).getHours()<7)s.early++;\n    if(x.in&&r&&!r.cut&&d>='2026-11-02'&&d<='2026-12-02')s.win++;\n")

# ---- 찌르기 알림
sub("'</div>'+noticeSec(V)+periodSec(V)+'", "'</div>'+pokeSec()+noticeSec(V)+periodSec(V)+'")
sub("chan:x.from});});}", "chan:x.from});if(x.poke&&Date.now()-(+x.at)<10*60000)sysNotify(nm+' 님이 찔렀습니다','눌러서 답장하기','poke-'+x.from);});}")
sub("    case 'notice-x':", r"""    case 'pn-toggle':{
      if(pnOn()){lsSet('gbb_pokenote',null);pnApply();flash('찌르기 알림을 껐습니다.');break;}
      if(typeof Notification==='undefined'){flash('이 브라우저는 알림을 지원하지 않습니다. 아이폰은 홈 화면에 추가한 앱에서만 됩니다.');break;}
      try{Notification.requestPermission().then(function(pm){
        if(pm==='granted'){lsSet('gbb_pokenote','1');pnApply();flash('찌르기 알림을 켰습니다.');try{new Notification('알림을 켰습니다',{body:'찌르기가 오면 이렇게 알려 드립니다.',icon:'icon-192.png',lang:'ko'});}catch(e){}}
        else flash('알림이 허용되지 않았습니다. 브라우저 설정에서 허용해 주세요.');
        S.sync=true;render();
      });}catch(e){flash('알림을 켜지 못했습니다.');}
      break;
    }
    case 'notice-x':""")

