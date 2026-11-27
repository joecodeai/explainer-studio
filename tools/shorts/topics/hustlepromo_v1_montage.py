"""ONE promotional Reel for 'Is Hustle Culture a Scam?' (library/SHORTS_RULES.md, 2026-11-25). Cut by tools/shorts/promo.py.
Story: a hustle guru promises that getting up at 4 a.m. is why he's rich; his routine is so empty even his reflection walks out,
he 'restructures' his own organs to cut sleep and fires a kidney, and then we learn his 4 a.m. sunrise is a desk lamp at
4 p.m. The real 4 a.m. belongs to the fox. The question 'Is hustle culture a scam?' is asked and left open for the episode.
Framing (from frame inspection): FULL = whole 16:9 frame over blur; f = width fraction kept (BOX), x = its centre."""
from topics.hustle import FOLDER  # noqa: F401
REEL = dict(title="He Gets Up at 4 AM. It Cost Him a Kidney", pieces=[
    # HOOK: guru at "4 a.m." – fox (left) and swan (right) are both gags -> FULL
    dict(id="c01", trim=(0.3, 0), f=[(0, 0.7), (0.55, 0.7), (0.72, 1.0), (1, 1.0)], x=[(0, 0.59), (0.55, 0.59), (0.72, 0.5), (1, 0.5)]),  # close on his face for the hook, pull back to FULL as the swan line starts
    # QUESTION: title card, text spans the middle half -> BOX
    dict(id="c06", f=0.62, trim=(0, 0.35)),
    # SETUP: the routine. One character, hands 0.3-0.7 -> BOX
    dict(id="d01", f=0.6, x=0.52),
    # Even his reflection quits: man left, reflection walks out right -> FULL
    dict(id="d02"),
    # ESCALATION: "Team. Let's talk about sleep." -> BOX on Brayden
    dict(id="b02", f=0.6, x=0.5),
    # reveal: the team is his organs. Whole table matters -> FULL
    dict(id="b03"),
    # both kidneys -> BOX keeping both
    dict(id="b07", f=0.66, x=0.49),
    # one kidney leaves with its box towards the left edge -> FULL
    dict(id="b08"),
    # "He fired a kidney." empty chair, slow push-in
    dict(id="b09", f=(0.62, 0.54), x=0.5),
    # PAYOFF: his 4 a.m. videos
    dict(id="v05", f=0.6, x=0.5),
    # wide reveal: lamp (left), Brayden, school bus in daylight (right) -> FULL
    dict(id="v06"),
    # lamp with sweet wrapper + daylight blinds -> BOX keeping both
    dict(id="v07", f=0.8, x=0.45),
    # "Still counts." lamp + thumbs up
    dict(id="v08", f=0.75, x=0.42),
    # BUTTON: the real 4 a.m. belongs to the fox -> FULL
    dict(id="v09", trim=(0, 0.6), f=(1.0, 0.82), x=(0.5, 0.52)),
])
