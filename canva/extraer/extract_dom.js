// Funcion que se ejecuta dentro de la pagina (page.evaluate) y devuelve las
// primitivas visibles de una escena: cajas, imagenes y bloques de texto.
// Coordenadas en pixeles del lienzo 1920x1080.
function extractScene(opts) {
  const scene = document.querySelector(opts.scene);
  const skip = opts.skip || '';
  const VW = 1920, VH = 1080;
  const items = [];

  const parseColor = (c) => {
    if (!c) return null;
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const hex = (c) => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');

  const opacityCache = new Map();
  const effOpacity = (el) => {
    if (!el || el === document.documentElement) return 1;
    if (opacityCache.has(el)) return opacityCache.get(el);
    const cs = getComputedStyle(el);
    let o = parseFloat(cs.opacity);
    if (cs.visibility === 'hidden' || cs.display === 'none') o = 0;
    o *= effOpacity(el.parentElement);
    opacityCache.set(el, o);
    return o;
  };

  const isInline = (cs) => cs.display === 'inline' || cs.display === 'contents';
  const isFlexLike = (cs) => /flex|grid/.test(cs.display);

  // Colapsa espacios comunes como CSS; los espacios duros (&nbsp;) se conservan.
  const normWs = (s, ws) => (/pre/.test(ws) ? s : s.replace(/[ \t\n\r\f]+/g, ' '));

  const runStyle = (el, opMul) => {
    const cs = getComputedStyle(el);
    const col = parseColor(cs.color) || { r: 255, g: 255, b: 255, a: 1 };
    let ls = cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing);
    return {
      font: cs.fontFamily,
      size: parseFloat(cs.fontSize),
      weight: parseInt(cs.fontWeight, 10),
      italic: cs.fontStyle === 'italic',
      color: hex(col),
      alpha: col.a * opMul,
      spacing: ls,
      transform: cs.textTransform,
      ws: cs.whiteSpace,
      sub: cs.verticalAlign === 'sub' || el.tagName === 'SUB',
      sup: cs.verticalAlign === 'super' || el.tagName === 'SUP',
    };
  };

  const pseudoRun = (el, which, opMul) => {
    const ps = getComputedStyle(el, which);
    const c = ps.content;
    if (!c || c === 'none' || c === 'normal') return null;
    const m = c.match(/^"(.*)"$/);
    if (!m || !m[1].trim()) return null;
    if (ps.display === 'none') return null;
    const col = parseColor(ps.color) || { r: 255, g: 255, b: 255, a: 1 };
    return {
      absolute: ps.position === 'absolute' || ps.position === 'fixed',
      pleft: ps.left, ptop: ps.top, lh: ps.lineHeight,
      text: m[1] + (which === '::before' && !(ps.position === 'absolute') ? ' ' : ''),
      font: ps.fontFamily, size: parseFloat(ps.fontSize), weight: parseInt(ps.fontWeight, 10),
      italic: ps.fontStyle === 'italic', color: hex(col), alpha: col.a * opMul,
      spacing: ps.letterSpacing === 'normal' ? 0 : parseFloat(ps.letterSpacing),
      transform: ps.textTransform, ws: 'normal', pseudo: true,
    };
  };

  // Recolecta segmentos de texto en flujo inline dentro de un contenedor.
  // Devuelve lista de segmentos; cada segmento es lista de partes {node|br|pseudo}.
  const collectSegments = (container) => {
    const csC = getComputedStyle(container);
    const flex = isFlexLike(csC);
    const segments = [];
    let cur = [];
    const flush = () => { if (cur.length) { segments.push(cur); cur = []; } };
    const visit = (node, depth) => {
      for (const ch of node.childNodes) {
        if (ch.nodeType === Node.TEXT_NODE) {
          if (!ch.textContent) continue;
          if (flex && depth === 0) {
            // cada texto directo de un flex/grid es su propio item anonimo
            if (ch.textContent.trim()) { flush(); cur.push({ node: ch }); flush(); }
          } else {
            cur.push({ node: ch });
          }
        } else if (ch.nodeType === Node.ELEMENT_NODE) {
          const cs = getComputedStyle(ch);
          if (cs.display === 'none') continue;
          if (ch.tagName === 'BR') { cur.push({ br: true }); continue; }
          if (isInline(cs) && !(flex && depth === 0)) {
            const extraL = parseFloat(cs.marginLeft) + parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
            const extraR = parseFloat(cs.marginRight) + parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
            if (extraL > 4) cur.push({ space: true, el: ch });
            const pb = pseudoRun(ch, '::before', effOpacity(ch));
            if (pb && !pb.absolute) cur.push({ pseudo: pb, el: ch });
            visit(ch, depth + 1);
            const pa = pseudoRun(ch, '::after', effOpacity(ch));
            if (pa && !pa.absolute) cur.push({ pseudo: pa, el: ch });
            if (extraR > 4) cur.push({ space: true, el: ch });
          } else {
            flush();
          }
        }
      }
    };
    visit(container, 0);
    flush();
    return segments;
  };

  const emitAbsPseudo = (el, which, op) => {
    const ps = pseudoRun(el, which, op);
    if (!ps || !ps.absolute) return;
    const cs = getComputedStyle(el);
    const base = (isInline(cs) ? el.getClientRects()[0] : null) || el.getBoundingClientRect();
    if (!base) return;
    const left = parseFloat(ps.pleft);
    const top = parseFloat(ps.ptop);
    const lh = ps.lh === 'normal' ? ps.size * 1.2 : parseFloat(ps.lh);
    const x = base.left + parseFloat(cs.borderLeftWidth) + (isNaN(left) ? 0 : left);
    const y = isNaN(top) ? base.top + (base.height - lh) / 2 : base.top + parseFloat(cs.borderTopWidth) + top;
    const w = ps.size * 0.9 * Math.max(1, ps.text.length);
    items.push({ type: 'text', runs: [{ ...ps }], align: 'left', bbox: [x, y, w, lh], content: [x, y, w, lh],
      lines: 1, lineHeight: lh, fontSize: ps.size, ws: 'normal', anon: false, firstH: lh, pseudoPrefix: false });
  };

  const handledText = new Set();

  const emitTextFor = (container, op) => {
    const csC = getComputedStyle(container);
    const segments = collectSegments(container);
    const before = pseudoRun(container, '::before', op);
    const after = pseudoRun(container, '::after', op);
    segments.forEach((seg, si) => {
      const textNodes = seg.filter(p => p.node);
      if (!textNodes.some(p => p.node.textContent.trim())) return;
      // runs
      let runs = [];
      let pseudoPrefix = false;
      if (before && !before.absolute && si === 0) { runs.push({ ...before }); pseudoPrefix = true; }
      for (const p of seg) {
        if (p.br) { runs.push({ br: true }); continue; }
        if (p.space) { const st = runStyle(p.el, effOpacity(p.el)); runs.push({ ...st, text: ' ', ws: 'normal' }); continue; }
        if (p.pseudo) { runs.push({ ...p.pseudo }); if (runs.length === 1) pseudoPrefix = true; continue; }
        const parent = p.node.parentElement;
        const st = runStyle(parent, effOpacity(parent));
        let t = normWs(p.node.textContent, st.ws);
        if (st.transform === 'uppercase') t = t.toUpperCase();
        else if (st.transform === 'lowercase') t = t.toLowerCase();
        runs.push({ text: t, ...st });
      }
      if (after && !after.absolute && si === segments.length - 1) runs.push({ ...after });
      // trim
      const firstIdx = runs.findIndex(r => !r.br);
      if (firstIdx >= 0) runs[firstIdx].text = runs[firstIdx].text.replace(/^ +/, '');
      for (let i = runs.length - 1; i >= 0; i--) { if (!runs[i].br) { runs[i].text = runs[i].text.replace(/ +$/, ''); break; } }
      // colapsar espacios entre runs
      let prevSpace = true;
      for (const r of runs) {
        if (r.br) { prevSpace = true; continue; }
        if (!/pre/.test(r.ws || '') && prevSpace) r.text = r.text.replace(/^ +/, '');
        if (r.text.length) prevSpace = /\s$/.test(r.text);
      }
      runs = runs.filter(r => r.br || r.text.length);
      if (!runs.some(r => !r.br && r.text.trim())) return;
      // geometria
      const range = document.createRange();
      const tn = textNodes;
      range.setStart(tn[0].node, 0);
      const last = tn[tn.length - 1].node;
      range.setEnd(last, last.textContent.length);
      const rects = Array.from(range.getClientRects()).filter(r => r.width > 0.5 && r.height > 0.5);
      if (!rects.length) return;
      let x0 = Math.min(...rects.map(r => r.left)), y0 = Math.min(...rects.map(r => r.top));
      let x1 = Math.max(...rects.map(r => r.right)), y1 = Math.max(...rects.map(r => r.bottom));
      if (x1 < 0 || y1 < 0 || x0 > VW || y0 > VH) return;
      const tops = [];
      rects.forEach(r => { if (!tops.some(t => Math.abs(t - r.top) < r.height * 0.5)) tops.push(r.top); });
      const cr = container.getBoundingClientRect();
      const padL = parseFloat(csC.paddingLeft) + parseFloat(csC.borderLeftWidth);
      const padR = parseFloat(csC.paddingRight) + parseFloat(csC.borderRightWidth);
      let align = csC.textAlign;
      if (align === 'start') align = 'left';
      if (align === 'end') align = 'right';
      if (align === '-webkit-center') align = 'center';
      const lhRaw = csC.lineHeight;
      const fs = parseFloat(csC.fontSize);
      const lh = lhRaw === 'normal' ? fs * 1.2 : parseFloat(lhRaw);
      items.push({
        type: 'text', runs, align,
        bbox: [x0, y0, x1 - x0, y1 - y0],
        content: [cr.left + padL, cr.top, cr.width - padL - padR, cr.height],
        lines: tops.length, lineHeight: lh, fontSize: fs,
        ws: csC.whiteSpace, anon: isFlexLike(csC), firstH: rects[0].height,
        pseudoPrefix,
      });
    });
  };

  const walk = (el) => {
    if (skip && el.matches && el.matches(skip)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return;
    const op = effOpacity(el);
    if (op < 0.03) return;
    const r = el.getBoundingClientRect();
    const offscreen = r.right < 0 || r.bottom < 0 || r.left > VW || r.top > VH;
    if (offscreen && cs.overflow !== 'visible') return;
    if (isInline(cs) && !offscreen) {
      const bg = parseColor(cs.backgroundColor);
      const bw = parseFloat(cs.borderTopWidth) || 0;
      const bc = parseColor(cs.borderTopColor);
      const hasB = bw > 0 && cs.borderTopStyle !== 'none' && bc && bc.a > 0;
      if ((bg && bg.a > 0.01) || hasB) {
        for (const fr of el.getClientRects()) {
          if (fr.width < 1 || fr.height < 1) continue;
          const b = hasB ? { w: bw, color: hex(bc), alpha: bc.a * op, style: cs.borderTopStyle } : null;
          items.push({ type: 'box', x: fr.left, y: fr.top, w: fr.width, h: fr.height,
            fill: bg && bg.a > 0.01 ? hex(bg) : null, fillAlpha: bg && bg.a > 0.01 ? bg.a * op : 0,
            sides: [b, b, b, b], radius: parseFloat(cs.borderTopLeftRadius) || 0, tag: el.tagName, inline: true });
        }
      }
    }
    if (!isInline(cs) && r.width >= 1 && r.height >= 1 && !offscreen) {
      const bg = parseColor(cs.backgroundColor);
      const sides = ['Top', 'Right', 'Bottom', 'Left'].map(S => {
        const w = parseFloat(cs['border' + S + 'Width']);
        const st = cs['border' + S + 'Style'];
        const c = parseColor(cs['border' + S + 'Color']);
        return (w > 0 && st !== 'none' && st !== 'hidden' && c && c.a > 0) ? { w, color: hex(c), alpha: c.a * op, style: st } : null;
      });
      const hasBg = bg && bg.a > 0.01;
      if (hasBg || sides.some(Boolean)) {
        items.push({
          type: 'box', x: r.left, y: r.top, w: r.width, h: r.height,
          fill: hasBg ? hex(bg) : null, fillAlpha: hasBg ? bg.a * op : 0,
          sides, radius: parseFloat(cs.borderTopLeftRadius) || 0, tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '',
        });
      }
      const bgi = cs.backgroundImage;
      const um = bgi && bgi.match(/url\("?([^")]+)"?\)/);
      if (um && el.tagName !== 'IMG') {
        items.push({ type: 'img', src: um[1], x: r.left, y: r.top, w: r.width, h: r.height, fit: cs.backgroundSize === 'contain' ? 'contain' : 'cover', opacity: op, bgimage: true });
      }
      if (el.tagName === 'IMG' && el.naturalWidth) {
        const pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth);
        const pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
        const pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
        const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
        items.push({ type: 'img', src: el.currentSrc || el.src, x: r.left + pl, y: r.top + pt, w: r.width - pl - pr, h: r.height - pt - pb, fit: cs.objectFit, nat: [el.naturalWidth, el.naturalHeight], opacity: op });
      }
    }
    if (!isInline(cs)) emitTextFor(el, op);
    if (!offscreen) { emitAbsPseudo(el, '::before', op); emitAbsPseudo(el, '::after', op); }
    for (const ch of el.children) walk(ch);
  };
  walk(scene);
  return items;
}
module.exports = { extractScene };
