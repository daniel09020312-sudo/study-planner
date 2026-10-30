# ---------------------------------------------------------------- v61: 마감 뒤 인증은 인증 3점만(모두 끝내기 점수 없음), 점수 팝업은 순위 보너스 변화를 빼고 보여 줌
sub("(isLate(V,d,x.certAt)?RULE.allLate:RULE.allCert):0),", "(isLate(V,d,x.certAt)?0:RULE.allCert):0),")
sub("""  var g=day.goals,n=g.length,dn=g.filter(isDone).length,pt=late?RULE.allLate:RULE.allCert;
  if(n>=3&&dn===n)""", """  if(late)return ' 마감이 지나 인증하면 '+RULE.certLate+'점만 받습니다.';
  var g0=day.goals.filter(Boolean),g=g0.filter(function(x){return !x.mv;}),n=g0.length,dn=g.filter(isDone).length,pt=RULE.allCert;
  if(n>=3&&dn===g.length)""")
sub("return ' 할 일 '+(n-dn)+'개를 마저 끝내면 '+pt+'점을 더 받습니다.';", "return ' 할 일 '+(g.length-dn)+'개를 마저 끝내면 '+pt+'점을 더 받습니다.';")
sub("지금 인증하면 '+RULE.certLate+'점, 다 끝냈으면 '+RULE.allLate+'점이 더해집니다.", "지금 인증하면 '+RULE.certLate+'점입니다. 모두 끝내기 점수는 마감 전에 인증해야 받습니다.")
sub("'마감 뒤 인증은 '+RULE.allLate+'점'", "'마감 뒤 인증은 받지 않음'")
sub("마감 뒤 인증 '+RULE.certLate+'점, 다 끝냈으면 '+RULE.allLate+'점.", "마감 뒤 인증은 '+RULE.certLate+'점만.")
# 팝업: 순위 보너스(하루 순위) 바뀐 몫은 빼고, 내가 한 일로 바뀐 점수만
sub("before=myGrand(V0);", "before=myPopPts(V0);")
sub("pop(myGrand(V0)-before);", "pop(myPopPts(V0)-before);")
sub("function myGrand(V){", "function myPopPts(V){if(!V||!V.me)return 0;var t=0,m=V.sc[V.me]||{};for(var d in m)t+=m[d].total-(m[d].bonus||0);return t+bingoPts(V,V.me,START,END);}\nfunction myGrand(V){")
