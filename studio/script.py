"""Script v2: a storyboard of scenes made of dialogue LINES (narrator + characters, each with emotion, pose and camera shot),
timed visual BEATS, varied ENVIRONMENTS, informative MAPS and per-scene TRANSITIONS. Free-form JSON from Qwen3.6, normalised + validated."""
import json, re
from . import config as C, llm

EMOTIONS = ["neutral", "happy", "excited", "angry", "worried", "surprised", "confused", "sad", "confident", "sarcastic"]
SHOTS = ["wide", "two_shot", "closeup", "detail"]
KINDS = ["stage", "map", "title_card", "chart", "hero"]
TRANSITIONS = ["cut", "slide", "zoom", "wipe", "whip", "fade"]
MUSIC = ["tense", "upbeat", "sad", "epic", "comedic", "mysterious"]
BEATS = ["keyword", "number", "label"]
ICONS = ["ship", "plane", "truck", "money", "none"]
EMOTION_POSE = {"neutral": "talk", "happy": "happy", "excited": "arms_up", "angry": "angry", "worried": "worried",
                "surprised": "surprised", "confused": "shrug", "sad": "worried", "confident": "point", "sarcastic": "shrug"}

SCHEMA = {"type": "object", "required": ["title", "thumbnail_text", "characters", "environments", "scenes", "sources"], "properties": {
    "title": {"type": "string"}, "thumbnail_text": {"type": "string"}, "description": {"type": "string"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "characters": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"}, "name": {"type": "string"}, "look": {"type": "string"}, "voice": {"type": "string"}, "role": {"type": "string"}, "real_person": {"type": "boolean"}}}},
    "environments": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"}, "prompt": {"type": "string"}, "ambience": {"type": "string"}}}},
    "scenes": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"}, "kind": {"enum": KINDS}, "environment": {"type": "string"},
        "cast": {"type": "array", "items": {"type": "object", "properties": {"char": {"type": "string"}, "position": {"enum": ["left", "right", "center"]}}}},
        "lines": {"type": "array", "items": {"type": "object", "properties": {
            "speaker": {"type": "string"}, "text": {"type": "string"}, "emotion": {"enum": EMOTIONS},
            "pose": {"enum": C.POSES}, "shot": {"enum": SHOTS}}}},
        "beats": {"type": "array", "items": {"type": "object", "properties": {
            "at_word": {"type": "string"}, "type": {"enum": BEATS}, "text": {"type": "string"}}}},
        "title_text": {"type": "string"},
        "map": {"type": "object", "properties": {
            "label": {"type": "string"}, "countries": {"type": "array", "items": {"type": "string"}},
            "places": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "lat": {"type": "number"}, "lon": {"type": "number"}}}},
            "routes": {"type": "array", "items": {"type": "object", "properties": {
                "from": {"type": "string"}, "to": {"type": "string"}, "via": {"type": "array", "items": {"type": "string"}},
                "label": {"type": "string"}, "icon": {"enum": ICONS}, "blocked": {"type": "boolean"}}}}}},
        "chart": {"type": "object", "properties": {"labels": {"type": "array", "items": {"type": "string"}},
                                                   "values": {"type": "array", "items": {"type": "number"}}, "unit": {"type": "string"}, "title": {"type": "string"},
                                                   "mode": {"type": "string"}, "items": {"type": "array", "items": {"type": "object", "properties": {
                                                       "value": {"type": "string"}, "label": {"type": "string"}}}}}},
        "hero_prompt": {"type": "string"},
        "transition": {"enum": TRANSITIONS},
        "sfx": {"type": "array", "items": {"type": "object", "properties": {"at_word": {"type": "string"}, "sound": {"type": "string"}}}},
        "music": {"enum": MUSIC}}}},
    "sources": {"type": "array", "items": {"type": "string"}}}}

