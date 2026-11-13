"""YouTube search metadata: a large, packed tag set (fills YouTube's 500-character tag box) + hashtags, from the local LLM."""
import json, os, re
from . import llm

LIMIT = 495   # YouTube: 500 chars; multi-word tags are counted with surrounding quotes


def _cost(t):
    return len(t) + (2 if " " in t else 0) + 1      # + comma


def pack(tags, limit=LIMIT):
    out, seen, n = [], set(), 0
    for t in tags:
        t = re.sub(r"[#\"<>,]", "", t).strip().lower()
        t = re.sub(r"\s+", " ", t)
        if not t or len(t) > 60 or t in seen: continue
        if n + _cost(t) > limit: continue
        out.append(t); seen.add(t); n += _cost(t)
    return out


def make(sc, topic=""):
    """Returns {"tags": [...], "hashtags": [...]}. Mix of broad, specific, question-style and long-tail search phrases."""
    lines = " ".join(l["text"] for s in sc["scenes"] for l in s.get("lines", []))[:3000]
    year = re.search(r"20\d\d", topic + " " + sc.get("title", ""))
    yr = year.group(0) if year else "2026"
    prompt = (f"Video title: {sc.get('title')}\nTopic: {topic}\nScript excerpt: {lines}\n\n"
              "Write YouTube search tags for this news explainer so it shows up when people search. Give 50 tags, one per line, no numbering:\n"
              "- 10 broad topic tags (e.g. country name, 'world news', 'politics explained')\n"
              "- 12 specific tags: every important person, party, place, institution and event named in the script\n"
              "- 12 question / search-phrase tags real viewers type (e.g. 'why did X happen', 'what is X', 'X explained')\n"
              f"- 8 timely tags with '{yr}' or 'news today' / 'latest'\n"
              "- 8 long-tail phrases (3-6 words) combining the main subject with an angle\n"
              "All lowercase, no hashtags inside tags, no quotes, no duplicates, nothing misleading or unrelated to the video. Only use names exactly as they appear in the script — never guess party abbreviations or facts. "
              "Also give 4 short hashtags.")
    tags, hashtags = [], []
    try:
        r = llm.chat([{"role": "user", "content": prompt}], temperature=0.4, max_tokens=6000,
                     schema={"type": "object", "required": ["tags", "hashtags"],
                             "properties": {"tags": {"type": "array", "items": {"type": "string"}},
                                            "hashtags": {"type": "array", "items": {"type": "string"}}}})
        tags = [t.strip() for t in r.get("tags", []) if isinstance(t, str) and 1 < len(t.strip()) < 70 and not re.search(r"[:*]|\btags?\b", t)]
        hashtags = ["#" + re.sub(r"\W", "", h) for h in r.get("hashtags", []) if isinstance(h, str) and re.sub(r"\W", "", h)][:4]
    except Exception as e:
        print("seo: LLM tag generation failed:", e)
    # deterministic backbone (always present even if the LLM fails)
    base = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]+(?: [A-Z][a-z]+)*", sc.get("title", "")) if len(w) > 3]
    backbone = list(sc.get("tags") or []) + [topic.lower()[:58], f"{topic.lower()[:40]} explained", "news explained",
                f"world news {yr}", "explainer", "current events", "animated news", "news today"] + [b.lower() for b in base]
    # interleave the five groups (broad / specific / questions / timely / long-tail) so every kind fits in the 500 chars
    groups = [tags[0:10], tags[10:22], tags[22:34], tags[34:42], tags[42:]]
    mixed = [g[i] for i in range(max(map(len, groups)) if tags else 0) for g in groups if i < len(g)]
    tags = pack(mixed[:6] + backbone[:4] + mixed[6:] + backbone[4:])
    if not hashtags:
        hashtags = ["#Explained", "#News", "#WorldNews"]
    return {"tags": tags, "hashtags": hashtags[:4]}


def apply(proj, topic=None):
    """Regenerate tags for a finished project and update script.json + YOUTUBE_UPLOAD.txt in place (no re-render)."""
    sp = os.path.join(proj, "script.json"); sc = json.load(open(sp))
    topic = topic or (open(os.path.join(proj, "TOPIC")).read().strip() if os.path.exists(os.path.join(proj, "TOPIC")) else sc.get("title", ""))
    m = make(sc, topic)
    sc.setdefault("seo", {}).update(tags=m["tags"], hashtags=m["hashtags"], tags_v=2)
    json.dump(sc, open(sp, "w"), indent=1, ensure_ascii=False)
    up = os.path.join(proj, "YOUTUBE_UPLOAD.txt")
    if os.path.exists(up):
        t = open(up).read()
        t = re.sub(r"(=== TAGS ===\n).*?(\n\n)", lambda x: x.group(1) + ", ".join(m["tags"]) + x.group(2), t, flags=re.S)
        if m["hashtags"]:
            t = re.sub(r"(Subscribe[^\n]*\n\n)[^\n=]*", lambda x: x.group(1) + " ".join(m["hashtags"]), t, count=1)
        open(up, "w").write(t)
    return m
