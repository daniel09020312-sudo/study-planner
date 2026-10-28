/* ---------- v51: 사람 목록은 10명까지만 보이고 '더보기'로 펼침, 1:1 대결을 더 재미있게(라운드제, 응원, 한마디, 도전장, 연승) ---------- */
function moreCut(key,list,n){n=n||10;return (S.more&&S.more[key])||list.length<=n?list:list.slice(0,n);}
function moreBtn(key,total,n,unit){
  n=n||10;if(total<=n)return '';
  var open=!!(S.more&&S.more[key]);
  return '<div class="moreb"><button class="btn small soft" data-act="more-list" data-k="'+key+'" aria-expanded="'+(open?'true':'false')+'">'+(open?'접기':'더보기 · 나머지 '+(total-n)+(unit||'명'))+'</button></div>';
}

/* 대결 종류 더하기: 할 일 달성률(하루 평균), 아침 출석(하루씩 누가 더 일찍 출석했나) */
DUEL_KINDS.push(
  {id:'rate',name:'할 일 달성률',unit:'%',desc:'하루 할 일 달성률의 평균(할 일이 있는 날만)',f:function(r){return r&&r.n?Math.round(r.done/r.n*100):0;},avg:true},
  {id:'early',name:'아침 출석',unit:'일',desc:'매일 누가 더 일찍 출석하나(이긴 날 수로 승부)',f:function(){return 0;},rounds:true}
);
function duelMode(d){return duelKindOf(d).rounds?'rounds':(d&&d.mode==='rounds'?'rounds':'sum');}
function duelDesc(d){return duelKindOf(d).name+' · '+duelLen(d)+'일 · '+(duelMode(d)==='rounds'?'하루씩 승부':'합계');}
/* 하루 값: 없으면 null(그날은 세지 않음) */
function duelDay(V,d,mid,date,r){
  var k=duelKindOf(d);
  if(k.id==='early'){var x=dayOf(V,mid,date);if(!x.in)return 0;var a=new Date(x.in);return Math.max(1,1700-(a.getHours()*60+a.getMinutes()));}
  if(k.id==='rate')return r&&r.n?Math.round(r.done/r.n*100):null;
  return duelVal(d,r);
}
function duelFinish(d){
  var k=duelKindOf(d);
  if(k.avg){d.pa=d.ca?Math.round(d.pa/d.ca):0;d.pb=d.cb?Math.round(d.pb/d.cb):0;}
  d.wa=0;d.wb=0;
  (d.rd||[]).forEach(function(x){if(x.a>x.b)d.wa++;else if(x.b>x.a)d.wb++;});
}
function duelSides(d){return duelMode(d)==='rounds'?[d.wa||0,d.wb||0]:[d.pa,d.pb];}
function duelWinner(d){
  var s=duelSides(d);
  if(s[0]===s[1]&&duelMode(d)==='rounds'&&duelKindOf(d).id!=='early')s=[d.pa,d.pb];
  return s[0]>s[1]?d.a:s[1]>s[0]?d.b:null;
}
function duelNum(d,n){var k=duelKindOf(d);return k.id==='time'?fmtMins(n):n+k.unit;}
/* 지금 상황 한 줄 */
function duelCoach(V,d){
  var me=V.me===d.a?'a':V.me===d.b?'b':'';if(!me)return '';
  var mine=me==='a'?d.pa:d.pb,opp=me==='a'?d.pb:d.pa,gap=mine-opp,k=duelKindOf(d);
  if(duelMode(d)==='rounds'){var s=duelSides(d),m=me==='a'?s[0]:s[1],o=me==='a'?s[1]:s[0];return m>o?'지금 라운드 '+(m-o)+'개 앞서고 있습니다.':m<o?'라운드가 '+(o-m)+'개 뒤져 있습니다. 오늘 이기면 따라잡습니다.':'라운드 동점입니다. 오늘이 승부처입니다.';}
  if(!gap)return '동점입니다. 조금만 더 하면 앞서갑니다.';
  var gtxt=k.id==='time'?fmtMins(Math.abs(gap)):Math.abs(gap)+k.unit;
  return gap>0?'지금 '+gtxt+' 앞서고 있습니다. 방심은 금물입니다.':'역전까지 '+(k.id==='time'?fmtMins(Math.abs(gap)+1):(Math.abs(gap)+1)+k.unit)+' 남았습니다.';
}
var TAUNTS=['한 판 붙자!','오늘은 내가 이긴다','끝까지 가 보자, 응원할게'];
function duelStreak(V,me){
  var l=duelList(V).filter(function(d){return d.state==='done'&&(d.a===me||d.b===me);}).sort(function(a,b){return a.end<b.end?1:-1;}),n=0;
  for(var i=0;i<l.length;i++){if(l[i].win===me)n++;else break;}
  return n;
}
function duelVs(V,me){
  var o={};
  duelList(V).forEach(function(d){
    if(d.state!=='done'||(d.a!==me&&d.b!==me))return;
    var id=d.a===me?d.b:d.a,r=o[id]=o[id]||{id:id,w:0,l:0,e:0};
    if(!d.win)r.e++;else if(d.win===me)r.w++;else r.l++;
  });
  return Object.keys(o).map(function(k){return o[k];}).sort(function(a,b){return (b.w+b.l+b.e)-(a.w+a.l+a.e);});
}
function duelRounds(V,d){
  var h='<div class="rdchips" aria-label="하루씩 결과">',t=today(),map={};
  (d.rd||[]).forEach(function(x){map[x.d]=x;});
  for(var i=0;i<duelLen(d);i++){
    var dt=addDays(d.start,i),x=map[dt],cl='p',tx='';
    if(x){if(x.a>x.b){cl='wa';tx=V.byId[d.a].name.slice(0,1);}else if(x.b>x.a){cl='wb';tx=V.byId[d.b].name.slice(0,1);}else{cl='t';tx='=';}if(x.d===t&&t<=d.end&&d.state==='on')cl+=' live';}
    h+='<span class="rdc '+cl+'" title="'+esc(shortDate(dt))+'"><small>'+DOW[pd(dt).getDay()]+'</small><b>'+esc(tx)+'</b></span>';
  }
  return h+'</div>';
}
function duelRow(V,d){
  var A=V.byId[d.a],B=V.byId[d.b],h='<div class="duel'+(d.state==='done'?' fin':'')+'" id="du-'+esc(d.id)+'">',part=d.a===V.me||d.b===V.me;
  if(d.state==='pending'){
    h+='<div class="pl"><span><b>'+esc(A.name)+'</b> 님이 <b>'+esc(B.name)+'</b> 님에게 도전장 <small>'+esc(duelDesc(d))+'</small></span><span class="tag">수락 대기</span></div>';
    if(d.note)h+='<p class="dnote">“'+esc(d.note)+'”</p>';
    if(d.b===V.me)h+='<div class="row" style="margin-top:8px"><button class="btn small primary" data-act="duel-ok" data-id="'+esc(d.id)+'">수락</button><button class="btn small" data-act="duel-no" data-id="'+esc(d.id)+'">거절</button></div>';
    else if(d.a===V.me)h+='<div class="row" style="margin-top:8px"><button class="btn small" data-act="duel-no" data-id="'+esc(d.id)+'">신청 취소</button></div>';
    return h+'</div>';
  }
  var s=duelSides(d),rounds=duelMode(d)==='rounds',tot=s[0]+s[1],k=duelKindOf(d),lab=d.state==='ready'?'내일 시작':d.state==='on'?(diffDays(today(),d.end)+1)+'일 남음':'종료';
  h+='<div class="vs"><span><b>'+esc(A.name)+'</b></span><em>'+esc(shortDate(d.start)+' ~ '+shortDate(d.end))+', '+lab+'</em><span class="r"><b>'+esc(B.name)+'</b></span></div><p class="duk">'+esc(duelDesc(d))+'</p>';
  if(d.note)h+='<p class="dnote">“'+esc(d.note)+'”</p>';
  h+='<div class="vs"><span class="p">'+(rounds?s[0]:esc(duelNum(d,d.pa)))+'</span><em>'+(rounds?'라운드':esc(k.name))+'</em><span class="p r">'+(rounds?s[1]:esc(duelNum(d,d.pb)))+'</span></div>';
  if(rounds&&k.id!=='early')h+='<p class="duk">합계 '+esc(duelNum(d,d.pa))+' : '+esc(duelNum(d,d.pb))+'</p>';
  h+='<div class="vbar" aria-hidden="true"><i class="'+(d.a===V.me?'me':'')+'" style="flex-grow:'+(tot?s[0]:1)+'"></i><i class="'+(d.b===V.me?'me':'')+'" style="flex-grow:'+(tot?s[1]:1)+'"></i></div>';
  if(d.state!=='ready')h+=duelRounds(V,d);
  if(d.state!=='done'){var cc=duelCoach(V,d);if(cc)h+='<p class="dcoach">'+esc(cc)+'</p>';}
  /* 응원 */
  var ch=obj(d.cheer),na=0,nb=0,my=ch[V.me]||'';Object.keys(ch).forEach(function(m){if(ch[m]==='a')na++;else if(ch[m]==='b')nb++;});
  if(d.state!=='done'||na||nb){
    h+='<div class="cheer"><span>응원</span>';
    if(!part&&d.state!=='done'&&V.me){
      h+='<button class="btn small'+(my==='a'?' primary':'')+'" data-act="duel-cheer" data-id="'+esc(d.id)+'" data-side="a" aria-pressed="'+(my==='a'?'true':'false')+'">'+esc(A.name)+' '+na+'</button><button class="btn small'+(my==='b'?' primary':'')+'" data-act="duel-cheer" data-id="'+esc(d.id)+'" data-side="b" aria-pressed="'+(my==='b'?'true':'false')+'">'+esc(B.name)+' '+nb+'</button>';
    }else h+='<b>'+esc(A.name)+' '+na+'</b><b>'+esc(B.name)+' '+nb+'</b>';
    h+='</div>';
  }
  /* 한마디 */
  if(part&&d.state!=='done'){
    h+='<div class="taunts"><span>한마디 보내기</span>';
    TAUNTS.forEach(function(t,i){h+='<button class="btn small" data-act="duel-taunt" data-id="'+esc(d.id)+'" data-i="'+i+'">'+esc(t)+'</button>';});
    h+='</div>';
  }
  if(d.state==='done'){
    var w=d.win,best=null;(d.rd||[]).forEach(function(x){var df=Math.abs(x.a-x.b);if(!best||df>best.df)best={x:x,df:df};});
    h+='<div class="dwin'+(w===V.me?' me':'')+'"><b>'+(w?esc(V.byId[w].name)+' 님 승리':'무승부')+'</b>'+(best&&best.df&&k.id!=='early'?'<small>가장 크게 갈린 날 '+esc(shortDate(best.x.d))+'</small>':'')+'</div>';
    h+='<div class="row" style="margin-top:8px">';
    if(part)h+='<button class="btn small" data-act="open" data-modal="duel" data-b="'+esc(d.a===V.me?d.b:d.a)+'" data-kind="'+esc(k.id)+'" data-len="'+duelLen(d)+'" data-mode="'+duelMode(d)+'">다시 붙기</button>';
    if(w&&w===V.me&&!d.brag)h+='<button class="btn small primary" data-act="duel-brag" data-id="'+esc(d.id)+'">결과 자랑하기</button>';
    h+='</div>';
  }
  return h+'</div>';
}
function modalDuel(V){
  var f=S.duelF,fk=duelKindOf({kind:f.kind}),rounds=fk.rounds||f.mode==='rounds',others=V.roster.filter(function(m){return m.id!==V.me;});
  var b='<p class="hint">상대가 수락한 다음 날부터 '+duelLen({days:f.len})+'일 동안, '+esc(fk.desc)+(rounds&&!fk.rounds?'를 하루씩 겨뤄 더 많이 이긴 쪽이 승리합니다':'로 겨룹니다')+'.</p><div class="fld"><h3>상대</h3><div class="chips">';
  var show=moreCut('duelopp',others);if(f.b&&show.indexOf(V.byId[f.b])<0&&show.filter(function(m){return m.id===f.b;}).length===0)show=show.concat(others.filter(function(m){return m.id===f.b;}));
  show.forEach(function(m){b+=chipBtn('duel-set','b',m.id,V.byId[m.id].name,f.b===m.id);});
  b+='</div>'+moreBtn('duelopp',others.length)+'</div><div class="fld"><h3>종류</h3><div class="chips">';
  DUEL_KINDS.forEach(function(k){b+=chipBtn('duel-set','kind',k.id,k.name,f.kind===k.id);});
  b+='</div></div><div class="fld"><h3>방식</h3><div class="chips">'+chipBtn('duel-set','mode','sum','합계로 겨루기',!rounds)+chipBtn('duel-set','mode','rounds','하루씩 승부(라운드제)',rounds)+'</div>'+(fk.rounds?'<p class="hint">이 종류는 항상 하루씩 승부합니다.</p>':'')+'</div><div class="fld"><h3>기간</h3><div class="chips">';
  DUEL_LENS.forEach(function(n){b+=chipBtn('duel-set','len',String(n),n===1?'하루':n+'일',+f.len===n);});
  b+='</div></div><div class="fld"><h3>도전장 한마디<small> 선택</small></h3><input type="text" data-draft="duelNote" maxlength="40" placeholder="예: 이번엔 내가 이긴다" aria-label="도전장 한마디"></div>';
  return dlg('wide',{id:'duel',t:'1:1 대결 신청'},b,'<span class="hint">신청하면 상대에게 알림이 갑니다.</span><div class="df"><button class="btn primary" data-act="duel-add"'+(f.b?'':' disabled')+'>도전장 보내기</button></div>');
}
function duelTab(V,t){
  var h='<section class="card" id="c-duels" style="--k:0"><div class="ct"><h2>1:1 대결</h2><button class="btn small primary" data-act="open" data-modal="duel"'+(V.roster.length<2?' disabled':'')+'>대결 신청</button></div>';
  var all=duelList(V),live=all.filter(function(d){return d.state!=='done';}),done=all.filter(function(d){return d.state==='done'&&diffDays(d.end,t)<=14;}),list=live.concat(done);
  if(!list.length)h+='<p class="empty">아직 대결이 없습니다. 한 명을 골라 점수, 공부 시간, 할 일 달성률 같은 걸로 겨뤄 보세요. 하루씩 승부하는 라운드제도 있고, 구경하는 사람은 응원할 수 있습니다.</p>';
  moreCut('duels',list).forEach(function(d){h+=duelRow(V,d);});
  h+=moreBtn('duels',list.length,10,'개');
  var wins={};all.forEach(function(d){if(d.state==='done'&&d.win)wins[d.win]=(wins[d.win]||0)+1;});
  var rc=duelRecord(V,V.me),st=V.me?duelStreak(V,V.me):0,vs=V.me?duelVs(V,V.me):[];
  h+='<div class="sec"><h3>내 전적'+(V.me?'<small>'+rc.w+'승 '+rc.e+'무 '+rc.l+'패'+(st>1?' · '+st+'연승 중':'')+'</small>':'')+'</h3>';
  if(!vs.length)h+='<p class="hint">끝난 대결이 쌓이면 상대별 전적이 여기 나옵니다.</p>';
  moreCut('duelvs',vs,5).forEach(function(r){var p=V.byId[r.id];if(!p)return;h+='<div class="brow">'+av(p,'s')+'<span>'+esc(p.name)+'</span><span></span><small>'+r.w+'승 '+r.e+'무 '+r.l+'패</small></div>';});
  h+=moreBtn('duelvs',vs.length,5,'명');
  h+='</div><div class="sec"><h3>대결 승수 순위</h3>';
  var rk=V.roster.slice().sort(function(a,b){return (wins[b.id]||0)-(wins[a.id]||0);});
  moreCut('duelrec',rk).forEach(function(m){h+='<div class="brow">'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><span></span><small>'+(wins[m.id]||0)+'승</small></div>';});
  h+=moreBtn('duelrec',rk.length)+'</div></section>';
  return h;
}