SYSTEM = f"""You write and storyboard animated YouTube explainers about trending news, in the style of the best casual
explainer channels: fast, clear, accurate and credible, but FUN to watch — a deadpan, witty presenter who reacts to the news like a real person, with recurring illustrated characters who TALK TO EACH OTHER.

FACTS
- Use ONLY facts in the provided sources. Never invent numbers, quotes, names or dates. Attribute claims ("according to ...").
- Prefer archetype characters (a small-town mayor, a tech CEO, a farmer, a power-grid engineer) over real people.
  If a real public figure must appear, mark real_person=true and keep it a respectful, realistic editorial illustration (no caricature). No real private individuals.

STORY
- Most viewers leave in the first 6 seconds. Scene 1 = the narrator: line 1 states the most striking fact plainly (emotion "excited",
  max ~16 words), line 2 is a short offhand deadpan reaction that also asks THE RUNNING-GAG QUESTION (emotion "sarcastic", max ~14 words),
  e.g. "The yen is nearly 160 to the dollar." / "So, is Japan worried? Hard to say, really." Shown visually (hero shot or map), not a talking head.
- Structure: hook -> why it matters -> background -> what happened -> twist/complication -> what's next -> punchy callback joke -> FINAL scene: a narrator "title_card" that wraps up the story in one sentence (the key takeaway / what to watch next) and signs off (\"Thanks for watching — subscribe for more explainers.\"). Never end on a character line or a question.
- About 155 spoken words per minute. A visual change at EVERY new idea (new shot, beat, map element or scene).
- RUNNING GAG (the core of the humour): one simple question about the story ("Is Japan worried?", "Is the strait open?",
  "Is peace close?") that the narrator keeps answering with mock caution ("Hard to say." / "Depends who you ask." / "Let's not get
  ahead of ourselves.") while the REAL facts that pile up make the answer more and more obvious. Ask it in scene 1, call it back
  2-3 times in narrator lines right after an escalating fact ("Tokyo has spent a record ¥27 trillion. Worried? Maybe they just
  really like yen."), and pay it off just before the final title_card ("Record spending, daily warnings... we still can't rule out
  that they're fine."). The deadpan understatement is the joke; the facts stay exact.
- Other humour: an offhand presenter reaction or a character aside every ~30 s. It must sound SPONTANEOUS, like a quick human
  reaction ("Just... sort of parked." / "Which is a polite word for a loophole." / "Honestly? Mostly paperwork."), not a
  written punchline. Short, conversational, varied. Never reuse stock phrases like "the classic ... strategy". Don't overdo it:
  natural first. Never more than one joke in a row, never at the expense of facts, never about deaths, victims, tragedies or
  ordinary people (on very serious topics keep the gag about officials, bureaucracy or markets, and keep it gentle).
- Voice: give narrator lines a real emotion — "excited" for the hook fact, "sarcastic" for gag lines and asides,
  "worried"/"sad" for grave facts, "neutral" otherwise — so the delivery changes tone instead of sounding monotonous.

SCENES (kinds: {KINDS})
- "stage": 2 characters (sometimes 1 or 3) in an environment, having a short conversation. Each scene has 2-6 LINES.
  A line is ONE speaker: "narrator" or a character id. Characters must look/act like they're talking to each other:
  questions, interruptions ("Wait—"), reactions ("Seriously?"), disagreements. The narrator bridges and explains.
  Each line gets: emotion {EMOTIONS}; pose for the speaker from {C.POSES}
  ("side_talk"/"side_listen" = turned toward the other character — use them a lot in conversations); shot {SHOTS}
  (wide = establishing, two_shot = conversation, closeup = punchline/emotional reaction, detail = focus on a beat graphic).
  Vary shots line to line. 1-3 sentences per line, max ~30 words. Wrap the 1-2 most important words of a line in *asterisks* (caption emphasis).
- "map": geography explained step by step. countries = countries to highlight (English names, in the order mentioned).
  places = cities/ports/landmarks with accurate lat/lon. routes = from/to place names (optionally via places), a short label,
  icon {ICONS} that travels along the route, blocked=true for a closed/blocked route. Narration lines on maps are by the narrator.
  Routes are drawn as straight great-circle segments between stops: for SEA routes add waypoint places at sea (straits, capes,
  ocean points) in "via" so no segment crosses land; every from/to/via name must be listed in places with accurate lat/lon.
- "chart": ONLY numbers that appear in the sources. mode "bars" = 2-5 comparable values in ONE unit (labels, values, unit, title);
  mode "stats" = 1-3 big headline figures that do not share a unit, as items [{{value:"750,000", label:"new homes needed (Bank of Spain)"}}];
  mode "timeline" = 2-5 dated events as items [{{value:"Oct 5", label:"Snap election called"}}]. Never invent a number or a poll.
- map: label = a short news headline (3-5 words, e.g. "Strike hits major cities"), never "...Map". countries = only a country the line is
  about AS A WHOLE; for states, regions or cities use places (lat/lon) instead of colouring the whole country.
- "hero": a cinematic editorial-illustration shot for big moments (1 in ~8 scenes) — vivid 1-2 sentence hero_prompt, no real faces. The hero_prompt must NOT ask for any written words, dates, numbers, labels, signs or headlines (image models garble text) — show the idea with objects, colour and action instead.
  Its LINES are normal narration that moves the story on — NEVER describe the shot in the narration.
- Never create a character called "narrator"; the narrator is an off-screen voice. Never draw real people as characters.
- Map routes only for real movements (shipping, flights, migration, supply chains) — never connect unrelated places just to decorate.
- "title_card": 2-3 short chapter cards (title_text <= 5 words), one line of narration each.
- beats: timed graphics INSIDE a scene that explain the narration: keyword (1-3 big words), number (a figure from the sources,
  e.g. "$64 billion"), label (short sticker). at_word = an exact word from that scene's lines. 1-2 beats per scene.
- environments: 5-6 DISTINCT locations that exist IN THIS STORY's country and topic (real kinds of places where these events
  happen — think about the story, do not use generic tech/industry sets). Never use the same environment in two consecutive stage scenes. ambience = what it sounds like.
- transition into each scene: one of {TRANSITIONS}; vary them; "cut" for fast back-and-forth, "zoom" into maps, "wipe"/"slide" for topic changes.
- sfx: 0-2 per scene, at_word = an exact word from the lines (or "start"): whoosh, pop, cash register, crowd murmur, etc.
- music mood per scene from {MUSIC}; keep the same mood for runs of scenes and build intensity toward the twist.

CHARACTERS (3-5)
- id snake_case; look = description for an editorial illustrator, adult realistic proportions, muted newsroom colours (no word "cartoon") (age, hair, face, clothes, colours, a signature prop); role = short on-screen job title for the name tag (real people: their real title, e.g. "Prime Minister of Spain"; invented characters: e.g. "Union organiser"; everyman: "");
  voice = distinct voice description for a voice actor: gender, age, accent, pitch, timbre, pace, energy. Make every voice
  clearly different (mix genders, ages and accents). Include "everyman", a plain everyday person who asks the audience's questions.

Return ONE JSON object only.
"""


