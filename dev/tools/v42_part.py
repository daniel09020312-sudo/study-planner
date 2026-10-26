# ---------------------------------------------------------------- v42: 인원 50명까지, 벌칙 없애기, 상품은 1·2·3등 (상품 화면은 src/award.js)
# 1) 참여 인원 한도 12 -> 50 (인원 추가, 처음 화면의 이름 추가). 새 방 만들기의 한도는 src/rooms.js
ROSTER_MAX = 50
s = s.replace("c.roster.length>=12", "c.roster.length>=ROSTER_MAX")
assert s.count("c.roster.length>=ROSTER_MAX") == 2
s = s.replace("참여 인원은 12명까지 추가할 수 있습니다.", "참여 인원은 '+ROSTER_MAX+'명까지 추가할 수 있습니다.")
assert s.count("참여 인원은 '+ROSTER_MAX+'명까지") == 2
sub("var GMAX=12;", "var GMAX=12,ROSTER_MAX=" + str(ROSTER_MAX) + ";")

# 사람마다 한 칸씩인 진도 표: 사람이 많으면 옆으로 밀어 보고, 과목 이름 칸은 왼쪽에 붙여 둔다
assert s.count("+(n>6?';--cw:46px':'')+'\"") >= 1
s = s.replace("<section class=\"card tbl\" id=\"c-tbl\" style=\"--k:0;--n:'+n+(n>6?';--cw:46px':'')+'\"",
              "<section class=\"card tbl'+(n>8?' many':'')+'\" id=\"c-tbl\" style=\"--k:0;--n:'+n+(n>6?';--cw:46px':'')+'\"")
assert s.count("tbl'+(n>8?' many':'')+'") >= 1

# 2) 벌칙 없애기: 벌칙 후보, 꼴찌 벌칙, 벌칙 룰렛(주간, 최종)
cut("function penList(V){", "function duelRow(V,d){", "")
cut("function wheelSvg(labels){", "function modalDuel(V){", "")
cut("function spinRoul(){", "function afterPlay(V){", "")
cut("    case 'pen-add':{", "    case 'duel-set':{", "")
cut("    case 'pen2-add':{", "    case 'abbr-open':", "")
sub("  if(t==='roul'&&S.roul)return modalRoul(V);\n", "")
sub("  ['최종 결과','2차 시험이 끝난 다음 날 공개. 1등은 선물, 꼴찌는 모두가 낸 벌칙 후보 중 룰렛으로 뽑은 벌칙']",
    "  ['최종 결과','2차 시험이 끝난 다음 날 공개. 1등, 2등, 3등은 미리 정해 둔 상품']")
sub("/* ---------- 도전: 빙고, 배지, 1:1 대결, 벌칙 룰렛 ---------- */", "/* ---------- 도전: 빙고, 배지, 1:1 대결 ---------- */")
for k in ['penList(', 'penItems(', 'penCard(', 'loserLine(', 'penLoser(', 'modalRoul(', 'spinRoul(', 'wheelSvg(', 'roul-open', '벌칙']:
    assert k not in s, (k, s.count(k))

# 3) 상품: 1·2·3등을 따로 정한다 (cfg.prizes['p'+등수]). 예전 cfg.prize는 1등 상품으로 읽는다
sub("    case 'prize-save':{var pzt=String(S.draft.prizeText||'').trim().slice(0,40),Vz=view();if(!pzt||!Vz.me||finalOpen())break;editCfg(function(c){c.prize={t:pzt,by:Vz.me};});if(canWrite()){S.draft.prizeText='';S.sync=true;flash('1등 선물을 정했습니다.');}break;}",
    """    case 'prize-save':{
      var pzk=Math.max(1,Math.min(PRIZE_N,Math.floor(+id||1))),pzt=String(S.draft['prizeText'+pzk]||'').trim().slice(0,40),Vz=view();if(!pzt||!Vz.me||finalOpen())break;
      editCfg(function(c){var ps=obj(c.prizes);if(pzk===1&&c.prize)delete c.prize;ps['p'+pzk]={t:pzt,by:Vz.me};c.prizes=ps;});
      if(canWrite()){S.draft['prizeText'+pzk]='';S.sync=true;flash(pzk+'등 상품을 정했습니다.');}break;
    }""")

sub("</style>", """.przs{display:grid;gap:8px}
.prz .row{margin-top:8px}
.prz input,.prz .btn{background:var(--surface)}
.prz.p2{background:color-mix(in srgb,var(--ts) 12%,var(--surface))}
.prz.p3{background:color-mix(in srgb,var(--tb) 10%,var(--surface))}
.tbl.many{overflow-x:auto;-webkit-overflow-scrolling:touch}
.tbl.many .orow{grid-template-columns:var(--lw,180px) repeat(var(--n),var(--cw));min-width:max-content}
@media (max-width:640px){.tbl.many{--lw:128px}}
.tbl.many .olabel{position:sticky;left:0;z-index:1;background:var(--surface)}
.tbl.many .ounits{position:sticky;left:0;max-width:calc(100vw - 32px)}
</style>""")
