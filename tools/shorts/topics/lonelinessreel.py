"""Reel / Short for 'Is modern society making us more lonely?': the whole argument in ~75 s, native 9:16. Same facts and sources as topics/loneliness.py."""
from topics.loneliness import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
FOLDER = "Is Modern Society Making Us More Lonely"
ERA = "modern"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="j01", spk=M, eng="still", mv="in", refs=["guy"], sfx="quiet flat at night, a fridge humming, a pigeon cooing softly",
      text="We have more ways to talk to each other than ever before. And yet Britain and Japan both decided they needed a minister for loneliness.",
      kf="The man from the reference sitting alone on a sofa in a small flat at night, completely surrounded by a huge pile of silent "
         "communication devices: a smartphone, a laptop, a tablet, an old rotary telephone, a walkie-talkie and a fax machine, while a grey "
         "carrier pigeon waits patiently on the windowsill holding a small blank envelope. He stares straight ahead with a blank "
         "expression. Exactly one person.",
      mv_ltx="The man slowly turns his head to look at the pigeon; the pigeon tilts its head back at him. " + P1),
 dict(id="j02", spk=M, eng="card", card=dict(big="1 IN 6", small="PEOPLE AFFECTED BY LONELINESS (WHO)", bg="#2E3A5C", accent="#C9B6E4"),
      sfx="busy international street, many voices",
      text="The World Health Organization says one in six people worldwide is affected by loneliness. America's Surgeon General compared its risk of early death to smoking up to fifteen cigarettes a day."),
 dict(id="j03", spk=M, eng="card", card=dict(big="60 → 20", small="MINUTES A DAY WITH FRIENDS (US, 2003–2020)", bg="#4A3C5A", accent="#F2B95A"),
      sfx="quiet cafe, a few cups clinking",
      text="Americans went from about an hour a day with friends in 2003 to twenty minutes in 2020. And far more of us live alone."),
 dict(id="j04", spk=M, eng="still", mv="in", refs=["teen"], sfx="park, birds, distant traffic",
      text="Add self-checkouts, food left at the door and phones in every hand, and modern life looks guilty.",
      kf="Four teenagers, including the girl from the reference, sitting together on a park bench, each staring down at their own glowing "
         "phone, none of them looking at each other, a frisbee lying forgotten on the grass. Exactly four people."),
 dict(id="j05", spk=M, eng="still", mv="out", sfx="dusty road at sunset, crickets",
      text="But it's murkier than that. Studies tracking loneliness over decades find small rises at most. And people in poorer countries report about twice the loneliness of people in rich ones.",
      kf="A simple split scene: on the left, a tired farm worker walking home alone along a long dusty road at sunset; on the right, a "
         "bright modern apartment where a woman on a sofa laughs while video-calling friends on a laptop. Exactly two people."),
 dict(id="j06", spk=M, eng="still", mv="in", env=True, sfx="quiet kitchen, a fork on a plate",
      text="Even the phone debate is unsettled. One big Oxford study found screen use was linked to teen wellbeing about as much as eating potatoes.",
      kf="A single plain baked potato on a white plate, a pair of round glasses and a smartphone, all lined up neatly side by side on a "
         "table under a bright spotlight like suspects in a police line-up. No people."),
 dict(id="j07", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="Nobody's writing a bestseller about potatoes.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, holding a baked potato on a fork, looking at camera with a flat expression. Exactly one person.",
      mv="The young man speaks flatly to camera, then looks down at the potato thoughtfully. Static camera, waist-up. Exactly one person; "
         "he keeps the same face, hair and hoodie."),
 dict(id="j08", spk=M, eng="still", mv="in", sfx="park, birds, two old men laughing",
      text="What nobody disputes is that connection matters. Harvard's study of adult life, running since 1938, found good relationships keep people happier and healthier.",
      kf="Two elderly men in cardigans sitting side by side on a park bench laughing together, feeding pigeons, autumn trees behind them. "
         "Exactly two people."),
 dict(id="j09", spk=M, eng="ltx", refs=["guy", "gran"],
      text="So modern life doesn't force us to be lonely. It just no longer forces us not to be. The full story is on our channel.",
      kf="The young man from the first reference standing in an apartment corridor at his neighbour's open door, where the old woman from "
         "the second reference stands smiling and holding out a plate of biscuits. Exactly two people.",
      mv="The old woman offers the plate; the young man takes a biscuit and smiles, and she waves him inside. " + P1),
]
THUMB = dict(text="LONELIER|THAN EVER?", refs=["guy"],
             kf="Vertical: the man from the reference sitting alone on a sofa at night, buried up to his chest in a huge pile of glowing "
                "phones, laptops and old telephones, looking at camera with a sad, puzzled face, while a carrier pigeon sits on his head. "
                "Deep navy background with warm amber light. Exactly one person.")
TAIL = 2.4
