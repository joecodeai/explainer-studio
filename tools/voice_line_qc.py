"""QC the voiced lines of a voice test: word accuracy (distil-large-v3), pace vs the delivery profile, and
silences inside a sentence (the user's rule: never pause mid-sentence; a stop only at sentence/clause ends).

  python tools/voice_line_qc.py projects/batbomb-voice-test
"""
import glob, json, os, re, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import hashlib
from studio import voice, script
from studio.voice import _line_key
for c in script.load_show()["cast"]:          # same engine tags narrate() sets, so the cache keys match
    t = c.get("tts") or {}
    if t.get("engine") == "qwen_custom": voice._SPK_TAG[c["id"]] = f"qc_{t['speaker']}"
    if t.get("engine") == "qwen_design": voice._SPK_TAG[c["id"]] = "qd_" + hashlib.md5(t["design"].encode()).hexdigest()[:6]
    if t.get("engine") == "qwen_clone": voice._SPK_TAG[c["id"]] = "ql_" + hashlib.md5(open(t["ref_audio"], "rb").read()).hexdigest()[:6]

proj = sys.argv[1]
lines = json.load(open(os.path.join(proj, "lines.json")))
pace = {v: json.load(open(f"library/voices/{v}/delivery.json"))["pace_words_per_sec"] for v in ("maya", "benny")}
from faster_whisper import WhisperModel
asr = WhisperModel("distil-large-v3", device="cuda", compute_type="float16")


def load16(f):
    from scipy.signal import resample_poly
    a, sr = sf.read(f, dtype="float32")
    if a.ndim > 1: a = a.mean(axis=1)
    g = np.gcd(sr, 16000)
    return resample_poly(a, 16000 // g, sr // g).astype(np.float32)


def norm(t):
    t = t.lower().replace("’", "'")
    t = re.sub(r"(\d)\s*,\s*(\d{3})", r"\1\2", t)                     # 100,000 / "100 ,000" -> 100000
    t = re.sub(r"\bfire\s+bomb", "firebomb", t)
    for a, b in [("a hundred thousand", "100000"), ("a hundred and fifty", "150"), ("three thousand", "3000"), ("a thousand", "1000"),
                 ("twenty", "20"), ("thirty", "30"), ("fifteen", "15"), ("'round", "round"), ("free-tailed", "freetailed"), ("free tailed", "freetailed")]:
        t = t.replace(a, b)
    t = re.sub(r"\b(\w+in)'", r"\1g", t)                             # flyin' -> flying, puttin' -> putting
    return re.findall(r"[a-z0-9']+", t)


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = np.arange(len(h) + 1)
    for i, rw in enumerate(r, 1):
        prev, d[0] = d.copy(), i
        for j, hw in enumerate(h, 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (rw != hw))
    return d[-1] / max(1, len(r))


rows, bad = [], 0
files = sorted(glob.glob(os.path.join(proj, "audio", "lines", "*.wav")))
for s in lines:
    for i, ln in enumerate(s["lines"]):
        f = os.path.join(proj, "audio", "lines", _line_key(ln["speaker"], ln["text"]) + ".wav")
        if not os.path.exists(f):
            rows.append({"line": f"{s['id']}#{i}", "error": "no wav found"}); bad += 1; continue
        segs, _ = asr.transcribe(load16(f), language="en", word_timestamps=True, beam_size=5)
        words = [w for sg in segs for w in sg.words]
        hyp = " ".join(w.word for w in words)
        dur = sf.info(f).duration
        span = (words[-1].end - words[0].start) if words else dur
        wps = len(norm(ln["text"])) / max(0.1, span)
        lo, hi = pace[ln["speaker"]].get(ln["voice"], pace[ln["speaker"]]["normal"])
        # gaps > 0.45 s between words that are NOT after sentence/clause punctuation in the script = mid-sentence pause
        mid = []
        for a, b in zip(words, words[1:]):
            gap = b.start - a.end
            if gap > 0.45 and not re.search(r"[.,;:?!\"”]$", a.word.strip()):
                mid.append(f"{a.word.strip()}|{gap:.2f}s|{b.word.strip()}")
        e = wer(ln["text"], hyp)
        flags = []
        if e > 0.08: flags.append(f"words off ({e:.0%})")
        if wps < lo * 0.9: flags.append(f"slow {wps:.2f} w/s")
        if wps > hi * 1.1: flags.append(f"rushed {wps:.2f} w/s")
        if mid: flags.append("mid-sentence pause " + "; ".join(mid))
        bad += bool(flags)
        rows.append({"line": f"{s['id']}#{i}", "spk": ln["speaker"], "tag": ln["voice"], "dur": round(dur, 1), "wps": round(wps, 2),
                     "range": [lo, hi], "wer": round(e, 3), "flags": flags, "heard": hyp.strip() if flags else ""})
json.dump(rows, open(os.path.join(proj, "VOICE_QC.json"), "w"), indent=1)
for r in rows:
    print(("FLAG " if r.get("flags") or r.get("error") else "ok   ") + json.dumps(r))
print(f"\n{len(rows)} lines, {bad} flagged")
