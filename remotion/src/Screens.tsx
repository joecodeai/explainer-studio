// On-screen inserts (laptop / phone UI cut-aways) for show episodes. Data-driven, times in SECONDS of scene time.
// Works in 16:9 and 9:16: every size is in "u" units (1u = 1px at 1920 wide landscape / 1080 wide portrait).
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { T } from "./theme";

export type TimedText = { text: string; at?: number; until?: number };
export type ScreenSpec =
  | { type: "desktop"; folder?: string; files: { name: string; meta: string; at?: number }[]; open?: { index: number; at: number } }
  | { type: "slide"; kicker?: string; title: string; sub?: string; source?: string; file?: string }
  | { type: "notepad"; columns: string[]; items: { text: string; col: number; at?: number; strike?: boolean; moveTo?: number; moveAt?: number }[]; paper?: "yellow" | "white" }
  | { type: "download"; title: string; steps: { at: number; pct: number; remain: string }[]; ready?: { at: number; text: string } }
  | { type: "chat"; title: string; messages: { who: string; time: string; text: string; at?: number; highlight?: boolean }[]; focusAt?: number }
  | { type: "email"; emails: { from: string; subject: string; body?: string; at: number }[] }
  | { type: "calendar"; day: string; events: { time: string; title: string; note?: string; at?: number; hot?: boolean }[] }
  | { type: "call"; title: string; tiles: { name: string; state?: "off" | "away" }[]; events: { at: number; kind: "thumbs" | "away" | "present" | "stopped" | "talk"; who: string; dur?: number; text?: string }[]; ended?: number }
  | { type: "form"; title: string; fields: { label: string; value: string; at: number }[]; submitAt?: number; result?: { at: number; text: string; ok?: boolean } }
  | { type: "phone"; clock: string; date?: string; notes?: { app: string; title: string; text: string; at: number }[]; thread?: { who: string; messages: { mine?: boolean; text: string; at: number }[]; typing?: { at: number; end: number } }; alarm?: { time: string; label: string } }
  | { type: "card"; lines: { text: string; at?: number; size?: number; color?: string }[]; dark?: boolean }
  | { type: "game"; title: string; sub?: string }
  | { type: "panel"; style?: "lift" | "crossing" | "thermostat" | "red"; buttons?: { label: string; hot?: boolean }[]; presses?: number[]; reading?: { at: number; text: string }[]; caption?: string }
  | { type: "spinner"; text: string; sub?: string };

