# ---------------------------------------------------------------- v31: 시간 고칠 때 시작과 끝을 따로
# 시작을 바꿔도 끝은 그대로 둔다(예전에는 길이를 지키려고 끝도 같이 밀었음). 할 일 시간, 그 날 고정 일정, 학교 교시 시간.
# 끝이 시작보다 이르거나 한쪽이 비어 있으면 저장하지 않고, 적은 값을 그대로 보여 주며 안내만 한다(되돌리지 않음).

sub("function ttTimeRow(kind,s,e,dis){", r"""/* 고치는 중인 시간(아직 저장 안 됨): {key,s,e} */
function ttPendSet(key,cur,k,m){
  var p=Object.assign({},S.ttPend&&S.ttPend.key===key?S.ttPend:{key:key,s:cur.s,e:cur.e});p[k]=m;
  if(p.s!=null&&p.e!=null&&p.e>p.s){S.ttPend=null;return p;}
  S.ttPend=p;return null;
}
function ttPendOf(key){return S.ttPend&&S.ttPend.key===key?S.ttPend:null;}
function ttPendHint(tp,dur){
  if(!tp)return '';
  return '<p class="hint ttpend" role="status">'+(tp.s==null||tp.e==null?(dur?'나머지 시간도 넣거나 아래에서 길이를 고르면 저장됩니다.':'나머지 시간도 넣으면 저장됩니다.'):'끝 시간이 시작보다 늦어야 저장됩니다. 끝 시간도 고쳐 주세요.')+'</p>';
}
function ttTimeRow(kind,s,e,dis,pk){
  var tp=pk?ttPendOf(pk):null;if(tp){s=tp.s;e=tp.e;}
  return ttTimeRow0(kind,s,e,dis)+ttPendHint(tp,kind==='ttg-time');
}
function ttTimeRow0(kind,s,e,dis){""")
sub("ttTimeRow('ttg-time',s,e)", "ttTimeRow('ttg-time',s,e,false,'ttg|'+d+'|'+g.id)")
sub("ttTimeRow('ttf-time',x.s,x.e,ro)", "ttTimeRow('ttf-time',x.s,x.e,ro,'ttf|'+d+'|'+x.id)")

sub("""    if(gq&&mq!=null){var isE=el.getAttribute('data-k')==='e',on=placed(gq),s1=on?+gq.ts:mq,e1=on?+gq.te:mq+60;if(isE){e1=mq;if(!on)s1=mq-60;}else{e1=mq+(e1-s1);s1=mq;}
      if(e1>s1)editDay(S.ttSel.d,function(d){d.goals.forEach(function(x){if(x.id===gq.id){x.ts=s1;x.te=Math.min(e1,28*60);}});});else flash('끝나는 시간이 시작보다 늦어야 합니다.');}""",
    """    if(gq&&mq!=null){var on=placed(gq),gr=ttPendSet('ttg|'+S.ttSel.d+'|'+gq.id,{s:on?+gq.ts:null,e:on?+gq.te:null},el.getAttribute('data-k')==='e'?'e':'s',mq);
      if(gr)editDay(S.ttSel.d,function(d){d.goals.forEach(function(x){if(x.id===gq.id){x.ts=gr.s;x.te=Math.min(gr.e,28*60);}});});}""")
sub("""    if(fq&&mf!=null){var isE2=el.getAttribute('data-k')==='e',s2=fq.s,e2=fq.e;if(isE2)e2=mf;else{e2=mf+(e2-s2);s2=mf;}
      if(e2>s2){var fd2=S.ttSel.d;editTT(function(T){if(fq.one)T.x[fd2]=arr(T.x[fd2]).map(function(x){return x.id===fq.id?Object.assign({},x,{s:s2,e:e2}):x;});else{var o=obj(T.ov[fd2]);o[fq.id]={s:s2,e:e2};T.ov[fd2]=o;}});}
      else flash('끝나는 시간이 시작보다 늦어야 합니다.');}""",
    """    if(fq&&mf!=null){var fd2=S.ttSel.d,fr=ttPendSet('ttf|'+fd2+'|'+fq.id,{s:+fq.s,e:+fq.e},el.getAttribute('data-k')==='e'?'e':'s',mf);
      if(fr)editTT(function(T){if(fq.one)T.x[fd2]=arr(T.x[fd2]).map(function(x){return x.id===fq.id?Object.assign({},x,{s:fr.s,e:fr.e}):x;});else{var o=obj(T.ov[fd2]);o[fq.id]={s:fr.s,e:fr.e};T.ov[fd2]=o;}});}""")
