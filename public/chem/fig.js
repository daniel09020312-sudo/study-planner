/* 한 입 화학: 노트 그림 (색은 CSS 변수) */
(function () {
  'use strict';
  var M = function (k, o) { return window.MOL.svg(k, o); };
  function row(items) { return '<div class="frow">' + items.join('') + '</div>'; }
  function arrow(label) { return '<div class="farr"><span>' + (label || '') + '</span><svg viewBox="0 0 40 12" width="40" height="12"><path d="M1 6h34M30 1l6 5-6 5" /></svg></div>'; }
  function plus() { return '<div class="fplus">+</div>'; }

  var F = {};
  F.resp = function () {
    return '<svg class="fig" viewBox="0 0 340 150">' +
      '<g class="fa"><rect x="10" y="40" width="110" height="64" rx="32" class="fill-g"/><text x="65" y="68" class="ft b">엽록체</text><text x="65" y="86" class="ft s">광합성</text></g>' +
      '<g class="fa"><rect x="220" y="40" width="110" height="64" rx="32" class="fill-r"/><text x="65" y="68" class="ft b" transform="translate(210 0)">미토콘드리아</text><text x="275" y="86" class="ft s">세포 호흡</text></g>' +
      '<path class="fl ar" d="M122 58 Q170 30 218 58"/><text x="170" y="30" class="ft s">포도당 + O₂</text>' +
      '<path class="fl ar" d="M218 88 Q170 118 122 88"/><text x="170" y="128" class="ft s">CO₂ + H₂O</text>' +
      '<path class="fl ar dash" d="M65 10 L65 36"/><text x="80" y="18" class="ft s l">빛에너지</text>' +
      '<path class="fl ar" d="M275 106 L275 134"/><text x="290" y="132" class="ft s l">에너지</text>' +
      '</svg>';
  };
  F.ncycle = function () {
    var nodes = [['N₂', '공기 중 질소'], ['NH₃', '암모니아'], ['NH₄⁺', '암모늄 이온'], ['NO₃⁻', '질산 이온'], ['아미노산 등', '질소동화 산물']];
    var labels = [['질소 고정', '뿌리혹세균 · 환원 (0 → -3)', 'cb'], ['토양', '산화·환원 아님 (-3 → -3)', ''], ['질산화 작용', '질산화 세균 · 산화 (-3 → +5)', 'cr'], ['식물이 흡수', '단백질의 재료로', '']];
    var s = '<svg class="fig" viewBox="0 0 340 344">', H = 72;
    for (var i = 0; i < nodes.length; i++) {
      var y = 8 + i * H;
      s += '<g class="fa" style="--d:' + i + '"><rect x="24" y="' + y + '" width="124" height="40" rx="20" class="fill-' + (i === 4 ? 'a' : i === 0 ? 'g' : 'b') + '"/><text x="86" y="' + (y + 18) + '" class="ft b">' + nodes[i][0] + '</text><text x="86" y="' + (y + 32) + '" class="ft xs">' + nodes[i][1] + '</text></g>';
      if (i < labels.length) {
        s += '<path class="fl ar" d="M86 ' + (y + 42) + ' V' + (y + H - 4) + '"/>';
        s += '<text x="104" y="' + (y + 55) + '" class="ft s l ' + labels[i][2] + '">' + labels[i][0] + '</text><text x="104" y="' + (y + 68) + '" class="ft xs l">' + labels[i][1] + '</text>';
      }
    }
    return s + '</svg>';
  };
  F.shapes = function () {
    function dot(x, y) { return '<circle cx="' + x + '" cy="' + y + '" r="7" class="atom"/>'; }
    function ln(a, b, c, d, n) {
      var o = '';
      if (!n || n === 1) return '<line class="fl" x1="' + a + '" y1="' + b + '" x2="' + c + '" y2="' + d + '"/>';
      var dx = c - a, dy = d - b, L = Math.sqrt(dx * dx + dy * dy), px = -dy / L, py = dx / L;
      var offs = n === 2 ? [-2.2, 2.2] : [-3.6, 0, 3.6];
      offs.forEach(function (k) { o += '<line class="fl" x1="' + (a + px * k) + '" y1="' + (b + py * k) + '" x2="' + (c + px * k) + '" y2="' + (d + py * k) + '"/>'; });
      return o;
    }
    var s = '<svg class="fig" viewBox="0 0 340 210">';
    // 사슬
    var cx = [18, 44, 70, 96, 122], i;
    for (i = 0; i < 4; i++) s += ln(cx[i], 30, cx[i + 1], 30);
    cx.forEach(function (x) { s += dot(x, 30); });
    s += '<text x="70" y="58" class="ft s">사슬 모양</text>';
    // 가지
    var bx = [190, 216, 242, 268];
    for (i = 0; i < 3; i++) s += ln(bx[i], 30, bx[i + 1], 30);
    s += ln(229, 30, 229, 8) + ln(229, 30, 229, 52);
    bx.forEach(function (x) { s += dot(x, 30); });
    s += dot(229, 8) + dot(229, 52) + '<text x="229" y="74" class="ft s">가지 달린 구조</text>';
    // 고리
    var pts = [];
    for (i = 0; i < 6; i++) { var a = (i * 60 - 90) * Math.PI / 180; pts.push([70 + 24 * Math.cos(a), 128 + 24 * Math.sin(a)]); }
    for (i = 0; i < 6; i++) s += ln(pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1]);
    pts.forEach(function (p) { s += dot(p[0], p[1]); });
    s += '<text x="70" y="176" class="ft s">고리 모양</text>';
    // 2중
    s += ln(190, 118, 222, 118, 2) + ln(222, 118, 254, 118) + ln(254, 118, 286, 118, 2);
    [190, 222, 254, 286].forEach(function (x) { s += dot(x, 118); });
    s += '<text x="238" y="140" class="ft s">2중 결합</text>';
    s += ln(190, 172, 222, 172) + ln(222, 172, 254, 172, 3) + ln(254, 172, 286, 172);
    [190, 222, 254, 286].forEach(function (x) { s += dot(x, 172); });
    s += '<text x="238" y="194" class="ft s">3중 결합</text>';
    return s + '</svg>';
  };
  F.tower = function () {
    var fr = [['석유 가스', '1~4', '25℃ 이하', '가정용 연료'], ['나프타', '5~10', '40~160℃', '자동차 연료·화학 원료'], ['등유', '11~15', '160~250℃', '항공기 연료'], ['경유', '16~20', '250~300℃', '디젤 차량 연료'], ['중유', '21~25', '300~350℃', '선박 연료'], ['아스팔트', '25 이상', '350℃ 이상', '도로 포장']];
    var s = '<svg class="fig" viewBox="0 0 340 300"><defs><linearGradient id="tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="tg0"/><stop offset="1" class="tg1"/></linearGradient></defs>';
    s += '<rect x="20" y="14" width="64" height="270" rx="30" fill="url(#tg)" class="tower"/>';
    s += '<text x="52" y="296" class="ft xs">가열 ↑ 원유</text>';
    for (var i = 0; i < fr.length; i++) {
      var y = 34 + i * 44;
      s += '<g class="fa" style="--d:' + i + '"><path class="fl" d="M84 ' + y + ' H112"/><circle cx="112" cy="' + y + '" r="3" class="dotc"/>' +
        '<text x="120" y="' + (y - 2) + '" class="ft b l">' + fr[i][0] + '</text>' +
        '<text x="120" y="' + (y + 13) + '" class="ft xs l">C ' + fr[i][1] + ' · ' + fr[i][2] + '</text>' +
        '<text x="334" y="' + (y + 5) + '" class="ft s r">' + fr[i][3] + '</text></g>';
    }
    s += '<text x="52" y="10" class="ft xs">낮다</text>';
    return s + '</svg>';
  };
  F.fuel = function () {
    return '<svg class="fig fuel" viewBox="0 0 340 220">' +
      '<rect x="60" y="40" width="220" height="150" rx="14" class="cellbox"/>' +
      '<rect x="100" y="48" width="16" height="134" class="elec"/><rect x="224" y="48" width="16" height="134" class="elec"/>' +
      '<rect x="120" y="48" width="100" height="134" class="elyte"/><text x="170" y="176" class="ft xs">전해질</text>' +
      '<path class="wire" d="M108 46 V18 H232 V46"/>' +
      '<circle cx="170" cy="18" r="9" class="bulb"/><path class="bulbray" d="M170 2v-0M158 6l-3-3M182 6l3-3"/>' +
      '<text x="96" y="14" class="ft s">(-)극</text><text x="246" y="14" class="ft s">(+)극</text>' +
      '<text x="108" y="200" class="ft xs cr">산화</text><text x="232" y="200" class="ft xs cb">환원</text>' +
      '<text x="30" y="96" class="ft b">H₂</text><path class="fl ar" d="M42 104 H96"/>' +
      '<text x="312" y="96" class="ft b">O₂</text><path class="fl ar" d="M300 104 H246"/>' +
      '<path class="fl ar" d="M246 150 H300"/><text x="314" y="146" class="ft s">H₂O</text>' +
      '<g class="mov hp"><circle r="9" class="ion"/><text class="ft xs ionl" y="3.5">H⁺</text></g>' +
      '<g class="mov hp hp2"><circle r="9" class="ion"/><text class="ft xs ionl" y="3.5">H⁺</text></g>' +
      '<g class="mov el"><circle r="5" class="eln"/><text class="ft xs" y="-8">e⁻</text></g>' +
      '<text x="170" y="214" class="ft xs">H₂ → 2H⁺ + 2e⁻  ·  4H⁺ + O₂ + 4e⁻ → 2H₂O</text>' +
      '</svg>';
  };
  F.oxid = function () {
    return '<div class="fgrid3">' +
      '<div class="fcell">' + M('methanol') + '<b>메탄올</b><small>C: -2</small></div>' + arrow('산화') +
      '<div class="fcell">' + M('formaldehyde') + '<b>폼알데하이드</b><small>C: 0</small></div>' + arrow('산화') +
      '<div class="fcell">' + M('formic') + '<b>폼산</b><small>C: +2</small></div>' +
      '<div class="fcell">' + M('ethanol') + '<b>에탄올</b></div>' + arrow('산화') +
      '<div class="fcell">' + M('acetaldehyde') + '<b>아세트알데하이드</b></div>' + arrow('산화') +
      '<div class="fcell">' + M('acetic') + '<b>아세트산</b></div></div>';
  };
  F.mirror = function () {
    var tubes = [['질산 은', 'clear'], ['+ 암모니아수', 'clear'], ['+ 포도당', 'clear'], ['+ NaOH', 'murk'], ['흔들기', 'mirror']];
    var s = '<svg class="fig" viewBox="0 0 340 160">';
    tubes.forEach(function (t, i) {
      var x = 22 + i * 66;
      s += '<g class="fa" style="--d:' + i + '"><path class="tube" d="M' + x + ' 30 V112 a14 14 0 0 0 28 0 V30"/>' +
        '<path class="liq ' + t[1] + '" d="M' + (x + 2) + ' ' + (t[1] === 'mirror' ? 36 : 80) + ' V112 a12 12 0 0 0 24 0 V' + (t[1] === 'mirror' ? 36 : 80) + ' Z"/>' +
        '<text x="' + (x + 14) + '" y="150" class="ft xs">' + t[0] + '</text></g>';
      if (i < 4) s += '<path class="fl ar" d="M' + (x + 34) + ' 72 H' + (x + 60) + '"/>';
    });
    return s + '</svg>';
  };
  var A = function (src, o) { return window.MOL.ascii(src, o); };
  F.ester = function () {
    var acid = A('     O\n     ‖\nCH3--C--OH', { hl: [[2, 8, 2, 9]] }), alc = A('H--O--C2H5', { hl: [[0, 0, 0, 0]] });
    return row(['<div class="fcell">' + acid + '<b>아세트산</b><small>-OH를 내놓음</small></div>', plus(), '<div class="fcell">' + alc + '<b>에탄올</b><small>H를 내놓음</small></div>', arrow('진한 H₂SO₄ · 가열'), '<div class="fcell">' + M('ethylacetate') + '<b>아세트산 에틸</b><small>사과 향</small></div>', plus(), '<div class="fbox">H₂O</div>']);
  };
  F.wine = function () {
    return row(['<div class="fbox">포도<small>당</small></div>', arrow('발효(효모)'), '<div class="fbox">포도주<small>에탄올 + CO₂</small></div>', arrow('발효·산화'), '<div class="fbox">포도 식초<small>아세트산</small></div>']);
  };
  F.addpoly = function () {
    var mono = A('   *  *\n   |  |\n*--C==C--*\n   |  |\n   *  *');
    var poly = A('   *  *  *  *\n   |  |  |  |\n*--C--C--C--C--*\n   |  |  |  |\n   *  *  *  *');
    return row(['<div class="fcell">' + mono + '<small>단위체(C=C)</small></div>', plus(), '<div class="fcell">' + mono + '<small>단위체</small></div>', arrow('첨가 중합'), '<div class="fcell">' + poly + '<small>고분자(단일 결합)</small></div>']);
  };
  F.condpoly = function () {
    return row(['<div class="fbox">단위체–<mark>OH</mark></div>', plus(), '<div class="fbox"><mark>H</mark>–단위체</div>', arrow('축합 중합'), '<div class="fbox">단위체–단위체</div>', plus(), '<div class="fbox">H₂O</div>']);
  };
  F.nucleo = function () {
    return '<svg class="fig" viewBox="0 0 340 130">' +
      '<circle cx="60" cy="60" r="30" class="fill-a"/><text x="60" y="64" class="ft b">인산</text>' +
      '<path class="fl" d="M90 60 H128"/>' +
      '<path d="M170 30 L204 54 L192 94 L148 94 L136 54 Z" class="fill-b"/><text x="170" y="72" class="ft b">당</text>' +
      '<path class="fl" d="M204 62 H240"/>' +
      '<rect x="240" y="38" width="80" height="48" rx="8" class="fill-r"/><text x="280" y="66" class="ft b">염기</text>' +
      '<text x="170" y="122" class="ft xs">뉴클레오타이드</text></svg>';
  };
  F.backbone = function () {
    var s = '<svg class="fig" viewBox="0 0 340 190">';
    for (var i = 0; i < 3; i++) {
      var y = 26 + i * 56;
      s += '<g class="fa" style="--d:' + i + '"><circle cx="70" cy="' + y + '" r="18" class="fill-a"/><text x="70" y="' + (y + 4) + '" class="ft xs">인산</text>' +
        '<path class="fl" d="M84 ' + (y + 12) + ' L112 ' + (y + 26) + '"/>' +
        '<path d="M130 ' + (y + 12) + ' l18 13 -7 21 h-22 l-7 -21z" class="fill-b"/><text x="130" y="' + (y + 32) + '" class="ft xs">당</text>' +
        '<path class="fl" d="M148 ' + (y + 30) + ' H196"/><rect x="196" y="' + (y + 18) + '" width="58" height="24" rx="6" class="fill-r"/><text x="225" y="' + (y + 34) + '" class="ft xs">염기</text>';
      if (i < 2) s += '<path class="fl" d="M124 ' + (y + 46) + ' L84 ' + (y + 46) + '"/>';
      s += '</g>';
    }
    s += '<text x="100" y="186" class="ft xs cb">인산과 당이 번갈아 이어진 당-인산 골격</text>';
    return s + '</svg>';
  };
  F.pairs = function () {
    var s = '<svg class="fig" viewBox="0 0 340 150">';
    var pr = [['A', 'T', 2], ['G', 'C', 3], ['T', 'A', 2], ['C', 'G', 3]];
    pr.forEach(function (p, i) {
      var y = 20 + i * 32;
      s += '<rect x="40" y="' + y + '" width="14" height="22" class="elec"/><rect x="286" y="' + y + '" width="14" height="22" class="elec"/>' +
        '<rect x="58" y="' + (y + 1) + '" width="72" height="20" rx="5" class="fill-' + (p[0] === 'A' || p[0] === 'T' ? 'r' : 'b') + '"/><text x="94" y="' + (y + 15) + '" class="ft b">' + p[0] + '</text>' +
        '<rect x="210" y="' + (y + 1) + '" width="72" height="20" rx="5" class="fill-' + (p[1] === 'A' || p[1] === 'T' ? 'r' : 'b') + '"/><text x="246" y="' + (y + 15) + '" class="ft b">' + p[1] + '</text>';
      for (var k = 0; k < p[2]; k++) { var yy = y + 11 + (k - (p[2] - 1) / 2) * 5; s += '<path class="hb" d="M134 ' + yy + ' H206"/>'; }
      s += '<text x="170" y="' + (y - 1) + '" class="ft xs">' + (p[2] === 2 ? '수소 결합 2개' : '수소 결합 3개') + '</text>';
    });
    s += '<text x="47" y="148" class="ft xs">골격</text><text x="293" y="148" class="ft xs">골격</text>';
    return s + '</svg>';
  };
  F.pe = function () {
    return row(['<div class="fcell">' + M('ethylene') + '<b>에틸렌</b></div>', plus(), '<div class="fcell">' + M('ethylene') + '<b>에틸렌</b></div>', arrow('첨가 중합'), '<div class="fcell">' + M('pe') + '<b>폴리에틸렌</b></div>']);
  };
  F.pvc = function () {
    return row(['<div class="fcell">' + M('vinylchloride') + '<b>염화 바이닐</b></div>', arrow('첨가 중합'), '<div class="fcell">' + M('pvc') + '<b>PVC</b></div>']);
  };
  F.drugdev = function () {
    var st = ['기초 탐색 및\n원천 기술 연구', '개발 후보\n물질 선정', '전임상(비임상)\n시험', '임상 시험', '신약 허가\n및 시판'];
    var s = '<svg class="fig" viewBox="0 0 340 120"><path class="fl" d="M30 40 H310"/>';
    st.forEach(function (t, i) {
      var x = 30 + i * 70, l = t.split('\n');
      s += '<g class="fa" style="--d:' + i + '"><circle cx="' + x + '" cy="40" r="13" class="fill-b"/><text x="' + x + '" y="45" class="ft b">' + (i + 1) + '</text>' +
        '<text x="' + x + '" y="74" class="ft xs">' + l[0] + '</text>' + (l[1] ? '<text x="' + x + '" y="88" class="ft xs">' + l[1] + '</text>' : '') + '</g>';
    });
    return s + '</svg>';
  };
  window.FIG = F;
})();
