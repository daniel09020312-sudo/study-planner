# ---------------------------------------------------------------- v99: 하루는 새벽 5시부터 다음 날 새벽 5시까지(DAY_H). today()와 점수의 날짜 나누기가 이 기준을 씀
sub("function today(){return fd(new Date());}", "var DAY_H=5;\nfunction dayKey(ts){return fd(new Date(+ts-DAY_H*3600000));}\nfunction today(){return dayKey(Date.now());}\nfunction inEarly(iso,h,d){var x=new Date(iso);if(isNaN(x))return false;var k=x.getHours();return d?(fd(x)===d&&k<h):(k>=DAY_H&&k<h);}")
# 시간표의 지금 선: 새벽 0~5시는 전날 24~29시
sub("function nowMin(){var x=new Date();return x.getHours()*60+x.getMinutes();}", "function nowMin(){var x=new Date(),m=x.getHours()*60+x.getMinutes();return m<DAY_H*60?m+1440:m;}")
# 문제·풀이 점수, 확인 필요 표시의 날짜
sub("var k=mid+'_'+fd(new Date(ts));", "var k=mid+'_'+dayKey(ts);")
sub("posts[q.mid+'_'+fd(new Date(+q.at))]=1;", "posts[q.mid+'_'+dayKey(+q.at)]=1;")
sub("ds=[fd(new Date(+f.end)),fd(new Date(+f.start))]", "ds=[dayKey(+f.end),dayKey(+f.start)]")
sub("if(fd(new Date(+f.end))===date)", "if(dayKey(+f.end)===date)")
# 아침 출석은 그날 새벽 5시 뒤부터
sub("if(dx.in&&new Date(dx.in).getHours()<8)o.early8++;if(dx.in&&new Date(dx.in).getHours()<7)o.early7++;", "if(dx.in&&inEarly(dx.in,8,d))o.early8++;if(dx.in&&inEarly(dx.in,7,d))o.early7++;")
sub("    if(x.in&&new Date(x.in).getHours()<7)s.early++;\n", "    if(x.in&&inEarly(x.in,7,d))s.early++;\n")
sub("var a=new Date(x.in);return Math.max(1,1700-(a.getHours()*60+a.getMinutes()));", "var a=new Date(x.in),am=a.getHours()*60+a.getMinutes();if(fd(a)!==date)am+=1440;return Math.max(1,1700-am);")
