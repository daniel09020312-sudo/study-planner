# ---------------------------------------------------------------- 시간표와 과목 색
TT_JS = open(BASE + '/src/tt.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", TT_JS + "\n/* ---------- 공부방 ---------- */")

# 상태
sub("S.calMode=(function(m){",
    "S.ttSpan=(function(v){return v===1||v===3||v===7?v:null;})(+lsGet('gbb_ttspan'));S.ttPrevSpan=null;S.ttStart=null;S.ttPick=null;S.ttScrollY=null;S.ttSel=null;S.ttSlot=null;S.ttTab='fixed';S.ttEd=null;S.ttXDur=60;S.ttXK='etc';S.drag=false;\n"
    "S.calMode=(function(m){")
sub("S.calMode=(function(m){return m==='list'||m==='tt'?m:'cal';})(lsGet('gbb_calmode'));",
    "S.calMode=(function(m){return m==='list'||m==='tt'?m:'cal';})(lsGet('gbb_calmode'));if(S.calMode==='tt')S.ttScrollY='auto';")

# 창
sub("  if(t==='compose')return modalCompose(V);",
    "  if(t==='ttset')return modalTTSet(V);\n  if(t==='ttg')return modalTTG(V);\n  if(t==='ttf')return modalTTF(V);\n  if(t==='ttslot')return modalTTSlot(V);\n"
    "  if(t==='compose')return modalCompose(V);")
sub("  if(type==='compose'){S.cmp={date:(el&&el.getAttribute('data-date'))||today(),sid:'',type:'',amt:0,unit:''};",
    "  if(type==='ttset'){S.ttTab=S.ttTab||'fixed';S.ttEd=null;}\n"
    "  if(type==='compose'){var cat=el&&el.getAttribute('data-at');S.cmp={date:(el&&el.getAttribute('data-date'))||today(),sid:'',type:'',amt:0,unit:'',at:cat!=null&&cat!==''?+cat:null};")
sub("      editDay(c.date,function(d){if(d.goals.length>=GMAX){full=true;return;}d.goals.push({id:rid('g'),text:text.slice(0,90),sid:c.sid||'',done:false});});",
    "      editDay(c.date,function(d){if(d.goals.length>=GMAX){full=true;return;}var ng={id:rid('g'),text:text.slice(0,90),sid:c.sid||'',done:false};if(c.at!=null){ng.ts=c.at;ng.te=Math.min(c.at+60,28*60);}d.goals.push(ng);});")
sub("      if(el.getAttribute('data-more')){S.cmp={date:c.date,sid:c.sid,type:'',amt:0,unit:''};break;}",
    "      if(el.getAttribute('data-more')){S.cmp={date:c.date,sid:c.sid,type:'',amt:0,unit:'',at:c.at!=null&&c.at+120<=28*60?c.at+60:null};break;}")

# 동작
sub("    case 'cal-today':", r"""    case 'tt-nav':{
      var tn=+el.getAttribute('data-d')||0,tds=ttDays(),st0=tds[0],sc0=document.getElementById('ttScroll');
      S.ttStart=tn===0?today():addDays(st0,tn*tds.length);S.vbDir=tn===0?(today()>st0?1:-1):tn;S.ttScrollY=tn===0?'auto':(sc0?sc0.scrollTop:'auto');S.ttPick=null;break;
    }
    case 'tt-span':{
      var nv=+el.getAttribute('data-v');if([1,3,7].indexOf(nv)<0)break;
      var sc1=document.getElementById('ttScroll');if(ttDays().indexOf(today())>=0)S.ttStart=today();
      S.ttSpan=nv;S.ttPrevSpan=null;lsSet('gbb_ttspan',String(nv));S.ttScrollY=sc1?sc1.scrollTop:'auto';S.vbDir=0;break;
    }
    case 'tt-day':{
      var tdd=el.getAttribute('data-d'),n1=ttSpan(),sc2=document.getElementById('ttScroll');S.ttScrollY=sc2?sc2.scrollTop:'auto';S.vbDir=0;
      if(n1===1){S.ttSpan=S.ttPrevSpan||(function(v){return v===3||v===7?v:null;})(+lsGet('gbb_ttspan'));S.ttPrevSpan=null;}else{S.ttPrevSpan=n1;S.ttSpan=1;S.ttStart=tdd;}
      break;
    }
    case 'tt-pick':S.ttPick=S.ttPick&&S.ttPick.id===id?null:{d:el.getAttribute('data-d'),id:id};break;
    case 'tt-pick-x':S.ttPick=null;break;
    case 'tt-slot':{
      if(el.classList.contains('ro'))break;
      var sd=el.getAttribute('data-d'),r0s=+el.getAttribute('data-r0'),r1s=+el.getAttribute('data-r1'),hhs=+el.getAttribute('data-hh'),rc=el.getBoundingClientRect(),ms=r0s+((S.pt?S.pt.y:rc.top)-rc.top)*60/hhs;
      ms=Math.max(r0s,Math.min(r1s-60,Math.floor(ms/30)*30));
      if(S.ttPick){var pk=S.ttPick;S.ttPick=null;ttCommit('q',pk.d,pk.id,ms,ms+60,sd);return;}
      S.ttSlot={d:sd,m:ms};S.draft.ttXT='';S.ttXDur=60;S.ttXK='etc';openModal('ttslot',null);return;
    }
    case 'tt-open':{var tk=el.getAttribute('data-k');S.ttSel={k:tk,d:el.getAttribute('data-d'),id:id};S.ttPick=null;openModal(tk==='f'?'ttf':'ttg',null);return;}
    case 'tt-put':{var sl=S.ttSlot;if(!sl)break;closeModal();ttCommit('q',sl.d,id,sl.m,Math.min(sl.m+60,28*60),sl.d);return;}
    case 'tt-xdur':S.ttXDur=+el.getAttribute('data-m')||60;break;
    case 'tt-xk':S.ttXK=el.getAttribute('data-v')==='academy'?'academy':'etc';break;
    case 'tt-xadd':{
      var sl2=S.ttSlot,xt=String(S.draft.ttXT||'').trim();if(!sl2)break;
      if(!xt){flash('일정 이름을 적어 주세요.');break;}
      editTT(function(T){var a=arr(T.x[sl2.d]);a.push({id:rid('x'),k:S.ttXK||'etc',t:xt.slice(0,20),s:sl2.m,e:Math.min(sl2.m+(S.ttXDur||60),28*60)});T.x[sl2.d]=a;});
      S.draft.ttXT='';closeModal();return;
    }
    case 'ttg-dur':{var sg=ttSelGoal();if(!sg)break;var dm=+el.getAttribute('data-m')||60,s0=placed(sg)?+sg.ts:Math.max(ttWin(view()).s,S.ttSel.d===today()?Math.ceil(nowMin()/10)*10:0);editDay(S.ttSel.d,function(d){d.goals.forEach(function(x){if(x.id===sg.id){x.ts=s0;x.te=Math.min(s0+dm,28*60);}});});break;}
    case 'ttg-off':{var sg2=ttSelGoal();if(!sg2)break;var sn5=snap(['days/'+view().me+'_'+S.ttSel.d]);editDay(S.ttSel.d,function(d){d.goals.forEach(function(x){if(x.id===sg2.id){delete x.ts;delete x.te;}});});closeModal();flash('시간표에서 뺐습니다. 할 일은 그대로 있습니다.',sn5);return;}
    case 'ttg-cal':{var sg3=S.ttSel;closeModal();act('al-goal',{getAttribute:function(n){return n==='data-d'?sg3.d:n==='data-id'?sg3.id:null;}});return;}
    case 'ttf-off':{
      var fb=ttSelFixed();if(!fb)break;var sn6=snap(['progress/'+view().me]),fd0=S.ttSel.d;
      editTT(function(T){if(fb.one)T.x[fd0]=arr(T.x[fd0]).filter(function(x){return x.id!==fb.id;});else{var o=obj(T.ov[fd0]);o[fb.id]={off:1};T.ov[fd0]=o;}});
      closeModal();flash(fb.one?'일정을 지웠습니다.':jos(fb.t||TTK[fb.k],'을','를')+' 이 날만 뺐습니다.',sn6);return;
    }
    case 'ttf-reset':{var fb2=ttSelFixed();if(!fb2)break;var fd1=S.ttSel.d;editTT(function(T){var o=obj(T.ov[fd1]);delete o[fb2.id];T.ov[fd1]=o;});break;}
    case 'ttf-edit':{var fb3=ttSelFixed();if(!fb3)break;S.ttTab='fixed';S.ttEd=ttEdFrom(view(),fb3.id);S.modal={type:'ttset'};S.closing=false;S.sync=true;break;}
    case 'tt-restore':{var rd=el.getAttribute('data-d');editTT(function(T){var o=obj(T.ov[rd]);Object.keys(o).forEach(function(k){if(o[k]&&o[k].off)delete o[k];});T.ov[rd]=o;});break;}
    case 'tt-tab':S.ttTab=el.getAttribute('data-v')||'fixed';S.ttEd=null;break;
    case 'tt-new':{
      var nk=el.getAttribute('data-v');nk=TTK[nk]?nk:'etc';
      S.ttEd={id:null,k:nk,sid:'',d:nk==='school'?'0111110':'0000000',s:nk==='school'?500:nk==='academy'?1080:1140,e:nk==='school'?990:nk==='academy'?1260:1200};
      S.draft.ttEdT=nk==='school'?'학교':nk==='academy'?'학원':'';S.sync=true;break;
    }
    case 'tt-ed':S.ttEd=ttEdFrom(view(),id);S.sync=true;break;
    case 'tt-ed-set':{if(!S.ttEd)break;var ek=el.getAttribute('data-k'),ev=el.getAttribute('data-v');if(ek==='k'){var oldK=S.ttEd.k;S.ttEd.k=TTK[ev]?ev:'etc';var dt0=String(S.draft.ttEdT||'').trim();if(!dt0||dt0===TTK[oldK]){S.draft.ttEdT=S.ttEd.k==='etc'?'':TTK[S.ttEd.k];S.sync=true;}}else if(ek==='sid')S.ttEd.sid=S.ttEd.sid===ev?'':ev;break;}
    case 'tt-ed-dow':{if(!S.ttEd)break;var di=+el.getAttribute('data-v'),ds=S.ttEd.d.split('');ds[di]=ds[di]==='1'?'0':'1';S.ttEd.d=ds.join('');break;}
    case 'tt-ed-x':S.ttEd=null;break;
    case 'tt-ed-save':{
      var E=S.ttEd;if(!E)break;var et=String(S.draft.ttEdT||'').trim()||TTK[E.k];
      if(E.d.indexOf('1')<0){flash('요일을 하나 이상 골라 주세요.');break;}
      if(!(E.e>E.s)){flash('끝나는 시간이 시작보다 늦어야 합니다.');break;}
      editTT(function(T){var nb={id:E.id||rid('b'),k:E.k,t:et.slice(0,20),sid:E.sid||'',d:E.d,s:E.s,e:E.e},f=false;T.b=T.b.map(function(x){if(x.id===nb.id){f=true;return nb;}return x;});if(!f)T.b.push(nb);});
      if(canWrite()){S.ttEd=null;flash(jos(et,'을','를')+' 저장했습니다.');}break;
    }
    case 'tt-ed-del':{
      var E2=S.ttEd;if(!E2||!E2.id)break;if(prev!=='ttdel:'+E2.id){S.confirm='ttdel:'+E2.id;break;}
      editTT(function(T){T.b=T.b.filter(function(x){return x.id!==E2.id;});Object.keys(T.ov).forEach(function(d){var o=obj(T.ov[d]);delete o[E2.id];T.ov[d]=o;});});
      S.ttEd=null;break;
    }
    case 'scol':{var sv=el.getAttribute('data-v');editProg(function(p){var c=obj(p.scol);c[id]=sv;p.scol=c;});break;}
    case 'tt-fill':ttFill();break;
    case 'cal-today':""")

# 입력칸 바뀜
sub("  else if(kind==='g-copy'){",
    r"""  else if(kind==='tt-ed-time'){if(S.ttEd){var me0=parseHM(v);if(me0!=null)S.ttEd[el.getAttribute('data-k')==='e'?'e':'s']=me0;}}
  else if(kind==='ttg-time'){
    var gq=ttSelGoal(),mq=parseHM(v);
    if(gq&&mq!=null){var isE=el.getAttribute('data-k')==='e',on=placed(gq),s1=on?+gq.ts:mq,e1=on?+gq.te:mq+60;if(isE){e1=mq;if(!on)s1=mq-60;}else{e1=mq+(e1-s1);s1=mq;}
      if(e1>s1)editDay(S.ttSel.d,function(d){d.goals.forEach(function(x){if(x.id===gq.id){x.ts=s1;x.te=Math.min(e1,28*60);}});});else flash('끝나는 시간이 시작보다 늦어야 합니다.');}
  }
  else if(kind==='ttf-time'){
    var fq=ttSelFixed(),mf=parseHM(v);
    if(fq&&mf!=null){var isE2=el.getAttribute('data-k')==='e',s2=fq.s,e2=fq.e;if(isE2)e2=mf;else{e2=mf+(e2-s2);s2=mf;}
      if(e2>s2){var fd2=S.ttSel.d;editTT(function(T){if(fq.one)T.x[fd2]=arr(T.x[fd2]).map(function(x){return x.id===fq.id?Object.assign({},x,{s:s2,e:e2}):x;});else{var o=obj(T.ov[fd2]);o[fq.id]={s:s2,e:e2};T.ov[fd2]=o;}});}
      else flash('끝나는 시간이 시작보다 늦어야 합니다.');}
  }
  else if(kind==='tt-win'){var mw=parseHM(v);if(mw!=null)editTT(function(T){T.win=obj(T.win);T.win[el.getAttribute('data-k')==='e'?'e':'s']=mw;});}
  else if(kind==='g-copy'){""")

# 그리기: 끄는 동안은 멈추고, 시간표 스크롤 맞추기
sub("function render(){\n  var V=view();V0=V;", "function render(){\n  if(S.drag){S.dragDirty=true;return;}\n  var V=view();V0=V;")
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);",
    "  if(S.ttScrollY!=null){var tsc=document.getElementById('ttScroll');if(tsc){var tv=S.ttScrollY;S.ttScrollY=null;tsc.scrollTop=tv==='auto'?(+tsc.getAttribute('data-auto')||0):tv;}}\n"
    "  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);")
