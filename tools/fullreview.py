"""Whole-video quality review (user's 11-point checklist). Run on EVERY finished video before delivery.

usage: python tools/fullreview.py <project_dir>

Writes <proj>/review/:
  sheet_NN.png   dense contact sheets: one frame every 2 s with timestamps (the WHOLE video, not samples)
  faces.png      camera-aware face crops of every spoken line at 3 moments (lip-sync / eyes / double mouths)
  REVIEW.md      automatic findings + the manual checklist to tick off while looking at the sheets
  review.json    machine-readable findings ("fail" = must fix before delivery)
"""
import json, os, re, subprocess, sys
import numpy as np

P = os.path.abspath(sys.argv[1]); NAME = os.path.basename(P)
VIDEO = f"{P}/{NAME}.mp4"
OUT = f"{P}/review"; os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
findings = []


def add(level, area, msg, t=None):
    findings.append({"level": level, "area": area, "t": None if t is None else round(t, 2), "msg": msg})


def ts(t): return f"{int(t // 60)}:{t % 60:04.1f}"


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


DUR = probe(VIDEO)
sc = json.load(open(f"{P}/script.json"))
_ap = f"{P}/work/all_props.json"   # every scene (render_jobs.json lists only the scenes re-rendered last time)
jobs = {p["id"]: p for p in json.load(open(_ap))} if os.path.exists(_ap) else \
       {j["props"]["id"]: j["props"] for j in json.load(open(f"{P}/work/render_jobs.json"))["jobs"]}

# ---------- scene start times (same xfade maths as pipeline.assemble_video) ----------
XF = {"slide": 0.45, "zoom": 0.5, "wipe": 0.45, "whip": 0.3, "fade": 0.5, "cut": 0.04}
starts, prev = {}, None
for s in sc["scenes"]:
    d = probe(f"{P}/renders/{s['id']}.mp4")
    starts[s["id"]] = 0.0 if prev is None else starts[prev[0]] + prev[1] - XF.get(s.get("transition", "cut"), 0.04)
    prev = (s["id"], d)

# ---------- 1. dense contact sheets (every 2 s, whole video) ----------
for f in os.listdir(OUT):
    if f.startswith("sheet_"): os.remove(os.path.join(OUT, f))
per = 30  # 6 x 5 tiles per sheet
n_sheets = int(DUR // (2 * per)) + 1
for k in range(n_sheets):
    t0 = k * 2 * per
    if t0 >= DUR: break
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", str(2 * per), "-i", VIDEO, "-vf",
                    f"fps=1/2,scale=384:216,drawtext=text='%{{pts\\:hms\\:{t0}}}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=6x5",
                    "-frames:v", "1", f"{OUT}/sheet_{k + 1:02d}.png"], check=False)

# ---------- 2. frame-level checks: blank/flat frames, single-frame glitches, freezes ----------
FPS = 8
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", VIDEO, "-vf", f"fps={FPS},scale=64:36,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64).astype(np.float32)
std = fr.reshape(len(fr), -1).std(1)
for i in np.where(std < 7)[0]:
    t = i / FPS
    if t > 0.3 and t < DUR - 0.5:
        add("fail", "visual", f"blank / flat frame (solid colour) at {ts(t)}", t)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
for i in range(1, len(d) - 1):
    skip = np.abs(fr[i + 1] - fr[i - 1]).mean()
    if d[i - 1] > 25 and d[i] > 25 and skip < 6:
        add("fail", "smoothness", f"single-frame flash/glitch at {ts(i / FPS)}", i / FPS)
run = 0
for i, v in enumerate(d):
    run = run + 1 if v < 0.15 else 0
    if run == int(3.5 * FPS):
        add("warn", "smoothness", f"picture frozen for >3.5 s around {ts(i / FPS)}", i / FPS)
# collapse duplicates of the same problem within 1 s
seen, uniq = set(), []
for f in findings:
    key = (f["area"], f["msg"].split(" at ")[0], None if f["t"] is None else round(f["t"]))
    if key not in seen: seen.add(key); uniq.append(f)
findings[:] = uniq

