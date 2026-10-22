/* ---------- 학교 시간표 ---------- */
// 칸: {s:과목 id} 또는 {t:직접 쓴 이름}, 선택으로 tc(선생님), r(장소)
// 같은 과목을 선생님 두 분이 나눠 하면 칸마다 선생님을 적고, 시간표와 수업 알림에 선생님 이름을 같이 보인다
// 같은 수업이 연달아 있으면(쉬는 시간 20분 이하) 시간표에서 이어 붙여 보이고, 알림은 첫 교시 앞에 한 번만 낸다
var SCH_DEF=[[510,560],[570,620],[630,680],[690,740],[810,860],[870,920],[930,980]];
var SCH_OLD=[[520,570],[580,630],[640,690],[700,750],[810,860],[870,920],[930,980]];
var SCH_QUICK=['창체','자습','동아리','진로'];
var SCH_DAYS=[1,2,3,4,5];
// Firebase는 열쇠가 숫자(요일 1~5)인 묶음을 배열로 돌려줄 때가 있어서 다시 묶음으로 바꿔 읽는다
function schW(x){if(Array.isArray(x)){var o={};x.forEach(function(v,i){if(v&&typeof v==='object')o[i]=v;});return o;}return obj(x);}
function schOf(V,mid){
  var t=obj(obj(V.progress[mid]).tt),s=obj(t.sch),w=schW(s.w);
  var p=arr(s.p).filter(function(x){return x&&+x.e>+x.s;}).map(function(x){return {s:+x.s,e:+x.e};});
  // 예전 기본 시간(8:40 시작)을 그대로 두었으면 지금 기본 시간(8:30 시작)으로 본다
  if(p.length===SCH_OLD.length&&p.every(function(x,i){return x.s===SCH_OLD[i][0]&&x.e===SCH_OLD[i][1];}))p=[];
  var has=Object.keys(w).some(function(k){return Object.keys(obj(w[k])).length>0;});
  return {p:p.length?p:SCH_DEF.map(function(x){return {s:x[0],e:x[1]};}),w:w,has:has};
}
function schCell(V,sch,dw,i){
  var c=obj(obj(sch.w[dw])['p'+i]),o=null;
  if(c.s&&V.subName[c.s])o={sid:c.s,name:V.subName[c.s]};
  else if(c.t)o={t:String(c.t),name:String(c.t)};
  if(o){o.tc=String(c.tc||'').trim();o.r=String(c.r||'').trim();o.key=o.sid?'s:'+o.sid:'t:'+o.t;}
  return o;
}
function schSame(a,b){return !!(a&&b&&a.key===b.key&&a.tc===b.tc&&a.r===b.r);}
function schJoin(sch,i){var a=sch.p[i-1],b=sch.p[i];return !!(a&&b&&b.s-a.e<=20);}
function schEach(V,sch,fn){SCH_DAYS.forEach(function(d){sch.p.forEach(function(p,i){var c=schCell(V,sch,d,i);if(c)fn(c,d,i);});});}
function schTeachers(V,sch,key){var m={};schEach(V,sch,function(c){if(c.key===key&&c.tc)m[c.tc]=1;});return Object.keys(m);}
function schCombos(V,sch,key){var m={},out=[];schEach(V,sch,function(c){if(c.key!==key||(!c.tc&&!c.r))return;var k=c.tc+'|'+c.r;if(!m[k]){m[k]=1;out.push({tc:c.tc,r:c.r});}});return out;}
function schBlocks(V,sch,dw){
  var out=[],cur=null;
  sch.p.forEach(function(p,i){
    var c=schCell(V,sch,dw,i);if(!c){cur=null;return;}
    if(cur&&schSame(cur.c,c)&&schJoin(sch,i)){cur.j=i;cur.e=p.e;return;}
    cur={i:i,j:i,c:c,s:p.s,e:p.e};out.push(cur);
  });
  return out;
}
/* 수업 알림: 수업 시작 전 정각부터 시작하고 10분 뒤까지 과목과 장소 */
function schNow(V,now){
  if(!V||!V.me||!S.ready)return null;
  var sch=schOf(V,V.me);if(!sch.has)return null;
  var d=new Date(now),dw=d.getDay();if(dw<1||dw>5)return null;
  var ds=fd(d),ev=typeof EVENTS!=='undefined'?EVENTS[ds]:null;if(ev&&ev.off)return null;
  var m=d.getHours()*60+d.getMinutes(),bl=schBlocks(V,sch,dw);
  for(var k=0;k<bl.length;k++){var b=bl[k],from=Math.floor((b.s-1)/60)*60;if(m>=from&&m<b.s+10)return {b:b,now:m>=b.s,ds:ds};}
  return null;
}
function schNowHtml(V){
  var x=schNow(V,Date.now());if(!x)return '';
  var b=x.b,c=b.c,multi=schTeachers(V,schOf(V,V.me),c.key).length>1,col=c.sid?subCol(V,c.sid):SGRAY;
  var per=(b.i+1)+(b.j>b.i?'~'+(b.j+1):'')+'교시';
  return '<div class="notice schnow" role="status" style="--sc:'+col+'"><span class="snl">'+(x.now?'지금 수업':fmtHM(b.s)+' 시작')+'</span><b class="snp">'+per+'</b><b class="sns">'+esc(c.name)+(multi&&c.tc?'<small>'+esc(c.tc)+'</small>':'')+'</b>'+(c.r?'<span class="snr">'+esc(c.r)+'</span>':'')+(b.j>b.i?'<span class="snx">'+(b.j-b.i+1)+'시간 연속</span>':'')+'</div>';
}
function schNowKey(V){var x=schNow(V,Date.now());return x?x.ds+'|'+x.b.i+'|'+(x.now?1:0)+'|'+x.b.c.key+'|'+x.b.c.tc+'|'+x.b.c.r+'|'+x.b.j:'';}
function schTick(){var k=schNowKey(V0);if(k!==S.schNowK){S.schNowK=k;paintBanner();}}
function schMetaSet(d,i,k,v){
  var V=view();if(!V.me||!canWrite())return;
  var c=obj(obj(schOf(V,V.me).w[d])['p'+i]);if(!c.s&&!c.t)return;if(String(c[k]||'')===v)return;
  editSch(function(s){var w=obj(s.w[d]),cc=clone(obj(w['p'+i]));if(!cc.s&&!cc.t)return;if(v)cc[k]=v;else delete cc[k];w['p'+i]=cc;s.w[d]=w;});
}
// 선생님, 장소는 적는 동안 S.draft에 두고 다음 칸, 다른 칸, 닫기 때 저장한다
// (포커스가 빠질 때 바로 저장하면 화면이 다시 그려지며 누른 곳이 어긋날 수 있어서)
function schMetaFromInputs(sel){
  if(!sel)return;var kk=sel.d+'-'+sel.i;
  [['tc','schTc:'],['r','schR:']].forEach(function(x){var v=S.draft[x[1]+kk];if(v==null)return;schMetaSet(sel.d,sel.i,x[0],String(v).trim().slice(0,x[0]==='tc'?10:16));});
}
// 칸 값이 바뀌면(과목 고르기, 이 과목에서 쓴 것) 적는 칸도 새 값으로
function schDraftSet(sel,tc,r){if(!sel)return;var kk=sel.d+'-'+sel.i;S.draft['schTc:'+kk]=tc||'';S.draft['schR:'+kk]=r||'';S.sync=true;}
function editSch(fn){
  editTT(function(T){
    var s=clone(obj(T.sch));s.p=arr(s.p).filter(function(x){return x&&+x.e>+x.s;});s.w=schW(s.w);
    if(!s.p.length)s.p=SCH_DEF.map(function(x){return {s:x[0],e:x[1]};});
    fn(s);T.sch=s;
  });
}
function schPeriods(V,date,b){
  var sch=schOf(V,V.me),dw=pd(date).getDay();if(!sch.has||dw<1||dw>5)return [];
  return sch.p.map(function(p,i){return {i:i,s:p.s,e:p.e,c:schCell(V,sch,dw,i)};}).filter(function(x){return x.c&&x.s>=b.s&&x.e<=b.e;});
}
function schLine(V,date){
  var sch=schOf(V,V.me),dw=pd(date).getDay();if(!sch.has||dw<1||dw>5)return '';
  var out=[];sch.p.forEach(function(p,i){var c=schCell(V,sch,dw,i);if(c)out.push('<span style="--sc:'+(c.sid?subCol(V,c.sid):SGRAY)+'"><b>'+(i+1)+'</b>'+esc(c.name)+'</span>');});
  return out.join('');
}
function modalSchool(V){
  var who=S.schWho&&V.byId[S.schWho]?S.schWho:V.me,mine=who===V.me,sch=schOf(V,who),sel=mine?S.schSel:null,tdw=pd(today()).getDay();
  var others=V.roster.filter(function(m){return m.id!==V.me&&V.byId[m.id]&&schOf(V,m.id).has;});
  var b='';
  if(others.length)b+='<div class="chips schwho" role="group" aria-label="누구의 시간표">'+[V.me].concat(others.map(function(m){return m.id;})).map(function(id){return '<button class="chip" data-act="sch-who" data-id="'+esc(id)+'" aria-pressed="'+(id===who?'true':'false')+'">'+(id===V.me?'나':esc(V.byId[id].name))+'</button>';}).join('')+'</div>';
  if(!mine&&!sch.has)b+='<p class="hint">아직 시간표를 넣지 않았습니다.</p>';
  b+='<div class="schwrap"><table class="sch"><thead><tr><th></th>'+SCH_DAYS.map(function(d){return '<th class="'+(d===tdw?'today':'')+'">'+DOW[d]+'</th>';}).join('')+'</tr></thead><tbody>';
  sch.p.forEach(function(p,i){
    b+='<tr><th><b>'+(i+1)+'</b><small>'+fmtHM(p.s)+'</small></th>';
    SCH_DAYS.forEach(function(d){
      var c=schCell(V,sch,d,i),on=!!(sel&&sel.d===d&&sel.i===i),col=c&&c.sid?subCol(V,c.sid):SGRAY;
      var cont=!!(c&&schSame(c,schCell(V,sch,d,i-1))&&schJoin(sch,i)),jn=!!(c&&schSame(c,schCell(V,sch,d,i+1))&&schJoin(sch,i+1));
      var mt=c&&schTeachers(V,sch,c.key).length>1?c.tc:'',meta=c?(mt?'<small>'+esc(mt)+'</small>':'')+(c.r?'<small>'+esc(c.r)+'</small>':''):'';
      var lab=DOW[d]+'요일 '+(i+1)+'교시'+(c?', '+c.name+(c.tc?', '+c.tc+' 선생님':'')+(c.r?', '+c.r:'')+(cont?', 앞 교시에 이어서':''):', 비어 있음');
      var inner=c?(cont?'<span class="cn">이어서</span>':'<span'+(meta?' class="m"':'')+'>'+esc(c.name)+'</span>'+meta):(mine?'<span class="ph">+</span>':'');
      var cls='schc'+(c?' f':'')+(on?' on':'')+(cont?' cont':'')+(jn?' jn':'');
      b+='<td class="'+(d===tdw?'today':'')+'">'+(mine?'<button class="'+cls+'" data-act="sch-sel" data-d="'+d+'" data-i="'+i+'" style="--sc:'+col+'" aria-pressed="'+(on?'true':'false')+'" aria-label="'+esc(lab)+'">'+inner+'</button>':'<div class="'+cls+'" style="--sc:'+col+'" aria-label="'+esc(lab)+'">'+inner+'</div>')+'</td>';
    });
    b+='</tr>';
  });
  b+='</tbody></table></div>';
  if(mine&&sel){
    var cur=schCell(V,sch,sel.d,sel.i);
    b+='<div class="schpick" id="schPick"><h3>'+DOW[sel.d]+'요일 '+(sel.i+1)+'교시<small>'+fmtHM(sch.p[sel.i].s)+'~'+fmtHM(sch.p[sel.i].e)+'</small></h3><div class="chips">';
    b+=mySubs(V).map(function(s){return '<button class="chip sch-sub" data-act="sch-put" data-v="'+esc(s.id)+'" style="--sc:'+subCol(V,s.id)+'" aria-pressed="'+(cur&&cur.sid===s.id?'true':'false')+'"><i></i>'+esc(s.name)+'</button>';}).join('');
    b+=SCH_QUICK.map(function(t){return '<button class="chip" data-act="sch-put" data-t="'+esc(t)+'" aria-pressed="'+(cur&&cur.t===t?'true':'false')+'">'+esc(t)+'</button>';}).join('');
    b+='</div><div class="row" style="margin-top:10px"><input type="text" data-draft="schT" data-enter="sch-text" maxlength="12" placeholder="직접 쓰기 (예: 체육)" aria-label="과목 직접 쓰기"><button class="btn small" data-act="sch-text">넣기</button></div>';
    if(cur){
      var kk=sel.d+'-'+sel.i,cbs=schCombos(V,sch,cur.key).filter(function(x){return !(x.tc===cur.tc&&x.r===cur.r);});
      if(S.draft['schTc:'+kk]==null)S.draft['schTc:'+kk]=cur.tc;if(S.draft['schR:'+kk]==null)S.draft['schR:'+kk]=cur.r;
      b+='<div class="schmeta"><div><label class="lb" for="schTc-'+kk+'">선생님<small>선택</small></label><input type="text" class="schf" id="schTc-'+kk+'" data-draft="schTc:'+kk+'" data-enter="sch-next" maxlength="10" placeholder="예: 김민수"></div>';
      b+='<div><label class="lb" for="schR-'+kk+'">장소<small>선택</small></label><input type="text" class="schf" id="schR-'+kk+'" data-draft="schR:'+kk+'" data-enter="sch-next" maxlength="16" placeholder="예: 2-2 수학과실"></div></div>';
      if(cbs.length)b+='<div class="schcombo"><small>이 과목에서 쓴 것</small><div class="chips">'+cbs.slice(0,4).map(function(x){return '<button class="chip" data-act="sch-combo" data-tc="'+esc(x.tc)+'" data-r="'+esc(x.r)+'">'+esc([x.tc,x.r].filter(Boolean).join(' · '))+'</button>';}).join('')+'</div></div>';
      b+='<p class="hint" style="margin-top:8px">같은 과목을 선생님 두 분이 나눠 하면 칸마다 선생님을 적어 두세요. 시간표와 수업 알림에 선생님 이름이 같이 나옵니다.</p>';
    }
    b+='<div class="row" style="margin-top:10px"><button class="btn small primary" data-act="sch-next">'+(sel.i+1<sch.p.length?'다음 칸':'끝')+'</button>'+(cur?'<button class="btn small" data-act="sch-clear">비우기</button>':'')+'</div></div>';
  }else if(mine)b+='<p class="hint" style="margin-top:12px">칸을 누르고 과목을 고른 뒤 선생님과 장소를 적으세요(선택). 수업 시작 전 정각부터 시작하고 10분 뒤까지 화면 위에 과목과 장소가 나옵니다. 같은 수업이 연달아 있으면 이어 붙여 보이고 알림은 한 번만 나옵니다.</p>';
  if(!mine&&sch.has)b+='<div class="row" style="margin-top:12px"><button class="btn small primary" data-act="sch-copy" data-id="'+esc(who)+'">'+(S.confirm==='schcopy:'+who?'한 번 더 누르면 내 시간표를 바꿉니다':'이 시간표를 내 걸로 가져오기')+'</button></div>';
  if(mine){
    b+='<div class="sec schsec"><div class="row"><button class="btn small" data-act="sch-times" aria-expanded="'+(S.schTimes?'true':'false')+'">'+(S.schTimes?'교시 시간 접기':'교시 시간 고치기')+'</button><button class="btn small" data-act="sch-fit">고정 시간표의 학교 시간 맞추기</button></div>';
    if(S.schTimes){
      b+='<div class="schtimes">';
      sch.p.forEach(function(p,i){b+='<div class="schtr"><b>'+(i+1)+'교시</b><div class="ttime"><input type="time" step="300" value="'+fmtHM(p.s)+'" data-chg="sch-time" data-k="s" data-i="'+i+'" aria-label="'+(i+1)+'교시 시작"><span>~</span><input type="time" step="300" value="'+fmtHM(p.e)+'" data-chg="sch-time" data-k="e" data-i="'+i+'" aria-label="'+(i+1)+'교시 끝"></div></div>';});
      b+='<div class="row" style="margin-top:8px"><button class="btn small" data-act="sch-padd"'+(sch.p.length>=10?' disabled':'')+'>교시 추가</button><button class="btn small" data-act="sch-pdel"'+(sch.p.length<=1?' disabled':'')+'>마지막 교시 빼기</button></div></div>';
    }
    b+='</div>';
  }
  // 바깥(어두운 곳)을 눌러도 닫히지 않게: 자판이 내려가며 화면이 움직일 때 잘못 눌려 닫히는 것 막기
  return dlg('wide',{id:'school',t:mine?'학교 시간표':esc(V.byId[who].name)+'의 학교 시간표'},b).replace('<div class="scrim" data-act="modal-close"></div>','<div class="scrim"></div>');
}

/* ---------- 확인 필요: 지울 시간 계산 ---------- */
function flagPlan(V,f){
  var sid=f.sid,out={},tot=0;
  if(f.cd&&typeof f.cd==='object'){
    Object.keys(f.cd).forEach(function(d){var want=Math.max(0,+f.cd[d]||0),have=+dayOf(V,f.mid,d).mins[sid]||0,n=Math.min(want,have);if(n>0){out[d]=n;tot+=n;}});
    return {d:out,total:tot};
  }
  var left=Math.min(300,Math.max(0,Math.round((+f.end-(+f.start))/60000))),ds=[fd(new Date(+f.end)),fd(new Date(+f.start))];
  ds.forEach(function(d){if(left<=0||out[d]!=null)return;var have=+dayOf(V,f.mid,d).mins[sid]||0,n=Math.min(left,have);if(n>0){out[d]=n;tot+=n;left-=n;}});
  return {d:out,total:tot};
}
function editDayOf(mid,date,fn){
  var V=view();if(!need())return;
  var d=clone(dayOf(V,mid,date));fn(d,V);
  if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;
  save('days/'+mid+'_'+date,d);
}
