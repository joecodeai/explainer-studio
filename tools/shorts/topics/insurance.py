"""How Insurance Actually Works (It's a Bet You Want to Lose). Approved script: VIDEOS/How Insurance Actually Works/SCRIPT FOR REVIEW.md
(Part B, dollars version, 2026-11-27). 16:9, about 9-10 minutes. Same cast, voices, tempo and helpers as topics/hustle.py and
topics/subscription.py; palette shifted to navy / cream / coin gold. 8 x LIPSYNC -> h(), 4 x MOTION -> eng="ltx", the rest stills and 3 cards.
Spoken text is verbatim from the script; Maya paragraphs are split only at sentence ends where the picture changes."""
from topics.hustle import (STYLE as _H_STYLE, ENV_STYLE as _H_ENV, LOOK, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, BRAY, GER, FOX,
                           M, R, B, G, I, h, s, silent)
from topics.subscription import CHARS, RY, ger, card, SHADOW  # noqa: F401
FOLDER = "How Insurance Actually Works"
ERA = "modern"
LANDSCAPE = True
GAP = 0.25
_PAL = "Warm palette of sunrise orange, teal, cream, navy and mustard."
assert _PAL in _H_STYLE and _PAL in _H_ENV
STYLE = _H_STYLE.replace(_PAL, "Palette of calm navy, warm cream, coin gold, soft teal and coral.")
ENV_STYLE = _H_ENV.replace(_PAL, "Palette of calm navy, warm cream, coin gold, soft teal and coral.")
RYAN_FULL = RYAN.replace("waist-up, ", "")
BRAY_FULL = BRAY.replace("waist-up, ", "")

# ---------------- sets
KF_KITCHEN = (RYAN + "sitting at a small kitchen table in the morning with a mug, frowning at a banking app on his phone; on the wall behind him a "
              "calendar covered in neat ticks; through the window behind him " + FOX + " is asleep, curled up in a blue recycling box." + ONE)
KF_RY_CLOSE = RYAN + "close-up at his kitchen table in the morning, staring at his phone, "
VILLAGE = ("A tiny flat cartoon village of many small identical houses with red roofs around a village square; in the middle of the square "
           "stands one big shiny tin bucket")
KF_FLOOD = (RYAN + "standing on a kitchen chair in his kitchen, which is flooded an inch deep with water, holding his phone to his ear; a single "
            "sock floats on the water; ")
GER_DESK = "at his desk"
SFX_K = "quiet kitchen, a clock ticking, a fridge humming"
SFX_V = "a quiet village square, birds, distant chatter"
SFX_F = "a flooded kitchen, slow dripping, water lapping"
SFX_G = "quiet office, air conditioning hum"
SFX_B = "empty room echo, a bare bulb buzzing"
KF_GER_PEN = ger("pen poised over his notepad, attentive, gentle smile.") + ONE
KF_GER_WRITE = ger("writing very slowly on his notepad, eyes down, serene.") + ONE
KF_GER_SMILE = ger("warm gentle smile, hands folded on his notepad.") + ONE
KF_RY_CHAIR = KF_FLOOD + "his face confused and polite." + ONE
NO_TEXT = " No writing, letters or numbers anywhere."

