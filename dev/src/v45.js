/* ---------- v45: 점수 집계 기간(시작일, 종료일)을 방장이 정함 ---------- */
var PERIOD_DEF=['2026-10-12','2026-12-08'],PERIOD_MAX_DAYS=400,TALLY_DEF='2026-11-02',TALLY='2026-11-02';
function isoOk(x){return typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&diffDays('2000-01-01',x)>=0&&addDays(x,0)===x;}
function periodOf(cfg){
  var p=obj(cfg&&cfg.period);
  var d=PERIOD_DEF,a;
  if(isoOk(p.s)&&isoOk(p.e)&&p.s<=p.e&&diffDays(p.s,p.e)<PERIOD_MAX_DAYS){
    d=[p.s,p.e];
    /* 집계 시작일 칸이 생기기 전에 방장이 정한 시작일은 집계 시작일이었다: 점수는 처음(10/12)부터 보이게 한다 */
    if(!isoOk(p.a)&&p.s>PERIOD_DEF[0]&&diffDays(PERIOD_DEF[0],p.e)<PERIOD_MAX_DAYS){p={s:PERIOD_DEF[0],e:p.e,a:p.s};d=[p.s,p.e];}
  }
  a=isoOk(p.a)&&p.a>=d[0]&&p.a<=d[1]?p.a:(TALLY_DEF<d[0]?d[0]:TALLY_DEF>d[1]?d[1]:TALLY_DEF);
  return [d[0],d[1],a];
}
function periodApply(cfg){var p=periodOf(cfg);START=p[0];END=p[1];TALLY=p[2];}
function periodSec(V){
  if(!V.me||adminId(V)!==V.me)return '';
  var p=periodOf(V.cfg),custom=!!obj(V.cfg.period).s;
  if(!S.draft.periodS)S.draft.periodS=p[0];if(!S.draft.periodE)S.draft.periodE=p[1];if(!S.draft.periodA)S.draft.periodA=p[2];
  return '<div class="sec"><h3>점수 집계 기간<small>방장만 바꿀 수 있습니다</small></h3><div class="row"><label for="perS">시작일</label><input type="date" id="perS" data-draft="periodS" value="'+(S.draft.periodS||p[0])+'" min="2026-01-01" max="2028-12-31"><label for="perE">종료일</label><input type="date" id="perE" data-draft="periodE" value="'+(S.draft.periodE||p[1])+'" min="2026-01-01" max="2028-12-31"></div><div class="row" style="margin-top:8px"><label for="perA">집계 시작일</label><input type="date" id="perA" data-draft="periodA" value="'+(S.draft.periodA||p[2])+'" min="2026-01-01" max="2028-12-31"></div><div class="row" style="margin-top:8px"><button class="btn small primary" data-act="period-save">저장</button>'+(custom?'<button class="btn small" data-act="period-reset">처음 값으로</button>':'')+'</div><p class="hint">지금 '+esc(shortDate(p[0])+' ~ '+shortDate(p[1]))+'. 점수는 시작일부터 보이고, 집계 시작일(지금 '+esc(shortDate(p[2]))+')부터 주간 우승, 배지, 최종 결과에 들어갑니다. 최종 결과는 종료일 다음 날 공개됩니다. 최대 '+PERIOD_MAX_DAYS+'일. 시작일은 월요일로 하면 주간 집계가 깔끔합니다.</p></div>';
}

