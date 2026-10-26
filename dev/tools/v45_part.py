# ---------------------------------------------------------------- v45: 점수 집계 기간을 방장이 정함 (JS는 src/v45.js)
V45_JS = open(BASE + '/src/v45.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V45_JS + "\n/* ---------- 공부방 ---------- */")
sub("  var roster=arr(cfg.roster).filter(function(m){return m&&m.id;});\n", "  periodApply(cfg);\n  var roster=arr(cfg.roster).filter(function(m){return m&&m.id;});\n")
sub("'</div>'+noticeSec(V)+'", "'</div>'+noticeSec(V)+periodSec(V)+'")
sub("    case 'notice-x':", r"""    case 'period-save':{
      var Vps=view(),ps=S.draft.periodS||periodOf(Vps.cfg)[0],pe=S.draft.periodE||periodOf(Vps.cfg)[1];
      if(!Vps.me||adminId(Vps)!==Vps.me||!need())break;
      if(!isoOk(ps)||!isoOk(pe)){flash('날짜를 골라 주세요.');break;}
      if(ps>pe){flash('시작일이 종료일보다 늦을 수 없습니다.');break;}
      if(diffDays(ps,pe)>=PERIOD_MAX_DAYS){flash('기간은 '+PERIOD_MAX_DAYS+'일까지입니다.');break;}
      editCfg(function(c){c.period={s:ps,e:pe};});
      if(canWrite()){S.draft.periodS='';S.draft.periodE='';S.sync=true;flash('집계 기간을 '+shortDate(ps)+' ~ '+shortDate(pe)+'로 정했습니다.');}
      break;
    }
    case 'period-reset':{var Vpr=view();if(!Vpr.me||adminId(Vpr)!==Vpr.me||!need())break;editCfg(function(c){delete c.period;});S.draft.periodS='';S.draft.periodE='';if(canWrite())flash('처음 기간으로 되돌렸습니다.');break;}
    case 'notice-x':""")