const ease = Easing.bezier(...T.ease);
const fadeIn = (t: number, at = 0, d = 0.35) => interpolate(t, [at, at + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
const shown = (t: number, at?: number) => at === undefined || t >= at;

function useU() {
  const { width: W, height: H, fps } = useVideoConfig();
  const vert = H > W;
  return { W, H, vert, u: vert ? (W / 1080) * 1.35 : W / 1920, fps };   // portrait UIs read on a phone: everything ~35% larger
}

/** a computer/phone window centred on a soft desk-blur background */
const Frame: React.FC<{ title?: string; dark?: boolean; children: React.ReactNode; phone?: boolean }> = ({ title, dark, children, phone }) => {
  const { W, H, vert, u } = useU();
  const w = phone || vert ? W * 0.92 : W * 0.82, h = vert ? H * 0.62 : H * 0.68;   // room for the top caption above, subtitles below
  return <AbsoluteFill style={{ background: dark ? "#0b1020" : "radial-gradient(ellipse at 50% 40%, #e9e6df 0%, #cfcac0 100%)" }}>
    <div style={{ position: "absolute", left: (W - w) / 2, top: vert ? H * 0.15 : H * 0.15, width: w, height: h, borderRadius: 26 * u, overflow: "hidden",
      background: dark ? "#141a2c" : "white", boxShadow: `0 ${30 * u}px ${90 * u}px rgba(0,0,0,0.28)` }}>
      {title !== undefined && <div style={{ height: 64 * u, display: "flex", alignItems: "center", gap: 12 * u, padding: `0 ${26 * u}px`,
        background: dark ? "#1d2438" : "#f1f0ec", borderBottom: `${2 * u}px solid ${dark ? "#2a3350" : "#e2dfd8"}` }}>
        {["#ff5f57", "#febc2e", "#28c840"].map((c) => <div key={c} style={{ width: 18 * u, height: 18 * u, borderRadius: 9 * u, background: c }} />)}
        <div style={{ flex: 1, textAlign: "center", fontFamily: T.body, fontWeight: 600, fontSize: 28 * u, color: dark ? "#c9d1e6" : "#555" }}>{title}</div>
      </div>}
      <div style={{ position: "absolute", top: title !== undefined ? 64 * u : 0, left: 0, right: 0, bottom: 0 }}>{children}</div>
    </div>
  </AbsoluteFill>;
};

const Desktop: React.FC<{ s: Extract<ScreenSpec, { type: "desktop" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  return <Frame title={s.folder || "Documents"}>
    <div style={{ padding: `${30 * u}px ${40 * u}px` }}>
      {s.files.map((f, i) => {
        const on = fadeIn(t, f.at ?? 0), sel = s.open && t >= s.open.at && s.open.index === i;
        return <div key={i} style={{ display: "flex", alignItems: "center", gap: 28 * u, padding: `${26 * u}px ${24 * u}px`, borderRadius: 14 * u, opacity: on,
          background: sel ? "#d9e6ff" : i % 2 ? "#faf9f6" : "white", marginBottom: 8 * u }}>
          <div style={{ width: 66 * u, height: 80 * u, borderRadius: 8 * u, background: "#d24726", color: "white", display: "flex", alignItems: "flex-end",
            justifyContent: "center", paddingBottom: 8 * u, fontFamily: T.head, fontWeight: 800, fontSize: 20 * u }}>PPT</div>
          <div style={{ flex: 1 }}>
            <div style={{ fontFamily: T.body, fontWeight: 700, fontSize: 40 * u, color: T.ink }}>{f.name}</div>
            <div style={{ fontFamily: T.body, fontWeight: 500, fontSize: 30 * u, color: T.grey, marginTop: 6 * u }}>{f.meta}</div>
          </div>
        </div>;
      })}
    </div>
  </Frame>;
};

const Slide: React.FC<{ s: Extract<ScreenSpec, { type: "slide" }>; t: number }> = ({ s, t }) => {
  const { u, vert } = useU();
  const a = fadeIn(t, 0.05, 0.45);
  return <Frame title={s.file || "WHY_THURSDAY.pptx"}>
    <AbsoluteFill style={{ background: "#0f1b2d", display: "flex", flexDirection: "column", justifyContent: "center", padding: `0 ${80 * u}px` }}>
      {s.kicker && <div style={{ fontFamily: T.body, fontWeight: 700, fontSize: 34 * u, letterSpacing: 4 * u, color: "#ffd166", opacity: a }}>{s.kicker.toUpperCase()}</div>}
      <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: (s.title.length > 26 ? 76 : vert ? 120 : 150) * u, lineHeight: 1.05, color: "white",
        marginTop: 18 * u, opacity: a, transform: `translateY(${(1 - a) * 30 * u}px)` }}>{s.title}</div>
      {s.sub && <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 44 * u, lineHeight: 1.3, color: "#c9d1e6", marginTop: 30 * u, opacity: fadeIn(t, 0.35) }}>{s.sub}</div>}
      {s.source && <div style={{ position: "absolute", bottom: 40 * u, left: 80 * u, fontFamily: T.body, fontSize: 26 * u, color: "#8792ab", letterSpacing: 1.5 * u }}>{s.source}</div>}
    </AbsoluteFill>
  </Frame>;
};