def _brief(pack, minutes):
    src = "\n\n".join(f"[{i + 1}] {s['title']} ({s['url']})\n{s['text'][:5000]}" for i, s in enumerate(pack["sources"]))
    return (f"Topic: {pack['topic']}\nTarget length: {minutes} minutes (~{int(minutes * 155)} spoken words, about "
            f"{int(minutes * 60 / 12)} scenes).\n\nSOURCES:\n{src}\n\nReturn the JSON.")


def write(pack, minutes):
    msg = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": _brief(pack, minutes)}]
    return validate(llm.chat(msg, SCHEMA, temperature=0.8, max_tokens=30000))


def _id(x):
    return re.sub(r"[^a-z0-9_]+", "_", str(x).lower()).strip("_")


def normalize(d):
    for k, v in (("title", "Untitled"), ("thumbnail_text", ""), ("description", ""), ("tags", []), ("characters", []),
                 ("environments", d.get("backgrounds", [])), ("scenes", []), ("sources", [])):
        d.setdefault(k, v)
    d["characters"] = [c for c in d["characters"] if _id(c.get("id") or c.get("name", "")) not in ("narrator", "")]
    for c in d["characters"]:
        c.setdefault("name", c.get("id", "?")); c.setdefault("look", c["name"]); c.setdefault("real_person", False)
        c.setdefault("voice", "an ordinary adult voice, clear, natural pace")
        c["id"] = _id(c.get("id") or c["name"])
    for e in d["environments"]:
        e["id"] = _id(e.get("id", "env")); e.setdefault("prompt", e["id"]); e.setdefault("ambience", "quiet room tone")
    chars = {c["id"] for c in d["characters"]}
    for i, s in enumerate(d["scenes"]):
        s["id"] = f"s{i + 1:02d}"
        if s.get("kind") not in KINDS: s["kind"] = "stage"
        s["environment"] = _id(s.get("environment") or s.get("background") or "")
        s["cast"] = [{"char": _id(c.get("char")), "position": c.get("position") if c.get("position") in ("left", "right", "center") else "center"}
                     for c in s.get("cast", []) if isinstance(c, dict) and _id(c.get("char", "")) in chars][:3]
        lines = s.get("lines") or ([{"speaker": "narrator", "text": s["narration"]}] if s.get("narration") else [])
        s["lines"] = []
        for ln in lines:
            if not isinstance(ln, dict) or not str(ln.get("text", "")).strip(): continue
            spk = _id(ln.get("speaker", "narrator")) or "narrator"
            if spk not in chars: spk = "narrator"
            emo = ln.get("emotion") if ln.get("emotion") in EMOTIONS else "neutral"
            pose = ln.get("pose") if ln.get("pose") in C.POSES else EMOTION_POSE[emo]
            shot = ln.get("shot") if ln.get("shot") in SHOTS else "two_shot"
            s["lines"].append({"speaker": spk, "text": " ".join(str(ln["text"]).split()), "emotion": emo, "pose": pose, "shot": shot})
        if s["kind"] in ("map", "chart", "title_card", "hero"):
            for ln in s["lines"]: ln["speaker"] = "narrator" if s["kind"] != "hero" else ln["speaker"]
        # a character who speaks in a stage scene must be on stage
        if s["kind"] == "stage":
            onstage = {c["char"] for c in s["cast"]}
            for ln in s["lines"]:
                if ln["speaker"] != "narrator" and ln["speaker"] not in onstage and len(s["cast"]) < 3:
                    s["cast"].append({"char": ln["speaker"], "position": "center"}); onstage.add(ln["speaker"])
            pos = ["left", "right"] if len(s["cast"]) == 2 else ["left", "center", "right"] if len(s["cast"]) == 3 else ["center"]
            for c, p in zip(s["cast"], pos): c["position"] = p
        s["narration"] = " ".join(ln["text"] for ln in s["lines"])
        s["beats"] = [b for b in s.get("beats", []) if isinstance(b, dict) and b.get("text")][:3]
        for b in s["beats"]:
            if b.get("type") not in BEATS: b["type"] = "keyword"
            b.setdefault("at_word", "start")
        s["title_text"] = s.get("title_text") or s.get("on_screen_text") or ""
        if s["kind"] == "title_card" and not s["title_text"] and s["lines"]:   # derive a short chapter title
            # use the first clause if it is short; otherwise mark it so the review step writes a real title
            clause = re.split(r"[.…?!,—:;]| but | and ", s["lines"][0]["text"].replace("*", ""))[0].strip()
            words = clause.split()
            s["title_text"] = clause.title().replace("'S ", "'s ") if 1 <= len(words) <= 5 else ""
            if not s["title_text"]: s["_needs_title"] = True
        m = s.get("map") or {}
        m["routes"] = [r for r in m.get("routes", []) if isinstance(r, dict) and r.get("icon") not in (None, "none") and r.get("from") != r.get("to")]
        s["map"] = {"label": m.get("label", ""), "countries": [str(x) for x in m.get("countries", [])],
                    "places": [p for p in m.get("places", []) if isinstance(p, dict) and isinstance(p.get("lat"), (int, float)) and isinstance(p.get("lon"), (int, float))],
                    "routes": [r for r in m.get("routes", []) if isinstance(r, dict) and r.get("from") and r.get("to")]}
        for r in s["map"]["routes"]:
            r.setdefault("via", []); r.setdefault("label", ""); r["blocked"] = bool(r.get("blocked"))
            if r.get("icon") not in ICONS: r["icon"] = "none"
        ch = s.get("chart") or {}
        items = [{"value": str(it.get("value", "")).strip(), "label": str(it.get("label", "")).strip()} for it in ch.get("items") or []
                 if isinstance(it, dict) and str(it.get("value", "")).strip()]
        s["chart"] = {"labels": ch.get("labels", []), "values": [v for v in ch.get("values", []) if isinstance(v, (int, float))],
                      "unit": ch.get("unit", ""), "title": ch.get("title", ""),
                      "mode": ch.get("mode") if ch.get("mode") in ("bars", "stats", "timeline") else "bars", "items": items}
        c2 = s["chart"]
        # bars only make sense for comparable numbers in one unit; wildly different magnitudes (2 vs 750,000) become stat cards
        if c2["mode"] == "bars" and c2["values"] and len(c2["values"]) == len(c2["labels"]):
            pos = [abs(v) for v in c2["values"] if v]
            if len(c2["values"]) < 2 or (pos and max(pos) / max(min(pos), 1e-9) > 25):
                c2["mode"] = "stats"
                c2["items"] = [{"value": f"{v:,.0f}" if v == int(v) else f"{v:,}", "label": l} for v, l in zip(c2["values"], c2["labels"])]
        if s["kind"] == "chart" and not (c2["mode"] != "bars" and c2["items"]) and (not c2["values"] or len(c2["values"]) != len(c2["labels"])):
            s["kind"] = "stage"
        s.setdefault("hero_prompt", "")
        if s.get("transition") not in TRANSITIONS: s["transition"] = "cut"
        if s.get("music") not in MUSIC: s["music"] = "upbeat"
        s["sfx"] = [x for x in s.get("sfx", []) if isinstance(x, dict) and x.get("sound")][:3]
        for x in s["sfx"]: x.setdefault("at_word", "start")
    d["scenes"] = [s for s in d["scenes"] if s["lines"]]
    return d


