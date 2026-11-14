/* ---------- v89: 전체 할 일 창(창 'gall'): 날짜마다 들어 있는 내 할 일을 모두 과목별 칸으로 한 화면에.
   완료 표시는 날짜 상관없이(goal-toggle). 이 창에서 뺀 할 일은 progress.<나>.gah={'<날짜>|<id>':1}(할 일 자체는 그대로), '뺀 할 일'에서 다시 넣기.
   이 창에서 새 할 일 더하기(날짜·과목 골라서). 기본은 최근 일주일(오늘-7일)부터 앞으로 전부, '일주일 전 것도 보기'(S.ga.old)로 전체 ---------- */
var GA_F=[['all','전체'],['left','남은 일'],['done','끝낸 일']];
function gaHid(V){return obj(obj(V.progress[V.me]).gah);}
function gaAll(V){
  var out=[],pre=V.me+'_';
  Object.keys(V.days).forEach(function(k){
    if(k.indexOf(pre)!==0)return;var d=k.slice(pre.length);if(!/^\d{4}-\d\d-\d\d$/.test(d))return;
    dayOf(V,V.me,d).goals.forEach(function(g,i){if(g&&g.id&&!g.mv&&String(g.text||'').trim())out.push({d:d,g:g,i:i,k:d+'|'+g.id});});
  });
  return out.sort(function(a,b){return a.d<b.d?-1:a.d>b.d?1:a.i-b.i;});
}
function gaDateLab(d){var x=pd(d);return (x.getMonth()+1)+'/'+x.getDate()+' '+DOW[x.getDay()];}
function modalGAll(V){
  var G=S.ga,t=today(),hid=gaHid(V),all=gaAll(V),wk=addDays(t,-7),nOld=all.filter(function(x){return !hid[x.k]&&x.d<wk;}).length,inV=all.filter(function(x){return !hid[x.k]&&(G.old||x.d>=wk);}),out=all.filter(function(x){return hid[x.k];});
  var nDone=inV.filter(function(x){return x.g.done;}).length,list=G.hid?out:inV.filter(function(x){return G.f==='left'?!x.g.done:G.f==='done'?x.g.done:true;});
  var b='<div class="ibadd gaadd"><div class="chips scroll">'+mySubs(V).map(function(s){return chipBtn('ga-sid','sid',s.id,s.name,G.sid===s.id);}).join('')+'</div>';
  b+='<div class="row"><input type="date" class="gadate" data-draft="gaDate" min="'+t+'" max="'+CAL_MAX+'-31" aria-label="넣을 날짜"><input type="text" id="gaText" data-draft="gaText" data-enter="ga-add" maxlength="90" placeholder="새 할 일 (날짜를 고르고 적기)" aria-label="새 할 일"><button class="btn primary" data-act="ga-add">더하기</button></div></div>';
  b+='<div class="ibhead gahead"><span>'+(G.hid?'뺀 할 일 '+out.length+'개':'할 일 '+inV.length+'개, 끝낸 일 '+nDone+'개')+'</span><span class="ibview">'+(G.hid?'':GA_F.map(function(x){return '<button class="chip" data-act="ga-f" data-v="'+x[0]+'" aria-pressed="'+(G.f===x[0]?'true':'false')+'">'+x[1]+'</button>';}).join(''))+(G.hid?'':'<button class="chip" data-act="ga-old" aria-pressed="'+(G.old?'true':'false')+'">'+(G.old?'일주일 전 것 숨기기':'일주일 전 것도 보기'+(nOld?' '+nOld:''))+'</button>')+'<button class="chip" data-act="ga-hid" aria-pressed="'+(G.hid?'true':'false')+'">'+(G.hid?'돌아가기':'뺀 할 일 '+out.length)+'</button></span></div>';
  if(!list.length)b+='<p class="empty ibempty">'+(G.hid?'이 창에서 뺀 할 일이 없습니다.':'보여 줄 할 일이 없습니다.')+'</p>';
  else{
    var grp={},keys=[];
    list.forEach(function(x){var k=V.subById[x.g.sid]&&!isEtcGoal(x.g)?x.g.sid:'';if(!grp[k]){grp[k]=[];keys.push(k);}grp[k].push(x);});
    keys.sort(function(a,c){return ibSubRank(V,a)-ibSubRank(V,c);});
    b+='<div class="ibcols gacols">';
    keys.forEach(function(k){
      var xs=grp[k],dn=xs.filter(function(x){return x.g.done;}).length;
      b+='<section class="ibcol gacol"'+(k?' style="--sc:'+subCol(V,k)+'"':'')+'><ul class="iblist"><li class="ibgrp"><i aria-hidden="true"></i><b>'+esc(k?V.subName[k]:'과목 없음·기타')+'</b><small>'+dn+'/'+xs.length+'</small>'+(k&&!G.hid?'<button class="linkbtn ibgadd" data-act="ga-addsub" data-v="'+esc(k)+'">+ 추가</button>':'')+'</li>';
      xs.forEach(function(x){
        var g=x.g,past=x.d<t,lock=doneLocked(V,x.d);
        b+='<li class="ibrow garow'+(g.done?' done':'')+(x.d===t?' today':'')+'" data-k="'+esc(x.k)+'">';
        b+='<button class="gack" data-act="goal-toggle" data-date="'+x.d+'" data-id="'+esc(g.id)+'" aria-pressed="'+(g.done?'true':'false')+'" aria-label="'+esc(g.text)+(g.done?' 끝냄 풀기':' 끝냄')+'"'+(lock?' disabled':'')+'><i aria-hidden="true"></i></button>';
        b+='<span class="gatx"><b>'+esc(g.text)+'</b><small class="gad'+(past&&!g.done?' late':'')+'">'+(x.d===t?'오늘':gaDateLab(x.d))+'</small></span>';
        b+='<button class="del" data-act="'+(G.hid?'ga-show':'ga-hide')+'" data-v="'+esc(x.k)+'">'+(G.hid?'다시 넣기':'빼기')+'</button></li>';
      });
      b+='</ul></section>';
    });
    b+='</div>';
  }
  return dlg('wide ibbig',{id:'gall',t:'전체 할 일'},b,'<div class="df"><span class="hint">동그라미를 누르면 날짜와 상관없이 끝냄 표시가 바뀝니다. \'빼기\'는 이 창에서만 숨기고 할 일은 그대로 둡니다.</span></div>');
}
function gaAdd(){
  var V=view();if(!V.me||!need())return;
  var txt=String(S.draft.gaText||'').trim(),d=String(S.draft.gaDate||'')||today();
  if(!txt){flash('할 일을 적어 주세요.');return;}
  if(!/^\d{4}-\d\d-\d\d$/.test(d)||d<today()){flash('오늘이나 앞으로의 날짜를 고르세요.');return;}
  if(!canAddTo(V,d)){flash('이 날에는 할 일을 더할 수 없습니다.');return;}
  if(dayOf(V,V.me,d).goals.length>=GMAX){flash(shortDate(d)+'에는 할 일이 가득 찼습니다.');return;}
  var sid=S.ga.sid||'',sn=snap(['days/'+V.me+'_'+d]);
  editDay(d,function(dd){dd.goals.push({id:rid('g'),text:txt.slice(0,90),sid:sid,done:false});});
  S.draft.gaText='';S.focusAfter='gaText';flash(gaDateLab(d)+'에 더했습니다.',sn);
}