const Notepad: React.FC<{ s: Extract<ScreenSpec, { type: "notepad" }>; t: number }> = ({ s, t }) => {
  const { W, H, u, vert } = useU();
  const n = s.columns.length;
  const pw = vert ? W * 0.9 : W * 0.62, ph = vert ? H * 0.7 : H * 0.86;
  const colW = (pw - 120 * u) / n;
  const pos = (it: (typeof s.items)[0]) => {
    const moved = it.moveTo !== undefined && it.moveAt !== undefined ? interpolate(t, [it.moveAt, it.moveAt + 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease }) : 0;
    return it.col + ((it.moveTo ?? it.col) - it.col) * moved;
  };
  return <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #8a6f55 0%, #5b4632 100%)" }}>
    <div style={{ position: "absolute", left: (W - pw) / 2, top: (H - ph) / 2, width: pw, height: ph, background: s.paper === "white" ? "#fbfaf6" : "#fdf3b8",
      boxShadow: `0 ${20 * u}px ${60 * u}px rgba(0,0,0,0.35)`, transform: `rotate(-1.2deg)`,
      backgroundImage: `repeating-linear-gradient(transparent 0, transparent ${62 * u}px, #c7d7ee ${62 * u}px, #c7d7ee ${64 * u}px)` }}>
      <div style={{ position: "absolute", left: 60 * u, top: 0, bottom: 0, width: 3 * u, background: "#e6a3a3" }} />
      {s.columns.map((c, i) => <div key={i} style={{ position: "absolute", left: 90 * u + i * colW, top: 60 * u, width: colW - 20 * u,
        fontFamily: T.head, fontWeight: 800, fontSize: 40 * u, color: "#1f2a44", borderBottom: `${4 * u}px solid #1f2a44` }}>{c}</div>)}
      {s.items.map((it, i) => {
        if (!shown(t, it.at)) return null;
        const write = interpolate(t, [it.at ?? 0, (it.at ?? 0) + 0.8], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const row = s.items.filter((x, j) => j < i && x.col === it.col && x.moveTo === undefined).length;
        const x = 90 * u + pos(it) * colW, y = 170 * u + row * 96 * u;
        const strike = it.strike ? interpolate(t, [(it.at ?? 0) + 0.9, (it.at ?? 0) + 1.3], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: colW - 30 * u, clipPath: `inset(0 ${100 - write}% 0 0)` }}>
          <div style={{ position: "relative", fontFamily: T.body, fontStyle: "italic", fontWeight: 600, fontSize: 42 * u, lineHeight: 1.15, color: "#24324f" }}>
            {it.text}
            {it.strike && <div style={{ position: "absolute", left: 0, top: "52%", height: 5 * u, width: `${strike}%`, background: "#24324f" }} />}
          </div>
        </div>;
      })}
    </div>
  </AbsoluteFill>;
};

const Download: React.FC<{ s: Extract<ScreenSpec, { type: "download" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  const cur = [...s.steps].reverse().find((x) => t >= x.at) || s.steps[0];
  const nxt = s.steps.find((x) => x.at > t);
  const pct = nxt ? interpolate(t, [cur.at, nxt.at], [cur.pct, nxt.pct]) : cur.pct;
  const ready = s.ready && t >= s.ready.at;
  return <Frame title="Library — Downloads" dark>
    <div style={{ padding: `${60 * u}px ${70 * u}px` }}>
      <div style={{ fontFamily: T.head, fontWeight: 800, fontSize: 64 * u, color: "white" }}>{s.title}</div>
      <div style={{ marginTop: 50 * u, height: 26 * u, borderRadius: 13 * u, background: "#2a3350", overflow: "hidden" }}>
        <div style={{ width: `${ready ? 100 : pct}%`, height: "100%", background: ready ? "#28c840" : "linear-gradient(90deg,#ff6a3d,#ffb347)" }} />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 26 * u, fontFamily: T.body, fontWeight: 600, fontSize: 40 * u, color: "#c9d1e6" }}>
        <div>{ready ? s.ready!.text : `Downloading ${Math.floor(pct)}%`}</div>
        <div style={{ color: "white" }}>{ready ? "" : cur.remain}</div>
      </div>
    </div>
  </Frame>;
};

