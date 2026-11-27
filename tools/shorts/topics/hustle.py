"""Is Hustle Culture a Scam? Final approved script (VIDEOS/Is Hustle Culture a Scam/SCRIPT FOR REVIEW.md), 16:9, about 10 minutes.
Cast: Maya (narrator), Ryan (benny), Brayden, Gerald, Inner Voice. Locked voices chosen 2026-11-25: Brayden E, Gerald A, Inner C, Maya +10%.
Editing approach: on-screen speakers lip-sync (H3); some lines play over the LISTENER's reaction (classic animation cut, and cheaper);
silent shots (text "") carry the visual punchlines; hold = extra seconds after a line for reveals. Sources: see the script document."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Is Hustle Culture a Scam"
ERA = "modern"
M, R, B, G, I = "maya", "benny", "brayden", "gerald", "inner"
LANDSCAPE = True
GAP = 0.25
TEMPO = {M: 1.10, R: 1.0, B: 1.06, G: 1.0, I: 1.0}
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Warm palette of sunrise orange, teal, cream, navy and mustard. Simple cute "
         "characters with round heads, small dot eyes, expressive simple faces, simple bodies, consistent proportions. Clean simple background "
         "with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Warm palette of sunrise orange, teal, cream, navy and mustard. Show only "
             "what the description names. There are NO people of any kind. Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector cartoon animation, smooth expressive motion, static background, shapes keep their exact form and colours, "
        "no morphing, no camera shake.")
CHARS = {
 "brayden": "a hustle-culture influencer as a simple flat vector character: tanned man in his late twenties, slicked-back blond hair, huge white "
            "grin, tight black t-shirt, chunky gold watch, white sneakers, small round head, dot eyes.",
 "gerald": "a corporate HR manager as a simple flat vector character: middle-aged man, neat grey side-parted hair, round glasses, beige "
           "cardigan over a pale blue shirt and navy tie, a lanyard, gentle smile, small round head, dot eyes.",
}
ONE = " Exactly one person."
RYAN = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown "
        "hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, ")
BRAY = "The man from the reference (slicked-back blond hair, tight black t-shirt, gold watch), waist-up, "
GER = "The man from the reference (grey side-parted hair, round glasses, beige cardigan, lanyard), waist-up, "
GER_ROOM = ("sitting in a small softly lit office with a box of tissues on a side table and a framed child's drawing of a smiling sun on the "
            "wall, notepad on his knee, facing camera, warm gentle smile.")
RY_ROOM = "sitting in a chair in a small softly lit office, a box of tissues on the side table, "
FOX = "a small orange fox"


def h(id_, spk, text, kf, mv, refs=None, hold=0.0, sfx=None):
    refs = refs if refs is not None else ({R: ["ryan", "ryan_face"], B: ["brayden"], G: ["gerald"]}[spk])
    return dict(id=id_, spk=spk, eng="h3", text=text, kf=kf + ONE, refs=refs, mv=mv + " Static camera. Exactly one person; same face and clothes.",
                hold=hold, sfx=sfx or "quiet room tone")


def s(id_, spk, text, kf, mv="in", refs=None, env=False, hold=0.0, sfx="quiet room tone", dur=None):
    d = dict(id=id_, spk=spk, eng="still", text=text, kf=kf, mv=mv, refs=refs or [], env=env, hold=hold, sfx=sfx)
    if dur: d["dur"] = dur
    return d


def silent(id_, kf, dur, mv="in", refs=None, env=False, sfx="quiet room tone", eng="still", motion=None):
    d = dict(id=id_, spk=M, eng=eng, text="", kf=kf, mv=motion if eng == "ltx" else mv, refs=refs or [], env=env, dur=dur, sfx=sfx)
    return d


def card(id_, text, big, small, bg="#2E4A62", accent="#F2C14E", sfx="quiet room tone", hold=0.0):
    return dict(id=id_, spk=M, eng="card", text=text, card=dict(big=big, small=small, bg=bg, accent=accent), sfx=sfx, hold=hold)


SHOTS = [
 # ---------------- COLD OPEN
 h("c01", B, "Good morning. It's four a.m. Right now, you're asleep. That's why you're broke. I've been up since three. I've already had a cold shower, a hot shower, and an argument with a swan.",
   BRAY + "standing at dawn on an empty road beside a spotless red sports car, filming himself with a phone on a selfie stick, huge grin, a "
   "car key with a rental key-tag in his other hand; behind him a soaking-wet angry white swan glares at him; " + FOX + " sits on a low wall far behind, watching.",
   "He talks excitedly into the phone on the selfie stick, grinning and gesturing; the wet swan behind him flaps its wings angrily.", hold=0.6,
   sfx="early morning empty road, birds, a swan hissing"),
 s("c02", M, "Somewhere right now, a man is standing next to a very clean car, telling you to wake up at four in the morning so you can be rich like him.",
   "Wide shot: the man from the reference, small in frame, filming himself beside a shiny red sports car on an empty road at sunrise, the "
   "sun just rising behind him." + ONE, mv="out", refs=["brayden"], sfx="early morning road, birds"),
 s("c03", M, "And if you watch to the end, he'll tell you exactly how he made his money.",
   BRAY + "grinning straight into a phone camera very close, eyebrows raised, one finger up as if about to share a secret." + ONE, refs=["brayden"]),
 dict(id="c04", spk=M, eng="ltx", text="It was selling you this video.", refs=["brayden"], hold=0.8,
      kf="The man from the reference sitting at a laptop showing a simple rising bar chart, golden coins raining down from the ceiling all "
         "around him, arms spread in delight." + ONE,
      mv="Golden coins rain down from the ceiling onto the desk and floor, the man laughs with his arms spread. Static camera."),
 h("c05", R, "I'm still watching.", RYAN + "sitting on a sofa at night in a dark living room, face lit by the glow of his phone, guilty expression.",
   "He looks up from his phone, guilty, speaks very quietly, then looks back down at the phone.", hold=0.8, sfx="quiet flat at night"),
 card("c06", "So. Is hustle culture a scam?", "SCAM?", "IS HUSTLE CULTURE A", bg="#3C5A50", hold=0.8),
 # ---------------- THE GOSPEL OF THE GRIND
 s("g01", M, "Hustle culture is the belief that success comes from working all the time, sleeping as little as possible, and turning every hobby you enjoy into a business you don't.",
   "Four small scenes side by side in one image: an ice bath in a dark bathroom, a laptop glowing on an unmade bed, an empty gym at night, "
   "a phone on a table with a glowing coin icon.", env=True, mv="right", sfx="gym at night, distant clanks"),
 s("g02", M, "Its best customers are people who are already exhausted, being told the problem is that they aren't exhausted enough.",
   "A long queue of exhausted simple people with dark circles under their eyes waiting at a bright market stall where the man from the "
   "reference is cheerfully selling energy drinks.", refs=["brayden"], sfx="busy market, chatter"),
 h("g03", B, "Rise and grind.", BRAY + "in a bright minimalist kitchen at dawn, doing a big fist pump at the camera.",
   "He does a big energetic fist pump and shouts at the camera.", sfx="kitchen, morning birds"),
 s("g04", M, "He has a slogan for waking up. Most people just make a noise.",
   "A dark bedroom at dawn, an alarm clock on the bedside table next to a pillow, curtains closed.", env=True, mv="in", sfx="alarm clock ringing in a bedroom"),
 silent("g05", RYAN + "lying face down in bed in a dark bedroom, his face buried in the pillow, an alarm clock ringing on the bedside table." + ONE,
        2.2, refs=["ryan", "ryan_face"], eng="ltx", sfx="muffled groan into a pillow, alarm clock",
        motion="The young man stays face down in the pillow and slowly lifts one hand to slap the alarm clock without lifting his head. Static camera."),
 card("g06", "And it isn't just guys with ring lights. In 2019, Alibaba's founder Jack Ma called China's nine-nine-six schedule a huge blessing. Nine a.m. to nine p.m., six days a week.",
      "996", "9AM TO 9PM · 6 DAYS A WEEK", sfx="busy open-plan office, keyboards"),
 s("g07", M, "I wanted to know what that looks like from the inside. So I asked Gerald.",
   "A closed office door in a quiet corridor with a child's drawing of a smiling sun taped to it.", env=True, sfx="quiet office corridor"),
 # ---------------- ABSURD SEQUENCE 1: THE WEEKEND SUBSCRIPTION
 h("w01", G, "Hi, Ryan. I'm Gerald, from People and Culture. Nobody's in trouble. I just want to talk. Let's start small. Saturday. You don't need all of Saturday. Do you?",
   GER + GER_ROOM, "He speaks gently and calmly, smiling, then tilts his head kindly and waits."),
 h("w02", R, "I... sort of use it.", RYAN + RY_ROOM + "uncertain and a little nervous.", "He answers hesitantly, shrugging slightly."),
 h("w03", G, "Of course. And that's completely valid. What if you kept the morning, and we just quietly looked after the afternoon for you?",
   GER + GER_ROOM, "He nods slowly, writes something on his notepad, and speaks softly with a warm smile."),
 silent("w04", "A closed office door seen from inside a small room, with no handle on this side.", 2.0, env=True, mv="in"),
 h("w05", G, "Put the weekend down, Ryan. Slowly. Nobody has to get hurt.", GER + GER_ROOM.replace("warm gentle smile", "very calm, leaning slightly forward"),
   "He leans in slightly and speaks very softly and slowly, one hand raised in a calming gesture.", hold=0.3),
 silent("w06", "Extreme close-up, top-down view of a wooden table surface: only two hands are visible, entering from the left and right edges of the "
        "frame; a young hand in an orange hoodie sleeve pushes a small glowing sun-shaped object towards an older hand in a beige cardigan sleeve. "
        "No faces, no bodies, only the two hands and the table.", 3.0, eng="ltx", sfx="a tiny sad chime",
        motion="The young hand slowly slides the glowing sun across the table; the cardigan hand takes it and slips it into a pocket. Static camera."),
 s("w07", G, "Good news, though. You can get it back. We've moved weekends to a subscription model. Weekend Lite gives you Saturday morning, with occasional emails. Weekend Plus adds Sunday, but the Sunday evening dread is billed separately. And Weekend Pro includes the afternoon you just gave me.",
   GER + "sitting in a small softly lit office, brightly holding up a laminated card showing three pastel price tiers decorated with little clouds, smiling." + ONE,
   refs=["gerald"], mv="in"),
 s("w08", R, "I just gave you that.", RYAN + RY_ROOM + "staring blankly, stunned." + ONE, refs=["ryan", "ryan_face"], mv="in"),
 s("w09", G, "And now you can have it back. Monthly.", GER + GER_ROOM + ONE, refs=["gerald"], mv="in"),
 h("w10", R, "Can I just... have the one I had before?", RYAN + RY_ROOM + "pleading quietly.", "He asks quietly and hopefully, hands clasped."),
 s("w11", G, "That plan's been discontinued. But we've kept your memories of it in a premium folder.",
   RYAN + RY_ROOM + "slowly realising, his face falling." + ONE, refs=["ryan", "ryan_face"], mv="in"),
 s("w12", I, "He's good.", RYAN + "close-up, staring ahead in shock, while a tiny dark impish shadow creature sits on his shoulder whispering into his ear, impressed." + ONE,
   refs=["ryan", "ryan_face"], mv="in"),
 h("w13", G, "And if you'd rather sleep when you're dead, we've partnered with a lovely cemetery. Staff get ten percent off.",
   GER + "sitting in a small softly lit office, warmly holding out a glossy brochure, smiling kindly.", "He holds out the brochure and speaks warmly and softly."),
 silent("w14", "An open glossy brochure for a cemetery: neat green lawns, gravestones in tidy rows, and one cheerful photo of a children's ball pit "
        "between the graves.", 2.2, env=True, mv="in"),
 h("w15", R, "How do I cancel?", RYAN + RY_ROOM + "barely holding it together, holding the brochure.", "He asks in a small, defeated voice."),
 h("w16", G, "Cancellations are done in person. On a Saturday.", GER + GER_ROOM.replace("warm gentle smile", "his warmest smile yet"),
   "He smiles his warmest smile and speaks softly.", hold=1.2),
 # ---------------- THE CULT OF FOUR A.M.
 s("f01", M, "Then there's the sacred early morning. Robin Sharma's 2018 book The 5 AM Club sold millions of copies telling people to get up before the sun.",
   "A dark bedroom: a person sitting up in bed staring in horror at a ringing alarm clock as if it were a weapon." + ONE, sfx="alarm clock ringing, dark bedroom"),
 s("f02", M, "I tried it, actually. Day one, I did yoga. Day two, I journaled. On day three, I woke up at five, looked at the ceiling, and said no out loud. To nobody.",
   "An unmade bed seen from above at dawn, a rolled-up yoga mat and a closed journal abandoned on the floor beside it.", env=True, mv="out", sfx="quiet bedroom at dawn, birds"),
 s("f03", M, "It's the most honest I've ever been.", "A plain bedroom ceiling with one small crack, lit by soft grey dawn light.", env=True, mv="in", hold=0.5),
 silent("f04", BRAY + "sitting bolt upright in bed in the dark, wide awake, staring intensely at a round analog alarm clock about to ring; "
        "through the window behind him " + FOX + " sits inside his wheelie bin eating a croissant, watching him." + ONE, 2.5, refs=["brayden"], mv="in",
        sfx="ticking clock in a quiet room"),
 # ---------------- A DAY IN THE LIFE
 h("d01", B, "Four a.m., awake. Four oh five, ice bath. Four thirty, I read one page of a book about reading. Five, I tell the mirror it's a winner.",
   BRAY + "in a bright bathroom, talking fast to camera, proudly counting on his fingers.", "He talks very fast and proudly to camera, counting on his fingers."),
 silent("d02", "A bathroom mirror: the man from the reference points proudly at his reflection, but the reflection in the mirror holds a small "
        "suitcase and looks unsure." + ONE, 3.0, refs=["brayden"], eng="ltx", sfx="bathroom, a door closing softly",
        motion="The reflection in the mirror turns, picks up its small suitcase and walks out of the mirror frame, leaving the mirror empty. Static camera."),
 s("d03", B, "Six, I film my morning routine. Seven, I edit my morning routine. Nine, I post my morning routine.",
   BRAY + "framed by a big ring light, filming himself on a phone on a tripod, then editing on a laptop, proud." + ONE, refs=["brayden"], mv="right"),
 s("d04", M, "So the main thing his morning produces is a video of his morning.",
   "The man from the reference slumped exhausted on a sofa at nine in the morning, watching himself on a big television, nodding along." + ONE,
   refs=["brayden"], mv="in", hold=0.8),
 s("d05", R, "I tried it once. Got up at four, cold shower, and by six I'd done everything I needed to do that day. Then I realised everyone I needed was asleep. So I just sat in my kitchen. Fully dressed. Like a butler with no house.",
   RYAN.replace("waist-up, ", "") + "at four in the morning stepping out of a cold shower in a dark bathroom, wrapped in a towel, shivering, wide awake and regretting it." + ONE,
   refs=["ryan", "ryan_face"], mv="in", sfx="dark bathroom, dripping water, shivering"),
 silent("d06", RYAN.replace("waist-up, ", "") + "sitting very upright at a kitchen table in a dark kitchen at six in the morning, fully dressed, hands folded, "
        "staring at the wall; a small bird at the window looks at him with concern." + ONE, 2.5, refs=["ryan", "ryan_face"], mv="in", sfx="quiet kitchen at dawn, a fridge humming"),
 s("d07", M, "Effort does matter, to be fair. The famous ten thousand hour rule comes from the psychologist Anders Ericsson's research on experts, although he said there was nothing magic about the number.",
   "Three side-by-side panels: a violinist, a chess player and a sprinter, each alone, practising." , mv="right", sfx="a violin practising scales"),
 s("d08", M, "Ten thousand hours. That's...", BRAY + "smugly sipping from an oversized white mug, eyebrows raised, in a bright kitchen." + ONE, refs=["brayden"], mv="in", hold=0.6),
 s("d09", M, "No, I had something for this.", BRAY + "smugly sipping from an oversized white mug, eyebrows raised, in a bright kitchen." + ONE, refs=["brayden"], mv="out", hold=0.6),
 s("d10", M, "It's gone. I got up at five.", "A plain bedroom ceiling with one small crack, lit by soft grey dawn light.", env=True, mv="out"),
 # ---------------- THE MATHS OF THE SIDE HUSTLE
 s("s01", M, "Side hustles are real. In 2025, Bankrate found about twenty-seven percent of American adults had one. For plenty of them, it's how the rent gets paid.",
   "A woman on a bicycle delivering food in the rain at night, a delivery bag on her back, tired but determined." + ONE, mv="left", sfx="rain on a city street, a bicycle"),
 card("s02", "The average side hustle earns eight hundred and eighty-five dollars a month.", "$885", "PER MONTH · AVERAGE", sfx="a small celebratory ding"),
 card("s03", "The median, the person exactly in the middle, earns two hundred.", "$200", "PER MONTH · MEDIAN", bg="#5A3C3C", sfx="one sad trombone note", hold=0.6),
 s("s04", M, "The average is a liar standing next to a millionaire.",
   "A long empty table with a row of tiny piles of gold coins, and at the far right end one colossal tower of gold coins reaching the "
   "ceiling, with the man from the reference standing on top of the tower, waving. He appears only once; there are no other people." + ONE,
   refs=["brayden"], mv="right"),
 silent("s05", "The colossal gold coin tower has tipped over: it was a flat cardboard cutout of coins and of a waving man, propped up with a broom.",
        2.5, env=True, mv="in", sfx="a cardboard sheet falling flat"),
 s("s06", M, "Then there's multi-level marketing, where you sell products and recruit your friends to sell them too.",
   "A cheerful woman at her kitchen table surrounded by stacks of boxes of scented candles, typing happily on her phone." + ONE, sfx="kitchen, phone typing"),
 silent("s07", "A phone screen showing a group chat as a row of round profile pictures with simple faces, several of them fading away, the last "
        "one an older woman with grey hair in a bun.", 2.5, env=True, mv="in", sfx="message notification blips in quick succession"),
 s("s08", I, "Text your ex. Sell her a candle.", RYAN + "close-up, uneasy, while a tiny dark impish shadow creature on his shoulder whispers delightedly into his ear." + ONE,
   refs=["ryan", "ryan_face"], mv="in"),
 s("s09", R, "No.", RYAN + "close-up, eyes wide, alarmed, shaking his head." + ONE, refs=["ryan", "ryan_face"], mv="out"),
 card("s10", "In 2018, an AARP Foundation survey of people who'd joined one found forty-seven percent lost money. Twenty-seven percent broke even.",
      "47%", "LOST MONEY · 27% BROKE EVEN", sfx="quiet office"),
 h("s11", R, "So a quarter of them did unpaid work.", RYAN + "standing in a simple flat cosy living room with a teal wall and a plant, slowly working it out.",
   "He speaks slowly, working it out, eyebrows rising."),
 s("s12", M, "Enthusiastically.", "The cheerful woman beaming proudly in her kitchen surrounded by towers of unsold candle boxes." + ONE, mv="in", hold=0.9),
 # ---------------- ABSURD SEQUENCE 2: THE 4 A.M. BOARD MEETING
 s("b01", M, "And all those extra hours have to come from somewhere. For Brayden, they come out of the night. Which, unfortunately, his body was using.",
   "A cartoon cross-section of a man's body drawn like a small office building at night, with tiny lit windows inside the chest and head.", env=True, mv="in"),
 h("b02", B, "Team. Let's talk about sleep. Every night, eight hours, gone. No revenue. No content. I'm not paying you to lie there in the dark.",
   BRAY + "standing at a whiteboard in a tiny glass boardroom lit by a ring light, wearing a headset, addressing the table like a CEO.",
   "He paces in front of the whiteboard and gives a fired-up pep talk, jabbing the air."),
 silent("b03", "A tiny glass boardroom table inside a body: cartoon organ characters wearing lanyards sit around it: a jittery red heart with eight "
        "empty coffee cups, a grey hollow-eyed liver, two identical lung interns, two kidneys, and a pink brain asleep face-down on the table.",
        2.5, env=True, mv="right", sfx="office air conditioning, a quiet snore"),
 s("b04", B, "Heart. Love the energy. You're getting more responsibility.",
   "A jittery cartoon red heart character in a lanyard sitting at a small desk covered in empty coffee cups, trembling with energy.", env=True, mv="in"),
 silent("b05", "A jittery cartoon red heart character in a lanyard sitting at a small desk covered in empty coffee cups.", 2.5, env=True, eng="ltx",
        sfx="rattling desk, cups clinking", motion="The heart character vibrates faster and faster until its whole desk slides sideways out of frame. Static camera."),
 s("b05b", B, "Liver, I've seen your numbers. You're on a performance plan.",
   "A grey, hollow-eyed cartoon liver character in a lanyard silently sliding a folded letter across a table.", env=True, mv="in"),
 silent("b06", "The man from the reference tearing a folded letter in half without looking at it, in front of a sad grey cartoon liver character." + ONE,
        2.0, refs=["brayden"], mv="in", sfx="paper tearing"),
 s("b07", B, "Kidneys. Two of you, doing the same job. That's a redundancy situation.",
   "Two identical cartoon kidney characters in lanyards sitting side by side at a table, looking at each other nervously.", env=True, mv="in"),
 silent("b08", "Two identical cartoon kidney characters at a table; one is standing holding a small cardboard box of belongings.", 3.0, env=True, eng="ltx",
        sfx="a chair scraping, footsteps, a door closing",
        motion="The kidney holding the box walks slowly out of frame; the other kidney stays and stares sadly at the empty chair. Static camera."),
 s("b09", M, "He fired a kidney.", "An empty office chair at a tiny boardroom table with a lanyard hanging on its back.", env=True, mv="in", hold=0.7),
 card("b10", "Sorry. The actual science. In 2000, Australian researchers found that after seventeen to nineteen hours awake, people did some tests as badly as someone with a blood alcohol level of zero point zero five percent.",
      "17-19 HRS", "AWAKE ≈ 0.05% BLOOD ALCOHOL", bg="#3C5A50", sfx="quiet office hum"),
 s("b11", M, "So a man who got up at four is, by ten p.m., cognitively two glasses of wine into a wedding. Except nobody's dancing, and he's trying to sell you a webinar.",
   "A pink cartoon brain character wearing a little party hat at the boardroom table, swaying slightly and giving an over-enthusiastic thumbs up.",
   env=True, mv="in", sfx="distant wedding party chatter, glasses clinking"),
 h("b12", B, "Sleep is a mindset.", BRAY + "in the tiny glass boardroom, pointing confidently at the camera.", "He points at the camera and speaks with total certainty."),
 s("b13", M, "It isn't. Researchers think one of the things sleep does is clear waste out of the brain. Skip it, and you're running the whole operation on yesterday's rubbish.",
   "A pink cartoon brain character dragging an enormous overflowing black bin bag towards a door, flies circling it.", env=True, mv="left", sfx="a heavy bin bag dragging, flies buzzing"),
 h("b14", B, "Where do you think you're going?", BRAY + "standing in a doorway with his arms spread, blocking it, frowning.", "He blocks the doorway and demands an answer."),
 silent("b15", "A pink cartoon brain character lying asleep across a doorway, hugging a bin bag, a lanyard around its neck.", 3.0, env=True, eng="ltx",
        sfx="a soft snore, light switches clicking off one by one",
        motion="The brain snores peacefully as the lights in the room switch off one by one until it is dark. Static camera."),
 s("b16", I, "Breathwork. Ninety-nine dollars.", "A dark empty boardroom where a tiny impish shadow creature holds up a small glossy leaflet with a smug grin.", env=True, mv="in"),
 s("b17", M, "Absolutely not.", "A dark empty boardroom, the leaflet now lying crumpled on the floor.", env=True, mv="out", hold=0.4),
 # ---------------- THE COST
 s("k01", M, "More hours don't even mean more work. The Stanford economist John Pencavel studied British munitions workers in the First World War. Their output at seventy hours a week was barely different from their output at fifty-six.",
   "A 1916 factory floor: women workers in caps and overalls filling artillery shells, two identical piles of finished shells in front.", mv="right", sfx="old factory machinery"),
 s("k02", M, "Those extra fourteen hours produced nothing. They were just looking busy. A craft that workers have since refined into the little green available dot next to their name.",
   "A 1916 factory worker very slowly polishing a single shell with a cloth while a foreman in a bowler hat walks past behind him." , mv="in", sfx="old factory, footsteps"),
 silent("k03", "A modern laptop on an office desk with a small glowing green dot on its screen next to an office worker who is fast asleep with "
        "his head on the desk." + ONE, 2.0, mv="in", sfx="quiet office, a soft snore", ),
 dict(id="k04", spk=M, eng="still", text="And sometimes it isn't funny at all. In 2021, the World Health Organization and the International Labour Organization estimated that long working hours led to seven hundred and forty-five thousand deaths from stroke and heart disease in 2016.",
      kf="An empty office chair under a single desk lamp in a dark office.", env=True, mv="in", sfx="silent empty office", hold=1.5),
 # ---------------- ABSURD SEQUENCE 3: THE ICEBERG
 s("i01", M, "So why does any of this feel true?",
   "A sunny ocean with the small white tip of an iceberg; on top, the man from the reference lounges on a yacht in sunglasses filming himself; "
   "behind him " + FOX + " lies on a sun lounger wearing tiny sunglasses with a drink." + ONE, refs=["brayden"], mv="in", sfx="calm sea, gulls"),
 s("i02", M, "This is the hustle success story. And this...", "The same sunny ocean and iceberg tip seen from a little further away, the waterline across the bottom of the picture.",
   env=True, mv="out", sfx="calm sea, gulls"),
 silent("i03", "Underwater cross-section: the bright waterline is a thin strip at the very top of the picture; below it a huge iceberg mass "
        "fills the deep blue water, and hundreds of small simple people stand on its underwater ledges with bubbles rising, holding boxes of phone "
        "cases, candles and laptops, all politely waving.", 3.0, mv="out", sfx="deep underwater ambience"),
 s("i04", M, "...is everyone else.", "Underwater: thousands of small simple people standing on the ledges of a vast iceberg, politely waving.", mv="in", sfx="deep underwater ambience"),
 silent("i05", RYAN.replace("waist-up, ", "") + "standing underwater on an iceberg ledge among other people, holding a cardboard box full of mugs printed "
        "with his own face, looking caught out." + ONE, 1.5, refs=["ryan", "ryan_face"], mv="in", sfx="deep underwater ambience"),
 s("i06", M, "Ryan?", RYAN.replace("waist-up, ", "") + "standing underwater on an iceberg ledge holding a cardboard box of mugs printed with his own face, "
   "frozen, embarrassed." + ONE, refs=["ryan", "ryan_face"], mv="in", sfx="deep underwater ambience"),
 h("i07", R, "It was a lockdown thing.", RYAN + "underwater in blue light on an iceberg ledge, holding up one mug printed with his own face, mortified but hopeful.",
   "He speaks quietly, mortified, then holds the mug up a little hopefully.", hold=0.8, sfx="deep underwater ambience"),
 s("i08", M, "In the Second World War, the statistician Abraham Wald was shown bombers covered in bullet holes, and asked where to add armour. He pointed out that the planes hit everywhere else never came back to be counted.",
   "Underwater: a few World War Two bombers resting on the iceberg beside the people; one person offers a pilot a candle.", mv="right", sfx="deep underwater ambience"),
 s("i09", M, "If hustle gurus had been in charge, they'd have armoured the bullet holes and called it a mindset.",
   "The man from the reference in a 1940s leather flight jacket, proudly bolting a metal plate over a bullet hole on a bomber's wing, thumbs up." + ONE,
   refs=["brayden"], mv="in", sfx="airfield wind, a wrench"),
 s("i10", M, "You only ever hear from the guy on top. Nobody hosts a podcast called How I Lost Everything Selling Phone Cases.",
   "A man alone in a dark room with his ring light switched off, surrounded by towers of unopened boxes of phone cases." + ONE, mv="in", sfx="quiet room"),
 s("i11", M, "Although honestly, I'd listen.", "A small podcast microphone on an empty desk in the dark room, the boxes of phone cases behind it.", env=True, mv="in", hold=0.6),
 # ---------------- THE COURSE
 card("x01", "And where there's a dream, there's a course. In 2024, the US Federal Trade Commission went after schemes selling passive income from AI-powered online stores. Customers paid tens of thousands of dollars. For nearly all of them, the FTC said, the money never arrived.",
      "AI COMPLY", "OPERATION · FTC 2024", bg="#5A3C3C", sfx="quiet government office"),
 silent("x02", "The man from the reference lovingly hanging an official-looking letter with a seal in a big gold frame on the wall above his desk." + ONE,
        2.2, refs=["brayden"], mv="in", sfx="a nail being tapped, a frame on the wall"),
 h("x03", B, "You know you've made it when the government knows your name.", BRAY + "standing proudly next to a gold-framed official letter on the wall.",
   "He gestures proudly at the framed letter and speaks with total pride."),
 # ---------------- THE BACKLASH
 s("y01", M, "People are pushing back. In 2021, a post about lying flat went viral in China. Doing the absolute minimum, on purpose.",
   "A young man lying perfectly flat and serene on a mat in the middle of a busy open-plan office, coworkers stepping over him." , mv="in", sfx="busy office, keyboards"),
 silent("y02", "The man from the reference kneeling beside a young man lying flat on a mat in an office, gently tucking a blanket over him.", 3.0,
        refs=["gerald"], eng="ltx", sfx="busy office, a soft blanket rustle",
        motion="The older man gently tucks the blanket in, then slides a laptop under the lying man's hands and pats it kindly. Static camera."),
 card("y03", "And in 2019, Microsoft Japan closed its offices every Friday in August. Sales per employee went up almost forty percent.",
      "+39.9%", "4-DAY WEEK · MICROSOFT JAPAN 2019", sfx="quiet office"),
 s("y04", M, "So, wellness.", "One sad beanbag in the middle of a vast grey office; a projector shows a picture of a mountain on the wall.", env=True, mv="in", sfx="empty office hum"),
 h("y05", G, "We hear you. So we've installed a beanbag, and booked a one-hour webinar on resilience. It's during your lunch break.",
   GER + "standing proudly beside a beanbag in a vast grey office, beaming.", "He gestures proudly at the beanbag and speaks warmly."),
 silent("y06", RYAN.replace("waist-up, ", "") + "sitting alone on a beanbag in a vast grey office, eating a sandwich, drinking from a mug printed with "
        "his own face, a projector showing a mountain." + ONE, 2.0, refs=["ryan", "ryan_face"], mv="in", sfx="empty office hum"),
 h("y07", R, "Is the beanbag mandatory?", RYAN + "sitting on a beanbag in a grey office holding a sandwich, quietly asking.", "He asks quietly, holding his sandwich."),
 h("y08", G, "Of course not. It's optional. Like the weekend.", GER + "standing beside a beanbag in a grey office, warm smile.", "He smiles warmly and speaks softly.", hold=1.2),
 # ---------------- THE VERDICT AND THE REVEAL
 s("v01", M, "So is hustle culture a scam? Not the work. Work is real, and some people genuinely love building things at midnight. Good for them.",
   "A happy woman building a wooden chair in her garage workshop at midnight under a warm lamp." + ONE, mv="in", sfx="quiet garage at night, sanding"),
 s("v02", M, "The scam is the packaging. Exhaustion sold as a personality, survivors sold as proof, and your insecurity sold back to you at a monthly rate.",
   "A shop shelf of identical shiny boxes, each box showing a sunrise and an exhausted face.", env=True, mv="right", sfx="quiet shop"),
 silent("v03", "The man from the reference asleep in the driver's seat of his red sports car at night, a parking ticket on the windscreen, a rental "
        "key-tag hanging from the ignition, a wet swan glaring at him through the side window." + ONE, 1.6, refs=["brayden"], mv="in", sfx="quiet street at night"),
 h("v04", B, "Link in bio.", BRAY + "asleep in the driver's seat of a car at night, mouth slightly open.", "He mumbles in his sleep without opening his eyes.",
   sfx="quiet street at night"),
 s("v05", M, "Oh, and Brayden's four a.m. videos?", BRAY + "filming himself in front of a glowing golden sunrise." + ONE, refs=["brayden"], mv="in"),
 silent("v06", "A wider view of a room: the golden sunrise is just a desk lamp with an orange sweet wrapper taped over it; the blinds are closed "
        "with bright afternoon daylight leaking round them; a school bus passes outside; the man from the reference stands by the lamp with "
        "his phone." + ONE, 3.0, refs=["brayden"], mv="out", sfx="afternoon street outside, a school bus passing"),
 s("v07", M, "Filmed at four in the afternoon. The sunrise is a lamp.", "A desk lamp with an orange sweet wrapper taped over it, glowing, next to closed blinds with daylight leaking round them.",
   env=True, mv="in", hold=0.6),
 h("v08", B, "Still counts.", BRAY + "standing next to the desk lamp, not embarrassed at all, giving two thumbs up to camera.", "He beams and gives two thumbs up."),
 silent("v09", "Real 4 a.m., dark and quiet: " + FOX + " wearing a tiny business suit sits on the bonnet of a red sports car eating a croissant, "
        "typing on a tiny laptop whose screen shows a small glowing green dot.", 3.2, env=True, mv="in", sfx="silent night street, one alarm clock beep"),
]
for _s in SHOTS:
    if _s["eng"] == "still" and _s.get("refs") and "ryan" in _s["refs"] and "Flat 2D" not in _s["kf"]:
        pass
THUMB = dict(text="RICH BY|4AM?", refs=["brayden"],
             kf="The man from the reference grinning with two huge thumbs up in front of a shiny red sports car at sunrise; a rental key-tag "
                "dangles from the car key in his hand; " + FOX + " sits on the car roof behind him looking unimpressed. Exactly one person.")
TAIL = 1.0

for _s in SHOTS:                                   # the door beat's generated room tone has a voice-like murmur: keep it near silent
    if _s["id"] == "w04": _s["sfx_db"] = -46
