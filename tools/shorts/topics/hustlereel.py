"""Reel / Short for 'Is Hustle Culture a Scam?' — v2 (2026-11-25, user: "the reel makes no sense").
v1 was a montage of out-of-context highlights. v2 tells ONE complete sketch with a beginning, escalation and punchline:
Gerald from People and Culture talks Ryan out of his weekend, then sells it back as a subscription. Title: "HR Took My Weekend and Sold It Back to Me".
Native 9:16. Reuses the v1 lip-sync clips r05/r07/r08/r09 and the r06 hands still; every other character line plays over the listener's
reaction (no new lip-sync renders). Lines are verbatim from the approved main script (topics/hustle.py), plus one setup line for Maya."""
from topics.hustle import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, BRAY, GER, GER_ROOM, RY_ROOM, FOX,
                           M, R, B, G, I, h, s, silent, card)
FOLDER = "Is Hustle Culture a Scam"
ERA = "modern"
GAP = 0.2
LTX_WH = (512, 896)
RY = ["ryan", "ryan_face"]
GER_KF = GER + GER_ROOM                                   # Gerald's office, same picture as the lip-sync shots
RY_FACE = RYAN + RY_ROOM                                  # Ryan opposite him
SHOTS = [
 # hook: the strangest line first
 h("r05", G, "Put the weekend down, Ryan. Slowly. Nobody has to get hurt.", GER + GER_ROOM.replace("warm gentle smile", "very calm, leaning slightly forward"),
   "He leans in slightly and speaks very softly and slowly, one hand raised in a calming gesture.", hold=0.3),
 # setup: who, where, why
 s("q02", M, "In 2019, Alibaba's founder called a nine a.m. to nine p.m., six-day week a huge blessing. Gerald, from People and Culture, has a gentler approach.",
   GER_KF + ONE, refs=["gerald"], mv="in", sfx="quiet office, a clock ticking"),
 s("q03", G, "Hi, Ryan. I'm Gerald, from People and Culture. Nobody's in trouble. I just want to talk. Let's start small. Saturday. You don't need all of Saturday. Do you?",
   RY_FACE + "uncertain, glancing at the box of tissues." + ONE, refs=RY, mv="in", sfx="quiet office, a clock ticking"),
 s("q04", R, "I... sort of use it.", GER_KF + ONE, refs=["gerald"], mv="out"),
 s("q05", G, "Of course. And that's completely valid. What if you kept the morning, and we just quietly looked after the afternoon for you?",
   RY_FACE + "looking at the door behind him, which has no handle." + ONE, refs=RY, mv="in"),
 silent("r06", "Extreme close-up, top-down view of a wooden table surface: only two hands are visible, entering from the bottom and top edges of the "
        "frame; a young hand in an orange hoodie sleeve pushes a small glowing sun-shaped object towards an older hand in a beige cardigan sleeve. "
        "No faces, no bodies. Exactly two hands in total: one from the bottom, one from the top.", 2.5, mv="in", sfx="a tiny sad chime"),
 # escalation: the subscription
 h("r07", G, "Good news. We've moved weekends to a subscription model. Weekend Plus adds Sunday, but the Sunday evening dread is billed separately.",
   GER + "sitting in a small softly lit office, brightly holding up a laminated card showing three pastel price tiers decorated with little clouds.",
   "He holds up the card cheerfully and points to a tier, delighted."),
 s("q08", R, "I just gave you that.", RY_FACE + "staring blankly, stunned." + ONE, refs=RY, mv="in"),
 s("q09", G, "And now you can have it back. Monthly.", GER_KF + ONE, refs=["gerald"], mv="in"),
 s("q10", R, "Can I just... have the one I had before?", RY_FACE + "pleading quietly, hands clasped." + ONE, refs=RY, mv="in"),
 s("q11", G, "That plan's been discontinued. But we've kept your memories of it in a premium folder.",
   RY_FACE + "slowly realising, his face falling." + ONE, refs=RY, mv="in"),
 s("q12", I, "He's good.", RYAN + "close-up, staring ahead in shock, while a tiny dark impish shadow creature sits on his shoulder whispering into his ear, impressed." + ONE,
   refs=RY, mv="in"),
 s("q13", G, "And if you'd rather sleep when you're dead, we've partnered with a lovely cemetery. Staff get ten percent off.",
   "An open glossy brochure for a cemetery: neat green lawns, gravestones in tidy rows, and one cheerful photo of a children's ball pit "
   "between the graves.", env=True, mv="in"),
 # punchline
 h("r08", R, "How do I cancel?", RYAN + RY_ROOM + "barely holding it together.", "He asks in a small, defeated voice."),
 h("r09", G, "Cancellations are done in person. On a Saturday.", GER + GER_ROOM.replace("warm gentle smile", "his warmest smile yet"),
   "He smiles his warmest smile and speaks softly.", hold=1.2),
 card("q16", "The full video is on our channel.", "SCAM?", "IS HUSTLE CULTURE A · FULL VIDEO", bg="#3C5A50"),
]
THUMB = dict(text="HR TOOK MY|WEEKEND", refs=["gerald"], pos="bottom",
             kf="Vertical: the man from the reference sitting in a small softly lit office, smiling warmly and holding a small glowing sun-shaped "
                "object in his hand like a confiscated item, a box of tissues on the side table. Exactly one person.")
TAIL = 0.8
