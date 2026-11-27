# CREATIVE BIBLE: permanent rules for every video
Set by the channel owner on 2026-11-25. Apply this to EVERY new topic without being asked. Change it only when the owner explicitly asks.
The new-video prompt can be as short as "New video: <topic>".

## 1. Identity
- **What we make:** short animated commentary inspired by the *spirit* of Casually Explained. That means intelligent observations, deadpan delivery, simple but effective animation, relatable subjects and unexpected humour.
- **Never copy** another creator's jokes, scripts, characters, voice or signature phrases. We build our own identity.
- **Humour palette:**
  - dry sarcasm; dark humour; brutally honest observations; savage social commentary
  - random, absurd and unhinged situations; intelligent stupidity
  - awkward and uncomfortable humour; relatable everyday observations
  - character comedy; visual punchlines; occasional ridiculous tangents
- **Sarcasm is not automatically comedy.** A joke needs at least one of these:
  - surprise; an unexpected interpretation; a strong observation
  - absurd escalation; a clever reversal; a memorable visual
  - an unusually specific comparison; a character behaving in a hilariously believable way
- **Aim:** laugh-out-loud moments, not "technically clever" ones. The target reaction is "WHAT THE HELL DID I JUST WATCH?" Optimise for genuinely funny moments, not joke count. 25 excellent jokes beat 100 mediocre ones.

## 2. Balance (targets, not maths)
- 60% dry observational humour and intelligent sarcasm
- 20% absurd and unpredictable
- 10% dark and savage
- 10% character and visual comedy

Never force a joke into a serious moment. Not every line needs a punchline. Contrast is essential: a serious fact followed by a ridiculous observation beats ten jokes in a row.

## 3. Recurring cast (keep them consistent and develop them across videos; inside jokes build the channel)
| Character | Voice | Personality and comedy |
|---|---|---|
| **MAYA** (narrator) | Female, late 20s, neutral American, mellow and slightly husky, natural and conversational. | **Calm, intelligent and observant.** She describes ridiculous things as completely normal; quietly judgemental, sometimes unexpectedly sincere, never trying to sound funny. Her delivery ranges from deadpan, to slightly more animated curiosity, to conversational anecdotes. Dark lines are restrained, serious moments sincere and quiet. She can show disbelief or irritation at the absurd, and rarely acknowledges a failed joke. Not artificially slow. |
| **RYAN** (the audience) | Male, late 20s, warm, neutral English accent. | **Relatable, slightly awkward, polite, confused, often exhausted.** His comedy is honest reactions, uncomfortable realisations, awkward questions, unexpectedly specific comparisons and quiet frustration. **NOT sarcastic.** Give him his own ridiculous moments sometimes, not only reactions. |
| **BRAYDEN** (the guru) | Male, late 20s, American, loud, fast, smiling, motivational. | **A walking motivational speech.** Totally unaware he's ridiculous and never acknowledges the joke; he stays confident even when caught. His comedy comes from sincerity, never intentional sarcasm. |
| **GERALD** (the corporate menace) | Middle-aged man, soft British, warm and unhurried. | **Hostage-negotiator calm.** His phrases: "Of course", "That's completely valid", "Nobody is in trouble", "Let's take this one step at a time", "That's a wonderful opportunity". The more disturbing the line, the softer he gets. Never shouts. Not one-note: give him new situations and inventive corporate behaviour, and don't overuse him. |
| **INNER VOICE** | Breathy, impish, close-mic whisper. | Terrible intrusive ideas. Rare, short, unexpected and inappropriate. Never filler. |

