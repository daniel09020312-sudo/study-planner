# ---------------------------------------------------------------- 10/10 저녁: 마감 있는 할 일, 날짜별 배분, 묶어 보기, 편의 기능
# 하루 할 일 개수 한도 8 -> 12 (나눠 넣은 할 일 때문에)
s = s.replace("if(d.goals.length<8)", "if(d.goals.length<GMAX)").replace("if(d.goals.length>=8)", "if(d.goals.length>=GMAX)")
s = s.replace("할 일은 하루 8개까지 넣을 수 있습니다.", "할 일은 하루 '+GMAX+'개까지 넣을 수 있습니다.")
assert "length>=8" not in s and "length<8)" not in s

# 저장소: plans 모음 추가
sub("var COLLS=['subjects','days','progress','quiz','events','live','replies','msgs','songs','duels','spins','locks','flags'];",
    "var COLLS=['subjects','days','progress','quiz','events','live','replies','msgs','songs','duels','spins','locks','flags','plans'];")
sub("S.locks={};S.flags={};", "S.locks={};S.flags={};S.plans={};S.pl=null;S.plOpen={};S.plShowDone=false;S.plGroup=lsGet('gbb_plgroup')==='sub'?'sub':'due';S.gGroup=(function(v){return v==='sub'||v==='plan'?v:'none';})(lsGet('gbb_ggroup'));S.gSel=null;S.gEdit=null;")
sub("replies:merged('replies'),byId:{}", "replies:merged('replies'),plans:merged('plans'),byId:{}")

# 여러 날짜를 한꺼번에 저장할 때 하나씩 차례로 저장 (한꺼번에 보내면 저장소가 거절할 수 있음)
sub("function save(path,data){\n  if(!canWrite())return;\n",
    "function save(path,data){\n  if(!canWrite())return;\n  if(BQ.has[path]){O[path]=data;if(BQ.list.indexOf(path)<0)BQ.list.push(path);if(!BQ.busy)bqRun();return;}\n")
sub("function wait(ms){return new Promise(function(r){setTimeout(r,ms);});}", r"""function wait(ms){return new Promise(function(r){setTimeout(r,ms);});}
var BQ={list:[],has:{},busy:false};
function queueWrite(path,data){
  if(!canWrite())return;
  if(W[path]&&W[path].busy){save(path,data);return;}
  O[path]=data;BQ.has[path]=1;if(BQ.list.indexOf(path)<0)BQ.list.push(path);
  if(!BQ.busy)bqRun();
}
async function bqRun(){
  BQ.busy=true;
  while(BQ.list.length){
    var path=BQ.list.shift();
    if(!Object.prototype.hasOwnProperty.call(O,path)){delete BQ.has[path];continue;}
    var d=O[path],tries=0,ok=false,code=null;
    for(;;){
      try{await S.net.write(path,d);ok=true;break;}
      catch(e){code=e&&e.code;if((code==='resource_exhausted'||code==='unavailable'||!code)&&tries<4){tries++;await wait(500*tries+Math.random()*400);continue;}break;}
    }
    if(ok){if(O[path]===d)commit(path,d);}
    else{writeFailed(code);if(O[path]===d)delete O[path];}
    if(BQ.list.indexOf(path)<0)delete BQ.has[path];
  }
  BQ.busy=false;render();
}""")

