export type Viseme = { start: number; end: number; value: string }; // seconds (scene time), Rhubarb A-H / X
export type Box = { x: number; y: number; w: number; h: number }; // fractions of the pose image (0..1)

export type PoseImg = { img: string; w: number; h: number; mouth: Box | null; eyes: Box[]; skin: string; eyeSkin: string; talk?: { mid: string; open: string } | null };

export type CastMember = {
  char: string;
  position: "left" | "center" | "right";
  x?: number | null;               // exact horizontal position (fraction of width) chosen by QC grounding fixes
  poses: Record<string, PoseImg>; // every pose this character uses in the scene
  color: string;                  // speaker colour (captions)
};

export type Line = {
  speaker: string; start: number; end: number; text: string;
  pose: string; emotion: string; shot: "wide" | "two_shot" | "closeup" | "detail";
  visemes: Viseme[];
};

export type Word = { text: string; startMs: number; endMs: number; speaker: string; emph: boolean };
export type Beat = { atMs: number; type: "keyword" | "number" | "label"; text: string };

export type Place = { name: string; lat: number; lon: number; atMs: number };
export type Route = { from: string; to: string; via: string[]; label: string; icon: string; blocked: boolean; atMs: number; color: string };

export type SceneProps = {
  id: string;
  kind: "stage" | "map" | "title_card" | "chart" | "hero";
  durationInFrames: number;
  background: string | null;
  cast: CastMember[];
  lines: Line[];
  words: Word[];
  beats: Beat[];
  titleText: string;
  chapter: number;
  map: { label: string; countries: { name: string; atMs: number }[]; places: Place[]; routes: Route[] } | null;
  chart: { labels: string[]; values: number[]; unit: string; title: string; mode?: "bars" | "stats" | "timeline"; items?: { value: string; label: string }[] } | null;
  heroVideo: string | null;
  heroRate: number;
  accent: string;
  speakerColors: Record<string, string>;
  names?: Record<string, { name: string; role: string }>;   // lower-third name tags
  introduce?: string[];                                       // characters whose first appearance in the video is this scene
  sources?: string;                                           // e.g. "AP · Wikipedia" (shown on maps/charts)
  brand?: string;
  shots?: { video: string; start: number; end: number }[] | null;   // animated talking shots (replace the cut-out cast)                                             // channel bug, top right ("" = none)
};