SHOTS = [
 # ---------------- COLD OPEN: ELEVEN YEARS
 s("c01", M, "For eleven years, Ryan has paid a stranger forty-five dollars a month, in case something terrible happens to him.", KF_KITCHEN, refs=RY, sfx=SFX_K),
 s("c02", M, "Nothing has.", KF_RY_CLOSE + "sulking, completely unharmed, his mug of tea perfectly fine." + ONE, refs=RY, hold=0.4, sfx=SFX_K),
 h("c03", R, "Eleven years. Not even a small flood.", KF_RY_CLOSE + "genuinely aggrieved.", "He speaks quietly, genuinely aggrieved, shaking his head slightly.", sfx=SFX_K),
 s("c04", I, "Leave the bath running.", KF_RY_CLOSE + "uneasy, while " + SHADOW + "." + ONE, refs=RY, sfx=SFX_K),
 s("c05", R, "No.", RYAN + "close-up, turning his head to frown firmly at the tiny dark imp on his shoulder, who looks disappointed." + ONE, refs=RY, hold=0.6, sfx=SFX_K),
 s("c05b", M, "He did check whether it was covered, though.", KF_RY_CLOSE + "glancing sideways, a little guilty." + ONE, refs=RY, hold=0.5,
   sfx=SFX_K),
 s("c06", M, "Insurance is the only thing you buy hoping it's a complete waste of money. And if it isn't, you have to prove it.",
   "A very thick stack of plain blank paper pages held together by a big black binder clip, seen from the side on a kitchen table next to a mug, dozens of coloured sticky tabs poking out of its edge." + NO_TEXT,
   env=True, sfx=SFX_K),
 card("c07", "So. How does insurance actually work?", "INSURANCE?", "HOW DOES IT ACTUALLY WORK", bg="#2E4A62", hold=1.5),
 # ---------------- ABSURD SEQUENCE 1: THE BUCKET
 s("u01", M, "It starts with a bucket.", VILLAGE + ", gleaming in the sun.", env=True, mv="in", sfx=SFX_V),
 s("u02", M, "A hundred families each put in a dollar. Nobody knows whose house will catch fire this year. But somebody's usually does.",
   VILLAGE + "; a long happy queue of small simple villagers drops one gold coin each into the bucket.", mv="right", sfx="coins plinking into a tin bucket, a village square"),
 silent("u03", VILLAGE + "; one small house nearby has bright orange flames on its roof, and the big tin bucket is tipped over on its side, a stream "
        "of gold coins pouring out towards the burning house.", 3.0, env=True, eng="ltx", sfx="a small fire crackling, coins pouring",
        motion="The flames on the roof flicker; gold coins tumble out of the tipped bucket towards the house. Static camera."),
 s("u04", M, "So when it happens, the bucket pays. Nobody loses everything. Everybody loses a dollar.",
   "The same small village house, rebuilt and shiny new with a big red ribbon on the door; small simple villagers clapping; the big tin bucket "
   "beside it, a little emptier.", sfx="a small crowd clapping, birds"),
 s("u05", R, "So it's a group chat. With money.", RYAN + "standing in a village square next to a big shiny tin bucket full of coins, nodding slowly, "
   "working it out." + ONE, refs=RY, sfx=SFX_V),
 s("u06", M, "Mathematicians call it the law of large numbers. You can't predict which house will burn. But with enough houses, you can predict roughly how many.",
   "A flat infographic on a cream background: five neat rows of many tiny identical house icons, and in every row exactly one house icon is "
   "coloured orange." + NO_TEXT, env=True, mv="right", sfx="quiet room tone"),
 s("u07", M, "Honestly, it's one of the best ideas humans have ever had.", VILLAGE + " at golden sunset, peaceful, the bucket glowing softly.",
   env=True, sfx="evening birds, a gentle breeze"),
 s("u08", M, "Then somebody had to look after the bucket.", VILLAGE + ", empty and quiet, with one small wooden stool beside the bucket.",
   env=True, hold=0.3, sfx=SFX_V),
 h("u09", G, "Hello. I'm Gerald. I'll be looking after the bucket.",
   GER + "standing beside a big shiny tin bucket in a village square, holding a clipboard, one hand resting on the bucket, warm gentle smile.",
   "He introduces himself warmly and calmly, one hand resting on the bucket.", sfx=SFX_V),
 s("u10", M, "Then the bucket needed an office. Then a logo. Then a mascot.",
   "A neat little office building in the village square, the big tin bucket visible through its front window; on its roof a big round logo of a "
   "tin bucket with a fox's face." + NO_TEXT, env=True, mv="out", sfx=SFX_V),
 silent("u11", "A big billboard above the village rooftops showing " + FOX + " in a tiny business suit, waving cheerfully." + NO_TEXT, 2.5, env=True,
        sfx="a village square, a jingle-like chime"),
 s("u12", M, "And then Gerald noticed something. Money goes into the bucket every month. Fires happen... occasionally.",
   GER + "in a small office, looking down into a huge tin bucket overflowing with gold coins, eyebrows raised." + ONE, refs=["gerald"], sfx=SFX_G),
 s("u13", G, "So the money's just... sitting there.", GER + "close-up, in a small office, softly amazed, a gold glow on his face from below." + ONE,
   refs=["gerald"], hold=0.4, sfx=SFX_G),
 s("u14", M, "So in between fires, the bucket invests it. The industry calls this \"float\". It's other people's money that you're holding until they need it, and in the meantime, you get to invest it.",
   GER + "very carefully carrying a heavy tin bucket of gold coins towards a big wall screen of rising green stock charts." + ONE + NO_TEXT,
   refs=["gerald"], mv="right", sfx="a busy trading floor, a cash register ding"),
 dict(silent("u15", "The neat little office building in the village square with a tin-bucket logo on its roof, beside a much taller glass tower "
             "under construction; small villagers looking up." + NO_TEXT, 0, env=True, eng="ltx", sfx="a long creak, construction, a lift ding",
             motion="The building grows upward floor by floor into a tall gleaming tower. Static camera.", ), hold=1.0,
      text="At the end of 2024, Warren Buffett's company, Berkshire Hathaway, was holding a hundred and seventy-one billion dollars of float."),
 s("u16", M, "An insurer can lose money on the insurance itself and still do very nicely on the investing. Which is how the bucket got a tower.",
   "A city skyline at dusk; the tallest tower in the middle has a giant shiny tin bucket on its very top." + NO_TEXT, env=True, mv="out", sfx="a city at dusk"),
 s("u17", R, "And the people with the dollars?", RYAN_FULL + "standing tiny at the foot of an enormous gleaming glass tower, looking up, holding one coin." + ONE,
   refs=RY, sfx="a windy city street"),
 s("u18", M, "They got a letter.", "An opened envelope on a doormat; the letter inside shows one big red upward-pointing arrow." + NO_TEXT,
   env=True, hold=1.5, sfx="a letterbox flap clacking, paper landing"),
 # ---------------- HOW WE GOT HERE
 s("w01", M, "The bucket isn't new. In the 1680s, London ship owners met at Edward Lloyd's coffee house, on Tower Street, because it had the best shipping gossip in the city.",
   "A crowded 17th-century London coffee house: men in long wigs and coats sitting at wooden tables with coffee cups, reading shipping lists, "
   "leaning in to gossip, model ships on a shelf." + NO_TEXT, mv="right", sfx="a busy coffee house, chatter, cups clinking"),
 s("w02", M, "Wealthy merchants would write their names under the description of a ship and its cargo, each taking a share of the risk. Which is where the word \"underwriter\" comes from.",
   "Close-up of an old parchment with a drawing of a sailing ship at the top and, under it, a column of squiggly ink signatures; a quill pen "
   "adding one more.", env=True, mv="in", sfx="a quill scratching on paper"),
 s("w03", M, "That coffee house became Lloyd's of London. And in 1912, it had insured a ship called the Titanic, for a million pounds. Nearly five million dollars, back then.",
   "A huge elegant four-funnel ocean liner sailing on a calm sea at sunset, smoke trailing from its funnels." + NO_TEXT, env=True, mv="right",
   hold=0.5, sfx="calm sea, a distant ship's horn"),
 s("w04", M, "It paid out in full, within thirty days.", "An old leather ledger open on a desk beside a neat stack of old banknotes and a red wax seal."
   + NO_TEXT, env=True, hold=1.0, sfx="a quiet old office, a clock ticking"),
 card("w05", "Thirty days? My phone claim's been open since March.", "DAY 214", "PHONE CLAIM · STILL OPEN", spk=R, bg="#5A3C3C", hold=1.0,
      sfx="quiet room tone"),
 s("w06", M, "Fire insurance also came from a disaster. After the Great Fire of 1666 destroyed most of the City of London, a builder called Nicholas Barbon opened the Fire Office, in 1680.",
   "Old 17th-century London rooftops and church spires under a sky still hazy with grey smoke; new timber houses being built." + NO_TEXT,
   env=True, mv="right", sfx="a quiet old city, distant hammering"),
 s("w07", M, "Insurers ran their own fire brigades and nailed metal badges, called fire marks, to the houses they covered. By 1690, one London house in ten was insured.",
   "A row of old London houses; above one front door a small shiny gold metal plaque; two old-time firemen in leather helmets carry leather "
   "buckets past." + NO_TEXT, mv="in", sfx="an old street, footsteps, a horse and cart"),
 s("w08", M, "You'll hear that the brigades just stood and watched uninsured houses burn. But fire doesn't check the badge. The house next door was usually somebody's customer.",
   "Two old-time firemen with an old wooden hand-pump spraying water over two neighbouring houses at once, shrugging; only one house has a gold "
   "plaque." + NO_TEXT, mv="right", sfx="water spraying, a hand pump creaking"),
 # ---------------- ABSURD SEQUENCE 2: THE CLAIM
 dict(silent("k01", KF_FLOOD + "outside the glass patio door behind him " + FOX + " floats past in a tiny inflatable swim ring." + ONE, 0, refs=RY,
             eng="ltx", sfx=SFX_F, motion="The sock drifts slowly across the water; outside the glass door the small fox paddles past in its "
             "inflatable ring. The man stands still on the chair. Static camera."),
      text="Which brings us back to Ryan. Last Tuesday, his washing machine flooded the kitchen."),
 s("k02", R, "Finally.", RYAN + "close-up, standing on a chair in a flooded kitchen, a small guilty smile, almost happy." + ONE, refs=RY, hold=0.4, sfx=SFX_F),
 s("k03", M, "He rang the bucket.", "Close-up of a phone screen showing a call on hold, with a big simple music-note icon and a spinning circle."
   + NO_TEXT, env=True, hold=3.0, sfx="tinny cheerful hold music"),
 h("k04", G, "Ryan. Nobody's in trouble. I've moved to Claims.", ger("warm reassuring smile."), "He speaks softly and reassuringly, smiling.", sfx=SFX_G),
 s("k05", G, "Let's take this one step at a time. Did the water come from above, or below?", KF_GER_PEN, refs=["gerald"], sfx=SFX_G),
 s("k06", R, "From the washing machine.", KF_RY_CHAIR, refs=RY, sfx=SFX_F),
 h("k07", G, "So... sideways.", ger("thoughtful, gazing slightly upward."), "He thinks for a moment, then speaks slowly and thoughtfully.", sfx=SFX_G),
 s("k08", G, "That's completely valid. Sideways is very brave.", KF_GER_WRITE, refs=["gerald"], sfx="quiet office, a pen scratching slowly"),
 s("k09", R, "Is that covered?", KF_RY_CHAIR, refs=RY, sfx=SFX_F),
 s("k10", G, "Sudden is covered. Gradual isn't. Was it sudden?", KF_GER_PEN, refs=["gerald"], sfx=SFX_G),
 s("k11", R, "I was standing in it.", RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, honest, a sock floating past "
   "below him." + ONE, refs=RY, sfx=SFX_F),
 s("k12", G, "And was the washing machine on, at the time?", KF_GER_WRITE, refs=["gerald"], sfx="quiet office, a pen scratching slowly"),
 s("k13", R, "It's a washing machine.", KF_RY_CHAIR, refs=RY, sfx=SFX_F),
 s("k14", G, "So you were aware it contained water.", ger("nodding slowly, very understanding.") + ONE, refs=["gerald"], sfx=SFX_G),
 s("k15", R, "...That's what it's for.", RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, small, defeated." + ONE,
   refs=RY, sfx=SFX_F),
 s("k16", G, "Wonderful. We'll need a photo of the water.", KF_GER_SMILE, refs=["gerald"], sfx=SFX_G),
 silent("k17", RYAN + "standing on a chair in a flooded kitchen, carefully taking a photo of the water on the floor with his phone." + ONE, 1.0,
        refs=RY, sfx="a phone camera shutter, dripping"),
 s("k18", G, "And a photo of the kitchen before there was water in it.", KF_GER_PEN, refs=["gerald"], sfx=SFX_G),
 s("k19", R, "Why would I have that?", RYAN + "close-up, standing on a chair in a flooded kitchen, phone to his ear, bewildered." + ONE, refs=RY, sfx=SFX_F),
 s("k20", G, "People do.", ger("gently, a kind patient smile.") + ONE, refs=["gerald"], sfx=SFX_G),
 silent("k21", BRAY_FULL + "in a bare white empty flat under one bare bulb, very seriously photographing an empty room with his phone, a ring "
        "light beside him." + ONE, 1.5, refs=["brayden"], mv="in", sfx=SFX_B),
 s("k22", M, "Some people do.", BRAY + "in a bare white kitchen, very seriously photographing the inside of an empty fridge with his phone." + ONE,
   refs=["brayden"], hold=0.3, sfx=SFX_B),
 s("k23", G, "Good news. Your claim's approved. The damage is two hundred and forty dollars. Your deductible is two hundred and fifty.",
   KF_GER_SMILE, refs=["gerald"], hold=0.5, sfx=SFX_G),
 s("k24", G, "So you don't owe us anything.", ger("beaming kindly, palms open.") + ONE, refs=["gerald"], sfx=SFX_G),
 s("k25", R, "...Thank you?", KF_RY_CHAIR, refs=RY, sfx=SFX_F),
 s("k26", G, "And because you made a claim, your price will go up next year.", ger("his warmest smile yet, leaning very slightly forward.") + ONE,
   refs=["gerald"], sfx=SFX_G),
 silent("k27", RYAN_FULL + "standing on a chair in his flooded kitchen, water up to his shins, phone lowered, staring into space; a single sock drifts "
        "past." + ONE, 3.5, refs=RY, mv="out", sfx="a flooded kitchen, slow dripping, silence"),
 # ---------------- THE EXPENSIVE FEAR
 s("x01", M, "That number, the bit you pay yourself, is called the deductible. And it turns out we're very strange about it.",
   "An insurance policy page on a desk with one number circled again and again in thick red pen, a coffee ring next to it." + NO_TEXT, env=True, sfx="quiet room tone"),
 s("x02", M, "In 2010, the economist Justin Sydnor studied home insurance customers in the US. Many of them paid about a hundred dollars a year extra to bring their deductible down from a thousand dollars to five hundred.",
   "A sunny American suburban street of neat detached houses with green lawns and white picket fences." + NO_TEXT, env=True, mv="right",
   sfx="a quiet suburban street, a lawnmower in the distance"),
 card("x03", "Only about four in a hundred of them made a claim in a year. So that hundred dollars bought, on average, less than twenty dollars of protection.",
      "$100 A YEAR", "BUYS LESS THAN $20 OF PROTECTION", bg="#5A3C3C", hold=1.2),
 s("x04", M, "Sydnor's paper calls the level of risk aversion this implies \"implausibly large.\"",
   "An academic economics journal lying open on a desk under a lamp, a magnifying glass resting on it." + NO_TEXT, env=True, sfx="a quiet library"),
 s("x05", M, "We're not scared of disaster. We're scared of a medium-sized bill.",
   RYAN_FULL + "crouching behind his sofa, peeking nervously at a single envelope lying on the living-room floor." + ONE, refs=RY, hold=0.5,
   sfx="a quiet living room, a clock ticking"),
 s("x06", M, "I once bought travel insurance for a weekend in Ohio. I still don't know what I thought was going to happen in Ohio.",
   "A peaceful, sunny small-town American main street with low brick shops and one pigeon on the pavement; in the foreground one hand holds "
   "up a plain folded blank paper ticket. Only that one hand is visible." + NO_TEXT, env=True, hold=1.5, sfx="a sleepy small-town street, one pigeon cooing"),
 s("x07", M, "Which is how Ryan ended up with a three-year protection plan on a fifteen-dollar kettle.",
   RYAN + "in an electrical shop holding a small cheap kettle; beside him a smiling salesman in a shop polo shirt holds up a laminated card with a "
   "big plus sign and a smiling kettle icon. Exactly two people." + NO_TEXT, refs=RY, mv="in", sfx="a quiet electrical shop, beeping tills"),
 s("x08", R, "It's peace of mind.", RYAN + "close-up in an electrical shop, cradling a small kettle in both arms like a baby, sincere." + ONE, refs=RY,
   sfx="a quiet electrical shop"),
 s("x09", I, "Insure the plan.", RYAN + "close-up in an electrical shop holding a small kettle, while " + SHADOW + "." + ONE, refs=RY, sfx="a quiet electrical shop"),
 s("x10", R, "...Can I insure the plan?", RYAN + "in an electrical shop holding a small kettle, turning hopefully to a salesman in a shop polo shirt, "
   "whose eyes light up with delight. Exactly two people." + ONE.replace(" Exactly one person.", ""), refs=RY, hold=1.0, sfx="a quiet electrical shop, a till chime"),
 # ---- moral hazard (added for the 8-minute mark, owner-approved 2026-11-27)
 s("x11", M, "Insurance also changes how we behave. Economists call it moral hazard.",
   RYAN_FULL + "standing at the top of a staircase cheerfully juggling his phone in the air with one hand, completely unbothered." + ONE, refs=RY,
   mv="in", sfx="a quiet hallway, a phone being tossed and caught"),
 s("x12", R, "It's covered.", RYAN + "close-up at the top of a staircase, smiling serenely, his phone mid-air above his hand." + ONE, refs=RY, hold=0.8,
   sfx="a quiet hallway"),
 s("x13", M, "In the 1970s, the RAND Corporation gave thousands of American families different health insurance plans. Families who had to pay most of their own medical bills spent about forty percent less than families who got their care free.",
   "A 1970s doctor's waiting room with orange plastic chairs, wood-panelled walls and a few families waiting patiently, magazines on a low table."
   + NO_TEXT, mv="right", sfx="a quiet waiting room, a clock ticking"),
 s("x14", M, "And for the average person, they weren't measurably less healthy. Though the poorest and sickest did better on some conditions with free care.",
   "A kind doctor gently listening to an older patient's chest with a stethoscope in a calm, sunny consulting room. Exactly two people." + NO_TEXT,
   mv="in", hold=0.5, sfx="a calm consulting room"),
 # ---------------- ABSURD SEQUENCE 3: BRAYDENGUARD
 s("y01", M, "Brayden doesn't believe in insurance.", BRAY + "standing proudly beside a shiny red sports car, arms crossed, grinning; a car key with a "
   "rental key-tag dangles from his hand." + ONE, refs=["brayden"], sfx="a quiet street, birds"),
 s("y02", M, "To be fair, insurance doesn't believe in Brayden.", "A laptop screen showing an online application form with a huge red X stamped "
   "across it." + NO_TEXT, env=True, hold=1.0, sfx="a computer error beep"),
 s("y03", M, "Insurers ask all those questions for a reason. The people keenest to buy insurance are often the ones most likely to need it. Economists call it adverse selection. Brayden calls it a hater.",
   BRAY + "sitting in an outdoor ice bath filming himself on a phone on a selfie stick, grinning, while a big white swan glares at him from the "
   "edge." + ONE, refs=["brayden"], mv="right", sfx="splashing ice water, an angry swan hissing"),
 h("y04", B, "Insurance is for people who plan to fail.", BRAY + "standing by a red sports car, a white swan watching from the background, pointing "
   "at camera, delighted.", "He points at the camera and speaks loudly and delightedly.", sfx="a quiet street, birds"),
 s("y05", M, "So he started his own insurance company.", BRAY + "standing proudly in front of a big shiny banner with a golden shield logo."
   + ONE + NO_TEXT, refs=["brayden"], sfx="a small crowd, a party popper"),
 card("y06", "You pay me forty-nine dollars a month, and if anything bad happens, I send you a motivational voice note.", "BRAYDENGUARD",
      "$49 A MONTH · MOTIVATIONAL VOICE NOTES", spk=B, bg="#3C5A50", sfx="an upbeat app notification sound"),
 s("y07", M, "Eleven people signed up.", "A small tin bucket on a pavement with exactly eleven gold coins at the bottom." + NO_TEXT, env=True,
   sfx="a few coins plinking"),
 s("y08", B, "Hey, champ. Your house didn't burn down. It made room.", "A phone screen showing a chat: a small fire emoji message, then an incoming "
   "voice message shown as a long waveform bar." + NO_TEXT, env=True, hold=0.4, sfx="a phone notification, a gym echo"),
 s("y08b", B, "Champ. Your car got stolen? Now you've got legs.", "A phone screen showing a chat: a small car emoji message, then another incoming "
   "voice message shown as a long waveform bar." + NO_TEXT, env=True, hold=0.4, sfx="a phone notification, a gym echo"),
 s("y09", M, "It was, technically, a bucket.", BRAY + "staring down into a small tin bucket of gold coins on the pavement, thinking hard." + ONE,
   refs=["brayden"], sfx="a quiet street"),
 s("y10", M, "Then Brayden noticed something.", "Close-up looking down into a small tin bucket of gold coins glinting in the sunlight." + NO_TEXT,
   env=True, sfx="coins glinting, a soft chime"),
 h("y11", B, "Bro. The money's just sitting there.", BRAY + "looking down into a small tin bucket of coins, hushed, awed, eyes wide.",
   "He whispers in awe, eyes wide, looking down.", sfx="a quiet street"),
 silent("y12", BRAY + "driving away in a second shiny red sports car, waving; an empty tin bucket left on the pavement behind." + ONE, 2.0,
        refs=["brayden"], mv="right", sfx="a sports car engine roaring away, then silence"),
 s("y13", M, "Two weeks later, the first claim came in.", "A phone on a table lighting up with one new notification bell icon." + NO_TEXT,
   env=True, sfx="a phone notification ping"),
 silent("y14", "A shiny red sports car upside down in a park pond, wheels in the air, and a big white swan standing proudly on top of it." + NO_TEXT,
        4.5, env=True, eng="ltx", sfx="a pond, ducks, a swan hissing", motion="The swan spreads its wings wide on top of the upturned car; gentle "
        "ripples on the pond. Static camera."),
 s("y15", M, "It was Brayden's.", BRAY + "standing soaking wet beside a park pond, dripping, holding his phone, a swan behind him." + ONE,
   refs=["brayden"], hold=0.6, sfx="a pond, dripping water"),
 s("y16", B, "Denied. That swan was a mindset.", BRAY + "at a laptop in a bare white flat, decisively clicking, completely confident." + ONE,
   refs=["brayden"], hold=0.8, sfx=SFX_B),
 # ---------------- THE LOYALTY PENALTY
 s("z01", M, "There's one more trick, and for years it was perfectly legal.", "The tall gleaming tower with a giant tin bucket on top, at night, "
   "with one office window lit." + NO_TEXT, env=True, sfx="a city at night"),
 s("z02", M, "In Britain, if you stayed with the same home or car insurer, your price would quietly creep up, year after year, while new customers got the cheap deal. The industry called it \"price walking.\"",
   RYAN_FULL + "walking wearily on a treadmill while a big price tag tied to a balloon floats higher and higher above his head; behind a glass wall, "
   "small smiling new customers sip champagne." + ONE.replace(" Exactly one person.", "") + NO_TEXT, refs=RY, mv="right", sfx="a treadmill whirring, distant glasses clinking"),
 s("z03", M, "In January 2022, the regulator banned it. A renewal price can't be higher than what a new customer would pay. Britain's Financial Conduct Authority estimated that would save people over five billion dollars in ten years.",
   "A big wooden judge's gavel coming down on a price tag on a desk." + NO_TEXT, env=True, mv="in", sfx="a gavel bang, a quiet room"),
 s("z04", G, "We've noticed you've been very loyal, Ryan.", ger("holding up a small thank-you card, warm.") + ONE + NO_TEXT, refs=["gerald"], sfx=SFX_G),
 h("z05", G, "We're not allowed to do anything about that anymore.", ger("gently regretful, a little sad, eyes lowered."), "He speaks gently and regretfully.",
   hold=1.0, sfx=SFX_G),
 s("z06", R, "Can I cancel, then?", KF_GER_SMILE, refs=["gerald"], sfx=SFX_G),
 s("z07", G, "Of course. Cancellations are done in person.", ger("his warmest smile yet, leaning very slightly forward.") + ONE, refs=["gerald"],
   hold=0.6, sfx=SFX_G),
 s("z08", G, "On a Saturday.", ger("his warmest smile yet, leaning very slightly forward.") + ONE, refs=["gerald"], hold=1.0, sfx=SFX_G),
 # ---------------- THE VERDICT AND THE REVEAL
 s("v01", M, "And to be fair, the bucket mostly does pay. In 2024, natural disasters alone cost insurers a hundred and thirty-seven billion dollars worldwide.",
   "A small town after a storm, seen from above: repair crews in hi-vis fixing roofs, new blue tarps, a crane, sunshine returning." + NO_TEXT,
   env=True, mv="right", sfx="distant hammering, a quiet town"),
 s("v02", M, "And more than half of the damage from those disasters wasn't insured at all.", "A quiet, damaged suburban street in early morning "
   "light after a storm, fallen branches, nobody around." + NO_TEXT, env=True, hold=1.2, sfx="a quiet morning after a storm, birds"),
 s("v03", M, "So, how does insurance work? Everybody pays a little, so that the unlucky few don't lose everything. It's a bet you're hoping to lose.",
   VILLAGE + " at sunrise; small simple villagers dropping coins into the bucket one by one.", mv="in", sfx="a village at dawn, coins plinking"),
 s("v04", M, "The trick is choosing which bets to make. Insure the things that would ruin you: your home, your car, your health, the people who depend on you. For the small stuff, like the kettle, the phone screen or that extra five hundred dollars, you can be your own bucket.",
   RYAN + "in his kitchen in the morning, placing a glass jam jar with a few coins in it on a shelf, a small paper label on the jar." + ONE + NO_TEXT,
   refs=RY, mv="in", sfx="a single coin dropping into a glass jar, a quiet kitchen"),
 h("v05", R, "Eleven years. Best money I never needed.", RYAN + "at his kitchen table in the morning, a glass jar on the shelf behind him, content, "
   "a small smile.", "He speaks quietly and contentedly, a small smile.", sfx=SFX_K),
 s("v06", M, "Nobody's quite sure who owns the bucket.", "The top-floor penthouse office of a tall tower, city lights through huge windows: behind a "
   "huge desk " + FOX + " in a tiny business suit sits with its feet up, counting gold coins, while " + GER.replace("waist-up, ", "").replace("The man", "the man")
   + "stands beside it politely offering a cup of tea." + NO_TEXT, refs=["gerald"], mv="in", hold=3.0, sfx="a quiet penthouse, a teacup clink"),
]
THUMB = dict(text="$240 DAMAGE|$250 DEDUCTIBLE", refs=RY,
             kf=RYAN + "standing on a kitchen chair in his flooded kitchen holding his phone to his ear, shocked, big worried eyes; a sock floating on the "
                "water; outside the glass patio door " + FOX + " floats past in a tiny inflatable swim ring. Exactly one person.")