# ---- 마감 있는 할 일 도구
sub("function carryList(V,date){", r"""var GMAX=12;
function plText(type,unit,note,amt){
  var parts=[];if(type)parts.push(type);if(amt>0)parts.push(amt+(unit||'문제'));
  var t=parts.join(' ');note=String(note||'').trim();
  return note?(t?t+' ('+note+')':note):t;
}
function planList(V){
  if(V._pl)return V._pl;
  if(!V.me)return V._pl=[];
  var parts={},t=today(),pre=V.me+'_';
  Object.keys(V.days).forEach(function(k){
    if(k.indexOf(pre)!==0)return;var date=k.slice(pre.length);
    arr(obj(V.days[k]).goals).forEach(function(g){if(g&&g.pid)(parts[g.pid]=parts[g.pid]||[]).push({date:date,id:g.id,done:!!g.done,part:g.part||'',amt:+g.amt||0,text:String(g.text||'')});});
  });
  return V._pl=Object.keys(V.plans).map(function(id){
    var p=Object.assign({id:id},obj(V.plans[id]));if(p.mid!==V.me||!p.due)return null;
    var ps=(parts[id]||[]).sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:0;});
    p.parts=ps;p.n=ps.length;p.dn=ps.filter(function(x){return x.done;}).length;
    p.late=ps.filter(function(x){return !x.done&&x.date<t;}).length;
    p.todayPart=ps.filter(function(x){return x.date===t;})[0]||null;
    p.finished=p.n>0&&p.dn===p.n;
    p.amtDone=ps.reduce(function(s2,x){return s2+(x.done?x.amt:0);},0);
    p.label=p.mode==='repeat'?plText(p.type,p.unit,p.note,0)+(p.per>0?', 매일 '+p.per+(p.unit||'문제'):', 매일'):plText(p.type,p.unit,p.note,+p.total||0);
    return p;
  }).filter(Boolean).sort(function(a,b){return (a.finished?1:0)-(b.finished?1:0)||(a.due<b.due?-1:a.due>b.due?1:0)||((+a.at||0)-(+b.at||0));});
}
function dueMap(V){if(V._dm)return V._dm;var m={};planList(V).forEach(function(p){if(!p.finished)(m[p.due]=m[p.due]||[]).push(p);});return V._dm=m;}
function ddayLabel(d){var n=diffDays(today(),d);return n===0?'오늘 마감':n<0?'마감 지남':'D-'+n;}
function plDows(pl){var s2=String(pl.dows||'1111111');return [0,1,2,3,4,5,6].map(function(i){return s2.charAt(i)!=='0';});}
function plDates(pl){
  var t=today(),out=[];if(!pl.due)return out;
  if(pl.mode==='once')return pl.due>=t?[pl.due]:[];
  var dw=plDows(pl),end=pl.mode==='split'&&pl.early?addDays(pl.due,-1):pl.due,d=(pl.start&&pl.start>t)?pl.start:t;
  for(;d<=end&&out.length<70;d=addDays(d,1)){if(dw[pd(d).getDay()])out.push(d);}
  return out;
}
function plAlloc(V,pl){
  var off=obj(pl.off),rows=plDates(pl).map(function(d){return {d:d,full:dayOf(V,V.me,d).goals.length>=GMAX,off:!!off[d],amt:0};});
  var use=rows.filter(function(r){return !r.full&&!r.off;}),n=use.length,tot=Math.max(0,+pl.total||0);
  if(n&&pl.mode==='split'&&tot>0){
    if(tot>=n){var base=Math.floor(tot/n),rem=tot-base*n;use.forEach(function(r,i){r.amt=base+(i<rem?1:0);});}
    else{for(var i=0;i<tot;i++)use[Math.floor(i*n/tot)].amt+=1;}
    use=use.filter(function(r){if(!r.amt)r.rest=true;return r.amt>0;});
  }else if(pl.mode==='repeat')use.forEach(function(r){r.amt=Math.max(0,+pl.per||0);});
  else if(pl.mode==='once')use.forEach(function(r){r.amt=tot;});
  use.forEach(function(r,i){r.on=true;r.part=(i+1)+'/'+use.length;});
  return {rows:rows,use:use};
}
function dayDoc(V,date){return clone(dayOf(V,V.me,date));}
function cleanDay(d){if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;return d;}
function putPlanGoals(pid,p,use){
  use.forEach(function(r){
    var V=view(),d=dayDoc(V,r.d);
    if(d.goals.length>=GMAX)return;
    d.goals.push({id:rid('g'),text:plText(p.type,p.unit,p.note,r.amt).slice(0,90)||'할 일',sid:p.sid||'',done:false,pid:pid,part:p.mode==='once'?'':r.part,amt:r.amt||0});
    queueWrite('days/'+V.me+'_'+r.d,cleanDay(d));
  });
}
function dropPlanGoals(p,onlyUndone){
  var byDate={};p.parts.forEach(function(x){if(!onlyUndone||!x.done)(byDate[x.date]=byDate[x.date]||[]).push(x.id);});
  Object.keys(byDate).forEach(function(date){
    var V=view(),d=dayDoc(V,date),ids=byDate[date];
    d.goals=d.goals.filter(function(g){return ids.indexOf(g.id)<0;});if(ids.indexOf(d.focus)>=0)d.focus=null;
    queueWrite('days/'+V.me+'_'+date,cleanDay(d));
  });
}
function dueChoices(V){
  var t=today(),out=[],seen={};
  function add(d,l){if(!d||d<=t||d>'2026-12-31'||seen[d])return;seen[d]=1;out.push({d:d,l:l});}
  var dw=pd(t).getDay();
  add(addDays(t,1),'내일');add(addDays(t,2),'모레');
  if(dw<5)add(addDays(t,5-dw),'이번 주 금요일');
  add(addDays(t,((8-dw)%7)||7),'다음 주 월요일');
  add(addDays(t,7),'1주 뒤');add(addDays(t,14),'2주 뒤');
  var evs=[];
  Object.keys(V.evByDate).forEach(function(d){if(d>t)V.evByDate[d].forEach(function(e){if(e.mid===V.me||e.shared)evs.push({d:d,l:cut(e.title,10)});});});
  Object.keys(EVENTS).forEach(function(d){if(d>t&&!EVENTS[d].off&&evs.length<12)evs.push({d:d,l:EVENTS[d].s});});
  evs.sort(function(a,b){return a.d<b.d?-1:1;}).slice(0,5).forEach(function(e){add(e.d,shortDate(e.d)+' '+e.l);});
  return out;
}
function newPlan(){return {sid:'',type:'',unit:'',total:0,per:0,due:'',start:today(),mode:'split',dows:'1111111',off:{},early:false};}
function modalPlan(V){
  var pl=S.pl,t=today(),subs=mySubs(V),sub=V.subById[pl.sid],b='',note=String(S.draft.plNote||'').trim(),u=pl.unit||'문제';
  var types=(sub&&sub.items.length?sub.items.map(function(it){return it.label;}):DEFAULT_ITEMS).concat(EXTRA_TYPES);
  b+='<div class="fld"><h3>어떻게 할까요</h3><div class="chips">'+[['split','날짜별로 나눠 하기'],['repeat','매일 같은 양 하기'],['once','마감일에 한 번']].map(function(x){return chipBtn('pl-set','mode',x[0],x[1],pl.mode===x[0]);}).join('')+'</div></div>';
  b+='<div class="fld"><h3>과목</h3><div class="chips">'+subs.map(function(s2){return chipBtn('pl-set','sid',s2.id,s2.name,pl.sid===s2.id);}).join('')+'</div></div>';
  b+='<div class="fld"><h3>할 일</h3><div class="chips">'+types.map(function(x){return chipBtn('pl-set','type',x,x,pl.type===x);}).join('')+'</div></div>';
  var av=pl.mode==='repeat'?pl.per:pl.total;
  b+='<div class="fld"><h3>'+(pl.mode==='repeat'?'하루 분량':'전체 분량')+'<small>'+(pl.mode==='split'?'나눌 양, 비워 두면 횟수로만 나눕니다':'선택')+'</small></h3><div class="amt"><button data-act="pl-amt" data-d="-10" aria-label="10 줄이기">-10</button><button data-act="pl-amt" data-d="-1" aria-label="1 줄이기">-1</button><b>'+(av||0)+'</b><button data-act="pl-amt" data-d="1" aria-label="1 늘리기">+1</button><button data-act="pl-amt" data-d="10" aria-label="10 늘리기">+10</button></div>';
  b+='<div class="chips">'+UNITS.map(function(x){return chipBtn('pl-set','unit',x,x,u===x&&av>0);}).join('')+'</div></div>';
  b+='<div class="fld"><h3>자세히<small>책 이름, 범위 등</small></h3><input type="text" data-draft="plNote" data-live="1" maxlength="60" placeholder="예: 쎈 3단원, 120~180쪽" aria-label="자세한 내용"></div>';
  b+='<div class="fld"><h3>'+(pl.mode==='repeat'?'언제까지':'마감')+'</h3><div class="chips">'+dueChoices(V).map(function(x){return chipBtn('pl-due','d',x.d,x.l,pl.due===x.d);}).join('')+'</div><div class="drow"><span>날짜 직접 고르기</span><input type="date" data-chg="pl-due" min="'+addDays(t,pl.mode==='once'?0:1)+'" max="2026-12-31" value="'+esc(pl.due)+'" aria-label="마감 날짜"></div></div>';
  if(pl.mode!=='once'){
    var dw=plDows(pl);
    b+='<div class="fld"><h3>언제부터</h3><div class="chips">'+chipBtn('pl-start','d',t,'오늘',pl.start===t)+chipBtn('pl-start','d',addDays(t,1),'내일',pl.start===addDays(t,1))+(t<START?chipBtn('pl-start','d',START,'새 주기 시작일',pl.start===START):'')+'</div><div class="drow"><span>날짜 직접 고르기</span><input type="date" data-chg="pl-start" min="'+t+'" max="2026-12-31" value="'+esc(pl.start)+'" aria-label="시작 날짜"></div>';
    b+='<h3 style="margin-top:12px">하는 요일</h3><div class="chips dows">'+DOW.map(function(x,i){return '<button class="chip" data-act="pl-dow" data-v="'+i+'" aria-pressed="'+(dw[i]?'true':'false')+'">'+x+'</button>';}).join('')+'</div>';
    if(pl.mode==='split')b+='<div class="chips" style="margin-top:8px">'+chipBtn('pl-early','v','1','마감 전날까지 끝내기',!!pl.early)+'</div>';
    b+='</div>';
  }
  var A=pl.due?plAlloc(V,pl):null,txt=plText(pl.type,pl.unit,note,0);
  if(A){
    b+='<div class="fld"><h3>날짜별로 이렇게 들어갑니다<small>'+(pl.mode==='once'?'':'날짜를 누르면 빼거나 다시 넣습니다')+'</small></h3><div class="pdays">';
    A.rows.forEach(function(r){
      var lab=shortDate(r.d)+' '+DOW[pd(r.d).getDay()],val=r.full?'가득 참':r.off?'뺌':r.rest?'쉬는 날':(r.amt>0?r.amt+u:(pl.mode==='split'?r.part:'할 일'));
      b+='<button class="pday'+(r.on?' on':'')+(r.full?' full':'')+(r.off?' off':'')+'" data-act="pl-day" data-d="'+r.d+'"'+(r.full||pl.mode==='once'?' disabled':'')+'><small>'+lab+'</small><b>'+esc(val)+'</b></button>';
    });
    b+='</div>';
    if(!A.rows.length)b+='<p class="hint">고른 기간에 해당하는 날이 없습니다. 시작일이나 요일을 바꿔 보세요.</p>';
    b+='</div>';
  }
  var sum='',ok=!!(txt&&A&&A.use.length);
  if(A&&A.use.length){
    var n=A.use.length,amts=A.use.map(function(r){return r.amt;}),mn=Math.min.apply(null,amts),mx=Math.max.apply(null,amts),fullN=A.rows.filter(function(r){return r.full;}).length;
    if(pl.mode==='once')sum=shortDate(pl.due)+' 할 일에 들어갑니다.';
    else if(pl.mode==='repeat')sum=n+'일 동안 매일'+(pl.per>0?' '+pl.per+u:'')+' 할 일로 들어갑니다.';
    else if(pl.total>0)sum=n+'일에 나눠 하루 '+(mn===mx?mn+u:mn+'~'+mx+u)+'씩 들어갑니다.';
    else sum=n+'일에 1/'+n+'부터 '+n+'/'+n+'까지 나눠 들어갑니다.';
    if(fullN)sum+=' 할 일이 가득 찬 '+fullN+'일은 뺐습니다.';
  }else if(A)sum='들어갈 날이 없습니다.';
  var f='<div class="preview"><small>'+(sum?esc(sum):'마감을 고르면 날짜별로 나눠 보여 줍니다')+'</small><p>'+(txt?(sub?'<em class="tag">'+esc(sub.name)+'</em>':'')+'<span>'+esc(pl.mode==='repeat'?txt+(pl.per>0?' 매일 '+pl.per+u:''):plText(pl.type,pl.unit,note,pl.total))+'</span>'+(pl.due?'<em class="tag a">'+esc(shortDate(pl.due))+'까지</em>':''):'<span class="ph">할 일을 고르거나 자세히에 적으세요</span>')+'</p></div>';
  f+='<div class="df"><button class="btn primary" data-act="pl-add"'+(ok?'':' disabled')+'>할 일에 넣기</button></div>';
  return dlg('wide',{id:'plan',t:'마감 있는 할 일'},b,f);
}
function planRow(V,p){
  var t=today(),open=!!S.plOpen[p.id],sub=p.sid&&V.subName[p.sid],pct=p.n?Math.round(p.dn/p.n*100):0,u=p.unit||'문제';
  var meta=shortDate(p.due)+' '+DOW[pd(p.due).getDay()]+'까지';
  if(p.n)meta+=', '+p.dn+'/'+p.n+' 완료';
  if(p.mode==='split'&&+p.total>0)meta+=', '+p.amtDone+'/'+p.total+u;
  var h='<div class="plrow'+(p.finished?' fin':'')+(p.late?' late':'')+'" id="pl-'+esc(p.id)+'"><button class="plmain" data-act="pl-open" data-id="'+esc(p.id)+'" aria-expanded="'+(open?'true':'false')+'"><span class="pltop">'+(sub?'<em class="tag">'+esc(sub)+'</em>':'')+'<b>'+esc(p.label)+'</b></span><span class="plbar" aria-hidden="true"><i style="width:'+pct+'%"></i></span><small>'+esc(meta)+(p.late?' <em class="tag r">밀린 '+p.late+'개</em>':'')+(p.todayPart&&!p.todayPart.done?' <em class="tag a">오늘 몫 있음</em>':'')+(!p.n?' <em class="tag">들어간 할 일 없음</em>':'')+'</small></button><span class="dd'+(p.finished?'':p.due<=addDays(t,1)?' hot':'')+'">'+(p.finished?'완료':ddayLabel(p.due))+'</span></div>';
  if(open){
    h+='<div class="plbody" id="pb-'+esc(p.id)+'">';
    if(p.parts.length){
      h+='<ul class="pparts">';
      p.parts.forEach(function(x){
        var m=modeOf(x.date);
        h+='<li class="'+(x.done?'done':'')+(x.date===t?' today':'')+(!x.done&&x.date<t?' late':'')+'"><button class="chk'+(x.done?' on':'')+'" data-act="goal-toggle" data-date="'+x.date+'" data-id="'+esc(x.id)+'" aria-pressed="'+(x.done?'true':'false')+'" aria-label="'+esc(x.text)+' 완료 표시"'+(m!=='full'?' disabled':'')+'><span></span></button><button class="pdate" data-act="pick-date" data-d="'+x.date+'">'+esc(shortDate(x.date)+' '+DOW[pd(x.date).getDay()])+'</button><span class="ptxt">'+esc(x.text)+(x.part?' <em class="tag">'+esc(x.part)+'</em>':'')+'</span></li>';
      });
      h+='</ul>';
    }
    h+='<div class="row" style="margin-top:10px">';
    if(p.mode==='split'&&!p.finished&&p.due>=t)h+='<button class="btn small soft" data-act="pl-redo" data-id="'+esc(p.id)+'">남은 것 오늘부터 다시 나누기</button>';
    if(p.mode==='once'&&!p.finished&&p.parts[0]&&p.parts[0].date!==t)h+='<button class="btn small soft" data-act="pl-today" data-id="'+esc(p.id)+'">오늘 하기</button>';
    h+='<button class="del" data-act="pl-del" data-id="'+esc(p.id)+'">'+(S.confirm==='pl:'+p.id?'한 번 더 누르면 삭제':'삭제')+'</button></div>';
    if(p.mode==='split'&&p.late)h+='<p class="hint" style="margin-top:6px">다시 나누면 못 한 '+p.late+'개와 앞으로 남은 몫을 합쳐 오늘부터 마감까지 다시 배분합니다.</p>';
    h+='</div>';
  }
  return h;
}
function plansCard(V,k){
  var all=planList(V),t=today(),live=all.filter(function(p){return !p.finished&&p.due>=addDays(t,-3);}),fin=all.filter(function(p){return p.finished&&p.due>=addDays(t,-14);});
  var h='<section class="card" id="c-plans" style="--k:'+k+'"><div class="ct"><h2>마감 있는 할 일'+(live.length?'<small>'+live.length+'개</small>':'')+'</h2><button class="btn small primary" data-act="open" data-modal="plan">추가</button></div>';
  if(!live.length&&!fin.length){h+='<p class="empty">며칠까지 끝낼 일을 정하면 날짜별로 나눠서 그날 할 일에 넣어 줍니다.</p>';return h+'</section>';}
  if(live.length>1)h+='<div class="seg mini" style="grid-template-columns:repeat(2,minmax(0,1fr))" role="group" aria-label="묶는 방법">'+[['due','마감 순'],['sub','과목별']].map(function(x){return '<button data-act="pl-group" data-id="'+x[0]+'" aria-pressed="'+(S.plGroup===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
  if(S.plGroup==='sub'&&live.length>1){
    var gs={},order=[];
    live.forEach(function(p){var key=p.sid&&V.subName[p.sid]?p.sid:'';if(!gs[key]){gs[key]=[];order.push(key);}gs[key].push(p);});
    order.sort(function(a,b){var sa=V.subById[a],sb=V.subById[b];return (sa?sa.order:999)-(sb?sb.order:999);});
    order.forEach(function(key){h+='<h3 class="plgh">'+esc(key?V.subName[key]:'과목 없음')+'<small>'+gs[key].length+'개</small></h3>';gs[key].forEach(function(p){h+=planRow(V,p);});});
  }else live.forEach(function(p){h+=planRow(V,p);});
  if(fin.length){
    h+='<button class="plfin" data-act="pl-fin" aria-expanded="'+(S.plShowDone?'true':'false')+'">끝낸 것 '+fin.length+'개 '+(S.plShowDone?'접기':'보기')+'</button>';
    if(S.plShowDone)fin.forEach(function(p){h+=planRow(V,p);});
  }
  return h+'</section>';
}
function carryList(V,date){""")

