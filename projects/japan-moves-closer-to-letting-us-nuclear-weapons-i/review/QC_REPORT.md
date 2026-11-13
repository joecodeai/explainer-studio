# QC report — japan-moves-closer-to-letting-us-nuclear-weapons-i

**Result: PASS** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 98.5 |
| Character consistency | 100.0 |
| Physical positioning | 100.0 |
| Animation quality | 85.6 |
| Audio quality | 97.6 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 85.9 |
| Scene continuity | 100.0 |
| Semantic accuracy | 98.5 |
| Overall | 96.2 |

Open findings: 0 critical · 0 high · 10 medium · 7 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| MEDIUM | voice | 0:05.69 | 171 | s01 | 0.60 | narrator's voice pitch jumps +5.4 semitones on this line |  | retake_line | open |
| MEDIUM | animation | 1:18.86 | 2366 | s12 | 0.80 | animated shot s12 line 0 (lipsync): mouth keeps moving when the speech stops (silent 2.73 vs speaking 2.32) — best of 2 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | text | 1:32.46 | 2774 | s13 | 0.70 | chart text missing/misread: ['Extracted plutonium (end of 2024)'] (read ["Japan's plutonium, as cited by China's envoy", '44.4 t', '~5,500', '191 t', 'Extracted plutonium (end', 'Warheads it could make,', 'of 2024)', 'he claimed', 'Unexracted, in spent fuel']) | check chart labels/values in script.json | no | open |
| MEDIUM | animation | 1:41.05 | 3032 | s16 | 0.80 | animated shot s16 line 1 (people): person size jumps (x0.59) at frame 0 — best of 3 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | animation | 1:53.35 | 3400 | s19 | 0.80 | animated shot s19 line 0 (lipsync): lip movement does not follow the speech (correlation 0.04) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | subtitle | 2:21.65 | 4250 | s23 | 0.90 | subtitles out of sync with speech (median 230 ms, worst 260 ms) |  | retime_subtitles | open |
| MEDIUM | animation | 2:23.28 | 4299 | s23 | 0.60 | sudden jump inside a shot (no cut expected here) | check pose switch / camera move at this time | no | open |
| MEDIUM | subtitle | 2:23.60 | 4308 | s23 | 0.90 | subtitles out of sync with speech (median 306 ms, worst 326 ms) |  | retime_subtitles | open |
| MEDIUM | animation | 2:26.88 | 4407 | s23 | 0.60 | sudden jump inside a shot (no cut expected here) | check pose switch / camera move at this time | no | open |
| MEDIUM | subtitle | 2:40.69 | 4821 | s25 | 0.90 | subtitles out of sync with speech (median 0 ms, worst 700 ms) |  | retime_subtitles | open |
| LOW | semantic | 0:00.00–0:10.37 | 0 | s01 | 0.50 | hero shot: The lantern's paper shade is depicted as cracked glass or stone, which is inconsistent with the intended description of a paper shade. |  | no | open |
| LOW | text | 0:14.04 | 421 | s02 | 0.50 | s02: The label 'Hiroshima' is positioned slightly to the west of its actual geographical location relative to Tokyo on the map, which may cause confusion. | Reposition the 'Hiroshima' label to align more accurately with its geographical location on the map. | no | open |
| LOW | visual | 1:04.47–1:08.44 | 1934 | s10 | 0.50 | hero shot: The shield has a slightly irregular top edge, appearing to merge with the character's back, which could be interpreted as a minor rendering artifact. |  | no | open |
| LOW | semantic | 1:04.47–1:08.44 | 1934 | s10 | 0.50 | hero shot: The fan's design includes a hibiscus flower, but the flower's petals appear slightly distorted, potentially affecting the clarity of the intended symbol. |  | no | open |
| LOW | visual | 1:34.94–1:37.44 | 2848 | s15 | 0.50 | hero shot: The image clearly shows a chessboard with stone and metal-like pieces, including a prominent red rook casting a long shadow, effectively conveying the intended cinematic and symbolic idea. |  | no | open |
| LOW | visual | 2:09.16–2:12.83 | 3875 | s21 | 0.50 | hero shot: The compass needle appears to be physically embedded in the man's chest, which is an unrealistic and visually jarring merging of objects. |  | no | open |
| LOW | semantic | 2:09.16–2:12.83 | 3875 | s21 | 0.50 | hero shot: The image conveys the intended idea of a compass spinning over a map with floating papers and ink blots, but the compass's placement on the man's chest may distract from the intended metaphor. |  | no | open |
