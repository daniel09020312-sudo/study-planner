# ---------------------------------------------------------------- 웹 판: 다른 방에서 내 것 가져오기 (src/carry.js)
# build_web.py 안에서 web_rooms_part.py 다음에 exec 된다.
CARRY_JS = open(BASE + '/src/carry.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", CARRY_JS + "\n/* ---------- 공부방 ---------- */")
# 설정 > 방: 세 번째 칸
sub("""<span><b>새로운 방 만들기</b><small>기록은 새로 시작</small></span></button></div></div>';""",
    """<span><b>새로운 방 만들기</b><small>기록은 새로 시작</small></span></button>'+(crRooms().length?'<button class="rmact cr" data-act="open" data-modal="carry"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M5 19h14"/></svg></i><span><b>다른 방에서 가져오기</b><small>내 일정, 할 일, 시간표, 과목 설정</small></span></button>':'')+'</div></div>';""")
sub("  if(type==='rooms'){S.jst.err='';S.draft.joinCode='';}", "  if(type==='rooms'){S.jst.err='';S.draft.joinCode='';}\n  if(type==='carry')S.cr={step:'pick',opt:{ev:true,goal:true,tt:true,prog:true,sub:true,rec:false}};")
sub("  if(t==='rooms')return modalRooms(V);", "  if(t==='rooms')return modalRooms(V);\n  if(t==='carry')return modalCarry(V);")
sub("    case 'join-go':joinGo();return;", r"""    case 'cr-pick':{var cre=crRooms().filter(function(x){return x.room===id;})[0];if(cre)crLoad(cre);return;}
    case 'cr-back':S.cr={step:'pick',opt:S.cr&&S.cr.opt||{ev:true,goal:true,tt:true,prog:true,sub:true,rec:false}};break;
    case 'cr-opt':if(S.cr&&S.cr.opt){var crk=el.getAttribute('data-k');S.cr.opt[crk]=!S.cr.opt[crk];}break;
    case 'cr-go':crGo();return;
    case 'join-go':joinGo();return;""")
sub("</style>", """.rmact.cr{grid-column:1/-1}
.rmact.cr i{background:color-mix(in srgb,var(--accent) 14%,var(--surface));color:var(--accent-ink)}
.crchk{align-items:flex-start;width:100%;margin-top:10px}
.crchk i{margin-top:1px}
.crchk span{display:flex;flex-direction:column;gap:2px;min-width:0}
.crchk b{color:var(--ink);font-weight:700;font-size:14.5px}
.crchk small{color:var(--ink-2);font-size:12.5px;line-height:1.4}
</style>""")

# 가져오기(와 그 되돌리기)는 지난 날 할 일 보호(guardDay)를 건너뛴다
sub("function guardDay(path,data){\n", "function guardDay(path,data){\n  if(S.crRaw)return data;\n")
sub("      var u=S.undo;if(!u||!need())break;\n      Object.keys(u).forEach(function(p){queueWrite(p,u[p]);});",
    "      var u=S.undo;if(!u||!need())break;\n      S.crRaw=!!(S.crUndo&&u===S.crUndo);try{Object.keys(u).forEach(function(p){queueWrite(p,u[p]);});}finally{S.crRaw=false;}")
sub("</style>", """.crsep{margin-top:16px;padding-top:12px;border-top:1px solid var(--line)}
.crsep h4{margin:0;font-size:13px;font-weight:700;color:var(--ink-2)}
.crsep h4 small{margin-left:6px;font-weight:500;color:var(--ink-3)}
</style>""")
