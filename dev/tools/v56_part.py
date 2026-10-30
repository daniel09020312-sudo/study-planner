# ---------------------------------------------------------------- v56: 전체 대화방 잉크 뿌리기(돌림판, 사다리타기) (JS는 src/v56.js, CSS는 src/v56.css)
V56_JS = open(BASE + '/src/v56.js', encoding='utf-8').read()
V56_CSS = open(BASE + '/src/v56.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V56_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V56_CSS + "</style>")
# 잉크 계산: 열려 있는 동안은 보낸 사람에게서 n이 빠지고, 끝나면 당첨자에게 나눠진다
sub("if(x.g){if(x.st==='done'){", "if(x.g==='first'){var fk=Math.max(1,+x.k||1),fe=Math.floor(n/fk),fc=lotClaims(V,k,x);if(fc.indexOf(V.me)>=0)gi+=fe;if(x.from===V.me)go+=(x.st==='back'||fc.length>=fk)?fe*fc.length:n;return;}if(x.g==='wheel'||x.g==='ladder'){var lw=obj(x.win),ls=0;Object.keys(lw).forEach(function(m){ls+=Math.max(0,Math.floor(+lw[m]||0));});ls=Math.min(ls,n);if(x.st==='done'){if(lw[V.me])gi+=Math.max(0,Math.min(n,Math.floor(+lw[V.me]||0)));if(x.from===V.me)go+=ls;}else if(x.st!=='back'){if(x.from===V.me)go+=n;}return;}if(x.g){if(x.st==='done'){")
sub("    if(x.gift)body=giftBubble(V,x,pick);", "    if(x.gift)body=x.lot?lotBubble(V,x,pick):giftBubble(V,x,pick);")
sub("  if(x.gift)return (x.gg?'선물 게임 도착: ':'')", "  if(x.gift&&x.lot)return '잉크 '+(+x.gift||0)+'방울 뿌리기';\n  if(x.gift)return (x.gg?'선물 게임 도착: ':'')")
sub("'+(ed?' hidden':'')+'>이모티콘</button>';", "'+(ed?' hidden':'')+'>이모티콘</button>'+(dm||ed?'':'<button class=\"btn\" id=\"msgLot\" data-act=\"lot-new\">잉크</button>');")
sub("  if(t==='help')return modalHelp(V);", "  if(t==='help')return modalHelp(V);\n  if(t==='lotnew'&&S.lot)return modalLotNew(V,inkOf(V));\n  if(t==='lot')return modalLot(V);")
sub("    case 'notice-x':", r"""    case 'lot-new':{var Vln=view();if(!Vln.me)break;S.lot={g:'first',k:3};S.draft.lotN='';S.draft.lotMsg='';S.modal={type:'lotnew',id:null};S.closing=false;break;}
    case 'lot-set':{if(!S.lot)break;var lk=el.getAttribute('data-k'),lv2=el.getAttribute('data-v');if(lk==='g'&&(lv2==='wheel'||lv2==='ladder'||lv2==='first')){S.lot.g=lv2;S.lot.k=lv2==='first'?3:1;}else if(lk==='k')S.lot.k=Math.max(1,Math.min(10,+lv2||1));break;}
    case 'lot-amt':S.draft.lotN=String(+el.getAttribute('data-v')||'');S.sync=true;break;
    case 'lot-add':{
      var Va=view(),La=S.lot,ln=Math.floor(+S.draft.lotN||0),lk2=inkOf(Va);if(!Va.me||!La||!(ln>0)||ln>99999)break;
      var lkk=La.g==='wheel'?1:La.k;
      if(!lk2.unl&&ln>lk2.bal){flash('잉크가 '+(ln-lk2.bal)+'방울 모자랍니다.');break;}
      if(ln<lkk){flash('받을 사람 수보다 많이 걸어 주세요.');break;}
      var lwho=Va.roster.filter(function(m){return m.id!==Va.me;}).map(function(m){return m.id;});
      if(!lwho.length){flash('방에 다른 사람이 없습니다.');break;}
      if(!need())break;
      var lid=rid('g'),lat=Date.now(),lmsg=String(S.draft.lotMsg||'').trim().slice(0,40),ldoc={from:Va.me,to:'all',n:ln,at:lat,g:La.g,k:lkk};
      if(La.g==='first')ldoc.st='open';
      else{var lseed=Math.floor(Math.random()*4294967295)>>>0;ldoc.who=lwho;ldoc.seed=lseed;ldoc.win=lotResult(ldoc,lwho,lseed);ldoc.st='done';ldoc.done=lat;}
      save('gifts/'+lid,ldoc);
      save('msgs/'+rid('x'),{from:Va.me,to:'all',text:lmsg,gift:ln,lot:lid,at:lat});
      S.lot=null;S.draft.lotN='';S.draft.lotMsg='';
      if(La.g==='first'){closeModal();flash('전체 대화방에 올렸습니다. 먼저 받는 사람부터 가져갑니다.');return;}
      S.modal={type:'lot',id:lid};S.closing=false;break;
    }
    case 'lot-claim':{
      var Vc2=view(),Gc=obj(Vc2.gifts[id]);if(!Vc2.me||Gc.g!=='first'||Gc.st==='back'||Gc.from===Vc2.me||!need())break;
      var cl0=lotClaims(Vc2,id,Gc);if(cl0.indexOf(Vc2.me)>=0)break;
      if(cl0.length>=Math.max(1,+Gc.k||1)){flash('이미 다 가져갔습니다.');break;}
      editProg(function(p){p.lc=obj(p.lc);p.lc[id]=Date.now();});
      var cl1=lotClaims(view(),id,Gc);
      flash(cl1.indexOf(Vc2.me)>=0?'잉크 '+Math.floor((+Gc.n||0)/Math.max(1,+Gc.k||1))+'방울을 받았습니다.':'아깝게 늦었습니다.');break;
    }
    case 'lot-join':{
      var Vj2=view(),Gj=obj(Vj2.gifts[id]);if(!Vj2.me||!Gj.g||Gj.st!=='open'||Gj.from===Vj2.me||!need())break;
      var cur=lotParts(Vj2,id,Gj),injn=cur.indexOf(Vj2.me)>=0;
      if(!injn&&cur.length>=LOT_MAX[Gj.g]){flash('참여 인원이 다 찼습니다.');break;}
      editProg(function(p){p.lj=obj(p.lj);Object.keys(p.lj).forEach(function(k){var g2=obj(Vj2.gifts[k]);if(!g2.g||g2.st!=='open')delete p.lj[k];});if(injn)delete p.lj[id];else p.lj[id]=1;});
      break;
    }
    case 'lot-go':{
      var Vg2=view(),Gg=obj(Vg2.gifts[id]);if(!Vg2.me||!Gg.g||Gg.st!=='open'||(Gg.from!==Vg2.me&&adminId(Vg2)!==Vg2.me))break;
      var who=lotParts(Vg2,id,Gg).slice(0,LOT_MAX[Gg.g]);if(who.length<2){flash('2명 이상 참여해야 시작할 수 있습니다.');break;}
      if(!need())break;
      var seed=Math.floor(Math.random()*4294967295)>>>0,Gn=clone(Gg);Gn.who=who;Gn.seed=seed;Gn.win=lotResult(Gg,who,seed);Gn.st='done';Gn.done=Date.now();
      save('gifts/'+id,Gn);S.modal={type:'lot',id:id};S.closing=false;break;
    }
    case 'lot-view':{var Vv=view(),Gv=obj(Vv.gifts[id]);if(Gv.st==='done'){S.modal={type:'lot',id:id};S.closing=false;}break;}
    case 'lot-back':{
      var Vb2=view(),Gb2=obj(Vb2.gifts[id]);if(!Gb2.g||Gb2.st!=='open'||Gb2.from!==Vb2.me)break;if(Gb2.g==='first'&&lotClaims(Vb2,id,Gb2).length>=Math.max(1,+Gb2.k||1))break;
      if(prev!=='lotback:'+id){S.confirm='lotback:'+id;break;}
      if(!need())break;var Gbn2=clone(Gb2);Gbn2.st='back';save('gifts/'+id,Gbn2);flash('남은 잉크를 거둬들였습니다.');break;
    }
    case 'notice-x':""")
