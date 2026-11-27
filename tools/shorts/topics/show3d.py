"""SHARED 3D LOOK (locked 2026-11-27): stylised 3D feature-film style (owner picked style option B) with Maya = 3D option 1.
Every new topic imports its style, cast, sets and helpers from here so characters, backgrounds, lighting and colour stay identical.
References live in library/show_refs3d/ (made by tools/cast3d.py). build.py adds a set plate / the fox reference automatically when a
shot's keyframe text uses that set or the fox (SET_REFS)."""
from topics.hustle import VOICE_REF, H3_REF_KF, TEMPO, h, s, silent, M, R, B, G, I  # noqa: F401
from topics.subscription import card  # noqa: F401

R3 = "library/show_refs3d/"
REFS3D = {"maya": R3 + "maya.png", "maya_face": R3 + "maya_face.png", "ryan": R3 + "ryan.png", "ryan_face": R3 + "ryan_face.png",
          "brayden": R3 + "brayden.png", "gerald": R3 + "gerald.png", "fox": R3 + "fox.png",
          "set_studio": R3 + "set_studio.png", "set_office": R3 + "set_office.png", "set_kitchen": R3 + "set_kitchen.png",
          "set_flat": R3 + "set_flat.png", "set_street": R3 + "set_street.png"}
CHARS = {}                     # no per-project t2i refs: the cast is fixed in REFS3D

ANATOMY = ("Correct anatomy: exactly five fingers on each hand, natural proportions, symmetrical eyes, hands resting on or holding objects "
           "without merging into them, bodies sitting on chairs and standing on floors with solid contact and soft contact shadows, nothing "
           "intersecting furniture.")   # QC_CHECKLIST sections 1, 3, 7 (PREVENT)
PALETTE = "Colour palette: warm cream, honey wood, soft teal, coin gold, deep navy and soft coral, with natural skin tones."
LIGHT = ("Lighting: bright soft key light from the upper left, warm fill, gentle warm rim light, soft global illumination, soft contact shadows.")
STYLE = ("High-quality stylised 3D animated feature-film render like a modern Pixar film: appealing stylised characters with big expressive eyes "
         "and soft rounded features, smooth clean materials, subtle depth of field, clean uncluttered sets, a bright and inviting image. "
         + LIGHT + " " + PALETTE + " The whole image, characters and background alike, is this 3D animated-film render. "
         "Clean bare skin and hands with no marks, no paint, no stickers, no green spots. " + ANATOMY + " Absolutely no text, letters, numbers, "
         "logos or badges anywhere.")
ENV_STYLE = ("High-quality stylised 3D animated feature-film render like a modern Pixar film: smooth clean materials, subtle depth of field, clean "
             "uncluttered set, a bright and inviting image. " + LIGHT + " " + PALETTE + " Show only what the description names. There are NO people "
             "of any kind. Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Stylised 3D animated feature film like a modern Pixar film, smooth expressive character animation with weight and follow-through, soft "
        "cinematic lighting, characters keep their exact design, face, skin tone, hair, clothes and accessories, no morphing, no flicker, no camera "
        "shake, no sudden zoom or cut inside the shot. Correct anatomy: five fingers on each hand, hands and bodies never pass through furniture, "
        "feet stay planted on the floor, objects stay in the hand that holds them and never appear or vanish, steady consistent lighting and shadows. "
        "The mouth moves only while speaking and rests closed in pauses.")
ONE = " Exactly one person."

# ---- cast (each line names the reference it relies on)
MAYA = ("The young woman from the reference, in the same stylised 3D animated-film look: long voluminous wavy dark brown hair, gold hoop earrings, "
        "fair light skin with a soft warm peach glow, big warm hazel-brown eyes with long lashes, softly arched eyebrows, rosy cheeks, bright "
        "friendly smile, olive-green overshirt over a cream top, waist-up, ")
RYAN = ("The young man from the reference, in the same stylised 3D animated-film look: thick curly dark brown hair, burnt-orange open hoodie over "
        "a white t-shirt, black crossbody strap, waist-up, ")
RYAN_FULL = RYAN.replace("waist-up, ", "full body, ")
BRAY = ("The man from the reference, in the same stylised 3D animated-film look (slicked-back blond hair, tight black t-shirt, gold watch, big "
        "confident grin), waist-up, ")
BRAY_FULL = BRAY.replace("waist-up, ", "full body, ")
GER = ("The older man from the reference, in the same stylised 3D animated-film look (grey side-parted hair, round glasses, beige cardigan, light "
       "blue shirt, navy tie, lanyard), waist-up, ")
FOX = "the small orange fox from the reference"
RY = ["ryan", "ryan_face"]
MY = ["maya", "maya_face"]

# ---- recurring sets (SET_REFS: when a keyframe uses one of these phrases, build.py adds that set plate as a reference)
STUDIO = ("in her bright cosy presenter's studio (the set from the reference): honey-wood desk, warm desk lamp, bookshelf, potted plant and a big "
          "sunny window full of bright daylight behind her, daytime, ")
GER_ROOM = ("sitting in his small softly lit office (the set from the reference): a box of tissues on a side table, a framed child's drawing "
            "of a smiling sun on the wall, notepad on his knee, facing camera, ")
KITCHEN = "in his small bright kitchen (the set from the reference), "
FLAT = "in his bare white empty flat under one bare bulb (the set from the reference), "
STREET = ("on a city street at night by a cash machine set into a brick wall (the set from the reference), lit by a warm streetlight with "
          "a soft blue night ambient, ")
SET_REFS = {STUDIO: "set_studio", GER_ROOM: "set_office", KITCHEN: "set_kitchen", FLAT: "set_flat", STREET: "set_street", FOX: "fox"}


def ger(expr):
    return GER + GER_ROOM + expr


CLOSE = ("close-up portrait shot from the chest up, her head and shoulders filling most of the frame, the studio softly blurred behind her, "
         "sitting at her desk, ")


def maya(id_, text, expr, hold=0.0, mv=None):
    """Maya on camera in her studio (lip-sync)."""
    # framed close: H3 jumps from a wide to a close-up mid-clip when the face is small in frame (o01 / b19 lesson)
    return dict(id=id_, spk=M, eng="h3", text=text, kf=MAYA.replace("waist-up, ", CLOSE) + STUDIO + expr + ONE, refs=list(MY), onscreen=True, close=True, hold=hold,
                mv=mv or ("She speaks to camera naturally and warmly, with small expressive head movements and relaxed hand gestures. Static "
                          "camera. Exactly one person; same face, skin tone and clothes."), sfx="a quiet studio, soft room tone")
