/* ---------- v102: 노동요 들은 횟수는 실제로 들었을 때만(앱 안 플레이어 1분, 링크는 1분 넘게 다녀왔을 때, 같은 곡은 30분에 한 번),
   반 전체 목표 단계별 잉크(CG_TIERS), 상점 새 종류(프로필 테두리 r:, 칭호 장식 g:)와 히든 상품 ---------- */
var SP_MIN=+window.__SP_MIN||60000,SP_GAP=1800000,SL={id:null,at:0,ext:false,t:0};
function songCount(id){
  var V=view();if(!V.me||!canWrite()||!V.songs[id])return;
  var last=+obj(obj(V.progress[V.me]).spt)[id]||0;if(Date.now()-last<SP_GAP)return;
  editProg(function(p){p.sp=obj(p.sp);p.sp[id]=(+p.sp[id]||0)+1;var st=p.spt=obj(p.spt),now=Date.now();Object.keys(st).forEach(function(k){if(now-(+st[k]||0)>86400000)delete st[k];});st[id]=now;});
}
function songListen(id,ext){
  if(!canWrite()||!view().me)return;
  editProg(function(p){p.now={id:id,at:Date.now()};});
  clearTimeout(SL.t);SL.id=id;SL.at=Date.now();SL.ext=!!ext;
  if(!ext)SL.t=setTimeout(function(){if(S.songPlay===id&&SL.id===id)songCount(id);},SP_MIN);
}
document.addEventListener('visibilitychange',function(){
  if(document.visibilityState!=='visible'||!SL.ext||!SL.id)return;
  var id=SL.id,dt=Date.now()-SL.at;SL.ext=false;
  if(dt>=SP_MIN){try{songCount(id);render();}catch(e){}}
});

