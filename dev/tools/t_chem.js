/* 한 입 화학(public/chem) 시험: node dev/tools/t_chem.js
   모든 문제와 탐험을 정답으로 풀어 채점이 맞는지, 화면이 옆으로 넘치지 않는지, 오프라인으로 열리는지 본다. */
const { chromium, devices } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const PORT = 8139, ROOT = path.join(__dirname, '..', '..', 'public');

// 지금 화면의 문제를 정답으로 푸는 함수 (브라우저 안에서 실행)
const SOLVE = `window.__solve = function (q, it) {
  const $ = s => document.querySelector(s), $$ = s => Array.from(document.querySelectorAll(s));
  if (q.k === 'mc') $$('.choices .ch')[it._o.indexOf(q.a)].click();
  else if (q.k === 'ox') $('.oxb.' + (q.a ? 'o' : 'x')).click();
  else if (q.k === 'pk') { it._o.forEach((c, i) => { if (q.a.includes(c)) $$('.choices.pk .ch')[i].click(); }); $('#pkok').click(); }
  else if (q.k === 'sq') q.s.forEach(s => { const i = it._o.findIndex((c, j) => c === s && !$('#pool .pc[data-i="' + j + '"]').classList.contains('used')); $('#pool .pc[data-i="' + i + '"]').click(); });
  else if (q.k === 'mt') q.p.forEach((_, i) => { $('.mcol:first-child .mi[data-i="' + i + '"]').click(); $('.mcol:last-child .mi[data-i="' + i + '"]').click(); });
  else if (q.k === 'tb' || q.k === 'cz') {
    const ans = []; if (q.k === 'cz') q.a.forEach(a => ans.push(a.trim())); else q.rows.forEach(r => r.forEach(c => { if (c[0] === '?') ans.push(c.slice(1).trim()); }));
    ans.forEach((a, i) => { $('.tbk[data-b="' + i + '"]').click(); $('.tile[data-v="' + it._bank.indexOf(a) + '"]').click(); });
    $('#chk').click();
  } else if (q.k === 'bd') {
    q.a.forEach((a, i) => { $('#bdw [data-bk="' + i + '"]').dispatchEvent(new MouseEvent('click', { bubbles: true })); $('.tile[data-v="' + q.tiles.indexOf(a) + '"]').click(); });
    $('#chk').click();
  } else if (q.k === 'bg') { q.items.forEach((x, i) => $('.bgb button[data-i="' + i + '"][data-v="' + (x[1] ? 1 : 0) + '"]').click()); $('#chk').click(); }
  else if (q.k === 'so') { q.items.forEach((x, i) => $('.sob button[data-i="' + i + '"][data-b="' + x[1] + '"]').click()); $('#chk').click(); }
  return !!$('#sheet.ok');
};`;

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(PORT)], { cwd: ROOT, stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 800));
  let fail = 0;
  const b = await chromium.launch();
  try {
    for (const scheme of ['light', 'dark']) {
      const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1, colorScheme: scheme });
      const p = await ctx.newPage(); const errs = [];
      p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      await p.goto(`http://localhost:${PORT}/chem/?t=${scheme}`); await p.waitForTimeout(500);
      await p.evaluate(SOLVE);
      const res = await p.evaluate(async () => {
        const C = __chem, all = C.Q.concat(C.gen()), bad = [], over = [];
        const wide = () => document.documentElement.scrollWidth > innerWidth + 1;
        for (const q of all) {
          C.play([q]); await new Promise(r => setTimeout(r, 2));
          try { if (!__solve(q, C.R().list[0])) bad.push(q.id + ' ' + q.q.slice(0, 30)); } catch (e) { bad.push(q.id + ' 오류 ' + e.message); }
          if (wide()) over.push(q.id);
        }
        // 탐험: 장면은 넘기고 문제는 정답으로
        let steps = 0;
        for (const tr of C.TRIPS) {
          C.start('trip', { id: tr.id }); await new Promise(r => setTimeout(r, 2));
          for (let g = 0; g < 60; g++) {
            const R = C.R(); if (!R || R.done || R.i >= R.list.length) break;
            const it = R.list[R.i]; steps++;
            if (it.k === 'say') document.querySelector('[data-act="sayok"]').click();
            else { try { if (!__solve(it, it)) bad.push('trip ' + it.id); } catch (e) { bad.push('trip ' + it.id + ' 오류 ' + e.message); } if (wide()) over.push(it.id); document.querySelector('#nextb').click(); }
            await new Promise(r => setTimeout(r, 160));
          }
          if (!(C.S.trip || {})[tr.id]) bad.push('trip 안 끝남 ' + tr.id);
          else if (C.S.trip[tr.id].star !== 3) bad.push('trip 별 ' + tr.id + ' ' + C.S.trip[tr.id].star);
        }
        for (const t of C.Q.map(q => q.t).filter((v, i, a) => a.indexOf(v) === i && v !== 'link')) { C.go('note', { t }); if (wide()) over.push('note:' + t); }
        for (const s of ['home', 'trips', 'wsl', 'chains', 'notes', 'wrong', 'marks', 'settings']) { C.go(s, {}); if (wide()) over.push('screen:' + s); }
        return { n: all.length, steps, bad, over };
      });
      console.log(scheme, '문제', res.n, '탐험 걸음', res.steps, '틀린 채점', res.bad.length, '넘침', res.over.length, '오류', errs.length);
      if (res.bad.length || res.over.length || errs.length) { fail = 1; console.log(res.bad.slice(0, 10), res.over.slice(0, 10), errs.slice(0, 5)); }
      await ctx.close();
    }
    // 헷갈리는 문제 저장, Claude에게 물어보기(가짜 /api/ask)
    {
      const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
      const p = await ctx.newPage(); const errs = []; let sent = null;
      p.on('pageerror', e => errs.push(e.message));
      await p.route('**/api/ask', r => { sent = JSON.parse(r.request().postData()); r.fulfill({ status: 200, contentType: 'text/plain; charset=utf-8', body: '하이드록시기가 **핵심**이에요.' }); });
      await p.goto(`http://localhost:${PORT}/chem/`); await p.waitForTimeout(400);
      const q = await p.evaluate(() => { const q = __chem.Q.find(x => x.k === 'mc' && !x.les); __chem.play([q]); return q.id; });
      await p.click('.qhead .mkb');
      await p.click('.choices .ch >> nth=0'); await p.waitForTimeout(300);
      const m1 = await p.evaluate(id => !!__chem.S.mark[id] && document.querySelector('#sheet .mkb').classList.contains('on'), q);
      await p.click('#sheet [data-act="askq"]'); await p.waitForTimeout(300);
      await p.click('.asksug .chip >> nth=0'); await p.waitForTimeout(500);
      const ans = await p.evaluate(() => (document.querySelector('.amsg.assistant') || {}).textContent || '');
      await p.click('.askp .pk-h [data-act="askx"]'); await p.waitForTimeout(300);
      await p.evaluate(() => __chem.go('marks', {}));
      const n1 = await p.evaluate(() => document.querySelectorAll('.v-marks .wcard').length);
      await p.evaluate(() => { document.querySelector('.v-marks details').open = true; });
      await p.click('.v-marks [data-act="mark"][data-rm]'); await p.waitForTimeout(200);
      const n2 = await p.evaluate(() => document.querySelectorAll('.v-marks .wcard').length);
      await p.route('**/api/ask', r => r.fulfill({ status: 503, contentType: 'application/json', body: '{"error":"no-key"}' }));
      await p.evaluate(() => document.querySelector('[data-act="ask"]') ? null : __chem.go('home', {}));
      await p.click('.mode[data-act="ask"]'); await p.fill('#askin', '에스터 냄새?'); await p.click('[data-act="asksend"]'); await p.waitForTimeout(400);
      const fb = await p.evaluate(() => (document.querySelector('.askerr a') || {}).href || '');
      const ok = m1 && ans.includes('핵심') && sent && sent.ctx.includes('정답') && n1 === 1 && n2 === 0 && fb.startsWith('https://claude.ai/new?q=') && !errs.length;
      console.log('저장·질문', ok, { m1, ans, ctx: !!(sent && sent.ctx), n1, n2, fb: fb.slice(0, 30), errs });
      if (!ok) fail = 1;
      await ctx.close();
    }
    // 오프라인
    const ctx = await b.newContext({ ...devices['iPhone 13'] });
    const p = await ctx.newPage();
    await p.goto(`http://localhost:${PORT}/chem/`); await p.evaluate(() => navigator.serviceWorker.ready); await p.waitForTimeout(1200);
    await ctx.setOffline(true); await p.reload(); await p.waitForTimeout(800);
    const ok = await p.evaluate(() => !!document.querySelector('.brand') && document.fonts.check('16px Pretendard') && !!window.CHEM.TRIPS);
    console.log('오프라인으로 열림', ok); if (!ok) fail = 1;
  } finally { await b.close(); srv.kill(); }
  process.exit(fail);
})();
