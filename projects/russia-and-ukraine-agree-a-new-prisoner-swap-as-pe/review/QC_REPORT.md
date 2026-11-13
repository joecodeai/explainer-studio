# QC report — russia-and-ukraine-agree-a-new-prisoner-swap-as-pe

**Result: FAIL** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 96.5 |
| Character consistency | 100.0 |
| Physical positioning | 100.0 |
| Animation quality | 90.4 |
| Audio quality | 97.6 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 78.4 |
| Scene continuity | 100.0 |
| Semantic accuracy | 99.0 |
| Overall | 95.8 |

Open findings: 0 critical · 1 high · 11 medium · 9 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| HIGH | text | 1:06.38 | 1991 | s06 | 0.50 | s06: The map labels 'Dublin' and 'Continued Negotiations' are missing. The narration mentions a flight to Dublin, but the map only shows Abu Dhabi and Moscow, making the route incomplete and misleading. | Add 'Dublin' to the map and include a flight path from Moscow to Dublin, ensuring all locations mentioned in the narration are visually represented. | no | manual |
| MEDIUM | text | 0:13.26 | 398 | s02 | 0.50 | s02: The label 'Abu Dhabi' is positioned over the city of Dubai on the map, which is geographically incorrect. Abu Dhabi is located further south along the coast, while Dubai is north of Abu Dhabi. This misplacement causes confusion between the two cities. | Reposition the 'Abu Dhabi' label to the correct location on the map, south of Dubai, to reflect accurate geography. | no | open |
| MEDIUM | text | 1:02.43 | 1873 | s05 | 0.70 | chart text missing/misread: ['Ukrainian troops returned (latest swap)'] (read ['Prisoner Exchange Scale', '150', '150', 'Pending', 'Ukrainian troops', 'Russian soldiers', 'Final numbers for Abu Dhabi', 'returned (latest swap)', 'exchanged', 'deal']) | check chart labels/values in script.json | no | open |
| MEDIUM | animation | 1:10.99 | 2130 | s07 | 0.80 | animated shot s07 line 0 (people): person size jumps (x0.57) at frame 0 | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | text | 1:53.64 | 3409 | s09 | 0.50 | s09: The label 'Kyiv' is missing from the map, despite being mentioned in the narration and expected in the scene. | Add the label 'Kyiv' to the map, placing it near the red area in Ukraine. | no | open |
| MEDIUM | text | 1:53.64 | 3409 | s09 | 0.50 | s09: The label 'Odesa' is missing from the map, despite being mentioned in the narration and expected in the scene. | Add the label 'Odesa' to the map, placing it on the western coast of Ukraine. | no | open |
| MEDIUM | text | 1:53.64 | 3409 | s09 | 0.50 | s09: The label 'Kharkiv' is missing from the map, despite being mentioned in the narration and expected in the scene. | Add the label 'Kharkiv' to the map, placing it in northeastern Ukraine. | no | open |
| MEDIUM | animation | 2:03.66 | 3710 | s10 | 0.80 | animated shot s10 line 1 (lipsync): lip movement does not follow the speech (correlation -0.04) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | voice | 2:22.18 | 4265 | s11 | 0.60 | narrator's voice pitch jumps +7.0 semitones on this line |  | retake_line | open |
| MEDIUM | text | 3:10.46 | 5714 | s14 | 0.70 | chart text missing/misread: ['4½ years'] (read ['Humanitarian Impact', 'Hundreds of', 'thousands', '4/2 years', 'Killed since 2022, reports estimate', 'Of full-scale war']) | check chart labels/values in script.json | no | open |
| MEDIUM | text | 3:14.68 | 5840 | s15 | 0.50 | s15: The label 'IRELAND' is positioned to the left of the island, but the red dot indicating Dublin is placed on the island, which may cause confusion about the label's association with the location. | Reposition the 'IRELAND' label closer to the red dot marking Dublin to ensure clear association. | no | open |
| MEDIUM | animation | 4:07.74 | 7432 | s19 | 0.80 | animated shot s19 line 1 (people): person size jumps (x0.57) at frame 0 | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| LOW | visual | 0:00.00–0:08.53 | 0 | s01 | 0.50 | hero shot: The cracked peace accord document has a visible crack line that appears to be part of the paper's design rather than a realistic crack, which may not clearly convey the intended symbolism of damage or fragility. |  | no | open |
| LOW | semantic | 0:00.00–0:08.53 | 0 | s01 | 0.50 | hero shot: The helmets are shown with full faces and expressions, which is inconsistent with the idea of them being 'weathered military helmets' as inanimate objects; this anthropomorphism may distract from the intended editorial message. |  | no | open |
| LOW | visual | 0:00.00–0:08.53 | 0 | s01 | 0.50 | hero shot: The glowing line dividing the table surface is not clearly visible or distinct, making it difficult to perceive as a meaningful division. |  | no | open |
| LOW | visual | 2:27.71–2:35.41 | 4431 | s12 | 0.50 | hero shot: The image contains a faint crack in the wooden table, which is a visual element intended to symbolize division. However, the crack appears slightly too uniform and stylized, lacking the natural irregularities of a real wood crack, which may reduce the realism of the scene. |  | no | open |
| LOW | semantic | 2:27.71–2:35.41 | 4431 | s12 | 0.50 | hero shot: The scene includes a compass, military maps, pens, and sealed envelopes, which align with the intended editorial theme of division between military and diplomatic efforts. However, the compass is placed on top of the maps, which may not be practical in a real-world scenario, potentially confusing the viewer about the object's function. |  | no | open |
| LOW | visual | 2:27.71–2:35.41 | 4431 | s12 | 0.50 | hero shot: The pens and envelopes are depicted with a high level of detail, but the envelopes appear to be slightly overlapping in a way that suggests they are merging, which could be interpreted as a rendering artifact. |  | no | open |
| LOW | visual | 3:50.73–3:58.76 | 6922 | s18 | 0.50 | hero shot: Hands are rendered with simplified, rounded forms typical of cartoon style; no extra or missing fingers, but fingers appear slightly fused and lack detailed articulation, which is stylistic rather than a defect. |  | no | open |
| LOW | visual | 3:50.73–3:58.76 | 6922 | s18 | 0.50 | hero shot: The map appears to have a slight warping effect at the edges, possibly due to lighting or rendering, but it remains clearly a folded paper map with visible markings. |  | no | open |
| LOW | visual | 3:50.73–3:58.76 | 6922 | s18 | 0.50 | hero shot: The pen and hand interaction shows a slight blending of the pen into the hand, which may be due to soft shadows and lighting, but no actual merging or structural defect is present. |  | no | open |

## Corrections applied

| Round | Finding | Result |
|---|---|---|
| 1 | narrator's voice pitch jumps +5.4 semitones on this line | s11: line 7d00e574a1 re-voiced |
| 1 | subtitles out of sync with speech (median 0 ms, worst 620 ms) | s11: subtitle timing rebuilt from speech |
| 1 | narrator's voice pitch jumps +5.4 semitones on this line | fixed (verified by re-inspection) |
| 1 | subtitles out of sync with speech (median 0 ms, worst 620 ms) | fixed (verified by re-inspection) |
| 2 | narrator's voice pitch jumps +5.1 semitones on this line | s11: line 7d00e574a1 re-voiced |
| 2 | narrator's voice pitch jumps +5.1 semitones on this line | fixed (verified by re-inspection) |
| 3 | narrator's voice pitch jumps +7.0 semitones on this line | could not auto-fix (needs manual review) |
