// Renderiza assets/retailers/svg/*.svg a PNG transparentes (alto 240 px) con Chromium.
// Uso: node canva/extraer/logos_png.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const DIR = path.resolve(__dirname, '../../assets/retailers');
const ALTO = 240;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2000, height: 600 } });
  for (const f of fs.readdirSync(path.join(DIR, 'svg')).filter((n) => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(DIR, 'svg', f), 'utf8');
    const html = `<html><body style="margin:0;background:transparent">
      <div id="l" style="display:inline-block;line-height:0">${svg}</div></body></html>`;
    await page.setContent(html);
    await page.evaluate((alto) => {
      const s = document.querySelector('#l svg');
      const vb = s.viewBox.baseVal;
      s.setAttribute('height', alto);
      s.setAttribute('width', (alto * vb.width) / vb.height);
    }, ALTO);
    const out = path.join(DIR, f.replace(/\.svg$/, '.png'));
    await page.locator('#l').screenshot({ path: out, omitBackground: true });
    console.log(out);
  }
  await browser.close();
})();
