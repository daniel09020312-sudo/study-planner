# ---------------------------------------------------------------- v37: 인증 마감 새벽 5시, 어제 할 일은 마감 뒤에도 완료 표시(인증은 늦은 인증 점수)
# 1) 마감: 기본 29시(다음 날 새벽 5시). 예전 방은 한 번만 29로 바꾼다(meta/config migCert5). 설정에서 새벽 3~5시도 고를 수 있게
sub("certHour:typeof cfg.certHour==='number'?cfg.certHour:26", "certHour:typeof cfg.certHour==='number'?cfg.certHour:29")
sub("[[22,'밤 10시'],[23,'밤 11시'],[24,'자정'],[25,'다음 날 새벽 1시'],[26,'다음 날 새벽 2시']]",
    "[[22,'밤 10시'],[23,'밤 11시'],[24,'자정'],[25,'다음 날 새벽 1시'],[26,'다음 날 새벽 2시'],[27,'다음 날 새벽 3시'],[28,'다음 날 새벽 4시'],[29,'다음 날 새벽 5시']]")
sub("else if(kind==='certHour'){editCfg(function(c){c.certHour=+v||26;});}", "else if(kind==='certHour'){editCfg(function(c){c.certHour=+v||29;c.migCert5=1;});}")
sub("if(typeof c.certHour!=='number')c.certHour=26;", "if(typeof c.certHour!=='number')c.certHour=29;")
sub("function tick(){\n", r"""var CERT_MIG=false;
function certMig(){
  if(CERT_MIG)return;var V=view();
  if(!S.ready||!V||!V.me||!canWrite())return;
  CERT_MIG=true;var c=obj(V.cfg);
  if(c.migCert5||!(typeof c.certHour==='number'&&c.certHour<29))return;
  editCfg(function(x){x.certHour=29;x.migCert5=1;});
}
function tick(){
  try{certMig();}catch(e){}
""")

# 2) 어제 할 일: 마감이 지나도 완료 표시를 바꿀 수 있다(그제부터는 그대로 막음). 할 일을 더하거나 빼는 것은 예전처럼 막는다
sub("function dayLocked(V,date){return date<today()&&Date.now()>certEnd(V,date).getTime();}",
    "function dayLocked(V,date){return date<today()&&Date.now()>certEnd(V,date).getTime();}\nfunction doneLocked(V,date){return dayLocked(V,date)&&date<addDays(today(),-1);}")
sub("    else if(!open)c.done=!!o.done;", "    else if(doneLocked(V,m[2]))c.done=!!o.done;")
sub("aria-label=\"'+esc(x.text)+' 완료 표시\"'+(mode!=='full'||dayLocked(V,date)?' disabled':'')", "aria-label=\"'+esc(x.text)+' 완료 표시\"'+(mode!=='full'||doneLocked(V,date)?' disabled':'')")
sub("(mode!=='full'||dayLocked(V,d)?", "(mode!=='full'||doneLocked(V,d)?")
sub("    case 'goal-toggle':if(dayLocked(view(),date)){", "    case 'goal-toggle':if(doneLocked(view(),date)){")

# 3) 오늘 화면: 어제를 인증하지 않았으면 마감 뒤에도 늦은 인증으로 할 수 있게 알려 준다
sub("""h+='<div class="cert"><div class="what"><b>어제 공부 인증</b><span class="hint">'+esc(certLabel(V.certHour).replace('다음 날 ','오늘 '))+'까지 인증하면 어제 점수에 10점이 더해집니다.</span></div><button class="btn small soft" data-act="cert" data-date="'+yd+'">어제 인증하기</button></div>';""",
    """h+='<div class="cert"><div class="what"><b>어제 공부 인증</b><span class="hint">'+esc(certLabel(V.certHour).replace('다음 날 ','오늘 '))+'까지 인증하면 어제 점수에 10점이 더해집니다.</span></div><button class="btn small soft" data-act="cert" data-date="'+yd+'">어제 인증하기</button></div>';
    else if(isT&&yd>=START&&!dayOf(V,V.me,yd).certAt&&dayOf(V,V.me,yd).goals.filter(function(g){return g&&!g.mv;}).length)h+='<div class="cert late"><div class="what"><b>어제 공부 인증 (마감 지남)</b><span class="hint">어제 할 일은 지금도 완료 표시를 할 수 있습니다. 지금 인증하면 '+RULE.certLate+'점이고, 어제 할 일을 다 끝냈으면 '+RULE.allLate+'점이 더해집니다.</span></div><div class="row"><button class="btn small" data-act="pick-date" data-d="'+yd+'">어제 할 일 보기</button><button class="btn small soft" data-act="cert" data-date="'+yd+'">어제 인증하기</button></div></div>';""")
