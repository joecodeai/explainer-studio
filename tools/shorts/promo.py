"""ONE promotional Reel (9:16) cut from a finished long-form video (library/SHORTS_RULES.md, 2026-11-25 strategy).

  P=.venv/bin/python; export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1
  $P tools/shorts/promo.py <topic> <reelspec>      # spec: tools/shorts/topics/<reelspec>.py with REEL = dict(title, pieces=[...])

Every frame is composed in Python, so no shot is blindly centre-cropped. A piece is one shot of the long video:
  dict(id="c01")                      FULL (default): the whole 16:9 frame, full canvas width, over a blurred enlarged copy
  dict(id="d01", f=0.6, x=0.5)        BOX: a window f of the source width (full height), centred at x, scaled to canvas width.
                                      f=1 is FULL; f=0.316 is a full-screen 9:16 crop. x / f may be (start, end) to pan / push in
                                      (eased over the piece), or [(0, v0), (0.4, v1), (1, v2)] keyframes on the piece's 0..1 time.
  dict(id="b03", h=0.9, y=0.45)       also crop to h of the source height, centred at y (removes empty floor / sky)
  dict(id="w07", words=(0, 14))       only words 0..14 of the line (sentence-level trims only); tail= / lead= seconds
  dict(id="v06", sub=(0.0, 1.5))      only seconds 0..1.5 of the piece (sequential framing: same shot twice, two framings)
Captions sit BELOW the picture in the blurred band when there is room, otherwise on the lower third, never in the bottom
UI band (y > 1540) and never on the right-side buttons. Output: VIDEOS/<FOLDER>/Reel/<title>.mp4 + a QC sheet per piece.
"""
import importlib, json, os, re, subprocess, sys
import cv2, numpy as np, soundfile as sf
ARGS = sys.argv[:]
TOPIC, SPEC = ARGS[1], ARGS[2]
sys.argv = ["build.py", TOPIC]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B                                              # noqa: E402  (chdir's to the repo root)
R = importlib.import_module(f"topics.{SPEC}").REEL
OUT = B.OUT; tl = json.load(open(f"{OUT}/timeline.json")); idx = {x["id"]: i for i, x in enumerate(tl)}
SH = {s["id"]: s for s in B.SHOTS}
W, H, FPS, SR, SW, SH_ = 1080, 1920, 24, 48000, 1920, 1080
CAP_TOP_MAX, UI_Y = 1330, 1540                                 # caption block must end above the bottom UI band
WD = f"{OUT}/promo"; os.makedirs(WD, exist_ok=True)
WCACHE = f"{WD}/words.json"; _w = json.load(open(WCACHE)) if os.path.exists(WCACHE) else {}


def words(sid):
    if sid not in _w:
        _w[sid] = B.line_words(SH[sid]) if B.spoken(SH[sid]) else []
        json.dump(_w, open(WCACHE, "w"))
    return _w[sid]


def span(p):
    i = idx[p["id"]]; a0, L = B.seg_len(i, tl); a, b = a0, a0 + L
    if "words" in p:
        w = words(p["id"]); st = tl[i]["start"]; f, l = p["words"]
        a = max(a0, st + w[f]["s"] - p.get("lead", 0.18)); b = min(a0 + L, st + w[l]["e"] + p.get("tail", 0.35))
    if "sub" in p: a, b = a + p["sub"][0], min(b, a + p["sub"][1])
    if "trim" in p: a, b = a + p["trim"][0], b - p["trim"][1]          # shave dead air (seconds) off the start / end
    return a, b


def ease(u): return u * u * (3 - 2 * u)


def val(v, u):
    """Parameter at piece time u (0..1): constant, (start, end) eased, or [(t, v), ...] keyframes."""
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, tuple): return v[0] + (v[1] - v[0]) * ease(u)
    for (t0, v0), (t1, v1) in zip(v, v[1:]):
        if u <= t1: return v0 + (v1 - v0) * ease(min(1, max(0, (u - t0) / max(1e-6, t1 - t0))))
    return float(v[-1][1])


def geom(p, u):
    f = max(0.316, min(1.0, val(p.get("f", 1.0), u))); h = val(p.get("h", 1.0), u)
    cw, ch = f * SW, h * SH_
    dh = min(H, W * ch / cw)                                    # displayed height at full canvas width
    if dh >= H - 1: cw = ch * W / H; dh = H                     # tall crop: fill the screen
    x = val(p.get("x", 0.5), u); y = val(p.get("y", 0.5), u)
    x0 = min(max(0, x * SW - cw / 2), SW - cw); y0 = min(max(0, y * SH_ - ch / 2), SH_ - ch)
    top = 0 if dh >= H else int(round(min(max(110, 880 - dh / 2), CAP_TOP_MAX - 34 - dh)))
    return (x0, y0, cw, ch), int(round(dh)), top