# 길이 고르기: 시작만 적어 둔 상태면 그 시작에서
sub("var dm=+el.getAttribute('data-m')||60,s0=placed(sg)?+sg.ts:", "var dm=+el.getAttribute('data-m')||60,sgp=ttPendOf('ttg|'+S.ttSel.d+'|'+sg.id);S.ttPend=null;var s0=sgp&&sgp.s!=null?sgp.s:placed(sg)?+sg.ts:")

# 학교 교시 시간
sub("""  else if(kind==='sch-time'){var smi=parseHM(v),sii=+el.getAttribute('data-i'),skk=el.getAttribute('data-k')==='e'?'e':'s';if(smi!=null)editSch(function(s){var p=s.p[sii];if(!p)return;var np={s:+p.s,e:+p.e};np[skk]=smi;if(np.e>np.s)s.p[sii]=np;else flash('끝나는 시간이 시작보다 늦어야 합니다.');});}""",
    """  else if(kind==='sch-time'){var smi=parseHM(v),sii=+el.getAttribute('data-i'),skk=el.getAttribute('data-k')==='e'?'e':'s',Vst=view(),spp=schOf(Vst,Vst.me).p[sii];
    if(smi!=null&&spp){var str=ttPendSet('sch|'+sii,{s:+spp.s,e:+spp.e},skk,smi);if(str)editSch(function(s){if(s.p[sii])s.p[sii]={s:str.s,e:str.e};});}}""")
sub("""      sch.p.forEach(function(p,i){b+='<div class="schtr"><b>'+(i+1)+'교시</b><div class="ttime"><input type="time" step="300" value="'+fmtHM(p.s)+'" data-chg="sch-time" data-k="s" data-i="'+i+'" aria-label="'+(i+1)+'교시 시작"><span>~</span><input type="time" step="300" value="'+fmtHM(p.e)+'" data-chg="sch-time" data-k="e" data-i="'+i+'" aria-label="'+(i+1)+'교시 끝"></div></div>';});""",
    """      sch.p.forEach(function(p0,i){var stp=ttPendOf('sch|'+i),p=stp||p0;b+='<div class="schtr"><b>'+(i+1)+'교시</b><div class="ttime"><input type="time" step="300" value="'+fmtHM(p.s)+'" data-chg="sch-time" data-k="s" data-i="'+i+'" aria-label="'+(i+1)+'교시 시작"><span>~</span><input type="time" step="300" value="'+fmtHM(p.e)+'" data-chg="sch-time" data-k="e" data-i="'+i+'" aria-label="'+(i+1)+'교시 끝"></div></div>'+ttPendHint(stp,false);});""")

# 창을 열고 닫을 때 고치던 값 비우기
sub("function openModal(type,el){\n  var V=view();", "function openModal(type,el){\n  var V=view();S.ttPend=null;")
sub("function closeModal(){\n  if(!S.modal||S.closing)return;\n", "function closeModal(){\n  if(!S.modal||S.closing)return;\n  S.ttPend=null;\n")

# ---------------------------------------------------------------- 고정 일정(학원 등)에 과목 여러 개
# 저장: sid는 첫 과목(예전 판과 맞춤), 두 개 이상이면 sids='s1,s3'도 같이 둔다
sub("function fixedOn(V,d,all){", r"""function fxSids(b){var a=b&&b.sids?String(b.sids).split(','):[];if(!a.length&&b&&b.sid)a=[b.sid];return a.filter(function(x,i){return x&&a.indexOf(x)===i;});}
function fxSubs(V,b){return fxSids(b).filter(function(s){return !!V.subName[s];});}
function fxGrad(V,ss){if(ss.length<2)return ss.length?subCol(V,ss[0]):'';var n=ss.length;return 'linear-gradient(to bottom,'+ss.map(function(s,i){return subCol(V,s)+' '+(i*100/n).toFixed(1)+'% '+((i+1)*100/n).toFixed(1)+'%';}).join(',')+')';}
function fxNames(V,ss){return ss.map(function(s){return V.subName[s];}).join(', ');}
function fixedOn(V,d,all){""")
sub("sid:b.sid||'',s:o.s!=null", "sid:b.sid||'',sids:b.sids||'',s:o.s!=null")
sub("return {id:b.id,k:TTK[b.k]?b.k:'etc',sid:b.sid||'',d:String(b.d||'0000000'),s:+b.s,e:+b.e};}", "return {id:b.id,k:TTK[b.k]?b.k:'etc',sid:b.sid||'',ss:fxSids(b),d:String(b.d||'0000000'),s:+b.s,e:+b.e};}")
sub("S.ttEd={id:null,k:nk,sid:'',d:", "S.ttEd={id:null,k:nk,sid:'',ss:[],d:")
sub("else if(ek==='sid')S.ttEd.sid=S.ttEd.sid===ev?'':ev;", "else if(ek==='sid'){var ssx=(S.ttEd.ss||[]).slice(),ssi=ssx.indexOf(ev);if(ssi>=0)ssx.splice(ssi,1);else ssx.push(ev);S.ttEd.ss=ssx;S.ttEd.sid=ssx[0]||'';}")
sub("""<h3>과목<small>선택, 고르면 그 과목 색 줄이 붙습니다</small></h3><div class="chips">'+mySubs(V).map(function(s){return '<button class="chip" data-act="tt-ed-set" data-k="sid" data-v="'+esc(s.id)+'" aria-pressed="'+(E.sid===s.id?'true':'false')+'">""",
    """<h3>과목<small>선택, 여러 개 고를 수 있습니다</small></h3><div class="chips">'+mySubs(V).map(function(s){return '<button class="chip" data-act="tt-ed-set" data-k="sid" data-v="'+esc(s.id)+'" aria-pressed="'+((E.ss||[]).indexOf(s.id)>=0?'true':'false')+'">""")
