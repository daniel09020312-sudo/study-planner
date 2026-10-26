/* ---------- v43: 할 일 모음, 지난 날 할 일, 메시지 읽음 숫자, 주간 리포트 더 보기, 모바일 더보기 메뉴 ---------- */

/* 할 일 모음: inbox/<나> = {items:{<id>:{t,sid,at,ct,ca,cu,cn}}}. 날짜 없이 적어 두고, 요일을 골라 그날 할 일로 옮긴다 */
function ibItems(V){
  if(!V.me)return [];
  var it=obj(obj(V.inbox[V.me]).items);
  return Object.keys(it).map(function(k){return Object.assign({id:k},obj(it[k]));}).filter(function(x){return x.t;}).sort(function(a,b){return (+a.at||0)-(+b.at||0);});
}
function editInbox(fn){
  var V=view();if(!V.me||!need())return;
  var d=clone(obj(V.inbox[V.me]));d.items=obj(d.items);fn(d);
  save('inbox/'+V.me,d);
}
function ibAdd(item){
  var n=0;editInbox(function(d){if(Object.keys(d.items).length>=60){n=-1;return;}d.items[rid('i')]=Object.assign({at:Date.now()},item);n=1;});
  if(n<0)flash('할 일 모음은 60개까지 적어 둘 수 있습니다.');
  return n>0;
}
function ibAssign(date){
  var V=view(),sel=Object.keys(obj(S.ib&&S.ib.sel)).filter(function(k){return S.ib.sel[k];}),items=ibItems(V).filter(function(x){return sel.indexOf(x.id)>=0;});
  if(!items.length){flash('넣을 할 일을 먼저 고르세요.');return;}
  if(date<today()){flash('지난 날에는 넣을 수 없습니다.');return;}
  var left=GMAX-dayOf(V,V.me,date).goals.length;
  if(left<=0){flash(shortDate(date)+'에는 할 일이 가득 찼습니다.');return;}
  var put=items.slice(0,left),sn=snap(['inbox/'+V.me,'days/'+V.me+'_'+date]);
  editDay(date,function(d){put.forEach(function(x){var g={id:rid('g'),text:String(x.t).slice(0,90),sid:x.sid||'',done:false};['ct','ca','cu','cn'].forEach(function(k){if(x[k]!=null&&x[k]!=='')g[k]=x[k];});d.goals.push(g);});});
  editInbox(function(d){put.forEach(function(x){delete d.items[x.id];});});
  S.ib.sel={};
  flash(shortDate(date)+' '+DOW[pd(date).getDay()]+'요일에 '+put.length+'개를 넣었습니다.'+(put.length<items.length?' '+(items.length-put.length)+'개는 자리가 없어 남겨 두었습니다.':''),sn);
}
function modalInbox(V){
  var I=S.ib,list=ibItems(V),t=today(),ws=I.week,nsel=list.filter(function(x){return I.sel[x.id];}).length,b='';
  b+='<div class="ibadd"><div class="chips scroll">'+mySubs(V).map(function(s){return chipBtn('ib-sid','sid',s.id,s.name,I.sid===s.id);}).join('')+'</div>';
  b+='<div class="row"><input type="text" id="ibText" data-draft="ibText" data-enter="ib-add" maxlength="90" placeholder="예: 쎈 3단원 50문제" aria-label="모아 둘 할 일"><button class="btn primary" data-act="ib-add">적기</button></div></div>';
  if(!list.length)b+='<p class="empty ibempty">아직 모아 둔 할 일이 없습니다. 이번 주에 할 일을 생각나는 대로 적어 두고, 아래에서 요일을 골라 나눠 넣으세요.</p>';
  else{
    b+='<div class="ibhead"><span>'+list.length+'개'+(nsel?', '+nsel+'개 고름':'')+'</span><button class="linkbtn" data-act="ib-all">'+(nsel===list.length?'모두 풀기':'모두 고르기')+'</button></div><ul class="iblist">';
    list.forEach(function(x){
      var on=!!I.sel[x.id],sub=x.sid&&V.subName[x.sid];
      b+='<li class="ibrow'+(on?' on':'')+'"><button class="ibpick" data-act="ib-sel" data-id="'+esc(x.id)+'" aria-pressed="'+(on?'true':'false')+'"><i aria-hidden="true"></i><span>'+(sub?'<em class="tag stag" style="--sc:'+subCol(V,x.sid)+'"><i></i>'+esc(sub)+'</em>':'')+'<b>'+esc(x.t)+'</b></span></button><button class="del" data-act="ib-del" data-id="'+esc(x.id)+'">'+(S.confirm==='ibdel:'+x.id?'한 번 더':'지우기')+'</button></li>';
    });
    b+='</ul>';
  }
  var f='';
  if(list.length){
    f='<div class="ibdays"><div class="ibwk"><button class="ib" data-act="ib-week" data-d="-1" aria-label="이전 주"'+(ws<=wkStart(t)?' disabled':'')+'>&lsaquo;</button><b>'+esc(wkTitle(ws))+'</b><button class="ib" data-act="ib-week" data-d="1" aria-label="다음 주">&rsaquo;</button></div><div class="ibdgrid">';
    for(var i=0;i<7;i++){
      var d=addDays(ws,i),dt=pd(d),n=dayOf(V,V.me,d).goals.length,past=d<t;
      f+='<button class="ibday'+(d===t?' today':'')+(dt.getDay()===0?' sun':'')+'" data-act="ib-put" data-d="'+d+'"'+(past||!nsel||n>=GMAX?' disabled':'')+' aria-label="'+esc(longDate(d))+'에 넣기"><small>'+DOW[dt.getDay()]+'</small><b>'+dt.getDate()+'</b><em>'+(n>=GMAX?'가득':n?n+'개':'')+'</em></button>';
    }
    f+='</div><p class="hint">'+(nsel?'요일을 누르면 고른 '+nsel+'개가 그날 할 일로 들어갑니다.':'할 일을 눌러 고른 뒤 넣을 요일을 누르세요.')+'</p></div>';
  }
  return dlg('wide',{id:'inbox',t:'할 일 모음'},b,f);
}
function ibBtn(V,cls){var n=ibItems(V).length;return '<button class="btn small '+(cls||'')+'" data-act="open" data-modal="inbox">할 일 모음'+(n?' <b class="ibn">'+n+'</b>':'')+'</button>';}