/* 반 전체 목표: 목표의 몇 %까지 갔는지에 따라 모두에게 주는 잉크가 늘어남(CG_TIER_FROM 주부터, 그 전 주는 달성하면 CG_INK) */
var CG_TIER_FROM='2026-11-16',CG_TIERS=[[0.5,5],[1,20],[1.25,30],[1.5,45],[2,70],[2.5,100],[3,140]];
function cgTierOf(W){var r=W.goal>0?W.mins/(W.goal*60):0,t=null;CG_TIERS.forEach(function(x,i){if(r>=x[0])t={i:i,f:x[0],ink:x[1]};});return t;}
function cgReward(W){if(W.mon<CG_TIER_FROM)return W.hit?CG_INK:0;var t=cgTierOf(W);return t?t.ink:0;}
function cgInk(V){
  var t=today(),n=0;
  for(var w=CG_FROM;addDays(w,6)<t;w=addDays(w,7))n+=cgReward(cgWeek(V,w));
  return n;
}
function cgCard(V,k){
  if(!V.me)return '';
  var t=today(),mon=mondayOf(t),W=cgWeek(V,mon),dl=diffDays(t,addDays(mon,6))+1,tier=cgTierOf(W),nx=CG_TIERS[tier?tier.i+1:0];
  var me=0;W.by.forEach(function(x){if(x.p.id===V.me)me=x.m;});
  var prev=cgWeek(V,addDays(mon,-7)),adm=adminId(V)===V.me,gm=W.goal*60,top=Math.max(2,Math.ceil(Math.max(W.mins/gm,1)*2)/2+0.5),pct=Math.round(W.mins/gm*100);
  top=Math.min(top,CG_TIERS[CG_TIERS.length-1][0]+0.25);
  var h='<section class="card cg cg2'+(W.hit?' hit':'')+'" id="c-cg" style="--k:'+k+'"><div class="ct"><h2>반 전체 목표<small>이번 주</small></h2><span class="tag'+(W.hit?' a':'')+'">'+(tier?'지금 +'+tier.ink+'방울':'D-'+(dl-1))+'</span></div>';
  h+='<div class="cgnum"><b>'+Math.floor(W.mins/60)+'</b><span>/ '+W.goal+'시간</span><em>'+pct+'%</em></div>';
  h+='<div class="cgbar2" aria-hidden="true"><i style="width:'+Math.min(100,W.mins/gm/top*100)+'%"></i>'+CG_TIERS.filter(function(x){return x[0]<=top;}).map(function(x){var on=W.mins>=x[0]*gm;return '<b class="'+(on?'on':'')+(x[0]===1?' g':'')+'" style="left:'+(x[0]/top*100)+'%"><span>+'+x[1]+'</span></b>';}).join('')+'</div>';
  h+='<p class="cgsub">'+(tier?'모두 잉크 <b>'+tier.ink+'방울</b>을 받습니다':'아직 보상 단계 전입니다')+(nx?' · '+fmtMins(Math.max(0,Math.ceil(nx[0]*gm-W.mins)))+' 더 하면 <b>'+nx[1]+'방울</b>':' · 최고 단계입니다')+'</p>';
  h+='<p class="hint cgtier">목표의 '+CG_TIERS.map(function(x){return Math.round(x[0]*100)+'% '+x[1];}).join(' · ')+'방울. 주가 끝나면 모두에게 들어갑니다.</p>';
  if(W.by.length){h+='<div class="cgtop">';W.by.slice(0,3).forEach(function(x,i){h+='<span>'+(i+1)+'. '+esc(x.p.name)+' <b>'+fmtMins(x.m)+'</b></span>';});h+='</div>';}
  var pr=cgReward(prev);
  h+='<p class="hint">내 몫 '+fmtMins(me)+(W.mins?' ('+Math.round(me/W.mins*100)+'%)':'')+(prev.mon>=CG_FROM?' · 지난주 '+(pr?'달성, 잉크 '+pr+'방울':'미달성')+' ('+Math.floor(prev.mins/60)+'/'+prev.goal+'시간)':'')+'</p>';
  if(adm){
    var open=!!S.cgEdit;
    h+='<div class="cgadm"><button class="linkbtn" data-act="cg-edit" aria-expanded="'+(open?'true':'false')+'">목표 바꾸기</button>';
    if(open){
      h+='<div class="chips" style="margin-top:6px">';[100,200,300,400,500].forEach(function(n){h+=chipBtn('cg-set','h',String(n),n+'시간',W.goal===n);});h+='</div>';
      h+='<div class="row" style="margin-top:6px"><input type="number" inputmode="numeric" min="10" max="5000" data-draft="cgH" placeholder="직접 입력 (시간)" aria-label="목표 시간 직접 입력"><button class="btn small primary" data-act="cg-save">저장</button></div><p class="hint">이번 주부터 적용됩니다.</p>';
    }
    h+='</div>';
  }
  return h+'</section>';
}
function cgTick(V){
  if(!V||!V.me||!S.ready)return;
  var mon=mondayOf(today()),W=cgWeek(V,mon),tr=cgTierOf(W);if(!tr||W.mins<=0)return;
  var key=mon+'|'+tr.i;if(lsGet('gbb_cgw')===key||lsGet('gbb_cgw')===mon&&tr.f<=1)return;
  lsSet('gbb_cgw',key);flash('반 전체 목표 '+Math.round(tr.f*100)+'% 달성. 이번 주가 끝나면 모두 잉크 '+tr.ink+'방울을 받습니다.');
}

