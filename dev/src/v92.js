/* ---------- v92: 시험 안내(창 'exam'). 방 설정 cfg.exam={t,days:[{d,ps:[[교시,[과목 이름..]]]}],times:[[교시,'시작','끝']],subs:[{n,r,by,at}],notes:[..]}
   과목은 이름으로 맞춤(examKey: 공백 빼고 Ⅰ/I/1 같게). 과목마다 시험 날·교시·범위와 그 과목 듣는 사람(skipOf). 범위는 누구나 고칠 수 있음(by, at).
   EXAM_PRESET은 2학기 2차 시험(2학년). 방 과목 이름이 3개 이상 맞으면 한 번만 넣음(examMig, cfg.migExam2) ---------- */
var EXAM_PRESET={t:'2학기 2차 시험',
  times:[[1,'08:40','09:30'],[2,'09:50','10:40'],[3,'11:00','11:50']],
  days:[
    {d:'2026-12-03',ps:[[1,['확률과 통계','세계 문화와 영어']],[2,['생물의 유전','현대 세계의 변화']],[3,['화학 반응의 세계','서양의 철학과 사상']]]},
    {d:'2026-12-04',ps:[[1,['영어 비평적 읽기와 쓰기']],[2,['전자기와 양자','지정학과 글로벌 이슈']],[3,['세포와 물질대사','행성우주과학']]]},
    {d:'2026-12-07',ps:[[1,['미적분Ⅰ']],[2,['물리학 실험','화학 실험','생명과학 실험','데이터 과학','일본 문화']]]},
    {d:'2026-12-08',ps:[[1,['화법과 언어']],[2,['지구시스템과학','기업과 경영']]]}],
  subs:[
    {n:'화법과 언어',r:'교과서 pp.42~85, pp.150~239, 수업 시간에 다뤄진 모든 자료'},
    {n:'미적분Ⅰ',r:'교과서 pp.87~165, 부교재 pp.105~239'},
    {n:'확률과 통계',r:'교과서 pp.63~143, 부교재 pp.34~77'},
    {n:'세계 문화와 영어',r:'수업시간에 다뤄진 모든 자료'},
    {n:'영어 비평적 읽기와 쓰기',r:'수업시간에 다뤄진 모든 자료, 부교재 pp.89~끝, 10월 전국연합, 수특영어 26, 27강'},
    {n:'기업과 경영',r:'Ⅲ. 기업의 부문별 활동 ~ Ⅳ. 글로벌 경영'},
    {n:'현대 세계의 변화',r:'교과서 pp.113~153, pp.161~169, p.186, p.191'},
    {n:'서양의 철학과 사상',r:'배부 유인물 pp.94~159'},
    {n:'지정학과 글로벌 이슈',r:'수업시간에 다뤄진 모든 자료'},
    {n:'전자기와 양자',r:'Ⅱ. 빛과 정보 통신 ~ Ⅲ. 양자와 미시세계, 교과서 및 모든 유인물'},
    {n:'화학 반응의 세계',r:'Ⅱ. 산화환원 반응 ~ Ⅲ. 탄소화합물과 반응, 수업시간에 제공된 모든 자료와 구글 클래스룸 과제 전체'},
    {n:'세포와 물질대사',r:'Ⅲ. 세포호흡과 광합성 (교과서 pp.82~127, 부교재 pp.130~227, 수업시간에 제공된 모든 자료와 구글 클래스룸 과제 전체)'},
    {n:'생물의 유전',r:'Ⅰ.1. 유전의 기본 원리 ~ Ⅰ.3. 사람의 유전병, Ⅱ. 유전자의 발현 전체(Ⅱ.1.~Ⅱ.3.), 수업 시간에 제공된 모든 자료와 구글 클래스룸 과제 전체'},
    {n:'지구시스템과학',r:'교과서 pp.54~121, 부교재 pp.90~207'},
    {n:'행성우주과학',r:'교과서 pp.22~111, 부교재 pp.32~207'},
    {n:'물리학 실험',r:'측정의 오차와 유효 숫자, 빗면을 내려가는 물체의 운동, 원운동 실험, 운동량 보존, 전기 회로 설계, 등전위선, 클래스룸 제출 과제 포함 수업시간에 진행한 모든 학습자료'},
    {n:'화학 실험',r:'중화적정, 비타민C 함량분석, 흡광도 분석, 은거울 반응, 수업시간에 제공한 모든 학습자료 포함'},
    {n:'생명과학 실험',r:'교과서 pp.120~125, pp.132~259 및 모든 교과서 범위 관련 유인물 및 실험보고서'},
    {n:'데이터 과학',r:'수업자체자료(파이썬 문법, numpy, pandas 실습)'},
    {n:'일본 문화',r:'교과서 pp.1~145'}],
  notes:['한 교시에 과목이 여럿이면 선택 과목입니다. 그 교시 시험이 없는 사람은 다른 교실로 이동하거나 귀가합니다.','성적 이의 신청 기간: 12월 9일 ~ 12월 10일','일정과 범위는 시험 전까지 바뀔 수 있습니다. 바뀌면 범위를 고쳐 주세요.']};
