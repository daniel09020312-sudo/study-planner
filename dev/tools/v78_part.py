# ---------------------------------------------------------------- v78: 잉크 뿌리기 방식 늘리기(행운 봉투·퀴즈·마감 추첨·모여라·오늘의 공부왕), 결과는 각자 열어 볼 때까지 숨김 (src/v78.js, v78.css)
V78_JS = open(BASE + '/src/v78.js', encoding='utf-8').read()
V78_CSS = open(BASE + '/src/v78.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V78_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V78_CSS + "</style>")
sub("try{certMig();}catch(e){}", "try{certMig();}catch(e){}\n  try{lotTick();}catch(e){}")
# 잉크 계산: 새 방식은 lotWin으로(확정 전에는 보낸 사람에게서 n이 빠져 있고, 확정되면 받은 몫만)
sub("if(x.g==='first'){var fk=", "if(LOT2[x.g]&&x.to==='all'){var lr2=lotWin(V,k,x);if(lr2.win[V.me])gi+=Math.max(0,Math.floor(+lr2.win[V.me]||0));if(x.from===V.me)go+=lr2.settled?Math.min(n,lr2.sum):n;return;}if(x.g==='first'){var fk=")
sub("    case 'lot-new':", r"""    case 'lot-set2':{if(!S.lot)break;var l2k=el.getAttribute('data-k'),l2v=el.getAttribute('data-v');
      if(l2k==='g'){S.lot.g=l2v;S.lot.k=l2v==='first'||l2v==='rand'?3:1;if(S.lot.dl==null)S.lot.dl=30;}
      else if(l2k==='k')S.lot.k=Math.max(1,Math.min(10,+l2v||1));else if(l2k==='dl')S.lot.dl=+l2v||30;break;}
    case 'lot-add2':{
      var Vq=view(),Lq=S.lot,qn=Math.floor(+S.draft.lotN||0),qink=inkOf(Vq);if(!Vq.me||!Lq||!(qn>0)||qn>99999)break;
      var qg=Lq.g,qk=qg==='wheel'||qg==='pot'||qg==='best'?1:Math.max(1,Lq.k||1);
      if(!qink.unl&&qn>qink.bal){flash('잉크가 '+(qn-qink.bal)+'방울 모자랍니다.');break;}
      if(qn<qk){flash('받을 사람 수보다 많이 걸어 주세요.');break;}
      var qwho=Vq.roster.filter(function(m){return m.id!==Vq.me;}).map(function(m){return m.id;});
      if(!qwho.length){flash('방에 다른 사람이 없습니다.');break;}
      var qq=String(S.draft.lotQ||'').trim().slice(0,60),qa=lotNorm(S.draft.lotA);
      if(qg==='quiz'&&(!qq||!qa)){flash('문제와 정답을 적어 주세요.');break;}
      if(!need())break;
      var qid=rid('g'),qat=Date.now(),qmsg=String(S.draft.lotMsg||'').trim().slice(0,40),qseed=Math.floor(Math.random()*4294967295)>>>0,qdoc={from:Vq.me,to:'all',n:qn,at:qat,g:qg,k:qk};
      if(qg==='wheel'||qg==='ladder'){qdoc.who=qwho;qdoc.seed=qseed;qdoc.win=lotResult(qdoc,qwho,qseed);qdoc.st='done';qdoc.done=qat;}
      else{qdoc.st='open';
        if(qg==='rand')qdoc.amts=lotRandAmts(qn,qk,qseed);
        if(qg==='quiz'){qdoc.q=qq;qdoc.h=ggHash(qid,qa);}
        if(qg==='draw')qdoc.seed=qseed;
        if(qg==='draw'||qg==='pot'||qg==='best'){var qdl=Lq.dl==null?30:Lq.dl,qe=new Date();if(qdl<0){qe.setHours(23,0,0,0);if(qe.getTime()<=qat+60000)qe=new Date(qat+3600000);}else qe=new Date(qat+qdl*60000);qdoc.end=qe.getTime();if(qg==='best')qdoc.day=today();}
      }
      save('gifts/'+qid,qdoc);
      save('msgs/'+rid('x'),{from:Vq.me,to:'all',text:qmsg,gift:qn,lot:qid,at:qat});
      S.lot=null;S.draft.lotN='';S.draft.lotMsg='';S.draft.lotQ='';S.draft.lotA='';closeModal();
      flash('전체 대화방에 올렸습니다.'+(qg==='wheel'||qg==='ladder'?' 결과는 대화방에서 열어 볼 수 있습니다.':''));return;
    }
    case 'lot-open':{var Vo=view(),Go=obj(Vo.gifts[id]);lotSeeMark(id);S.modal={type:'lot',id:id};S.closing=false;break;}
    case 'lot-env':{
      var Ve=view(),Ge=obj(Ve.gifts[id]);if(!Ve.me||Ge.g!=='rand'||Ge.st==='back'||Ge.from===Ve.me||!need())break;
      var ce=lotClaimsBy(Ve,id,Ge,'lc');if(ce.indexOf(Ve.me)>=0)break;if(ce.length>=Math.max(1,+Ge.k||1)){flash('봉투가 다 열렸습니다.');break;}
      editProg(function(p){p.lc=obj(p.lc);p.lc[id]=Date.now();});
      var ce2=lotClaimsBy(view(),id,Ge,'lc'),mi=ce2.indexOf(Ve.me);
      flash(mi>=0?'봉투를 열었더니 '+(+arr(Ge.amts)[mi]||0)+'방울!':'아깝게 늦었습니다.');break;
    }
    case 'lot-ans':{
      var Vqa=view(),Gqa=obj(Vqa.gifts[id]);if(!Vqa.me||Gqa.g!=='quiz'||Gqa.st==='back'||Gqa.from===Vqa.me)break;
      S.lqTry=S.lqTry||{};if((+S.lqTry[id]||0)>=3)break;
      var aEl=document.querySelector('[data-draft="lq:'+id+'"]'),av0=lotNorm((aEl&&aEl.value)||S.draft['lq:'+id]);if(!av0)break;
      if(lotClaimsBy(Vqa,id,Gqa,'lq').length>=Math.max(1,+Gqa.k||1)){flash('이미 정답자가 다 나왔습니다.');break;}
      S.draft['lq:'+id]='';
      if(ggHash(id,av0)!==Gqa.h){S.lqTry[id]=(+S.lqTry[id]||0)+1;flash('틀렸습니다.'+(S.lqTry[id]<3?' '+(3-S.lqTry[id])+'번 남았습니다.':''));break;}
      if(!need())break;editProg(function(p){p.lq=obj(p.lq);p.lq[id]=Date.now();});
      flash(lotClaimsBy(view(),id,Gqa,'lq').indexOf(Vqa.me)>=0?'정답! 잉크 '+Math.floor((+Gqa.n||0)/Math.max(1,+Gqa.k||1))+'방울을 받았습니다.':'정답이지만 아깝게 늦었습니다.');break;
    }
    case 'lot-join2':{
      var Vj3=view(),Gj3=obj(Vj3.gifts[id]);if(!Vj3.me||(Gj3.g!=='draw'&&Gj3.g!=='pot')||Gj3.st==='back'||Gj3.from===Vj3.me||Date.now()>=(+Gj3.end||0)||!need())break;
      var inj3=+obj(obj(Vj3.progress[Vj3.me]).lj)[id]>0;
      editProg(function(p){p.lj=obj(p.lj);if(inj3)delete p.lj[id];else p.lj[id]=Date.now();});
      flash(inj3?'참여를 취소했습니다.':'참여했습니다. 결과는 마감 뒤에 열어 볼 수 있습니다.');break;
    }
    case 'lot-new':""")
# 거두기: 새 방식도(확정 전, 받은 몫은 그대로)
sub("var Vb2=view(),Gb2=obj(Vb2.gifts[id]);if(!Gb2.g||Gb2.st!=='open'||Gb2.from!==Vb2.me)break;", "var Vb2=view(),Gb2=obj(Vb2.gifts[id]);if(!Gb2.g||Gb2.st!=='open'||Gb2.from!==Vb2.me)break;if(LOT2[Gb2.g]&&Gb2.to==='all'&&lotWin(Vb2,id,Gb2).settled)break;")
