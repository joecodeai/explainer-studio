"""End-to-end production v2: research -> script (approval gate) -> voices -> assets -> hero shots -> sound -> render -> QC/repair -> master.
Every stage is cached in projects/<slug>/; rerunning resumes and only redoes what changed."""
import glob, sys, hashlib, json, math, os, re, shutil, subprocess, time
import numpy as np, soundfile as sf
from . import ending, assets, audio, comfy, config as C, hero, llm, news, progress, script, talk, voice

ACCENTS = ["#ffd23f", "#4cc9f0", "#ff7aa8", "#80ed99", "#ff9f1c"]
SPEAKER_COLORS = ["#4cc9f0", "#ff7aa8", "#80ed99", "#ff9f1c", "#c77dff", "#ffd23f"]
ROUTE_COLORS = ["#2a9d8f", "#e76f51", "#3a86ff", "#8338ec"]
XFADE = {"slide": ("slideleft", 0.45), "zoom": ("circleopen", 0.5), "wipe": ("wiperight", 0.45), "whip": ("smoothleft", 0.3),
         "fade": ("fade", 0.5), "cut": ("fade", 0.04)}
TAIL = 0.25          # seconds of breathing room after the last line of a scene


def log(proj, msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    open(os.path.join(proj, "production.log"), "a").write(line + "\n")


def project_dir(topic):
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50] or "video"
    d = os.path.join(C.PROJECTS, slug)
    for sub in ("audio", "public", "renders", "props", "hero", "work"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    return d


def _j(path, data=None):
    if data is None:
        return json.load(open(path)) if os.path.exists(path) else None
    json.dump(data, open(path, "w"), indent=1, ensure_ascii=False)
    return data


# ---------------------------------------------------------------- 1-3: research, script, approval
def stage_script(proj, topic, minutes):
    res = _j(f"{proj}/research.json") or _j(f"{proj}/research.json", news.research(topic))
    log(proj, f"research: {len(res['sources'])} sources")
    sc = _j(f"{proj}/script.json")
    if not sc:
        sh = script.load_show()      # recurring show (library/show.json); PLAIN=1 for a plain explainer
        sc = script.write_episode(res, minutes, sh) if sh else script.write(res, minutes)
        _j(f"{proj}/script.draft.json", sc)
        for _ in range(1):
            if not sc["_problems"]: break
            log(proj, f"script problems -> repairing: {sc['_problems'][:5]}")
            sc = script.repair(sc, script.show_system(sh) if sh else None)
            if sh: sc = script.apply_show(sc, sh)
        _j(f"{proj}/script.json", sc)
    if "seo" not in sc:
        try:
            txt = llm.chat([{"role": "user", "content": "Write YouTube metadata for this explainer video, in EXACTLY this plain-text format:\n"
                "TITLE: <max 70 chars, curiosity-driven but accurate>\nDESCRIPTION: <2 short engaging paragraphs on one line>\n"
                "TAGS: <20 comma-separated lowercase search keywords>\nHASHTAGS: <3 hashtags>\n\nVideo: " + sc["title"] + "\nScript: " +
                " ".join(x["narration"] for x in sc["scenes"])[:6000]}], temperature=0.6, max_tokens=900)
            g = lambda k: (re.search(rf"^{k}:\s*(.+)$", txt, re.M) or [None, ""])[1].strip()
            sc["seo"] = {"title": g("TITLE") or sc["title"], "description": g("DESCRIPTION") or sc.get("description", ""),
                         "tags": [t.strip() for t in g("TAGS").split(",") if t.strip()] or sc.get("tags", []), "hashtags": g("HASHTAGS").split()}
            _j(f"{proj}/script.json", sc)
        except Exception as e:
            log(proj, f"SEO metadata generation failed ({e}); falling back to script title/tags")
    words = sum(len(s["narration"].split()) for s in sc["scenes"])
    review = [f"# {sc['title']}\n", f"~{words / 155:.1f} min, {len(sc['scenes'])} scenes. Edit script.json, then run with --approve.\n",
              "## Sources\n" + "\n".join(f"- {u}" for u in sc["sources"]) + "\n",
              "## Cast\n" + "\n".join(f"- **{c['id']}** — {c['look']} | voice: {c['voice']}" for c in sc["characters"]) + "\n", "## Script\n"]
    for s in sc["scenes"]:
        review.append(f"### {s['id']} · {s['kind']} · {s.get('environment', '')} · transition {s['transition']}")
        for ln in s["lines"]:
            review.append(f"- **{ln['speaker']}** ({ln['emotion']}, {ln['shot']}): {ln['text']}")
        review.append("")
    open(f"{proj}/SCRIPT_REVIEW.md", "w").write("\n".join(review))
    return sc


# ---------------------------------------------------------------- 4: voices
def stage_voice(proj, sc):
    llm.unload(); comfy.free()
    voice.narrate(sc, f"{proj}/audio")
    voice.word_timings(sc, f"{proj}/audio")
    voice.visemes(sc, f"{proj}/audio")
    log(proj, f"voice: {sum(s['_dur'] for s in sc['scenes']) / 60:.1f} min of dialogue, "
              f"{len({l['speaker'] for s in sc['scenes'] for l in s['lines']})} distinct voices")


# ---------------------------------------------------------------- 5-6: assets & hero shots
REACTIONS = {"surprised": "surprised", "angry": "worried", "excited": "happy", "sad": "worried", "confused": "thinking"}


def stage_assets(proj, sc):
    need = {}                                    # (character, outfit) -> poses
    for s in sc["scenes"]:
        on = [(c["char"], c.get("outfit")) for c in s["cast"]]
        for k in on:
            need.setdefault(k, {"neutral", "talk", "side_talk", "side_listen"})
        for ln in s["lines"]:
            for k in on:
                if k[0] == ln["speaker"]: need[k].add(ln["pose"])
                elif ln["emotion"] in REACTIONS: need[k].add(REACTIONS[ln["emotion"]])
    chars = {c["id"]: c for c in sc["characters"]}
    for (cid, outfit), poses in need.items():
        if cid not in chars: continue
        log(proj, f"character {cid}{' (' + outfit + ')' if outfit else ''}: {len(poses)} poses/expressions")
        if outfit: assets.build_outfit(chars[cid], outfit, sorted(poses))
        else: assets.build_character(chars[cid], sorted(poses))
    for e in sc["environments"]:
        if any(s.get("environment") == e["id"] for s in sc["scenes"]):
            e["_file"] = assets.build_background(e)
            early_text_check(proj, e)
    _j(f"{proj}/script.json", sc)


def early_text_check(proj, e):
    """Catch garbled AI text in a background right after it is made (not after rendering + QC):
    repaint just those regions. Result cached per file hash in the environment entry."""
    from . import repaint
    f = e["_file"]; h = hashlib.md5(open(f, "rb").read()).hexdigest()[:12]
    if e.get("_text_ok") == h: return
    try:
        bad = repaint.garbled_text_boxes(f)
        if bad and e.get("_repaints", 0) < 2:
            base, ext = os.path.splitext(f)
            out = f"{base.split('_rp')[0]}_rp{e.get('_repaints', 0) + 1}{ext}"
            log(proj, f"assets: garbled text in background {e['id']} {[t for t, _ in bad][:4]} -> repainting {len(bad)} region(s)")
            comfy.start(); repaint.repaint(f, [bb for _, bb in bad], out)
            e["bg_file"] = e["_file"] = out; e["_repaints"] = e.get("_repaints", 0) + 1
            h = hashlib.md5(open(out, "rb").read()).hexdigest()[:12]
        e["_text_ok"] = h
    except Exception as ex:
        log(proj, f"assets: early text check skipped for {e['id']}: {ex}")
    finally:
        from .qc import models as M
        M.free()


def stage_hero(proj, sc):
    for s in sc["scenes"]:
        if s["kind"] != "hero": continue
        out = f"{proj}/hero/{s['id']}.mp4"
        if os.path.exists(out): continue
        secs = int(min(8, max(3, math.ceil(s["_dur"]))))
        log(proj, f"hero {s['id']}: LTX-2.5 {secs}s — {s['hero_prompt'][:60]}")
        shutil.copy(hero.make(s["hero_prompt"], f"{proj}/work", f"hero_{s['id']}", seconds=secs), out)
    comfy.free()


# ---------------------------------------------------------------- 6b: talking shots (LTX image+audio -> video)
FRONT_POSES = ("talk", "point", "shrug", "thinking", "worried", "happy", "angry", "surprised", "neutral")   # no facepalm/arms_up: held for a whole line they look odd and wreck hands


def _pose_img(cid, want):
    rig = _j(os.path.join(C.CHAR_LIB, assets.slug(cid), "rig.json")) or {}
    poses = rig.get("poses", {})
    for p in ([want] if want in FRONT_POSES else []) + ["talk", "neutral"] + list(FRONT_POSES):
        if p in poses: return os.path.join(C.LIBRARY, poses[p]["img"])
    return None


def _still(bg, chars, out, top=None):
    """chars: [(img_path, x_frac, height_frac)] composited on the background at 1280x720, feet near the bottom edge.
    top: if set, the figure's head sits at this fraction of the frame height instead (waist-up framing, legs cropped)."""
    from PIL import Image
    B = Image.open(bg).convert("RGB").resize((1280, 720))
    for img, x, hf in chars:
        ch = Image.open(img).convert("RGBA"); hh = int(720 * hf)
        ch = ch.resize((max(1, int(ch.width * hh / ch.height)), hh))
        bb = ch.getbbox() or (0, 0, ch.width, ch.height)
        y = int(720 * top) - bb[1] if top is not None else 720 - hh + int(hh * 0.04)
        B.paste(ch, (int(1280 * x - ch.width / 2), y), ch)
    B.save(out); return out


def _talk_style(c):
    """Style words for the LTX prompt: the show's warm animated look, or the default muted newsroom look."""
    return ("Polished 2D animated-series illustration style, warm friendly colours, attractive expressive faces" if c.get("style")
            else "Clean modern editorial illustration style, muted colours")



# ---------------------------------------------------------------- 6b: conversation staging (show episodes)
CONV_W, CONV_H = 1280, 704
# Medium two-shot (mid-thigh up): LTX keeps this framing (measured +7% drift per shot vs +30% from a wide shot), and the crop
# leaves enough margin that the stabiliser never has to invent edges.
CONV_CROP = (45, 24, 1190, 669)                 # steady window in reference coordinates (covers up to ~7.5% zoom without fill)
CU_WIN = {"left": (0, 1080), "right": (840, 1080), "center": (420, 1080)}     # closeup windows in the 1920 frame (exclude the other face)


def _tag(c, outfit=None):
    o = (c.get("outfits") or {}).get(outfit) if outfit else None
    if o and o.get("tag"): return o["tag"]
    return c.get("tag") or ("the " + " ".join(c["look"].replace("a ", "", 1).split(",")[0].split()[:6]))


def _conv_still(bg, cast, out):
    """Reference still: two characters facing each other (left uses side_talk, right uses side_listen mirrored), or one centred."""
    from PIL import Image, ImageOps
    B = Image.open(bg).convert("RGB").resize((CONV_W, CONV_H))
    def put(img, x, hpx, top, mirror=False):
        ch = Image.open(img).convert("RGBA")
        if mirror: ch = ImageOps.mirror(ch)
        ch = ch.resize((max(1, int(ch.width * hpx / ch.height)), hpx)); bb = ch.getbbox() or (0, 0, ch.width, ch.height)
        B.paste(ch, (int(CONV_W * x - ch.width / 2), int(top) - bb[1]), ch)
    if len(cast) >= 2:
        put(_pose_img_any(assets.art_id(cast[0]["char"], cast[0].get("outfit")), "side_talk"), 0.36, 1150, 40)
        put(_pose_img_any(assets.art_id(cast[1]["char"], cast[1].get("outfit")), "side_listen"), 0.64, 1120, 52, mirror=True)
    else:
        put(_pose_img_any(assets.art_id(cast[0]["char"], cast[0].get("outfit")), "talk"), 0.5, 1150, 40)
    B.save(out); return out


def _pose_img_any(cid, want):
    rig = _j(os.path.join(C.CHAR_LIB, assets.slug(cid), "rig.json")) or {}
    poses = rig.get("poses", {})
    for p in [want, "side_talk", "talk", "neutral"]:
        if p in poses: return os.path.join(C.LIBRARY, poses[p]["img"])
    return _pose_img(cid, "neutral")


DEFAULT_ACT = {"excited": "talks excitedly, eyes bright", "happy": "smiles and talks warmly", "surprised": "reacts with genuine surprise, then talks",
               "confused": "frowns slightly, puzzled, and talks", "worried": "talks with a worried look", "sarcastic": "says it dryly with a tiny knowing smile",
               "confident": "talks confidently", "sad": "talks quietly, a little deflated", "angry": "talks with controlled irritation",
               "neutral": "talks naturally"}


def stage_conversation(proj, sc):
    """Show episodes: every stage scene is ONE continuous conversation. Each line is an LTX shot that starts from the previous
    shot's (stabilised) last frame, so expressions carry over instead of resetting; both characters stay in frame, the listener
    reacts with mouth closed. Every shot is stabilised to a fixed medium two-shot (no zoom creep); a closeup is a crop of the same
    take. Shots are cached by content in library/talk_cache. A shot with a HIGH/CRITICAL glitch is regenerated once from the same
    start frame. Writes talk/<scene>.json and talk/ANIMATION_QC.json. Returns the scene ids handled."""
    from . import stabilize
    from .qc import animcheck as A, core as QC
    chars = {c["id"]: c for c in sc["characters"]}
    envs = {e["id"]: e for e in sc["environments"]}
    TALK_CACHE = f"{proj}/talk/cache"            # per project: every video gets its own takes, nothing reused from other videos
    os.makedirs(f"{proj}/talk", exist_ok=True); os.makedirs(f"{proj}/work/talk", exist_ok=True); os.makedirs(TALK_CACHE, exist_ok=True)
    style = _talk_style(next(iter(chars.values()), {}))
    scenes = [s for s in sc["scenes"] if s["kind"] == "stage" and s.get("cast") and envs.get(s.get("environment"), {}).get("_file")]
    shots = []                                   # per line: dict with everything needed to (re)generate + edit

    def gen(sh, attempt):
        key = hashlib.md5(open(sh["start"], "rb").read() + open(sh["aud"], "rb").read() + sh["prompt"].encode() + str(attempt).encode()).hexdigest()[:16]
        raw = os.path.join(TALK_CACHE, key + ".mp4")
        if not os.path.exists(raw):
            out = talk.clip(sh["start"], sh["aud"], sh["prompt"], f"{proj}/work/talk", f"{sh['scene']}_{sh['i']}_a{attempt}", sh["secs"],
                            seed=sh["seed"] + 7919 * attempt, neg=talk.NEG_SCENE)
            shutil.copy(out, raw); talk.fix_doubled(raw)
        stab = os.path.join(TALK_CACHE, key + f"_stab_{sh['crop_sig']}.mp4")
        last = stab.rsplit(".", 1)[0] + "_last.png"
        if not (os.path.exists(stab) and os.path.exists(last)):
            stabilize.stabilize(raw, sh["ref"], stab, sh["crop"])
        return raw, stab, last

    # 1) generate every scene as a chain (a scene in the same place with the same people continues from the previous scene's last frame)
    prev_key, prev_last = None, None
    for s in scenes:
        cast = s["cast"][:2]
        lines = _j(f"{proj}/audio/{s['id']}.lines.json") or []
        wav = f"{proj}/audio/{s['id']}.wav"
        if not lines or not os.path.exists(wav): continue
        ref = _conv_still(envs[s["environment"]]["_file"], cast, f"{proj}/work/talk/{s['id']}_ref.png")
        side = {c["char"]: ("left" if k == 0 else "right") for k, c in enumerate(cast)} if len(cast) >= 2 else {cast[0]["char"]: "center"}
        outfit = {c["char"]: c.get("outfit") for c in cast}
        place = envs[s["environment"]]["prompt"].split(":")[0].split(".")[0].lower()
        end = s["_dur"] + TAIL + 2.6
        key_here = (s["environment"], tuple((c["char"], c.get("outfit")) for c in cast))
        start = prev_last if key_here == prev_key and prev_last and os.path.exists(prev_last) else ref
        for i, ln in enumerate(lines):
            a = 0.0 if i == 0 else ln["start"]
            b = lines[i + 1]["start"] if i + 1 < len(lines) else end
            src = s["lines"][i] if i < len(s["lines"]) else {}
            sp = ln["speaker"]
            aud, secs = talk.cut_audio(wav, a, b, f"{proj}/work/talk/{s['id']}_{i}.wav", pad=0.0)
            others = [c["char"] for c in cast if c["char"] != sp]
            if sp in chars and sp in side:
                who = f"{_tag(chars[sp], outfit.get(sp))} on the {side[sp]}" if side[sp] != "center" else _tag(chars[sp], outfit.get(sp))
                act = src.get("act") or f"{who} {DEFAULT_ACT.get(src.get('emotion', 'neutral'), 'talks naturally')}"
                react = src.get("react") or (f"{_tag(chars[others[0]], outfit.get(others[0]))} listens and reacts naturally, mouth closed" if others else "")
                talking = (f"{act}; {react}. Only the speaking person's lips move, in exact sync with the speech; "
                           f"the listener's mouth stays closed.") if others else f"{act}. Lips move in exact sync with the speech."
                silent = False
            else:                                # narrator voice-over over a stage scene: everyone listens / idles
                talking = (src.get("act") or "they share a quiet look and react naturally to what is being said") + ". Nobody on screen speaks; mouths closed."
                silent = True
            two = len(cast) >= 2
            prompt = ((f"Two people having a conversation in {place}, medium two-shot from mid-thigh up, they look at each other. " if two else
                       f"One person in {place}, medium shot. ") + talking +
                      " Natural, subtle acting: blinking, small head movements, expressions change gradually and stay. "
                      "Static locked-off camera, no zoom. " + style + ", natural hands with five fingers, hands mostly relaxed.")
            sh = {"scene": s["id"], "i": i, "start": start, "ref": ref, "aud": aud, "secs": secs, "prompt": prompt, "a": round(a, 3), "b": round(b, 3),
                  "seed": int(hashlib.md5((sp + ln["text"] + s["environment"]).encode()).hexdigest()[:7], 16),
                  "crop": CONV_CROP, "crop_sig": "c2", "side": side.get(sp), "silent": silent, "n": len(cast),
                  "shot": src.get("shot", "two_shot"), "pause_after": src.get("pause_after"),
                  "listener_side": side.get(others[0]) if others and others[0] in side else None,
                  "refs": [_pose_img_any(assets.art_id(c["char"], c.get("outfit")), "neutral") for c in cast], "desc": f"{len(cast)} people talking in {place}"}
            try:
                sh["raw"], sh["stab"], last = gen(sh, 0)
                start = last
            except Exception as e:
                log(proj, f"conversation shot {s['id']}#{i} failed: {e!r}")
            shots.append(sh)
        prev_key, prev_last = key_here, start
        log(proj, f"conversation {s['id']}: {len(lines)} shots")
    comfy.free()
    # 2) check every shot (glitches, people, identity, speaker lip-sync, anatomy on a third of the sampled frames)
    cfg = QC.load_config(proj)
    for rnd in range(int(os.environ.get("TALK_TRIES", "3"))):
        todo = [sh for sh in shots if sh.get("raw") and (rnd == 0 or not sh["qc"]["ok"])]
        if not todo: break
        if rnd >= 1:                              # regenerate failures with a new seed, from the same start frame
            for sh in todo:
                try: sh["raw2"], sh["stab2"], _ = gen(sh, rnd)
                except Exception as e: log(proj, f"conversation shot {sh['scene']}#{sh['i']} retry failed: {e!r}")
            comfy.free()
        for sh in todo:
            v = sh.get("raw2") if rnd >= 1 else sh["raw"]
            if not v: continue
            try:
                r = A.check_shot(v, sh["aud"], sh["desc"], sh["n"], refs=sh["refs"], silent=sh["silent"], work=f"{proj}/work/talk", cfg=cfg,
                                 speaker_side=sh["side"] if sh["side"] in ("left", "right") else None, vlm_every=1)
            except Exception as e:
                r = {"findings": [{"severity": "MEDIUM", "check": "qc", "msg": f"check crashed: {e!r}", "frame": None, "t": None}], "score": 1, "ok": True}
            if rnd == 0: sh["qc"] = r
            elif r["score"] < sh["qc"]["score"]: sh["qc"] = r; sh["stab"] = sh["stab2"]; sh["retried_better"] = rnd + 1
            bad = [f for f in r["findings"] if f["severity"] in ("CRITICAL", "HIGH")]
            log(proj, f"conversation QC {sh['scene']}#{sh['i']} try {rnd + 1}: " + ("PASS" if r["ok"] else "FAIL — " +
                "; ".join(f"{f['check']}: {f['msg'][:70]}" for f in bad[:3])))
        from .qc import models as QM
        QM.free(); llm.unload()
    # 3) edit: wide two-shot or closeup crop of the same take; after a written beat, cut to the listener's reaction
    report = []
    for sid in dict.fromkeys(sh["scene"] for sh in shots):
        man = []
        for sh in [x for x in shots if x["scene"] == sid]:
            if not sh.get("stab"): continue
            def cut(t0, t1, side, tag):
                o = f"{proj}/talk/{sid}_{sh['i']}_{tag}_{hashlib.md5(sh['stab'].encode()).hexdigest()[:8]}.mp4"
                if not os.path.exists(o):
                    vf = "scale=1920:1080"
                    if side in CU_WIN:
                        x, w = CU_WIN[side]; vf = f"crop={w}:{int(w * 9 / 16)}:{x}:30,scale=1920:1080:flags=lanczos"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", sh["stab"], "-t", f"{t1 - t0:.3f}", "-vf", vf, "-an",
                                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(C.FPS), o], check=True)
                return o
            dur = sh["b"] - sh["a"]
            cu = sh["side"] if sh["shot"] == "closeup" and sh["side"] else None
            beat = float(sh["pause_after"] or 0)
            if beat >= 0.6 and sh["listener_side"] and dur - beat > 0.8:
                split = dur - beat + 0.1                     # reaction: hold on the listener during the beat
                man.append({"video": cut(0, split, cu, "a"), "start": sh["a"], "end": round(sh["a"] + split, 3)})
                man.append({"video": cut(split, dur, sh["listener_side"], "r"), "start": round(sh["a"] + split, 3), "end": sh["b"]})
            else:
                man.append({"video": cut(0, dur, cu, "a"), "start": sh["a"], "end": sh["b"]})
            q = sh.get("qc") or {"findings": [], "ok": False}
            report.append({"scene": sid, "line": sh["i"], "start": sh["a"], "end": sh["b"], "video": sh["stab"], "ok": q.get("ok", False),
                           "attempts": 1 + bool(sh.get("raw2")), "chosen_attempt": sh.get("retried_better") or 1, "findings": q.get("findings", [])})
        json.dump(man, open(f"{proj}/talk/{sid}.json", "w"), indent=1)
    json.dump(report, open(f"{proj}/talk/ANIMATION_QC.json", "w"), indent=1)
    log(proj, f"conversation: {len(shots)} shots; QC {sum(r['ok'] for r in report)}/{len(report)} clean")
    return {s["id"] for s in scenes}

