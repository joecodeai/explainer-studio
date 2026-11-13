#!/usr/bin/env python3
"""Pre-fetch research.json for a topic with a hand-written search query:  tools/research.py "<topic>" "<short news query>" """
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import news, pipeline
topic, q = sys.argv[1], sys.argv[2]
proj = pipeline.project_dir(topic)
open(f"{proj}/TOPIC", "w").write(topic)
for f in ("research.json", "script.json", "script.draft.json", "FACTCHECK.md", "SCRIPT_REVIEW.md"):
    if os.path.exists(f"{proj}/{f}"): os.remove(f"{proj}/{f}")
r = news.research(topic, max_articles=6, search=q)
json.dump(r, open(f"{proj}/research.json", "w"), indent=1)
for s in r["sources"]: print(len(s["text"]), s["url"][:90])
