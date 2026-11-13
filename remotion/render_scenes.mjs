// node render_scenes.mjs jobs.json   — jobs: {publicDir, bundleDir, concurrency, jobs:[{props, out}]}
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition, openBrowser } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const entry = path.resolve("src/index.ts");
const serveUrl = await bundle({ entryPoint: entry, publicDir: cfg.publicDir, outDir: cfg.bundleDir, enableCaching: true });
const browser = await openBrowser("chrome", { chromiumOptions: { gl: "angle" } });
for (const [i, job] of cfg.jobs.entries()) {
  const t = Date.now();
  const composition = await selectComposition({ serveUrl, id: "Scene", inputProps: job.props, puppeteerInstance: browser });
  await renderMedia({ composition, serveUrl, codec: "h264", outputLocation: job.out + ".tmp.mp4", inputProps: job.props, muted: true,
    puppeteerInstance: browser, concurrency: cfg.concurrency, crf: 18, x264Preset: "veryfast", logLevel: "error" });
  fs.renameSync(job.out + ".tmp.mp4", job.out);
  console.log(JSON.stringify({ done: job.props.id, i, n: cfg.jobs.length, sec: (Date.now() - t) / 1000 }));
}
await browser.close({ silent: true });
