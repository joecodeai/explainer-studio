"""Cut a 9:16 Short from a finished long-form video (library/SHORTS_RULES.md): real picture + real mix, reframed, re-captioned.

  P=.venv/bin/python; export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1
  $P tools/shorts/cutdown.py <topic> <shortspec>     # spec module: tools/shorts/topics/<shortspec>.py with SHORTS = [...]

Each Short = dict(name, title, pieces=[...]). A piece is one shot of the long video:
  dict(id="w05")                          whole shot span (from half a gap before its line to half a gap before the next shot)
  dict(id="w07", words=(0, 14))           only words 0..14 of the line (sentence-level trim; never mid-sentence)
  dict(id="w07", tail=0.6)                ...with extra seconds kept after the last word (default 0.35)
  dict(id="c01", x=0.40)                  crop centre (0 = left edge, 1 = right edge; default 0.5)
  dict(id="i03", fit="pad")               whole 16:9 frame over a blurred, enlarged copy (for wide images)
Output: VIDEOS/<FOLDER>/Reel/Short N - <title>.mp4 (+ a contact sheet in projects/short-<topic>/shorts/).
"""
import importlib, json, os, re, subprocess, sys
import numpy as np, soundfile as sf
ARGS = sys.argv[:]
TOPIC, SPEC = ARGS[1], ARGS[2]
sys.argv = ["build.py", TOPIC]                                  # reuse the builder's timeline + word-timing code
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B                                              # noqa: E402  (chdir's to the repo root)
S = importlib.import_module(f"topics.{SPEC}")
OUT = B.OUT; tl = json.load(open(f"{OUT}/timeline.json")); idx = {x["id"]: i for i, x in enumerate(tl)}
SH = {s["id"]: s for s in B.SHOTS}
W, H, FPS, SR = 1080, 1920, 24, 48000
os.makedirs(f"{OUT}/shorts", exist_ok=True)
_wcache = {}


def words(sid):
    if sid not in _wcache: _wcache[sid] = B.line_words(SH[sid]) if B.spoken(SH[sid]) else []
    return _wcache[sid]


def span(p):
    """(a, b) seconds in the long video for one piece."""
    i = idx[p["id"]]; a0, L = B.seg_len(i, tl)
    if "words" not in p: return a0, a0 + L
    w = words(p["id"]); st = tl[i]["start"]; f, l = p["words"]
    a = st + w[f]["s"] - 0.18; b = st + w[l]["e"] + p.get("tail", 0.35)
    if p.get("lead") is not None: a = st + w[f]["s"] - p["lead"]
    return max(a0, a), min(a0 + L, b)


def vf(p):
    if p.get("fit") == "pad":
        return ("split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.08[bg];"
                "[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,setsar=1")
    z = p.get("zoom", 1.0); x = p.get("x", 0.5)
    cw = f"ih*9/16/{z}"; ch = f"ih/{z}"
    return f"crop={cw}:{ch}:(iw-{cw})*{x}:(ih-{ch})*{p.get('y', 0.5)},scale={W}:{H}:flags=lanczos,setsar=1"


def ass_time(t): h, m = divmod(t, 3600); m, s = divmod(m, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def make(n, short):
    segs, ev, t = [], [], 0.0
    aud = []
    mix, _ = sf.read(f"{OUT}/mix.wav", dtype="float32")
    if mix.ndim > 1: mix = mix.mean(1)
    for k, p in enumerate(short["pieces"]):
        a, b = span(p); d = b - a
        o = f"{OUT}/shorts/s{n}_{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", f"{a:.3f}", "-i", f"{OUT}/picture.mp4", "-t", f"{d:.3f}",
                        "-vf", vf(p) + f",fps={FPS}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", o], check=True)
        segs.append(o)
        clip = mix[int(a * SR):int(b * SR)].copy(); fd = min(len(clip) // 2, int(0.03 * SR))
        if fd: clip[:fd] *= np.linspace(0, 1, fd); clip[-fd:] *= np.linspace(1, 0, fd)
        aud.append(clip)
        s = SH[p["id"]]
        if B.spoken(s):                                         # captions: the words that fall inside this piece
            st = tl[idx[p["id"]]]["start"]; ws = [w for w in words(p["id"]) if a - 0.05 <= st + w["s"] <= b]
            chunks, cur = [], []
            for w in ws:
                cur.append(w)
                if len(cur) == 3 or re.search(r"[.,?!]$", w["w"]): chunks.append(cur); cur = []
            if cur: chunks.append(cur)
            for j, c in enumerate(chunks):
                s0 = t + (st + c[0]["s"] - a); s1 = t + ((st + chunks[j + 1][0]["s"] - a) if j + 1 < len(chunks) else (st + c[-1]["e"] - a + 0.25))
                ev.append(f"Dialogue: 0,{ass_time(s0)},{ass_time(min(s1, t + d))},C,,0,0,0,,{' '.join(w['w'] for w in c).upper()}")
        t += d
    lst = f"{OUT}/shorts/s{n}_list.txt"; open(lst, "w").write("\n".join(f"file '{os.path.abspath(x)}'" for x in segs))
    pic = f"{OUT}/shorts/s{n}_picture.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic], check=True)
    wav = f"{OUT}/shorts/s{n}.wav"; sf.write(wav, np.concatenate(aud), SR)
    ass = f"{OUT}/shorts/s{n}.ass"                              # captions sit above the bottom UI band, centred (clear of the right-side buttons)
    open(ass, "w").write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: C,Montserrat ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,120,160,600,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ev) + "\n")
    dst = os.path.join("VIDEOS", getattr(B.T, "FOLDER", TOPIC), "Reel"); os.makedirs(dst, exist_ok=True)
    final = os.path.join(dst, f"Short {n} - {short['title']}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", pic, "-i", wav, "-vf",
                    f"subtitles={ass}:fontsdir={os.path.abspath('studio/fonts_reel')}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", final], check=True)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", final, "-vf", "fps=1/3,scale=180:-1,tile=8x3", "-frames:v", "1",
                    f"{OUT}/shorts/s{n}_sheet.jpg"])
    print(f"short {n}: {t:.1f}s -> {final}", flush=True)


for n, sh in enumerate(S.SHORTS, 1):
    if len(ARGS) > 3 and str(n) not in ARGS[3].split(","): continue
    make(n, sh)
