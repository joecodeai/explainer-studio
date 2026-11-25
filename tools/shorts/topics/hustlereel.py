"""Reel / Short for 'Is Hustle Culture a Scam?': the best moments as one story, native 9:16, about 75 s. Same cast, voices and facts as topics/hustle.py."""
from topics.hustle import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, BRAY, GER, GER_ROOM, RY_ROOM, FOX,
                           M, R, B, G, I, h, s, silent, card)
FOLDER = "Is Hustle Culture a Scam"
ERA = "modern"
GAP = 0.2
LTX_WH = (512, 896)
SHOTS = [
 h("r01", B, "Good morning. It's four a.m. Right now, you're asleep. That's why you're broke. I've already had a cold shower, a hot shower, and an argument with a swan.",
   BRAY + "standing at dawn beside a spotless red sports car, filming himself with a phone on a selfie stick, huge grin; behind him a soaking-wet "
   "angry white swan glares at him; " + FOX + " sits on a low wall far behind.",
   "He talks excitedly into the phone, grinning; the wet swan behind him flaps angrily.", sfx="early morning road, birds, a swan hissing"),
 s("r02", M, "Somewhere right now, a man is telling you to wake up at four in the morning so you can be rich like him.",
   BRAY + "grinning straight into a phone camera very close, one finger raised." + ONE, refs=["brayden"]),
 dict(id="r03", spk=M, eng="ltx", text="He'll even tell you how he made his money. It was selling you this video.", refs=["brayden"], hold=0.5,
      kf=BRAY + "sitting at a laptop showing a simple rising bar chart, plain golden coins raining down from the ceiling around him, arms spread in delight. He appears only once." + ONE,
      mv="Golden coins rain down onto the desk and floor, the man laughs with his arms spread. Static camera."),
 h("r04", R, "I'm still watching.", RYAN + "sitting on a sofa at night, face lit by the glow of his phone, guilty expression.",
   "He looks up from his phone, guilty, speaks very quietly.", hold=0.5, sfx="quiet flat at night"),
 h("r05", G, "Put the weekend down, Ryan. Slowly. Nobody has to get hurt.", GER + GER_ROOM.replace("warm gentle smile", "very calm, leaning slightly forward"),
   "He leans in slightly and speaks very softly and slowly, one hand raised in a calming gesture."),
 silent("r06", "Extreme close-up, top-down view of a wooden table surface: only two hands are visible, entering from the bottom and top edges of the "
        "frame; a young hand in an orange hoodie sleeve pushes a small glowing sun-shaped object towards an older hand in a beige cardigan sleeve. "
        "No faces, no bodies. Exactly two hands in total: one from the bottom, one from the top.", 2.5, mv="in", sfx="a tiny sad chime",
        motion="The young hand slides the glowing sun across the table; the cardigan hand takes it and slips it into a pocket. Static camera."),
 h("r07", G, "Good news. We've moved weekends to a subscription model. Weekend Plus adds Sunday, but the Sunday evening dread is billed separately.",
   GER + "sitting in a small softly lit office, brightly holding up a laminated card showing three pastel price tiers decorated with little clouds.",
   "He holds up the card cheerfully and points to a tier, delighted."),
 h("r08", R, "How do I cancel?", RYAN + RY_ROOM + "barely holding it together.", "He asks in a small, defeated voice."),
 h("r09", G, "Cancellations are done in person. On a Saturday.", GER + GER_ROOM.replace("warm gentle smile", "his warmest smile yet"),
   "He smiles his warmest smile and speaks softly.", hold=0.8),
 card("r10", "The average side hustle earns eight hundred and eighty-five dollars a month. The median earns two hundred. The average is a liar standing next to a millionaire.",
      "$885 vs $200", "AVERAGE vs MEDIAN SIDE HUSTLE", sfx="one sad trombone note"),
 s("r11", B, "Kidneys. Two of you, doing the same job. That's a redundancy situation.",
   "Two identical cartoon kidney characters in lanyards at a tiny boardroom table; one is standing holding a small cardboard box of belongings.", env=True, mv="in"),
 s("r12", M, "He fired a kidney.", "An empty office chair at a tiny boardroom table with a lanyard hanging on its back.", env=True, mv="in", hold=0.6),
 s("r13", M, "Oh, and his four a.m. sunrise videos? Filmed at four in the afternoon. The sunrise is a lamp.",
   "A desk lamp with an orange sweet wrapper taped over it, glowing, next to closed blinds with bright afternoon daylight leaking round them.", env=True, mv="out"),
 h("r14", B, "Still counts.", BRAY + "standing next to the desk lamp, not embarrassed at all, giving two thumbs up to camera.", "He beams and gives two thumbs up."),
 s("r15", M, "The full video is on our channel.", "Real 4 a.m., dark and quiet: " + FOX + " wearing a tiny business suit sits on the bonnet of a red "
   "sports car eating a croissant, typing on a tiny laptop with a glowing green dot.", env=True, mv="in", sfx="silent night street, one alarm clock beep"),
]
THUMB = dict(text="RICH BY|4AM?", refs=["brayden"], pos="bottom",
             kf="Vertical: the man from the reference grinning with two huge thumbs up in front of a shiny red sports car at sunrise; a rental "
                "key-tag dangles from the car key in his hand; " + FOX + " sits on the car roof behind him looking unimpressed. Exactly one person.")
TAIL = 1.0