/* 지난 날 할 일: 오늘 화면에서 지난 날(2주)의 못 끝낸 할 일과 인증하지 않은 날을 바로 처리 */
function pastList(V){
  var t=today(),from=[START,CAL_MIN,addDays(t,-14)].sort().pop(),out=[];
  for(var d=addDays(t,-1);d>=from;d=addDays(d,-1)){
    var day=dayOf(V,V.me,d),g=day.goals.filter(function(x){return x&&!x.mv;});if(!g.length)continue;
    var un=g.filter(function(x){return !x.done;});
    if(un.length||!day.certAt)out.push({d:d,g:g,un:un,cert:day.certAt});
  }
  return out;
}
function pastCard(V,k){
  var L=pastList(V);if(!L.length)return '';
  var open=!!S.pastOpen,show=open?L:L.slice(0,2);
  var h='<section class="card" id="c-past" style="--k:'+k+'"><div class="ct"><h2>지난 날 할 일<small>'+L.length+'일</small></h2></div><p class="hint">지난 날 할 일도 지금 완료 표시하고 인증할 수 있습니다. 마감이 지난 인증은 '+RULE.certLate+'점, 할 일을 다 끝냈으면 '+RULE.allLate+'점이 더해집니다.</p>';
  show.forEach(function(x){
    var dn=x.g.length-x.un.length;
    h+='<div class="pday2" id="pd-'+x.d+'"><div class="pdh"><button class="pdl" data-act="pick-date" data-d="'+x.d+'"><b>'+esc(shortDate(x.d))+' '+DOW[pd(x.d).getDay()]+'</b><small>'+dlabel(x.d)+'</small></button><span class="pdn">'+dn+'/'+x.g.length+'</span>'+(x.cert?'<em class="tag">인증함</em>':'<button class="btn small soft" data-act="cert" data-date="'+x.d+'">인증하기</button>')+'</div><ul>';
    x.g.forEach(function(g){
      h+='<li class="'+(g.done?'done':'')+'"><button class="chk'+(g.done?' on':'')+'" data-act="goal-toggle" data-date="'+x.d+'" data-id="'+esc(g.id)+'" aria-pressed="'+(g.done?'true':'false')+'" aria-label="'+esc(g.text)+' 완료 표시"><span></span></button><span class="gtx">'+(g.sid&&V.subName[g.sid]?subTag(V,g):'')+'<span>'+esc(g.text)+'</span></span></li>';
    });
    h+='</ul></div>';
  });
  if(L.length>2)h+='<button class="plfin" data-act="past-more" aria-expanded="'+(open?'true':'false')+'">'+(open?'접기':'지난 날 '+(L.length-2)+'일 더 보기')+'</button>';
  return h+'</section>';
}

