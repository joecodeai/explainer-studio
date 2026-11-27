"""Why Is Everything a Subscription Now? Final approved script (VIDEOS/Why Is Everything a Subscription Now/SCRIPT FOR REVIEW.md, Part B), 16:9, about 9-10 minutes.
Follow-up to topics/hustle.py: same cast, voices, tempo, helpers and style family (palette shifted to frost blue + heater orange).
Cast: Maya (narrator), Ryan (benny), Brayden, Gerald, Inner Voice; Future Ryan never speaks (own ref sheet "futureryan").
Script marks: 8 x LIPSYNC -> h(); every OVER line -> s() (or a card when the line plays over an edit card); 4 x MOTION -> eng="ltx".
Spoken text is verbatim from the script; Maya paragraphs are split only at sentence ends where the picture changes.
(beat) = hold 0.5 on the shot before; a timed hold = hold on the shot before or a silent() shot with dur.
If the measured cut is under 9:30, the script's cheap fix is longer holds: r24 rain 2->4, rooms r20-r23, c07 Brayden 2->3, l06 office 1.5->3, v14 fox.
Sources: Part 6 of the script document."""
from topics.hustle import (STYLE as _H_STYLE, ENV_STYLE as _H_ENV, LOOK, CHARS as _H_CHARS, VOICE_REF, H3_REF_KF, TEMPO, ONE, RYAN, BRAY,
                           GER, GER_ROOM, RY_ROOM, FOX, M, R, B, G, I, h, s, silent, card as _card)
FOLDER = "Why Is Everything a Subscription Now"
ERA = "modern"
LANDSCAPE = True
GAP = 0.25
_PAL = "Warm palette of sunrise orange, teal, cream, navy and mustard."
assert _PAL in _H_STYLE and _PAL in _H_ENV
STYLE = _H_STYLE.replace(_PAL, "Palette of frosty pale blue, warm heater orange, cream, navy and teal.")
ENV_STYLE = _H_ENV.replace(_PAL, "Palette of frosty pale blue, warm heater orange, cream, navy and teal.")
CHARS = dict(_H_CHARS)          # brayden + gerald: identical descriptions to hustle.py (copy its refs/ to keep the exact same faces)
CHARS["futureryan"] = ("a calm, healthy, athletic version of a young man as a simple flat vector character: thick curly dark brown hair, tanned "
                       "skin, broad shoulders, serene smile, teal sweatband, fitted teal sports top, grey joggers, white trainers, small round "
                       "head, dot eyes.")
RY = ["ryan", "ryan_face"]
RY_F = ["ryan", "futureryan"]          # two-person shots: first reference = Ryan, second = Future Ryan
RYAN_FULL = RYAN.replace("waist-up, ", "")
BRAY_FULL = BRAY.replace("waist-up, ", "")
FUT = ("The athletic man from the reference (thick curly dark brown hair, tanned, broad-shouldered, serene, teal sweatband, teal "
       "sports top), waist-up, ")
FUT2 = ("his future self from the second reference: the same thick curly dark brown hair, but tanned, broad-shouldered and serene, in a teal "
        "sweatband and teal sports top")
SHADOW = "a tiny dark impish shadow creature with two glowing eyes sits on his shoulder, leaning to his ear and whispering"
GER_RET = GER + "wearing a small headset, " + GER_ROOM          # Gerald now works in Retention: same office, same framed sun drawing


def ger(expr):
    """Gerald in his Retention office with a different expression (GER_ROOM ends on 'warm gentle smile.')."""
    return GER_RET.replace("warm gentle smile.", expr)


def ry_ret(expr):
    """Ryan's face across the table in Gerald's office (the listener shot most OVER lines play on)."""
    return RYAN + RY_ROOM + expr + ONE


def card(id_, text, big, small, bg="#2E4A62", accent="#F2C14E", sfx="quiet room tone", hold=0.0, spk=M, dur=None, size=None):
    """hustle.card plus: spk (a character line playing over a card), dur (silent card), size (big-text font size)."""
    d = _card(id_, text, big, small, bg=bg, accent=accent, sfx=sfx, hold=hold)
    d["spk"] = spk
    if dur: d["dur"] = dur
    if size: d["card"]["size"] = size
    return d


# ---------------- keyframes the reel reuses verbatim (so the images match)
KF_CAR = (RYAN + "sitting in the driver's seat of a small, plain, second-hand grey car in a frosty car park on a winter morning, seen through "
          "the windscreen: gloves on, breath fogging, hands tucked into his armpits, shivering; on the car's bonnet " + FOX + " is curled up "
          "on the warm engine, eyes closed, blissful." + ONE)
KF_XRAY = ("A flat diagram-style X-ray cutaway of a car seat on a dark navy background: warm orange heating coils glowing inside the cushion "
           "and backrest, and one tiny gold padlock fixed on the coils.")
KF_RADIATOR = (RYAN + "sitting in the driver's seat of a small plain grey car on a frosty morning, gloves on, breath fogging, shivering, "
               "glancing down at the seat, honest and slightly hurt.")
