/* ---------- v56: 전체 대화방에 잉크 뿌리기: 돌림판(1명) 또는 사다리타기(여러 명)로 받을 사람을 정한다 ----------
   gifts/<id>={from,to:'all',n,at,g:'wheel'|'ladder',k(당첨 수),st:'open'|'done'|'back',who:[참여자],seed,win:{mid:방울}}
   참여는 각자 progress.<나>.lj={id:1}(여럿이 동시에 눌러도 겹치지 않게). 보낸 사람이 시작하면 그때 참여자로 결과를 정한다 */
var LOT_MAX={wheel:20,ladder:10};
function lotRng(seed){var a=seed>>>0;return function(){a=(a+0x6D2B79F5)>>>0;var t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296;};}
function lotParts(V,id,G){return V.roster.filter(function(m){return m.id!==G.from&&obj(obj(V.progress[m.id]).lj)[id];}).map(function(m){return m.id;});}
/* 사다리: 줄(rungs)과 아래 당첨 칸을 seed로 만들고, 위에서부터 따라 내려간다 */
function lotLadder(n,k,seed){
  var r=lotRng(seed),rows=Math.max(6,n+3),rung=[],i,j,prize=[];
  for(i=0;i<rows;i++){var row=[];for(j=0;j<n-1;j++){row.push(!(j>0&&row[j-1])&&r()<0.5);}rung.push(row);}
  var slots=[];for(i=0;i<n;i++)slots.push(i);
  for(i=slots.length-1;i>0;i--){j=Math.floor(r()*(i+1));var t=slots[i];slots[i]=slots[j];slots[j]=t;}
  for(i=0;i<n;i++)prize.push(false);slots.slice(0,k).forEach(function(s){prize[s]=true;});
  var end=[];for(var c=0;c<n;c++){var x=c;for(i=0;i<rows;i++){if(x<n-1&&rung[i][x])x++;else if(x>0&&rung[i][x-1])x--;}end.push(x);}
  return {rows:rows,rung:rung,prize:prize,end:end};
}
function lotResult(G,who,seed){
  var n=who.length,k=G.g==='wheel'?1:Math.max(1,Math.min(+G.k||1,n-1)),win={},tot=+G.n||0,ws=[];
  if(G.g==='wheel'){var r=lotRng(seed);ws=[who[Math.floor(r()*n)]];}
  else{var L=lotLadder(n,k,seed);who.forEach(function(m,i){if(L.prize[L.end[i]])ws.push(m);});}
  var each=Math.floor(tot/ws.length),rest=tot-each*ws.length;
  ws.forEach(function(m,i){win[m]=each+(i===0?rest:0);});
  return win;
}
function lotName(g){return g==='wheel'?'뽑기':g==='first'?'선착순':'사다리타기';}
/* 선착순: 각자 progress.<나>.lc={id:누른 시각}. 누른 시각 순서로 앞의 k명 */
function lotClaims(V,id,G){
  var k=Math.max(1,+G.k||1);
  return V.roster.filter(function(m){return m.id!==G.from&&obj(obj(V.progress[m.id]).lc)[id];}).map(function(m){return {m:m.id,at:+obj(obj(V.progress[m.id]).lc)[id]||0};}).sort(function(a,b){return a.at-b.at||(a.m<b.m?-1:1);}).slice(0,k).map(function(x){return x.m;});
}
function lotBubble(V,x,pick){
  if(obj(V.gifts[x.lot]).g==='first')return lotFirstBubble(V,x,pick);
  var id=x.lot,G=obj(V.gifts[id]),st=G.st||'open',parts=st==='done'?arr(G.who):lotParts(V,id,G),mine=G.from===V.me,inn=parts.indexOf(V.me)>=0;
  var h='<div class="bb gift lot"'+pick+'><span class="gfi">'+INK_SVG+'<b>잉크 '+(+G.n||0)+'방울 '+esc(lotName(G.g))+'</b>'+(G.g==='ladder'?' · '+(+G.k||1)+'명 당첨':'')+'</span>';
  if(x.text)h+='<span class="gft">'+esc(x.text)+'</span>';
  if(st==='back')return h+'<span class="ggres">보낸 사람이 취소했습니다</span></div>';
  if(st==='done'){
    var wn=obj(G.win);
    h+='<span class="ggres">'+Object.keys(wn).map(function(m){return '<b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b> '+wn[m]+'방울';}).join(', ')+'</span>';
    return h+'<button class="btn small" data-act="lot-view" data-id="'+esc(id)+'">'+esc(lotName(G.g))+' 보기</button></div>';
  }
  h+='<span class="ggres">참여 '+parts.length+'명'+(parts.length?': '+parts.slice(0,8).map(function(m){return esc(V.byId[m]?V.byId[m].name:'');}).join(', ')+(parts.length>8?' 외':''):'')+'</span><span class="row">';
  if(!mine&&V.me)h+='<button class="btn small'+(inn?'':' primary')+'" data-act="lot-join" data-id="'+esc(id)+'">'+(inn?'참여 취소':'참여')+'</button>';
  if(mine||adminId(V)===V.me){
    h+='<button class="btn small primary" data-act="lot-go" data-id="'+esc(id)+'"'+(parts.length<2?' disabled':'')+'>'+(parts.length<2?'2명 이상 모이면 시작':esc(lotName(G.g))+' 시작')+'</button>';
    if(mine)h+='<button class="btn small" data-act="lot-back" data-id="'+esc(id)+'">'+(S.confirm==='lotback:'+id?'한 번 더 누르면 취소':'취소')+'</button>';
  }
  return h+'</span></div>';
}
function modalLotNew(V,ink){
  var L=S.lot,n=Math.floor(+S.draft.lotN||0),others=V.roster.filter(function(m){return m.id!==V.me;}).length,b='<p class="hint">전체 대화방에 잉크를 걸고 받을 사람을 정합니다.</p>';
  b+='<div class="fld"><h3>방식</h3><div class="chips">'+chipBtn('lot-set','g','first','선착순',L.g==='first')+chipBtn('lot-set','g','wheel','뽑기 (전체 중 1명)',L.g==='wheel')+chipBtn('lot-set','g','ladder','사다리타기 (전체)',L.g==='ladder')+'</div>';
  b+='<p class="hint">'+(L.g==='first'?'먼저 받기를 누른 사람부터 가져갑니다.':'방 사람 모두('+others+'명)가 대상이고, 올리자마자 결과가 정해집니다.')+'</p></div>';
  if(L.g!=='wheel'){var ks=L.g==='first'?[1,2,3,5,10]:[1,2,3];b+='<div class="fld"><h3>'+(L.g==='first'?'받을 사람 수':'당첨')+'</h3><div class="chips">';ks.forEach(function(k){b+=chipBtn('lot-set','k',String(k),k+'명',L.k===k);});b+='</div><p class="hint">잉크를 똑같이 나눠 받습니다.</p></div>';}
  b+='<div class="fld"><h3>걸 잉크</h3><div class="chips gfamt">'+GIFT_AMTS.map(function(a){return '<button class="chip" data-act="lot-amt" data-v="'+a+'" aria-pressed="'+(n===a?'true':'false')+'"'+(!ink.unl&&a>ink.bal?' disabled':'')+'>'+inkTag(a)+'</button>';}).join('')+'<input type="number" inputmode="numeric" min="1" data-draft="lotN" data-live="1" placeholder="직접" aria-label="걸 잉크"></div><p class="hint">내 잉크 '+(ink.unl?'무제한':ink.bal+'방울')+(L.g!=='wheel'&&n>0?' · 1명당 '+Math.floor(n/L.k)+'방울':'')+'</p></div>';
  b+='<input type="text" data-draft="lotMsg" maxlength="40" placeholder="한마디 (예: 오늘 공부 수고했어)" aria-label="한마디">';
  var kk=L.g==='wheel'?1:L.k,ok=n>0&&n<=99999&&(ink.unl||n<=ink.bal)&&n>=kk&&others>0;
  return dlg('',{id:'lotnew',t:'잉크 뿌리기'},b,'<div class="df"><button class="btn primary" data-act="lot-add"'+(ok?'':' disabled')+'>'+(n>0&&!ink.unl&&n>ink.bal?'잉크가 모자랍니다':L.g==='first'?'전체 대화방에 올리기':'올리고 결과 보기')+'</button></div>');
}
/* 결과 보기: 돌림판은 돌아가다 멈추고, 사다리는 길을 따라 내려간다 */
function lotWheelSvg(V,who,win){
  var n=who.length,seg=360/n,wid=Object.keys(win)[0],wi=Math.max(0,who.indexOf(wid)),R=120,s='',cols=['var(--accent)','color-mix(in srgb,var(--accent) 45%,var(--surface))'];
  for(var i=0;i<n;i++){
    var a0=(i*seg-90)*Math.PI/180,a1=((i+1)*seg-90)*Math.PI/180,large=seg>180?1:0;
    var x0=R+R*Math.cos(a0),y0=R+R*Math.sin(a0),x1=R+R*Math.cos(a1),y1=R+R*Math.sin(a1);
    s+=n===1?'<circle cx="'+R+'" cy="'+R+'" r="'+R+'" fill="'+cols[0]+'"/>':'<path d="M'+R+','+R+' L'+x0.toFixed(1)+','+y0.toFixed(1)+' A'+R+','+R+' 0 '+large+' 1 '+x1.toFixed(1)+','+y1.toFixed(1)+' Z" fill="'+cols[i%2]+(n%2&&i===n-1?'" style="fill:color-mix(in srgb,var(--accent) 70%,#F2C14E)':'')+'"/>';
    var am=((i+.5)*seg-90)*Math.PI/180,tx=R+R*.62*Math.cos(am),ty=R+R*.62*Math.sin(am);
    s+='<text x="'+tx.toFixed(1)+'" y="'+ty.toFixed(1)+'" transform="rotate('+(function(d){d=d%360;return d>90&&d<270?d+180:d;})((i+.5)*seg)+' '+tx.toFixed(1)+' '+ty.toFixed(1)+')" text-anchor="middle" dominant-baseline="middle">'+esc(cut(V.byId[who[i]]?V.byId[who[i]].name:'?',5))+'</text>';
  }
  var end=360*6-((wi+.5)*seg);
  return '<div class="lwheel"><div class="lptr" aria-hidden="true"></div><svg viewBox="0 0 240 240" class="lwh'+(n>24?' xs':n>12?' sm':'')+'" style="--end:'+end+'deg">'+s+'<circle cx="120" cy="120" r="16" class="lhub"/></svg></div>';
}
function lotLadderSvg(V,G,who){
  var n=who.length,k=Math.max(1,Math.min(+G.k||1,n-1)),L=lotLadder(n,k,+G.seed||1),W=Math.max(260,n*56),gx=W/n,H=60+L.rows*26+40,s='',top=34;
  for(var c=0;c<n;c++){var x=gx*(c+.5);s+='<line class="lv" x1="'+x+'" y1="'+top+'" x2="'+x+'" y2="'+(top+L.rows*26)+'"/><text class="lnm" x="'+x+'" y="20" text-anchor="middle">'+esc(cut(V.byId[who[c]]?V.byId[who[c]].name:'?',5))+'</text>';}
  for(var i=0;i<L.rows;i++)for(var j=0;j<n-1;j++)if(L.rung[i][j]){var y=top+13+i*26;s+='<line class="lr" x1="'+gx*(j+.5)+'" y1="'+y+'" x2="'+gx*(j+1.5)+'" y2="'+y+'"/>';}
  for(c=0;c<n;c++)s+='<text class="lpz'+(L.prize[c]?' on':'')+'" x="'+gx*(c+.5)+'" y="'+(top+L.rows*26+24)+'" text-anchor="middle">'+(L.prize[c]?'당첨':'꽝')+'</text>';
  who.forEach(function(m,c0){
    var x=c0,pts=[[gx*(x+.5),top]];
    for(var i=0;i<L.rows;i++){var y=top+13+i*26;pts.push([gx*(x+.5),y]);if(x<n-1&&L.rung[i][x])x++;else if(x>0&&L.rung[i][x-1])x--;pts.push([gx*(x+.5),y]);}
    pts.push([gx*(x+.5),top+L.rows*26]);
    s+='<polyline class="lp'+(L.prize[x]?' win':'')+'" pathLength="1" style="animation-delay:'+(c0*0.35)+'s" points="'+pts.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1);}).join(' ')+'"/>';
  });
  return '<div class="lladder"><svg viewBox="0 0 '+W+' '+H+'" style="max-width:'+W+'px">'+s+'</svg></div>';
}
function modalLot(V){
  var id=S.modal.id,G=obj(V.gifts[id]);if(G.st!=='done'){S.modal=null;return '';}
  var who=arr(G.who),wn=obj(G.win),b=G.g==='wheel'?lotWheelSvg(V,who,wn):lotLadderSvg(V,G,who);
  b+='<div class="lres">'+Object.keys(wn).map(function(m){return '<span'+(m===V.me?' class="me"':'')+'><b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b> '+wn[m]+'방울</span>';}).join('')+'</div>';
  return dlg('wide',{id:'lot',t:lotName(G.g)+' 결과'},b,'<div class="df"><button class="btn primary" data-act="modal-close">확인</button></div>');
}