const Chat: React.FC<{ s: Extract<ScreenSpec, { type: "chat" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  return <Frame title={s.title}>
    <div style={{ padding: `${24 * u}px ${36 * u}px` }}>
      {s.messages.filter((m) => shown(t, m.at)).map((m, i) => {
        const a = fadeIn(t, m.at ?? 0, 0.3);
        const hl = m.highlight && s.focusAt !== undefined && t >= s.focusAt;
        return <div key={i} style={{ display: "flex", gap: 22 * u, padding: `${18 * u}px ${18 * u}px`, borderRadius: 14 * u, opacity: a,
          background: hl ? "#fff3c4" : "transparent", outline: hl ? `${4 * u}px solid #f2c94c` : "none", marginBottom: 6 * u }}>
          <div style={{ width: 70 * u, height: 70 * u, borderRadius: 35 * u, background: ["#5b8def", "#e0795b", "#7cb87a", "#b57be0", "#e0b85b"][m.who.length % 5],
            color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: T.head, fontWeight: 800, fontSize: 32 * u, flexShrink: 0 }}>{m.who[0]}</div>
          <div>
            <div style={{ fontFamily: T.body, fontSize: 30 * u, color: T.grey }}><b style={{ color: T.ink }}>{m.who}</b>  {m.time}</div>
            <div style={{ fontFamily: T.body, fontWeight: 500, fontSize: 40 * u, lineHeight: 1.25, color: T.ink, marginTop: 4 * u }}>{m.text}</div>
          </div>
        </div>;
      })}
    </div>
  </Frame>;
};

const Email: React.FC<{ s: Extract<ScreenSpec, { type: "email" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  const vis = s.emails.filter((e) => t >= e.at);
  const top = vis[vis.length - 1];
  return <Frame title="Inbox">
    <div style={{ padding: `${20 * u}px ${36 * u}px` }}>
      {[...vis].reverse().map((e, i) => {
        const a = fadeIn(t, e.at, 0.3);
        return <div key={e.subject} style={{ padding: `${22 * u}px ${20 * u}px`, borderBottom: `${2 * u}px solid #eee`, opacity: a,
          transform: `translateY(${(1 - a) * -20 * u}px)`, background: e === top ? "#f3f7ff" : "white" }}>
          <div style={{ fontFamily: T.body, fontSize: 30 * u, color: T.grey }}>{e.from}</div>
          <div style={{ fontFamily: T.body, fontWeight: 800, fontSize: 42 * u, color: T.ink, marginTop: 4 * u }}>{e.subject}</div>
          {e === top && e.body && <div style={{ fontFamily: T.body, fontSize: 36 * u, lineHeight: 1.35, color: "#333", marginTop: 14 * u }}>{e.body}</div>}
        </div>;
      })}
    </div>
  </Frame>;
};

const Calendar: React.FC<{ s: Extract<ScreenSpec, { type: "calendar" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  return <Frame title={`Calendar — ${s.day}`}>
    <div style={{ padding: `${20 * u}px ${36 * u}px` }}>
      {s.events.filter((e) => shown(t, e.at)).map((e, i) => <div key={i} style={{ display: "flex", gap: 26 * u, alignItems: "center", padding: `${14 * u}px 0`,
        borderBottom: `${2 * u}px solid #eee`, opacity: fadeIn(t, e.at ?? i * 0.08, 0.25) }}>
        <div style={{ width: 150 * u, fontFamily: T.body, fontWeight: 700, fontSize: 32 * u, color: T.grey }}>{e.time}</div>
        <div style={{ flex: 1, padding: `${12 * u}px ${20 * u}px`, borderLeft: `${8 * u}px solid ${e.hot ? T.red : "#5b8def"}`, background: e.hot ? "#fdecee" : "#eef3ff", borderRadius: 8 * u }}>
          <div style={{ fontFamily: T.body, fontWeight: 700, fontSize: 36 * u, color: T.ink }}>{e.title}</div>
          {e.note && <div style={{ fontFamily: T.body, fontSize: 28 * u, color: T.grey }}>{e.note}</div>}
        </div>
      </div>)}
    </div>
  </Frame>;
};

const GameMenu: React.FC<{ title: string; sub?: string; u: number }> = ({ title, sub, u }) =>
  <AbsoluteFill style={{ background: "linear-gradient(160deg,#2b0f3f 0%,#c2185b 45%,#ff9e40 100%)", display: "flex", flexDirection: "column", justifyContent: "center", padding: `0 ${70 * u}px` }}>
    <div style={{ fontFamily: T.head, fontWeight: 800, fontStyle: "italic", fontSize: 96 * u, lineHeight: 0.95, color: "white", textShadow: `0 ${6 * u}px ${20 * u}px rgba(0,0,0,0.4)` }}>{title}</div>
    {(sub || "STORY MODE\nONLINE\nSETTINGS").split("\n").map((x, i) => <div key={i} style={{ fontFamily: T.head, fontWeight: 700, fontSize: 40 * u, color: i === 0 ? "white" : "rgba(255,255,255,0.7)", marginTop: (i ? 10 : 50) * u }}>{x}</div>)}
  </AbsoluteFill>;

const Call: React.FC<{ s: Extract<ScreenSpec, { type: "call" }>; t: number }> = ({ s, t }) => {
  const { u, vert } = useU();
  const present = s.events.find((e) => e.kind === "present" && t >= e.at && t < e.at + (e.dur ?? 0.5));
  const stopped = s.events.find((e) => e.kind === "stopped" && t >= e.at && t < e.at + 2.2);
  const cols = vert ? 2 : Math.min(3, s.tiles.length);
  if (s.ended !== undefined && t >= s.ended) return <Frame title={s.title} dark><AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center",
    fontFamily: T.head, fontWeight: 800, fontSize: 56 * u, color: "#c9d1e6" }}>You left the meeting</AbsoluteFill></Frame>;
  return <Frame title={s.title} dark>
    {present ? <GameMenu title={present.text || "GRAND THEFT AUTO VI"} u={u} /> :
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 18 * u, padding: 24 * u, height: "100%", boxSizing: "border-box" }}>
        {s.tiles.map((tl) => {
          const ev = [...s.events].reverse().find((e) => e.who === tl.name && t >= e.at);
          const away = tl.state === "away" || (ev && ev.kind === "away");
          const thumbs = s.events.find((e) => e.who === tl.name && e.kind === "thumbs" && t >= e.at && t < e.at + 2);
          const talk = s.events.find((e) => e.who === tl.name && e.kind === "talk" && t >= e.at && t < e.at + (e.dur ?? 1.5));
          return <div key={tl.name} style={{ position: "relative", background: "#0a0e1a", borderRadius: 16 * u, outline: talk ? `${5 * u}px solid #28c840` : "none",
            display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ width: 120 * u, height: 120 * u, borderRadius: 60 * u, background: "#2a3350", display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: T.head, fontWeight: 800, fontSize: 40 * u, color: "#c9d1e6" }}>{tl.name[0]}</div>
            <div style={{ position: "absolute", left: 18 * u, bottom: 14 * u, fontFamily: T.body, fontWeight: 600, fontSize: 30 * u, color: "white" }}>
              {tl.name}{away ? "  · Away" : ""}  <span style={{ color: "#ff6b6b", fontSize: 24 * u }}>● muted</span></div>
            {thumbs && <div style={{ position: "absolute", top: 20 * u, right: 24 * u, fontSize: 70 * u, opacity: fadeIn(t, thumbs.at, 0.2),
              transform: `translateY(${-interpolate(t, [thumbs.at, thumbs.at + 2], [0, 60]) * u}px)` }}>👍</div>}
          </div>;
        })}
      </div>}
    {stopped && <div style={{ position: "absolute", left: "50%", top: 30 * u, transform: "translateX(-50%)", background: "rgba(0,0,0,0.75)", padding: `${12 * u}px ${28 * u}px`,
      borderRadius: 12 * u, fontFamily: T.body, fontWeight: 600, fontSize: 32 * u, color: "white" }}>{stopped.who} stopped sharing</div>}
    {present && <div style={{ position: "absolute", left: "50%", top: 30 * u, transform: "translateX(-50%)", background: "rgba(0,0,0,0.75)", padding: `${12 * u}px ${28 * u}px`,
      borderRadius: 12 * u, fontFamily: T.body, fontWeight: 600, fontSize: 32 * u, color: "white" }}>{present.who} is presenting</div>}
  </Frame>;
};