sub("editTT(function(T){var nb={id:E.id||rid('b'),k:E.k,t:et.slice(0,20),sid:E.sid||'',d:E.d,s:E.s,e:E.e},f=false;",
    "var ssv=(E.ss||[]).filter(function(s){return !!view().subName[s];});editTT(function(T){var nb={id:E.id||rid('b'),k:E.k,t:et.slice(0,20),sid:ssv[0]||'',d:E.d,s:E.s,e:E.e},f=false;if(ssv.length>1)nb.sids=ssv.join(',');")
# 시간표 칸: 왼쪽 색 줄을 과목 수만큼 나눠 칠하고, 두 개 이상이면 줄임말도
sub("(b.sid?' hs':'')", "(fxSubs(V,b).length?' hs'+(fxSubs(V,b).length>1?' hsm':''):'')")
sub("(b.sid?';--sc:'+subCol(V,b.sid):'')", "(fxSubs(V,b).length?';--sc:'+subCol(V,fxSubs(V,b)[0])+';--scg:'+fxGrad(V,fxSubs(V,b)):'')")
sub("""'+ps+'<span class="tbt">'+esc(lab)+'</span><small>'+tm+'</small>'""",
    """'+ps+'<span class="tbt">'+esc(lab)+'</span><small>'+tm+'</small>'+(fxSubs(V,b).length>1?'<small class="tbs">'+esc(fxSubs(V,b).map(function(s){return subAbbr(V,s);}).join(' · '))+'</small>':'')""")
sub("""'<div class="ttsum fx k-'+x.k+'"'+(x.sid?' style="--sc:'+subCol(V,x.sid)+'"':'')""",
    """'<div class="ttsum fx k-'+x.k+'"'+(fxSubs(V,x).length?' style="--sc:'+fxGrad(V,fxSubs(V,x))+'"':'')""")
sub("""<small>'+esc(TTK[x.k])+' · '+(x.tpl?""", """<small>'+esc(TTK[x.k])+(fxSubs(V,x).length?' · '+esc(fxNames(V,fxSubs(V,x))):'')+' · '+(x.tpl?""")
sub("""data-act="tt-ed" data-id="'+esc(x.id)+'"'+(x.sid?' style="--sc:'+subCol(V,x.sid)+'"':'')""",
    """data-act="tt-ed" data-id="'+esc(x.id)+'"'+(fxSubs(V,x).length?' style="--sc:'+fxGrad(V,fxSubs(V,x))+'"':'')""")
sub("""fmtHM(x.e)+'</small></span><em>고치기</em>""",
    """fmtHM(x.e)+(fxSubs(V,x).length?' · '+esc(fxNames(V,fxSubs(V,x))):'')+'</small></span><em>고치기</em>""")
# 고치는 중이면 길이 칩은 눌린 표시를 끈다
sub("""data-act="ttg-dur" data-m="'+x[0]+'" aria-pressed="'+(on&&e-s===x[0]?""", """data-act="ttg-dur" data-m="'+x[0]+'" aria-pressed="'+(on&&!ttPendOf('ttg|'+d+'|'+g.id)&&e-s===x[0]?""")
