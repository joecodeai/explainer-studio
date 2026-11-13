"""Face-crop contact sheet of speaking characters across a finished video (one look = catch mouth glitches).
usage: python tools/mouthcheck.py <project_dir> [max_crops]"""
import json, os, subprocess, sys
P = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
jobs = json.load(open(f"{P}/work/render_jobs.json"))["jobs"]
props = {j["props"]["id"]: j["props"] for j in jobs}
sc = json.load(open(f"{P}/script.json"))
# scene start times in the final video = same xfade maths as pipeline.assemble_video
XF = {"slide": 0.45, "zoom": 0.5, "wipe": 0.45, "whip": 0.3, "fade": 0.5, "cut": 0.04}
starts, t = {}, 0.0
rend = {}
for s in sc["scenes"]:
    out = f"{P}/renders/{s['id']}.mp4"
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout or 0)
    rend[s["id"]] = d
prev = None
for s in sc["scenes"]:
    if prev is None: starts[s["id"]] = 0.0
    else: starts[s["id"]] = starts[prev["id"]] + rend[prev["id"]] - XF[s["transition"]]
    prev = s
SLOT = {"left": 0.27, "center": 0.5, "right": 0.73}
crops = []
for s in sc["scenes"]:
    if s["kind"] != "stage": continue
    lines = json.load(open(f"{P}/audio/{s['id']}.lines.json"))
    pos = {c["char"]: c["position"] for c in s["cast"]}
    for l, src in zip(lines, s["lines"]):
        if l["speaker"] not in pos: continue
        x = SLOT[pos[l["speaker"]]] * 1920
        if src["shot"] == "closeup": x = 960
        for frac in (0.3, 0.7):   # two moments per line
            tt = starts[s["id"]] + l["start"] + (l["end"] - l["start"]) * frac
            crops.append((tt, x, src["shot"], f"{s['id']} {l['speaker'][:10]} {src['pose']}"))
step = max(1, len(crops) // N); crops = crops[::step][:N]
video = f"{P}/{os.path.basename(P)}.mp4"
tiles = []
for i, (tt, x, shot, label) in enumerate(crops):
    f = f"{P}/work/mc_{i}.png"
    w, y = (700, 60) if shot == "closeup" else (420, 230)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{tt:.2f}", "-i", video, "-frames:v", "1", "-vf",
                    f"crop={w}:{w}:{int(max(0, min(1920 - w, x - w / 2)))}:{y},scale=200:200,drawtext=text='{label}':x=4:y=4:fontsize=13:fontcolor=white:box=1:boxcolor=black@0.6",
                    f], check=False)
    if os.path.exists(f): tiles.append(f)
cols = 8
rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
args, filt, names = [], [], []
for r, row in enumerate(rows):
    while len(row) < cols: row.append(row[-1])
    for f in row: args += ["-i", f]
k = 0
for r, row in enumerate(rows):
    filt.append("".join(f"[{k + j}]" for j in range(cols)) + f"hstack={cols}[r{r}]"); k += cols
filt.append("".join(f"[r{r}]" for r in range(len(rows))) + (f"vstack={len(rows)}[o]" if len(rows) > 1 else "null[o]"))
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", ";".join(filt), "-map", "[o]", f"{P}/work/mouthcheck.png"], check=True)
print(f"{P}/work/mouthcheck.png", len(tiles), "crops")