function examKey(n){return String(n||'').replace(/\s+/g,'').replace(/[ⅠI1]$/,'1').replace(/Ⅱ$/,'2').toLowerCase();}
function examOf(V){var e=obj(obj(V.cfg).exam);return arr(e.days).length?e:null;}
/* 과목 이름 -> {d,p,s,e,r,by,at,i} */
function examMap(E){
  var m={},tm={};arr(E.times).forEach(function(t){t=arr(t);tm[t[0]]=t;});
  arr(E.days).forEach(function(dy){dy=obj(dy);arr(dy.ps).forEach(function(pp){pp=arr(pp);var t=tm[pp[0]]||[];arr(pp[1]).forEach(function(n){m[examKey(n)]={n:n,d:dy.d,p:+pp[0],s:t[1]||'',e:t[2]||'',sel:arr(pp[1]).length>1};});});});
  arr(E.subs).forEach(function(x,i){x=obj(x);var k=examKey(x.n);m[k]=Object.assign(m[k]||{n:x.n},{r:x.r||'',by:x.by||'',at:x.at||0,i:i});});
  return m;
}
function examForSub(V,sid){var E=examOf(V);if(!E||!V.subName[sid])return null;return examMap(E)[examKey(V.subName[sid])]||null;}
function examTakers(V,name){var sid=null;V.subs.forEach(function(s){if(examKey(s.name)===examKey(name))sid=s.id;});if(!sid)return null;return V.roster.filter(function(m){return !skipOf(V,m.id)[sid];});}
function examDate(d){var x=pd(d);return (x.getMonth()+1)+'/'+x.getDate()+'('+DOW[x.getDay()]+')';}
function examMine(V){var E=examOf(V);if(!E)return [];var mp=examMap(E),out=[];mySubs(V).forEach(function(s){var x=mp[examKey(s.name)];if(x&&x.d)out.push(Object.assign({sid:s.id},x));});return out.sort(function(a,b){return a.d<b.d?-1:a.d>b.d?1:a.p-b.p;});}
/* 진도 화면 맨 위 카드: 다음 시험 날과 내 과목 */
function examCard(V){
  var E=examOf(V);if(!E)return '';var t=today(),last=arr(E.days).map(function(x){return obj(x).d;}).sort().pop();if(!last||last<t)return '';
  var mine=examMine(V),next=mine.filter(function(x){return x.d>=t;})[0],h='<section class="card excard" id="c-exam" style="--k:0"><div class="ct"><h2>'+esc(E.t||'시험 안내')+'<small>'+(next?dlabel(next.d):'')+'</small></h2><button class="btn small primary" data-act="open" data-modal="exam">범위·일정 보기</button></div>';
  if(mine.length){h+='<div class="exchips">'+mine.map(function(x){return '<button class="exchip'+(x.d<t?' past':'')+'" data-act="open" data-modal="exam" data-id="'+esc(x.sid)+'" style="--sc:'+subCol(V,x.sid)+'"><i></i><b>'+esc(V.subName[x.sid])+'</b><small>'+examDate(x.d)+' '+x.p+'교시</small></button>';}).join('')+'</div>';}
  else h+='<p class="hint">내 과목 중 시험 일정에 있는 과목이 없습니다.</p>';
  return h+'</section>';
}
function modalExam(V){
  var E=examOf(V);if(!E)return dlg('wide',{id:'exam',t:'시험 안내'},'<p class="empty">아직 시험 안내가 없습니다.</p>','');
  var X=S.ex||{},mp=examMap(E),mine={},t=today(),tm={};mySubs(V).forEach(function(s){mine[examKey(s.name)]=s.id;});arr(E.times).forEach(function(x){x=arr(x);tm[x[0]]=x;});
  var b='<div class="seg mini exseg" role="group" style="grid-template-columns:repeat(2,minmax(0,1fr))"><button data-act="ex-all" data-v="" aria-pressed="'+(X.all?'false':'true')+'">내 과목</button><button data-act="ex-all" data-v="1" aria-pressed="'+(X.all?'true':'false')+'">모든 과목</button></div>';
  arr(E.days).forEach(function(dy,di){
    dy=obj(dy);var rows='';
    arr(dy.ps).forEach(function(pp){pp=arr(pp);var tt=tm[pp[0]]||[];
      arr(pp[1]).forEach(function(n){
        var k=examKey(n),sid=mine[k],x=mp[k]||{n:n};if(!X.all&&!sid)return;
        var tk=examTakers(V,n),open=X.open===k,col=sid?subCol(V,sid):SGRAY;
        rows+='<div class="exrow'+(sid?' mine':'')+(X.focus&&X.focus===sid?' focus':'')+'" id="ex-'+esc(k)+'" style="--sc:'+col+'"><div class="exh"><span class="exp">'+pp[0]+'교시<small>'+esc(tt[1]||'')+(tt[2]?'~'+esc(tt[2]):'')+'</small></span><b class="exn"><i></i>'+esc(n)+(arr(pp[1]).length>1?'<em class="tag">선택</em>':'')+'</b>'+(tk?'<button class="linkbtn" data-act="ex-who" data-v="'+esc(k)+'">'+tk.length+'명 들음</button>':'')+'</div>';
        if(X.who===k&&tk)rows+='<p class="exwho">'+tk.map(function(m){return esc(m.id===V.me?'나':V.byId[m.id].name);}).join(', ')+'</p>';
        if(X.edit===k)rows+='<div class="exedit"><textarea data-draft="exR:'+esc(k)+'" rows="3" maxlength="400" aria-label="'+esc(n)+' 시험 범위"></textarea><div class="row"><button class="btn small primary" data-act="ex-save" data-v="'+esc(k)+'" data-n="'+esc(n)+'">저장</button><button class="btn small" data-act="ex-edit" data-v="">취소</button></div></div>';
        else rows+='<p class="exr">'+(x.r?esc(x.r):'<span class="hint">범위가 아직 없습니다.</span>')+'</p><div class="exft">'+(x.by&&V.byId[x.by]?'<small>'+esc(V.byId[x.by].name)+'이(가) 고침</small>':'<small></small>')+'<button class="del" data-act="ex-edit" data-v="'+esc(k)+'">범위 고치기</button></div>';
        rows+='</div>';
      });
    });
    if(!rows)return;
    b+='<section class="exday'+(dy.d<t?' past':'')+'"><h3>'+(di+1)+'일차 <b>'+examDate(dy.d)+'</b><small>'+dlabel(dy.d)+'</small></h3>'+rows+'</section>';
  });
  if(!X.all&&!examMine(V).length)b+='<p class="empty">내 과목 중 시험 일정에 있는 과목이 없습니다. \'모든 과목\'을 눌러 보세요.</p>';
  b+='<div class="exnotes"><h3>시험 시간</h3><p>'+arr(E.times).map(function(x){x=arr(x);return x[0]+'교시 '+esc(x[1])+'~'+esc(x[2]);}).join(' · ')+'</p>'+arr(E.notes).map(function(n){return '<p class="hint">'+esc(n)+'</p>';}).join('')+'</div>';
  return dlg('wide',{id:'exam',t:esc(E.t||'시험 안내')},b,'<div class="df"><span class="hint">과목 이름이 같으면 그 과목을 듣는 사람 모두에게 같은 범위가 보입니다.</span></div>');
}
var EXAM_MIG=false;
function examMig(){
  if(EXAM_MIG||!netFresh())return;var V=view();if(!S.ready||!V||!V.me||!canWrite())return;
  EXAM_MIG=true;var c=obj(V.cfg);if(c.migExam2||c.exam)return;
  var have={};V.subs.forEach(function(s){have[examKey(s.name)]=1;});
  var hit=EXAM_PRESET.subs.filter(function(x){return have[examKey(x.n)];}).length;if(hit<3)return;
  editCfg(function(cc){cc.exam=clone(EXAM_PRESET);cc.migExam2=1;});
}
