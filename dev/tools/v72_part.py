# ---------------------------------------------------------------- v72: 할 일 목록 위 날짜 제목·화살표 없앰(오늘로 단추만), 할 일 끌 때 옆 스크롤 막음, 위 알림줄(공지·되돌리기 등)은 화면을 밀지 않고 위에 떠서
sub("""<div class="mnav"><button class="ib" data-act="al-week" data-d="-1" aria-label="이전 주"'+(ws<=AL_MIN?' disabled':'')+'>&lsaquo;</button><h1 class="wkt" id="alTitle">'+wkTitle(fv)+'</h1><button class="ib" data-act="al-week" data-d="1" aria-label="다음 주"'+(ws>=AL_MAX?' disabled':'')+'>&rsaquo;</button>';
  if(wkStart(fv)!==cur)h+='<button class="btn small" data-act="al-week" data-d="0" style="margin-left:6px">이번 주</button>';""",
"""<div class="mnav">';
  if(t<fv||t>addDays(fv,6))h+='<button class="btn small" data-act="al-week" data-d="0">오늘로</button>';""")