TAIL = 1.0

# ---------------- MAYA ON CAMERA (owner, 2026-11-27: "show Maya… start videos with her and keep showing her"; design E)
MAYA = ("Flat 2D vector illustration of the young woman from the reference redrawn in a simple flat explainer style, attractive and warm, big "
        "expressive eyes, light warm-tan skin, clear well-drawn eyes and face: long wavy dark brown hair, gold hoop earrings, olive-green overshirt over a cream top, waist-up, ")
STUDIO = "in a cosy, stylish presenter's studio with a warm desk lamp, a bookshelf, a potted plant and a big window behind her, "
_ON = {
    "c01": "sitting on the edge of a desk facing camera with a knowing half-smile, telling a story; through the window behind her " + FOX + " is asleep, curled up in a blue recycling box.",
    "c06": "leaning on the desk towards camera, eyebrows raised, amused, one hand gesturing.",
    "u01": "holding up a small shiny tin bucket next to her face, smiling.",
    "u07": "a sincere warm smile, one hand on her chest.",
    "x05": "deadpan, calm, arms folded, looking straight at camera with a dry little smile.",
    "x06": "laughing a little, embarrassed, holding up a plain blank paper ticket.",
    "y01": "arms crossed, deadpan, a tiny smirk, looking straight at camera.",
    "z01": "leaning towards camera, conspiratorial, one finger raised.",
    "v03": "close-up, sitting at the desk, warm and sincere, smiling, both palms open.",
}
for _s in SHOTS:
    if _s["id"] in _ON:
        _s.update(eng="h3", kf=MAYA + STUDIO + _ON[_s["id"]] + ONE, refs=["maya", "maya_face"], onscreen=True,
                  mv="She speaks to camera naturally and warmly, with small expressive head movements and hand gestures. Static camera. "
                     "Exactly one person; same face and clothes.")

