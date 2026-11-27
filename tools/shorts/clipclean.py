"""Clean the image model's colour specks from finished animated clips, frame by frame, in place (original kept in clips/_orig/).
  python tools/shorts/clipclean.py <clip.mp4> [<clip.mp4> ...]
Use only on clips whose speck hits were reviewed by eye (tools/shorts/blobscan.py): it inpaints EVERY small isolated green/purple blob."""
import os, shutil, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from speck import despeck  # noqa: E402

for clip in sys.argv[1:]:
    d = os.path.join(os.path.dirname(clip), "_orig"); os.makedirs(d, exist_ok=True)
    src = os.path.join(d, os.path.basename(clip))
    if not os.path.exists(src): shutil.copy(clip, src)
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", src],
                        capture_output=True, text=True).stdout.strip().split(",")
    W, H, fps = int(pr[0]), int(pr[1]), pr[2]
    has_audio = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", src],
                                    capture_output=True, text=True).stdout.strip())
    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    tmp = clip + ".clean.mp4"
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", fps, "-i", "-"]
                           + (["-i", src, "-map", "0:v", "-map", "1:a", "-c:a", "copy"] if has_audio else [])
                           + ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        enc.stdin.write(despeck(np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()).tobytes()); n += 1
    dec.wait(); enc.stdin.close(); enc.wait(); os.replace(tmp, clip)
    print(f"cleaned {clip} ({n} frames)", flush=True)
