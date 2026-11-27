"""3D LOOK CHECK (2026-11-27): eight ATM shots across every recurring set, built with the locked 3D look (topics/show3d.py),
to check that characters, sets, lighting and colour stay consistent and that no green specks survive. Audio reused from projects/short-atm."""
from topics.show3d import *  # noqa: F401,F403
from topics.show3d import MAYA, STUDIO, RYAN, RYAN_FULL, BRAY, FLAT, GER, GER_ROOM, KITCHEN, STREET, FOX, ONE, RY, MY, maya, ger, s, h, silent, M, R, B, G  # noqa: F401
FOLDER = "_LOOK TEST 3D"
ERA = "modern"
LANDSCAPE = True
GAP = 0.25
TAIL = 1.0

SHOTS = [
    maya("o01", "You put a piece of plastic into a wall. You type four numbers. And the wall gives you money.",
         "facing camera, warm, a hint of wonder, hands resting together."),
    s("o03", M, "The person in front of you is always checking their balance. Twice.",
      RYAN_FULL + STREET + "waiting patiently in the queue while " + FOX + " stands at the machine ahead of him reading a long paper receipt. "
      "Exactly one person and one fox.", refs=list(RY), sfx="a city street at night"),
    s("h10", R, "The first cash machine was radioactive.", RYAN + KITCHEN + "sitting at the small round table, mug halfway to his mouth, frozen, "
      "wide-eyed." + ONE, refs=list(RY), sfx="quiet kitchen"),
    h("j06", G, "Ryan. Nobody's in trouble. I've moved to Authorisations.", ger("holding a small white paper plane in one hand, warm smile."),
      "He speaks softly and reassuringly, smiling.", refs=["gerald"], sfx="quiet office"),
    h("b02", B, "Bro. I own an ATM now. Passive income.", BRAY + FLAT + "standing proudly next to a brand-new cash machine, delighted.",
      "He gestures proudly at the machine and speaks loudly, thrilled.", refs=["brayden"], sfx="empty room echo"),
    s("b13", B, "So I'm the bank now.", BRAY + FLAT + "leaning on his cash machine, confident, arms crossed." + ONE, refs=["brayden"], sfx="empty room echo"),
    maya("b18", "He doesn't. He loses a dollar sixty-four.", "an unimpressed look with one eyebrow raised, arms folded."),
    s("v09", M, "There isn't.", "Inside a cash machine, a cosy cutaway: " + FOX + " wearing a tiny green banker's visor, counting banknotes by the "
      "light of a small desk lamp, licking its thumb.", refs=[], sfx="a soft mechanical hum"),
]
