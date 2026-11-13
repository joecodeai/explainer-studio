"""Compact review aid: unsupported numbers, cast, hero lines, structure. Usage: python tools/review.py <project_dir>"""
import json, re, sys
P = sys.argv[1]
sc = json.load(open(f"{P}/script.json")); res = json.load(open(f"{P}/research.json"))
src = " ".join(s["text"] for s in res["sources"]).lower().replace(",", "")
from collections import Counter
print("TITLE:", sc["title"], "| scenes", len(sc["scenes"]), dict(Counter(s["kind"] for s in sc["scenes"])),
      "| words", sum(len(s["narration"].split()) for s in sc["scenes"]))
print("SOURCES:", [s["title"][:50] for s in res["sources"]])
for c in sc["characters"]: print("CHAR", c["id"], "| real" if c.get("real_person") else "", "|", c["look"][:60])
print("ENVS", [e["id"] for e in sc["environments"]])
for s in sc["scenes"]:
    for l in s["lines"]:
        t = l["text"].replace("*", "")
        nums = [n for n in re.findall(r"\d[\d,.]*", t) if n.replace(",", "").rstrip(".") not in src]
        words = {"one": "1", "two": "2", "three": "3"}
        if nums: print(f"NUM? {s['id']} {l['speaker']}: {t}  -> not in sources: {nums}")
    if s["kind"] == "hero": print(f"HERO {s['id']}: {s['lines'][0]['text'][:110]}")
    if s["kind"] == "map": print(f"MAP {s['id']}: {s['map']['countries']} {[p['name'] for p in s['map']['places']]} routes={[(r['from'], r['to']) for r in s['map']['routes']]}")
    if s["kind"] == "chart": print(f"CHART {s['id']}: {s['chart']}")

for s in sc["scenes"]:
    if s["kind"] == "title_card":
        print(f"CARD {s['id']}: {s.get('title_text')!r}" + ("   <-- WRITE A SHORT TITLE (<=5 words, not a sentence fragment)" if not s.get("title_text") or s.get("_needs_title") else ""))
    if s["kind"] == "hero":
        print(f"HERO {s['id']}: {s.get('hero_prompt', '')[:110]}  <-- must ask for NO words/dates/numbers")
