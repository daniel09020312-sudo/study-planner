# ---------------------------------------------------------------- v32: 과목 '후마니타스' 더하기
# 새 방은 처음 과목 목록(TEMPLATE)에 들어 있고, 이미 있는 방은 같은 학교 과목(TEMPLATE 중 4개 이상)일 때 한 번만 더한다.
# 한 번 더한 뒤(meta/config migHum)에는 누가 지워도 다시 넣지 않는다.
sub("'생명과학 실험'];", "'생명과학 실험','후마니타스'];")
sub("var SUB_ABBR={", "var SUB_ABBR={'후마니타스':'후마',")
sub("function tick(){\n", r"""var HUM_DONE=false;
function humMig(){
  if(HUM_DONE)return;var V=view();
  if(!S.ready||!V||!V.me||!canWrite()||!V.subs.length)return;
  HUM_DONE=true;
  if(obj(V.cfg).migHum)return;
  var names=V.subs.map(function(s){return s.name;});
  if(TEMPLATE.filter(function(n){return names.indexOf(n)>=0;}).length<4)return;
  if(names.indexOf('후마니타스')<0){
    var ord=V.subs.reduce(function(a,s){return Math.max(a,+s.order||0);},0)+1;
    save('subjects/shum',{name:'후마니타스',order:ord,items:itemsOf(DEFAULT_ITEMS)});
  }
  editCfg(function(c){c.migHum=1;});
}
function tick(){
  try{humMig();}catch(e){}
""")
