"""Render one MiniMax-H3 shot by hand (bake-offs, debugging). Production uses studio.h3 via the pipeline.

  python tools/h3_run.py --keyframe kf.png --audio line.wav --ref a.png --ref b.png --prompt-file p.txt \
      --out shot.mp4 [--mode flex|base] [--size 864x480] [--seconds 5] [--seed 7] [--guide-clip last5.mp4]
"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from studio import h3

p = argparse.ArgumentParser()
p.add_argument("--keyframe", required=True); p.add_argument("--audio", required=True)
p.add_argument("--ref", action="append", default=[], help="identity references (the keyframe is always <Picture 1>)")
p.add_argument("--prompt-file", required=True); p.add_argument("--out", required=True)
p.add_argument("--mode", default="flex", choices=["flex", "base"]); p.add_argument("--size", default="864x480")
p.add_argument("--seconds", type=float, default=5.0); p.add_argument("--seed", type=int, default=7)
p.add_argument("--steps", type=int, default=14)
p.add_argument("--guide-clip", help="previous shot's last 5 frames, to continue a take")
p.add_argument("--no-audio-anchor", action="store_true")
a = p.parse_args()
t0 = time.time()
r = h3.render(a.out, keyframe=a.keyframe, refs=[x for x in a.ref if x != a.keyframe], audio=a.audio,
              prompt=open(a.prompt_file).read(), size=tuple(map(int, a.size.split("x"))), seconds=a.seconds, seed=a.seed,
              mode=a.mode, guide_clip=a.guide_clip, steps=a.steps, anchor_audio=not a.no_audio_anchor)
print(json.dumps({"out": a.out, "wall_s": round(time.time() - t0, 1), **r, "mode": a.mode, "size": a.size,
                  "frames": h3.frames_for(a.seconds), "seed": a.seed}))
