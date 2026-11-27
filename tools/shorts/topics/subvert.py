"""Subscription Reel, native 9:16 intro (2026-11-27), same format as topics/hustlevert.py: one storyline (Ryan tries to cancel
Weekend Plus), recorded lines copied from projects/short-subscription/audio, one new Maya call to action (v1), fox payoff on the
heated seat. Script for owner approval: VIDEOS/Why Is Everything a Subscription Now/REEL SCRIPT.md."""
from topics.subscription import (STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, FOX, M, R, G, h, s, silent, card,
                                 RY, ger, ry_ret, KF_CAR, KF_RADIATOR, MV_RADIATOR, KF_CAFE, KF_GER_LISTEN, KF_INPERSON, MV_INPERSON,
                                 KF_FOX_END, MV_FOX_END, SFX_LOT, SFX_RET)  # noqa: F401
FOLDER = "Why Is Everything a Subscription Now"
ERA = "modern"
LANDSCAPE = False
GAP = 0.25
TAIL = 1.0
LTX_WH = (512, 896)
V = "Vertical portrait composition, the subject filling the tall frame. "
SHOTS = [
    # HOOK. MAYA: BMW heated seats for £15 a month -- Ryan freezing; the fox curled up on the warm bonnet
    s("c01", M, "In 2022, BMW started offering British drivers heated front seats. For fifteen pounds a month.", V + KF_CAR, refs=RY, sfx=SFX_LOT),
    # RYAN (lip-sync): "It's right there. It's like sitting on a radiator that isn't speaking to me."
    h("c04", R, "It's right there. It's like sitting on a radiator that isn't speaking to me.", V + KF_RADIATOR, MV_RADIATOR, hold=0.6,
      sfx="inside a cold parked car, winter wind outside"),
    # RYAN: "I'm still paying for Weekend Plus."  -- his phone's subscription list
    s("c09", R, "I'm still paying for Weekend Plus.",
      V + "Close-up inside a cold parked car: one hand in a black winter glove, with an orange hoodie cuff, holds a phone whose screen shows a "
      "simple list of coloured rows, small app-icon blobs and grey bars. Only that one hand is visible.", env=True, mv="in", sfx="inside a cold parked car, wind"),
    # MAYA: "He hasn't had a weekend since he signed up. He works Saturdays now. To pay for Weekend Plus."
    s("c10", M, "He hasn't had a weekend since he signed up. He works Saturdays now. To pay for Weekend Plus.",
      V + KF_CAFE.replace("tired, drying", "tired, lips together, drying"), refs=RY, hold=0.6, sfx="small café on a Saturday, a coffee machine hissing"),
    # MAYA: "So Ryan decided to cancel everything. He started with Weekend Plus, which can only be cancelled in person, on a Saturday."
    s("r01", M, "So Ryan decided to cancel everything. He started with Weekend Plus, which can only be cancelled in person, on a Saturday.",
      V + RYAN + "sitting at his kitchen table on a Friday night with a pen and a long list, looking determined." + ONE, refs=RY, sfx="quiet kitchen at night"),
    # GERALD (lip-sync): "Ryan. Come in. Nobody's in trouble. I've moved to Retention."
    h("r04", G, "Ryan. Come in. Nobody's in trouble. I've moved to Retention.",
      V + ger("standing in the open doorway of a small softly lit office, gently beckoning, warm smile."), "He gently beckons and speaks calmly and softly, smiling.", sfx=SFX_RET),
    # RYAN: "I'd like to cancel Weekend Plus, please."  -- over Gerald, pen poised
    s("r05", R, "I'd like to cancel Weekend Plus, please.", V + ger("nodding kindly, pen poised over his notepad.") + ONE, refs=["gerald"], sfx=SFX_RET),
    # GERALD: "What if we paused it? You'd keep paying, but the weekends would stop."  -- PAUSE card
    card("r10", "What if we paused it? You'd keep paying, but the weekends would stop.", "PAUSE", "YOUR WEEKEND", spk=G, bg="#3C5A50",
         size=210, sfx="a laminated card sliding on a table, quiet office"),
    # RYAN: "That's what's happening now."  -- over Gerald listening
    s("r11", R, "That's what's happening now.", V + KF_GER_LISTEN, refs=["gerald"], hold=0.5, sfx=SFX_RET),
    # RYAN: "What if I died?"  -- Ryan, quietly desperate
    s("r17", R, "What if I died?", V + RYAN + "close-up, seated in a chair in a softly lit office opposite a desk with a box of tissues, leaning "
      "forward with his hands clasped together, quietly desperate, eyebrows raised." + ONE, refs=RY, sfx=SFX_RET),
    # GERALD (lip-sync): "Then we'd need you to come in. In person."
    h("r18", G, "Then we'd need you to come in. In person.", V + KF_INPERSON, MV_INPERSON, hold=1.2, sfx=SFX_RET),
    # CTA. MAYA (new) over the fox curling up on the glowing heated seat -- for free
    silent("v1", V + KF_FOX_END, 0, env=True, eng="ltx", sfx="a single soft heater click, a quiet car interior, faint winter wind outside", motion=MV_FOX_END),
    card("v2", "Watch the full video on our channel.", "NOW?", "WHY IS EVERYTHING A SUBSCRIPTION", bg="#3C5A50", size=210, hold=1.3),
]
SHOTS[-2]["text"] = "So why is everything a subscription now?"
