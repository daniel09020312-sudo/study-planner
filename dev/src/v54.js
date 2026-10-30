/* ---------- v54: 반 전체 목표, 같이 공부하기, 공부 잔디, 조용히 빠진 사람 ---------- */

/* 반 전체 목표: 한 주 동안 모두의 공부 시간 합. 달성한 주마다 모두에게 잉크 CG_INK방울.
   cfg.cgoal={h:시간, hist:{<월요일>:시간}} 방장이 바꾸면 그 주부터 적용(지난 주는 그때 값) */
var CG_INK=20,CG_FROM='2026-10-26';
function cgAuto(V){return Math.max(10,Math.round(V.roster.length*10/10)*10);}
function cgTarget(V,mon){
  var g=obj(V.cfg.cgoal),hs=obj(g.hist),best='',v=0;
  Object.keys(hs).forEach(function(k){if(k<=mon&&k>best&&+hs[k]>0){best=k;v=+hs[k];}});
  return v||cgAuto(V);
}
function cgWeek(V,mon){
  var g=gcSync(V),k='cg'+mon;if(g[k])return g[k];
  var st=standings(V,mon,addDays(mon,6)),tot=0,by=[];
  st.forEach(function(x){tot+=x.mins;if(x.mins>0)by.push({p:x.p,m:x.mins});});
  by.sort(function(a,b){return b.m-a.m;});
  var h=cgTarget(V,mon);
  return g[k]={mon:mon,mins:tot,goal:h,hit:tot>=h*60,by:by};
}
function cgInk(V){
  var t=today(),n=0;
  for(var w=CG_FROM;addDays(w,6)<t;w=addDays(w,7)){if(cgWeek(V,w).hit)n++;}
  return n*CG_INK;
}
function cgCard(V,k){
  if(!V.me)return '';
  var t=today(),mon=mondayOf(t),W=cgWeek(V,mon),pct=Math.min(100,Math.round(W.mins/(W.goal*60)*100)),left=Math.max(0,W.goal*60-W.mins),dl=diffDays(t,addDays(mon,6))+1;
  var me=0;W.by.forEach(function(x){if(x.p.id===V.me)me=x.m;});
  var prev=cgWeek(V,addDays(mon,-7)),adm=adminId(V)===V.me;
  var h='<section class="card cg'+(W.hit?' hit':'')+'" id="c-cg" style="--k:'+k+'"><div class="ct"><h2>반 전체 목표<small>이번 주</small></h2><span class="tag'+(W.hit?' a':'')+'">'+(W.hit?'달성':'D-'+(dl-1))+'</span></div>';
  h+='<div class="cgnum"><b>'+Math.floor(W.mins/60)+'</b><span>/ '+W.goal+'시간</span><em>'+pct+'%</em></div>';
  h+='<div class="cgbar" aria-hidden="true"><i style="width:'+pct+'%"></i></div>';
  h+='<p class="cgsub">'+(W.hit?'모두 잉크 '+CG_INK+'방울을 받습니다':'남은 '+fmtMins(left)+' · 달성하면 모두 잉크 '+CG_INK+'방울')+'</p>';
  if(W.by.length){
    h+='<div class="cgtop">';
    W.by.slice(0,3).forEach(function(x,i){h+='<span>'+(i+1)+'. '+esc(x.p.name)+' <b>'+fmtMins(x.m)+'</b></span>';});
    h+='</div>';
  }
  h+='<p class="hint">내 몫 '+fmtMins(me)+(W.mins?' ('+Math.round(me/W.mins*100)+'%)':'')+(prev.mon>=CG_FROM?' · 지난주 '+(prev.hit?'달성':'미달성')+' ('+Math.floor(prev.mins/60)+'/'+prev.goal+'시간)':'')+'</p>';
  if(adm){
    var open=!!S.cgEdit;
    h+='<div class="cgadm"><button class="linkbtn" data-act="cg-edit" aria-expanded="'+(open?'true':'false')+'">목표 바꾸기</button>';
    if(open){
      h+='<div class="chips" style="margin-top:6px">';[100,200,300,400,500].forEach(function(n){h+=chipBtn('cg-set','h',String(n),n+'시간',W.goal===n);});h+='</div>';
      h+='<div class="row" style="margin-top:6px"><input type="number" inputmode="numeric" min="10" max="5000" data-draft="cgH" placeholder="직접 입력 (시간)" aria-label="목표 시간 직접 입력"><button class="btn small primary" data-act="cg-save">저장</button></div><p class="hint">이번 주부터 적용됩니다.</p>';
    }
    h+='</div>';
  }
  return h+'</section>';
}
function cgTick(V){
  if(!V||!V.me||!S.ready)return;
  var mon=mondayOf(today()),W=cgWeek(V,mon);
  if(W.hit&&lsGet('gbb_cgw')!==mon){lsSet('gbb_cgw',mon);if(W.mins>0)flash('반 전체 목표를 달성했습니다. 모두 잉크 '+CG_INK+'방울을 받습니다.');}
}

