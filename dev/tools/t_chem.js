/* 한 입 화학(public/chem) 시험: node dev/tools/t_chem.js
   모든 문제를 정답으로 풀어 채점이 맞는지, 화면이 옆으로 넘치지 않는지, 오프라인으로 열리는지 본다. */
const { chromium, devices } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const PORT = 8139, ROOT = path.join(__dirname, '..', '..', 'public');
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
      const res = await p.evaluate(async () => {
        const C = __chem, all = C.Q.concat(C.gen()), bad = [], over = [];
        for (const q of all) {
          C.play([q]); await new Promise(r => setTimeout(r, 2));
          const it = C.R().list[0];
          if (q.k === 'mc') document.querySelectorAll('.choices .ch')[it._o.indexOf(q.a)].click();
          else if (q.k === 'ox') document.querySelector('.oxb.' + (q.a ? 'o' : 'x')).click();
          else if (q.k === 'pk') { it._o.forEach((c, i) => { if (q.a.includes(c)) document.querySelectorAll('.choices.pk .ch')[i].click(); }); document.querySelector('#pkok').click(); }
          else if (q.k === 'sq') q.s.forEach(s => { const i = it._o.findIndex((c, j) => c === s && !document.querySelector('#pool .pc[data-i="' + j + '"]').classList.contains('used')); document.querySelector('#pool .pc[data-i="' + i + '"]').click(); });
          else if (q.k === 'mt') q.p.forEach((_, i) => { document.querySelector('.mcol:first-child .mi[data-i="' + i + '"]').click(); document.querySelector('.mcol:last-child .mi[data-i="' + i + '"]').click(); });
          if (!document.querySelector('#sheet').classList.contains('ok')) bad.push(q.id);
          if (document.documentElement.scrollWidth > innerWidth + 1) over.push(q.id);
        }
        // 노트와 이야기 줄도 모두 열어 보기
        for (const t of C.Q.map(q => q.t).filter((v, i, a) => a.indexOf(v) === i && v !== 'link')) { C.go('note', { t }); if (document.documentElement.scrollWidth > innerWidth + 1) over.push('note:' + t); }
        return { n: all.length, bad, over };
      });
      console.log(scheme, '문제', res.n, '틀린 채점', res.bad.length, '넘침', res.over.length, '오류', errs.length);
      if (res.bad.length || res.over.length || errs.length) { fail = 1; console.log(res.bad.slice(0, 10), res.over.slice(0, 10), errs.slice(0, 5)); }
      await ctx.close();
    }
    // 오프라인
    const ctx = await b.newContext({ ...devices['iPhone 13'] });
    const p = await ctx.newPage();
    await p.goto(`http://localhost:${PORT}/chem/`); await p.evaluate(() => navigator.serviceWorker.ready); await p.waitForTimeout(1200);
    await ctx.setOffline(true); await p.reload(); await p.waitForTimeout(800);
    const ok = await p.evaluate(() => !!document.querySelector('.brand') && document.fonts.check('16px Pretendard'));
    console.log('오프라인으로 열림', ok); if (!ok) fail = 1;
  } finally { await b.close(); srv.kill(); }
  process.exit(fail);
})();