# ---- 할 일 카드: 묶어 보기, 마감 표시, 편집 줄
i0 = s.index("function goalsCard(V,date,k){")
i1 = s.index("  }else if(mode==='view'){\n    h+='<p class=\"empty\">이날은 할 일을 적지 않았습니다.</p>';")
s = s[:i0] + r"""function goalRow(V,date,mode,day,x,isT){
  var key=date+'|'+x.id,f=isT&&day.focus===x.id&&!x.done,sub=x.sid&&V.subName[x.sid],p=x.pid&&V.plans[x.pid]?obj(V.plans[x.pid]):null,sel=S.gSel===key,ed=S.gEdit===key;
  var h='<li class="goal'+(x.done?' done':'')+(f?' focus':'')+(sel?' sel':'')+'" id="g-'+esc(x.id)+'"><button class="chk'+(x.done?' on':'')+'" data-act="goal-toggle" data-date="'+date+'" data-id="'+esc(x.id)+'" aria-pressed="'+(x.done?'true':'false')+'" aria-label="'+esc(x.text)+' 완료 표시"'+(mode!=='full'?' disabled':'')+'><span></span></button>';
  if(ed)h+='<div class="gt gedit"><input type="text" id="gEditIn" data-draft="gEdit" data-enter="g-save" data-date="'+date+'" data-id="'+esc(x.id)+'" maxlength="90" aria-label="할 일 고치기"><button class="btn small primary" data-act="g-save" data-date="'+date+'" data-id="'+esc(x.id)+'">저장</button><button class="btn small" data-act="g-sel" data-date="'+date+'" data-id="'+esc(x.id)+'">취소</button></div>';
  else h+='<div class="gt">'+(sub&&S.gGroup!=='sub'?'<em class="tag">'+esc(sub)+'</em>':'')+'<span>'+esc(x.text)+'</span>'+(p?'<em class="tag due">'+esc(shortDate(p.due))+' 마감'+(x.part?', '+esc(x.part):'')+'</em>':'')+(f?'<em class="tag a">지금 하는 중</em>':'')+'</div>';
  var canAct=mode!=='view'||!x.done;
  h+=(canAct&&!ed?'<button class="gmore" data-act="g-sel" data-date="'+date+'" data-id="'+esc(x.id)+'" aria-expanded="'+(sel?'true':'false')+'" aria-label="'+esc(x.text)+' 편집">'+(sel?'닫기':'편집')+'</button>':'<span></span>')+'</li>';
  if(sel&&!ed){
    var t=today(),a='';
    if(mode==='view'){a+='<button class="btn small soft" data-act="g-today" data-date="'+date+'" data-id="'+esc(x.id)+'">오늘로 가져오기</button>';}
    else{
      a+='<button class="btn small" data-act="g-edit" data-date="'+date+'" data-id="'+esc(x.id)+'">수정</button>';
      if(!x.done){a+='<button class="btn small" data-act="g-tomorrow" data-date="'+date+'" data-id="'+esc(x.id)+'">'+(date<t?'오늘로':'다음 날로')+'</button>';
        a+='<label class="gdate"><span>날짜 바꾸기</span><input type="date" data-chg="g-move" data-date="'+date+'" data-id="'+esc(x.id)+'" min="'+t+'" max="2026-12-31" value="'+date+'" aria-label="옮길 날짜"></label>';}
      a+='<button class="btn small" data-act="g-up" data-date="'+date+'" data-id="'+esc(x.id)+'" aria-label="위로">위로</button><button class="btn small" data-act="g-down" data-date="'+date+'" data-id="'+esc(x.id)+'" aria-label="아래로">아래로</button>';
      if(isT&&!x.done)a+='<button class="btn small soft" data-act="g-now" data-date="'+date+'" data-id="'+esc(x.id)+'">지금 하기</button>';
      a+='<button class="del" data-act="goal-del" data-date="'+date+'" data-id="'+esc(x.id)+'">'+(S.confirm==='gdel:'+x.id?'한 번 더 누르면 삭제':'삭제')+'</button>';
    }
    h+='<li class="gacts" id="ga-'+esc(x.id)+'">'+a+'</li>';
  }
  return h;
}
function goalsCard(V,date,k){
  var mode=modeOf(date),isT=date===today(),day=dayOf(V,V.me,date),g=day.goals,done=g.filter(isDone).length,undone=g.length-done;
  var h='<section class="card" id="c-goals" style="--k:'+k+'"><div class="ct"><h2>할 일'+(g.length?'<small>'+done+'/'+g.length+'</small>':'')+'</h2><div class="acts">';
  if(isT&&undone>=2)h+='<button class="btn small" data-act="open" data-modal="wheel">돌림판</button>';
  if(mode!=='view')h+='<button class="btn small primary" data-act="open" data-modal="compose" data-date="'+date+'">추가</button>';
  h+='</div></div>';
  if(g.length){
    if(g.length>1)h+='<div class="seg mini" style="grid-template-columns:repeat(3,minmax(0,1fr))" role="group" aria-label="할 일 묶어 보기">'+[['none','적은 순서'],['sub','과목별'],['plan','마감별']].map(function(x){return '<button data-act="g-group" data-id="'+x[0]+'" aria-pressed="'+(S.gGroup===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join('')+'</div>';
    h+='<ul>';
    if(S.gGroup==='none'||g.length<2)g.forEach(function(x){h+=goalRow(V,date,mode,day,x,isT);});
    else{
      var gs={},order=[];
      g.forEach(function(x){var key;if(S.gGroup==='sub')key=x.sid&&V.subName[x.sid]?x.sid:'';else key=x.pid&&V.plans[x.pid]?x.pid:'';if(!gs[key]){gs[key]=[];order.push(key);}gs[key].push(x);});
      if(S.gGroup==='sub')order.sort(function(a,b){var sa=V.subById[a],sb=V.subById[b];return (sa?sa.order:999)-(sb?sb.order:999);});
      else order.sort(function(a,b){if(!a)return 1;if(!b)return -1;var da=obj(V.plans[a]).due,db=obj(V.plans[b]).due;return da<db?-1:da>db?1:0;});
      order.forEach(function(key){
        var list=gs[key],dn=list.filter(isDone).length,lab;
        if(S.gGroup==='sub')lab=key?V.subName[key]:'과목 없음';
        else{var pp=obj(V.plans[key]);lab=key?plText(pp.type,pp.unit,pp.note,0)+' · '+shortDate(pp.due)+' 마감':'그 밖의 할 일';}
        h+='<li class="ghead"><span>'+esc(lab)+'</span><small>'+dn+'/'+list.length+'</small></li>';
        list.forEach(function(x){h+=goalRow(V,date,mode,day,x,isT);});
      });
    }
    h+='</ul>';
""" + s[i1:]

