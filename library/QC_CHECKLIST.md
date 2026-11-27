# AI VIDEO ERROR CHECKLIST (owner, 2026-11-27)
This is the standard for every long video (10 min) and every Reel. The goal is a professional result **without adding render time**.

Each error is handled in one of three ways:
- **PREVENT:** stopped before generation by the prompt and shot rules in `tools/shorts/topics/show3d.py` and the script rules below. This costs nothing.
- **AUTO:** caught by `build.py <topic> qc` (`tools/shorts/qc_auto.py`), which runs after the mix in about a minute. Any flagged shot is fixed with a targeted redo: a new seed, a regenerated keyframe, or a timing change. Never a full re-render.
- **EYE:** checked by Claude on the contact sheets and lip-sync strips that `sheets` already makes. Claude reports any failure honestly.

**Fixed causes from past videos**, already built in so they don't repeat:

| Cause | Fix |
|---|---|
| Wide framing made H3 jump to a close-up mid-clip | Maya close-ups (`close=True`); the AUTO jump check |
| The image model paints green/purple specks | `autoclean.py` on every keyframe |
| Duplicate characters | "Exactly one person" and ONCE |
| A set plate forced wide shots | Close-ups skip the plate |
| A night clause turned the studio to night | Night lighting lives only in STREET |
| Generated room tone contained murmurs | Synthetic room tone |

---

## Before writing (script and shot rules: PREVENT)
- **One action per shot.** Never write "stands up and sits down" or "picks up and puts away" in one shot. Each change of posture gets its own shot, which avoids teleports and posture jumps.
- **Hands:**
  - Hands are relaxed, holding one clear object, or folded.
  - Avoid open raised palms (green smudges), fingers counting (wrong finger counts), and hands touching a desk surface.
  - When a count matters (for example "four fingers"), say "exactly four fingers raised, thumb folded", and check by EYE.
- **Objects:**
  - Every prop a character holds is named in that shot's keyframe text, so it can't appear or disappear.
  - A prop stays in the same hand for the whole sequence; the hand is written into the keyframe.
  - No liquids being poured. Cups show no visible liquid level.
- **On-screen text:** none in any generated image (the STYLE already forbids it). All numbers, words and charts are `card()` shots, rendered by the builder, so they are always spelled correctly.
- **Sets:**
  - Recurring sets use the show3d phrases (STUDIO, GER_ROOM, KITCHEN, FLAT, STREET), so the room, window view, lighting and time of day stay identical.
  - A set's time of day is fixed: the studio, office and kitchen are daytime, the street is night.
- **Characters:**
  - Always use the show3d cast strings and the `REFS3D` refs. Never 2D-era refs.
  - Clothes, hair and accessories are fixed in the cast strings, so they never change between shots.
- **Lip-sync shots (H3):**
  - One speaker, framed from the chest up, under about 12 s of speech.
  - A line longer than that is split at a sentence end into two shots with different framing.
- **Motion clips (LTX):**
  - Describe one simple, physically plain action plus a slow camera move.
  - No walking across the frame, sitting down, standing up, objects being handed over, or doors opening.
  - Those moments are told by a cut between two stills instead.
- **Edit rules:**
  - A cut never lands inside a line: shots are built from whole lines, and the timeline adds GAP plus a hold after each one.
  - Punchlines get `hold` so the reaction lands before the cut.
  - A line spoken over another picture is marked OVER in the script, so a talking character is never shown silent and a silent one never shown talking.
- **Audio:**
  - No music bed.
  - One locked voice per character (Qwen presets), so the voice can't change identity.
  - Synthetic room tone, so no murmurs.
  - SFX prompts describe only the sound of that shot's action.

## The checklist and how each part is covered

### 1. Human anatomy and body
**Errors to catch:**
- Extra or missing fingers, or fingers merging.
- Extra or missing limbs.
- Limbs changing shape.
- Hands merging with objects, or passing through desks and walls.
- Bodies intersecting furniture.
- Parts disappearing.
- Neck stretching.
- Face changing shape.
- Asymmetric or unnatural eyes.
- Teeth appearing or disappearing.
- Head size changing.
- Proportions changing.
- Feet floating, or sinking into the floor or furniture.

