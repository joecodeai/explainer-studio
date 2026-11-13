import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { CastMember, Line, PoseImg } from "./types";

// Rhubarb mouth shapes (A..H, X) as cartoon mouths in a 100x60 box
const MOUTH: Record<string, React.ReactNode> = {
  X: <path d="M27 31 Q50 35 73 31" stroke="#1a1a1a" strokeWidth={6} fill="none" strokeLinecap="round" />,
  A: <path d="M28 30 Q50 33 72 30" stroke="#1a1a1a" strokeWidth={7} fill="none" strokeLinecap="round" />,          // M B P
  B: <><path d="M24 26 Q50 22 76 26 Q50 40 24 26Z" fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} /><rect x={34} y={25} width={32} height={5} fill="#fff" /></>, // K S T
  C: <ellipse cx={50} cy={30} rx={24} ry={13} fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} />,                    // E
  D: <><ellipse cx={50} cy={30} rx={28} ry={20} fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} /><ellipse cx={50} cy={41} rx={14} ry={7} fill="#d9534f" /></>, // A
  E: <ellipse cx={50} cy={30} rx={16} ry={16} fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} />,                    // O
  F: <ellipse cx={50} cy={30} rx={9} ry={10} fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} />,                     // U W
  G: <><path d="M26 26 Q50 22 74 26 Q50 38 26 26Z" fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} /><rect x={36} y={23} width={28} height={7} fill="#fff" /></>, // F V
  H: <><ellipse cx={50} cy={30} rx={22} ry={14} fill="#3a1010" stroke="#1a1a1a" strokeWidth={5} /><ellipse cx={50} cy={25} rx={10} ry={6} fill="#d9534f" /></>, // L TH
};

export const SLOT: Record<string, number> = { left: 0.27, center: 0.5, right: 0.73 };
export const posX = (m: CastMember) => (m.x ?? SLOT[m.position]);
export const CHAR_H = 0.70; // character height as fraction of frame height
export const FEET_Y = 0.95; // feet line (fraction of frame height) — keeps feet + contact shadow in frame

// deterministic pseudo-random from a string
const rnd = (s: string, i: number) => { let h = 2166136261 ^ i; for (const c of s) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return ((h >>> 0) % 10000) / 10000; };

const pick = (m: CastMember, want: string): string =>
  m.poses[want] ? want : m.poses["talk"] ? "talk" : m.poses["neutral"] ? "neutral" : Object.keys(m.poses)[0];

/** Which pose + facing a cast member shows at time t (seconds). */
export function stateAt(m: CastMember, cast: CastMember[], lines: Line[], t: number) {
  let cur: Line | undefined = lines.find((l) => t >= l.start && t < l.end + 0.12);
  if (!cur) { // between lines: keep the previous line's state
    const prev = [...lines].reverse().find((l) => l.end <= t);
    cur = prev ?? lines[0];
  }
  const speaking = !!cur && cur.speaker === m.char && t >= cur.start && t < cur.end;
  const isSpeaker = !!cur && cur.speaker === m.char;
  const speakerMember = cast.find((c) => c.char === cur?.speaker);
  // face toward the speaker (or toward the listener when speaking); side images face RIGHT
  let target = speakerMember && speakerMember !== m ? speakerMember : cast.find((c) => c !== m);
  const faceRight = target ? posX(target) > posX(m) : m.position !== "right";
  let pose: string;
  if (isSpeaker) {
    const p = cur!.pose;
    const conversational = ["talk", "neutral", "side_talk"].includes(p) && cur!.shot === "two_shot" && cast.length > 1;
    pose = pick(m, conversational ? "side_talk" : p);
  } else if (cast.length > 1 && cur && cur.speaker !== "narrator") {
    // listener reacts to strong emotions, otherwise listens facing the speaker
    const react: Record<string, string> = { surprised: "surprised", angry: "worried", excited: "happy", sad: "worried", confused: "thinking" };
    const r = react[cur.emotion];
    pose = pick(m, r && m.poses[r] && t - cur.start > 0.6 ? r : "side_listen");
  } else {
    pose = pick(m, "neutral");
  }
  const side = pose.startsWith("side_");
  return { pose, flip: side ? !faceRight : false, speaking, line: cur, isSpeaker };
}

