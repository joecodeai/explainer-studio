"""Proper endings: every video closes with a narrator wrap-up (one-line takeaway) and a sign-off card.
Used by the pipeline (before voicing) and by QC (check + auto-fix)."""
import re

SIGNOFF = re.compile(r"thanks? (you )?for watching|subscribe|see you (next|in the)|until next time|catch you", re.I)
OUTRO_TAG = "_outro"


def problems(sc):
    """List of reasons the script has no proper ending (empty = fine)."""
    scenes = sc.get("scenes") or []
    if not scenes: return ["no scenes"]
    last = scenes[-1]; lines = last.get("lines") or []
    out = []
    if not lines: return ["last scene has no closing line"]
    final = lines[-1]
    if final.get("speaker") != "narrator":
        out.append("video ends mid-conversation (last line is a character, no narrator wrap-up)")
    if not SIGNOFF.search(" ".join(l["text"] for l in lines)):
        out.append("no sign-off (thanks for watching / subscribe) at the end")
    if final["text"].rstrip().endswith("?"):
        out.append("video ends on an unanswered question")
    return out


def _takeaway(sc, topic=""):
    """One-sentence wrap-up of the whole story, from the local LLM (fallback: generic)."""
    from . import llm
    text = " ".join(l["text"] for s in sc["scenes"] for l in s.get("lines", []))[-2500:]
    try:
        r = llm.chat([{"role": "user", "content":
                       f"Video: {sc.get('title')}\nTopic: {topic}\nEnd of script: {text}\n\n"
                       "Write the narrator's closing line for this news explainer: ONE sentence (max 22 words) that sums up the key "
                       "takeaway / what to watch next, slightly dry and witty, no new facts, no question. Then a separate short sign-off "
                       "sentence inviting viewers to subscribe (max 10 words)."}],
                     temperature=0.5, max_tokens=3000,
                     schema={"type": "object", "required": ["takeaway", "signoff"],
                             "properties": {"takeaway": {"type": "string"}, "signoff": {"type": "string"}}})
        t, s = r["takeaway"].strip().replace("*", ""), r["signoff"].strip().replace("*", "")
        if t and not t.endswith("?") and len(t.split()) <= 30 and SIGNOFF.search(s):
            return f"{t} {s}"
    except Exception as e:
        print("ending: LLM outro failed:", e)
    return "That's the story so far — we'll be watching what happens next. Thanks for watching, and subscribe for more explainers."


def ensure_outro(sc, topic=""):
    """Append a narrator outro title card if the script has no proper ending. Returns True if the script changed."""
    if not problems(sc): return False
    last = sc["scenes"][-1]
    if last.get(OUTRO_TAG):            # an outro we added earlier is being re-checked: just rewrite its line
        last["lines"][-1]["text"] = _takeaway(sc, topic); return True
    n = len(sc["scenes"]) + 1
    sc["scenes"].append({
        "id": f"s{n:02d}", "kind": "title_card", "environment": "", "cast": [], OUTRO_TAG: True,
        "lines": [{"speaker": "narrator", "text": _takeaway(sc, topic), "emotion": "happy", "pose": "neutral", "shot": "detail"}],
        "beats": [{"at_word": "watching", "type": "keyword", "text": "THANKS!"}],
        "title_text": "Thanks for Watching", "map": {"label": "", "countries": [], "places": [], "routes": []},
        "chart": {"labels": [], "values": [], "unit": "", "title": ""}, "hero_prompt": None, "transition": "fade",
        "sfx": [], "music": last.get("music") or "upbeat"})
    return True