**Coverage:**
- **PREVENT:** STYLE and LOOK ask for correct anatomy, five fingers, solid contact with furniture and floors, and a stable face and proportions. The hand rules above.
- **AUTO:** the jump and morph check flags any lip-sync or motion clip whose picture changes abruptly inside the clip, which is how face changes and limb pops show up.
- **EYE:** the keyframe contact sheet (hands, feet and furniture contact) and the five-frame strips of every animated clip.

### 2. Scene continuity
**Errors to catch:**
- Sudden position or posture changes.
- Teleporting.
- Standing in one frame and sitting in the next.
- Objects appearing, disappearing, moving or resizing.
- Background changing.
- Doors or windows changing.
- Clothing, hair or accessories changing.
- Lighting or time of day changing.
- Identity drift.
- A character switching sides.
- Inconsistent spatial relationships.

**Coverage:**
- **PREVENT:** the locked cast, set phrases, set plates and lighting. One action per shot. Fixed time of day per set.
- **AUTO:** the jump check inside clips.
- **EYE:** the contact sheet read in story order, checking side of room, props in hands, clothes, hair and time of day shot to shot.

### 3. Movement and physical logic
**Errors to catch:**
- Walking without moving forward, or sliding.
- Feet not touching the ground.
- Wrong speed.
- Motion with no physical cause.
- Floating objects, or objects moving on their own.
- Objects passing through each other.
- Grabbing without touching.
- A set-down object vanishing.
- A hand not following a held object.
- A chair moving on its own.
- Hair or clothes moving without cause.
- Turning without body movement.
- Sitting or standing unnaturally.
- Shadows or reflections not matching the movement.

**Coverage:**
- **PREVENT:** the LTX rules above (no walking, sitting or handing over; one plain action). LOOK asks for weight, contact and no sliding.
- **AUTO:** the jump check.
- **EYE:** the motion-clip strips.

### 4. Dialogue, speech and lip-sync
**Errors to catch:**
- Lips moving without audio, or audio without lips moving.
- Lip movements not matching the words.
- Mouth moving after the line ends, during a pause, or before the line starts.
- Distorted teeth or tongue.
- Wrong speaker, or two people talking at once.
- Expression not matching the line.
- Voice continuing after the speaker has stopped.
- Dialogue cut off by a scene cut.

**Coverage:**
- **PREVENT:**
  - H3 is driven by each character's own line audio (`anchor_audio`), one speaker per lip-sync shot.
  - On-camera only when that character is speaking (`talk` rule in build).
  - Each line's mood is written into the keyframe expression and the H3 prompt.
- **AUTO:**
  - The whole-video transcript is compared with the script, flagging missing, extra or garbled words.
  - Unexpected silences over 2.5 s are flagged, as is audio clipped at a cut (a line longer than its shot).
- **EYE:** the lip-sync strips (mouth open on silent frames, expression versus line).

### 5. Editing and scene transitions
**Errors to catch:**
- Cutting before a line or action finishes, or while someone is about to speak.
- An interrupted gesture.
- A mouth left open, or a half-blink, at the cut.
- Jump cuts, sudden angle changes, camera jumps.
- Transitions too early or too late.
- Repeated or black frames, flashes, unintended blends.
- An unfinished movement carried into the next scene.
- Audio bleeding into the next scene.

**Coverage:**
- **PREVENT:** cuts only fall between whole lines (GAP plus hold); punchline holds; each shot's SFX is cut and faded with its shot.
- **AUTO:**
  - Black frames and flashes (`blackdetect`).
  - Frozen video (`freezedetect` outside planned holds).
  - The jump check inside clips.
  - Any shot whose clip is shorter than its slot (the "holding last frame" warning).
- **EYE:** the first and last frame of every lip-sync clip (mouth state at the cut).

### 6. Facial expressions and emotion
**Errors to catch:**
- A smile appearing or vanishing.
- An unmotivated change of expression.
- The wrong emotion for the line.
- Eyes not following the person or object they look at.
- Staring, unnatural blinking.
- Eyebrows changing.
- A frozen face.
- Reacting too early, or not at all.
- An abrupt emotion change between shots.

**Coverage:**
- **PREVENT:** every shot names its expression; reaction shots come after the event in the shot order.
- **EYE:** the lip-sync strips and the contact sheet in order.

