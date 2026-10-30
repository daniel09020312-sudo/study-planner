/* ---------- v55: 잉크 선물을 게임으로: 선물 상자, 퀴즈, 가위바위보 ----------
   gifts/<id>={from,to,n,at,g:'box'|'quiz'|'rps',st:'wait'|'done'|'back',got, r(상자 결과), q(문제), h(정답·낸 손 확인값), tries}
   기다리는 동안은 보낸 사람 잉크에서 n이 빠져 있고, 끝나면 got만큼만 옮겨지고 나머지는 돌아온다. 'back'은 회수 */
var GG_TYPES=[['now','바로 주기'],['box','선물 상자'],['quiz','퀴즈'],['rps','가위바위보']],RPS=[['r','바위'],['p','보'],['s','가위']];
function ggHash(id,s){var t=String(id)+'|'+String(s),h=5381;for(var i=0;i<t.length;i++)h=((h<<5)+h+t.charCodeAt(i))|0;return (h>>>0).toString(36);}
function ggNorm(a){return String(a||'').replace(/\s+/g,'').toLowerCase();}
function ggBoxRoll(n){var p=[[.3,3],[.5,4],[.7,2],[1,1]],t=0,i,r=Math.random()*10;for(i=0;i<p.length;i++){t+=p[i][1];if(r<t)break;}return Math.max(1,Math.round(n*p[Math.min(i,p.length-1)][0]));}
function ggName(g){return g==='box'?'선물 상자':g==='quiz'?'퀴즈 선물':g==='rps'?'가위바위보 선물':'선물';}
function ggPanel(){
  var g=S.giftG||'now',b='<div class="fld ggsel"><h3>주는 방식</h3><div class="chips">';
  GG_TYPES.forEach(function(x){b+=chipBtn('gg-type','g',x[0],x[1],g===x[0]);});
  b+='</div>';
  if(g==='box')b+='<p class="hint">상자를 열면 보낸 잉크의 30~100% 중 하나가 나옵니다. 남은 건 돌아옵니다.</p>';
  if(g==='quiz')b+='<input type="text" data-draft="ggQ" data-live="1" maxlength="60" placeholder="문제 (예: 우리 반 담임 선생님 이름은?)" aria-label="문제"><input type="text" data-draft="ggA" data-live="1" maxlength="30" placeholder="정답" aria-label="정답" style="margin-top:6px"><p class="hint">한 번에 맞히면 전부, 두 번째 2/3, 세 번째 1/3. 세 번 다 틀리면 돌아옵니다.</p>';
  if(g==='rps'){b+='<div class="chips" style="margin-top:4px">';RPS.forEach(function(x){b+=chipBtn('gg-rps-pick','m',x[0],x[1],S.ggMove===x[0]);});b+='</div><p class="hint">내가 낼 손을 미리 고릅니다. 상대가 이기면 전부, 비기면 절반, 지면 1/5.</p>';}
  return b+'</div>';
}
function ggReady(){
  var g=S.giftG||'now';
  if(g==='quiz')return !!String(S.draft.ggQ||'').trim()&&!!ggNorm(S.draft.ggA);
  if(g==='rps')return !!S.ggMove;
  return true;
}
/* 메시지 말풍선 */
function giftBubble(V,x,pick){
  if(!x.gg)return '<div class="bb gift"'+pick+'><span class="gfi">'+INK_SVG+'<b>잉크 '+(+x.gift||0)+'방울</b> 선물</span>'+(x.text?'<span class="gft">'+esc(x.text)+'</span>':'')+'</div>';
  var G=obj(V.gifts[x.gg]),st=G.st||'wait',me=V.me,mine=G.from===me,h='<div class="bb gift gg"'+pick+'><span class="gfi">'+INK_SVG+'<b>'+esc(ggName(G.g))+'</b> 잉크 '+(+G.n||0)+'방울</span>';
  if(x.text)h+='<span class="gft">'+esc(x.text)+'</span>';
  if(st==='done')h+='<span class="ggres">'+(+G.got>0?'<b>'+(+G.got)+'방울</b>을 받았습니다':'아쉽게도 0방울. 보낸 잉크는 돌아갔습니다')+'</span>';
  else if(st==='back')h+='<span class="ggres">보낸 사람이 회수했습니다</span>';
  else if(G.to===me)h+='<button class="btn small primary" data-act="gg-play" data-id="'+esc(x.gg)+'">'+(G.g==='box'?'상자 열기':G.g==='quiz'?'문제 풀기':'가위바위보 하기')+'</button>';
  else if(mine)h+='<span class="ggres">상대가 열기를 기다리는 중</span><button class="btn small" data-act="gg-back" data-id="'+esc(x.gg)+'">'+(S.confirm==='ggback:'+x.gg?'한 번 더 누르면 회수':'회수')+'</button>';
  return h+'</div>';
}
/* 게임 창 */
function modalGG(V){
  var id=S.modal.id,G=obj(V.gifts[id]),from=V.byId[G.from],R=S.ggRes&&S.ggRes.id===id?S.ggRes:null;
  if(!G.g||G.to!==V.me){S.modal=null;return '';}
  var b='<p class="hint">'+esc(from?from.name:'누군가')+' 님이 보낸 '+esc(ggName(G.g))+' · 잉크 '+(+G.n||0)+'방울</p>';
  if(R&&Date.now()-R.t<1300&&G.g==='box')b+='<div class="ggbox opening" aria-label="상자를 여는 중"><div class="ggb"></div></div>';
  else if(G.st==='done'||R){
    var got=R?R.got:+G.got||0;
    b+='<div class="ggwin'+(got>0?'':' zero')+'"><b>'+got+'</b><span>방울</span></div><p class="ggmsg">'+esc(R&&R.msg||'')+'</p>';
    return dlg('',{id:'gg',t:ggName(G.g)},b,'<div class="df"><button class="btn primary" data-act="modal-close">확인</button></div>');
  }else if(G.g==='box'){
    b+='<div class="ggbox"><div class="ggb"></div></div>';
    return dlg('',{id:'gg',t:'선물 상자'},b,'<div class="df"><button class="btn primary" data-act="gg-box">열기</button></div>');
  }else if(G.g==='quiz'){
    var tr=+G.tries||0;
    b+='<div class="ggq">'+esc(G.q||'')+'</div><input type="text" data-draft="ggTry" data-enter="gg-ans" maxlength="30" placeholder="정답" aria-label="정답"><p class="hint">남은 기회 '+(3-tr)+'번 · 지금 맞히면 '+ggQuizAmt(+G.n,tr)+'방울</p>';
    return dlg('',{id:'gg',t:'퀴즈 선물'},b,'<div class="df"><button class="btn primary" data-act="gg-ans">제출</button></div>');
  }else if(G.g==='rps'){
    b+='<div class="ggrps">';RPS.forEach(function(x){b+='<button class="btn" data-act="gg-rps" data-v="'+x[0]+'">'+x[1]+'</button>';});b+='</div>';
    return dlg('',{id:'gg',t:'가위바위보'},b,'');
  }
  return dlg('',{id:'gg',t:ggName(G.g)},b,'');
}
function ggQuizAmt(n,tr){return tr===0?n:tr===1?Math.ceil(n*2/3):Math.ceil(n/3);}
function ggFinish(V,id,got,msg){
  var G=clone(obj(V.gifts[id]));G.st='done';G.got=Math.max(0,Math.min(+G.n||0,got));save('gifts/'+id,G);
  save('msgs/'+rid('x'),{from:V.me,to:G.from,text:ggName(G.g)+' 결과: '+(G.got>0?G.got+'방울을 받았습니다.':'0방울. 보낸 잉크는 돌아갔습니다.'),at:Date.now()});
  S.ggRes={id:id,got:G.got,msg:msg,t:Date.now()};
  if(G.g==='box')setTimeout(function(){render();},1350);
}