**Maya on camera (owner, 2026-11-27):** Maya is now the channel's visible host, not only a voice. She's appealing and polished, and she keeps viewers watching.
- **Look:** design **E**, locked: long wavy dark brown hair, gold hoop earrings, olive-green overshirt over a cream top, light warm-tan skin. The references are `library/show_refs/maya_front.png` and `maya_face.png`.
- **Set:** a recurring cosy presenter's studio (desk lamp, bookshelf, plant, big window). The fox can appear outside the window.
- **Where she appears:**
  - Every video and every Reel **opens on her** (the hook line).
  - She returns on camera at section turns, for her own anecdotes, for key one-line punches, and for the verdict.
  - Plan about 8–10 on-camera lines per video, each ideally 6 s or less.
  - Her longer explanations still play over the visuals.
- **Build:** shots with `onscreen=True`, `eng="h3"`, refs `["maya", "maya_face"]` (see `topics/insurance.py`).
- **Lip-sync budget:** about 16–18 lip-sync shots per video, Maya's included.

The cast can talk to background characters (shop staff, a neighbour, a passer-by, an angry swan), which keeps scenes from being only these five.

## 4. Length and pacing
- **Target:** 9–11 minutes (usually about 10).
- **Runtime is calculated separately:**
  - spoken words at each character's speed:

    | Character | Words per minute |
    |---|---|
    | Maya | 125–145 |
    | Ryan | 120–145 |
    | Brayden | 145–170 |
    | Gerald | 110–130 |
    | Inner Voice | slower |

  - plus pauses, dialogue exchanges, animation-only sequences, reveals, transitions and sound effects
- **Every script reports:** word count, spoken runtime, animation-only runtime, total runtime, and the sections at risk of running over.
- **Timing rules:**
  - Don't rush punchlines.
  - Hold 0.5–1.5 s after big jokes; reveals get 2–4 s.
  - Absurd sequences need room.
  - Don't pause after every sentence, and avoid artificially slow dialogue.
  - Vary the pace and keep explanations short.
  - Never let an animation run longer than it's funny.
  - Use silence deliberately.

## 5. Structure (flexible)
| Time | Section | What it does |
|---|---|---|
| 0:00–0:40 | Cold open | Strong visual or absurd situation, curiosity, the central question. No topic explaining. |
| 0:40–2:00 | Intro | The subject through interesting observations; bring in characters naturally. |
| 2:00–4:00 | Development | Entertaining examples, interactions, visual jokes. |
| 4:00–6:00 | Escalation | At least one big absurd scenario. |
| 6:00–8:00 | Deeper | The most interesting research and observations. Never a lecture. |
| 8:00–9:30 | Payoff | Callbacks, reveals, a final comedic sequence. |
| 9:30–10:30 | Verdict | The conclusion, then a memorable final punchline, reveal or callback. No subscribe request. |

## 6. Absurd sequences (2–3 per video)
Each one should:
1. Start from a recognisable premise.
2. Add the unexpected.
3. Escalate step by step, with characters interacting.
4. Develop the situation instead of explaining it.
5. End on a memorable payoff.

It needs internal comic logic. Random images are not absurdism. (Model example: Weekend Lite / Plus / Pro, with cancellations done in person, on a Saturday.)

## 7. Visual comedy, running gags and callbacks
- **Visual comedy:**
  - Animation is half the comedy: background gags, reactions, visual metaphors, exaggerated expressions, sudden cuts, silent developing absurdity, deliberately crude drawings, reveals, callbacks.
  - Some jokes live only in the animation. Never explain a visual joke.
  - Keep it achievable in simple 2D.
  - Vary the devices; for example, don't turn every concept into a tortured cute cartoon object.
- **Running gags:**
  - Plant a small gag early and pay it off later, evolving each time (the fox gets more ridiculous each appearance, unexplained).
  - Reward attentive viewers. Never overuse a gag and never explain it.

## 8. Facts
- Research independently. Prefer primary and reputable sources.
- Verify every number, date and quote; explain what a statistic measures.
- Keep correlation distinct from causation; never exaggerate findings.
- Never invent statistics or quotes. Flag anything uncertain.
- A joke must never depend on a false fact, and fiction is never presented as fact.
- Add a sources section without cluttering the narration.