function lotFirstBubble(V,x,pick){
  var id=x.lot,G=obj(V.gifts[id]),k=Math.max(1,+G.k||1),each=Math.floor((+G.n||0)/k),cl=lotClaims(V,id,G),full=cl.length>=k,mine=G.from===V.me,got=cl.indexOf(V.me)>=0,back=G.st==='back';
  var h='<div class="bb gift lot"'+pick+'><span class="gfi">'+INK_SVG+'<b>선착순 '+k+'명</b> · 1명당 '+each+'방울</span>';
  if(x.text)h+='<span class="gft">'+esc(x.text)+'</span>';
  h+='<span class="ggres">'+(cl.length?cl.map(function(m){return '<b>'+esc(V.byId[m]?V.byId[m].name:'나간 인원')+'</b>';}).join(', ')+' 받음 ('+cl.length+'/'+k+')':'아직 아무도 안 받았습니다')+'</span>';
  if(back)return h+'<span class="ggres">보낸 사람이 남은 잉크를 거둬들였습니다</span></div>';
  h+='<span class="row">';
  if(!mine&&V.me)h+=got?'<em class="tag a">받았습니다</em>':full?'<em class="tag">마감</em>':'<button class="btn small primary" data-act="lot-claim" data-id="'+esc(id)+'">받기</button>';
  if(mine&&!full)h+='<button class="btn small" data-act="lot-back" data-id="'+esc(id)+'">'+(S.confirm==='lotback:'+id?'한 번 더 누르면 남은 잉크 거두기':'남은 잉크 거두기')+'</button>';
  return h+'</span></div>';
}
