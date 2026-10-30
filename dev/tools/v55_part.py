# ---------------------------------------------------------------- v55: 잉크 선물 게임 (JS는 src/v55.js, CSS는 src/v55.css)
V55_JS = open(BASE + '/src/v55.js', encoding='utf-8').read()
V55_CSS = open(BASE + '/src/v55.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V55_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V55_CSS + "</style>")
# 잉크 계산: 게임 선물은 끝나기 전에는 보낸 사람에게서만 빠지고, 끝나면 받은 만큼만 옮겨진다
sub("Object.keys(g).forEach(function(k){var x=obj(g[k]),n=Math.max(0,Math.floor(+x.n||0));if(x.to===V.me)gi+=n;if(x.from===V.me)go+=n;});",
    "Object.keys(g).forEach(function(k){var x=obj(g[k]),n=Math.max(0,Math.floor(+x.n||0));if(x.g){if(x.st==='done'){var gg=Math.max(0,Math.min(n,Math.floor(+x.got||0)));if(x.to===V.me)gi+=gg;if(x.from===V.me)go+=gg;}else if(x.st!=='back'){if(x.from===V.me)go+=n;}return;}if(x.to===V.me)gi+=n;if(x.from===V.me)go+=n;});")
sub("    if(x.gift)body='<div class=\"bb gift\"'+pick+'><span class=\"gfi\">'+INK_SVG+'<b>잉크 '+(+x.gift||0)+'방울</b> 선물</span>'+(x.text?'<span class=\"gft\">'+esc(x.text)+'</span>':'')+'</div>';",
    "    if(x.gift)body=giftBubble(V,x,pick);")
sub("  if(x.gift)return '잉크 '+(+x.gift||0)+'방울 선물'+(x.text?', '+cut(x.text,14):'');", "  if(x.gift)return (x.gg?'선물 게임 도착: ':'')+'잉크 '+(+x.gift||0)+'방울 선물'+(x.text?', '+cut(x.text,14):'');")
# 선물 창: 주는 방식
sub("  b+='<input type=\"text\" id=\"giftMsg\" data-draft=\"giftMsg\"", "  b+=ggPanel();\n  b+='<input type=\"text\" id=\"giftMsg\" data-draft=\"giftMsg\"")
sub("  var ok=to&&n>0&&(ink.unl||n<=ink.bal)&&n<=99999,cf=S.confirm==='gift';", "  var ok=to&&n>0&&(ink.unl||n<=ink.bal)&&n<=99999&&ggReady(),cf=S.confirm==='gift';")
sub("  return b+'<p class=\"hint\">보낸 잉크는 받는 사람의 잉크가 되고, 1:1 메시지로 알려 줍니다.</p></div>';", "  return b+'<p class=\"hint\">1:1 메시지로 알려 줍니다.</p></div>';")
sub("      save('gifts/'+rid('g'),{from:Vgf.me,to:gto,n:gn,at:gat});\n      save('msgs/'+rid('x'),{from:Vgf.me,to:gto,text:gmsg,gift:gn,at:gat});",
    "      var ggt=S.giftG||'now',gid=rid('g'),gdoc={from:Vgf.me,to:gto,n:gn,at:gat};\n      if(ggt!=='now'){if(!ggReady())break;gdoc.g=ggt;gdoc.st='wait';if(ggt==='box')gdoc.r=ggBoxRoll(gn);if(ggt==='quiz'){gdoc.q=String(S.draft.ggQ||'').trim().slice(0,60);gdoc.h=ggHash(gid,ggNorm(S.draft.ggA));gdoc.tries=0;}if(ggt==='rps')gdoc.h=ggHash(gid,S.ggMove);}\n      save('gifts/'+gid,gdoc);\n      var gm={from:Vgf.me,to:gto,text:gmsg,gift:gn,at:gat};if(ggt!=='now')gm.gg=gid;save('msgs/'+rid('x'),gm);")
sub("S.giftOpen=false;S.giftTo=null;S.draft.giftN='';S.draft.giftMsg='';S.sync=true;\n      flash(", "S.giftOpen=false;S.giftTo=null;S.draft.giftN='';S.draft.giftMsg='';S.giftG='now';S.ggMove='';S.draft.ggQ='';S.draft.ggA='';S.sync=true;\n      flash(")
sub("  if(t==='help')return modalHelp(V);", "  if(t==='help')return modalHelp(V);\n  if(t==='gg')return modalGG(V);")
sub("    case 'notice-x':", r"""    case 'gg-type':{var gv=el.getAttribute('data-v');if(GG_TYPES.some(function(x){return x[0]===gv;}))S.giftG=gv;S.confirm=null;break;}
    case 'gg-rps-pick':S.ggMove=el.getAttribute('data-v');break;
    case 'gg-play':{var Vpl=view(),Gp=obj(Vpl.gifts[id]);if(!Gp.g||Gp.to!==Vpl.me||(Gp.st&&Gp.st!=='wait'))break;S.ggRes=null;S.draft.ggTry='';S.modal={type:'gg',id:id};S.closing=false;break;}
    case 'gg-back':{
      var Vbk=view(),Gb=obj(Vbk.gifts[id]);if(!Gb.g||Gb.from!==Vbk.me||(Gb.st&&Gb.st!=='wait'))break;
      if(prev!=='ggback:'+id){S.confirm='ggback:'+id;break;}
      if(!need())break;var Gbn=clone(Gb);Gbn.st='back';save('gifts/'+id,Gbn);flash('선물을 회수했습니다. 잉크가 돌아왔습니다.');break;
    }
    case 'gg-box':{
      var Vbx=view(),gid2=S.modal&&S.modal.id,Gx=obj(Vbx.gifts[gid2]);if(!Gx.g||Gx.to!==Vbx.me||(Gx.st&&Gx.st!=='wait')||!need())break;
      var rr=Math.max(1,Math.min(+Gx.n||0,Math.round(+Gx.r||1)));ggFinish(Vbx,gid2,rr,rr>=+Gx.n?'대박! 전부 들어 있었습니다.':'상자 속 잉크를 받았습니다.');break;
    }
    case 'gg-ans':{
      var Vq=view(),gid3=S.modal&&S.modal.id,Gq=obj(Vq.gifts[gid3]),ans=ggNorm(S.draft.ggTry);if(!Gq.g||Gq.to!==Vq.me||(Gq.st&&Gq.st!=='wait'))break;
      if(!ans){flash('정답을 적어 주세요.');break;}if(!need())break;
      var tq=+Gq.tries||0;
      if(ggHash(gid3,ans)===Gq.h){ggFinish(Vq,gid3,ggQuizAmt(+Gq.n,tq),tq?'정답입니다!':'한 번에 맞혔습니다!');break;}
      tq++;S.draft.ggTry='';
      if(tq>=3){ggFinish(Vq,gid3,0,'세 번 다 틀렸습니다.');break;}
      var Gqn=clone(Gq);Gqn.tries=tq;save('gifts/'+gid3,Gqn);flash('틀렸습니다. 남은 기회 '+(3-tq)+'번');break;
    }
    case 'gg-rps':{
      var Vr=view(),gid4=S.modal&&S.modal.id,Gr=obj(Vr.gifts[gid4]),mv=el.getAttribute('data-v');if(!Gr.g||Gr.to!==Vr.me||(Gr.st&&Gr.st!=='wait')||!/^[rps]$/.test(mv)||!need())break;
      var sm=['r','p','s'].filter(function(m){return ggHash(gid4,m)===Gr.h;})[0]||'r',beat={r:'s',p:'r',s:'p'},nm={r:'바위',p:'보',s:'가위'},n0=+Gr.n||0;
      var res=mv===sm?'draw':beat[mv]===sm?'win':'lose',amt=res==='win'?n0:res==='draw'?Math.ceil(n0/2):Math.ceil(n0/5);
      ggFinish(Vr,gid4,amt,'상대는 '+nm[sm]+', 나는 '+nm[mv]+'. '+(res==='win'?'이겼습니다!':res==='draw'?'비겼습니다.':'졌습니다.'));break;
    }
    case 'notice-x':""")
