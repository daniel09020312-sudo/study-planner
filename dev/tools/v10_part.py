# ---------------------------------------------------------------- 10/10 요청
# 새 주기 시작: 10월 12일 월요일
sub("var START='2026-10-05',", "var START='2026-10-12',")
sub("{name:'개념',from:'2026-10-05',", "{name:'개념',from:'2026-10-12',")

# 벌칙 칸 없애기: 순위 화면의 벌칙 룰렛 카드, 꼴찌 벌칙 표시, 1:1 대결의 벌칙
sub("  h+='</div><div class=\"stack\">'+penCard(V,2);", "  h+='</div><div class=\"stack\">';")
sub("+(last?'<span class=\"tag r\">'+(done?'벌칙 확정':'지금 벌칙 자리')+'</span>':'')", "")
cut("function duelRow(V,d){", "function viewPlay(V){", r"""function duelRow(V,d){
  var A=V.byId[d.a],B=V.byId[d.b],h='<div class="duel" id="du-'+esc(d.id)+'">';
  if(d.state==='pending'){
    h+='<div class="pl"><span><b>'+esc(A.name)+'</b> 님이 <b>'+esc(B.name)+'</b> 님에게 신청</span><span class="tag">수락 대기</span></div>';
    if(d.b===V.me)h+='<div class="row" style="margin-top:8px"><button class="btn small primary" data-act="duel-ok" data-id="'+esc(d.id)+'">수락</button><button class="btn small" data-act="duel-no" data-id="'+esc(d.id)+'">거절</button></div>';
    else if(d.a===V.me)h+='<div class="row" style="margin-top:8px"><button class="btn small" data-act="duel-no" data-id="'+esc(d.id)+'">신청 취소</button></div>';
    return h+'</div>';
  }
  var tot=d.pa+d.pb,lab=d.state==='ready'?'내일 시작':d.state==='on'?(diffDays(today(),d.end)+1)+'일 남음':'종료';
  h+='<div class="vs"><span><b>'+esc(A.name)+'</b></span><em>'+esc(shortDate(d.start)+' ~ '+shortDate(d.end))+', '+lab+'</em><span class="r"><b>'+esc(B.name)+'</b></span></div>';
  h+='<div class="vs"><span class="p">'+d.pa+'</span><em>점</em><span class="p r">'+d.pb+'</span></div>';
  h+='<div class="vbar" aria-hidden="true"><i class="'+(d.a===V.me?'me':'')+'" style="flex-grow:'+(tot?d.pa:1)+'"></i><i class="'+(d.b===V.me?'me':'')+'" style="flex-grow:'+(tot?d.pb:1)+'"></i></div>';
  if(d.state==='done')h+='<p style="margin-top:8px"><b>'+(d.win?esc(V.byId[d.win].name)+' 님 승리':'무승부')+'</b></p>';
  return h+'</div>';
}
""")
cut("function modalDuel(V){", "function spinRoul(){", r"""function modalDuel(V){
  var f=S.duelF,b='<p class="hint">상대가 수락한 다음 날부터 2일 동안 얻은 점수의 합으로 겨룹니다.</p><div class="fld"><h3>상대</h3><div class="chips">';
  V.roster.forEach(function(m){if(m.id!==V.me)b+=chipBtn('duel-set','b',m.id,V.byId[m.id].name,f.b===m.id);});
  b+='</div></div>';
  return dlg('wide',{id:'duel',t:'1:1 대결 신청'},b,'<span class="hint">신청하면 상대에게 알림이 갑니다.</span><div class="df"><button class="btn primary" data-act="duel-add"'+(f.b?'':' disabled')+'>신청하기</button></div>');
}
""")
sub("""      var stx=F.stake==='text'?String(S.draft.duelStake||'').trim().slice(0,40):'';
      if(F.stake==='text'&&!stx){flash('벌칙 내용을 적어주세요.');break;}""", "      var stx='';")

