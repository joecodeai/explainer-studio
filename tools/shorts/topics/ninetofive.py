"""Is working 9-5 a trap? 10-minute LANDSCAPE explainer (fast flat pipeline).
Comedic personality: a quietly unimpressed time auditor. It treats the working week like an expense report, itemising where the
hours actually go (the commute, the postcard, the Admiralty, the jacket left on the chair) and finding the comedy in the gap between
the schedule and the work. Dry about meetings, commutes and escape-the-rat-race gurus; never sneers at people who like their jobs,
at people who quit them, or at the unemployed. Balanced: the case for the trap, the case for the steady job, honest verdict.
Sources: Our World in Data, 'Are we working more than ever?' (1870: 3,000+ hours a year, 60-70 hours a week, Huberman & Minns 2005);
Robert Owen's 1817 slogan 'Eight hours labour, eight hours recreation, eight hours rest' (eight-hour day movement); ILO Hours of Work
(Industry) Convention 1919 (No. 1): 8 hours a day / 48 a week, the ILO's first convention; Ford Motor Company five-day, 40-hour week,
1926 (automotivehistory.org; Literary Digest 1922; Ford's argument that rested workers are more productive and free time fuels consumer
spending, Arcadia/History); US Fair Labor Standards Act 1938 (overtime after 44 h, 42 h in 1939, 40 h from 1940; DOL opinion letter
FLSA2026-9); J. M. Keynes, 'Economic Possibilities for our Grandchildren' (1930: living standards 4-8x higher in 100 years; 'three-hour
shifts or a fifteen-hour week'); NPR Planet Money, 13 Aug 2015 (Keynes had no children; sister's grandson Nicholas Humphrey worked about
15 hours a day; family says Keynes died from working too hard; Richard Freeman: higher pay makes time off feel costlier); N. Crafts,
'The 15-Hour Week: Keynes's Prediction Revisited', Economica 2022 (UK real GDP per person in 2011 a little over 5x 1931; men's hours fell
by more than a quarter 1931-2011; lifetime leisure up 58%, driven by longer retirement); B. Hunnicutt, 'Kellogg's Six-Hour Day' (Temple
UP) and MR Online (six-hour shifts from 1 Dec 1930; last department voted for eight hours in 1985); C. N. Parkinson, 'Parkinson's Law',
The Economist, 19 Nov 1955 (postcard to niece at Bognor Regis; capital ships 62 -> 20 and Admiralty officials 2,000 -> 3,569, 1914-28);
US Census ACS 1-year 2025 (mean one-way commute 27.4 min; 'five extra working weeks' = 27.4 x 2 x 5 x 48 / 60 / 40, own calculation);
Kahneman et al., 'A survey method for characterizing daily life experience', Science 2004 (909 employed women in Texas; commuting
ranked last of 16 activities, working second-last; boss lowest of interaction partners except being alone); Gallup, State of the Global
Workplace 2026 (20% engaged in 2025, 64% not engaged, 16% actively disengaged, 40% a lot of daily stress, ~$10 trillion lost
productivity); Autonomy, UK four-day week pilot results 2023 (61 companies, ~2,900 workers, Jun-Dec 2022; 56 continuing, 18 permanent;
revenue broadly the same; staff leaving -57%; sick days -65%, WEF); Autonomy/Alda and BBC 2021 on Iceland's 2015-19 trials (2,500+
workers, 35-36 hours, 86% of workforce now on or entitled to shorter hours); Roon summary of pilot limitations (volunteer firms, no
control group, self-reported; mostly white-collar); Fan & Schor, Nature Human Behaviour 2025 (2,896 employees, 141 organisations, six
countries, 12 control companies, lower burnout); OECD Data Explorer, average annual hours actually worked per worker (2025: Germany
1,332, USA 1,800, Mexico 2,205; OECD warns levels are not fully comparable); OECD Employment Outlook 2021 and Destatis (Germany: 20
days statutory leave, ~30 by collective agreement); US DOL (FLSA does not require paid vacation); BLS Business Employment Dynamics
(~20% of new establishments fail in year one, ~50% within five); gov.uk (self-employed not eligible for Statutory Sick Pay); IRS
(self-employment tax 15.3%); KFF Employer Health Benefits Survey 2026 (employer plans cover almost 157 m people under 65) and 2025
(average family premium $26,993, workers pay 26%); Jahoda, Lazarsfeld & Zeisel, 'Marienthal' (1933; factory closed 1929, nearly every
family affected; men walked slower and stopped more often; 88 of 100 men wore no watch; leisure 'a tragic gift'); M. Benz & B. Frey,
'Being Independent is a Great Thing', Economica 2008 (self-employed more satisfied irrespective of income or hours; autonomy)."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Is Working 9 to 5 a Trap"            # VIDEOS/<FOLDER>/...
ERA = "modern"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Calm office palette of slate blue, warm beige, tangerine orange, mint green and "
         "charcoal grey. Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. "
         "Clean simple background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Calm office palette of slate blue, warm beige, tangerine orange, mint green "
             "and charcoal grey. Show only what the description names. There are NO characters of any kind: no people, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "worker": "a modern office worker as a simple flat vector character: man in his early thirties, short neat dark hair, light blue shirt with "
           "rolled sleeves, loose navy tie, charcoal trousers, small round head, dot eyes, slightly tired expression.",
 "freelancer": "a self-employed modern woman as a simple flat vector character: short curly ginger hair, mustard-yellow jumper, dark green "
               "trousers, white trainers, a brown laptop bag over her shoulder, small round head, dot eyes.",
 "fordman": "a 1926 car-factory worker as a simple flat vector character: man with a flat grey cap, blue denim overalls over a white shirt "
            "with rolled sleeves, small neat moustache, small round head, dot eyes.",
}
P1 = "Static camera. Characters keep the same faces and clothes."
RY = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
      "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
      "wall and a plant, ")
RYM = "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."
def ryan(id_, text, pose, mv): return dict(id=id_, spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"], text=text, kf=RY + pose, mv=mv + " " + RYM)
SHOTS = [
 # --- hook
 dict(id="n00", spk=M, eng="still", mv="in", refs=["worker"], sfx="quiet office, a wall clock ticking, a keyboard",
      text="In 1930, a famous economist predicted that by now we'd only need to work fifteen hours a week. Most of us have done fifteen hours by Tuesday afternoon.",
      kf="The man from the reference slumped over his office desk behind a towering stack of paper folders that reaches the ceiling, while on "
         "the wall behind him a framed portrait of a cheerful 1930s gentleman with a neat moustache and a bow tie gives a big thumbs-up. "
         "Exactly one person at the desk."),
 dict(id="n01", spk=M, eng="still", mv="right", sfx="open-plan office, phones ringing softly",
      text="So is the nine-to-five a trap? Depending on who you ask online, it's either a slow prison with a pension, or the only sensible thing a grown-up can do. The people calling it a trap are quite often selling a course on how to escape it.",
      kf="A simple open-plan office seen from the side with rows of workers typing at desks, and through the big window a smiling man in a "
         "bright tracksuit on a tropical beach, filming himself with a phone on a stick and pointing at the office."),
 dict(id="n02", spk=M, eng="still", mv="in", sfx="quiet office, a printer whirring",
      text="Let's look at it properly. Where the forty-hour week came from, what it costs, what happens when people try something else, and what the escape videos leave out.",
      kf="An office desk seen from directly above, with a cup of coffee, a pair of glasses, a stopwatch, a magnifying glass and a neat stack "
         "of paper laid out side by side like evidence. No people."),
 # --- where the 40-hour week came from
 dict(id="n03", spk=M, eng="card", card=dict(big="60–70 HRS", small="A TYPICAL FACTORY WEEK IN 1870", bg="#34495E", accent="#F39C4F"),
      sfx="old factory, machines clanking",
      text="First, some perspective. In 1870, factory workers in most industrial countries put in sixty to seventy hours a week. Nine to five would have sounded like a holiday."),
 dict(id="n04", spk=M, eng="still", mv="out", sfx="Victorian factory, steam hissing, heavy machinery",
      text="In 1817, the reformer Robert Owen came up with a slogan. Eight hours labour, eight hours recreation, eight hours rest. It was catchy. It took about a hundred years for governments to agree with it.",
      kf="A busy Victorian factory floor with tall iron machines, clouds of steam, and tired workers in caps and aprons, a high window "
         "showing a dark early-morning sky."),
 dict(id="n05", spk=M, eng="still", mv="in", sfx="crowded meeting hall, murmuring, a gavel knock",
      text="In 1919, the brand new International Labour Organization made the eight-hour day its very first convention. Eight hours a day, forty-eight a week. Which still meant working Saturdays.",
      kf="A grand 1919 conference hall with rows of delegates in dark suits and moustaches raising their hands in a vote, tall arched "
         "windows behind them."),
 dict(id="n06", spk=M, eng="card", card=dict(big="1926", small="FORD'S FIVE-DAY, 40-HOUR WEEK", bg="#2E4A62", accent="#F39C4F"),
      sfx="car factory, metal clanging, a horn",
      text="One of the first big employers to go further was Henry Ford, who in 1926 moved his factory workers to five days and forty hours."),
 dict(id="n07", spk=M, eng="ltx", refs=["fordman"],
      text="Ford wasn't being sentimental. He argued that rested workers were more productive, and that people with free time would buy more things. Such as cars.",
      kf="The man from the reference in his overalls and cap proudly driving a shiny black 1920s car out through an open brick factory gate "
         "on a sunny day. Exactly one person.",
      mv="The car rolls slowly forward through the gate, the man smiles and lifts one hand off the wheel in a small wave. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="n08", spk=M, eng="still", mv="right", refs=["fordman"], sfx="countryside, birds, a car engine ticking as it cools",
      text="The modern weekend, in other words, was partly a sales strategy.",
      kf="The man from the reference, a woman in a 1920s cloche hat and a small boy having a picnic on a checked blanket next to a shiny "
         "black 1920s car on a green hill. Exactly three people."),
 dict(id="n09", spk=M, eng="still", mv="out", sfx="1930s factory yard, a steam whistle, footsteps",
      text="In America, the Fair Labor Standards Act of 1938 made employers pay overtime after forty-four hours a week. By 1940 that had dropped to forty, and it hasn't moved since.",
      kf="A 1930s American factory at closing time, crowds of workers in caps and overalls streaming happily out of the big iron gates "
         "under a large round clock on the brick wall."),
 dict(id="n10", spk=M, eng="still", mv="in", sfx="quiet wood-panelled room, a pen scratching",
      text="The nine-to-five, then, isn't an ancient law of nature. It's a deal struck about a hundred years ago, between people who wanted shorter days and people who owned factories.",
      kf="A 1930s meeting room where a worker in a flat cap and a factory owner in a pinstripe suit shake hands across a wooden table, both "
         "looking slightly unhappy about it. Exactly two people."),
 dict(id="n11", spk=M, eng="still", mv="right", sfx="office, keyboards, a phone ringing",
      text="Then most of us stopped working in factories. The deal stayed exactly where it was.",
      kf="A modern office where rows of desks are lined up exactly like a factory assembly line, office workers in shirts passing sheets "
         "of paper along a long conveyor belt from desk to desk."),
 # --- Keynes
 dict(id="n12", spk=M, eng="still", mv="in", sfx="1930s study, a fire crackling, a pen scratching",
      text="And at the time, everyone assumed the week would keep shrinking. In 1930, the economist John Maynard Keynes wrote an essay called Economic Possibilities for our Grandchildren.",
      kf="A cosy 1930s study with a tall bookcase and a fire, and an elegant gentleman with a neat moustache and a bow tie writing with a "
         "fountain pen at a wooden desk. Exactly one person."),
 dict(id="n13", spk=M, eng="still", mv="right", sfx="1930s study, rain on the window, a clock ticking",
      text="He predicted that within a hundred years, people in rich countries would be four to eight times better off. And he worried that the big problem of the future would be what to do with all the free time.",
      kf="An elegant 1930s gentleman with a neat moustache and a bow tie gazing out of a window at a big daydream cloud showing a future "
         "family lying bored on a sofa on a sunny afternoon, all yawning. Exactly one person in the room."),
 dict(id="n14", spk=M, eng="card", card=dict(big="15 HOURS", small="KEYNES'S WORKING WEEK FOR 2030", bg="#3B6E62", accent="#F2C14E"),
      sfx="quiet study, a fire crackling",
      text="His suggestion was three-hour shifts, or a fifteen-hour week. Not because we'd need the money, but because a little work would stop us getting bored."),
 dict(id="n15", spk=M, eng="still", mv="out", sfx="busy city at night, distant traffic",
      text="On the money, he was remarkably close. By 2011, British income per person was already about five times its 1931 level. On the hours, it went less well.",
      kf="A modern city at night: on one side cosy houses, nice cars and bright shops, on the other a tall office tower with every single "
         "window still lit. No people."),
 dict(id="n16", spk=M, eng="still", mv="in", sfx="quiet study at night, a desk lamp buzzing",
      text="When the radio show Planet Money went looking for Keynes's grandchildren, they found he didn't have any. The closest they got was his sister's grandson, who said he used to work about fifteen hours. A day.",
      kf="A cheerful old man with white hair and glasses at a cluttered desk piled with books and papers in a lamp-lit study late at night, "
         "still writing, a cold cup of tea beside him. Exactly one person."),
 ryan("n17", "Right number. Wrong unit.", "standing with his arms folded, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, arms folded, then gives a tiny nod."),
 dict(id="n18", spk=M, eng="still", mv="out", sfx="quiet empty study, a clock ticking",
      text="Keynes himself, according to his family, died from working too hard.",
      kf="An empty 1940s wooden desk piled high with papers, a fountain pen and a pair of round spectacles lying on top, a single desk lamp "
         "still on. No people."),
 # --- where the free time went
 dict(id="n19", spk=M, eng="still", mv="right", sfx="seaside, gentle waves, gulls",
      text="Where did all the free time go? We did get some. In Britain, men's working hours fell by more than a quarter between 1931 and 2011. But a lot of our extra leisure arrived at the end of life, in one big lump called retirement.",
      kf="A happy elderly couple in sun hats asleep on striped deckchairs on a sunny beach, a huge pile of unread books between them. "
         "Exactly two people."),
 dict(id="n20", spk=M, eng="still", mv="in", sfx="beach, waves, children playing far away",
      text="The Harvard economist Richard Freeman points out another problem. The better paid you are, the harder it is to stop. At two hundred dollars an hour, a day at the beach is a very expensive day at the beach.",
      kf="A man in a grey suit sitting stiffly on a beach towel under a parasol, typing on a laptop and sweating nervously, while families "
         "play happily in the sea behind him. Exactly one person in the foreground."),
 dict(id="n21", spk=M, eng="still", mv="right", sfx="old factory, a conveyor belt rattling",
      text="Some workers were offered the time directly. In 1930, the cereal maker W. K. Kellogg moved his Michigan factory to six-hour shifts, so he could hire more people during the Depression.",
      kf="A bright 1930s cereal factory with conveyor belts carrying golden cornflakes towards boxes, and a group of workers in white caps "
         "waving goodbye cheerfully at the open door in the afternoon sunshine."),
 dict(id="n22", spk=M, eng="still", mv="out", sfx="quiet factory, a single machine humming",
      text="Some departments kept six-hour shifts for over fifty years. But after long pressure from management, the last one voted to go back to eight hours in 1985. Time had been losing to money for quite a while.",
      kf="A simple old balance scale in an empty factory: on one side a small alarm clock, on the other a big pile of gold coins, the scale "
         "tipped heavily towards the coins. No people."),
 # --- Parkinson's law
 dict(id="n23", spk=M, eng="still", mv="in", sfx="1950s office, typewriters, a tea trolley rattling",
      text="There's also a less flattering theory. In 1955, a naval historian called Cyril Northcote Parkinson wrote a satirical essay for The Economist. It starts with a law.",
      kf="A 1950s office full of men in grey suits at typewriters surrounded by tall piles of paper, a tea trolley parked in the aisle."),
 dict(id="n24", spk=M, eng="card", card=dict(big="WORK EXPANDS", small="SO AS TO FILL THE TIME AVAILABLE", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet office, a clock ticking",
      text="Work expands so as to fill the time available for its completion."),
 dict(id="n25", spk=M, eng="still", mv="right", sfx="quiet cottage, a clock ticking, rain on the window",
      text="His example is an elderly lady who spends an entire day sending one postcard to her niece in Bognor Regis. An hour finding the postcard, another hunting for her glasses, and twenty minutes deciding whether to take an umbrella to the postbox.",
      kf="An elderly lady in a cardigan standing in a cosy cottage hallway holding a small picture postcard of the seaside, staring "
         "thoughtfully at an umbrella stand, her glasses pushed up on top of her head. Exactly one person."),
 dict(id="n26", spk=M, eng="card", card=dict(big="62 → 20", small="ROYAL NAVY CAPITAL SHIPS, 1914–1928", bg="#34495E", accent="#F39C4F"),
      sfx="harbour, gulls, a ship's horn far away",
      text="His serious example was the British Admiralty. Between 1914 and 1928, the number of capital ships in service fell from sixty-two to twenty."),
 dict(id="n27", spk=M, eng="still", mv="in", sfx="busy government office, typewriters, footsteps",
      text="Over the same years, the number of Admiralty officials went up from two thousand to three thousand five hundred and sixty-nine. Fewer ships. More people looking after them.",
      kf="A tiny toy battleship sitting alone in the middle of a huge desk, surrounded by a big crowd of officials in suits all leaning in "
         "and peering at it with clipboards."),
 ryan("n28", "Somebody had to schedule the meetings.", "holding a coffee mug, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then takes a slow sip from the mug."),
 dict(id="n29", spk=M, eng="still", mv="out", refs=["worker"], sfx="quiet office, a clock ticking, air conditioning hum",
      text="Parkinson was writing satire. People have been quoting it seriously ever since, usually in meetings. It's also the core of the case against a fixed working day. If the day is eight hours long, the work has a way of becoming eight hours long.",
      kf="The man from the reference at his office desk gently stretching a single sheet of paper like a long elastic band between his two "
         "hands, a big wall clock above him. Exactly one person."),
 # --- the costs
 dict(id="n30", spk=M, eng="card", card=dict(big="27 MIN", small="AVERAGE US COMMUTE, EACH WAY (2025)", bg="#3B6E62", accent="#F39C4F"),
      sfx="traffic jam, engines idling, a distant horn",
      text="Then there's the part of the working day nobody pays you for. In 2025, the average American commute was about twenty-seven minutes each way."),
 dict(id="n31", spk=M, eng="still", mv="right", refs=["worker"], sfx="traffic jam, engines idling, rain on a windscreen",
      text="That's almost an hour a day. Over a working year, that's about five extra working weeks, spent mostly looking at the back of someone else's car.",
      kf="The man from the reference sitting in a small car in a long traffic jam, chin resting on his hand, staring at the back of the car "
         "in front, a long line of cars stretching to the horizon. Exactly one person visible."),
 dict(id="n32", spk=M, eng="ltx", env=True,
      text="In one study, more than nine hundred working women in Texas rated their daily activities. Commuting came last for enjoyment. Working came second to last.",
      kf="A long line of simple cars stuck nose to tail in a traffic jam on a wide motorway at sunrise, the sun low and orange on the "
         "horizon. No people.",
      mv="The cars inch forward very slowly in the jam, the low sun rises slightly. Static camera."),
 dict(id="n33", spk=M, eng="still", mv="in", sfx="office, quiet chatter, a door closing",
      text="They also rated the people they spent time with. The boss came last. The only thing that scored lower was being completely on their own.",
      kf="A woman at her office desk forcing a tight polite smile while a manager in a grey suit leans over her shoulder pointing at her "
         "screen with a pen. Exactly two people."),
 dict(id="n34", spk=M, eng="card", card=dict(big="20%", small="OF EMPLOYEES WORLDWIDE ARE ENGAGED (GALLUP)", bg="#2E4A62", accent="#F2C14E"),
      sfx="large open-plan office, quiet keyboards",
      text="And the job itself? Gallup's latest State of the Global Workplace report found that only twenty percent of employees worldwide are engaged at work."),
 dict(id="n35", spk=M, eng="still", mv="out", sfx="large open-plan office, keyboards, a phone ringing",
      text="Sixty-four percent are not engaged, which roughly means present, polite and mentally somewhere else. Sixteen percent are actively disengaged. And forty percent said they'd felt a lot of stress the day before.",
      kf="A big open-plan office with rows of workers at desks; most look politely blank, a few look grumpy, and one woman in the middle "
         "is typing with great enthusiasm."),
 dict(id="n36", spk=M, eng="still", mv="in", sfx="busy city street, distant traffic, coins clinking",
      text="Gallup puts the cost of all that low engagement at around ten trillion dollars in lost productivity. Which is a lot of money to spend on not quite being there.",
      kf="A tall office building with a thin stream of gold coins leaking out through a crack in its side and rolling away down the street. "
         "No people."),
 dict(id="n37", spk=M, eng="still", mv="right", sfx="quiet empty room, a clock ticking",
      text="That's the case for the trap. A schedule built for nineteen-twenties factories, applied to jobs where nobody's output is measured in cars. Hours that fill themselves up. An unpaid hour in traffic. And a lot of people who are there, but not really.",
      kf="A giant wooden mousetrap with its metal bar pulled back, and sitting on it where the cheese would go, a small office desk with a "
         "swivel chair and a computer, on a beige floor. No people."),
 # --- four-day week
 dict(id="n38", spk=M, eng="card", card=dict(big="61", small="UK COMPANIES IN THE 2022 FOUR-DAY WEEK PILOT", bg="#3B6E62", accent="#F2C14E"),
      sfx="bright office, relaxed chatter",
      text="What happens when people just work less? In 2022, sixty-one British companies and about two thousand nine hundred staff tried a four-day week for six months, with no cut in pay."),
 dict(id="n39", spk=M, eng="still", mv="in", refs=["worker"], sfx="sunny street, birds, distant traffic",
      text="Afterwards, fifty-six of the companies kept it going, and eighteen made it permanent. Revenue stayed broadly the same. The number of people leaving fell by more than half.",
      kf="The man from the reference walking out of a bright office building on a sunny afternoon with his jacket over his shoulder, "
         "smiling up at the sky. Exactly one person."),
 dict(id="n40", spk=M, eng="still", mv="right", sfx="dentist's waiting room, a quiet drill in the distance",
      text="Sick days fell by sixty-five percent. Some of that is people being less worn out. Some of it, presumably, is that the dentist is now open on your day off.",
      kf="A relaxed man lying in a dentist's chair on a sunny weekday giving a thumbs-up, while a dentist in a white coat looks at his teeth. "
         "Exactly two people."),
 dict(id="n41", spk=M, eng="still", mv="out", sfx="windy town street, gulls, a door bell",
      text="Iceland had already run public-sector trials between 2015 and 2019, with more than two thousand five hundred workers. They were reported around the world as a four-day week. They were actually five shorter days, of thirty-five or thirty-six hours.",
      kf="A colourful Reykjavik street of small painted houses with snowy mountains behind, and simple office workers in warm coats "
         "walking home in the daylight."),
 ryan("n42", "So, a four-day week. Over five days.", "with his hands in his hoodie pockets, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then gives a tiny shrug."),
 dict(id="n43", spk=M, eng="still", mv="in", sfx="cosy kitchen, an oven door, snow outside",
      text="Either way, it stuck. About eighty-six percent of Iceland's workforce has since moved to shorter hours, or gained the right to ask for them.",
      kf="A cosy Icelandic kitchen in the afternoon, a woman in a woollen jumper baking bread with her small daughter, snow falling "
         "outside the window. Exactly two people."),
 dict(id="n44", spk=M, eng="still", mv="right", sfx="quiet office, a pen tapping on a desk",
      text="Before everyone emails HR, the catches. The British companies volunteered, there was no proper control group, and most results were self-reported. And firms that sign up tend to be the ones that already think it'll work.",
      kf="A small group of cheerful people in a modern office all eagerly raising their hands at once, while a researcher with a clipboard "
         "watches them with one eyebrow raised."),
 dict(id="n45", spk=M, eng="still", mv="in", sfx="city street, a bus engine idling, doors hissing",
      text="A bigger 2025 study across six countries did use comparison companies, and still found real drops in burnout. But most of the people in it worked in offices. It's easier to squeeze a week of emails into four days than a week of bus routes.",
      kf="A bus driver in a cap at the wheel of a city bus looking calmly ahead, with a long queue of passengers boarding behind him. "
         "Exactly one person in front."),
 # --- countries
 dict(id="n46", spk=M, eng="card", card=dict(big="1,332 vs 1,800", small="HOURS WORKED PER YEAR: GERMANY vs USA (OECD)", bg="#2E4A62", accent="#F39C4F"),
      sfx="quiet office hum",
      text="Hours also vary a lot between countries. In 2025, the OECD put the average German worker at about thirteen hundred and thirty hours a year. The average American, about eighteen hundred."),
 dict(id="n47", spk=M, eng="still", mv="right", sfx="busy city street, traffic, a street vendor calling",
      text="In Mexico, it was around twenty-two hundred. The OECD warns these figures aren't perfectly comparable, but the gap between Germany and Mexico is still about twenty-two forty-hour weeks a year.",
      kf="A simple split scene: on the left a relaxed worker wheeling a bicycle out of a tidy office in the early afternoon sun; on the right "
         "a tired worker still at a desk under a lamp late in the evening. Exactly two people."),
 dict(id="n48", spk=M, eng="still", mv="in", sfx="lakeside, birds, a bicycle bell, distant laughter",
      text="Part of the difference is holidays. German law guarantees at least twenty days of paid leave, and collective agreements typically give around thirty. American federal law guarantees none.",
      kf="A sunny lake with a few small sailboats, families picnicking on the grass and people swimming off a wooden jetty."),
 dict(id="n49", spk=M, eng="still", mv="out", sfx="quiet room, a clock ticking",
      text="None of this is a law of physics. It's a choice each country makes, usually without anyone noticing they've made it.",
      kf="A simple flat globe on a wooden desk with a small brass alarm clock standing on top of it. No people."),
 # --- the case for the steady job
 dict(id="n50", spk=M, eng="still", mv="in", refs=["freelancer"], sfx="quiet cafe, a coffee machine hissing",
      text="So far, the nine-to-five isn't looking great. But the escape videos tend to skip a few things, starting with the obvious alternative. Working for yourself.",
      kf="The woman from the reference sitting in a bright cafe with her laptop and a coffee, looking confident, a small potted plant on "
         "the table. Exactly one person."),
 dict(id="n51", spk=M, eng="card", card=dict(big="1 IN 5", small="NEW US BUSINESSES GONE WITHIN A YEAR (BLS)", bg="#34495E", accent="#F2C14E"),
      sfx="quiet empty shop, a door bell",
      text="According to the US Bureau of Labor Statistics, about twenty percent of new businesses don't survive their first year. About half are gone within five."),
 dict(id="n52", spk=M, eng="still", mv="right", refs=["freelancer"], sfx="quiet flat at night, rain, a calculator beeping",
      text="Working for yourself also means nobody pays you to be ill. In Britain, the self-employed can't get Statutory Sick Pay. In America, they pay both halves of Social Security and Medicare tax, fifteen point three percent.",
      kf="The woman from the reference at her kitchen table late at night wrapped in a blanket, with a red nose and a box of tissues, still "
         "typing on her laptop next to a calculator and a pile of receipts. Exactly one person."),
 dict(id="n53", spk=M, eng="still", mv="in", sfx="doctor's waiting room, quiet, a water cooler gurgling",
      text="And in America, a job usually comes with health insurance. Employer plans cover almost a hundred and fifty-seven million people. In 2025, the average family plan cost about twenty-seven thousand dollars, and employers paid most of it.",
      kf="A calm doctor's waiting room with comfortable chairs, a water cooler and a potted plant, sunlight through the window. No people."),
 ryan("n54", "So the trap comes with dental.", "holding a mug, looking at camera with a small flat smile. Exactly one person.",
      "The young man speaks flatly to camera, then takes a small sip from the mug."),
 dict(id="n55", spk=M, eng="still", mv="out", sfx="empty village street, wind, a distant dog barking",
      text="There's also something less obvious. In 1929, the textile factory in the Austrian village of Marienthal closed, and nearly every family in the village was hit by unemployment. Researchers moved in to study what happened.",
      kf="A quiet 1930s Austrian village street with a large closed brick textile factory at the end, its tall chimney cold, a few simple "
         "houses along the road under a grey sky. No people."),
 dict(id="n56", spk=M, eng="ltx",
      text="They found the unemployed men walked more slowly down the street, and stopped more often. Eighty-eight out of a hundred weren't wearing a watch.",
      kf="A 1930s village bridge where several men in worn jackets and caps lean on the stone railing looking down at the river, and one "
         "man walks very slowly past them with his hands behind his back.",
      mv="The men lean on the railing and shift slightly, the walking man strolls very slowly across the bridge. Static camera."),
 dict(id="n57", spk=M, eng="still", mv="in", sfx="quiet village, a church bell far away",
      text="The researchers called all that free time a tragic gift. A job, it turns out, doesn't only pay you. It gives the day a shape, people to talk to, and a reason to put trousers on.",
      kf="A man in a worn jacket sitting alone on a kitchen chair in a bare 1930s room, looking at a pale empty patch on the wall where a "
         "clock used to hang. Exactly one person."),
 dict(id="n58", spk=M, eng="still", mv="right", refs=["freelancer"], sfx="park, birds, a dog panting",
      text="To be fair to the people who leave, the self-employed do tend to be more satisfied with their work, even after accounting for income and hours. Economists Matthias Benz and Bruno Frey put it down to independence.",
      kf="The woman from the reference working happily on her laptop on a sunny park bench, a dog lying at her feet. Exactly one person."),
 dict(id="n59", spk=M, eng="still", mv="in", refs=["worker"], sfx="quiet office, a wall clock ticking",
      text="That might be the real point. What people seem to dislike isn't work. It's having no say over when, where and how they do it.",
      kf="The man from the reference sitting at his office desk, pointing a small television remote control hopefully at the big wall "
         "clock above him. Exactly one person."),
 # --- verdict
 dict(id="n60", spk=M, eng="still", mv="out", sfx="quiet office at evening, a cleaner's trolley rolling",
      text="So, is working nine to five a trap?",
      kf="An empty office at sunset with rows of tidy desks, chairs pushed in, golden light pouring through the windows. No people."),
 dict(id="n61", spk=M, eng="still", mv="in", refs=["fordman", "worker"], sfx="windy hilltop, birds",
      text="Not really. The forty-hour week was a victory. People fought for it, and it was a huge improvement on seventy. The trap, if there is one, is treating a deal from the nineteen-twenties as if it were a law of nature.",
      kf="The man in overalls from the first reference and the office worker from the second reference standing side by side on a hill, "
         "looking up at a huge blank stone tablet, both scratching their heads. Exactly two people."),
 dict(id="n62", spk=M, eng="still", mv="right", refs=["worker"], sfx="city street at evening, birds, distant traffic",
      text="For a lot of people, a steady job is exactly the point. Security, colleagues, a pension, and a clear line where work stops. If that's you, it isn't a trap. It's a good deal, and you're allowed to like it.",
      kf="The man from the reference walking out of his office building at the end of the day, smiling and putting his phone away, the "
         "warm evening sun ahead of him. Exactly one person."),
 dict(id="n63", spk=M, eng="still", mv="in", sfx="empty office, air conditioning hum",
      text="But if your job is mostly about being seen at a desk until five, the evidence suggests the hours could be shorter, the commute could be optional, and the work would probably still get done. Possibly sooner.",
      kf="An empty office chair with a suit jacket draped over its back and a half-full coffee mug left on the desk, carefully arranged to "
         "look as if someone is still there. No people."),
 dict(id="n64", spk=M, eng="ltx", refs=["worker", "freelancer"],
      text="Tell us in the comments: is your nine-to-five a trap or a good deal? And subscribe. It takes less time than your commute.",
      kf="The man from the first reference and the woman from the second reference sitting side by side on a park bench in the sunshine, "
         "both turning to look at camera, the man holding a travel mug. Exactly two people.",
      mv="Both turn to look at camera; the woman raises one eyebrow and the man slowly checks his wristwatch. " + P1),
]
THUMB = dict(text="IS 9 TO 5|A TRAP?", refs=["worker"],
             kf="The man from the reference sitting at his office desk, which stands on top of a giant wooden mousetrap with its metal bar "
                "pulled back, looking up nervously at a big wall clock. Bright tangerine background. Exactly one person.")
TAIL = 2.4
