# ---------------------------------------------------------------- v84: 학교 시간표 자습 수업(진도가 끝나 수업 시간에 자습하는 과목). 내 시간표 tt.sch.sj={<칸 key>:표시한 날}, 그 과목 모든 교시에 '자습'
sub("  return {p:p.length?p:SCH_DEF.map(function(x){return {s:x[0],e:x[1]};}),w:w,has:has};", "  return {p:p.length?p:SCH_DEF.map(function(x){return {s:x[0],e:x[1]};}),w:w,has:has,sj:obj(s.sj)};")
sub("function schCell(V,sch,dw,i){", "function sjKey(k){return String(k||'').replace(/[.#$\\[\\]\\/]/g,'_');}\nfunction schCell(V,sch,dw,i){")
sub("  if(o){o.tc=String(c.tc||'').trim();o.r=String(c.r||'').trim();o.key=o.sid?'s:'+o.sid:'t:'+o.t;}", "  if(o){o.tc=String(c.tc||'').trim();o.r=String(c.r||'').trim();o.key=o.sid?'s:'+o.sid:'t:'+o.t;o.sj=!!obj(sch.sj)[sjKey(o.key)];}")
# 시간표 창 칸
sub("'<span'+(meta?' class=\"m\"':'')+'>'+esc(c.name)+'</span>'+meta", "'<span'+(meta?' class=\"m\"':'')+'>'+esc(c.name)+'</span>'+(c.sj?'<small class=\"sjb\">자습</small>':'')+meta")
sub("var cls='schc'+(c?' f':'')", "var cls='schc'+(c&&c.sj?' sj':'')+(c?' f':'')")
sub("b+='</tbody></table></div>';", "b+='</tbody></table></div>';\n  var sjn={};schEach(V,sch,function(c){if(c.sj)sjn[c.name]=1;});if(Object.keys(sjn).length)b+='<p class=\"hint sjlist\">자습 수업(진도 끝): '+Object.keys(sjn).map(esc).join(', ')+'</p>';")
sub("(cur?'<button class=\"btn small\" data-act=\"sch-clear\">비우기</button>':'')", "(cur?'<button class=\"btn small'+(cur.sj?'':' soft')+'\" data-act=\"sch-sj\" aria-pressed=\"'+(cur.sj?'true':'false')+'\">'+(cur.sj?'자습 표시 끄기':'진도 끝, 자습 수업')+'</button><button class=\"btn small\" data-act=\"sch-clear\">비우기</button>':'')")
# 수업 알림, 시간표 화면, 이 날 교시
sub("(b.j>b.i?'<span class=\"snx\">'+(b.j-b.i+1)+'시간 연속</span>':'')+'<button class=\"bnx\"", "(b.j>b.i?'<span class=\"snx\">'+(b.j-b.i+1)+'시간 연속</span>':'')+(c.sj?'<span class=\"snx sjx\">자습</span>':'')+'<button class=\"bnx\"")
sub("<b class=\"scn\">'+scn+'</b> '+esc(scc.name)+'</span>", "<b class=\"scn\">'+scn+'</b> '+esc(scc.name)+(scc.sj?'<em class=\"sjb\">자습</em>':'')+'</span>")
sub("h+='<div class=\"ttb fx k-school ttsc'+cls+'\"", "h+='<div class=\"ttb fx k-school ttsc'+(scc.sj?' sj':'')+cls+'\"")
sub("'</b>'+esc(c.name)+'</span>'", "'</b>'+esc(c.name)+(c.sj?' (자습)':'')+'</span>'")
sub("    case 'sch-clear':{", "    case 'sch-sj':{var sjs=S.schSel;if(!sjs)break;var Vsj=view(),sjc=schCell(Vsj,schOf(Vsj,Vsj.me),sjs.d,sjs.i);if(!sjc)break;var sjk=sjKey(sjc.key),sjOn=!sjc.sj;editSch(function(s){s.sj=obj(s.sj);if(sjOn)s.sj[sjk]=today();else delete s.sj[sjk];});flash(sjOn?sjc.name+': 진도 끝, 모든 교시에 자습으로 표시했습니다.':sjc.name+': 자습 표시를 껐습니다.');break;}\n    case 'sch-clear':{")
