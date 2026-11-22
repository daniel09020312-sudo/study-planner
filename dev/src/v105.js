/* ---------- v105: 병맛 히든. 엉뚱한 조건으로 열리는 꾸미기 ---------- */
function bmStats(V){
  var g=gcSync(V),k='bm';if(g[k])return g[k];
  var o={z0:0,lateIn:0,plan30:0,zeroDone:0,m71:0,lateCert:0,songs:0},t=today(),last=t<END?t:END;
  for(var d=TALLY;d<=last;d=addDays(d,1)){
    var x=dayOf(V,V.me,d),m=sumMins(x.mins)+sumMins(x.manual),gl=x.goals.filter(function(q){return q&&!q.mv;});
    if(x.in&&m===0&&d<t)o.z0++;
    if(x.in){var h=new Date(x.in).getHours();if(h>=23||h<DAY_H)o.lateIn++;}
    if(x.goals.length>=30)o.plan30++;
    if(d<t&&gl.length>=3&&gl.filter(isDone).length===0)o.zeroDone++;
    if(m===71)o.m71++;
    if(x.certAt&&isLate(V,d,x.certAt))o.lateCert++;
  }
  for(var id in V.songs)if(obj(V.songs[id]).mid===V.me)o.songs++;
  return g[k]=o;
}
/* 병맛 테두리·칭호 장식 */
[
  ['r','potato','감자',30,'출석만 하고 공부 0분인 날 3번',function(s,V){return bmStats(V).z0>=3;}],
  ['r','zzz','쿨쿨',30,'밤 11시 넘어서 출석 3번',function(s,V){return bmStats(V).lateIn>=3;}],
  ['g','gungseo','궁서체',40,'하루에 할 일 30개 넘게 적기',function(s,V){return bmStats(V).plan30>=1;}],
  ['g','upside','뒤집힌 칭호',40,'할 일 3개 이상 적고 하나도 안 끝낸 날 3번',function(s,V){return bmStats(V).zeroDone>=3;}]
].forEach(function(x){DECO_ITEMS.push({id:x[0]+':'+x[1],v:x[1],cat:x[0]==='r'?'ring':'ttag',name:x[2],price:x[3],desc:'병맛 히든',hid:x[4],cond:x[5],bm:1});});
/* 병맛 방 꾸미기·색·타이머 */
CONCEPTS.push({id:'banana',name:'바나나 우유',soft:[.3,'#FFF3A8'],font:'Jua',face:'Jua',w:400,hid:1});
ACCENTS.push({id:'hlime',name:'형광 연두',g:'h',l:{a:'#5BC800',on:'#102000',soft:'#EDFFD6',ink:'#3C8A00',mark:'#5BC800'},d:{a:'#A6FF3D',on:'#102000',soft:'#22340F',ink:'#A6FF3D',mark:'#A6FF3D'}});
TVAR.wobble='digits';TSTYLES.push(['wobble','흔들 숫자']);TSPREV.wobble=TSPREV.digits;
SHOP_LOOK.banana=[60,'노랗고 동글동글한 바나나 우유 갑'];SHOP_TIMER.wobble=[40,'숫자가 혼자 춤을 춥니다'];
HID_EXTRA['c:banana']=['딱 1시간 11분 공부한 날',function(s,V){return bmStats(V).m71>=1;}];
HID_EXTRA['a:hlime']=['노동요 5곡 올리기',function(s,V){return bmStats(V).songs>=5;},20];
HID_EXTRA['t:wobble']=['인증 마감 지나서 인증 5번',function(s,V){return bmStats(V).lateCert>=5;}];
['c:banana','a:hlime','t:wobble'].forEach(function(k){HID_EXTRA[k].bm=1;});
var hidExtraMark0=hidExtraMark;hidExtraMark=function(a){hidExtraMark0(a);a.forEach(function(x){if(HID_EXTRA[x.id]&&HID_EXTRA[x.id].bm){x.bm=1;x.desc='병맛 히든 · '+x.desc;}});};
var hidLine0=hidLine;hidLine=function(V,it){var h=hidLine0(V,it);return it.bm&&h?h.replace('히든 · 조건','병맛 히든 · 조건'):h;};
var decoHidCard0=decoHidCard;decoHidCard=function(V,it,foc){var h=decoHidCard0(V,it,foc);return it.bm?h.replace('class="shi hid hid2','class="shi hid hid2 bm').replace('<b>히든 ','<b>병맛 히든 '):h;};
try{applyLook();}catch(e){}
