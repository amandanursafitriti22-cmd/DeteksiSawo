#!/usr/bin/env node
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, "public");
const distClientDir = path.join(__dirname, "dist", "client");

const PORT = 5174;

const server = http.createServer((req, res) => {
  // Handle model requests
  if (req.url.startsWith("/models/")) {
    const modelPath = path.join(publicDir, req.url);
    if (fs.existsSync(modelPath)) {
      const stat = fs.statSync(modelPath);
      res.writeHead(200, {
        "Content-Type": "application/octet-stream",
        "Content-Length": stat.size,
      });
      fs.createReadStream(modelPath).pipe(res);
      return;
    }
  }

  // Try to serve from dist/client
  let filePath = path.join(distClientDir, req.url);
  if (req.url === "/" || req.url === "") {
    filePath = path.join(distClientDir, "index.html");
  }

  // If it's a directory, try index.html
  if (fs.existsSync(filePath)) {
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      filePath = path.join(filePath, "index.html");
    }
  }

  // Read and serve file
  if (fs.existsSync(filePath)) {
    const ext = path.extname(filePath);
    const contentTypes = {
      ".html": "text/html",
      ".js": "application/javascript",
      ".css": "text/css",
      ".json": "application/json",
      ".png": "image/png",
      ".jpg": "image/jpeg",
      ".gif": "image/gif",
      ".svg": "image/svg+xml",
      ".wasm": "application/wasm",
    };

    const contentType = contentTypes[ext] || "application/octet-stream";
    const stat = fs.statSync(filePath);

    res.writeHead(200, {
      "Content-Type": contentType,
      "Content-Length": stat.size,
    });
    fs.createReadStream(filePath).pipe(res);
  } else {
    // Serve index.html for SPA routing
    const indexPath = path.join(distClientDir, "index.html");
    if (fs.existsSync(indexPath)) {
      const content = fs.readFileSync(indexPath);
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(content);
    } else {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("Not found");
    }
  }
});

server.listen(PORT, () => {
  console.log(`\n  ➜  Local:   http://localhost:${PORT}/`);
  console.log(`  ➜  press Ctrl+C to stop\n`);
});
