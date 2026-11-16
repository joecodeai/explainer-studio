"""Natural pacing for generated speech.

TTS models drop random pauses inside phrases and run separate sentences together. Using word timestamps, rebuild each line
so every pause has a reason: a short breath between sentences, a longer beat on "...", a tiny catch at commas, and no stray
pauses inside a phrase. Between lines, the gap depends on the conversation (question, interruption, joke beat, same speaker).
"""
import re
import numpy as np

# pause after a word, by how the word ends (seconds)
END_PAUSE = [(re.compile(r"(\.\.\.|…)[\"')\]]*$"), 0.55),     # "..." = deliberate beat
             (re.compile(r"\?[\"')\]]*$"), 0.34),
             (re.compile(r"[.!][\"')\]]*$"), 0.30),
             (re.compile(r"[—–-]$"), 0.12),                      # cut-off / dash
             (re.compile(r"[,;:][\"')\]]*$"), 0.16)]
INSIDE = 0.08            # pause inside a phrase (the model's random hesitations shrink to this)
MARGIN = 0.035           # never cut closer than this to a word edge (ASR timestamps are approximate)
XF = 0.008               # crossfade at each join


def _target(word):
    for rx, t in END_PAUSE:
        if rx.search(word): return t
    return INSIDE


def _silences(audio, sr, min_len=0.06):
    """[(start_s, end_s)] of internal silences from the energy envelope (10 ms frames)."""
    hop = int(sr * 0.01); n = len(audio) // hop
    if n < 3: return [], np.zeros(0)
    e = np.sqrt(np.mean(audio[:n * hop].reshape(n, hop) ** 2, axis=1))
    th = max(np.percentile(e, 95) * 0.06, 1e-4)
    quiet = e < th; out = []; i = 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if j - i >= int(min_len / 0.01) and i > 0 and j < n: out.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    return out, e


def pace(audio, sr, words):
    """audio: mono float32; words: [[text, start, end], ...] (script words with approximate ASR times).
    Only silence is ever removed or added, so words can't be clipped: each real pause is resized to what its punctuation
    calls for, and a sentence break with no pause gets one at the quietest point near the boundary."""
    if len(words) < 2: return audio
    sil, env = _silences(audio, sr)
    bounds = [((a1 + b0) / 2, _target(w)) for (w, a0, a1), (_, b0, b1) in zip(words, words[1:])]
    edits = []                                   # (start_s, end_s, new_len_s): replace [start, end) with new_len of quiet
    th = max(np.percentile(env, 95) * 0.06, 1e-4) if len(env) else 0
    owner = {}                                   # silence index -> boundary index (each punctuation mark claims its nearest pause)
    for k, (t, want) in sorted(enumerate(bounds), key=lambda kv: -kv[1][1]):      # strongest pauses pick first
        if want <= INSIDE: continue
        cand = [(abs((s0 + s1) / 2 - t), i) for i, (s0, s1) in enumerate(sil) if i not in owner and min(abs(s0 - t), abs(s1 - t), abs((s0 + s1) / 2 - t)) < 0.45]
        if cand: owner[min(cand)[1]] = k
        elif want >= 0.25 and len(env):          # sentence break the model ran together: add a pause at a truly quiet point
            lo, hi = max(0, int((t - 0.08) / 0.01)), min(len(env), int((t + 0.08) / 0.01) + 1)
            if hi > lo:
                j = lo + int(np.argmin(env[lo:hi]))
                if env[j] < 3 * th: edits.append((j * 0.01, j * 0.01, want))
    for i, (s0, s1) in enumerate(sil):
        want = bounds[owner[i]][1] if i in owner else 0.1        # a pause the text doesn't ask for: keep it tiny
        if abs((s1 - s0) - want) > 0.03: edits.append((s0, s1, max(want, 0.06)))
    edits.sort()
    xf = int(sr * XF); out = []; pos = 0; rng = np.random.default_rng(0)
    for s0, s1, want in edits:
        i0, i1 = int(s0 * sr), int(s1 * sr)
        if i0 < pos: continue
        out.append(audio[pos:i0])
        keep = audio[i0:i1][:int(want * sr)]
        pad = int(want * sr) - len(keep)
        out.append(np.concatenate([keep, rng.normal(0, 2e-4, max(0, pad)).astype(np.float32)]))
        pos = i1
    out.append(audio[pos:])
    res = out[0]
    for p in out[1:]:
        if len(res) > xf and len(p) > xf:
            ramp = np.linspace(0, 1, xf, dtype=np.float32)
            res = np.concatenate([res[:-xf], res[-xf:] * (1 - ramp) + p[:xf] * ramp, p[xf:]])
        else:
            res = np.concatenate([res, p])
    return res.astype(np.float32)


INTERRUPT = re.compile(r"^\W*(wait|no|hold on|hang on|but|okay okay|sorry)\b", re.I)


def gap_between(prev, nxt):
    """Seconds of silence between two consecutive lines of dialogue (dicts with speaker, text, optional pause_after)."""
    if prev.get("pause_after") is not None: return float(prev["pause_after"])   # written-in beat (after a joke, awkward silence)
    pt, nt = prev["text"].strip(), nxt["text"].strip()
    if pt.endswith(("—", "–", "-")): return 0.03                                 # cut off mid-sentence
    if INTERRUPT.search(nt) and prev["speaker"] != nxt["speaker"]: return 0.12   # quick comeback / interruption
    if prev["speaker"] == nxt["speaker"]: return 0.25
    if pt.endswith("?"): return 0.32
    if pt.endswith(("...", "…")): return 0.6
    return 0.4                                                                    # normal turn-taking
