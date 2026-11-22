/* ---------- v105: 병맛 히든. 엉뚱한 조건으로 열리는 이상한 꾸미기 ---------- */
function bmStats(V){
  var g=gcSync(V),k='bm';if(g[k])return g[k];
  var o={z0:0,lateIn:0,plan30:0,zeroDone:0,m71:0,lateCert:0,songs:0,amolla:0,t444:0,kkk:0,hate:0},t=today(),last=t<END?t:END;
  for(var d=TALLY;d<=last;d=addDays(d,1)){
    var x=dayOf(V,V.me,d),m=sumMins(x.mins)+sumMins(x.manual),gl=x.goals.filter(function(q){return q&&!q.mv;});
    if(x.in&&m===0&&d<t)o.z0++;
    if(x.in){var dt=new Date(x.in),h=dt.getHours();if(h>=23||h<DAY_H)o.lateIn++;if((h===16||h===4)&&dt.getMinutes()===44)o.t444++;}
    if(x.goals.length>=30)o.plan30++;
    if(d<t&&gl.length>=3&&gl.filter(isDone).length===0)o.zeroDone++;
    if(m===71)o.m71++;
    if(x.certAt&&isLate(V,d,x.certAt))o.lateCert++;
    x.goals.forEach(function(q){var s=String(q&&q.text||'').replace(/\s/g,'');if(s.indexOf('아몰라')>=0)o.amolla++;if(s.indexOf('공부하기싫다')>=0)o.hate++;});
  }
  for(var id in V.songs){var so=obj(V.songs[id]);if(so.mid===V.me){o.songs++;if((String(so.title||'').match(/ㅋ/g)||[]).length>=3)o.kkk++;}}
  return g[k]=o;
}
function bmOk(f){return function(s,V){return f(bmStats(V));};}
[
  ['r','googly','눈알',44,'할 일 이름에 \'아 몰라\' 적기',bmOk(function(b){return b.amolla>=1;})],
  ['r','stache','콧수염',44,'딱 4시 44분에 출석하기',bmOk(function(b){return b.t444>=1;})],
  ['r','tornado','회오리',66,'하루에 할 일 30개 넘게 적기',bmOk(function(b){return b.plan30>=1;})],
  ['r','flame','불타는 머리',66,'출석만 하고 공부 0분인 날 3번',bmOk(function(b){return b.z0>=3;})],
  ['r','zzz','쿨쿨',33,'밤 11시 넘어서 출석 3번',bmOk(function(b){return b.lateIn>=3;})],
  ['g','alien','외계어',33,'할 일 3개 이상 적고 하나도 안 끝낸 날 3번',bmOk(function(b){return b.zeroDone>=3;})],
  ['g','blink','90년대 깜빡이',33,'노동요 제목에 ㅋ 3개 넘게 넣어 올리기',bmOk(function(b){return b.kkk>=1;})],
  ['g','huge','왕 큰 칭호',55,'밤 11시 넘어서 출석 3번',bmOk(function(b){return b.lateIn>=3;})]
].forEach(function(x){DECO_ITEMS.push({id:x[0]+':'+x[1],v:x[1],cat:x[0]==='r'?'ring':'ttag',name:x[2],price:x[3],desc:'히든',hid:x[4],cond:x[5],bm:1});});
CONCEPTS.push({id:'mini02',name:'2002년 미니홈피',mode:'light',soft:[.3,'#D8ECFF'],font:'Gaegu:wght@700',face:'Gaegu',w:700,hid:1},{id:'glitch',name:'고장난 화면',mode:'dark',soft:[.2,'#1A0F24'],hid:1});
TVAR.drunk='digits';TVAR.headstand='ring';TSTYLES.push(['drunk','술 취한 숫자'],['headstand','물구나무 타이머']);TSPREV.drunk=TSPREV.digits;TSPREV.headstand=TSPREV.ring;
SHOP_LOOK.mini02=[77,'하늘 배경, 반짝이 글씨, 그때 그 감성'];SHOP_LOOK.glitch=[77,'지지직, 화면이 계속 고장나 있습니다'];
SHOP_TIMER.drunk=[44,'숫자가 비틀비틀 제정신이 아닙니다'];SHOP_TIMER.headstand=[44,'타이머가 거꾸로 서 있습니다'];
HID_EXTRA['c:mini02']=['딱 1시간 11분 공부한 날',bmOk(function(b){return b.m71>=1;})];
HID_EXTRA['c:glitch']=['인증 마감 지나서 인증 5번',bmOk(function(b){return b.lateCert>=5;})];
HID_EXTRA['t:drunk']=['할 일 이름에 \'공부하기 싫다\' 적기',bmOk(function(b){return b.hate>=1;})];
HID_EXTRA['t:headstand']=['밤 11시 넘어서 출석 3번',bmOk(function(b){return b.lateIn>=3;})];
['c:mini02','c:glitch','t:drunk','t:headstand'].forEach(function(k){HID_EXTRA[k].bm=1;});
var hidExtraMark0=hidExtraMark;hidExtraMark=function(a){hidExtraMark0(a);a.forEach(function(x){if(HID_EXTRA[x.id]&&HID_EXTRA[x.id].bm){x.bm=1;}});};
var decoHidCard0=decoHidCard;decoHidCard=function(V,it,foc){var h=decoHidCard0(V,it,foc);return it.bm?h.replace('class="shi hid hid2','class="shi hid hid2 bm'):h;};
try{applyLook();}catch(e){}