/* 상점: 프로필 테두리(r:), 칭호 장식(g:). 고른 것은 progress.<나>.deco={r,g}에 적어 모두에게 보임 */
var DECO_RING=[['none','테두리 없음',0,'처음 모양'],['dash','점선',30,'가볍게 두른 점선'],['mint','민트',50,'시원한 민트 고리'],['rose','장밋빛',50,'부드러운 장밋빛 고리'],['double','두 겹',60,'얇은 고리 두 줄'],['gold','금빛',80,'반짝이는 금빛 고리'],['neon','네온',100,'빛나며 천천히 도는 네온'],['sakura','벚꽃',100,'분홍 꽃잎 그러데이션'],['rainbow','무지개',120,'일곱 색이 도는 고리']];
var DECO_TAG=[['none','기본 칭호',0,'처음 모양'],['outline','테두리',30,'선만 두른 칭호'],['ink','먹물',40,'검은 바탕 흰 글씨'],['glow','은은한 빛',50,'칭호 주위로 퍼지는 빛'],['grad','그러데이션',60,'대표 색 그러데이션'],['shine','반짝',80,'빛이 스쳐 지나가는 칭호']];
/* 히든: 조건을 채워야 보이고 살 수 있음 */
var DECO_HID=[
  ['r','dawn','새벽빛',60,'아침 7시 전 출석 10번',function(s){return s.early>=10;}],
  ['r','crown','왕관',90,'주간 1등 한 번',function(s){return s.weekWins>=1;}],
  ['r','blaze','불꽃',120,'하루 12시간 넘게 공부',function(s){return s.d12>=1;}],
  ['r','galaxy','은하',150,'누적 공부 100시간',function(s){return s.mins>=6000;}],
  ['r','seven','럭키 세븐',77,'숨은 업적 럭키 세븐',function(s,V){return !!obj(V.progress[V.me]).egg7;}],
  ['r','void','인간 아님',180,'히든 칭호 인간 아님',function(s){return s.d18>=1;}],
  ['r','prism','프리즘',200,'보이는 테두리를 모두 사기',function(s,V){return DECO_RING.every(function(x){return x[2]===0||shopOwns(V,'r:'+x[0]);});}],
  ['g','gold','황금 칭호',80,'배지 10개 모으기',function(s,V){return badgeList(V,V.me).filter(function(b){return b.on;}).length>=10;}],
  ['g','fire','불타는 칭호',100,'1:1 대결 5승',function(s){return s.duelWins>=5;}],
  ['g','holo','홀로그램',150,'보이는 칭호 장식을 모두 사기',function(s,V){return DECO_TAG.every(function(x){return x[2]===0||shopOwns(V,'g:'+x[0]);});}]
];
var DECO_ITEMS=(function(){var a=[];
  DECO_RING.forEach(function(x){a.push({id:'r:'+x[0],v:x[0],cat:'ring',name:x[1],price:x[2],desc:x[3],free:x[2]===0});});
  DECO_TAG.forEach(function(x){a.push({id:'g:'+x[0],v:x[0],cat:'ttag',name:x[1],price:x[2],desc:x[3],free:x[2]===0});});
  DECO_HID.forEach(function(x){a.push({id:x[0]+':'+x[1],v:x[1],cat:x[0]==='r'?'ring':'ttag',name:x[2],price:x[3],desc:x[0]==='r'?'히든 테두리':'히든 칭호 장식',hid:x[4],cond:x[5]});});
  return a;})();
function decoOk(V,it){if(!it||!it.hid)return true;if(!V||!V.me)return false;try{return !!it.cond(memberStats(V,V.me),V);}catch(e){return false;}}
function shopShown(V,id){var it=shopItem(id);if(it&&it.hid)return shopOwns(V,id)||decoOk(V,it);return shopShown0(V,id);}
function decoOf(mid){var V=V0;if(!V||!mid)return {};return obj(obj(V.progress[mid]).deco);}
function decoRingCls(mid){var r=decoOf(mid).r;return r&&r!=='none'&&/^[a-z]+$/.test(r)?' rg rg-'+r:'';}
function decoTagCls(mid){var g=decoOf(mid).g;return g&&g!=='none'&&/^[a-z]+$/.test(g)?' tg2 tg-'+g:'';}
function decoPrev(it){
  if(it.cat==='ring')return '<span class="shpv shring" aria-hidden="true"><span class="av'+(it.v==='none'?'':' rg rg-'+it.v)+'">나</span></span>';
  return '<span class="shpv shttag" aria-hidden="true"><em class="tag tt-g'+(it.v==='none'?'':' tg2 tg-'+it.v)+'">공부 기계</em></span>';
}
function decoHidCard(V,it,foc){
  return '<div class="shi hid hid2'+(foc?' foc':'')+'" id="shi-'+esc(it.id.replace(':','-'))+'"><span class="shpv shq2" aria-hidden="true"><i>?</i></span><div class="shn"><b>히든 '+(it.cat==='ring'?'테두리':'칭호 장식')+'</b><small>열리는 조건: '+esc(it.hid)+'</small></div><div class="sha"><span class="shst"><svg class="lki" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg>잠김</span></div></div>';
}
function decoHidCount(V,cat){var l=DECO_ITEMS.filter(function(x){return x.hid&&x.cat===cat;});return [l.filter(function(x){return shopShown(V,x.id);}).length,l.length];}
