"""Stage 2: vision-language review (Qwen3-VL-30B in LM Studio) — only where it is needed:
  * every character pose used (anatomy, hands, face, mouth frames, outfit/identity vs the character's reference)
  * every background used (distortion, garbled text, floating objects, open floor where characters stand)
  * every AI hero shot (anatomy, garbled text, artefacts)
  * one representative frame per scene (does the picture match the narration? physical plausibility)
  * escalations from stage 1 (e.g. floor not detected under a character's feet)
Results are cached by image hash. High-severity asset defects are re-asked once (confirmation) before auto-fixing."""
import base64, io, json, os, re, subprocess, time
import numpy as np
import requests
from PIL import Image, ImageDraw
from .core import Finding, W, H, FEET_Y, file_hash, log, pos_x, proj_path, state_at, CHAR_H
from . import models as M
from .stage1 import frame_at, silhouette
from .. import config as C, llm

SEV = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}
SYS = ("You are a meticulous quality-control inspector for 2D cartoon explainer videos (flat style, bold outlines, simple "
       "rounded characters with small dot eyes). The cartoon style itself is intentional: simplified hands, big heads, dot eyes "
       "and missing noses are NOT defects. Report only real, visible defects. Be precise and do not invent problems.")
ISSUES_SCHEMA = '{"issues": [{"category": "anatomy|identity|physical|objects|visual|text|semantic|continuity", "severity": "critical|high|medium|low", "description": "...", "fix": "..."}]}'


def _ensure(model):
    llm.ensure_loaded()   # starts the LM Studio service if needed
    ps = llm._lms("ps").stdout
    if model not in ps:
        llm._lms("unload", "--all")
        r = llm._lms("load", model, "--gpu", "max", "--context-length", "16384", "-y")
        if r.returncode != 0: raise RuntimeError(f"cannot load {model}: {r.stderr or r.stdout}")


def _b64(img, maxside=1024):
    if isinstance(img, str): img = Image.open(img)
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255)); bg.paste(img, mask=img.split()[-1]); img = bg
    img = img.convert("RGB"); img.thumbnail((maxside, maxside))
    b = io.BytesIO(); img.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def ask(model, prompt, images, schema_hint=ISSUES_SCHEMA, retries=2):
    _ensure(model)
    content = [{"type": "image_url", "image_url": {"url": _b64(i)}} for i in images] + \
              [{"type": "text", "text": prompt + "\n\nReply with ONLY a JSON object of this form: " + schema_hint}]
    body = {"model": model, "temperature": 0.1, "max_tokens": 1500,
            "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": content}]}
    last = None
    for _ in range(retries + 1):
        try:
            r = requests.post(f"{C.LLM_URL}/chat/completions", json=body, timeout=600); r.raise_for_status()
            txt = r.json()["choices"][0]["message"].get("content") or ""
            txt = re.sub(r"<think>.*?</think>", "", txt, flags=re.S)
            i = txt.find("{")
            return json.JSONDecoder().raw_decode(txt[i:])[0]
        except Exception as e:
            last = e; time.sleep(1)
    raise RuntimeError(f"VLM failed: {last}")


NONDEFECT = re.compile(r"not a defect|is intentional|intentional(ly)? (stylis|for)|consistent with the (flat )?cartoon style|clearly conveys|"
                       r"is coherent|no visible (text|defect)|which is (a )?plausible|effectively conveys|may be intentional", re.I)


def _issues(cache, ns, key, model, prompt, images):
    hit = cache.get(ns, key)
    if hit is None:
        try: hit = ask(model, prompt, images).get("issues", [])
        except Exception as e: hit = [{"category": "visual", "severity": "low", "description": f"VLM check could not run: {e}", "fix": ""}]
        cache.put(ns, key, hit)
    # the VLM sometimes "reports" things it then says are fine / intentional — drop those
    return [i for i in hit if isinstance(i, dict) and i.get("description") and not NONDEFECT.search(i["description"])]