const Form: React.FC<{ s: Extract<ScreenSpec, { type: "form" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  const res = s.result && t >= s.result.at;
  return <Frame title={s.title} phone>
    <div style={{ padding: `${40 * u}px ${44 * u}px` }}>
      {s.fields.map((f, i) => {
        const n = Math.floor(interpolate(t, [f.at, f.at + 0.06 * f.value.length + 0.1], [0, f.value.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
        return <div key={i} style={{ marginBottom: 30 * u }}>
          <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 30 * u, color: T.grey }}>{f.label}</div>
          <div style={{ marginTop: 8 * u, padding: `${18 * u}px ${20 * u}px`, border: `${3 * u}px solid #d6d3cc`, borderRadius: 12 * u, fontFamily: T.body, fontSize: 40 * u, color: T.ink, minHeight: 50 * u }}>
            {f.value.slice(0, Math.max(0, n))}{t >= f.at && n < f.value.length ? "|" : ""}</div>
        </div>;
      })}
      {s.submitAt !== undefined && <div style={{ marginTop: 20 * u, padding: `${20 * u}px`, textAlign: "center", borderRadius: 14 * u,
        background: t >= s.submitAt ? "#9aa8c6" : "#3b5bdb", fontFamily: T.body, fontWeight: 700, fontSize: 40 * u, color: "white" }}>Submit request</div>}
      {res && <div style={{ marginTop: 34 * u, padding: `${26 * u}px ${28 * u}px`, borderRadius: 14 * u, opacity: fadeIn(t, s.result!.at, 0.25),
        background: s.result!.ok ? "#e7f6ea" : "#fdecee", borderLeft: `${10 * u}px solid ${s.result!.ok ? "#28a745" : T.red}`,
        fontFamily: T.body, fontWeight: 600, fontSize: 38 * u, lineHeight: 1.35, color: T.ink, whiteSpace: "pre-line" }}>{s.result!.text}</div>}
    </div>
  </Frame>;
};

const Phone: React.FC<{ s: Extract<ScreenSpec, { type: "phone" }>; t: number }> = ({ s, t }) => {
  const { W, H, u, vert } = useU();
  const pw = vert ? W * 0.84 : H * 0.5, ph = vert ? H * 0.82 : H * 0.94;
  return <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #3a4258 0%, #10131c 100%)" }}>
    <div style={{ position: "absolute", left: (W - pw) / 2, top: (H - ph) / 2, width: pw, height: ph, borderRadius: 70 * u, border: `${14 * u}px solid #05070c`,
      background: "linear-gradient(170deg,#24324f 0%,#5b4a7a 60%,#b46a6a 100%)", overflow: "hidden", boxShadow: `0 ${30 * u}px ${80 * u}px rgba(0,0,0,0.5)` }}>
      {!s.thread && <div style={{ textAlign: "center", marginTop: 110 * u, color: "white" }}>
        <div style={{ fontFamily: T.body, fontWeight: 500, fontSize: 34 * u, opacity: 0.85 }}>{s.date || "Thursday 19 November"}</div>
        <div style={{ fontFamily: T.head, fontWeight: 700, fontSize: 170 * u, lineHeight: 1 }}>{s.clock}</div>
      </div>}
      {s.alarm && <div style={{ margin: `${60 * u}px ${36 * u}px 0`, padding: `${26 * u}px ${30 * u}px`, borderRadius: 30 * u, background: "rgba(255,255,255,0.85)" }}>
        <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 28 * u, color: T.grey }}>⏰ Alarm · {s.alarm.time}</div>
        <div style={{ fontFamily: T.body, fontWeight: 800, fontSize: 44 * u, color: T.ink, marginTop: 6 * u }}>{s.alarm.label}</div>
      </div>}
      {(s.notes || []).filter((n) => t >= n.at).map((n, i) => <div key={i} style={{ margin: `${24 * u}px ${30 * u}px 0`, padding: `${22 * u}px ${28 * u}px`,
        borderRadius: 30 * u, background: "rgba(255,255,255,0.9)", opacity: fadeIn(t, n.at, 0.25), transform: `translateY(${(1 - fadeIn(t, n.at, 0.25)) * -30 * u}px)` }}>
        <div style={{ fontFamily: T.body, fontWeight: 600, fontSize: 26 * u, color: T.grey }}>{n.app.toUpperCase()} · now</div>
        <div style={{ fontFamily: T.body, fontWeight: 800, fontSize: 38 * u, color: T.ink, marginTop: 4 * u }}>{n.title}</div>
        <div style={{ fontFamily: T.body, fontSize: 34 * u, color: "#333", marginTop: 4 * u, lineHeight: 1.3 }}>{n.text}</div>
      </div>)}
      {s.thread && <div style={{ position: "absolute", inset: 0, background: "#f2f2f7" }}>
        <div style={{ padding: `${70 * u}px 0 ${24 * u}px`, textAlign: "center", background: "#e9e9ef", fontFamily: T.body, fontWeight: 700, fontSize: 40 * u, color: T.ink }}>{s.thread.who}</div>
        <div style={{ padding: `${20 * u}px ${30 * u}px` }}>
          {s.thread.messages.filter((m) => t >= m.at).map((m, i) => {
            const n = m.mine ? Math.floor(interpolate(t, [m.at, m.at + 0.05 * m.text.length], [0, m.text.length], { extrapolateRight: "clamp" })) : m.text.length;
            return <div key={i} style={{ display: "flex", justifyContent: m.mine ? "flex-end" : "flex-start", marginTop: 18 * u }}>
              <div style={{ maxWidth: "78%", padding: `${18 * u}px ${26 * u}px`, borderRadius: 34 * u, background: m.mine ? "#2f7cf6" : "white",
                color: m.mine ? "white" : T.ink, fontFamily: T.body, fontSize: 38 * u, lineHeight: 1.3 }}>{m.text.slice(0, n)}</div>
            </div>;
          })}
          {s.thread.typing && t >= s.thread.typing.at && t < s.thread.typing.end && <div style={{ display: "flex", marginTop: 18 * u }}>
            <div style={{ padding: `${20 * u}px ${30 * u}px`, borderRadius: 34 * u, background: "white", fontSize: 40 * u, letterSpacing: 6 * u, color: "#999" }}>
              {"•••".slice(0, 1 + (Math.floor(t * 3) % 3))}</div></div>}
        </div>
      </div>}
    </div>
  </AbsoluteFill>;
};

