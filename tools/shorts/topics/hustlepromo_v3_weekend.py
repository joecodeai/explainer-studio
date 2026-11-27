"""Hustle Culture Reel v3: "Your Company Wants Your Weekend" -- the owner's own Reel 1 script (2026-11-27), cut from the
Gerald/Ryan scene. v2 (the whole scene, 79 s) is hustlepromo_v2_fullscene.py; v1 (montage) is hustlepromo_v1_montage.py.
New work: the door's handle painted out (keyframes/w04.png, original in keyframes/_orig), and one new Maya line (topics/hustlecta.py)."""
from topics.hustle import FOLDER  # noqa: F401
CTA = "projects/short-hustlecta/audio/x01.t.wav"
REEL = dict(title="Your Company Wants Your Weekend", pieces=[
    # HOOK: "Saturday. You don't need all of Saturday. Do you?"  (end of w01, Gerald already in close-up)
    dict(id="w01", words=(19, 27), lead=0.25, f=0.9, x=0.5),
    dict(id="w02", f=0.66, x=0.48, clean=True),                         # "I... sort of use it."
    dict(id="w03", f=0.86, x=0.5),                                      # "...quietly looked after the afternoon for you?"
    # Ryan glances at the door: no handle (painted out); slow push-in towards the empty backplate
    dict(id="w04", src="projects/short-hustle/clips/w04_still_s21.mp4", f=(0.8, 0.5), x=(0.55, 0.58), gain=-14, hold=0.4),
    # "Good news, though. ... Weekend Lite gives you Saturday morning,"  -- Gerald and the price card
    dict(id="w07", words=(0, 20), tail=0.3, f=0.7, x=0.42, clean=True),
    # "Weekend Plus adds Sunday, but the Sunday evening dread is billed separately."  -- cut in tighter on the card
    dict(id="w07", words=(24, 35), lead=0.22, tail=0.45, f=0.5, h=0.8, x=0.4, y=0.45, clean=True),
    dict(id="w08", f=0.62, x=0.5),                                      # "I just gave you that."
    dict(id="w09", f=0.86, x=0.5),                                      # "And now you can have it back. Monthly."
    dict(id="w10", f=0.62, x=0.5),                                      # "Can I just... have the one I had before?"
    dict(id="w11", words=(0, 3), tail=0.28, f=0.62, x=0.47),             # "That plan's been discontinued."
    # PAYOFF. "How do I cancel?" framed on Ryan's face only (the cemetery brochure he holds is not in this cut)
    dict(id="w15", f=0.5, h=0.58, x=0.5, y=0.3, clean=True),
    dict(id="w16", f=0.66, x=0.5),                                      # "Cancellations are done in person. On a Saturday."
    # Hold on Ryan's face: the end of his face-falling shot, silent
    dict(id="w11", sub=(3.2, 5.0), mute=True, f=0.62, x=0.47),
    # CTA over the end card
    dict(id="c06", f=0.62, vo=dict(wav=CTA, text="And that's just one way hustle culture takes your time. Watch the full video on our "
                                                  "channel. Is Hustle Culture a Scam?", at=0.35, tail=1.0)),
])