# 달력: 마감 표시, 날짜 칸, 다가오는 일정, 마감 있는 할 일 카드
sub("    mine.forEach(function(e){lab+=', '+e.title;if(n<2){evs+='<span class=\"ev mine\">'+esc(e.title)+'</span>';n++;}});\n    var more=(ev?1:0)+mine.length-n;",
    "    mine.forEach(function(e){lab+=', '+e.title;if(n<2){evs+='<span class=\"ev mine\">'+esc(e.title)+'</span>';n++;}});\n    var dues=dueMap(V)[d]||[];dues.forEach(function(p){lab+=', 마감 '+p.label;if(n<2){evs+='<span class=\"ev due\">마감 '+esc(p.label)+'</span>';n++;}});\n    var more=(ev?1:0)+mine.length+dues.length-n;")
sub("  Object.keys(V.evByDate).forEach(function(d){if(d>=t)V.evByDate[d].forEach(function(e){up.push({d:d,title:e.title,mine:1});});});\n  up.sort(",
    "  Object.keys(V.evByDate).forEach(function(d){if(d>=t)V.evByDate[d].forEach(function(e){up.push({d:d,title:e.title,mine:1});});});\n  Object.keys(dueMap(V)).forEach(function(d){if(d>=t)dueMap(V)[d].forEach(function(p){up.push({d:d,title:'마감 · '+p.label,mine:1});});});\n  up.sort(")
