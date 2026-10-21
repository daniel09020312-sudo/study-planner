# ---------------------------------------------------------------- 과목 색: 기본은 과목 순서대로 무지개, 고를 수 있는 색 넓히기, 직접 색상 코드
PAL_JS = open(BASE + '/src/palette.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", PAL_JS + "\n/* ---------- 공부방 ---------- */")
cut("function subCol(V,sid){", "function isEtcGoal(g){", r"""function subCol(V,sid){
  if(!sid||!V.subById[sid])return SGRAY;
  var my=obj(obj(V.progress[V.me]).scol)[sid];
  if(my==='g')return SGRAY;
  if(hexOk(my))return my;
  for(var i=0;i<SCOLS.length;i++)if(SCOLS[i][0]===my)return SCOLS[i][1];
  var k=V.subs.indexOf(V.subById[sid]);return DEF_RAINBOW[(k<0?0:k)%DEF_RAINBOW.length];
}
""")
cut("  }else if(tab==='color'){", "  }else{\n    var w=ttWin(V);", r"""  }else if(tab==='color'){
    b+='<p class="hint" style="margin:14px 0 6px">시간표, 할 일, 달력에 쓰는 내 과목 색과 줄임말입니다. 줄임말은 달력 칸에 보이는 짧은 이름이고 3글자까지 쓸 수 있습니다. 둘 다 나에게만 적용됩니다.</p>';
    b+='<div class="row" style="margin-bottom:4px"><button class="btn small'+(S.confirm==='scolreset'?' warn':'')+'" data-act="scol-reset">'+(S.confirm==='scolreset'?'한 번 더 누르면 모든 과목 색을 무지개 순서로 바꿉니다':'무지개 순서로 다시 맞추기')+'</button></div><div class="scols">';
    V.subs.forEach(function(s){
      var cur=subCol(V,s.id),open=S.scolOpen===s.id,ab=String(obj(obj(V.progress[V.me]).abbr)[s.id]||''),abd=subShort(s.name);
      b+='<div class="scrow'+(open?' open':'')+'" id="scr-'+esc(s.id)+'"><span><i style="background:'+cur+'"></i>'+esc(s.name)+'</span><div class="scctl"><label class="abin"><span>줄임말</span><input type="text" maxlength="3" value="'+esc(ab)+'" placeholder="'+esc(abd)+'" class="abin-in" data-id="'+esc(s.id)+'" aria-label="'+esc(s.name)+' 줄임말"></label><button class="btn small scbtn" data-act="scol-open" data-id="'+esc(s.id)+'" aria-expanded="'+(open?'true':'false')+'"><i style="background:'+cur+'"></i>'+(open?'닫기':'색 바꾸기')+'</button></div>';
      if(open){
        b+='<div class="scpal">';
        PALS.forEach(function(g){b+='<div class="spg"><small>'+g.n+'</small><div class="sws">'+g.c.map(function(c){return '<button class="sw2" data-act="scol" data-id="'+esc(s.id)+'" data-v="'+c[0]+'" style="--c:'+c[0]+'" aria-pressed="'+(cur.toUpperCase()===c[0].toUpperCase()?'true':'false')+'" aria-label="'+esc(s.name)+' '+c[1]+'" title="'+c[1]+'"></button>';}).join('')+'</div></div>';});
        b+='<div class="spg"><small>직접 고르기</small><div class="sccustom"><input type="color" class="scpick" data-id="'+esc(s.id)+'" value="'+(hexOk(cur)?cur:'#9AA1AD')+'" aria-label="'+esc(s.name)+' 색 직접 고르기"><input type="text" class="hexin" data-id="'+esc(s.id)+'" maxlength="7" value="'+esc(String(cur).toUpperCase())+'" spellcheck="false" autocapitalize="off" aria-label="'+esc(s.name)+' 색상 코드"><button class="sw2" data-act="scol" data-id="'+esc(s.id)+'" data-v="g" style="--c:'+SGRAY+'" aria-pressed="'+(cur===SGRAY?'true':'false')+'" aria-label="'+esc(s.name)+' 회색" title="회색"></button></div></div>';
        b+='</div>';
      }
      b+='</div>';
    });
    b+='</div>';
""")
sub("    case 'pick-date':", "    case 'scol-open':S.scolOpen=S.scolOpen===id?null:id;break;\n    case 'scol-reset':if(prev!=='scolreset'){S.confirm='scolreset';break;}editProg(function(p){delete p.scol;});if(canWrite())flash('과목 색을 무지개 순서로 맞췄습니다.');break;\n    case 'pick-date':")
# 단원 진도 단추: 색 위 글자를 밝기에 맞게
sub("""h+='<section class="card usub" id="us-'+esc(s.id)+'" style="--k:'+Math.min(k+1,6)+';--sc:'+col+'">""", """h+='<section class="card usub" id="us-'+esc(s.id)+'" style="--k:'+Math.min(k+1,6)+';--sc:'+col+';--fg:'+fgOn(col)+'">""")
# 설정에서도 바로 가기
sub("""  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3>""", """  if(V.me)b+='<div class="fld"><h3>과목 색과 줄임말<small>나에게만 적용</small></h3><div class="row"><button class="btn small" data-act="abbr-open">바꾸기</button></div></div>';
  b+='<div class="sec"><h3>화면<small>이 기기에만 적용</small></h3>""")
