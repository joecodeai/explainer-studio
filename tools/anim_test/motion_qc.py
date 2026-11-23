"""Motion QC for a test clip: is it really animated, smooth, and free of jumps/freezes/flicker?

Per clip prints: frame-to-frame motion (median / max / spikes), frozen stretches, brightness flicker, and makes
  qc/<clip>_strip.jpg  - 6 consecutive full frames from the middle (shows real per-frame motion / smear)
  qc/<clip>_motion.png - motion-energy plot over time
  python tools/anim_test/motion_qc.py projects/batbomb-animtest/clips/*.mp4
"""
import json, os, subprocess, sys
import numpy as np


def frames(path, w=320):
    h_probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                              "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip().split(",")
    W0, H0 = int(h_probe[0]), int(h_probe[1]); h = int(round(H0 * w / W0 / 2) * 2)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def analyse(path):
    f = frames(path)
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))            # motion energy per frame step
    med = float(np.median(d)) if len(d) else 0.0
    spikes = [int(i + 1) for i in np.where(d > max(3.0, 4 * med + 1.5))[0]]
    frozen = int((d < 0.05).sum())                              # identical consecutive frames (H3 animates on twos: ~50% is normal there)
    lum = f.mean(axis=(1, 2)); flick = float(np.abs(np.diff(lum)).max()) if len(lum) > 1 else 0.0
    # how much of the frame actually moves: share of pixels changing > 4 levels between frames 1 s apart
    k = min(24, len(f) - 1); moving = float((np.abs(f[k:] - f[:-k]) > 4).mean()) if k > 0 else 0.0
    qc = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), "qc"); os.makedirs(qc, exist_ok=True)
    stem = os.path.basename(path)[:-4]; mid = len(f) // 2
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf",
                    f"select='between(n\\,{mid}\\,{mid + 5})',scale=640:-1,drawtext=text='%{{n}}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=3x2",
                    "-frames:v", "1", os.path.join(qc, f"{stem}_strip.jpg")], check=True)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 2.2)); plt.plot(d); plt.title(f"{stem}: motion per frame"); plt.tight_layout()
        plt.savefig(os.path.join(qc, f"{stem}_motion.png")); plt.close()
    except Exception:
        pass
    return {"clip": stem, "frames": len(f), "motion_median": round(med, 2), "motion_max": round(float(d.max()), 2),
            "spikes": spikes[:12], "frozen_steps": frozen, "frozen_pct": round(100 * frozen / max(1, len(d)), 1),
            "max_brightness_jump": round(flick, 2), "pixels_moving_1s": round(100 * moving, 1)}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(analyse(p)), flush=True)
