"""Insurance Reel, native 9:16 intro (2026-11-27), same format as topics/subvert.py, with Maya on camera to open and close.
One storyline: Ryan's flood claim. Recorded lines copied from projects/short-insurance/audio; one new Maya CTA line (cta).
Approved script: VIDEOS/How Insurance Actually Works/REEL SCRIPT.md."""
from topics.insurance import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, RYAN_FULL, FOX, M, R, G, h, s, silent, card,
                              RY, ger, MAYA, KF_FLOOD, KF_RY_CHAIR, KF_GER_PEN, KF_GER_WRITE, KF_GER_SMILE, SFX_K, SFX_F, SFX_G)  # noqa: F401
FOLDER = "How Insurance Actually Works"
ERA = "modern"
LANDSCAPE = False
GAP = 0.25
TAIL = 1.0
LTX_WH = (512, 896)
V = "Vertical portrait composition, the subject filling the tall frame. "
STUDIO = "in a cosy, stylish presenter's studio with a warm desk lamp, a bookshelf, a potted plant and a big window behind her, "
MV_MAYA = ("She speaks to camera naturally and warmly, with small expressive head movements and hand gestures. Static camera. "
           "Exactly one person; same face and clothes.")


def maya(id_, text, expr, hold=0.0):
    return dict(id=id_, spk=M, eng="h3", text=text, kf=V + MAYA + STUDIO + expr + ONE, refs=["maya", "maya_face"], onscreen=True,
                mv=MV_MAYA, hold=hold, sfx="a quiet studio, soft room tone")


SHOTS = [
    # HOOK: Maya on camera, the fox asleep in a recycling box outside her window
    maya("c01", "For eleven years, Ryan has paid a stranger forty-five dollars a month, in case something terrible happens to him.",
         "close-up, waist-up, her face large in frame, sitting at a desk facing camera with a knowing half-smile, telling a story; through the window behind her " + FOX +
         " is asleep, curled up in a blue recycling box."),
    s("c02", M, "Nothing has.", V + RYAN + "close-up at his kitchen table in the morning, staring at his phone, sulking, completely unharmed, his mug "
      "of tea perfectly fine." + ONE, refs=RY, hold=0.4, sfx=SFX_K),
    h("c03", R, "Eleven years. Not even a small flood.", V + RYAN + "close-up at his kitchen table in the morning, staring at his phone, genuinely "
      "aggrieved.", "He speaks quietly, genuinely aggrieved, shaking his head slightly.", sfx=SFX_K),
    # THE FLOOD (the fox paddles past)
    dict(silent("k01", V + KF_FLOOD + "outside the glass patio door behind him " + FOX + " floats past in a tiny inflatable swim ring." + ONE, 0,
                refs=RY, eng="ltx", sfx=SFX_F, motion="The sock drifts slowly across the water; outside the glass door the small fox paddles "
                "past in its inflatable ring. The man stands still on the chair. Static camera."),
         text="Which brings us back to Ryan. Last Tuesday, his washing machine flooded the kitchen."),
    s("k02", R, "Finally.", V + RYAN + "close-up, standing on a chair in a flooded kitchen, a small guilty smile, almost happy." + ONE, refs=RY, hold=0.4, sfx=SFX_F),
    # THE CALL
    h("k04", G, "Ryan. Nobody's in trouble. I've moved to Claims.", V + ger("warm reassuring smile."), "He speaks softly and reassuringly, smiling.", sfx=SFX_G),
    s("k05", G, "Let's take this one step at a time. Did the water come from above, or below?", V + KF_GER_PEN, refs=["gerald"], sfx=SFX_G),
    s("k06", R, "From the washing machine.", V + KF_RY_CHAIR, refs=RY, sfx=SFX_F),
    h("k07", G, "So... sideways.", V + ger("thoughtful, gazing slightly upward."), "He thinks for a moment, then speaks slowly and thoughtfully.", sfx=SFX_G),
    s("k12", G, "And was the washing machine on, at the time?", V + KF_GER_WRITE, refs=["gerald"], sfx="quiet office, a pen scratching slowly"),
    s("k13", R, "It's a washing machine.", V + RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, patient and confused." + ONE,
      refs=RY, sfx=SFX_F),
    s("k14", G, "So you were aware it contained water.", V + ger("nodding slowly, very understanding.") + ONE, refs=["gerald"], sfx=SFX_G),
    s("k15", R, "...That's what it's for.", V + RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, small, defeated." + ONE,
      refs=RY, sfx=SFX_F),
    # PAYOFF
    s("k23", G, "Good news. Your claim's approved. The damage is two hundred and forty dollars. Your deductible is two hundred and fifty.",
      V + KF_GER_SMILE, refs=["gerald"], hold=0.5, sfx=SFX_G),
    s("k24", G, "So you don't owe us anything.", V + ger("beaming kindly, palms open.") + ONE, refs=["gerald"], sfx=SFX_G),
    s("k25", R, "...Thank you?", V + RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, confused gratitude." + ONE, refs=RY, sfx=SFX_F),
    s("k26", G, "And because you made a claim, your price will go up next year.", V + ger("his warmest smile yet, leaning very slightly forward.") + ONE,
      refs=["gerald"], sfx=SFX_G),
    silent("k27", V + RYAN_FULL + "standing on a chair in his flooded kitchen, water up to his shins, phone lowered, staring into space; a single sock "
           "drifts past." + ONE, 2.0, refs=RY, mv="out", sfx="a flooded kitchen, slow dripping, silence"),
    # CTA: Maya on camera, then the end card
    maya("cta", "So how does insurance actually work? Watch the full video on our channel.", "close-up, waist-up, her face large in frame, leaning towards camera with a warm, inviting smile."),
    card("end", "", "INSURANCE?", "HOW DOES IT ACTUALLY WORK", bg="#2E4A62", dur=1.8, size=210),
]
