# ---------------------------------------------------------------- v89: 전체 할 일 창(src/v89.js, 창 'gall', 할 일 목록 카드와 하루 할 일 도구 줄의 '전체 할 일')
V89_JS = open(BASE + '/src/v89.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V89_JS + "\n/* ---------- 공부방 ---------- */")
sub("<button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button>", "<button class=\"chip\" data-act=\"open\" data-modal=\"gall\">전체 할 일</button><button class=\"chip\" data-act=\"open\" data-modal=\"gorder\">순서 정리</button>", 2)
sub("  if(t==='gorder')return modalGOrder(V);", "  if(t==='gorder')return modalGOrder(V);\n  if(t==='gall')return modalGAll(V);")
sub("  if(type==='inbox'){S.ib=", "  if(type==='gall'){S.ga={f:'all',hid:false,old:false,nod:!!(S.ga&&S.ga.nod),sid:(S.ga&&S.ga.sid)||''};S.draft.gaText='';if(!S.draft.gaDate||S.draft.gaDate<today())S.draft.gaDate=today();}\n  if(type==='inbox'){S.ib=")
sub("    case 'ib-big':", r"""    case 'ga-f':if(S.ga)S.ga.f=el.getAttribute('data-v');break;
    case 'ga-nod':if(S.ga)S.ga.nod=!S.ga.nod;break;
    case 'ga-ibdone':{if(!need())break;var gib=id;editInbox(function(d){var it=d.items[gib];if(it){if(it.done)delete it.done;else it.done=true;}});break;}
    case 'ga-old':if(S.ga)S.ga.old=!S.ga.old;break;
    case 'ga-hid':if(S.ga)S.ga.hid=!S.ga.hid;break;
    case 'ga-sid':if(S.ga)S.ga.sid=S.ga.sid===el.getAttribute('data-v')?'':el.getAttribute('data-v');break;
    case 'ga-addsub':if(S.ga){S.ga.sid=el.getAttribute('data-v')||'';S.focusAfter='gaText';var gdb=document.querySelector('#dlg-gall .db');if(gdb)gdb.scrollTop=0;}break;
    case 'ga-add':gaAdd();break;
    case 'ga-hide':case 'ga-show':{var gk=el.getAttribute('data-v'),gon=name==='ga-hide';if(!gk||!need())break;editProg(function(p){p.gah=obj(p.gah);if(gon)p.gah[gk]=1;else delete p.gah[gk];});flash(gon?'이 창에서 뺐습니다. \'뺀 할 일\'에서 다시 넣을 수 있습니다.':'다시 넣었습니다.');break;}
    case 'ib-big':""")
# 할 일 모음에서 끝낸 항목(전체 할 일 창에서 표시)은 줄을 긋고 보임
sub("      b+='<li class=\"ibrow'+(on?' on':'')+'\" data-id=", "      b+='<li class=\"ibrow'+(on?' on':'')+(x.done?' ibdone':'')+'\" data-id=")