### 7. Objects and props
**Errors to catch:**
- Props changing shape, colour or size.
- A prop disappearing or switching hands.
- Liquid levels changing.
- A phone or laptop changing design or position.
- Distorted pages.
- Duplicated or merged objects.
- Objects wrongly placed on surfaces.
- An orientation flip.
- Interacting with an imaginary object.

**Coverage:**
- **PREVENT:** the prop rules above. Recurring props (Gerald's paper plane, receipts, Brayden's watch) are written the same way every time.
- **EYE:** the contact sheet.

### 8. Camera
**Errors to catch:**
- A sudden zoom.
- Shake.
- The camera passing through objects or people.
- Odd rotation.
- The subject leaving the frame or being badly cropped.
- A focus or depth-of-field jump.
- An angle change without an edit.
- An abrupt change in framing.

**Coverage:**
- **PREVENT:**
  - Lip-sync shots are "Static camera".
  - LTX gets one slow, named move.
  - Still shots use the builder's smooth push in or out only.
  - The Reel compositor never crops faces.
- **AUTO:** the jump check (angle changes inside a clip).
- **EYE:** the strips.

### 9. Clothing and appearance
**Errors to catch:**
- Colour, pattern, buttons, tie, sleeves or shoes changing.
- Clothes merging with the body or passing through furniture.
- Jewellery, Maya's hoops or Gerald's glasses changing.
- Hair, makeup or wrinkles flickering.

**Coverage:**
- **PREVENT:** the cast strings fix every garment and accessory, and the refs show them.
- **EYE:** the contact sheet (hoops, glasses, watch, lanyard, hoodie strap).

### 10. Lighting, shadows and environment
**Errors to catch:**
- Wrong shadow direction, or no shadow.
- A shadow moving on its own.
- Flicker, or face brightness changing.
- Background lighting changing.
- Wrong reflections or mirrors.
- An inconsistent window view.
- Weather changing.
- Warping walls, flickering textures.

**Coverage:**
- **PREVENT:** one LIGHT line (key light from the upper left, warm fill, contact shadows) for every shot; a fixed time of day per set; the set plates. LOOK asks for no flicker.
- **AUTO:** a brightness-jump check inside each clip (part of the jump check).
- **EYE:** the contact sheet.

### 11. Audio and sound design
**Errors to catch:**
- Music stopping or changing (there is no music).
- Dialogue volume or voice changing between shots.
- Background noise dropping out.
- SFX early or late.
- Abrupt cut-offs, or audio continuing past the scene.
- Unwanted silence.
- Overlaps.
- Duplicated dialogue.

**Coverage:**
- **PREVENT:** locked voices; per-line loudness normalisation; synthetic room tone under every shot; SFX faded per shot.
- **AUTO:**
  - Integrated loudness (target −14 LUFS ±1, peak below −1 dBFS).
  - Silences over 2.5 s.
  - Duplicated or missing words in the transcript diff.
  - A murmur check: speech-like words found where the script has none.

### 12. Text, graphics and screen content
**Errors to catch:**
- Misspelled, changing, distorted or unreadable text.
- Changing logos.
- Changing screen content.
- Changing numbers or dates.
- Subtitles not matching the dialogue or mistimed.
- Floating or misplaced text or UI.

**Coverage:**
- **PREVENT:** no text in generated images (the STYLE forbids it); all text comes from `card()` and the caption builder; screens are described as plain glowing screens or simple icons.
- **AUTO:** captions are built from the word-aligned audio, so they can't drift. The transcript diff checks that the words match.
- **EYE:** any screen or sign in the contact sheet.

---

## The QC routine for every video (same render time; the checks run in about a minute)
1. **Keyframes:** after `kf`, `autoclean` has already run. Read the keyframe contact sheet in story order against sections 1, 2, 7, 9, 10 and 12. Redo only the failed keyframes.
2. **Animation:** after `anim`/`sheets`, read every lip-sync and motion strip against sections 1–6 and 8. Re-seed only the failed clips.
3. **Final check:** after `mix`, run `build.py <topic> qc` and fix every FLAG.
4. **Report:** report the remaining warnings honestly in the hand-off. Never claim "no errors" without these three passes.
