# ---------------------------------------------------------------- v53: 1:1 대결 종류를 다시 줄이고(점수·공부 시간·끝낸 할 일), 오른쪽 칸 추가. 지난 날에서 옮긴 할 일은 모두 끝내기·인증 점수 계산에서 뺀다
sub("  DUEL_KINDS.forEach(function(k){b+=chipBtn('duel-set','kind',k.id,k.name,f.kind===k.id);});", "  DUEL_KINDS.filter(function(k){return !k.hide;}).forEach(function(k){b+=chipBtn('duel-set','kind',k.id,k.name,f.kind===k.id);});")
sub("한 명을 골라 점수, 공부 시간, 할 일 달성률 같은 걸로 겨뤄 보세요.", "한 명을 골라 점수, 공부 시간, 끝낸 할 일 중 하나로 겨뤄 보세요.")
sub("한 명을 골라 점수, 공부 시간 같은 걸로 겨룹니다.", "한 명을 골라 점수, 공부 시간, 끝낸 할 일로 겨룹니다.")
sub("var x=obj(V.days[m.id+'_'+d]),g=arr(x.goals),done=g.filter(isDone).length,", "var x=obj(V.days[m.id+'_'+d]),g=arr(x.goals).filter(function(q){return !(q&&q.mv);}),done=g.filter(isDone).length,")
sub("var x=dayOf(V,mid,d),r=rows[d],g=x.goals,dm=", "var x=dayOf(V,mid,d),r=rows[d],g=x.goals.filter(function(q){return !(q&&q.mv);}),dm=")
sub("var y=dayOf(V,mid,dd),gg=y.goals;", "var y=dayOf(V,mid,dd),gg=y.goals.filter(function(q){return !(q&&q.mv);});")
# 주간 리포트의 할 일 개수에서도 옮긴(mv) 할 일은 뺀다
sub("tm=0,k,g=x.goals,dn=g.filter(isDone).length,r=V.sc[m.id]&&V.sc[m.id][d];", "tm=0,k,g=x.goals.filter(function(q){return !(q&&q.mv);}),dn=g.filter(isDone).length,r=V.sc[m.id]&&V.sc[m.id][d];")
