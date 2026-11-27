"""On-screen Maya (host/narrator) design options, as character model sheets in the channel's style (2026-11-27).
  .venv/bin/python tools/maya_host_design.py            -> VIDEOS/_MAYA DESIGN OPTIONS/Maya option A..D.png
The owner picks one; it is then locked as library/show_refs/maya_host_sheet.png (and the project ref 'maya')."""
import os, shutil, sys
sys.argv = ["build.py", "insurance"]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shorts"))
import build as B  # noqa: E402  (chdir's to the repo root)

BASE = ("a friendly, confident, attractive young woman in her late twenties who is the host and narrator of a smart comedy explainer show, "
        "as a polished flat 2D vector cartoon character in the same style as a modern animated explainer: big expressive eyes, warm "
        "knowing half-smile, clean appealing proportions, tasteful and professional, ")
OPTIONS = {
    "A": "long wavy dark brown hair, gold hoop earrings, warm light-brown skin, olive-green overshirt over a cream top, dark trousers",
    "B": "sleek shoulder-length black bob with a side fringe, warm brown skin, small gold stud earrings, fitted navy blazer over a white t-shirt, slim trousers",
    "C": "long straight dark hair in a high ponytail, light olive skin, delicate gold necklace, mustard-yellow knit sweater, dark jeans",
    "D": "soft auburn curls just past the shoulders, light freckled skin, cream turtleneck under a camel coat, tortoiseshell glasses pushed up in her hair",
}
out = os.path.join("VIDEOS", "_MAYA DESIGN OPTIONS"); os.makedirs(out, exist_ok=True)
B.h3.free(); B.comfy.start()
for k, look in OPTIONS.items():
    p = os.path.join(out, f"Maya option {k}.png")
    if os.path.exists(p): continue
    got = B.imagegen.t2i(f"{B.STYLE} Character model sheet on a plain flat light grey background: the SAME character shown full body three times "
                         f"(front, three-quarter, side) plus a large head close-up with a warm smile. Consistent design in every view. "
                         f"No text. The character: {BASE}{look}.", out, f"maya_{k}", 1344, 768, seed=101 + ord(k))
    shutil.move(got, p); print("option", p, flush=True)
B.comfy.free()
