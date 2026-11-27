"""Hustle Culture Reel v4: "The 4 AM Morning Routine" -- the owner's Brayden script (2026-11-27), an intro to the episode.
Owner: "do it in reel format vertical without cutting anything" -> every shot FULL frame (whole 16:9 over blur), every existing
line played complete. New Maya lines x02-x05 (topics/hustlecta.py) play over existing pictures; their original audio is muted.
Earlier versions: hustlepromo_v1_montage.py, hustlepromo_v2_fullscene.py, hustlepromo_v3_weekend.py."""
from topics.hustle import FOLDER  # noqa: F401
A = "projects/short-hustlecta/audio/"
REEL = dict(title="The 4 AM Morning Routine", pieces=[
    # HOOK  BRAYDEN: "It's four a.m. Right now, you're asleep. That's why you're broke."
    dict(id="c01", words=(2, 12), lead=0.2, tail=0.35),
    # MAYA (new): "Brayden has already had a cold shower, a hot shower, and an argument with a swan."  -- the same shot continues; the swan flares up
    dict(id="c01", sub=(5.29, 11.84), vo=dict(wav=A + "x02.t.wav", text="Brayden has already had a cold shower, a hot shower, and an argument with a swan.", at=0.35, tail=0.6)),
    # BRAYDEN: "Four a.m., awake. Four oh five, ice bath. Four thirty, I read one page of a book about reading. Five, I tell the mirror it's a winner."
    dict(id="d01"),
    # His reflection quietly packs a suitcase and leaves
    dict(id="d02"),
    # MAYA (new): "Six, he films his morning routine. Seven, he edits ... Nine, he posts ..."  -- over his ring-light still; a beat after it
    dict(id="d03", vo=dict(wav=A + "x03.t.wav", text="Six, he films his morning routine. Seven, he edits his morning routine. Nine, he posts his morning routine.", at=0.3, tail=1.0)),
    # MAYA: "So the main thing his morning produces is a video of his morning."
    dict(id="d04"),
    # CTA  MAYA (new): "But here's the real question. Is working harder actually making you richer, or just more tired?"  -- Brayden asleep in his car
    dict(id="v03", vo=dict(wav=A + "x04.t.wav", text="But here's the real question. Is working harder actually making you richer, or just more tired?", at=0.3, tail=0.7)),
    # MAYA (new): "Watch the full video on our channel."  -- end card
    dict(id="c06", vo=dict(wav=A + "x05.t.wav", text="Watch the full video on our channel.", at=0.35, tail=1.3)),
])
