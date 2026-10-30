# ---------------------------------------------------------------- v56: 전체 대화방 잉크 뿌리기(돌림판, 사다리타기) (JS는 src/v56.js, CSS는 src/v56.css)
V56_JS = open(BASE + '/src/v56.js', encoding='utf-8').read()
V56_CSS = open(BASE + '/src/v56.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V56_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V56_CSS + "</style>")
# 잉크 계산: 열려 있는 동안은 보낸 사람에게서 n이 빠지고, 끝나면 당첨자에게 나눠진다
sub("if(x.g){if(x.st==='done'){", "if(x.g==='wheel'||x.g==='ladder'){var lw=obj(x.win),ls=0;Object.keys(lw).forEach(function(m){ls+=Math.max(0,Math.floor(+lw[m]||0));});ls=Math.min(ls,n);if(x.st==='done'){if(lw[V.me])gi+=Math.max(0,Math.min(n,Math.floor(+lw[V.me]||0)));if(x.from===V.me)go+=ls;}else if(x.st!=='back'){if(x.from===V.me)go+=n;}return;}if(x.g){if(x.st==='done'){")
sub("    if(x.gift)body=giftBubble(V,x,pick);", "    if(x.gift)body=x.lot?lotBubble(V,x,pick):giftBubble(V,x,pick);")
sub("  if(x.gift)return (x.gg?'선물 게임 도착: ':'')", "  if(x.gift&&x.lot)return '잉크 '+(+x.gift||0)+'방울 뿌리기';\n  if(x.gift)return (x.gg?'선물 게임 도착: ':'')")
sub("'+(ed?' hidden':'')+'>이모티콘</button>';", "'+(ed?' hidden':'')+'>이모티콘</button>'+(dm||ed?'':'<button class=\"btn\" id=\"msgLot\" data-act=\"lot-new\">잉크</button>');")
sub("  if(t==='help')return modalHelp(V);", "  if(t==='help')return modalHelp(V);\n  if(t==='lotnew'&&S.lot)return modalLotNew(V,inkOf(V));\n  if(t==='lot')return modalLot(V);")
sub("    case 'notice-x':", r"""    case 'lot-new':{var Vln=view();if(!Vln.me)break;S.lot={g:'wheel',k:1};S.draft.lotN='';S.draft.lotMsg='';S.modal={type:'lotnew',id:null};S.closing=false;break;}
    case 'lot-set':{if(!S.lot)break;var lk=el.getAttribute('data-k'),lv2=el.getAttribute('data-v');if(lk==='g'&&(lv2==='wheel'||lv2==='ladder'))S.lot.g=lv2;else if(lk==='k')S.lot.k=Math.max(1,Math.min(3,+lv2||1));break;}
    case 'lot-amt':S.draft.lotN=String(+el.getAttribute('data-v')||'');S.sync=true;break;
    case 'lot-add':{
      var Va=view(),La=S.lot,ln=Math.floor(+S.draft.lotN||0),lk2=inkOf(Va);if(!Va.me||!La||!(ln>0)||ln>99999)break;
      if(!lk2.unl&&ln>lk2.bal){flash('잉크가 '+(ln-lk2.bal)+'방울 모자랍니다.');break;}
      if(La.g==='ladder'&&ln<La.k){flash('당첨 인원보다 많이 걸어 주세요.');break;}
      if(!need())break;
      var lid=rid('g'),lat=Date.now(),lmsg=String(S.draft.lotMsg||'').trim().slice(0,40);
      save('gifts/'+lid,{from:Va.me,to:'all',n:ln,at:lat,g:La.g,k:La.g==='ladder'?La.k:1,st:'open'});
      save('msgs/'+rid('x'),{from:Va.me,to:'all',text:lmsg,gift:ln,lot:lid,at:lat});
      S.lot=null;S.draft.lotN='';S.draft.lotMsg='';closeModal();flash('전체 대화방에 올렸습니다. 참여가 모이면 시작하세요.');return;
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
      var Vb2=view(),Gb2=obj(Vb2.gifts[id]);if(!Gb2.g||Gb2.st!=='open'||Gb2.from!==Vb2.me)break;
      if(prev!=='lotback:'+id){S.confirm='lotback:'+id;break;}
      if(!need())break;var Gbn2=clone(Gb2);Gbn2.st='back';save('gifts/'+id,Gbn2);flash('취소했습니다. 잉크가 돌아왔습니다.');break;
    }
    case 'notice-x':""")
