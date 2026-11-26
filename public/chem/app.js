/* 한 입 화학: 앱 */
(function () {
  'use strict';
  var C = window.CHEM, MOL = window.MOL, FIG = window.FIG;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var app = $('#app'), fxl = $('#fx');
  var MIN = 60e3, HOUR = 36e5, DAY = 864e5;
  var IV = [0, 10 * MIN, DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY];
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 저장 ---------- */
  var KEY = 'hanip-chem-v1', S;
  function fresh() { return { q: {}, days: {}, seen: {}, best: {}, set: { sound: false, vib: true, auto: false, theme: 'auto', big: false, logo: 'red' }, scope: 'all', tip: 0, made: Date.now() }; }
  try { S = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { S = null; }
  if (!S || !S.q) S = fresh();
  if (S.scope === 'u3') S.scope = 'u2';
  var dflt = fresh();
  for (var k in dflt) if (S[k] == null) S[k] = dflt[k];
  for (k in dflt.set) if (S.set[k] == null) S.set[k] = dflt.set[k];
  var saveT = 0;
  function save() { clearTimeout(saveT); saveT = setTimeout(saveNow, 120); }
  function saveNow() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { } }
  window.addEventListener('pagehide', saveNow);
  document.addEventListener('visibilitychange', function () { if (document.hidden) saveNow(); });

  /* ---------- 문제 준비 ---------- */
  function hash(s) { var h = 5381; for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; return h.toString(36); }
  var Q = [], QI = {}, TI = {}, UI = {};
  C.UNITS.forEach(function (u) { UI[u.id] = u; });
  C.TOPICS.forEach(function (t, ti) {
    t.order = ti; TI[t.id] = t;
    t.qs.forEach(function (q, i) {
      q.id = t.id + '-' + hash(q.k + '|' + q.q + '|' + JSON.stringify(q.a || q.s || q.p));
      if (QI[q.id]) q.id += '-' + i;
      q.u = t.u; q.n = i; q.topic = t;
      Q.push(q); QI[q.id] = q;
    });
  });
  // 분자 -> 주제
  var MOLT = {};
  C.TOPICS.forEach(function (t) {
    var re = /@mol:(\w+)/g, m;
    while ((m = re.exec(t.note || ''))) if (!MOLT[m[1]]) MOLT[m[1]] = t.id;
    t.qs.forEach(function (q) { if (q.fig && !MOLT[q.fig]) MOLT[q.fig] = t.id; });
  });
  ['fgOH', 'fgCOOH', 'fgCHO', 'fgCOO'].forEach(function (k) { MOLT[k] = 'fg'; });
  var TRIPS = C.TRIPS || [], TRI = {};
  TRIPS.forEach(function (tr, ti) {
    tr.order = ti; TRI[tr.id] = tr;
    tr.steps.forEach(function (q, i) { q.id = 'T-' + tr.id + '-' + i; q.les = tr.id; q.topic = TI[tr.t[0]]; q.t = tr.t[0]; q.u = tr.u; });
  });
  var WSA = C.WS || [];

  /* ---------- 글 ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function chem(f) {
    var out = '', i = 0, prev = '';
    while (i < f.length) {
      var c = f[i], j, s;
      if (c === '^') {
        j = i + 1; s = '';
        while (j < f.length && /[0-9]/.test(f[j])) s += f[j++];
        if (j < f.length && /[+\-]/.test(f[j])) s += f[j++];
        out += '<sup>' + s.replace('-', '−') + '</sup>'; i = j; prev = '^'; continue;
      }
      if (c === '_') {
        if (f[i + 1] === '{') { j = f.indexOf('}', i); out += '<sub>' + esc(f.slice(i + 2, j)) + '</sub>'; i = j + 1; }
        else { out += '<sub>' + esc(f[i + 1]) + '</sub>'; i += 2; }
        prev = '_'; continue;
      }
      if (/[0-9]/.test(c) && /[A-Za-z)\]]/.test(prev)) {
        j = i; s = '';
        while (j < f.length && /[0-9]/.test(f[j])) s += f[j++];
        out += '<sub>' + s + '</sub>'; i = j; prev = '0'; continue;
      }
      out += esc(c); prev = c; i++;
    }
    return '<span class="cf">' + out + '</span>';
  }
  function fmt(s) {
    if (s == null) return '';
    var keep = [];
    var t = String(s).replace(/`([^`]*)`/g, function (m, f) { keep.push(chem(f)); return '\u0001' + (keep.length - 1) + '\u0002'; });
    t = esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/==(.+?)==/g, '<mark>$1</mark>');
    return t.replace(/\u0001(\d+)\u0002/g, function (m, i) { return keep[+i]; });
  }
  function plain(s) { return String(s || '').replace(/[`*=]/g, '').replace(/\^/g, '').replace(/_\{?([^}]*)\}?/g, '$1'); }
  function choiceHtml(c) {
    if (typeof c === 'string' && c[0] === '@') return '<span class="mchoice">' + MOL.svg(c.slice(1)) + '</span>';
    return fmt(c);
  }

  /* ---------- 노트 그리기 ---------- */
  function noteHtml(src) {
    var lines = String(src || '').replace(/^\n+/, '').split('\n'), h = '', list = false, tbl = null;
    function close() { if (list) { h += '</ul>'; list = false; } if (tbl) { h += '<div class="tscroll"><table>' + tbl + '</table></div>'; tbl = null; } }
    lines.forEach(function (raw) {
      var l = raw.trim();
      if (!l) { close(); return; }
      if (l[0] === '|') {
        if (list) { h += '</ul>'; list = false; }
        var cells = l.replace(/^\||\|$/g, '').split('|');
        var first = tbl === null;
        tbl = (tbl || '') + '<tr>' + cells.map(function (c, i) { var tag = first ? 'th' : (i === 0 ? 'th' : 'td'); return '<' + tag + '>' + fmt(c.trim()) + '</' + tag + '>'; }).join('') + '</tr>';
        return;
      }
      if (tbl) { h += '<div class="tscroll"><table>' + tbl + '</table></div>'; tbl = null; }
      if (l.indexOf('# ') === 0) { close(); h += '<h3>' + fmt(l.slice(2)) + '</h3>'; return; }
      if (l.indexOf('- ') === 0) { if (!list) { h += '<ul>'; list = true; } h += '<li>' + fmt(l.slice(2)) + '</li>'; return; }
      close();
      if (l.indexOf('> ') === 0) { h += '<div class="callout link"><span>연결</span><p>' + fmt(l.slice(2)) + '</p></div>'; return; }
      if (l.indexOf('! ') === 0) { h += '<div class="callout tip"><span>시험 포인트</span><p>' + fmt(l.slice(2)) + '</p></div>'; return; }
      var m = /^@(mol|fig):(\w+)\|?(.*)$/.exec(l);
      if (m) {
        var body = m[1] === 'mol' ? MOL.svg(m[2]) : (FIG[m[2]] ? FIG[m[2]]() : '');
        h += '<figure class="nfig ' + m[1] + '">' + body + (m[3] ? '<figcaption>' + fmt(m[3]) + '</figcaption>' : '') + '</figure>';
        return;
      }
      h += '<p>' + fmt(l) + '</p>';
    });
    close();
    return h;
  }

  /* ---------- 아이콘 ---------- */
  var IC = {
    x: '<path d="M6 6l12 12M18 6L6 18"/>', back: '<path d="M15 5l-7 7 7 7"/>', gear: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    snd: '<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>', mute: '<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9l5 6M22 9l-5 6"/>',
    bolt: '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>', hex: '<path d="M12 2.5l8.2 4.75v9.5L12 21.5l-8.2-4.75v-9.5z"/><path d="M12 7.5l4 2.3v4.4l-4 2.3-4-2.3V9.8z"/>',
    link: '<path d="M4 7h4l3 5-3 5H4M20 7h-4l-3 5 3 5h4"/>', route: '<circle cx="5" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><path d="M7 6h7a3.5 3.5 0 0 1 0 7H10a3.5 3.5 0 0 0 0 7h7"/>',
    book: '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 21.5A2.5 2.5 0 0 1 6.5 19H20v3H6.5"/>',
    redo: '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 3v5h5"/>', check: '<path d="M4.5 12.5l5 5L20 7"/>', play: '<path d="M7 4.5v15l13-7.5z"/>', arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>', flame: '<path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 2-5 3-7 0 3 1 4 2 4 0-3-1-6 1-9z"/>',
    leaf: '<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19l8-8"/>', sprout: '<path d="M12 21V11"/><path d="M12 11C12 7 9 5 4 5c0 4 3 6 8 6zM12 13c0-4 3-6 8-6 0 4-3 6-8 6z"/>', shield: '<path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5z"/>', flame2: '<path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 2-5 3-7 0 3 1 4 2 4 0-3-1-6 1-9z"/>',
    tower: '<rect x="8" y="2" width="8" height="20" rx="4"/><path d="M16 7h4M16 12h4M16 17h4"/>', tag: '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>', drop: '<path d="M12 3s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z"/>', flask: '<path d="M9 2h6M10 2v6L4.5 19a2 2 0 0 0 1.8 3h11.4a2 2 0 0 0 1.8-3L14 8V2"/><path d="M7 15h10"/>',
    apple: '<path d="M12 7c-2-2-7-2-7 4 0 5 3 10 5 10 1 0 1.4-.5 2-.5s1 .5 2 .5c2 0 5-5 5-10 0-6-5-6-7-4z"/><path d="M12 7c0-2 1-4 3-5"/>', dna: '<path d="M7 2c0 7 10 7 10 14v6M17 2c0 7-10 7-10 14v6M8 6h8M8 18h8M9.5 12h5"/>', grape: '<circle cx="9" cy="10" r="2.5"/><circle cx="15" cy="10" r="2.5"/><circle cx="12" cy="15" r="2.5"/><circle cx="12" cy="20" r="1.8"/><path d="M12 7.5V3l3-1"/>',
    chain: '<rect x="2" y="9" width="8" height="6" rx="3"/><rect x="14" y="9" width="8" height="6" rx="3"/><path d="M10 12h4"/>', helix: '<path d="M7 2c0 7 10 7 10 14v6M17 2c0 7-10 7-10 14v6M8 6h8M8 18h8M9.5 12h5"/>', bottle: '<path d="M10 2h4v4l2 3v13H8V9l2-3z"/><path d="M8 13h8"/>', thread: '<circle cx="12" cy="12" r="8"/><path d="M6 8c4 0 8 4 12 8M4.5 13c3 0 6 3 8 6.5M9 4.5c2 2 5 2.5 10.5 4"/>', wave: '<path d="M2 12c3-4 5-4 8 0s5 4 8 0 3-4 4-4"/><path d="M2 17c3-4 5-4 8 0s5 4 8 0"/>', pill: '<rect x="2.5" y="8.5" width="19" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="M9 9l6 6"/>', bolt2: '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>', star: '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>'
  };
  function ic(n, cls) { return '<svg class="ic ' + (cls || '') + '" viewBox="0 0 24 24" aria-hidden="true">' + (IC[n] || IC.hex) + '</svg>'; }

  /* ---------- 학습 상태 ---------- */
  function st(id) { return S.q[id]; }
  function box(id) { var s = S.q[id]; return s ? s.b : -1; }
  function seenTopic(t) { return !!S.seen[t]; }
  function inScope(q) {
    if (q.topic.hidden) return S.scope === 'all' && (!q.req || q.req.every(seenTopic));
    return uIn(q.u);
  }
  function uIn(u) { return S.scope === 'all' || u === S.scope || (S.scope === 'c' && u !== 'u1'); }
  function scopeTopics() { return C.TOPICS.filter(function (t) { return !t.hidden && uIn(t.u); }); }
  function scopeQs() { return Q.filter(function (q) { return !q.topic.hidden && uIn(q.u); }); }
  function mastery(qs) {
    if (!qs.length) return 0;
    var s = 0;
    qs.forEach(function (q) { var b = box(q.id); if (b > 0) s += Math.min(b, 4) / 4; });
    return s / qs.length;
  }
  function learnedCount(qs) { return qs.filter(function (q) { return box(q.id) >= 3; }).length; }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dayKey(t) { var d = new Date(t); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function streak() {
    var n = 0, t = Date.now();
    if (!S.days[today()]) t -= DAY;
    while (S.days[dayKey(t)]) { n++; t -= DAY; }
    return n;
  }
  function noteQs(qs) { return qs.filter(function (q) { var s = S.q[q.id]; return s && s.w > 0; }); }
  function dueQs(qs) { var now = Date.now(); return qs.filter(function (q) { var s = S.q[q.id]; return s && s.b > 0 && s.d <= now; }); }
  function wrongQs(qs) { return qs.filter(function (q) { var s = S.q[q.id]; return s && s.b === 0; }); }

  function record(q, ok, retry) {
    var s = S.q[q.id], now = Date.now(), first = !s;
    if (!s) s = S.q[q.id] = { b: 0, d: 0, n: 0, w: 0, l: 0 };
    var before = s.b;
    s.n++; s.l = now; s.s = ok ? 1 : 0;
    if (ok) {
      if (first) s.b = 2;
      else if (retry || s.b === 0) s.b = 1;
      else s.b = Math.min(6, s.b + 1);
    } else { s.w++; s.b = 0; }
    s.d = now + IV[s.b];
    S.days[today()] = (S.days[today()] || 0) + 1;
    save();
    return { learned: before < 3 && s.b >= 3, before: before, after: s.b };
  }

  /* ---------- 효과 ---------- */
  var AC = null;
  function tone(seq) {
    if (!S.set.sound) return;
    try {
      AC = AC || new (window.AudioContext || window.webkitAudioContext)();
      if (AC.state === 'suspended') AC.resume();
      var t0 = AC.currentTime + 0.01;
      seq.forEach(function (n) {
        var o = AC.createOscillator(), g = AC.createGain();
        o.type = n[3] || 'sine'; o.frequency.value = n[0];
        g.gain.setValueAtTime(0.0001, t0 + n[1]);
        g.gain.exponentialRampToValueAtTime(n[4] || 0.12, t0 + n[1] + 0.012);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + n[1] + n[2]);
        o.connect(g); g.connect(AC.destination); o.start(t0 + n[1]); o.stop(t0 + n[1] + n[2] + 0.02);
      });
    } catch (e) { }
  }
  var SND = {
    ok: function () { tone([[784, 0, 0.12], [1175, 0.07, 0.22]]); },
    no: function () { tone([[196, 0, 0.22, 'triangle', 0.14], [165, 0.08, 0.26, 'triangle', 0.1]]); },
    combo: function (n) { var b = 523 * Math.pow(1.06, Math.min(n, 12)); tone([[b, 0, 0.1], [b * 1.25, 0.06, 0.1], [b * 1.5, 0.12, 0.2]]); },
    tick: function () { tone([[1400, 0, 0.03, 'square', 0.03]]); },
    done: function () { tone([[523, 0, 0.3], [659, 0.1, 0.3], [784, 0.2, 0.4], [1047, 0.32, 0.6]]); },
    tap: function () { tone([[880, 0, 0.04, 'sine', 0.05]]); }
  };
  function vib(p) { if (S.set.vib && navigator.vibrate) try { navigator.vibrate(p); } catch (e) { } }
  function burst(el, kind) {
    if (reduced || !el || !el.getBoundingClientRect) return;
    var r = el.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var cols = ['var(--green)', 'var(--blue)', 'var(--amber)', 'var(--red)'];
    for (var i = 0; i < 12; i++) {
      var p = document.createElement('i');
      p.className = 'pt ' + (i % 3 === 0 ? 'hexp' : i % 3 === 1 ? 'dotp' : 'barp');
      p.style.left = cx + 'px'; p.style.top = cy + 'px';
      p.style.color = cols[i % cols.length];
      fxl.appendChild(p);
      var a = (i / 12) * Math.PI * 2 + Math.random() * 0.4, d = 60 + Math.random() * 70;
      var anim = p.animate([
        { transform: 'translate(-50%,-50%) scale(.4) rotate(0deg)', opacity: 1 },
        { transform: 'translate(calc(-50% + ' + Math.cos(a) * d + 'px), calc(-50% + ' + Math.sin(a) * d + 'px)) scale(1) rotate(' + (Math.random() * 180 - 90) + 'deg)', opacity: 0 }
      ], { duration: 620 + Math.random() * 260, easing: 'cubic-bezier(.15,.7,.3,1)' });
      anim.onfinish = (function (n) { return function () { n.remove(); }; })(p);
    }
  }
  function floatText(el, txt, cls) {
    if (!el) return;
    var r = el.getBoundingClientRect(), p = document.createElement('div');
    p.className = 'ftxt ' + (cls || ''); p.textContent = txt;
    p.style.left = (r.left + r.width / 2) + 'px'; p.style.top = (r.top) + 'px';
    fxl.appendChild(p);
    var a = p.animate([{ transform: 'translate(-50%,0) scale(.8)', opacity: 0 }, { transform: 'translate(-50%,-26px) scale(1)', opacity: 1, offset: .3 }, { transform: 'translate(-50%,-46px) scale(1)', opacity: 0 }], { duration: reduced ? 400 : 900, easing: 'ease-out' });
    a.onfinish = function () { p.remove(); };
  }
  var toastT;
  function toast(html, cls) {
    var t = $('#toast');
    if (!t) { t = document.createElement('div'); t.id = 'toast'; document.body.appendChild(t); }
    t.className = 'toast show ' + (cls || ''); t.innerHTML = html;
    clearTimeout(toastT); toastT = setTimeout(function () { t.className = 'toast'; }, 2600);
  }
  function shake(el) { if (!el || reduced) return; el.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(-7px)' }, { transform: 'translateX(6px)' }, { transform: 'translateX(-4px)' }, { transform: 'translateX(2px)' }, { transform: 'translateX(0)' }], { duration: 340, easing: 'ease-out' }); }
  function countUp(el, to, ms) {
    if (!el) return;
    if (reduced) { el.textContent = to; return; }
    var t0 = performance.now();
    (function f(t) { var k = Math.min(1, (t - t0) / ms); k = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * k); if (k < 1) requestAnimationFrame(f); })(t0);
  }

  /* ---------- 화면 전환 ---------- */
  var view = { name: 'home' }, R = null; // R = 진행 중인 판
  function go(name, p, replace) {
    var stt = { name: name, p: p || {} };
    try { if (replace) history.replaceState(stt, ''); else history.pushState(stt, ''); } catch (e) { }
    show(stt);
  }
  function show(stt) {
    stopBolt();
    view = stt;
    var f = SCREENS[stt.name] || SCREENS.home;
    app.innerHTML = '<div class="view v-' + stt.name + '">' + f(stt.p || {}) + '</div>';
    app.scrollTop = 0; window.scrollTo(0, 0);
    var after = AFTER[stt.name]; if (after) after(stt.p || {});
  }
  window.addEventListener('popstate', function (e) {
    var stt = e.state || { name: 'home' };
    if (view.name === 'quiz' && R && !R.done && stt.name !== 'quiz') { R = null; }
    show(stt);
  });

  /* ---------- 공통 조각 ---------- */
  function ring(p, size, stroke, cls) {
    var r = (size - stroke) / 2, c = 2 * Math.PI * r;
    return '<svg class="ring ' + (cls || '') + '" viewBox="0 0 ' + size + ' ' + size + '" width="' + size + '" height="' + size + '"><circle cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '" class="rbg" stroke-width="' + stroke + '"/><circle cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '" class="rfg" stroke-width="' + stroke + '" stroke-dasharray="' + c.toFixed(2) + '" stroke-dashoffset="' + (c * (1 - p)).toFixed(2) + '" style="--c:' + c.toFixed(2) + (p < 0.004 ? ';opacity:0' : '') + '"/></svg>';
  }
  function bar(p, cls) { return '<span class="bar ' + (cls || '') + '"><i style="width:' + Math.round(p * 100) + '%"></i></span>'; }
  function topbar(title, opt) {
    opt = opt || {};
    return '<header class="top"><button class="ibtn" data-act="back" aria-label="뒤로">' + ic('back') + '</button><h1>' + title + '</h1>' + (opt.right || '<span class="ibsp"></span>') + '</header>';
  }
  function scopeChips() {
    var items = [{ id: 'all', short: '전체' }, { id: 'c', short: '탄소 화합물' }].concat(C.UNITS);
    return '<div class="chips" role="tablist">' + items.map(function (u) {
      return '<button class="chip' + (S.scope === u.id ? ' on' : '') + '" data-act="scope" data-v="' + u.id + '">' + esc(u.short) + '</button>';
    }).join('') + '</div>';
  }

  /* ---------- 홈 ---------- */
  var SCREENS = {}, AFTER = {};
  SCREENS.home = function () {
    var qs = scopeQs(), m = mastery(qs), ln = learnedCount(qs), due = dueQs(qs).length + wrongQs(qs).length;
    var tdy = S.days[today()] || 0, stk = streak();
    var unseen = qs.filter(function (q) { return !S.q[q.id]; }).length;
    var sub = due ? '복습할 문제 ' + due + '개가 기다려요' : unseen ? '새 문제 ' + unseen + '개 남았어요' : '모두 외웠어요. 그래도 복습은 계속!';
    var bite = biteOfDay();
    var h = '';
    h += '<header class="hhead"><div class="brand"><span class="logo">' + logoSvg() + '</span><div><b>한 입 화학</b><small>화학 반응의 세계</small></div></div>' +
      '<div class="hbtns"><button class="ibtn" data-act="sound" aria-label="소리">' + ic(S.set.sound ? 'snd' : 'mute') + '</button><button class="ibtn" data-act="settings" aria-label="설정">' + ic('gear') + '</button></div></header>';
    h += scopeChips();
    h += '<section class="hero card">' +
      '<div class="hring">' + ring(m, 112, 10, 'hr') + '<div class="hnum"><b><span id="mnum">' + Math.round(m * 100) + '</span><small>%</small></b><span>외운 정도</span></div></div>' +
      '<div class="hstats"><div><b>' + ln + '<small>/' + qs.length + '</small></b><span>완전히 외운 문제</span></div>' +
      '<div><b>' + tdy + '</b><span>오늘 푼 문제</span></div>' +
      '<div><b>' + stk + '<small>일</small></b><span>연속</span></div></div>' +
      '<button class="big primary" data-act="play" data-mode="mix">' + ic('play') + '<span><b>한 판 하기</b><small>10문제 · 약 2분</small></span></button>' +
      '<p class="hsub">' + esc(sub) + '</p></section>';
    var nt = nextTrip(), beginner = Object.keys(S.q).length < 25;
    if (nt && beginner) h = h.replace('<section class="hero card">', tripCta(nt, true) + '<section class="hero card">');
    else if (nt) h += tripCta(nt, false);
    h += '<section class="modes">' +
      mode('trips', 'route', '탐험', '몰라도 OK, 퍼즐로 시작', tripsDone() + '/' + TRIPS.length) +
      mode('wsl', 'book', '탐구활동지', '프린트 1~18 그대로', '') +
      mode('bolt', 'bolt', '번개 O/X', '60초 동안 몇 개?', S.best[S.scope] ? '최고 ' + S.best[S.scope] : '') +
      mode('mol', 'hex', '구조식', '보고 이름, 이름 보고 모양', '') +
      mode('link', 'link', '순서·짝 맞추기', '반응 순서, 짝 잇기', '') +
      mode('chains', 'chain', '이야기 줄', '개념을 이어서 보기', '') +
      mode('wrong', 'redo', '오답 노트', noteQs(qs).length ? noteQs(qs).length + '개' : '틀린 문제 다시', noteQs(qs).some(function (q) { return S.q[q.id].b === 0; }) ? 'hot' : '') +
      mode('notes', 'book', '개념 노트', 'PPT 내용 전부', '') +
      '</section>';
    if (bite) h += '<section class="bite card" data-act="note" data-t="' + bite.t.id + '"><span class="bitek">오늘의 한 입 · ' + esc(bite.t.name) + '</span><p>' + fmt(bite.line) + '</p></section>';
    h += '<section class="units">' + C.UNITS.filter(function (u) { return uIn(u.id); }).map(function (u) {
      var ts = C.TOPICS.filter(function (t) { return t.u === u.id; });
      return '<div class="unit card"><div class="uh"><span class="dot c-' + u.color + '"></span><b>' + esc(u.name) + '</b><span class="upc">' + Math.round(mastery(Q.filter(function (q) { return q.u === u.id; })) * 100) + '%</span></div>' +
        ts.map(function (t) {
          var mm = mastery(t.qs);
          return '<button class="trow" data-act="note" data-t="' + t.id + '">' + ic(t.icon, 'tic') + '<span class="tn">' + esc(t.name) + '</span>' + bar(mm, 'c-' + u.color) + '<span class="tp">' + learnedCount(t.qs) + '/' + t.qs.length + '</span></button>';
        }).join('') + '</div>';
    }).join('') + '</section>';
    h += installTip();
    h += '<button class="resetlink" data-act="settings">' + ic('gear') + '설정 · 전체 초기화</button>';
    h += '<footer class="foot">모든 내용은 화학 반응의 세계 수업 PPT(Ⅱ-05, Ⅲ-1~4)와 탐구활동지에서 가져왔어요. 기록은 이 기기에만 저장돼요.</footer>';
    return h;
  };
  function tripsDone() { S.trip = S.trip || {}; return TRIPS.filter(function (t) { return S.trip[t.id]; }).length; }
  function nextTrip() { S.trip = S.trip || {}; for (var i = 0; i < TRIPS.length; i++) if (!S.trip[TRIPS[i].id] && uIn(TRIPS[i].u)) return TRIPS[i]; return null; }
  function tripCta(t, big) {
    var i = TRIPS.indexOf(t);
    return '<button class="tripcta card' + (big ? ' first' : '') + '" data-act="trip" data-id="' + t.id + '">' +
      (big ? '<span class="tck">처음이라면 여기부터</span>' : '<span class="tck">다음 탐험</span>') +
      '<b>' + (i + 1) + '. ' + esc(t.name) + '</b><small>' + esc(t.sub) + ' · ' + t.steps.length + '걸음 · 몰라도 풀 수 있어요</small><span class="tgo">' + ic('play') + '</span></button>';
  }
  function mode(act, icon, name, desc, badge) {
    return '<button class="mode card" data-act="' + act + '"><span class="mic">' + ic(icon) + '</span><b>' + name + '</b><small>' + desc + '</small>' + (badge ? '<em class="' + (badge === 'hot' ? 'hot' : '') + '">' + (badge === 'hot' ? '' : esc(badge)) + '</em>' : '') + '</button>';
  }
  function biteOfDay() {
    var ts = scopeTopics(); if (!ts.length) return null;
    var d = new Date(), seed = d.getFullYear() * 400 + d.getMonth() * 31 + d.getDate() + (S.scope.charCodeAt(0) || 0);
    var lines = [];
    ts.forEach(function (t) { t.key.forEach(function (l) { lines.push({ t: t, line: l }); }); });
    return lines[seed % lines.length];
  }
  var LOGO = [["red", "빨강", "#F5A3A0"], ["orange", "주황", "#F7BC8C"], ["yellow", "노랑", "#F3D27C"], ["green", "초록", "#A6D8AE"], ["blue", "파랑", "#9FC8F0"], ["navy", "남색", "#A7ADE8"], ["purple", "보라", "#CDAAEC"]];
  function logoSvg() {
    return '<svg viewBox="0 0 512 512" aria-hidden="true"><defs><mask id="lgb"><rect width="512" height="512" fill="#fff"/><circle cx="470" cy="58" r="92" fill="#000"/><circle cx="372" cy="14" r="52" fill="#000"/><circle cx="500" cy="160" r="52" fill="#000"/></mask></defs><rect width="512" height="512" rx="120" style="fill:var(--logo)" mask="url(#lgb)"/><path d="M256 96l138.6 80v160L256 416l-138.6-80V176z" fill="#FFFDF8" stroke="#FFFDF8" stroke-width="34" stroke-linejoin="round"/><ellipse cx="180" cy="300" rx="26" ry="15" fill="#F0717A" fill-opacity=".4"/><ellipse cx="332" cy="300" rx="26" ry="15" fill="#F0717A" fill-opacity=".4"/><circle cx="208" cy="262" r="22" fill="#2C1A14"/><circle cx="304" cy="262" r="22" fill="#2C1A14"/><path d="M230 302q26 28 52 0" fill="none" stroke="#2C1A14" stroke-width="14" stroke-linecap="round"/></svg>';
  }
  function applyThemeColor() { try { var m = $('meta[name="theme-color"]:not([media])'); if (m) m.content = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim(); } catch (e) { } }
  function applyLogo() {
    var k = S.set.logo || 'red', c = LOGO[0][2];
    LOGO.forEach(function (x) { if (x[0] === k) c = x[2]; });
    if (window.__theme) window.__theme(c); else document.documentElement.style.setProperty('--logo', c);
    applyThemeColor();
    // 홈 화면에 추가할 때 쓰는 아이콘도 같은 색으로
    // 홈 화면 아이콘은 index.html이 읽어 들일 때 정한다(나중에 바꾸면 아이폰이 아이콘을 못 받음)
  }
  function installTip() {
    var standalone = document.documentElement.classList.contains('standalone') || window.navigator.standalone || (window.matchMedia && matchMedia('(display-mode: standalone)').matches);
    if (standalone || S.tip >= 2) return '';
    var ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
    return '<section class="tipcard card"><b>앱처럼 쓰기</b><p>' + (ios ? 'Safari 아래 공유 단추 → <b>홈 화면에 추가</b>를 누르면 인터넷이 없어도 열려요.' : '브라우저 메뉴에서 <b>홈 화면에 추가</b>(앱 설치)를 누르면 인터넷이 없어도 열려요.') + '</p><button class="tbtn" data-act="tipx">알겠어요</button></section>';
  }
  AFTER.home = function () {
    var r = $('.hero .rfg');
    if (r && !reduced) { var c = r.style.getPropertyValue('--c'); var off = r.getAttribute('stroke-dashoffset'); r.setAttribute('stroke-dashoffset', c); requestAnimationFrame(function () { requestAnimationFrame(function () { r.setAttribute('stroke-dashoffset', off); }); }); }
  };

  /* ---------- 판 만들기 ---------- */
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function pickN(a, n) { return shuffle(a).slice(0, n); }
  function orderNew(qs) { return qs.slice().sort(function (a, b) { return a.topic.order - b.topic.order || a.n - b.n; }); }

  function buildMix(size) {
    var pool = Q.filter(inScope), now = Date.now();
    var wrong = pool.filter(function (q) { var s = S.q[q.id]; return s && s.b === 0; }).sort(function (a, b) { return S.q[a.id].l - S.q[b.id].l; });
    var due = pool.filter(function (q) { var s = S.q[q.id]; return s && s.b > 0 && s.d <= now; }).sort(function (a, b) { return S.q[a.id].d - S.q[b.id].d; });
    var news = orderNew(pool.filter(function (q) { return !S.q[q.id] && !q.topic.hidden; }));
    var links = pool.filter(function (q) { return q.topic.hidden && !S.q[q.id]; });
    var rev = wrong.slice(0, 3).concat(due.slice(0, 3));
    var nNew = size - rev.length;
    // 새 문제: 지금 배우는 주제부터 차례로, 같은 주제에서는 섞기 (O/X가 몰리지 않게)
    var fr = [];
    if (news.length) {
      var tset = [], byT = {};
      news.forEach(function (q) { if (!byT[q.t]) { byT[q.t] = []; tset.push(q.t); } byT[q.t].push(q); });
      for (var i = 0; i < tset.length && fr.length < nNew; i++) {
        var list = byT[tset[i]];
        // 앞쪽(개념 순서) 위주로 고르고 그 안에서 섞기
        var take = list.slice(0, Math.max(nNew - fr.length, 0) + 3);
        fr = fr.concat(shuffle(take).slice(0, nNew - fr.length));
      }
    }
    if (links.length && fr.length >= 4 && Math.random() < 0.6) fr[fr.length - 1] = pickN(links, 1)[0];
    var picked = rev.concat(fr);
    if (picked.length < size) {
      var rest = wrong.slice(3).concat(due.slice(3));
      picked = picked.concat(rest.slice(0, size - picked.length));
    }
    if (picked.length < size) {
      var seen = pool.filter(function (q) { return S.q[q.id] && picked.indexOf(q) < 0; }).sort(function (a, b) { return (S.q[a.id].b - S.q[b.id].b) || (S.q[a.id].l - S.q[b.id].l); });
      picked = picked.concat(seen.slice(0, size - picked.length));
    }
    // 복습은 사이사이에
    var revs = picked.filter(function (q) { return S.q[q.id]; }), nw = picked.filter(function (q) { return !S.q[q.id]; });
    var out = [], ri = 0;
    for (var k = 0; k < nw.length; k++) { if (k % 2 === 0 && ri < revs.length) out.push(revs[ri++]); out.push(nw[k]); }
    while (ri < revs.length) out.push(revs[ri++]);
    return out.slice(0, size);
  }
  function withLearn(list) {
    var out = [], shown = {};
    list.forEach(function (q) {
      if (!q.topic.hidden && !seenTopic(q.t) && !shown[q.t] && !S.q[q.id]) { out.push({ learn: q.t }); shown[q.t] = 1; }
      out.push(q);
    });
    return out;
  }

  /* 구조식 문제 만들기 */
  var MOLPOOL = ['methane', 'ethane', 'propane', 'butane', 'ethene', 'ethyne', 'methanol', 'ethanol', 'glycol', 'glycerol', 'formaldehyde', 'acetaldehyde', 'formic', 'acetic', 'ethylacetate', 'glucose', 'alanine', 'leucine', 'aspartic', 'serine', 'vinylchloride', 'pe', 'pvc', 'isoprene', 'chloroprene', 'rubber', 'neoprene', 'hmda', 'adipoyl', 'nylon', 'anhydride', 'terephthalic', 'pet', 'salicylic', 'aspirin', 'ribose', 'deoxyribose'];
  function molInScope(k) { var t = TI[MOLT[k]]; return t && uIn(t.u); }
  function genMol(kind, k) {
    var m = MOL.db[k], others = MOLPOOL.filter(function (x) { return x !== k; });
    var same = others.filter(function (x) { return MOL.db[x].cat === m.cat; });
    var near = shuffle(same).concat(shuffle(others.filter(function (x) { return same.indexOf(x) < 0; })));
    var t = TI[MOLT[k]] || TI.fg;
    if (kind === 'name') {
      return { id: 'g-n-' + k, k: 'mc', q: '이 구조식의 물질은?', fig: k, a: m.name, o: near.slice(0, 3).map(function (x) { return MOL.db[x].name; }), e: m.name + (m.f ? ' (`' + m.f + '`)' : '') + '. ' + molNote(k), t: t.id, topic: t, u: t.u, gen: 1 };
    }
    return { id: 'g-s-' + k, k: 'mc', q: '**' + m.name + '**의 구조식은?', a: '@' + k, o: near.slice(0, 3).map(function (x) { return '@' + x; }), e: molNote(k), t: t.id, topic: t, u: t.u, gen: 1 };
  }
  function molNote(k) {
    var N = { methane: '정사면체, LNG.', ethene: 'C=C 한 개, 식물 호르몬.', ethyne: 'C≡C 한 개, 용접.', glycol: 'OH 2개, 부동액.', glycerol: 'OH 3개, 보습.', glucose: '-CHO가 있어 은거울 반응.', formic: 'H-C=O 부분이 알데하이드 특징.', ethylacetate: '사과 향 에스터.', pvc: 'Cl이 달린 반복 단위.', pet: '벤젠 고리 + 에스터 결합.', nylon: '아마이드 결합.', isoprene: '천연고무 단위체, -CH3.', chloroprene: '네오프렌 단위체, -Cl.', aspirin: '살리실산의 -OH가 에스터로.', salicylic: '-OH와 -COOH.', ribose: "2′에 OH, RNA.", deoxyribose: "2′에 H, DNA.", terephthalic: 'PET 단위체.', hmda: '나일론 단위체(-NH2 두 개).', adipoyl: '나일론 단위체(-COCl 두 개).', anhydride: '아스피린 합성 반응물.' };
    return N[k] || '';
  }
  function buildMol(size) {
    var fixed = Q.filter(function (q) { return inScope(q) && !q.topic.hidden && (q.fig || q.k === 'bd' || (typeof q.a === 'string' && q.a[0] === '@')); });
    var keys = MOLPOOL.filter(molInScope), gen = [];
    keys.forEach(function (k) { gen.push(genMol('name', k)); gen.push(genMol('pick', k)); });
    var all = fixed.concat(gen);
    all.sort(function (a, b) { return (box(a.id) - box(b.id)) || (Math.random() - 0.5); });
    var weak = all.slice(0, Math.min(all.length, size * 2));
    return shuffle(weak).slice(0, size);
  }
  function buildKinds(kinds, size) {
    var pool = Q.filter(function (q) { return inScope(q) && kinds.indexOf(q.k) >= 0; });
    var chainQs = S.scope === 'all' || S.scope === 'c' ? chainQuestions(null).filter(function (q) { return q.k === 'sq'; }) : [];
    pool = pool.concat(chainQs);
    pool.sort(function (a, b) { return (box(a.id) - box(b.id)) || (Math.random() - 0.5); });
    return shuffle(pool.slice(0, size * 2)).slice(0, size);
  }
  function buildTopic(tid) {
    var t = TI[tid], qs = t.qs;
    var un = qs.filter(function (q) { return !S.q[q.id]; });
    var wr = qs.filter(function (q) { var s = S.q[q.id]; return s && s.b < 3; });
    var list = un.length ? un.slice(0, 10) : shuffle(wr.length ? wr : qs).slice(0, 10);
    if (un.length && list.length < 10) list = list.concat(shuffle(wr).slice(0, 10 - list.length));
    return shuffle(list);
  }
  function chainQuestions(cid) {
    var out = [];
    C.CHAINS.forEach(function (ch) {
      if (cid && ch.id !== cid) return;
      var nodes = ch.steps.filter(function (s) { return s.n; });
      var t = TI[{ glu: 'ferm', nit: 'nfix', meth: 'alc', oil: 'plas', rub: 'rubber', asp: 'drug', redox: 'anti' }[ch.id]];
      if (nodes.length >= 3) {
        var start = Math.max(0, Math.min(nodes.length - 4, Math.floor(Math.random() * (nodes.length - 2))));
        var seg = nodes.slice(0, Math.min(nodes.length, 6));
        out.push({ id: 'c-' + ch.id + '-seq', k: 'sq', q: '「' + ch.name + '」 흐름을 순서대로 놓아요.', s: seg.map(function (s) { return s.n; }), e: seg.map(function (s) { return s.n; }).join(' → '), t: t.id, topic: t, u: t.u, gen: 1 });
      }
      for (var i = 0; i < ch.steps.length; i++) {
        var s = ch.steps[i];
        if (!s.a) continue;
        var prev = ch.steps[i - 1], next = ch.steps[i + 1];
        if (!prev || !next) continue;
        var wrongs = [];
        C.CHAINS.forEach(function (c2) { c2.steps.forEach(function (x) { if (x.n && x.n !== next.n && x.n !== prev.n) wrongs.push(x.n); }); });
        var sameChain = ch.steps.filter(function (x) { return x.n && x.n !== next.n && x.n !== prev.n; }).map(function (x) { return x.n; });
        var opts = shuffle(sameChain).slice(0, 2);
        shuffle(wrongs).forEach(function (w) { if (opts.length < 3 && opts.indexOf(w) < 0) opts.push(w); });
        out.push({ id: 'c-' + ch.id + '-' + i, k: 'mc', q: '**' + prev.n + '** → [' + s.a + '] → ?', a: next.n, o: opts, e: (next.d || ''), t: t.id, topic: t, u: t.u, gen: 1, fig: next.m && MOL.has(next.m) ? null : null });
      }
    });
    return out;
  }

  function wsCmp(a, b) { var A = String(a).match(/\d+/g).map(Number), Bb = String(b).match(/\d+/g).map(Number); for (var i = 0; i < Math.max(A.length, Bb.length); i++) { var d = (A[i] || 0) - (Bb[i] || 0); if (d) return d; } return 0; }
  function startRound(mode, p) {
    p = p || {};
    var list, title;
    if (mode === 'mix') { list = withLearn(buildMix(10)); title = '한 판'; }
    else if (mode === 'mol') { list = buildMol(10); title = '구조식'; }
    else if (mode === 'link') { list = buildKinds(['sq', 'mt', 'pk', 'so', 'tb', 'cz'], 8); title = '순서·짝 맞추기'; }
    else if (mode === 'topic') { list = buildTopic(p.t); if (!seenTopic(p.t)) list.unshift({ learn: p.t }); title = TI[p.t].name; }
    else if (mode === 'wrong') { var w = noteQs(Q.filter(inScope)).sort(function (a, b) { return S.q[a.id].b - S.q[b.id].b; }); list = shuffle(w.slice(0, 20)).slice(0, 10); title = '오답 다시'; }
    else if (mode === 'chain') { list = shuffle(chainQuestions(p.c)).slice(0, 8); title = '이야기 줄'; }
    else if (mode === 'trip') { var tr = TRI[p.id]; list = tr.steps.slice(); title = tr.name; tr.steps.forEach(function (q) { q._o = q._l = q._r = q._bank = null; }); }
    else if (mode === 'ws') { list = Q.filter(function (q) { return q.wa === p.a; }).sort(function (a, b) { return wsCmp(a.ws, b.ws); }); title = '탐구활동 ' + p.a; }
    else if (mode === 'cz') { var czs = Q.filter(function (q) { return q.k === 'cz' && inScope(q); }); czs.sort(function (a, b) { return (box(a.id) - box(b.id)) || (Math.random() - 0.5); }); list = shuffle(czs.slice(0, 20)).slice(0, 10); title = 'PPT 문장'; }
    else if (mode === 'bg') { list = shuffle(Q.filter(function (q) { return q.k === 'bg' && inScope(q); })).slice(0, 8); title = '보기 문제'; }
    else list = [];
    if (!list.length) { toast('이 범위에는 아직 문제가 없어요'); return; }
    R = { mode: mode, p: p, title: title, list: list, i: 0, ok: 0, total: 0, combo: 0, maxc: 0, learned: 0, wrong: [], retried: {}, firstNew: 0, t0: Date.now(), mols: [], trip: mode === 'trip' ? TRI[p.id] : null };
    go('quiz', {});
  }

  /* ---------- 문제 화면 ---------- */
  SCREENS.quiz = function () {
    if (!R) return '<div class="empty"><p>진행 중인 판이 없어요.</p><button class="big" data-act="home">처음으로</button></div>';
    return '<header class="qtop"><button class="ibtn" data-act="quit" aria-label="그만하기">' + ic('x') + '</button>' +
      '<div class="qprog" id="qprog"></div><div class="combo" id="combo"></div></header>' +
      '<main class="qmain" id="qmain"></main><div class="sheet" id="sheet"></div>';
  };
  AFTER.quiz = function () { if (R) renderItem(); };
  function progHtml() {
    var n = R.list.length, h = '';
    for (var i = 0; i < n; i++) {
      var it = R.list[i], c = i < R.i ? (it._res === 1 ? 'ok' : it._res === 0 ? 'no' : 'done') : i === R.i ? 'cur' : '';
      if (it.learn || it.k === 'say') c += ' lr';
      h += '<i class="' + c + '"></i>';
    }
    return h;
  }
  function renderItem() {
    var it = R.list[R.i];
    $('#qprog').innerHTML = progHtml();
    var main = $('#qmain'), sh = $('#sheet');
    sh.className = 'sheet'; sh.innerHTML = '';
    if (!it) return finishRound();
    if (it.learn) { main.innerHTML = learnCard(TI[it.learn]); main.className = 'qmain enter'; return; }
    if (it.k === 'say') { main.innerHTML = sayCard(it); main.className = 'qmain enter'; R.cur = { done: true }; return; }
    R.cur = { q: it, picked: [], done: false, mtSel: null, mtDone: {}, mtMiss: 0, sqPlaced: [], vals: [], sel: 0, bgv: [], sov: [] };
    main.innerHTML = questionHtml(it);
    main.className = 'qmain enter';
    void main.offsetWidth;
  }
  function learnCard(t) {
    var u = UI[t.u];
    return '<div class="learn card">' +
      '<div class="tape c-' + u.color + '">새 개념</div>' +
      '<div class="lhead">' + ic(t.icon, 'lic') + '<div><small>' + esc(u.name) + '</small><h2>' + esc(t.name) + '</h2></div></div>' +
      '<ol class="lkeys">' + t.key.map(function (l, i) { return '<li style="--d:' + i + '">' + fmt(l) + '</li>'; }).join('') + '</ol>' +
      '<div class="lbtns"><button class="big primary" data-act="learned" data-t="' + t.id + '">알겠어요, 풀어 볼게요' + ic('arrow') + '</button><button class="tbtn" data-act="peek" data-t="' + t.id + '">노트 자세히 보기</button></div></div>';
  }
  function sayCard(it) {
    var trip = R.trip, n = R.list.slice(0, R.i + 1).filter(function (x) { return x.k === 'say'; }).length;
    return '<div class="say card">' + (trip ? '<div class="tape c-' + UI[trip.u].color + '">탐험 · ' + esc(trip.name) + '</div>' : '') +
      '<h2>' + fmt(it.h) + '</h2><p>' + fmt(it.tx) + '</p>' + figHtml(it.fig) +
      '<button class="big primary" data-act="sayok">' + pick(['다음', '오, 그렇구나', '좋아요, 계속']) + ic('arrow') + '</button></div>';
  }
  function figHtml(f) {
    if (!f) return '';
    if (f.indexOf('fig:') === 0) return FIG[f.slice(4)] ? '<figure class="nfig fig">' + FIG[f.slice(4)]() + '</figure>' : '';
    return '<figure class="qfig">' + MOL.svg(f, { anim: true, scale: 1.2 }) + '</figure>';
  }
  function kindLabel(k) { return { mc: '고르기', ox: 'O / X', sq: '순서대로', mt: '짝 맞추기', pk: '모두 고르기', tb: '빈 칸 채우기', cz: '문장 빈칸', bd: '구조식 완성', bg: '보기 고르기', so: '분류하기' }[k]; }
  function bankOf(q) {
    if (q._bank) return q._bank;
    var seen = {}, out = [];
    function addv(v) { var k = v.trim(); if (!seen[k]) { seen[k] = 1; out.push(k); } }
    tbBlanks(q).forEach(addv);
    (q.bank || []).forEach(addv);
    return (q._bank = shuffle(out));
  }
  function tbBlanks(q) { if (q.k === 'cz') return q.a.slice(); var a = []; q.rows.forEach(function (r) { r.forEach(function (c) { if (c[0] === '?') a.push(c.slice(1).trim()); }); }); return a; }
  function blankBtn(i, ans, cur, inl) {
    var v = cur.vals[i], done = cur.done, cls = 'tbk' + (inl ? ' inl' : '') + (v != null ? ' full' : '') + (!done && cur.sel === i ? ' on' : '');
    if (done) cls += v === ans ? ' right' : ' wrongc';
    var inner = v != null ? fmt(v) : '<span class="qmk">?</span>';
    if (done && v !== ans) inner = (v != null ? '<s>' + fmt(v) + '</s>' : '') + '<b>' + fmt(ans) + '</b>';
    return '<button class="' + cls + '" data-act="tbc" data-b="' + i + '">' + inner + '</button>';
  }
  function czHtml(q, cur) {
    var i = 0, parts = q.cs.split(/\[\[(.+?)\]\]/), h = '<p class="czs">';
    parts.forEach(function (p, k) { h += k % 2 ? blankBtn(i++, p.trim(), cur, true) : fmt(p); });
    return h + '</p>';
  }
  function tbHtml(q, cur) {
    if (q.k === 'cz') return czHtml(q, cur);
    var b = 0, done = cur.done, h = '<div class="tscroll tbq"><table>';
    q.rows.forEach(function (r, ri) {
      h += '<tr>' + r.map(function (c) {
        if (c[0] === '!') return '<th>' + fmt(c.slice(1)) + '</th>';
        if (c[0] !== '?') return '<td class="tgiven">' + fmt(c) + '</td>';
        var i = b++, v = cur.vals[i], ans = c.slice(1).trim(), cls = 'tbk' + (v != null ? ' full' : '') + (!done && cur.sel === i ? ' on' : '');
        if (done) cls += v === ans ? ' right' : ' wrongc';
        var inner = v != null ? fmt(v) : '<span class="qmk">?</span>';
        if (done && v !== ans) inner = (v != null ? '<s>' + fmt(v) + '</s>' : '') + '<b>' + fmt(ans) + '</b>';
        return '<td><button class="' + cls + '" data-act="tbc" data-b="' + i + '">' + inner + '</button></td>';
      }).join('') + '</tr>';
    });
    return h + '</table></div>';
  }
  function tileLabel(t) { return t === '-' ? '<span class="bt">─</span> 단일 결합' : t === '=' ? '<span class="bt">═</span> 이중 결합' : t === '≡' ? '<span class="bt">≡</span> 삼중 결합' : chem(t); }
  function isBond(v) { return v === '-' || v === '=' || v === '≡'; }
  function bdSvg(q, cur) {
    var bad = {}, good = {};
    if (cur.done) q.a.forEach(function (a, i) { if (cur.vals[i] === a) good[i] = 1; else bad[i] = 1; });
    return MOL.ascii(q.src, { vals: cur.done ? q.a.map(function (a, i) { return cur.vals[i] === a ? a : a; }) : cur.vals, sel: cur.done ? -1 : cur.sel, bad: bad, good: good, scale: 1.45 });
  }
  function extrasHtml(q) {
    var h = '';
    if (q.box) h += '<div class="qbox">' + String(q.box).split('\n').map(fmt).join('<br>') + '</div>';
    if (q.figs) h += '<div class="qfigs">' + q.figs.map(function (f) { return '<figure>' + MOL.svg(f[0], { anim: true }) + '<figcaption>' + esc(f[1]) + '</figcaption></figure>'; }).join('') + '</div>';
    return h;
  }
  function questionHtml(q) {
    var t = q.topic, h = '<div class="qhead">' + (q.les ? '<span class="qtag trip">탐험 · ' + esc(R && R.trip ? R.trip.name : '') + '</span>' : q.src ? '<span class="qws ppt">PPT ' + esc(q.src) + '</span>' : q.ws ? '<span class="qws">탐구활동 ' + esc(q.ws) + '</span>' : '<span class="qtag">' + esc(t.hidden ? '연결' : t.name) + '</span>') + '<span class="qkind">' + kindLabel(q.k) + '</span>' + (q.les || S.q[q.id] ? '' : '<span class="qnew">처음</span>') + '</div>';
    h += '<h2 class="qq' + (q.q.length > 70 ? ' long' : '') + '">' + fmt(q.q) + '</h2>' + extrasHtml(q);
    if (q.fig) h += '<figure class="qfig">' + MOL.svg(q.fig, { anim: true, scale: 1.3 }) + '</figure>';
    var opts;
    if (q.k === 'mc') {
      if (!q._o) q._o = shuffle([q.a].concat(q.o));
      opts = q._o;
      var molc = typeof q.a === 'string' && q.a[0] === '@';
      h += '<div class="choices' + (molc ? ' molgrid' : '') + '">' + opts.map(function (c, i) {
        return '<button class="ch" data-act="pick" data-i="' + i + '"><span class="key">' + (i + 1) + '</span><span class="ct">' + choiceHtml(c) + '</span></button>';
      }).join('') + '</div>';
    } else if (q.k === 'ox') {
      h += '<div class="oxrow"><button class="oxb o" data-act="ox" data-v="1"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="13"/></svg><span>맞아요</span></button><button class="oxb x" data-act="ox" data-v="0"><svg viewBox="0 0 40 40"><path d="M10 10l20 20M30 10L10 30"/></svg><span>아니에요</span></button></div>';
    } else if (q.k === 'pk') {
      if (!q._o) q._o = shuffle(q.a.concat(q.o));
      h += '<p class="qhint">맞는 것을 모두 누른 뒤 확인을 눌러요. 정답 ' + q.a.length + '개</p>';
      h += '<div class="choices pk">' + q._o.map(function (c, i) {
        return '<button class="ch" data-act="pk" data-i="' + i + '"><span class="box">' + ic('check') + '</span><span class="ct">' + choiceHtml(c) + '</span></button>';
      }).join('') + '</div><button class="big primary" data-act="pkok" id="pkok" disabled>확인</button>';
    } else if (q.k === 'sq') {
      if (!q._o) { var o = shuffle(q.s); while (q.s.length > 1 && o.join('|') === q.s.join('|')) o = shuffle(q.s); q._o = o; }
      h += '<ol class="slots" id="slots">' + q.s.map(function (_, i) { return '<li data-i="' + i + '"><span class="sn">' + (i + 1) + '</span><span class="sv"></span></li>'; }).join('') + '</ol>';
      h += '<p class="qhint">앞에서부터 차례로 눌러요. 놓은 것을 누르면 빠져요.</p>';
      h += '<div class="pool" id="pool">' + q._o.map(function (c, i) { return '<button class="pc" data-act="sqp" data-i="' + i + '">' + fmt(c) + '</button>'; }).join('') + '</div>';
    } else if (q.k === 'mt') {
      if (!q._l) { q._l = shuffle(q.p.map(function (p, i) { return i; })); q._r = shuffle(q.p.map(function (p, i) { return i; })); }
      h += '<p class="qhint">왼쪽 하나, 오른쪽 하나를 차례로 눌러 이어요.</p><div class="mt">' +
        '<div class="mcol">' + q._l.map(function (i) { return '<button class="mi" data-act="mtl" data-i="' + i + '">' + fmt(q.p[i][0]) + '</button>'; }).join('') + '</div>' +
        '<div class="mcol">' + q._r.map(function (i) { return '<button class="mi" data-act="mtr" data-i="' + i + '">' + fmt(q.p[i][1]) + '</button>'; }).join('') + '</div></div>';
    } else if (q.k === 'tb') {
      h += '<p class="qhint">빈 칸을 누르고 아래 낱말 카드를 골라요. 같은 카드를 여러 번 써도 돼요.</p><div id="tbw">' + tbHtml(q, { vals: [], sel: 0 }) + '</div>';
      h += '<div class="tiles" id="tiles">' + bankOf(q).map(function (v, i) { return '<button class="tile" data-act="tbt" data-v="' + i + '">' + fmt(v) + '</button>'; }).join('') + '</div><button class="big primary" data-act="chk" id="chk" disabled>확인</button>';
    } else if (q.k === 'cz') {
      h += '<div id="tbw" class="czw">' + czHtml(q, { vals: [], sel: 0 }) + '</div>';
      h += '<div class="tiles" id="tiles">' + bankOf(q).map(function (v, i) { return '<button class="tile" data-act="tbt" data-v="' + i + '">' + fmt(v) + '</button>'; }).join('') + '</div><button class="big primary" data-act="chk" id="chk" disabled>확인</button>';
    } else if (q.k === 'bd') {
      h += '<p class="qhint">물음표(?)나 점선을 누르고 아래 카드로 채워요. 탄소는 결합 4개!</p><div class="bdwrap" id="bdw">' + bdSvg(q, { vals: [], sel: 0 }) + '</div>';
      h += '<div class="tiles" id="tiles">' + q.tiles.map(function (v, i) { return '<button class="tile' + (isBond(v) ? ' bond' : ' atom') + '" data-act="bdt" data-v="' + i + '">' + tileLabel(v) + '</button>'; }).join('') + '</div><button class="big primary" data-act="chk" id="chk" disabled>확인</button>';
    } else if (q.k === 'bg') {
      var L = 'ㄱㄴㄷㄹ';
      h += '<div class="bgbox"><span class="bgt">보기</span>' + q.items.map(function (it, i) {
        return '<div class="bgi" data-i="' + i + '"><p><b>' + L[i] + '.</b> ' + fmt(it[0]) + '</p><div class="bgb"><button data-act="bgv" data-i="' + i + '" data-v="1" aria-label="옳다">' + 'O' + '</button><button data-act="bgv" data-i="' + i + '" data-v="0" aria-label="옳지 않다">' + 'X' + '</button></div></div>';
      }).join('') + '</div><p class="qhint">ㄱ, ㄴ, ㄷ이 각각 옳은지 판단해요. 옳은 것만 모으면 답이에요.</p><button class="big primary" data-act="chk" id="chk" disabled>확인</button>';
    } else if (q.k === 'so') {
      if (!q._o) q._o = shuffle(q.items.map(function (x, i) { return i; }));
      h += '<div class="solist">' + q._o.map(function (i) {
        return '<div class="soi" data-i="' + i + '"><span class="sot">' + fmt(q.items[i][0]) + '</span><div class="seg sob">' + q.buckets.map(function (b, j) { return '<button data-act="sov" data-i="' + i + '" data-b="' + j + '">' + fmt(b) + '</button>'; }).join('') + '</div></div>';
      }).join('') + '</div><button class="big primary" data-act="chk" id="chk" disabled>확인</button>';
    }
    return h;
  }
  function answer(ok, el, detail) {
    var cur = R.cur, q = R.list[R.i];
    if (cur.done) return;
    cur.done = true;
    var retry = !!q._retry;
    var res = q.les ? {} : record(q, ok, retry);
    q._res = ok ? 1 : 0;
    if (!retry) { R.total++; if (ok) R.ok++; }
    if (ok) {
      R.combo++; R.maxc = Math.max(R.maxc, R.combo);
      SND.ok(); vib(12); burst(el, 'ok');
      if (R.combo >= 3) { var cb = $('#combo'); if (cb) { cb.innerHTML = ic('flame') + '<b>' + R.combo + '</b>연속'; cb.className = 'combo show'; void cb.offsetWidth; cb.classList.add('pop'); } if (R.combo % 5 === 0) SND.combo(R.combo); }
      if (res.learned) { R.learned++; floatText(el, '외웠어요', 'learnt'); }
    } else {
      R.combo = 0; var cb2 = $('#combo'); if (cb2) cb2.className = 'combo';
      SND.no(); vib([30, 50, 30]); shake(el && el.closest ? (el.closest('.choices,.oxrow,.mt,.slots') || el) : el);
      R.wrong.push(q);
      if (!retry && !R.retried[q.id] && R.list.length < 18) { R.retried[q.id] = 1; var copy = Object.create(q); copy._retry = 1; copy._res = undefined; copy.cur = null; R.list.push(copy); }
    }
    if (q.fig) R.mols.push(q.fig);
    var tdone = !q.les && topicDone(q.topic);
    $('#qprog').innerHTML = progHtml();
    showSheet(q, ok, detail);
    if (tdone) setTimeout(function () { toast(ic('star') + '<span><b>' + esc(q.topic.name) + '</b> 전부 외웠어요</span>', 'gold'); }, 500);
  }
  function topicDone(t) {
    if (t.hidden || !t.qs.length) return false;
    var all = t.qs.every(function (q) { return box(q.id) >= 3; });
    if (all && !(S.done || {})[t.id]) { S.done = S.done || {}; S.done[t.id] = 1; save(); return true; }
    return false;
  }
  function correctText(q) {
    if (q.k === 'mc') return choiceHtml(q.a);
    if (q.k === 'ox') return q.a ? '맞아요 (O)' : '아니에요 (X)';
    if (q.k === 'pk') return q.a.map(fmt).join(' · ');
    if (q.k === 'sq') return q.s.map(fmt).join(' → ');
    if (q.k === 'mt') return q.p.map(function (p) { return fmt(p[0]) + ' – ' + fmt(p[1]); }).join('<br>');
    if (q.k === 'tb') return tbBlanks(q).map(fmt).join(' · ');
    if (q.k === 'cz') return fmt(q.cs.replace(/\[\[(.+?)\]\]/g, '**$1**'));
    if (q.k === 'bd') return MOL.ascii(q.src, { vals: q.a });
    if (q.k === 'bg') return q.items.map(function (it, i) { return 'ㄱㄴㄷㄹ'[i] + ' ' + (it[1] ? 'O' : 'X'); }).join(' · ');
    if (q.k === 'so') return q.buckets.map(function (b, j) { return '<b>' + fmt(b) + '</b>: ' + q.items.filter(function (x) { return x[1] === j; }).map(function (x) { return fmt(x[0]); }).join(', '); }).join('<br>');
    return '';
  }
  function showSheet(q, ok, detail) {
    var sh = $('#sheet');
    var head = ok ? '<div class="sh-h ok">' + ic('check') + '<b>' + pick(['정답', '좋아요', '맞아요', '정확해요']) + '</b>' + (q._retry ? '<small>다시 풀어 맞혔어요</small>' : '') + '</div>'
      : '<div class="sh-h no">' + ic('x') + '<b>' + pick(['아쉬워요', '다시 볼게요', '이건 헷갈리죠']) + '</b><small>이번 판 끝에 한 번 더 나와요</small></div>';
    var body = '';
    var showAns = (!ok || q.k === 'mt' || q.k === 'sq') && q.k !== 'tb' && q.k !== 'bd' && q.k !== 'bg' && q.k !== 'cz';
    if (q.k === 'cz') body += '<div class="sh-ans"><span>슬라이드</span><div>' + correctText(q) + '</div></div>';
    if (q.k === 'bg') body += '<div class="bgwhy">' + q.items.map(function (it, i) { return '<p><b class="' + (it[1] ? 'o' : 'x') + '">' + 'ㄱㄴㄷㄹ'[i] + ' ' + (it[1] ? 'O' : 'X') + '</b> ' + fmt(it[2]) + '</p>'; }).join('') + '</div>';
    if (showAns && q.k !== 'mc') body += '<div class="sh-ans"><span>정답</span><div>' + correctText(q) + '</div></div>';
    if (!ok && q.k === 'mc' && !(typeof q.a === 'string' && q.a[0] === '@')) body += '<div class="sh-ans"><span>정답</span><div>' + fmt(q.a) + '</div></div>' + (detail && detail.mine ? '<div class="sh-ans mine"><span>내 답</span><div>' + fmt(detail.mine) + '</div></div>' : '');
    if (!ok && q.k === 'mc' && typeof q.a === 'string' && q.a[0] === '@') body += '<div class="sh-ans"><span>정답</span><div>' + MOL.svg(q.a.slice(1)) + '<p>' + esc(MOL.db[q.a.slice(1)].name) + '</p></div></div>';
    if (q.e) body += '<p class="sh-e">' + fmt(q.e) + '</p>';
    sh.innerHTML = '<div class="sh-in">' + head + body + '<div class="sh-btns">' + (q.topic && !q.topic.hidden ? '<button class="tbtn" data-act="peek" data-t="' + q.t + '">' + ic('book') + '노트</button>' : '') + '<button class="big primary" data-act="next" id="nextb">다음' + ic('arrow') + '</button></div></div>';
    sh.className = 'sheet show ' + (ok ? 'ok' : 'no');
    if (ok && S.set.auto && !q.e) setTimeout(function () { if (R && R.cur && R.cur.done) next(); }, 900);
    else if (ok && S.set.auto) { clearTimeout(R.autoT); R.autoT = setTimeout(function () { if (R && R.cur && R.cur.done && view.name === 'quiz') next(); }, 1800); }
  }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function next() {
    if (!R) return;
    clearTimeout(R.autoT);
    R.i++;
    var main = $('#qmain');
    if (main && !reduced) {
      main.className = 'qmain leave';
      setTimeout(renderItem, 140);
    } else renderItem();
  }

  /* 고르기 처리 */
  function onPick(i, el) {
    var q = R.list[R.i], c = q._o[i], ok = c === q.a;
    $$('.choices .ch').forEach(function (b, j) {
      b.disabled = true;
      if (q._o[j] === q.a) b.classList.add('right');
    });
    if (!ok) el.classList.add('wrongc');
    answer(ok, el, ok ? null : { mine: c });
  }
  function onOx(v, el) {
    var q = R.list[R.i], ok = (v === 1) === !!q.a;
    $$('.oxb').forEach(function (b) { b.disabled = true; if ((b.dataset.v === '1') === !!q.a) b.classList.add('right'); });
    if (!ok) el.classList.add('wrongc');
    answer(ok, el);
  }
  function onPk(i, el) {
    if (R.cur.done) return;
    el.classList.toggle('sel');
    var n = $$('.choices.pk .ch.sel').length;
    $('#pkok').disabled = n === 0;
    SND.tap();
  }
  function onPkOk() {
    var q = R.list[R.i], sel = [];
    $$('.choices.pk .ch').forEach(function (b, j) { if (b.classList.contains('sel')) sel.push(q._o[j]); b.disabled = true; });
    var ok = sel.length === q.a.length && sel.every(function (s) { return q.a.indexOf(s) >= 0; });
    $$('.choices.pk .ch').forEach(function (b, j) {
      var isA = q.a.indexOf(q._o[j]) >= 0, isS = b.classList.contains('sel');
      if (isA) b.classList.add('right'); if (isS && !isA) b.classList.add('wrongc'); if (isA && !isS) b.classList.add('missed');
    });
    $('#pkok').disabled = true;
    answer(ok, $('#pkok'));
  }
  function onSq(i, el) {
    var q = R.list[R.i], cur = R.cur;
    if (cur.done || el.classList.contains('used')) return;
    cur.sqPlaced.push(i); el.classList.add('used'); SND.tap();
    paintSlots();
    if (cur.sqPlaced.length === q.s.length) {
      var got = cur.sqPlaced.map(function (k) { return q._o[k]; });
      var ok = got.join('\u0001') === q.s.join('\u0001');
      $$('#slots li').forEach(function (li, j) { li.classList.add(got[j] === q.s[j] ? 'right' : 'wrongc'); });
      $$('#pool .pc').forEach(function (b) { b.disabled = true; });
      answer(ok, $('#slots'));
    }
  }
  function onSlot(j) {
    var cur = R.cur; if (cur.done) return;
    if (j >= cur.sqPlaced.length) return;
    var k = cur.sqPlaced.splice(j, 1)[0];
    var b = $('#pool .pc[data-i="' + k + '"]'); if (b) b.classList.remove('used');
    paintSlots();
  }
  function paintSlots() {
    var q = R.list[R.i], cur = R.cur;
    $$('#slots li').forEach(function (li, j) {
      var k = cur.sqPlaced[j];
      li.querySelector('.sv').innerHTML = k == null ? '' : fmt(q._o[k]);
      li.classList.toggle('filled', k != null);
      li.dataset.act = k != null ? 'slot' : '';
    });
  }
  function onMt(side, i, el) {
    var q = R.list[R.i], cur = R.cur;
    if (cur.done || cur.mtDone[i] && el.classList.contains('done')) return;
    if (side === 'l') {
      $$('.mcol:first-child .mi').forEach(function (b) { b.classList.remove('sel'); });
      if (el.classList.contains('done')) return;
      el.classList.add('sel'); cur.mtSel = i; SND.tap(); return;
    }
    if (cur.mtSel == null) { shake(el); return; }
    if (el.classList.contains('done')) return;
    var lb = $('.mcol:first-child .mi[data-i="' + cur.mtSel + '"]');
    if (i === cur.mtSel) {
      lb.classList.remove('sel'); lb.classList.add('done'); el.classList.add('done');
      var n = Object.keys(cur.mtDone).length; lb.dataset.n = el.dataset.n = n + 1;
      lb.style.setProperty('--h', n); el.style.setProperty('--h', n);
      cur.mtDone[i] = 1; cur.mtSel = null; SND.tap(); vib(8);
      if (Object.keys(cur.mtDone).length === q.p.length) answer(cur.mtMiss === 0, el);
    } else {
      cur.mtMiss++; shake(el); shake(lb); vib(20);
      el.classList.add('miss'); setTimeout(function () { el.classList.remove('miss'); }, 400);
    }
  }

  /* 새 문제 종류 처리 */
  function nextEmpty(n, vals, from, okType) {
    for (var k = 1; k <= n; k++) { var j = (from + k) % n; if (vals[j] == null && (!okType || okType(j))) return j; }
    return -1;
  }
  function refreshChk() {
    var cur = R.cur, q = R.list[R.i], n = q.k === 'tb' || q.k === 'cz' ? tbBlanks(q).length : q.k === 'bd' ? q.a.length : q.items.length;
    var arr = q.k === 'bg' ? cur.bgv : q.k === 'so' ? cur.sov : cur.vals, c = 0;
    for (var i = 0; i < n; i++) if (arr[i] != null) c++;
    var b = $('#chk'); if (b) b.disabled = c < n;
  }
  function onTbCell(i) { var cur = R.cur; if (cur.done) return; cur.sel = i; paintTb(); SND.tap(); }
  function onTbTile(vi) {
    var cur = R.cur, q = R.list[R.i]; if (cur.done) return;
    var n = tbBlanks(q).length;
    if (cur.sel < 0 || cur.sel >= n) cur.sel = nextEmpty(n, cur.vals, -1);
    if (cur.sel < 0) return;
    cur.vals[cur.sel] = bankOf(q)[vi];
    var nx = nextEmpty(n, cur.vals, cur.sel); cur.sel = nx < 0 ? cur.sel : nx;
    SND.tap(); vib(6); paintTb(); refreshChk();
  }
  function paintTb() { var w = $('#tbw'), q = R.list[R.i]; if (w) w.innerHTML = tbHtml(q, R.cur); }
  function onBdBlank(i) { var cur = R.cur; if (cur.done) return; cur.sel = i; paintBd(); SND.tap(); }
  function onBdTile(vi) {
    var cur = R.cur, q = R.list[R.i]; if (cur.done) return;
    var v = q.tiles[vi], bond = isBond(v), n = q.a.length;
    var okT = function (j) { return isBond(q.a[j]) === bond; };
    if (cur.sel < 0 || cur.sel >= n || !okT(cur.sel)) {
      var e = nextEmpty(n, cur.vals, -1, okT);
      if (e < 0) { toast(bond ? '결합 자리가 다 찼어요. 바꿀 자리를 눌러요' : '원자 자리가 다 찼어요. 바꿀 자리를 눌러요'); return; }
      cur.sel = e;
    }
    cur.vals[cur.sel] = v;
    var nx = nextEmpty(n, cur.vals, cur.sel); if (nx >= 0) cur.sel = nx;
    SND.tap(); vib(6); paintBd(); refreshChk();
  }
  function paintBd() { var w = $('#bdw'), q = R.list[R.i]; if (w) w.innerHTML = bdSvg(q, R.cur); }
  function onBgv(i, v) {
    var cur = R.cur; if (cur.done) return;
    cur.bgv[i] = v; $$('.bgi[data-i="' + i + '"] .bgb button').forEach(function (b) { b.classList.toggle('on', +b.dataset.v === v); });
    SND.tap(); refreshChk();
  }
  function onSov(i, b) {
    var cur = R.cur; if (cur.done) return;
    cur.sov[i] = b; $$('.soi[data-i="' + i + '"] button').forEach(function (x) { x.classList.toggle('on', +x.dataset.b === b); });
    SND.tap(); refreshChk();
  }
  function onChk() {
    var cur = R.cur, q = R.list[R.i], ok = true, el = $('#chk');
    if (cur.done) return;
    if (q.k === 'tb' || q.k === 'cz') { tbBlanks(q).forEach(function (a, i) { if ((cur.vals[i] || '').trim() !== a) ok = false; }); cur.done = true; paintTb(); cur.done = false; }
    else if (q.k === 'bd') { q.a.forEach(function (a, i) { if (cur.vals[i] !== a) ok = false; }); cur.done = true; paintBd(); cur.done = false; }
    else if (q.k === 'bg') { q.items.forEach(function (it, i) { var r = (cur.bgv[i] === 1) === it[1]; if (!r) ok = false; $('.bgi[data-i="' + i + '"]').classList.add(r ? 'right' : 'wrongc'); }); }
    else if (q.k === 'so') { q.items.forEach(function (it, i) { var r = cur.sov[i] === it[1]; if (!r) ok = false; var row = $('.soi[data-i="' + i + '"]'); row.classList.add(r ? 'right' : 'wrongc'); $$('button', row).forEach(function (x) { if (+x.dataset.b === it[1]) x.classList.add('ans'); }); }); }
    $$('#tiles .tile, .bgb button, .sob button').forEach(function (b) { b.disabled = true; });
    if (el) el.disabled = true;
    answer(ok, q.k === 'tb' || q.k === 'cz' ? $('#tbw') : q.k === 'bd' ? $('#bdw') : el);
  }

  /* ---------- 결과 ---------- */
  function finishRound() {
    if (!R) return;
    R.done = true;
    if (R.trip) {
      S.trip = S.trip || {};
      var miss = R.total - R.ok, star = miss === 0 ? 3 : miss <= 2 ? 2 : 1, prev = S.trip[R.trip.id];
      R.star = star; R.firstTrip = !prev;
      S.trip[R.trip.id] = { at: Date.now(), star: Math.max(star, prev ? prev.star : 0) };
      R.trip.t.forEach(function (t) { S.seen[t] = S.seen[t] || Date.now(); });
      save();
    }
    SND.done();
    go('result', {}, true);
  }
  SCREENS.result = function () {
    if (!R) return SCREENS.home();
    if (R.trip) return tripResult();
    var pct = R.total ? R.ok / R.total : 0, sec = Math.round((Date.now() - R.t0) / 1000);
    var mk = R.mols.length ? R.mols[R.mols.length - 1] : resultMol();
    var msg = pct >= 0.9 ? '거의 다 맞혔어요' : pct >= 0.7 ? '잘하고 있어요' : pct >= 0.4 ? '반쯤 왔어요' : '처음엔 다 그래요';
    var wr = uniq(R.wrong);
    var qs = scopeQs();
    var h = '<div class="res">' +
      '<div class="rmol">' + MOL.svg(mk, { anim: true }) + '<small>' + esc(MOL.db[mk] ? MOL.db[mk].name : '') + '</small></div>' +
      '<p class="rmsg">' + msg + '</p>' +
      '<div class="rscore"><b id="rs">0</b><span>/ ' + R.total + '</span></div>' +
      '<div class="rstats"><div><b>' + R.maxc + '</b><span>최고 연속</span></div><div><b>' + R.learned + '</b><span>새로 외움</span></div><div><b>' + Math.floor(sec / 60) + ':' + ('0' + sec % 60).slice(-2) + '</b><span>걸린 시간</span></div></div>' +
      '<div class="rbar card"><div class="rbh"><span>' + esc(scopeName()) + ' 외운 정도</span><b>' + Math.round(mastery(qs) * 100) + '%</b></div>' + bar(mastery(qs), 'c-blue') + '</div>' +
      (wr.length ? '<div class="rwrong card"><h3>다시 볼 것</h3>' + wr.map(function (q) { return '<div class="rw"><p>' + fmt(q.q) + '</p><div class="ra">' + correctText(q) + '</div></div>'; }).join('') + '</div>' : '') +
      '<div class="rbtns"><button class="big primary" data-act="again">' + ic('redo') + '한 판 더</button><button class="big ghost" data-act="home">처음으로</button></div></div>';
    return h;
  };
  AFTER.result = function () { countUp($('#rs'), R ? R.ok : 0, 900); if (R && R.total && R.ok / R.total >= 0.8) setTimeout(function () { burst($('.rscore'), 'ok'); }, 500); };
  function resultMol() { var a = ['glucose', 'aspirin', 'ethylacetate', 'nylon', 'isoprene', 'dipeptide', 'pet']; return a[Math.floor(Math.random() * a.length)]; }
  function uniq(a) { var s = {}, o = []; a.forEach(function (q) { if (!s[q.id]) { s[q.id] = 1; o.push(q); } }); return o; }
  function scopeName() { return S.scope === 'all' ? '전체' : S.scope === 'c' ? '탄소 화합물' : UI[S.scope].short; }

  function stars(n) { var h = ''; for (var i = 0; i < 3; i++) h += '<i class="st' + (i < n ? ' on' : '') + '" style="--d:' + i + '">' + ic('star') + '</i>'; return h; }
  function tripResult() {
    var tr = R.trip, i = TRIPS.indexOf(tr), nx = TRIPS[i + 1], wr = uniq(R.wrong);
    return '<div class="res">' +
      '<div class="stars">' + stars(R.star) + '</div>' +
      '<p class="rmsg">' + (R.star === 3 ? '완벽해요' : R.star === 2 ? '거의 다 왔어요' : '끝까지 왔어요') + '</p>' +
      '<h2 class="trname">탐험 ' + (i + 1) + '. ' + esc(tr.name) + ' 완료</h2>' +
      '<p class="trsub">이제 이 내용은 \'한 판\'에서 처음 보는 문제로도 나와요. 노트에서 다시 볼 수 있어요.</p>' +
      (wr.length ? '<div class="rwrong card"><h3>다시 볼 것</h3>' + wr.map(function (q) { return '<div class="rw"><p>' + fmt(q.q) + '</p><div class="ra">' + correctText(q) + '</div></div>'; }).join('') + '</div>' : '') +
      '<div class="rbtns">' + (nx ? '<button class="big primary" data-act="trip" data-id="' + nx.id + '">' + ic('play') + '다음 탐험: ' + esc(nx.name) + '</button>' : '<button class="big primary" data-act="play" data-mode="mix">' + ic('play') + '이제 한 판 하기</button>') +
      '<button class="big ghost" data-act="note" data-t="' + tr.t[0] + '">' + ic('book') + '노트 보기</button><button class="tbtn" data-act="home">처음으로</button></div></div>';
  }
  SCREENS.trips = function () {
    return topbar('탐험') + '<p class="lead">아무것도 몰라도 괜찮아요. 짧은 장면을 보고, 먼저 짐작해 보고, 규칙을 스스로 찾는 길이에요. 순서대로 가면 PPT 내용 전체를 한 번씩 만나요.</p><div class="trlist">' +
      TRIPS.map(function (t, i) {
        var d = (S.trip || {})[t.id], u = UI[t.u];
        return '<button class="trcard card c-' + u.color + (d ? ' done' : '') + '" data-act="trip" data-id="' + t.id + '"><span class="trn">' + (i + 1) + '</span><div class="tri"><small>' + esc(u.short) + '</small><b>' + esc(t.name) + '</b><span>' + esc(t.sub) + ' · ' + t.steps.length + '걸음</span></div><div class="trs">' + (d ? stars(d.star) : ic('play')) + '</div></button>';
      }).join('') + '</div>';
  };
  SCREENS.wsl = function () {
    var bgs = Q.filter(function (q) { return q.k === 'bg'; }).length;
    return topbar('탐구활동지') + '<p class="lead">Ⅲ. 탄소 화합물과 반응 탐구활동지의 문제를 같은 말 그대로 옮겼어요. 쓰는 대신 고르고, 채우고, 조립해요.</p>' +
      '<button class="wsbg card" data-act="wsbg"><b>보기 ㄱㄴㄷ 문제만 모아 풀기</b><small>실전 문제 스타일 ' + bgs + '개</small>' + ic('arrow') + '</button>' +
      '<button class="wsbg card" data-act="pptcz"><b>PPT 문장 빈칸만 모아 풀기</b><small>탄소 화합물 PPT 문장을 글자 그대로 ' + Q.filter(function (q) { return q.k === 'cz'; }).length + '개</small>' + ic('arrow') + '</button><div class="wslist">' +
      WSA.map(function (w) {
        var qs = Q.filter(function (q) { return q.wa === w[0]; }), ln = learnedCount(qs), seen = qs.filter(function (q) { return S.q[q.id]; }).length;
        return '<button class="wsc card" data-act="wsa" data-a="' + w[0] + '"><span class="wsn">' + w[0] + '</span><div><b>' + esc(w[1]) + '</b><small>' + qs.length + '문제 · 푼 것 ' + seen + '</small>' + bar(qs.length ? mastery(qs) : 0, 'c-blue') + '</div></button>';
      }).join('') + '</div>';
  };

  /* ---------- 번개 O/X ---------- */
  var B = null;
  function boltPool() {
    var pool = Q.filter(function (q) { return q.k === 'ox' && inScope(q); });
    return pool;
  }
  SCREENS.bolt = function () {
    var pool = boltPool();
    return topbar('번개 O/X') + '<div class="boltintro">' +
      '<div class="bicon">' + ic('bolt') + '</div><h2>60초 동안 몇 개나?</h2>' +
      '<p>카드를 <b>오른쪽으로 밀면 O</b>, <b>왼쪽으로 밀면 X</b>. 아래 단추를 눌러도 돼요.<br>틀린 것은 끝나고 모아서 보여 줘요.</p>' +
      '<div class="bmeta"><span>' + esc(scopeName()) + ' · ' + pool.length + '문장</span>' + (S.best[S.scope] ? '<span>최고 기록 ' + S.best[S.scope] + '</span>' : '') + '</div>' +
      '<button class="big primary" data-act="boltgo">' + ic('play') + '시작</button></div>';
  };
  SCREENS.boltrun = function () {
    return '<header class="qtop"><button class="ibtn" data-act="boltquit" aria-label="그만하기">' + ic('x') + '</button><div class="btime"><i id="btbar"></i></div><div class="bscore" id="bscore">0</div></header>' +
      '<main class="bstage" id="bstage"><div class="bhint l">X</div><div class="bhint r">O</div></main>' +
      '<div class="oxrow bbtns"><button class="oxb x" data-act="bx" data-v="0"><svg viewBox="0 0 40 40"><path d="M10 10l20 20M30 10L10 30"/></svg><span>X</span></button><button class="oxb o" data-act="bx" data-v="1"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="13"/></svg><span>O</span></button></div>';
  };
  AFTER.boltrun = function () {
    var pool = boltPool();
    var weak = pool.slice().sort(function (a, b) { return (box(a.id) - box(b.id)) || (Math.random() - .5); });
    var order = shuffle(weak.slice(0, Math.max(20, Math.ceil(weak.length * 0.6)))).concat(shuffle(weak.slice(Math.max(20, Math.ceil(weak.length * 0.6)))));
    B = { order: order, i: 0, ok: 0, n: 0, wrong: [], combo: 0, maxc: 0, end: Date.now() + 60000, run: true, t: 0 };
    nextBoltCard();
    tickBolt();
  };
  function stopBolt() { if (B) { B.run = false; cancelAnimationFrame(B.t); } }
  function tickBolt() {
    if (!B || !B.run) return;
    var left = B.end - Date.now(), bb = $('#btbar');
    if (bb) { bb.style.transform = 'scaleX(' + Math.max(0, left / 60000) + ')'; bb.classList.toggle('hurry', left < 10000); }
    if (left <= 0) return endBolt();
    B.t = requestAnimationFrame(tickBolt);
  }
  function nextBoltCard() {
    var stage = $('#bstage'); if (!stage) return;
    if (B.i >= B.order.length) { B.order = B.order.concat(shuffle(B.order)); }
    var q = B.order[B.i];
    var card = document.createElement('div');
    card.className = 'bcard card';
    card.innerHTML = '<span class="qtag">' + esc(q.topic.hidden ? '연결' : q.topic.name) + '</span><p>' + fmt(q.q) + '</p>';
    stage.appendChild(card);
    if (!reduced) card.animate([{ transform: 'translateY(18px) scale(.96)', opacity: 0 }, { transform: 'none', opacity: 1 }], { duration: 220, easing: 'cubic-bezier(.2,.8,.2,1)' });
    dragCard(card);
  }
  function dragCard(card) {
    var sx = 0, sy = 0, dx = 0, on = false, id = null;
    card.addEventListener('pointerdown', function (e) { on = true; id = e.pointerId; sx = e.clientX; sy = e.clientY; dx = 0; card.setPointerCapture(id); card.style.transition = 'none'; });
    card.addEventListener('pointermove', function (e) {
      if (!on) return; dx = e.clientX - sx;
      card.style.transform = 'translateX(' + dx + 'px) rotate(' + dx / 18 + 'deg)';
      card.classList.toggle('lean-o', dx > 30); card.classList.toggle('lean-x', dx < -30);
    });
    function up() {
      if (!on) return; on = false;
      if (Math.abs(dx) > 80) boltAnswer(dx > 0 ? 1 : 0, card, dx > 0 ? 1 : -1);
      else { card.style.transition = 'transform .25s cubic-bezier(.2,.8,.2,1)'; card.style.transform = ''; card.classList.remove('lean-o', 'lean-x'); }
    }
    card.addEventListener('pointerup', up); card.addEventListener('pointercancel', up);
  }
  function boltAnswer(v, card, dir) {
    if (!B || !B.run) return;
    card = card || $('#bstage .bcard:last-child');
    if (!card || card._gone) return;
    card._gone = true;
    var q = B.order[B.i], ok = (v === 1) === !!q.a;
    B.n++; B.i++;
    record(q, ok, false);
    if (ok) { B.ok++; B.combo++; B.maxc = Math.max(B.maxc, B.combo); SND.ok(); vib(10); }
    else { B.combo = 0; B.wrong.push(q); SND.no(); vib([25, 40, 25]); }
    var sc = $('#bscore'); if (sc) { sc.textContent = B.ok; sc.className = 'bscore ' + (ok ? 'up' : 'dn'); void sc.offsetWidth; }
    var stage = $('#bstage'); if (stage) { stage.classList.remove('flash-ok', 'flash-no'); void stage.offsetWidth; stage.classList.add(ok ? 'flash-ok' : 'flash-no'); }
    dir = dir || (v ? 1 : -1);
    card.classList.add(ok ? 'is-ok' : 'is-no');
    var a = card.animate([{ transform: card.style.transform || 'none', opacity: 1 }, { transform: 'translateX(' + dir * 420 + 'px) rotate(' + dir * 22 + 'deg)', opacity: 0 }], { duration: reduced ? 1 : 260, easing: 'ease-in' });
    a.onfinish = function () { card.remove(); };
    nextBoltCard();
  }
  function endBolt() {
    if (!B) return;
    B.run = false;
    var nb = !S.best[S.scope] || B.ok > S.best[S.scope];
    if (nb && B.ok > 0) S.best[S.scope] = B.ok;
    B.newBest = nb && B.ok > 0;
    save(); SND.done();
    go('boltres', {}, true);
  }
  SCREENS.boltres = function () {
    if (!B) return SCREENS.home();
    var wr = uniq(B.wrong);
    return '<div class="res">' +
      '<div class="bicon big">' + ic('bolt') + '</div>' +
      (B.newBest ? '<p class="rmsg gold">새 최고 기록</p>' : '<p class="rmsg">60초 끝</p>') +
      '<div class="rscore"><b id="rs">0</b><span>개 맞힘</span></div>' +
      '<div class="rstats"><div><b>' + B.n + '</b><span>푼 문장</span></div><div><b>' + B.maxc + '</b><span>최고 연속</span></div><div><b>' + (S.best[S.scope] || 0) + '</b><span>최고 기록</span></div></div>' +
      (wr.length ? '<div class="rwrong card"><h3>틀린 문장</h3>' + wr.map(function (q) { return '<div class="rw"><p>' + fmt(q.q) + '</p><div class="ra"><b>' + (q.a ? 'O' : 'X') + '</b> ' + fmt(q.e) + '</div></div>'; }).join('') + '</div>' : '') +
      '<div class="rbtns"><button class="big primary" data-act="boltgo">' + ic('redo') + '다시</button><button class="big ghost" data-act="home">처음으로</button></div></div>';
  };
  AFTER.boltres = function () { countUp($('#rs'), B ? B.ok : 0, 800); if (B && B.newBest) setTimeout(function () { burst($('.rscore')); }, 400); };

  /* ---------- 노트 ---------- */
  SCREENS.notes = function () {
    return topbar('개념 노트') + scopeChips() + '<div class="nlist">' + C.UNITS.filter(function (u) { return uIn(u.id); }).map(function (u) {
      return '<h2 class="uhd"><span class="dot c-' + u.color + '"></span>' + esc(u.name) + '</h2>' + C.TOPICS.filter(function (t) { return t.u === u.id; }).map(function (t) {
        var m = mastery(t.qs);
        return '<button class="ncard card" data-act="note" data-t="' + t.id + '">' + ic(t.icon, 'tic') + '<div class="nci"><b>' + esc(t.name) + '</b><small>' + fmt(t.key[0]) + '</small>' + bar(m, 'c-' + u.color) + '</div>' + ring(m, 34, 4, 'sm c-' + u.color) + '</button>';
      }).join('');
    }).join('') + '</div>';
  };
  SCREENS.note = function (p) {
    var t = TI[p.t]; if (!t) return SCREENS.notes();
    var u = UI[t.u], m = mastery(t.qs), ix = C.TOPICS.indexOf(t);
    var prev = C.TOPICS[ix - 1], nxt = C.TOPICS[ix + 1];
    if (prev && prev.hidden) prev = null; if (nxt && nxt.hidden) nxt = null;
    S.seen[t.id] = S.seen[t.id] || Date.now(); save();
    return topbar(esc(t.name)) + '<article class="note">' +
      '<div class="nhead"><small class="c-' + u.color + '">' + esc(u.name) + '</small><div class="nprog">' + bar(m, 'c-' + u.color) + '<span>' + learnedCount(t.qs) + ' / ' + t.qs.length + ' 외움</span></div></div>' +
      '<div class="keybox card"><b>핵심만</b><ol>' + t.key.map(function (l) { return '<li>' + fmt(l) + '</li>'; }).join('') + '</ol></div>' +
      '<div class="nbody">' + noteHtml(t.note) + '</div>' +
      '<div class="nfoot"><button class="big primary" data-act="play" data-mode="topic" data-t="' + t.id + '">' + ic('play') + '이 주제 풀기</button>' +
      '<div class="npn">' + (prev ? '<button class="tbtn" data-act="note" data-t="' + prev.id + '" data-r="1">' + ic('back') + esc(prev.name) + '</button>' : '<span></span>') + (nxt ? '<button class="tbtn r" data-act="note" data-t="' + nxt.id + '" data-r="1">' + esc(nxt.name) + ic('arrow') + '</button>' : '') + '</div></div></article>';
  };
  // 문제 중에 노트 엿보기(시트)
  function peek(tid) {
    var t = TI[tid]; if (!t) return;
    var d = document.createElement('div');
    d.className = 'peek';
    d.innerHTML = '<div class="pk-bg" data-act="peekx"></div><div class="pk-in"><div class="pk-h"><b>' + esc(t.name) + '</b><button class="ibtn" data-act="peekx" aria-label="닫기">' + ic('x') + '</button></div><div class="pk-b note"><div class="keybox card"><b>핵심만</b><ol>' + t.key.map(function (l) { return '<li>' + fmt(l) + '</li>'; }).join('') + '</ol></div><div class="nbody">' + noteHtml(t.note) + '</div></div></div>';
    document.body.appendChild(d);
    requestAnimationFrame(function () { d.classList.add('show'); });
    S.seen[t.id] = S.seen[t.id] || Date.now(); save();
  }
  function peekClose() { var d = $('.peek'); if (!d) return; d.classList.remove('show'); setTimeout(function () { d.remove(); }, 260); }

  /* ---------- 이야기 줄 ---------- */
  SCREENS.chains = function () {
    return topbar('이야기 줄') + '<p class="lead">따로 외운 개념들이 실제로는 한 줄로 이어져 있어요. 흐름으로 보면 훨씬 오래 남아요.</p><div class="clist">' + C.CHAINS.map(function (c, i) {
      var ns = c.steps.filter(function (s) { return s.n; });
      return '<button class="ccard card" data-act="chain" data-c="' + c.id + '"><span class="cnum">' + (i + 1) + '</span><div><b>' + esc(c.name) + '</b><small>' + esc(c.desc) + '</small><div class="cpath">' + ns.map(function (s) { return '<span>' + esc(s.n) + '</span>'; }).join('<i></i>') + '</div></div></button>';
    }).join('') + '</div>';
  };
  SCREENS.chain = function (p) {
    var c = C.CHAINS.filter(function (x) { return x.id === p.c; })[0]; if (!c) return SCREENS.chains();
    var h = topbar(esc(c.name)) + '<p class="lead">' + esc(c.desc) + '</p><ol class="flow">';
    c.steps.forEach(function (s, i) {
      if (s.a) { h += '<li class="fa-step" style="--d:' + i + '"><span>' + fmt(s.a) + '</span></li>'; return; }
      h += '<li class="fn card" style="--d:' + i + '"><div class="fnh"><b>' + esc(s.n) + '</b>' + (s.f ? chem(s.f) : '') + '</div>' + (s.m && MOL.has(s.m) ? '<div class="fnm">' + MOL.svg(s.m) + '</div>' : '') + (s.d ? '<p>' + fmt(s.d) + '</p>' : '') + '</li>';
    });
    h += '</ol><div class="nfoot"><button class="big primary" data-act="play" data-mode="chain" data-c="' + c.id + '">' + ic('play') + '이 흐름 퀴즈</button></div>';
    return h;
  };

  /* ---------- 오답 노트 ---------- */
  SCREENS.wrong = function () {
    var list = noteQs(Q.filter(inScope)).sort(function (a, b) { var A = S.q[a.id], Bq = S.q[b.id]; return (A.b - Bq.b) || (Bq.l - A.l); });
    var h = topbar('오답 노트') + scopeChips();
    if (!list.length) return h + '<div class="empty"><p>오답 노트가 비어 있어요.<br>한 판 하다 틀리면 여기에 모여요.</p><button class="big primary" data-act="play" data-mode="mix">' + ic('play') + '한 판 하기</button></div>';
    var done = list.filter(function (q) { return S.q[q.id].b >= 3; }).length;
    h += '<div class="wtop"><span>' + list.length + '문제 · 빨간 점은 아직 못 외운 것</span><button class="big primary sm" data-act="play" data-mode="wrong">' + ic('redo') + '다시 풀기</button></div>';
    h += '<div class="wclr">' + (done ? '<button class="tbtn" data-act="wdelok">' + ic('check') + '외운 것 ' + done + '개 지우기</button>' : '<span></span>') + '<button class="tbtn danger" data-act="wdelall">' + ic('x') + '이 범위 모두 지우기</button></div><div class="wlist">';
    h += list.map(function (q) {
      var s = S.q[q.id];
      return '<details class="wcard card" data-id="' + q.id + '"><summary><span class="wd ' + (s.b >= 3 ? 'ok' : s.b === 0 ? 'no' : 'mid') + '"></span><span class="wq">' + fmt(q.q) + '</span><span class="wn">' + s.w + '번 틀림</span></summary><div class="wa">' + extrasHtml(q) + (q.fig ? MOL.svg(q.fig) : '') + '<div class="sh-ans"><span>정답</span><div>' + correctText(q) + '</div></div><p>' + fmt(q.e) + '</p><div class="wbtns"><button class="tbtn" data-act="note" data-t="' + q.t + '">' + ic('book') + esc(q.topic.hidden ? '' : q.topic.name) + ' 노트</button><button class="tbtn danger" data-act="wdel" data-id="' + q.id + '">' + ic('x') + '오답 노트에서 지우기</button></div></div></details>';
    }).join('');
    return h + '</div><p class="foot">지워도 복습 일정은 그대로예요. 다시 틀리면 다시 들어와요.</p>';
  };
  function wdel(ids) {
    ids.forEach(function (id) { if (S.q[id]) S.q[id].w = 0; });
    save();
  }

  /* ---------- 설정 ---------- */
  SCREENS.settings = function () {
    function sw(k, label, desc) { return '<label class="srow"><span><b>' + label + '</b><small>' + desc + '</small></span><input type="checkbox" data-set="' + k + '"' + (S.set[k] ? ' checked' : '') + '><i class="sw"></i></label>'; }
    var total = Object.keys(S.q).length;
    return topbar('설정') + '<div class="sets card">' +
      sw('sound', '소리', '맞히거나 틀릴 때 짧은 소리') +
      sw('vib', '진동', '안드로이드에서 정답·오답 진동') +
      sw('auto', '맞히면 자동으로 넘기기', '해설은 잠깐 보여 주고 넘어가요') +
      sw('big', '글자 크게', '차에서 볼 때 편하게') +
      '<div class="srow logo-row"><span><b>테마 색</b><small>로고와 앱 색이 함께 바뀌어요. 홈 화면 아이콘은 앱을 다시 연 뒤 새로 추가하면 바뀌어요.</small></span><span class="logo-pv">' + logoSvg() + '</span></div><div class="swatches">' + LOGO.map(function (x) { return '<button class="sw-c' + ((S.set.logo || 'red') === x[0] ? ' on' : '') + '" data-act="logo" data-v="' + x[0] + '" style="--c:' + x[2] + '" aria-label="' + x[1] + '"><i></i><span>' + x[1] + '</span></button>'; }).join('') + '</div>' +
      '<div class="srow"><span><b>화면</b><small>밝게, 어둡게, 기기 따라</small></span><div class="seg">' + ['auto', 'light', 'dark'].map(function (v) { return '<button data-act="theme" data-v="' + v + '" class="' + (S.set.theme === v ? 'on' : '') + '">' + { auto: '기기', light: '밝게', dark: '어둡게' }[v] + '</button>'; }).join('') + '</div></div>' +
      '</div><div class="sets card"><div class="srow"><span><b>내 기록</b><small>푼 문제 ' + total + '개 · 이 기기에만 저장</small></span></div>' +
      '<button class="srow danger" data-act="reset"><span><b>전체 초기화</b><small>푼 기록, 오답 노트, 외운 정도, 탐험 별, 번개 최고 기록을 모두 지워요. 설정은 그대로.</small></span></button></div>' +
      '<p class="foot">한 입 화학 · 인터넷 없이도 돼요 · 글꼴 Pretendard(OFL)</p>';
  };

  /* ---------- 테마 ---------- */
  function applyTheme() {
    var r = document.documentElement;
    if (S.set.theme === 'auto') r.removeAttribute('data-theme'); else r.setAttribute('data-theme', S.set.theme);
    r.classList.toggle('big', !!S.set.big);
    var dark = S.set.theme === 'dark' || (S.set.theme === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
    var m = $('meta[name="theme-color"]:not([media])');
    if (!m) { m = document.createElement('meta'); m.name = 'theme-color'; document.head.appendChild(m); }
    m.content = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim() || (dark ? '#141316' : '#F3EFE6');
  }
  applyTheme();
  applyLogo();
  try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme); } catch (e) { }

  /* ---------- 누르기 ---------- */
  var resetArm = 0, wArm = 0;
  document.addEventListener('click', function (e) {
    var bk = e.target.closest && e.target.closest('#bdw [data-bk]');
    if (bk && view.name === 'quiz' && R) { onBdBlank(+bk.getAttribute('data-bk')); return; }
    var el = e.target.closest('[data-act]'); if (!el) return;
    var a = el.dataset.act, d = el.dataset;
    switch (a) {
      case 'back': if (history.length > 1 && history.state) history.back(); else go('home', {}, true); break;
      case 'home': R = null; B = null; go('home', {}, true); break;
      case 'scope': S.scope = d.v; save(); show(view); break;
      case 'sound': S.set.sound = !S.set.sound; save(); if (S.set.sound) SND.ok(); el.innerHTML = ic(S.set.sound ? 'snd' : 'mute'); toast(S.set.sound ? '소리를 켰어요' : '소리를 껐어요'); break;
      case 'settings': go('settings'); break;
      case 'play': startRound(d.mode, { t: d.t, c: d.c }); break;
      case 'again': startRound(R ? R.mode : 'mix', R ? R.p : {}); break;
      case 'bolt': go('bolt'); break;
      case 'boltgo': go('boltrun', {}, view.name === 'boltres'); break;
      case 'boltquit': stopBolt(); B = null; history.back(); break;
      case 'bx': boltAnswer(+d.v); break;
      case 'mol': startRound('mol'); break;
      case 'link': startRound('link'); break;
      case 'chains': go('chains'); break;
      case 'chain': go('chain', { c: d.c }); break;
      case 'wrong': go('wrong'); break;
      case 'notes': go('notes'); break;
      case 'note': if (e.target.closest('details') && el.tagName !== 'BUTTON') return; go('note', { t: d.t }, !!d.r); break;
      case 'quit': if (R && R.total && !confirm('이번 판을 그만할까요? 푼 문제는 저장돼요.')) return; R = null; go('home', {}, true); break;
      case 'learned': S.seen[d.t] = S.seen[d.t] || Date.now(); save(); next(); break;
      case 'peek': peek(d.t); break;
      case 'peekx': peekClose(); break;
      case 'pick': onPick(+d.i, el); break;
      case 'ox': onOx(+d.v, el); break;
      case 'pk': onPk(+d.i, el); break;
      case 'pkok': onPkOk(); break;
      case 'sqp': onSq(+d.i, el); break;
      case 'slot': onSlot(+el.closest('li').dataset.i); break;
      case 'mtl': onMt('l', +d.i, el); break;
      case 'mtr': onMt('r', +d.i, el); break;
      case 'next': next(); break;
      case 'sayok': next(); break;
      case 'tbc': onTbCell(+d.b); break;
      case 'tbt': onTbTile(+d.v); break;
      case 'bdt': onBdTile(+d.v); break;
      case 'bgv': onBgv(+d.i, +d.v); break;
      case 'sov': onSov(+d.i, +d.b); break;
      case 'chk': onChk(); break;
      case 'wdel': {
        var card = el.closest('.wcard'); wdel([d.id]); SND.tap();
        if (card && !reduced) { var an = card.animate([{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'translateX(40px)' }], { duration: 220, easing: 'ease-in' }); an.onfinish = function () { show(view); }; }
        else show(view);
        toast('오답 노트에서 지웠어요');
        break;
      }
      case 'wdelok': { var ok3 = noteQs(Q.filter(inScope)).filter(function (q) { return S.q[q.id].b >= 3; }); wdel(ok3.map(function (q) { return q.id; })); toast('외운 ' + ok3.length + '문제를 지웠어요'); show(view); break; }
      case 'wdelall':
        if (Date.now() - (wArm) < 3000) { var all = noteQs(Q.filter(inScope)); wdel(all.map(function (q) { return q.id; })); wArm = 0; toast(all.length + '문제를 지웠어요'); show(view); }
        else { wArm = Date.now(); el.lastChild.textContent = '한 번 더 누르면 모두 지워져요'; el.classList.add('armed'); }
        break;
      case 'trips': go('trips'); break;
      case 'trip': startRound('trip', { id: d.id }); break;
      case 'wsl': go('wsl'); break;
      case 'wsa': startRound('ws', { a: +d.a }); break;
      case 'wsbg': startRound('bg'); break;
      case 'pptcz': startRound('cz'); break;
      case 'tipx': S.tip = 2; save(); el.closest('.tipcard').remove(); break;
      case 'logo': S.set.logo = d.v; save(); applyLogo(); $$('.sw-c').forEach(function (b) { b.classList.toggle('on', b.dataset.v === d.v); }); SND.tap(); vib(8); { var pv = $('.logo-pv svg'); if (pv && !reduced) pv.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.18) rotate(-6deg)' }, { transform: 'scale(1)' }], { duration: 380, easing: 'cubic-bezier(.3,1.6,.5,1)' }); } break;
      case 'theme': S.set.theme = d.v; save(); applyTheme(); show(view); break;
      case 'reset':
        if (!confirm('정말 전체 초기화할까요? 푼 기록, 오답 노트, 탐험 별이 모두 지워지고 되돌릴 수 없어요.')) break;
        (function () { var keep = S.set; S = fresh(); S.set = keep; window.__chem.S = S; saveNow(); toast('전체 초기화했어요. 처음부터 시작해요'); go('home', {}, true); })();
        break;
    }
  });
  document.addEventListener('change', function (e) {
    var k = e.target.dataset && e.target.dataset.set; if (!k) return;
    S.set[k] = e.target.checked; save(); applyTheme();
    if (k === 'sound' && S.set.sound) SND.ok();
  });
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (view.name === 'quiz' && R) {
      var it = R.list[R.i];
      if (R.cur && R.cur.done) { if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') { e.preventDefault(); next(); } return; }
      if (it && it.learn && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); var b = $('[data-act="learned"]'); if (b) b.click(); return; }
      if (it && it.k === 'mc' && /^[1-4]$/.test(e.key)) { var c = $$('.choices .ch')[+e.key - 1]; if (c) c.click(); }
      if (it && it.k === 'ox') { if (/^[oO1]$/.test(e.key)) $('.oxb.o').click(); if (/^[xX2]$/.test(e.key)) $('.oxb.x').click(); }
      if (it && it.k === 'pk' && e.key === 'Enter') { var ok = $('#pkok'); if (ok && !ok.disabled) ok.click(); }
    }
    if (view.name === 'boltrun') { if (e.key === 'ArrowRight' || /^[oO]$/.test(e.key)) boltAnswer(1); if (e.key === 'ArrowLeft' || /^[xX]$/.test(e.key)) boltAnswer(0); }
    if (e.key === 'Escape' && $('.peek')) peekClose();
  });

  /* ---------- 시작 ---------- */
  var first = history.state && history.state.name && history.state.name !== 'quiz' && history.state.name !== 'result' && history.state.name !== 'boltrun' && history.state.name !== 'boltres' ? history.state : { name: 'home' };
  try { history.replaceState(first, ''); } catch (e) { }
  show(first);
  // 홈 화면 앱 시작 표지: 앱이 준비될 때까지 숨 쉬듯 기다렸다가, 마스코트가 왼쪽 위 로고로 쏙 들어가며 열림
  (function () {
    var root = document.documentElement, cv = document.getElementById('cover');
    if (!cv || !root.classList.contains('cov')) return;
    var t0 = performance.now(), gone = false;
    function finish() { root.classList.remove('cov', 'cov-out'); cv.style.cssText = ''; }
    function open() {
      if (gone) return; gone = true;
      var m = cv.querySelector('.mascot'), logo = document.querySelector('.hhead .logo'), view = document.querySelector('#app .view');
      if (reduced || !m || !m.animate) { cv.style.transition = 'opacity .2s'; cv.style.opacity = '0'; setTimeout(finish, 220); return; }
      root.classList.add('cov-out');
      var a = m.getBoundingClientRect(), D = 520, ease = 'cubic-bezier(.65,0,.25,1)';
      if (logo) {
        var b = logo.getBoundingClientRect(), s = b.width / a.width;
        var dx = (b.left + b.width / 2) - (a.left + a.width / 2), dy = (b.top + b.height / 2) - (a.top + a.height / 2);
        m.animate([{ transform: 'none' }, { transform: 'translate(0,-3%) scale(1.06)', offset: .18 }, { transform: 'translate(' + dx + 'px,' + dy + 'px) scale(' + s + ')' }], { duration: D, easing: ease, fill: 'forwards' });
        logo.animate([{ opacity: 0 }, { opacity: 0, offset: .8 }, { opacity: 1 }], { duration: D, fill: 'backwards' });
      } else m.animate([{ transform: 'none', opacity: 1 }, { transform: 'scale(.6)', opacity: 0 }], { duration: D * .7, easing: ease, fill: 'forwards' });
      cv.animate([{ backgroundColor: getComputedStyle(cv).backgroundColor }, { backgroundColor: 'rgba(243,239,230,0)' }], { duration: D * .8, delay: D * .2, easing: 'ease-out', fill: 'forwards' });
      if (view) view.animate([{ opacity: 0, transform: 'scale(.97)' }, { opacity: 1, transform: 'none' }], { duration: D * .8, delay: D * .2, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'backwards' });
      setTimeout(finish, D + 40);
    }
    var ready = (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve();
    ready.then(function () {
      var wait = Math.max(0, 750 - (performance.now() - t0));
      setTimeout(function () { requestAnimationFrame(function () { requestAnimationFrame(open); }); }, wait);
    });
    setTimeout(open, 2600);
    cv.addEventListener('click', open);
  })();
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    window.addEventListener('load', function () {
      // 같은 사이트의 플래너 서비스 워커가 이 화면을 대신 저장했으면 플래너 화면을 다시 받아 둔다(예전 판 플래너)
      try {
        var ctl = navigator.serviceWorker.controller;
        if (ctl && !/\/chem\/sw\.js$/.test(ctl.scriptURL) && window.caches) caches.keys().then(function (ks) { ks.forEach(function (k) { if (k.indexOf('gbb-shell') === 0) caches.open(k).then(function (c) { fetch('../', { cache: 'no-store' }).then(function (r) { if (r.ok) c.put('../', r); }); }); }); });
      } catch (e) { }
      navigator.serviceWorker.register('sw.js', { scope: './' }).catch(function () { });
    });
  }
  window.__chem = { S: S, Q: Q, TRIPS: TRIPS, start: startRound, go: go, R: function () { return R; },
    play: function (list) { R = { mode: 'mix', p: {}, title: 'test', list: list, i: 0, ok: 0, total: 0, combo: 0, maxc: 0, learned: 0, wrong: [], retried: {}, t0: Date.now(), mols: [] }; go('quiz', {}); },
    gen: function () { return MOLPOOL.map(function (k) { return [genMol('name', k), genMol('pick', k)]; }).reduce(function (a, b) { return a.concat(b); }, []).concat(chainQuestions(null)); } };
})();