def stage_talk(proj, sc):
    """Every stage scene becomes a run of animated shots: the speaker alone (interview framing) animated to their REAL voice
    line, or the whole cast listening quietly (silent audio) while the narrator talks. Cached by content hash.
    Every shot is checked frame by frame (qc.animcheck: jumps/flashes/flicker/blur on every frame; people, identity, anatomy
    glitches via the vision model 4x a second + every flagged frame; lip-sync vs the voice). Failed shots are regenerated with
    new seeds (max 3 attempts, best kept). Writes talk/<scene>.json = [{video, start, end}] and talk/ANIMATION_QC.json;
    a scene whose best shot still has a CRITICAL problem falls back to the cut-out puppets."""
    from .qc import animcheck as A, core as QC
    done = stage_conversation(proj, sc) if sc.get("show") else set()
    chars = {c["id"]: c for c in sc["characters"]}
    envs = {e["id"]: e for e in sc["environments"]}
    os.makedirs(f"{proj}/talk", exist_ok=True); os.makedirs(f"{proj}/work/talk", exist_ok=True)
    X = {"left": 0.36, "center": 0.5, "right": 0.64}
    jobs = []                                                   # one per line of every stage scene
    for s in sc["scenes"]:
        if s["kind"] != "stage" or not s.get("cast") or s["id"] in done: continue
        bg = envs.get(s.get("environment"), {}).get("_file")
        lines = _j(f"{proj}/audio/{s['id']}.lines.json") or []
        wav = f"{proj}/audio/{s['id']}.wav"
        if not bg or not lines or not os.path.exists(wav): continue
        end = s["_dur"] + TAIL + 2.6                       # covers the tail, the last-scene tail and the cross-fade into the next scene
        cast = [c for c in s["cast"] if _pose_img(c["char"], "neutral")]
        place = envs[s["environment"]]["prompt"].split(".")[0].lower()
        for i, ln in enumerate(lines):
            a = 0.0 if i == 0 else ln["start"]
            b = lines[i + 1]["start"] if i + 1 < len(lines) else end
            src = s["lines"][i] if i < len(s["lines"]) else {}
            sp = ln["speaker"]
            if sp in chars and _pose_img(sp, src.get("pose", "talk")):
                pos = next((c["position"] for c in s["cast"] if c["char"] == sp), "center")
                pose_img = _pose_img(sp, src.get("pose", "talk"))
                people = [(pose_img, X.get(pos, 0.5), 1.75)]   # waist-up: big face, so LTX keeps the identity
                look = chars[sp]["look"].split(".")[0]
                prompt = (f"{look}. In {place}, the person speaks {src.get('emotion', 'calmly')} and naturally to the viewer, natural hand "
                          f"gestures, subtle head movement, blinking, lips moving exactly in sync with the speech. Locked-off tripod camera that never "
                          f"moves or zooms, waist-up medium shot, framing stays exactly the same. {_talk_style(chars[sp])}, consistent face and clothes, "
                          f"correct anatomy, five fingers on each hand.")
                silent, refs, desc = False, [pose_img], f"one person ({look}) speaking to the viewer in {place}"
            else:
                xs = [0.5] if len(cast) == 1 else [0.3, 0.7] if len(cast) == 2 else [0.22, 0.5, 0.78]
                people = [(_pose_img(c["char"], "neutral"), xs[k % len(xs)], 0.74) for k, c in enumerate(cast[:3])]
                prompt = (f"In {place}, the people stand and listen quietly, mouths closed, small natural idle movements, breathing, "
                          f"occasional glance and nod. Nobody speaks. Locked-off tripod camera that never moves or zooms, wide shot. "
                          f"{_talk_style(chars.get(cast[0]['char'], {}) if cast else {})}, correct anatomy.")
                silent, refs, desc = True, [p[0] for p in people], f"{len(people)} people standing and listening quietly in {place}"
            if not people: continue
            still = _still(bg, people, f"{proj}/work/talk/{s['id']}_{i}.png", top=None if silent else 0.07)
            aud, secs = talk.cut_audio(wav, a, b, f"{proj}/work/talk/{s['id']}_{i}.wav", pad=0.0)
            if silent:
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(secs), aud], check=True)
            h = hashlib.md5(open(still, "rb").read() + open(aud, "rb").read() + prompt.encode()).hexdigest()[:12]
            jobs.append({"scene": s["id"], "i": i, "start": round(a, 3), "end": round(b, 3), "still": still, "aud": aud, "secs": secs,
                         "prompt": prompt, "silent": silent, "refs": refs, "desc": desc, "n": len(people), "h": h,
                         "seed0": int(hashlib.md5((sp + s["id"]).encode()).hexdigest()[:7], 16) + _reseed(proj, s["id"], i)})
    if not jobs: return

    def path(j, k): return f"{proj}/talk/{j['scene']}_{j['i']}_{j['h']}" + (f"_t{k}" if k else "") + ".mp4"

    def gen(j, k):
        out = path(j, k)
        if not os.path.exists(out):
            shutil.copy(talk.clip(j["still"], j["aud"], j["prompt"], f"{proj}/work/talk", f"{j['scene']}_{j['i']}_t{k}", j["secs"],
                                  seed=j["seed0"] + 7919 * k), out)
            if talk.fix_doubled(out): log(proj, f"talk shot {j['scene']} line {j['i']} attempt {k + 1}: repaired 12-fps frame doubling")
        return out

    cfg = QC.load_config(proj)
    n_new = 0
    for j in jobs: j["tries"] = {}
    for rnd in range(int(os.environ.get("TALK_TRIES", "3"))):
        todo = [j for j in jobs if j.get("best") is None or (not j["best"]["ok"] and rnd not in j["tries"])]
        if not todo: break
        # 1) generate (GPU: LTX)
        for j in todo:
            try:
                existed = os.path.exists(path(j, rnd)); j["tries"][rnd] = gen(j, rnd); n_new += not existed
            except Exception as e:
                log(proj, f"talk shot {j['scene']} line {j['i']} attempt {rnd + 1} failed to generate: {e!r}")
        comfy.free()
        # 2) frame-by-frame QC (GPU: detectors + vision model)
        for j in todo:
            v = j["tries"].get(rnd)
            if not v: continue
            try:
                r = A.check_shot(v, j["aud"], j["desc"], j["n"], refs=j["refs"], silent=j["silent"], work=f"{proj}/work/talk", cfg=cfg)
            except Exception as e:
                r = {"findings": [{"severity": "MEDIUM", "check": "qc", "msg": f"animation check crashed: {e!r}", "frame": None, "t": None}],
                     "score": 1, "ok": True}
            r["video"] = v; r["attempt"] = rnd + 1
            if j.get("best") is None or r["score"] < j["best"]["score"]: j["best"] = r
            bad = [f for f in r["findings"] if f["severity"] in ("CRITICAL", "HIGH")]
            log(proj, f"animation QC {j['scene']}#{j['i']} try {rnd + 1}: " + ("PASS" if r["ok"] else
                "FAIL — " + "; ".join(f"{f['check']}: {f['msg'][:70]}" for f in bad[:3])))
        from .qc import models as QM
        QM.free(); llm.unload()
    # 3) manifests + report
    report = []
    for sid in dict.fromkeys(j["scene"] for j in jobs):
        js = [j for j in jobs if j["scene"] == sid]
        man = f"{proj}/talk/{sid}.json"
        crit = [j for j in js if not j.get("best") or any(f["severity"] == "CRITICAL" for f in j["best"]["findings"])]
        for j in js:
            b = j.get("best") or {"findings": [], "ok": False, "video": None, "attempt": 0}
            report.append({"scene": sid, "line": j["i"], "start": j["start"], "end": j["end"], "video": b.get("video"), "ok": b.get("ok", False),
                           "attempts": len(j["tries"]), "chosen_attempt": b.get("attempt"), "findings": b.get("findings", [])})
        if crit:
            log(proj, f"talk: scene {sid} keeps the cut-out characters ({len(crit)} shot(s) with critical animation problems)")
            if os.path.exists(man): os.remove(man)
            continue
        json.dump([{"video": j["best"]["video"], "start": j["start"], "end": j["end"]} for j in js], open(man, "w"), indent=1)
    json.dump(report, open(f"{proj}/talk/ANIMATION_QC.json", "w"), indent=1)
    nok = sum(r["ok"] for r in report)
    log(proj, f"talk: {n_new} new animated shots; animation QC {nok}/{len(report)} shots clean")
    comfy.free()


