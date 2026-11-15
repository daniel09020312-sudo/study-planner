# ---------------------------------------------------------------- v95: 최종 결과 3D 공개 연출(src/finrev3d.js, finrev3d.css, three.js r128은 public/vendor/three-r128.min.js를 열 때만 불러옴). 3D가 안 되면 연출 없이 결과 화면으로(2D 연출은 v96에서 지움)
FR3_JS = open(BASE + '/src/finrev3d.js', encoding='utf-8').read()
FR3_CSS = open(BASE + '/src/finrev3d.css', encoding='utf-8').read()
sub("</style>", FR3_CSS + "</style>")
sub("/* ---------- 공부방 ---------- */", FR3_JS + r"""
var FR3_ON=false;
function finPlay(V){
  if(FR3_ON)return;
  var old=function(){S.range='all';try{goTab('rank');}catch(e){}flash('이 기기에서는 3D 연출을 열 수 없어 결과만 보여 드립니다.');render();};
  if(!FR3.webgl())return old();
  var fs=finalStandings(V);
  var data={title:'최종 결과 발표',period:shortDate(TALLY)+' ~ '+shortDate(END),cut:FIN_CUT,people:fs.map(function(x){return {name:x.p.name,total:x.total,me:x.p.id===V.me};}),prizes:[1,2,3].map(function(k){return prizeOf(V,k).t;})};
  FR3_ON=true;
  FR3.play(data,{onClose:function(){FR3_ON=false;render();},onFail:function(){FR3_ON=false;old();},onReplay:function(){setTimeout(function(){finPlay(view());},500);}});
}
/* ---------- 공부방 ---------- */""")