sub("  h+='<section class=\"card upcard\" id=\"c-up\" style=\"--k:2\"><div class=\"ct\"><h2>다가오는 일정</h2></div>';",
    "  h+='<div class=\"col upcol\">'+plansCard(V,2)+'<section class=\"card upcard\" id=\"c-up\" style=\"--k:3\"><div class=\"ct\"><h2>다가오는 일정</h2></div>';")
sub("  up.slice(0,5).forEach(function(u){h+='<button class=\"uprow\" data-act=\"pick-date\" data-d=\"'+u.d+'\"><b>'+dlabel(u.d)+'</b><span>'+esc(u.title)+'</span><small>'+esc(shortDate(u.d))+' '+DOW[pd(u.d).getDay()]+'</small></button>';});\n  return h+'</section></div></div>';",
    "  up.slice(0,6).forEach(function(u){h+='<button class=\"uprow\" data-act=\"pick-date\" data-d=\"'+u.d+'\"><b>'+dlabel(u.d)+'</b><span>'+esc(u.title)+'</span><small>'+esc(shortDate(u.d))+' '+DOW[pd(u.d).getDay()]+'</small></button>';});\n  return h+'</section></div></div></div>';")
# 날짜 칸(오른쪽): 그날 마감인 할 일
sub("  if(!ev&&!mine.length)h+='<p class=\"empty\">일정이 없습니다.</p>';",
    "  (dueMap(V)[d]||[]).forEach(function(p){h+='<div class=\"evrow\"><span><em class=\"tag due\">마감</em>'+esc(p.label)+'</span><button class=\"del\" data-act=\"pl-show\" data-id=\"'+esc(p.id)+'\">보기</button></div>';});\n  if(!ev&&!mine.length&&!(dueMap(V)[d]||[]).length)h+='<p class=\"empty\">일정이 없습니다.</p>';")

