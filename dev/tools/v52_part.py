# ---------------------------------------------------------------- v52: 5시간 상한 등 '확인 필요' 표시: 시간을 일부 줄이고 확인하면 표시가 사라진다
cut("function flagAct(V,f){", "function flagTags(f){", r"""function flagAct(V,f){
  if(!V.me||(f.mid!==V.me&&adminId(V)!==V.me))return '';
  var pl=flagPlan(V,f),open=S.flagFix&&S.flagFix.id===f.id;
  if(!open)return '<div class="flact"><button class="btn small primary" data-act="flag-open" data-id="'+esc(f.id)+'">시간 줄이고 확인하기</button></div>';
  var T=S.flagFix,typed=Math.round(+S.draft.flagN),n=typed>=0&&S.draft.flagN!==''&&S.draft.flagN!=null?typed:T.n,tot=pl.total;
  n=Math.max(0,Math.min(tot,Math.round(+n)||0));
  var h='<div class="flfix"><p class="hint">공부하지 않은 시간이 있다면 그만큼 빼 주세요. 뺀 뒤 확인하면 이 표시가 사라집니다.'+(tot?' 지금 기록은 '+fmtMins(tot)+'입니다.':' 이 기록에는 지울 시간이 남아 있지 않습니다.')+'</p>';
  if(tot){
    h+='<div class="chips">';
    [30,60,120,180,240].filter(function(m){return m<tot;}).forEach(function(m){h+=chipBtn('flag-set','n',String(m),m>=60?(m/60)+'시간':m+'분',!S.draft.flagN&&T.n===m);});
    h+=chipBtn('flag-set','n',String(tot),'전부 '+fmtMins(tot),!S.draft.flagN&&T.n===tot);
    h+='</div><input type="number" inputmode="numeric" min="0" max="'+tot+'" data-draft="flagN" data-live="1" placeholder="직접 입력 (분)" aria-label="뺄 시간 직접 입력(분)" style="margin-top:8px">';
    h+='<p class="hint">'+fmtMins(tot)+' → <b>'+fmtMins(tot-n)+'</b> 남김 ('+fmtMins(n)+' 뺌)</p>';
  }
  h+='<div class="row" style="margin-top:6px"><button class="btn small primary" data-act="flag-fix" data-id="'+esc(f.id)+'">'+(n?'빼고 확인 완료':'그대로 확인 완료')+'</button><button class="btn small" data-act="flag-close">닫기</button></div></div>';
  return '<div class="flact">'+h+'</div>';
}
""")
sub("<p class=\"hint\">켜놓기만 했을 수 있는 타이머 기록입니다. 본인이나 방장은 이 시간과 그만큼의 점수를 지울 수 있습니다.</p>", "<p class=\"hint\">켜놓기만 했을 수 있는 타이머 기록입니다. 본인이나 방장이 공부하지 않은 시간을 빼고 확인하면 이 표시가 사라집니다.</p>")
sub("    case 'flag-cut':{", r"""    case 'flag-open':{var Vfo=view(),flo=obj(Vfo.flags[id]);if(!Vfo.me||!flo.mid||(flo.mid!==Vfo.me&&adminId(Vfo)!==Vfo.me))break;S.flagFix={id:id,n:30};S.draft.flagN='';break;}
    case 'flag-close':S.flagFix=null;S.draft.flagN='';break;
    case 'flag-set':{if(!S.flagFix)break;S.flagFix.n=+el.getAttribute('data-v')||0;S.draft.flagN='';break;}
    case 'flag-fix':{
      var Vx=view(),fx=obj(Vx.flags[id]);if(!Vx.me||!fx.mid||(fx.mid!==Vx.me&&adminId(Vx)!==Vx.me)||!S.flagFix||S.flagFix.id!==id)break;
      var fpx=flagPlan(Vx,fx),totx=fpx.total,typx=S.draft.flagN!==''&&S.draft.flagN!=null?Math.round(+S.draft.flagN):S.flagFix.n,nx=Math.max(0,Math.min(totx,Math.round(+typx)||0));
      if(!need())break;
      var pathx=Object.keys(fpx.d).map(function(d){return 'days/'+fx.mid+'_'+d;}).concat(['flags/'+id]),snx=snap(pathx),leftx=nx;
      Object.keys(fpx.d).forEach(function(d){
        if(leftx<=0)return;var take=Math.min(leftx,fpx.d[d]);leftx-=take;
        editDayOf(fx.mid,d,function(dd){var v=(+dd.mins[fx.sid]||0)-take;if(v>0)dd.mins[fx.sid]=v;else delete dd.mins[fx.sid];if(typeof hhSub==='function')hhSub(dd,fx.sid,take);});
      });
      save('flags/'+id,Object.assign({},fx,{cut:Date.now(),by:Vx.me,cutMins:nx,ok:1}));
      S.flagFix=null;S.draft.flagN='';
      flash(nx?((fx.mid===Vx.me?'내':Vx.byId[fx.mid].name+' 님의')+' 공부 시간 '+fmtMins(nx)+'을 빼고 확인했습니다.'):'확인했습니다. 시간은 그대로 둡니다.',snx);
      break;
    }
    case 'flag-cut':{""")
