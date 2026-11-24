"""Reel / Short for 'Is working 9-5 a trap?': the whole argument in ~75 s, native 9:16. Same facts and sources as topics/ninetofive.py."""
from topics.ninetofive import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
FOLDER = "Is Working 9 to 5 a Trap"            # VIDEOS/<FOLDER>/...
ERA = "modern"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="r01", spk=M, eng="still", mv="in", refs=["worker"], sfx="quiet office, a wall clock ticking, a keyboard",
      text="In 1930, a famous economist predicted we'd only need to work fifteen hours a week. Most of us have done that by Tuesday afternoon.",
      kf="The man from the reference slumped over his office desk behind a towering stack of paper folders that reaches the ceiling, while on "
         "the wall behind him a framed portrait of a cheerful 1930s gentleman with a neat moustache and a bow tie gives a big thumbs-up. "
         "Exactly one person at the desk."),
 dict(id="r02", spk=M, eng="card", card=dict(big="1926", small="FORD'S FIVE-DAY, 40-HOUR WEEK", bg="#2E4A62", accent="#F39C4F"),
      sfx="car factory, metal clanging, a horn",
      text="The forty-hour week isn't a law of nature. Henry Ford adopted it in 1926, arguing that people with free time buy more cars."),
 dict(id="r03", spk=M, eng="still", mv="in", sfx="busy government office, typewriters, footsteps",
      text="Parkinson's law says work expands to fill the time available. His example: the Admiralty gained officials while losing two thirds of its ships.",
      kf="A tiny toy battleship sitting alone in the middle of a huge desk, surrounded by a big crowd of officials in suits all leaning in "
         "and peering at it with clipboards."),
 dict(id="r04", spk=M, eng="still", mv="in", refs=["worker"], sfx="traffic jam, engines idling, rain on a windscreen",
      text="Add an average American commute of twenty-seven minutes each way. And Gallup finds only twenty percent of employees worldwide are engaged at work.",
      kf="The man from the reference sitting in a small car in a long traffic jam, chin resting on his hand, staring at the back of the car "
         "in front, a long line of cars stretching into the distance. Exactly one person visible."),
 dict(id="r05", spk=M, eng="card", card=dict(big="56 OF 61", small="UK FIRMS KEPT THE FOUR-DAY WEEK", bg="#3B6E62", accent="#F2C14E"),
      sfx="bright office, relaxed chatter",
      text="When sixty-one British companies tried a four-day week in 2022, fifty-six kept it going, revenue held steady, and sick days fell by sixty-five percent."),
 dict(id="r06", spk=M, eng="still", mv="in", refs=["freelancer"], sfx="quiet flat at night, rain, a calculator beeping",
      text="But steady jobs have a real case. About half of new American businesses are gone within five years, and in Britain the self-employed get no statutory sick pay.",
      kf="The woman from the reference at her kitchen table late at night wrapped in a blanket, with a red nose and a box of tissues, still "
         "typing on her laptop next to a calculator and a pile of receipts. Exactly one person."),
 dict(id="r07", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So the trap comes with dental.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, holding a mug, looking at camera with a small flat smile. Exactly one person.",
      mv="The young man speaks flatly to camera, then takes a small sip from the mug. Static camera, waist-up. Exactly one person; he keeps "
         "the same face, hair and hoodie."),
 dict(id="r08", spk=M, eng="ltx",
      text="And when an Austrian village lost its factory in 1929, researchers found the unemployed men walked slower, and most weren't even wearing a watch.",
      kf="A 1930s village bridge where several men in worn jackets and caps lean on the stone railing looking down at the river, and one "
         "man walks very slowly past them with his hands behind his back.",
      mv="The men lean on the railing and shift slightly, the walking man strolls very slowly across the bridge. Static camera."),
 dict(id="r09", spk=M, eng="still", mv="in", refs=["fordman", "worker"], sfx="windy hilltop, birds",
      text="The forty-hour week was a victory. The trap is treating a deal from the nineteen-twenties like a law of nature.",
      kf="The man in overalls from the first reference and the office worker from the second reference standing side by side on a hill, "
         "looking up at a huge blank stone tablet, both scratching their heads. Exactly two people."),
 dict(id="r10", spk=M, eng="ltx", refs=["worker", "freelancer"],
      text="Is yours a trap or a good deal? The full story is on our channel.",
      kf="The man from the first reference and the woman from the second reference sitting side by side on a park bench in the sunshine, "
         "both turning to look at camera, the man holding a travel mug. Exactly two people.",
      mv="Both turn to look at camera; the woman raises one eyebrow and the man slowly checks his wristwatch. " + P1),
]
THUMB = dict(text="IS 9 TO 5|A TRAP?", refs=["worker"],
             kf="Vertical: the man from the reference sitting at his office desk, which stands on top of a giant wooden mousetrap with its "
                "metal bar pulled back, looking up nervously at a big wall clock. Bright tangerine background. Exactly one person.")
TAIL = 2.4
