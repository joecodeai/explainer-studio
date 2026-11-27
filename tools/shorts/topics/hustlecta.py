"""New Maya lines for the Hustle Reels (owner's Reel scripts, 2026-11-27). Voice only: build.py hustlecta voice."""
from topics.hustle import *  # noqa: F401,F403  (same cast, voices and tempo as the episode)
from topics.hustle import card
_C = dict(big="SCAM?", small="IS HUSTLE CULTURE A", bg="#3C5A50")
SHOTS = [
    card("x01", "And that's just one way hustle culture takes your time. Watch the full video on our channel. Is Hustle Culture a Scam?", **_C),
    card("x02", "Brayden has already had a cold shower, a hot shower, and an argument with a swan.", **_C),
    card("x03", "Six, he films his morning routine. Seven, he edits his morning routine. Nine, he posts his morning routine.", **_C),
    card("x04", "But here's the real question. Is working harder actually making you richer, or just more tired?", **_C),
    card("x05", "Watch the full video on our channel.", **_C),
]
