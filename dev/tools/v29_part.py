# ---------------------------------------------------------------- v29: 시간표 화면에 학교 수업을 교시마다, 빌드 번호
# 학교 시간표를 넣은 요일은 '고정 시간표의 학교' 덩어리 대신 교시마다 과목 칸을 보인다(연달아 있는 수업은 한 칸).
# 빈 시간에 채우기도 수업 시간을 피한다.
sub("fx:fixedOn(V,d),", "fx:(function(f,sc){return sc.length?f.filter(function(b){return b.k!=='school';}):f;})(fixedOn(V,d),schItems(V,d)),sc:schItems(V,d),")
sub("c.fx.concat(c.pl.map(function(g){return {s:+g.ts,e:+g.te};}))", "c.fx.concat(c.sc).concat(c.pl.map(function(g){return {s:+g.ts,e:+g.te};}))")
sub("var items=c.fx.map(function(b){return {k:'f',b:b,s:b.s,e:b.e};}).concat(c.pl.map(", "var items=c.fx.map(function(b){return {k:'f',b:b,s:b.s,e:b.e};}).concat(c.sc.map(function(x){return {k:'sc',x:x,s:x.s,e:x.e};})).concat(c.pl.map(")
sub("      if(it.k==='f'){", r"""      if(it.k==='sc'){
        var sx=it.x,scc=sx.c,scn=(sx.i+1)+(sx.j>sx.i?'~'+(sx.j+1):'')+'교시',scol=scc.sid?subCol(V,scc.sid):SGRAY,sml=[scc.r,tm].filter(Boolean).join(' · ');
        h+='<div class="ttb fx k-school ttsc hs'+cls+'" id="tsc-'+c.d+'-'+sx.i+'" role="button" tabindex="0" data-act="open" data-modal="school"'+dat+' style="'+pos+';--sc:'+scol+'" aria-label="'+esc(scn+' '+scc.name+(scc.r?', '+scc.r:'')+', '+tm)+'"><span class="tbt"><b class="scn">'+scn+'</b> '+esc(scc.name)+'</span><small>'+esc(sml)+'</small></div>';
      }else if(it.k==='f'){""")
sub("var busy=fixedOn(V,d).map(function(b){return [b.s,b.e];})", "var busy=fixedOn(V,d).map(function(b){return [b.s,b.e];}).concat(schItems(V,d).map(function(b){return [b.s,b.e];}))")
# 빌드 번호: 웹 판은 version.txt와 비교해 새 판이 올라왔으면 다시 읽는다(web_offline_part.py)
import time as _time
APP_BUILD = str(int(_time.time()))
sub("function splashDone(){", "var APP_BUILD='" + APP_BUILD + "';\nfunction splashDone(){")
