"""How Do ATMs Actually Work? Approved script: VIDEOS/How Do ATMs Actually Work/SCRIPT FOR REVIEW.md (2026-11-27). 16:9.
Same cast, voices, tempo and helpers as topics/insurance.py. Maya on camera (13 lines, design E). Dollars throughout.
Spoken text is verbatim from the script; Maya paragraphs are split only at sentence ends where the picture changes."""
from topics.insurance import (STYLE, ENV_STYLE, LOOK, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, RYAN_FULL, BRAY, BRAY_FULL, GER, FOX, M, R, B, G,
                              I, h, s, silent, card, CHARS, RY, ger, SHADOW, MAYA, STUDIO, NO_TEXT)  # noqa: F401
FOLDER = "How Do ATMs Actually Work"
ERA = "modern"
LANDSCAPE = True
GAP = 0.25
TAIL = 1.0
MV_MAYA = ("She speaks to camera naturally and warmly, with small expressive head movements and hand gestures. Static camera. "
           "Exactly one person; same face and clothes.")


def maya(id_, text, expr, hold=0.0):
    """Maya on camera in her studio (lip-sync)."""
    return dict(id=id_, spk=M, eng="h3", text=text, kf=MAYA + STUDIO + expr + ONE, refs=["maya", "maya_face"], onscreen=True, mv=MV_MAYA,
                hold=hold, sfx="a quiet studio, soft room tone")


ATM = "standing at a cash machine set into a brick wall on a city street at night, "
KF_ATM = RYAN + ATM + "looking at the screen, "
FLAT = "in a bare white empty flat under one bare bulb, "
SFX_ST = "a city street at night, distant traffic, a faint ATM whirr"
SFX_G = "quiet office, air conditioning hum"
SFX_FL = "empty room echo, a bare bulb buzzing"
SFX_K = "quiet kitchen, a clock ticking"

