# ---------------------------------------------------------------- v51: 더보기 목록, 1:1 대결 재구성 (JS는 src/v51.js, CSS는 src/v51.css)
V51_JS = open(BASE + '/src/v51.js', encoding='utf-8').read()
V51_CSS = open(BASE + '/src/v51.css', encoding='utf-8').read()
# 이전 duelRow, modalDuel은 지우고 v51.js의 것을 쓴다(뒤에 있는 선언이 이기므로)
cut("function duelRow(V,d){", "var PLAYTABS=", "")
cut("function modalDuel(V){", "function afterPlay(V){", "")
sub("/* ---------- 공부방 ---------- */", V51_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V51_CSS + "</style>")
# 이전 duelRow, modalDuel, duelNum, duelDesc는 v51.js의 것으로 덮는다(뒤에 선언된 함수가 이김)
# --- 대결 계산
sub("for(var x=d.start;x<=d.end&&x<=t;x=addDays(x,1)){var ra=V.sc[d.a]&&V.sc[d.a][x],rb=V.sc[d.b]&&V.sc[d.b][x];d.pa+=duelVal(d,ra);d.pb+=duelVal(d,rb);}",
    "for(var x=d.start;x<=d.end&&x<=t;x=addDays(x,1)){var ra=V.sc[d.a]&&V.sc[d.a][x],rb=V.sc[d.b]&&V.sc[d.b][x],va=duelDay(V,d,d.a,x,ra),vb=duelDay(V,d,d.b,x,rb);(d.rd=d.rd||[]).push({d:x,a:va||0,b:vb||0});if(va!=null){d.pa+=va;d.ca=(d.ca||0)+1;}if(vb!=null){d.pb+=vb;d.cb=(d.cb||0)+1;}}")
sub("d.state=t>d.end?'done':t<d.start?'ready':'on';\n      if(d.state==='done'){d.win=d.pa>d.pb?d.a:d.pb>d.pa?d.b:null;d.lose=d.win?(d.win===d.a?d.b:d.a):null;}",
    "d.state=t>d.end?'done':t<d.start?'ready':'on';\n      duelFinish(d);\n      if(d.state==='done'){d.win=duelWinner(d);d.lose=d.win?(d.win===d.a?d.b:d.a):null;}")
# --- 신청, 응원, 한마디, 자랑
sub("save('duels/'+did,{a:Vd.me,b:F.b,stake:stx,kind:F.kind||'score',days:duelLen({days:F.len}),status:'pending',at:Date.now()});",
    "var dnote=String(S.draft.duelNote||'').trim().slice(0,40),dmode=(duelKindOf({kind:F.kind}).rounds||F.mode==='rounds')?'rounds':'sum',dobj={a:Vd.me,b:F.b,stake:stx,kind:F.kind||'score',days:duelLen({days:F.len}),mode:dmode,status:'pending',at:Date.now()};if(dnote)dobj.note=dnote;\n      save('duels/'+did,dobj);S.draft.duelNote='';")
sub("text:'1:1 대결을 신청했습니다('+duelDesc({kind:F.kind,days:F.len})+'). 도전 화면에서 수락해 주세요.'",
    "text:'1:1 대결을 신청했습니다('+duelDesc({kind:F.kind,days:F.len,mode:dmode})+')'+(dnote?' “'+dnote+'”':'')+'. 도전 화면에서 수락해 주세요.'")
sub("text:'1:1 대결을 수락했습니다. 내일부터 '+duelLen(dd0)+'일 동안 '+duelKindOf(dd0).name+' 기준으로 겨룹니다.'",
    "text:'1:1 대결을 수락했습니다. 내일부터 '+duelDesc(dd0)+' 기준으로 겨룹니다.'")
sub("S.duelF={b:(el&&el.getAttribute('data-b'))||'',kind:(el&&el.getAttribute('data-kind'))||'score',len:+(el&&el.getAttribute('data-len'))||DUEL_DAYS,stake:'roul'};S.draft.duelStake='';",
    "S.duelF={b:(el&&el.getAttribute('data-b'))||'',kind:(el&&el.getAttribute('data-kind'))||'score',len:+(el&&el.getAttribute('data-len'))||DUEL_DAYS,mode:(el&&el.getAttribute('data-mode'))||'sum',stake:'roul'};S.draft.duelStake='';S.draft.duelNote='';")
