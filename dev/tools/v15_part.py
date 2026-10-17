# ---------------------------------------------------------------- 학교 시간표, 확인 필요 시간 지우기
SCH_JS = open(BASE + '/src/school.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", SCH_JS + "\n/* ---------- 공부방 ---------- */")

# 상태와 창
sub("S.ttSpan=(function(v){", "S.schWho=null;S.schSel=null;S.schTimes=false;\nS.ttSpan=(function(v){")
sub("  if(t==='ttset')return modalTTSet(V);", "  if(t==='school')return modalSchool(V);\n  if(t==='ttset')return modalTTSet(V);")
sub("  if(type==='ttset'){S.ttTab=S.ttTab||'fixed';S.ttEd=null;}",
    "  if(type==='ttset'){S.ttTab=S.ttTab||'fixed';S.ttEd=null;}\n  if(type==='school'){S.schWho=null;S.schSel=null;S.schTimes=false;S.draft.schT='';}")

# 동작
sub("    case 'cal-today':", r"""    case 'sch-who':S.schWho=id;S.schSel=null;break;
    case 'sch-sel':{var sd0=+el.getAttribute('data-d'),si0=+el.getAttribute('data-i');S.schSel=S.schSel&&S.schSel.d===sd0&&S.schSel.i===si0?null:{d:sd0,i:si0};break;}
    case 'sch-put':case 'sch-text':{
      var ssel=S.schSel;if(!ssel)break;var sval=null;
      if(name==='sch-text'){var stx=String(S.draft.schT||'').trim().slice(0,12);if(!stx)break;sval={t:stx};S.draft.schT='';S.sync=true;}
      else{var sv0=el.getAttribute('data-v'),st0=el.getAttribute('data-t');sval=sv0?{s:sv0}:st0?{t:st0}:null;}
      if(!sval)break;
      editSch(function(s){var w=obj(s.w[ssel.d]);w['p'+ssel.i]=sval;s.w[ssel.d]=w;});
      if(canWrite()){var snp=schOf(view(),view().me).p.length;S.schSel=ssel.i+1<snp?{d:ssel.d,i:ssel.i+1}:null;}
      break;
    }
    case 'sch-clear':{var ssel2=S.schSel;if(!ssel2)break;editSch(function(s){var w=obj(s.w[ssel2.d]);delete w['p'+ssel2.i];s.w[ssel2.d]=w;});break;}
    case 'sch-times':S.schTimes=!S.schTimes;break;
    case 'sch-padd':editSch(function(s){var l=s.p[s.p.length-1]||{e:480};if(s.p.length<10)s.p.push({s:l.e+10,e:l.e+60});});break;
    case 'sch-pdel':editSch(function(s){if(s.p.length>1)s.p.pop();});break;
    case 'sch-fit':{
      var Vsf=view(),sp0=schOf(Vsf,Vsf.me).p,fs0=sp0[0].s,fe0=sp0[sp0.length-1].e,had0=false;
      editTT(function(T){T.b.forEach(function(b){if(b.k==='school'){b.s=fs0;b.e=fe0;had0=true;}});if(!had0)T.b.push({id:rid('b'),k:'school',t:'학교',sid:'',d:'0111110',s:fs0,e:fe0});});
      if(canWrite())flash('고정 시간표의 학교를 '+fmtHM(fs0)+'~'+fmtHM(fe0)+'에 맞췄습니다.');break;
    }
    case 'sch-copy':{
      var Vsc=view();if(!Vsc.byId[id])break;
      if(prev!=='schcopy:'+id){S.confirm='schcopy:'+id;break;}
      var ssrc=obj(obj(obj(Vsc.progress[id]).tt).sch);if(!Object.keys(ssrc).length)break;
      editTT(function(T){T.sch=clone(ssrc);});
      if(canWrite()){S.schWho=null;flash(Vsc.byId[id].name+' 님의 학교 시간표를 가져왔습니다.');}break;
    }
    case 'flag-cut':{
      var Vf=view(),fl0=obj(Vf.flags[id]);if(!Vf.me||!fl0.mid||(fl0.mid!==Vf.me&&adminId(Vf)!==Vf.me))break;
      if(prev!=='fcut:'+id){S.confirm='fcut:'+id;break;}
      if(!need())break;
      var fpl=flagPlan(Vf,fl0),fpaths=Object.keys(fpl.d).map(function(d){return 'days/'+fl0.mid+'_'+d;}).concat(['flags/'+id]),fsn=snap(fpaths);
      Object.keys(fpl.d).forEach(function(d){editDayOf(fl0.mid,d,function(dd){var v=(+dd.mins[fl0.sid]||0)-fpl.d[d];if(v>0)dd.mins[fl0.sid]=v;else delete dd.mins[fl0.sid];});});
      save('flags/'+id,Object.assign({},fl0,{cut:Date.now(),by:Vf.me,cutMins:fpl.total}));
      flash(fpl.total?((fl0.mid===Vf.me?'내':Vf.byId[fl0.mid].name+' 님의')+' 공부 시간 '+fmtMins(fpl.total)+'과 그만큼의 점수를 지웠습니다.'):'확인 필요 표시를 지웠습니다.',fsn);
      break;
    }
    case 'cal-today':""")
sub("  else if(kind==='g-copy'){",
    "  else if(kind==='sch-time'){var smi=parseHM(v),sii=+el.getAttribute('data-i'),skk=el.getAttribute('data-k')==='e'?'e':'s';if(smi!=null)editSch(function(s){var p=s.p[sii];if(!p)return;var np={s:+p.s,e:+p.e};np[skk]=smi;if(np.e>np.s)s.p[sii]=np;else flash('끝나는 시간이 시작보다 늦어야 합니다.');});}\n"
    "  else if(kind==='g-copy'){")

# 확인 필요: 날짜별로 어디에 몇 분이 들어갔는지 기록해 두고, 지울 수 있게
sub("  if(mins>0){editDay(today(),function(d){d.mins[L.sid]=Math.min(1200,(+d.mins[L.sid]||0)+mins);});cm+=mins;}",
    "  if(mins>0){editDay(today(),function(d){d.mins[L.sid]=Math.min(1200,(+d.mins[L.sid]||0)+mins);});cm+=mins;var td0=today();n.cd=obj(n.cd);n.cd[td0]=(+n.cd[td0]||0)+mins;}")
sub("  flushLive(L,now);S.myPh=null;\n  save('live/'+V.me,{sid:L.sid,mode:'pomo',f:L.f,b:L.b,start:now,flushed:now,cm:0,run:runStart(L),n0:o.n});",
    "  var fl1=flushLive(L,now);S.myPh=null;\n  save('live/'+V.me,{sid:L.sid,mode:'pomo',f:L.f,b:L.b,start:now,flushed:now,cm:0,run:runStart(L),n0:o.n,cd:obj(fl1.cd)});")
sub("  if(why.length&&canWrite())save('flags/'+rid('f'),{mid:V.me,sid:L.sid,start:st,end:end,why:why});",
    "  if(!why.length||!canWrite())return;\n"
    "  var cd=clone(obj(L.cd)),pend=Math.floor(lv(L,Date.now()).focus/60000)-credited(L),td1=today();if(pend>0)cd[td1]=(+cd[td1]||0)+pend;\n"
    "  save('flags/'+rid('f'),{mid:V.me,sid:L.sid,start:st,end:end,why:why,cd:cd});")
sub("return f.mid&&V.byId[f.mid]&&+f.end>lim&&+f.start>0;", "return f.mid&&V.byId[f.mid]&&+f.end>lim&&+f.start>0&&!f.cut;")
sub("<p class=\"hint\">켜놓기만 했을 수 있는 타이머 기록입니다. 점수는 그대로이고 모두에게 보이기만 합니다.</p>",
    "<p class=\"hint\">켜놓기만 했을 수 있는 타이머 기록입니다. 본인이나 방장은 이 시간과 그만큼의 점수를 지울 수 있습니다.</p>")
sub("fmtMins(Math.round((+f.end-+f.start)/60000))+'</small></div></div>';",
    "fmtMins(Math.round((+f.end-+f.start)/60000))+'</small>'+flagAct(V,f)+'</div></div>';")
sub("function flagTags(f){",
    "function flagAct(V,f){\n"
    "  if(!V.me||(f.mid!==V.me&&adminId(V)!==V.me))return '';\n"
    "  var pl=flagPlan(V,f),c=S.confirm==='fcut:'+f.id;\n"
    "  return '<div class=\"flact\"><button class=\"btn small'+(c?' warn':'')+'\" data-act=\"flag-cut\" data-id=\"'+esc(f.id)+'\">'+(pl.total?(c?'한 번 더 누르면 '+fmtMins(pl.total)+' 지움':'이 시간과 점수 지우기 ('+fmtMins(pl.total)+')'):(c?'한 번 더 누르면 표시 지움':'표시 지우기'))+'</button></div>';\n"
    "}\n"
    "function flagTags(f){")
