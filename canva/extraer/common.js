// Abre index.html con GSAP local y fuentes sustitutas (las mismas que usara Canva).
// Variables de entorno opcionales: FONTS_DIR (TTF de Montserrat, Barlow y Roboto Mono),
// GSAP_PATH (gsap.min.js local; por defecto node_modules/gsap/dist/gsap.min.js).
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

const REPO = path.resolve(__dirname, '..', '..');
const GSAP = process.env.GSAP_PATH || path.join(__dirname, 'node_modules/gsap/dist/gsap.min.js');
const F = (process.env.FONTS_DIR || path.join(require('os').homedir(), '.fonts')).replace(/\/?$/, '/');

const FONT_CSS = `
@font-face{font-family:"Cambria";src:url(file://${F}montserrat-600.ttf);font-weight:100 600;}
@font-face{font-family:"Cambria";src:url(file://${F}montserrat-700.ttf);font-weight:700 800;}
@font-face{font-family:"Cambria";src:url(file://${F}montserrat-800.ttf);font-weight:900;}
@font-face{font-family:"Bahnschrift";src:url(file://${F}Barlow-300.ttf);font-weight:100 300;}
@font-face{font-family:"Bahnschrift";src:url(file://${F}Barlow-400.ttf);font-weight:400;}
@font-face{font-family:"Bahnschrift";src:url(file://${F}Barlow-500.ttf);font-weight:500;}
@font-face{font-family:"Bahnschrift";src:url(file://${F}Barlow-600.ttf);font-weight:600;}
@font-face{font-family:"Bahnschrift";src:url(file://${F}Barlow-700.ttf);font-weight:700 900;}
@font-face{font-family:"Arial";src:url(file://${F}Barlow-400.ttf);font-weight:100 500;}
@font-face{font-family:"Arial";src:url(file://${F}Barlow-700.ttf);font-weight:600 900;}
@font-face{font-family:"Consolas";src:url(file://${F}robotomono-400.ttf);font-weight:100 400;}
@font-face{font-family:"Consolas";src:url(file://${F}robotomono-500.ttf);font-weight:500 600;}
@font-face{font-family:"Consolas";src:url(file://${F}robotomono-700.ttf);font-weight:700 900;}
`;

function loadPasos() {
  const src = fs.readFileSync(path.join(REPO, 'presentar.html'), 'utf8');
  const m = src.match(/const PASOS = (\[[\s\S]*?\]);\s*const CAPITULOS/);
  return JSON.parse(m[1]);
}

async function openDeck(extraCss = '') {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.route(/^https?:\/\//, route => {
    if (/gsap.*\.js/.test(route.request().url())) return route.fulfill({ path: GSAP, contentType: 'application/javascript' });
    return route.abort();
  });
  await page.goto('file://' + REPO + '/index.html');
  await page.addStyleTag({ content: FONT_CSS + extraCss });
  await page.evaluate(() => document.fonts.ready);
  const ok = await page.evaluate(() => !!(window.__timelines && window.__timelines['trabajo-grado']));
  if (!ok) throw new Error('timeline no registrado');
  return { browser, page };
}

async function seek(page, t) {
  await page.evaluate(t => { window.__timelines['trabajo-grado'].seek(t, false); }, t);
  await page.waitForTimeout(60);
}

const PASOS = loadPasos();
module.exports = { openDeck, seek, PASOS, REPO };