/* 같이 공부하기: 지금 공부 중인 사람과 함께 시작하는 약속. cfg.meet={id:{at,m,t,by}}, 참여는 progress.<나>.mj={id:1} */
function meetList(V){
  var now=Date.now(),mt=obj(V.cfg.meet);
  return Object.keys(mt).map(function(id){var x=obj(mt[id]);return {id:id,at:+x.at||0,m:Math.max(10,Math.min(240,+x.m||50)),t:String(x.t||''),by:x.by};}).filter(function(x){return x.at&&x.at+x.m*60000>now-600000;}).sort(function(a,b){return a.at-b.at;});
}
function meetWho(V,id){return V.roster.filter(function(m){return obj(obj(V.progress[m.id]).mj)[id];}).map(function(m){return V.byId[m.id];});}
function meetTime(at){var d=new Date(at),t=fd(d),td=today(),lab=t===td?'오늘':t===addDays(td,1)?'내일':shortDate(t);return lab+' '+fmtClock(d.toISOString());}
function togetherCard(V,k){
  if(!V.me)return '';
  var now=Date.now(),live=V.roster.map(function(m){var L=liveOf(V,m.id);return L&&!isStale(L)?{p:V.byId[m.id],L:L}:null;}).filter(Boolean),myL=liveOf(V,V.me);
  var h='<section class="card tg" id="c-tg" style="--k:'+k+'"><div class="ct"><h2>같이 공부하기<small>'+(live.length?'지금 '+live.length+'명':'지금 아무도 없음')+'</small></h2>'+(!myL?'<button class="btn small primary" data-act="timer-start">나도 시작</button>':'')+'</div>';
  if(live.length){
    h+='<div class="tglive">';
    moreCut('tglive',live,10).forEach(function(x){var o=lv(x.L,now);h+='<div class="tgp'+(x.p.me?' me':'')+'">'+av(x.p,'s')+'<span><b>'+esc(x.p.name)+'</b><small>'+(o.rest?'쉬는 중':esc(subLabel(V,x.L.sid)))+' · <span data-lv="'+esc(x.p.id)+'">'+lvText(o)+'</span></small></span></div>';});
    h+='</div>'+moreBtn('tglive',live.length);
  }
  var ms=meetList(V);
  h+='<div class="sec"><h3>함께 시작하기 약속</h3>';
  if(!ms.length)h+='<p class="hint">시간을 정해 두면 그 시간에 같이 타이머를 켭니다.</p>';
  ms.slice(0,5).forEach(function(x){
    var who=meetWho(V,x.id),inn=who.some(function(p){return p.id===V.me;}),on=now>=x.at-300000&&now<x.at+x.m*60000,mine=x.by===V.me||adminId(V)===V.me;
    h+='<div class="tgm'+(on?' on':'')+'" id="mt-'+esc(x.id)+'"><div><b>'+esc(meetTime(x.at))+'</b> <small>'+x.m+'분</small>'+(x.t?'<span class="tgt">'+esc(x.t)+'</span>':'')+(on?'<em class="tag a">지금</em>':'')+'<small class="tgw">'+(who.length?who.slice(0,6).map(function(p){return esc(p.name);}).join(', ')+(who.length>6?' 외 '+(who.length-6)+'명':''):'아직 참여한 사람이 없습니다')+'</small></div><div class="row">';
    if(on&&inn&&!myL)h+='<button class="btn small primary" data-act="timer-start">타이머 켜고 합류</button>';
    h+='<button class="btn small'+(inn?'':' soft')+'" data-act="meet-join" data-id="'+esc(x.id)+'">'+(inn?'참여 취소':'참여')+'</button>';
    if(mine)h+='<button class="btn small" data-act="meet-del" data-id="'+esc(x.id)+'">'+(S.confirm==='mdel:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button>';
    h+='</div></div>';
  });
  if(S.meetForm){
    var F=S.meetForm;
    h+='<div class="tgform"><div class="chips">'+chipBtn('meet-set','d','0','오늘',F.d===0)+chipBtn('meet-set','d','1','내일',F.d===1)+'</div>';
    h+='<div class="row" style="margin-top:6px"><input type="time" data-draft="meetT" aria-label="시작 시각"><input type="text" data-draft="meetN" maxlength="20" placeholder="이름 (선택)" aria-label="약속 이름"></div>';
    h+='<div class="chips" style="margin-top:6px">';[25,50,90].forEach(function(n){h+=chipBtn('meet-set','m',String(n),n+'분',F.m===n);});h+='</div>';
    h+='<div class="row" style="margin-top:8px"><button class="btn small primary" data-act="meet-add">만들기</button><button class="btn small" data-act="meet-form">닫기</button></div></div>';
  }else h+='<div class="row" style="margin-top:6px"><button class="btn small" data-act="meet-form">약속 만들기</button></div>';
  return h+'</div></section>';
}
function meetTick(V){
  if(!V||!V.me)return;
  var now=Date.now();S.meetFl=S.meetFl||{};
  meetList(V).forEach(function(x){
    if(S.meetFl[x.id]||now<x.at||now>x.at+120000)return;
    if(!obj(obj(V.progress[V.me]).mj)[x.id])return;
    S.meetFl[x.id]=1;flash('같이 공부하기 시작 시간입니다'+(x.t?': '+x.t:'')+'.');
    try{if(typeof sysNotify==='function')sysNotify('같이 공부할 시간입니다',x.t||'타이머를 켜고 합류하세요','meet-'+x.id);}catch(e){}
  });
}

/* 공부 잔디: 한 달 동안 매일 공부 시간 */
function grassLv(m){return m<=0?0:m<60?1:m<180?2:m<300?3:4;}
function grassCard(V,k){
  if(!V.me)return '';
  var t=today(),ym=S.grassM||t.slice(0,7),first=ym+'-01',y=+ym.slice(0,4),mo=+ym.slice(5),nd=new Date(y,mo,0).getDate();
  var days=[],tot=0,on=0,run=0,best=0,top=null;
  for(var i=1;i<=nd;i++){
    var d=ym+'-'+(i<10?'0':'')+i,x=dayOf(V,V.me,d),m=sumMins(x.mins)+sumMins(x.manual);
    days.push({d:d,m:m});if(d<=t){tot+=m;if(m>0){on++;run++;if(run>best)best=run;if(!top||m>top.m)top={d:d,m:m};}else if(d<t)run=0;}
  }
  var lead=(pd(first).getDay()+6)%7,prevM=addDays(first,-1).slice(0,7),nextM=addDays(ym+'-'+nd,1).slice(0,7);
  var h='<section class="card" id="c-grass" style="--k:'+k+'"><div class="ct"><h2>공부 잔디</h2><div class="mnav sm"><button class="ib" data-act="grass-m" data-v="'+prevM+'" aria-label="이전 달"'+(prevM<CAL_MIN.slice(0,7)?' disabled':'')+'>&lsaquo;</button><b>'+y+'년 '+mo+'월</b><button class="ib" data-act="grass-m" data-v="'+nextM+'" aria-label="다음 달"'+(nextM>t.slice(0,7)?' disabled':'')+'>&rsaquo;</button></div></div>';
  h+='<div class="grass"><div class="gdow"><span>월</span><span></span><span>수</span><span></span><span>금</span><span></span><span>일</span></div><div class="ggrid">';
  for(i=0;i<lead;i++)h+='<i class="gx"></i>';
  days.forEach(function(x){h+='<i class="g'+(x.d>t?' gx':grassLv(x.m))+(x.d===t?' gt':'')+'" title="'+esc(shortDate(x.d)+' '+fmtMins(x.m))+'"></i>';});
  h+='</div></div><div class="glegend"><small>적음</small><i class="g0"></i><i class="g1"></i><i class="g2"></i><i class="g3"></i><i class="g4"></i><small>많음</small></div>';
  h+='<div class="hbands gstat"><div><small>공부한 날</small><b>'+on+'일</b></div><div><small>합계</small><b>'+fmtMins(tot)+'</b></div><div><small>최장 연속</small><b>'+best+'일</b></div><div><small>최고</small><b>'+(top?fmtMins(top.m):'-')+'</b></div></div>';
  return h+'</section>';
}

/* 조용히 빠진 사람: 방장만. 3일 넘게 출석하지 않은 사람 */
function quietList(V){
  var t=today(),out=[];
  V.roster.forEach(function(m){
    if(m.id===V.me)return;
    var last=null;for(var i=0;i<30;i++){var d=addDays(t,-i);if(dayOf(V,m.id,d).in){last=d;break;}}
    var gap=last?diffDays(last,t):99;
    if(gap>3)out.push({p:V.byId[m.id],last:last,gap:gap});
  });
  return out.sort(function(a,b){return b.gap-a.gap;});
}
function quietCard(V,k){
  if(!V.me||adminId(V)!==V.me)return '';
  var l=quietList(V);if(!l.length)return '';
  var h='<section class="card" id="c-quiet" style="--k:'+k+'"><div class="ct"><h2>요즘 안 보이는 사람<small>방장만 보입니다</small></h2></div>';
  moreCut('quiet',l).forEach(function(x){
    h+='<div class="brow">'+av(x.p,'s')+'<span>'+esc(x.p.name)+'<small class="rvs">'+(x.last?x.gap+'일째 출석 없음':'30일 넘게 출석 없음')+'</small></span><span></span><div class="row"><button class="btn small" data-act="poke" data-id="'+esc(x.p.id)+'">찌르기</button><button class="btn small soft" data-act="dm" data-id="'+esc(x.p.id)+'">메시지</button></div></div>';
  });
  return h+moreBtn('quiet',l.length)+'</section>';
}
