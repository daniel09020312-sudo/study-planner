# ---------------------------------------------------------------- v54: 반 전체 목표, 같이 공부하기, 공부 잔디, 요즘 안 보이는 사람, 긴 안내문 줄이기
V54_JS = open(BASE + '/src/v54.js', encoding='utf-8').read()
V54_CSS = open(BASE + '/src/v54.css', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", V54_JS + "\n/* ---------- 공부방 ---------- */")
sub("</style>", V54_CSS + "</style>")
sub("  return {e:e,gi:gi,go:go};\n}", "  gi+=cgInk(V);\n  return {e:e,gi:gi,go:go};\n}")
sub("try{paintMore();pruneOnce(V);eggTick(V);}catch(e){}", "try{paintMore();pruneOnce(V);eggTick(V);cgTick(V);meetTick(V);}catch(e){}")
sub("  return h+'</section></div><div class=\"stack\">'+peopleCard(V,t,1)+flagCard(V,2)+songsCard(V,3)+'</div></div></div>';",
    "  return h+'</section>'+cgCard(V,1)+togetherCard(V,2)+'</div><div class=\"stack\">'+quietCard(V,1)+peopleCard(V,t,1)+flagCard(V,2)+songsCard(V,3)+'</div></div></div>';")
sub("h+='</section><section class=\"card\" id=\"c-rcmp-'", "h+='</section>'+grassCard(V,3)+'<section class=\"card\" id=\"c-rcmp-'")
sub("    case 'notice-x':", r"""    case 'cg-edit':S.cgEdit=!S.cgEdit;S.draft.cgH='';break;
    case 'cg-set':case 'cg-save':{
      var Vg=view();if(!Vg.me||adminId(Vg)!==Vg.me||!need())break;
      var gh=name==='cg-set'?+el.getAttribute('data-v'):Math.round(+S.draft.cgH);
      if(!(gh>=10&&gh<=5000)){flash('목표는 10시간에서 5000시간 사이로 정해 주세요.');break;}
      var gmon=mondayOf(today());
      editCfg(function(c){c.cgoal=obj(c.cgoal);c.cgoal.hist=obj(c.cgoal.hist);c.cgoal.hist[gmon]=gh;c.cgoal.h=gh;});
      if(canWrite()){S.cgEdit=false;S.draft.cgH='';flash('이번 주 반 전체 목표를 '+gh+'시간으로 정했습니다.');}
      break;
    }
    case 'meet-form':{
      if(S.meetForm){S.meetForm=null;break;}
      var md=new Date(Date.now()+30*60000);md.setMinutes(md.getMinutes()<30?30:60,0,0);
      S.meetForm={d:fd(md)===today()?0:1,m:50};S.draft.meetT=String(md.getHours()).padStart(2,'0')+':'+String(md.getMinutes()).padStart(2,'0');S.draft.meetN='';S.sync=true;break;
    }
    case 'meet-set':{if(!S.meetForm)break;var mk2=el.getAttribute('data-k'),mv2=+el.getAttribute('data-v');if(mk2==='d')S.meetForm.d=mv2?1:0;else if(mk2==='m'&&[25,50,90].indexOf(mv2)>=0)S.meetForm.m=mv2;break;}
    case 'meet-add':{
      var Vm=view(),MF=S.meetForm,mt=/^(\d{1,2}):(\d{2})$/.exec(String(S.draft.meetT||''));if(!Vm.me||!MF)break;
      if(!mt){flash('시작 시각을 골라 주세요.');break;}
      var mdt=pd(addDays(today(),MF.d));mdt.setHours(+mt[1],+mt[2],0,0);var mat=mdt.getTime();
      if(mat<Date.now()-60000){flash('이미 지난 시각입니다.');break;}
      if(meetList(Vm).length>=10){flash('약속은 10개까지 만들 수 있습니다.');break;}
      if(!need())break;
      var mid=rid('mt'),mnm=String(S.draft.meetN||'').trim().slice(0,20),mnow=Date.now();
      editCfg(function(c){c.meet=obj(c.meet);Object.keys(c.meet).forEach(function(k){var x=obj(c.meet[k]);if(!(+x.at)||+x.at+(+x.m||50)*60000<mnow-86400000)delete c.meet[k];});c.meet[mid]={at:mat,m:MF.m,t:mnm,by:Vm.me};});
      editProg(function(p){p.mj=obj(p.mj);p.mj[mid]=1;});
      S.meetForm=null;S.draft.meetN='';flash(meetTime(mat)+' 약속을 만들었습니다.');break;
    }
    case 'meet-join':{
      var Vj=view();if(!Vj.me||!obj(Vj.cfg.meet)[id]||!need())break;
      var live2={};meetList(Vj).forEach(function(x){live2[x.id]=1;});
      editProg(function(p){p.mj=obj(p.mj);Object.keys(p.mj).forEach(function(k){if(!live2[k])delete p.mj[k];});if(p.mj[id])delete p.mj[id];else p.mj[id]=1;});
      break;
    }
    case 'meet-del':{
      var Vd2=view(),xm=obj(obj(Vd2.cfg.meet)[id]);if(!Vd2.me||!xm.at||(xm.by!==Vd2.me&&adminId(Vd2)!==Vd2.me))break;
      if(prev!=='mdel:'+id){S.confirm='mdel:'+id;break;}
      if(!need())break;
      editCfg(function(c){c.meet=obj(c.meet);delete c.meet[id];});flash('약속을 지웠습니다.');break;
    }
    case 'grass-m':{var gmv=el.getAttribute('data-v');if(/^\d{4}-\d{2}$/.test(gmv))S.grassM=gmv;break;}
    case 'notice-x':""")

# ---- 긴 안내문 줄이기 (없는 글은 건너뜀)
def subx(a, b):
    global s
    if s.count(a) == 0:
        print('  (v54 text skip)', a[:40])
        return
    s = s.replace(a, b)
for a, b in [
    ("집중한 시간만 기록되고 쉬는 시간은 기록되지 않습니다. 끝내기를 누를 때까지 반복하고, 5시간이 넘으면 자동으로 끝납니다.", "집중한 시간만 기록됩니다. 5시간이 넘으면 자동으로 끝납니다."),
    ("목표 시간이 되면 자동으로 끝나고 기록됩니다. 먼저 끝내도 그때까지 한 만큼 기록됩니다.", "목표 시간이 되면 끝나고, 먼저 끝내도 한 만큼 기록됩니다."),
    ("끝내기를 누르면 기록됩니다. 한 번에 5시간까지 기록되고, 5시간이 넘으면 자동으로 끝납니다.", "끝내기를 누르면 기록됩니다. 5시간이 넘으면 자동으로 끝납니다."),
    ("매주 월요일에 바뀌는 빙고 판입니다. 기록으로 자동 계산됩니다.", "매주 월요일에 바뀌고, 기록으로 저절로 채워집니다."),
    ("한 명을 골라 점수, 공부 시간, 끝낸 할 일로 겨룹니다. 하루씩 승부하는 라운드제, 구경하는 사람의 응원, 도전장 한마디도 있습니다.", "한 명을 골라 정한 기간 동안 겨룹니다."),
    ("기록이 쌓이면 배지를 받습니다. 등급이 높을수록 어렵고, 받은 배지는 최종 점수에 더해집니다.", "기록이 쌓이면 받고, 최종 점수에 더해집니다."),
    ("누가 나를 찌르면 앱이 가려져 있어도 알림으로 알려 줍니다. 앱을 완전히 닫았거나 기기가 앱을 멈춘 뒤에는 받지 못합니다.", "앱이 가려져 있어도 찌르기를 알려 줍니다. 앱을 완전히 닫으면 받지 못합니다."),
    ("시간표가 잠겨 있어 끌거나 눌러도 바뀌지 않습니다. 블록을 누르면 내용만 보입니다. 고치려면 위의 잠김을 눌러 푸세요.", "잠겨 있어 바뀌지 않습니다. 고치려면 위의 잠김을 푸세요."),
    ("빈 곳을 누르면 그 시간에 넣을 할 일을 고를 수 있습니다. 블록을 꾹 눌러 끌면 옮겨지고, 아래 끝을 끌면 길이가 바뀝니다.", "빈 곳 누르기: 할 일 넣기 · 꾹 눌러 끌기: 옮기기 · 아래 끝 끌기: 길이"),
    ("등급마다 동 '+TIERS.b[1]+'점, 은 '+TIERS.s[1]+'점, 금 '+TIERS.g[1]+'점, 전설 '+TIERS.l[1]+'점이 최종 점수에 더해집니다. 받은 배지를 누르면 그 칭호가 이름 옆에 붙습니다.", "동 '+TIERS.b[1]+' · 은 '+TIERS.s[1]+' · 금 '+TIERS.g[1]+' · 전설 '+TIERS.l[1]+'점이 최종 점수에 더해집니다. 누르면 칭호로 붙습니다."),
    ("어제 할 일은 지금도 완료 표시를 할 수 있습니다(더 지난 날은 달력에서 그 날을 눌러서). 지금 인증하면 '+RULE.certLate+'점이고, 어제 할 일을 다 끝냈으면 '+RULE.allLate+'점이 더해집니다.", "지금 인증하면 '+RULE.certLate+'점, 다 끝냈으면 '+RULE.allLate+'점이 더해집니다."),
    ("칸을 누르고 과목을 고른 뒤 선생님과 장소를 적으세요(선택). 수업 시작 전 정각부터 시작하고 10분 뒤까지 화면 위에 과목과 장소가 나옵니다. 같은 수업이 연달아 있으면 이어 붙여 보이고 알림은 한 번만 나옵니다.", "칸을 누르고 과목을 고르세요. 선생님과 장소는 선택입니다."),
    ("모양만 바뀌고 기능과 점수는 그대로입니다. 고른 모양은 이 기기에 저장됩니다.", "모양만 바뀌고 점수는 그대로입니다."),
    ("매일 한 만큼 점수가 쌓이고, 주마다 그리고 시험이 끝났을 때 순위를 매깁니다.", "매일 점수가 쌓이고, 주마다와 시험 뒤에 순위를 매깁니다."),
    ("' 집계는 '+shortDate(TALLY)+'부터이고, 그 전 점수는 보이기만 합니다.'", "' 집계는 '+shortDate(TALLY)+'부터입니다.'"),
    ("내 시험 범위의 단원을 적고 단원별로 끝낸 공부를 표시하세요. 단원은 사람마다 따로 정합니다.", "시험 범위 단원을 적고 끝낸 공부를 표시하세요."),
    ("과목마다 각자 얼마나 했는지 봅니다. 과목을 누르면 단원별로 보입니다.", "과목을 누르면 단원별로 보입니다."),
    ("지난 날 할 일도 지금 완료 표시하고 인증할 수 있습니다. 마감이 지난 인증은 '+RULE.certLate+'점, 할 일을 다 끝냈으면 '+RULE.allLate+'점이 더해집니다.", "마감 뒤 인증 '+RULE.certLate+'점, 다 끝냈으면 '+RULE.allLate+'점."),
    ("아직 대결이 없습니다. 한 명을 골라 점수, 공부 시간, 끝낸 할 일 중 하나로 겨뤄 보세요. 하루씩 승부하는 라운드제도 있고, 구경하는 사람은 응원할 수 있습니다.", "아직 대결이 없습니다. 대결 신청으로 시작해 보세요."),
    ("시간표, 할 일, 달력에 쓰는 내 과목 색과 줄임말입니다. 줄임말은 달력 칸에 보이는 짧은 이름이고 3글자까지 쓸 수 있습니다. 둘 다 나에게만 적용됩니다.", "내 과목 색과 줄임말(3글자까지)입니다. 나에게만 적용됩니다."),
    ("아직 시간대 기록이 없습니다. 타이머로 공부하면 몇 시에 무슨 과목을 했는지 여기에 쌓입니다. (이 기능을 올리기 전의 기록은 시간대를 알 수 없습니다.)", "아직 시간대 기록이 없습니다. 타이머로 공부하면 쌓입니다."),
    ("시간대가 기록된 시간은 이 주 공부 시간의 '+Math.min(100,pct)+'%입니다. 직접 입력한 시간과 예전 기록은 시간대를 알 수 없어 빠집니다.", "이 주 공부 시간의 '+Math.min(100,pct)+'%만 시간대가 있습니다(직접 입력, 예전 기록 제외)."),
    ("집계는 '+esc(longDate(TALLY))+'부터 시작해서 지금은 0점입니다. 매일 얻은 점수는 오늘 화면과 순위의 이번 주에서 그대로 보입니다.", "집계는 '+esc(longDate(TALLY))+'부터라 지금은 0점입니다."),
    ("타이머를 끄는 걸 깜빡해서, 공부하지 않은 시간까지 기록됐다면 그만큼 빼 주세요. 실제로 공부한 시간만 남고 점수도 그에 맞게 다시 계산됩니다.", "공부하지 않은 시간만큼 빼면 점수도 다시 계산됩니다."),
    ("할 일을 꾹 눌러 끌면 다른 날로 옮기거나 순서를 바꿀 수 있습니다. 끄는 채로 달력 오른쪽 끝에 잠깐 대고 있으면 다음 주로 넘어갑니다.", "꾹 눌러 끌면 다른 날로 옮기거나 순서를 바꿉니다."),
    ("아직 모아 둔 할 일이 없습니다. 이번 주에 할 일을 생각나는 대로 적어 두고, 아래에서 요일을 골라 나눠 넣으세요.", "생각나는 할 일을 적어 두고, 요일을 골라 나눠 넣으세요."),
    ("공부하지 않은 시간이 있다면 그만큼 빼 주세요. 뺀 뒤 확인하면 이 표시가 사라집니다.", "공부하지 않은 시간만큼 빼고 확인하면 표시가 사라집니다."),
    ("켜놓기만 했을 수 있는 타이머 기록입니다. 본인이나 방장이 공부하지 않은 시간을 빼고 확인하면 이 표시가 사라집니다.", "켜 두기만 했을 수 있는 기록입니다. 본인이나 방장이 확인하면 사라집니다."),
    ("오늘 끝낼 일을 정해보세요. 과목과 할 일을 눌러서 고르면 됩니다.", "오늘 끝낼 일을 골라 보세요."),
    ("전체 대화와 1:1 메시지를 주고받습니다. 내가 보낸 메시지를 누르면 고치거나 지울 수 있습니다.", "내 메시지를 누르면 고치거나 지울 수 있습니다."),
    ("타이머를 켜면 참여 인원 모두에게 바로 공부 중으로 보입니다.", "타이머를 켜면 모두에게 공부 중으로 보입니다."),
    ("직접 입력은 하루 1시간까지만 점수에 반영되고, 다른 사람에게도 직접 입력으로 표시됩니다.", "직접 입력은 하루 1시간까지 점수에 들어갑니다."),
    ("'. 점수는 시작일부터 보이고, 집계 시작일(지금 '+esc(shortDate(p[2]))+')부터 주간 우승, 배지, 최종 결과에 들어갑니다. 최종 결과는 종료일 다음 날 공개됩니다. 최대 '+PERIOD_MAX_DAYS+'일. 시작일은 월요일로 하면 주간 집계가 깔끔합니다.", "'. 주간 순위·배지·최종 결과는 '+esc(shortDate(p[2]))+'부터 집계합니다. 월요일로 맞추면 깔끔합니다."),
    ("가로, 세로, 대각선 한 줄을 채울 때마다 주간 점수에 '+bingoLine(mon)+'점이 더해집니다. 판은 매주 월요일에 바뀝니다.", "한 줄을 채울 때마다 '+bingoLine(mon)+'점."),
    ("학교와 학원처럼 매주 같은 시간에 있는 일정을 넣어 두면 시간표에 고정으로 깔립니다. 시간표에서 끌어 옮기면 그 날만 바뀝니다.", "매주 같은 시간의 일정은 시간표에 고정으로 깔립니다."),
    ("문제를 올린 날 '+RULE.quiz+'점, 다른 사람 문제를 풀거나 질문에 답하면 1개당 '+RULE.help+'점(하루 '+RULE.helpMax+'개까지)입니다.", "문제 올리기 '+RULE.quiz+'점, 풀이·답변 1개당 '+RULE.help+'점(하루 '+RULE.helpMax+'개)."),
    ("숫자 4자리를 정하면 어느 기기에서든 비밀번호를 눌러야 '+esc(V.byId[V.me].name)+' 님으로 들어올 수 있습니다. 이 기기는 한 번 들어오면 다시 묻지 않습니다.", "정해 두면 다른 기기에서 '+esc(V.byId[V.me].name)+' 님으로 들어올 때 묻습니다."),
    ("빈 시간에 채우기를 누르면 이 범위 안에서 고정 일정이 없는 시간에 할 일을 1시간씩, 사이에 10분씩 쉬며 차례로 넣습니다.", "빈 시간에 할 일을 1시간씩, 10분 쉬며 차례로 넣습니다."),
    ("같은 과목을 선생님 두 분이 나눠 하면 칸마다 선생님을 적어 두세요. 시간표와 수업 알림에 선생님 이름이 같이 나옵니다.", "선생님이 둘인 과목은 칸마다 선생님을 적어 두세요."),
]:
    subx(a, b)
