# ---------------------------------------------------------------- v50: 시간대별 공부 기록과 리포트 칸 (JS는 src/v50.js, CSS는 src/v50.css)
V50_JS = open(BASE + '/src/v50.js', encoding='utf-8').read()
V50_CSS = open(BASE + '/src/v50.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V50_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V50_CSS + "</style>")
# 날마다 기록에 hh(시간대별 분)를 남기고 지워지지 않게
sub("  return {mid:mid,date:date,goals:arr(d.goals),mins:obj(d.mins),manual:obj(d.manual),certAt:d.certAt||null,in:d.in||null,focus:d.focus||null};",
    "  var r0={mid:mid,date:date,goals:arr(d.goals),mins:obj(d.mins),manual:obj(d.manual),certAt:d.certAt||null,in:d.in||null,focus:d.focus||null};\n  if(d.hh)r0.hh=obj(d.hh);\n  return r0;")
sub("editDay(today(),function(d){d.mins[L.sid]=Math.min(1200,(+d.mins[L.sid]||0)+mins);});", "editDay(today(),function(d){d.mins[L.sid]=Math.min(1200,(+d.mins[L.sid]||0)+mins);hhAdd(d,L.sid,mins);});")
sub("me.cert+'일</td></tr></tbody></table></div></section></div>';", "me.cert+'일</td></tr></tbody></table></div></section>'+reportTimes(V,Wk,me)+'</div>';")
