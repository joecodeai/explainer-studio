"""Reel / Short for 'Are poor people poor because of bad decisions?': the whole argument in ~75 s, native 9:16. Same facts and sources as topics/poverty.py."""
from topics.poverty import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
FOLDER = "Are Poor People Poor Because of Bad Decisions"
ERA = "modern"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="w01", spk=M, eng="still", mv="in", refs=["jo"], sfx="quiet city street, a cash machine beeping, a single coin clinking",
      text="Are poor people poor because they make bad decisions? Possibly. Although in America, a bank can charge you thirty-five dollars for not having enough money.",
      kf="The woman from the reference standing at a cash machine set into a brick wall, holding her open purse, while a small mechanical hand "
         "has reached out of the machine's card slot and is politely taking her last coin. She stares at the hand flatly. Exactly one person.",
      mv_ltx="The mechanical hand slowly lifts the coin out of her purse; the woman watches it go without moving. " + P1),
 dict(id="w02", spk=M, eng="card", card=dict(big="2%", small="IN POVERTY AFTER ALL THREE STEPS", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet library, a page turning",
      text="The case for decisions is real. Finish school, work full time, marry before kids. Of households that did all three, about two percent were poor."),
 dict(id="w03", spk=M, eng="still", mv="in", sfx="quiet nursery, a child chewing",
      text="But correlation isn't cause. In one marshmallow test, kids who'd just been let down by an adult waited three minutes. Kids whose adult kept a promise waited twelve.",
      kf="A small child calmly and happily eating a marshmallow at a little table, while in the doorway behind them an adult holds up an empty "
         "crayon box and shrugs apologetically. Exactly two people."),
 dict(id="w04", spk=M, eng="still", mv="in", refs=["farmer"], sfx="village courtyard, birds, a distant tractor",
      text="Scarcity also eats brainpower. Indian sugarcane farmers did worse on reasoning tests before harvest, when money was tight, than after it.",
      kf="The man from the reference sitting on a wooden bench outside his village house, frowning hard at a simple coloured-shape puzzle on a "
         "clipboard, while a small pile of borrowed cooking pots and a goat wait beside him. Exactly one person."),
 dict(id="w05", spk=M, eng="card", card=dict(big="391%", small="TYPICAL PAYDAY LOAN, AS A YEARLY RATE", bg="#5A3C3C", accent="#F2C14E"),
      sfx="small shop, a door chime, a till drawer",
      text="And being poor is expensive. A typical payday loan works out at almost four hundred percent a year. Good boots cost more up front. Cheap boots cost more in the end."),
 dict(id="w06", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="Money's cheaper if you've already got some.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, leaning on a kitchen counter with arms folded, looking at camera with a flat expression. "
         "Exactly one person.",
      mv="The young man speaks flatly to camera, arms folded, then gives a slow single nod. Static camera, waist-up. Exactly one person; he "
         "keeps the same face, hair and hoodie."),
 dict(id="w07", spk=M, eng="card", card=dict(big="+31%", small="ADULT EARNINGS, MOVED BEFORE AGE 13", bg="#2E4A62", accent="#F2A65A"),
      sfx="quiet leafy street, birds, a lawnmower far away",
      text="Place matters too. Kids whose families won a lottery to move somewhere less poor before age thirteen earned thirty-one percent more as young adults."),
 dict(id="w08", spk=M, eng="still", mv="in", env=True, sfx="park, wind in trees, a chess clock ticking",
      text="Choices matter. But they're made on a very uneven board. And when a poor person makes a mistake, it comes with a late fee.",
      kf="A big chessboard in a park where one side has a full set of shiny pieces and the other side has only a few small chipped pawns, "
         "the board itself tilted downhill towards the pawns. No people."),
 dict(id="w09", spk=M, eng="ltx", env=True,
      text="So the real question isn't whether poor people make bad decisions. Everyone does. It's why theirs cost so much more. Full video on our channel.",
      kf="A simple old balance scale on a plain warm sand background, one pan holding a single tiny coin and pressed all the way down, the "
         "other pan holding a big bag of gold coins floating high. No people.",
      mv="The scale wobbles gently, the heavy pan with the single coin sinks a little lower and the bag of gold rises. Static camera."),
]
THUMB = dict(text="BAD|DECISIONS?", refs=["jo"],
             kf="Vertical: the woman from the reference holding her open purse upside down with a shocked face, while a cash machine beside her "
                "has stuck out a small mechanical hand and is holding out its palm towards her, one coin falling into it. Bright terracotta "
                "background. Exactly one person.")
TAIL = 2.4
