# ---------------------------------------------------------------- v38: 지난 날 할 일은 언제든 완료 표시, 인증은 늦은 인증 점수
# 지난 날(그제 이전 포함)도 완료 표시와 인증을 할 수 있다. 마감이 지난 인증은 RULE.certLate, 다 끝냈으면 RULE.allLate.
# 할 일을 더하거나 빼거나 고치는 것은 예전처럼 막는다(guardDay). 앞날(plan)은 완료 표시를 못 한다.
sub("function doneLocked(V,date){return dayLocked(V,date)&&date<addDays(today(),-1);}", "function doneLocked(V,date){return date<CAL_MIN;}")
sub("aria-label=\"'+esc(x.text)+' 완료 표시\"'+(mode!=='full'||doneLocked(V,date)?' disabled':'')", "aria-label=\"'+esc(x.text)+' 완료 표시\"'+(mode==='plan'||doneLocked(V,date)?' disabled':'')")
sub("(mode!=='full'||doneLocked(V,d)?", "(mode==='plan'||doneLocked(V,d)?")
sub("(c.mode==='full'?'<button class=\"ttbchk'", "(c.mode!=='plan'?'<button class=\"ttbchk'")
sub("  if(mode==='full'){\n    var hour=certLabel(V.certHour)", "  if(mode==='full'||(mode==='view'&&date>=START&&day.goals.length)){\n    var hour=certLabel(V.certHour)")
sub("<span class=\"hint\">어제 할 일은 지금도 완료 표시를 할 수 있습니다. ", "<span class=\"hint\">어제 할 일은 지금도 완료 표시를 할 수 있습니다(더 지난 날은 달력에서 그 날을 눌러서). ")
