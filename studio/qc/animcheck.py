"""Frame-by-frame QC for AI-animated talking shots (LTX image+audio -> video).

Every frame:  jumps / single-frame flashes / flicker (frame differences + brightness), melting or blurred frames (sharpness).
4x a second:  people count + size (GroundingDINO), identity drift vs the first frame and the character's reference art (SigLIP),
              anatomy/glitch review by the vision model (Qwen3-VL) on numbered frame grids; every frame the numeric checks
              flagged is reviewed too, and every VLM report is re-confirmed on the full-size frame before it counts.
Lip-sync:     mouth-region motion (relative to the upper face, so head moves cancel out) vs the speech envelope:
              mouth must move while the line is spoken and settle when it stops; silent group shots must keep mouths still.

check_shot(...) -> {"findings": [{severity, frame, t, check, msg}], "score": int, "ok": bool}; results are cached per video hash."""
import hashlib, json, os, subprocess
import numpy as np

W, H = 640, 352                 # analysis resolution (keeps the face ~45 px tall in a medium shot)
VLM_FPS = 4.0
SEV_W = {"CRITICAL": 10, "HIGH": 3, "MEDIUM": 1, "LOW": 0}


def _probe_fps(v):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v],
                       capture_output=True, text=True).stdout.strip() or "24/1"
    a, b = r.split("/"); return float(a) / float(b or 1)


def frames(video, w=W, h=H):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def full_frame(video, n, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"select=eq(n\\,{n})", "-vsync", "0", "-frames:v", "1", out], check=True)
    return out


def _lap_var(g):
    k = g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    return float(k.var())


def _env(audio, fps, n):
    """Speech envelope per video frame (0..1)."""
    import soundfile as sf
    a, sr = sf.read(audio, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    hop = sr / fps
    e = np.array([np.sqrt(np.mean(a[int(i * hop):int((i + 1) * hop)] ** 2)) if int(i * hop) < len(a) else 0.0 for i in range(n)])
    return e / (e.max() + 1e-9)


def _f(sev, check, msg, frame=None, fps=24.0):
    return {"severity": sev, "check": check, "msg": msg, "frame": frame, "t": None if frame is None else round(frame / fps, 2)}


def _runs(idx, gap=2):
    """Group frame indices into (first, last) runs."""
    out = []
    for i in sorted(idx):
        if out and i - out[-1][1] <= gap: out[-1][1] = i
        else: out.append([i, i])
    return out


def _numeric(F, g, fps):
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))                       # d[k] = change from frame k to k+1
    med = float(np.median(d)) if len(d) else 0.0
    thr = max(3.0, 4 * med + 1.5)
    spikes = [k + 1 for k in range(len(d)) if d[k] > thr]
    flagged = set()
    for a, b in _runs(spikes, 1):
        k = a
        flash = 0 < k < len(g) - 1 and np.abs(g[k + 1] - g[k - 1]).mean() < 0.5 * d[k - 1]
        F.append(_f("HIGH", "glitch", f"{'single-frame flash' if flash else 'sudden jump'} at frames {a}-{b} "
                    f"(change {d[k - 1]:.1f} vs typical {med:.1f})", a, fps)); flagged.update(range(max(0, a - 1), b + 2))
    L = g.mean(axis=(1, 2)); dl = np.abs(np.diff(L))
    fl = [k + 1 for k in range(len(dl)) if dl[k] > 5.0]
    for a, b in _runs(fl, 2):
        F.append(_f("MEDIUM", "flicker", f"brightness jumps at frames {a}-{b}", a, fps)); flagged.update(range(a, b + 1))
    sh = np.array([_lap_var(x) for x in g]); smed = float(np.median(sh[3:])) if len(sh) > 4 else float(np.median(sh))
    blur = [k for k in range(3, len(sh)) if sh[k] < 0.45 * smed]
    for a, b in _runs(blur, 2):
        if b - a >= 1:
            F.append(_f("HIGH", "blur", f"blurred / melting frames {a}-{b} (sharpness {sh[a]:.0f} vs typical {smed:.0f})", a, fps))
            flagged.update(range(a, b + 1))
    return flagged


def _boxes(M, img, q, th):
    return [(s, b) for s, _, b in M.detect(img, q, th)]


