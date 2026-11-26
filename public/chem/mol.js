/* 한 입 화학: 구조식 그리기
   글자 그림(ASCII)이나 좌표로 적은 분자를 SVG로 바꾼다.
   결합 글자: - = ≡ (가로)  | ‖ (세로)  / \ (대각선)
   원자 글자: 영문, 숫자(원소 뒤면 아래 첨자), ( ) [ ] ' ^+ ^-  */
(function () {
  'use strict';
  var CW = 11, RH = 16, U = 34, FS = 15;
  var BONDS = { '-': [1, 'h'], '=': [2, 'h'], '≡': [3, 'h'], '|': [1, 'v'], '‖': [2, 'v'], '/': [1, 'u'], '\\': [1, 'd'], '~': [0, 'h'], '¦': [0, 'v'] };
  var DIRS = { h: [[0, -1], [0, 1]], v: [[-1, 0], [1, 0]], u: [[-1, 1], [1, -1]], d: [[-1, -1], [1, 1]] };

  function cw(ch, kind) {
    if (kind === 'sub' || kind === 'sup') return /[0-9]/.test(ch) ? 6.4 : 6.8;
    if (ch === 'l' || ch === 'i') return 4.2;
    if (ch === "'") return 3.5;
    if (ch === '(' || ch === ')' || ch === '[' || ch === ']') return 5.2;
    if (/[A-Z]/.test(ch)) return ch === 'O' ? 11.4 : ch === 'I' ? 4.6 : 10.2;
    return 8;
  }
  // 글자 하나하나를 어디에 둘지(첫 글자의 가운데 = x0)
  function layout(text, x0, y) {
    var out = [], prev = null, x = x0, kind;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (ch === '^') { // ^+  ^-  ^2-
        var j = i + 1, s = '';
        while (j < text.length && /[0-9+\-]/.test(text[j])) { s += text[j]; j++; if (/[+\-]/.test(text[j - 1])) break; }
        for (var k = 0; k < s.length; k++) push(s[k], 'sup');
        i = j - 1; continue;
      }
      kind = 'n';
      if (/[0-9]/.test(ch) && prev && /[A-Za-z)\]]/.test(prev.ch) && prev.ch !== 'R' || /[0-9]/.test(ch) && prev && prev.kind === 'sub') kind = 'sub';
      if (/[0-9]/.test(ch) && prev && prev.ch === 'R') kind = 'sub';
      if (ch === 'n' && prev && (prev.ch === ']' || prev.ch === ')')) kind = 'sub';
      push(ch, kind);
    }
    function push(ch, kind) {
      var w = cw(ch, kind);
      if (out.length) x += (out[out.length - 1].w + w) / 2;
      var o = { ch: ch, kind: kind, w: w, x: x, y: y };
      out.push(o); prev = o;
    }
    return out;
  }
  function tokenBox(chars) {
    var a = chars[0], b = chars[chars.length - 1];
    return { l: a.x - a.w / 2, r: b.x + b.w / 2 };
  }

  /* 글자 그림 읽기 */
  function parseAscii(src) {
    var rows = src.replace(/^\n+|\s+$/g, '').split('\n');
    var R = rows.length, C = 0;
    rows.forEach(function (r) { if (r.length > C) C = r.length; });
    var cell = [], toks = [], atomRe = /[A-Za-z0-9()\[\]'^*?]/, blanks = {}, nb = 0;
    for (var r0 = 0; r0 < R; r0++) for (var c0 = 0; c0 < rows[r0].length; c0++) {
      var bc = rows[r0][c0];
      if (bc === '?' || (bc === '~' && rows[r0][c0 - 1] !== '~') || (bc === '¦' && !(rows[r0 - 1] && rows[r0 - 1][c0] === '¦'))) blanks[r0 + ',' + c0] = nb++;
    }
    for (var r = 0; r < R; r++) {
      cell.push([]);
      var row = rows[r];
      for (var c = 0; c < row.length; c++) {
        var ch = row[c];
        if (atomRe.test(ch)) {
          var start = c, s = '';
          if (ch === '?') { s = '?'; c++; }
          else while (c < row.length && row[c] !== '?' && (atomRe.test(row[c]) || (/[+\-]/.test(row[c]) && row[c - 1] === '^'))) { s += row[c]; c++; }
          c--;
          var t = { text: s, r: r, c0: start, c1: c, id: toks.length };
          if (s === '?') t.blank = blanks[r + ',' + start];
          toks.push(t);
          for (var k = start; k <= c; k++) cell[r][k] = t;
        }
      }
    }
    // 원자 글자 배치: 첫 글자 가운데를 그 칸 가운데에
    toks.forEach(function (t) {
      if (t.blank != null) { t.chars = [{ ch: '?', kind: 'b', w: 30, x: t.c0 * CW + CW / 2, y: t.r * RH + RH / 2 }]; return; }
      if (t.text === '*') { t.chars = [{ ch: '', kind: 'v', w: 0, x: t.c0 * CW + CW / 2, y: t.r * RH + RH / 2 }]; t.vertex = true; return; }
      t.chars = layout(t.text, t.c0 * CW + CW / 2, t.r * RH + RH / 2);
    });
    var bonds = [], seen = {};
    for (r = 0; r < R; r++) {
      for (c = 0; c < rows[r].length; c++) {
        ch = rows[r][c];
        var B = BONDS[ch];
        if (!B || cell[r][c] || seen[r + ',' + c]) continue;
        if (ch === '-' && rows[r][c - 1] === '^') continue;
        var dirs = DIRS[B[1]], ends = [];
        for (var d = 0; d < 2; d++) {
          var rr = r, cc = c, dr = dirs[d][0], dc = dirs[d][1], hit = null, n = 0;
          while (n++ < 40) {
            seen[rr + ',' + cc] = 1;
            rr += dr; cc += dc;
            if (rr < 0 || rr >= R || cc < 0) break;
            var tk = cell[rr] && cell[rr][cc];
            if (tk) { hit = { t: tk, idx: cc - tk.c0 }; break; }
            var ch2 = rows[rr][cc];
            if (ch2 !== ch) break;
          }
          ends.push(hit);
        }
        if (ends[0] && ends[1]) bonds.push({ a: ends[0], b: ends[1], o: B[0], k: B[1], blank: B[0] === 0 ? blanks[r + ',' + c] : null });
      }
    }
    return { toks: toks, bonds: bonds, ascii: true, nb: nb };
  }

  /* 좌표로 만들기 */
  function Builder() { this.toks = []; this.bonds = []; this.extra = []; }
  Builder.prototype.at = function (x, y, text, anchor) {
    var t = { text: text || '', id: this.toks.length };
    if (!text) { t.vertex = true; t.chars = [{ ch: '', kind: 'v', w: 0, x: x * U, y: y * U }]; }
    else {
      var ch = layout(text, 0, y * U), a = anchor || 0;
      var shift = x * U - ch[Math.min(a, ch.length - 1)].x;
      ch.forEach(function (o) { o.x += shift; });
      t.chars = ch; t.anchor = a;
    }
    this.toks.push(t);
    return t.id;
  };
  Builder.prototype.b = function (i, j, o, inner) {
    var ti = this.toks[i], tj = this.toks[j];
    this.bonds.push({ a: { t: ti, idx: ti.anchor || 0 }, b: { t: tj, idx: tj.anchor || 0 }, o: o || 1, inner: inner });
    return this;
  };
  Builder.prototype.ring = function (cx, cy, n, r, rot, labels) { // 고리 꼭짓점
    var ids = [];
    for (var i = 0; i < n; i++) {
      var ang = (rot + i * 360 / n) * Math.PI / 180;
      ids.push(this.at(cx + r * Math.cos(ang), cy + r * Math.sin(ang), labels ? labels[i] : ''));
    }
    this.lastRing = { ids: ids, cx: cx * U, cy: cy * U };
    return ids;
  };
  Builder.prototype.benzene = function (cx, cy, rot) {
    var ids = this.ring(cx, cy, 6, 1, rot, null), c = { x: cx * U, y: cy * U };
    for (var i = 0; i < 6; i++) this.b(ids[i], ids[(i + 1) % 6], 1, i % 2 === 0 ? c : null);
    return ids;
  };
  Builder.prototype.note = function (x, y, text, cls) { this.extra.push({ x: x * U, y: y * U, text: text, cls: cls || 'mnote' }); return this; };
  Builder.prototype.hl = function (x0, y0, x1, y1) { (this.hls = this.hls || []).push([x0 * U, y0 * U, x1 * U, y1 * U]); return this; };

  function charAt(end) {
    var t = end.t, i = Math.max(0, Math.min(end.idx, t.chars.length - 1));
    var o = t.chars[i];
    if (o.kind === 'sub' || o.kind === 'sup') { // 첨자에 닿으면 가까운 원소 글자로
      for (var k = i; k >= 0; k--) if (t.chars[k].kind === 'n' && /[A-Za-z]/.test(t.chars[k].ch)) return t.chars[k];
    }
    return o;
  }

  var ELCOL = { O: 'o', N: 'n', Cl: 'cl', S: 's', P: 'p' };
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  function render(m, opt) {
    opt = opt || {};
    var toks = m.toks, segs = [];
    m.bonds.forEach(function (bd) {
      var A = charAt(bd.a), B = charAt(bd.b), ax = A.x, ay = A.y, bx = B.x, by = B.y;
      var ta = bd.a.t, tb = bd.b.t;
      var dx = bx - ax, dy = by - ay, L = Math.sqrt(dx * dx + dy * dy) || 1, ux = dx / L, uy = dy / L;
      // 끝 줄이기
      function trim(t, ch, sgn) {
        if (t.vertex) return 0;
        if (t.blank != null) return Math.abs(uy) < 0.2 ? 16 : 13;
        if (t.text === '[' || t.text === ']' || /^\]/.test(t.text)) return 1;
        if (Math.abs(uy) < 0.2) { // 가로: 글자 덩어리 가장자리에서 멈춤
          var bx2 = tokenBox(t.chars);
          var edge = sgn > 0 ? bx2.r : bx2.l;
          return Math.abs(edge - ch.x) + 2.5;
        }
        return Math.abs(uy) > 0.9 ? 9.5 : 8.5;
      }
      var s0 = trim(ta, A, ux >= 0 ? 1 : -1), s1 = trim(tb, B, ux >= 0 ? -1 : 1);
      var x0 = ax + ux * s0, y0 = ay + uy * s0, x1 = bx - ux * s1, y1 = by - uy * s1;
      var px = -uy, py = ux;
      if (bd.inner) { // 고리 안쪽 이중 결합
        var mx = (x0 + x1) / 2, my = (y0 + y1) / 2, cx = bd.inner.x, cy = bd.inner.y;
        var sg = ((cx - mx) * px + (cy - my) * py) > 0 ? 1 : -1, off = 5.2 * sg, sh = 0.16 * L;
        segs.push([x0, y0, x1, y1]);
        segs.push([x0 + ux * sh + px * off, y0 + uy * sh + py * off, x1 - ux * sh + px * off, y1 - uy * sh + py * off]);
        return;
      }
      if (bd.blank != null) {
        var bv = (opt.vals || [])[bd.blank], bo = bv === '=' ? 2 : bv === '≡' ? 3 : bv === '-' ? 1 : 0;
        var bcls = 'bkl' + (opt.sel === bd.blank ? ' on' : '') + (opt.bad && opt.bad[bd.blank] ? ' bad' : '') + (opt.good && opt.good[bd.blank] ? ' good' : '');
        var offs = bo === 2 ? [-2.6, 2.6] : bo === 3 ? [-4, 0, 4] : [0];
        offs.forEach(function (k) { segs.push([x0 + px * k, y0 + py * k, x1 + px * k, y1 + py * k, bcls + (bo ? '' : ' empty')]); });
        segs.push([x0, y0, x1, y1, 'bkhit', bd.blank]);
        return;
      }
      if (bd.o === 1) segs.push([x0, y0, x1, y1]);
      else if (bd.o === 2) { segs.push([x0 + px * 2.6, y0 + py * 2.6, x1 + px * 2.6, y1 + py * 2.6]); segs.push([x0 - px * 2.6, y0 - py * 2.6, x1 - px * 2.6, y1 - py * 2.6]); }
      else { segs.push([x0, y0, x1, y1]); segs.push([x0 + px * 4, y0 + py * 4, x1 + px * 4, y1 + py * 4]); segs.push([x0 - px * 4, y0 - py * 4, x1 - px * 4, y1 - py * 4]); }
    });
    // 테두리 계산
    var minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    function grow(x, y, w, h) { if (x - w < minX) minX = x - w; if (x + w > maxX) maxX = x + w; if (y - h < minY) minY = y - h; if (y + h > maxY) maxY = y + h; }
    toks.forEach(function (t) { t.chars.forEach(function (o) { grow(o.x, o.y, o.w / 2 + 1, 9); }); });
    segs.forEach(function (s) { grow(s[0], s[1], 1, 1); grow(s[2], s[3], 1, 1); });
    (m.extra || []).forEach(function (e) { grow(e.x, e.y, e.text.length * 3.6 + 2, 7); });
    var hls = [];
    if (Array.isArray(m.hl)) m.hl.forEach(function (h) { // [r0,c0,r1,c1] 칸
      var x0 = h[1] * CW - 2, x1 = (h[3] + 1) * CW + 2, y0 = h[0] * RH - 1, y1 = (h[2] + 1) * RH + 1;
      hls.push([x0, y0, x1, y1]);
    });
    if (m.hls) m.hls.forEach(function (h) { hls.push(h); });
    hls.forEach(function (h) { grow(h[0], h[1], 0, 0); grow(h[2], h[3], 0, 0); });
    // 대괄호는 위아래 끝까지
    var brTop = minY + 2, brBot = maxY - 2;
    var pad = opt.pad == null ? 6 : opt.pad, W = maxX - minX + pad * 2, H = maxY - minY + pad * 2;
    var ox = -minX + pad, oy = -minY + pad;
    var out = [];
    var anim = opt.anim ? ' anim' : '';
    out.push('<svg class="mol' + anim + '" viewBox="0 0 ' + W.toFixed(1) + ' ' + H.toFixed(1) + '" width="' + Math.round(W * (opt.scale || 1)) + '" role="img" aria-label="' + esc(opt.label || m.name || '구조식') + '">');
    hls.forEach(function (h) { out.push('<rect class="mhl" x="' + (h[0] + ox).toFixed(1) + '" y="' + (h[1] + oy).toFixed(1) + '" width="' + (h[2] - h[0]).toFixed(1) + '" height="' + (h[3] - h[1]).toFixed(1) + '" rx="7"/>'); });
    out.push('<g class="mb">');
    segs.forEach(function (s, i) {
      out.push('<line pathLength="1" style="--i:' + i + '"' + (s[4] ? ' class="' + s[4] + '"' : '') + (s[5] != null ? ' data-bk="' + s[5] + '"' : '') + ' x1="' + (s[0] + ox).toFixed(1) + '" y1="' + (s[1] + oy).toFixed(1) + '" x2="' + (s[2] + ox).toFixed(1) + '" y2="' + (s[3] + oy).toFixed(1) + '"/>');
    });
    out.push('</g><g class="ma" style="--n:' + segs.length + '">');
    toks.forEach(function (t) {
      if (t.vertex) return;
      if (t.blank != null) {
        var c0b = t.chars[0], v = (opt.vals || [])[t.blank], bx = c0b.x + ox, by = c0b.y + oy;
        var cls2 = 'bka' + (opt.sel === t.blank ? ' on' : '') + (v ? ' full' : '') + (opt.bad && opt.bad[t.blank] ? ' bad' : '') + (opt.good && opt.good[t.blank] ? ' good' : '');
        out.push('<g class="' + cls2 + '" data-bk="' + t.blank + '"><rect x="' + (bx - 15).toFixed(1) + '" y="' + (by - 12).toFixed(1) + '" width="30" height="24" rx="6"/>');
        if (v) layout(v, 0, 0).forEach(function (o, i, arr) {
          var tot = arr[arr.length - 1].x - arr[0].x, sx = bx - tot / 2 + o.x - arr[0].x, sy = by + 5.3 + (o.kind === 'sub' ? 4.2 : 0);
          out.push('<text class="mt' + (o.kind === 'sub' ? ' msub' : '') + (ELCOL[o.ch] ? ' e' + ELCOL[o.ch] : '') + '" x="' + sx.toFixed(1) + '" y="' + sy.toFixed(1) + '">' + esc(o.ch) + '</text>');
        });
        else out.push('<text class="mt bkq" x="' + bx.toFixed(1) + '" y="' + (by + 5).toFixed(1) + '">?</text>');
        out.push('</g>');
        return;
      }
      if (t.text === '[' || t.text === ']' || /^\][n]?$/.test(t.text)) {
        var c0 = t.chars[0], x = c0.x + ox, y0 = brTop + oy, y1 = brBot + oy, op = c0.ch === '[' ? 1 : -1;
        out.push('<path class="mbr" d="M' + (x + op * 4).toFixed(1) + ' ' + y0.toFixed(1) + ' Q' + (x - op * 2).toFixed(1) + ' ' + ((y0 + y1) / 2).toFixed(1) + ' ' + (x + op * 4).toFixed(1) + ' ' + y1.toFixed(1) + '"/>');
        if (t.chars[1]) out.push('<text class="msub" x="' + (t.chars[1].x + ox + 2).toFixed(1) + '" y="' + (y1 + 1).toFixed(1) + '">n</text>');
        return;
      }
      var cls = '', txt = t.text.replace(/[^A-Za-z]/g, '');
      t.chars.forEach(function (o, i) {
        var c = '';
        if (o.kind === 'n') {
          var two = t.text.substr(i, 2);
          if (two === 'Cl') c = 'cl';
          else if (o.ch === 'l' && t.chars[i - 1] && t.chars[i - 1].ch === 'C') c = 'cl';
          else c = ELCOL[o.ch] || '';
        }
        var y = o.y + oy + 5.3, k = o.kind;
        var size = k === 'sub' || k === 'sup' ? ' msub' : '';
        if (k === 'sub') y += 4.2; if (k === 'sup') y -= 6.5;
        out.push('<text class="mt' + (c ? ' e' + c : '') + size + '" x="' + (o.x + ox).toFixed(1) + '" y="' + y.toFixed(1) + '">' + esc(o.ch) + '</text>');
      });
    });
    (m.extra || []).forEach(function (e) {
      out.push('<text class="' + e.cls + '" x="' + (e.x + ox).toFixed(1) + '" y="' + (e.y + oy + 4).toFixed(1) + '">' + esc(e.text) + '</text>');
    });
    out.push('</g></svg>');
    return out.join('');
  }

  /* ---------- 분자 목록 ---------- */
  var DB = {};
  function A(key, meta, src, hl) { var m = parseAscii(src); m.hl = hl; for (var k in meta) m[k] = meta[k]; m.key = key; DB[key] = m; }
  function B(key, meta, fn) { var b = new Builder(); fn(b); b.key = key; for (var k in meta) b[k] = meta[k]; DB[key] = b; }

  function alkane(n) {
    var m = 'H', i;
    for (i = 0; i < n; i++) m += '--C';
    m += '--H';
    var rowT = '', rowP = '';
    for (i = 0; i < n; i++) { var col = 3 + 3 * i; while (rowT.length < col) { rowT += ' '; rowP += ' '; } rowT += 'H'; rowP += '|'; }
    return [rowT, rowP, m, rowP, rowT].join('\n');
  }
  A('methane', { name: '메테인', f: 'CH4', cat: 'alkane' }, alkane(1));
  A('ethane', { name: '에테인', f: 'C2H6', cat: 'alkane' }, alkane(2));
  A('propane', { name: '프로페인', f: 'C3H8', cat: 'alkane' }, alkane(3));
  A('butane', { name: '뷰테인', f: 'C4H10', cat: 'alkane' }, alkane(4));
  A('ethene', { name: '에텐(에틸렌)', f: 'C2H4', cat: 'alkene' }, String.raw`
H      H
 \    /
  C==C
 /    \
H      H`);
  A('ethyne', { name: '에타인(아세틸렌)', f: 'C2H2', cat: 'alkyne' }, 'H--C≡≡C--H');
  A('methanol', { name: '메탄올', f: 'CH3OH', cat: 'alcohol', fg: ['OH'] }, `
   H
   |
H--C--OH
   |
   H`, [[2, 6, 2, 7]]);
  A('ethanol', { name: '에탄올', f: 'C2H5OH', cat: 'alcohol', fg: ['OH'] }, `
   H  H
   |  |
H--C--C--OH
   |  |
   H  H`, [[2, 9, 2, 10]]);
  A('glycol', { name: '에틸렌 글리콜', f: 'C2H4(OH)2', cat: 'alcohol', fg: ['OH'] }, `
   H  H
   |  |
H--C--C--H
   |  |
   OH OH`, [[4, 3, 4, 4], [4, 6, 4, 7]]);
  A('glycerol', { name: '글리세롤', f: 'C3H5(OH)3', cat: 'alcohol', fg: ['OH'] }, `
   H  H  H
   |  |  |
H--C--C--C--H
   |  |  |
   OH OH OH`, [[4, 3, 4, 4], [4, 6, 4, 7], [4, 9, 4, 10]]);
  A('formaldehyde', { name: '폼알데하이드', f: 'HCHO', cat: 'aldehyde', fg: ['CHO'] }, `
   O
   ‖
H--C--H`, [[0, 2.6, 2, 6]]);
  A('acetaldehyde', { name: '아세트알데하이드', f: 'CH3CHO', cat: 'aldehyde', fg: ['CHO'] }, `
   H  O
   |  ‖
H--C--C--H
   |
   H`, [[0, 5.6, 2, 9]]);
  A('formic', { name: '폼산', f: 'HCOOH', cat: 'acid', fg: ['COOH'] }, `
   O
   ‖
H--C--O--H`, [[0, 2.6, 2, 9]]);
  A('acetic', { name: '아세트산', f: 'CH3COOH', cat: 'acid', fg: ['COOH'] }, `
   H  O
   |  ‖
H--C--C--O--H
   |
   H`, [[0, 5.6, 2, 12]]);
  A('ethylacetate', { name: '아세트산 에틸', f: 'CH3COOC2H5', cat: 'ester', fg: ['COO'] }, `
     O
     ‖
CH3--C--O--C2H5`, [[0, 4.6, 2, 8]]);
  A('glucose', { name: '포도당', f: 'C6H12O6', cat: 'sugar', fg: ['OH', 'CHO'] }, `
     H  H  H  OH H
     |  |  |  |  |
HO---C--C--C--C--C--C==O
     |  |  |  |  |  |
     H  OH OH H  OH H`, [[2, 19.6, 4, 23.4]]);
  A('aminoacid', { name: '아미노산', f: 'H2N-CHR-COOH', cat: 'amino', fg: ['NH2', 'COOH'] }, `
   H  H  O
   |  |  ‖
H--N--C--C--OH
      |
      R`);
  A('alanine', { name: '알라닌', cat: 'amino', fg: ['NH2', 'COOH'] }, `
   H  H  O
   |  |  ‖
H--N--C--C--OH
      |
      CH3`, [[4, 5.6, 4, 8]]);
  A('leucine', { name: '류신', cat: 'amino', fg: ['NH2', 'COOH'] }, String.raw`
   H  H  O
   |  |  ‖
H--N--C--C--OH
      |
      CH2
      |
      CH
     / \
    CH3 CH3`);
  A('aspartic', { name: '아스파르트산', cat: 'amino', fg: ['NH2', 'COOH'] }, `
   H  H  O
   |  |  ‖
H--N--C--C--OH
      |
      CH2
      |
      COOH`);
  A('serine', { name: '세린', cat: 'amino', fg: ['NH2', 'COOH', 'OH'] }, `
   H  H  O
   |  |  ‖
H--N--C--C--OH
      |
      CH2
      |
      OH`);
  A('dipeptide', { name: '펩타이드 결합', cat: 'protein' }, `
   H  H  O  H  H  O
   |  |  ‖  |  |  ‖
H--N--C--C--N--C--C--OH
      |        |
      R1       R2`, [[0, 8.6, 2, 12.4]]);
  A('vinylchloride', { name: '염화 바이닐', f: 'C2H3Cl', cat: 'monomer' }, `
H  H
|  |
C==C
|  |
H  Cl`);
  A('ethylene', { name: '에틸렌', f: 'C2H4', cat: 'monomer' }, `
H  H
|  |
C==C
|  |
H  H`);
  A('pe', { name: '폴리에틸렌(PE)', cat: 'polymer' }, `
   H  H
   |  |
[--C--C--]n
   |  |
   H  H`);
  A('pvc', { name: '폴리염화 바이닐(PVC)', cat: 'polymer' }, `
   H  H
   |  |
[--C--C--]n
   |  |
   H  Cl`);
  A('isoprene', { name: '아이소프렌', cat: 'monomer' }, `
CH2==C--CH==CH2
     |
     CH3`, [[2, 5, 2, 7]]);
  A('chloroprene', { name: '클로로프렌', cat: 'monomer' }, `
CH2==C--CH==CH2
     |
     Cl`, [[2, 5, 2, 6]]);
  A('rubber', { name: '천연 고무', cat: 'polymer' }, `
[--CH2--C==CH--CH2--]n
        |
        CH3`);
  A('neoprene', { name: '네오프렌', cat: 'polymer' }, `
[--CH2--C==CH--CH2--]n
        |
        Cl`);
  A('hmda', { name: '헥사메틸렌다이아민', cat: 'monomer', fg: ['NH2'] }, 'H2N--(CH2)6--NH2');
  A('adipoyl', { name: '염화 아디프산', cat: 'monomer' }, `
    O          O
    ‖          ‖
Cl--C--(CH2)4--C--Cl`);
  A('nylon', { name: '나일론', cat: 'polymer' }, `
   H          H  O          O
   |          |  ‖          ‖
[--N--(CH2)6--N--C--(CH2)4--C--]n`, [[0, 13.6, 2, 17.4]]);
  A('anhydride', { name: '아세트산 무수물', cat: 'drug' }, `
     O        O
     ‖        ‖
CH3--C--O--C--CH3`);
  A('fgOH', { name: '하이드록시기', f: 'R-OH', cat: 'fg' }, 'R--O--H', [[0, 2.6, 0, 7.4]]);
  A('fgCOOH', { name: '카복실기', f: 'R-COOH', cat: 'fg' }, `
   O
   ‖
R--C--O--H`, [[0, 2.6, 2, 10.4]]);
  A('fgCHO', { name: '알데하이드기(포밀기)', f: 'R-CHO', cat: 'fg' }, `
   O
   ‖
R--C--H`, [[0, 2.6, 2, 7.4]]);
  A('fgCOO', { name: '에스터기', f: "R-COO-R'", cat: 'fg' }, `
   O
   ‖
R--C--O--R'`, [[0, 2.6, 2, 7.4]]);
  A('ammonia', { name: '암모니아', f: 'NH3', cat: 'etc' }, `
H--N--H
   |
   H`);

  B('terephthalic', { name: '테레프탈산', cat: 'monomer', fg: ['COOH'] }, function (b) {
    var r = b.benzene(0, 0, 0);
    var c1 = b.at(2, 0, 'C'), o1 = b.at(2, -1, 'O'), h1 = b.at(3, 0, 'OH');
    var c2 = b.at(-2, 0, 'C'), o2 = b.at(-2, -1, 'O'), h2 = b.at(-3.1, 0, 'HO', 1);
    b.b(r[0], c1).b(c1, o1, 2).b(c1, h1).b(r[3], c2).b(c2, o2, 2).b(c2, h2);
  });
  B('pet', { name: 'PET', cat: 'polymer' }, function (b) {
    var br = b.at(-3.3, 0, '[');
    var c2 = b.at(-2, 0, 'C'), o2 = b.at(-2, -1, 'O');
    var r = b.benzene(0, 0, 0);
    var c1 = b.at(2, 0, 'C'), o1 = b.at(2, -1, 'O'), o3 = b.at(3, 0, 'O');
    var e1 = b.at(4.25, 0, 'CH2'), e2 = b.at(5.75, 0, 'CH2'), o4 = b.at(7, 0, 'O'), br2 = b.at(8, 0, ']n');
    b.b(br, c2).b(c2, o2, 2).b(c2, r[3]).b(r[0], c1).b(c1, o1, 2).b(c1, o3).b(o3, e1).b(e1, e2).b(e2, o4).b(o4, br2);
    b.hl(1.55, -1.45, 3.45, 0.45);
  });
  B('salicylic', { name: '살리실산', cat: 'drug', fg: ['OH', 'COOH'] }, function (b) {
    var r = b.benzene(0, 0, -90);
    var oh = b.at(1.73, -1, 'OH'), co = b.at(1.73, 1, 'COOH');
    b.b(r[1], oh).b(r[2], co);
    b.hl(1.4, -1.42, 2.55, -0.58);
  });
  B('aspirin', { name: '아세틸살리실산(아스피린)', cat: 'drug', fg: ['COO', 'COOH'] }, function (b) {
    var r = b.benzene(0, 0, -90);
    var o = b.at(1.73, -1, 'O'), c = b.at(2.73, -1, 'C'), o2 = b.at(2.73, -2, 'O'), m = b.at(3.73, -1, 'CH3');
    var co = b.at(1.73, 1, 'COOH');
    b.b(r[1], o).b(o, c).b(c, o2, 2).b(c, m).b(r[2], co);
    b.hl(1.42, -2.4, 3.05, -0.58);
  });
  function sugar(b, deoxy) {
    // 오각형: O 위, 1' 오른쪽 위, 2' 오른쪽 아래, 3' 왼쪽 아래, 4' 왼쪽 위
    var R = 1.05, pts = [-90, -18, 54, 126, 198].map(function (a) { a = a * Math.PI / 180; return [R * Math.cos(a), R * Math.sin(a)]; });
    var O = b.at(pts[0][0], pts[0][1], 'O'), c1 = b.at(pts[1][0], pts[1][1], 'C'), c2 = b.at(pts[2][0], pts[2][1], 'C'), c3 = b.at(pts[3][0], pts[3][1], 'C'), c4 = b.at(pts[4][0], pts[4][1], 'C');
    b.b(O, c1).b(c1, c2).b(c2, c3).b(c3, c4).b(c4, O);
    var oh1 = b.at(pts[1][0] + 0.75, pts[1][1] - 0.75, 'OH'); b.b(c1, oh1);
    var h1 = b.at(pts[1][0] + 0.8, pts[1][1] + 0.5, 'H'); b.b(c1, h1);
    var ch2 = b.at(pts[4][0] - 0.5, pts[4][1] - 0.98, 'HOCH2', 2); b.b(c4, ch2);
    var h4 = b.at(pts[4][0] - 0.75, pts[4][1] + 0.55, 'H'); b.b(c4, h4);
    var o3 = b.at(pts[3][0], pts[3][1] + 1.05, 'OH'); b.b(c3, o3);
    var o2 = b.at(pts[2][0], pts[2][1] + 1.05, deoxy ? 'H' : 'OH'); b.b(c2, o2);
    b.note(pts[1][0] - 0.3, pts[1][1] + 0.08, "1'", 'mnum').note(pts[2][0] - 0.3, pts[2][1] - 0.3, "2'", 'mnum').note(pts[3][0] + 0.3, pts[3][1] - 0.3, "3'", 'mnum').note(pts[4][0] + 0.32, pts[4][1] + 0.08, "4'", 'mnum').note(pts[4][0] - 0.12, pts[4][1] - 1.42, "5'", 'mnum');
    b.hl(pts[2][0] - 0.38, pts[2][1] + 0.72, pts[2][0] + (deoxy ? 0.38 : 0.62), pts[2][1] + 1.38);
  }
  B('ribose', { name: '라이보스', cat: 'sugar' }, function (b) { sugar(b, false); });
  B('deoxyribose', { name: '디옥시라이보스', cat: 'sugar' }, function (b) { sugar(b, true); });

  B('nucleotide', { name: '뉴클레오타이드', cat: 'monomer' }, function (b) {
    var R = 1.05, pts = [-90, -18, 54, 126, 198].map(function (a) { a = a * Math.PI / 180; return [R * Math.cos(a), R * Math.sin(a)]; });
    var O = b.at(pts[0][0], pts[0][1], 'O'), c1 = b.at(pts[1][0], pts[1][1], 'C'), c2 = b.at(pts[2][0], pts[2][1], 'C'), c3 = b.at(pts[3][0], pts[3][1], 'C'), c4 = b.at(pts[4][0], pts[4][1], 'C');
    b.b(O, c1).b(c1, c2).b(c2, c3).b(c3, c4).b(c4, O);
    b.b(c3, b.at(pts[3][0], pts[3][1] + 1, 'OH')).b(c2, b.at(pts[2][0], pts[2][1] + 1, 'H'));
    var ch2 = b.at(pts[4][0] - 0.2, pts[4][1] - 1.1, 'CH2'); b.b(c4, ch2);
    var o5 = b.at(pts[4][0] - 1.3, pts[4][1] - 1.1, 'O'), p = b.at(pts[4][0] - 2.3, pts[4][1] - 1.1, 'P');
    b.b(ch2, o5).b(o5, p).b(p, b.at(pts[4][0] - 2.3, pts[4][1] - 2.1, 'O'), 2).b(p, b.at(pts[4][0] - 3.4, pts[4][1] - 1.1, 'HO', 1)).b(p, b.at(pts[4][0] - 2.3, pts[4][1] - 0.1, 'OH'));
    var cx = pts[1][0] + 1.95, cy = pts[1][1], ang = [180, 240, 300, 0, 60, 120], lab = ['N', 'C', 'C', 'C', 'N', 'C'], v = [];
    ang.forEach(function (a, i) { a = a * Math.PI / 180; v.push(b.at(cx + Math.cos(a), cy + Math.sin(a), lab[i])); });
    b.b(c1, v[0]).b(v[0], v[1]).b(v[1], v[2], 2).b(v[2], v[3]).b(v[3], v[4], 2).b(v[4], v[5]).b(v[5], v[0]);
    b.b(v[5], b.at(cx - 0.5, cy + 1.85, 'O'), 2).b(v[3], b.at(cx + 2, cy, 'NH2'));
    b.note(cx - 1.4, cy - 1.75, '인산', 'mnote').note(cx, cy - 1.6, '염기', 'mnote');
  });
  window.MOL = {
    db: DB,
    svg: function (key, opt) { var m = DB[key]; if (!m) return ''; return render(m, opt); },
    ascii: function (src, opt) { var m = parseAscii(src); if (opt && opt.hl) m.hl = opt.hl; return render(m, opt); },
    blanks: function (src) { return parseAscii(src).nb; },
    has: function (k) { return !!DB[k]; }
  };
})();
