# QC report — placebo-buttons-reel

**Result: FAIL** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 0.0 |
| Character consistency | 100.0 |
| Physical positioning | 100.0 |
| Animation quality | 76.0 |
| Audio quality | 95.2 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 100.0 |
| Scene continuity | 62.0 |
| Semantic accuracy | 100.0 |
| Overall | 81.5 |

Open findings: 12 critical · 3 high · 7 medium · 3 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| CRITICAL | visual | 0:00.00 | 0 | s01 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:03.08 | 74 | s02 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:12.25 | 294 | s03 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:19.21 | 461 | s04 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:23.01 | 552 | s05 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:25.09 | 602 | s06 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:26.63 | 639 | s07 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:28.72 | 689 | s08 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:30.26 | 726 | s09 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:33.35 | 800 | s10 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | visual | 0:37.01 | 888 | s11 | 0.90 | scene renders at 1080x1920, expected 1920x1080 | re-render the scene | rerender | open |
| CRITICAL | ending | 0:37.01 | 888 | s11 | 0.95 | no proper ending: no sign-off (thanks for watching / subscribe) at the end | end with a narrator wrap-up (key takeaway) and a thanks-for-watching / subscribe sign-off | add_outro | open |
| HIGH | animation | 0:26.76 | 642 | s05 | 0.80 | animated shot s05 line 0 (identity): shot drifts away from its first frame (similarity 0.83) from frame 90 — best of 2 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| HIGH | visual | 0:30.26–0:30.30 | 726 | s09 | 0.90 | blank / single-colour frame | re-render the scene; if it persists regenerate the source shot | rerender | open |
| HIGH | visual | 0:37.01–0:37.06 | 888 | s11 | 0.90 | blank / single-colour frame | re-render the scene; if it persists regenerate the source shot | rerender | open |
| MEDIUM | voice | 0:07.94 | 191 | s02 | 0.60 | benny's voice pitch jumps +7.1 semitones on this line |  | retake_line | open |
| MEDIUM | voice | 0:08.84 | 212 | s02 | 0.60 | maya's voice pitch jumps +6.2 semitones on this line |  | retake_line | open |
| MEDIUM | animation | 0:11.36 | 273 | s02 | 0.80 | animated shot s02 line 3 (glitch): sudden jump at frames 9-13 (change 6.0 vs typical 0.4) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | animation | 0:19.63 | 471 | s04 | 0.80 | animated shot s04 line 0 (glitch): sudden jump at frames 10-25 (change 9.5 vs typical 0.8) — best of 2 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | animation | 0:21.92 | 526 | s04 | 0.80 | animated shot s04 line 0 (glitch): sudden jump at frames 65-74 (change 9.0 vs typical 0.8) — best of 2 attempts | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | animation | 0:24.67–0:24.84 | 592 | s05 | 0.60 | sudden jump inside a shot (no cut expected here) | check pose switch / camera move at this time | no | open |
| MEDIUM | animation | 0:27.80–0:28.05 | 667 | s07 | 0.60 | sudden jump inside a shot (no cut expected here) | check pose switch / camera move at this time | no | open |
| LOW | visual | 0:24.07 | 578 | s05 | 0.50 | s05: VLM check could not run: lms load failed: Error: Operation canceled.
 |  | no | open |
| LOW | visual | 0:27.70 | 665 | s07 | 0.50 | s07: VLM check could not run: lms load failed: Error: Operation canceled.
 |  | no | open |
| LOW | visual | 0:35.43 | 850 | s10 | 0.50 | s10: VLM check could not run: cannot load qwen/qwen3-vl-30b: Error: Operation canceled.
 |  | no | open |
