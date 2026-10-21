# ---------------------------------------------------------------- 과목 줄임말을 각자 정하기 (설정 > 과목 색과 줄임말)
sub("[['fixed','고정 시간표'],['color','과목 색'],['win','공부 시간']]", "[['fixed','고정 시간표'],['color','색과 줄임말'],['win','공부 시간']]")
sub("""<p class="hint" style="margin:14px 0 4px">시간표와 할 일 목록에 쓰는 내 과목 색입니다. 과목이 없거나 수행평가 같은 기타 일은 회색으로 보입니다.</p>""",
    """<p class="hint" style="margin:14px 0 4px">시간표와 할 일 목록에 쓰는 내 과목 색입니다. 줄임말은 달력 칸에 보이는 짧은 이름이고 3글자까지 쓸 수 있습니다. 둘 다 나에게만 적용됩니다.</p>""")
sub("""      b+='<div class="scrow"><span><i style="background:'+cur+'"></i>'+esc(s.name)+'</span><div class="sws">'""",
    """      var ab=String(obj(obj(V.progress[V.me]).abbr)[s.id]||''),abd=subShort(s.name);
      b+='<div class="scrow"><span><i style="background:'+cur+'"></i>'+esc(s.name)+'</span><label class="abin"><span>줄임말</span><input type="text" maxlength="3" value="'+esc(ab)+'" placeholder="'+esc(abd)+'" class="abin-in" data-id="'+esc(s.id)+'" aria-label="'+esc(s.name)+' 줄임말"></label><div class="sws">'""")
# 줄임말 칸은 창을 닫으면서 바뀌는 일이 많아서, change를 따로 받아 한 박자 늦게 저장한다
sub("    case 'pick-date':", "    case 'abbr-open':S.ttTab='color';openModal('ttset',el);return;\n    case 'pick-date':")