def _lipsync(F, g, fps, faces, env, silent):
    """faces: {frame: (x0,y0,x1,y1)} at analysis resolution for the speaker (solo) or each face (group, list)."""
    if not faces: return
    ks = sorted(faces); n = len(g)
    def box_at(i):
        j = min(ks, key=lambda k: abs(k - i)); return faces[j]
    mouth, upper = np.zeros(n), np.zeros(n)
    for i in range(1, n):
        x0, y0, x1, y1 = [int(v) for v in box_at(i)]
        fh, fw = y1 - y0, x1 - x0
        if fh < 12 or fw < 10: continue
        my0, my1, mx0, mx1 = y0 + int(fh * 0.60), y0 + int(fh * 0.88), x0 + int(fw * 0.25), x0 + int(fw * 0.75)
        uy0, uy1 = y0 + int(fh * 0.15), y0 + int(fh * 0.45)
        mouth[i] = np.abs(g[i, my0:my1, mx0:mx1] - g[i - 1, my0:my1, mx0:mx1]).mean()
        upper[i] = np.abs(g[i, uy0:uy1, mx0:mx1] - g[i - 1, uy0:uy1, mx0:mx1]).mean()
    r = mouth / (upper + 0.6)
    if silent:
        if np.mean(r[1:]) > 1.8 and np.mean(mouth[1:]) > 1.2:
            F.append(_f("MEDIUM", "lipsync", f"mouth moves although nobody speaks in this shot (mouth/face motion {np.mean(r[1:]):.2f})", None, fps))
        return
    sp = env > 0.25
    sil = np.convolve(~sp, np.ones(int(fps * 0.3)), "same") >= int(fps * 0.3) - 1      # >= 0.3 s away from speech
    rs = float(np.mean(r[sp])) if sp.sum() > 5 else None
    rq = float(np.mean(r[sil])) if sil.sum() > 5 else None
    keeps = nofollow = False; c = None
    if rs is not None and np.mean(mouth[sp]) < 0.6:
        F.append(_f("HIGH", "lipsync", f"mouth barely moves while the line is spoken (mouth motion {np.mean(mouth[sp]):.2f})", None, fps))
    elif rs is not None and rq is not None and rq > 0.85 * rs and np.mean(mouth[sil]) > 1.0:
        keeps = True
    if sp.sum() > 10 and (~sp).sum() > 10 and np.std(r) > 0:
        c = float(np.corrcoef(r[1:], env[1:])[0, 1]); nofollow = c < 0.05
    # calibrated on a good shot (corr +0.32, mouth calmer in pauses) vs the same shot with reversed/shifted audio (both signs flip)
    if keeps and nofollow:
        F.append(_f("HIGH", "lipsync", f"lips do not match the speech: mouth moves in the pauses (silent {rq:.2f} vs speaking {rs:.2f}) "
                    f"and does not follow the voice (correlation {c:.2f})", None, fps))
    elif keeps:
        F.append(_f("MEDIUM", "lipsync", f"mouth keeps moving when the speech stops (silent {rq:.2f} vs speaking {rs:.2f})", None, fps))
    elif nofollow:
        F.append(_f("MEDIUM", "lipsync", f"lip movement does not follow the speech (correlation {c:.2f})", None, fps))


VLM_PROMPT = ("These are numbered frames (the number is in the top-left corner) from a short AI-animated clip in a clean editorial "
              "illustration style: {desc}. Inspect every frame carefully for GENERATION GLITCHES only: extra, missing or fused fingers, "
              "hands or limbs; distorted, melting, smeared or duplicated faces; eyes or mouth in the wrong place or deformed; body parts "
              "merging with the background or with objects; a person or object appearing, vanishing or changing identity/clothes; "
              "garbled text or letters; sudden style change. Do NOT report the illustration style itself, the slow camera push-in, "
              "normal talking, gestures or blinking.")
VLM_SCHEMA = '{"frames": [{"n": <frame number>, "severity": "high"|"medium"|"low", "problem": "<what is wrong, where>"}]}'