/* 메시지 읽음: reads/<나> = {all:읽은 시각, <상대 id>:읽은 시각}. 내 메시지 옆에 아직 안 읽은 사람 수(카톡처럼) */
var READS_SINCE=1793027217321; // 이 기능을 올린 시각: 그 전 메시지는 읽음 숫자를 세지 않음
function readsMark(V,c,at){
  if(!V.me||!canWrite()||!(at>0)||document.visibilityState==='hidden')return;
  var cur=obj(V.reads[V.me]);if((+cur[c]||0)>=at)return;
  S.readsBusy=S.readsBusy||{};if(S.readsBusy[c]>=at)return;S.readsBusy[c]=at;
  var d=clone(cur);d[c]=at;save('reads/'+V.me,d);
}
function unreadN(V,c,x){
  if(x.from!==V.me||+x.at<READS_SINCE)return 0;
  if(c!=='all'){var o=V.byId[c]?obj(V.reads[c]):null;return o&&(+o[V.me]||0)<+x.at?1:0;}
  var n=0;V.roster.forEach(function(m){if(m.id!==V.me&&(+obj(V.reads[m.id]).all||0)<+x.at)n++;});
  return n;
}
function unreadTag(V,c,x){var n=unreadN(V,c,x);return n?'<b class="urd" aria-label="안 읽은 사람 '+n+'명">'+n+'</b>':'';}

