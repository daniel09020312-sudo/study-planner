/* ---------- 배지(등급과 점수), 주간 우승 점수, 최종 결과, 선물과 벌칙 ---------- */
var TIERS={b:['동',10],s:['은',30],g:['금',60],l:['전설',100]};
var WEEK_BONUS=[100,60,30];
var BADGE_CATS=[['att','출석'],['time','공부 시간'],['plan','할 일과 인증'],['rank','순위'],['board','게시판'],['play','빙고와 대결']];
function fmtN(n){n=Math.round(+n||0);return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function finalOpen(){return today()>END;}
/* 주마다 1, 2, 3등 (같은 점수는 같은 등수) */
function weekResults(V){
  if(V._wr)return V._wr;
  var t=today(),out=[];
  for(var w=START;w<=END&&w<=t;w=addDays(w,7)){
    var e=addDays(w,6);if(e>END)e=END;
    var done=t>e,st=standings(V,w,e),rows=[],place=0,prev=null;
    st.forEach(function(x,i){if(x.total!==prev){place=i+1;prev=x.total;}if(place<=3&&x.total>0&&st.length>1)rows.push({p:x.p,place:place,total:x.total,bonus:done?WEEK_BONUS[place-1]:0});});
    out.push({w:w,e:e,done:done,rows:rows,no:weekNo(w)});
  }
  return V._wr=out;
}
function weekBonusOf(V,mid){var s=0;weekResults(V).forEach(function(r){if(r.done)r.rows.forEach(function(x){if(x.p.id===mid)s+=x.bonus;});});return s;}
function badgePts(V,mid){return badgeList(V,mid).reduce(function(s,b){return s+(b.on?b.pts:0);},0);}
function finalStandings(V){
  if(V._fs)return V._fs;
  return V._fs=standings(V,START,END).map(function(x){var wb=weekBonusOf(V,x.p.id),bp=badgePts(V,x.p.id);return {p:x.p,base:x.total,wb:wb,bp:bp,total:x.total+wb+bp,mins:x.mins};})
    .sort(function(a,b){return b.total-a.total||b.base-a.base||b.mins-a.mins||a.p.name.localeCompare(b.p.name);});
}
function finBreak(x){return '<div class="finbk"><span>누적 '+fmtN(x.base)+'</span><span>주간 순위 +'+fmtN(x.wb)+'</span><span>배지 +'+fmtN(x.bp)+'</span><b>'+fmtN(x.total)+'<small>점</small></b></div>';}
/* 선물과 벌칙 */
function penItems(V){
  return arr(V.cfg.penalties).map(function(x,i){var o=typeof x==='object'&&x?x:{t:x};return {t:String(o.t||'').trim(),by:o.by?String(o.by):'',i:i};}).filter(function(x){return x.t;});
}
function prizeOf(V){var p=V.cfg.prize;return p&&typeof p==='object'?{t:String(p.t||''),by:String(p.by||'')}:{t:String(p||''),by:''};}
function penLoser(V){var fs=finalStandings(V);return fs.length>1&&fs[0].total>0?fs[fs.length-1]:null;}
function prizeCard(V,k){
  var rev=finalOpen(),pz=prizeOf(V),items=penItems(V),mine=items.filter(function(x){return x.by===V.me;}).length,adm=V.me&&adminId(V)===V.me;
  var h='<section class="card" id="c-prize" style="--k:'+k+'"><div class="ct"><h2>선물과 벌칙<small>시험이 끝나면 정해집니다</small></h2></div>';
  h+='<div class="prz"><small>최종 1등 선물</small><b>'+(pz.t?esc(pz.t):'아직 정하지 않았습니다')+'</b>'+(pz.by&&V.byId[pz.by]?'<span class="hint">'+esc(V.byId[pz.by].name)+' 님이 적음</span>':'')+'</div>';
  if(!rev&&V.me)h+='<div class="row" style="margin-top:8px"><input type="text" data-draft="prizeText" data-enter="prize-save" maxlength="40" placeholder="예: 꼴찌가 사는 기프티콘" aria-label="1등 선물"><button class="btn small" data-act="prize-save">'+(pz.t?'바꾸기':'정하기')+'</button></div>';
  h+='<div class="sec"><h3>벌칙 후보<small>한 사람당 2개까지</small></h3>';
  if(!items.length)h+='<p class="empty">아직 벌칙 후보가 없습니다. 모두 하나씩 적어 두면 결과 발표 때 꼴찌가 룰렛을 돌려 하나를 뽑습니다.</p>';
  items.forEach(function(x){
    var who=x.by&&V.byId[x.by]?V.byId[x.by].name:'',can=!rev&&V.me&&(x.by===V.me||adm||!x.by);
    h+='<div class="pl" id="pn-'+x.i+'"><span>'+esc(x.t)+(who?'<small class="pby">'+esc(who)+'</small>':'')+'</span>'+(can?'<button class="del" data-act="pen2-del" data-i="'+x.i+'">'+(S.confirm==='pen2:'+x.i?'한 번 더 누르면 삭제':'삭제')+'</button>':'')+'</div>';
  });
  if(!rev&&V.me){
    if(mine<2&&items.length<12)h+='<div class="row" style="margin-top:8px"><input type="text" data-draft="penText" data-enter="pen2-add" maxlength="40" placeholder="예: 매점 간식 사기" aria-label="추가할 벌칙"><button class="btn" data-act="pen2-add">추가</button></div>';
    else h+='<p class="hint" style="margin-top:8px">'+(mine>=2?'벌칙 후보는 한 사람당 2개까지 적을 수 있습니다.':'벌칙 후보가 12개로 가득 찼습니다.')+'</p>';
  }else if(rev)h+='<p class="hint" style="margin-top:8px">결과가 나와서 더 고칠 수 없습니다.</p>';
  return h+'</div></section>';
}
function loserLine(V){
  var lo=penLoser(V);if(!lo)return '';
  var sp=obj(V.spins.final),items=penItems(V);
  var h='<div class="finpen"><div><small>최종 꼴찌 벌칙</small><b>'+esc(lo.p.name)+'</b></div>';
  if(sp.text)h+='<p>뽑힌 벌칙: <b>'+esc(sp.text)+'</b></p>';
  else if(lo.p.id===V.me)h+='<button class="btn primary" data-act="roul-open" data-key="final"'+(items.length<2?' disabled':'')+'>벌칙 룰렛 돌리기</button>'+(items.length<2?'<span class="hint">벌칙 후보가 2개 이상 있어야 돌릴 수 있습니다.</span>':'');
  else h+='<p class="hint">'+esc(lo.p.name)+' 님이 룰렛을 돌리면 여기 결과가 나옵니다.</p>';
  return h+'</div>';
}
function finalBody(V){
  var t=today(),rev=finalOpen(),fs=finalStandings(V),me=fs.filter(function(x){return x.p.id===V.me;})[0],wr=weekResults(V),L='',pz=prizeOf(V);
  if(!rev){
    var open=addDays(END,1);
    L+='<section class="card fin" id="c-fin-wait" style="--k:0"><div class="ct"><h2>최종 결과<small>'+esc(longDate(open))+' 공개</small></h2></div>';
    L+='<div class="fincd"><b>D-'+Math.max(0,diffDays(t,open))+'</b><span>2차 시험이 끝난 다음 날 모두에게 공개됩니다. 그 전까지는 내 점수만 보입니다.</span></div>';
    if(me)L+='<div class="finme"><small>지금까지 내 최종 점수</small>'+finBreak(me)+'</div>';
    L+='<p class="hint" style="margin-top:10px">최종 점수는 매일 쌓인 점수에 주간 순위 점수와 배지 점수를 더한 값입니다.</p></section>';
  }else{
    L+='<section class="card fin" id="c-fin" style="--k:0"><div class="ct"><h2>최종 결과<small>'+esc(shortDate(START)+' ~ '+shortDate(END))+'</small></h2></div>';
    if(!fs.some(function(x){return x.total>0;}))return L+'<p class="empty">기간 동안 쌓인 점수가 없습니다.</p></section></div><div class="stack">'+prizeCard(V,2);
    L+='<div class="podium">';
    [1,0,2].forEach(function(i){var x=fs[i];if(!x)return;L+='<div class="pd p'+(i+1)+'">'+av(x.p)+'<b>'+esc(x.p.name)+'</b><small>'+fmtN(x.total)+'점</small><span class="pdn">'+(i+1)+'</span>'+(i===0&&pz.t?'<em class="tag a">선물: '+esc(pz.t)+'</em>':'')+'</div>';});
    L+='</div>';
    fs.forEach(function(x,i){var last=i===fs.length-1&&fs.length>1;L+='<div class="rk fr2'+(x.p.me?' me':'')+'" id="fn-'+esc(x.p.id)+'"><div class="n">'+(i+1)+'</div>'+av(x.p)+'<div><div class="line"><b>'+esc(x.p.name)+'</b>'+titleTag(V,x.p.id)+(i===0?'<span class="tag a">1등</span>':'')+(last?'<span class="tag r">벌칙</span>':'')+'</div>'+finBreak(x)+'</div></div>';});
    L+=loserLine(V)+'</section>';
  }
  L+='<section class="card" id="c-weeks" style="--k:1"><div class="ct"><h2>주간 우승 기록<small>1등 '+WEEK_BONUS[0]+'점, 2등 '+WEEK_BONUS[1]+'점, 3등 '+WEEK_BONUS[2]+'점</small></h2></div>';
  if(!wr.length)L+='<p class="empty">아직 끝난 주가 없습니다.</p>';
  wr.slice().reverse().forEach(function(r){
    L+='<div class="wkres"><div class="wkn"><b>'+r.no+'주차</b><small>'+esc(shortDate(r.w)+' ~ '+shortDate(r.e))+'</small></div><div class="wkw">';
    if(!r.done)L+='<span class="hint">진행 중'+(r.rows[0]?', 지금 1등 '+esc(r.rows[0].p.name):'')+'</span>';
    else if(!r.rows.length)L+='<span class="hint">점수가 없었습니다</span>';
    else r.rows.forEach(function(x){L+='<span class="ww p'+x.place+'">'+x.place+'등 <b>'+esc(x.p.name)+'</b> +'+x.bonus+'</span>';});
    L+='</div></div>';
  });
  L+='</section>';
  return L+'</div><div class="stack">'+prizeCard(V,2);
}
/* 배지 화면 */
function badgeView(V){
  var bl=badgeList(V,V.me),mt=obj(V.progress[V.me]).title,got=bl.filter(function(b){return b.on;}),pts=got.reduce(function(s,b){return s+b.pts;},0),own={};
  V.roster.forEach(function(m){badgeList(V,m.id).forEach(function(b){if(b.on)own[b.id]=(own[b.id]||0)+1;});});
  var h='<section class="card" id="c-badges" style="--k:0"><div class="ct"><h2>배지와 칭호<small>'+got.length+' / '+bl.length+'</small></h2><span class="tag a">배지 점수 '+pts+'점</span></div>';
  h+='<p class="hint">등급마다 동 '+TIERS.b[1]+'점, 은 '+TIERS.s[1]+'점, 금 '+TIERS.g[1]+'점, 전설 '+TIERS.l[1]+'점이 최종 점수에 더해집니다. 받은 배지를 누르면 그 칭호가 이름 옆에 붙습니다.</p>';
  BADGE_CATS.forEach(function(c){
    var list=bl.filter(function(b){return b.cat===c[0];});if(!list.length)return;
    h+='<h3 class="bcat">'+c[1]+'<small>'+list.filter(function(b){return b.on;}).length+' / '+list.length+'</small></h3><div class="bdgs">';
    list.forEach(function(b){
      var n=own[b.id]||0,pct=Math.min(100,Math.round(Math.min(b.v,b.max)/b.max*100));
      if(b.on)h+='<button class="bdg on t-'+b.tier+'" data-act="badge-title" data-id="'+b.id+'" aria-pressed="'+(mt===b.id?'true':'false')+'"><span class="tier">'+b.tname+'</span><b>'+esc(b.name)+'</b><small>칭호: '+esc(b.title)+'</small><small class="own">+'+b.pts+'점'+(n>1?', '+n+'명 보유':', 나만 보유')+'</small></button>';
      else h+='<div class="bdg t-'+b.tier+'"><span class="tier">'+b.tname+'</span><b>'+esc(b.name)+'</b>'+(b.desc!==b.name?'<small>'+esc(b.desc)+'</small>':'')+'<div class="bpb" aria-hidden="true"><i style="width:'+pct+'%"></i></div><small>'+prog(b,b.v)+(n?', '+n+'명 보유':'')+'</small></div>';
    });
    h+='</div>';
  });
  h+='<div class="sec"><h3>참여 인원 배지</h3>';
  V.roster.map(function(m){var l=badgeList(V,m.id).filter(function(b){return b.on;});return {m:m,n:l.length,p:l.reduce(function(s,b){return s+b.pts;},0)};}).sort(function(a,b){return b.p-a.p;}).forEach(function(x){
    h+='<div class="brow">'+av(V.byId[x.m.id],'s')+'<span>'+esc(V.byId[x.m.id].name)+' '+titleTag(V,x.m.id)+'</span><span></span><small>'+x.n+'개, '+x.p+'점</small></div>';
  });
  return h+'</div></section>';
}