def compose(fr, p, u):
    small = cv2.resize(fr, (240, 135), interpolation=cv2.INTER_AREA)[:, 82:158]      # cover-crop to 9:16 at low res
    bg = cv2.GaussianBlur(cv2.resize(small, (W // 4, H // 4), interpolation=cv2.INTER_LINEAR), (0, 0), 9)
    bg = (cv2.resize(bg, (W, H), interpolation=cv2.INTER_LINEAR) * 0.62).astype(np.uint8)
    (x0, y0, cw, ch), dh, top = geom(p, u)
    M = np.float32([[W / cw, 0, -x0 * W / cw], [0, dh / ch, -y0 * dh / ch]])           # sub-pixel crop+scale (smooth pans)
    fg = cv2.warpAffine(fr, M, (W, dh), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    if dh >= H: return fg
    bg[top:top + dh] = fg
    cv2.line(bg, (0, top - 1), (W, top - 1), (0, 0, 0), 2); cv2.line(bg, (0, top + dh), (W, top + dh), (0, 0, 0), 2)
    return bg


def cap_y(p):
    return CAP_TOP_MAX                                          # one consistent caption line, under every boxed picture


def ass_time(t): h, m = divmod(t, 3600); m, s = divmod(m, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def main():
    mix, _ = sf.read(f"{OUT}/mix.wav", dtype="float32")
    if mix.ndim > 1: mix = mix.mean(1)
    pic = f"{WD}/picture.mp4"
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", pic], stdin=subprocess.PIPE)
    aud, ev, t, nf, qc = [], [], 0.0, 0, []
    for k, p in enumerate(R["pieces"]):
        a, b = span(p); n = max(1, int(round((b - a) * FPS))); d = n / FPS
        s0 = B.seg_len(idx[p["id"]], tl)[0]                    # read the shot's own segment: no bleed from neighbouring shots
        dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{a - s0:.3f}", "-i", f"{OUT}/seg/{idx[p['id']]:02d}.mp4", "-frames:v", str(n),
                                "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
        last = None
        for j in range(n):
            buf = dec.stdout.read(SW * SH_ * 3)
            fr = np.frombuffer(buf, np.uint8).reshape(SH_, SW, 3) if len(buf) == SW * SH_ * 3 else last
            last = fr; out = compose(fr, p, j / max(1, n - 1)); enc.stdin.write(out.tobytes())
            if j in (0, n // 2, n - 1): qc.append((k, p["id"], j, out))
        dec.wait()
        clip = mix[int(a * SR):int(a * SR) + int(d * SR)].copy(); fd = min(len(clip) // 2, int(0.025 * SR))
        if fd: clip[:fd] *= np.linspace(0, 1, fd); clip[-fd:] *= np.linspace(1, 0, fd)
        aud.append(clip)
        s = SH[p["id"]]
        if B.spoken(s):
            st = tl[idx[p["id"]]]["start"]; ws = [w for w in words(p["id"]) if a - 0.05 <= st + w["s"] <= b]
            chunks, cur = [], []
            for w in ws:
                cur.append(w)
                if len(cur) == 3 or re.search(r"[.,?!]$", w["w"]): chunks.append(cur); cur = []
            if cur: chunks.append(cur)
            for j, c in enumerate(chunks):
                s0 = t + max(0, st + c[0]["s"] - a)
                s1 = t + ((st + chunks[j + 1][0]["s"] - a) if j + 1 < len(chunks) else (st + c[-1]["e"] - a + 0.3))
                ev.append(f"Dialogue: 0,{ass_time(s0)},{ass_time(min(s1, t + d))},C,,0,0,{cap_y(p)},,{' '.join(w['w'] for w in c).upper()}")
        print(f"{k:2d} {p['id']:5s} {a:7.2f}-{b:7.2f}  {d:5.2f}s  at {t:5.1f}s", flush=True)
        t += d; nf += n
    enc.stdin.close(); enc.wait()
    wav = f"{WD}/reel.wav"; sf.write(wav, np.concatenate(aud), SR)
    ass = f"{WD}/reel.ass"                                      # Alignment 8 = top-centre; per-line MarginV is the caption's top y
    open(ass, "w").write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: C,Montserrat ExtraBold,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,8,110,170,0,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ev) + "\n")
    dst = os.path.join("VIDEOS", getattr(B.T, "FOLDER", TOPIC), "Reel"); os.makedirs(dst, exist_ok=True)
    final = os.path.join(dst, f"{R['title']}.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", pic, "-i", wav, "-vf",
                    f"subtitles={ass}:fontsdir={os.path.abspath('studio/fonts_reel')}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", final], check=True)
    # QC: first / middle / last composed frame of every piece (before captions), 9 per row
    th = [cv2.putText(cv2.resize(o, (216, 384)), f"{k} {sid}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2) for k, sid, _, o in qc]
    rows = [np.hstack(th[i:i + 9] + [np.zeros_like(th[0])] * (9 - len(th[i:i + 9]))) for i in range(0, len(th), 9)]
    cv2.imwrite(f"{WD}/qc_frames.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82])
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", final, "-vf", "fps=1/2,scale=180:-1,tile=10x4", "-frames:v", "1",
                    f"{WD}/qc_final_sheet.jpg"])
    print(f"REEL {t:.1f}s -> {final}", flush=True)


if __name__ == "__main__":
    main()
