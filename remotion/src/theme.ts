// Newsroom look (2026-11-12): clean sans fonts, navy/white/red, no comic outlines or wobbly springs.
import { loadFont } from "@remotion/fonts";
// @ts-ignore
import montserrat from "./fonts/Montserrat.ttf";
// @ts-ignore
import inter from "./fonts/Inter.ttf";

loadFont({ family: "Montserrat", url: montserrat, weight: "100 900" });
loadFont({ family: "Inter", url: inter, weight: "100 900" });

export const T = {
  head: "Montserrat",      // headlines, numbers, part cards
  body: "Inter",           // captions, labels, name tags
  navy: "#0f1b2d",
  navy2: "#1c2b44",
  ink: "#111827",
  paper: "#f5f4f0",
  grey: "#6b7280",
  rule: "#d6d3cc",
  red: "#d62839",
  ease: [0.22, 1, 0.36, 1] as const,
};
