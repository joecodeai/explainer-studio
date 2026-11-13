import React, { useMemo } from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { geoNaturalEarth1, geoPath, geoCentroid, geoInterpolate } from "d3-geo";
import { feature } from "topojson-client";
// @ts-ignore
import world from "world-atlas/countries-50m.json";
import { Place, Route } from "./types";
import { T as TH } from "./theme";

const PALETTE = ["#d62839", "#1c2b44", "#4f6d8f", "#c98a2b", "#7a8f6a", "#8a3b4a", "#5b5f97"];
const ALIAS: Record<string, string> = {
  usa: "united states of america", us: "united states of america", "united states": "united states of america", america: "united states of america",
  uk: "united kingdom", britain: "united kingdom", "great britain": "united kingdom", england: "united kingdom",
  drc: "dem. rep. congo", "democratic republic of the congo": "dem. rep. congo", "czech republic": "czechia",
  "ivory coast": "côte d'ivoire", uae: "united arab emirates", "the netherlands": "netherlands", holland: "netherlands",
};
const all = (feature(world as any, (world as any).objects.countries) as any).features as any[];
const find = (n: string) => {
  const k = ALIAS[n.toLowerCase().trim()] ?? n.toLowerCase().trim();
  return all.find((f) => f.properties.name.toLowerCase() === k) ?? all.find((f) => f.properties.name.toLowerCase().includes(k));
};

const ICON: Record<string, (c: string) => React.ReactNode> = {
  ship: (c) => <g><path d="M-26,2 L26,2 L18,16 L-18,16 Z" fill={c} stroke="#111" strokeWidth={3} /><rect x={-12} y={-12} width={20} height={14} fill="#fff" stroke="#111" strokeWidth={3} /><rect x={-4} y={-22} width={6} height={10} fill="#111" /></g>,
  plane: (c) => <g><path d="M-28,0 L28,0 M-6,-20 L6,0 L-6,20 M-24,-8 L-20,0 L-24,8" stroke="#111" strokeWidth={9} fill="none" strokeLinecap="round" /><path d="M-28,0 L28,0 M-6,-20 L6,0 L-6,20" stroke={c} strokeWidth={5} fill="none" strokeLinecap="round" /></g>,
  truck: (c) => <g><rect x={-26} y={-14} width={34} height={24} fill={c} stroke="#111" strokeWidth={3} /><rect x={8} y={-6} width={16} height={16} fill="#fff" stroke="#111" strokeWidth={3} /><circle cx={-16} cy={12} r={6} fill="#111" /><circle cx={14} cy={12} r={6} fill="#111" /></g>,
  money: (c) => <g><circle r={20} fill="#f3c623" stroke="#111" strokeWidth={4} /><text y={10} textAnchor="middle" fontFamily="Montserrat" fontWeight={800} fontSize={26} fill="#111">$</text></g>,
};

type MapData = { label: string; countries: { name: string; atMs: number }[]; places: Place[]; routes: Route[] };

