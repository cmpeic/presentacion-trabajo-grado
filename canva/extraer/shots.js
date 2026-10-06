// Capturas de referencia del HTML original. Uso: node shots.js <dir> [desde] [hasta]
const fs = require('fs');
const { openDeck, seek, PASOS } = require('./common');
(async () => {
  const out = process.argv[2];
  const from = +(process.argv[3] || 1), to = +(process.argv[4] || PASOS.length);
  fs.mkdirSync(out, { recursive: true });
  const { browser, page } = await openDeck();
  for (let i = from; i <= to; i++) {
    await seek(page, PASOS[i - 1].rest);
    await page.screenshot({ path: `${out}/s${String(i).padStart(2, '0')}.png` });
  }
  await browser.close();
})();
