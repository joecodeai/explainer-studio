"""Two live progress bars: the current video and all videos in the batch, with time remaining. Ctrl+C to quit."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import progress


def bar(f, w=40):
    f = max(0.0, min(1.0, f)); n = int(f * w)
    return "█" * n + "░" * (w - n)


def hms(s):
    s = int(max(0, s)); h, m = divmod(s // 60, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m {s % 60:02d}s"


LABEL = {"script": "writing script", "voice": "voices", "assets": "characters & backgrounds", "hero": "AI hero shots", "talk": "animated talking shots", "sound": "music & sfx",
         "render": "rendering scenes", "master": "mixing & master", "qc": "quality check + auto-fix", "reel": "instagram reel", "done": "finished"}
first = True
while True:
    s = progress.snapshot()
    name = (s["video"] or "—")[:52]
    lines = [f" This video  {bar(s['video_frac'])} {s['video_frac'] * 100:5.1f}%  ~{hms(s['video_left'])} left",
             f"   {name}  ·  {LABEL.get(s['stage'], s['stage'] or '')}",
             f" All videos  {bar(s['all_frac'])} {s['all_frac'] * 100:5.1f}%  ~{hms(s['all_left'])} left",
             f"   {s['done']} of {s['total']} done"]
    if not first: sys.stdout.write("\033[4F")
    sys.stdout.write("\n".join(l + "\033[K" for l in lines) + "\n"); sys.stdout.flush(); first = False
    if s["total"] and s["done"] >= s["total"] and s["all_frac"] >= 1: print(" ✅ all done"); break
    time.sleep(2)
