"""Are poor people poor because of bad decisions? 10-minute LANDSCAPE explainer (fast flat pipeline).
Comedic personality: a patient forensic accountant auditing a popular opinion. It reads the small print, itemises the bill and finds
the comedy in fees, in confident advice, in experiments that end up measuring the experimenters, and in the fact that being poor is
the most expensive way to live. Mostly straight-faced. It takes the 'decisions' case seriously and never mocks people living in poverty;
the jokes land on fees, myths, systems and the people handing out advice. Balanced: both cases, honest verdict.
Sources: CFPB overdraft reports (median fee ~$35, Dec 2023; 2014 Data Point: $24 overdraft repaid in 3 days with $34 fee = 17,000% APR);
Haskins & Sawhill, 'Creating an Opportunity Society' (Brookings 2009; via ACF/OPRE 'Success Sequence: A Synthesis of the Literature' 2020:
2.0% of households meeting all three norms in poverty vs 76.0% meeting none; the review says the evidence says less about causation;
Sawhill & Rodrigue 2016: full-time work the strongest factor); Wang & Wilcox, IFS/AEI 2017 'The Millennial Success Sequence' (97% of
millennials who followed it not poor at 28-34); CRS R48055 'Poverty in the United States in 2022' (1.9% of full-time year-round workers
18-64 in poverty); Watts, Duncan & Quan, Psychological Science 2018 (900+ children; correlation half the original size, reduced by two
thirds with controls for family background, early ability and home environment; Mischel's original children at Stanford's nursery);
Kidd, Palmeri & Aslin, Cognition 2013 'Rational snacking' (reliable adult: mean wait ~12 min; unreliable: ~3 min); Mani, Mullainathan,
Shafir & Zhao, Science 2013 'Poverty Impedes Cognitive Function' (New Jersey mall, $150 vs $1,500 car repair; effect comparable to losing
a full night's sleep; 464 Tamil Nadu sugarcane farmers worse before harvest than after); Mullainathan & Shafir, 'Scarcity' (2013,
'bandwidth tax'); Terry Pratchett, 'Men at Arms' (1993) boots theory ($50 boots last ten years, $10 boots a season or two, $100 over ten
years and still wet feet); CFPB (payday fee $15 per $100 for two weeks = almost 400% APR; 391% in the 2017 rule); Pew 2012 'Payday Lending
in America' ($375 loans, ~5 months in debt, $520 in fees; 69% for recurring expenses, 16% unexpected); Fair By Design / University of
Bristol PFRC, 'Paying More for Less: The Poverty Premium in 2026' (95% of low-income households pay it, average GBP 380 a year; one in ten
GBP 736 or more; energy prepayment, insurance, local supermarket branches, high-cost credit); Milanovic, REStat 2015 'Global Inequality of
Opportunity' (more than half of global income variability explained by country of residence) and VoxEU (97% live in their birth country);
UN SDG Report 2025 / World Bank June 2025 ($3.00/day line; about 808 m people in extreme poverty in 2025); Chetty et al., QJE 2014 'Where is
the Land of Opportunity?' (bottom-to-top-fifth odds 4.4% Charlotte vs 12.9% San Jose); HUD MTO (1994-98, 4,608 families, Baltimore,
Boston, Chicago, Los Angeles, New York, random assignment); Chetty, Hendren & Katz, AER 2016 (moved before 13: +31% earnings in
mid-twenties; older children, if anything, negative effects, perhaps disruption); US Census P70-137 'Dynamics of Economic Well-Being:
Poverty 2009-2011' (31.6% had a poverty spell of 2+ months; 3.5% poor all 36 months); Evans & Popova, World Bank WPS6886 2014 (19 studies,
44 estimates: no rise or a fall in alcohol and tobacco spending); Haushofer & Shapiro, QJE 2016 (GiveDirectly Kenya: assets such as
livestock, furniture and metal roofs, consumption, food security, no rise in alcohol or tobacco); Egger et al., Econometrica 2022 (about USD 1,000 to
10,500+ households in 653 villages; local multiplier 2.5); OpenResearch Unconditional Cash Study 2024 (1,000 people got $1,000/month for
three years, 2,000 controls got $50; 1.3 fewer work hours a week; about 5% lower earned income)."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Are Poor People Poor Because of Bad Decisions"
ERA = "modern"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Grounded warm palette of sage green, warm sand, terracotta, deep navy and soft gold. "
         "Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. Clean simple "
         "background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Grounded warm palette of sage green, warm sand, terracotta, deep navy and soft gold. "
             "Show only what the description names. There are NO characters of any kind: no people, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "jo": "a hard-working young mother as a simple flat vector character: woman in her early thirties, dark curly hair tied up in a puff, "
       "mustard-yellow work polo shirt, navy trousers, white trainers, a small canvas tote bag, small round head, dot eyes, tired but kind face.",
 "uncle": "a comfortable advice-giving older man as a simple flat vector character: neat silver hair, tanned face, sky-blue quarter-zip "
          "jumper, beige chinos, brown loafers, holding a takeaway coffee cup, small round head, dot eyes, very confident smile.",
 "farmer": "an Indian sugarcane farmer as a simple flat vector character: middle-aged man with short grey hair and a grey moustache, white "
           "cotton shirt, checked green and white cloth wrap around his waist, a thin towel over one shoulder, sandals, small round head, dot eyes.",
}
P1 = "Static camera. Characters keep the same faces and clothes."
RY = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
      "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
      "wall and a plant, ")
RYM = "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."
def ryan(id_, text, pose, mv): return dict(id=id_, spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"], text=text, kf=RY + pose, mv=mv + " " + RYM)
SHOTS = [
 # --- hook
 dict(id="p00", spk=M, eng="still", mv="in", refs=["jo"], sfx="quiet city street, a cash machine beeping, a single coin clinking",
      text="Are poor people poor because they make bad decisions? Possibly. Although in America, a bank can charge you thirty-five dollars for not having enough money.",
      kf="The woman from the reference standing at a cash machine set into a brick wall, holding her open purse, while a small mechanical hand "
         "has reached out of the machine's card slot and is politely taking her last coin. She stares at the hand flatly. Exactly one person."),
 dict(id="p01", spk=M, eng="card", card=dict(big="17,000%", small="AN OVERDRAFT FEE AS A YEARLY RATE (CFPB)", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet bank lobby, a pen tapping",
      text="It's called an overdraft fee. In 2014, America's consumer watchdog worked out that a typical overdraft, treated as a loan, has an annual interest rate of about seventeen thousand percent."),
 ryan("p02", "Can I get that rate on my savings?", "holding a small paper bank statement, looking at camera with a flat expression. Exactly one person.",
      "The young man looks up from the bank statement and speaks flatly to camera, then slowly folds the statement in half."),
 dict(id="p03", spk=M, eng="still", mv="in", env=True, sfx="quiet office, a desk lamp clicking on, paper rustling",
      text="So today, let's audit a popular opinion. The idea that people are poor mainly because of the choices they make. We'll look at the evidence for it, the evidence against it, and the bill.",
      kf="A wooden accountant's desk under a warm green desk lamp, with a big magnifying glass, a calculator and a very long paper receipt "
         "unrolling off the edge of the desk and across the floor. No people."),
 # --- the case for decisions
 dict(id="p04", spk=M, eng="still", mv="right", sfx="school corridor, a bell ringing, distant chatter",
      text="First, the case for. And it isn't a silly one. Choices clearly matter. Leaving school early, not working, or having children before you can support them all make life harder. Few researchers dispute that.",
      kf="A simple road splitting into three paths in front of a young person with a backpack: one path leads to a school, one to a busy "
         "workplace, one to a small family house. Exactly one person, seen from behind."),
 dict(id="p05", spk=M, eng="card", card=dict(big="2%", small="IN POVERTY AFTER ALL THREE STEPS", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet library, a page turning",
      text="In 2009, the Brookings researchers Ron Haskins and Isabel Sawhill popularised what's now called the success sequence. Finish high school, work full time, and marry before having children."),
 dict(id="p06", spk=M, eng="still", mv="in", env=True, sfx="quiet suburban street, birds",
      text="Of the households that managed all three, about two percent were poor. Of the households that managed none, seventy-six percent were.",
      kf="Two houses side by side: on the left a neat bright house with a sunny sky and a full fruit tree, on the right a small leaning house "
         "under a single grey rain cloud with a bucket catching drips by the door. No people."),
 dict(id="p07", spk=M, eng="card", card=dict(big="97%", small="OF MILLENNIALS WHO FOLLOWED IT: NOT POOR", bg="#2E4A62", accent="#F2A65A"),
      sfx="busy cafe, cups clinking",
      text="A 2017 study of millennials found the same pattern. Ninety-seven percent of those who followed the sequence weren't poor by their late twenties and early thirties."),
 dict(id="p08", spk=M, eng="still", mv="right", refs=["uncle"], sfx="back garden, a barbecue sizzling, birds",
      text="Those numbers get quoted a lot. Usually by someone who followed the sequence, and would like you to know about it.",
      kf="The man from the reference standing at a garden barbecue, pointing a pair of tongs at a polite young guest while explaining something "
         "at great length, the young guest holding a paper plate with a single sausage and nodding slowly. Exactly two people."),
 dict(id="p09", spk=M, eng="still", mv="in", refs=["jo"], sfx="supermarket, tills beeping, a trolley rattling",
      text="And work really is the big one. In 2022, fewer than two percent of working-age Americans who worked full time all year were in poverty. Brookings researchers found that of the three steps, a full-time job made by far the biggest difference.",
      kf="The woman from the reference working at a supermarket checkout, scanning groceries with a calm, focused face, a short queue of "
         "shoppers waiting. Exactly one person behind the till."),
 dict(id="p10", spk=M, eng="still", mv="out", sfx="quiet town square, a fountain, pigeons",
      text="So the decisions argument goes like this. Poverty isn't random. It's strongly linked to things people do. And telling people that nothing they do makes a difference isn't kindness. It's a polite way of giving up on them.",
      kf="A simple town square with a big old balance scale standing in the middle, one pan holding a school backpack and a work lunchbox, the "
         "other pan holding a single wedding ring, both pans level. No people."),
 # --- the audit: correlation, marshmallows
 dict(id="p11", spk=M, eng="still", mv="right", sfx="athletics track, a starting pistol, a small crowd",
      text="Now the audit. First, a correlation isn't a cause. People who manage school, steady work and marriage are often people who already had a stable home, a job nearby, and someone to help with the kids.",
      kf="A running race on a simple athletics track where most runners crouch at the starting line, while one runner in a smart outfit is "
         "already standing halfway down the track, stretching casually."),
 dict(id="p12", spk=M, eng="still", mv="in", env=True, sfx="quiet government office, papers shuffling",
      text="A 2020 review for the US government said much the same. The links are clear. Whether the sequence itself causes the results is much less clear.",
      kf="A tidy government office desk with a thick bound report, a pair of reading glasses resting on it and a small chain linking two "
         "puzzle pieces that don't quite fit together. No people."),
 dict(id="p13", spk=M, eng="still", mv="left", refs=["jo"], sfx="early morning bus stop, rain, a distant bus engine",
      text="Getting full-time work is partly a choice. It's also whether anyone nearby is hiring, whether the bus runs at six in the morning, and who looks after your kids.",
      kf="The woman from the reference waiting at a dark early-morning bus stop in the rain, holding a sleepy toddler on her hip and looking "
         "down an empty road. Exactly one adult and one small child."),
 dict(id="p14", spk=M, eng="still", mv="in", sfx="quiet nursery classroom, a clock ticking",
      text="Or take the most famous experiment about self-control, the marshmallow test. A small child gets one marshmallow now, or two if they can wait. The original studies, at Stanford University's nursery school, suggested the patient kids did better later in life.",
      kf="A small child sitting alone at a little table in a bright nursery room, staring intensely at a single white marshmallow on a plate, "
         "hands pressed flat on the table. Exactly one person."),
 dict(id="p15", spk=M, eng="ltx",
      text="In a 2013 study, an adult first made the children a promise. For some children, the adult kept it. For others, they didn't.",
      kf="A bright simple playroom: a friendly adult crouching beside a small child at a craft table, holding out a big box of new crayons, the "
         "child looking up hopefully. Exactly two people.",
      mv="The adult slowly holds the crayon box out towards the child, the child reaches up for it eagerly. " + P1),
 dict(id="p16", spk=M, eng="card", card=dict(big="12 MIN vs 3 MIN", small="HOW LONG CHILDREN WAITED", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet nursery, a clock ticking",
      text="The children whose adult had kept the promise waited about twelve minutes for the second marshmallow. The ones who'd just been let down waited about three."),
 dict(id="p17", spk=M, eng="still", mv="right", sfx="quiet nursery, a child chewing",
      text="That isn't a lack of self-control. If the adults around you break their promises, eating the marshmallow now is the sensible choice. It's the only one you're sure of.",
      kf="A small child calmly and happily eating a marshmallow at a little table, while in the doorway behind them an adult holds up an empty "
         "crayon box and shrugs apologetically. Exactly two people."),
 dict(id="p18", spk=M, eng="still", mv="out", sfx="university lecture hall, quiet murmuring",
      text="In 2018, a much bigger study of more than nine hundred children found the link to later success was half the original size. Once family background and home life were taken into account, it shrank by about two thirds.",
      kf="A long row of small children at little tables, each with one marshmallow on a plate, stretching far into the distance, a few "
         "researchers with clipboards walking along the row."),
 ryan("p19", "So the marshmallow was a background check.", "holding a single marshmallow between two fingers, looking at it and then at camera with a flat expression. Exactly one person.",
      "The young man holds up the marshmallow, speaks flatly to camera, then puts the marshmallow in his mouth."),
 # --- scarcity
 dict(id="p20", spk=M, eng="still", mv="in", env=True, sfx="shopping mall, footsteps, soft chatter, a fountain",
      text="But maybe the question is the wrong way round. Maybe being poor changes how people decide. That's what the economist Sendhil Mullainathan and the psychologist Eldar Shafir set out to test.",
      kf="A bright simple shopping mall corridor with a small folding research table set up in the middle, two empty chairs, a tablet computer "
         "and a neat stack of paper on it, shop fronts in the background. No people."),
 dict(id="p21", spk=M, eng="still", mv="right", sfx="shopping mall, footsteps, a car alarm far away in the car park",
      text="At a shopping mall in New Jersey, they asked shoppers to imagine their car needed repairs. For some, the bill was a hundred and fifty dollars. For others, fifteen hundred. Then everyone did a reasoning test.",
      kf="A shopper sitting at a small research table in a mall, holding a tablet, with a big thought bubble above their head showing a "
         "small grey car with smoke coming out of the bonnet. Exactly one person."),
 dict(id="p22", spk=M, eng="still", mv="in", sfx="shopping mall, a quiet murmur",
      text="With the small bill, richer and poorer shoppers did about equally well. With the big bill, the poorer shoppers' scores dropped.",
      kf="Two shoppers side by side at a research table doing a puzzle on tablets: the one on the left relaxed, the one on the right sweating "
         "slightly with a huge thought bubble above their head full of spanners and coins. Exactly two people."),
 dict(id="p23", spk=M, eng="still", mv="out", sfx="quiet bedroom at night, a clock ticking, an owl outside",
      text="The drop was about as big as the effect of losing a full night's sleep. And nothing had actually happened. They were only imagining the bill.",
      kf="A person sitting up in bed at night with wide tired eyes, a small grey car parked at the end of the bed like a pet, moonlight "
         "through the window. Exactly one person."),
 dict(id="p24", spk=M, eng="still", mv="in", sfx="quiet outdoor ambience, birds, distant traffic", refs=["farmer"],
      text="Next, they went to India, to sugarcane farmers who get most of their money once a year, at harvest.",
      kf="The man from the reference standing in a tall green sugarcane field under a bright sun, holding a long curved harvesting knife, "
         "bundles of cut cane at his feet. Exactly one person.",
      mv_ltx="The man wipes his brow with the towel from his shoulder and looks out across the swaying sugarcane. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="p25", spk=M, eng="still", mv="in", refs=["farmer"], sfx="village courtyard, birds, a distant tractor",
      text="Before the harvest, money is tight and loans pile up. After it, they've got cash. The same farmers did noticeably worse on the tests before the harvest than after.",
      kf="The man from the reference sitting on a wooden bench outside his village house, frowning hard at a simple coloured-shape puzzle on a "
         "clipboard, while a small pile of borrowed cooking pots and a goat wait beside him. Exactly one person."),
 dict(id="p26", spk=M, eng="still", mv="right", refs=["farmer"], sfx="village evening, crickets, a fire crackling",
      text="They hadn't become less intelligent and then cleverer again a few weeks later. Their minds were simply busy with money. The researchers call it a bandwidth tax.",
      kf="The man from the reference sitting relaxed under a tree in the evening after harvest, smiling and finishing the same puzzle easily, "
         "a big neat stack of cut sugarcane behind him. Exactly one person."),
 dict(id="p27", spk=M, eng="still", mv="in", refs=["jo"], sfx="small kitchen at night, a pot bubbling, a phone buzzing, a toddler babbling",
      text="It helps explain things that look like bad decisions from the outside. A missed appointment. A form filled in wrong. A bill paid late. When your head is full of this week, next year is hard to plan for.",
      kf="The woman from the reference at a small kitchen table at night, holding a phone to her ear and a pile of envelopes in her other "
         "hand, a toddler tugging her sleeve and a pot boiling over on the stove behind her. Exactly one adult and one small child."),
 dict(id="p28", spk=M, eng="still", mv="out", sfx="quiet office late at night, a keyboard, a radiator ticking",
      text="Most people know a mild version of this. In the week before a big deadline, you forget birthdays and eat cereal for dinner. Now imagine the deadline never ends.",
      kf="An office worker at a desk late at night surrounded by sticky notes and coffee cups, eating cereal from a bowl with one hand while "
         "typing with the other. Exactly one person."),
 # --- the poverty premium
 dict(id="p29", spk=M, eng="still", mv="right", sfx="cobbled street in the rain, footsteps, a squelch",
      text="Then there's the price of being poor. In his 1993 novel Men at Arms, Terry Pratchett gave a city guard a theory about boots. Good boots cost fifty dollars and last ten years. Cheap ones cost ten and fall apart in a season or two.",
      kf="A rainy old cobbled street: a pair of sturdy shiny leather boots standing on one side, and on the other side a tall pile of worn-out "
         "cheap boots with flapping soles. No people."),
 dict(id="p30", spk=M, eng="still", mv="in", sfx="rain on a window, a dripping sock",
      text="Over ten years, the poor man spends a hundred dollars on boots and still has wet feet. People now call it the boots theory. It may be the only well-known economic idea first explained by a fictional policeman.",
      kf="A man in an old guard's uniform sitting on a stool in a small room, wringing out a soggy sock over a bucket, a row of broken cheap "
         "boots lined up behind him. Exactly one person."),
 dict(id="p31", spk=M, eng="card", card=dict(big="391%", small="TYPICAL PAYDAY LOAN, AS A YEARLY RATE", bg="#5A3C3C", accent="#F2C14E"),
      sfx="small shop, a door chime, a till drawer",
      text="Real life has plenty of boots. A typical payday loan in America charges fifteen dollars for every hundred you borrow for two weeks. Over a year, that's a rate of almost four hundred percent."),
 dict(id="p32", spk=M, eng="still", mv="left", env=True, sfx="busy high street, traffic, a shop door chime",
      text="Pew found the average borrower borrows three hundred and seventy-five dollars at a time, stays in debt about five months a year, and pays around five hundred and twenty dollars in fees.",
      kf="A small bright shopfront with a yellow awning on a high street, its window full of gold coins on little stands, and a long paper "
         "chain of receipts trailing out of the door and along the pavement. No people."),
 dict(id="p33", spk=M, eng="still", mv="in", refs=["uncle"], sfx="quiet cafe, a spoon stirring",
      text="The decisions side has a point here. Payday loans are a terrible deal. And most borrowers in Pew's survey used them for regular bills like rent and food, not emergencies.",
      kf="The man from the reference sitting at a pavement cafe table, stirring his coffee and shaking his head disapprovingly at a small "
         "shopfront with a bright yellow awning and gold coins in its window across the street. Exactly one person."),
 dict(id="p34", spk=M, eng="still", mv="out", refs=["jo"], sfx="quiet flat, a fridge humming, rain outside",
      text="But that's also the problem. If your income doesn't cover the rent, the choice isn't between a payday loan and a sensible savings plan. It's between a payday loan and something worse.",
      kf="The woman from the reference standing in a small kitchen between two doors, one door with a gold coin painted on it and the other "
         "door dark with a storm cloud behind it, holding her rent money envelope, looking at both. Exactly one person."),
 dict(id="p35", spk=M, eng="card", card=dict(big="£380", small="AVERAGE UK POVERTY PREMIUM A YEAR (2026)", bg="#3C5A50", accent="#F2A65A"),
      sfx="British high street, a bus pulling away",
      text="In Britain, University of Bristol researchers found that nineteen in twenty low-income households pay a poverty premium. On average, three hundred and eighty pounds a year extra for the same essentials."),
 dict(id="p36", spk=M, eng="still", mv="right", env=True, sfx="hallway, an electricity meter clicking, coins",
      text="It comes from prepayment energy meters, pricier insurance, high-cost credit, and shopping at small local branches instead of big cheap supermarkets.",
      kf="A narrow hallway with an old electricity meter on the wall that has a small coin slot and a hungry open mouth, a little pile of "
         "coins on the floor beneath it. No people."),
 dict(id="p37", spk=M, eng="still", mv="in", refs=["jo"], sfx="supermarket aisle, a trolley wheel squeaking",
      text="Bulk buying is a classic. The giant pack of toilet roll is cheaper per roll. But you need the money for the giant pack, somewhere to keep it, and ideally a car to get it home.",
      kf="The woman from the reference in a supermarket aisle holding a single small four-pack of toilet roll, looking up at an enormous "
         "towering multipack of toilet roll on the shelf that is taller than her. Exactly one person."),
 ryan("p38", "Money's cheaper if you've already got some.", "leaning on a kitchen counter with arms folded, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, arms folded, then gives a slow single nod."),
 # --- where you're born
 dict(id="p39", spk=M, eng="still", mv="out", env=True, sfx="wind high in the sky, distant birds, flapping wings",
      text="Then there's the decision none of us got to make. Where we were born.",
      kf="A big round globe floating in a soft blue sky, with a flock of white storks flying around it, each carrying a small cloth bundle "
         "and dropping them gently onto different countries. No people."),
 dict(id="p40", spk=M, eng="card", card=dict(big="50%+", small="OF GLOBAL INCOME GAPS: YOUR COUNTRY", bg="#2E4A62", accent="#F2C14E"),
      sfx="busy airport hall, announcements muffled, footsteps",
      text="The economist Branko Milanovic estimated that more than half of the differences in income between people around the world can be explained by the country they live in."),
 dict(id="p41", spk=M, eng="still", mv="in", sfx="quiet maternity ward, a baby gurgling",
      text="And about ninety-seven percent of people still live in the country they were born in. So the biggest financial decision most people ever face was made before they were born, by nobody.",
      kf="A row of newborn babies in little cots in a simple hospital nursery, each baby wrapped in a blanket of a different bright colour, "
         "all looking up calmly."),
 dict(id="p42", spk=M, eng="still", mv="right", sfx="rural village, roosters, wind in dry grass",
      text="In 2025, around eight hundred million people lived in extreme poverty, on less than three dollars a day. That isn't eight hundred million people all making the same mistake.",
      kf="A wide dry rural landscape at sunrise with many small simple homes scattered across the hills, people walking along paths carrying "
         "water cans and firewood."),
 # --- where you grow up
 dict(id="p43", spk=M, eng="still", mv="in", sfx="quiet suburban street, a school bell far away, children playing",
      text="Even inside one rich country, where you grow up matters. The economist Raj Chetty and his team followed millions of American children into adulthood.",
      kf="A simple map of the United States made of patchwork fabric squares in different colours, with tiny houses and schools dotted "
         "across it. No people."),
 dict(id="p44", spk=M, eng="card", card=dict(big="4.4% vs 12.9%", small="POOREST FIFTH TO RICHEST FIFTH", bg="#3C5A50", accent="#F2C14E"),
      sfx="city traffic, distant sirens",
      text="A child from the poorest fifth of families had a four point four percent chance of reaching the richest fifth if they grew up in Charlotte, North Carolina. In San Jose, California, it was nearly thirteen percent."),
 dict(id="p45", spk=M, eng="still", mv="left", env=True, sfx="wind, distant city traffic",
      text="Same country. Same currency. Same flag. Roughly three times the odds.",
      kf="Two small cities side by side on two hills, each with a tall wooden ladder reaching up to a golden sun: the left ladder has most of "
         "its rungs missing, the right ladder is complete. No people."),
 dict(id="p46", spk=M, eng="still", mv="in", refs=["uncle"], sfx="quiet office, a pen clicking",
      text="Of course, you could argue that families in some places just make worse choices. Which is why it helps that there was an experiment.",
      kf="The man from the reference standing in front of a big map pinned to a wall, confidently pointing at one spot with his coffee cup, "
         "while a small sticky note on the map behind him is about to fall off. Exactly one person."),
 dict(id="p47", spk=M, eng="still", mv="right", sfx="quiet outdoor ambience, birds, distant traffic", refs=["jo"],
      text="In the 1990s, an American programme called Moving to Opportunity offered families in public housing vouchers to move to lower-poverty neighbourhoods.",
      kf="The woman from the reference and a small child carrying cardboard boxes out of a tall grey apartment block towards a small moving "
         "van parked on the street. Exactly one adult and one small child.",
      mv_ltx="The woman and the child carry the boxes to the van and the woman lifts one into the back. " + P1),
 dict(id="p48", spk=M, eng="still", mv="right", env=True, sfx="community hall, a raffle drum turning, murmuring",
      text="About four thousand six hundred families signed up, in Baltimore, Boston, Chicago, Los Angeles and New York. Who got the vouchers was decided at random, like a lottery.",
      kf="A big wooden raffle drum full of small paper house shapes on a table in a community hall, rows of empty folding chairs in front "
         "of it. No people."),
 dict(id="p49", spk=M, eng="card", card=dict(big="+31%", small="ADULT EARNINGS, MOVED BEFORE AGE 13", bg="#2E4A62", accent="#F2A65A"),
      sfx="quiet leafy street, birds, a lawnmower far away",
      text="Years later, Chetty's team checked on the children. Those who moved before thirteen earned thirty-one percent more in their mid-twenties than those who didn't get the chance."),
 dict(id="p50", spk=M, eng="still", mv="in", sfx="leafy suburban street, birds, children laughing",
      text="The families had all applied for the same chance. Only the street was different. For teenagers who moved, the benefit didn't show up at all, possibly because moving at that age is disruptive.",
      kf="A leafy quiet street with a small house and garden, a young child on a bicycle riding past a library, while a teenager sits on the "
         "front step looking a bit lost with a cardboard box beside them. Exactly two people."),
 # --- luck and churn
 dict(id="p51", spk=M, eng="still", mv="out", sfx="busy train station concourse, footsteps, announcements muffled",
      text="Poverty also isn't a fixed group of people. Between 2009 and 2011, almost a third of Americans spent at least two months in poverty. Only three and a half percent were poor the whole time.",
      kf="A big busy station concourse seen from above with crowds of simple commuters walking in all directions, a few of them stepping in "
         "and out of a soft grey shadow on the floor."),
 dict(id="p52", spk=M, eng="still", mv="in", refs=["jo"], sfx="roadside, wind, a car engine ticking as it cools, a distant siren",
      text="Which means poverty is often something that happens to people, not something they are. A lost job, an illness, a break-up, a car that won't start. Things that happen to people who make good decisions too.",
      kf="The woman from the reference standing beside a small old car on a rural roadside with its bonnet open and steam rising, holding her "
         "phone and looking at the sky. Exactly one person."),
 # --- the cash test
 dict(id="p53", spk=M, eng="still", mv="right", env=True, sfx="quiet room, an envelope tearing",
      text="Here's a fairly direct test. If bad choices were the main problem, then giving people money should mostly be wasted. Researchers have tried it many times.",
      kf="A plain brown paper envelope on a simple wooden table, opened, with a neat stack of banknotes poking out, sunlight across the table. "
         "No people."),
 dict(id="p54", spk=M, eng="card", card=dict(big="19 STUDIES", small="NO RISE IN ALCOHOL OR TOBACCO SPENDING", bg="#5A3C3C", accent="#F2C14E"),
      sfx="quiet office, a printer whirring",
      text="In 2014, a World Bank review of nineteen studies looked at whether cash transfers get spent on alcohol and tobacco. Almost every result showed either no change, or a fall."),
 dict(id="p55", spk=M, eng="still", mv="in", sfx="Kenyan village, goats bleating, a hammer on metal, children playing",
      text="In rural Kenya, the charity GiveDirectly gives poor families large one-off cash grants. In an early study, people mostly spent the money on food, livestock, furniture and metal roofs.",
      kf="A sunny Kenyan village with a man fixing a shiny new metal roof onto a small house, a woman leading two goats, and a small busy "
         "roadside shop selling fruit."),
 dict(id="p56", spk=M, eng="still", mv="right", sfx="busy village market, chatter, a bicycle bell",
      text="A later study gave about a thousand dollars each to more than ten thousand households. For every dollar given, local economic activity rose by about two and a half dollars, because the shops that got the money spent it too.",
      kf="A lively village market with many small stalls, a few coins visibly passing from hand to hand along a chain of smiling stallholders "
         "and customers."),
 dict(id="p57", spk=M, eng="still", mv="out", sfx="quiet American suburb, a dog barking far away",
      text="To be fair, cash isn't magic. In a big American study, a thousand people got a thousand dollars a month for three years. They worked a little over an hour less each week than the comparison group, and earned about five percent less from their jobs.",
      kf="A modest American house porch with a mailbox full of envelopes, a person sitting on the porch step with a cup of coffee, looking "
         "calmly at the street. Exactly one person."),
 dict(id="p58", spk=M, eng="still", mv="in", sfx="quiet kitchen, a kettle clicking off",
      text="Money mostly gets spent on what people say they need. Which is roughly what you'd expect if the main problem was a lack of money.",
      kf="A simple kitchen table with a bag of groceries, a pair of new children's school shoes and a small calculator, morning "
         "light through the window. No people.", env=True),
 # --- verdict
 dict(id="p59", spk=M, eng="still", mv="out", env=True, sfx="quiet office, a desk lamp humming",
      text="So, are poor people poor because of bad decisions?",
      kf="The same wooden accountant's desk under a warm green desk lamp, the very long paper receipt now neatly rolled up and tied with a "
         "string, the magnifying glass resting on top. No people."),
 dict(id="p60", spk=M, eng="still", mv="in", sfx="school corridor, distant chatter",
      text="Sometimes, partly. Choices do matter, and the success sequence isn't wrong that finishing school, steady work and a stable family make poverty much less likely.",
      kf="A young adult in a graduation gown walking confidently along a sunny path towards a small house, a work lanyard around their neck. "
         "Exactly one person."),
 dict(id="p61", spk=M, eng="still", mv="right", env=True, sfx="park, wind in trees, a chess clock ticking",
      text="But those choices are made on a very uneven board. Where you're born, where you grow up, what happens to you, and what poverty itself costs all shape the options before anyone decides anything.",
      kf="A big chessboard in a park where one side has a full set of shiny pieces and the other side has only a few small chipped pawns, "
         "the board itself tilted downhill towards the pawns. No people."),
 dict(id="p62", spk=M, eng="still", mv="in", refs=["jo", "uncle"], sfx="busy high street, footsteps, a till beeping",
      text="And being poor makes good decisions harder and bad ones more expensive. When a rich person makes a mistake, it's an anecdote. When a poor person makes one, it comes with a late fee.",
      kf="The man from the second reference laughing as he drops his takeaway coffee on a sunny pavement, while the woman from the first "
         "reference, standing next to him, drops a single coin down a drain and is immediately handed a small paper bill by a mechanical arm "
         "coming out of the drain. Exactly two people."),
 ryan("p63", "Plus thirty-five dollars.", "holding a single coin up between two fingers, looking at camera with a flat expression. Exactly one person.",
      "The young man holds up the coin, speaks flatly to camera, then lets the coin drop out of frame."),
 dict(id="p64", spk=M, eng="still", mv="out", sfx="quiet town square, a fountain, pigeons",
      text="So maybe the better question isn't whether poor people make bad decisions. Everyone does. It's why some people's bad decisions cost so much more.",
      kf="A simple town square with the big old balance scale from before, now one pan holding a single tiny coin and pressed all the way down, "
         "and the other pan holding a huge bag of gold floating high. No people."),
 dict(id="p65", spk=M, eng="ltx", refs=["jo", "uncle"],
      text="Tell us in the comments what you think. And subscribe. It's free, which, as we've learned, is unusually generous.",
      kf="The woman from the first reference and the man from the second reference sitting side by side on a park bench, both turning to look "
         "at camera, the man holding his takeaway coffee and the woman holding her purse. Exactly two people.",
      mv="Both turn to look at camera; the man takes a slow sip of coffee and the woman raises one eyebrow and closes her purse. " + P1),
]
THUMB = dict(text="BAD|DECISIONS?", refs=["jo"],
             kf="The woman from the reference holding her open purse upside down with a shocked face, while a cash machine beside her has stuck "
                "out a small mechanical hand and is holding out its palm towards her, one coin falling into it. Bright terracotta background. "
                "Exactly one person.")
TAIL = 2.4
