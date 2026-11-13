import React from "react";
import { Composition } from "remotion";
import { Scene } from "./Scene";
import { SceneProps } from "./types";

const demo: SceneProps = { id: "demo", kind: "title_card", durationInFrames: 90, background: null, cast: [], lines: [], words: [], beats: [],
  titleText: "HELLO WORLD", chapter: 1, map: null, chart: null, heroVideo: null, heroRate: 1, accent: "#ffd23f", speakerColors: {} };

export const Root: React.FC = () => (
  <Composition id="Scene" component={Scene as any} width={1920} height={1080} fps={30} durationInFrames={90} defaultProps={demo}
    calculateMetadata={({ props }) => ({ durationInFrames: (props as SceneProps).durationInFrames })} />
);