# ---------------------------------------------------------------- 7: sound
def stage_sound(proj, sc):
    n = 0
    for s in sc["scenes"]:
        for c in s["sfx"]: audio.sfx(c["sound"]); n += 1
    for e in sc["environments"]:
        if any(s.get("environment") == e["id"] for s in sc["scenes"]):
            audio.sfx(f"{e['ambience']}, continuous background ambience, no music, no speech", 10)
    for snd in ("fast swoosh transition", "soft cartoon pop", "quick paper whoosh"):
        audio.sfx(snd, 1.5)
    beds, cur = [], None
    for s in sc["scenes"]:
        if cur and cur["mood"] == s["music"]: cur["scenes"].append(s["id"])
        else: cur = {"mood": s["music"], "scenes": [s["id"]]}; beds.append(cur)
    for b in beds:  # pre-generate while ComfyUI is warm
        secs = sum(next(x for x in sc["scenes"] if x["id"] == i)["_dur"] for i in b["scenes"])
        if secs >= 6: audio.music(b["mood"], secs + 4)
    comfy.free()
    log(proj, f"sound: {n} sfx, {len(beds)} music beds, ambience for {len(sc['environments'])} environments")
    return beds


# ---------------------------------------------------------------- 8: props + render
def _stage_file(proj, src, sub):
    rel = os.path.join(sub, os.path.basename(src))
    dst = os.path.join(proj, "public", rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        shutil.copy(src, dst)
    return rel


def _when(words, name, default_ms):
    """time (ms) a name is first mentioned: match its first significant word."""
    toks = [t for t in re.findall(r"[a-z0-9]+", name.lower()) if len(t) > 2] or re.findall(r"[a-z0-9]+", name.lower())
    for w in words:
        if toks and toks[0] in re.sub(r"[^a-z0-9]", "", w["text"].lower()):
            return max(0, w["startMs"] - 150)
    return default_ms


_PUB = {"apnews": "AP", "reuters": "Reuters", "bbc": "BBC", "nytimes": "New York Times", "wikipedia": "Wikipedia", "theguardian": "The Guardian",
        "cnn": "CNN", "aljazeera": "Al Jazeera", "ft": "Financial Times", "bloomberg": "Bloomberg", "politico": "Politico", "npr": "NPR",
        "euronews": "Euronews", "washingtonpost": "Washington Post", "wsj": "Wall Street Journal", "nbcnews": "NBC News", "cnbc": "CNBC", "outlookindia": "Outlook India", "indianexpress": "Indian Express", "news18": "News18", "forexfactory": "Forex Factory", "fxstreet": "FXStreet", "yahoo": "Yahoo Finance", "globaltimes": "Global Times", "wionews": "WION", "turkiyetoday": "Türkiye Today"}


def _reseed(proj, sid, i):
    """Seed offset from talk/RESEED lines like 's10_0 1' — lets a bad shot be regenerated with fresh seeds."""
    try:
        for ln in open(os.path.join(proj, "talk", "RESEED")):
            k, _, v = ln.strip().partition(" ")
            if k == f"{sid}_{i}": return 104729 * int(v or 1)
    except OSError: pass
    return 0


def source_names(sc, k=3, proj=None):
    """Publisher names for the on-screen source credit, from the script's source URLs."""
    out, urls = [], list(sc.get("sources") or [])
    if proj and not any("http" in u for u in urls):
        try: urls = [x.get("url", "") for x in json.load(open(os.path.join(proj, "research.json")))["sources"]]
        except Exception: pass
    for u in urls:
        m = re.search(r"https?://[^\s)]+", u)
        if not m: continue
        u = m.group(0)
        host = re.sub(r"^https?://", "", u).split("/")[0].split(":")[0]
        parts = [x for x in host.split(".") if x not in ("www", "en", "english", "m", "edition", "amp")]
        key = parts[-2] if len(parts) >= 2 else (parts[0] if parts else "")
        name = _PUB.get(key, key.capitalize())
        if name and name not in out: out.append(name)
    while len(out) > 1 and len(" · ".join(out[:k])) > 48: k -= 1
    return " · ".join(out[:k])


def build_props(proj, sc):
    chars = {c["id"]: c for c in sc["characters"]}
    names = {c["id"]: {"name": c.get("tag_name") or c["name"], "role": c.get("role", "")}
             for c in sc["characters"] if c.get("tag", True) is not False and (c.get("role") or c.get("real_person") or c.get("tag_name"))}
    srcs, seen = source_names(sc, proj=proj), set()
    envs = {e["id"]: e for e in sc["environments"]}
    colors = {"narrator": "#ffffff"}
    for i, c in enumerate(sc["characters"]): colors[c["id"]] = SPEAKER_COLORS[i % len(SPEAKER_COLORS)]
    chapter, props, last_bg = 0, [], None
    scenes = sc["scenes"]
    for i, s in enumerate(scenes):
        nxt = scenes[i + 1]["transition"] if i + 1 < len(scenes) else "cut"
        overlap = XFADE[nxt][1]
        frames = max(int(C.FPS * 1.6), math.ceil((s["_dur"] + TAIL + overlap + (s.get("_tail") or (1.2 if s is sc["scenes"][-1] else 0))) * C.FPS))
        W = _j(f"{proj}/audio/{s['id']}.words.json") or {"words": []}
        words = W["words"]
        lines = _j(f"{proj}/audio/{s['id']}.lines.json") or []
        for ln, src in zip(lines, s["lines"]):
            ln.update(pose=src["pose"], emotion=src["emotion"], shot=src["shot"])
            ln.setdefault("visemes", [])
        # beat words also get caption emphasis
        bw = {t.lower() for b in s["beats"] for t in re.findall(r"[a-z0-9]+", b["text"].lower()) if len(t) > 3}
        for w in words:
            if re.sub(r"[^a-z0-9]", "", w["text"].lower()) in bw: w["emph"] = True
        cast = []
        for c in s["cast"]:
            # mouth-moving frames for every pose this character can speak in (cached in the library)
            spoken = {l["pose"] for l in s["lines"] if l["speaker"] == c["char"]} | {"side_talk", "talk", "neutral"}
            try: assets.talk_frames(assets.slug(c["char"]), spoken)
            except Exception as e: log(proj, f"talk frames failed for {c['char']}: {e}")
            rig = _j(os.path.join(C.CHAR_LIB, assets.slug(c["char"]), "rig.json"))
            if not rig: continue
            poses = {}
            for name, pz in rig["poses"].items():
                m, e = pz["mouth"], pz["eyes"]
                poses[name] = {"img": _stage_file(proj, os.path.join(C.LIBRARY, pz["img"]), f"chars/{assets.slug(c['char'])}"),
                               "w": pz["w"], "h": pz["h"], "mouth": dict(zip("xywh", m)) if m else None,
                               "eyes": [dict(zip("xywh", b)) for b in e], "skin": pz["skin"], "eyeSkin": pz.get("eye_skin", pz["skin"]),
                               "talk": {k: _stage_file(proj, os.path.join(C.LIBRARY, v), f"chars/{assets.slug(c['char'])}") for k, v in pz["talk"].items()} if pz.get("talk") else None}
            cast.append({"char": c["char"], "position": c["position"], "poses": poses, "color": colors.get(c["char"], "#fff"),
                         "x": (s.get("layout") or {}).get(c["char"])})      # QC grounding fix may set an exact x
        bg = None
        if s.get("environment") in envs and envs[s["environment"]].get("_file"):
            bg = _stage_file(proj, envs[s["environment"]]["_file"], "bg")
        if s["kind"] == "stage" and bg: last_bg = bg
        hv, rate = None, 1
        if s["kind"] == "hero" and os.path.exists(f"{proj}/hero/{s['id']}.mp4"):
            hv = _stage_file(proj, f"{proj}/hero/{s['id']}.mp4", "hero")
            hd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                       f"{proj}/hero/{s['id']}.mp4"], capture_output=True, text=True).stdout.strip() or 5)
            rate = min(1.0, hd / (frames / C.FPS))
        shots = None
        man = _j(f"{proj}/talk/{s['id']}.json")
        if s["kind"] == "stage" and man and all(os.path.exists(x["video"]) for x in man):
            shots = [{"video": _stage_file(proj, x["video"], "talk"), "start": x["start"], "end": x["end"]} for x in man]
        # "PART n" only on real chapter cards: never on the closing card(s) or sign-offs, and never in a show episode (sketch, not a lecture)
        closing = s is sc["scenes"][-1] or bool(ending.SIGNOFF.search(s.get("narration", ""))) or \
            (s.get("title_text") or "").lower().strip() in ("the takeaway", "takeaway", "see you next time", "thanks for watching")
        if s["kind"] == "title_card" and not closing and not sc.get("show"): chapter += 1
        shown_chapter = chapter if s["kind"] == "title_card" and not closing and not sc.get("show") else 0
        beats = [{"atMs": _when(words, b["at_word"], 400) if b["at_word"] != "start" else 300, "type": b["type"], "text": b["text"]} for b in s["beats"]]
        # each beat gets >= 1.1 s on screen before the next replaces it (no flashing text); drop ones that no longer fit
        beats.sort(key=lambda b: b["atMs"]); spaced = []
        end_ms = (max([w["endMs"] for w in words] or [0]) + 600)
        for b in beats:
            if spaced and b["atMs"] < spaced[-1]["atMs"] + 1100: b["atMs"] = spaced[-1]["atMs"] + 1100
            if b["atMs"] <= end_ms: spaced.append(b)
        beats = spaced
        if s["kind"] == "chart" and (s.get("chart") or {}).get("mode") in ("stats", "timeline"): beats = []   # the cards already show the numbers
        mp = None
        if s["kind"] == "map":
            m = s["map"]
            mp = {"label": m["label"],
                  "countries": [{"name": c, "atMs": _when(words, c, 600 + k * 700)} for k, c in enumerate(m["countries"])],
                  "places": [{**p, "atMs": _when(words, p["name"], 900 + k * 700)} for k, p in enumerate(m["places"])],
                  "routes": [{**r, "atMs": _when(words, r["label"] or r["to"], 1500 + k * 1800), "color": ROUTE_COLORS[k % len(ROUTE_COLORS)]}
                             for k, r in enumerate(m["routes"])]}
        kind = s["kind"] if not (s["kind"] == "hero" and not hv) else ("stage" if cast else "title_card")
        intro = [] if kind != "stage" else [c["char"] for c in cast if c["char"] not in seen and any(l["speaker"] == c["char"] for l in s["lines"])]
        seen.update(intro)
        props.append({"id": s["id"], "kind": kind, "durationInFrames": frames,
                      "names": names, "introduce": intro, "sources": srcs, "brand": C.BRAND,
                      "background": bg if kind != "title_card" else last_bg, "cast": cast if kind == "stage" and not shots else [], "shots": shots,
                      "lines": lines, "words": words, "beats": beats,
                      "titleText": s.get("title_text") or sc["title"], "chapter": shown_chapter, "map": mp,
                      "chart": s["chart"] if kind == "chart" else None, "heroVideo": hv, "heroRate": rate,
                      "accent": ACCENTS[chapter % len(ACCENTS)], "speakerColors": colors,
                      "_transition": s["transition"], "_overlap": overlap})
    return props