sub("  S.tab=nt;\n  if(reduced)", "  S.tab=nt;S.vbDir=0;if(nt==='cal'&&S.calMode==='tt')S.ttScrollY='auto';\n  if(reduced)")

# 끈 직후의 클릭은 무시
sub("document.addEventListener('click',function(e){\n  var el=e.target.closest?e.target.closest('[data-act]'):null;",
    "document.addEventListener('click',function(e){\n  if(Date.now()-(window.__ttDragEnd||0)<400){e.preventDefault();return;}\n  var el=e.target.closest?e.target.closest('[data-act]'):null;")
# 키보드: Esc로 놓기 취소, 블록에서 Enter
sub("  if(e.key==='Escape'&&S.modal&&!S.check&&!S.missed){closeModal();return;}",
    "  if(e.key==='Escape'&&!S.modal&&S.ttPick){S.ttPick=null;render();return;}\n"
    "  if((e.key==='Enter'||e.key===' ')&&!S.modal&&e.target&&e.target.classList&&e.target.classList.contains('ttb')){e.preventDefault();act('tt-open',e.target);return;}\n"
    "  if(e.key==='Escape'&&S.modal&&!S.check&&!S.missed){closeModal();return;}")

# 달력의 할 일 줄에도 과목 색과 시간
sub("'<div class=\"gt\">'+(sub&&S.gGroup!=='sub'?'<em class=\"tag\">'+esc(sub)+'</em>':'')+'<span>'+esc(x.text)+'</span>'",
    "'<div class=\"gt\">'+(sub&&S.gGroup!=='sub'?subTag(V,x):'')+'<span>'+esc(x.text)+'</span>'+(placed(x)?'<em class=\"tag\">'+fmtHM(x.ts)+'</em>':'')")
# 다른 날로 옮기면 시간은 비운다
sub("  editDay(to,function(d){var c=clone(g);c.done=false;d.goals.push(c);});",
    "  editDay(to,function(d){var c=clone(g);c.done=false;delete c.ts;delete c.te;d.goals.push(c);});")
