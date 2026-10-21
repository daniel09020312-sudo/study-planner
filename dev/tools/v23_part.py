# ---------------------------------------------------------------- 달력 칸 정리: 수행평가는 과목 줄임말 색 칩, 내용은 날짜를 눌러서
CALEV_JS = open(BASE + '/src/calev.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", CALEV_JS + "\n/* ---------- 공부방 ---------- */")
sub("""    if(ev){evs+='<span class="ev'+(ev.exam?' exam':'')+'">'+esc(ev.s)+'</span>';n++;lab+=', '+ev.l;}
    mine.forEach(function(e){lab+=', '+e.title;if(n<2){evs+='<span class="ev mine">'+esc(e.title)+'</span>';n++;}});
    var dues=dueMap(V)[d]||[];dues.forEach(function(p){lab+=', 마감 '+p.label;if(n<2){evs+='<span class="ev due">마감 '+esc(p.label)+'</span>';n++;}});
    var more=(ev?1:0)+mine.length+dues.length-n;
    if(more>0)evs+='<span class="ev">+'+more+'</span>';""",
"""    if(ev){evs+='<span class="ev'+(ev.exam?' exam':'')+'">'+esc(ev.s)+'</span>';lab+=', '+ev.l;}
    mine.forEach(function(e){lab+=', '+e.title;});
    var chips=cellChips(V,mine),dues=dueMap(V)[d]||[];dues.forEach(function(p){lab+=', 마감 '+p.label;});
    if(chips.length||dues.length)evs+='<span class="sevs">'+chips.slice(0,3).map(function(c){return chipHtml(V,c);}).join('')+(chips.length>3?'<i class="sev more">+'+(chips.length-3)+'</i>':'')+(dues.length?'<i class="sev due">마감'+(dues.length>1?'<b>'+dues.length+'</b>':'')+'</i>':'')+'</span>';""")
# 달력 아래: 이번 달 수행평가 과목별 개수
sub("""  h+='</div></section><div class="col daycol" id="dp-'+S.date+'">'+dayPanel(V,S.date)+'</div>';""",
    """  h+='</div>'+monthLegend(V,ym)+'</section><div class="col daycol" id="dp-'+S.date+'">'+dayPanel(V,S.date)+'</div>';""")
# 날짜 칸을 누르면 오른쪽에: 과목 색 칩과 내용을 나눠서
sub("""    h+='<div class="evrow" id="ev-'+esc(e.id)+'"><span><em class="tag a">'+(e.shared?(own?'공유':esc(who?shortName(who.name):'공유')):'내 일정')+'</em>'+esc(e.title)+'</span>'""",
    """    var esid=evSid(V,e),rest=evRest(V,e,esid);
    h+='<div class="evrow sv" id="ev-'+esc(e.id)+'" style="--sc:'+(esid?subCol(V,esid):e.grp==='exam'?'var(--accent)':SGRAY)+'"><span>'+(esid?'<em class="tag sub">'+esc(V.subName[esid])+'</em>':'')+'<span class="evtx">'+esc(rest||e.title)+'</span><em class="tag">'+(e.shared?(own?'공유':esc(who?shortName(who.name):'공유')):'나만')+'</em></span>'""")
