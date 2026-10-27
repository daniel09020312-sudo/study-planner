# ---------------------------------------------------------------- v47: 공부 시간 빼기 (JS는 src/v47.js)
V47_JS = open(BASE + '/src/v47.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V47_JS + "\n/* ---------- 공부방 ---------- */")
sub("data-act=\"timer-stop\">끝내고 기록하기</button></div>';}", "data-act=\"timer-stop\">끝내고 기록하기</button><button class=\"btn soft\" data-act=\"open\" data-modal=\"trim\" data-stop=\"1\" style=\"margin-top:8px\">끄는 걸 깜빡했어요: 시간 빼고 끝내기</button></div>';}")
sub("+' 공부 시작</button>';", "+' 공부 시작</button><div class=\"row\" style=\"justify-content:center;margin-top:6px\"><button class=\"linkbtn\" data-act=\"open\" data-modal=\"trim\">공부 시간 빼기</button></div>';")
sub("  if(t==='help')return modalHelp(V);", "  if(t==='help')return modalHelp(V);\n  if(t==='trim'&&S.trim)return modalTrim(V);")
sub("  if(type==='duel'){S.duelF={", "  if(type==='trim')trimInit(el);\n  if(type==='duel'){S.duelF={")
sub("    case 'notice-x':", r"""    case 'trim-set':{
      var tk=el.getAttribute('data-k'),tv=el.getAttribute('data-v');if(!S.trim)break;
      if(tk==='date'){S.trim.date=tv;S.trim.sid='';}else if(tk==='sid')S.trim.sid=tv;else if(tk==='n'){S.trim.n=+tv||30;S.draft.trimN='';}
      break;
    }
    case 'trim-go':trimGo();break;
    case 'notice-x':""")
