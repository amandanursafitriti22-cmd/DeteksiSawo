import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import server from "../dist/server/server.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distClientDir = path.join(__dirname, "..", "dist", "client");

const contentTypes = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".wasm": "application/wasm",
  ".webp": "image/webp",
  ".txt": "text/plain",
};

function getContentType(filePath) {
  return contentTypes[path.extname(filePath).toLowerCase()] || "application/octet-stream";
}

function sendStaticFile(res, filePath) {
  const data = fs.readFileSync(filePath);
  res.statusCode = 200;
  res.setHeader("Content-Type", getContentType(filePath));
  res.setHeader("Content-Length", data.length);
  res.end(data);
}

export default async function handler(req, res) {
  const host = req.headers.host || "localhost";
  const url = new URL(req.url, `https://${host}`);

  if (url.pathname.startsWith("/assets/") || url.pathname.startsWith("/models/")) {
    const filePath = path.join(distClientDir, url.pathname);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      return sendStaticFile(res, filePath);
    }
  }

  const request = new Request(url.toString(), {
    method: req.method,
    headers: req.headers,
    body: ["GET", "HEAD"].includes(req.method) ? undefined : req,
  });

  const response = await server.default.fetch(request);

  res.statusCode = response.status;
  response.headers.forEach((value, name) => {
    try {
      res.setHeader(name, value);
    } catch {}
  });

  const body = await response.arrayBuffer();
  res.end(Buffer.from(body));
}
