# ---------------------------------------------------------------- v92: 시험 안내(src/v92.js, 창 'exam', cfg.exam): 시험 날·교시·범위·듣는 사람, 범위 고치기, 진도 화면 위 카드, 'D-' 알약 누르면 열림
V92_JS = open(BASE + '/src/v92.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V92_JS + "\n/* ---------- 공부방 ---------- */")
sub("<span class=\"pill\">2차 시험<b>D-'+dd+'</b></span>", "<button class=\"pill pillbtn\" data-act=\"open\" data-modal=\"exam\">2차 시험<b>D-'+dd+'</b></button>", 4)
sub("  try{itemMig();}catch(e){}", "  try{itemMig();}catch(e){}\n  try{examMig();}catch(e){}")
sub("  h+='<section class=\"card usum\" id=\"c-usum\"", "  h+=examCard(V);\n  h+='<section class=\"card usum\" id=\"c-usum\"")
sub("<b class=\"upct\">'+st.pct+'%</b></div><div class=\"ubar\" aria-hidden=\"true\"><i style=\"width:'+st.pct+'%\"></i></div>';", "<b class=\"upct\">'+st.pct+'%</b></div><div class=\"ubar\" aria-hidden=\"true\"><i style=\"width:'+st.pct+'%\"></i></div>';\n    var exs=examForSub(V,s.id);if(exs&&exs.d)h+='<button class=\"uexam\" data-act=\"open\" data-modal=\"exam\" data-id=\"'+esc(s.id)+'\"><b>시험 '+examDate(exs.d)+' '+exs.p+'교시</b><span>'+esc(exs.r||'범위 보기')+'</span></button>';")
sub("  if(t==='gall')return modalGAll(V);", "  if(t==='gall')return modalGAll(V);\n  if(t==='exam')return modalExam(V);")
sub("  if(type==='gall'){", "  if(type==='exam'){var exid=el&&el.getAttribute&&el.getAttribute('data-id');S.ex={all:false,focus:exid||null};}\n  if(type==='gall'){")
sub("    case 'ga-old':", r"""    case 'ex-all':if(S.ex)S.ex.all=!!el.getAttribute('data-v');break;
    case 'ex-who':if(S.ex)S.ex.who=S.ex.who===el.getAttribute('data-v')?null:el.getAttribute('data-v');break;
    case 'ex-edit':{if(!S.ex)break;var exk=el.getAttribute('data-v')||null;S.ex.edit=exk;if(exk){var Vx=view(),ex0=obj(examMap(examOf(Vx)||{})[exk]);S.draft['exR:'+exk]=ex0.r||'';}break;}
    case 'ex-save':{var Ve=view(),E0=examOf(Ve),ek=el.getAttribute('data-v'),en=el.getAttribute('data-n'),er=String(S.draft['exR:'+ek]||'').trim().slice(0,400);if(!E0||!need())break;editCfg(function(c){var e=c.exam;e.subs=arr(e.subs);var i=-1;e.subs.forEach(function(x,j){if(examKey(obj(x).n)===ek)i=j;});var nx={n:en,r:er,by:Ve.me,at:Date.now()};if(i<0)e.subs.push(nx);else e.subs[i]=Object.assign({},obj(e.subs[i]),nx);});S.ex.edit=null;flash(en+' 시험 범위를 고쳤습니다.');break;}
    case 'ga-old':""")
