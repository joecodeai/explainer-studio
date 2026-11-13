# Explainer Studio — local AI news-explainer videos

Turns a news topic (or article URL) into a 3–10 minute animated explainer in a flat-cartoon style:
narrated, lip-synced, with maps, charts, cinematic shots, music, sound effects, burned-in captions and an `.srt`.
Everything runs on this PC (RTX 5090), no paid credits.

## Use

```bash
./make_video "Japan's new rice crisis" --minutes 6        # 1) research + script, then STOPS
#   read projects/<slug>/SCRIPT_REVIEW.md, fix facts/jokes in projects/<slug>/script.json
./make_video "Japan's new rice crisis" --approve          # 2) produce the video
./make_video "Japan's new rice crisis" --approve --rerender s07 s12   # redo just those scenes
```

Output in `projects/<slug>/`: `<slug>.mp4`, `subtitles.srt`, `thumbnail.png`, `YOUTUBE.md` (title, description, chapters,
sources, tags, upload checklist), `production.log`, `work/qc.json`.

## Pipeline (studio/pipeline.py)

| Stage | Tool | Cached in |
|---|---|---|
| Research | Google News RSS + article extraction + Wikipedia | `research.json` |
| Script & storyboard | Qwen3.6-35B-A3B (LM Studio), JSON-schema output, validator + LLM repair | `script.json`, `SCRIPT_REVIEW.md` |
| **Approval gate** | you | `APPROVED` |
| Narration | Qwen3-TTS: narrator designed once, then cloned for every line | `library/voices/narrator/`, `audio/` |
| Word timings / lip-sync | faster-whisper (timing only, script text is kept) / Rhubarb visemes | `audio/*.words.json`, `*.visemes.json` |
| Characters | Qwen-Image-2.1: base drawing → pose variants by reference edit → bg removal → mouth/eye anchors (GroundingDINO) | `library/characters/<id>/` (reused forever) |
| Backgrounds | Qwen-Image-2.1 | `library/backgrounds/` |
| Hero shots | Qwen-Image keyframe → LTX-2.5 distilled (int8), with its own synced ambience | `hero/` |
| SFX / music | Stable Audio 3 / ACE-Step 1.5 | `library/sounds/` |
| Animation | Remotion: puppets (bob, talk wobble, visemes, blinks), camera moves, SVG maps, charts, title cards, captions | `renders/<scene>.mp4` (+hash → only changed scenes re-render) |
| QC + repair | size/frame-count/black-frame/silence/speech-rate checks → redo only the failed scenes | `work/qc.json` |
| Master | ffmpeg: concat, narration + ducked music + SFX, −14 LUFS, AAC | `<slug>.mp4` |

GPU models are loaded one at a time (LLM unloads before ComfyUI; ComfyUI frees VRAM between stages).

## Customise
- Channel look & narrator voice: `studio/config.py` (`ART_STYLE`, `NARRATOR`). Delete `library/voices/narrator/` to redesign the voice.
- Pronunciations: `library/voices/pronunciations.json` e.g. `{"Xi": "Shee", "NATO": "Nay-toe"}`.
- Character looks are permanent once generated; delete `library/characters/<id>/` to redraw one.
- Animation components: `remotion/src/` (preview with `cd remotion && PATH=../bin/node/bin:$PATH npx remotion studio`).

## Before publishing
Read the script against the sources (the LLM can be wrong), mark realistic AI footage as "altered or synthetic" on YouTube,
and keep real-person depictions as clear caricature/commentary.

## Style (2026-11-13): fun, natural, news-accurate

- **Hook in the first 6 seconds.** Scene 1 is the narrator. Line 1 states the most striking fact (emotion `excited`). Line 2 is a short, offhand deadpan reaction that asks the video's *running-gag question* (emotion `sarcastic`).
- **Running gag.** The narrator keeps answering one simple question ("Is Japan worried? Hard to say.") with mock caution while real facts pile up. The question comes back 2-3 times and pays off before the end. Jokes must sound like a spontaneous reaction, not a written punchline. They are never about victims or deaths, and facts stay exact. Rules live in `studio/script.py` (SYSTEM prompt) and `studio/reel.py` (`plan()`).
- **Narrator tone changes.** `library/voices/narrator/ref_excited.wav` and `ref_sarcastic.wav` are the same voice with a different delivery. `voice.narrate` picks one based on each line's emotion (`excited`/`surprised` or `sarcastic`).
- **Reels** reuse the running gag: the hook question, a callback in the middle and the payoff at the end. The caption always says "link in bio".

## Useful knobs

- `TALK_TRIES=2 ./batch produce`: fewer LTX attempts per talking shot (faster).
- `projects/<p>/talk/RESEED` with lines like `s10_0 1`: regenerate that talking shot with fresh seeds (delete its clips first).
- `python -m studio.reel <project> [--force]`: rebuild only the reel. A hand-written plan can go in `reel/reel.json` (set `master_mtime` to 0).

## Not in git

Models, ComfyUI, `.venv`, `remotion/node_modules`, the generated art and sound libraries, and all media (mp4/wav/png). Voices are kept. Re-create the environment from the setup notes above.
