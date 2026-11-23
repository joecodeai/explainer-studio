import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { SceneProps, Line, Beat } from "./types";
import { Character, SLOT, CHAR_H, FEET_Y, posX } from "./Character";
import { Captions } from "./Captions";
import { MapScene } from "./MapScene";
import { T } from "./theme";
import { ScreenInsert, TopText } from "./Screens";

type Cam = { s: number; x: number; y: number };

/** camera framing for a line: wide / two_shot / closeup on speaker / detail on beat area */
function camFor(p: SceneProps, l: Line | undefined, W: number, H: number): Cam {
  if (!l || p.cast.length === 0) return { s: 1.0, x: W / 2, y: H / 2 };
  const sp = p.cast.find((c) => c.char === l.speaker);
  const feet = H * FEET_Y, head = H * (FEET_Y - CHAR_H), push = 1.035;
  // closeup: head keeps ~70 px headroom; everything else: feet stay in frame (~25 px above the bottom edge)
  if (l.shot === "closeup" && sp) { const s = 1.6; return { s, x: W * posX(sp), y: head + (H / 2 - 70) / (s * push) }; }
  if (l.shot === "detail") return { s: 1.2, x: W / 2, y: H * 0.4 };
  if (l.shot === "wide") return { s: 1.0, x: W / 2, y: H / 2 };
  const xs = p.cast.map((c) => W * posX(c));
  const s = 1.06;
  return { s, x: (Math.min(...xs) + Math.max(...xs)) / 2, y: feet - (H / 2 - 25) / (s * push) };
}

