# ---------------------------------------------------------------- v28: 학교 시간표(선생님, 장소, 연달아 있는 수업), 수업 알림, 할 일 상세 편집
# 학교 시간표와 수업 알림 함수는 src/school.js (v15에서 넣음)

# 1) 과목을 고르면 그 칸에 머문다(선생님, 장소를 적을 수 있게). 같은 과목에 쓴 선생님/장소가 하나뿐이면 채워 준다
sub("""      editSch(function(s){var w=obj(s.w[ssel.d]);w['p'+ssel.i]=sval;s.w[ssel.d]=w;});
      if(canWrite()){var snp=schOf(view(),view().me).p.length;S.schSel=ssel.i+1<snp?{d:ssel.d,i:ssel.i+1}:null;}
      break;""", """      var Vsp=view(),schp=schOf(Vsp,Vsp.me),sold=schCell(Vsp,schp,ssel.d,ssel.i),snk=sval.s?'s:'+sval.s:'t:'+sval.t;
      if(sold&&sold.key===snk){sval.tc=sold.tc;sval.r=sold.r;}
      else{var scb=schCombos(Vsp,schp,snk);if(scb.length===1){sval.tc=scb[0].tc;sval.r=scb[0].r;}}
      if(!sval.tc)delete sval.tc;if(!sval.r)delete sval.r;
      editSch(function(s){var w=obj(s.w[ssel.d]);w['p'+ssel.i]=sval;s.w[ssel.d]=w;});
      schDraftSet(ssel,sval.tc,sval.r);
      break;""")
sub("    case 'sch-clear':", r"""    case 'sch-next':{
      var snx=S.schSel;if(!snx)break;schMetaFromInputs(snx);
      var snn=schOf(view(),view().me).p.length;S.schSel=snx.i+1<snn?{d:snx.d,i:snx.i+1}:null;break;
    }
    case 'sch-combo':{
      var scs=S.schSel;if(!scs)break;var Vcb=view(),ccur=schCell(Vcb,schOf(Vcb,Vcb.me),scs.d,scs.i);if(!ccur)break;
      var ctc=String(el.getAttribute('data-tc')||''),cr=String(el.getAttribute('data-r')||'');
      editSch(function(s){var w=obj(s.w[scs.d]),cc=clone(obj(w['p'+scs.i]));if(ctc)cc.tc=ctc;else delete cc.tc;if(cr)cc.r=cr;else delete cc.r;w['p'+scs.i]=cc;s.w[scs.d]=w;});
      schDraftSet(scs,ctc,cr);break;
    }
    case 'sch-clear':""")
# 다른 칸을 누를 때 적던 선생님/장소를 먼저 저장
sub("    case 'sch-sel':{var sd0=", "    case 'sch-sel':{schMetaFromInputs(S.schSel);var sd0=")

# 2) 수업 알림: 화면 위 알림 줄, 1초마다 바뀌었는지 확인
sub("  if(S.flash)b+='<div class=\"flash\" role=\"status\"><span>'", "  try{b+=schNowHtml(V0);}catch(e){}\n  if(S.flash)b+='<div class=\"flash\" role=\"status\"><span>'")
sub("function tick(){\n", "function tick(){\n  try{schTick();}catch(e){}\n")

# 3) 설정에서 바로 학교 시간표 열기
sub("""  if(V.me)b+='<div class="fld"><h3>과목 색과 줄임말<small>나에게만 적용</small></h3>""",
    """  if(V.me)b+='<div class="fld"><h3>학교 시간표<small>수업 전에 과목과 장소를 알려 줌</small></h3><div class="row"><button class="btn small" data-act="open" data-modal="school">'+(schOf(V,V.me).has?'고치기':'넣기')+'</button></div></div>';
  if(V.me)b+='<div class="fld"><h3>과목 색과 줄임말<small>나에게만 적용</small></h3>""")

# 4) 할 일 상세 편집: 편집 -> 상세 편집 -> 추가할 때의 창을 그 할 일로 채워서 연다
sub("""      if(date>=t)a+='<button class="btn small" data-act="g-edit" data-date="'+date+'" data-id="'+esc(x.id)+'">수정</button>';""",
    """      if(date>=t)a+='<button class="btn small" data-act="g-edit" data-date="'+date+'" data-id="'+esc(x.id)+'">수정</button><button class="btn small" data-act="g-detail" data-date="'+date+'" data-id="'+esc(x.id)+'">상세 편집</button>';""")
sub("function cmpText(){", r"""/* 할 일 문장을 추가 창의 칸(할 일 종류, 분량, 단위, 자세히)으로 되돌린다. 새로 넣은 할 일은 칸 값을 같이 저장해 둔다 */
function goalParse(V,g){
  if(g.ct!=null||g.ca!=null||g.cn!=null)return {type:String(g.ct||''),amt:+g.ca||0,unit:String(g.cu||''),note:String(g.cn||'')};
  var t=String(g.text||''),rest=t,note='',m=/^(.*?)\s*\(([^()]*)\)$/.exec(t);
  if(m){rest=m[1];note=m[2];}
  var sub=V.subById[g.sid],types=(sub&&sub.items.length?sub.items.map(function(it){return it.label;}):DEFAULT_ITEMS).concat(EXTRA_TYPES),amt=0,unit='';
  var mm=new RegExp('\\s*(\\d+)('+UNITS.join('|')+')$').exec(rest);
  if(mm){amt=+mm[1];unit=mm[2];rest=rest.slice(0,mm.index);}
  rest=rest.trim();
  if(rest&&types.indexOf(rest)<0)return {type:'',amt:0,unit:'',note:t};
  if(!rest&&!amt)return {type:'',amt:0,unit:'',note:note||t};
  return {type:rest,amt:amt,unit:unit,note:note};
}
function cmpText(){""")
sub("""  if(type==='compose'){var cat=el&&el.getAttribute('data-at');S.cmp={date:(el&&el.getAttribute('data-date'))||today(),sid:'',type:'',amt:0,unit:'',at:cat!=null&&cat!==''?+cat:null};S.draft.cmpNote='';}""",
    """  if(type==='compose'){var cat=el&&el.getAttribute('data-at');S.cmp={date:(el&&el.getAttribute('data-date'))||today(),sid:'',type:'',amt:0,unit:'',at:cat!=null&&cat!==''?+cat:null};S.draft.cmpNote='';}
  if(type==='compose'&&S.cmpPre){S.cmp=S.cmpPre.c;S.draft.cmpNote=S.cmpPre.note;S.cmpPre=null;}""")
