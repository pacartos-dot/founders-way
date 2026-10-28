// Smoke test: the game loads without errors and the simulation runs 60 in-game days in every preset.
// Run with `npm test`. CI runs it on every pull request; a failure blocks the merge.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|fonts\.g/.test(m.text())) errors.push(m.text()); });

  await page.goto('file://' + path.resolve(__dirname, '..', 'index.html'));
  await page.waitForTimeout(3000);

  const result = await page.evaluate(() => {
    const out = {};
    for (const preset of Object.keys(PRESETS)) {
      const f = { name: 'CI ' + preset, founder: 'Bot', pitch: 'test', problem: 'test', customer: 'test', industry: 'saas', preset, profile: 'player' };
      newProject(f, { ...PRESETS[preset].cfg, mentor: false }, preset);
      let n = 0; while (S.day < 60 && !S.over && n++ < 200000) simStep(.25);
      out[preset] = { day: Math.floor(S.day), cash: Math.round(S.cash), finite: Number.isFinite(S.cash) };
    }
    return out;
  });

  await browser.close();
  console.log(result);
  const bad = Object.entries(result).filter(([, r]) => !r.finite);
  if (errors.length) console.error('Page errors:\n' + errors.join('\n'));
  if (bad.length) console.error('Non-numeric cash in: ' + bad.map(b => b[0]).join(', '));
  process.exit(errors.length || bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
