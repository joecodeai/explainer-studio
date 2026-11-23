import React, { useMemo } from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { Word } from "./types";
import { T } from "./theme";

/** Pages of <= ~38 characters that never span two speakers; break on punctuation. */
function paginate(words: Word[], maxLen = 38) {
  const pages: Word[][] = [];
  let cur: Word[] = [], len = 0;
  words.forEach((w, i) => {
    const prev = cur[cur.length - 1];
    const newSpeaker = prev && prev.speaker !== w.speaker;
    const pause = prev && w.startMs - prev.endMs > 350;
    if (cur.length && (newSpeaker || pause || len + w.text.length > maxLen)) { pages.push(cur); cur = []; len = 0; }
    cur.push(w); len += w.text.length + 1;
    if (/[.!?]$/.test(w.text) && len > 18) { pages.push(cur); cur = []; len = 0; }
  });
  if (cur.length) pages.push(cur);
  return pages;
}

export const Captions: React.FC<{ words: Word[]; accent: string; colors: Record<string, string> }> = ({ words, accent, colors }) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H } = useVideoConfig();
  const vert = H > W, u = vert ? W / 1080 : 1;
  const ms = (frame / fps) * 1000;
  const pages = useMemo(() => paginate(words, vert ? 26 : 38), [words, vert]);
  const idx = pages.findIndex((pg, i) => ms >= pg[0].startMs - 60 && ms < (pages[i + 1] ? pages[i + 1][0].startMs - 60 : pg[pg.length - 1].endMs + 400));
  if (idx < 0) return null;
  const page = pages[idx];
  const start = page[0].startMs - 60;
  const pop = interpolate(frame - Math.round((start / 1000) * fps), [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const bar = colors[page[0].speaker] ?? "#ffffff";
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: vert ? H * 0.2 : 70, display: "flex", justifyContent: "center" }}>
      <div style={{ maxWidth: vert ? W * 0.88 : 1380, textAlign: "center", padding: "10px 26px 12px", borderLeft: `6px solid ${bar === "#ffffff" ? T.red : bar}`,
        background: "rgba(15,27,45,0.78)", borderRadius: 6, transform: `translateY(${(1 - pop) * 8}px)`, opacity: pop }}>
        <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: vert ? 58 * u : 50, lineHeight: 1.25, color: "white", letterSpacing: 0.2 }}>
          {page.map((w, i) => {
            const active = ms >= w.startMs - 30 && ms < w.endMs + 30;
            const said = ms >= w.startMs;
            return <span key={i} style={{ display: "inline-block", margin: "0 0.22em",
              color: w.emph ? "#ffd166" : said || active ? "white" : "rgba(255,255,255,0.72)",
              fontWeight: w.emph ? 800 : 600 }}>{w.text.replace(/\*/g, "")}</span>;
          })}
        </div>
      </div>
    </div>
  );
};
