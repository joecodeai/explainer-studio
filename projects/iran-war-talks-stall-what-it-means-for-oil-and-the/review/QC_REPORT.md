# QC report — iran-war-talks-stall-what-it-means-for-oil-and-the

**Result: FAIL** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 98.0 |
| Character consistency | 100.0 |
| Physical positioning | 100.0 |
| Animation quality | 93.6 |
| Audio quality | 100.0 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 71.6 |
| Scene continuity | 100.0 |
| Semantic accuracy | 93.5 |
| Overall | 95.2 |

Open findings: 0 critical · 2 high · 10 medium · 5 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| HIGH | text | 2:09.84 | 3895 | s12 | 0.50 | s12: The label 'Jordan' is incorrectly placed over the Red Sea, far from the actual location of Jordan. The label 'Jordan,' appears twice, once correctly near Amman and once incorrectly over the Red Sea. | Relocate the 'Jordan' label to the correct geographical position near Amman and remove the incorrect label over the Red Sea. | no | manual |
| HIGH | semantic | 2:09.84 | 3895 | s12 | 0.50 | s12: The map labels Amman and Manama correctly, but omits Kuwait City, which is mentioned in the narration. This creates a mismatch between the visual content and the narration. | Add a label for Kuwait City on the map to align with the narration. | no | manual |
| MEDIUM | subtitle | 0:00.00 | 0 | s01 | 0.90 | subtitles out of sync with speech (median 1005 ms, worst 2470 ms) |  | retime_subtitles | open |
| MEDIUM | text | 0:02.12 | 64 | s01 | 0.50 | s01: The label 'Muscot' is misspelled and should be 'Muscat'. | Correct the spelling of 'Muscot' to 'Muscat'. | no | open |
| MEDIUM | text | 0:36.91 | 1107 | s04 | 0.50 | s04: The label 'Gaza City' is missing from the map, which is a critical geographical omission given the narration mentions 'a wider ceasefire in Gaza and Lebanon' and the map should show Gaza City as one of the key locations. | Add a label for 'Gaza City' on the map, positioned near the coast of the Gaza Strip, between Israel and Egypt. | no | open |
| MEDIUM | text | 1:11.44 | 2143 | s07 | 0.50 | s07: The label 'Red Sea Approach' is positioned too close to 'Bab al-Mandeb Strait Center', causing visual crowding and potential readability issues. | Reposition the 'Red Sea Approach' label slightly upward or to the side to avoid overlap with 'Bab al-Mandeb Strait Center'. | no | open |
| MEDIUM | subtitle | 2:05.00 | 3750 | s12 | 0.90 | subtitles out of sync with speech (median 0 ms, worst 800 ms) |  | retime_subtitles | open |
| MEDIUM | animation | 3:19.09 | 5973 | s19 | 0.80 | animated shot s19 line 0 (lipsync): lip movement does not follow the speech (correlation -0.02) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | text | 3:47.37 | 6821 | s21 | 0.50 | s21: The label 'Attack Corridor' is positioned over the Red Sea, which is geographically incorrect as it should be over the land area of Yemen near the Bab al-Mandeb Strait. This misplacement could confuse viewers about the actual location of the attack corridor. | Reposition the 'Attack Corridor' label to accurately overlay the land area of Yemen adjacent to the Bab al-Mandeb Strait. | no | open |
| MEDIUM | subtitle | 4:09.86 | 7496 | s23 | 0.90 | subtitles out of sync with speech (median 0 ms, worst 620 ms) |  | retime_subtitles | open |
| MEDIUM | animation | 4:46.30 | 8589 | s26 | 0.80 | animated shot s26 line 0 (lipsync): lip movement does not follow the speech (correlation 0.05) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | subtitle | 5:04.26 | 9128 | s27 | 0.90 | subtitles out of sync with speech (median 1985 ms, worst 5880 ms) |  | retime_subtitles | open |
| LOW | visual | 0:09.66–0:17.66 | 290 | s02 | 0.50 | hero shot: The image contains no visible watermarks, garbled text, or rendering artefacts. The cartoon style is consistent with the intended flat, bold-outline aesthetic, and the characters (helicopters, ships) are clearly defined without merging or blending issues. |  | no | open |
| LOW | visual | 1:15.44–1:23.61 | 2263 | s08 | 0.50 | hero shot: The red sea water appears unnatural and may be interpreted as blood, which could be misleading or disturbing in a non-contextual setting. |  | no | open |
| LOW | semantic | 1:15.44–1:23.61 | 2263 | s08 | 0.50 | hero shot: The smoke plumes are very dark and dense, which might suggest a fire or explosion, but there is no visible fire or damage to the ship. |  | no | open |
| LOW | visual | 1:15.44–1:23.61 | 2263 | s08 | 0.50 | hero shot: The rescue boats appear to be too small relative to the large commercial ship, which may affect the sense of scale. |  | no | open |
| LOW | visual | 3:12.76–3:19.16 | 5783 | s18 | 0.50 | hero shot: The lamp is positioned to the right, casting a warm glow on the desk and book, which aligns with the intended cinematic lighting effect. |  | no | open |

## Corrections applied

| Round | Finding | Result |
|---|---|---|
| 1 | narrator's voice pitch jumps +7.0 semitones on this line | s01: line 48b32e85a0 re-voiced |
| 1 | subtitles out of sync with speech (median 1005 ms, worst 2470 ms) | s01: subtitle timing rebuilt from speech |
| 1 | subtitles out of sync with speech (median 0 ms, worst 800 ms) | s12: subtitle timing rebuilt from speech |
| 1 | subtitles out of sync with speech (median 0 ms, worst 620 ms) | s23: subtitle timing rebuilt from speech |
| 1 | subtitles out of sync with speech (median 1985 ms, worst 5880 ms) | s27: subtitle timing rebuilt from speech |
| 1 | narrator's voice pitch jumps +7.0 semitones on this line | fixed (verified by re-inspection) |
| 2 | subtitles out of sync with speech (median 1005 ms, worst 2470 ms) | s01: subtitle timing rebuilt from speech |
| 2 | subtitles out of sync with speech (median 0 ms, worst 800 ms) | s12: subtitle timing rebuilt from speech |
| 2 | subtitles out of sync with speech (median 0 ms, worst 620 ms) | s23: subtitle timing rebuilt from speech |
| 2 | subtitles out of sync with speech (median 1985 ms, worst 5880 ms) | s27: subtitle timing rebuilt from speech |
| 3 | subtitles out of sync with speech (median 1005 ms, worst 2470 ms) | s01: subtitle timing rebuilt from speech |
| 3 | subtitles out of sync with speech (median 0 ms, worst 800 ms) | s12: subtitle timing rebuilt from speech |
| 3 | subtitles out of sync with speech (median 0 ms, worst 620 ms) | s23: subtitle timing rebuilt from speech |
| 3 | subtitles out of sync with speech (median 1985 ms, worst 5880 ms) | s27: subtitle timing rebuilt from speech |
