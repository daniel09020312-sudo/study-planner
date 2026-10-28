/* ---------- v47: 끄는 걸 깜빡하고 공부 안 한 시간이 기록됐을 때, 그만큼 빼기 ---------- */
var TRIM_CH=[10,20,30,60,90];
function trimInit(el){
  var V=view(),L=V.me&&liveOf(V,V.me),stop=!!L&&!!el&&el.getAttribute('data-stop')==='1';
  S.trim={stop:stop,date:today(),sid:stop?L.sid:'',n:30};S.draft.trimN='';
}
function trimPend(V,L){return L?Math.max(0,Math.floor(lv(L,Date.now()).focus/60000)-credited(L)):0;}
function trimRows(V,date){
  var d=dayOf(V,V.me,date),L=date===today()&&S.trim&&S.trim.stop?liveOf(V,V.me):null,pend=trimPend(V,L),rows=[],seen={};
  Object.keys(d.mins).forEach(function(k){var m=(+d.mins[k]||0)+(L&&L.sid===k?pend:0);if(m>0){rows.push({sid:k,mins:m});seen[k]=1;}});
  if(L&&!seen[L.sid]&&pend>0)rows.push({sid:L.sid,mins:pend});
  return rows;
}
function trimSel(V){
  var T=S.trim,rows=trimRows(V,T.date),r=rows.filter(function(x){return x.sid===T.sid;})[0]||rows[0]||null;
  var typed=Math.round(+S.draft.trimN),n=typed>0?typed:Math.round(+T.n)||0;
  return {rows:rows,row:r,n:n,ok:!!r&&n>=1&&n<=r.mins};
}
function modalTrim(V){
  var T=S.trim,sel=trimSel(V),yd=addDays(today(),-1),b='<p class="hint">타이머를 끄는 걸 깜빡해서, 공부하지 않은 시간까지 기록됐다면 그만큼 빼 주세요. 실제로 공부한 시간만 남고 점수도 그에 맞게 다시 계산됩니다.</p>';
  if(!T.stop){
    b+='<div class="fld"><h3>날짜</h3><div class="chips">'+chipBtn('trim-set','date',today(),'오늘',T.date===today());
    if(!dayLocked(V,yd))b+=chipBtn('trim-set','date',yd,'어제',T.date===yd);
    b+='</div></div>';
  }
  b+='<div class="fld"><h3>과목</h3>';
  if(!sel.rows.length)b+='<p class="empty">이 날 기록된 공부 시간이 없습니다.</p>';
  else{b+='<div class="chips">';sel.rows.forEach(function(r){b+=chipBtn('trim-set','sid',r.sid,subLabel(V,r.sid)+' '+fmtMins(r.mins),sel.row&&sel.row.sid===r.sid);});b+='</div>';}
  b+='</div><div class="fld"><h3>뺄 시간</h3><div class="chips">';
  TRIM_CH.forEach(function(n){b+=chipBtn('trim-set','n',String(n),n>=60?(n/60)+'시간'+(n%60?' '+n%60+'분':''):n+'분',!(+S.draft.trimN>0)&&+T.n===n);});
  b+='</div><input type="number" inputmode="numeric" min="1" max="1200" data-draft="trimN" data-live="1" placeholder="직접 입력 (분)" aria-label="뺄 시간 직접 입력(분)" style="margin-top:8px"></div>';
  if(sel.row)b+='<p class="hint">'+(sel.ok?esc(subLabel(V,sel.row.sid))+' '+fmtMins(sel.row.mins)+' → <b>'+fmtMins(sel.row.mins-sel.n)+'</b>':'뺄 시간은 1분 이상, 기록된 '+fmtMins(sel.row.mins)+' 이하로 넣어 주세요.')+'</p>';
  return dlg('wide',{id:'trim',t:T.stop?'시간 빼고 끝내기':'공부 시간 빼기'},b,'<span class="hint">'+(T.stop?'타이머를 끝내고 빼는 만큼을 뺍니다.':'오늘과 어제 기록만 고칠 수 있습니다.')+'</span><div class="df"><button class="btn primary" data-act="trim-go"'+(sel.ok?'':' disabled')+'>'+(T.stop?'빼고 끝내기':'빼기')+'</button></div>');
}
function trimGo(){
  var V=view(),T=S.trim;if(!T||!V.me||!need())return;
  var sel=trimSel(V);if(!sel.ok)return;
  var sid=sel.row.sid,n=sel.n,date=T.date,stop=T.stop;
  if(date!==today()&&dayLocked(V,date)){flash('이 날은 마감이 지나 고칠 수 없습니다.');return;}
  if(stop)stopTimer();
  editDay(date,function(d){var m=Math.max(0,(+d.mins[sid]||0)-n);if(m)d.mins[sid]=m;else delete d.mins[sid];hhSub(d,sid,n);});
  if(S.modal&&S.modal.type==='trim')closeModal();
  flash(subLabel(V,sid)+'에서 '+fmtMins(n)+'을 뺐습니다.');
}