def autofix(d):
    """Fix small structural issues locally (no LLM round-trip): drop routes whose places lack coordinates,
    and swap environments so the same location never appears in two consecutive stage scenes."""
    for s in d["scenes"]:
        names = {p["name"] for p in s["map"]["places"]}
        s["map"]["routes"] = [r for r in s["map"]["routes"] if all(n in names for n in [r["from"], r["to"], *r["via"]])]
    envs = [e["id"] for e in d["environments"]]
    prev = None
    for s in d["scenes"]:
        if s["kind"] != "stage": continue
        if s["environment"] not in envs and envs: s["environment"] = envs[0]
        if s["environment"] == prev and len(envs) > 1:
            s["environment"] = next(e for e in envs if e != prev)
        prev = s["environment"]
    return d


def validate(d):
    d = autofix(normalize(d))
    envs = {e["id"] for e in d["environments"]}
    probs, prev_env = [], None
    if len(envs) < 4: probs.append(f"only {len(envs)} environments; need 4-6 distinct locations")
    for s in d["scenes"]:
        if s["kind"] == "stage":
            if not s["cast"]: probs.append(f"{s['id']}: stage scene with no characters on stage")
            if s["environment"] not in envs: probs.append(f"{s['id']}: unknown environment '{s['environment']}'")
            if s["environment"] == prev_env: probs.append(f"{s['id']}: same environment as the previous stage scene")
            prev_env = s["environment"]
        if s["kind"] == "hero" and not s["hero_prompt"].strip(): probs.append(f"{s['id']}: hero scene without hero_prompt")
        if s["kind"] == "map" and not (s["map"]["countries"] or s["map"]["places"]): probs.append(f"{s['id']}: map with nothing to show")
        if s["kind"] == "map":
            names = {p["name"] for p in s["map"]["places"]}
            for r in s["map"]["routes"]:
                for n in [r["from"], r["to"], *r["via"]]:
                    if n not in names: probs.append(f"{s['id']}: route place '{n}' missing from places (add it with lat/lon)")
    d["_problems"] = probs
    return d


