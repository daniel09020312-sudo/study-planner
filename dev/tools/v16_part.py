# ---------------------------------------------------------------- 할 일(주간 달력) 끌어 옮기기
WD_JS = open(BASE + '/src/wkdrag.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", WD_JS + "\n/* ---------- 공부방 ---------- */")
sub("""  var h='<div class="wki'+(x.done?' done':'')+(late?' late':'')+'" id="wi-'+esc(x.id)+'" style="--sc:'+goalCol(V,x)+'">';""",
    """  var h='<div class="wki'+(x.done?' done':'')+(late?' late':'')+'" id="wi-'+esc(x.id)+'"'+(x.done?'':' data-wdrag="1"')+' data-d="'+d+'" data-id="'+esc(x.id)+'" style="--sc:'+goalCol(V,x)+'">';""")
sub("""  var h='<div class="wkc'+(d===t?' today':'')+(d<t?' past':'')+'" id="wc-'+d+'">';""",
    """  var h='<div class="wkc'+(d===t?' today':'')+(d<t?' past':'')+'" id="wc-'+d+'" data-d="'+d+'">';""")
sub("""  if(!tot)h+='<p class="hint wkhint">이 주에는 적은 할 일이 없습니다. 날짜 칸의 추가를 눌러 적어 보세요.</p>';""",
    """  if(!tot)h+='<p class="hint wkhint">이 주에는 적은 할 일이 없습니다. 날짜 칸의 추가를 눌러 적어 보세요.</p>';
  else h+='<p class="hint wkhint">할 일을 꾹 눌러 끌면 다른 날로 옮기거나 순서를 바꿀 수 있습니다. 끄는 채로 달력 오른쪽 끝에 잠깐 대고 있으면 다음 주로 넘어갑니다.</p>';""")
