"""Bat-bomb animation test, stage B: animate the chosen keyframes into real moving clips.

Environment/FX shots -> LTX-2.5 image-to-video. Character-acting shots -> MiniMax H3 (keyframe + identity refs) AND LTX,
so the two engines can be compared on the same shot. Then a QC contact sheet (12 frames) per clip.

Chosen keyframes are keyframes/<shot>.png (copied by hand after review).
  PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1 .venv/bin/python tools/anim_test/batbomb_animate.py [--only t1,t3] [--seed 11]
"""
import argparse, os, random, shutil, subprocess, sys, wave
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from studio import comfy, h3, workflows as W
from studio.hero import NEG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "projects", "batbomb-animtest")
REF, KF, CL, QC = (os.path.join(OUT, d) for d in ("refs", "keyframes", "clips", "qc"))

LOOK = ("2D hand-drawn animated feature film, cel-shaded characters with clean ink outlines, painted backgrounds, "
        "smooth fluid professional character animation with weight, anticipation and follow-through, cinematic camera.")

SHOTS = {
    # id: (engines, seconds, refs for H3, action prompt)
    "t1_batflight": (["ltx"], 6, [], "Millions of small bats pour continuously out of the dark cave mouth and spiral upward in a huge "
                     "twisting column into the orange and violet sunset sky, the swarm flowing and swirling like smoke, thousands of tiny "
                     "wings flickering. The camera cranes slowly upward following the column. Desert shrubs sway gently in the breeze."),
    "t2_fieser": (["h3", "ltx"], 6, ["fieser", "bat"], "The chemist in the white lab coat slowly presses the syringe plunger into the tiny "
                  "capsule on the sleepy bat's chest and lifts the syringe away. The small bat blinks awake, shakes its head, spreads its "
                  "dark wings and flutters up out of the ice tray, flying off past his shoulder. The chemist looks up after it, startled, "
                  "eyebrows raised. Locked-off camera with a slight push in. Exactly one person; he keeps the same face and lab coat."),
    "t3_tower": (["ltx"], 6, [], "Bright flames roar out of the control tower's windows and climb up the wooden tower, the glass cab "
                 "fills with fire, thick black smoke pours upward and drifts sideways in the wind, sparks and embers float, heat "
                 "shimmer. A few tiny bats flutter away. Slow dramatic push in toward the burning tower."),
    "t4_jeep": (["ltx"], 5, [], "The army jeep speeds toward the camera across the cracked white lakebed and swerves past, wheels "
                "bouncing, a long white dust plume trailing behind it, the two soldiers holding on and pointing up at the sky. The "
                "camera tracks low alongside and pans to follow the jeep as it passes."),
    "t5_rancher": (["h3", "ltx"], 6, ["rancher", "bat"], "The old rancher keeps his face turned UP toward the bat in the porch ceiling the whole time, squinting at it, "
                   "then slowly scratches his white stubble and gives one slow knowing nod while still looking up at it. Up in the gap between "
                   "the ceiling boards the small bat blinks its big eyes, twitches its ears and shifts its grip nervously, looking down at him. "
                   "The camera slowly tilts and pushes up from the rancher's upturned face to a close-up of the worried bat. Exactly one "
                   "person; he keeps the same face, hat and clothes."),
}


def silent(path, seconds):
    if not os.path.exists(path):
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\x00\x00" * int(24000 * seconds))
    return path


def ltx(image, prompt, out, seconds, seed):
    api = W.load("ltx_i2v")
    n = lambda i: f"398:{i}"
    api[n(364)]["inputs"]["text"] = f"{prompt} {LOOK} Matching ambient sound effects, no music, no speech."
    api[n(373)]["inputs"]["text"] = NEG + ", morphing, warping, melting, sliding feet, frozen still image, slideshow"
    api[n(362)]["inputs"]["value"] = int(seconds)
    api[n(361)]["inputs"]["value"] = 24
    api[n(372)]["inputs"]["value"] = 1280
    api[n(360)]["inputs"]["value"] = 704
    api[n(366)]["inputs"]["batch_size"] = 1
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(339)]["inputs"]["noise_seed"] = seed
    api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    got = comfy.run(W.prune(api), CL, os.path.basename(out)[:-4], timeout=1800)[0]
    shutil.move(got, out)


def contact(clip, n=12):
    """12 evenly spaced frames in a 4x3 grid with frame numbers, for eyeballing motion/identity/glitches."""
    os.makedirs(QC, exist_ok=True)
    out = os.path.join(QC, os.path.basename(clip)[:-4] + "_sheet.jpg")
    nf = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                             "stream=nb_read_frames", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip() or 0)
    step = max(1, nf // n)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vf",
                    f"select='not(mod(n\\,{step}))',scale=480:-1,drawtext=text='%{{n}}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=4x3",
                    "-frames:v", "1", out], check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--engine", default="", help="limit to h3 or ltx")
    a = ap.parse_args()
    os.makedirs(CL, exist_ok=True)
    jobs = [(sid, eng, *rest) for sid, (engs, *rest) in SHOTS.items() for eng in engs
            if (not a.only or sid in a.only.split(",")) and (not a.engine or eng == a.engine)]
    # LTX first (ComfyUI 8188), then free it and run H3 (8189) so the two never share VRAM
    for sid, eng, secs, refs, prompt in sorted(jobs, key=lambda j: j[1] != "ltx"):
        kf = os.path.join(KF, f"{sid}.png")
        out = os.path.join(CL, f"{sid}_{eng}_s{a.seed}.mp4")
        if os.path.exists(out):
            continue
        if eng == "ltx":
            ltx(kf, prompt, out, secs, a.seed)
        else:
            comfy.free()
            rp = [os.path.join(REF, f"{c}.png") for c in refs]
            r = h3.render(out, keyframe=kf, refs=rp, audio=silent(os.path.join(OUT, f"silent_{secs}.wav"), secs),
                          prompt=f"{prompt} {LOOK}", size=(1344, 768), seconds=secs, seed=a.seed, mode="flex")
            print("h3", r, flush=True)
        print("clip", out, "->", contact(out), flush=True)
    comfy.free(); h3.free()


if __name__ == "__main__":
    main()