# 도전: 빙고, 1:1 대결, 배지와 칭호를 따로 나눠 보기
i0 = s.index("function viewPlay(V){")
i1 = s.index("function wheelSvg(labels){")
s = s[:i0] + r"""var PLAYTABS=[['bingo','스터디 빙고'],['duel','1:1 대결'],['badge','배지와 칭호']];
function viewPlay(V){
  var t=today(),mon=mondayOf(t)<START?START:mondayOf(t),pt=PLAYTABS.some(function(x){return x[0]===S.playTab;})?S.playTab:'bingo';
  var pend=duelList(V).filter(function(d){return d.state==='pending'&&d.b===V.me;}).length;
  var h='<div class="view" id="view-play"><header class="vhead"><div><h1>도전</h1><p>'+({bingo:'매주 월요일에 바뀌는 빙고 판입니다. 기록으로 자동 계산됩니다.',duel:'한 명을 골라 2일 동안 얻은 점수로 겨룹니다.',badge:'기록이 쌓이면 배지를 받고, 받은 배지의 칭호를 이름 옆에 붙일 수 있습니다.'}[pt])+'</p></div>';
  h+='<div class="seg" role="group" aria-label="도전 종류">'+PLAYTABS.map(function(x){return '<button data-act="play-tab" data-id="'+x[0]+'" aria-pressed="'+(pt===x[0]?'true':'false')+'">'+x[1]+(x[0]==='duel'&&pend?'<b class="sbadge">'+pend+'</b>':'')+'</button>';}).join('')+'</div></header><div class="pwrap" id="pw-'+pt+'">';
  if(pt==='bingo'){
    var B=bingo(V,mon),me=B.per[V.me];
    h+='<section class="card" id="c-bingo-'+mon+'" style="--k:0"><div class="ct"><h2>스터디 빙고<small>'+esc(shortDate(mon)+' ~ '+shortDate(addDays(mon,6)))+'</small></h2><span class="tag a">'+me.lines+'줄, '+me.pts+'점</span></div><div class="bingo">';
    B.cells.forEach(function(c,i){h+='<div class="bcell'+(me.done[i]?' on':'')+'"><span>'+esc(c.t)+'</span><small>'+(me.done[i]?'완료':prog(c,me.vals[i]))+'</small></div>';});
    h+='</div><p class="hint">가로, 세로, 대각선 한 줄을 채울 때마다 주간 점수에 10점이 더해집니다. 판은 매주 월요일에 바뀝니다.</p><div class="sec"><h3>참여 인원 진행</h3>';
    V.roster.map(function(m){return {p:V.byId[m.id],b:B.per[m.id]};}).sort(function(a,b){return b.b.lines-a.b.lines||b.b.n-a.b.n;}).forEach(function(x){
      h+='<div class="brow">'+av(x.p,'s')+'<span>'+esc(x.p.name)+'</span><span class="mini" aria-hidden="true">'+x.b.done.map(function(d){return '<i class="'+(d?'on':'')+'"></i>';}).join('')+'</span><small>'+x.b.n+'칸, '+x.b.lines+'줄</small></div>';
    });
    h+='</div></section>';
  }else if(pt==='duel'){
    h+='<section class="card" id="c-duels" style="--k:0"><div class="ct"><h2>1:1 대결</h2><button class="btn small primary" data-act="open" data-modal="duel"'+(V.roster.length<2?' disabled':'')+'>대결 신청</button></div>';
    var dl=duelList(V).filter(function(d){return d.state!=='done'||diffDays(d.end,t)<=14;}).slice(0,8);
    if(!dl.length)h+='<p class="empty">아직 대결이 없습니다. 한 명을 골라 2일 동안의 점수로 겨뤄보세요.</p>';
    dl.forEach(function(d){h+=duelRow(V,d);});
    var wins={};duelList(V).forEach(function(d){if(d.state==='done'&&d.win)wins[d.win]=(wins[d.win]||0)+1;});
    h+='<div class="sec"><h3>대결 전적</h3>';
    V.roster.forEach(function(m){h+='<div class="brow">'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+'</span><span></span><small>'+(wins[m.id]||0)+'승</small></div>';});
    h+='</div></section>';
  }else{
    var bl=badgeList(V,V.me),mt=obj(V.progress[V.me]).title,got=bl.filter(function(b){return b.on;}).length;
    h+='<section class="card" id="c-badges" style="--k:0"><div class="ct"><h2>배지와 칭호<small>'+got+' / '+bl.length+'</small></h2></div><div class="bdgs">';
    bl.forEach(function(b){
      if(b.on)h+='<button class="bdg on" data-act="badge-title" data-id="'+b.id+'" aria-pressed="'+(mt===b.id?'true':'false')+'"><b>'+esc(b.name)+'</b><small>칭호: '+esc(b.title)+'</small></button>';
      else h+='<div class="bdg"><b>'+esc(b.name)+'</b><small>'+esc(b.desc)+'</small><small>'+prog(b,b.v)+'</small></div>';
    });
    h+='</div><p class="hint" style="margin-top:10px">받은 배지를 누르면 그 칭호가 이름 옆에 붙습니다. 한 번 더 누르면 뗍니다.</p><div class="sec"><h3>참여 인원 배지</h3>';
    V.roster.forEach(function(m){var n=badgeList(V,m.id).filter(function(b){return b.on;}).length;h+='<div class="brow">'+av(V.byId[m.id],'s')+'<span>'+esc(V.byId[m.id].name)+' '+titleTag(V,m.id)+'</span><span></span><small>'+n+'개</small></div>';});
    h+='</div></section>';
  }
  return h+'</div></div>';
}
""" + s[i1:]
sub("    case 'note-open':{\n      var ntab=el.getAttribute('data-tab')||'chat',nid=el.getAttribute('data-n');",
    "    case 'note-open':{\n      var ntab=el.getAttribute('data-tab')||'chat',nid=el.getAttribute('data-n');\n      if(ntab==='play'){S.playTab=String(nid||'').indexOf('bd')===0?'badge':'duel';lsSet('gbb_playtab',S.playTab);}")