MV_RADIATOR = "He shivers, glances down at the seat and speaks honestly and a little hurt, breath fogging."
KF_LOT = "A frosty car park at dawn with rows of plain grey cars covered in white frost, pale winter sky."
KF_BRAY_SEAT = (BRAY + "sitting in the driver's seat of an identical plain grey car in a frosty car park, sunglasses on in winter, the seat "
                "glowing warm orange beneath him, eyes closed in bliss, steam rising off his shoulders; a car key with a rental key-tag "
                "swings from the ignition." + ONE)
KF_CAFE = (RYAN + "wearing an apron, behind a small café counter on a sunny Saturday, tired, drying a cup, bright sunshine in the empty street "
           "outside the window." + ONE)
KF_WAIT = ("A beige waiting room: a plain ticket machine, rows of plastic chairs, one wilting plant, a box of tissues on every seat; on one "
           "chair sits " + FOX + " in reading glasses, holding a small plain paper ticket, with a long grey beard that reaches the floor.")
KF_SHADOW_GER = ry_ret("staring ahead, uneasy, while " + SHADOW + ".")
KF_GER_LISTEN = ger("listening patiently, hands folded on his notepad, calm gentle smile.") + ONE
KF_INPERSON = ger("his warmest smile yet, leaning very slightly forward.")
MV_INPERSON = "He smiles his warmest smile and speaks very softly and slowly."
KF_RAIN = (RYAN_FULL + "stepping out of a building into a grey city street on a rainy Monday morning, commuters with coffee cups hurrying past "
           "under umbrellas, a bin lorry in the road, grey sky.")
KF_TROY = ("A flat illustration of an ancient walled city under siege at dusk, a giant wooden horse standing outside the gates, campfires "
           "and tents on the plain.")
KF_RY_RADIATOR = (RYAN + "sitting back at his kitchen table in the evening, resting one hand on an old white radiator under the window, "
                  "quiet, a phone on the table." + ONE)
KF_FOX_END = ("The frosty car park from the opening: inside a small plain grey car, " + FOX + " in a tiny scarf sits in the driver's seat, the "
              "seat glowing warm orange beneath it.")
MV_FOX_END = "The small orange fox turns round once and curls up on the warm glowing seat, eyes closing. Static camera."
SFX_LOT = "frosty car park on a winter morning, light wind"
SFX_RET = "quiet office, air conditioning hum"