def repair(d, system=None):
    if not d.get("_problems"):
        return d
    msg = [{"role": "system", "content": system or SYSTEM},
           {"role": "user", "content": "This storyboard has problems:\n- " + "\n- ".join(d["_problems"][:30]) +
            "\nFix them and return the full corrected JSON.\n" + json.dumps({k: v for k, v in d.items() if not k.startswith('_')})}]
    return validate(llm.chat(msg, SCHEMA, temperature=0.3, max_tokens=30000))


# ---------------------------------------------------------------- recurring show (library/show.json)
import os


def load_show():
    """The channel's recurring show (cast, art style), or None. PLAIN=1 makes a plain explainer instead."""
    f = os.path.join(C.LIBRARY, "show.json")
    if os.environ.get("PLAIN") == "1" or not os.path.exists(f): return None
    sh = json.load(open(f))
    return sh if sh.get("active", True) else None


def show_system(sh):
    lead = sh["cast"][0]
    nar = next((c for c in sh["cast"] if c["id"] == sh.get("narrator")), None)
    cast = "\n".join(f"  - id \"{c['id']}\" ({c['name']}{', ' + c['role'] if c.get('role') else ''}): {c.get('bio', '')}" for c in sh["cast"])
    scenes = SYSTEM[SYSTEM.index("SCENES (kinds"):SYSTEM.index("CHARACTERS (3-5)")]
    return f"""You write and storyboard episodes of "{sh['name']}", an animated YouTube comedy-explainer series.
{lead['name']} is a lovable, confidently clueless guy. Every episode something real (a news story, money, career, dating, social life,
health, tech) hits HIS life; he gets it hilariously wrong; {nar['name'] if nar else 'the NARRATOR'} (dry, warm, witty, has known {lead['name']} far
too long) explains how it really works with real facts, maps and charts. {lead['name']} learns — and so does the viewer. Funny AND informative.

RECURRING CAST (use these exact ids; do not redefine their look or voice):
{cast}
  - "narrator": {(nar['name'] + "'s voice-over — " + nar['name'] + " tells the story to the viewer (same voice as on screen) and is the straight man who corrects " + lead['name']) if nar else "off-screen voice, the straight man"} ("No, {lead['name']}." / "That's... not what that means.").
    {("Use speaker 'narrator' for " + nar['name'] + "'s voice-over on maps, charts, hero shots and title cards; use speaker '" + nar['id'] + "' when she is ON SCREEN talking with " + lead['name'] + " in stage scenes. Put " + nar['name'] + " and " + lead['name'] + " on stage together in most stage scenes: he gets it wrong, she corrects him, he reacts. Their banter is the heart of the show — friendly, playful, never mean.") if nar else ""}
Add 0-2 GUEST characters per episode only when the story needs them (a landlord, a boss, a date, a banker, an expert).

FACTS
- Use ONLY facts in the provided sources. Never invent numbers, quotes, names or dates. Attribute claims ("according to ...").
- {lead['name']}'s mistakes are the joke — the facts are never wrong. When he says something false, the narrator corrects it on screen.
- Never put real people on screen as characters and never invent quotes from real people.

EPISODE STRUCTURE
1. COLD OPEN (first 6 seconds — most viewers leave here): a "hero" or "stage" scene. Narrator line 1 (emotion "excited", max ~16 words)
   states the funny situation: {lead['name']} did something dumb because of the topic ("{lead['name']} just cancelled his Japan trip
   because he heard the yen collapsed."). Line 2: a short deadpan narrator reaction that hints at the real fact (emotion "sarcastic",
   max ~14 words): "The yen collapsing is the best thing that ever happened to his holiday."
2. {lead['name']} says his catchphrase early (scene 2 or 3): "Okay, but how does this affect *me*?" — then the narrator promises what we'll learn.
3. {lead['name']}'s WRONG THEORY: a short funny stage scene showing the misconception viewers may share.
4. EXPLAIN in 3-4 chunks (map / chart / hero / stage). After each chunk {lead['name']} reacts or asks the next "dumb" question —
   which is really the viewer's question. Keep facts exact and concrete (numbers from the sources).
5. HOW IT REALLY AFFECTS {lead['name'].upper()}: his wallet, job, rent, dating life or plans — concrete and relatable.
6. {lead['name']} TRIES TO USE THE LESSON and gets it 80% right — the payoff joke.
7. FINAL scene: a narrator "title_card" with the one-sentence takeaway for the viewer, then {lead['name']} asks the audience one
   question for the comments (a character line is allowed here: "Would you have cancelled the trip? Tell me in the comments."),
   then the narrator signs off ("Subscribe — {lead['name']} has a lot more to learn.").

HUMOUR
- Character comedy, not stand-up: the joke is {lead['name']}'s logic, reactions and over-confidence, and the narrator's understatement.
- A {lead['name']} reaction or exchange every ~20-30 s. Jokes must sound spontaneous and conversational, never a written punchline.
  Vary them. Never reuse stock phrases. One joke at a time.
- {lead['name']} is dumb but never cruel, sexist or offensive; he is likeable and he genuinely learns.
- Never joke about deaths, victims, tragedies, illness or ordinary people's suffering. If the topic has a tragic side, keep {lead['name']}
  out of it and let the narrator state it plainly.
- Voice: give every line a real emotion — {lead['name']} is very expressive (excited, confused, surprised, worried, happy); the narrator
  is "excited" for the hook, "sarcastic" for dry asides, "neutral" for explaining. Vary the tone; never monotonous.
- About 155 spoken words per minute; a visual change at EVERY new idea; {lead['name']} appears in at least half of the stage scenes.

{scenes}
GUEST CHARACTERS (only if needed)
- id snake_case; look = description for an illustrator, adult realistic proportions (age, hair, face, clothes, colours, a prop);
  role = short on-screen job title; voice = distinct voice description (gender, age, accent, pitch, pace, energy), clearly different
  from the recurring cast.
- In "characters" list the recurring cast members who appear (just id + name) plus any guests.

Return ONE JSON object only.
"""