def _confirm(model, desc, images, cache, key):
    hit = cache.get("vlm_confirm", key)
    if hit is None:
        try:
            r = ask(model, f"A reviewer reported this defect: \"{desc}\". Look very carefully. Is this defect really visible in the image? "
                           "Ignore intentional cartoon simplification.", images, '{"visible": true|false, "confidence": 0.0-1.0}')
            hit = bool(r.get("visible")) and float(r.get("confidence", 0)) >= 0.6
        except Exception:
            hit = False
        cache.put("vlm_confirm", key, hit)
    return hit


def _triptych(paths):
    ims = [Image.open(p).convert("RGBA") for p in paths]
    h = max(i.height for i in ims); out = Image.new("RGB", (sum(int(i.width * h / i.height) for i in ims) + 20 * (len(ims) - 1), h), "white")
    x = 0
    for i in ims:
        j = i.resize((int(i.width * h / i.height), h)); bg = Image.new("RGB", j.size, "white"); bg.paste(j, mask=j.split()[-1])
        out.paste(bg, (x, 0)); x += j.width + 20
    return out


# ---------------------------------------------------------------- assets
def check_assets(pr, cache, cfg):
    model = cfg["vlm_model"]; res = []
    # characters: every pose used in this video, with its mouth frames, next to the character's reference pose
    used = {}
    for s in pr.scenes:
        p = pr.props[s["id"]]
        for m in p.get("cast", []):
            for t in [l["start"] + 0.3 for l in p["lines"]] + [(l["start"] + l["end"]) / 2 for l in p["lines"]]:
                st = state_at(m, p["cast"], p["lines"], t)
                used.setdefault((m["char"], st["pose"]), (m, s["id"], pr.start[s["id"]] + t))
    log(pr.dir, f"VLM: {len(used)} character poses")
    for (char, pose), (m, sid, t) in used.items():
        pz = m["poses"][pose]; files = [proj_path(pr.dir, pz["img"])] + [proj_path(pr.dir, v) for v in (pz.get("talk") or {}).values()]
        ref = m["poses"].get("neutral") or next(iter(m["poses"].values()))
        img = _triptych(files)
        key = "|".join(file_hash(f) for f in files)
        prompt = (f"Image: the cartoon character '{char}' in pose '{pose}'" + (" shown three times: mouth closed, half open, wide open (these are "
                  "lip-sync frames of the same drawing — only the mouth should differ)" if len(files) > 1 else "") + ". "
                  "Check anatomy: number of arms/legs/hands, fingers (cartoon hands with 4-5 fingers are fine), deformed or duplicated "
                  "body parts, distorted face, eyes, mouth (a mouth frame must look like a mouth, one mouth only), neck/shoulders, "
                  "limbs passing through clothing, objects held correctly (hand around a cup/tablet), anything floating.")
        for i in _issues(cache, "vlm_pose", key, model, prompt, [img]):
            sev = SEV.get(str(i.get("severity", "")).lower(), "LOW")
            f = Finding("anatomy", sev, f"{char} / {pose}: {i['description']}", start=t, scene=sid, confidence=0.6, source="stage2",
                        recommendation=i.get("fix", ""))
            if sev in ("CRITICAL", "HIGH") and _confirm(model, i["description"], [img], cache, key + i["description"][:60]):
                f.confidence = 0.85; f.fix = "fix_pose"; f.fix_args = {"char": char, "pose": pose, "problem": i["description"]}
            res.append(f)
        # identity: embeddings first, VLM only if the pose drifts from the reference
        if pose != "neutral" and ref is not m["poses"][pose]:
            e = M.embed([proj_path(pr.dir, ref["img"]), files[0]]); simv = float(e[0] @ e[1])
            if simv < 0.80:
                pair = _triptych([proj_path(pr.dir, ref["img"]), files[0]])
                for i in _issues(cache, "vlm_ident", key + "id", model,
                                 f"Left: reference drawing of '{char}'. Right: the same character in pose '{pose}'. Is it clearly the SAME character "
                                 "(same face, hair, colours, outfit, accessories, age, body proportions)? Report only identity/outfit differences.", [pair]):
                    res.append(Finding("identity", SEV.get(str(i.get("severity", "")).lower(), "MEDIUM"), f"{char} / {pose}: {i['description']}",
                                       start=t, scene=sid, confidence=0.6, source="stage2", fix="fix_pose",
                                       fix_args={"char": char, "pose": pose, "problem": i["description"], "match_reference": True}))
    # backgrounds
    for bg in sorted({p["background"] for p in pr.props.values() if p.get("kind") == "stage" and p.get("background")}):
        f = proj_path(pr.dir, bg); sid = next(s["id"] for s in pr.scenes if pr.props[s["id"]].get("background") == bg)
        env = next((s.get("environment") for s in pr.scenes if s["id"] == sid), None)
        for i in _issues(cache, "vlm_bg2", file_hash(f), model,
                         "This is an empty background for a cartoon scene (characters are added later). Report only real defects: "
                         "distorted or impossible architecture (warped windows/doors/walls), wrong perspective, objects floating or passing "
                         "through each other, garbled/nonsense writing on signs or boards.", [f]):
            sev = SEV.get(str(i.get("severity", "")).lower(), "LOW")
            res.append(Finding("continuity", sev, f"background {os.path.basename(bg)}: {i['description']}", scene=sid, start=pr.start[sid],
                               confidence=0.6, source="stage2", fix="regen_background" if sev in ("CRITICAL", "HIGH") else None, fix_args={"env": env}))
        fl = cache.get("vlm_bgfloor", file_hash(f))
        if fl is None:
            try:
                fl = ask(model, "Look at the bottom third of this background image. Is there a clear, empty area of floor or ground there, "
                         "wide enough for two people to stand side by side, with no tables, chairs, desks, counters or shelves in it?",
                         [f], '{"open_floor": true|false, "what_blocks_it": "...", "confidence": 0.0-1.0}')
            except Exception as e:
                fl = {"open_floor": True, "confidence": 0, "error": str(e)}
            cache.put("vlm_bgfloor", file_hash(f), fl)
        if fl.get("open_floor") is False and float(fl.get("confidence", 0)) >= 0.7:
            res.append(Finding("physical", "HIGH", f"background {os.path.basename(bg)}: no open floor for the characters ({fl.get('what_blocks_it', '')})",
                               scene=sid, start=pr.start[sid], confidence=0.75, source="stage2", fix="regen_background", fix_args={"env": env}))
    # hero shots
    for s in pr.scenes:
        if s["kind"] != "hero": continue
        src = os.path.join(pr.dir, "hero", f"{s['id']}.mp4")      # the raw AI clip: no subtitles / keywords on top
        if not os.path.exists(src): continue
        from .core import probe_dur
        img = frame_at(src, probe_dur(src) * 0.4)
        if img is None: continue
        im = Image.fromarray(img)
        for i in _issues(cache, "vlm_hero", file_hash(src), model,
                         f"A cinematic cartoon shot meant to show: \"{s.get('hero_prompt', '')}\". Report "
                         "anatomy defects (extra/missing limbs or fingers, melted faces), garbled text or fake writing, watermarks, "
                         "rendering artefacts, objects merging into each other, and whether it clearly shows the intended idea.", [im]):
            sev = SEV.get(str(i.get("severity", "")).lower(), "LOW")
            ok = sev in ("CRITICAL", "HIGH") and _confirm(model, i["description"], [im], cache, file_hash(src) + i["description"][:60])
            res.append(Finding("visual" if i.get("category") != "semantic" else "semantic", sev if ok or sev not in ("CRITICAL", "HIGH") else "MEDIUM",
                               f"hero shot: {i['description']}", start=pr.start[s["id"]], end=pr.start[s["id"]] + pr.dur[s["id"]], scene=s["id"],
                               confidence=0.85 if ok else 0.5, source="stage2", fix="regen_hero" if ok else None, fix_args={"scene": s["id"]}))
    return res


