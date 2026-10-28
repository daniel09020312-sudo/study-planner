# ---------------------------------------------------------------- v49: 점수는 처음부터 보이고, 집계(주간 우승, 배지, 최종 결과)는 집계 시작일(TALLY, 기본 11/2)부터
sub("bonus:done?WEEK_BONUS[place-1]:0", "bonus:done&&w>=TALLY?WEEK_BONUS[place-1]:0")
sub("standings(V,START,END)", "standings(V,TALLY,END)")
sub("else if(S.range==='all'){from=START;to=END;label='최종';}", "else if(S.range==='all'){from=TALLY;to=END;label='최종';}")
sub("for(var d=START;d<=last;d=addDays(d,1)){\n    var x=dayOf(V,mid,d)", "var cs0=0;for(var d=TALLY;d<=last;d=addDays(d,1)){\n    var x=dayOf(V,mid,d)")
sub("for(var w=START;w<=last;w=addDays(w,7)){\n    s.lines", "for(var w=TALLY;w<=last;w=addDays(w,7)){\n    s.lines")
sub("if(r){if(r.streak>s.maxStreak)s.maxStreak=r.streak;if(r.place===1)s.dayWins++;}", "cs0=x.in?cs0+1:0;if(cs0>s.maxStreak)s.maxStreak=cs0;if(r&&r.place===1)s.dayWins++;")
sub("shortDate(START)+' ~ '+shortDate(END)", "shortDate(TALLY)+' ~ '+shortDate(END)")
sub("<p>매일 한 만큼 점수가 쌓이고, 주마다 그리고 시험이 끝났을 때 순위를 매깁니다.</p>", "<p>매일 한 만큼 점수가 쌓이고, 주마다 그리고 시험이 끝났을 때 순위를 매깁니다.'+(TALLY>START?' 집계는 '+shortDate(TALLY)+'부터이고, 그 전 점수는 보이기만 합니다.':'')+'</p>")
# 집계 전에는 최종 결과 점수가 0으로 보이는 이유를 알려 준다
sub("if(me)L+='<div class=\"finme\"><small>지금까지 내 최종 점수</small>'+finBreak(me)+'</div>';", "if(me)L+='<div class=\"finme\"><small>지금까지 내 최종 점수</small>'+finBreak(me)+(today()<TALLY?'<p class=\"hint\" style=\"margin-top:6px\">집계는 '+esc(longDate(TALLY))+'부터 시작해서 지금은 0점입니다. 매일 얻은 점수는 오늘 화면과 순위의 이번 주에서 그대로 보입니다.</p>':'')+'</div>';")
# 집계 전 주는 주간 순위 점수 대신 '집계 전'
sub("""'<span class="tag wb">주간 '+(i+1)+'등 +'+WEEK_BONUS[i]+'</span>'""", """'<span class="tag wb">주간 '+(i+1)+'등'+(from>=TALLY?' +'+WEEK_BONUS[i]:' (집계 전)')+'</span>'""")
