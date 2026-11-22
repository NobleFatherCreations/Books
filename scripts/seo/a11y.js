// axe-core WCAG 2.2 AA scan of generated pages (web-accessibility skill). Usage: node a11y.js url...
const { chromium } = require('playwright');
const fs = require('fs');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
(async () => {
  const b = await chromium.launch(); const tot = {};
  for (const url of process.argv.slice(2)) {
    for (const scheme of ['dark', 'light']) {
      const p = await b.newPage({ viewport: { width: 375, height: 812 }, colorScheme: scheme });
      await p.goto(url); await p.addScriptTag({ content: axeSrc });
      const r = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice'] })).violations
        .map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, ex: v.nodes[0].target.join(' ').slice(0, 70), why: (v.nodes[0].failureSummary || '').split('\n')[1] })));
      const short = url.replace(/^https?:\/\/[^/]+/, '');
      console.log(short, scheme, r.length ? '' : 'clean'); r.forEach(v => { console.log('   ', v.impact, v.id, 'x' + v.n, v.ex, '|', (v.why || '').slice(0, 90)); tot[v.id] = (tot[v.id] || 0) + v.n; });
      await p.close();
    }
  }
  console.log('TOTAL', JSON.stringify(tot)); await b.close();
})();