sub("  if(carry.length||rec.length){", "  if(!c.edit&&(carry.length||rec.length)){")
sub("""  f+='<div class="df"><button class="btn" data-act="cmp-add" data-more="1"'+(text?'':' disabled')+'>넣고 하나 더</button><button class="btn primary" data-act="cmp-add"'+(text?'':' disabled')+'>추가</button></div>';
  return dlg('wide',{id:'compose',t:(c.date===today()?'오늘':shortDate(c.date))+' 할 일 추가'},b,f);""",
    """  if(c.edit)f+='<div class="df"><button class="btn" data-act="modal-close">취소</button><button class="btn primary" data-act="cmp-save"'+(text?'':' disabled')+'>저장</button></div>';
  else f+='<div class="df"><button class="btn" data-act="cmp-add" data-more="1"'+(text?'':' disabled')+'>넣고 하나 더</button><button class="btn primary" data-act="cmp-add"'+(text?'':' disabled')+'>추가</button></div>';
  return dlg('wide',{id:'compose',t:c.edit?(c.date===today()?'오늘':shortDate(c.date))+' 할 일 고치기':(c.date===today()?'오늘':shortDate(c.date))+' 할 일 추가'},b,f);""")
sub("""var ng={id:rid('g'),text:text.slice(0,90),sid:c.sid||'',done:false};""",
    """var ng={id:rid('g'),text:text.slice(0,90),sid:c.sid||'',done:false},cn0=String(S.draft.cmpNote||'').trim();if(c.type)ng.ct=c.type;if(c.amt>0){ng.ca=+c.amt;ng.cu=c.unit||'문제';}if(cn0)ng.cn=cn0;""")
sub("    case 'cmp-add':{", r"""    case 'g-detail':{
      var Vgd=view(),ggd=dayOf(Vgd,Vgd.me,date).goals.filter(function(x){return x.id===id;})[0];if(!ggd||date<today())break;
      var gpr=goalParse(Vgd,ggd);
      S.cmpPre={c:{date:date,sid:ggd.sid&&Vgd.subName[ggd.sid]?ggd.sid:'',type:gpr.type,amt:gpr.amt,unit:gpr.amt>0?(gpr.unit||'문제'):'',at:null,edit:ggd.id},note:gpr.note};
      S.gSel=null;S.sync=true;openModal('compose',el);return;
    }
    case 'cmp-save':{
      var csv=S.cmp,tsv=cmpText();if(!csv||!csv.edit||!tsv)break;
      var nsv=String(S.draft.cmpNote||'').trim(),found=false;
      editDay(csv.date,function(d){d.goals.forEach(function(x){if(x.id!==csv.edit)return;found=true;x.text=tsv.slice(0,90);x.sid=csv.sid||'';
        if(csv.type)x.ct=csv.type;else delete x.ct;if(csv.amt>0){x.ca=+csv.amt;x.cu=csv.unit||'문제';}else{delete x.ca;delete x.cu;}if(nsv)x.cn=nsv;else delete x.cn;});});
      if(!found){flash('고칠 할 일을 찾지 못했습니다.');break;}
      if(!canWrite())break;
      S.draft.cmpNote='';closeModal();flash('할 일을 고쳤습니다.');return;
    }
    case 'cmp-add':{""")
# 한 줄 수정으로 문장을 바꾸면 저장해 둔 칸 값은 맞지 않으므로 지운다(상세 편집은 문장에서 다시 읽음)
sub("editDay(date,function(d){d.goals.forEach(function(x){if(x.id===id)x.text=gtx;});});S.gEdit=null;",
    "editDay(date,function(d){d.goals.forEach(function(x){if(x.id===id&&x.text!==gtx){x.text=gtx;delete x.ct;delete x.ca;delete x.cu;delete x.cn;}});});S.gEdit=null;")
# 고칠 때는 '마감 정하고 나눠 넣기'를 숨긴다
sub("""  b+='<div class="fld plink"><span class="hint">며칠까지 끝낼 일인가요?</span>""", """  if(!c.edit)b+='<div class="fld plink"><span class="hint">며칠까지 끝낼 일인가요?</span>""")

# 창을 닫을 때 적던 선생님/장소 저장, 열 때 예전에 적다 만 값 비우기
sub("function closeModal(){\n  if(!S.modal||S.closing)return;", "function closeModal(){\n  if(!S.modal||S.closing)return;\n  if(S.modal.type==='school'){try{schMetaFromInputs(S.schSel);}catch(e){}}")
sub("  if(type==='school'){S.schWho=null;S.schSel=null;S.schTimes=false;S.draft.schT='';}", "  if(type==='school'){S.schWho=null;S.schSel=null;S.schTimes=false;S.draft.schT='';Object.keys(S.draft).forEach(function(k){if(/^sch(Tc|R):/.test(k))delete S.draft[k];});}")
