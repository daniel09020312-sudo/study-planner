# ---------------------------------------------------------------- v79: 할 일 순서 정리 창(여러 날 할 일 한 번에, 위·아래, 과목순·끝낸 일 아래로) (src/v79.js, v79.css)
V79_JS = open(BASE + '/src/v79.js', encoding='utf-8').read()
V79_CSS = open(BASE + '/src/v79.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V79_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V79_CSS + "</style>")
sub("  if(t==='help')return modalHelp(V);", "  if(t==='help')return modalHelp(V);\n  if(t==='gorder')return modalGOrder(V);")
sub("<button class=\"chip\" data-act=\"al-sort\"", "<button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button><button class=\"chip\" data-act=\"al-sort\"")
sub("<button class=\"chip\" data-act=\"g-donelast\"", "<button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button><button class=\"chip\" data-act=\"g-donelast\"")
sub("    case 'al-sort':", r"""    case 'go-r':S.gord=S.gord||{};S.gord.r=el.getAttribute('data-v')||'next';break;
    case 'go-left':S.gord=S.gord||{};S.gord.left=!S.gord.left;break;
    case 'go-mv':{
      var gV=view(),gdir=+el.getAttribute('data-v')||0;if(!gV.me||!need()||dayLocked(gV,date))break;
      var gleft=S.gord&&S.gord.left;
      editDay(date,function(d){
        var vis=d.goals.map(function(x,i){return {x:x,i:i};}).filter(function(o){return o.x&&!o.x.mv&&!(gleft&&o.x.done);});
        var p=-1;vis.forEach(function(o,j){if(o.x.id===id)p=j;});var q=p+gdir;if(p<0||q<0||q>=vis.length)return;
        var a=vis[p].i,b=vis[q].i,tmp=d.goals[a];d.goals[a]=d.goals[b];d.goals[b]=tmp;
      });
      S.scrollAfter='go-'+date;break;
    }
    case 'go-sort':{
      var gV2=view(),gk=el.getAttribute('data-k')==='done'?'done':'sub';if(!gV2.me||!need())break;
      var gds=date==='all'?gordDays():[date],gn=0;
      gds.forEach(function(d){if(dayLocked(gV2,d))return;var g0=dayOf(gV2,gV2.me,d).goals;if(g0.length<2)return;var g1=gordSort(gV2,g0,gk);if(g1.some(function(x,i){return x!==g0[i];})){gn++;editDay(d,function(dd){dd.goals=gordSort(gV2,dd.goals,gk);});}});
      flash(gn?(gk==='sub'?'과목순으로 정리했습니다.':'끝낸 일을 아래로 내렸습니다.'):'이미 그 순서입니다.');break;
    }
    case 'al-sort':""")
