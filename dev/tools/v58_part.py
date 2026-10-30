# ---------------------------------------------------------------- v58: 지난 날에서 다른 날로 옮긴 할 일(mv)은 그 날 '모두 끝내고 인증'에서 끝낸 것으로 친다
# (3개 이상 조건에는 세고, 끝내야 할 목록에서는 뺀다. 남은 할 일을 다 끝내고 인증하면 최고점)
sub("((g.length>=3&&done===g.length&&x.certAt)?", "((arr(x.goals).filter(Boolean).length>=3&&done===g.length&&x.certAt)?")
sub("all=g.length>=3&&g.filter(isDone).length===g.length;", "all=x.goals.filter(Boolean).length>=3&&g.filter(isDone).length===g.length;")
sub("gg.length>=3&&gg.filter(isDone).length===gg.length", "y.goals.filter(Boolean).length>=3&&gg.filter(isDone).length===gg.length")
sub("'할 일 3개 이상 세우고 전부 끝내기'", "'할 일 3개 이상 세우고 전부 끝내기(다른 날로 옮긴 할 일은 끝낸 것으로 침)'")
