/* ---------- 과목 색 ---------- */
var SCOLS=[['c0','#4A86F0','파랑'],['c1','#2BA673','초록'],['c2','#F0883A','주황'],['c3','#8D6CEB','보라'],['c4','#E5609A','분홍'],['c5','#1DA3B5','청록'],['c6','#D9A520','노랑'],['c7','#E2544C','빨강'],['c8','#5A67D6','남색'],['c9','#7FAE34','연두']],SGRAY='#9AA1AD';
function subCol(V,sid){
  if(!sid||!V.subById[sid])return SGRAY;
  var my=obj(obj(V.progress[V.me]).scol)[sid];
  if(my==='g')return SGRAY;
  for(var i=0;i<SCOLS.length;i++)if(SCOLS[i][0]===my)return SCOLS[i][1];
  var k=V.subs.indexOf(V.subById[sid]);return SCOLS[(k<0?0:k)%SCOLS.length][1];
}
function isEtcGoal(g){return !g||!g.sid||/수행\s?평가/.test(String(g.text||''));}
function goalCol(V,g){return isEtcGoal(g)||!V.subById[g.sid]?SGRAY:subCol(V,g.sid);}
function subTag(V,g){var n=V.subName[g.sid];return n?'<em class="tag stag" style="--sc:'+goalCol(V,g)+'"><i></i>'+esc(n)+'</em>':'';}
function jos(w,a,b){w=String(w||'');var c=w.charCodeAt(w.length-1);if(!(c>=0xAC00&&c<=0xD7A3))return w+a;return w+((c-0xAC00)%28?a:b);}

/* ---------- 시간 ---------- */
function pad2(n){return (n<10?'0':'')+n;}
function fmtHM(m){m=Math.round(+m||0);return pad2(Math.floor(m/60)%24)+':'+pad2(m%60);}
function parseHM(v){var r=/^(\d{1,2}):(\d{2})/.exec(String(v||''));if(!r)return null;var m=(+r[1])*60+(+r[2]);if(m<5*60)m+=1440;return m;}
function placed(g){return !!g&&g.ts!=null&&+g.te>+g.ts;}
function snap10(m){return Math.round(m/10)*10;}
function nowMin(){var x=new Date();return x.getHours()*60+x.getMinutes();}

/* ---------- 시간표 자료 ---------- */
var TTK={school:'학교',academy:'학원',etc:'기타'};
function ttData(V){var t=obj(obj(V.progress[V.me]).tt);return {b:arr(t.b).filter(function(b){return b&&b.id;}),ov:obj(t.ov),x:obj(t.x),win:obj(t.win)};}
function ttWin(V){var w=ttData(V).win;return {s:+w.s>0?+w.s:9*60,e:+w.e>0?+w.e:24*60};}
function editTT(fn){
  editProg(function(p){
    var t=clone(obj(p.tt));t.b=arr(t.b);t.ov=obj(t.ov);t.x=obj(t.x);t.win=obj(t.win);fn(t);
    var lim=addDays(today(),-21);
    Object.keys(t.ov).forEach(function(d){if(d<lim||!Object.keys(obj(t.ov[d])).length)delete t.ov[d];});
    Object.keys(t.x).forEach(function(d){if(d<lim||!arr(t.x[d]).length)delete t.x[d];});
    p.tt=t;
  });
}
function fixedOn(V,d,all){
  var T=ttData(V),dw=pd(d).getDay(),ov=obj(T.ov[d]),out=[];
  T.b.forEach(function(b){
    if(String(b.d||'').charAt(dw)!=='1')return;
    var o=obj(ov[b.id]);if(o.off&&!all)return;
    out.push({id:b.id,k:TTK[b.k]?b.k:'etc',t:String(b.t||''),sid:b.sid||'',s:o.s!=null?+o.s:+b.s,e:o.e!=null?+o.e:+b.e,bs:+b.s,be:+b.e,moved:o.s!=null,off:!!o.off,tpl:true,dw:String(b.d||'')});
  });
  arr(T.x[d]).forEach(function(b){if(b&&b.id)out.push({id:b.id,k:TTK[b.k]?b.k:'etc',t:String(b.t||''),sid:b.sid||'',s:+b.s,e:+b.e,one:true});});
  return out.filter(function(b){return b.e>b.s;});
}
function ttLanes(items){
  items.sort(function(a,b){return a.s-b.s||b.e-a.e;});
  var cur=null;
  items.forEach(function(it){
    if(!cur||it.s>=cur.end)cur={end:it.e,lanes:[]};
    var li=-1;for(var i=0;i<cur.lanes.length;i++){if(cur.lanes[i]<=it.s){li=i;break;}}
    if(li<0){li=cur.lanes.length;cur.lanes.push(it.e);}else cur.lanes[li]=it.e;
    it.lane=li;it.cl=cur;cur.end=Math.max(cur.end,it.e);
  });
  items.forEach(function(it){it.lanes=it.cl.lanes.length;delete it.cl;});
  return items;
}
function ttSpan(){var s=S.ttSpan;if(s===1||s===3||s===7)return s;var w=window.innerWidth||1024;return w>=1000?7:w>=640?3:1;}
function ttDays(){var n=ttSpan(),st=S.ttStart||today(),out=[];for(var i=0;i<n;i++)out.push(addDays(st,i));return out;}
function ttEnter(){S.ttStart=S.date||today();S.ttPick=null;S.ttScrollY='auto';}
function ttSelGoal(){var sl=S.ttSel,V=view();if(!sl||!V.me)return null;return dayOf(V,V.me,sl.d).goals.filter(function(g){return g.id===sl.id;})[0]||null;}
function ttSelFixed(){var sl=S.ttSel,V=view();if(!sl||!V.me)return null;return fixedOn(V,sl.d,true).filter(function(b){return b.id===sl.id;})[0]||null;}
function ttEdFrom(V,id){var b=ttData(V).b.filter(function(x){return x.id===id;})[0];if(!b)return null;S.draft.ttEdT=b.t||'';return {id:b.id,k:TTK[b.k]?b.k:'etc',sid:b.sid||'',d:String(b.d||'0000000'),s:+b.s,e:+b.e};}