# ---------- 3. audio ----------
r = subprocess.run(["ffmpeg", "-nostats", "-i", VIDEO, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
lufs = float(I[-1]) if I else None; peak = float(TP[-1]) if TP else None
if lufs is not None and abs(lufs + 14) > 1.5: add("fail", "audio", f"integrated loudness {lufs} LUFS (target -14)")
if peak is not None and peak > -0.5: add("fail", "audio", f"true peak {peak} dBFS (clipping risk)")
r = subprocess.run(["ffmpeg", "-nostats", "-i", VIDEO, "-af", "silencedetect=n=-45dB:d=1.5", "-f", "null", "-"], capture_output=True, text=True).stderr
for a, b in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r):
    if float(a) > 0.5 and float(b) < DUR - 0.5:
        add("warn", "audio", f"dead air {float(b) - float(a):.1f}s at {ts(float(a))}", float(a))

_asr = None


def asr_match(wav, text):
    global _asr
    import difflib, soundfile as sf, torch, torchaudio
    from faster_whisper import WhisperModel
    if not os.path.exists(wav): return 0.0
    if _asr is None: _asr = WhisperModel("small.en", device="cuda", compute_type="float16")
    a, sr = sf.read(wav, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    a = torchaudio.functional.resample(torch.from_numpy(a), sr, 16000).numpy()
    heard = " ".join(x.text for x in _asr.transcribe(a, beam_size=5)[0])
    n = lambda t: re.findall(r"[a-z0-9']+", t.lower().replace("*", ""))
    return difflib.SequenceMatcher(None, n(text), n(heard)).ratio()


# ---------- 4. per-line checks: speech rate (TTS glitches), clipped words, mouth frames, caption coverage ----------
spoken_lines = []
for s in sc["scenes"]:
    lp = f"{P}/audio/{s['id']}.lines.json"
    if not os.path.exists(lp): continue
    lines = json.load(open(lp)); props = jobs.get(s["id"], {})
    cast = {c["char"]: c for c in props.get("cast", [])}
    for ln, src in zip(lines, s.get("lines", [])):
        t0 = starts[s["id"]] + ln["start"]; dur = ln["end"] - ln["start"]
        nw = len(re.findall(r"[A-Za-z0-9']+", src.get("text", "")))
        if dur > 0 and nw / dur > 4.6:
            # quick line or TTS glitch? transcribe it: fail only if the words don't match the script
            sim = asr_match(f"{P}/audio/lines/{ln['key']}.wav", src["text"]) if ln.get("key") else 0
            if sim < 0.8: add("fail", "audio", f"garbled/rushed speech (ASR match {sim:.2f}, {nw / dur:.1f} w/s) {s['id']} \"{src['text'][:50]}\"", t0)
        if dur > 0 and nw >= 3 and nw / dur < 1.1: add("warn", "audio", f"speech very slow ({nw / dur:.1f} w/s) — long pause/garble? {s['id']}", t0)
        if src["speaker"] in cast:
            spoken_lines.append((s, ln, src, cast[src["speaker"]], props))
            pz = cast[src["speaker"]]["poses"]
            pose = src["pose"] if src["pose"] in pz else "talk" if "talk" in pz else "neutral"
            if pz.get(pose) and not pz[pose].get("talk"):
                add("warn", "lip-sync", f"{src['speaker']} pose '{pose}' has no mouth-move frames (falls back to overlay mouth) {s['id']}", t0)
    words = props.get("words", [])
    if s.get("lines") and len(words) < sum(len(l["text"].split()) for l in s["lines"]) * 0.9:
        add("fail", "text", f"captions missing words in {s['id']}", starts[s["id"]])
    end_ms = max([w["endMs"] for w in words] or [0])
    if props.get("durationInFrames") and end_ms / 1000 > props["durationInFrames"] / props.get("fps", 30) + 0.05:
        add("fail", "audio", f"speech runs past the end of scene {s['id']} (clipped words)", starts[s["id"]])

# ---------- 5. layout checks from props ----------
for sid, p in jobs.items():
    if p.get("kind") == "chart" and p.get("chart"):
        c = p["chart"]
        if len(set(c["values"])) == 1 and len(c["values"]) > 1: add("warn", "text", f"chart {sid} has identical bars", starts.get(sid))
        if any(len(l) > 28 for l in c["labels"]): add("warn", "text", f"chart {sid} has very long labels", starts.get(sid))
    beats = sorted(p.get("beats", []), key=lambda b: b["atMs"])
    for a, b in zip(beats, beats[1:]):
        if b["atMs"] - a["atMs"] < 900: add("warn", "text", f"beats in {sid} {b['atMs'] - a['atMs']} ms apart (second replaces first too fast)", starts.get(sid))

# ---------- 6. camera-aware face crops for every spoken line ----------
SLOT = {"left": 0.27, "center": 0.5, "right": 0.73}
CHAR_H, FEET_Y, PUSH = 0.70, 0.95, 1.035


def cam(cast, shot, sp_pos):
    feet, head = H * FEET_Y, H * (FEET_Y - CHAR_H)
    if shot == "closeup": s = 1.6; return s, W * SLOT[sp_pos], head + (H / 2 - 70) / (s * PUSH)
    if shot == "detail": return 1.2, W / 2, H * 0.4
    if shot == "wide": return 1.0, W / 2, H / 2
    xs = [W * SLOT[c["position"]] for c in cast]; s = 1.06
    return s, (min(xs) + max(xs)) / 2, feet - (H / 2 - 25) / (s * PUSH)


tiles = []
for f in os.listdir(OUT):
    if f.startswith("_f"): os.remove(os.path.join(OUT, f))
for s, ln, src, member, props in spoken_lines:
    pz = member["poses"]; pose = src["pose"] if src["pose"] in pz else next(iter(pz))
    if pose in ("talk", "neutral", "side_talk") and src["shot"] == "two_shot" and len(props["cast"]) > 1 and "side_talk" in pz: pose = "side_talk"
    im = pz[pose]; th = H * CHAR_H; sc_ = th / im["h"]
    m = im.get("mouth") or {"x": 0.45, "y": 0.18, "w": 0.1, "h": 0.03}
    wx = W * SLOT[member["position"]]; wy = H * FEET_Y - th + (m["y"] + m["h"] / 2) * th - th * 0.04
    s_, cx, cy = cam(props["cast"], src["shot"], member["position"])
    s_ *= PUSH
    cx = min(max(cx, W / (2 * s_)), W - W / (2 * s_)); cy = min(max(cy, H / (2 * s_)), H - H / (2 * s_))
    sx, sy = W / 2 + s_ * (wx - cx), H / 2 + s_ * (wy - cy)
    size = int(min(H, th * 0.42 * s_))
    for frac in (0.25, 0.5, 0.75):
        t = starts[s["id"]] + ln["start"] + (ln["end"] - ln["start"]) * frac
        x0 = int(max(0, min(W - size, sx - size / 2))); y0 = int(max(0, min(H - size, sy - size * 0.55)))
        out = f"{OUT}/_f{len(tiles):04d}.png"
        label = f"{ts(t)} {s['id']} {src['speaker'][:9]}".replace(":", "\\:")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", VIDEO, "-frames:v", "1", "-vf",
                        f"crop={size}:{size}:{x0}:{y0},scale=180:180,drawtext=text='{label}':x=3:y=3:fontsize=12:fontcolor=white:box=1:boxcolor=black@0.6",
                        out], check=False)
        if os.path.exists(out): tiles.append(out)