SHOTS = [
 # ---------------- COLD OPEN: THE WALL
 maya("o01", "You put a piece of plastic into a wall. You type four numbers. And the wall gives you money.",
      "sitting on the edge of her desk facing camera, warm, a hint of wonder."),
 maya("o02", "If that happened once, we'd call it a miracle. Instead, we complain about the fee.", "dry, eyebrows raised, a small knowing smile, clear clean face."),
 s("o03", M, "The person in front of you is always checking their balance. Twice.",
   "A cash machine set into a brick wall on a city street at night; " + FOX + " stands at the machine reading a long receipt, while behind it "
   + RYAN_FULL.replace("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: ", "a young man with ")
   + "waits patiently in the queue. Exactly one person and one fox." + NO_TEXT, refs=RY, mv="in", sfx=SFX_ST),
 s("o04", R, "It's thinking.", KF_ATM + "patient, a little anxious, the screen showing a spinning circle." + ONE + NO_TEXT, refs=RY, sfx=SFX_ST),
 s("o05", M, "It isn't thinking. It's asking.", "Close-up of a cash machine screen at night showing a simple spinning loading circle." + NO_TEXT,
   env=True, mv="in", sfx=SFX_ST),
 card("o06", "So. How do ATMs actually work?", "ATMs?", "HOW DO THEY ACTUALLY WORK", bg="#2E4A62", hold=1.5),
 # ---------------- HOW WE GOT HERE: THE BATH
 maya("h01", "It started in a bath.", "storytelling, leaning forward, a playful smile."),
 s("h02", M, "In the 1960s, a Scottish engineer called John Shepherd-Barron was in the bath, thinking about how annoying it was that you could only get your own money when the bank was open.",
   "A 1960s bathroom: a middle-aged man with a neat moustache lying in a bubble bath with a rubber duck, staring thoughtfully at the ceiling."
   + ONE, mv="in", sfx="a quiet bathroom, a dripping tap"),
 s("h03", M, "Then he thought of a chocolate machine. If a machine could give you a chocolate bar, why couldn't it give you cash?",
   "A vintage 1960s chocolate vending machine on a station platform; in its tray lie a chocolate bar and a folded banknote side by side." + NO_TEXT,
   env=True, sfx="a vending machine clunk, a soft ding"),
 s("h04", M, "On the twenty-seventh of June, 1967, the world's first cash machine opened at a Barclays bank in Enfield, north London. The first person to use it was a comedy actor called Reg Varney.",
   "A 1960s high street: a small excited crowd in coats and hats watches as a red velvet curtain is pulled back from a chunky metal machine set "
   "into a bank wall." + NO_TEXT, mv="right", sfx="polite 1960s applause, a small crowd"),
 card("h05", "It gave out one-pound notes, up to a limit of ten pounds. About twenty-eight dollars at the time.", "£10 LIMIT", "ABOUT $28 IN 1967",
      bg="#5A3C3C", sfx="paper rustling"),
 s("h06", M, "Within days, Barclays had ordered six more machines. Then another fifty.",
   "A 1960s factory floor with a long row of identical chunky cash machines being assembled by workers in overalls." + NO_TEXT, mv="right",
   sfx="a busy factory, clanking"),
 s("h07", M, "America got its first one two years later, on the second of September, 1969, at Chemical Bank in Rockville Centre, New York. The newspaper ad said: \"On Sept. 2, our bank will open at 9:00 and never close again.\"",
   "A delighted man in a 1960s hat holding up a newspaper advert showing a cartoon bank building wearing sunglasses." + ONE + NO_TEXT, mv="in",
   sfx="a 1960s street, a newspaper rustling"),
 maya("h08", "Which, for a bank, was either a promise or a threat.", "amused, one eyebrow raised."),
 s("h09", M, "There were no plastic cards yet. Instead, you used a special paper cheque, impregnated with carbon-14, which is mildly radioactive.",
   "An old paper bank cheque lying on a desk, glowing with a faint warm yellow halo, a tiny radiation symbol sticker in its corner." + NO_TEXT,
   env=True, mv="in", sfx="a faint electrical hum"),
 s("h10", R, "The first cash machine was radioactive.", RYAN + "at his kitchen table in the morning, his mug frozen halfway to his mouth, eyes wide." + ONE,
   refs=RY, sfx=SFX_K),
 s("h11", M, "Mildly.", RYAN + "at his kitchen table, very slowly lowering his mug, unsettled." + ONE, refs=RY, hold=0.4, sfx=SFX_K),
 s("h12", M, "And then there was the number. Shepherd-Barron wanted a six-digit code, because he could remember his six-digit army number. So he checked with his wife, Caroline.",
   "A 1960s kitchen table: a man with a neat moustache eagerly holding up six fingers, and his smiling wife holding a cup of tea. Exactly two people.",
   mv="in", sfx="a 1960s kitchen, a teacup on a saucer"),
 s("h13", M, "Over the kitchen table, she said she could only remember four.",
   "The same 1960s kitchen table: the wife calmly holding up four fingers over her cup of tea while the man looks at his own six fingers. Exactly two people.",
   hold=1.0, sfx="a 1960s kitchen, a clock ticking"),
 maya("h14", "That's it. That's why your PIN is four digits. One woman, one cup of tea, the entire planet.",
      "delighted, slightly incredulous, holding up one hand with exactly four fingers raised and the thumb folded in."),
 s("h15", R, "Mine's my birthday.", KF_ATM + "typing on the keypad, quietly proud." + ONE, refs=RY, sfx=SFX_ST),
 maya("h16", "Don't.", "instant, flat, deadpan, one hand raised like a stop sign.", hold=0.6),
 # ---------------- ABSURD SEQUENCE 1: THE JOURNEY
 s("j01", M, "Here's the strange part. The machine doesn't know how much money you have.",
   "A cash machine in a brick wall at night, its screen showing one big simple question mark icon." + NO_TEXT, env=True, mv="in", sfx=SFX_ST),
 s("j02", M, "When you type your PIN, it's scrambled inside the keypad before it goes anywhere. Then the machine writes a tiny message: this card, this PIN, this much money, please.",
   "Close-up of one hand typing on a cash machine keypad, little jumbled coloured shapes floating up out of the keys. Only that one hand is visible."
   + NO_TEXT, env=True, mv="in", sfx="four soft key beeps"),
 silent("j03", "Night rooftops of a city seen from above; a small white paper plane flies out from a cash machine in a brick wall below and away over "
        "the roofs." + NO_TEXT, 4.0, env=True, eng="ltx", sfx="a whoosh, night wind",
        motion="The small white paper plane flies up and away over the night rooftops in a long arc. Static camera."),
 s("j04", M, "That message goes to a network that connects thousands of banks, and the network passes it to your bank, wherever it is.",
   "A vast busy sorting office full of tiny clerks catching small white paper planes and throwing them on; on the wall a big billboard of "
   + FOX + " in a headset giving a thumbs up." + NO_TEXT, mv="right", sfx="a busy sorting office, paper fluttering, chatter"),
 s("j05", M, "And at your bank, someone says yes or no.", "A small softly lit office doorway; a little white paper plane floats in through the "
   "open door towards a desk with a box of tissues and a framed child's drawing of a smiling sun on the wall." + NO_TEXT, env=True, sfx=SFX_G),
 h("j06", G, "Ryan. Nobody's in trouble. I've moved to Authorisations.", ger("holding a small white paper plane in one hand, warm smile."),
   "He speaks softly and reassuringly, smiling.", sfx=SFX_G),
 s("j07", G, "You'd like forty dollars. You have fourteen.", ger("unfolding a small white paper plane and reading it kindly.") + ONE, refs=["gerald"], sfx=SFX_G),
 s("j08", R, "Can I have fourteen, then?", KF_ATM + "hopeful." + ONE, refs=RY, sfx=SFX_ST),
 s("j09", G, "Of course. The machine only does twenties.", ger("brightly, as if it's good news.") + ONE, refs=["gerald"], sfx=SFX_G),
 card("j10", "", "$20", "AMOUNTS IN MULTIPLES OF TWENTY", bg="#5A3C3C", dur=1.5),
 h("j11", R, "So my money's in there. I just can't have it.", KF_ATM + "a quiet realisation.", "He speaks quietly, realising, staring at the screen.",
   sfx=SFX_ST),
 s("j12", G, "Good news, though. We can lend you the other six dollars.", ger("brightening, leaning in a little.") + ONE, refs=["gerald"], sfx=SFX_G),
 s("j13", R, "Really?", KF_ATM + "hopeful, eyebrows up." + ONE, refs=RY, sfx=SFX_ST),
 s("j14", G, "Of course. There's a small overdraft fee. Twenty-six dollars and seventy-seven cents.",
   ger("his warmest smile yet, leaning very slightly forward, clean soft pink cheeks.") + ONE, refs=["gerald"], sfx=SFX_G),
 s("j15", R, "To borrow six dollars.", KF_ATM + "very quiet, deflated, shoulders dropping." + ONE, refs=RY, sfx=SFX_ST),
 card("j16", "That's not a joke number. In 2025, Bankrate put the average overdraft fee at twenty-six dollars and seventy-seven cents.",
      "$26.77", "AVERAGE US OVERDRAFT FEE · 2025", bg="#5A3C3C", hold=0.4),
 s("j17", G, "Would you like a receipt? It'll say fourteen dollars.", ger("helpfully holding up a long paper receipt.") + ONE + NO_TEXT,
   refs=["gerald"], sfx=SFX_G),
 s("j18", R, "I know it's fourteen dollars.", KF_ATM + "tired, patient." + ONE, refs=RY, sfx=SFX_ST),
 s("j19", G, "Most people like to check twice.", ger("gently, a kind patient smile.") + ONE, refs=["gerald"], hold=0.5, sfx=SFX_G),
 s("j20", M, "All of that, there and back, usually takes a few seconds. Then the machine counts out notes from locked boxes inside it, called cassettes, and checks they haven't stuck together.",
   "A cutaway view inside a cash machine: neat metal cassettes stacked with banknotes, little rollers and belts, a tiny sensor eye blinking." + NO_TEXT,
   env=True, mv="in", sfx="a soft mechanical shuffle of notes"),
 s("j21", M, "And then there's the fee.", KF_ATM + "the screen glowing, a little wary." + ONE + NO_TEXT, refs=RY, sfx=SFX_ST),
 card("j22", "In 2025, Bankrate found the average cost of using an ATM that isn't your bank's was four dollars and eighty-six cents. That's the machine's own charge, plus a separate charge from your own bank for going somewhere else.",
      "$4.86", "TO USE SOMEONE ELSE'S ATM · US AVERAGE 2025", bg="#2E4A62", hold=0.4),
 s("j23", M, "When Bankrate started tracking it in 1998, the same thing cost a dollar ninety-seven. Do it once a week now, and it's about two hundred and fifty dollars a year.",
   "A wall calendar with a small cash-machine sticker on every single week." + NO_TEXT, env=True, mv="in", sfx="a quiet room, a clock ticking"),
 s("j24", R, "So to take out twenty dollars, I pay nearly five.", KF_ATM + "holding one banknote up, doing the maths, unimpressed." + ONE, refs=RY, sfx=SFX_ST),
 maya("j25", "It's the only shop where you pay to collect your own shopping.", "dry, arms folded, a tiny smile."),
 maya("j26", "I once used an ATM abroad, panicked about the exchange rate, and took out what turned out to be about four dollars. The fee was more than the money.",
      "laughing a little, embarrassed, holding up a long paper receipt.", hold=0.8),
 # ---------------- WHO OWNS THE WALL
 s("w01", M, "And a lot of those machines don't belong to banks at all. Shops, bars and private owners can buy an ATM, fill it with cash, set a fee, and keep it.",
   "A cosy dim bar with one lonely cash machine glowing in the corner next to the toilets." + NO_TEXT, env=True, mv="right", sfx="bar chatter, glasses clinking"),
 s("w02", M, "To be fair to them, an ATM isn't free to run. Someone has to buy the machine, fill it with cash, pay for the connection, and send an armoured truck when it's empty.",
   "An armoured truck parked outside a corner shop; a guard carrying a metal cash box; " + FOX + " watching from a bus stop. Exactly one person." + NO_TEXT,
   mv="right", sfx="a heavy van door, street noise"),
 s("w03", M, "There are somewhere around half a million ATMs in the United States, and about three million around the world.",
   "A flat world map on a dark navy background covered in many tiny glowing dots." + NO_TEXT, env=True, mv="out", sfx="quiet room tone"),
 maya("w04", "There are even two in Antarctica. At McMurdo Station, run by Wells Fargo. Only one of them works at a time.", "genuinely delighted, hands open."),
 dict(silent("w05", "Inside a small snowy research-station hut: two cash machines side by side, one with its panel open and parts missing; through the "
             "window " + FOX + " in a tiny parka waits patiently in a queue of one." + NO_TEXT, 0, env=True, eng="ltx", sfx="howling wind, a hut creaking",
             motion="Snow blows past the window; the small fox in its parka shuffles forward one step. Static camera."),
      text="The other one is spare parts.", hold=2.0),
 # ---------------- ABSURD SEQUENCE 2: BRAYDEN'S PASSIVE INCOME
 s("b01", M, "Which gave Brayden an idea.", BRAY + FLAT + "staring at his phone, his eyes lighting up." + ONE, refs=["brayden"], sfx=SFX_FL),
 h("b02", B, "Bro. I own an ATM now. Passive income.", BRAY + FLAT + "standing proudly next to a brand-new cash machine, delighted.",
   "He gestures proudly at the machine and speaks loudly, thrilled.", sfx=SFX_FL),
 s("b03", M, "He set the fee at nine ninety-nine.", "Close-up of a cash machine screen showing one big shiny golden price-tag icon." + NO_TEXT,
   env=True, sfx="a cash register ding"),
 s("b04", M, "He installed it in his flat.", "A completely empty white flat with one bare bulb and a single cash machine glowing in the corner." + NO_TEXT,
   env=True, mv="out", hold=2.0, sfx="empty room, a bare bulb buzzing, silence"),
 s("b06", M, "Nobody came.", "The same empty white flat: the lonely cash machine in the corner, one cobweb on it." + NO_TEXT, env=True, sfx=SFX_FL),
 s("b07", M, "Then, one evening, a customer.", RYAN_FULL + "standing awkwardly in a bare white empty flat in front of a cash machine, while "
   + BRAY.replace("The man from the reference", "a blond man").replace("waist-up, ", "") + "beams beside it. Exactly two people.", refs=["ryan", "brayden"],
   sfx=SFX_FL),
 s("b08", R, "I just needed twenty dollars for a pizza.", RYAN + "alone in a bare white empty flat, standing at a cash machine, polite, a little awkward. Only one person in the whole picture." + ONE, refs=RY, sfx=SFX_FL),
 s("b09", M, "Ryan paid nine ninety-nine to Brayden, and a dollar sixty-four to his own bank, for a twenty-dollar pizza.",
   "A sad cardboard pizza box on a kitchen counter next to a very long paper receipt." + NO_TEXT, env=True, sfx="a quiet kitchen"),
 s("b10", B, "You're investing in me, bro.", BRAY + FLAT + "with his hand on the shoulder of a young man in an orange hoodie, beaming. Exactly two people.",
   refs=["brayden", "ryan"], sfx=SFX_FL),
 s("b11", M, "He never came back.", "The front door of a bare white flat closing; a cash machine alone in the corner." + NO_TEXT, env=True, hold=0.5,
   sfx="a door closing, silence"),
 s("b12", M, "Then Brayden found out something about owning an ATM. It doesn't come with money. You have to fill it yourself.",
   BRAY + FLAT + "feeding a few of his own plain pale banknotes, one by one, into the open back of a cash machine. Clean simple shapes." + ONE, refs=["brayden"], sfx=SFX_FL),
 s("b13", B, "So I'm the bank now.", BRAY + FLAT + "leaning on his cash machine, confident, arms crossed." + ONE, refs=["brayden"], sfx=SFX_FL),
 s("b14", M, "The machine ran out by Wednesday. So he paid an armoured truck to bring his own money back to his own flat.",
   "An armoured truck squeezed into a narrow residential street; two guards carry one small metal cash box up the front steps while the blond man "
   "from the reference holds the door open. Exactly three people." + NO_TEXT, refs=["brayden"], mv="in", sfx="a heavy van door, footsteps on stairs"),
 s("b15", M, "Then his rent was due, so he took his money out again.", BRAY + FLAT + "typing on the keypad of his own cash machine." + ONE,
   refs=["brayden"], sfx="key beeps, an empty room"),
 s("b16", M, "The machine charged him nine ninety-nine, which went to him. And his own bank charged him a dollar sixty-four for using an ATM that wasn't theirs.",
   BRAY + FLAT + "holding his cash in one hand and a receipt in the other, puzzled." + ONE + NO_TEXT, refs=["brayden"], sfx=SFX_FL),
 s("b17", B, "Every time I take my money out, I make ten bucks.", BRAY + FLAT + "counting three plain pale-green banknotes in his hands, beaming. Clean simple flat shapes." + ONE, refs=["brayden"], sfx=SFX_FL),
 maya("b18", "He doesn't. He loses a dollar sixty-four.", "flat, deadpan, arms folded."),
 h("b19", B, "Bro, I'm vertically integrated.", BRAY + FLAT + "next to his cash machine, serene, one hand on his heart.",
   "He speaks calmly and serenely, completely sure of himself.", hold=0.8, sfx=SFX_FL),
 # ---------------- THE DARK SIDE
 s("d01", M, "Not everyone at an ATM is there to take out their own money.", "A cash machine in a brick wall at night under a flickering streetlight, "
   "nobody around." + NO_TEXT, env=True, mv="in", sfx="a quiet street at night, a buzzing streetlight"),
 silent("d02", "Close-up of a cash machine: one hand pulling a thick fake grey plastic cover off the card slot, revealing tangled wires, a small circuit "
        "board and a tiny pinhole camera hidden behind it. No banknotes." + NO_TEXT, 2.0, env=True, mv="in", sfx="a soft plastic click"),
 s("d03", M, "Skimmers are fake card readers that fit over the real one, often with a hidden camera to watch your PIN. The FBI estimates skimming costs banks and customers more than a billion dollars a year.",
   "An evidence table under a lamp with several small fake card-reader devices and tiny cameras laid out in neat rows." + NO_TEXT, env=True,
   mv="right", sfx="a quiet room, a camera shutter"),
 s("d04", M, "So, cover the keypad when you type. And if anything on the machine looks loose, or a bit different, use a different machine.",
   "Close-up of a cash machine keypad: one hand types while the other hand covers it like a little roof. Only those two hands are visible." + NO_TEXT,
   env=True, mv="in", sfx="key beeps"),
 s("d05", M, "Then there's jackpotting. In 2010, a security researcher called Barnaby Jack stood on stage at the Black Hat hacking conference and made two ATMs spit out cash, live, in front of an audience.",
   "A conference stage under spotlights with two cash machines side by side and a presenter in a dark shirt standing between them; an audience "
   "in silhouette in the foreground." + NO_TEXT, mv="right", sfx="a conference hall, murmuring"),
 silent("d06", "A cash machine on a conference stage under spotlights, banknotes bursting out of it into the air; an audience in silhouette." + NO_TEXT,
        3.5, env=True, eng="ltx", sfx="a crowd gasp, then cheering",
        motion="Banknotes stream out of the cash machine and flutter up into the air under the spotlights. Static camera."),
 s("d07", M, "He did it to show the manufacturers how, so they'd fix it. Criminals have since used similar tricks for real.",
   "An engineer in a workshop carefully fixing a cash machine laid open on a workbench, tools all around." + ONE + NO_TEXT, mv="in",
   sfx="a workshop, a screwdriver turning"),
 maya("d08", "Part of the problem was the software.", "conspiratorial, leaning towards camera."),
 s("d09", M, "In 2014, when Microsoft stopped supporting Windows XP, an estimated ninety-five percent of the world's ATMs were still running it.",
   "A cash machine with its front panel open, revealing a chunky old beige computer inside with a small monitor showing a plain blue screen."
   + NO_TEXT, env=True, mv="in", sfx="an old computer fan whirring"),
 s("d10", R, "The cash machine is older than my phone.", KF_ATM + "squinting at it suspiciously." + ONE, refs=RY, sfx=SFX_ST),
 s("d11", I, "Type your PIN backwards. The police will come.", KF_ATM + "close-up, uneasy, while " + SHADOW + "." + ONE, refs=RY, sfx=SFX_ST),
 s("d12", M, "They won't. That's a myth. Fact-checkers have looked into it more than once: entering your PIN backwards doesn't summon anyone.",
   "A quiet empty city street at night; one police car parked far away with its lights off." + NO_TEXT, env=True, mv="out",
   sfx="a quiet street at night, crickets"),
 s("d13", R, "I was going to do it for fun.", KF_ATM + "slightly disappointed." + ONE, refs=RY, hold=0.5, sfx=SFX_ST),
 # ---------------- THE VERDICT AND THE REVEAL
 s("v01", M, "Fewer of us use cash every year. In 2025, the Federal Reserve found cash made up just fourteen percent of payments in the US. But eighty-one percent of people had still used cash in the past month.",
   "A wallet with a few banknotes on a café table next to a phone and a coffee cup." + NO_TEXT, env=True, mv="in", sfx="a quiet café"),
 s("v02", M, "Cash is the thing we keep for when everything else goes wrong. And the ATM is how we get it.",
   "A city street during a power cut at night, all the windows dark, one cash machine still glowing and a short calm queue in front of it." + NO_TEXT,
   mv="in", sfx="a quiet street, a generator humming"),
 maya("v03", "A machine on your street asks a bank that might be thousands of miles away whether you're good for forty dollars. And it usually gets an answer before you've finished putting your card away.",
      "sitting on the edge of her desk, sincere and warm, open hands."),
 s("v04", M, "More and more machines don't even need the card any more. You can tap your phone instead, and the same message makes the same journey.",
   "Close-up of one hand tapping a phone against the contactless reader of a cash machine, a tiny white paper plane rising from it. Only that one "
   "hand is visible." + NO_TEXT, env=True, mv="in", sfx="a soft contactless beep"),
 s("v05", M, "So use your own bank's machines when you can. In the US, a machine that charges a fee has to tell you how much before you're committed, so read that screen and feel free to cancel. Cover the keypad. Pick a PIN that isn't your birthday.",
   KF_ATM + "carefully covering the keypad with one hand while typing, responsible." + ONE + NO_TEXT, refs=RY, mv="in", sfx=SFX_ST),
 s("v06", R, "I'm changing it.", RYAN + "close-up at a cash machine at night, determined, nodding." + ONE, refs=RY, sfx=SFX_ST),
 s("v07", M, "And if you've ever wondered whether there's a tiny person inside the machine, counting out your notes...",
   "A cash machine in a brick wall at night, a single banknote sliding out of its slot." + NO_TEXT, env=True, mv="in", sfx="a soft note-dispensing whirr"),
 s("v08", M, "There isn't.", "Close-up of the cash machine's slot at night, quiet and still." + NO_TEXT, env=True, hold=0.3, sfx=SFX_ST),
 silent("v09", "A cutaway inside a cash machine lit by a tiny desk lamp: " + FOX + " wearing a green banker's visor sits among stacks of banknotes, "
        "counting them and licking its thumb." + NO_TEXT, 3.0, env=True, mv="in", sfx="paper notes being counted, a tiny lamp click"),
 maya("v10", "Usually.", "a tiny shrug, deadpan.", hold=1.5),
]
THUMB = dict(text="WHY IS YOUR PIN|ONLY 4 DIGITS?", refs=["maya", "maya_face"],
             kf=MAYA + "standing next to a cash machine set into a brick wall on a city street at night, holding up one open hand beside her face with exactly four "
                "fingers raised and the thumb folded across the palm, a warm knowing smile, symmetrical even eyes. Exactly one person.")
