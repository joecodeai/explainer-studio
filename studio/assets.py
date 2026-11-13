"""Persistent asset library: character rigs (base + pose variants + mouth/eye anchors) and backgrounds.
A character is generated ONCE and reused in every future video (library/characters/<id>/)."""
import hashlib, json, os, re
import numpy as np
from PIL import Image
from . import config as C, imagegen

POSE_TEXT = {
    "neutral": "standing relaxed with arms at the sides, neutral expression",
    "point": "pointing to the side with one arm fully extended, explaining something, confident",
    "arms_up": "both arms raised high in excitement or panic, wide eyes",
    "shrug": "shrugging with both palms up, unsure expression",
    "facepalm": "facepalming with one hand over the eyes, embarrassed",
    "angry": "fists clenched, angry frown, leaning forward",
    "thinking": "one hand on the chin, thinking, eyes looking up",
    "talk": "one hand open in a natural explaining gesture, friendly expression",
    "happy": "big happy grin, relaxed open arms, cheerful",
    "surprised": "shocked surprised face, eyebrows raised high, wide eyes, hands up near the cheeks",
    "worried": "worried anxious expression, eyebrows tilted, hands clasped nervously",
    "side_talk": "body and head turned three-quarters to the RIGHT side of the image as if talking to someone standing on the right, one hand gesturing toward them",
    "side_listen": "body and head turned three-quarters to the RIGHT side of the image, listening attentively to someone on the right, arms relaxed, slight smile",
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]


def _detector():
    import torch
    from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
    mid = "IDEA-Research/grounding-dino-base"
    return AutoProcessor.from_pretrained(mid), AutoModelForZeroShotObjectDetection.from_pretrained(mid).to("cuda").eval()


def _boxes(det, img, query, th=0.25):
    import torch
    proc, model = det
    rgb = Image.new("RGB", img.size, (255, 255, 255)); rgb.paste(img, mask=img.split()[-1])
    x = proc(images=rgb, text=query, return_tensors="pt").to("cuda")
    with torch.no_grad(): o = model(**x)
    r = proc.post_process_grounded_object_detection(o, x.input_ids, threshold=th, text_threshold=0.2, target_sizes=[rgb.size[::-1]])[0]
    W, H = img.size
    return sorted([(float(s), [b[0] / W, b[1] / H, (b[2] - b[0]) / W, (b[3] - b[1]) / H]) for s, b in zip(r["scores"].tolist(), r["boxes"].tolist())], reverse=True)


def _skin(img, box):
    """Median colour of a ring just outside the box (what to paint over the drawn mouth/eyes)."""
    a = np.asarray(img.convert("RGBA")).astype(int); H, W = a.shape[:2]
    x, y, w, h = box
    x0, y0, x1, y1 = int((x - w * .35) * W), int((y - h * .35) * H), int((x + w * 1.35) * W), int((y + h * 1.35) * H)
    reg = a[max(0, y0):min(H, y1), max(0, x0):min(W, x1)].reshape(-1, 4)
    ix0, iy0 = int(x * W) - max(0, x0), int(y * H) - max(0, y0)
    reg = reg[reg[:, 3] > 200]
    if not len(reg): return "#f1c27d"
    m = np.median(reg[:, :3], axis=0).astype(int)
    return "#%02x%02x%02x" % tuple(m)


def _ensure_alpha(path, tmp, name):
    if imagegen.has_alpha(path):
        return path
    return imagegen.remove_bg(path, tmp, name + "_nobg")


def _crop(img):
    bb = img.split()[-1].point(lambda v: 255 if v > 20 else 0).getbbox()
    if bb:
        pad = 12; img = img.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(img.width, bb[2] + pad), min(img.height, bb[3] + pad)))
    return img


