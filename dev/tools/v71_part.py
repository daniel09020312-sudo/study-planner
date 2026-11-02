# ---------------------------------------------------------------- v71: 할 일 목록은 날짜가 이어지게 옆으로 스크롤(앞뒤 1주씩 더 그려 두고, 멈추면 보이는 첫날 기준으로 다시 맞춤)
sub("  S.alWeek=ws;\n  var h='<div class=\"view\" id=\"view-cal\">", "  S.alWeek=ws;var fv=S.alFirst&&S.alFirst>=addDays(ws,-6)&&S.alFirst<=addDays(ws,13)?S.alFirst:ws,alFrom=addDays(fv,-7);\n  var h='<div class=\"view\" id=\"view-cal\">")
sub("<h1 class=\"wkt\">'+wkTitle(ws)+'</h1>", "<h1 class=\"wkt\" id=\"alTitle\">'+wkTitle(fv)+'</h1>")
sub("if(ws!==cur)h+='<button class=\"btn small\" data-act=\"al-week\" data-d=\"0\"", "if(wkStart(fv)!==cur)h+='<button class=\"btn small\" data-act=\"al-week\" data-d=\"0\"")
sub("for(var i=0;i<7;i++){var d=addDays(ws,i),g=dayOf(V,V.me,d).goals", "for(var i=0;i<7;i++){var d=addDays(fv,i),g=dayOf(V,V.me,d).goals")
sub("h+='<div class=\"vbody'+(S.vbDir?' side':'')+'\" id=\"vb-list-'+ws+'\"", "h+='<div class=\"vbody'+(S.vbDir?' side':'')+'\" id=\"vb-list-'+(S.alKey||ws)+'\"")
sub("h+='<div class=\"wkscroll\" id=\"wkScroll\"><div class=\"wk\">';\n  days.forEach(", "var alDays=[];for(var ai=0;ai<21;ai++)alDays.push(addDays(alFrom,ai));\n  h+='<div class=\"wkscroll alc\" id=\"wkScroll\" data-fv=\"'+fv+'\" data-from=\"'+alFrom+'\"><div class=\"wk\">';\n  alDays.forEach(")
sub("  days.forEach(function(d){h+=wkCell(V,d,t);});", "  alDays.forEach(function(d){h+=wkCell(V,d,t);});")
sub("case 'al-week':{var aw=", "case 'al-week':{S.alFirst=null;S.alKey=null;var aw=")
sub("if(m==='list'){S.alWeek=", "if(m==='list'){S.alFirst=null;S.alKey=null;S.alWeek=")
sub("function after(V){\n  afterChat(V);", r"""/* 이어지는 할 일 목록: 그린 뒤 보이는 첫날로 맞추고, 스크롤이 멈추면 그 날 기준으로 다시 그림 */
function alSync(){
  var sc=document.getElementById('wkScroll');if(!sc||!sc.getAttribute('data-from'))return;
  var fv=sc.getAttribute('data-fv'),k=sc.getAttribute('data-from')+'|'+fv;
  if(sc.__k!==k){var c=document.getElementById('wc-'+fv),w=sc.firstElementChild;if(c&&w){sc.__lock=Date.now();sc.scrollLeft=c.offsetLeft-w.offsetLeft;}sc.__k=k;}
  if(sc.__on)return;sc.__on=1;
  sc.addEventListener('scroll',function(){
    if(Date.now()-(sc.__lock||0)<120)return;
    clearTimeout(sc.__t);sc.__t=setTimeout(function(){
      if(S.drag||S.calMode!=='list')return;
      var from=sc.getAttribute('data-from'),c0=document.getElementById('wc-'+from),w=sc.firstElementChild;if(!c0||!w)return;
      var cw=c0.offsetWidth||1,idx=Math.max(0,Math.min(20,Math.round(sc.scrollLeft/cw))),d=addDays(from,idx);
      if(d===sc.getAttribute('data-fv'))return;
      var tl=document.getElementById('alTitle');if(tl)tl.textContent=wkTitle(d);
      S.alKey=S.alKey||S.alWeek;S.alFirst=d;S.alWeek=wkStart(d);S.vbDir=0;render();
    },180);
  },{passive:true});
}
function after(V){
  afterChat(V);
  try{alSync();}catch(e){}""")
# 처음 열 때: 휴대폰은 오늘부터, 넓은 화면은 월요일부터(예전의 오늘로 스크롤은 쓰지 않음)
sub("S.scrollTo=S.calMode==='list'?{id:'wc-'+today(),inline:'start',quiet:1}:null;", "S.scrollTo=null;S.alFirst=S.calMode==='list'&&innerWidth<700?today():null;")
sub("S.scrollTo={id:'wc-'+today(),inline:'start',quiet:1};", "S.alFirst=innerWidth<700?today():null;", 2)
