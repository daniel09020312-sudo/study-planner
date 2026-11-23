# ---------------------------------------------------------------- v108: 순위 > 최종 결과에 '전체 순위(이름 없이)' 카드. 공개 전까지 모두에게 순위·점수·공부 시간만 보이고, 내 줄만 '나'로 표시
sub("/* ---------- 공부방 ---------- */", r"""function finAnonCard(V){
  if(finalOpen()||!V.me)return '';
  var fs=finalStandings(V),n=fs.length;if(!n)return '';
  var h='<section class="card fin fanon" id="c-fin-anon" style="--k:1"><div class="ct"><h2>전체 순위<small>이름은 가려집니다</small></h2><span class="tag">'+n+'명</span></div><p class="hint">'+esc(shortDate(TALLY))+'부터 오늘까지의 최종 점수(배지 점수 포함)와 공부 시간입니다. 내 줄만 표시됩니다.</p>';
  h+='<div class="fanh"><span>순위</span><span></span><span>점수</span><span>공부 시간</span></div><div class="fanl">';
  var rk=0,prev=null;
  fs.forEach(function(x,i){if(prev===null||x.total!==prev)rk=i+1;prev=x.total;var me=x.p.id===V.me;h+='<div class="fanr'+(me?' me':'')+'"'+(me?' id="fan-me"':'')+'><b>'+rk+'</b><span>'+(me?'<em class="tag a">나</em>':'<i aria-hidden="true"></i>')+'</span><strong>'+fmtN(x.total)+'<small>점</small></strong><span class="fant">'+fmtMins(x.mins)+'</span></div>';});
  return h+'</div></section>';
}
/* ---------- 공부방 ---------- */""")
sub("  L+='<section class=\"card\" id=\"c-weeks\"", "  L+=finAnonCard(V);\n  L+='<section class=\"card\" id=\"c-weeks\"")
sub("</style>", """.fanh,.fanr{display:grid;grid-template-columns:44px minmax(0,1fr) auto 96px;gap:10px;align-items:center;padding:7px 10px;font-variant-numeric:tabular-nums}
.fanh{font-size:11.5px;color:var(--ink-3);border-bottom:1px solid var(--line)}
.fanh span:nth-child(3),.fanh span:nth-child(4),.fanr strong,.fanr .fant{text-align:right}
.fanl{max-height:420px;overflow:auto}
.fanr{border-radius:10px;font-size:14px}
.fanr b{font-size:13px;color:var(--ink-2)}
.fanr i{display:block;height:8px;width:62%;border-radius:4px;background:repeating-linear-gradient(90deg,var(--fill) 0 10px,transparent 10px 14px)}
.fanr strong{font-weight:700}
.fanr strong small{font-size:11px;font-weight:500;color:var(--ink-3);margin-left:2px}
.fanr .fant{color:var(--ink-2);font-size:13px}
.fanr.me{background:color-mix(in srgb,var(--accent) 12%,transparent)}
.fanr:nth-child(-n+3) b{color:var(--accent-ink)}
</style>""")
