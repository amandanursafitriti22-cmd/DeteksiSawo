import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import tsconfigPaths from "vite-tsconfig-paths";
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Middleware untuk serve large model files dari public folder
function largeFilesPlugin() {
  return {
    name: "serve-large-files",
    apply: "serve",
    configResolved() {},
    transformIndexHtml() {
      return [];
    },
  };
}

// Custom middleware untuk serve public files
function servePublicMiddleware() {
  return {
    name: "serve-public",
    apply: "serve",
    configResolved(config: any) {
      const middlewares = config.middlewares;
      middlewares.use((req: any, res: any, next: any) => {
        // Handle /models/ requests
        if (req.url.startsWith("/models/")) {
          const filePath = path.join(__dirname, "public", req.url);
          if (fs.existsSync(filePath)) {
            const stat = fs.statSync(filePath);
            res.setHeader("Content-Type", "application/octet-stream");
            res.setHeader("Content-Length", stat.size);
            res.setHeader("Access-Control-Allow-Origin", "*");
            res.setHeader("Cache-Control", "no-cache");
            const stream = fs.createReadStream(filePath);
            stream.pipe(res);
            return;
          }
        }
        next();
      });
    },
  };
}

// Redirect TanStack Start's bundled server entry to src/server.ts (our SSR error wrapper).
// @cloudflare/vite-plugin builds from this — wrangler.jsonc main alone is insufficient.
export default defineConfig(async ({ command }) => {
  const plugins = [
    tanstackStart({
      server: { entry: "server" },
      importProtection: {
        behavior: "error",
        client: {
          files: ["**/server/**"],
          specifiers: ["server-only"],
        },
      },
    }),
    react(),
    tailwindcss(),
    tsconfigPaths(),
  ];

  if (command === "build") {
    try {
      const { cloudflare } = await import("@cloudflare/vite-plugin");
      plugins.push(
        cloudflare({
          viteEnvironment: { name: "ssr" },
        }),
      );
    } catch {
    }
  }

  return {
    resolve: {
      alias: { "@": `${process.cwd()}/src` },
      dedupe: [
        "react",
        "react-dom",
        "react/jsx-runtime",
        "react/jsx-dev-runtime",
        "@tanstack/react-query",
        "@tanstack/query-core",
      ],
    },
    publicDir: "public",
    server: {
      host: true,
      port: 5173,
      middlewares: [
        // Serve large model files from public folder
        (req: any, res: any, next: any) => {
          if (req.url.startsWith("/models/")) {
            const filePath = path.join(__dirname, "public", req.url);
            if (fs.existsSync(filePath)) {
              const stat = fs.statSync(filePath);
              res.setHeader("Content-Type", "application/octet-stream");
              res.setHeader("Content-Length", stat.size);
              res.setHeader("Access-Control-Allow-Origin", "*");
              res.setHeader("Cache-Control", "no-cache");
              const stream = fs.createReadStream(filePath);
              stream.pipe(res);
              return;
            }
          }
          next();
        },
      ],
    },
    build: {
      rollupOptions: {
        output: {
          entryFileNames: (chunkInfo: any) => {
            if (chunkInfo.name === "server") {
              return "[name].js";
            }
            return "assets/[name]-[hash].js";
          },
        },
      },
    },
    plugins,
  };
});
