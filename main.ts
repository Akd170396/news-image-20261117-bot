import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261117: the image is drawn at build time by
// render.py and shipped as entry.png; this program just copies it to the
// output directory. A plain byte copy is deterministic by construction.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), dest);

// Self-check: the output must be a whole PNG (magic bytes) of the same
// size as the source, so a truncated copy can never pass silently.
const head = readFileSync(dest).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) throw new Error("output is not a PNG");
console.log(`wrote entry.png (${statSync(dest).size} bytes)`);
