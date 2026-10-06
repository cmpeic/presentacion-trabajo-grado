// Servidor estático de alto rendimiento en memoria RAM para la presentación.
// Uso: node servidor.js [puerto]
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = Number(process.argv[2]) || 4600;
const ROOT = __dirname;

const TIPOS = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".mp4": "video/mp4",
  ".woff2": "font/woff2",
};

// Caché en memoria RAM para entrega en 0 ms
const memoriaCache = new Map();

function precargarDirectorio(dir) {
  try {
    const archivos = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of archivos) {
      const rutaCompleta = path.join(dir, item.name);
      if (item.isDirectory()) {
        precargarDirectorio(rutaCompleta);
      } else if (item.isFile()) {
        const ext = path.extname(item.name).toLowerCase();
        if (TIPOS[ext]) {
          try {
            const buffer = fs.readFileSync(rutaCompleta);
            memoriaCache.set(rutaCompleta, buffer);
          } catch (e) {}
        }
      }
    }
  } catch (e) {}
}

// Precargar assets en RAM al iniciar
precargarDirectorio(path.join(ROOT, "assets"));

const servidor = http.createServer((req, res) => {
  let ruta = decodeURIComponent(req.url.split("?")[0]);
  if (ruta === "/") ruta = "/presentar.html";

  const destino = path.join(ROOT, path.normalize(ruta).replace(/^([\\/])+/, ""));
  if (!destino.startsWith(ROOT)) {
    res.writeHead(403).end("Prohibido");
    return;
  }

  const ext = path.extname(destino).toLowerCase();
  const esEstatico = [".png", ".jpg", ".jpeg", ".svg", ".webp", ".mp4", ".woff2"].includes(ext);
  const headers = {
    "Content-Type": TIPOS[ext] || "application/octet-stream",
    "Cache-Control": esEstatico ? "public, max-age=31536000, immutable" : "no-cache",
  };

  // Si está en RAM y es estático, responder de inmediato
  if (esEstatico && memoriaCache.has(destino)) {
    const contenido = memoriaCache.get(destino);
    headers["Content-Length"] = contenido.length;
    res.writeHead(200, headers);
    res.end(contenido);
    return;
  }

  fs.readFile(destino, (error, contenido) => {
    if (error) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("No encontrado: " + ruta);
      return;
    }
    if (esEstatico) memoriaCache.set(destino, contenido);
    headers["Content-Length"] = contenido.length;
    res.writeHead(200, headers);
    res.end(contenido);
  });
});

servidor.listen(PORT, "127.0.0.1", () => {
  console.log("Presentación servida en http://localhost:" + PORT + "/presentar.html");
  console.log("Composición cruda:      http://localhost:" + PORT + "/index.html?t=0");
  console.log("Caché en RAM activa con " + memoriaCache.size + " archivos multimedia precargados.");
  console.log("Ctrl+C para detener.");
});
