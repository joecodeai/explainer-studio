# Ryan Figures It Out: production architecture v2 (design, 2026-11-17)

Status: **DESIGN, validated by the bake-off on 2026-11-17 (§9).** You approved H3's quality and speed. The production build is next.
Numbers marked **[validate]** are published figures we have not yet measured ourselves. Everything in §9 was measured on this machine.

---

## 0. Targets

| | Target |
|---|---|
| 10-min YouTube episode, script → final MP4 | **≤ 3 h** on the RTX 5090, unattended and resumable |
| 60-s reel | **≤ 30 min** |
| Delivered resolution | 1920×1080, 24 fps, H.264 high quality |
| Character identity | Every shot passes an identity check against the character sheet. No visible face or outfit drift |
| Lip-sync | Mouth matches **our** TTS track within ±2 frames. The listener's mouth stays closed while the other person talks |
| Expressions | Subtle to clear, never over the top (intensity ≤ 2 on a 0–3 scale) |
| Motion | No lag, no frozen frames, no zoom creep, no blur |
| Cost | €0 per episode locally. Paid cloud is optional, only for hero shots |

## 1. Design principles

1. **Consistency is decided before animation.**
   - Every shot starts from a keyframe drawn from fixed character and location assets.
   - The video model only adds motion. It never invents a face, outfit or room.
2. **Our audio is the master clock.**
   - The voices are made first.
   - Each video shot is generated to fit the audio.
   - The final mix always uses our TTS track. A voice the video model generates is thrown away.
3. **Expensive models only where they show.**
   - A shot router sends acting and dialogue to the best model.
   - Reactions, establishing shots and B-roll go to the fastest model.
4. **Every shot is checked by machines, not hope.**
   - Automatic QC gates catch problems.
   - Failures are re-rolled with a new seed, then escalated to a stronger tier.
