"""Hustle Culture Reel, native 9:16 (owner, 2026-11-27: "re-animate so it takes full screen"). The owner's Brayden script,
re-drawn and re-animated vertically. ALL audio is the already-recorded lines (copied into projects/short-hustlevert/audio/):
h1 = Brayden's hook cut from c01, h3 = d01, h6 = d04, h2/h5/h7/h8 = Maya's new lines x02-x05 (topics/hustlecta.py)."""
from topics.hustle import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, BRAY, FOX, M, B, h, s, silent, card)  # noqa: F401
FOLDER = "Is Hustle Culture a Scam"
ERA = "modern"
LANDSCAPE = False
GAP = 0.25
TAIL = 1.0
LTX_WH = (512, 896)
V = "Vertical portrait composition, the subject filling the tall frame. "
SHOTS = [
    # HOOK. BRAYDEN: "It's four a.m. Right now, you're asleep. That's why you're broke."
    h("h1", B, "It's four a.m. Right now, you're asleep. That's why you're broke.",
      V + BRAY + "standing at dawn on an empty road, filming himself with a phone on a selfie stick, huge grin, a car key with a rental key-tag in "
      "his other hand; behind him a spotless red sports car, a soaking-wet angry white swan glaring at him from the road, and " + FOX +
      " sitting on a low wall far behind, watching.",
      "He talks excitedly into the phone on the selfie stick, grinning and gesturing.", sfx="early morning empty road, birds, a swan hissing"),
    # MAYA: "Brayden has already had a cold shower, a hot shower, and an argument with a swan."  -- the swan goes for him
    silent("h2", V + "On an empty road at dawn beside a red sports car, a soaking-wet angry white swan rears up with its wings spread wide at the "
           "man from the reference, who leans back holding a car key on a rental key-tag, grinning nervously." + ONE, 0, refs=["brayden"],
           eng="ltx", sfx="a swan hissing and flapping, early morning road",
           motion="The wet swan spreads its wings wide, hisses and flaps angrily; the man leans back and raises his hands. Static camera."),
    # BRAYDEN: "Four a.m., awake. Four oh five, ice bath. Four thirty, I read one page of a book about reading. Five, I tell the mirror it's a winner."
    h("h3", B, "Four a.m., awake. Four oh five, ice bath. Four thirty, I read one page of a book about reading. Five, I tell the mirror it's a winner.",
      V + BRAY + "in a bright bathroom with a mirror and a sink behind him, talking fast to camera, proudly counting on his fingers.",
      "He talks very fast and proudly to camera, counting on his fingers.", sfx="small bathroom, a dripping tap"),
    # His reflection quietly packs a suitcase and leaves
    silent("h4", V + "A tall bathroom mirror: the man from the reference stands in front of it pointing proudly at his reflection, but the reflection "
           "in the mirror holds a small suitcase and looks unsure." + ONE, 3.0, refs=["brayden"], eng="ltx", sfx="bathroom, a door closing softly",
           motion="The man standing in front of the mirror stays completely still, frozen, pointing at the mirror; he does not move at all. Only the "
                  "reflection inside the mirror moves: it turns away, lifts its small suitcase and walks off sideways inside the mirror, disappearing "
                  "past the mirror's edge, leaving the mirror showing an empty bathroom. Static camera."),
    # MAYA: "Six, he films his morning routine. Seven, he edits ... Nine, he posts ..."  (+ a beat)
    s("h5", M, "Six, he films his morning routine. Seven, he edits his morning routine. Nine, he posts his morning routine.",
      V + BRAY + "framed by a big glowing ring light, filming himself on a phone on a tripod, a laptop with a video editor open on the desk beside "
      "him, proud." + ONE, refs=["brayden"], mv="in", hold=1.0, sfx="quiet room, a ring light humming"),
    # MAYA: "So the main thing his morning produces is a video of his morning."
    s("h6", M, "So the main thing his morning produces is a video of his morning.",
      V + "The man from the reference slumped sideways on a sofa at nine in the morning, completely exhausted, eyes half-closed, dark rings under his "
      "eyes, hair messy, while on a big television on the wall above him a video of himself grins and gives a thumbs up." + ONE, refs=["brayden"], mv="in", hold=0.8, sfx="quiet living room, a television murmuring"),
    # CTA. MAYA: "But here's the real question. Is working harder actually making you richer, or just more tired?"
    s("h7", M, "But here's the real question. Is working harder actually making you richer, or just more tired?",
      V + "Late at night, dark street lit by one orange streetlamp: the man from the reference fast asleep in the driver's seat of his red sports car, "
      "eyes closed, head tilted back, mouth open; a parking ticket under the windscreen wiper, a rental key-tag hanging from the ignition, a wet "
      "swan glaring at him through the side window." + ONE, refs=["brayden"], mv="in", hold=0.6,
      sfx="quiet street at night"),
    # MAYA: "Watch the full video on our channel."  -- end card
    card("h8", "Watch the full video on our channel.", "SCAM?", "IS HUSTLE CULTURE A", bg="#3C5A50", hold=1.3),
]
SHOTS[1]["text"] = "Brayden has already had a cold shower, a hot shower, and an argument with a swan."   # Maya speaks over the swan clip
SHOTS[7]["card"]["size"] = 210                     # vertical end card: "SCAM?" must fit inside the 1080-wide frame
