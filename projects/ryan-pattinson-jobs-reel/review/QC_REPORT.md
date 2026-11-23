# QC report — ryan-pattinson-jobs-reel

**Result: PASS** (every score ≥ 85 and no open CRITICAL)

| Score | Value |
|---|---|
| Visual quality | 100.0 |
| Character consistency | 100.0 |
| Physical positioning | 100.0 |
| Animation quality | 93.6 |
| Audio quality | 97.6 |
| Lip synchronization | 100.0 |
| Subtitle accuracy | 93.6 |
| Scene continuity | 100.0 |
| Semantic accuracy | 100.0 |
| Overall | 98.3 |

Open findings: 0 critical · 0 high · 5 medium · 0 low

| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |
|---|---|---|---|---|---|---|---|---|---|
| MEDIUM | voice | 0:18.62 | 447 | s01 | 0.60 | benny's voice pitch jumps +5.2 semitones on this line |  | retake_line | open |
| MEDIUM | animation | 0:18.95 | 455 | s01 | 0.80 | animated shot s01 line 3 (glitch): sudden jump at frames 8-20 (change 9.2 vs typical 1.0) | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | text | 0:29.15 | 700 | s02 | 0.70 | chart text missing/misread: ['what Amazon paid for MGM, Bond included', 'Sherwin Rosen: the economics of superstars'] (read ['Why one actor gets every big role', '$8.5bn', '1 film', '1981', 'what Amazon paid for', 'reaches millions of people', 'Sherwin Rosen: the', 'MGM, Bond included', 'at once', 'economics of superstars']) | check chart labels/values in script.json | no | open |
| MEDIUM | animation | 0:32.71 | 785 | s03 | 0.80 | animated shot s03 line 0 (people): person size jumps (x0.58) at frame 84 | regenerate this shot: delete it from talk/ and re-run, or ./fix with a FEEDBACK note | no | open |
| MEDIUM | subtitle | 0:37.80 | 907 | s03 | 0.90 | subtitles out of sync with speech (median 715 ms, worst 1780 ms) |  | retime_subtitles | open |