# 할 일 추가 창에서 마감 할 일로 넘어가기
sub("aria-label=\"자세한 내용\"></div>';\n  var f='<div class=\"preview\"><small>이렇게 올라갑니다</small>",
    "aria-label=\"자세한 내용\"></div>';\n  b+='<div class=\"fld plink\"><span class=\"hint\">며칠까지 끝낼 일인가요?</span><button class=\"btn small soft\" data-act=\"plan-from-cmp\">마감 정하고 날짜별로 나눠 넣기</button></div>';\n  var f='<div class=\"preview\"><small>이렇게 올라갑니다</small>")

# 팝업 열기와 그리기
sub("  if(type==='compose'){S.cmp=", "  if(type==='plan'){S.pl=newPlan();S.draft.plNote='';}\n  if(type==='compose'){S.cmp=")
sub("  if(t==='compose')return modalCompose(V);", "  if(t==='compose')return modalCompose(V);\n  if(t==='plan'&&S.pl)return modalPlan(V);")

# 마감 알림 (하루 한 번)
sub("  afterPlay(V);\n", "  afterPlay(V);\n  afterDue(V);\n", 1)
sub("function afterChat(V){", r"""function afterDue(V){
  if(!S.ready||!V.me)return;
  var t=today(),mark=t+'|'+V.me;if(lsGet('gbb_due')===mark)return;
  var soon=planList(V).filter(function(p){return !p.finished&&p.due>=t&&p.due<=addDays(t,2);});
  lsSet('gbb_due',mark);
  soon.slice(0,2).forEach(function(p){var left=p.n-p.dn;addNote({id:'due'+p.id+t,key:'due'+p.id,title:(p.due===t?'오늘 마감: ':ddayLabel(p.due)+' 마감: ')+cut(p.label,22),sub:left?'남은 몫 '+left+'개':'모두 끝냈습니다',tab:'cal'});});
}
function afterChat(V){""")

