/* ---------- 다른 방에서 내 것 가져오기 (웹 판) ---------- */
// 이 기기로 들어간 적 있는 다른 방에서, 나 혼자 쓰던 것을 지금 방으로 복사한다.
// 가져오는 것: 내 수행평가·일정, 오늘부터의 할 일과 마감 계획, 시간표(고정 일정, 학교 시간표, 공부 시간),
//            과목 설정(단원, 진도 체크, 줄임말, 색, 안 듣는 과목, 하루 목표, 할 일 숨기기), 이 방에 없는 내 과목
// 점수와 공부 기록(공부 시간, 인증, 출석, 지난 할 일, 점수 기준일, 칭호)은 방장만, 따로 켰을 때만 가져온다.
// 같은 방에서 다시 가져와도 두 번 더해지지 않게 가져온 시간을 progress.crl[방]에 적어 둔다.
// 가져오지 않는 것: 대화, 게시판, 음악, 타이머
// 과목은 이름으로 맞추고, 이미 있는 것은 겹치지 않게 건너뛴다. 원래 방은 바꾸지 않는다.
function crMeOf(room){
  try{var v=localStorage.getItem('gbb_me@'+room);if(v)return v;if(localStorage.getItem('gbb_legacy_room')===room)return localStorage.getItem('gbb_me')||'';}catch(e){}
  return '';
}
function crRooms(){var cur=S.remote;return roomsList().filter(function(x){return !(cur&&x.room===cur.room&&x.url===cur.url);});}
function crObj(x){if(Array.isArray(x)){var o={};x.forEach(function(v,i){if(v!=null)o[i]=v;});return o;}return obj(x);}
function crLoad(e){
  var me=crMeOf(e.room);
  S.cr={step:'load',src:e,me:me,err:'',opt:S.cr&&S.cr.opt||{ev:true,goal:true,tt:true,prog:true,sub:true,rec:false}};render();
  var base=e.room+'/d/',t=today();
  function get(p){return fbRaw(e.url,base+p).catch(function(){return null;});}
  var k0=me+'_',k1=me+'_9999';
  var dq=fetch(e.url.replace(/\/+$/,'')+'/rooms/'+e.room+'/d/days.json?orderBy=%22%24key%22&startAt=%22'+encodeURIComponent(k0)+'%22&endAt=%22'+encodeURIComponent(k1)+'%22')
    .then(function(r){if(!r.ok)throw new Error('http '+r.status);return r.json();}).catch(function(){return get('days');});
  Promise.all([get('meta/config'),get('meta/room'),get('subjects'),get('events'),get('plans'),get('progress/'+me),dq]).then(function(r){
    if(!S.cr||S.cr.src!==e)return;
    var cfg=obj(r[0]),ros=arr(cfg.roster).filter(function(m){return m&&m.id;}),who=ros.filter(function(m){return m.id===me;})[0];
    if(!who){S.cr.step='err';S.cr.err='그 방에서 누구였는지 찾지 못했습니다. 그 방에 들어가 이름을 고른 뒤 다시 해 주세요.';render();return;}
    var days={};Object.keys(crObj(r[6])).forEach(function(k){if(k.indexOf(me+'_')===0)days[k]=r[6][k];});
    S.cr.D={name:String(who.name||''),room:String(obj(r[1]).name||e.name||'공부방'),subjects:crObj(r[2]),events:crObj(r[3]),plans:crObj(r[4]),prog:obj(r[5]),days:days};
    S.cr.step='preview';render();
  }).catch(function(){if(S.cr){S.cr.step='err';S.cr.err='그 방 기록을 불러오지 못했습니다. 인터넷 연결을 확인해 주세요.';render();}});
}
/* 무엇을 어떻게 쓸지 정한다(미리 보기 숫자와 실제 쓰기가 같은 계산) */
function crPlan(V,D,opt){
  var me=V.me,t=today(),W={},n={ev:0,evDup:0,goal:0,goalDup:0,plan:0,blk:0,sch:false,schHad:false,unit:0,chk:0,misc:0,newSubs:[],recDays:0,recMins:0,recGoal:0};
  var srcSkip=obj(D.prog.skip),byName={},maxOrd=0;
  V.subs.forEach(function(s){byName[s.name.trim()]=s;maxOrd=Math.max(maxOrd,s.order);});
  // 과목 맞추기: 이름이 같은 과목, 없으면(내가 듣던 과목이면) 새로 만든다
  var map={},items={};
  Object.keys(D.subjects).forEach(function(sid){
    var s=obj(D.subjects[sid]),nm=String(s.name||'').trim(),its=arr(s.items).filter(function(it){return it&&it.id;});if(!nm)return;
    var hit=byName[nm];
    if(hit){map[sid]=hit.id;items[sid]={};its.forEach(function(it){var d=hit.items.filter(function(x){return x.label===String(it.label||'');})[0];if(d)items[sid][it.id]=d.id;});return;}
    if(srcSkip[sid]||!opt.sub)return;
    var nid=rid('s');map[sid]=nid;items[sid]={};its.forEach(function(it){items[sid][it.id]=String(it.id);});
    W['subjects/'+nid]={name:nm.slice(0,24),order:maxOrd+1+n.newSubs.length,items:its.map(function(it){return {id:String(it.id),label:String(it.label||'').slice(0,30)};})};
    n.newSubs.push(nm);
  });
  function ms(sid){return sid&&map[sid]?map[sid]:'';}
  // 수행평가·일정 (내 것만)
  if(opt.ev){
    var have={};Object.keys(V.events).forEach(function(id){var x=obj(V.events[id]);if(x.mid===me)have[x.date+'|'+x.title]=1;});
    Object.keys(D.events).forEach(function(id){
      var x=obj(D.events[id]);if(x.mid!==S.cr.me||!x.date||!x.title)return;
      if(have[x.date+'|'+x.title]){n.evDup++;return;}have[x.date+'|'+x.title]=1;
      var y=clone(x);y.mid=me;if(y.sid)y.sid=ms(y.sid);if(!y.sid)delete y.sid;
      W['events/'+rid('e')]=y;n.ev++;
    });
  }
  // 마감 계획과 할 일 (오늘부터)
  var pmap={};
  if(opt.goal){
    Object.keys(D.plans).forEach(function(id){
      var p=obj(D.plans[id]);if(p.mid!==S.cr.me||!p.due||p.due<t||p.finished)return;
      var dup=Object.keys(V.plans).filter(function(k){var q=obj(V.plans[k]);return q.mid===me&&q.due===p.due&&q.type===p.type&&String(q.note||'')===String(p.note||'')&&q.sid===ms(p.sid);})[0];
      if(dup){pmap[id]=dup;return;}
      var np=rid('p'),y=clone(p);y.mid=me;y.sid=ms(p.sid);W['plans/'+np]=y;pmap[id]=np;n.plan++;
    });
    Object.keys(D.days).forEach(function(k){
      var date=k.slice(S.cr.me.length+1),src=arr(obj(D.days[k]).goals).filter(function(g){return g&&g.text;});if(date<t||!src.length)return;
      var d=clone(dayOf(V,me,date)),seen={},added=0;
      d.goals.forEach(function(g){seen[g.text+'|'+(g.sid||'')]=1;});
      src.forEach(function(g){
        var sid=ms(g.sid),key=g.text+'|'+sid;
        if(seen[key]){n.goalDup++;return;}
        if(d.goals.length>=GMAX)return;
        seen[key]=1;var y=clone(g);y.id=rid('g');y.sid=sid;
        if(y.pid){if(pmap[y.pid])y.pid=pmap[y.pid];else{delete y.pid;delete y.part;}}
        d.goals.push(y);added++;n.goal++;
      });
      if(added)W['days/'+me+'_'+date]=cleanDay(d);
    });
  }
  // 내 설정(progress): 시간표, 과목 설정
  var P0=obj(V.progress[me]),P=clone(P0),sp=D.prog,pch=false;
  if(opt.tt&&sp.tt){
    var st=obj(sp.tt),tt=P.tt=obj(clone(P.tt||{})),bl=arr(tt.b).slice(),bmap={};
    arr(st.b).forEach(function(b){
      if(!b||!b.id)return;
      var ss=fxSids(b).map(ms).filter(Boolean),y=clone(b);y.sid=ss[0]||'';if(ss.length>1)y.sids=ss.join(',');else delete y.sids;
      var dup=bl.filter(function(x){return x&&x.k===y.k&&String(x.t||'')===String(y.t||'')&&x.d===y.d&&+x.s===+y.s&&+x.e===+y.e;})[0];
      if(dup){bmap[b.id]=dup.id;return;}
      y.id=rid('b');bmap[b.id]=y.id;bl.push(y);n.blk++;pch=true;
    });
    tt.b=bl;
    var ov=obj(tt.ov),sov=obj(st.ov);
    Object.keys(sov).forEach(function(date){if(date<t)return;var o=obj(ov[date]),so=obj(sov[date]),ch=false;Object.keys(so).forEach(function(bid){var nb=bmap[bid];if(nb&&!o[nb]){o[nb]=clone(so[bid]);ch=true;}});if(ch){ov[date]=o;pch=true;}});
    tt.ov=ov;
    var tx=obj(tt.x),sx=obj(st.x);
    Object.keys(sx).forEach(function(date){if(date<t)return;var a=arr(tx[date]).slice(),ch=false;arr(sx[date]).forEach(function(b){if(!b)return;if(a.some(function(x){return x&&String(x.t||'')===String(b.t||'')&&+x.s===+b.s&&+x.e===+b.e;}))return;var y=clone(b);y.id=rid('x');a.push(y);ch=true;n.blk++;});if(ch){tx[date]=a;pch=true;}});
    tt.x=tx;
    if(st.win&&!tt.win){tt.win=clone(st.win);pch=true;n.misc++;}
    if(st.sch){
      if(schOf(V,me).has)n.schHad=true;
      else{
        var sc=clone(st.sch),w=schW(sc.w),nw={};
        Object.keys(w).forEach(function(dw){var row=obj(w[dw]),nr={};Object.keys(row).forEach(function(pk){var c=obj(row[pk]);if(c.s){var m=ms(c.s);c=clone(c);if(m)c.s=m;else{var snm=String(obj(D.subjects[c.s]).name||'').trim();delete c.s;if(!snm)return;c.t=snm.slice(0,12);}}nr[pk]=c;});nw[dw]=nr;});
        sc.w=nw;tt.sch=sc;n.sch=true;pch=true;
      }
    }
  }
  if(opt.prog){
    var units=P.units=obj(clone(P.units||{})),checks=P.checks=obj(clone(P.checks||{})),umap={};
    Object.keys(obj(sp.units)).forEach(function(sid){
      var d=ms(sid);if(!d)return;var cur=arr(units[d]).slice(),src=arr(sp.units[sid]);umap[sid]={};
      src.forEach(function(u){
        if(!u||!u.id)return;
        var same=cur.filter(function(x){return x&&String(x.n||'')===String(u.n||'');})[0];
        if(same){umap[sid][u.id]=same.id;return;}
        var y=clone(u);if(cur.some(function(x){return x&&x.id===y.id;}))y.id=rid('u');umap[sid][u.id]=y.id;cur.push(y);n.unit++;pch=true;
      });
      units[d]=cur;
    });
    Object.keys(obj(sp.checks)).forEach(function(k){
      if(!sp.checks[k])return;var a=k.split('__'),sid=a[0],d=ms(sid);if(!d||!items[sid])return;
      var key;
      if(a.length===2){var it=items[sid][a[1]];if(!it)return;key=d+'__'+it;}
      else if(a.length===3){var u=umap[sid]&&umap[sid][a[1]],it2=items[sid][a[2]];if(!u||!it2)return;key=d+'__'+u+'__'+it2;}
      else return;
      if(!checks[key]){checks[key]=true;n.chk++;pch=true;}
    });
    var sc2=P.scol=obj(clone(P.scol||{}));Object.keys(obj(sp.scol)).forEach(function(k){var d=D.subjects[k]?ms(k):k;if(d&&sc2[d]==null){sc2[d]=sp.scol[k];n.misc++;pch=true;}});
    var ab=P.abbr=obj(clone(P.abbr||{}));Object.keys(obj(sp.abbr)).forEach(function(k){var d=ms(k);if(d&&!ab[d]&&sp.abbr[k]){ab[d]=sp.abbr[k];n.misc++;pch=true;}});
    var sk=P.skip=obj(clone(P.skip||{}));Object.keys(srcSkip).forEach(function(k){var d=ms(k);if(srcSkip[k]&&d&&!sk[d]){sk[d]=true;n.misc++;pch=true;}});
    if(+sp.goalMins>0&&!(+P.goalMins>0)){P.goalMins=+sp.goalMins;n.misc++;pch=true;}
    if(sp.hideGoals!=null&&P.hideGoals==null){P.hideGoals=sp.hideGoals;pch=true;}
  }
  // 점수와 공부 기록 (방장만, 따로 켰을 때)
  if(opt.rec&&adminId(V)===me){
    var led=P.crl=obj(clone(P.crl||{})),lk=String(S.cr.src.room).replace(/[.#$\[\]\/]/g,'_'),L=led[lk]=obj(led[lk]);
    var mapM=function(o){var r={};o=obj(o);Object.keys(o).forEach(function(k){var v=+o[k]||0;if(v<=0)return;var d=ms(k)||'etc';r[d]=(r[d]||0)+v;});return r;};
    var mergeM=function(cu,pv,sr){var out={},ks={};[cu,pv,sr].forEach(function(o){Object.keys(o).forEach(function(x){ks[x]=1;});});Object.keys(ks).forEach(function(x){var v=Math.max(0,(+cu[x]||0)-(+pv[x]||0))+(+sr[x]||0);if(v>0)out[x]=v;});return out;};
    Object.keys(D.days).forEach(function(k){
      var date=k.slice(S.cr.me.length+1);if(date>t)return;
      var sd=obj(D.days[k]),path='days/'+me+'_'+date,cur=W[path]?clone(W[path]):clone(dayOf(V,me,date)),before=JSON.stringify(cur);
      var sm=mapM(sd.mins),sn=mapM(sd.manual),pv=obj(L[date]),oldTot=sumMins(cur.mins)+sumMins(cur.manual);
      cur.mins=mergeM(obj(cur.mins),obj(pv.m),sm);cur.manual=mergeM(obj(cur.manual),obj(pv.n),sn);
      if(sd.certAt&&!cur.certAt)cur.certAt=sd.certAt;
      if(sd.in&&(!cur.in||String(sd.in)<String(cur.in)))cur.in=sd.in;
      if(date<t){
        var seen={};cur.goals=arr(cur.goals);cur.goals.forEach(function(g){seen[g.text+'|'+(g.sid||'')]=1;});
        arr(sd.goals).forEach(function(g){if(!g||!g.text)return;var sid=ms(g.sid),key=g.text+'|'+sid;if(seen[key]||cur.goals.length>=GMAX)return;seen[key]=1;var y=clone(g);y.id=rid('g');y.sid=sid;delete y.pid;delete y.part;cur.goals.push(y);n.recGoal++;});
      }
      var nl={};if(Object.keys(sm).length)nl.m=sm;if(Object.keys(sn).length)nl.n=sn;
      if(JSON.stringify(pv)!==JSON.stringify(nl)){if(Object.keys(nl).length)L[date]=nl;else delete L[date];pch=true;}
      if(JSON.stringify(cur)!==before){W[path]=cleanDay(cur);n.recDays++;n.recMins+=Math.max(0,sumMins(cur.mins)+sumMins(cur.manual)-oldTot);}
    });
    if(!Object.keys(L).length)delete led[lk];
    if(sp.reset&&!P.reset){P.reset=clone(sp.reset);pch=true;}
    if(sp.title&&!P.title){P.title=sp.title;pch=true;}
  }
  if(pch)W['progress/'+me]=P;
  return {W:W,n:n};
}
function modalCarry(V){
  var c=S.cr||{step:'pick'},b='',f='';
  if(c.step==='pick'){
    var list=crRooms();
    b+='<p class="hint" style="margin:0 0 12px">이 기기로 들어간 적 있는 방에서 나 혼자 쓰던 것을 지금 방으로 복사합니다. 원래 방은 그대로 남습니다.</p><div class="rmlist">';
    list.forEach(function(x){var me=crMeOf(x.room);b+='<div class="rmrow"><div class="rmn"><b>'+esc(x.name||'공부방')+'</b><small>'+(me?(x.code?'참여 코드 '+fmtCode(x.code):''):'이 기기로 이름을 고른 적이 없어 가져올 수 없습니다')+'</small></div>'+(me?'<button class="btn small" data-act="cr-pick" data-id="'+esc(x.room)+'">이 방에서 가져오기</button>':'')+'</div>';});
    if(!list.length)b+='<p class="hint">다른 방에 들어가 본 적이 없습니다.</p>';
    b+='</div>';
  }else if(c.step==='load'){
    b='<p class="hint" role="status">'+esc(c.src.name||'공부방')+' 기록을 불러오는 중입니다.</p>';
  }else if(c.step==='err'){
    b='<p class="hint serr" role="status">'+esc(c.err)+'</p>';f='<div class="df"><button class="btn" data-act="cr-back">다른 방 고르기</button></div>';
  }else{
    var D=c.D,o=c.opt,pl=crPlan(V,D,o),n=pl.n,one=function(k,lab,sub){return '<button class="nrchk crchk" data-act="cr-opt" data-k="'+k+'" aria-pressed="'+(o[k]?'true':'false')+'"><i aria-hidden="true"></i><span><b>'+lab+'</b>'+(sub?'<small>'+sub+'</small>':'')+'</span></button>';};
    var adm=adminId(V)===V.me,pr=crPlan(V,D,{ev:true,goal:true,tt:true,prog:true,sub:o.sub,rec:adm}).n;
    b+='<p class="hint" style="margin:0 0 6px"><b>'+esc(D.room)+'</b>의 <b>'+esc(D.name)+'</b> 님 것을 지금 방의 <b>'+esc(V.byId[V.me].name)+'</b> 님에게 복사합니다.</p>';
    b+=one('ev','수행평가와 일정','새로 '+pr.ev+'개'+(pr.evDup?', 이미 있는 '+pr.evDup+'개는 건너뜀':''));
    b+=one('goal','오늘부터의 할 일','할 일 '+pr.goal+'개, 마감 계획 '+pr.plan+'개'+(pr.goalDup?', 겹치는 '+pr.goalDup+'개는 건너뜀':''));
    b+=one('tt','시간표','고정 일정 '+pr.blk+'개'+(pr.sch?', 학교 시간표':pr.schHad?', 학교 시간표는 이미 있어 그대로':''));
    b+=one('prog','과목 설정','단원 '+pr.unit+'개, 진도 체크 '+pr.chk+'개, 줄임말·색·안 듣는 과목·하루 목표');
    b+=one('sub','이 방에 없는 내 과목 만들기',pr.newSubs.length?esc(pr.newSubs.join(', '))+' (방 사람 모두에게 보이고, 안 듣는 사람은 진도에서 뺄 수 있습니다)':'모두 이미 있습니다');
    if(adm){
      b+='<div class="crsep"><h4>점수와 공부 기록<small>방장만 보이고, 켜야만 옮깁니다</small></h4>';
      b+=one('rec','점수와 공부 기록도 가져오기',pr.recDays?pr.recDays+'일치 공부 시간 '+fmtMins(pr.recMins)+', 인증과 출석, 지난 할 일 '+pr.recGoal+'개. 점수는 이 기록으로 다시 계산되고, 순위 보너스는 이 방 사람들과 비교해 정해집니다.':'가져올 기록이 없습니다');
      b+='</div>';
    }
    b+='<p class="hint" style="margin-top:12px">'+(adm?'':'점수와 공부 기록은 옮기지 않습니다. ')+'대화와 게시판은 옮기지 않습니다. 과목은 이름이 같은 것끼리 맞춥니다.</p>';
    var any=Object.keys(pl.W).length>0;
    f='<div class="df"><button class="btn" data-act="cr-back">다른 방 고르기</button><button class="btn primary" data-act="cr-go"'+(any&&!c.busy?'':' disabled')+'>'+(c.busy?'가져오는 중':any?'가져오기':'가져올 것이 없습니다')+'</button></div>';
  }
  return dlg('',{id:'carry',t:'다른 방에서 가져오기'},b,f);
}
function crGo(){
  var c=S.cr,V=view();if(!c||!c.D||!V.me||!need())return;
  var pl=crPlan(V,c.D,c.opt),paths=Object.keys(pl.W);if(!paths.length)return;
  var sn=snap(paths),n=pl.n;
  S.crRaw=true;try{paths.forEach(function(p){save(p,pl.W[p]);});}finally{S.crRaw=false;}S.crUndo=sn;
  var parts=[];if(n.ev)parts.push('일정 '+n.ev+'개');if(n.goal)parts.push('할 일 '+n.goal+'개');if(n.plan)parts.push('마감 계획 '+n.plan+'개');if(n.blk||n.sch)parts.push('시간표');if(n.unit||n.chk||n.misc)parts.push('과목 설정');if(n.newSubs.length)parts.push('과목 '+n.newSubs.length+'개');if(n.recDays)parts.push('공부 기록 '+n.recDays+'일치');
  S.cr=null;closeModal();flash(jos(parts.join(', ')||'설정','을','를')+' 가져왔습니다.',sn);
}
