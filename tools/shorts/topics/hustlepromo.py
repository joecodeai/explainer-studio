"""Hustle Culture Reel, v2 (approved 2026-11-25): ONE situation, "HR Took My Weekend". Storyboard:
VIDEOS/Is Hustle Culture a Scam/REEL STORYBOARD.md. The whole Gerald/Ryan scene w01-w16 in its original order, full length,
nothing sped up. v1 (montage across the episode) is kept as hustlepromo_v1_montage.py. Built by tools/shorts/promo.py."""
from topics.hustle import FOLDER  # noqa: F401
REEL = dict(title="HR Took My Weekend", pieces=[
    dict(id="w01", f=0.9, x=0.5),                        # Gerald, tissues, sun picture; hook "Nobody's in trouble"
    dict(id="w02", f=0.66, x=0.48, clean=True),            # Ryan: "I... sort of use it."
    dict(id="w03", f=0.86, x=0.5),                         # "quietly looked after the afternoon"
    dict(id="w04", f=0.8, x=0.55, gain=-14),               # quiet beat: the door, the way out (its generated room tone murmurs: -14 dB)
    dict(id="w05", f=0.75, x=0.5, clean=True),             # "Put the weekend down, Ryan. Slowly."
    dict(id="w06"),                                        # FULL: the sun slides across the table between two hands
    dict(id="w07", f=(0.7, 0.62), x=0.42, clean=True),     # the subscription tiers, slow push-in on Gerald + card
    dict(id="w08", f=0.62, x=0.5),                         # "I just gave you that."
    dict(id="w09", f=0.86, x=0.5),                         # "And now you can have it back. Monthly."
    dict(id="w10", f=0.62, x=0.5),                         # "Can I just... have the one I had before?"
    dict(id="w11", f=0.62, x=0.47),                        # "discontinued ... premium folder" on Ryan's face
    dict(id="w12", f=0.6, x=0.52, hold=0.5),               # the imp: "He's good." (held so it registers)
    dict(id="w13", f=0.7, x=0.45, clean=True),             # the cemetery offer
    dict(id="w14", f=0.85, x=0.5),                         # the brochure (ball pit has real green/purple balls: no cleaning)
    dict(id="w15", f=0.62, x=0.5, clean=True),             # "How do I cancel?"
    dict(id="w16", f=0.66, x=0.5),                         # "Cancellations are done in person. On a Saturday." + hold
])