export const MapScene: React.FC<{ map: MapData; accent: string }> = ({ map, accent }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const proj = useMemo(() => geoNaturalEarth1().fitExtent([[0, 0], [width, height]], { type: "Sphere" } as any), [width, height]);
  const path = geoPath(proj);
  const hl = useMemo(() => map.countries.map((c) => ({ f: find(c.name), atMs: c.atMs })).filter((x) => x.f), [map]);
  const P = useMemo(() => Object.fromEntries(map.places.map((p) => [p.name, p])), [map]);

  // camera: bbox of highlighted countries' centroids (+ their size) and all places
  const cam = useMemo(() => {
    const pts: [number, number, number][] = [];
    for (const { f } of hl) { const c = proj(geoCentroid(f)); if (c) pts.push([c[0], c[1], Math.min(Math.sqrt(path.area(f)) * 0.7, width * 0.22)]); }
    for (const p of map.places) { const c = proj([p.lon, p.lat]); if (c) pts.push([c[0], c[1], 40]); }
    if (!pts.length) return { k: 1, cx: width / 2, cy: height / 2 };
    const x0 = Math.min(...pts.map((p) => p[0] - p[2])), x1 = Math.max(...pts.map((p) => p[0] + p[2]));
    const y0 = Math.min(...pts.map((p) => p[1] - p[2])), y1 = Math.max(...pts.map((p) => p[1] + p[2]));
    const k = Math.max(1, Math.min(9, Math.min((width * 0.72) / Math.max(40, x1 - x0), (height * 0.6) / Math.max(40, y1 - y0))));
    return { k, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 };
  }, [hl, map, proj, width, height]);
  const z = interpolate(frame, [0, fps * 1.1], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const drift = interpolate(frame, [fps * 1.1, durationInFrames], [1, 1.06], { extrapolateLeft: "clamp" });
  // zoom straight INTO the target (it grows from where it sits on the world map) — never sweeps across other regions
  const kz = Math.pow(cam.k, z), u = cam.k > 1.001 ? (kz - 1) / (cam.k - 1) : 1;
  const tx = cam.cx + (width / 2 - cam.cx) * u, ty = cam.cy + (height / 2 - cam.cy) * u;   // target's screen position
  const k = kz * drift;
  const cx = cam.cx - (tx - width / 2) / kz, cy = cam.cy - (ty - height / 2) / kz;
  const T = (x: number, y: number): [number, number] => [(x - cx) * k + width / 2, (y - cy) * k + height / 2 + 20];
  const at = (lon: number, lat: number) => { const p = proj([lon, lat]); return p ? T(p[0], p[1]) : [0, 0] as [number, number]; };
  const tf = `translate(${width / 2} ${height / 2 + 20}) scale(${k}) translate(${-cx} ${-cy})`;

  // label layout: every label (cities first, then countries, then route labels) gets the nearest free spot that does not
  // overlap another label, a city dot or the map title, and stays inside the frame above the subtitle area
  const boxes: { x: number; y: number; w: number; h: number }[] = [];
  if (map.label) { const w = map.label.length * 52 * 0.66 + 80; boxes.push({ x: 70 + w / 2, y: 92, w, h: 100 }); }
  map.places.forEach((pl) => { const [x, y] = at(pl.lon, pl.lat); boxes.push({ x, y, w: 36, h: 36 }); });
  const place = (x: number, y: number, text: string, size: number) => {
    const w = text.length * size * 0.55 + 20, h = size * 1.15;
    const offs: [number, number][] = [[0, 0]];
    for (let r = 1; r <= 6; r++) offs.push([0, -r], [0, r], [r * 0.5, 0], [-r * 0.5, 0], [r * 0.5, -r], [-r * 0.5, -r], [r * 0.5, r], [-r * 0.5, r]);
    let best: [number, number] = [x, y];
    for (const [ox, oy] of offs) {
      const bx = Math.min(Math.max(x + ox * w, w / 2 + 16), width - w / 2 - 16);
      const by = Math.min(Math.max(y + oy * h, 150 + h / 2), height - 170);
      const cyy = by - size * 0.35;
      if (!boxes.some((b) => Math.abs(b.x - bx) < (b.w + w) / 2 && Math.abs(b.y - cyy) < (b.h + h) / 2)) { best = [bx, by]; break; }
    }
    boxes.push({ x: best[0], y: best[1] - size * 0.35, w, h }); return best;
  };
  const placeLabel = map.places.map((pl) => { const [x, y] = at(pl.lon, pl.lat); const [bx, by] = place(x, y - 30, pl.name, 36); return [bx - x, by - y] as [number, number]; });
  const labels = hl.map(({ f }) => { const c = proj(geoCentroid(f)) ?? [0, 0]; const [x, y] = T(c[0], c[1]); return place(x, y, f.properties.name, 44); });

  const routeGeo = (r: Route) => {
    const stops = [r.from, ...r.via, r.to].map((n) => P[n]).filter(Boolean);
    const pts: [number, number][] = [];
    for (let i = 0; i < stops.length - 1; i++) {
      const it = geoInterpolate([stops[i].lon, stops[i].lat], [stops[i + 1].lon, stops[i + 1].lat]);
      for (let s = 0; s <= 40; s++) { const g = it(s / 40); pts.push(at(g[0], g[1])); }
    }
    return pts;
  };

  return (
    <div style={{ position: "absolute", inset: 0, background: "#d9e3ec" }}>
      <svg width={width} height={height}>
        <rect width={width} height={height} fill="#d9e3ec" />
        <g transform={tf}>
          {all.map((f, i) => <path key={i} d={path(f) ?? ""} fill="#f7f5f0" stroke="#aaa497" strokeWidth={1} vectorEffect="non-scaling-stroke" />)}
          {hl.map(({ f, atMs }, i) => {
            const p = spring({ frame: frame - Math.round((atMs / 1000) * fps), fps, config: { damping: 12 } });
            return <path key={"h" + i} d={path(f) ?? ""} fill={PALETTE[i % PALETTE.length]} fillOpacity={0.85 * p} stroke="#ffffff" strokeWidth={2} vectorEffect="non-scaling-stroke" />;
          })}
        </g>
        {map.routes.map((r, i) => {
          const pts = routeGeo(r); if (pts.length < 2) return null;
          const d = "M" + pts.map((p) => p.join(",")).join(" L");
          let len = 0; for (let j = 1; j < pts.length; j++) len += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]);
          const t0 = r.atMs / 1000;
          const draw = interpolate(frame / fps, [t0, t0 + 1.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) });
          const color = r.blocked ? "#d62828" : r.color;
          // icon travels along the drawn route and loops
          const loop = ((frame / fps - t0 - 1.6) / 3.5) % 1;
          const u = draw < 1 ? draw : (r.blocked ? 0.5 : loop < 0 ? 0 : loop);
          const idx = Math.min(pts.length - 2, Math.floor(u * (pts.length - 1)));
          const [ix, iy] = pts[idx], [jx, jy] = pts[idx + 1];
          const ang = Math.atan2(jy - iy, jx - ix) * 180 / Math.PI;
          const mid = pts[Math.floor(pts.length / 2)];
          const lab = pts[Math.floor(pts.length * 0.32)];
          const labP = r.label ? place(lab[0], lab[1] - 34, r.label, 38) : [lab[0], 0];
          return <g key={"r" + i} opacity={draw > 0 ? 1 : 0}>
            <path d={d} fill="none" stroke="#111" strokeWidth={13} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - draw)} opacity={0.35} />
            <path d={d} fill="none" stroke={color} strokeWidth={8} strokeLinecap="round" strokeDasharray={r.blocked ? "18 14" : `${len}`} strokeDashoffset={r.blocked ? 0 : len * (1 - draw)} />
            {r.icon !== "none" && ICON[r.icon] && draw > 0.02 && <g transform={`translate(${ix},${iy}) rotate(${r.icon === "money" ? 0 : ang})`}>{ICON[r.icon](color)}</g>}
            {r.blocked && draw > 0.9 && <g transform={`translate(${mid[0]},${mid[1]}) scale(${spring({ frame: frame - Math.round((t0 + 1.6) * fps), fps })})`}>
              <circle r={34} fill="#fff" stroke="#d62828" strokeWidth={8} /><path d="M-16,-16 L16,16 M16,-16 L-16,16" stroke="#d62828" strokeWidth={9} strokeLinecap="round" /></g>}
            {r.label && draw > 0.6 && <text x={labP[0]} y={labP[1]} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={38}
              fill={color} stroke="#fff" strokeWidth={9} paintOrder="stroke">{r.label}</text>}
          </g>;
        })}
        {hl.map(({ f, atMs }, i) => {
          const p = spring({ frame: frame - Math.round((atMs / 1000) * fps) - 4, fps });
          return <text key={"t" + i} x={labels[i][0]} y={labels[i][1]} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={40}
            fill={TH.navy} stroke="#fff" strokeWidth={8} paintOrder="stroke" opacity={p} letterSpacing={1}>{f.properties.name.toUpperCase()}</text>;
        })}
        {map.places.map((pl, i) => {
          const [x, y] = at(pl.lon, pl.lat);
          const p = spring({ frame: frame - Math.round((pl.atMs / 1000) * fps), fps, config: { damping: 10 } });
          return <g key={"p" + i} transform={`translate(${x},${y})`} opacity={p}>
            <circle r={11 * p} fill={TH.red} stroke="#fff" strokeWidth={4} />
            <circle r={11 + 22 * ((frame / fps * 0.8 + i * 0.3) % 1)} fill="none" stroke={TH.red} strokeWidth={3} opacity={1 - ((frame / fps * 0.8 + i * 0.3) % 1)} />
            <text x={placeLabel[i][0]} y={placeLabel[i][1]} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={34} fill={TH.ink} stroke="#fff" strokeWidth={8} paintOrder="stroke">{pl.name}</text>
          </g>;
        })}
      </svg>
      {map.label && <div style={{ position: "absolute", top: 50, left: 70, background: "rgba(255,255,255,0.96)", borderLeft: `10px solid ${TH.red}`,
        padding: "12px 28px 14px", boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
        clipPath: `inset(0 ${(1 - interpolate(frame, [0, 14], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(...TH.ease) })) * 100}% 0 0)` }}>
        <div style={{ fontFamily: TH.head, fontWeight: 800, fontSize: 52, color: TH.navy, textTransform: "uppercase", letterSpacing: 0.5 }}>{map.label}</div></div>}
      {map.routes.length > 1 && <div style={{ position: "absolute", left: 60, bottom: 200, background: "rgba(255,255,255,0.95)", borderLeft: `8px solid ${TH.navy}`,
        padding: "14px 22px", fontFamily: TH.body, fontWeight: 600, fontSize: 28, color: TH.ink, boxShadow: "0 8px 24px rgba(0,0,0,0.15)" }}>
        {map.routes.map((r, i) => <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, opacity: ms > r.atMs ? 1 : 0.25 }}>
          <div style={{ width: 44, height: 8, background: r.blocked ? "#d62828" : r.color, borderRadius: 4 }} />{r.label || `${r.from} → ${r.to}`}{r.blocked ? " ✕" : ""}</div>)}
      </div>}
    </div>
  );
};
