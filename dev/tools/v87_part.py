# ---------------------------------------------------------------- v87: 할 일 모음 항목 고치기(ib-edit: 그 줄이 글 칸과 과목 칩으로 바뀜, S.ibEdit={id,sid}, 저장 ib-esave·엔터, 취소 ib-ecancel)
sub("function modalInbox(V){", r"""function ibEditRow(V,x){
  var E=S.ibEdit,k='ibE:'+x.id;if(S.draft[k]==null)S.draft[k]=x.t;
  var h='<li class="ibrow ibedit" data-id="'+esc(x.id)+'"><div class="ibe"><input type="text" id="ibE-'+esc(x.id)+'" data-draft="'+esc(k)+'" data-enter="ib-esave" maxlength="90" aria-label="할 일 고치기">';
  h+='<div class="chips scroll">'+mySubs(V).map(function(s){return '<button class="chip" data-act="ib-esid" data-v="'+esc(s.id)+'" aria-pressed="'+(E.sid===s.id?'true':'false')+'">'+esc(s.name)+'</button>';}).join('')+'<button class="chip" data-act="ib-esid" data-v="" aria-pressed="'+(!E.sid?'true':'false')+'">과목 없음</button></div>';
  h+='<div class="row"><button class="btn small primary" data-act="ib-esave">저장</button><button class="btn small" data-act="ib-ecancel">취소</button></div></div></li>';
  return h;
}
function modalInbox(V){""")
sub("      b+='<li class=\"ibrow'+(on?' on':'')+'\" data-id=", "      if(S.ibEdit&&S.ibEdit.id===x.id){b+=ibEditRow(V,x);return;}\n      b+='<li class=\"ibrow'+(on?' on':'')+'\" data-id=")
sub("<button class=\"del\" data-act=\"ib-del\" data-id=\"'+esc(x.id)+'\">", "<span class=\"ibacts\"><button class=\"del ibedb\" data-act=\"ib-edit\" data-id=\"'+esc(x.id)+'\">고치기</button><button class=\"del\" data-act=\"ib-del\" data-id=\"'+esc(x.id)+'\">")
sub("(S.confirm==='ibdel:'+x.id?'한 번 더':'지우기')+'</button>", "(S.confirm==='ibdel:'+x.id?'한 번 더':'지우기')+'</button></span>")
sub("    case 'ib-view':", r"""    case 'ib-edit':{var Ve=view(),xe=ibItems(Ve).filter(function(q){return q.id===id;})[0];if(!xe)break;S.ibEdit={id:id,sid:Ve.subName[xe.sid]?xe.sid:''};S.draft['ibE:'+id]=xe.t;S.focusAfter='ibE-'+id;break;}
    case 'ib-esid':if(S.ibEdit)S.ibEdit.sid=el.getAttribute('data-v')||'';break;
    case 'ib-ecancel':if(S.ibEdit){delete S.draft['ibE:'+S.ibEdit.id];S.ibEdit=null;}break;
    case 'ib-esave':{var Es=S.ibEdit;if(!Es)break;var et=String(S.draft['ibE:'+Es.id]||'').trim();if(!et){flash('할 일 내용을 적어 주세요.');break;}var Vs=view();if(!ibItems(Vs).some(function(q){return q.id===Es.id;})){S.ibEdit=null;break;}var esn=snap(['inbox/'+Vs.me]);editInbox(function(d){var it=d.items[Es.id];if(!it)return;it.t=et.slice(0,90);if(Es.sid)it.sid=Es.sid;else delete it.sid;});delete S.draft['ibE:'+Es.id];S.ibEdit=null;flash('고쳤습니다.',esn);break;}
    case 'ib-view':""")
sub("if(type==='inbox'){S.ib={sel:{},week:wkStart(today()),sid:''};S.draft.ibText='';}", "if(type==='inbox'){S.ib={sel:{},week:wkStart(today()),sid:''};S.draft.ibText='';S.ibEdit=null;}")