def build_character(c, poses=None, det=None):
    """c = {'id','name','look'} from the script. Returns path to rig.json (cached in the library)."""
    cid = slug(c["id"]); d = os.path.join(C.CHAR_LIB, cid); os.makedirs(os.path.join(d, "poses"), exist_ok=True)
    rig_path = os.path.join(d, "rig.json")
    rig = json.load(open(rig_path)) if os.path.exists(rig_path) else {"id": cid, "name": c["name"], "look": c["look"], "poses": {}}
    poses = poses or C.POSES
    base = os.path.join(d, "base.png")
    seed = int(hashlib.md5(cid.encode()).hexdigest()[:7], 16)
    if not os.path.exists(base):
        p = imagegen.t2i(f"{C.ART_STYLE}. {c['look']}. {POSE_TEXT['neutral']}. {C.CHAR_SUFFIX}", os.path.join(d, "_tmp"), "base", 896, 1344, seed=seed)
        p = _ensure_alpha(p, os.path.join(d, "_tmp"), "base")
        _crop(Image.open(p).convert("RGBA")).save(base)
    for pose in poses:
        out = os.path.join(d, "poses", f"{pose}.png")
        if os.path.exists(out) and pose in rig["poses"]: continue
        if not os.path.exists(out):
            if pose == "neutral":
                Image.open(base).save(out)
            else:
                p = imagegen.edit(f"The exact same cartoon character from image 1 — same face, hair, outfit, colours and art style — now "
                                  f"{POSE_TEXT[pose]}. Mouth closed (small simple closed mouth line). Full body, facing the viewer, isolated on a transparent background, no text.",
                                  [base], os.path.join(d, "_tmp"), pose, seed=seed + len(pose))
                p = _ensure_alpha(p, os.path.join(d, "_tmp"), pose)
                _crop(Image.open(p).convert("RGBA")).save(out)
        det = det or _detector()
        img = Image.open(out).convert("RGBA")
        mouth = _boxes(det, img, "mouth.", 0.22)
        eyes = [b for s, b in _boxes(det, img, "eye.", 0.22)][:2]
        mb = mouth[0][1] if mouth else None
        if mb and (mb[2] > 0.3 or mb[1] > 0.5): mb = None           # reject implausible mouth boxes
        eyes = [e for e in eyes if e[2] < 0.2 and e[1] < 0.45]
        if mb is None:                                              # beard / hidden mouth: place it from the face box
            face = [b for s, b in _boxes(det, img, "face.", 0.25) if b[1] < 0.5 and b[2] < 0.6]
            if face:
                fx, fy, fw, fh = face[0]
                mb = [fx + fw * 0.33, fy + fh * 0.68, fw * 0.34, fh * 0.12]
            elif len(eyes) == 2:
                ex = min(e[0] for e in eyes); ew = max(e[0] + e[2] for e in eyes) - ex; ey = max(e[1] + e[3] for e in eyes)
                mb = [ex + ew * 0.25, ey + ew * 0.45, ew * 0.5, ew * 0.18]
        rig["poses"][pose] = {"img": os.path.relpath(out, C.LIBRARY), "w": img.width, "h": img.height, "mouth": mb, "eyes": eyes,
                              "skin": _skin(img, mb) if mb else "#f1c27d",
                              "eye_skin": _skin(img, eyes[0]) if eyes else (_skin(img, mb) if mb else "#f1c27d")}
        json.dump(rig, open(rig_path, "w"), indent=1)
    close_mouths(cid)
    fix_anchors()
    return rig_path


def build_background(b):
    """b = {'id','prompt'}; cached by prompt hash so the same location is reused across videos."""
    if b.get("bg_file") and os.path.exists(b["bg_file"]): return b["bg_file"]      # locally repaired version (studio.repaint)
    key = slug(b["id"]) + "_" + hashlib.md5(b["prompt"].encode()).hexdigest()[:6]
    out = os.path.join(C.BG_LIB, key + ".png")
    if not os.path.exists(out):
        p = imagegen.t2i(f"{C.BG_STYLE}. {b['prompt']}", os.path.join(C.BG_LIB, "_tmp"), key, 1920, 1088)
        Image.open(p).convert("RGB").resize((C.W, C.H), Image.LANCZOS).save(out)
    return out


