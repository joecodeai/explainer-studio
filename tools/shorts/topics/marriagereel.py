"""Reel / Short for 'Is marriage becoming obsolete?': the whole argument in ~75 s, native 9:16. Same facts and sources as topics/marriage.py."""
from topics.marriage import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
FOLDER = "Is Marriage Becoming Obsolete"
ERA = "modern"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="n01", spk=M, eng="still", mv="in", refs=["her", "him"], sfx="small wedding chapel, organ fading, a camera shutter",
      text="Four in ten Americans say marriage is becoming obsolete. And yet people still spend the price of a car on one afternoon to do it. So which is it?",
      kf="The woman from the first reference in a white wedding dress and the man from the second reference in a navy suit standing at a "
         "flower-covered wedding arch, smiling, while behind them a shiny red family car sits on the altar with a giant gold price tag "
         "dangling from it. Exactly two people."),
 dict(id="n02", spk=M, eng="card", card=dict(big="25%", small="OF 40-YEAR-OLDS NEVER MARRIED", bg="#2E4A62", accent="#F2A65A"),
      sfx="quiet room tone, a clock ticking",
      text="In 2021, a record quarter of American forty-year-olds had never married. People marry later, and more couples just live together."),
 dict(id="n03", spk=M, eng="still", mv="in", sfx="medieval hall, a fire crackling",
      text="But for most of history, marriage wasn't about love. It was about property, alliances and survival. For a lot of women, it was the only option on the menu.",
      kf="A restaurant menu card on a table showing only one single dish, a wedding cake, with a lonely fork beside it. No people."),
 dict(id="n04", spk=M, eng="still", mv="out", refs=["her"], sfx="busy modern office, keyboards",
      text="Now women can work, own property and borrow money on their own. Most of the reasons marriage was necessary have gone.",
      kf="The woman from the reference striding confidently out of a modern office building with a laptop bag and house keys in her hand, "
         "city behind her. Exactly one person."),
 dict(id="n05", spk=M, eng="card", card=dict(big="$34,200", small="AVERAGE US WEDDING (2025)", bg="#3C5A50", accent="#F2A65A"),
      sfx="busy wedding venue, champagne pop, chatter",
      text="And the average American wedding now costs thirty-four thousand dollars. So plenty of couples wait."),
 dict(id="n06", spk=M, eng="card", card=dict(big="69%", small="OF YOUNG SINGLES WANT TO MARRY", bg="#2E4A62", accent="#F2C14E"),
      sfx="busy cafe, chatter",
      text="But here's the twist. Sixty-nine percent of never-married Americans aged eighteen to thirty-four still want to marry someday. And divorce rates are down a lot since 1980."),
 dict(id="n07", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So, not dead. Just pickier.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, holding a mug, looking at camera with a small knowing smile. Exactly one person.",
      mv="The young man speaks flatly to camera, then takes a small sip from the mug. Static camera, waist-up. Exactly one person; he keeps "
         "the same face, hair and hoodie."),
 dict(id="n08", spk=M, eng="ltx", refs=["her", "him"],
      text="Marriage isn't becoming obsolete. It's becoming optional. Fewer people do it, later, and for love. The full story is on our channel.",
      kf="The woman from the first reference and the man from the second reference walking hand in hand along a path in a sunny park, "
         "talking and smiling. Exactly two people.",
      mv="The couple walk slowly forward along the path hand in hand, smiling at each other, leaves drifting down. " + P1),
]
THUMB = dict(text="IS MARRIAGE|DYING?", refs=["her", "him"],
             kf="Vertical: the woman from the first reference in a white wedding dress and the man from the second reference in a navy suit "
                "both staring in shock at a giant wedding cake that is leaning and cracking, a huge gold price tag hanging from the cake. Soft "
                "pink background. Exactly two people.")
TAIL = 2.4