# 동작
sub("    case 'goal-del':editDay(date,function(d){d.goals=d.goals.filter(function(g){return g.id!==id;});if(d.focus===id)d.focus=null;});break;",
    "    case 'goal-del':if(prev!=='gdel:'+id){S.confirm='gdel:'+id;break;}editDay(date,function(d){d.goals=d.goals.filter(function(g){return g.id!==id;});if(d.focus===id)d.focus=null;});S.gSel=null;break;")
sub("""      var Vc=view(),list=Vc.me?carryList(Vc,date):[];
      editDay(date,function(d){list.forEach(function(g){if(d.goals.length<GMAX)d.goals.push({id:rid('g'),text:g.text,sid:g.sid||'',done:false});});});break;""",
    """      var Vc=view(),list=Vc.me?carryList(Vc,date):[],yd=addDays(date,-1),moved=[];
      editDay(date,function(d){list.forEach(function(g){if(d.goals.length<GMAX){var c={id:rid('g'),text:g.text,sid:g.sid||'',done:false};if(g.pid){c.pid=g.pid;c.part=g.part||'';c.amt=+g.amt||0;moved.push(g.id);}d.goals.push(c);}});});
      if(moved.length&&modeOf(yd)!=='view')editDay(yd,function(d){d.goals=d.goals.filter(function(x){return moved.indexOf(x.id)<0;});});
      break;""")