def mouth_open_score(img, box):
    """Fraction of very dark / mouth-red pixels in a region around the mouth anchor (open painted mouths score high)."""
    if not box: return 0.0
    a = np.asarray(img.convert("RGBA")).astype(int); H, W = a.shape[:2]
    x, y, w, h = box; w = max(w, 0.08)
    x0, x1 = int((x + box[2] / 2 - w * 0.6) * W), int((x + box[2] / 2 + w * 0.6) * W)
    y0, y1 = int((y - 0.01) * H), int((y + max(h, 0.02) + 0.06) * H)
    r = a[max(0, y0):min(H, y1), max(0, x0):min(W, x1)].reshape(-1, 4)
    r = r[r[:, 3] > 200]
    if not len(r): return 0.0
    lum = 0.3 * r[:, 0] + 0.59 * r[:, 1] + 0.11 * r[:, 2]
    cavity = (lum < 70) | ((r[:, 0] > 150) & (r[:, 1] < 80) & (r[:, 2] < 90))
    return float(cavity.mean())


def close_mouths(cid, threshold=0.17):
    """Redraw any pose of a library character whose painted mouth is open, with a closed mouth (same everything else)."""
    d = os.path.join(C.CHAR_LIB, cid); rig_path = os.path.join(d, "rig.json")
    if not os.path.exists(rig_path): return []
    rig = json.load(open(rig_path)); fixed = []
    det = None
    for pose, pz in rig["poses"].items():
        path = os.path.join(C.LIBRARY, pz["img"]); img = Image.open(path).convert("RGBA")
        sc = mouth_open_score(img, pz["mouth"])
        th = 0.09 if pose in ("arms_up", "surprised", "happy", "angry", "shrug", "point", "side_talk", "talk") else threshold   # expressive poses are usually drawn open-mouthed
        if sc < th or pz.get("mouth_closed"): continue
        p = imagegen.edit("Keep this cartoon character exactly the same — same pose, face, eyes, hair, outfit, colours and art style — "
                          "but change ONLY the mouth to a small simple CLOSED mouth line. Transparent background, no text.",
                          [path], os.path.join(d, "_tmp"), pose + "_closed", seed=7)
        p = _ensure_alpha(p, os.path.join(d, "_tmp"), pose + "_closed")
        _crop(Image.open(p).convert("RGBA")).save(path)
        det = det or _detector()
        img = Image.open(path).convert("RGBA")
        m = _boxes(det, img, "mouth.", 0.22); mb = m[0][1] if m and m[0][1][2] < 0.3 and m[0][1][1] < 0.5 else pz["mouth"]
        eyes = [e for s, e in _boxes(det, img, "eye.", 0.22)][:2] or pz["eyes"]
        pz.update(w=img.width, h=img.height, mouth=mb, eyes=eyes, mouth_closed=True, skin=_skin(img, mb) if mb else pz["skin"])
        fixed.append((pose, round(sc, 2)))
        json.dump(rig, open(rig_path, "w"), indent=1)
    return fixed


def sane_mouth(mouth, eyes, aspect=0.5, side=False):
    """Mouth anchor must sit below and between the eyes; otherwise estimate it from eye geometry.
    aspect = image width / height (boxes are fractions of width / height respectively)."""
    if len(eyes) < 2: return mouth
    ex0 = min(e[0] for e in eyes); ex1 = max(e[0] + e[2] for e in eyes); ey = max(e[1] + e[3] for e in eyes)
    span = ex1 - ex0; spy = span * aspect; cx = (ex0 + ex1) / 2
    est = [cx - span * 0.25, ey + spy * 0.52, span * 0.5, spy * 0.12]
    if not mouth: return est
    mx, my = mouth[0] + mouth[2] / 2, mouth[1] + mouth[3] / 2
    ok = abs(mx - cx) < span * (0.9 if side else 0.35) and ey + spy * 0.12 < my < ey + spy * 0.75 and mouth[2] < span * 0.8 and mouth[3] < spy * 0.3
    return mouth if ok else est


