# ---------------------------------------------------------------- v93: 스터디 빙고는 BINGO_NEW(2026-11-16 주)부터 새 칸 묶음 BINGO_POOL2에서 주마다 다르게 9칸(갈래 c마다 BINGO_CAP까지). 7일 매일 해야 하는 칸은 없음. 그 전 주는 예전 BINGO_POOL 그대로
sub("function bingoCells(mon){", r"""var BINGO_NEW='2026-11-16';
var BINGO_CAP={time:4,plan:3,day:2,board:2};
var BINGO_POOL2=[
  {g:'mins',c:'time',t:'이번 주 공부 35시간',max:2100,u:'m',f:function(o){return o.mins;}},
  {g:'mins',c:'time',t:'이번 주 공부 28시간',max:1680,u:'m',f:function(o){return o.mins;}},
  {c:'time',t:'7시간 넘게 공부한 날 3일',max:3,f:function(o){return o.daily.filter(function(x){return x>=420;}).length;}},
  {c:'time',t:'5시간 넘게 공부한 날 5일',max:5,f:function(o){return o.daily.filter(function(x){return x>=300;}).length;}},
  {c:'time',t:'4시간 넘게 공부한 날 6일',max:6,f:function(o){return o.daily.filter(function(x){return x>=240;}).length;}},
  {c:'time',t:'한 과목 10시간',max:600,u:'m',f:function(o){var m=0;for(var k in o.subj)m=Math.max(m,o.subj[k]);return m;}},
  {g:'subn',c:'time',t:'과목 5개를 3시간씩',max:5,f:function(o){var n=0;for(var k in o.subj)if(o.subj[k]>=180)n++;return n;}},
  {g:'subn',c:'time',t:'과목 7개를 2시간씩',max:7,f:function(o){var n=0;for(var k in o.subj)if(o.subj[k]>=120)n++;return n;}},
  {c:'time',t:'타이머로만 25시간',max:1500,u:'m',f:function(o){return o.tmins;}},
  {c:'time',t:'주말에 14시간 공부',max:840,u:'m',f:function(o){return (o.daily[5]||0)+(o.daily[6]||0);}},
  {c:'time',t:'월·화·수 합쳐 16시간',max:960,u:'m',f:function(o){return (o.daily[0]||0)+(o.daily[1]||0)+(o.daily[2]||0);}},
  {c:'time',t:'목·금 합쳐 11시간',max:660,u:'m',f:function(o){return (o.daily[3]||0)+(o.daily[4]||0);}},
  {g:'done',c:'plan',t:'할 일 40개 완료',max:40,f:function(o){return o.done;}},
  {g:'done',c:'plan',t:'할 일 30개 완료',max:30,f:function(o){return o.done;}},
  {c:'plan',t:'할 일을 모두 끝낸 날 5일',max:5,f:function(o){var n=0;o.dn.forEach(function(x,i){if(x>=3&&o.ddone[i]===x)n++;});return n;}},
  {c:'plan',t:'할 일 6개 넘게 끝낸 날 5일',max:5,f:function(o){return o.ddone.filter(function(x){return x>=6;}).length;}},
  {c:'plan',t:'하루에 할 일 12개 끝낸 날 2일',max:2,f:function(o){return o.ddone.filter(function(x){return x>=12;}).length;}},
  {c:'day',t:'출석 6일',max:6,f:function(o){return o.att;}},
  {c:'day',t:'인증 6일',max:6,f:function(o){return o.cert;}},
  {c:'day',t:'아침 7시 전 출석 3번',max:3,f:function(o){return o.early7;}},
  {g:'dpts',c:'day',t:'100점 넘긴 날 5일',max:5,f:function(o){return o.dpts.filter(function(x){return x>=100;}).length;}},
  {g:'dpts',c:'day',t:'150점 넘긴 날 3일',max:3,f:function(o){return o.dpts.filter(function(x){return x>=150;}).length;}},
  {c:'day',t:'하루 순위 1등 2번',max:2,f:function(o){return o.wins;}},
  {c:'board',t:'문제 5개 내기',max:5,f:function(o){return o.posts;}},
  {c:'board',t:'풀이나 답변 7개',max:7,f:function(o){return o.helps;}},
  {c:'board',t:'노동요 2곡 올리기',max:2,f:function(o){return o.songs;}}
];
function bingoCells(mon){
  if(mon<BINGO_NEW)return bingoCells0(mon);
  var seed=(weekNo(mon)*7919+104729)%233280,idx=BINGO_POOL2.map(function(x,i){return i;}),i,j,t,cnt={},out=[];
  for(i=idx.length-1;i>0;i--){seed=(seed*9301+49297)%233280;j=Math.floor(seed/233280*(i+1));t=idx[i];idx[i]=idx[j];idx[j]=t;}
  var ug={};idx.forEach(function(k){var c=BINGO_POOL2[k];if(out.length>=9||(cnt[c.c]||0)>=(BINGO_CAP[c.c]||9)||(c.g&&ug[c.g]))return;cnt[c.c]=(cnt[c.c]||0)+1;if(c.g)ug[c.g]=1;out.push(c);});
  return out;
}
function bingoCells0(mon){""")
sub("o.tmins=0;o.wins=0;Wk.days.forEach(function(d){o.tmins+=sumMins(dayOf(V,m.id,d).mins);", "o.tmins=0;o.wins=0;o.early8=0;o.early7=0;Wk.days.forEach(function(d){var dx=dayOf(V,m.id,d);if(dx.in&&new Date(dx.in).getHours()<8)o.early8++;if(dx.in&&new Date(dx.in).getHours()<7)o.early7++;o.tmins+=sumMins(dx.mins);")
