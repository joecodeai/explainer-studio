"""Local fact-check: the LLM compares each scene's claims against the sources and lists only questionable lines (FACTCHECK.md)."""
import json, re
from . import llm


def run(proj):
    sc = json.load(open(f"{proj}/script.json")); res = json.load(open(f"{proj}/research.json"))
    src = "\n\n".join(f"[{i + 1}] {s['title']}\n{s['text'][:3500]}" for i, s in enumerate(res["sources"]))
    lines = [f"{s['id']} | {l['speaker']}: {l['text']}" for s in sc["scenes"] for l in s["lines"]]
    lines += [f"{s['id']} | CHART {s['chart']}" for s in sc["scenes"] if s["kind"] == "chart"]
    out = llm.chat([{"role": "user", "content": "You are a strict fact-checker. SOURCES below. Then SCRIPT lines. For every line that states a fact, "
        "number, name, date or quote that is NOT clearly supported by the sources (or is distorted/overstated), output one line:\n"
        "FLAG <scene id> | <the claim> | <why> | <corrected wording or 'cut'>\nJokes and opinions clearly framed as such are fine. "
        "If everything is supported, output: ALL CLEAR\n\nSOURCES:\n" + src + "\n\nSCRIPT:\n" + "\n".join(lines)}], temperature=0.1, max_tokens=2500)
    flags = [l for l in out.splitlines() if l.startswith("FLAG")]
    open(f"{proj}/FACTCHECK.md", "w").write("# Fact-check flags\n\n" + ("\n".join(f"- {f[5:]}" for f in flags) if flags else "ALL CLEAR") + "\n")
    return flags
