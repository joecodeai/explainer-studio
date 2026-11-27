"""Automatic final QC (2026-11-27), the AUTO half of library/QC_CHECKLIST.md. Runs after `mix` in about a minute; adds no render time.
  python tools/shorts/qc_auto.py <topic>      (or: build.py <topic> qc)   -> projects/short-<topic>/qc/QC_REPORT.txt
Every FLAG line names the shot to redo (re-seed a clip, regenerate a keyframe, adjust a hold), never a full re-render."""
import difflib, glob, importlib, json, os, re, subprocess, sys
import cv2, numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import autoclean  # noqa: E402

TOPIC = sys.argv[1]; OUT = f"projects/short-{TOPIC}"
T = importlib.import_module(f"topics.{TOPIC}"); LAND = getattr(T, "LANDSCAPE", False)
FINAL = f"{OUT}/{TOPIC.upper()}_{'VIDEO' if LAND else 'SHORT'}.mp4"
tl = json.load(open(f"{OUT}/timeline.json")); shots = {s["id"]: s for s in T.SHOTS}
flags, notes = [], []
def flag(m): flags.append("FLAG " + m)
def note(m): notes.append("ok   " + m)
def at(t):                                             # shot id playing at time t
    for x in tl:
        if x["start"] <= t < x["start"] + x["dur"]: return x["id"]
    return "end"
def ff(args): return subprocess.run(["ffmpeg", "-nostdin", "-hide_banner"] + args, capture_output=True, text=True).stderr

# 1. length (mid-roll needs 8:00) and loudness
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", FINAL], capture_output=True, text=True).stdout)
if LAND and dur < 480: flag(f"length {dur / 60:.2f} min is under 8:00 (mid-roll); stretch holds or add a beat")
elif not LAND and not 30 <= dur <= 90: flag(f"Reel length {dur:.1f}s outside 30-90 s")
else: note(f"length {int(dur // 60)}:{int(dur % 60):02d}")
e = ff(["-i", FINAL, "-af", "ebur128=peak=true", "-f", "null", "-"])
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); pk = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
(flag if not (-15.0 <= I <= -13.0 and pk <= -1.0) else note)(f"loudness {I} LUFS, peak {pk} dBFS (target -14 +/-1, peak <= -1)")

# 2. black frames / flashes, unexpected silence, frozen animated shots
for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", ff(["-i", FINAL, "-vf", "blackdetect=d=0.08:pix_th=0.06", "-an", "-f", "null", "-"])):
    flag(f"black frames {m.group(1)}-{m.group(2)}s in shot {at(float(m.group(1)))}")
for m in re.finditer(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", ff(["-i", FINAL, "-af", "silencedetect=noise=-50dB:d=2.5", "-vn", "-f", "null", "-"])):
    if float(m.group(1)) < dur - 3: flag(f"silence {m.group(1)}-{m.group(2)}s in shot {at(float(m.group(1)))} (missing room tone or audio?)")
for m in re.finditer(r"freeze_start: ([\d.]+)[\s\S]*?freeze_end: ([\d.]+)", ff(["-i", FINAL, "-vf", "freezedetect=n=0.002:d=1.5", "-an", "-f", "null", "-"])):
    sid = at(float(m.group(1))); eng = shots.get(sid, {}).get("eng", "")
    if eng in ("h3", "ltx"): flag(f"picture frozen {m.group(1)}-{m.group(2)}s in animated shot {sid} (clip too short / stalled)")

# 3. per animated clip: jumps, morph pops, brightness flicker; clip shorter than its slot
def clip_for(i):
    c = [p for p in glob.glob(f"{OUT}/clips/{i}_*.mp4") if not p.endswith(("_a.mp4", "_b.mp4"))]
    return max(c, key=os.path.getmtime) if c else None
for x in tl:
    s = shots.get(x["id"], {})
    if s.get("eng") not in ("h3", "ltx"): continue
    p = clip_for(x["id"])
    if not p: flag(f"{x['id']}: no clip"); continue
    cap = cv2.VideoCapture(p); fps = cap.get(cv2.CAP_PROP_FPS) or 24; prev = None; d, lum = [], []
    while True:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (96, 54)).astype(np.float32)
        if prev is not None: d.append(np.abs(g - prev).mean())
        lum.append(g.mean()); prev = g
    n = len(lum) / fps
    if n + 0.05 < x["dur"]: flag(f"{x['id']}: clip {n:.1f}s shorter than its {x['dur']:.1f}s slot (last frame held)")
    if len(d) > 5:
        d = np.array(d); k = int(d.argmax()); med = float(np.median(d)) + 0.5
        if d[k] > max(14.0, 7 * med): flag(f"{x['id']}: jump/cut inside the clip at {k / fps:.1f}s (diff {d[k]:.0f} vs typical {med:.1f}) - re-seed")
        dl = np.abs(np.diff(np.array(lum)))
        if dl.max() > 10: flag(f"{x['id']}: brightness jump at {dl.argmax() / fps:.1f}s ({dl.max():.0f}) - re-seed")
note("animated clips scanned for jumps, flicker and length")

# 4. specks left in keyframes
left = {f[:-4]: r for f in sorted(os.listdir(f"{OUT}/keyframes")) if f.endswith(".png")
        for r in [autoclean.find(cv2.imread(f"{OUT}/keyframes/{f}"))[1]] if r}
for k, r in left.items(): flag(f"{k}: possible speck(s) {[(x, y, a) for _, x, y, a, _ in r]} - look at it; autoclean or regenerate if real")
if not left: note("no green/purple specks left in keyframes")

# 5. transcript vs script: dropped / cut / duplicated / extra (murmur) words
NUM = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen "
          "twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion dollar dollars cent cents percent point and a "
          "us united states uk".split())   # whisper writes numbers as digits ("$26.77"); compare the words around them instead
def words(t): return [w for w in re.sub(r"[^a-z0-9' ]", " ", t.lower().replace("-", " ")).split() if not re.search(r"\d", w) and w not in NUM]
script = words(" ".join(s.get("text", "") for s in T.SHOTS if s.get("text")))
try:
    import soundfile as sf
    from faster_whisper import WhisperModel
    wav = f"{OUT}/qc/_qc16.wav"; os.makedirs(f"{OUT}/qc", exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", FINAL, "-ac", "1", "-ar", "16000", wav], check=True)
    a, _ = sf.read(wav, dtype="float32")
    heard = words(" ".join(x.text for x in WhisperModel("distil-large-v3", device="cuda", compute_type="float16").transcribe(a, language="en", vad_filter=True)[0]))
    sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        a_, b_ = " ".join(script[i1:i2]), " ".join(heard[j1:j2])
        if op == "replace" and difflib.SequenceMatcher(None, a_, b_).ratio() > 0.5: continue      # spelling / paraphrase near-miss
        if op in ("delete", "replace") and i2 - i1 >= 4: flag(f"words not heard: '{a_}' (dropped/cut line?)")
        if op in ("insert", "replace") and j2 - j1 >= 4: flag(f"extra words heard: '{b_}' (murmur, duplicate or garbled?)")
    note(f"transcript match {sm.ratio() * 100:.1f}% ({len(script)} script words)")
    os.remove(wav)
except Exception as ex:
    flag(f"transcript check could not run: {ex!r}"[:200])

rep = "\n".join([f"QC {TOPIC}  {FINAL}"] + notes + flags + [f"\n{len(flags)} flag(s). EYE checks still due: keyframe contact sheet + clip strips (library/QC_CHECKLIST.md)."])
open(f"{OUT}/qc/QC_REPORT.txt", "w").write(rep); print(rep)
