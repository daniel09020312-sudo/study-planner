# ---------------------------------------------------------------- v82: 할 일 모음 과목별 정리(이 기기 gbb_ibview: 기본 과목별, '적은 순'으로 바꿀 수 있음). 과목 순서(무지개)로 묶고 묶음마다 이름·개수·모두 고르기/풀기
sub("function modalInbox(V){", r"""function ibBySub(){return lsGet('gbb_ibview')!=='at';}
function ibSubRank(V,sid){var s=sid&&V.subById[sid];return s?V.subs.indexOf(s):9999;}
function modalInbox(V){""")
sub("<ul class=\"iblist\">';\n    list.forEach(function(x){\n      var on=!!I.sel[x.id],sub=x.sid&&V.subName[x.sid];",
    "<ul class=\"iblist\">';\n    var ibg=ibBySub(),ibPrev=null,ibCnt={},ibOn={};\n    if(ibg){list=list.map(function(x,i){return {x:x,i:i,r:ibSubRank(V,x.sid)};}).sort(function(a,c){return a.r-c.r||a.i-c.i;}).map(function(o){return o.x;});list.forEach(function(x){var k=V.subById[x.sid]?x.sid:'';ibCnt[k]=(ibCnt[k]||0)+1;if(I.sel[x.id])ibOn[k]=(ibOn[k]||0)+1;});}\n    list.forEach(function(x){\n      var on=!!I.sel[x.id],sub=x.sid&&V.subName[x.sid];\n      if(ibg){var gk=V.subById[x.sid]?x.sid:'';if(gk!==ibPrev){ibPrev=gk;var all=ibOn[gk]===ibCnt[gk];b+='<li class=\"ibgrp\"'+(gk?' style=\"--sc:'+subCol(V,gk)+'\"':'')+'><i aria-hidden=\"true\"></i><b>'+esc(gk?V.subName[gk]:'과목 없음')+'</b><small>'+ibCnt[gk]+'개</small><button class=\"linkbtn\" data-act=\"ib-selsub\" data-v=\"'+esc(gk)+'\">'+(all?'풀기':'모두 고르기')+'</button></li>';}}")
# 묶음 보기에서는 위 '과목별 고르기' 칩 대신 묶음 머리를 씀
sub("if(iks.length>1)b+='<div class=\"chips ibsubs\">", "if(iks.length>1&&!ibg)b+='<div class=\"chips ibsubs\">")
# 보기 바꾸기
sub("<button class=\"linkbtn\" data-act=\"ib-all\">", "<span class=\"ibview\"><button class=\"chip\" data-act=\"ib-view\" data-v=\"sub\" aria-pressed=\"'+(ibBySub()?'true':'false')+'\">과목별</button><button class=\"chip\" data-act=\"ib-view\" data-v=\"at\" aria-pressed=\"'+(ibBySub()?'false':'true')+'\">적은 순</button></span><button class=\"linkbtn\" data-act=\"ib-all\">")
# 과목 고르기는 이미 다 골랐으면 풀기
sub("case 'ib-selsub':{if(!S.ib)break;var Vis=view(),isid=el.getAttribute('data-v');ibItems(Vis).forEach(function(x){if((x.sid||'')===isid)S.ib.sel[x.id]=1;});break;}",
    "case 'ib-selsub':{if(!S.ib)break;var Vis=view(),isid=el.getAttribute('data-v'),ism=ibItems(Vis).filter(function(x){return (Vis.subById[x.sid]?x.sid:'')===isid||(x.sid||'')===isid;}),isAll=ism.length&&ism.every(function(x){return S.ib.sel[x.id];});ism.forEach(function(x){if(isAll)delete S.ib.sel[x.id];else S.ib.sel[x.id]=1;});break;}\n    case 'ib-view':lsSet('gbb_ibview',el.getAttribute('data-v')==='at'?'at':null);break;")