# ---------------------------------------------------------------- scenes (semantic + physical plausibility)
def check_scenes(pr, cache, cfg, unknown_floor=()):
    model = cfg["vlm_model"]; res = []
    envs = {e["id"]: e for e in pr.script.get("environments", [])}
    chars = {c["id"]: c for c in pr.script.get("characters", [])}
    for s in pr.scenes:
        if s["kind"] not in ("stage", "map"): continue
        p = pr.props[s["id"]]; line = p["lines"][0] if p["lines"] else None
        t = (line["start"] + line["end"]) / 2 if line else pr.dur[s["id"]] / 2
        img = frame_at(pr.render[s["id"]], t)
        if img is None: continue
        im = Image.fromarray(img)
        narr = " ".join(l["text"] for l in s.get("lines", []))[:600]
        if s["kind"] == "stage":
            who = "; ".join(f"{c['char']} ({chars.get(c['char'], {}).get('look', '')[:60]})" for c in p["cast"])
            prompt = (f"Scene from an explainer video. Intended location: {envs.get(s.get('environment'), {}).get('prompt', '')[:200]}. "
                      f"Characters: {who}. Dialogue: \"{narr}\". Check physical positioning (characters standing ON the floor, not floating, "
                      "not sinking, not standing inside/through furniture, not overlapping each other, feet touching the ground, correct "
                      "scale/perspective vs the room), objects resting on surfaces, and whether the location and characters fit the "
                      "dialogue. Ignore the subtitle bar and big comic-style keyword text (intentional).")
        else:
            prompt = (f"A map scene titled '{p['map'].get('label', '')}' that should show: {', '.join(x['name'] for x in p['map'].get('places', []))}. "
                      f"Narration: \"{narr}\". Check that the geography shown is plausible for these places, labels are readable and not "
                      "overlapping, and nothing is garbled. Ignore the subtitle bar.")
        for i in _issues(cache, "vlm_scene", pr.render_hash(s["id"]) + ":" + str(round(t, 2)), model, prompt, [im]):
            cat = i.get("category", "semantic"); cat = cat if cat in ("physical", "objects", "semantic", "continuity", "text", "visual") else "semantic"
            sev = SEV.get(str(i.get("severity", "")).lower(), "LOW")
            res.append(Finding(cat, sev, f"{s['id']}: {i['description']}", start=pr.start[s["id"]] + t, scene=s["id"], confidence=0.5,
                               source="stage2", recommendation=i.get("fix", "")))
    # escalation: floor under the feet could not be segmented -> ask with the feet marked
    for sid, who in unknown_floor:
        s = next(x for x in pr.scenes if x["id"] == sid); p = pr.props[sid]
        bg = Image.open(proj_path(pr.dir, p["background"])).convert("RGB").resize((W, H)); d = ImageDraw.Draw(bg)
        m = next(c for c in p["cast"] if c["char"] == who)
        st = state_at(m, p["cast"], p["lines"], 0.5); sil, feet = silhouette(pr, m["poses"][st["pose"]], W * pos_x(m), H * FEET_Y, st["flip"])
        ys, xs = np.where(sil)
        if len(xs): d.rectangle([xs.min(), ys.min(), xs.max(), ys.max()], outline=(255, 0, 0), width=6)
        for x, y in feet: d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 0, 0))
        r = cache.get("vlm_floor", file_hash(proj_path(pr.dir, p["background"])) + f":{pos_x(m):.3f}")
        if r is None:
            try:
                r = ask(cfg["vlm_model"], "The red rectangle is where a cartoon character will stand; the red dots are their feet. Are the red dots on "
                        "walkable floor/ground that is visible and unobstructed, and is nothing (table, chair, desk, counter) standing in front of "
                        "the rectangle closer to the viewer?", [bg], '{"feet_on_floor": true|false, "blocked_by": "object name or empty", "confidence": 0.0-1.0}')
            except Exception as e:
                r = {"feet_on_floor": True, "blocked_by": "", "confidence": 0, "error": str(e)}
            cache.put("vlm_floor", file_hash(proj_path(pr.dir, p["background"])) + f":{pos_x(m):.3f}", r)
        if (not r.get("feet_on_floor", True) or r.get("blocked_by")) and float(r.get("confidence", 0)) >= 0.5:
            res.append(Finding("physical", "HIGH", f"{who} is not standing on open floor" + (f" (blocked by {r['blocked_by']})" if r.get("blocked_by") else ""),
                               start=pr.start[sid], end=pr.start[sid] + pr.dur[sid], scene=sid, confidence=0.7, source="stage2",
                               fix="reposition", fix_args={"scene": sid, "env": s.get("environment")}))
    return res