const Card: React.FC<{ s: Extract<ScreenSpec, { type: "card" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  return <AbsoluteFill style={{ background: s.dark === false ? T.paper : "#0b0f1a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: `0 ${80 * u}px` }}>
    {s.lines.filter((l) => shown(t, l.at)).map((l, i) => <div key={i} style={{ fontFamily: T.head, fontWeight: 800, fontSize: (l.size ?? 70) * u, lineHeight: 1.12,
      color: l.color || (s.dark === false ? T.navy : "white"), textAlign: "center", marginTop: (i ? 30 : 0) * u, opacity: fadeIn(t, l.at ?? 0, 0.4),
      transform: `translateY(${(1 - fadeIn(t, l.at ?? 0, 0.4)) * 20 * u}px)` }}>{l.text}</div>)}
  </AbsoluteFill>;
};


/** a physical control in close-up: lift panel, crossing box, thermostat or a big red button. `presses` = seconds when it is pressed
 *  (the hot button flashes and dips); `reading` = what its display shows over time. */
const Panel: React.FC<{ s: Extract<ScreenSpec, { type: "panel" }>; t: number }> = ({ s, t }) => {
  const { W, H, u, vert } = useU();
  const pressed = (s.presses || []).some((p) => t >= p && t < p + 0.18);
  const n = (s.presses || []).filter((p) => t >= p).length;
  const read = [...(s.reading || [])].reverse().find((r) => t >= r.at);
  const style = s.style || "lift";
  const bg = style === "crossing" ? "radial-gradient(ellipse at 50% 40%, #9aa3ad 0%, #4e5660 100%)" : style === "red" ? "radial-gradient(ellipse at 50% 40%, #8a6f55 0%, #4a3826 100%)"
    : "radial-gradient(ellipse at 50% 40%, #c9ccd1 0%, #7d828a 100%)";
  const btn = (label: string, hot: boolean, i: number) => {
    const dip = hot && pressed;
    const sz = (style === "red" ? 360 : 170) * u;
    return <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 * u }}>
      <div style={{ width: sz, height: sz, borderRadius: sz / 2, display: "flex", alignItems: "center", justifyContent: "center",
        background: style === "red" ? (dip ? "#a01818" : "radial-gradient(circle at 40% 35%, #ff6b6b, #c41e1e)") : dip ? "#ffd166" : "linear-gradient(160deg,#f4f5f7,#b9bec6)",
        boxShadow: dip ? `inset 0 ${6 * u}px ${14 * u}px rgba(0,0,0,0.35)` : `0 ${10 * u}px ${24 * u}px rgba(0,0,0,0.35)`, transform: `scale(${dip ? 0.94 : 1})`,
        border: `${6 * u}px solid ${hot && style !== "red" ? "#ffd166" : "rgba(0,0,0,0.15)"}`, fontFamily: T.head, fontWeight: 800,
        fontSize: (style === "red" ? 44 : 34) * u, color: style === "red" ? "white" : "#2b2f36", textAlign: "center", lineHeight: 1.05, padding: 10 * u }}>
        {label}</div>
    </div>;
  };
  return <AbsoluteFill style={{ background: bg, display: "flex", alignItems: "center", justifyContent: "center" }}>
    <div style={{ padding: 60 * u, borderRadius: 30 * u, background: style === "red" ? "transparent" : style === "crossing" ? "#f2c230" : "linear-gradient(160deg,#e3e5e8,#a9aeb6)",
      boxShadow: style === "red" ? "none" : `0 ${20 * u}px ${60 * u}px rgba(0,0,0,0.35)`, display: "flex", flexDirection: vert || style === "lift" ? "column" : "row",
      alignItems: "center", gap: 40 * u, marginTop: vert ? -H * 0.05 : 0 }}>
      {style === "crossing" && <div style={{ padding: `${14 * u}px ${30 * u}px`, borderRadius: 12 * u, background: "#111", fontFamily: T.head, fontWeight: 800,
        fontSize: 56 * u, color: n > 0 ? "#ff9f43" : "#3a3a3a", letterSpacing: 6 * u }}>WAIT</div>}
      {style === "thermostat" && <div style={{ width: 300 * u, height: 300 * u, borderRadius: 150 * u, background: "#1d2127", display: "flex", alignItems: "center",
        justifyContent: "center", fontFamily: T.head, fontWeight: 800, fontSize: 110 * u, color: "#7ee0ff" }}>{read ? read.text : "21°"}</div>}
      {style !== "thermostat" && <div style={{ display: "flex", flexDirection: style === "lift" && !vert ? "row" : "column", gap: 40 * u }}>
        {(s.buttons || []).map((b, i) => btn(b.label, !!b.hot, i))}</div>}
    </div>
    {s.caption && <div style={{ position: "absolute", left: 40 * u, right: 40 * u, top: vert ? H * 0.13 : H * 0.84, textAlign: "center", fontFamily: T.body, fontWeight: 700,
      fontSize: 40 * u, color: "white", textShadow: "0 2px 10px rgba(0,0,0,0.6)" }}>{s.caption}</div>}
    {(s.presses || []).length > 0 && style !== "red" && <div style={{ position: "absolute", right: vert ? 40 * u : 70 * u, top: vert ? (s.caption ? H * 0.27 : H * 0.16) : 60 * u,
      padding: `${10 * u}px ${22 * u}px`, borderRadius: 12 * u, background: "rgba(10,14,26,0.85)", fontFamily: T.head, fontWeight: 800, fontSize: 40 * u, color: "#ffd166" }}>
      PRESSES: {n}</div>}
  </AbsoluteFill>;
};

const Spinner: React.FC<{ s: Extract<ScreenSpec, { type: "spinner" }>; t: number }> = ({ s, t }) => {
  const { u } = useU();
  return <Frame title="TravelSearch" phone>
    <AbsoluteFill style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 40 * u }}>
      <div style={{ width: 200 * u, height: 200 * u, borderRadius: 100 * u, border: `${16 * u}px solid #e6ecf5`, borderTopColor: "#3b5bdb", transform: `rotate(${t * 360}deg)` }} />
      <div style={{ fontFamily: T.body, fontWeight: 700, fontSize: 44 * u, color: T.ink, textAlign: "center", padding: `0 ${40 * u}px` }}>{s.text}</div>
      {s.sub && <div style={{ fontFamily: T.body, fontSize: 32 * u, color: T.grey }}>{s.sub}</div>}
    </AbsoluteFill>
  </Frame>;
};

