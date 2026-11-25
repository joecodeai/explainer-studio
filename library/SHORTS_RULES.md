# REEL RULES: permanent, set by the owner on 2026-11-25 (second revision)
These work alongside `CREATIVE_BIBLE.md`. They apply to every long-form video.

## ONE promotional Reel per episode, not three Shorts
- **What to make:** one carefully built promotional Reel, about 45–60 seconds, published **before** the full YouTube video.
- **What it is:** a 60-second trailer that is also a complete comedy sketch: one topic, one narrative, one payoff.
- **What it is not:** a highlights montage, three Shorts joined together, or a random collection of jokes.
- **Its job:**
  - introduce the episode's subject
  - entertain a completely new viewer
  - show the characters' personality
  - leave the viewer wanting the full video
- **Pre-release, not a recap:** give enough to understand the premise. Don't explain every argument or spend every major punchline; keep value for the episode.

## Build one story from the whole episode
Read the whole script: its central argument, characters, visual gags, best dialogue, reveals and running jokes. Then build one narrative:

| Beat | What it does |
|---|---|
| Hook | An immediately interesting situation, line or visual. The subject is clear within seconds. |
| Setup | One central problem or question. |
| Development | Moments from different parts of the episode, made to feel like connected events in one story. |
| Escalation | Progressively more ridiculous, surprising or interesting. |
| Payoff | A strong joke, reveal or visual callback that makes the whole thing satisfying. |
| Teaser | Curiosity about the bigger subject. Never just "watch the full video". |

- **Order:** moments may be reordered, but the result must make logical sense.
- **Connections:** use a short existing narration line or reaction shot to connect moments.
- **Relevance:** don't force unrelated characters or jokes in. Every scene must serve the one story.
- **New material:** use existing footage, voices, animation and sound. Aim for zero new work. If a tiny connecting line or animation is truly needed, say so rather than making a confusing edit.

## Vertical framing must not destroy the animation
Our animation is designed in 16:9. Never put a blind 9:16 crop over the middle. Preserve all the visual information the joke needs. Inspect every source shot, then choose, in order of preference:
- **A. Full width plus blurred background.** The whole 16:9 frame at canvas width, with a softly blurred, enlarged copy filling above and below. This is the default for wide scenes, group shots, props and visual gags.
- **B. Smart reframing.** A deliberate window on the clear focus, with enough context kept. It tracks or pans with the action and is never automatically centred.
- **C. Custom vertical composition.** Several important elements arranged together, preserving their spatial relationship when the joke depends on it.
- **D. Split or sequential framing.** For very wide scenes: establish the whole scene, then the close-up, then the reaction.

Use intentional moves, for example opening close on the speaker and pulling back to full frame as the punchline's object comes into play.

**Shot-by-shot check, before approving any shot:**
- Are all important characters visible, with faces and expressions readable?
- Are the hands and props visible?
- Is the action clear?
- Are background gags visible?
- Is the setup and payoff preserved?
- Is anything accidentally cut off?
- Is a caption covering a face or object?

A complete horizontal image over blur is always better than a badly cropped vertical one.

## Technical
- **Format:** 1080×1920, source aspect ratio preserved, never stretched.
- **Captions:**
  - one consistent style and height
  - placed in the band under the picture
  - clear of the bottom interface (y > 1540) and the right-side buttons
- **Sound:** original dialogue, effects and comic pauses. No music bed.
- **No:** intro, logo, or forced subscribe request.
- **Length:** about 45–60 s, but story beats exact duration.

## Deliverable (`VIDEOS/<Title>/REEL PLAN.md` + `Reel/`)
**Plan first:**
- **A.** the story in one sentence
- **B.** why it's the strongest introduction
- **C.** beginning, middle and end
- **D.** the exact dialogue and source shots
- **E.** how each connects to the next
- **F.** the framing method per shot
- **G.** runtime
- **H.** any extra work

**Then the files in `Reel/`:** the Reel, a cover (`Thumbnail.jpg`, text inside the 4:5 grid crop) and `Upload text.txt` (title, caption, tags of about 495 characters).

**Final QC:** watch it as a stranger.
- Is it one story?
- Does every cut make sense?
- Does it build naturally to a satisfying ending?
- Would a stranger want the episode?
- Is nothing cut off, and does every shot look composed?

Fix anything that fails before delivery.

## Tool
`tools/shorts/promo.py <topic> <spec>`, with the spec at `tools/shorts/topics/<topic>promo.py` containing `REEL = dict(title, pieces=[...])`.
- Composes every frame in Python. Pieces can be FULL, BOX `f`/`x`/`y`/`h`, eased pans and push-ins, keyframes, or sequential `sub` spans.
- Reads each shot from its own segment file.
- Writes a QC sheet of first, middle and last frames per shot to `projects/short-<topic>/promo/qc_frames.jpg`.

Example: `topics/hustlepromo.py`. `tools/shorts/cutdown.py` (centre crops) is retired for Reels.
