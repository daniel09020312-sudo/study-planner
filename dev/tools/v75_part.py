# ---------------------------------------------------------------- v75: 안 읽은 메시지 수는 이 기기에서 본 시각과 다른 기기에서 본 시각(reads/<나>) 중 늦은 것 기준
sub("function unreadOf(V,c){var lr=+S.read[c]||0,", "function unreadOf(V,c){var lr=Math.max(+S.read[c]||0,+obj(V.reads&&V.reads[V.me])[c]||0),")
