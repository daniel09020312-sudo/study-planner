/* ---------- 점수 규칙: 줄글 대신 묶음별로 항목, 점수, 짧은 조건 ---------- */
// 점수는 RULE, TIERS, WEEK_BONUS에서 그대로 읽어 실제 계산과 어긋나지 않게 한다
function rulesData(){
  var T=typeof TIERS!=='undefined'?TIERS:null,WB=typeof WEEK_BONUS!=='undefined'?WEEK_BONUS:null;
  var g=[
    {t:'매일',items:[
      ['출석','5~10점',['연속 출석할수록 하루 1점씩 올라감','7일째마다 10점 더']],
      ['할 일 모두 끝내고 인증',RULE.allCert+'점',['할 일 3개 이상 세우고 전부 끝내기','마감 뒤 인증은 '+RULE.allLate+'점']],
      ['인증',RULE.certOn+'점',['마감 뒤 인증은 '+RULE.certLate+'점']],
      ['공부 시간','30분 '+RULE.per30+'점',['하루 '+RULE.timeMax+'점까지','직접 입력한 시간은 하루 1시간까지']],
      ['문제 내기',RULE.quiz+'점',['문제를 올린 날']],
      ['풀이와 답변','1개 '+RULE.help+'점',['다른 사람 문제 풀기, 질문에 답하기','하루 '+RULE.helpMax+'개까지']],
      ['하루 순위',RULE.rank.join(' · ')+'점',['그날 점수 1 · 2 · 3등']]
    ]},
    {t:'매주',items:[
      ['스터디 빙고','1줄 10점',['한 줄 채울 때마다']]
    ]}
  ];
  if(WB)g[1].items.push(['주간 순위',WB.join(' · ')+'점',['한 주 점수 1 · 2 · 3등','최종 점수에 더함']]);
  if(T)g.push({t:'시험 끝나고',items:[
    ['배지',T.b[1]+' · '+T.s[1]+' · '+T.g[1]+' · '+T.l[1]+'점',[T.b[0]+' · '+T.s[0]+' · '+T.g[0]+' · '+T.l[0]+' 등급 순서','받은 배지마다 최종 점수에 더함']],
    ['최종 점수','합계',['누적 점수 + 주간 순위 + 배지']]
  ]});
  return g;
}
function rulesHtml(){
  return '<div class="rlz">'+rulesData().map(function(gr){
    return '<div class="rlg"><h4>'+esc(gr.t)+'</h4><ul>'+gr.items.map(function(it){
      return '<li><div class="rln"><b>'+esc(it[0])+'</b>'+(it[2]&&it[2].length?'<small>'+it[2].map(esc).join('<br>')+'</small>':'')+'</div><em class="rlp">'+esc(it[1])+'</em></li>';
    }).join('')+'</ul></div>';
  }).join('')+'</div>';
}