sub("    case 'timer-stop':stopTimer();break;",
    "    case 'timer-stop':stopTimer();break;\n    case 'play-tab':if(PLAYTABS.some(function(x){return x[0]===id;})){S.playTab=id;lsSet('gbb_playtab',id);}break;\n    case 'tstyle':{var tsv=el.getAttribute('data-v');if(TSTYLES.some(function(x){return x[0]===tsv;})){S.tstyle=tsv;lsSet('gbb_tstyle',tsv);}break;}")
sub("S.tstyle=lsGet('gbb_tstyle')||'ring';", "S.tstyle=lsGet('gbb_tstyle')||'ring';S.playTab=lsGet('gbb_playtab')||'bingo';")

# 참여 인원 삭제: 나와 방장을 뺀 다른 사람은 누구나 삭제할 수 있게 (두 번 눌러야 삭제)
sub("+(isAdm&&m.id!==V.me?'<button class=\"del\" data-act=\"member-del\" data-id=\"'+esc(m.id)+'\"'+dis+'>'+(S.confirm==='mem:'+m.id?'한 번 더 누르면 삭제':'삭제')+'</button>':'')",
    "+(V.me&&m.id!==V.me&&(isAdm||m.id!==adm)?'<button class=\"btn small'+(S.confirm==='mem:'+m.id?' warn':'')+'\" data-act=\"member-del\" data-id=\"'+esc(m.id)+'\"'+dis+'>'+(S.confirm==='mem:'+m.id?'한 번 더 누르면 삭제':'삭제')+'</button>':'')")
sub("다른 사람의 이름 수정과 삭제, 비밀번호 초기화는 '+esc(V.byId[adm].name)+' 님만 할 수 있습니다.",
    "그만두는 사람은 옆의 삭제를 두 번 눌러 목록에서 뺄 수 있습니다. 다른 사람 이름 수정과 비밀번호 초기화, '+esc(V.byId[adm].name)+' 님 삭제는 '+esc(V.byId[adm].name)+' 님만 할 수 있습니다.")
sub("""      var Vmd=view();if(!Vmd.me||adminId(Vmd)!==Vmd.me||id===Vmd.me)break;
      if(prev==='mem:'+id){editCfg(function(c){c.roster=c.roster.filter(function(m){return m&&m.id!==id;});});if(canWrite()&&Vmd.locks[id])save('locks/'+id,null);}""",
    """      var Vmd=view();if(!Vmd.me||id===Vmd.me||!Vmd.byId[id]||(id===adminId(Vmd)&&adminId(Vmd)!==Vmd.me))break;
      if(prev==='mem:'+id){var dnm=Vmd.byId[id].name;editCfg(function(c){c.roster=c.roster.filter(function(m){return m&&m.id!==id;});});if(canWrite()&&Vmd.locks[id])save('locks/'+id,null);if(canWrite()&&Vmd.live[id])save('live/'+id,null);if(canWrite())flash(dnm+' 님을 참여 인원에서 뺐습니다.');}""")

# 설정 > 화면: 타이머 모양 고르기
sub("aria-label=\"파스텔 대표 색\">'+sws('p')+'</div></div>';",
    "aria-label=\"파스텔 대표 색\">'+sws('p')+'</div><h4 class=\"lb\">타이머 모양</h4><div class=\"cvs tsv\" role=\"group\" aria-label=\"타이머 모양\">'+TSTYLES.map(function(x){return '<button class=\"cv\" data-act=\"tstyle\" data-v=\"'+x[0]+'\" aria-pressed=\"'+(tstyle()===x[0]?'true':'false')+'\"><span class=\"tsp tsp-'+x[0]+'\" aria-hidden=\"true\">'+TSPREV[x[0]]+'</span>'+x[1]+'</button>';}).join('')+'</div></div>';")
sub("var TSTYLES=[", "var TSPREV={ring:'<svg viewBox=\"0 0 48 48\"><circle class=\"k\" cx=\"24\" cy=\"24\" r=\"17\"/><path class=\"a\" d=\"M24,7 A17,17 0 1,1 7,24\"/></svg>',digits:'<b>25:00</b>',bar:'<b>25:00</b><i><u></u></i>',pie:'<svg viewBox=\"0 0 48 48\"><circle class=\"f\" cx=\"24\" cy=\"24\" r=\"19\"/><path class=\"w\" d=\"M24,24 L24,8 A16,16 0 0,1 40,24 Z\"/><circle class=\"n\" cx=\"24\" cy=\"24\" r=\"2.4\"/></svg>',flip:'<b><i>2</i><i>5</i><em>:</em><i>0</i><i>0</i></b>'};\nvar TSTYLES=[")