sub("else if(dk2==='len'){if(DUEL_LENS.indexOf(+dv2)>=0)S.duelF.len=+dv2;}", "else if(dk2==='len'){if(DUEL_LENS.indexOf(+dv2)>=0)S.duelF.len=+dv2;}else if(dk2==='mode'){S.duelF.mode=dv2==='rounds'?'rounds':'sum';}")
sub("    case 'notice-x':", r"""    case 'more-list':{var mk=el.getAttribute('data-k');S.more=S.more||{};S.more[mk]=!S.more[mk];break;}
    case 'duel-cheer':{
      var Vc=view(),dc=Vc.duels[id],side=el.getAttribute('data-side');
      if(!dc||!Vc.me||dc.status==='pending'||dc.a===Vc.me||dc.b===Vc.me||(side!=='a'&&side!=='b')||!need())break;
      var dcn=clone(dc);dcn.cheer=obj(dcn.cheer);if(dcn.cheer[Vc.me]===side)delete dcn.cheer[Vc.me];else dcn.cheer[Vc.me]=side;
      if(!Object.keys(dcn.cheer).length)delete dcn.cheer;
      save('duels/'+id,dcn);break;
    }
    case 'duel-taunt':{
      var Vt=view(),dt=Vt.duels[id],ti=+el.getAttribute('data-i');
      if(!dt||!Vt.me||(dt.a!==Vt.me&&dt.b!==Vt.me)||!TAUNTS[ti]||!need())break;
      S.tauntAt=S.tauntAt||{};if(Date.now()-(S.tauntAt[id]||0)<30000){flash('조금 뒤에 다시 보낼 수 있습니다.');break;}
      S.tauntAt[id]=Date.now();
      save('msgs/'+rid('x'),{from:Vt.me,to:dt.a===Vt.me?dt.b:dt.a,text:TAUNTS[ti],go:'play',duel:id,at:Date.now()});
      flash('상대에게 보냈습니다.');break;
    }
    case 'duel-brag':{
      var Vb=view(),db=duelList(Vb).filter(function(x){return x.id===id;})[0];
      if(!db||db.state!=='done'||db.win!==Vb.me||db.brag||!need())break;
      var dbn=clone(Vb.duels[id]);dbn.brag=true;save('duels/'+id,dbn);
      var sb=duelSides(db),lo=Vb.byId[db.win===db.a?db.b:db.a];
      save('msgs/'+rid('x'),{from:Vb.me,to:'all',text:'1:1 대결에서 '+(lo?lo.name+' 님을 ':'')+'이겼습니다! ('+duelDesc(db)+', '+(duelMode(db)==='rounds'?sb[0]+' : '+sb[1]+' 라운드':duelNum(db,db.pa)+' : '+duelNum(db,db.pb))+')',go:'play',duel:id,at:Date.now()});
      flash('대화방에 자랑했습니다.');break;
    }
    case 'notice-x':""")
sub("    case 'rank-me':{", "    case 'rank-me':{S.more=S.more||{};S.more['rank'+S.range]=true;")
# --- 도전 화면: 대결 탭 본문과 안내
i_a = "}else if(pt==='duel'){\n    h+='<section class=\"card\" id=\"c-duels\""
cut(i_a, "  }else{\n    h+=badgeView(V);", "}else if(pt==='duel'){\n    h+=duelTab(V,t);\n")
sub("duel:'한 명을 골라 2일 동안 얻은 점수로 겨룹니다.'", "duel:'한 명을 골라 점수, 공부 시간 같은 걸로 겨룹니다. 하루씩 승부하는 라운드제, 구경하는 사람의 응원, 도전장 한마디도 있습니다.'")
# --- 10명까지만 보이고 더보기
sub("st.forEach(function(x,i){\n    var last=i===st.length-1&&st.length>1&&any", "moreCut('rank'+S.range,st).forEach(function(x){var i=st.indexOf(x);\n    var last=i===st.length-1&&st.length>1&&any")
sub("  h+='</section>';\n  if(S.range!=='all'&&st.length){", "  h+=moreBtn('rank'+S.range,st.length)+'</section>';\n  if(S.range!=='all'&&st.length){")
sub("    st.forEach(function(x){\n      h+='<tr><th class=\"nm\">'", "    moreCut('rank'+S.range,st).forEach(function(x){\n      h+='<tr><th class=\"nm\">'")
sub("  byT.forEach(function(o){h+='<div class=\"hb'", "  moreCut('rcmp',byT).forEach(function(o){h+='<div class=\"hb'")
sub("  order.forEach(function(o){h+='<tr'+(o.p.me?' class=\"me\"':'')+'><td>'+esc(o.p.name)", "  moreCut('rcmp',order).forEach(function(o){h+='<tr'+(o.p.me?' class=\"me\"':'')+'><td>'+esc(o.p.name)")
sub("  return h+'</tbody></table></div></section></div></div>'+reportMore(V,from,Wk,Pv)+'</div>';", "  return h+'</tbody></table></div>'+moreBtn('rcmp',order.length)+'</section></div></div>'+reportMore(V,from,Wk,Pv)+'</div>';")
sub("if(S.frAll||list.length<=14)return list;\n  var top=list.slice(0,12)", "if(S.frAll||list.length<=10)return list;\n  var top=list.slice(0,10)")
