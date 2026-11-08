/* ---------- v81: 넣어 둔 할 일을 여러 개 골라 할 일 모음으로 거둬들이고(지난 날 못 끝낸 것도), 모음에서 날짜에 골고루 다시 나눠 넣기 ---------- */
/* 고른 할 일을 날짜에서 빼서 모음으로. 지난 날에서 뺀 것은 그 날에 '다른 날로 옮김'으로 남는다(guardDay) */
function gordCollect(){
  var V=view();if(!V.me||!need())return;
  var keys=gselKeys(),items=[],byd={};
  keys.forEach(function(s){var i=s.indexOf('|'),d=s.slice(0,i),id=s.slice(i+1),g=dayOf(V,V.me,d).goals.filter(function(q){return q&&q.id===id&&!q.mv;})[0];if(g&&!(g.done&&dayLocked(V,d))){items.push([d,g]);(byd[d]=byd[d]||[]).push(id);}});
  if(!items.length){flash('거둬들일 할 일을 고르세요.');return;}
  var have=ibItems(V).length;if(have+items.length>IB_MAX){flash('할 일 모음은 '+IB_MAX+'개까지입니다. '+(IB_MAX-have)+'개만 더 넣을 수 있습니다.');return;}
  items.sort(function(a,b){if(a[0]!==b[0])return a[0]<b[0]?-1:1;var gl=dayOf(V,V.me,a[0]).goals;return gl.indexOf(a[1])-gl.indexOf(b[1]);});
  var paths=['inbox/'+V.me];Object.keys(byd).forEach(function(d){paths.push('days/'+V.me+'_'+d);});var sn=snap(paths),now=Date.now(),newIds=[];
  Object.keys(byd).forEach(function(d){editDay(d,function(dd){dd.goals=dd.goals.filter(function(q){return !(q&&byd[d].indexOf(q.id)>=0&&!q.mv);});if(byd[d].indexOf(dd.focus)>=0)dd.focus=null;});});
  editInbox(function(dd){items.forEach(function(p,j){var g=p[1],x={t:String(g.text||'').slice(0,90),sid:g.sid||'',at:now+j,od:p[0]};['ct','ca','cu','cn'].forEach(function(k){if(g[k]!=null&&g[k]!=='')x[k]=g[k];});var nid=rid('i');newIds.push(nid);dd.items[nid]=x;});});
  S.gsel={};S.ib={sel:{},week:wkStart(today()),sid:'',spread:S.ib&&S.ib.spread||3,start:today()};newIds.forEach(function(k){S.ib.sel[k]=1;});
  S.modal={type:'inbox'};S.closing=false;
  flash(items.length+'개를 할 일 모음으로 거둬들였습니다. 날짜를 골라 다시 나눠 넣으세요.',sn);
}
/* 골고루 나누기: start부터 n일 동안, 그날 할 일이 적은 날부터 하나씩(같으면 앞 날). 하루 GMAX를 넘지 않는다 */
function ibSpread(){
  var V=view(),I=S.ib||{},sel=Object.keys(obj(I.sel)).filter(function(k){return I.sel[k];}),items=ibItems(V).filter(function(x){return sel.indexOf(x.id)>=0;});
  if(!items.length){flash('나눌 할 일을 먼저 고르세요.');return;}
  var n=Math.max(1,+I.spread||3),st=I.start&&I.start>=today()?I.start:today(),days=[],cnt={},plan={};
  for(var i=0;i<n;i++){var d=addDays(st,i);days.push(d);cnt[d]=dayOf(V,V.me,d).goals.length;plan[d]=[];}
  var left=[];
  items.forEach(function(x){var best=null;days.forEach(function(d){if(cnt[d]>=GMAX)return;if(!best||cnt[d]<cnt[best])best=d;});if(!best){left.push(x);return;}cnt[best]++;plan[best].push(x);});
  var paths=['inbox/'+V.me];days.forEach(function(d){if(plan[d].length)paths.push('days/'+V.me+'_'+d);});var sn=snap(paths),put=[];
  days.forEach(function(d){if(!plan[d].length)return;editDay(d,function(dd){plan[d].forEach(function(x){var g={id:rid('g'),text:String(x.t).slice(0,90),sid:x.sid||'',done:false};['ct','ca','cu','cn'].forEach(function(k){if(x[k]!=null&&x[k]!=='')g[k]=x[k];});dd.goals.push(g);put.push(x.id);});});});
  editInbox(function(dd){put.forEach(function(id){delete dd.items[id];});});
  S.ib.sel={};
  var sum=days.filter(function(d){return plan[d].length;}).map(function(d){var dt=pd(d);return (dt.getMonth()+1)+'/'+dt.getDate()+' '+plan[d].length+'개';}).join(', ');
  flash(put.length+'개를 나눠 넣었습니다: '+sum+(left.length?' (자리가 없어 '+left.length+'개 남김)':''),sn);
}
function ibSpreadHtml(V,nsel){
  var I=S.ib,t=today(),st=I.start&&I.start>=t?I.start:t,n=+I.spread||3;
  var h='<div class="ibspread"><b>골고루 나누기</b><span class="chips">'+[[t,'오늘부터'],[addDays(t,1),'내일부터']].map(function(x){return chipBtn('ib-start','d',x[0],x[1],st===x[0]);}).join('')+'</span>';
  h+='<span class="chips">'+[1,2,3,4,5,7,10,14].map(function(k){return chipBtn('ib-n','n',String(k),k+'일',n===k);}).join('')+'</span>';
  h+='<button class="btn small primary" data-act="ib-spread"'+(nsel?'':' disabled')+'>'+(nsel?'고른 '+nsel+'개를 '+n+'일에 나누기':'할 일을 고르세요')+'</button><p class="hint">할 일이 적은 날부터 하나씩 넣습니다. 한 날만 고르려면 아래 날짜를 누르세요.</p></div>';
  return h;
}