def _grid(imgs, labels, out, cols=3):
    from PIL import Image, ImageDraw
    w, h = imgs[0].size; rows = -(-len(imgs) // cols)
    G = Image.new("RGB", (w * cols, h * rows), (255, 255, 255)); d = ImageDraw.Draw(G)
    for k, (im, lb) in enumerate(zip(imgs, labels)):
        x, y = (k % cols) * w, (k // cols) * h; G.paste(im, (x, y))
        d.rectangle([x, y, x + 70, y + 34], fill=(0, 0, 0)); d.text((x + 8, y + 6), str(lb), fill=(255, 255, 0), font_size=24)
    G.save(out); return out


def check_shot(video, audio, desc, n_people, refs=(), silent=False, work=None, vlm=True, cfg=None, speaker_side=None, vlm_every=1):
    """video: the generated mp4; audio: the wav it was conditioned on; desc: who/what is in the shot; n_people: expected people;
    refs: reference images of the characters (identity); silent: True for listening/group shots."""
    from PIL import Image
    from . import models as M
    h = hashlib.md5(open(video, "rb").read()).hexdigest()[:16]
    cp = video + ".qc.json"
    if os.path.exists(cp):
        c = json.load(open(cp))
        if c.get("hash") == h and (c.get("vlm") or not vlm): return c
    work = work or os.path.dirname(video); os.makedirs(work, exist_ok=True)
    fps = _probe_fps(video)
    rgb = frames(video); g = rgb.astype(np.float32).mean(axis=3)
    n = len(g); F = []
    if n < 10:
        res = {"hash": h, "findings": [_f("CRITICAL", "glitch", f"clip has only {n} frames")], "score": 10, "ok": False, "vlm": vlm}
        json.dump(res, open(cp, "w"), indent=1); return res
    flagged = _numeric(F, g, fps)
    # sampled frames: people, identity, faces
    step = max(1, int(round(fps / VLM_FPS)))
    samp = list(range(0, n, step))
    if samp[-1] != n - 1: samp.append(n - 1)
    ims = {i: Image.fromarray(rgb[i]) for i in samp}
    counts, areas, faces = {}, {}, {}
    for i in samp:
        ppl = [b for s, b in _boxes(M, ims[i], "a person.", 0.35)]
        ppl = [b for b in ppl if (b[2] - b[0]) * (b[3] - b[1]) > 0.02 * W * H]
        counts[i] = len(ppl); areas[i] = max([(b[2] - b[0]) * (b[3] - b[1]) for b in ppl], default=0)   # largest box: nested duplicate boxes made false 'size jumps'
        fb = [b for s, b in _boxes(M, ims[i], "a human head.", 0.3) if (b[3] - b[1]) < 0.35 * H and (b[2] - b[0]) < 0.3 * W]
        if fb:
            if speaker_side and not silent:          # conversation two-shot: the speaker is the left- or right-most head
                faces[i] = (min if speaker_side == "left" else max)(fb, key=lambda b: (b[0] + b[2]) / 2)
            elif not silent: faces[i] = max(fb, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
            else: faces[i] = fb[0]
    wrong = [i for i in samp if counts[i] != n_people]
    if len(wrong) > 0.15 * len(samp):
        F.append(_f("HIGH", "people", f"expected {n_people} person(s) but saw {sorted({counts[i] for i in wrong})} in {len(wrong)}/{len(samp)} "
                    f"sampled frames (first at frame {wrong[0]})", wrong[0], fps)); flagged.update(wrong)
    a0 = float(np.median([a for a in areas.values() if a])) if any(areas.values()) else 1
    odd = [i for i in samp if areas[i] and not 0.6 <= areas[i] / a0 <= 1.7]
    if odd: F.append(_f("MEDIUM", "people", f"person size jumps (x{areas[odd[0]] / a0:.2f}) at frame {odd[0]}", odd[0], fps))
    emb = M.embed([ims[i] for i in samp])
    sims = emb @ emb[0]
    low = [samp[k] for k in range(len(samp)) if sims[k] < 0.86]
    if low:
        F.append(_f("HIGH", "identity", f"shot drifts away from its first frame (similarity {float(sims.min()):.2f}) from frame {low[0]}", low[0], fps))
        flagged.update(low)
    if refs and not silent:
        ref_imgs = []
        for r in refs:
            im = Image.open(r).convert("RGBA"); bg = Image.new("RGBA", im.size, (235, 235, 235, 255)); bg.alpha_composite(im); ref_imgs.append(bg.convert("RGB"))
        crops = []
        for i in samp:
            ppl = [b for s, b in _boxes(M, ims[i], "a person.", 0.35)]
            if ppl:
                b = max(ppl, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])); crops.append((i, ims[i].crop(tuple(int(v) for v in b))))
        if crops:
            e = M.embed([c for _, c in crops] + ref_imgs); ce, re_ = e[:len(crops)], e[len(crops):]
            s = (ce @ re_.T).max(axis=1); base = float(s[0])
            drop = [crops[k][0] for k in range(len(crops)) if s[k] < base - 0.10]
            if drop:
                F.append(_f("HIGH", "identity", f"character stops looking like their reference art (similarity {float(s.min()):.2f} vs {base:.2f}) "
                            f"from frame {drop[0]}", drop[0], fps)); flagged.update(drop)
    _lipsync(F, g, fps, faces, _env(audio, fps, n), silent)
    # vision model: every sampled frame + every flagged frame, 6 per grid, then confirm each report on the full frame
    if vlm:
        from .stage2 import ask
        model = (cfg or {}).get("vlm_model", "qwen/qwen3-vl-30b")
        todo = sorted(set(samp[::max(1, int(vlm_every))]) | {i for i in flagged if 0 <= i < n})   # vlm_every>1: fewer frames (faster)
        reports = []
        for k in range(0, len(todo), 6):
            chunk = todo[k:k + 6]
            gp = _grid([Image.fromarray(rgb[i]) for i in chunk], chunk, os.path.join(work, f"_grid_{h}_{k}.jpg"))
            try:
                r = ask(model, VLM_PROMPT.format(desc=desc), [gp], VLM_SCHEMA)
                for x in r.get("frames", []) if isinstance(r, dict) else []:
                    if isinstance(x, dict) and x.get("n") in chunk and x.get("severity") in ("high", "medium") and x.get("problem"):
                        reports.append(x)
            except Exception as e:
                F.append(_f("LOW", "vlm", f"vision check could not run on frames {chunk}: {e}"))
            finally:
                if os.path.exists(gp): os.remove(gp)
        seen = set()
        for x in sorted(reports, key=lambda x: x["severity"] != "high"):
            i = int(x["n"])
            if any(abs(i - j) <= step for j in seen): continue
            fp = full_frame(video, i, os.path.join(work, f"_f_{h}_{i}.png"))
            try:
                c = ask(model, f"A reviewer says this frame of an AI-animated illustration has a generation glitch: \"{x['problem']}\". "
                               "Look very carefully. Is that glitch really visible? Ignore the illustration style itself.", [fp],
                        '{"visible": true|false, "confidence": 0.0-1.0}')
                if bool(c.get("visible")) and float(c.get("confidence", 0)) >= 0.6:
                    F.append(_f("HIGH" if x["severity"] == "high" else "MEDIUM", "anatomy", x["problem"][:200], i, fps)); seen.add(i)
            except Exception:
                pass
            finally:
                if os.path.exists(fp): os.remove(fp)
    score = sum(SEV_W[f["severity"]] for f in F)
    res = {"hash": h, "findings": F, "score": score, "ok": not any(f["severity"] in ("CRITICAL", "HIGH") for f in F),
           "frames": n, "fps": fps, "vlm": vlm}
    json.dump(res, open(cp, "w"), indent=1)
    return res


def check_talkshots(pr, cache, cfg):
    """Main QC step: report the per-frame animation QC of every animated shot used in the video (talk/ANIMATION_QC.json)."""
    from .core import Finding
    rp = os.path.join(pr.dir, "talk", "ANIMATION_QC.json")
    if not os.path.exists(rp): return []
    used = {s["id"] for s in pr.scenes if (pr.props.get(s["id"]) or {}).get("shots")}
    out = []
    for r in json.load(open(rp)):
        if r["scene"] not in used or r["scene"] not in pr.start: continue
        for f in r["findings"]:
            if f["severity"] == "LOW": continue
            t = pr.start[r["scene"]] + r["start"] + (f.get("t") or 0)
            out.append(Finding("animation", f["severity"], f"animated shot {r['scene']} line {r['line']} ({f['check']}): {f['msg']}"
                               + (f" — best of {r['attempts']} attempts" if r["attempts"] > 1 else ""),
                               start=round(t, 2), scene=r["scene"], confidence=0.8,
                               recommendation="regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note"))
    return out
