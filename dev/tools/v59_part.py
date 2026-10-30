# ---------------------------------------------------------------- v59: 할 일 하루 최대 20개, 다른 날로 옮긴 할 일 되돌리기(mv-back)
sub("var GMAX=12,ROSTER_MAX=", "var GMAX=20,ROSTER_MAX=")
sub("<em class=\"tag\">다른 날로 옮김</em></div><span></span></li>'", "<em class=\"tag\">다른 날로 옮김</em></div><button class=\"btn small soft\" data-act=\"mv-back\" data-date=\"'+esc(date)+'\" data-id=\"'+esc(x.id)+'\">되돌리기</button></li>'")
sub("/* ---------- 점수 ---------- */", r"""/* ---------- v59: 옮긴 할 일 되돌리기. 옮겨 간 날(오늘이나 그 뒤)에서 빼고, 원래 날의 '다른 날로 옮김'을 다시 할 일로 ---------- */
function mvTarget(V,from,g){
  var pre=V.me+'_',best=null;
  Object.keys(V.days).forEach(function(k){
    if(k.indexOf(pre)!==0)return;var d=k.slice(pre.length);if(d===from||!/^\d{4}-\d{2}-\d{2}$/.test(d))return;
    arr(obj(V.days[k]).goals).forEach(function(x){
      if(!x||x.mv)return;
      var same=x.id===g.id,like=!same&&d>from&&x.text===g.text&&(x.sid||'')===(g.sid||'');
      if(!same&&!like)return;
      var sc=same?0:1;
      if(!best||sc<best.sc||(sc===best.sc&&d<best.d))best={d:d,g:x,sc:sc};
    });
  });
  return best;
}
function mvBack(from,id){
  var V=view();if(!V.me||!need())return;
  var g=dayOf(V,V.me,from).goals.filter(function(x){return x&&x.id===id&&x.mv;})[0];if(!g)return;
  var tg=mvTarget(V,from,g);
  if(tg&&tg.g.done){flash(shortDate(tg.d)+'에 이미 끝낸 할 일이라 되돌릴 수 없습니다.');return;}
  if(tg&&tg.d<today()){flash('옮겨 간 날('+shortDate(tg.d)+')이 지나서 되돌릴 수 없습니다.');return;}
  var paths=['days/'+V.me+'_'+from];if(tg)paths.push('days/'+V.me+'_'+tg.d);
  var sn=snap(paths);
  if(tg)editDay(tg.d,function(d){d.goals=d.goals.filter(function(x){return !(x&&x.id===tg.g.id);});if(d.focus===tg.g.id)d.focus=null;});
  editDay(from,function(d){d.goals.forEach(function(x){if(x&&x.id===id){delete x.mv;x.done=false;}});});
  flash(shortDate(from)+' 할 일로 되돌렸습니다.'+(tg?' ('+shortDate(tg.d)+'에서 뺐습니다)':''),sn);
}
/* ---------- 점수 ---------- */""")
sub("    case 'rep-week':S.repWeek=id;break;", "    case 'mv-back':mvBack(date,id);break;\n    case 'rep-week':S.repWeek=id;break;")
sub(".goal.mv{opacity:.62}", ".goal.mv>.chk,.goal.mv>.gt{opacity:.62}")
