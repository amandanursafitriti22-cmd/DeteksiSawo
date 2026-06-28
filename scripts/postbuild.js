import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.join(__dirname, "..");
const distServerDir = path.join(projectRoot, "dist", "server");
const assetsDir = path.join(distServerDir, "assets");

// Find the server file in assets (usually named server-<hash>.js)
const files = fs.readdirSync(assetsDir);
const serverFile = files.find((f) => f.startsWith("server-") && f.endsWith(".js"));

if (!serverFile) {
  console.warn("[postbuild] No server-*.js file found in dist/server/assets/");
  process.exit(0);
}

const sourceFile = path.join(assetsDir, serverFile);
const destFile = path.join(distServerDir, "server.js");

// Copy server file to root of dist/server
fs.copyFileSync(sourceFile, destFile);
console.log(`[postbuild] Copied ${serverFile} → server.js`);
