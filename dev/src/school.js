/* ---------- 학교 시간표 ---------- */
var SCH_DEF=[[520,570],[580,630],[640,690],[700,750],[810,860],[870,920],[930,980]];
var SCH_QUICK=['창체','자습','동아리','진로'];
var SCH_DAYS=[1,2,3,4,5];
function schOf(V,mid){
  var t=obj(obj(V.progress[mid]).tt),s=obj(t.sch),w=obj(s.w);
  var p=arr(s.p).filter(function(x){return x&&+x.e>+x.s;}).map(function(x){return {s:+x.s,e:+x.e};});
  var has=Object.keys(w).some(function(k){return Object.keys(obj(w[k])).length>0;});
  return {p:p.length?p:SCH_DEF.map(function(x){return {s:x[0],e:x[1]};}),w:w,has:has};
}
function schCell(V,sch,dw,i){
  var c=obj(obj(sch.w[dw])['p'+i]);
  if(c.s&&V.subName[c.s])return {sid:c.s,name:V.subName[c.s]};
  if(c.t)return {t:String(c.t),name:String(c.t)};
  return null;
}
function editSch(fn){
  editTT(function(T){
    var s=clone(obj(T.sch));s.p=arr(s.p).filter(function(x){return x&&+x.e>+x.s;});s.w=obj(s.w);
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
      var c=schCell(V,sch,d,i),on=!!(sel&&sel.d===d&&sel.i===i),col=c&&c.sid?subCol(V,c.sid):SGRAY,lab=DOW[d]+'요일 '+(i+1)+'교시'+(c?', '+c.name:', 비어 있음');
      var inner=c?'<span>'+esc(c.name)+'</span>':(mine?'<span class="ph">+</span>':'');
      b+='<td class="'+(d===tdw?'today':'')+'">'+(mine?'<button class="schc'+(c?' f':'')+(on?' on':'')+'" data-act="sch-sel" data-d="'+d+'" data-i="'+i+'" style="--sc:'+col+'" aria-pressed="'+(on?'true':'false')+'" aria-label="'+esc(lab)+'">'+inner+'</button>':'<div class="schc'+(c?' f':'')+'" style="--sc:'+col+'" aria-label="'+esc(lab)+'">'+inner+'</div>')+'</td>';
    });
    b+='</tr>';
  });
  b+='</tbody></table></div>';
  if(mine&&sel){
    var cur=schCell(V,sch,sel.d,sel.i);
    b+='<div class="schpick" id="schPick"><h3>'+DOW[sel.d]+'요일 '+(sel.i+1)+'교시<small>'+fmtHM(sch.p[sel.i].s)+'~'+fmtHM(sch.p[sel.i].e)+'</small></h3><div class="chips">';
    b+=mySubs(V).map(function(s){return '<button class="chip sch-sub" data-act="sch-put" data-v="'+esc(s.id)+'" style="--sc:'+subCol(V,s.id)+'" aria-pressed="'+(cur&&cur.sid===s.id?'true':'false')+'"><i></i>'+esc(s.name)+'</button>';}).join('');
    b+=SCH_QUICK.map(function(t){return '<button class="chip" data-act="sch-put" data-t="'+esc(t)+'" aria-pressed="'+(cur&&cur.t===t?'true':'false')+'">'+esc(t)+'</button>';}).join('');
    b+='</div><div class="row" style="margin-top:10px"><input type="text" data-draft="schT" data-enter="sch-text" maxlength="12" placeholder="직접 쓰기" aria-label="과목 직접 쓰기"><button class="btn small" data-act="sch-text">넣기</button>'+(cur?'<button class="btn small" data-act="sch-clear">비우기</button>':'')+'</div></div>';
  }else if(mine)b+='<p class="hint" style="margin-top:12px">칸을 누르고 과목을 고르면 다음 교시로 넘어갑니다. 시간표의 학교 칸에도 교시별로 표시됩니다.</p>';
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
  return dlg('wide',{id:'school',t:mine?'학교 시간표':esc(V.byId[who].name)+'의 학교 시간표'},b);
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
