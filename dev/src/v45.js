/* ---------- v45: 점수 집계 기간(시작일, 종료일)을 방장이 정함 ---------- */
var PERIOD_DEF=['2026-10-12','2026-12-08'],PERIOD_MAX_DAYS=400;
function isoOk(x){return typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&diffDays('2000-01-01',x)>=0&&addDays(x,0)===x;}
function periodOf(cfg){
  var p=obj(cfg&&cfg.period);
  if(isoOk(p.s)&&isoOk(p.e)&&p.s<=p.e&&diffDays(p.s,p.e)<PERIOD_MAX_DAYS)return [p.s,p.e];
  return PERIOD_DEF;
}
function periodApply(cfg){var p=periodOf(cfg);START=p[0];END=p[1];}
function periodSec(V){
  if(!V.me||adminId(V)!==V.me)return '';
  var p=periodOf(V.cfg),custom=!!obj(V.cfg.period).s;
  return '<div class="sec"><h3>점수 집계 기간<small>방장만 바꿀 수 있습니다</small></h3><div class="row"><label for="perS">시작일</label><input type="date" id="perS" data-draft="periodS" value="'+(S.draft.periodS||p[0])+'" min="2026-01-01" max="2028-12-31"><label for="perE">종료일</label><input type="date" id="perE" data-draft="periodE" value="'+(S.draft.periodE||p[1])+'" min="2026-01-01" max="2028-12-31"></div><div class="row" style="margin-top:8px"><button class="btn small primary" data-act="period-save">저장</button>'+(custom?'<button class="btn small" data-act="period-reset">처음 값으로</button>':'')+'</div><p class="hint">지금 '+esc(shortDate(p[0])+' ~ '+shortDate(p[1]))+'. 점수, 순위, 주간 우승, 최종 결과(종료일 다음 날 공개)가 이 기간으로 계산됩니다. 최대 '+PERIOD_MAX_DAYS+'일. 시작일은 월요일로 하면 주간 집계가 깔끔합니다.</p></div>';
}
