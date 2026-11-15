# ---------------------------------------------------------------- v95: 최종 결과 3D 공개 연출(src/finrev3d.js, finrev3d.css, three.js r128은 public/vendor/three-r128.min.js를 열 때만 불러옴). 3D가 안 되거나 움직임 줄이기면 v94 연출(창 'finrev')
FR3_JS = open(BASE + '/src/finrev3d.js', encoding='utf-8').read()
FR3_CSS = open(BASE + '/src/finrev3d.css', encoding='utf-8').read()
sub("</style>", FR3_CSS + "</style>")
sub("/* ---------- 공부방 ---------- */", FR3_JS + r"""
var FR3_ON=false;
function finPlay(V){
  if(FR3_ON)return;
  var old=function(){S.fr={s:0};openModal('finrev');render();};
  if(reduced||!FR3.webgl())return old();
  var fs=finalStandings(V);
  var data={title:'최종 결과 발표',period:shortDate(TALLY)+' ~ '+shortDate(END),cut:FIN_CUT,people:fs.map(function(x){return {name:x.p.name,total:x.total,me:x.p.id===V.me};}),prizes:[1,2,3].map(function(k){return prizeOf(V,k).t;})};
  FR3_ON=true;
  FR3.play(data,{onClose:function(){FR3_ON=false;render();},onFail:function(){FR3_ON=false;old();},onReplay:function(){setTimeout(function(){finPlay(view());},500);}});
}
/* ---------- 공부방 ---------- */""")
sub("S.fr={s:0};openModal('finrev');}catch(e){}", "finPlay(V);}catch(e){}")
sub("    case 'fr-replay':S.fr={s:0};openModal('finrev');return;", "    case 'fr-replay':finPlay(view());return;")
