# SHORTS / REELS RULES: permanent, set by the owner on 2026-11-25
These work alongside `CREATIVE_BIBLE.md`. They apply to every long-form video.

## What a Short is
- A Short is **cut from the finished long-form video**: its real voices, animation, sound effects and picture.
- It is **not a separate production**. Aim for zero new dialogue, voice or animation.
- If footage genuinely can't tell a complete story, say so honestly and name the smallest addition needed.
- **EVERY REEL MUST TELL A COMPLETE STORY.** It's a miniature episode, never a highlights compilation or random funny clips.
  - Two moments with no natural relationship never go in the same Reel.
  - Judge a Reel by whether the viewer wants to know what happens next, not by how many jokes it has.

## Structure
| Time | Beat | What it does |
|---|---|---|
| 0–2 s | Hook | Visual or verbal, inside the action. No logo or slow setup. |
| 2–10 s | Premise | Who is involved, what is happening, why. |
| 10–40 s | Development | Escalation; each shot leads logically to the next. |
| Last 5–15 s | Payoff | Connects directly to the setup, ideally making the opening funnier in hindsight. |

- **Length:** 30–60 s, aiming for 35–50 s. Never stretch.
- **Story types:**
  - mini-story (one character's problem escalates to a payoff)
  - comedic explanation (one question or fact, explained, then a joke)
  - visual story (the animation carries it)
- **The continuity test:** without the long video, does a stranger understand who, what, why, what changes, and why the ending is funny? If not, restructure.

## Editing
- **Reuse and rearrange:**
  - Rearrange existing shots and lines, and use reaction and establishing shots or a short existing context line.
  - Cut only at sentence boundaries.
  - Never splice in a way that changes meaning or distorts a statistic.
- **Pacing:**
  - Keep the deadpan pacing and the pauses that make jokes work; remove only dead time.
  - Never speed up Maya to fit more words.
- **Framing (9:16, 1080×1920):**
  - Reframe 16:9 intelligently: keep faces and the joke's object in the safe area.
  - Use per-shot crop position; use background extension or blur when a full-width image is needed.
- **Subtitles:**
  - Readable, high contrast, sensible line breaks.
  - Kept above the bottom interface area and away from the right-side buttons.
- **Sound:**
  - Original voices and effects. No music bed and no trendy or added music.
  - Keep any silence that is part of a punchline.
- **Ending:** end on the strongest punchline or visual reveal. No automatic subscribe request.

## Deliverable for every long-form video
Propose 3–5 Shorts. For each:
- title
- one-sentence story
- concept, and why it works standalone
- the opening situation and hook (first line and first visual)
- the character's objective or problem, the escalation and the payoff
- exact existing dialogue and shots, in order, with source sections
- editing notes (cuts, reactions, pauses, subtitles, sound, reframing)
- the ending, and why it works
- any new work needed (aim for none)
- runtime

Rank them by:
- hook
- how fast the premise becomes clear
- comedy and visual payoff
- standalone sense
- shareability and replay value
- how little extra work they need

Recommend the strongest 3, not the easiest 3. Then produce the editing document with in/out points. Ours come from the real `timeline.json`, so they are exact, not guessed.

**Tool:** `tools/shorts/cutdown.py` cuts Shorts from a long-form project (`picture.mp4` + `mix.wav` + `timeline.json`).
