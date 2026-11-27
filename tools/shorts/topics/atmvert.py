"""ATM Reel, native 9:16 intro (2026-11-27), same format as topics/insvert.py, with Maya on camera to open and close.
One storyline: Brayden's passive-income ATM. Recorded lines copied from projects/short-atm/audio; two new Maya lines (hk, cta).
Approved script: VIDEOS/How Do ATMs Actually Work/REEL SCRIPT.md."""
from topics.atm import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, BRAY, FOX, M, B, h, s, silent, card,  # noqa: F401
                        MAYA, NO_TEXT, FLAT, SFX_FL)
FOLDER = "How Do ATMs Actually Work"
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
    # HOOK: Maya on camera; the fox outside her window, peering at a tiny cash machine
    maya("hk", "You can buy your own ATM. Brayden did.",
         "close-up, waist-up, her face large in frame, sitting at a desk facing camera with a knowing half-smile, telling a story; through the window "
         "behind her " + FOX + " is peering curiously at a tiny cash machine on the pavement. Exactly one fox in the whole picture."),
    h("b02", B, "Bro. I own an ATM now. Passive income.", V + BRAY + FLAT + "standing proudly next to a brand-new cash machine, delighted.",
      "He gestures proudly at the machine and speaks loudly, thrilled.", sfx=SFX_FL),
    # THE PLAN
    s("b03", M, "He set the fee at nine ninety-nine.", V + "Close-up of a cash machine screen showing one big shiny golden price-tag icon." + NO_TEXT,
      env=True, sfx="a cash register ding"),
    s("b04", M, "He installed it in his flat.", V + "A completely empty white flat with one bare bulb hanging from the ceiling and a single cash machine "
      "glowing in the corner." + NO_TEXT, env=True, mv="out", hold=1.5, sfx="empty room, a bare bulb buzzing, silence"),
    s("b06", M, "Nobody came.", V + "The same empty white flat: the lonely cash machine in the corner, one cobweb on it." + NO_TEXT, env=True, hold=0.3,
      sfx=SFX_FL),
    # THE PROBLEM
    s("b12", M, "Then Brayden found out something about owning an ATM. It doesn't come with money. You have to fill it yourself.",
      V + BRAY + FLAT + "feeding a few of his own plain pale banknotes, one by one, into the open back of a cash machine. Clean simple shapes." + ONE,
      refs=["brayden"], sfx=SFX_FL),
    s("b13", B, "So I'm the bank now.", V + BRAY + FLAT + "leaning on his cash machine, confident, arms crossed." + ONE, refs=["brayden"], sfx=SFX_FL),
    s("b14", M, "The machine ran out by Wednesday. So he paid an armoured truck to bring his own money back to his own flat.",
      V + "An armoured truck squeezed into a narrow residential street; two guards carry one small metal cash box up the front steps while the blond "
      "man from the reference holds the door open. Exactly three people." + NO_TEXT, refs=["brayden"], mv="in",
      sfx="a heavy van door, footsteps on stairs"),
    # THE PAYOFF
    s("b15", M, "Then his rent was due, so he took his money out again.", V + BRAY + FLAT + "typing on the keypad of his own cash machine." + ONE,
      refs=["brayden"], sfx="key beeps, an empty room"),
    s("b16", M, "The machine charged him nine ninety-nine, which went to him. And his own bank charged him a dollar sixty-four for using an ATM that "
      "wasn't theirs.", V + BRAY + FLAT + "holding his cash in one hand and a receipt in the other, puzzled." + ONE + NO_TEXT, refs=["brayden"],
      sfx=SFX_FL),
    s("b17", B, "Every time I take my money out, I make ten bucks.", V + BRAY + FLAT + "counting three plain pale-green banknotes in his hands, beaming. "
      "Clean simple flat shapes." + ONE, refs=["brayden"], sfx=SFX_FL),
    maya("b18", "He doesn't. He loses a dollar sixty-four.", "close-up, waist-up, facing camera, her face large in frame, light warm-tan skin, an unimpressed look with one eyebrow raised, arms folded."),
    h("b19", B, "Bro, I'm vertically integrated.", V + BRAY + FLAT + "next to his cash machine, serene, one hand on his heart.",
      "He speaks calmly and serenely, completely sure of himself.", hold=0.8, sfx=SFX_FL),
    # CTA: Maya on camera, then the end card
    maya("cta", "So how do ATMs actually work? Watch the full video on our channel.",
         "close-up, waist-up, her face large in frame, leaning towards camera with a warm, inviting smile."),
    card("end", "", "ATMs?", "HOW DO THEY ACTUALLY WORK", bg="#2E4A62", dur=1.8, size=210),
]
