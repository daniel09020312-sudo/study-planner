/* ---------- v78: 잉크 뿌리기 방식 늘리기, 결과는 각자 열어 볼 때까지 숨김 ----------
   gifts/<id>.g: first(선착순) rand(행운 봉투, amts) quiz(퀴즈, q·h) wheel(뽑기) ladder(사다리)
                 draw(마감 추첨, end·seed·k) pot(모여라 나눠 갖기, end) best(오늘의 공부왕, end·day, win은 마감 뒤 처음 본 사람이 적음)
   받기: 봉투는 progress.<나>.lc={id:누른 시각}, 퀴즈는 progress.<나>.lq={id:맞힌 시각}, 추첨·모여라는 progress.<나>.lj={id:참여 시각}
   열어 본 결과는 이 기기 gbb_lotseen(목록)에 적어 둔다 */
var LOT2={rand:1,quiz:1,draw:1,pot:1,best:1};
var LOT_MODES=[
  ['first','선착순','먼저 받기를 누른 사람부터 똑같이 나눠 가져갑니다.'],
  ['rand','행운 봉투','먼저 연 사람부터 봉투를 하나씩 가져갑니다. 봉투마다 든 잉크가 달라서 열어 봐야 압니다.'],
  ['quiz','퀴즈','문제를 내고, 먼저 맞힌 사람부터 받습니다. 한 사람당 세 번까지 답할 수 있습니다.'],
  ['wheel','뽑기','방 사람 모두 중 1명이 받습니다. 결과는 각자 열어 볼 때 돌림판으로 나옵니다.'],
  ['ladder','사다리타기','방 사람 모두 중 여러 명이 받습니다. 결과는 각자 열어 볼 때 사다리로 나옵니다.'],
  ['draw','마감 추첨','마감까지 참여한 사람 중에서 추첨합니다. 결과는 마감 뒤에 열어 볼 수 있습니다.'],
  ['pot','모여라','마감까지 참여한 사람이 모두 똑같이 나눠 가집니다. 많이 모일수록 한 사람 몫이 줄어듭니다.'],
  ['best','오늘의 공부왕','마감 때 오늘 공부 시간이 가장 긴 사람이 모두 가져갑니다.']
];
var LOT_DL=[[10,'10분'],[30,'30분'],[60,'1시간'],[180,'3시간'],[-1,'오늘 밤 11시']];
function lotName(g){for(var i=0;i<LOT_MODES.length;i++)if(LOT_MODES[i][0]===g)return LOT_MODES[i][1];return '잉크 뿌리기';}
function lotSeen(id){try{return JSON.parse(localStorage.getItem('gbb_lotseen')||'[]').indexOf(id)>=0;}catch(e){return false;}}
function lotSeeMark(id){try{var a=JSON.parse(localStorage.getItem('gbb_lotseen')||'[]');if(a.indexOf(id)<0){a.push(id);localStorage.setItem('gbb_lotseen',JSON.stringify(a.slice(-150)));}}catch(e){}}
function lotNorm(s){return String(s||'').replace(/\s+/g,'').toLowerCase();}
function lotClaimsBy(V,id,G,f){
  var k=Math.max(1,+G.k||1);
  return V.roster.filter(function(m){return m.id!==G.from&&obj(obj(V.progress[m.id])[f])[id];}).map(function(m){return {m:m.id,at:+obj(obj(V.progress[m.id])[f])[id]||0};}).sort(function(a,b){return a.at-b.at||(a.m<b.m?-1:1);}).slice(0,k).map(function(x){return x.m;});
}
/* 마감 추첨·모여라 참여자: 마감 전에 참여한 사람(보낸 사람 빼고), 이름 순서가 아니라 id 순서로 고정 */
function lotJoiners(V,id,G){
  var end=+G.end||0;
  return V.roster.filter(function(m){if(m.id===G.from)return false;var t=+obj(obj(V.progress[m.id]).lj)[id]||0;return t>0&&(!end||t<=end);}).map(function(m){return m.id;}).sort();
}
function lotRandAmts(n,k,seed){
  var r=lotRng(seed),w=[],s=0,i;for(i=0;i<k;i++){var x=0.25+r();w.push(x);s+=x;}
  var a=w.map(function(x){return Math.max(1,Math.floor(x/s*n));}),t=a.reduce(function(p,c){return p+c;},0);
  a[Math.floor(r()*k)]+=n-t;if(a.some(function(x){return x<1;})){a=[];for(i=0;i<k;i++)a.push(Math.floor(n/k)+(i<n%k?1:0));}
  return a;
}
function lotDayMins(V,mid,d){var x=dayOf(V,mid,d);return sumMins(x.mins)+Math.min(sumMins(x.manual),RULE.manualMax);}
/* 결과 계산: settled면 win이 확정. 잉크 계산(inkLocal)과 화면이 같은 값을 쓴다 */
function lotWin(V,id,G){
  var n=Math.max(0,Math.floor(+G.n||0)),k=Math.max(1,+G.k||1),now=Date.now(),win={},settled=false,back=G.st==='back',i;
  if(G.g==='rand'){
    var cl=lotClaimsBy(V,id,G,'lc'),am=arr(G.amts);cl.forEach(function(m,j){win[m]=+am[j]||0;});settled=back||cl.length>=k;
  }else if(G.g==='quiz'){
    var cq=lotClaimsBy(V,id,G,'lq'),eq=Math.floor(n/k);cq.forEach(function(m){win[m]=eq;});settled=back||cq.length>=k;
  }else if(G.g==='draw'||G.g==='pot'){
    if(back)return {win:{},settled:true,sum:0,who:[]};
    if(now<(+G.end||0))return {win:{},settled:false,sum:0,who:[]};
    var who=lotJoiners(V,id,G);settled=true;
    if(who.length){
      if(G.g==='pot'){var ep=Math.floor(n/who.length);who.forEach(function(m){win[m]=ep;});}
      else if(who.length<=k){var ea=Math.floor(n/who.length);who.forEach(function(m){win[m]=ea;});}
      else win=lotResult({g:k===1?'wheel':'ladder',k:k,n:n},who,+G.seed||1);
    }
    var sd=0;for(i in win)sd+=win[i];return {win:win,settled:settled,sum:sd,who:who};
  }else if(G.g==='best'){
    if(back)return {win:{},settled:true,sum:0};
    if(G.win)win=obj(G.win);
    else{
      if(now<(+G.end||0))return {win:{},settled:false,sum:0};
      var top=null,tm=0;V.roster.forEach(function(m){if(m.id===G.from)return;var mm=lotDayMins(V,m.id,G.day);if(mm>tm){tm=mm;top=m.id;}});
      if(top)win[top]=n;
    }
    settled=true;
  }
  var s=0;for(i in win)s+=win[i];return {win:win,settled:settled,sum:s};
}
/* 공부왕은 마감 뒤 처음 본 사람이 결과를 적어 둔다(그 뒤로 공부 시간이 바뀌어도 그대로) */
var LOT_TICK={};
function lotTick(){
  var V=V0;if(!V||!V.me||!S.ready||!canWrite())return;var now=Date.now(),need2=false;
  Object.keys(obj(V.gifts)).forEach(function(id){
    var G=obj(V.gifts[id]);if(!LOT2[G.g]||G.to!=='all'||G.st==='back')return;
    if((G.g==='draw'||G.g==='pot'||G.g==='best')&&+G.end&&now>=+G.end&&!LOT_TICK[id]){LOT_TICK[id]=1;need2=true;}
    if(G.g==='best'&&!G.win&&now>=+G.end&&!LOT_TICK['w'+id]&&netFresh()){LOT_TICK['w'+id]=1;var r=lotWin(V,id,G),Gn=clone(G);Gn.win=r.win;Gn.st='done';Gn.done=now;save('gifts/'+id,Gn);}
  });
  if(need2)render();
}
function lotLeft(end){var s=Math.max(0,Math.round((+end-Date.now())/60000));return s>=60?Math.floor(s/60)+'시간 '+(s%60?s%60+'분':''):s+'분';}
function lotWinList(V,win,amt){var ks=Object.keys(win);if(!ks.length)return '받은 사람이 없어 잉크가 돌아갔습니다';return ks.map(function(m){return '<b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b>'+(amt?' '+win[m]+'방울':'');}).join(', ');}
function lotBubble(V,x,pick){
  var id=x.lot,G=obj(V.gifts[id]);
  if(G.g==='first')return lotFirstBubble(V,x,pick);
  var mine=G.from===V.me,k=Math.max(1,+G.k||1),n=+G.n||0,back=G.st==='back',seen=lotSeen(id)||mine&&back;
  var head={rand:'행운 봉투 '+k+'개',quiz:'퀴즈 · 먼저 맞힌 '+k+'명',wheel:'뽑기 · 1명',ladder:'사다리타기 · '+k+'명',draw:'마감 추첨 · '+k+'명',pot:'모여라 · 참여자 모두',best:'오늘의 공부왕'}[G.g]||lotName(G.g);
  var h='<div class="bb gift lot lot2"'+pick+'><span class="gfi">'+INK_SVG+'<b>잉크 '+n+'방울</b> · '+esc(head)+'</span>';
  if(x.text)h+='<span class="gft">'+esc(x.text)+'</span>';
  if(back)return h+'<span class="ggres">보낸 사람이 거둬들였습니다</span></div>';
  var R=lotWin(V,id,G),btn=function(a,label,pri){return '<button class="btn small'+(pri?' primary':'')+'" data-act="'+a+'" data-id="'+esc(id)+'">'+label+'</button>';},row=[];
  if(G.g==='wheel'||G.g==='ladder'){
    if(seen)h+='<span class="ggres">'+lotWinList(V,obj(G.win),true)+'</span>';
    else h+='<span class="ggres lhid">누가 받았는지는 열어 봐야 압니다</span>';
    row.push(btn('lot-open',seen?esc(lotName(G.g))+' 다시 보기':'결과 열어 보기',!seen));
  }else if(G.g==='rand'){
    var cl=lotClaimsBy(V,id,G,'lc'),my=cl.indexOf(V.me);
    h+='<span class="ggres">봉투 '+cl.length+'/'+k+'개 열림'+(my>=0?' · 내 봉투 <b>'+(+arr(G.amts)[my]||0)+'방울</b>':'')+'</span>';
    if(R.settled&&seen)h+='<span class="ggres">'+lotWinList(V,R.win,true)+'</span>';
    if(!mine&&V.me&&my<0&&!R.settled)row.push(btn('lot-env','봉투 열기',true));
    if(R.settled&&!seen)row.push(btn('lot-open','누가 얼마 받았나 보기',true));
  }else if(G.g==='quiz'){
    var cq=lotClaimsBy(V,id,G,'lq'),me2=cq.indexOf(V.me)>=0,tr=+obj(S.lqTry)[id]||0;
    h+='<span class="lq">Q. '+esc(G.q||'')+'</span>';
    h+='<span class="ggres">맞힌 사람 '+cq.length+'/'+k+(cq.length?': '+lotWinList(V,R.win,false):'')+'</span>';
    if(!mine&&V.me&&!me2&&!R.settled){
      if(tr>=3)h+='<span class="ggres">세 번 다 틀렸습니다</span>';
      else h+='<span class="row"><input type="text" data-draft="lq:'+esc(id)+'" data-enter="lot-ans" data-id="'+esc(id)+'" maxlength="30" placeholder="정답 ('+(3-tr)+'번 남음)" aria-label="퀴즈 정답"><button class="btn small primary" data-act="lot-ans" data-id="'+esc(id)+'">답하기</button></span>';
    }
    if(me2)h+='<span class="ggres"><b>정답!</b> '+Math.floor(n/k)+'방울을 받았습니다</span>';
  }else if(G.g==='draw'||G.g==='pot'||G.g==='best'){
    var open=Date.now()<(+G.end||0);
    if(open){
      var dt=new Date(+G.end);
      h+='<span class="ggres">마감 '+pad2(dt.getHours())+':'+pad2(dt.getMinutes())+' (남은 시간 '+lotLeft(G.end)+')</span>';
      if(G.g!=='best'){
        var inn=+obj(obj(V.progress[V.me]).lj)[id]>0,cnt=V.roster.filter(function(m){return m.id!==G.from&&obj(obj(V.progress[m.id]).lj)[id];}).length;
        h+='<span class="ggres">참여 '+cnt+'명'+(G.g==='pot'&&cnt?' · 지금이면 1명당 '+Math.floor(n/cnt)+'방울':'')+'</span>';
        if(!mine&&V.me)row.push(btn('lot-join2',inn?'참여 취소':'참여',!inn));
      }else h+='<span class="ggres">마감 때 오늘 공부 시간이 가장 긴 사람이 받습니다</span>';
    }else{
      if(seen)h+='<span class="ggres">'+lotWinList(V,R.win,G.g!=='best'||true)+'</span>';
      else h+='<span class="ggres lhid">마감되었습니다. 결과는 열어 봐야 압니다</span>';
      row.push(btn('lot-open',seen?'결과 다시 보기':'결과 열어 보기',!seen));
    }
  }
  if(mine&&!R.settled&&G.g!=='wheel'&&G.g!=='ladder')row.push('<button class="btn small" data-act="lot-back" data-id="'+esc(id)+'">'+(S.confirm==='lotback:'+id?'한 번 더 누르면 거두기':'거두기')+'</button>');
  if(row.length)h+='<span class="row">'+row.join('')+'</span>';
  return h+'</div>';
}
function modalLotNew(V,ink){
  var L=S.lot,g=L.g,n=Math.floor(+S.draft.lotN||0),others=V.roster.filter(function(m){return m.id!==V.me;}).length,b='',md=LOT_MODES.filter(function(x){return x[0]===g;})[0]||LOT_MODES[0];
  b+='<div class="fld"><h3>방식</h3><div class="chips lmodes">'+LOT_MODES.map(function(x){return chipBtn('lot-set2','g',x[0],x[1],g===x[0]);}).join('')+'</div><p class="hint">'+esc(md[2])+'</p></div>';
  if(g==='quiz')b+='<div class="fld"><h3>문제</h3><input type="text" data-draft="lotQ" maxlength="60" placeholder="예: 미분계수의 정의에 나오는 극한 기호는?" aria-label="퀴즈 문제"><input type="text" data-draft="lotA" maxlength="30" placeholder="정답 (띄어쓰기·대소문자 상관없음)" aria-label="퀴즈 정답" style="margin-top:6px"></div>';
  if(g!=='wheel'&&g!=='pot'&&g!=='best'){var ks=[1,2,3,5,10];b+='<div class="fld"><h3>'+(g==='rand'?'봉투 수':g==='quiz'?'정답자 수':'받을 사람 수')+'</h3><div class="chips">'+ks.map(function(kk){return chipBtn('lot-set2','k',String(kk),kk+(g==='rand'?'개':'명'),L.k===kk);}).join('')+'</div></div>';}
  if(g==='draw'||g==='pot'||g==='best')b+='<div class="fld"><h3>마감</h3><div class="chips">'+LOT_DL.map(function(x){return chipBtn('lot-set2','dl',String(x[0]),x[1],L.dl===x[0]);}).join('')+'</div></div>';
  b+='<div class="fld"><h3>걸 잉크</h3><div class="chips gfamt">'+GIFT_AMTS.map(function(a){return '<button class="chip" data-act="lot-amt" data-v="'+a+'" aria-pressed="'+(n===a?'true':'false')+'"'+(!ink.unl&&a>ink.bal?' disabled':'')+'>'+inkTag(a)+'</button>';}).join('')+'<input type="number" inputmode="numeric" min="1" data-draft="lotN" data-live="1" placeholder="직접" aria-label="걸 잉크"></div><p class="hint">내 잉크 '+(ink.unl?'무제한':ink.bal+'방울')+'</p></div>';
  b+='<input type="text" data-draft="lotMsg" maxlength="40" placeholder="한마디 (예: 오늘 공부 수고했어)" aria-label="한마디">';
  var kk2=g==='wheel'||g==='pot'||g==='best'?1:L.k,ok=n>0&&n<=99999&&(ink.unl||n<=ink.bal)&&n>=kk2&&others>0;
  return dlg('',{id:'lotnew',t:'잉크 뿌리기'},b,'<div class="df"><button class="btn primary" data-act="lot-add2"'+(ok?'':' disabled')+'>'+(n>0&&!ink.unl&&n>ink.bal?'잉크가 모자랍니다':'전체 대화방에 올리기')+'</button></div>');
}
/* 결과 창: 뽑기·사다리·추첨은 돌림판·사다리로, 나머지는 카드가 하나씩 뒤집힌다 */
function modalLot(V){
  var id=S.modal.id,G=obj(V.gifts[id]),R=lotWin(V,id,G),b='',t=lotName(G.g)+' 결과';
  if(G.g==='wheel'||G.g==='ladder'){if(G.st!=='done'){S.modal=null;return '';}var who=arr(G.who);b=G.g==='wheel'?lotWheelSvg(V,who,obj(G.win)):lotLadderSvg(V,G,who);R={win:obj(G.win),settled:true};}
  else if(!R.settled){S.modal=null;return '';}
  else if(G.g==='draw'&&R.who&&R.who.length>Math.max(1,+G.k||1)){var kk=Math.max(1,+G.k||1);b=kk===1?lotWheelSvg(V,R.who,R.win):lotLadderSvg(V,{k:kk,seed:+G.seed||1},R.who);}
  else{var ks=Object.keys(R.win);b='<div class="lcards">'+(ks.length?ks.map(function(m,i){return '<div class="lcard'+(m===V.me?' me':'')+'" style="--d:'+(i*0.25)+'s"><b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b><span>'+R.win[m]+'방울</span></div>';}).join(''):'<p class="hint">받은 사람이 없어 잉크가 보낸 사람에게 돌아갔습니다.</p>')+'</div>';}
  var ks2=Object.keys(R.win),fast=!(G.g==='wheel'||G.g==='ladder'||G.g==='draw'&&R.who&&R.who.length>Math.max(1,+G.k||1));
  b+='<div class="lres'+(fast?' fast':'')+'">'+ks2.map(function(m){return '<span'+(m===V.me?' class="me"':'')+'><b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b> '+R.win[m]+'방울</span>';}).join('')+'</div>';
  if(G.g==='best'&&ks2.length)b+='<p class="hint center">오늘 공부 '+lotFmtMin(lotDayMins(V,ks2[0],G.day))+'</p>';
  return dlg('wide',{id:'lot',t:t},b,'<div class="df"><button class="btn primary" data-act="modal-close">확인</button></div>');
}
function lotFmtMin(m){m=Math.round(+m||0);return (m>=60?Math.floor(m/60)+'시간 ':'')+(m%60?m%60+'분':m>=60?'':'0분');}
