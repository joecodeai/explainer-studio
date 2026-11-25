"""Reel / Short for 'Why Is Everything a Subscription Now?': the script's REEL section (9:16 summary edit, about 60-75 s).
Same cast, voices, facts and keyframe prompts as topics/subscription.py (prompts reused verbatim so the images match).
Two NEW Maya lines from the script: "And it can only be cancelled in person. On a Saturday." and the Iliad Flow line (r11)."""
from topics.subscription import (STYLE, ENV_STYLE, LOOK, VOICE_REF, H3_REF_KF, TEMPO, CHARS as _CHARS, ONE, FOX, RY, M, R, B, G, I,
                                 h, s, silent, card, KF_CAR, KF_XRAY, KF_RADIATOR, MV_RADIATOR, KF_LOT, KF_BRAY_SEAT, KF_CAFE, KF_WAIT,
                                 KF_SHADOW_GER, KF_GER_LISTEN, KF_INPERSON, MV_INPERSON, KF_RAIN, KF_TROY, KF_RY_RADIATOR, KF_FOX_END,
                                 MV_FOX_END, SFX_LOT, SFX_RET)
FOLDER = "Why Is Everything a Subscription Now"
ERA = "modern"
GAP = 0.2
LTX_WH = (512, 896)
CHARS = {k: _CHARS[k] for k in ("brayden", "gerald")}       # Future Ryan is not in the reel
SHOTS = [
 s("r01", M, "In 2022, BMW started offering British drivers heated front seats. For fifteen pounds a month.", KF_CAR, refs=RY, sfx=SFX_LOT),
 s("r02", M, "Customers weren't paying for heat. They were paying for permission.", KF_XRAY, env=True,
   sfx="quiet car interior, a faint electrical hum"),
 h("r03", R, "It's right there. It's like sitting on a radiator that isn't speaking to me.", KF_RADIATOR, MV_RADIATOR,
   sfx="inside a cold parked car, winter wind outside"),
 s("r04", M, "In 2023, BMW dropped the idea. Not many people signed up.", KF_LOT, env=True, mv="out", hold=0.5, sfx=SFX_LOT),
 s("r05", M, "Not many.", "A frosty empty car park at dawn with just one lonely plain grey car parked in the middle.", env=True, mv="in", sfx=SFX_LOT),
 silent("r06", KF_BRAY_SEAT, 1.0, refs=["brayden"], mv="in", sfx="a car heater fan humming, a contented sigh"),
 card("r07", "I'm still paying for Weekend Plus.", "£14.99", "WEEKEND PLUS · MONTHLY", spk=R, size=250, sfx="a phone buzzing inside a cold car"),
 s("r08", M, "He works Saturdays now. To pay for Weekend Plus.", KF_CAFE, refs=RY, sfx="small café on a Saturday, a coffee machine hissing"),
 s("r09", M, "And it can only be cancelled in person. On a Saturday.", KF_WAIT, env=True, mv="in", sfx="waiting room hum, a ticket machine beep"),
 s("r10", I, "Fake your death.", KF_SHADOW_GER, refs=RY, sfx=SFX_RET),
 s("r11", R, "What if I died?", KF_GER_LISTEN, refs=["gerald"], mv="out", sfx=SFX_RET),
 h("r12", G, "Then we'd need you to come in. In person.", KF_INPERSON, MV_INPERSON, hold=1.0, sfx=SFX_RET),
 silent("r13", KF_RAIN, 1.0, refs=RY, mv="out", sfx="rainy city street on a Monday morning, traffic, a bin lorry"),
 card("r14", "The FTC said that inside Amazon, cancelling Prime was known as the Iliad Flow.", "REAL", "FTC v. AMAZON · 2023", bg="#5A3C3C",
      sfx="rain on a city street, muffled"),
 s("r15", M, "The Iliad is a poem about a war that lasts ten years. Somebody chose that name. For the way out.", KF_TROY, env=True, mv="out",
   sfx="wind over an empty plain at dusk, a distant campfire crackle"),
 s("r16", G, "We noticed you'd left, so we've signed you up for Weekend Lite. The first month's completely free.", KF_RY_RADIATOR, refs=RY,
   mv="in", sfx="an old radiator ticking, a phone call on speaker, quiet kitchen"),
 silent("r17", KF_FOX_END, 2.0, env=True, eng="ltx", sfx="a single soft heater click, a quiet car interior, faint winter wind outside",
        motion=MV_FOX_END),
 card("r18", "", "WATCH", "FULL VIDEO ON YOUTUBE", dur=1.5, size=220, sfx="quiet car interior, faint winter wind"),
]
THUMB = dict(text="£15 A MONTH|FOR MY OWN SEAT?", refs=RY, pos="bottom",
             kf="Vertical: the young man from the reference (thick curly dark brown hair, burnt-orange open hoodie) shivering in the driver's "
                "seat of a small plain grey car on a frosty morning, the seat glowing warm orange beneath him with one tiny gold padlock on "
                "it, gloves on, breath fogging, big worried eyes; " + FOX + " curled up asleep on the warm bonnet. Exactly one person.")
TAIL = 1.0