sub("    case 'timer-stop':stopTimer();break;", r"""    case 'timer-stop':stopTimer();break;
    case 'g-group':if(['none','sub','plan'].indexOf(id)>=0){S.gGroup=id;lsSet('gbb_ggroup',id);}break;
    case 'g-sel':{var gk=date+'|'+id;S.gSel=S.gSel===gk?null:gk;S.gEdit=null;break;}
    case 'g-edit':{var ge=dayOf(view(),view().me,date).goals.filter(function(x){return x.id===id;})[0];if(!ge)break;S.gEdit=date+'|'+id;S.draft.gEdit=ge.text;S.focusAfter='gEditIn';break;}
    case 'g-save':{
      var gtx=String(S.draft.gEdit||'').trim().slice(0,90);if(!gtx){flash('내용을 적어주세요.');break;}
      editDay(date,function(d){d.goals.forEach(function(x){if(x.id===id)x.text=gtx;});});S.gEdit=null;S.gSel=null;break;
    }
    case 'g-tomorrow':{var gto=date<today()?today():addDays(date,1);moveGoal(date,id,gto);break;}
    case 'g-today':moveGoal(date,id,today());break;
    case 'g-up':case 'g-down':{
      var dir=name==='g-up'?-1:1;
      editDay(date,function(d){var i=-1;d.goals.forEach(function(x,j){if(x.id===id)i=j;});var j2=i+dir;if(i<0||j2<0||j2>=d.goals.length)return;var tmp=d.goals[i];d.goals[i]=d.goals[j2];d.goals[j2]=tmp;});break;
    }
    case 'g-now':{
      var Vn=view(),gn=dayOf(Vn,Vn.me,today()).goals.filter(function(x){return x.id===id;})[0];if(!gn)break;
      editDay(today(),function(d){d.focus=id;});if(gn.sid)S.draft.timeSub=gn.sid;S.gSel=null;goTab('room');
      if(!liveOf(Vn,Vn.me))flash('공부방에서 '+(gn.sid&&Vn.subName[gn.sid]?Vn.subName[gn.sid]+' ':'')+'타이머를 켜세요.');
      break;
    }
    case 'pl-set':{
      var pk2=el.getAttribute('data-k'),pv2=el.getAttribute('data-v'),P2=S.pl;if(!P2)break;
      if(pk2==='mode'){P2.mode=pv2;P2.off={};}
      else if(pk2==='unit'){P2.unit=pv2;if(P2.mode==='repeat'){if(!P2.per)P2.per=pv2==='분'?30:pv2==='단원'||pv2==='회'||pv2==='강'?1:10;}else if(!P2.total)P2.total=pv2==='분'?120:pv2==='단원'||pv2==='회'||pv2==='강'?3:50;}
      else{if(pk2==='sid'&&P2.sid!==pv2)P2.type='';P2[pk2]=P2[pk2]===pv2?'':pv2;}
      break;
    }
    case 'pl-amt':{var P3=S.pl;if(!P3)break;var dd3=+el.getAttribute('data-d')||0;if(P3.mode==='repeat')P3.per=Math.max(0,Math.min(999,(+P3.per||0)+dd3));else P3.total=Math.max(0,Math.min(999,(+P3.total||0)+dd3));if(!P3.unit)P3.unit='문제';break;}
    case 'pl-due':if(S.pl){S.pl.due=el.getAttribute('data-v');S.pl.off={};}break;
    case 'pl-start':if(S.pl){S.pl.start=el.getAttribute('data-v');S.pl.off={};}break;
    case 'pl-dow':{var P4=S.pl;if(!P4)break;var dw4=plDows(P4),i4=+el.getAttribute('data-v');dw4[i4]=!dw4[i4];if(!dw4.some(Boolean))dw4[i4]=true;P4.dows=dw4.map(function(x){return x?'1':'0';}).join('');P4.off={};break;}
    case 'pl-early':if(S.pl){S.pl.early=!S.pl.early;S.pl.off={};}break;
    case 'pl-day':{var P5=S.pl,d5=el.getAttribute('data-d');if(!P5)break;P5.off=obj(P5.off);if(P5.off[d5])delete P5.off[d5];else P5.off[d5]=true;break;}
    case 'plan-from-cmp':{
      var c6=S.cmp;if(!c6)break;
      S.pl=newPlan();S.pl.sid=c6.sid||'';S.pl.type=c6.type||'';S.pl.unit=c6.unit||'';S.pl.total=+c6.amt||0;S.draft.plNote=S.draft.cmpNote||'';
      S.modal={type:'plan'};S.closing=false;break;
    }
    case 'pl-add':{
      var P6=S.pl,V6=view();if(!P6||!V6.me||!need())break;
      var note6=String(S.draft.plNote||'').trim().slice(0,60),A6=plAlloc(V6,P6);
      if(!plText(P6.type,P6.unit,note6,0)){flash('할 일을 고르거나 자세히에 적어주세요.');break;}
      if(!P6.due||!A6.use.length){flash('들어갈 날짜가 없습니다. 마감이나 요일을 확인하세요.');break;}
      var pid6=rid('p'),doc6={mid:V6.me,sid:P6.sid||'',type:P6.type||'',unit:P6.unit||'문제',note:note6,mode:P6.mode,total:+P6.total||0,per:+P6.per||0,due:P6.due,start:P6.start||today(),dows:String(P6.dows||'1111111'),early:!!P6.early,at:Date.now()};
      queueWrite('plans/'+pid6,doc6);putPlanGoals(pid6,doc6,A6.use);
      S.plOpen[pid6]=true;S.draft.plNote='';flash(A6.use.length+'일에 나눠 넣었습니다.');
      if(P6.mode!=='once'&&A6.use[0])S.date=A6.use[0].d;
      closeModal();return;
    }
    case 'pl-open':S.plOpen[id]=!S.plOpen[id];break;
    case 'pl-show':S.plOpen[id]=true;S.scrollAfter='pl-'+id;break;
    case 'pl-fin':S.plShowDone=!S.plShowDone;break;
    case 'pl-group':if(id==='due'||id==='sub'){S.plGroup=id;lsSet('gbb_plgroup',id);}break;
    case 'pl-del':{
      if(prev!=='pl:'+id){S.confirm='pl:'+id;break;}
      var V7=view(),p7=planList(V7).filter(function(x){return x.id===id;})[0];if(!p7||!need())break;
      dropPlanGoals(p7,true);queueWrite('plans/'+id,null);flash('마감 할 일과 남은 몫을 지웠습니다.');break;
    }
    case 'pl-redo':{
      var V8=view(),p8=planList(V8).filter(function(x){return x.id===id;})[0];if(!p8||!need())break;
      var left8=+p8.total>0?Math.max(0,+p8.total-p8.amtDone):p8.parts.filter(function(x){return !x.done;}).length;
      if(left8<=0){flash('남은 분량이 없습니다.');break;}
      dropPlanGoals(p8,true);
      var st8=p8.parts.some(function(x){return x.done&&x.date===today();})?addDays(today(),1):today(),spec8=Object.assign({},p8,{total:left8,start:st8,off:{}});
      if(!(+p8.total>0)){spec8.total=0;}
      var A8=plAlloc(view(),spec8);
      if(!(+p8.total>0)){A8.use=A8.use.slice(0,left8);A8.use.forEach(function(r,i){r.part=(i+1)+'/'+A8.use.length;});}
      if(!A8.use.length){flash('마감까지 넣을 수 있는 날이 없습니다.');break;}
      putPlanGoals(id,p8,A8.use);flash('남은 것을 '+A8.use.length+'일에 다시 나눴습니다.');break;
    }
    case 'pl-today':{
      var V9=view(),p9=planList(V9).filter(function(x){return x.id===id;})[0];if(!p9||!p9.parts[0])break;
      moveGoal(p9.parts[0].date,p9.parts[0].id,today());break;
    }""")
sub("  else if(kind==='checkMin'){editCfg(function(c){c.checkMin=+v||15;});}",
    """  else if(kind==='checkMin'){editCfg(function(c){c.checkMin=+v||15;});}
  else if(kind==='pl-due'||kind==='pl-start'){if(S.pl&&/^\\d{4}-\\d{2}-\\d{2}$/.test(v)){if(kind==='pl-due')S.pl.due=v;else S.pl.start=v;S.pl.off={};}}
  else if(kind==='g-move'){if(/^\\d{4}-\\d{2}-\\d{2}$/.test(v)&&v!==el.getAttribute('data-date'))moveGoal(el.getAttribute('data-date'),id,v);}""")
sub("function dayDoc(V,date){", r"""function moveGoal(from,id,to){
  var V=view(),t=today();if(!V.me||!need())return;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(to)||to<t){flash('오늘이나 그 뒤 날짜로만 옮길 수 있습니다.');return;}
  if(to===from)return;
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x.id===id;})[0];if(!g)return;
  if(dayOf(V,V.me,to).goals.length>=GMAX){flash(shortDate(to)+'에는 할 일이 가득 찼습니다.');return;}
  editDay(from,function(d){d.goals=d.goals.filter(function(x){return x.id!==id;});if(d.focus===id)d.focus=null;});
  editDay(to,function(d){var c=clone(g);c.done=false;d.goals.push(c);});
  S.gSel=null;flash(shortDate(to)+' '+DOW[pd(to).getDay()]+'요일로 옮겼습니다.');
}
function dayDoc(V,date){""")