export const ScreenInsert: React.FC<{ s: ScreenSpec }> = ({ s }) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H } = useVideoConfig();
  const t = frame / fps, u = H > W ? W / 1080 : W / 1920;
  switch (s.type) {
    case "desktop": return <Desktop s={s} t={t} />;
    case "slide": return <Slide s={s} t={t} />;
    case "notepad": return <Notepad s={s} t={t} />;
    case "download": return <Download s={s} t={t} />;
    case "chat": return <Chat s={s} t={t} />;
    case "email": return <Email s={s} t={t} />;
    case "calendar": return <Calendar s={s} t={t} />;
    case "call": return <Call s={s} t={t} />;
    case "form": return <Form s={s} t={t} />;
    case "phone": return <Phone s={s} t={t} />;
    case "card": return <Card s={s} t={t} />;
    case "game": return <GameMenu title={s.title} sub={s.sub} u={u} />;
    case "panel": return <Panel s={s} t={t} />;
    case "spinner": return <Spinner s={s} t={t} />;
  }
  return null;
};

/** caption text pinned to the top of the frame (reel hooks, time stamps like "6:01 AM") */
export const TopText: React.FC<{ items: TimedText[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H } = useVideoConfig();
  const t = frame / fps, vert = H > W, u = vert ? W / 1080 : W / 1920;
  const cur = items.filter((x) => t >= (x.at ?? 0) && (x.until === undefined || t < x.until)).pop();
  if (!cur) return null;
  const a = fadeIn(t, cur.at ?? 0, 0.3);
  return <div style={{ position: "absolute", top: vert ? H * 0.07 : 50 * u, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: a }}>
    <div style={{ maxWidth: W * 0.88, padding: `${16 * u}px ${30 * u}px`, background: "rgba(10,14,26,0.82)", borderRadius: 12 * u, textAlign: "center",
      fontFamily: T.head, fontWeight: 800, fontSize: (vert ? 54 : 46) * u, lineHeight: 1.2, color: "white" }}>{cur.text}</div>
  </div>;
};
