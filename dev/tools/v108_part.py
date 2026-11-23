# ---------------------------------------------------------------- v108: 순위 > 최종 결과에 '전체 순위(이름 없이)' 카드. 관리자 코드를 넣은 기기에서만, 공개 전까지 순위·점수·공부 시간만(내 줄 표시도 없음)
sub("/* ---------- 공부방 ---------- */", r"""function finAnonCard(V){
  if(finalOpen()||!V.me||!admCodeOn())return '';
  var fs=finalStandings(V),n=fs.length;if(!n)return '';
  var h='<section class="card fin fanon" id="c-fin-anon" style="--k:1"><div class="ct"><h2>전체 순위<small>관리자만 보입니다 · 이름은 가려집니다</small></h2><span class="tag">'+n+'명</span></div><p class="hint">'+esc(shortDate(TALLY))+'부터 오늘까지의 최종 점수(배지 점수 포함)와 공부 시간입니다. 참여한 사람 모두를 한 화면에 보여 줍니다.</p>';
  h+='<div class="fanl">';
  var rk=0,prev=null;
  fs.forEach(function(x,i){if(prev===null||x.total!==prev)rk=i+1;prev=x.total;h+='<div class="fanr"><b>'+rk+'</b><strong>'+fmtN(x.total)+'<small>점</small></strong><span class="fant">'+fmtMins(x.mins)+'</span></div>';});
  return h+'</div></section>';
}
/* ---------- 공부방 ---------- */""")
sub("  L+='<section class=\"card\" id=\"c-weeks\"", "  L+=finAnonCard(V);\n  L+='<section class=\"card\" id=\"c-weeks\"")
sub("</style>", """.fanl{columns:200px auto;column-gap:14px;margin-top:6px}
.fanr{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:8px;align-items:baseline;padding:4px 8px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums;break-inside:avoid;font-size:13.5px}
.fanr b{font-size:12.5px;color:var(--ink-2)}
.fanr strong{font-weight:700}
.fanr strong small{font-size:10.5px;font-weight:500;color:var(--ink-3);margin-left:2px}
.fanr .fant{color:var(--ink-2);font-size:12.5px;text-align:right}
.fanr:nth-child(-n+3) b{color:var(--accent-ink)}
</style>""")
