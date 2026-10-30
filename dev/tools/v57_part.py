# ---------------------------------------------------------------- v57: 시작 연출 끄기 (이 기기 gbb_nosplash)
sub("if(seen){sp0.parentNode.removeChild(sp0);return;}", "try{if(localStorage.getItem('gbb_nosplash')==='1')seen=true;}catch(e){}\nif(seen){sp0.parentNode.removeChild(sp0);return;}")
sub("pokeSec()+noticeSec(V)", "spSec()+pokeSec()+noticeSec(V)")
sub("/* ---------- 찌르기 알림:", """/* ---------- v57: 시작 연출 끄기 (이 기기) ---------- */
function spOff(){return lsGet('gbb_nosplash')==='1';}
function spSec(){
  var off=spOff();
  return '<div class="sec"><h3>시작 연출<small>이 기기</small></h3><div class="row"><button class="btn small'+(off?' primary':'')+'" data-act="sp-toggle" aria-pressed="'+(off?'false':'true')+'">'+(off?'연출 켜기':'연출 끄기')+'</button></div><p class="hint">'+(off?'앱을 켤 때 그림 없이 바로 엽니다.':'앱을 켤 때 아이콘을 그리는 연출을 보여 줍니다. 끄면 바로 엽니다.')+'</p></div>';
}
/* ---------- 찌르기 알림:""")
sub("    case 'rep-week':S.repWeek=id;break;", "    case 'sp-toggle':lsSet('gbb_nosplash',spOff()?null:'1');flash(spOff()?'다음부터 연출 없이 바로 엽니다.':'다음부터 시작 연출을 보여 줍니다.');break;\n    case 'rep-week':S.repWeek=id;break;")