def _mouth_from_one_eye(img, eye):
    """Only one eye detected (e.g. a hand covers the other): face centre = middle of the opaque head at eye height."""
    import numpy as np
    a = np.asarray(img.split()[-1]); H, W = a.shape
    ey = min(H - 1, int((eye[1] + eye[3] / 2) * H))
    cols = np.where(a[ey] > 128)[0]
    if len(cols) < 2: cx, fw = eye[0] + eye[2] / 2, eye[2] * 4
    else:
        # keep the opaque run that contains the eye (the head), not arms/hands far away
        ex = int((eye[0] + eye[2] / 2) * W); runs = np.split(cols, np.where(np.diff(cols) > 3)[0] + 1)
        run = next((r for r in runs if r[0] <= ex <= r[-1]), cols)
        cx, fw = (run[0] + run[-1]) / 2 / W, (run[-1] - run[0]) / W
    my = eye[1] + eye[3] + fw * 0.33 * W / H
    return [cx - fw * 0.15, my, fw * 0.3, fw * 0.06 * W / H]


def fix_anchors():
    out = []
    for cid in sorted(os.listdir(C.CHAR_LIB)):
        rp = os.path.join(C.CHAR_LIB, cid, "rig.json")
        if not os.path.exists(rp): continue
        rig = json.load(open(rp)); changed = False
        for pose, pz in rig["poses"].items():
            # drop impossible eye boxes (the detector sometimes boxes the whole body or a hand)
            good = [e for e in pz["eyes"] if e[2] < 0.25 and e[3] < 0.08 and e[1] < 0.45 and e[0] >= 0 and e[0] + e[2] <= 1]
            bad_mouth = not pz["mouth"] or not (0 <= pz["mouth"][1] <= 0.5 and 0 <= pz["mouth"][0] <= 1)
            if good != pz["eyes"] or bad_mouth:
                pz["eyes"] = good; pz["mouth_est"] = True; changed = True; pz.pop("talk", None)
                if len(good) == 1 and not pose.startswith("side_"):
                    img = Image.open(os.path.join(C.LIBRARY, pz["img"])).convert("RGBA")
                    pz["mouth"] = _mouth_from_one_eye(img, good[0]); pz["skin"] = _skin(img, pz["mouth"])
                    out.append((cid, pose)); continue
            m2 = sane_mouth(None if pz.get("mouth_est") else pz["mouth"], pz["eyes"], pz["w"] / pz["h"], pose.startswith("side_"))
            if m2 != pz["mouth"] and len(pz["eyes"]) >= 2: pz["mouth_est"] = True
            if m2 is None and pz["eyes"]:      # side pose with one eye left after filtering
                m2 = _mouth_from_one_eye(Image.open(os.path.join(C.LIBRARY, pz["img"])).convert("RGBA"), pz["eyes"][0])
            if m2 is not None and not (0 <= m2[1] <= 0.6 and 0 <= m2[0] <= 1): m2 = None
            if m2 != pz["mouth"]:
                img = Image.open(os.path.join(C.LIBRARY, pz["img"])).convert("RGBA")
                pz["mouth"] = m2; changed = True; out.append((cid, pose))
                if m2: pz["skin"] = _skin(img, m2)
        if changed: json.dump(rig, open(rp, "w"), indent=1)
    return out