5. **Batch by model, cache everything, survive reboots.**
   - Model swaps cost minutes, so all shots for one model run together.
   - Every artefact is cached by a content hash. A crash or reboot resumes where it stopped (today's 11:05 reboot cost a full hour).

## 2. Model landscape (research summary)

| Model | Local? | Keeps OUR voice + lip-syncs? | Use in this design |
|---|---|---|---|
| **MiniMax H3** (Aug 2026, 33B) | **Yes** (open weights, 768p stage) | **Yes.** Ref2VA uses the uploaded recording as the dialogue track | **Tier A**: all dialogue and acting |
| Pika-H3-Flex / Turbo LoRA | Yes | (H3) | H3 in 6 steps (Flex) or 4 steps (Turbo): about 2× faster |
| LTX-2.5 | Yes | Partial | **Tier B**: silent motion, B-roll, establishing shots |
| LongCat-Video-Avatar 1.6 | Yes (installed) | Yes | **Fallback** for lip-sync failures |
| Qwen-Image 2.1 edit | Yes (installed) | n/a | **Keyframes** and character and location assets |
| Wan 2.2 | Yes | S2V only | Not used. Slightly nicer stills than LTX but slower; Wan 2.5–3.0 are closed |
| Kling 3.0, Veo 3.1, Seedance 2.x, Grok | Cloud, paid | **No**: they generate their own voice (Seedance re-voices the line) | Optional **Tier C** for silent hero shots only |
| MiniMax H3 API (2K) | Cloud, paid | Yes | Optional **Tier C** for 2K hero shots ($0.13/s) |

Key H3 facts used in this design:
- On a 5090 it uses ~27 GB of VRAM (int8/NVFP4).
- 864×480 is its sweet spot: a 5-s clip takes ~21 s with Flex. 1344×768 takes ~100 s for 5 s.
- It needs torch cu130; on cu128 it runs 1.5× slower.
- Up to 9 reference images and up to 3 audio clips (2–15 s each).
- Its prompts have three fields (`integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music`), with speaker IDs `(S1)` and dialogue inside `<d>…</d>`.
- **Faces need pixels:** at 480p, a face in a wide shot comes out as mush and upscaling cannot fix it. Framing has to be medium-close or closer.

## 3. System overview

```
 ┌─────────────── PRE-PRODUCTION (once per show / location) ───────────────┐
 │ Character identity packs   Location packs        Camera setups           │
 │ (sheet, 6 portrait refs,   (clean plate per      (2-shot medium-close,   │
 │  outfit refs, voice,       location × setup,     single L, single R,     │
 │  face-embedding centroid)  lighting note)        over-shoulder, insert)  │
 └──────────────────────────────────────────────────────────────────────────┘
                 │
 EPISODE ────────▼───────────────────────────────────────────────────────────
 1 Script (LLM + research)            → script.json                [exists]
 2 Shot compiler                      → shots.json (shot specs, §4.2)  [NEW]
 3 Voices (Qwen Ryan / Chatterbox Maya, shared tempo, pacing) → per-line wav + master track [exists]
 4 Keyframes (Qwen-Image edit: setup plate + identity refs + pose/expression) [rework]
      └ gate: identity, outfit, composition, no text/artefacts
 5 Motion, batched by engine:
      A  H3 Ref2VA + Flex   (dialogue/acting)          [NEW]
      B  LTX-2.5 I2V        (silent B-roll, inserts)   [exists]
      C  H3 1344×768 14-step / optional cloud hero     [NEW]
 6 QC all shots → re-render failures (max 2 rounds, then escalate/fallback) [extend]
 7 Finishing: upscale to 1080p, colour-match per scene, mix, captions, end card [extend]
 8 Deliverables: episode MP4, reel MP4, thumbnails, upload text files [exists]
```

## 4. Components

### 4.1 Identity and location packs (built once, reused every episode)
- **Character identity pack** (`library/identity/<char>/`):
  - Canonical sheet.
  - 6 reference portraits: front, ¾ left, ¾ right, profile, smiling, neutral. Each at 1024 px with the face filling the frame.
  - One full-body reference per outfit in `wardrobe.json`.
  - Voice settings.
  - A **face-embedding centroid** for QC (anime-face detector + DINOv2 embedding, averaged over the refs).
  - H3 gets ≤ 4 of these per shot: 2 portraits + the outfit + the location plate.
- **Location pack:**
  - One clean background plate per (location × camera setup), painted once.
  - Lighting note (time of day, key light side).
  - Every keyframe in that location reuses the same plate, so the background can't drift.
- **Camera setups** (fixed set, which also gives the show a recognisable visual grammar):

| Setup | Framing | Native size | Use |
|---|---|---|---|
| `two_mc` | 2-shot **medium-close** (faces ≥ 18% of frame height) | 864×480 [validate] | Banter, most dialogue |
| `single_L` / `single_R` | Medium close-up on one character | 864×480 | Punchlines, reactions, explanations |
| `ots` | Over-the-shoulder | 864×480 | Variety in long exchanges |
| `wide` | Establishing, both small | LTX, no lip-sync | Scene openers only, no dialogue |
| `insert` | Object or graphic (phone, chart, map) | LTX or still + motion | Facts and numbers |

No wide shots with dialogue: faces would be too small for 480p generation.

### 4.2 Shot compiler (new; the data contract)
This replaces "one LTX clip per line". A **beat shot** groups 1–3 consecutive lines in the same setup into one 4–12 s clip with a single audio track. That's fewer, longer shots, which gives more natural back-and-forth and fewer cuts.

```json
{ "id": "s03_b02", "scene": "s03", "setup": "two_mc", "location": "coffee_shop",
  "start": 41.20, "end": 49.85,
  "audio": "voice/s03_b02.wav",
  "lines": [ {"spk": "ryan", "t0": 0.00, "t1": 3.10, "text": "...", "intensity": 1},
             {"spk": "maya", "t0": 3.40, "t1": 8.65, "text": "...", "intensity": 1} ],
  "listener_rules": "mouth closed while the other speaks",
  "acting": {"ryan": "leans in, counts on fingers", "maya": "small amused smile → raised eyebrow"},
  "camera": "Static Shot", "tier": "A", "outfits": {"ryan": "home", "maya": "evening"},
  "keyframe": "kf/s03_b02.png", "seed": 1234, "attempt": 0 }
```

Compiler rules:
- **Shot length:**
  - Lines over 12 s are split at a sentence boundary.
  - Audio under 2 s is merged with a neighbour or padded with silence (H3 needs at least 2 s).
- **Setup choice:**
  - A punchline or reveal gets a `single` on the speaker.
  - A reaction beat gets a `single` on the listener.
  - Consecutive same-setup shots are limited to 3, for visual variety.
- **Intensity:** 0 = neutral, 1 = subtle, 2 = clear, 3 = forbidden. It maps to fixed prompt phrases ("a small smile", "eyebrows lift slightly"), never "shocked/screams".
- **The H3 prompt is generated from the spec** in the official three-field format:
  - speakers as `(S1)` / `(S2)` with their dialogue and timestamps;
  - `Static Shot` camera;
  - `overall_soundscape` = room tone only;
  - `non_diegetic_music: N/A` (music is added in the mix).
- **Fallback if two-speaker beat shots misattribute mouths** (bake-off test T4): one line per shot. The design works either way; beat shots are just ~40% faster.

### 4.3 Audio (existing, small changes)
- Voices, shared tempo and pacing stay as they are.
- New: a per-shot audio slice of the master track, so the audio fed to H3 is exactly what is heard in the final mix.

### 4.4 Keyframes (rework of the current still stage)
- Qwen-Image 2.1 edit composes:
  - the setup plate;
  - character identity refs + outfit;
  - the start pose and expression from the shot spec.
- Output is at the H3 generation size (864×480).
- Gates (CPU and GPU, fast):
  - identity similarity ≥ threshold;
  - outfit colours within tolerance of the wardrobe palette;
  - both characters present and on their correct side;
  - no text or garbled signs;
  - face height ≥ 18% of frame for dialogue setups.
- Failures are redrawn with a new seed (≤ 3 tries).
- **Cut rule (from the bake-off):** never cut between two shots with the same framing from a fresh keyframe. The pose snaps back, and you saw it as a glitch.
  - **Same setup back-to-back = one continuous take.** The next shot's guide is the previous shot's **last 5 frames**, anchored at frame 0 (`--guide-clip`), and its reference Picture 1 is the previous last frame. Measured seam jump: 4.2 versus 18.8 for a fresh keyframe; normal motion is 1.5.
  - **A change of setup** (two-shot → single and so on) starts from a fresh keyframe. That reads as a normal cut.
  - H3 holds `Static Shot` cleanly, so chaining doesn't cause the zoom creep LTX had.

### 4.5 Motion engines and router

| Tier | When | Engine and settings | Est. time per 8-s shot |
|---|---|---|---|
| **A** | Any shot with dialogue or acting | H3 Ref2VA int8 + Pika-Flex 6-step, 864×480. First frame locked by `MiniMaxH3AddGuide(keyframe)`. Refs: 2 portraits + outfit + plate. Audio: shot slice | ~45–60 s [validate] |
| **B** | Silent: establishing, inserts, B-roll, transitions | LTX-2.5 I2V from the keyframe, stabilised (existing code) | ~20–40 s |
| **C** | Cold-open hook, reel moments, physical comedy (≤ 6 per episode) | H3 at 1344×768, 14 steps (local). Optional: H3 2K or Kling/Veo through your paid account | ~3–4 min local |
| **Fallback** | A failed lip-sync QC twice | LongCat-Avatar (multi-person, our audio) or LatentSync mouth re-render on the best A take | ~2–4 min |

### 4.6 QC and auto-repair (extends `studio/qc/animcheck.py`)
All QC runs after a model batch, because the GPU can't hold H3 and the QC models together.

| Check | How | Pass rule |
|---|---|---|
| Lip-sync | SyncNet (LSE-C / LSE-D) on the speaker's face crop vs our audio slice | Offset ≤ 2 frames, confidence ≥ calibrated threshold [validate on anime faces] |
| Listener silent | Mouth-open ratio on the non-speaking face during the other's lines | Closed ≥ 90% of the time |
| Identity | Anime-face detection + DINOv2 embedding vs identity centroid, sampled every 12 frames | Min similarity ≥ calibrated threshold |
| Outfit / background | Colour histogram vs keyframe; plate SSIM in background regions | Within tolerance |
| Expression ceiling | VLM (existing) scores intensity 0–3 on 4 frames | ≤ 2 |
| Anatomy | VLM (existing): extra or missing fingers, merged faces | None |
| Lag / judder | Frame-difference series: frozen runs > 4 frames during speech, duplicate frames, single-frame spikes | None |
| Camera | Existing ORB scale tracking (zoom creep), Laplacian sharpness | Scale drift < 3%, sharpness ≥ keyframe × 0.8 |

Repair ladder:
1. New seed, same tier.
2. New seed, simplify the acting text.
3. Escalate: A → C, or lip-sync → fallback.
4. Flag for human review in `QC_REPORT.md`.

The pipeline never blocks; it finishes and lists anything flagged.

### 4.7 Finishing
- **Upscale** 864×480 → 1920×1080 with the NVIDIA RTX Video Super Resolution node (the Linux SDK exists but is untested here [validate]). Fallbacks:
  - Real-ESRGAN anime-video (very fast, made for flat 2D art);
  - LTX refine (the "H3 draft → LTX refine" route, ~45 s per clip).
- **Colour match** per scene (the first shot's grade is the reference).
- **Mix:** our dialogue master, plus H3 room tone at −24 dB (its invented voice is never used), music, SFX.
- **Captions, end card, reel cut, thumbnails, upload text files:** existing code.

### 4.8 Orchestrator
- **One resident ComfyUI server** for H3, driven over its HTTP API from `studio/h3.py`. Weights stay loaded across shots, and the text encoder output is cached per prompt.
- **Stage order** keeps model swaps to about 6 per episode:
  - LLM;
  - TTS;
  - Qwen-Image (keyframes);
  - H3 (all A shots, then C);
  - LTX (B);
  - QC models;
  - re-renders;
  - finishing.
- **Resumable:**
  - Each shot's output is keyed by a hash of (spec + keyframe + audio + model version), as `talk/cache` does today.
  - A reboot loses at most the shot in progress.
  - The runner is a systemd user service, so it restarts after a reboot without anyone touching it.

## 5. Time budget: 10-min episode (~75 beat shots: ~60 A, ~10 B, ~5 C)

| Stage | Estimate |
|---|---|
| Script + research + SEO | 10 min |
| Voices + pacing | 15 min |
| Keyframes (75 × ~20 s incl. gates) | 25 min |
| Tier A, measured 7.3 s of render per second of video: ~560 s of A video | 70 min |
| Tier C at 768p, measured 33 s per video second: ~40 s of hero video | 22 min |
| Tier B (10 × ~30 s) | 5 min |
| QC all + re-render ~25% | 25 min |
| Upscale + finish + reel | 15 min |
| **Total** | **≈ 3 h** (the A and C rows are measured) |

- If two-speaker beat shots fail T4 and we use one line per shot (~125 shots), the total is ≈ 3 h 40 min.
- If faces need 1344×768 for two-shots, it rises to ≈ 4.5 h, and we'd use `single` setups more.
- The bake-off decides both.

## 6. How each known problem is closed

| Problem seen so far | Root cause | Fix in v2 |
|---|---|---|
| Zoom creep, PIP seams | Chaining from generated last frames | Fresh keyframe per shot + `Static Shot` + stabiliser on B |
| Lag, stiff mouths (LTX) | Model not audio-driven | H3 drives the mouth from our audio. Lag QC |
| Maya's eyebrow not reacting | Listener had no direction | Shot spec has per-character acting + a listener rule |
| Face and outfit drift | Text-only identity | Identity refs on every keyframe and H3 call + identity QC |
| Over-the-top faces | Free-text emotions | Intensity scale with fixed phrases + VLM ceiling |
| Blur | Upscaling small faces | Medium-close framing rule + face-height gate |
| Extra or missing fingers | Model artefact | Anatomy QC + re-roll |
| Lost hour at reboot | No auto-resume | systemd service + per-shot cache |

## 7. Alternatives considered

| Option | Why not (now) |
|---|---|
| LTX-only (current) | Weak acting and lip-sync; ~6 h per episode with checks |
| LongCat-only | Look you liked, but ~2 min per 3 s at 480p: 8+ h per episode |
| All-cloud (Veo/Kling/Seedance) | They replace our voices. ~$60–300 per episode; uploads the characters |
| H3 cloud API for everything | Works, ~1 h and ~$50–75 per episode. Kept as an **option** if speed matters more than cost |
| 2D puppet rig (layered art + viseme lip-sync) | Fastest and perfectly consistent, but stiff; may later be used for tiny reaction inserts |

## 8. Risks

- **H3 licence:** it excludes the US, EU, UK and South Korea. Confirm your territory before production. Outside those, local use is covered.
- **Anime style on H3:** most published tests are photoreal; cartoon lip-sync quality is unproven → T1.
- **SyncNet** is trained on real faces; its scores on anime may be unreliable → calibrate in T1, VLM as backup.
- **RTX VSR on Linux** is untested → T6, with Real-ESRGAN as the fallback.

## 9. Validation bake-off (before any production build)
These use the existing 34-s yen acting scene (`tests/acting_scene`), so the results compare directly with the earlier LTX vs LongCat test you saw.

| Test | Question | Pass criterion |
|---|---|---|
| T1 | Does H3 Ref2VA lip-sync **our** Ryan and Maya audio on our art style? | You judge lip-sync and expressions ≥ LongCat (your earlier favourite) |
| T2 | Identity: do 8 shots keep both faces and outfits? | Identity QC passes 8/8; you can't spot drift |
| T3 | Speed: real seconds per 8-s shot (Flex vs Turbo, 864×480 vs 1344×768) | ≤ 60 s per 8-s A shot at 864×480 |
| T4 | Two speakers in one beat shot: right mouth moves, listener stays quiet? | ≥ 4 of 5 correct |
| T5 | Faces at 864×480 in `two_mc` sharp enough after upscale? | Your eye + sharpness gate |
| T6 | Upscaler on Linux (RTX VSR vs Real-ESRGAN anime) | Visually clean at 1080p, ≤ 15 s per clip |

Output: `OUTPUT/test_scene_C_H3.mp4` next to A (LTX) and B (LongCat), plus a timing table.

### Results (2026-11-17, RTX 5090, torch 2.15 cu132, ComfyUI 0.45, H3 Ref2VA pruned int8 + NVFP4 text encoder)
Each shot is anchored to our keyframe and **our audio** at frame 0.

| Shot | Video length | Mode / size | Render time | s per video-s |
|---|---|---|---|---|
| b1 two-shot (incl. first model load) | 9.4 s | Flex 6-step 864×480 | 71 s | 7.5 |
| b2 two speakers | 10.8 s | Flex 864×480 | 86 s | 7.9 |
| b3 Ryan single | 7.3 s | Flex 864×480 | 51 s | 7.0 |
| b4 two-shot | 8.0 s | Flex 864×480 | 58 s | 7.2 |
| b2 continued from b1 | 10.8 s | Flex 864×480 + 5-frame guide | 92 s | 8.5 |
| b2 | 10.8 s | Base 14-step 864×480 | 174 s | 16.1 |
| b2 | 10.8 s | Flex 1344×768 | 354 s | 32.8 |

- **T1 lip-sync / acting: PASS.** Your verdict was that you like the quality.
  - The output soundtrack is our recording: envelope correlation 0.986, zero offset.
  - The acting follows the script (counting on fingers, the eyebrow, folded arms, rubbing the neck).
- **T2 identity: PASS** across 4 shots and 2 framings. One flaw: Ryan's backpack from the sheet leaked into b1. Fix: a reference crop without the backpack, plus "no backpack" in the subject definition.
- **T3 speed: PASS.** Flex is 2× faster than base with no visible loss.
- **T4 two speakers in one shot: PASS.** The right mouth moves, and the listener's lips stay closed with the scripted reaction.
- **T5 sharpness:** 480p upscaled is slightly softer than native 768p (eyelashes, earrings) but clean.
  - Decision: 480p Flex for A shots, 768p only for hero (C) shots.
- **T6 upscaler: not yet tested.** It currently uses plain Lanczos. Real-ESRGAN anime / RTX VSR comes in the build phase.
- **Cut glitch b1→b2:** found by you and fixed by the cut rule in §4.4. If T1 or T3 fail, the fallback design is: LongCat for close-up dialogue, LTX for the rest, H3 cloud for hero shots.

## 9b. Build notes (2026-11-17, production build)
- **Code:**
  - `studio/h3.py` is the engine. It runs its own ComfyUI in `engines/ComfyUI` on **port 8189**; the LTX/Qwen ComfyUI stays on 8188.
  - `studio/h3stage.py` holds the shot compiler, keyframes, prompts, rendering, QC and manifests.
  - `stage_talk` uses H3 by default (`TALK_ENGINE=ltx|longcat` overrides), and LTX takes any scene H3 couldn't do.
- **24 fps end to end** (`VIDEO_FPS`, default 24; Remotion reads `fps` from props).
  - H3 and LTX are native 24.
  - Converting to 30 duplicated every 4th frame, which reads as judder (the "lag").
- **H3 animates "on twos"** (each drawing held 2 frames, the anime look you approved in the bake-off).
  - `animcheck.check_shot(..., twos=True)` compares frames 2 apart, so held drawings aren't flagged as jumps or "mouth barely moves".
- **People rule** in every prompt: exactly N people, each appears once, nobody else.
  - The 768p hook once grew a second Maya; QC caught it.
  - Fewer people detected = warning (the detector misses dark clothes on dark backgrounds). More people = hard fail.
- **Speaker face pick:** a head on the wrong half of the frame is never used as the left or right speaker (a headlamp once hid Ryan's head).
- **Known gaps:**
  - Props mentioned in the acting text (a headlamp) can appear mid-shot when the keyframe doesn't have them.
  - The upscaler is still Lanczos + unsharp.

## 10. Sources
- MiniMax H3 model card (open weights, Ref2VA, 33B): https://huggingface.co/MiniMaxAI/MiniMax-H3
- H3 on one RTX 5090 (VRAM, 175 s per 10-s 480p clip): https://ai-muninn.com/en/blog/minimax-h3-nvfp4-rtx5090
- H3 768p config stack (KJNodes chunking, cu130): https://ai-muninn.com/en/blog/minimax-h3-rtx5090-config-stack
- H3 character lock (reference portraits, framing vs blur): https://ai-muninn.com/en/blog/minimax-h3-rtx5090-character-lock
- Pika-H3-Flex / Turbo speeds: https://ai-muninn.com/en/blog/pika-h3-flex-rtx5090-whitebox-orbit
- H3 API pricing: https://www.wireflow.ai/blog/hailuo-pricing
- Models that keep your own audio: https://www.8frame.co/blog/which-ai-video-models-can-use-your-own-audio , https://fuser.studio/articles/best-ai-lip-sync-tools
- Veo / Kling / Seedance: https://pixo.video/blog/seedance-vs-veo-vs-kling , https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0
- Wan 2.7 / 3.0 not open: https://www.runpod.io/articles/guides/wan-2-7-runpod
- LTX-2.5 speed: https://ltx.io/blog/ai-video-model-speed-comparison
- NVIDIA VFX nodes for ComfyUI: https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes
