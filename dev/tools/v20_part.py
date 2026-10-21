# ---------------------------------------------------------------- 배지 늘리기(등급, 점수), 주간 우승 점수, 최종 결과, 선물과 벌칙 룰렛
AWARD_JS = open(BASE + '/src/award.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", AWARD_JS + "\n/* ---------- 공부방 ---------- */")

cut("var BADGES=[", "function prog(c,v){", r"""var BADGES=[
  {id:'att7',cat:'att',tier:'b',name:'7일 연속 출석',title:'개근',desc:'7일 연속 출석',max:7,f:function(s){return s.maxStreak;}},
  {id:'att21',cat:'att',tier:'s',name:'21일 연속 출석',title:'출석왕',desc:'21일 연속 출석',max:21,f:function(s){return s.maxStreak;}},
  {id:'att42',cat:'att',tier:'g',name:'42일 연속 출석',title:'철인',desc:'42일 연속 출석',max:42,f:function(s){return s.maxStreak;}},
  {id:'att58',cat:'att',tier:'l',name:'하루도 빠짐없이',title:'불멸의 출석',desc:'10/12부터 12/8까지 매일 출석',max:58,f:function(s){return s.maxStreak;}},
  {id:'early5',cat:'att',tier:'b',name:'아침 출석 5번',title:'아침형',desc:'오전 7시 전에 출석 5번',max:5,f:function(s){return s.early;}},
  {id:'early20',cat:'att',tier:'s',name:'아침 출석 20번',title:'새벽의 학자',desc:'오전 7시 전에 출석 20번',max:20,f:function(s){return s.early;}},
  {id:'h30',cat:'time',tier:'b',name:'누적 30시간',title:'시동 걸림',desc:'누적 공부 30시간',max:1800,u:'m',f:function(s){return s.mins;}},
  {id:'h80',cat:'time',tier:'s',name:'누적 80시간',title:'꾸준함',desc:'누적 공부 80시간',max:4800,u:'m',f:function(s){return s.mins;}},
  {id:'h150',cat:'time',tier:'g',name:'누적 150시간',title:'공부 기계',desc:'누적 공부 150시간',max:9000,u:'m',f:function(s){return s.mins;}},
  {id:'h250',cat:'time',tier:'l',name:'누적 250시간',title:'전설의 끈기',desc:'누적 공부 250시간',max:15000,u:'m',f:function(s){return s.mins;}},
  {id:'d6',cat:'time',tier:'b',name:'6시간 넘은 날 5일',title:'몰입',desc:'하루 6시간 넘게 공부한 날 5일',max:5,f:function(s){return s.d6;}},
  {id:'d8',cat:'time',tier:'s',name:'8시간 넘은 날 7일',title:'몰입 장인',desc:'하루 8시간 넘게 공부한 날 7일',max:7,f:function(s){return s.d8;}},
  {id:'d10',cat:'time',tier:'g',name:'10시간 넘은 날 3일',title:'한계 돌파',desc:'하루 10시간 넘게 공부한 날 3일',max:3,f:function(s){return s.d10;}},
  {id:'d12',cat:'time',tier:'l',name:'하루 12시간',title:'시간의 지배자',desc:'하루 12시간 넘게 공부하기',max:1,f:function(s){return s.d12;}},
  {id:'bal5',cat:'time',tier:'s',name:'전 과목 5시간씩',title:'균형 잡힌',desc:'내 과목 모두 각각 5시간 넘게',max:300,u:'m',f:function(s){return s.balMin;}},
  {id:'bal15',cat:'time',tier:'g',name:'전 과목 15시간씩',title:'빈틈 없음',desc:'내 과목 모두 각각 15시간 넘게',max:900,u:'m',f:function(s){return s.balMin;}},
  {id:'clr7',cat:'plan',tier:'b',name:'모두 끝내고 인증 7일',title:'약속 지킴이',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 7일',max:7,f:function(s){return s.clrCert;}},
  {id:'clr21',cat:'plan',tier:'s',name:'모두 끝내고 인증 21일',title:'계획의 달인',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 21일',max:21,f:function(s){return s.clrCert;}},
  {id:'clr40',cat:'plan',tier:'g',name:'모두 끝내고 인증 40일',title:'완벽주의자',desc:'할 일 3개 이상을 모두 끝내고 인증한 날 40일',max:40,f:function(s){return s.clrCert;}},
  {id:'pw1',cat:'plan',tier:'g',name:'완벽한 한 주',title:'흠잡을 데 없음',desc:'한 주 7일 모두 출석, 마감 전 인증, 할 일 3개 이상 모두 완료',max:1,f:function(s){return s.perfect;}},
  {id:'pw3',cat:'plan',tier:'l',name:'완벽한 한 주 3번',title:'무결점',desc:'완벽한 한 주를 3번',max:3,f:function(s){return s.perfect;}},
  {id:'day3',cat:'rank',tier:'b',name:'하루 1등 3번',title:'오늘의 1등',desc:'하루 순위 1등 3번',max:3,f:function(s){return s.dayWins;}},
  {id:'day10',cat:'rank',tier:'s',name:'하루 1등 10번',title:'연승 행진',desc:'하루 순위 1등 10번',max:10,f:function(s){return s.dayWins;}},
  {id:'day20',cat:'rank',tier:'g',name:'하루 1등 20번',title:'독주',desc:'하루 순위 1등 20번',max:20,f:function(s){return s.dayWins;}},
  {id:'wk1',cat:'rank',tier:'s',name:'주간 1등',title:'주간 챔피언',desc:'끝난 주에 1등 하기',max:1,f:function(s){return s.weekWins;}},
  {id:'wk3',cat:'rank',tier:'g',name:'주간 1등 3번',title:'왕좌',desc:'주간 1등 3번',max:3,f:function(s){return s.weekWins;}},
  {id:'wk5',cat:'rank',tier:'l',name:'주간 1등 5번',title:'절대 강자',desc:'주간 1등 5번',max:5,f:function(s){return s.weekWins;}},
  {id:'quiz5',cat:'board',tier:'b',name:'문제 5개',title:'출제 위원',desc:'문제 5개 올리기',max:5,f:function(s){return s.posts;}},
  {id:'quiz20',cat:'board',tier:'s',name:'문제 20개',title:'문제 은행',desc:'문제 20개 올리기',max:20,f:function(s){return s.posts;}},
  {id:'help10',cat:'board',tier:'b',name:'풀이와 답변 10개',title:'해결사',desc:'다른 사람 문제 풀이나 질문 답변 10개',max:10,f:function(s){return s.helps;}},
  {id:'help30',cat:'board',tier:'s',name:'풀이와 답변 30개',title:'모두의 과외 선생',desc:'다른 사람 문제 풀이나 질문 답변 30개',max:30,f:function(s){return s.helps;}},
  {id:'lapse3',cat:'board',tier:'b',name:'타임랩스 3개',title:'기록하는 사람',desc:'공부 타임랩스 3개 올리기',max:3,f:function(s){return s.lapses;}},
  {id:'lapse10',cat:'board',tier:'s',name:'타임랩스 10개',title:'공부 브이로거',desc:'공부 타임랩스 10개 올리기',max:10,f:function(s){return s.lapses;}},
  {id:'bingo5',cat:'play',tier:'b',name:'빙고 5줄',title:'빙고 장인',desc:'빙고 줄을 모두 합쳐 5개',max:5,f:function(s){return s.lines;}},
  {id:'bingo15',cat:'play',tier:'g',name:'빙고 15줄',title:'빙고 마스터',desc:'빙고 줄을 모두 합쳐 15개',max:15,f:function(s){return s.lines;}},
  {id:'duel3',cat:'play',tier:'b',name:'대결 3승',title:'승부사',desc:'1:1 대결에서 3번 이기기',max:3,f:function(s){return s.duelWins;}},
  {id:'duel10',cat:'play',tier:'g',name:'대결 10승',title:'무패의 검',desc:'1:1 대결에서 10번 이기기',max:10,f:function(s){return s.duelWins;}}
];
""")

cut("function memberStats(V,mid){", "function titleOf(V,mid){", r"""function memberStats(V,mid){
  V._ms=V._ms||{};if(V._ms[mid])return V._ms[mid];
  var t=today(),last=t<END?t:END,rows=V.sc[mid]||{},skip=obj(obj(V.progress[mid]).skip),subj={},k;
  var s={maxStreak:0,mins:0,clear:0,clrCert:0,dayWins:0,weekWins:0,posts:0,helps:0,lines:0,duelWins:0,early:0,d6:0,d8:0,d10:0,d12:0,perfect:0,lapses:0,balMin:0};
  for(var d=START;d<=last;d=addDays(d,1)){
    var x=dayOf(V,mid,d),r=rows[d],g=x.goals,dm=sumMins(x.mins)+sumMins(x.manual),all=g.length>=3&&g.filter(isDone).length===g.length;
    s.mins+=dm;for(k in x.mins)subj[k]=(subj[k]||0)+(+x.mins[k]||0);for(k in x.manual)subj[k]=(subj[k]||0)+(+x.manual[k]||0);
    if(all)s.clear++;if(all&&x.certAt)s.clrCert++;
    if(dm>=360)s.d6++;if(dm>=480)s.d8++;if(dm>=600)s.d10++;if(dm>=720)s.d12++;
    if(r){if(r.streak>s.maxStreak)s.maxStreak=r.streak;if(r.place===1)s.dayWins++;}
    if(x.in&&new Date(x.in).getHours()<7)s.early++;
  }
  for(var w=START;w<=last;w=addDays(w,7)){
    s.lines+=bingo(V,w).per[mid].lines;
    var we=addDays(w,6);
    if(we<t){
      var st=standings(V,w,we);if(st.length>1&&st[0].total>0&&st[0].p.id===mid)s.weekWins++;
      if(we<=END){var ok=true;for(var dd=w;dd<=we;dd=addDays(dd,1)){var y=dayOf(V,mid,dd),gg=y.goals;if(!(y.in&&y.certAt&&!isLate(V,dd,y.certAt)&&gg.length>=3&&gg.filter(isDone).length===gg.length)){ok=false;break;}}if(ok)s.perfect++;}
    }
  }
  s.posts=V.posts.filter(function(q){return q.mid===mid&&q.kind!=='ask'&&q.kind!=='lapse';}).length;
  s.lapses=V.posts.filter(function(q){return q.mid===mid&&q.kind==='lapse';}).length;
  s.helps=helpIds(V,mid,function(ts){return ts>1e11;});
  duelList(V).forEach(function(du){if(du.state==='done'&&du.win===mid)s.duelWins++;});
  var mys=V.subs.filter(function(x){return !skip[x.id];});
  s.balMin=mys.length?Math.min.apply(null,mys.map(function(x){return subj[x.id]||0;})):0;
  return V._ms[mid]=s;
}
function badgeList(V,mid){
  V._bl=V._bl||{};if(V._bl[mid])return V._bl[mid];
  var s=memberStats(V,mid);
  return V._bl[mid]=BADGES.map(function(b){var v=Math.max(0,+b.f(s)||0),tr=TIERS[b.tier];return {id:b.id,name:b.name,title:b.title,desc:b.desc,on:v>=b.max,v:v,max:b.max,u:b.u,tier:b.tier,tname:tr[0],pts:tr[1],cat:b.cat};});
}
""")
sub("function titleTag(V,mid){var t=titleOf(V,mid);return t?'<em class=\"tag\">'+esc(t)+'</em>':'';}",
    "function titleTag(V,mid){var id=obj(V.progress[mid]).title;if(!id)return '';var b=badgeList(V,mid).filter(function(x){return x.id===id&&x.on;})[0];return b?'<em class=\"tag tt-'+b.tier+'\">'+esc(b.title)+'</em>':'';}")
sub("  var l=arr(V.cfg.penalties).map(function(x){return String(x||'').trim();}).filter(Boolean);", "  var l=penItems(V).map(function(x){return x.t;});")
# 새 배지 알림: 배지 목록이 바뀐 첫날에는 한꺼번에 알리지 않는다
sub("  if(pb&&pb.me===V.me&&Array.isArray(pb.ids))earned.forEach(function(b){if(pb.ids.indexOf(b.id)<0)addNote({id:'bd'+b.id,key:'bd'+b.id,title:'새 배지: '+b.name,sub:'도전 화면에서 칭호로 쓸 수 있습니다',tab:'play'});});\n  var nb=JSON.stringify({me:V.me,ids:earned.map(function(b){return b.id;})});",
    "  if(pb&&pb.v===2&&pb.me===V.me&&Array.isArray(pb.ids))earned.forEach(function(b){if(pb.ids.indexOf(b.id)<0)addNote({id:'bd'+b.id,key:'bd'+b.id,title:'새 배지: '+b.name+' ('+b.tname+')',sub:'최종 점수에 '+b.pts+'점이 더해집니다. 칭호: '+b.title,tab:'play'});});\n  var nb=JSON.stringify({v:2,me:V.me,ids:earned.map(function(b){return b.id;})});")

# 도전 > 배지 화면
cut("    var bl=badgeList(V,V.me),mt=obj(V.progress[V.me]).title,got=bl.filter(function(b){return b.on;}).length;", "  return h+'</div></div>';\n}\nfunction wheelSvg", "    h+=badgeView(V);\n  }\n")
sub("badge:'기록이 쌓이면 배지를 받고, 받은 배지의 칭호를 이름 옆에 붙일 수 있습니다.'", "badge:'기록이 쌓이면 배지를 받습니다. 등급이 높을수록 어렵고, 받은 배지는 최종 점수에 더해집니다.'")

# 순위 > 최종
sub("  var st=standings(V,from,to),max=st.length?st[0].total:0,any=st.some(function(x){return x.total>0;});",
    "  if(S.range==='all')return h+finalBody(V)+'</div></div></div>';\n  var st=standings(V,from,to),max=st.length?st[0].total:0,any=st.some(function(x){return x.total>0;});")
sub("[['this','이번 주'],['last','지난주'],['all','최종']]", "[['this','이번 주'],['last','지난주'],['all','최종 결과']]")
sub("'+(x.p.me?'<span class=\"tag a\">나</span>':'')+titleTag(V,x.p.id)+'</div>';\n    h+='<div class=\"bar\">",
    "'+(x.p.me?'<span class=\"tag a\">나</span>':'')+titleTag(V,x.p.id)+(S.range==='last'&&i<3&&x.total>0&&st.length>1?'<span class=\"tag wb\">주간 '+(i+1)+'등 +'+WEEK_BONUS[i]+'</span>':'')+'</div>';\n    h+='<div class=\"bar\">")
sub("  ['스터디 빙고','한 줄을 채울 때마다 10점. 주간 점수와 최종 점수에 더함']",
    "  ['스터디 빙고','한 줄을 채울 때마다 10점. 주간 점수와 최종 점수에 더함'],\n  ['주간 순위','한 주가 끝나면 1등 100점, 2등 60점, 3등 30점을 최종 점수에 더함'],\n  ['배지','받은 배지마다 동 10점, 은 30점, 금 60점, 전설 100점을 최종 점수에 더함'],\n  ['최종 결과','2차 시험이 끝난 다음 날 공개. 1등은 선물, 꼴찌는 모두가 낸 벌칙 후보 중 룰렛으로 뽑은 벌칙']")

# 동작
sub("    case 'pick-date':", r"""    case 'prize-save':{var pzt=String(S.draft.prizeText||'').trim().slice(0,40),Vz=view();if(!pzt||!Vz.me||finalOpen())break;editCfg(function(c){c.prize={t:pzt,by:Vz.me};});if(canWrite()){S.draft.prizeText='';S.sync=true;flash('1등 선물을 정했습니다.');}break;}
    case 'pen2-add':{
      var p2t=String(S.draft.penText||'').trim().slice(0,40),Vp=view();if(!p2t||!Vp.me||finalOpen())break;
      var its2=penItems(Vp);if(its2.length>=12){flash('벌칙 후보는 12개까지 적을 수 있습니다.');break;}
      if(its2.filter(function(x){return x.by===Vp.me;}).length>=2){flash('벌칙 후보는 한 사람당 2개까지 적을 수 있습니다.');break;}
      editCfg(function(c){c.penalties=arr(c.penalties).concat([{t:p2t,by:Vp.me}]);});
      if(canWrite()){S.draft.penText='';S.sync=true;}break;
    }
    case 'pen2-del':{
      var pi2=+el.getAttribute('data-i'),Vq=view();if(finalOpen())break;
      var it2=penItems(Vq).filter(function(x){return x.i===pi2;})[0];if(!it2)break;
      if(it2.by&&it2.by!==Vq.me&&adminId(Vq)!==Vq.me)break;
      if(prev!=='pen2:'+pi2){S.confirm='pen2:'+pi2;break;}
      editCfg(function(c){var l=arr(c.penalties);l.splice(pi2,1);c.penalties=l;c.penalty='';});break;
    }
    case 'pick-date':""")
