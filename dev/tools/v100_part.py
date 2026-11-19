# ---------------------------------------------------------------- v100: 순위 > 최종 결과에서 방장만 지금까지의 총점(모든 사람) 보기. 다른 사람은 예전처럼 내 점수만
sub("/* ---------- 공부방 ---------- */", r"""function finAdminNow(V){
  if(adminId(V)!==V.me||finalOpen()||(today()>END&&!finOk(V)))return '';
  var fs=finalStandings(V);
  return '<section class="card fin" id="c-fin-now" style="--k:0"><div class="ct"><h2>지금까지 총점<small>방장만 보입니다</small></h2></div><p class="hint">'+esc(shortDate(TALLY))+'부터 오늘까지 매일 쌓인 점수와 배지 점수를 더한 값입니다. 다른 사람에게는 자기 점수만 보입니다.</p><div class="finpre open">'+(fs.length?fs.map(function(x,i){return '<div class="frr'+(x.p.id===V.me?' me':'')+'"><b>'+(i+1)+'등</b><span>'+esc(x.p.name)+'</span><em>'+fmtN(x.total)+'점</em></div>';}).join(''):'<p class="empty">아직 점수가 없습니다.</p>')+'</div></section>';
}
/* ---------- 공부방 ---------- */""")
sub("    L+=finAdminCard(V);\n", "    L+=finAdminCard(V)+finAdminNow(V);\n")
sub("</style>", ".finpre.open .frr.me{background:color-mix(in srgb,var(--accent) 10%,transparent);border-radius:8px}</style>")
