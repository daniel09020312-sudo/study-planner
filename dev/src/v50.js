/* ---------- v50: 시간대별 공부 기록(day.hh = {h<시>:{<과목>:분}})과 리포트의 과목 x 요일, 시간대별 칸 ---------- */
var HR_AXIS=[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4];
function hhAdd(d,sid,mins){
  var now=Date.now(),h=obj(d.hh);d.hh=h;mins=Math.min(Math.round(mins)||0,600);
  for(var i=mins;i>=1;i--){var k='h'+new Date(now-(i-0.5)*60000).getHours(),o=h[k]=obj(h[k]);o[sid]=(+o[sid]||0)+1;}
}
function hhSub(d,sid,n){
  var h=obj(d.hh);if(!d.hh)return;
  for(var a=HR_AXIS.length-1;a>=0&&n>0;a--){
    var k='h'+HR_AXIS[a],o=obj(h[k]),v=+o[sid]||0;if(!v)continue;
    var x=Math.min(v,n);n-=x;if(v-x>0)o[sid]=v-x;else delete o[sid];
    if(Object.keys(o).length)h[k]=o;else delete h[k];
  }
  if(!Object.keys(h).length)delete d.hh;else d.hh=h;
}
function hrLabel(h){return (h<12?'오전 ':'오후 ')+(h%12||12)+'시';}
function fmtHM(m){return m?Math.floor(m/60)+':'+(m%60<10?'0':'')+(m%60):'';}
var HR_BANDS=[['새벽',[0,1,2,3,4]],['오전',[5,6,7,8,9,10,11]],['오후',[12,13,14,15,16,17]],['저녁과 밤',[18,19,20,21,22,23]]];
function reportTimes(V,Wk,me){
  var days=Wk.days,grid={},hrs={},tracked=0,k,i;
  days.forEach(function(d,di){
    var x=dayOf(V,V.me,d);
    Object.keys(x.mins).concat(Object.keys(x.manual)).forEach(function(s){var m=(+x.mins[s]||0)+(+x.manual[s]||0);if(!m)return;var g=grid[s]=grid[s]||[0,0,0,0,0,0,0];g[di]=m;});
    var hh=obj(x.hh);
    Object.keys(hh).forEach(function(hk){var hr=+hk.slice(1),o=obj(hh[hk]);Object.keys(o).forEach(function(s){var v=+o[s]||0;if(!v)return;var r=hrs[hr]=hrs[hr]||{};r[s]=(r[s]||0)+v;tracked+=v;});});
  });
  var rows=Object.keys(grid).map(function(s){var t=grid[s].reduce(function(a,b){return a+b;},0);return {s:s,t:t,g:grid[s]};}).sort(function(a,b){return b.t-a.t;});
  var h='<section class="card" id="c-rgrid-'+S.repWeek+'" style="--k:3"><div class="ct"><h2>과목별 요일 공부</h2><small>시:분</small></div>';
  if(!rows.length)h+='<p class="empty">이 주에 기록된 공부 시간이 없습니다.</p>';
  else{
    var mx=0;rows.forEach(function(r){r.g.forEach(function(m){if(m>mx)mx=m;});});
    h+='<div class="wtwrap"><table class="tb rgrid"><thead><tr><th>과목</th>'+days.map(function(d){return '<th>'+DOW[pd(d).getDay()]+'</th>';}).join('')+'<th>합계</th></tr></thead><tbody>';
    rows.forEach(function(r){
      var col=r.s==='etc'?SGRAY:subCol(V,r.s);
      h+='<tr><td><span class="rgd" style="background:'+col+'"></span>'+esc(subLabel(V,r.s))+'</td>'+r.g.map(function(m){return '<td class="rgc"'+(m?' style="--a:'+(0.15+0.7*m/mx).toFixed(2)+';--c:'+col+'"':'')+'>'+fmtHM(m)+'</td>';}).join('')+'<td><b>'+fmtMins(r.t)+'</b></td></tr>';
    });
    var dt=days.map(function(d,di){return rows.reduce(function(a,r){return a+r.g[di];},0);});
    h+='<tr class="sum"><td>하루 합계</td>'+dt.map(function(m){return '<td>'+fmtHM(m)+'</td>';}).join('')+'<td>'+fmtMins(dt.reduce(function(a,b){return a+b;},0))+'</td></tr></tbody></table></div>';
  }
  h+='</section>';
  h+='<section class="card" id="c-rhour-'+S.repWeek+'" style="--k:4"><div class="ct"><h2>시간대별 공부</h2><small>타이머로 공부한 시간</small></div>';
  if(!tracked)h+='<p class="empty">아직 시간대 기록이 없습니다. 타이머로 공부하면 몇 시에 무슨 과목을 했는지 여기에 쌓입니다. (이 기능을 올리기 전의 기록은 시간대를 알 수 없습니다.)</p>';
  else{
    var tot={},best=-1,bh=0;
    HR_AXIS.forEach(function(hr){var o=hrs[hr]||{},t=0;Object.keys(o).forEach(function(s){t+=o[s];});tot[hr]=t;if(t>best){best=t;bh=hr;}});
    h+='<div class="hrchart" role="img" aria-label="시간대별 공부 시간 막대 그래프">';
    HR_AXIS.forEach(function(hr,ix){
      var o=hrs[hr]||{},t=tot[hr],bar='';
      Object.keys(o).sort(function(a,b){return o[b]-o[a];}).forEach(function(s){bar+='<i style="height:'+Math.max(2,Math.round(o[s]/best*96))+'px;background:'+(s==='etc'?SGRAY:subCol(V,s))+'" title="'+esc(subLabel(V,s))+' '+o[s]+'분"></i>';});
      h+='<div class="hc'+(hr===bh?' pk':'')+'"><div class="hcs">'+bar+'</div><small>'+(ix%3===0?hr:'')+'</small></div>';
    });
    h+='</div>';
    h+='<p class="hint" style="margin:6px 0 10px">가장 오래 공부한 시간은 <b>'+hrLabel(bh)+'~'+hrLabel((bh+1)%24)+'</b> ('+fmtMins(best)+')입니다.</p>';
    h+='<div class="hbands">';
    HR_BANDS.forEach(function(b){var t=0;b[1].forEach(function(hr){t+=tot[hr]||0;});h+='<div><small>'+b[0]+'</small><b>'+fmtMins(t)+'</b><span>'+Math.round(t/tracked*100)+'%</span></div>';});
    h+='</div>';
    var top=[];
    Object.keys(grid).forEach(function(s){
      var bt=HR_BANDS.map(function(b){var t=0;b[1].forEach(function(hr){t+=obj(hrs[hr])[s]||0;});return t;}),bi=0;
      bt.forEach(function(t,j){if(t>bt[bi])bi=j;});
      var sum=bt.reduce(function(a,b){return a+b;},0);if(sum)top.push({s:s,band:HR_BANDS[bi][0],sum:sum});
    });
    top.sort(function(a,b){return b.sum-a.sum;});
    if(top.length){h+='<ul class="rdelta rband">';top.forEach(function(x){h+='<li style="--sc:'+(x.s==='etc'?SGRAY:subCol(V,x.s))+'"><i></i><span>'+esc(subLabel(V,x.s))+'</span><b>'+esc(x.band)+'</b><em>'+fmtMins(x.sum)+'</em></li>';});h+='</ul>';}
    var pct=me.mins?Math.round(tracked/me.mins*100):0;
    if(pct<90)h+='<p class="hint">시간대가 기록된 시간은 이 주 공부 시간의 '+Math.min(100,pct)+'%입니다. 직접 입력한 시간과 예전 기록은 시간대를 알 수 없어 빠집니다.</p>';
  }
  return h+'</section>';
}