/* ---------- 시간표 화면 ---------- */
function viewTT(V){
  var t=today(),days=ttDays(),n=days.length,T=ttData(V),dd=diffDays(t,EXAM[0]),HH=n===7?46:52,nm=nowMin(),hasT=days.indexOf(t)>=0;
  var title=n===1?longDate(days[0]):wkTitle(days[0],n);
  var h='<div class="view" id="view-cal"><header class="vhead"><div class="mnav"><button class="ib" data-act="tt-nav" data-d="-1" aria-label="이전">&lsaquo;</button><h1 class="wkt">'+esc(title)+'</h1><button class="ib" data-act="tt-nav" data-d="1" aria-label="다음">&rsaquo;</button>';
  if(!hasT)h+='<button class="btn small" data-act="tt-nav" data-d="0" style="margin-left:6px">오늘</button>';
  h+='</div><div class="vacts">'+calModeSeg()+(dd>0?'<span class="pill">2차 시험<b>D-'+dd+'</b></span>':'')+'</div></header>';
  var cols=days.map(function(d){
    var day=dayOf(V,V.me,d),mode=modeOf(d);
    return {d:d,day:day,mode:mode,ro:mode==='view',fx:fixedOn(V,d),offN:fixedOn(V,d,true).filter(function(b){return b.off;}).length,
      pl:day.goals.filter(placed),un:day.goals.filter(function(g){return !placed(g)&&!g.done;})};
  });
  var r0=7*60,r1=24*60;
  cols.forEach(function(c){c.fx.concat(c.pl.map(function(g){return {s:+g.ts,e:+g.te};})).forEach(function(b){r0=Math.min(r0,Math.floor(b.s/60)*60);r1=Math.max(r1,Math.ceil(b.e/60)*60);});});
  r0=Math.max(0,r0);r1=Math.min(28*60,r1);
  var tot=Math.round((r1-r0)*HH/60),px=function(m){return Math.round((m-r0)*HH/6)/10;};
  var auto;
  if(hasT)auto=nm-60;
  else{var ends=[];cols.forEach(function(c){c.fx.forEach(function(b){if(b.k==='school')ends.push(b.e);});});auto=ends.length?Math.min.apply(null,ends)-30:9*60;}
  auto=Math.max(r0,Math.min(r1,auto));
  var fillable=0;cols.forEach(function(c){if(!c.ro&&c.d>=t)fillable+=c.un.length;});
  h+='<div class="vbody'+(S.vbDir?' side':'')+'" id="vb-tt-'+days[0]+'-'+n+'" style="--vd:'+S.vbDir+'"><section class="card ttcard" id="c-tt" style="--k:0">';
  h+='<div class="tttools"><div class="seg mini ttspan" style="--i:'+[1,3,7].indexOf(n)+';--n:3" role="group" aria-label="며칠씩 볼지">'+[[1,'1일'],[3,'3일'],[7,'7일']].map(function(x){return '<button data-act="tt-span" data-v="'+x[0]+'" aria-pressed="'+(n===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div><div class="acts">'+(fillable?'<button class="btn small soft" data-act="tt-fill">빈 시간에 채우기</button>':'')+'<button class="btn small" data-act="open" data-modal="school">학교 시간표</button><button class="btn small" data-act="open" data-modal="ttset">고정 시간표</button></div></div>';
  if(!T.b.length)h+='<div class="ttnote"><p>학교와 학원 시간을 먼저 넣어 두면 남는 시간에 할 일을 놓을 수 있습니다.</p><button class="btn small primary" data-act="open" data-modal="ttset">고정 시간표 넣기</button></div>';
  if(S.ttPick){var pg=dayOf(V,V.me,S.ttPick.d).goals.filter(function(g){return g.id===S.ttPick.id;})[0];
    if(pg)h+='<div class="ttpickbar" role="status" style="--sc:'+goalCol(V,pg)+'"><i></i><span><b>'+esc(cut(pg.text,28))+'</b> 놓을 시간을 누르세요</span><button class="btn small" data-act="tt-pick-x">취소</button></div>';else S.ttPick=null;}
  h+='<div class="ttscroll" id="ttScroll" data-auto="'+Math.round(px(auto))+'"><div class="ttg n'+n+'" style="--n:'+n+';--hh:'+HH+'px">';
  h+='<div class="tthc" aria-hidden="true"></div>';
  cols.forEach(function(c){
    var dt=pd(c.d),g=c.day.goals,dn=g.filter(isDone).length,off=dt.getDay()===0||(EVENTS[c.d]&&EVENTS[c.d].off);
    h+='<div class="tth'+(c.d===t?' today':'')+(off?' sun':'')+(c.ro?' past':'')+'"><button class="tthd" data-act="tt-day" data-d="'+c.d+'" aria-label="'+esc(longDate(c.d))+(n===1?', 여러 날 보기로 돌아가기':', 이 날만 크게 보기')+'"><small>'+DOW[dt.getDay()]+'</small><b>'+dt.getDate()+'</b>'+(g.length?'<em>'+dn+'/'+g.length+'</em>':'')+'</button><div class="ttq" id="tq-'+c.d+'">';
    if(!c.ro)c.un.forEach(function(x){var on=!!(S.ttPick&&S.ttPick.id===x.id);h+='<button class="ttchip'+(on?' on':'')+'" id="tqc-'+esc(x.id)+'" data-act="tt-pick" data-tdrag="q" data-d="'+c.d+'" data-id="'+esc(x.id)+'" data-dur="60" style="--sc:'+goalCol(V,x)+'" aria-pressed="'+(on?'true':'false')+'" aria-label="'+esc(x.text)+', 시간표에 넣기"><i></i><span>'+esc(x.text)+'</span></button>';});
    if(c.offN&&!c.ro)h+='<button class="ttrest" data-act="tt-restore" data-d="'+c.d+'">뺀 고정 일정 '+c.offN+'개 되살리기</button>';
    h+='</div></div>';
  });
  h+='<div class="ttax" style="height:'+tot+'px" aria-hidden="true">';
  for(var m=r0+60;m<r1;m+=60)h+='<span style="top:'+px(m)+'px">'+(Math.floor(m/60)%24)+'시</span>';
  h+='</div>';
  cols.forEach(function(c){
    var items=c.fx.map(function(b){return {k:'f',b:b,s:b.s,e:b.e};}).concat(c.pl.map(function(g){return {k:'g',g:g,s:+g.ts,e:+g.te};}));
    ttLanes(items);
    h+='<div class="ttcol'+(c.ro?' ro':'')+(S.ttPick&&!c.ro?' picking':'')+(c.d===t?' today':'')+'" id="tc-'+c.d+'" data-act="tt-slot" data-d="'+c.d+'" data-r0="'+r0+'" data-r1="'+r1+'" data-hh="'+HH+'" style="height:'+tot+'px">';
    items.forEach(function(it){
      var top=px(it.s),ht=Math.max(16,px(it.e)-top),pos='top:'+top+'px;height:'+ht+'px;left:calc('+it.lane+' * 100% / '+it.lanes+');width:calc(100% / '+it.lanes+');--lc:'+Math.max(1,Math.min(4,Math.floor((ht-23)/16))),cls=(ht<30?' sm':'')+(ht<20?' xs':''),tm=fmtHM(it.s)+'~'+fmtHM(it.e),dr=c.ro?'':' data-tdrag="'+it.k+'"';
      var dat=' data-d="'+c.d+'" data-s="'+it.s+'" data-e="'+it.e+'" data-dur="'+(it.e-it.s)+'"';
      if(it.k==='f'){
        var b=it.b,lab=b.t||TTK[b.k],per=b.k==='school'?schPeriods(V,c.d,b):[],ps='';
        per.forEach(function(x){ps+='<i class="tper" style="top:'+(px(x.s)-px(b.s))+'px;height:'+Math.max(10,px(x.e)-px(x.s))+'px;--pc:'+(x.c.sid?subCol(V,x.c.sid):SGRAY)+'" aria-hidden="true"><b>'+(x.i+1)+'</b>'+esc(x.c.name)+'</i>';});
        h+='<div class="ttb fx k-'+b.k+cls+(b.moved?' moved':'')+(b.sid?' hs':'')+(per.length?' hasp':'')+'" id="tb-'+esc(b.id)+'-'+c.d+'" role="button" tabindex="0" data-act="tt-open" data-k="f" data-id="'+esc(b.id)+'"'+dr+dat+' style="'+pos+(b.sid?';--sc:'+subCol(V,b.sid):'')+'" aria-label="'+esc(lab+', '+tm)+'">'+ps+'<span class="tbt">'+esc(lab)+'</span><small>'+tm+'</small>'+(c.ro?'':'<i class="tbr" aria-hidden="true"></i>')+'</div>';
      }else{
        var g=it.g,sub=g.sid&&V.subName[g.sid];
        h+='<div class="ttb td'+cls+(g.done?' done':'')+'" id="tb-'+esc(g.id)+'" role="button" tabindex="0" data-act="tt-open" data-k="g" data-id="'+esc(g.id)+'"'+dr+dat+' style="'+pos+';--sc:'+goalCol(V,g)+'" aria-label="'+esc(g.text+', '+tm)+'">'+(c.mode==='full'?'<button class="ttbchk'+(g.done?' on':'')+'" data-act="goal-toggle" data-date="'+c.d+'" data-id="'+esc(g.id)+'" aria-pressed="'+(g.done?'true':'false')+'" aria-label="'+esc(g.text)+' 완료 표시"><span></span></button>':'')+'<span class="tbt">'+esc(g.text)+'</span><small>'+tm+(sub?' · '+esc(sub):'')+'</small>'+(c.ro?'':'<i class="tbr" aria-hidden="true"></i>')+'</div>';
      }
    });
    if(c.d===t&&nm>=r0&&nm<=r1)h+='<div class="ttnow" style="top:'+px(nm)+'px" aria-hidden="true"></div>';
    h+='</div>';
  });
  h+='</div></div>';
  h+='<p class="hint tthint">빈 곳을 누르면 그 시간에 넣을 할 일을 고를 수 있습니다. 블록을 꾹 눌러 끌면 옮겨지고, 아래 끝을 끌면 길이가 바뀝니다.</p>';
  return h+'</section></div></div>';
}

/* ---------- 시간표 바꾸기 ---------- */
function ttCommit(kind,from,id,s,e,to){
  var V=view();S.ttPick=null;
  if(!V.me||!need()){render();return;}
  if(kind==='f'){
    var b=fixedOn(V,from).filter(function(x){return x.id===id;})[0];if(!b){render();return;}
    var sn=snap(['progress/'+V.me]);
    editTT(function(T){if(b.one)T.x[from]=arr(T.x[from]).map(function(x){return x.id===id?Object.assign({},x,{s:s,e:e}):x;});else{var o=obj(T.ov[from]);o[id]={s:s,e:e};T.ov[from]=o;}});
    if(b.tpl)flash(jos(b.t||TTK[b.k],'을','를')+' 이 날만 '+fmtHM(s)+'~'+fmtHM(e)+'에 두었습니다.',sn);
    render();return;
  }
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x.id===id;})[0];if(!g){render();return;}
  if(to!==from){
    if(to<today()){flash('지난 날로는 옮길 수 없습니다.');render();return;}
    if(dayOf(V,V.me,to).goals.length>=GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');render();return;}
    var sn2=snap(['days/'+V.me+'_'+from,'days/'+V.me+'_'+to]);
    editDay(from,function(d){d.goals=d.goals.filter(function(x){return x.id!==id;});if(d.focus===id)d.focus=null;});
    editDay(to,function(d){var c=clone(g);c.done=false;c.ts=s;c.te=e;d.goals.push(c);});
    flash(shortDate(to)+' '+DOW[pd(to).getDay()]+'요일 '+fmtHM(s)+'에 옮겨 놓았습니다.',sn2);render();return;
  }
  editDay(from,function(d){d.goals.forEach(function(x){if(x.id===id){x.ts=s;x.te=e;}});});
  render();
}
function ttFill(){
  var V=view();if(!V.me||!need())return;
  var t=today(),win=ttWin(V),nm=nowMin(),paths=[],plan=[],left=0,n=0;
  ttDays().filter(function(d){return d>=t;}).forEach(function(d){
    var day=dayOf(V,V.me,d),un=day.goals.filter(function(g){return !placed(g)&&!g.done;});if(!un.length)return;
    var busy=fixedOn(V,d).map(function(b){return [b.s,b.e];}).concat(day.goals.filter(placed).map(function(g){return [+g.ts,+g.te];}));
    var cur=win.s,set={},k=0;if(d===t)cur=Math.max(cur,Math.ceil((nm+5)/10)*10);
    un.forEach(function(g){
      var dur=60,s=cur;
      for(var guard=0;guard<100;guard++){
        if(s+dur>win.e){s=null;break;}
        var hit=null;busy.forEach(function(b){if(s<b[1]&&s+dur>b[0]&&(!hit||b[1]>hit[1]))hit=b;});
        if(!hit)break;s=hit[1];
      }
      if(s==null){left++;return;}
      set[g.id]=[s,s+dur];busy.push([s,s+dur]);cur=s+dur+10;k++;
    });
    if(k){paths.push('days/'+V.me+'_'+d);plan.push([d,set]);}
  });
  if(!plan.length){flash(left?'빈 시간이 모자라 넣지 못했습니다. 공부 시간 범위나 고정 일정을 확인하세요.':'시간표에 넣을 할 일이 없습니다.');return;}
  var sn=snap(paths);
  plan.forEach(function(p){editDay(p[0],function(d){d.goals.forEach(function(x){var v=p[1][x.id];if(v){x.ts=v[0];x.te=v[1];n++;}});});});
  flash('할 일 '+n+'개를 빈 시간에 넣었습니다.'+(left?' '+left+'개는 시간이 모자라 남겨 뒀습니다.':''),sn);
}

/* ---------- 시간표 창 ---------- */
function ttTimeRow(kind,s,e,dis){
  return '<div class="ttime"><input type="time" step="600" value="'+(s!=null?fmtHM(s):'')+'" data-chg="'+kind+'" data-k="s" aria-label="시작 시간"'+(dis?' disabled':'')+'><span>~</span><input type="time" step="600" value="'+(e!=null?fmtHM(e):'')+'" data-chg="'+kind+'" data-k="e" aria-label="끝 시간"'+(dis?' disabled':'')+'></div>';
}
var TT_DURS=[[30,'30분'],[60,'1시간'],[90,'1시간 30분'],[120,'2시간']];
function modalTTG(V){
  var g=ttSelGoal();if(!g){S.modal=null;return '';}
  var d=S.ttSel.d,mode=modeOf(d),sub=g.sid&&V.subName[g.sid],on=placed(g),s=on?+g.ts:null,e=on?+g.te:null;
  var b='<div class="ttsum" style="--sc:'+goalCol(V,g)+'"><i></i><div><b>'+esc(g.text)+'</b><small>'+esc(longDate(d))+(sub?' · '+esc(sub):'')+(g.done?' · 끝냄':'')+'</small></div></div>';
  if(mode!=='view'){
    b+='<div class="fld"><h3>시간</h3>'+ttTimeRow('ttg-time',s,e)+'<div class="chips" style="margin-top:10px">'+TT_DURS.map(function(x){return '<button class="chip" data-act="ttg-dur" data-m="'+x[0]+'" aria-pressed="'+(on&&e-s===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div></div>';
  }
  var f='<div class="df">'+(on&&mode!=='view'?'<button class="btn" data-act="ttg-off">시간표에서 빼기</button>':'')+'<button class="btn" data-act="ttg-cal">달력에서 열기</button>'+(mode==='full'?'<button class="btn primary" data-act="goal-toggle" data-date="'+d+'" data-id="'+esc(g.id)+'">'+(g.done?'완료 취소':'끝냈어요')+'</button>':'')+'</div>';
  return dlg('',{id:'ttg',t:'할 일 시간'},b,f);
}
function modalTTF(V){
  var x=ttSelFixed();if(!x){S.modal=null;return '';}
  var d=S.ttSel.d,lab=x.t||TTK[x.k],ro=modeOf(d)==='view',dws=x.tpl?[1,2,3,4,5,6,0].filter(function(i){return x.dw.charAt(i)==='1';}).map(function(i){return DOW[i];}).join(' '):'';
  var b='<div class="ttsum fx k-'+x.k+'"'+(x.sid?' style="--sc:'+subCol(V,x.sid)+'"':'')+'><i></i><div><b>'+esc(lab)+'</b><small>'+esc(TTK[x.k])+' · '+(x.tpl?'매주 '+esc(dws)+' '+fmtHM(x.bs)+'~'+fmtHM(x.be):'이 날만 있는 일정')+'</small></div></div>';
  if(x.off)b+='<p class="hint" style="margin-top:12px">이 날은 빼 두었습니다.</p>';
  else b+='<div class="fld"><h3>'+esc(shortDate(d)+' '+DOW[pd(d).getDay()]+'요일')+' 시간'+(x.tpl?'<small>여기서 바꾸면 이 날만 바뀝니다</small>':'')+'</h3>'+ttTimeRow('ttf-time',x.s,x.e,ro)+'</div>';
  if(x.k==='school'){var sl0=schLine(V,d);b+='<div class="fld"><h3>이 날 교시</h3>'+(sl0?'<div class="schline">'+sl0+'</div>':'<p class="hint">학교 시간표를 넣으면 교시별 과목이 여기에 보입니다.</p>')+'</div>';}
  var f=ro?(x.k==='school'?'<div class="df"><button class="btn" data-act="open" data-modal="school">학교 시간표</button></div>':''):'<div class="df">'+(x.k==='school'?'<button class="btn" data-act="open" data-modal="school">학교 시간표</button>':'')+(x.moved?'<button class="btn" data-act="ttf-reset">원래 시간으로</button>':'')+(x.off?'':'<button class="btn" data-act="ttf-off">'+(x.one?'지우기':'이 날만 빼기')+'</button>')+(x.tpl?'<button class="btn primary" data-act="ttf-edit">매주 시간표 고치기</button>':'')+'</div>';
  return dlg('',{id:'ttf',t:'고정 일정'},b,f);
}
function modalTTSlot(V){
  var sl=S.ttSlot;if(!sl){S.modal=null;return '';}
  var d=sl.d,un=dayOf(V,V.me,d).goals.filter(function(g){return !g.done&&!placed(g);}),xd=S.ttXDur||60,xk=S.ttXK||'etc';
  var b='<div class="fld" style="margin-top:0"><h3>이 시간에 할 일 넣기<small>'+fmtHM(sl.m)+'부터 1시간</small></h3>';
  if(un.length)b+='<div class="ttpicks">'+un.map(function(g){var sub=g.sid&&V.subName[g.sid];return '<button class="ttpk" data-act="tt-put" data-id="'+esc(g.id)+'" style="--sc:'+goalCol(V,g)+'"><i></i><span>'+esc(g.text)+'</span>'+(sub?'<small>'+esc(sub)+'</small>':'')+'</button>';}).join('')+'</div>';
  else b+='<p class="hint">시간표에 아직 안 넣은 할 일이 없습니다.</p>';
  b+='<div class="row" style="margin-top:10px"><button class="btn small" data-act="open" data-modal="compose" data-date="'+d+'" data-at="'+sl.m+'">새 할 일 적어서 넣기</button></div></div>';
  b+='<div class="fld"><h3>이 날만 일정 넣기<small>보강, 모임처럼 하루짜리</small></h3><input type="text" data-draft="ttXT" data-enter="tt-xadd" maxlength="20" placeholder="예: 학원 보강" aria-label="일정 이름">';
  b+='<div class="chips" style="margin-top:10px">'+[['academy','학원'],['etc','기타']].map(function(x){return '<button class="chip" data-act="tt-xk" data-v="'+x[0]+'" aria-pressed="'+(xk===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  b+='<div class="chips" style="margin-top:8px">'+TT_DURS.map(function(x){return '<button class="chip" data-act="tt-xdur" data-m="'+x[0]+'" aria-pressed="'+(xd===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div><div class="row" style="margin-top:10px"><button class="btn" data-act="tt-xadd">일정 넣기</button></div></div>';
  return dlg('',{id:'ttslot',t:esc(shortDate(d)+' '+DOW[pd(d).getDay()]+'요일 '+fmtHM(sl.m))},b);
}
function modalTTSet(V){
  var tab=S.ttTab||'fixed',T=ttData(V),f='';
  var b='<div class="seg mini ttsets" style="--i:'+['fixed','color','win'].indexOf(tab)+';--n:3" role="group" aria-label="설정 종류">'+[['fixed','고정 시간표'],['color','과목 색'],['win','공부 시간']].map(function(x){return '<button data-act="tt-tab" data-v="'+x[0]+'" aria-pressed="'+(tab===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  if(tab==='fixed'){
    var E=S.ttEd;
    if(E){
      b+='<div class="fld"><h3>종류</h3><div class="chips">'+['school','academy','etc'].map(function(k){return '<button class="chip" data-act="tt-ed-set" data-k="k" data-v="'+k+'" aria-pressed="'+(E.k===k?'true':'false')+'">'+TTK[k]+'</button>';}).join('')+'</div></div>';
      b+='<div class="fld"><h3>이름</h3><input type="text" id="ttEdT" data-draft="ttEdT" maxlength="20" placeholder="'+(E.k==='academy'?'예: 수학 학원':E.k==='school'?'예: 학교':'예: 독서실')+'" aria-label="일정 이름"></div>';
      b+='<div class="fld"><h3>요일</h3><div class="dows">'+[1,2,3,4,5,6,0].map(function(i){return '<button class="dw'+(i===0?' sun':'')+'" data-act="tt-ed-dow" data-v="'+i+'" aria-pressed="'+(E.d.charAt(i)==='1'?'true':'false')+'">'+DOW[i]+'</button>';}).join('')+'</div></div>';
      b+='<div class="fld"><h3>시간</h3>'+ttTimeRow('tt-ed-time',E.s,E.e)+'</div>';
      b+='<div class="fld"><h3>과목<small>선택, 고르면 그 과목 색 줄이 붙습니다</small></h3><div class="chips">'+mySubs(V).map(function(s){return '<button class="chip" data-act="tt-ed-set" data-k="sid" data-v="'+esc(s.id)+'" aria-pressed="'+(E.sid===s.id?'true':'false')+'">'+esc(s.name)+'</button>';}).join('')+'</div></div>';
      f='<div class="df">'+(E.id?'<button class="btn" data-act="tt-ed-del">'+(S.confirm==='ttdel:'+E.id?'한 번 더 누르면 삭제':'삭제')+'</button>':'')+'<button class="btn" data-act="tt-ed-x">취소</button><button class="btn primary" data-act="tt-ed-save">저장</button></div>';
    }else{
      if(!T.b.length)b+='<p class="hint" style="margin-top:14px">학교와 학원처럼 매주 같은 시간에 있는 일정을 넣어 두면 시간표에 고정으로 깔립니다. 시간표에서 끌어 옮기면 그 날만 바뀝니다.</p>';
      else{
        b+='<div class="ttrows">';
        T.b.slice().sort(function(a,c){return a.s-c.s;}).forEach(function(x){
          var k=TTK[x.k]?x.k:'etc',dws=[1,2,3,4,5,6,0].filter(function(i){return String(x.d||'').charAt(i)==='1';}).map(function(i){return DOW[i];}).join(' ');
          b+='<button class="ttrow k-'+k+'" data-act="tt-ed" data-id="'+esc(x.id)+'"'+(x.sid?' style="--sc:'+subCol(V,x.sid)+'"':'')+'><i></i><span><b>'+esc(x.t||TTK[k])+'</b><small>'+esc(dws||'요일 없음')+' · '+fmtHM(x.s)+'~'+fmtHM(x.e)+'</small></span><em>고치기</em></button>';
        });
        b+='</div>';
      }
      b+='<div class="row" style="margin-top:14px">'+[['school','학교 넣기'],['academy','학원 넣기'],['etc','기타 넣기']].map(function(x){return '<button class="btn small'+(x[0]==='school'&&!T.b.length?' primary':'')+'" data-act="tt-new" data-v="'+x[0]+'">'+x[1]+'</button>';}).join('')+'</div>';
    }
  }else if(tab==='color'){
    b+='<p class="hint" style="margin:14px 0 4px">시간표와 할 일 목록에 쓰는 내 과목 색입니다. 과목이 없거나 수행평가 같은 기타 일은 회색으로 보입니다.</p><div class="scols">';
    V.subs.forEach(function(s){
      var cur=subCol(V,s.id);
      b+='<div class="scrow"><span><i style="background:'+cur+'"></i>'+esc(s.name)+'</span><div class="sws">'+SCOLS.map(function(c){return '<button class="sw2" data-act="scol" data-id="'+esc(s.id)+'" data-v="'+c[0]+'" style="--c:'+c[1]+'" aria-pressed="'+(cur===c[1]?'true':'false')+'" aria-label="'+esc(s.name)+' '+c[2]+'" title="'+c[2]+'"></button>';}).join('')+'<button class="sw2" data-act="scol" data-id="'+esc(s.id)+'" data-v="g" style="--c:'+SGRAY+'" aria-pressed="'+(cur===SGRAY?'true':'false')+'" aria-label="'+esc(s.name)+' 회색" title="회색"></button></div></div>';
    });
    b+='</div>';
  }else{
    var w=ttWin(V);
    b+='<p class="hint" style="margin:14px 0 4px">빈 시간에 채우기를 누르면 이 범위 안에서 고정 일정이 없는 시간에 할 일을 1시간씩, 사이에 10분씩 쉬며 차례로 넣습니다.</p><div class="fld"><h3>공부하는 시간</h3>'+ttTimeRow('tt-win',w.s,w.e)+'</div>';
  }
  return dlg('wide',{id:'ttset',t:'시간표 설정'},b,f);
}

/* ---------- 끌어 옮기기 ---------- */
var DR=null;
function ttDragOk(){return S.vtab==='cal'&&S.calMode==='tt'&&!S.modal;}
function ttDragCancel(){if(!DR)return;clearTimeout(DR.timer);clearTimeout(DR.pt);if(DR.src)DR.src.classList.remove('press');DR=null;}
function ttDragEnd(){
  if(!DR)return;cancelAnimationFrame(DR.raf);clearTimeout(DR.timer);clearTimeout(DR.pt);
  if(DR.gh)DR.gh.remove();if(DR.pv)DR.pv.remove();
  if(DR.src)DR.src.classList.remove('lifting','resizing','press');
  document.documentElement.classList.remove('ttdragging');
  S.drag=false;window.__ttDragEnd=Date.now();
}
function ttDragStart(){
  var src=DR.src;clearTimeout(DR.timer);clearTimeout(DR.pt);src.classList.remove('press');
  if(!document.body.contains(src)){DR=null;return;}
  DR.on=true;S.drag=true;document.documentElement.classList.add('ttdragging');
  DR.d=src.getAttribute('data-d');DR.gid=src.getAttribute('data-id');DR.s0=+src.getAttribute('data-s');DR.e0=+src.getAttribute('data-e');DR.dur=+src.getAttribute('data-dur')||60;
  DR.sc=document.getElementById('ttScroll');DR.col0=src.closest('.ttcol');DR.color=src.style.getPropertyValue('--sc')||'';
  if(DR.rs){src.classList.add('resizing');DR.e=DR.e0;ttAuto();return;}
  var anyCol=DR.col0||document.querySelector('.ttcol:not(.ro)')||document.querySelector('.ttcol'),hh=anyCol?+anyCol.getAttribute('data-hh'):52;
  var r=src.getBoundingClientRect(),gh;
  if(DR.kind==='q'){
    var w=anyCol?anyCol.getBoundingClientRect().width:120;
    gh=document.createElement('div');gh.className='ttb td ttghost';gh.innerHTML='<span class="tbt"></span><small>1시간</small>';gh.firstChild.textContent=src.textContent;
    gh.style.width=Math.max(96,w-6)+'px';gh.style.height=Math.round(DR.dur*hh/60)+'px';gh.style.left=(DR.x0-22)+'px';gh.style.top=(DR.y0-14)+'px';DR.offMin=14*60/hh;
  }else{
    gh=src.cloneNode(true);gh.removeAttribute('id');gh.removeAttribute('data-act');gh.removeAttribute('data-tdrag');gh.classList.add('ttghost');
    gh.style.width=r.width+'px';gh.style.height=r.height+'px';gh.style.left=r.left+'px';gh.style.top=r.top+'px';DR.offMin=(DR.y0-r.top)*60/hh;src.classList.add('lifting');
  }
  if(DR.color)gh.style.setProperty('--sc',DR.color);
  document.body.appendChild(gh);DR.gh=gh;
  requestAnimationFrame(function(){if(DR&&DR.gh)DR.gh.classList.add('up');});
  ttAuto();ttDragMove();
}
function ttPrev(col,m,dur,hh,r0){
  var pv=DR.pv;
  if(!col){if(pv){pv.remove();DR.pv=null;}return;}
  if(!pv||pv.parentNode!==col){if(pv)pv.remove();pv=document.createElement('div');pv.className='ttprev';if(DR.color)pv.style.setProperty('--sc',DR.color);pv.innerHTML='<b></b>';col.appendChild(pv);DR.pv=pv;}
  pv.style.top=((m-r0)*hh/60)+'px';pv.style.height=(dur*hh/60)+'px';pv.firstChild.textContent=fmtHM(m)+'~'+fmtHM(m+dur);
}
function ttDragMove(){
  if(!DR||!DR.on)return;
  if(DR.rs){
    var c0=DR.col0,hh0=+c0.getAttribute('data-hh'),rc0=c0.getBoundingClientRect(),me=snap10(+c0.getAttribute('data-r0')+(DR.y-rc0.top)*60/hh0);
    me=Math.max(DR.s0+20,Math.min(+c0.getAttribute('data-r1'),me));DR.e=me;
    DR.src.style.height=((me-DR.s0)*hh0/60)+'px';var sm=DR.src.querySelector('small');if(sm)sm.textContent=fmtHM(DR.s0)+'~'+fmtHM(me);
    return;
  }
  DR.gh.style.transform='translate3d('+(DR.x-DR.x0)+'px,'+(DR.y-DR.y0)+'px,0)';
  var col=null,els=document.elementsFromPoint?document.elementsFromPoint(DR.x,DR.y):[];
  for(var i=0;i<els.length;i++){var c=els[i].closest&&els[i].closest('.ttcol');if(c){col=c;break;}}
  if(col&&(col.classList.contains('ro')||(DR.kind==='f'&&col.getAttribute('data-d')!==DR.d)))col=null;
  if(!col){ttPrev(null);DR.tgt=null;return;}
  var hh=+col.getAttribute('data-hh'),r0=+col.getAttribute('data-r0'),r1=+col.getAttribute('data-r1'),rc=col.getBoundingClientRect(),dur=DR.dur;
  var m=snap10(r0+(DR.y-rc.top)*60/hh-DR.offMin);m=Math.max(r0,Math.min(r1-dur,m));
  DR.tgt={d:col.getAttribute('data-d'),s:m,e:m+dur};
  ttPrev(col,m,dur,hh,r0);
}
function ttAuto(){
  if(!DR||!DR.on)return;
  var sc=DR.sc;
  if(sc){
    var r=sc.getBoundingClientRect(),hd=sc.querySelector('.tthc'),top=r.top+(hd?hd.offsetHeight:0),left=r.left+46,E=46,dy=0,dx=0;
    if(DR.y<top+E)dy=-Math.min(18,Math.ceil((top+E-DR.y)/3));else if(DR.y>r.bottom-E)dy=Math.min(18,Math.ceil((DR.y-(r.bottom-E))/3));
    if(DR.x<left+E/2&&sc.scrollLeft>0)dx=-Math.min(16,Math.ceil((left+E/2-DR.x)/3));else if(DR.x>r.right-E/2)dx=Math.min(16,Math.ceil((DR.x-(r.right-E/2))/3));
    if(dy||dx){var y0=sc.scrollTop,x0=sc.scrollLeft;sc.scrollTop+=dy;sc.scrollLeft+=dx;if(sc.scrollTop!==y0||sc.scrollLeft!==x0)ttDragMove();}
  }
  DR.raf=requestAnimationFrame(ttAuto);
}
function ttDrop(){
  var R=DR;ttDragEnd();DR=null;
  if(R.rs){if(R.e!=null&&R.e!==R.e0)ttCommit(R.kind,R.d,R.gid,R.s0,R.e,R.d);else render();return;}
  var tg=R.tgt;
  if(!tg||(R.kind!=='q'&&tg.d===R.d&&tg.s===R.s0)){render();return;}
  if(R.kind!=='q'&&tg.d===R.d&&R.col0){var hh=+R.col0.getAttribute('data-hh'),r0=+R.col0.getAttribute('data-r0');R.src.style.transition='none';R.src.style.top=((tg.s-r0)*hh/60)+'px';void R.src.offsetWidth;R.src.style.transition='';}
  ttCommit(R.kind,R.d,R.gid,tg.s,tg.e,tg.d);
}
document.addEventListener('pointerdown',function(e){
  if(DR||!ttDragOk()||e.button>0||e.isPrimary===false)return;
  var tg=e.target;if(!tg||!tg.closest)return;
  var src=tg.closest('[data-tdrag]');if(!src||tg.closest('.ttbchk'))return;
  var rs=!!tg.closest('.tbr'),touch=e.pointerType==='touch',quick=!touch||rs||src.getAttribute('data-tdrag')==='q';
  DR={src:src,kind:src.getAttribute('data-tdrag'),rs:rs,quick:quick,id:e.pointerId,x0:e.clientX,y0:e.clientY,x:e.clientX,y:e.clientY,on:false};
  if(!quick){DR.timer=setTimeout(function(){if(DR&&!DR.on)ttDragStart();},300);DR.pt=setTimeout(function(){if(DR&&!DR.on&&DR.src)DR.src.classList.add('press');},120);}
  if(rs)e.preventDefault();
});
document.addEventListener('pointermove',function(e){
  if(!DR||e.pointerId!==DR.id)return;
  DR.x=e.clientX;DR.y=e.clientY;
  if(!DR.on){
    var dist=Math.abs(DR.x-DR.x0)+Math.abs(DR.y-DR.y0);
    if(!DR.quick){if(dist>12)ttDragCancel();return;}
    if(dist<6)return;
    ttDragStart();
  }
  if(DR&&DR.on){e.preventDefault();ttDragMove();}
},{passive:false});
document.addEventListener('pointerup',function(e){if(!DR||e.pointerId!==DR.id)return;if(DR.on)ttDrop();else ttDragCancel();});
document.addEventListener('pointercancel',function(e){if(!DR||e.pointerId!==DR.id)return;if(DR.on){ttDragEnd();DR=null;render();}else ttDragCancel();});
document.addEventListener('touchmove',function(e){if(DR&&DR.on)e.preventDefault();},{passive:false});
document.addEventListener('contextmenu',function(e){if(DR)e.preventDefault();});