/* 주간 리포트 더 보기: 한 주 요약, 점수 내역, 과목별 지난주와 비교, 과목별 할 일 */
function reportMore(V,from,Wk,Pv){
  var me=Wk.per[V.me],pm=Pv.per[V.me],t=today(),days=Wk.days,past=days.filter(function(d){return d<=t;}).length||1;
  var gm=+obj(V.progress[V.me]).goalMins||0,studied=me.daily.filter(function(m){return m>0;}).length,best=-1,bi=0;
  me.daily.forEach(function(m,i){if(m>best){best=m;bi=i;}});
  var goalDays=gm?me.daily.filter(function(m){return m>=gm;}).length:0,streak=0;
  for(var dd=addDays(from,6)>t?t:addDays(from,6);streak<70;dd=addDays(dd,-1)){if(!dayOf(V,V.me,dd).in)break;streak++;}
  var h='<div class="cols rmore"><div class="stack">';
  h+='<section class="card" id="c-rsum-'+S.repWeek+'" style="--k:3"><div class="ct"><h2>한 주 요약</h2></div><div class="rsum">';
  [['하루 평균',fmtMins(Math.round(me.mins/past))],['공부한 날',studied+'일 / '+past+'일'],['가장 많이 한 날',best>0?DOW[pd(days[bi]).getDay()]+'요일 '+fmtMins(best):'-'],['하루 목표 채운 날',gm?goalDays+'일':'목표 없음'],['연속 출석',streak+'일'],['인증한 날',me.cert+'일']].forEach(function(x){h+='<div><small>'+x[0]+'</small><b>'+x[1]+'</b></div>';});
  h+='</div></section>';
  var cat={att:0,goal:0,time:0,cert:0,quiz:0,bonus:0,off:0};
  days.forEach(function(d){var r=V.sc[V.me]&&V.sc[V.me][d];if(!r)return;cat.att+=r.att;cat.goal+=r.goal+r.clear;cat.time+=r.time;cat.cert+=r.cert;cat.quiz+=r.quiz;cat.bonus+=r.bonus;cat.off+=r.off||0;});
  var bg=from>=START?(bingo(V,from).per[V.me]||{}).pts||0:0,rows=[['출석',cat.att],['할 일 모두 끝내기',cat.goal],['공부 시간',cat.time],['인증',cat.cert],['문제, 풀이, 답변',cat.quiz],['하루 순위 보너스',cat.bonus],['스터디 빙고',bg]],tot=rows.reduce(function(s,x){return s+x[1];},0),mx=Math.max.apply(null,rows.map(function(x){return x[1];}).concat([1]));
  h+='<section class="card" id="c-rpts-'+S.repWeek+'" style="--k:4"><div class="ct"><h2>점수 내역<small>합계 '+tot+'점</small></h2></div>';
  rows.forEach(function(x){h+='<div class="hb'+(x[1]?'':' o')+'"><span>'+x[0]+'</span><span class="tr"><i style="width:'+Math.round(x[1]/mx*100)+'%"></i></span><small>'+x[1]+'점</small></div>';});
  if(cat.off)h+='<p class="hint">점수 초기화로 '+cat.off+'점을 뺐습니다.</p>';
  h+='</section></div><div class="stack">';
  var ks={};Object.keys(me.subj).concat(Object.keys(pm.subj)).forEach(function(k){ks[k]=1;});
  var subs=Object.keys(ks).map(function(k){return {k:k,a:me.subj[k]||0,b:pm.subj[k]||0};}).sort(function(x,y){return y.a-x.a||y.b-x.b;});
  h+='<section class="card" id="c-rdelta-'+S.repWeek+'" style="--k:4"><div class="ct"><h2>과목별 지난주와 비교</h2></div>';
  if(!subs.length)h+='<p class="empty">두 주 모두 기록된 공부 시간이 없습니다.</p>';
  else h+='<ul class="rdelta">'+subs.map(function(x){var dl=x.a-x.b;return '<li style="--sc:'+(x.k==='etc'?SGRAY:subCol(V,x.k))+'"><i></i><span>'+esc(subLabel(V,x.k))+'</span><b>'+fmtMins(x.a)+'</b><em class="'+(dl>0?'up':dl<0?'dn':'')+'">'+(dl===0?'같음':(dl>0?'+':'-')+fmtMins(Math.abs(dl)))+'</em></li>';}).join('')+'</ul>';
  h+='</section>';
  var gs={};days.forEach(function(d){dayOf(V,V.me,d).goals.forEach(function(g){if(!g||g.mv)return;var k=g.sid&&V.subName[g.sid]?g.sid:'';var o=gs[k]=gs[k]||{n:0,d:0};o.n++;if(g.done)o.d++;});});
  var gk=Object.keys(gs).sort(function(a,b){return gs[b].n-gs[a].n;});
  h+='<section class="card" id="c-rgoal-'+S.repWeek+'" style="--k:5"><div class="ct"><h2>과목별 할 일 달성</h2></div>';
  if(!gk.length)h+='<p class="empty">이 주에 적은 할 일이 없습니다.</p>';
  gk.forEach(function(k){var o=gs[k],p=Math.round(o.d/o.n*100);h+='<div class="hb"><span>'+esc(k?V.subName[k]:'과목 없음')+'</span><span class="tr"><i style="width:'+p+'%"></i></span><small>'+o.d+'/'+o.n+'</small></div>';});
  return h+'</section></div></div>';
}