## 9. Dark humour
- Edgy, dark and savage is allowed, but always intelligent, never shock for its own sake.
- **Targets:** hypocrisy, corporate exploitation, fake gurus, social absurdity, vanity, scams, pretentiousness, powerful institutions.
- Never cruelty instead of a joke, and never punching at vulnerable people.

## 10. Audio
- Every line gets acting notes: intention, speed, energy, pitch, pauses, emphasis.
- **Markers:**

  | Marker | Meaning |
  |---|---|
  | `[ ]` | Animation |
  | 🔊 | Sound effect |
  | ♪ | Music or sting |
  | (beat) | Short pause, between lines only, never mid-sentence |
  | (silence Xs) | Deliberate silence |

- **Music:** by default, no continuous music under dialogue. Use music only with a clear purpose. Sound effects serve the joke and never drown it.

## 11. Quality control (be strict, never self-praise)
Before presenting any script, check:
- the opening
- whether the jokes are genuinely funny and not predictable
- variety and character distinctness
- natural dialogue and no joke pile-ups
- absurd sequences that are actually developed
- visuals that add something
- no explanations or repeated explanations
- educational parts that entertain
- serious moments handled with respect
- a strong payoff
- a realistic runtime

Remove: generic AI jokes, obvious punchlines, forced puns, repetitive sarcasm, unneeded dialogue, explained visuals, lines a character wouldn't say.

## 12. Standard output for every script
1. **Video concept:** topic, argument, comedic angle, why it's interesting.
2. **Full script:** sections, timestamps, dialogue, characters, animation, sound effects, music, pauses and holds.
3. **Voice acting directions:** for every speaking character, including any new voice needs.
4. **Animation and editing notes:** running gags, visual punchlines, transitions, rhythm, sound design, complexity.
5. **Runtime breakdown:** words, dialogue time, animation time, total, sections at risk.
6. **Fact-check and sources:** verified claims, references, anything still to verify.
7. **Final quality review:** remaining weaknesses and production concerns. No invented perfect scores.

## 13. Permanent "never" list
Never:
- write like a generic explainer
- make every line a joke
- make every character sarcastic
- repeat a joke structure
- trade natural dialogue for clever wording
- over-explain a punchline
- rush the best moments
- confuse randomness with originality, or offensiveness with humour
- stuff in statistics
- sacrifice accuracy
- force a character into a scene
- change a character's personality without asking
- forget that animation is part of the comedy

## The look: stylised 3D (locked 2026-11-27)
From "How Do ATMs Actually Work?" onward, every new video and Reel uses the stylised 3D feature-film look (Pixar-like). The owner chose it from 13 style options. The four finished 2D videos stay as they are.

**Maya:** 3D option 1.
- Big hazel-brown eyes, bright friendly smile, rosy cheeks.
- Fair light skin with a soft warm peach glow.
- Long wavy dark brown hair, gold hoops, olive overshirt over a cream top.

**One lock for everything:**
- New topics import their style, cast, sets and helpers from `tools/shorts/topics/show3d.py`.
- The references live in `library/show_refs3d/`, made by `tools/cast3d.py`. This includes the set plates for the studio, office, kitchen, flat and night street.
- The builder attaches the matching set plate whenever a shot uses that set.

**Consistency rules:**
- Lighting, palette and render quality come only from `show3d.STYLE`.
- Never mix in 2D-era references.
- Maya's on-camera shots are close-ups from the chest up in the daylight studio. `maya()` sets `close=True`, so no set plate is attached, because a plate forces a wide shot. A wide shot makes the H3 lip-sync jump to a close-up mid-clip.
- Night lighting belongs only to the street set's own wording; the shared lighting line has no night clause.

**Green specks:** `tools/shorts/autoclean.py` runs on every keyframe and thumbnail. Still check the blobscan crops by eye during QC.

**Production time** is unchanged: the same Qwen-Image, H3 and LTX engines, with only the prompts and references changed. Measured on the test: 222 s for a 9-second Maya line and about 112 s for a short line, the same as 2D.
