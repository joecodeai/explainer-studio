# QC report — myanmar-lobbies-the-us-to-invest-in-its-rare-earth

**Result: PASS** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 97.6 |
| Character consistency | 100.0 |
| Physical positioning | 98.0 |
| Animation quality | 90.4 |
| Audio quality | 88.0 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 85.3 |
| Scene continuity | 100.0 |
| Semantic accuracy | 99.5 |
| Overall | 95.4 |

Open findings: 0 critical · 2 high · 9 medium · 4 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| HIGH | voice |  |  |  | 0.60 | dr_aris_thorne and elena_vance sound almost identical (timbre 0.989, pitch Δ 0.5 st) | redesign one of the two voices | no | manual |
| HIGH | animation | 2:27.07 | 4412 | s13 | 0.80 | animated shot s13 line 1 (identity): character stops looking like their reference art (similarity 0.77 vs 0.89) from frame 36 — best of 3 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | manual |
| MEDIUM | voice | 0:04.95 | 149 | s01 | 0.60 | narrator's voice pitch jumps +11.4 semitones on this line |  | retake_line | open |
| MEDIUM | visual | 0:07.47 | 224 | s01 | 0.60 | blurred frames |  | no | open |
| MEDIUM | text | 0:57.25 | 1717 | s06 | 0.50 | s06: The label 'Myitkyina, Kachin State' is placed over the red area but does not clearly indicate the city's location with a marker or precise positioning, potentially causing confusion about its exact position within Kachin State. | Add a small dot or marker at the location of Myitkyina to clearly indicate its position on the map, and ensure the label is properly aligned and does not overlap with other elements. | no | open |
| MEDIUM | voice | 1:04.38 | 1932 | s06 | 0.60 | narrator's voice pitch jumps +5.4 semitones on this line |  | retake_line | open |
| MEDIUM | subtitle | 1:53.79 | 3414 | s10 | 0.90 | subtitles out of sync with speech (median 19 ms, worst 720 ms) |  | retime_subtitles | open |
| MEDIUM | physical | 3:01.07 | 5432 | s16 | 0.50 | s16: Character's feet are not visible, making it impossible to confirm if they are standing on the floor or floating. The character's scale appears slightly off relative to the office furniture and windows, suggesting a potential perspective issue. | Ensure the character's feet are visible and clearly touching the floor, and adjust the character's scale to match the perspective of the room and furniture. | no | open |
| MEDIUM | text | 4:08.68 | 7460 | s22 | 0.50 | s22: The label 'MYANMAR' is partially obscured by the red shape of the country, making it less readable. | Reposition the 'MYANMAR' label to ensure it is fully visible and not overlapped by the country's fill color. | no | open |
| MEDIUM | text | 4:30.87 | 8126 | s24 | 0.50 | s24: The label 'Naypyidaw' is positioned slightly to the west of its correct geographical location on the map, placing it closer to the border with India rather than its actual position in central Myanmar. | Reposition the label 'Naypyidaw' to align more accurately with its geographical location in central Myanmar. | no | open |
| MEDIUM | subtitle | 4:42.51 | 8475 | s25 | 0.90 | subtitles out of sync with speech (median 1610 ms, worst 5580 ms) |  | retime_subtitles | open |
| LOW | text | 0:09.24 | 277 | s02 | 0.50 | s02: The label 'Kunming' is positioned slightly north of its correct geographical location relative to Myitkyina and the border with China. | Reposition the 'Kunming' label to a more accurate location on the map, closer to the actual city in Yunnan Province, China. | no | open |
| LOW | text | 1:51.23 | 3337 | s10 | 0.50 | s10: The label 'Myitkyina, Kachin State' is slightly cut off at the end, making it partially unreadable. | Adjust the label position or font size to ensure 'Myitkyina, Kachin State' is fully visible and not truncated. | no | open |
| LOW | semantic | 2:16.19–2:20.19 | 4086 | s12 | 0.50 | hero shot: The cracked map, mineral samples, and diplomatic cables are clearly depicted, and the dramatic side lighting effectively creates long shadows, accurately conveying the intended editorial illustration. |  | no | open |
| LOW | text | 2:35.93 | 4678 | s14 | 0.50 | s14: The label 'Myitkyina, Kachin State' is positioned slightly above and to the left of the actual location on the map, which may cause confusion. The label 'Naypyidaw' is correctly placed but could be more clearly associated with its location due to proximity to the red area. | Reposition the 'Myitkyina, Kachin State' label to align more accurately with its geographical location on the map. Ensure labels are clearly associated with their respective points using lines or better placement. | no | open |