/* 모바일 아래 메뉴: 달력, 공부방, 메시지, 상점, 설정만 두고 나머지는 '더보기' */
var MORE_TABS=[['prog','진도','과목별 진도와 단원'],['rank','순위','이번 주 순위와 최종 결과'],['report','리포트','한 주 공부 기록'],['play','도전','빙고, 1:1 대결, 배지'],['board','게시판','문제 내기와 질문']];
function moreIcon(tab){var b=navs.querySelector('[data-tab="'+tab+'"] svg');return b?b.outerHTML:'';}
function paintMore(){
  var mb=document.getElementById('navMore');if(!mb)return;
  var cur=MORE_TABS.filter(function(x){return x[0]===S.tab;})[0];
  mb.setAttribute('aria-expanded',S.moreOpen?'true':'false');
  if(cur)mb.setAttribute('aria-current','page');else mb.removeAttribute('aria-current');
  var key=cur?cur[0]:'';
  if(mb.__k!==key){mb.__k=key;mb.innerHTML=(cur?moreIcon(cur[0]):'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.8"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.8"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.8"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.8"/></svg>')+'<span>'+(cur?cur[1]:'더보기')+'</span>';}
  var m=document.getElementById('moreMenu');
  if(!S.moreOpen){if(m&&!m.classList.contains('out')){m.classList.add('out');setTimeout(function(){if(m.parentNode&&!S.moreOpen)m.parentNode.removeChild(m);},200);}return;}
  if(m&&m.classList.contains('out')){m.parentNode.removeChild(m);m=null;}
  if(!m){m=document.createElement('div');m.id='moreMenu';document.body.appendChild(m);}
  var h='<div class="mscrim" data-act="more-x"></div><div class="mpanel" role="menu" aria-label="다른 화면">';
  MORE_TABS.forEach(function(x){h+='<button role="menuitem" class="mitem'+(S.tab===x[0]?' on':'')+'" data-act="tab" data-tab="'+x[0]+'"><span class="mic">'+moreIcon(x[0])+'</span><span class="mtx"><b>'+x[1]+'</b><small>'+x[2]+'</small></span><i class="mchev" aria-hidden="true"></i></button>';});
  m.innerHTML=h+'</div>';
}

/* 타이머 모양: 아날로그 시계(분침은 남은/지난 비율, 초침은 초), 두 겹 고리(바깥 분, 안쪽 초), 눈금과 숫자 */
var ORB=464.96;
var RING_TICKS=(function(){var t='';for(var i=0;i<60;i++){var a=i*Math.PI/30,b=i%5===0,r1=b?72:75;t+='<line'+(b?' class="bg"':'')+' x1="'+(100+r1*Math.sin(a)).toFixed(1)+'" y1="'+(100-r1*Math.cos(a)).toFixed(1)+'" x2="'+(100+79*Math.sin(a)).toFixed(1)+'" y2="'+(100-79*Math.cos(a)).toFixed(1)+'"/>';}return t;})();
var AN_TICKS=(function(){var t='';for(var i=0;i<60;i++){var a=i*Math.PI/30,b=i%5===0,r1=b?74:80;t+='<line'+(b?' class="bg"':'')+' x1="'+(100+r1*Math.sin(a)).toFixed(1)+'" y1="'+(100-r1*Math.cos(a)).toFixed(1)+'" x2="'+(100+85*Math.sin(a)).toFixed(1)+'" y2="'+(100-85*Math.cos(a)).toFixed(1)+'"/>';}return t;})();
var AN_NUMS=(function(){var t='<g class="ann">';for(var i=0;i<12;i++){var a=i*Math.PI/6;t+='<text x="'+(100+62*Math.sin(a)).toFixed(1)+'" y="'+(100-62*Math.cos(a)+4.2).toFixed(1)+'">'+(i*5)+'</text>';}return t+'</g>';})();
var PIE_NUMS=(function(){var t='<g class="pnn">';[0,15,30,45].forEach(function(n,i){var a=i*Math.PI/2;t+='<text x="'+(100+70*Math.sin(a)).toFixed(1)+'" y="'+(100-70*Math.cos(a)+4).toFixed(1)+'">'+n+'</text>';});return t+'</g>';})();
function anAngles(L,o,f){var p=f&&f.pie!=null?f.pie:0;return {m:(p*360).toFixed(2),s:f&&f.idle?0:(((o.e||0)/1000)%60*6).toFixed(2)};}
function anSet(g,L,o){
  var p=lvPie(L,o),a=anAngles(L,o,{pie:p});
  var w=g.querySelector('.ans');if(w)w.setAttribute('d',piePath(p));
  var m=g.querySelector('.anm');if(m)m.setAttribute('transform','rotate('+a.m+' 100 100)');
  var s=g.querySelector('.ansec');if(s)s.setAttribute('transform','rotate('+a.s+' 100 100)');
}