def apply_show(d, sh):
    """Force the recurring cast's look/voice/name and the show's art style onto the storyboard."""
    fixed = {c["id"]: c for c in sh["cast"]}
    used = {ln["speaker"] for s in d["scenes"] for ln in s["lines"]} | {c["char"] for s in d["scenes"] for c in s["cast"]}
    chars = [c for c in d["characters"] if c["id"] not in fixed]
    for cid, c in fixed.items():
        if cid in used or cid == sh["cast"][0]["id"]:
            chars.insert(0, {k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person")})
    for c in chars: c["style"] = sh["style"]
    for e in d.get("environments", []):
        if sh.get("bg_style"): e["style"] = sh["bg_style"]
    d["characters"] = chars
    d["show"] = sh["name"]
    if sh.get("narrator"):
        d["narrator_voice"] = sh["narrator"]
        if all(c["id"] != sh["narrator"] for c in chars):
            c = fixed[sh["narrator"]]; chars.append({k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person")} | {"style": sh["style"]})
    return d


def write_episode(pack, minutes, sh):
    msg = [{"role": "system", "content": show_system(sh)}, {"role": "user", "content": _brief(pack, minutes)}]
    raw = llm.chat(msg, SCHEMA, temperature=0.85, max_tokens=30000)
    ids = {c["id"] for c in sh["cast"]}
    raw.setdefault("characters", [])
    have = {_id(c.get("id") or c.get("name", "")) for c in raw["characters"] if isinstance(c, dict)}
    raw["characters"] += [{"id": c["id"], "name": c["name"], "look": c["look"], "voice": c["voice"]} for c in sh["cast"] if c["id"] not in have]
    d = validate(raw)
    return apply_show(d, sh)
