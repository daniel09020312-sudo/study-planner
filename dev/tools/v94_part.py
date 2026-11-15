# ---------------------------------------------------------------- v94: 노동요 방장 보기, 최종 결과 방장 승인 뒤 공개 연출(src/v94.js)
V94_JS = open(BASE + '/src/v94.js', encoding='utf-8').read()
sub("function finalOpen(){return today()>END;}", "")
sub("/* ---------- 공부방 ---------- */", V94_JS + "\n/* ---------- 공부방 ---------- */")
# 노동요 방장 보기
sub("  if(!pv)h+=songTools(V,all.length);", "  if(!pv)h+=songTools(V,all.length);\n  if(adminId(V)===V.me&&all.length)h+='<div class=\"row sadmb\"><button class=\"btn small soft\" data-act=\"song-adm\" aria-pressed=\"'+(S.songAdm?'true':'false')+'\">'+(S.songAdm?'누가 들었나 닫기':'누가 들었나 보기 (방장만)')+'</button></div>'+songAdmHtml(V);")
sub("if(x.note)h+='<p class=\"snote\">'+esc(x.note)+'</p>';", "if(x.note)h+='<p class=\"snote\">'+esc(x.note)+'</p>';\n    h+=songAdmRow(V,x.id);")
# 최종 결과: 승인 전 안내, 방장 승인 카드, 다시 보기
sub("    L+='<section class=\"card fin\" id=\"c-fin-wait\" style=\"--k:0\"><div class=\"ct\"><h2>최종 결과<small>'+esc(longDate(open))+' 공개</small></h2></div>';\n    L+='<div class=\"fincd\"><b>D-'+Math.max(0,diffDays(t,open))+'</b><span>2차 시험이 끝난 다음 날 모두에게 공개됩니다. 그 전까지는 내 점수만 보입니다.</span></div>';",
    "    L+=finAdminCard(V);\n    L+='<section class=\"card fin\" id=\"c-fin-wait\" style=\"--k:0\"><div class=\"ct\"><h2>최종 결과<small>'+(t>END?'공개 준비 중':esc(longDate(open))+'부터')+'</small></h2></div>';\n    L+='<div class=\"fincd\">'+(t>END?'<b>곧</b><span>집계가 끝났습니다. 방장이 승인하면 공개 연출과 함께 순위가 공개됩니다.</span>':'<b>D-'+Math.max(0,diffDays(t,open))+'</b><span>2차 시험이 끝나고 방장이 승인하면 공개 연출과 함께 모두에게 공개됩니다. 그 전까지는 내 점수만 보입니다.</span>')+'</div>';")
sub("    L+='<section class=\"card fin\" id=\"c-fin\" style=\"--k:0\"><div class=\"ct\"><h2>최종 결과<small>'+esc(shortDate(TALLY)+' ~ '+shortDate(END))+'</small></h2></div>';",
    "    L+='<section class=\"card fin\" id=\"c-fin\" style=\"--k:0\"><div class=\"ct\"><h2>최종 결과<small>'+esc(shortDate(TALLY)+' ~ '+shortDate(END))+'</small></h2><button class=\"btn small soft\" data-act=\"fr-replay\">공개 연출 다시 보기</button></div>';\n    var cutL=fs.filter(function(x){return x.total>=FIN_CUT;});L+='<div class=\"fincut\"><b>'+FIN_CUT+'점 넘긴 사람 '+cutL.length+'명</b><span>'+cutL.map(function(x){return esc(x.p.name);}).join(', ')+'</span></div>';")
sub("'2차 시험이 끝난 다음 날 최종 결과와 함께 1·2·3등이 정해집니다.'", "'2차 시험이 끝나고 방장이 승인하면 최종 결과와 함께 1·2·3등이 공개됩니다.'")
sub("['최종 결과','2차 시험이 끝난 다음 날 공개. 1등, 2등, 3등은 미리 정해 둔 상품']", "['최종 결과','2차 시험이 끝나고 방장이 승인하면 공개 연출과 함께 공개. 100점 넘긴 사람 명단, 4등부터, 3·2·1등 순서. 1등, 2등, 3등은 미리 정해 둔 상품']")
sub("try{songDock();}catch(e){}", "try{songDock();}catch(e){}\n  try{finRevTick(V);}catch(e){}")
sub("    case 'ga-old':", r"""    case 'song-adm':S.songAdm=!S.songAdm;break;
    case 'fin-ok':{var Vf=view();if(adminId(Vf)!==Vf.me||today()<=END)break;if(prev!=='finok'){S.confirm='finok';break;}editCfg(function(c){c.finalOk={at:Date.now(),by:Vf.me};});flash('최종 결과를 공개했습니다.');break;}
    case 'fr-replay':finPlay(view());return;
    case 'ga-old':""")