def nomouth(img_path, mouth, pad_x=0.25, pad_y=0.6):
    """Copy of a pose image with the painted mouth removed (OpenCV inpaint from the surrounding skin/beard),
    shown while the character speaks so only the animated mouth is ever visible. Cached next to the source."""
    import cv2, numpy as np
    out = img_path[:-4] + "_nm.png"
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(img_path):
        return out
    im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    H, W = im.shape[:2]
    x, y, w, h = mouth
    x0, x1 = int((x - w * pad_x) * W), int((x + w * (1 + pad_x)) * W)
    y0, y1 = int((y - h * pad_y) * H), int((y + h * (1 + pad_y)) * H)
    mask = np.zeros((H, W), np.uint8)
    cv2.ellipse(mask, ((x0 + x1) // 2, (y0 + y1) // 2), (max(2, (x1 - x0) // 2), max(2, (y1 - y0) // 2)), 0, 0, 360, 255, -1)
    rgb = np.ascontiguousarray(im[:, :, :3])
    fixed = cv2.inpaint(rgb, mask, 3, cv2.INPAINT_TELEA)
    if im.shape[2] == 4:
        fixed = np.dstack([fixed, im[:, :, 3]])
    cv2.imwrite(out, fixed)
    return out


def find_mouth(img_path, eyes, rough=None):
    """Locate the PAINTED mouth precisely: the dark, horizontal stroke/blob below the eyes (not the nose, not the
    face outline). Returns [x,y,w,h] fractions or None. Used to place the animated mouth and to erase the painted one."""
    import cv2, numpy as np
    im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    H, W = im.shape[:2]
    if not eyes:
        return None
    ex0 = min(e[0] for e in eyes) * W; ex1 = max(e[0] + e[2] for e in eyes) * W
    ew = max(e[2] for e in eyes) * W
    ey = max(e[1] + e[3] for e in eyes) * H
    span = max(ex1 - ex0, ew * 3.2)
    cx = (ex0 + ex1) / 2
    side = len(eyes) == 1
    rx0, rx1 = int(max(0, cx - span * (0.95 if side else 0.7))), int(min(W, cx + span * (0.95 if side else 0.7)))
    ry0, ry1 = int(min(H - 1, ey + span * 0.08)), int(min(H, ey + span * 1.05))
    if rx1 - rx0 < 10 or ry1 - ry0 < 10:
        return None
    reg = im[ry0:ry1, rx0:rx1]
    gray = cv2.cvtColor(np.ascontiguousarray(reg[:, :, :3]), cv2.COLOR_BGR2GRAY)
    dark = (gray < 95).astype(np.uint8)
    if reg.shape[2] == 4:
        dark &= (reg[:, :, 3] > 200).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
    best, bs = None, -1e9
    rh, rw = dark.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < max(12, span * 0.02) or x <= 1 or y <= 1 or x + w >= rw - 1 or y + h >= rh - 1:
            continue                       # noise, or touches the region edge (face outline, collar, hair)
        if w < h * 0.9 or w > span * 0.95 or w < span * 0.08:
            continue                       # vertical strokes = nose / chin lines
        mx = rx0 + x + w / 2
        score = w - abs(mx - cx) * (0.3 if side else 0.8) - y * 0.15
        if score > bs:
            bs, best = score, (rx0 + x, ry0 + y, w, h)
    if not best:
        return None
    x, y, w, h = best
    return [x / W, y / H, w / W, h / H]


TALK_PROMPTS = {
    "mid": "Keep this cartoon character EXACTLY the same — same pose, head position, face, eyes, eyebrows, hair, outfit, colours, "
           "line art and framing. Change ONLY the mouth: slightly open, mid-word while talking (small dark opening). White background, no text.",
    "open": "Keep this cartoon character EXACTLY the same — same pose, head position, face, eyes, eyebrows, hair, outfit, colours, "
            "line art and framing. Change ONLY the mouth: open wide while talking, saying 'ah' (dark mouth opening, tongue visible). White background, no text.",
}


def _face_window(pz, W, H):
    eyes = pz.get("eyes") or []
    if not eyes:
        return None
    ex0 = min(e[0] for e in eyes) * W; ex1 = max(e[0] + e[2] for e in eyes) * W
    ew = max(e[2] for e in eyes) * W; ey = max(e[1] + e[3] for e in eyes) * H
    span = max(ex1 - ex0, ew * 3.2); cx = (ex0 + ex1) / 2
    k = 1.25 if len(eyes) == 1 else 0.9
    return int(max(0, cx - span * k)), int(max(0, ey)), int(min(W, cx + span * k)), int(min(H, ey + span * (1.9 if len(eyes) == 1 else 1.4)))


def talk_frames(cid, poses=None, det=None):
    """For each pose make mouth-only variants (mid / open) of the SAME drawing: a Qwen edit, aligned to the original
    and pasted back only where the face window changed. While speaking the renderer swaps between closed/mid/open
    images, so the painted mouth itself moves and there is never a second mouth on top."""
    import cv2, numpy as np
    d = os.path.join(C.CHAR_LIB, cid); rp = os.path.join(d, "rig.json")
    if not os.path.exists(rp): return []
    rig = json.load(open(rp)); made = []
    for pose, pz in rig["poses"].items():
        if poses and pose not in poses: continue
        src = os.path.join(C.LIBRARY, pz["img"])
        talk = pz.get("talk") or {}
        if all(k in talk and os.path.exists(os.path.join(C.LIBRARY, talk[k])) and
               os.path.getmtime(os.path.join(C.LIBRARY, talk[k])) >= os.path.getmtime(src) for k in TALK_PROMPTS):
            continue
        orig = cv2.imread(src, cv2.IMREAD_UNCHANGED)
        H, W = orig.shape[:2]
        win = _face_window(pz, W, H)
        if not win: continue
        a = orig[:, :, 3:4].astype(np.float32) / 255 if orig.shape[2] == 4 else np.ones((H, W, 1), np.float32)
        flat = (orig[:, :, :3].astype(np.float32) * a + 255 * (1 - a)).astype(np.uint8)
        tmp = os.path.join(d, "_tmp"); os.makedirs(tmp, exist_ok=True)
        fp = os.path.join(tmp, f"{pose}_flat.png"); cv2.imwrite(fp, flat)
        x0, y0, x1, y1 = win
        talk = {}
        for kind, prompt in TALK_PROMPTS.items():
            ok = False
            for seed in (11, 23):
                p = imagegen.edit(prompt, [fp], tmp, f"{pose}_{kind}", seed=seed)
                ed = cv2.resize(cv2.imread(p, cv2.IMREAD_COLOR), (W, H), interpolation=cv2.INTER_AREA)
                # align the edit to the original (the model can shift the drawing by a few pixels)
                g0 = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY).astype(np.float32); g1 = cv2.cvtColor(ed, cv2.COLOR_BGR2GRAY).astype(np.float32)
                (dx, dy), _ = cv2.phaseCorrelate(g0, g1)
                ed = cv2.warpAffine(ed, np.float32([[1, 0, -dx], [0, 1, -dy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
                diff = cv2.absdiff(ed, flat).max(axis=2)
                m = np.zeros((H, W), np.uint8)
                m[y0:y1, x0:x1] = (diff[y0:y1, x0:x1] > 40).astype(np.uint8) * 255
                m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
                if n < 2: continue
                big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))      # the mouth = biggest changed blob in the face window
                m = (lab == big).astype(np.uint8) * 255
                bx, by, bw, bh, area = st[big]
                frac = area / max(1, (x1 - x0) * (y1 - y0))
                if frac < 0.004 or frac > 0.35 or bw > (x1 - x0) * 0.8: continue
                m = cv2.dilate(m, np.ones((9, 9), np.uint8))
                mf = cv2.GaussianBlur(m, (0, 0), 2.5).astype(np.float32)[:, :, None] / 255
                out = orig.copy()
                out[:, :, :3] = (ed.astype(np.float32) * mf + orig[:, :, :3].astype(np.float32) * (1 - mf)).astype(np.uint8)
                rel = os.path.join(os.path.dirname(pz["img"]), f"{pose}_{kind}.png")
                cv2.imwrite(os.path.join(C.LIBRARY, rel), out)
                talk[kind] = rel; ok = True
                break
            if not ok: break
        if len(talk) == len(TALK_PROMPTS):
            pz["talk"] = talk; made.append(pose)
        else:
            pz.pop("talk", None)
        json.dump(rig, open(rp, "w"), indent=1)
    return made
