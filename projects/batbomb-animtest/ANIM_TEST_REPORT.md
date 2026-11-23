# Bat-bomb film: 5-shot animation capability test (21 Nov 2026)

**Watch:** `BATBOMB_ANIM_TEST.mp4` (28 s, 1920×1080, 24 fps, picture only; sound design is Stage 6).
**All takes:** `clips/`. **Per-clip frame sheets and motion plots:** `qc/`. **References:** `refs/`. **Keyframes:** `keyframes/`.

## How it was made
1. **Style lock and reference sheets.** Qwen-Image-2.1 made the style lock (2D hand-drawn feature-film look) and reference sheets for the hero bat, Adams, Fieser and the rancher. I picked one design per character out of 2 options.
2. **Keyframes.** Qwen-Image multi-reference edit placed the reference characters into each scene: 2 options per shot, 1 picked.
3. **Animation.** Every shot was animated as a real moving clip.
   - **LTX-2.5** (image-to-video): environment, FX and vehicle shots.
   - **MiniMax H3** (keyframe plus identity references): character shots.
   - Both engines were run on the two character shots so they could be compared.
4. **QC on every clip:**
   - 12-frame contact sheet.
   - 6 consecutive frames from the middle, to prove it's real motion and not a sliding still.
   - Frame-to-frame motion plot, plus checks for frozen frames, jumps and brightness flicker.
   - Manual review against the narration beat.

## Results
| # | Shot | Best take | Motion QC | Verdict | Notes |
|---|---|---|---|---|---|
| 1 | Carlsbad dusk bat flight | LTX s11 | smooth, 0 jumps, 0 frozen, 77% of the frame moving | ✅ PASS | The crane-up follows the column and loose bats really flap frame to frame. **Trim to ~3.5 s** (it drifts into empty sky). Some loose bats are pale smears that read as moths. At distance the column reads more as texture than individual bats. |
| 2 | Fieser arms the bat | **H3 s12** | smooth; the only spikes are real wing-beats (checked frame by frame) | ✅ PASS | Pushes in to the injection, the bat wakes, spreads its wings and takes off, and Fieser reacts. **His face, coat and syringe stay identical; the bat matches its reference sheet.** ❌ *Continuity error: the capsule stays in his hand when the bat takes off.* |
| 2 | (same) | LTX s11 | | ❌ FAIL | The bat balloons to giant size over his face and its snout morphs. **LTX must not animate character shots.** |
| 3 | Control tower catches fire | LTX s11 | smooth, 67% moving | ✅ PASS | Strongest clip: fire grows, black smoke, embers and a dramatic push-in. The two bats in the sky disappear after the first second. |
| 4 | Jeep chase on the lakebed | LTX s11 | smooth | ✅ PASS | The jeep drives toward and past camera with a real dust plume and a following pan. The bats vanish from the sky mid-shot, and the soldiers stop pointing. |
| 5 | Rancher and the hero bat | **H3 s12** | smooth | ✅ PASS | The rancher looks up, strokes his moustache, and the camera moves up to the worried bat. Identity is stable. *(LTX s12 is also usable: a great bat close-up with expressive blinks, but the rancher's face shifts slightly.)* |

**Revisions done:** shots 2 and 5 were re-rendered once (new seed, plus tighter direction for shot 5). That fixed the bat not taking off (shot 2) and the rancher looking the wrong way (shot 5).

## What this proves, and what it doesn't
**Proven:**
- Characters stay on-model while acting (H3).
- Fire, smoke and dust animate convincingly.
- The camera can track a moving vehicle.
- A massive swarm can move.
- Creature close-ups are expressive.
- There's no slideshow effect: every clip is continuous motion, with 0 frozen frames outside H3's normal animating "on twos".

**Not yet proven (needs a second mini-test before full production):**
- **Walking without sliding feet.** None of the 5 shots had a character walking. Doc Adams (the main character) hasn't been animated yet.
- **Several named characters in one shot** (e.g., Adams + Fieser + Epler at the dinner party).
- **Fire spreading building to building in sequence** (the hook).
- **The same character across 20 scenes.** Shown so far for 1–2 shots per character.

## Production rules learned (carry into the storyboard)
1. **Engine routing.**
   - **H3** is used for any shot where a character must stay on-model or handles a prop.
   - **LTX** is used for environment, FX, vehicles and big camera moves with no recognisable person, and for hero-bat close-ups.
2. **Props stay attached.** Every bat shot after arming must say "the capsule stays clipped to the bat's chest", and QC checks it.
3. **Background bats use the hero-bat sheet.** In the shot 2 tray, unreferenced bats came out looking like hamsters.
4. **Sky elements disappear in LTX.** Bats in the sky vanish, so if the narration needs them to stay, add them as a separate overlay layer (Remotion) or re-prompt.
5. **Trim to the strong part.** Plan 6 s renders for 3–5 s on screen.
6. **Unify the character style in Stage 3.** The rancher came out more realistic than the rounder Adams. Final sheets should share one proportion system.
7. **Resolution.** Renders are 1280×704 (LTX) or 1344×768 (H3), upscaled to 1080p. Hero shots can use LTX's ×2 latent upscaler for sharper detail.

## Cost and time estimate for the full film
- **Per 6 s shot:** LTX about 1.5 min; H3 about 3 min.
- **Film size:** about 120 shots. Using about 1.5 takes each on average (first-of-its-kind run), that's **about 7–9 h of GPU time**, plus keyframes (~1 h) and QC.
- **Plan:** render in scene groups of 10–15 shots, reviewing each group before the next.