def _renderer_sig():
    """Hash of the Remotion source: any renderer fix automatically re-renders every scene."""
    h = hashlib.md5()
    for root, _, files in os.walk(os.path.join(C.REMOTION, "src")):
        for f in sorted(files):
            if f.endswith((".ts", ".tsx")): h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()


def stage_review(proj):
    """Full-video review (user's 11-point checklist): dense sheets of the WHOLE video, face crops of every line,
    automatic checks (blank/flash frames, freezes, loudness, peaks, dead air, TTS speed, clipped words, captions).
    Writes review/REVIEW.md; Claude must look at every sheet before the video counts as delivered."""
    r = subprocess.run([sys.executable, os.path.join(C.ROOT, "tools", "fullreview.py"), proj], capture_output=True, text=True)
    log(proj, "review: " + (r.stdout.strip().splitlines() or ["(no output)"])[-1] + (" " + r.stderr[-400:] if r.returncode not in (0, 1) else ""))
    return r.returncode == 0


def stage_render(proj, props, only=None):
    # full props of EVERY scene (QC reads this; render_jobs.json only lists the scenes re-rendered this time)
    _j(f"{proj}/work/all_props.json", [{k: v for k, v in p.items() if not k.startswith("_")} | {"_transition": p.get("_transition")} for p in props])
    jobs = []
    for p in props:
        clean = {k: v for k, v in p.items() if not k.startswith("_")}
        h = hashlib.md5((json.dumps(clean, sort_keys=True) + _renderer_sig()).encode()).hexdigest()
        out = f"{proj}/renders/{p['id']}.mp4"
        cached = os.path.exists(out) and os.path.exists(out + ".hash") and open(out + ".hash").read() == h
        if (only is None and cached) or (only is not None and p["id"] not in only):
            continue
        jobs.append({"props": clean, "out": out}); open(out + ".hash", "w").write(h)
    if not jobs:
        log(proj, "render: all scenes cached"); return
    log(proj, f"render: {len(jobs)} scene(s)")
    cfg = {"publicDir": f"{proj}/public", "bundleDir": f"{proj}/work/bundle", "concurrency": max(4, (os.cpu_count() or 8) // 2), "jobs": jobs}
    _j(f"{proj}/work/render_jobs.json", cfg)
    env = dict(os.environ, PATH=C.NODE + ":" + os.environ["PATH"])
    r = subprocess.run(["node", "render_scenes.mjs", f"{proj}/work/render_jobs.json"], cwd=C.REMOTION, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        for j in jobs:
            if os.path.exists(j["out"] + ".hash") and not os.path.exists(j["out"]): os.remove(j["out"] + ".hash")
        raise RuntimeError("render failed:\n" + r.stderr[-3000:])


# ---------------------------------------------------------------- 9: QC + repair
def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=width,height,nb_read_packets", "-of", "json", path], capture_output=True, text=True)
    st = json.loads(r.stdout or "{}").get("streams", [{}])[0]
    return st.get("width"), st.get("height"), int(st.get("nb_read_packets", 0))


def qc(proj, sc, props):
    problems, prev_bg = [], None
    for s, p in zip(sc["scenes"], props):
        a, sr = sf.read(f"{proj}/audio/{s['id']}.wav")
        if len(a) < sr * 0.5 or np.abs(a).max() < 0.01: problems.append((s["id"], "audio", "dialogue missing or silent"))
        for ln in _j(f"{proj}/audio/{s['id']}.lines.json") or []:
            d = ln["end"] - ln["start"]; n = len(ln["text"].split())
            if d > 0 and not (1.1 < n / d < 4.8): problems.append((s["id"], "audio", f"line '{ln['text'][:30]}' speech rate {n / d:.1f} w/s (TTS glitch?)"))
        out = f"{proj}/renders/{s['id']}.mp4"
        if not os.path.exists(out): problems.append((s["id"], "render", "missing render")); continue
        w, h, n = probe(out)
        if (w, h) != (C.W, C.H): problems.append((s["id"], "render", f"size {w}x{h}"))
        if abs(n - p["durationInFrames"]) > 1: problems.append((s["id"], "render", f"{n} frames, expected {p['durationInFrames']}"))
        if s["kind"] == "stage" and not p["cast"] and not p.get("shots"): problems.append((s["id"], "assets", "stage scene rendered with no characters"))
        if s["kind"] == "hero" and not p["heroVideo"]: problems.append((s["id"], "hero", "hero clip missing"))
        if p["kind"] == "stage":
            if p["background"] == prev_bg: problems.append((s["id"], "visual", "same environment as previous stage scene (warning)"))
            prev_bg = p["background"]
        mid = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(p["durationInFrames"] / C.FPS / 2), "-i", out, "-frames:v", "1",
                              "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        if mid and np.frombuffer(mid, np.uint8).mean() < 8: problems.append((s["id"], "render", "frame is black"))
    _j(f"{proj}/work/qc.json", [{"scene": a, "area": b, "problem": c} for a, b, c in problems])
    return [x for x in problems if x[1] != "visual"]


def repair(proj, sc, problems):
    for sid, area, _ in problems:
        if area == "audio":
            for ln in _j(f"{proj}/audio/{sid}.lines.json") or []:
                for ext in (".wav", ".words.json", ".visemes.json"):
                    f = f"{proj}/audio/lines/{ln['key']}{ext}"
                    if os.path.exists(f): os.remove(f)
    if any(a == "audio" for _, a, _ in problems): stage_voice(proj, sc)
    for sid in {s for s, a, _ in problems if a == "hero"}:
        f = f"{proj}/hero/{sid}.mp4"
        if os.path.exists(f): os.remove(f)
    stage_hero(proj, sc)
    return {s for s, _, _ in problems}


# ---------------------------------------------------------------- 10: master
def srt_time(t):
    h, m = int(t // 3600), int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def _seg_encode(job):
    """Encode one piece of the final timeline (frame-exact). job = (out, cmd)."""
    out, cmd = job
    tmp = out + ".tmp.mp4"
    subprocess.run(cmd + [tmp], check=True)
    os.replace(tmp, out)
    return out


ENC = ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "19", "-pix_fmt", "yuv420p", "-g", "60", "-bf", "0", "-an"]


def assemble_video(proj, props):
    """Segmented master: the timeline is cut into scene BODIES and short TRANSITION pieces at frame boundaries.
    Each piece is cached by the hashes of the renders it uses, so after a fix only the touched scene(s) and their
    transitions are re-encoded; everything is then stitched with stream copy (seconds instead of a full re-encode).
    Returns {scene_id: start_seconds}, total — the same timeline as the old one-pass xfade chain."""
    from concurrent.futures import ThreadPoolExecutor
    F = C.FPS
    lens = [p["durationInFrames"] / F for p in props]
    starts, d_in = {props[0]["id"]: 0.0}, [0.0]
    for i in range(1, len(props)):
        d = XFADE[props[i]["_transition"]][1]
        starts[props[i]["id"]] = starts[props[i - 1]["id"]] + lens[i - 1] - d; d_in.append(d)
    total = starts[props[-1]["id"]] + lens[-1]
    seg = f"{proj}/work/seg"; os.makedirs(seg, exist_ok=True)
    rh = {p["id"]: (open(f"{proj}/renders/{p['id']}.mp4.hash").read() if os.path.exists(f"{proj}/renders/{p['id']}.mp4.hash") else
                    str(os.path.getmtime(f"{proj}/renders/{p['id']}.mp4"))) for p in props}
    # transition windows [a_i, b_i) in global frames
    win = [None] + [(math.floor(starts[props[i]["id"]] * F + 1e-6), math.ceil((starts[props[i]["id"]] + d_in[i]) * F - 1e-6))
                    for i in range(1, len(props))]
    pieces, jobs = [], []
    total_f = round(total * F)
    for i, p in enumerate(props):
        src = f"{proj}/renders/{p['id']}.mp4"; st = starts[p["id"]]
        if i > 0:     # transition piece between scene i-1 and i
            a, b = win[i]; q = props[i - 1]; kind, d = XFADE[p["_transition"]]
            t0 = st - a / F                                  # where the xfade starts inside this window (0..1 frame)
            la = a / F - starts[q["id"]]                     # local time of the window start in the previous scene
            key = hashlib.md5(f"T2|{rh[q['id']]}|{rh[p['id']]}|{a}|{b}|{kind}|{d}|{st:.5f}".encode()).hexdigest()[:12]
            out = f"{seg}/t{i:03d}_{key}.mp4"; pieces.append(out)
            if not os.path.exists(out):
                n = b - a
                fc = (f"[0:v]trim=start_frame={max(0, math.floor(la * F + 1e-6))},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1,fps={F}[A];"
                      f"[1:v]tpad=start_mode=clone:start_duration={t0:.5f},fps={F}[B];"
                      f"[A][B]xfade=transition={kind}:duration={d}:offset={t0:.5f},trim=end_frame={n},setpts=PTS-STARTPTS[v]")
                jobs.append((out, ["ffmpeg", "-y", "-v", "error", "-i", f"{proj}/renders/{q['id']}.mp4", "-i", src,
                                   "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n), *ENC]))
        # body piece of scene i: from end of its in-transition to start of the next transition
        a = win[i][1] if i > 0 else 0
        b = win[i + 1][0] if i + 1 < len(props) else total_f
        if b > a:
            key = hashlib.md5(f"B2|{rh[p['id']]}|{a}|{b}|{st:.5f}".encode()).hexdigest()[:12]
            out = f"{seg}/b{i:03d}_{key}.mp4"; pieces.append(out)
            if not os.path.exists(out):
                ls = a / F - st
                jobs.append((out, ["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
                                   f"trim=start_frame={max(0, math.floor(ls * F + 1e-6))},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1,fps={F}",
                                   "-frames:v", str(b - a), *ENC]))
    if jobs:
        with ThreadPoolExecutor(4) as ex: list(ex.map(_seg_encode, jobs))
    log(proj, f"master: {len(jobs)} of {len(pieces)} segments re-encoded")
    keep = set(pieces)
    for f in glob.glob(f"{seg}/*.mp4"):
        if f not in keep: os.remove(f)
    lst = f"{seg}/list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in pieces))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{proj}/work/video.mp4"], check=True)
    return starts, total


def stage_master(proj, sc, props, beds):
    starts, total = assemble_video(proj, props)
    envs = {e["id"]: e for e in sc["environments"]}
    tl = [{"file": f"{proj}/audio/{p['id']}.wav", "start": starts[p["id"]] + 0.02, "kind": "narration"} for p in props]
    for s, p in zip(sc["scenes"], props):
        st, dur = starts[s["id"]], p["durationInFrames"] / C.FPS
        words = p["words"]
        for c in s["sfx"]:
            at = 0.0 if c["at_word"] == "start" else _when(words, c["at_word"], 0) / 1000
            tl.append({"file": audio.sfx(c["sound"]), "start": st + at, "kind": "sfx", "gain_db": -8})
        for b in p["beats"]:
            tl.append({"file": audio.sfx("soft cartoon pop", 1.5), "start": st + b["atMs"] / 1000, "kind": "sfx", "gain_db": -14})
        if p["_transition"] in ("slide", "wipe", "whip", "zoom") and st > 0:
            snd = "fast swoosh transition" if p["_transition"] in ("whip", "slide") else "quick paper whoosh"
            tl.append({"file": audio.sfx(snd, 1.5), "start": max(0, st - 0.15), "kind": "sfx", "gain_db": -12})
        if p["kind"] == "stage" and s.get("environment") in envs:   # environment ambience bed
            e = envs[s["environment"]]
            amb = audio.sfx(f"{e['ambience']}, continuous background ambience, no music, no speech", 10)
            tl.append({"file": amb, "start": st, "dur": dur, "kind": "ambience", "gain_db": -22})
        if p["kind"] == "hero" and os.path.exists(f"{proj}/hero/{s['id']}.mp4"):   # LTX's own synced sound
            amb = f"{proj}/work/{s['id']}_amb.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{proj}/hero/{s['id']}.mp4", "-vn", amb])
            if os.path.exists(amb): tl.append({"file": amb, "start": st, "kind": "sfx", "gain_db": -11})
    for b in beds:
        st = starts[b["scenes"][0]]
        lastp = next(p for p in props if p["id"] == b["scenes"][-1])
        en = starts[b["scenes"][-1]] + lastp["durationInFrames"] / C.FPS
        secs = sum(next(x for x in sc["scenes"] if x["id"] == i)["_dur"] for i in b["scenes"])
        if secs < 6: continue
        tl.append({"file": audio.music(b["mood"], secs + 4), "start": st, "dur": en - st, "kind": "music", "gain_db": (sc.get("mix") or {}).get("music_db", -15)})
    comfy.free()
    mix = audio.mix(tl, total, f"{proj}/work/mix.wav")
    final = f"{proj}/{os.path.basename(proj)}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{proj}/work/video.mp4", "-i", mix, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", final], check=True)
    # subtitles: one cue per caption-sized chunk, never spanning speakers
    srt, n = [], 1
    for p in props:
        chunk = []
        for w in p["words"] + [None]:
            if w is None or (chunk and (w["speaker"] != chunk[0]["speaker"] or len(" ".join(x["text"] for x in chunk)) > 38)):
                if chunk:
                    srt.append(f"{n}\n{srt_time(starts[p['id']] + chunk[0]['startMs'] / 1000)} --> {srt_time(starts[p['id']] + chunk[-1]['endMs'] / 1000 + 0.1)}\n"
                               f"{' '.join(x['text'] for x in chunk)}\n"); n += 1
                chunk = []
            if w is not None: chunk.append(w)
    open(f"{proj}/subtitles.srt", "w").write("\n".join(srt))
    chapters = ["0:00 Intro"] + [f"{int(starts[s['id']] // 60)}:{int(starts[s['id']] % 60):02d} {s.get('title_text') or 'Part'}"
                                 for s in sc["scenes"] if s["kind"] == "title_card" and starts[s["id"]] > 10]
    seo = sc.get("seo") or {"title": sc["title"], "description": sc["description"], "tags": sc["tags"], "hashtags": []}
    sc["seo"] = seo
    if seo.get("tags_v") != 2:      # big search tag set (fills YouTube's 500-char box), generated once by the local LLM
        from . import seo as SEO
        m = SEO.make(sc, open(f"{proj}/TOPIC").read().strip() if os.path.exists(f"{proj}/TOPIC") else sc["title"])
        seo.update(tags=m["tags"], hashtags=m["hashtags"] or seo.get("hashtags", []), tags_v=2)
        _j(f"{proj}/script.json", {k: v for k, v in sc.items() if not k.startswith("_")})
    from .seo import pack
    tags = pack(seo["tags"])
    hasreal = any(c.get("real_person") for c in sc["characters"])
    open(f"{proj}/YOUTUBE_UPLOAD.txt", "w").write(
        f"=== TITLE ===\n{seo['title'][:100]}\n\n\n=== DESCRIPTION ===\n{seo['description']}\n\n⏱️ Chapters\n" + "\n".join(chapters) +
        "\n\n📚 Sources\n" + "\n".join(f"- {u}" for u in sc["sources"]) +
        "\n\nThis video is commentary and analysis of news reports. Characters are fictional cartoon archetypes"
        + (" and caricatures" if hasreal else "") + ". Animation, voices and music were created with AI tools.\n\n"
        "🔔 Subscribe for more clear, quick breakdowns of the stories everyone's talking about.\n\n" + " ".join(seo["hashtags"]) +
        f"\n\n\n=== TAGS ===\n{', '.join(tags)}\n\n\n=== OTHER SETTINGS ===\n"
        "Thumbnail ............ thumbnail.png\nSubtitles ............ Upload file -> With timing -> subtitles.srt (English)\n"
        "Audience ............. Not made for kids\nCategory ............. News & Politics (or Education)\n"
        "Altered or synthetic . No for cartoon-only videos; YES if any realistic-looking AI footage is used\n"
        "Visibility ........... Unlisted first, check it, then Public\n")
    log(proj, f"master: {final} ({total / 60:.1f} min)")
    return final


def thumbnail(proj, sc):
    from . import imagegen
    out = f"{proj}/thumbnail.png"
    if os.path.exists(out): return out
    cast = [c["char"] for s in sc["scenes"] for c in s["cast"]]
    main = max(set(cast), key=cast.count) if cast else None
    base = os.path.join(C.CHAR_LIB, assets.slug(main), "base.png") if main else None
    prompt = (f"{C.ART_STYLE}. YouTube thumbnail, bold and dramatic: the character from image 1 (same face, hair and outfit) on the left "
              f"with an exaggerated shocked expression, big bold yellow comic text with thick black outline reading "
              f"\"{sc['thumbnail_text']}\" on the right, bright saturated background, high contrast")
    if base and os.path.exists(base):
        p = imagegen.edit(prompt, [base], f"{proj}/work", "thumb", 1280, 720, fixed_size=True)
        from PIL import Image
        im = Image.open(p).convert("RGB")
        if im.size != (1280, 720): im = im.resize((1280, 720), Image.LANCZOS)
        im.save(p)
    else:
        p = imagegen.t2i(prompt.replace("the character from image 1 (same face, hair and outfit)", "a cartoon presenter"), f"{proj}/work", "thumb", 1280, 720)
    shutil.copy(p, out); return out


# ---------------------------------------------------------------- driver
def make_video(topic, minutes=6, approve=False, rerender=None, run_qc=True, review=True):
    proj = project_dir(topic)
    t0 = time.time()
    log(proj, f"=== {topic} ({minutes} min) ===")
    P = (lambda name: progress.stage(proj, name)) if run_qc else (lambda name: None)   # outer run only
    P("script")
    sc = stage_script(proj, topic, minutes)
    if not (approve or os.path.exists(f"{proj}/APPROVED")):
        log(proj, f"STOP: review {proj}/SCRIPT_REVIEW.md (edit script.json if needed), then rerun with --approve")
        return proj
    open(f"{proj}/APPROVED", "w").write(time.ctime())
    raw = _j(f"{proj}/script.json")
    if ending.ensure_outro(raw, topic):            # every video gets a wrap-up + sign-off ending
        _j(f"{proj}/script.json", raw); log(proj, f"ending: added outro -> {raw['scenes'][-1]['lines'][-1]['text']}")
    sc = script.validate(raw)
    hard = [p for p in sc["_problems"] if "environment as the previous" not in p and "environments; need" not in p]
    if hard:
        raise SystemExit("script.json has problems: " + "; ".join(hard))
    P("voice"); stage_voice(proj, sc)
    P("assets"); stage_assets(proj, sc)
    P("hero"); stage_hero(proj, sc)
    P("talk"); stage_talk(proj, sc)
    P("sound"); beds = stage_sound(proj, sc)
    comfy.free()
    P("render"); props = build_props(proj, sc)
    stage_render(proj, props, only=set(rerender) if rerender else None)
    for attempt in range(2):
        problems = qc(proj, sc, props)
        if not problems: break
        log(proj, f"QC found {len(problems)} problem(s): {problems[:6]} -> repairing (attempt {attempt + 1})")
        ids = repair(proj, sc, problems)
        props = build_props(proj, sc)
        stage_render(proj, props, only=ids)
    problems = qc(proj, sc, props)
    if problems: log(proj, f"QC still reports: {problems}")
    P("master"); thumbnail(proj, sc)
    final = stage_master(proj, sc, props, beds)
    comfy.free()
    if review and not stage_review(proj):          # (skipped inside QC fix rounds; runs once at the end)
        log(proj, f"REVIEW: automatic checks FAILED — see {proj}/review/REVIEW.md")
    if run_qc:   # two-stage QC with automatic correction + re-inspection (see studio/qc)
        P("qc"); from . import qc as QC
        ok, sc_, _ = QC.run(proj, fix=True, rebuild=lambda p: make_video(topic, minutes, approve=True, run_qc=False, review=False))
        stage_review(proj)
        log(proj, f"QC {'PASS' if ok else 'FAIL'}: {sc_} — see {proj}/review/QC_REPORT.md")
    if run_qc and not os.path.exists(f"{proj}/NO_REEL"):   # Instagram Reel (+ its own checks), cut from the final video
        P("reel"); from . import reel
        try: reel.make(proj)
        except Exception as e: log(proj, f"REEL FAILED: {e!r} — rerun: python -m studio.reel {proj}")
    P("done")
    log(proj, f"done in {(time.time() - t0) / 60:.1f} min -> {final}")
    return final
