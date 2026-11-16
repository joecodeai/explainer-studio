# Audit: `benny-japan-yen-reel.mp4` (75 s), 2026-11-16

## Stage 1: scene by scene

| Time | What's on screen | Problem | Fix |
|---|---|---|---|
| 0:00–0:07 | Wide static shot: Benny and Maya stand far apart, frozen. Off-screen narration. "TRIP CANCELLED" sticker clipped at the top edge. | Hook is told, not shown. Nothing happens in the first 2 s, the characters are tiny and don't interact, and the narrator explains the joke. | Open on the situation itself: Benny at the airport exchange counter, the clerk counts out ¥159,000, Benny freezes. First line within 1 s. Fix the sticker position. |
| 0:07–0:15 | Benny alone, waist-up, talking to the camera. | Talks to the viewer, not to Maya, so it reads as a monologue. Long line with stray pauses ("I read it. Well…"). | Two-shot: he tells Maya and she reacts. Pacing fixed. |
| 0:15–0:18 | Maya alone, to camera. "Put the suitcase down." | The joke needs Benny holding a suitcase. He isn't, so the line doesn't land. | Jokes must refer to things the viewer can see (objects in hand/scene), or be cut. |
| 0:18–0:30 | Café: alternating solo shots, each a new pose. | The core "taking turns" problem: one person per shot, both facing the camera, the face resets to the pose drawing at every cut, and no reactions. | Continuous two-shot of the whole scene, with closeups and reaction cuts taken from the same take (same acting). |
| 0:30–0:43 | 12 s white "stats" card ($1,000 / ¥1,000 ramen). | Longest dead spot. The newsroom white-card style clashes with the warm show style. No character on screen. | Show it in the world: a ramen-shop ticket machine (¥1,000 button) with Benny's reaction; numbers as an overlay in the show style, max 4 s. |
| 0:43–0:48 | "Six dollars! … there, it's culture." | Good joke, but delivered to the camera with no listener. | Two-shot, with Maya's deadpan reaction cut-in. |
| 0:49–1:01 | Payoff scene, solo shots. | "It cost more than the old one" lands without a beat, and the next line starts too soon. | Written beats (`pause_after`) after punchlines; reaction shot during the beat. |
| 1:01–1:06 | Rooftop, Benny alone asks the comments question. | Fine idea, weak staging. | Keep, but in a two-shot with Maya's reply in the same frame. |
| 1:07–1:15 | 8 s dark "Full Episode on YouTube" card labelled "PART 1". | Dead air at the end (viewers swipe away, hurting completion rate). Wrong "PART 1" label. | Fixed: no part numbers on closing cards or in show episodes. The reel ends on the last joke + a 1.5 s overlay CTA. |

**Throughout:**
- **Voices:**
  - The excited/sarcastic lines used separately designed recordings, so the identity drifted.
  - Benny's delivery was flat and "read".
- **Pauses:** random pauses inside phrases, sentences run together, and the same fixed gap between every line.
- **Lip-sync:**
  - 6 of 19 shots failed the automatic lip-sync check ("mouth moves in the pauses"); one was used anyway (Benny's "It cost more than the old one").
  - The cause: the model animates the mouth during the padded silence at the end of each clip.
- **Expressions:** each shot starts from a fresh pose drawing, so the face snaps back to "default" at every cut.

## Stage 3: root causes in the pipeline

1. **`pipeline.stage_talk`:** one LTX shot per line, made from a single-character pose image, with the prompt "speaks … to the viewer". This causes the monologue feel, the face resets and the missing reactions.
2. **`voice.narrate`:** per-emotion reference clips (`ref_excited` / `ref_sarcastic`) each carry a slightly different voice, so the identity drifts. Qwen3-TTS Base copies the reference's flat prosody, so the delivery sounds "read".
3. **Pausing:** fixed `GAP`/`GAP_SAME` constants between lines. The model's random pauses inside lines are never corrected.
4. **`pipeline.build_props`:** every title card counted as a "PART", including the closing card.
5. **Reel-cut and stats cards:** the newsroom-style white cards were never restyled for the show.
6. **Speed:** about 40% of the hour went to the animation-QC loop re-generating shots for lip-sync false alarms.

## Stage 4: what's been changed (so far)

- **Voice:**
  - New engine: Chatterbox (MIT licence, OK for monetisation), `studio/tts_cb.py`.
  - ONE reference per character for every line, so the identity is fixed. Emotion now changes only the intensity and pacing of the delivery.
- **Pacing (`studio/pace.py`):**
  - Within a line:
    - only real silences are resized: about 0.3 s between sentences, about 0.15 s at commas, about 0.55 s for "…";
    - a breath is inserted where the model ran sentences together;
    - stray mid-phrase pauses shrink to about 0.1 s.
  - Between lines, the gap depends on the context: interruption 0.12 s, question 0.32 s, normal turn 0.4 s, or a written beat after a joke (`pause_after`).
- **Part numbers:** removed from closing cards and from show episodes.
- **Staging:**
  - A continuous two-shot conversation, where each shot starts from the previous shot's last frame (acting carries over).
  - The listener reacts with their mouth closed.
  - Prototype 1 confirmed this works; prototype 2 is fixing the camera creep and the busy hands.

## Still to do

- Production version of the staging: two-shot takes plus closeup/reaction crops from the same take, written beats, and object interaction.
- A new 10+ minute episode built as a story (Benny at the exchange counter, then the ramen ticket machine, then the summer intervention panic, then the shopkeeper's side, then Benny finally right, then a callback ending), plus a reel cut from its best moments.
- Production speed-ups.
