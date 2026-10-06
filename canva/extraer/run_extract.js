// Extrae primitivas y capa de decoraciones de las laminas indicadas.
// Uso: node run_extract.js <dir_salida> <desde> <hasta>
const path = require('path');
const fs = require('fs');
const { openDeck, seek, PASOS } = require('./common');
const { extractScene } = require('./extract_dom');

const HEADER_SKIP = '.blueprint,.ghost-mark,.chapter-logo,.chapter-heading,.title-rule,.text-scene-logo';

const DECO_CSS = `
html.deco-pass, html.deco-pass body, html.deco-pass #root, html.deco-pass .scene { background: transparent !important; }
html.deco-pass .scene::before, html.deco-pass .scene::after { display: none !important; }
html.deco-pass .blueprint, html.deco-pass .ghost-mark, html.deco-pass .chapter-logo, html.deco-pass .chapter-heading, html.deco-pass .title-rule { visibility: hidden !important; }
html.deco-pass .scene * { color: transparent !important; background-color: transparent !important; border-color: transparent !important; box-shadow: none !important; text-shadow: none !important; text-decoration-color: transparent !important; outline-color: transparent !important; }
html.deco-pass .scene *::before, html.deco-pass .scene *::after { color: transparent !important; }
html.deco-pass .scene img { visibility: hidden !important; }
`;

(async () => {
  const out = process.argv[2];
  const from = +process.argv[3], to = +process.argv[4];
  fs.mkdirSync(out, { recursive: true });
  const { browser, page } = await openDeck(DECO_CSS);
  for (let i = from; i <= to; i++) {
    await seek(page, PASOS[i - 1].rest);
    // escena visible = la de mayor opacidad
    const sceneId = await page.evaluate(() => {
      let best = null, bo = 0;
      document.querySelectorAll('.scene').forEach(s => { const o = parseFloat(getComputedStyle(s).opacity); if (o > bo) { bo = o; best = s.id; } });
      return best;
    });
    const items = await page.evaluate(([fnSrc, opts]) => { const f = eval('(' + fnSrc + ')'); return f(opts); },
      [extractScene.toString(), { scene: '#' + sceneId, skip: HEADER_SKIP }]);
    const n = String(i).padStart(2, '0');
    fs.writeFileSync(path.join(out, `s${n}.json`), JSON.stringify({ paso: i, scene: sceneId, items }, null, 0));
    await page.evaluate(() => document.documentElement.classList.add('deco-pass'));
    await page.waitForTimeout(30);
    await page.screenshot({ path: path.join(out, `s${n}_deco.png`), omitBackground: true });
    await page.evaluate(() => document.documentElement.classList.remove('deco-pass'));
    console.log(i, sceneId, items.length);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
