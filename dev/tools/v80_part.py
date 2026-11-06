# ---------------------------------------------------------------- v80: 순서 정리 창 끌어 옮기기·여러 개 골라 옮기기 (src/v80.js)
V80_JS = open(BASE + '/src/v80.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V80_JS + "\n/* ---------- 공부방 ---------- */")
# 줄: 고르기 칸, 손잡이, data-date·data-id / 날짜 묶음에 data-d
sub("b+='<section class=\"gordd'+(d===t?' today':'')+'\" id=\"go-'+d+'\">", "b+='<section class=\"gordd'+(d===t?' today':'')+'\" id=\"go-'+d+'\" data-d=\"'+d+'\">")
sub("      b+='<li class=\"gordi'+(x.done?' done':'')+'\" style=\"--sc:'+goalCol(V,x)+'\"><i class=\"sdot\"></i>",
    "      var gk=d+'|'+x.id,gon=!!(S.gsel&&S.gsel[gk]);\n      b+='<li class=\"gordi'+(x.done?' done':'')+(gon?' sel':'')+(lock?' lock':'')+'\" data-date=\"'+d+'\" data-id=\"'+esc(x.id)+'\" style=\"--sc:'+goalCol(V,x)+'\">'+(lock?'<i class=\"sdot\"></i>':'<button class=\"gck'+(gon?' on':'')+'\" data-act=\"go-sel\" data-date=\"'+d+'\" data-id=\"'+esc(x.id)+'\" aria-pressed=\"'+(gon?'true':'false')+'\" aria-label=\"고르기\"><span></span></button>')+'")
sub("      if(!lock)b+='<button class=\"ib sm\" data-act=\"go-mv\"", "      if(!lock)b+='<span class=\"gdh\" aria-label=\"끌어서 옮기기\" role=\"img\">&#8801;</span>';\n      if(!lock)b+='<button class=\"ib sm\" data-act=\"go-mv\"")
# 고른 것이 있으면 위쪽에 옮기기 줄
sub("  b+='<div class=\"row gorda\">", r"""  var gks=gselKeys();
  if(gks.length){var fut=days.filter(function(d){return d>=t&&!dayLocked(V,d);});b+='<div class="gselbar"><b>'+gks.length+'개 고름</b><span class="gseld">'+fut.slice(0,14).map(function(d){var dt=pd(d);return '<button class="chip" data-act="go-to" data-date="'+d+'">'+(d===t?'오늘':(dt.getMonth()+1)+'/'+dt.getDate()+' '+DOW[dt.getDay()])+'</button>';}).join('')+'</span><button class="btn small soft" data-act="go-top">고른 것 맨 위로</button><button class="btn small" data-act="go-clr">고르기 풀기</button></div>';}
  b+='<div class="row gorda">""")
sub("마감이 지난 날은 보기만 됩니다.", "≡를 끌어 순서를 바꾸거나 다른 날로 옮깁니다. 동그라미로 여러 개를 고르면 한 번에 옮깁니다. 마감이 지난 날은 보기만 됩니다.")
sub("    case 'go-r':", r"""    case 'go-sel':{S.gsel=S.gsel||{};var gsk=date+'|'+id;if(S.gsel[gsk])delete S.gsel[gsk];else S.gsel[gsk]=1;break;}
    case 'go-clr':S.gsel={};break;
    case 'go-to':{var gti=gselKeys().map(function(s){var i=s.indexOf('|');return [s.slice(0,i),s.slice(i+1)];});gordMove(gti,date,null);break;}
    case 'go-top':{
      var gtk=gselKeys().map(function(s){var i=s.indexOf('|');return [s.slice(0,i),s.slice(i+1)];}),gbyd={};gtk.forEach(function(x){(gbyd[x[0]]=gbyd[x[0]]||[]).push(x);});
      var Vtp=view();Object.keys(gbyd).forEach(function(d){var first=dayOf(Vtp,Vtp.me,d).goals.filter(function(q){return q&&!q.mv;})[0];gordMove(gbyd[d],d,first?first.id:null);});S.gsel={};break;
    }
    case 'go-r':""")