SHOTS = [
 # ---------------- COLD OPEN: THE HEATED SEAT
 s("c01", M, "In 2022, BMW started offering British drivers heated front seats. For about eighteen dollars a month.", KF_CAR, refs=RY, sfx=SFX_LOT),
 card("c02", "", "$18", "HEATED SEATS · A MONTH · BMW UK 2022", dur=1.5, sfx="frosty car park, wind"),
 s("c03", M, "The heaters were already inside the seats. Fitted at the factory. Customers weren't paying for heat. They were paying for permission.",
   KF_XRAY, env=True, hold=0.5, sfx="quiet car interior, a faint electrical hum"),
 h("c04", R, "It's right there. It's like sitting on a radiator that isn't speaking to me.", KF_RADIATOR, MV_RADIATOR, hold=1.0,
   sfx="inside a cold parked car, winter wind outside"),
 s("c05", M, "In 2023, BMW dropped the idea. Not many people signed up.", KF_LOT, env=True, mv="out", hold=0.5, sfx=SFX_LOT),
 s("c06", M, "Not many.", "A frosty empty car park at dawn with just one lonely plain grey car parked in the middle.", env=True, mv="in", sfx=SFX_LOT),
 silent("c07", KF_BRAY_SEAT, 3.0, refs=["brayden"], mv="in", sfx="a car heater fan humming, a contented sigh"),
 card("c08", "", "MONTHLY", "GYM · MEAL KIT · LANGUAGE APP · WEEKEND PLUS", dur=2.0, sfx="a phone buzzing inside a cold car"),
 s("c09", R, "I'm still paying for Weekend Plus.",
   "Close-up inside a cold parked car: one hand in a black winter glove, with an orange hoodie cuff, holds a phone whose screen shows a "
   "simple list of coloured rows, small app-icon blobs and grey bars. Only that one hand is visible.", env=True, mv="in",
   sfx="inside a cold parked car, wind"),
 s("c10", M, "He hasn't had a weekend since he signed up. He works Saturdays now. To pay for Weekend Plus.", KF_CAFE.replace("tired, drying", "tired, lips together, drying"), refs=RY, hold=1.0,
   sfx="small café on a Saturday, a coffee machine hissing"),
 card("c11", "So. Why is everything a subscription now?", "NOW?", "WHY IS EVERYTHING A SUBSCRIPTION", bg="#3C5A50", hold=1.5),
 # ---------------- HOW WE GOT HERE
 s("h01", M, "Subscriptions used to be for things that actually run out. Milk. Newspapers.",
   "A doorstep at dawn with two glass milk bottles and a rolled-up newspaper tied with string.", env=True, sfx="quiet street at dawn, milk bottles clinking"),
 s("h02", M, "Then, in 2013, Adobe announced that new versions of Photoshop would only come by subscription.",
   "A plain cardboard software box with a blank colourful cover and a shiny disc beside it, on a tidy desk.", env=True, mv="right", sfx="quiet office"),
 silent("h03", "A museum display case: on a velvet cushion inside sits a plain boxed piece of software with a blank cover; a school group of "
        "small children and their teacher stand around it staring in wonder, the way you'd stare at a fossil.", 1.5, mv="in",
        sfx="quiet museum hall, children whispering, footsteps echoing"),
 s("h04", R, "I had one of those. You put it on a shelf, and it was just yours.",
   "A museum display case: on a velvet cushion inside sits a plain boxed piece of software with a blank cover; a school group of "
   "small children and their teacher stand around it staring in wonder, the way you'd stare at a fossil.", mv="out",
   sfx="quiet museum hall, children whispering, footsteps echoing"),
 s("h05", M, "Then cars. Printers. Toothbrushes.",
   "Three objects in a row on a plain background: a small car, a desktop printer and an electric toothbrush, each with a thin glowing string "
   "rising from it up out of the frame like a puppet string.", env=True, mv="right"),
 s("h06", M, "And companies worked out that their most valuable customer isn't the one who loves the product. It's the one who's forgotten about it.",
   "A dusty exercise bike in a dim corner of a spare room, draped with clothes, a cobweb between its handlebars.", env=True, sfx="quiet spare room, a clock ticking"),
 s("h07", M, "To be fair, some of it is brilliant. Nearly any song you can think of, on a bus, for a monthly fee. Teenage me would have wept.",
   "A happy young woman on a city bus wearing big headphones, eyes closed, smiling, the city passing by the window." + ONE,
   sfx="city bus interior, engine hum"),
 s("h08", M, "I also pay for a meditation app. I've opened it twice. Every morning it sends me a notification reminding me to breathe.",
   "A phone on a bedside table at dawn, its screen lit with one calm notification bubble with a simple lotus flower icon.", env=True, hold=0.5,
   sfx="quiet bedroom at dawn, a soft phone chime"),
 s("h09", M, "I still breathe. But now it's out of spite.",
   "The same phone lying face down on the bedside table, a mug of black coffee steaming beside it.", env=True, mv="out", hold=1.0,
   sfx="quiet bedroom at dawn, birds outside"),
 # ---------------- THE TEN-SECOND GUESS
 s("q01", M, "In 2022, the research firm C plus R gave a thousand Americans ten seconds to guess what they spent on subscriptions each month.",
   "A row of ordinary people sitting in a plain room, each staring hard at a big stopwatch held up in front of them, thinking.", mv="right",
   sfx="a stopwatch ticking, a quiet room"),
 card("q02", "The average guess was eighty-six dollars.", "$86", "THE GUESS · A MONTH", sfx="quiet room tone"),
 s("q03", M, "Then they listed every subscription, one by one.",
   "A very long paper receipt unrolling off a desk and across the floor, covered in rows of simple grey bars.", env=True, mv="left", sfx="paper unrolling"),
 card("q04", "The average came to two hundred and nineteen.", "$219", "THE LIST · A MONTH", bg="#5A3C3C", hold=1.0, sfx="a single heavy thud"),
 card("q05", "And forty-two percent admitted they'd stopped using something they were still paying for.", "42%", "STILL PAYING · STOPPED USING",
      sfx="quiet room tone"),
 s("q06", I, "Don't open the statement. If you don't look, it's free.",
   RYAN + "close-up at his kitchen table at night, staring at his phone, uneasy, while " + SHADOW + " with delight." + ONE, refs=RY,
   sfx="quiet flat at night, a fridge humming"),
 silent("q07", RYAN + "at his kitchen table at night, carefully placing his phone face down on the table." + ONE, 1.0, refs=RY, mv="in",
        sfx="a phone set down on a wooden table"),
 silent("q08", "A phone standing upright on a kitchen table, propped against the wall with its screen facing the wall.", 1.5, env=True, mv="in",
        sfx="quiet kitchen at night"),
 # ---------------- ABSURD SEQUENCE 1: FUTURE RYAN
 s("f01", M, "So who is signing us up for all this?",
   RYAN + "standing in his kitchen scratching his head, looking at a pile of unopened delivery boxes on the counter." + ONE, refs=RY, sfx="quiet kitchen"),
 s("f02", M, "In 2006, two economists published a study of three American gyms.",
   "Three plain gym buildings side by side on a sunny street, big windows showing rows of empty treadmills.", env=True, mv="right",
   sfx="quiet street, distant traffic"),
 card("f03", "Members paying over seventy dollars a month went, on average, four point three times a month.", "4.3", "VISITS A MONTH · $70+ PLAN",
      sfx="quiet gym, a treadmill whirring"),
 card("f04", "That's more than seventeen dollars a visit. A ten-visit pass would have cost them ten.", "$17+", "PER VISIT · $10 WITH A PASS",
      bg="#5A3C3C", hold=1.0, sfx="quiet gym, a treadmill whirring"),
 s("f05", M, "Their best explanation was overconfidence. People sign up for a much more disciplined version of themselves.",
   "A man in pyjamas standing at a bathroom mirror; his reflection is a much fitter, disciplined version of him in gym kit, flexing proudly. "
   "Exactly one person and his reflection.", sfx="bathroom, a dripping tap"),
 s("f06", M, "Everyone has one. He's the reason there's a yoga mat behind your door, still in its plastic.",
   "A rolled yoga mat still wrapped in shiny plastic, leaning behind a bedroom door, a little dusty.", env=True, sfx="quiet bedroom"),
 silent("f07", RYAN_FULL + "standing at a bright gym reception desk signing a form; behind him, one hand resting on his shoulder, stands " + FUT2 +
        ", holding a green smoothie. Exactly two people.", 1.5, refs=RY_F, mv="in", sfx="gym reception, distant treadmills, low chatter"),
 s("f08", M, "This is Ryan's. Future Ryan.", FUT + "close-up, smiling serenely, sipping a green smoothie, morning sunlight." + ONE, refs=["futureryan"],
   sfx="calm morning, birds"),
 s("f09", M, "He gets up at six, he's read the terms and conditions, and he signed Ryan up for the gym. And the meal kit. And the language app.",
   FUT + "at a desk at sunrise, happily reading a very long paper scroll covered in tiny squiggles, a pen in his hand." + ONE, refs=["futureryan"],
   mv="right", sfx="calm morning, a pen scratching"),
 silent("f10", "A small kitchen: " + FUT2.replace("his future self from the second reference", "the athletic man from the second reference") +
        ", calmly unpacking a meal-kit box full of fresh herbs; beside him the young man from the first reference eats dry cereal straight from "
        "the box. Exactly two people.", 1.0, refs=RY_F, mv="in", sfx="kitchen, cardboard box, cereal crunching"),
 s("f11", R, "He made a risotto. On a Tuesday. I didn't know you were allowed.",
   FUT + "calmly stirring a pan of risotto in a small kitchen, serene." + ONE, refs=["futureryan"], sfx="kitchen, gentle simmering, a wooden spoon"),
 s("f12", M, "Ryan pays for all of it. Future Ryan uses all of it.",
   RYAN_FULL + "sitting at a kitchen table with a pile of bills, tired; through the open doorway behind him " + FUT2 +
   " does yoga happily on a mat. Exactly two people.", refs=RY_F, sfx="quiet flat, soft breathing from the next room"),
 silent("f13", RYAN_FULL + "standing at a window in a dressing gown holding a slice of toast, seen from inside his flat; outside on the sunny "
        "pavement " + FUT2 + " jogs past waving, and " + FOX + " jogs beside him in a tiny matching sweatband. Exactly two people.", 2.5,
        refs=RY_F, eng="ltx", sfx="morning street through a window, jogging footsteps",
        motion="Outside the window the athletic man jogs past from left to right, waving, with the small orange fox in a tiny sweatband "
               "jogging beside him; the man in the dressing gown stays still holding his toast. Static camera."),
 s("f14", R, "He speaks Portuguese now. I hear him on the phone, laughing. I don't know what about.",
   FUT + "sitting at a kitchen table laughing warmly into his phone." + ONE, refs=["futureryan"], sfx="quiet kitchen, muffled happy laughter"),
 s("f15", M, "Then Future Ryan met someone. At the gym.", FUT + "in a gym, looking across the room and smiling shyly." + ONE, refs=["futureryan"],
   hold=0.5, sfx="gym, weights clinking"),
 s("f16", M, "Ryan's gym.", FUT + "and a sporty woman in matching teal gym kit sitting close on a gym bench, sharing one green smoothie with two "
   "straws, smiling at each other. Exactly two people.", refs=["futureryan"], hold=1.5, sfx="gym, weights clinking, a smoothie slurp"),
 s("f17", M, "Last month, Future Ryan moved to Lisbon.",
   "A sunny Lisbon street of colourful tiled houses with a yellow tram climbing a steep hill.", env=True, mv="right", sfx="sunny city street, a tram bell, gulls"),
 s("f18", M, "He left a lovely note. He didn't cancel anything.",
   "A kitchen counter: a folded note covered in squiggle handwriting, and next to it a clean, dust-free rectangle on the dusty counter where "
   "an appliance used to stand.", env=True, mv="in", hold=1.5, sfx="quiet kitchen, a fridge humming"),
 h("f19", R, "He's taken the air fryer.", RYAN + "standing in his kitchen staring down at the counter, quietly wounded.",
   "He stares down at the counter and speaks quietly, a small crack in his voice.", hold=1.5, sfx="quiet kitchen, a fridge humming"),
 # ---------------- ABSURD SEQUENCE 2: RETENTION
 s("r01", M, "So Ryan decided to cancel everything. He started with Weekend Plus, which can only be cancelled in person, on a Saturday.",
   RYAN + "sitting at his kitchen table on a Friday night with a pen and a long list, looking determined." + ONE, refs=RY, sfx="quiet kitchen at night"),
 s("r02", M, "So he took a Saturday off. Unpaid.", KF_WAIT, env=True, mv="right", hold=1.0, sfx="waiting room hum, a ticket machine beep"),
 silent("r03", "A beige office door slightly ajar and swinging open; in the gap stands " + GER.replace("waist-up, ", "").replace("The man", "the man") + "wearing a small headset, "
        "smiling like warm milk; behind him on the office wall hangs a framed child's drawing of a smiling sun." + ONE, 2.0, refs=["gerald"],
        eng="ltx", sfx="a door creaking slowly open, quiet office",
        motion="The door swings slowly open, revealing the man standing in the doorway smiling warmly. Static camera."),
 h("r04", G, "Ryan. Come in. Nobody's in trouble. I've moved to Retention.",
   GER + "wearing a small headset, standing in the open doorway of a small softly lit office, a framed child's drawing of a smiling sun on the "
   "wall behind him, gently beckoning, warm smile.", "He gently beckons and speaks calmly and softly, smiling.", sfx=SFX_RET),
 s("r05", R, "I'd like to cancel Weekend Plus, please.", ger("nodding kindly, pen poised over his notepad.") + ONE, refs=["gerald"], sfx=SFX_RET),
 s("r06", G, "Of course. That's completely valid. Can I ask why?", ry_ret("polite and attentive."), refs=RY, sfx=SFX_RET),
 s("r07", R, "I have to work weekends to pay for it.", ger("writing very slowly on his notepad, eyes down, serene.") + ONE, refs=["gerald"],
   sfx="quiet office, a pen scratching slowly"),
 s("r08", G, "So what I'm hearing is, you love it so much, you work for it.", ry_ret("staring blankly, lost for words."), refs=RY, mv="in", sfx=SFX_RET),
 s("r09", M, "That's not what he said.", ger("not reacting at all, serene, hands folded.") + ONE, refs=["gerald"], mv="out", sfx=SFX_RET),
 card("r10", "What if we paused it? You'd keep paying, but the weekends would stop.", "PAUSE", "YOUR WEEKEND", spk=G, bg="#3C5A50",
      sfx="a laminated card sliding on a table, quiet office"),
 s("r11", R, "That's what's happening now.", KF_GER_LISTEN, refs=["gerald"], hold=0.5, sfx=SFX_RET),
 silent("r12", "A small pet carrier on a table in a softly lit office; inside, the small glowing sun-shaped object from before, dimmer now, with "
        "two tiny dot eyes, looking up hopefully.", 2.0, env=True, mv="in", sfx="a pet carrier set down on a table, quiet office"),
 s("r13", G, "It's been asking about you.", "A small pet carrier on a table in a softly lit office; inside, the small glowing sun-shaped object from "
   "before, dimmer now, with two tiny dot eyes, looking up hopefully.", env=True, mv="in", sfx="quiet office, a faint sad chime"),
 s("r14", R, "Is it eating?", "A small pet carrier on a table in a softly lit office; inside, the small glowing sun-shaped object from before, "
   "dimmer now, with two tiny dot eyes, looking up hopefully.", env=True, mv="out", sfx=SFX_RET),
 s("r15", G, "It gets Sunday evenings.", ry_ret("worried and sincere, eyebrows raised."), refs=RY, hold=1.5, sfx=SFX_RET),
 s("r16", I, "Fake your death.", KF_SHADOW_GER, refs=RY, sfx=SFX_RET),
 s("r17", R, "What if I died?", KF_GER_LISTEN, refs=["gerald"], mv="out", sfx=SFX_RET),
 h("r18", G, "Then we'd need you to come in. In person.", KF_INPERSON, MV_INPERSON, hold=1.5, sfx=SFX_RET),
 s("r19", G, "Of course, if you're sure, cancellations are just through there. Take your time. Most people do.",
   ry_ret("glancing nervously to one side towards a second door."), refs=RY, sfx=SFX_RET),
 silent("r20", "A room full of colourful balloons around a table with a big frosted cake.", 1.0, env=True, mv="in",
        sfx="a door creaking open, balloons squeaking"),
 silent("r21", "A long beige corridor lined with framed photos of sunny weekend picnics, parks and beach days.", 1.0, env=True, mv="in",
        sfx="a door creaking open, footsteps in a corridor"),
 silent("r22", "A small bare room with one plastic chair, a small wall speaker and a plain round wall clock.", 1.0, env=True, mv="in",
        sfx="a door creaking open, a clock ticking, a faint tinny beep from a speaker"),
 silent("r23", "One final plain beige door at the end of a short corridor.", 1.0, env=True, mv="in", sfx="a door creaking open slowly"),
 silent("r24", KF_RAIN, 4.0, refs=RY, mv="out", sfx="rainy city street on a Monday morning, traffic, a bin lorry"),
 # ---------------- THE ILIAD
 s("l01", M, "That part was made up.", KF_RAIN, refs=RY, mv="in", hold=0.5, sfx="rainy city street, traffic"),
 s("l02", M, "This part isn't. In 2023, the US Federal Trade Commission sued Amazon over Prime.",
   "A grand government building with tall stone columns on a grey day, wide steps in front.", env=True, mv="in", sfx="city street, distant traffic, pigeons"),
 card("l03", "It said cancelling took four pages, six clicks and fifteen options, and that inside Amazon this was known as the Iliad Flow.",
      "6 CLICKS", "4 PAGES · 15 OPTIONS · FTC v. AMAZON 2023", hold=0.5, sfx="mouse clicks, quiet office"),
 s("l04", M, "The Iliad is a poem about a war that lasts ten years. Somebody chose that name. For the way out.", KF_TROY, env=True, mv="out",
   hold=1.0, sfx="wind over an empty plain at dusk, a distant campfire crackle"),
 s("l05", M, "The FTC said Amazon's leaders slowed or rejected changes that would have made cancelling easier, because those changes hurt the bottom line.",
   "A huge grey maze seen from above, with one tiny exit door far away in the corner.", env=True, mv="in", sfx="quiet wind"),
 s("l06", M, "In its words, the process existed \"not to enable subscribers to cancel, but to stop them.\"",
   "An empty open-plan office at night, one computer monitor glowing, everything still.", env=True, mv="in", hold=1.5,
   sfx="near-silent empty office at night, very faint room tone"),
 card("l07", "In 2025, Amazon settled for two and a half billion dollars, without admitting wrongdoing.", "$2.5BN", "FTC SETTLEMENT · SEPT 2025",
      bg="#5A3C3C", hold=1.0, sfx="quiet office"),
 s("l08", M, "Adobe was sued too.", "A courtroom with a wooden judge's bench and a gavel, empty benches, soft daylight.", env=True, mv="in",
   sfx="quiet courtroom, a chair creaking"),
 card("l09", "The government said that cancelling in your first year could cost half of what you had left to pay, and that the warning was in small print, or behind tiny icons you had to hover over.",
      "50%", "OF WHAT'S LEFT · CANCEL IN YEAR ONE", hold=1.0, sfx="quiet office, a mouse click"),
 s("l10", M, "In March 2026, Adobe agreed to settle for a hundred and fifty million dollars. Half of it was a fine. The other half was paid in free Adobe.",
   "A judge's gavel resting on top of a big pile of plain software boxes with blank colourful covers, tied with a gift ribbon.", env=True, mv="in",
   hold=1.0, sfx="quiet courtroom, a gavel tap"),
 # ---------------- CLICK TO CANCEL
 card("k01", "In 2024, the FTC adopted a rule that cancelling had to be as easy as signing up.", "CLICK", "TO CANCEL · FTC · OCT 2024", bg="#3C5A50",
      sfx="a single mouse click, quiet office"),
 s("k02", M, "In July 2025, six days before businesses had to comply, a federal appeals court threw it out. The FTC had skipped a required cost analysis.",
   "A courtroom bench with a gavel and a single document torn neatly in half lying on it.", env=True, mv="in", sfx="quiet courtroom, paper tearing"),
 silent("k03", GER + "sitting alone at his desk after hours under a single lamp, a newspaper covered in grey squiggles open in front of him, "
        "pouring himself one very small glass of sherry, content." + ONE, 2.0, refs=["gerald"], mv="in",
        sfx="quiet office after hours, a small glass being filled"),
 s("k04", M, "The law Amazon settled under still stands. And in March 2026, the FTC started again. From the beginning.",
   "A single blank sheet of paper and a freshly sharpened pencil on a big empty government desk.", env=True, mv="in", sfx="quiet office, a clock ticking"),
 # ---------------- THINGS YOU ALREADY OWN
 s("o01", M, "Meanwhile, the newest idea is charging monthly for things you've already bought.",
   "A plain desktop printer on a home desk with a small coin slot on its side.", env=True, mv="in", sfx="quiet home office"),
 s("o02", M, "In January 2024, HP's chief executive told CNBC that the company's long-term objective was \"to make printing a subscription.\"",
   "A businessman in a dark suit sitting alone on a television studio set, talking confidently towards the camera, a large snowy-mountain picture on the backdrop behind him." + ONE,
   mv="right", sfx="quiet TV studio, faint camera whirr"),
 card("o03", "He also said a customer who doesn't print enough, or doesn't use HP's supplies, is \"a bad investment.\"", "BAD", "INVESTMENT · HP CEO, 2024",
      bg="#5A3C3C", sfx="quiet TV studio"),
 silent("o04", RYAN + "sitting at his desk beside a plain desktop printer, looking at it; the printer just sits there." + ONE, 1.0, refs=RY, mv="in",
        sfx="quiet home office, a printer humming"),
 h("o05", R, "I've never been an investment before. I don't think I'm doing very well.",
   RYAN + "sitting at his desk beside a plain desktop printer, looking quietly at the camera, honest.",
   "He glances at the printer, then speaks quietly and honestly to the camera, with a short pause between the two sentences.", hold=1.0,
   sfx="quiet home office, a printer humming"),
 s("o06", M, "And if you cancel HP's Instant Ink, the cartridges already in your printer stop working at the end of the billing cycle.",
   "Close-up of a printer ink cartridge glowing bright cyan, magenta and yellow.", env=True, mv="in", sfx="quiet home office, a printer humming"),
 silent("o07", "Close-up of the same printer ink cartridge, now dull grey and lifeless, with one tiny gold padlock fixed on it.", 1.5, env=True,
        mv="in", sfx="a printer powering down with a soft click"),
 s("o08", M, "Which is usually when someone online says: you'll own nothing, and be happy.",
   "A man alone in a dark room lit only by his computer screen, typing furiously, wide-eyed." + ONE, mv="in", sfx="dark room, fast keyboard typing"),
 card("o09", "", "NOTHING", "YOU'LL OWN NOTHING AND BE HAPPY", bg="#5A3C3C", dur=1.5, sfx="a low gust of wind"),
 s("o10", M, "It isn't a secret plan. It comes from a short World Economic Forum video in 2016, based on an essay by the Danish politician Ida Auken, imagining life in a city in 2030.",
   "A bright futuristic green city with gardens on every roof, shared bicycles and small delivery drones in the sky.", env=True, mv="right",
   sfx="calm city ambience, birds, bicycle bells"),
 s("o11", M, "She later wrote that it wasn't her utopia, just a scenario to get people talking.",
   "An open notebook and a pen on a desk by a window overlooking the green futuristic city.", env=True, mv="in", sfx="quiet room, a window open, birds"),
 s("o12", M, "The internet decided it was a threat.",
   "A crowd of people at laptops in a dark room, wide-eyed, pointing at their screens in alarm.", mv="in", hold=0.5, sfx="many keyboards typing, worried murmurs"),
 s("o13", M, "Brayden decided it was a goal.", BRAY + "standing in a completely empty white room, arms spread wide, beaming with joy." + ONE,
   refs=["brayden"], mv="in", sfx="empty room echo"),
 # ---------------- ABSURD SEQUENCE 3: BRAYDEN OWNS NOTHING
 s("b01", M, "Nine days later, Ryan went round with a housewarming present.",
   RYAN_FULL + "standing at a front door at night holding a bottle of wine, about to knock." + ONE, refs=RY,
   sfx="quiet street at night, a knock on a door"),
 silent("b02", BRAY_FULL + "climbing out of the front window of his house at night, one leg over the sill, beaming, a bed of roses below the "
        "window." + ONE, 3.0, refs=["brayden"], eng="ltx", sfx="a window sliding open, a thump into a flower bed, leaves rustling",
        motion="The man swings his other leg over the sill, drops into the rose bed, and pops up beaming. Static camera."),
 h("b03", B, "Bro! The door's on the premium tier. Window's free. Mind the roses, they're rented.",
   BRAY + "standing in a rose bed outside his front window at night, a few petals on his t-shirt, beaming, arms open.",
   "He brushes a petal off his shirt and speaks loudly and delightedly, gesturing at the window.", sfx="quiet street at night, leaves rustling"),
 silent("b04", "A bare white flat with no furniture at all, one bare light bulb hanging from the ceiling.", 1.0, env=True, mv="in",
        sfx="empty room echo, a bare bulb buzzing"),
 s("b05", B, "I don't own anything anymore. Sofa's on demand. Even my hairline's on a subscription. Ownership is an anchor. I'm a boat.",
   RYAN_FULL + "standing in a bare white empty flat under one bare bulb, holding a bottle of wine, looking around in polite confusion." + ONE,
   refs=RY, mv="out", sfx="empty room echo, a bare bulb buzzing"),
 silent("b06", BRAY + "opening a dark fridge in a bare white kitchen, lighting the inside with his phone torch." + ONE, 1.0, refs=["brayden"],
        mv="in", sfx="a fridge door opening, quiet hum"),
 s("b07", B, "Fridge light's on pause. Keeps me hungry.",
   "Inside a dark empty fridge lit by a single beam of torchlight: one lonely carton of oat milk on a shelf.", env=True, mv="in",
   sfx="an open fridge humming, empty room"),
 s("b08", R, "Where do you sit?", BRAY + "his face lit from below by his phone torch, peering proudly into a dark open fridge." + ONE, refs=["brayden"],
   sfx="an open fridge humming, empty room"),
 s("b09", B, "Sitting's on the Plus plan. I stand. Standing's free.",
   RYAN + "in a bare white flat under one bare bulb, holding a bottle of wine, nodding slowly and politely." + ONE, refs=RY,
   sfx="empty room echo, a bare bulb buzzing"),
 silent("b10", RYAN_FULL + "slowly lowering himself to sit on the bare floor of the empty white flat, holding the bottle of wine." + ONE, 1.0,
        refs=RY, mv="in", sfx="clothes rustling, a cheerful electronic ding"),
 card("b11", "", "99p", "THE FLOOR · PER MINUTE", dur=1.5, sfx="a cheerful electronic ding, empty room"),
 s("b12", I, "Lie down. Make it worth it.",
   RYAN_FULL + "sitting on the bare floor of the empty white flat holding a bottle of wine, while " + SHADOW + "." + ONE, refs=RY,
   sfx="empty room, a bare bulb buzzing"),
 silent("b13", RYAN_FULL + "standing very straight in the empty white flat under one bare bulb, holding the bottle of wine stiffly." + ONE, 1.0,
        refs=RY, mv="in", sfx="empty room, a bare bulb buzzing"),
 s("b14", R, "It's like visiting someone who's been burgled. And they're proud of it.",
   RYAN_FULL + "standing very straight in the empty white flat under one bare bulb, holding the bottle of wine stiffly." + ONE, refs=RY,
   mv="out", hold=1.0, sfx="empty room, a bare bulb buzzing"),
 s("b15", B, "And for nine ninety-nine a month, you can subscribe to me. You get my mornings. Most of them are filmed in the afternoon.",
   RYAN + "in the empty white flat holding the bottle of wine, blinking slowly, speechless." + ONE, refs=RY, mv="in",
   sfx="empty room echo, a bare bulb buzzing"),
 silent("b16", RYAN + "in the empty white flat, politely holding out the bottle of wine as a gift." + ONE, 1.0, refs=RY, mv="in",
        sfx="empty room, a bare bulb buzzing"),
 h("b17", B, "I can't take that. Then I'd own it.", BRAY + "in the bare white flat under one bare bulb, one hand on his heart, genuinely touched, "
   "the other palm raised in a gentle no.", "He puts a hand on his heart, deeply touched, and gently refuses.", sfx="empty room, a bare bulb buzzing"),
 silent("b18", "In a bare white flat under one bare bulb, the man from the first reference gently pushes a bottle of wine back into the hands of "
        "the young man from the second reference; the two stand together in the empty room. Exactly two people.", 1.5, refs=["brayden", "ryan"],
        mv="out", sfx="a bare bulb buzzing and flickering, empty room"),
 # ---------------- THE VERDICT AND THE REVEAL
 s("v01", M, "So, why is everything a subscription now? Partly because some things genuinely work better that way. I'm keeping my music.",
   "A happy young woman on a city bus wearing big headphones, eyes closed, smiling, the city passing by the window." + ONE, mv="out",
   sfx="city bus interior, engine hum"),
 s("v02", M, "But mostly because a subscription is a bet on three things. That you'll forget. That you'll overestimate the person you're about to become. And that leaving will be just annoying enough to put off until next month.",
   "Three plain face-down playing cards on a green card table under a lamp, a small pile of coins beside them.", env=True, mv="in",
   sfx="quiet room, cards sliding on felt"),
 silent("v03", "A phone standing upright on a kitchen table, propped against the wall with its screen facing the wall.", 0.7, env=True, mv="in",
        sfx="quiet kitchen at night"),
 silent("v04", FUT + "standing alone on a sunny Lisbon balcony, happily hugging an air fryer in both arms, colourful tiled houses far behind him." + ONE, 0.7,
        refs=["futureryan"], mv="in", sfx="sunny city, gulls, a tram bell"),
 silent("v05", KF_RAIN, 0.7, refs=RY, mv="in", sfx="rainy city street on a Monday morning, traffic"),
 s("v06", M, "A decent test is whether you'd sign up again today, at today's price. If you wouldn't, it's not a subscription anymore. It's a monthly charge you keep for sentimental reasons.",
   "A small wooden keepsake box lined with velvet, holding a neatly folded paper bill tied with a ribbon like an old love letter.", env=True,
   mv="in", hold=1.0, sfx="quiet room, a clock ticking"),
 silent("v07", RYAN + "at his kitchen table in the evening, tapping on his phone, cancelling things one by one, focused." + ONE, 1.0, refs=RY,
        mv="in", sfx="quiet kitchen in the evening, soft pops one after another"),
 card("v08", "Sorry.", "GYM", "CANCELLED", spk=R, hold=0.5, sfx="a soft pop, quiet kitchen"),
 card("v09", "Sorry.", "MEAL KIT", "CANCELLED", spk=R, hold=0.5, sfx="a soft pop, quiet kitchen"),
 card("v10", "Really sorry about this one.", "LANGUAGE", "APP · CANCELLED", spk=R, sfx="a soft pop, quiet kitchen"),
 s("v11", M, "It took him the whole evening.",
   RYAN + "at his kitchen table late at night, the window dark, a cold cup of tea beside him, tired but relieved." + ONE, refs=RY,
   sfx="quiet kitchen late at night, a clock ticking"),
 silent("v12", KF_RY_RADIATOR, 1.5, refs=RY, mv="in", sfx="an old radiator ticking as it warms, quiet kitchen at night"),
 h("v13", R, "This one's mine.", RYAN + "sitting at his kitchen table in the evening, one hand resting on an old white radiator under the window, "
   "small sincere smile.", "He rests his hand on the radiator and speaks softly, almost moved.", hold=1.0,
   sfx="an old radiator ticking as it warms, quiet kitchen at night"),
 silent("v14", "Close-up of a phone buzzing on an empty wooden kitchen table, its screen showing an incoming call; the caller photo is a tiny round picture of a smiling grey-haired man with round glasses and a beige cardigan. The room around the table is empty.",
        1.0, env=True, mv="in", sfx="a phone buzzing on a wooden table"),
 s("v15", G, "Hi Ryan. It's Gerald. Nobody's in trouble. We noticed you'd left, so we've signed you up for Weekend Lite. The first month's completely free.",
   KF_RY_RADIATOR, refs=RY, mv="in", hold=1.5, sfx="an old radiator ticking, a phone call on speaker, quiet kitchen"),
 silent("v16", KF_FOX_END, 3.0, env=True, eng="ltx", sfx="a single soft heater click, a quiet car interior, faint winter wind outside",
        motion=MV_FOX_END),
]
THUMB = dict(text="$18 A MONTH|FOR MY OWN SEAT?", refs=RY,
             kf=RYAN + "shivering in the driver's seat of a small plain grey car on a frosty morning, the seat glowing warm orange beneath him "
                "with one tiny gold padlock on it, gloves on, breath fogging, big worried eyes; " + FOX + " curled up asleep on the warm "
                "bonnet. Exactly one person.")
TAIL = 1.0