const PoseLayer: React.FC<{ p: PoseImg; opacity: number; speaking: boolean; viseme: string; blinking: boolean }> = ({ p, opacity, speaking, viseme, blinking }) => (
  <div style={{ position: "absolute", inset: 0, opacity }}>
    {p.talk ? (() => {
      // the painted mouth itself moves: swap closed / mid / open versions of the same drawing (never a second mouth)
      const k = !speaking ? "closed" : ["D", "E"].includes(viseme) ? "open" : ["X", "A"].includes(viseme) ? "closed" : "mid";
      return <>
        <Img src={staticFile(p.img)} style={{ position: "absolute", width: "100%", height: "100%", opacity: k === "closed" ? 1 : 0 }} />
        <Img src={staticFile(p.talk.mid)} style={{ position: "absolute", width: "100%", height: "100%", opacity: k === "mid" ? 1 : 0 }} />
        <Img src={staticFile(p.talk.open)} style={{ position: "absolute", width: "100%", height: "100%", opacity: k === "open" ? 1 : 0 }} />
      </>;
    })() : <Img src={staticFile(p.img)} style={{ width: "100%", height: "100%" }} />}
    {!p.talk && p.mouth && speaking && (() => {
      // 1) cover the painted mouth completely (sized from the DETECTED box + margin), 2) draw the animated mouth on top
      const bx = p.mouth.x, by = p.mouth.y, bw = Math.max(p.mouth.w, 0.06), bh = Math.max(p.mouth.h, 0.025);
      const cw = Math.max(bw, 0.06) * 1.3, ch = Math.max(bh * 2.2, (cw * p.w * 0.32) / p.h);   // tight: painted mouths are pre-closed
      const cx = bx + p.mouth.w / 2, cy = by + p.mouth.h / 2;
      const mw = Math.max(bw, 0.09) * 1.15, mh = (mw * p.w * 0.62) / p.h;
      return <>
        <div style={{ position: "absolute", left: `${(cx - cw / 2) * 100}%`, top: `${(cy - ch / 2) * 100}%`, width: `${cw * 100}%`, height: `${ch * 100}%`,
          background: p.skin, borderRadius: "50%", filter: "blur(1.5px)" }} />
        <svg viewBox="0 0 100 60" preserveAspectRatio="none" style={{ position: "absolute", overflow: "visible",
          left: `${(cx - mw / 2) * 100}%`, top: `${(cy - mh / 2) * 100}%`, width: `${mw * 100}%`, height: `${mh * 100}%` }}>
          {MOUTH[viseme] ?? MOUTH.X}
        </svg>
      </>;
    })()}
    {blinking && p.eyes.map((e, i) => (
      <svg key={i} viewBox="0 0 100 100" preserveAspectRatio="none" style={{ position: "absolute",
        left: `${(e.x - e.w * 0.1) * 100}%`, top: `${(e.y - e.h * 0.1) * 100}%`, width: `${e.w * 120}%`, height: `${e.h * 120}%` }}>
        <ellipse cx={50} cy={50} rx={50} ry={50} fill={p.eyeSkin || p.skin} />
        <path d="M8 55 Q50 75 92 55" stroke="#1a1a1a" strokeWidth={9} fill="none" strokeLinecap="round" />
      </svg>
    ))}
  </div>
);

export const Character: React.FC<{ m: CastMember; index: number; cast: CastMember[]; lines: Line[]; enter: boolean }> = ({ m, index, cast, lines, enter }) => {
  const frame = useCurrentFrame();
  const { fps, height, width } = useVideoConfig();
  const t = frame / fps;
  const st = stateAt(m, cast, lines, t);
  const prevSt = stateAt(m, cast, lines, Math.max(0, t - 6 / fps));
  // pose cross-fade: find when the current pose started (look back up to 0.4 s)
  let since = 0;
  for (let k = 1; k <= 12; k++) { if (stateAt(m, cast, lines, t - k / fps).pose !== st.pose) break; since = k; }
  const fadeIn = interpolate(since, [0, 2], [0, 1], { extrapolateRight: "clamp" });
  const oldPose = stateAt(m, cast, lines, t - (since + 1) / fps).pose;

  const p0 = m.poses[st.pose];
  const targetH = height * CHAR_H;
  const scale = targetH / p0.h;
  const w = p0.w * scale;
  const cx = width * posX(m);

  // acting: breathing, weight shift, talk wobble, listener nods, reaction hop on pose change
  const seed = rnd(m.char, 1) * 10;
  const breathe = 1 + Math.sin(t * 2.1 + seed) * 0.006;
  const sway = Math.sin(t * 0.7 + seed) * 0.9;
  const talk = st.speaking ? Math.sin(t * 8.5) * 1.4 : 0;
  const nodPhase = (t + seed) % 1.6;
  const nod = !st.isSpeaker && st.line && st.line.speaker !== "narrator" && nodPhase < 0.35 ? Math.sin((nodPhase / 0.35) * Math.PI) * 0.018 : 0;
  const hop = since < 8 ? Math.sin((since / 8) * Math.PI) * 5 : 0;
  const ent = enter ? spring({ frame: frame - index * 5, fps, config: { damping: 13, stiffness: 120 } }) : 1;
  const entX = (1 - ent) * (m.position === "left" ? -320 : m.position === "right" ? 320 : 0);

  // viseme for the active line
  let v = "X";
  if (st.speaking && st.line) for (const c of st.line.visemes) if (t >= c.start && t < c.end) { v = c.value; break; }
  // random blink intervals (2–5.5 s), 4 frames
  let blinking = false;
  { let tb = rnd(m.char, 7) * 2; for (let i = 0; i < 400 && tb < t + 1; i++) { if (t >= tb && t < tb + 4 / fps) { blinking = true; break; } tb += 2 + rnd(m.char, i + 11) * 3.5; } }

  const shadowW = Math.min(w * 0.85, targetH * 0.42);
  return (<>
    <div style={{ position: "absolute", left: cx - shadowW / 2 + entX, top: height * FEET_Y - shadowW * 0.07, width: shadowW, height: shadowW * 0.14,
      borderRadius: "50%", background: "radial-gradient(ellipse at center, rgba(0,0,0,0.38) 0%, rgba(0,0,0,0.18) 55%, rgba(0,0,0,0) 72%)",
      transform: `scaleX(${1 - hop / 60})` }} />
    <div style={{
      position: "absolute", left: cx - w / 2 + entX, top: height * FEET_Y - targetH - hop,
      width: w, height: targetH, transformOrigin: "50% 100%",
      transform: `rotate(${sway + talk}deg) scaleY(${breathe - nod}) scaleX(${st.flip ? -1 : 1})`,
      filter: "drop-shadow(0 6px 6px rgba(0,0,0,0.22))",
    }}>
      {fadeIn < 1 && m.poses[oldPose] && <PoseLayer p={m.poses[oldPose]} opacity={1 - fadeIn} speaking={false} viseme="X" blinking={false} />}
      <PoseLayer p={p0} opacity={fadeIn < 1 ? fadeIn : 1} speaking={st.speaking} viseme={v} blinking={blinking} />
    </div>
  </>);
};
