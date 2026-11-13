"""Local repairs on still images: repaint only a small region (e.g. garbled AI text on a wall) instead of regenerating
the whole picture. ~20 s per region with Qwen-Image-Edit, and the rest of the image stays pixel-identical."""
import os
import numpy as np
from PIL import Image, ImageFilter
from . import config as C, imagegen

TEXT_FIX = ("Remove all writing, letters, numbers and signs' text from this picture; paint plain surface there instead "
            "(blank sign / plain wall / plain paper). Keep everything else exactly the same: same colours, outlines, shapes, "
            "lighting and flat cartoon style.")


def _crop_box(b, W, H, pad=0.6, min_side=384):
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    side_w = max(min_side, w * (1 + 2 * pad)); side_h = max(min_side, h * (1 + 2 * pad))
    X0 = int(max(0, min(W - side_w, cx - side_w / 2))); Y0 = int(max(0, min(H - side_h, cy - side_h / 2)))
    return X0, Y0, int(min(W, X0 + side_w)), int(min(H, Y0 + side_h))


def _merge(boxes, gap=40):
    """Merge nearby text boxes so one edit covers a whole sign."""
    boxes = [list(map(float, b)) for b in boxes]
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] - gap < b[2] and b[0] - gap < a[2] and a[1] - gap < b[3] and b[1] - gap < a[3]:
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                    del boxes[j]; changed = True; break
            if changed: break
    return boxes


def repaint(src, boxes, out, instruction=TEXT_FIX, work=None):
    """Repaint each (merged) box region of `src` with an edit instruction; feathered paste-back. Returns out."""
    im = Image.open(src).convert("RGB"); W, H = im.size
    work = work or os.path.join(os.path.dirname(out), "_repaint"); os.makedirs(work, exist_ok=True)
    for k, b in enumerate(_merge(boxes)):
        X0, Y0, X1, Y1 = _crop_box(b, W, H)
        crop = im.crop((X0, Y0, X1, Y1)); cw, ch = crop.size
        cp = os.path.join(work, f"crop{k}.png"); crop.save(cp)
        ew, eh = max(256, round(cw / 64) * 64), max(256, round(ch / 64) * 64)      # model-friendly size
        res = Image.open(imagegen.edit(instruction, [cp], work, f"rp{k}", ew, eh, fixed_size=True)).convert("RGB").resize((cw, ch), Image.LANCZOS)
        # feathered mask: the text box (+ margin) fully replaced, fading out towards the crop border
        m = Image.new("L", (cw, ch), 0); mx = int(max(12, (b[2] - b[0]) * 0.15)); my = int(max(12, (b[3] - b[1]) * 0.25))
        from PIL import ImageDraw
        ImageDraw.Draw(m).rectangle([b[0] - X0 - mx, b[1] - Y0 - my, b[2] - X0 + mx, b[3] - Y0 + my], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(max(6, min(mx, my))))
        im.paste(Image.composite(res, crop, m), (X0, Y0))
    im.save(out)
    return out


def garbled_text_boxes(path, min_h=38):
    """Big garbled (non-dictionary) text painted into an image -> list of (text, box)."""
    from .qc import models as M
    from .qc.stage1 import is_word, norm_words
    return [(t, bb) for t, bb in M.ocr(path) if bb[3] - bb[1] > min_h and any(not is_word(w) and len(w) >= 3 for w in norm_words(t))]