const Camera: React.FC<{ p: SceneProps; children: React.ReactNode }> = ({ p, children }) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const found = p.lines.findIndex((l) => t < l.end + 0.1);
  const idx = found === -1 ? p.lines.length - 1 : found;   // after the last line keep its framing (was snapping back to line 0)
  const cur = p.lines[idx];
  const prev = p.lines[Math.max(0, idx - 1)];
  const a = camFor(p, prev, W, H), b = camFor(p, cur, W, H);
  const st = cur ? cur.start : 0;
  // closeups/cuts snap fast (like an edit), other moves ease over ~0.5 s
  const dur = cur && (cur.shot === "closeup" || prev?.shot === "closeup") ? 0.12 : 0.55;
  const k = idx === 0 ? 1 : interpolate(t, [st - 0.05, st - 0.05 + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const c = { s: a.s + (b.s - a.s) * k, x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k };
  const push = 1 + interpolate(frame, [0, durationInFrames], [0, 0.035]); // slow push-in
  const s = c.s * push;
  // keep the frame filled: clamp centre so edges never show
  const x = Math.min(Math.max(c.x, W / (2 * s)), W - W / (2 * s)), y = Math.min(Math.max(c.y, H / (2 * s)), H - H / (2 * s));
  return <AbsoluteFill style={{ transform: `scale(${s}) translate(${W / 2 - x}px, ${H / 2 - y}px)`, transformOrigin: "50% 50%" }}>{children}</AbsoluteFill>;
};

/** big keyword / animated number / sticker label, timed to the narration.
 *  Only the newest beat is shown (no stacking). Placement: stage = top band above the heads (or the free side in a
 *  closeup); map/chart = top-right corner under the title; hero = top band. */
type Spot = "band" | "left" | "right" | "corner";
const BeatLayer: React.FC<{ beats: Beat[]; accent: string; spot: Spot }> = ({ beats, accent, spot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const live = beats.filter((b) => ms >= b.atMs && ms < b.atMs + 2600);
  if (!live.length) return null;
  const b = live[live.length - 1];
  const next = beats.find((x) => x.atMs > b.atMs);
  const end = Math.min(b.atMs + 2600, next ? next.atMs : Infinity);
  const f = frame - Math.round((b.atMs / 1000) * fps);
  const p = interpolate(f, [0, 9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  const out = interpolate(ms, [end - 250, end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const small = spot === "corner";
  const wrap: React.CSSProperties =
    spot === "band" ? { position: "absolute", top: 56, left: 70 } :
    spot === "corner" ? { position: "absolute", top: 170, right: 70, display: "flex", justifyContent: "flex-end", maxWidth: 640 } :
    { position: "absolute", top: 120, [spot]: 80, maxWidth: 640 } as any;
  const card: React.CSSProperties = { display: "inline-block", background: "rgba(255,255,255,0.96)", borderLeft: `10px solid ${T.red}`,
    padding: "12px 26px 14px", boxShadow: "0 10px 30px rgba(0,0,0,0.22)", opacity: out * p,
    transform: `translateX(${(1 - p) * (spot === "right" || spot === "corner" ? 40 : -40)}px)`, maxWidth: 640 };
  let el: React.ReactNode;
  if (b.type === "number") {
    const m = b.text.match(/^([^\d\-]*)(-?[\d.,]+)(.*)$/);
    const num = m ? parseFloat(m[2].replace(/,/g, "")) : 0;
    const dec = m && m[2].includes(".") ? (m[2].split(".")[1] || "").length : 0;
    const val = interpolate(f, [0, 22], [0, num], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
    const isYear = m && !m[2].includes(".") && !m[2].includes(",") && num >= 1800 && num <= 2100;   // years / dates: no count-up, no thousands comma
    const shown = !m || isYear ? b.text : `${m[1]}${val.toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec })}${m[3]}`;
    el = <div style={card}><div style={{ fontFamily: T.head, fontWeight: 800, fontSize: small ? 76 : 92, lineHeight: 1, color: T.red, letterSpacing: -1 }}>{shown}</div></div>;
  } else if (b.type === "keyword") {
    el = <div style={card}><div style={{ fontFamily: T.head, fontWeight: 800, fontSize: small ? 44 : 52, lineHeight: 1.1, color: T.navy, textTransform: "uppercase", letterSpacing: 0.5 }}>{b.text}</div></div>;
  } else {
    el = <div style={{ ...card, background: T.navy, borderLeft: `10px solid ${T.red}` }}><div style={{ fontFamily: T.body, fontWeight: 700, fontSize: small ? 34 : 38, color: "white" }}>{b.text}</div></div>;
  }
  return <div style={wrap}>{el}</div>;
};

const TitleCard: React.FC<{ text: string; chapter: number; accent: string; bg: string | null }> = ({ text, chapter, bg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const e = (a: number, b: number) => interpolate(frame, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  const rule = e(4, 20), wipe = e(8, 26), kick = e(0, 12);
  return <AbsoluteFill style={{ background: T.navy, justifyContent: "center", overflow: "hidden" }}>
    {bg && <Img src={staticFile(bg)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", filter: "blur(18px) grayscale(0.6) brightness(0.35)", transform: `scale(${1.1 + frame * 0.001})` }} />}
    <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(15,27,45,0.95) 0%, rgba(15,27,45,0.7) 60%, rgba(15,27,45,0.5) 100%)" }} />
    <div style={{ position: "relative", marginLeft: 170, maxWidth: 1450 }}>
      {chapter > 0 && <div style={{ fontFamily: T.body, fontWeight: 700, fontSize: 30, color: T.red, letterSpacing: 8, opacity: kick, marginBottom: 18 }}>PART {chapter}</div>}
      <div style={{ width: 140 * rule, height: 8, background: T.red, marginBottom: 30 }} />
      <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 92, lineHeight: 1.08, color: "white", letterSpacing: -1,
        clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)` }}>{text}</div>
    </div>
  </AbsoluteFill>;
};

const ChartTitle: React.FC<{ title: string; t0: number }> = ({ title, t0 }) => <div style={{ position: "absolute", top: 70, left: 120, right: 120, opacity: t0 }}>
  <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 60, color: T.navy, letterSpacing: -0.5 }}>{title}</div>
  <div style={{ width: 120 * t0, height: 7, background: T.red, marginTop: 14 }} />
</div>;

/** big-number cards: for figures that do not share a unit (never put 2x and 750,000 on one bar axis) */
const Stats: React.FC<{ chart: NonNullable<SceneProps["chart"]> }> = ({ chart }) => {
  const frame = useCurrentFrame();
  const t0 = interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  const items = chart.items || [];
  return <AbsoluteFill style={{ background: T.paper }}>
    {chart.title && <ChartTitle title={chart.title} t0={t0} />}
    <div style={{ position: "absolute", top: 260, bottom: 230, left: 120, right: 120, display: "flex", gap: 50, alignItems: "stretch" }}>
      {items.map((it, i) => {
        const g = interpolate(frame - 8 - i * 10, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
        return <div key={i} style={{ flex: 1, background: "white", borderTop: `10px solid ${i === 0 ? T.red : T.navy}`, padding: "50px 46px",
          boxShadow: "0 14px 40px rgba(15,27,45,0.12)", opacity: g, transform: `translateY(${(1 - g) * 30}px)`, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: it.value.length > 9 ? 84 : 120, lineHeight: 1, color: i === 0 ? T.red : T.navy, letterSpacing: -2 }}>{it.value}</div>
          <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 36, lineHeight: 1.25, color: T.ink, marginTop: 26 }}>{it.label}</div>
        </div>;
      })}
    </div>
  </AbsoluteFill>;
};

/** dated events on a horizontal line */
const Timeline: React.FC<{ chart: NonNullable<SceneProps["chart"]> }> = ({ chart }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t0 = interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  const items = chart.items || [];
  const n = Math.max(1, items.length);
  const span = Math.min(durationInFrames * 0.7, 30 + n * 28);
  const line = interpolate(frame, [6, span], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const L = 180, R = 1920 - 180, Y = 540;
  return <AbsoluteFill style={{ background: T.paper }}>
    {chart.title && <ChartTitle title={chart.title} t0={t0} />}
    <div style={{ position: "absolute", left: L, top: Y - 3, width: (R - L) * line, height: 6, background: T.navy }} />
    {items.map((it, i) => {
      const x = n === 1 ? (L + R) / 2 : L + ((R - L) * i) / (n - 1);
      const on = interpolate(line * (n - 1) - i, [-0.05, 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const last = i === n - 1, up = i % 2 === 0;
      return <div key={i} style={{ position: "absolute", left: x, top: Y, opacity: on }}>
        <div style={{ position: "absolute", left: -16, top: -16, width: 32, height: 32, borderRadius: 16, background: last ? T.red : "white", border: `6px solid ${last ? T.red : T.navy}` }} />
        <div style={{ position: "absolute", left: -190, width: 380, textAlign: "center", [up ? "bottom" : "top"]: 40 } as any}>
          <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 46, color: last ? T.red : T.navy }}>{it.value}</div>
          <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 30, lineHeight: 1.2, color: T.ink, marginTop: 6 }}>{it.label}</div>
        </div>
      </div>;
    })}
  </AbsoluteFill>;
};

const Chart: React.FC<{ chart: NonNullable<SceneProps["chart"]>; accent: string }> = ({ chart }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (chart.mode === "stats" && chart.items?.length) return <Stats chart={chart} />;
  if (chart.mode === "timeline" && chart.items?.length) return <Timeline chart={chart} />;
  const max = Math.max(...chart.values, 1);
  const cur = /^[$€£¥₹]$/.test(chart.unit);
  const u = /^(%|percent|pct)$/i.test(chart.unit.trim()) ? "%" : /^[a-z]/i.test(chart.unit.trim()) ? " " + chart.unit.trim().toLowerCase() : chart.unit;
  const top = chart.values.indexOf(Math.max(...chart.values));
  const H = 520;
  const t0 = interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  return <AbsoluteFill style={{ background: T.paper, padding: "230px 200px 250px" }}>
    {chart.title && <ChartTitle title={chart.title} t0={t0} />}
    <div style={{ position: "relative", height: "100%" }}>
      {[0.25, 0.5, 0.75, 1].map((g) => <div key={g} style={{ position: "absolute", left: 0, right: 0, bottom: H * g + 70, height: 2, background: T.rule, opacity: 0.8 * t0 }} />)}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 68, height: 4, background: T.navy }} />
      <div style={{ display: "flex", alignItems: "flex-end", gap: 70, justifyContent: "center", height: "100%" }}>
        {chart.values.map((v, i) => {
          const g = interpolate(frame - 10 - i * 6, [0, 24], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
          return <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", flex: 1, maxWidth: 240 }}>
            <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 54, color: i === top ? T.red : T.navy, opacity: g, marginBottom: 10 }}>{cur ? chart.unit : ""}{(v * g).toLocaleString(undefined, { maximumFractionDigits: v % 1 ? 1 : 0 })}{cur ? "" : u}</div>
            <div style={{ width: "100%", height: H * (v / max) * g, background: i === top ? T.red : T.navy2, borderRadius: "4px 4px 0 0" }} />
            <div style={{ height: 68, display: "flex", alignItems: "center", fontFamily: T.body, fontWeight: 600, fontSize: 30, color: T.grey, textAlign: "center", lineHeight: 1.1 }}>{chart.labels[i]}</div>
          </div>;
        })}
      </div>
    </div>
  </AbsoluteFill>;
};

const Grade: React.FC = () => <AbsoluteFill style={{ pointerEvents: "none",
  background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 60%, rgba(10,15,30,0.22) 100%)", mixBlendMode: "multiply" }} />;

/** lower-third name tag the first time a character speaks in the video */
const NameTag: React.FC<{ p: SceneProps }> = ({ p }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const who = (p.introduce || []).map((c) => ({ c, l: p.lines.find((l) => l.speaker === c) })).filter((x) => x.l && p.names?.[x.c]);
  const cur = who.find((x) => t >= x.l!.start && t < x.l!.start + 3.6);
  if (!cur) return null;
  const n = p.names![cur.c];
  const k = (t - cur.l!.start) * fps;
  const inn = interpolate(k, [0, 10], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(...T.ease) });
  const out = interpolate(t, [cur.l!.start + 3.2, cur.l!.start + 3.6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const m = p.cast.find((c) => c.char === cur.c);
  const right = m && posX(m) > 0.5;
  return <div style={{ position: "absolute", bottom: 200, [right ? "right" : "left"]: 90, opacity: out,
    clipPath: `inset(0 ${right ? 0 : (1 - inn) * 100}% 0 ${right ? (1 - inn) * 100 : 0}%)` } as any}>
    <div style={{ display: "flex" }}>
      <div style={{ width: 10, background: T.red }} />
      <div>
        <div style={{ background: "white", padding: "10px 24px 8px", fontFamily: T.head, fontWeight: 800, fontSize: 38, color: T.navy }}>{n.name}</div>
        {n.role && <div style={{ background: T.navy, padding: "7px 24px 9px", fontFamily: T.body, fontWeight: 500, fontSize: 26, color: "white" }}>{n.role}</div>}
      </div>
    </div>
  </div>;
};

const SourceTag: React.FC<{ text?: string; dark?: boolean }> = ({ text, dark }) => text ?
  <div style={{ position: "absolute", left: 70, bottom: 26, maxWidth: 1100, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", fontFamily: T.body, fontWeight: 600, fontSize: 22, letterSpacing: 1.5,
    color: dark ? "rgba(255,255,255,0.75)" : T.grey }}>SOURCE: {text.toUpperCase()}</div> : null;

const Brand: React.FC<{ text?: string }> = ({ text }) => text ?
  <div style={{ position: "absolute", top: 40, right: 50, display: "flex", alignItems: "center", gap: 10, background: "rgba(15,27,45,0.82)", padding: "8px 16px" }}>
    <div style={{ width: 10, height: 26, background: T.red }} />
    <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 24, color: "white", letterSpacing: 2 }}>{text.toUpperCase()}</div>
  </div> : null;

export const Scene: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const cur = p.lines.find((l) => t >= l.start && t < l.end);
  const speaker = cur ? p.cast.find((c) => c.char === cur.speaker) : undefined;
  const closeup = cur && cur.shot === "closeup";
  const spot: Spot = p.kind === "map" || p.kind === "chart" ? "corner"
    : p.kind === "stage" && closeup ? (speaker && speaker.position === "left" ? "right" : "left") : "band";
  return (
    <AbsoluteFill style={{ background: T.paper, overflow: "hidden" }}>
      {p.kind === "stage" && p.shots && p.shots.length > 0 && p.shots.map((sh, i) => {
        const from = Math.round(sh.start * fps), to = i + 1 < p.shots!.length ? Math.round(p.shots![i + 1].start * fps) : p.durationInFrames;
        return <Sequence key={i} from={from} durationInFrames={Math.max(1, to - from)}>
          <OffthreadVideo src={staticFile(sh.video)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </Sequence>;
      })}
      {p.kind === "stage" && !(p.shots && p.shots.length) && <Camera p={p}>
        {p.background && <Img src={staticFile(p.background)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "saturate(1.05)" }} />}
        {p.cast.map((m, i) => <Character key={m.char} m={m} index={i} cast={p.cast} lines={p.lines} enter={false} />)}
      </Camera>}
      {p.kind === "screen" && p.screen && <ScreenInsert s={p.screen} />}
      {p.kind === "map" && p.map && <MapScene map={p.map} accent={p.accent} />}
      {p.kind === "title_card" && <TitleCard text={p.titleText} chapter={p.chapter} accent={p.accent} bg={p.background} />}
      {p.kind === "chart" && p.chart && <Chart chart={p.chart} accent={p.accent} />}
      {p.kind === "hero" && p.heroVideo && <AbsoluteFill style={{ transform: `scale(${1.02 + frame * 0.0006})` }}>
        <OffthreadVideo src={staticFile(p.heroVideo)} muted playbackRate={p.heroRate || 1} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>}
      {p.kind !== "screen" && <Grade />}
      {p.kind !== "title_card" && <BeatLayer beats={p.beats} accent={p.accent} spot={spot} />}
      {p.kind === "stage" && <NameTag p={p} />}
      {(p.kind === "chart" || p.kind === "map") && <SourceTag text={p.sources} />}
      {p.kind !== "title_card" && <Brand text={p.brand} />}
      {p.topText && p.topText.length > 0 && <TopText items={p.topText} />}
      <Captions words={p.words} accent={p.accent} colors={p.speakerColors} />
    </AbsoluteFill>
  );
};