if tiles:
    from PIL import Image
    cols = 12; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (180 * cols, 180 * rows), "black")
    for i, f in enumerate(tiles):
        sheet.paste(Image.open(f).convert("RGB"), ((i % cols) * 180, (i // cols) * 180)); os.remove(f)
    sheet.save(f"{OUT}/faces.png")

# ---------- report ----------
json.dump({"duration": DUR, "lufs": lufs, "true_peak": peak, "findings": findings}, open(f"{OUT}/review.json", "w"), indent=1)
fails = [f for f in findings if f["level"] == "fail"]
md = [f"# Full review — {NAME}", f"Duration {ts(DUR)} · loudness {lufs} LUFS · true peak {peak} dBFS",
      f"Sheets: {', '.join(sorted(x for x in os.listdir(OUT) if x.startswith('sheet_')))} · faces.png", "",
      f"## Automatic findings ({len(fails)} fail, {len(findings) - len(fails)} warn)"]
md += [f"- **{f['level'].upper()}** [{f['area']}] {f['msg']}" for f in findings] or ["- none"]
md += ["", "## Manual checklist (look at EVERY sheet tile and faces.png)",
       "1. Grounding: feet on the floor, not floating/sinking/sliding, not overlapping furniture, consistent scale, facing the partner",
       "2. Lip-sync: only the speaker's mouth moves, ONE mouth only, closed when silent",
       "3. Eyes/expressions: blinking, looking at the speaker, expression fits the line",
       "4. Body language: poses change smoothly, listeners react, hands not distorted",
       "5. Consistency: same character look/outfit/size every scene, stable lighting/backgrounds",
       "6. Camera: no cut-off heads, feet visible in wide/two-shots, balanced framing",
       "7. Backgrounds: undistorted, no garbled text, characters have contact shadows",
       "8. Text: captions match audio, never over faces, no overlapping/cropped graphics, no garbled text in images, spelling",
       "9. Audio: clear, even voices, no clipped words, music under speech",
       "10. Smoothness: no jumps/flicker/ghosting/duplicated frames at transitions",
       "11. Overall: sharp, clean edges, consistent colour",
       "", "Do not change narration, meaning, sequence, character design, aspect ratio or style when fixing."]
open(f"{OUT}/REVIEW.md", "w").write("\n".join(md) + "\n")
print(f"{OUT}/REVIEW.md  fails={len(fails)} warns={len(findings) - len(fails)} sheets={n_sheets}")
sys.exit(1 if fails else 0)
