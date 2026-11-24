"""Is modern society making us more lonely? 10-minute LANDSCAPE explainer (fast flat pipeline).
Comedic personality: a kind, slightly bewildered flatmate noticing how strange modern life has become. Dry about convenience that
designs conversation out of the day, about friendship being measured in hours, and about experts arguing over loneliness online.
Warm and gentle; it never laughs at lonely people, only at the absurd corners of modern life. Balanced: both cases, honest verdict.
Sources: US Surgeon General advisory 'Our Epidemic of Loneliness and Isolation' (May 2023: ~half of US adults report loneliness; more
widespread than smoking, diabetes or obesity; mortality impact similar to smoking up to 15 cigarettes a day; ATUS time with friends
60 -> 20 min/day 2003-2020, time alone +24 h/month, ages 15-24 down nearly 70% (150 -> 40 min/day); individual recommendations incl.
reach out daily, join community groups, serve others, don't check your phone during meals with friends); Murthy interviews (NYT 2 May
2023, PBS: 15 minutes a day reaching out); Holt-Lunstad et al. 2010 PLoS Med (148 studies, 50% greater likelihood of survival);
WHO Commission on Social Connection report, 30 Jun 2025 (1 in 6 people affected; ~871,000 deaths a year, ~100 an hour; loneliness
defined as painful gap between desired and actual connections; ~24% lonely in low-income vs ~11% in high-income countries; poverty
limits time and places to meet); UK: Tracey Crouch given loneliness brief, Jan 2018, after the Jo Cox Commission (NPR/Guardian/BBC:
9 m people always or often lonely; ~200,000 older people without a conversation with friend or relative for over a month); Japan:
Tetsushi Sakamoto, Feb 2021, suicides rose for the first time in 11 years (Japan Times, Business Insider); US Census 2022 (one-person
households 29%, 13% in 1960); R. Putnam, 'Bowling Alone', J. of Democracy Jan 1995 (bowlers +10%, league bowling -40%, 1980-93) and
book (Simon & Schuster 2000); Buecker et al. 2021, Psychological Bulletin (loneliness in emerging adults 1976-2019 rose slightly;
'relatively small'); Hawkley et al. 2019 (US adults 57-85, loneliness nearly unchanged 2005-06 to 2015-16; later-born cohorts less
lonely; living alone linked to more loneliness); F. Bound Alberti, 'A Biography of Loneliness' (OUP 2019: before 1800 its language
did not exist); J. Haidt, 'The Anxious Generation' (2024) and C. Odgers' review in Nature 628 (29 Mar 2024: mostly correlational) and
Haidt's reply; Hunt et al. 2018, J. Social & Clinical Psychology (limiting social media to ~30 min/day for 3 weeks reduced loneliness
and depression); Orben & Przybylski 2019, Nature Human Behaviour (n = 355,358; tech use explains at most 0.4% of wellbeing variation;
eating potatoes nearly as negative, wearing glasses more); Harvard Study of Adult Development (since 1938; 268 Harvard sophomores incl.
JFK, later 456 inner-city Boston boys; Waldinger: relationship satisfaction at 50 predicted health at 80 better than cholesterol;
Harvard Gazette Apr 2017); J. Hall 2018 (~50 h casual friend, ~90 h friend, 200+ h close friend); Epley & Schroeder 2014, JEP: General
(Chicago train commuters had a more pleasant commute talking to a stranger than in solitude, predicted the opposite); Boothby, Cooney,
Sandstrom & Clark 2018, Psychological Science (the liking gap); Jumbo 'Kletskassa' chat checkouts, summer 2019 (Grocery Dive)."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Is Modern Society Making Us More Lonely"
ERA = "modern"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Gentle dusk palette of dusty blue, warm amber, soft lilac, cream and deep navy. "
         "Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. Clean simple "
         "background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Gentle dusk palette of dusty blue, warm amber, soft lilac, cream and deep navy. "
             "Show only what the description names. There are NO characters of any kind: no people, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "guy": "a modern young man in his late twenties as a simple flat vector character: short messy black hair, mustard-yellow hoodie, grey "
        "joggers, white trainers, small round head, dot eyes.",
 "gran": "an elderly woman in her late seventies as a simple flat vector character: short curly white hair, round glasses, lavender cardigan "
         "over a cream blouse, navy skirt, small round head, dot eyes, warm smile.",
 "teen": "a teenage girl of about sixteen as a simple flat vector character: long brown hair in a high ponytail, oversized dusty-blue hoodie, "
         "black leggings, white trainers, small round head, dot eyes.",
}
P1 = "Static camera. Characters keep the same faces and clothes."
RY = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
      "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
      "wall and a plant, ")
RYM = "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."
def ryan(id_, text, pose, mv): return dict(id=id_, spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"], text=text, kf=RY + pose, mv=mv + " " + RYM)
SHOTS = [
 # --- hook
 dict(id="l00", spk=M, eng="still", mv="in", refs=["guy"], sfx="quiet flat at night, a fridge humming, a pigeon cooing softly",
      text="We now have more ways to talk to each other than at any point in human history. And in 2018, Britain decided it needed a minister for loneliness.",
      kf="The man from the reference sitting alone on a sofa in a small flat at night, completely surrounded by a huge pile of silent "
         "communication devices: a smartphone, a laptop, a tablet, an old rotary telephone, a walkie-talkie, a fax machine and a vintage "
         "radio, while a grey carrier pigeon waits patiently on the windowsill holding a small blank envelope. He stares straight ahead "
         "with a blank expression. Exactly one person."),
 dict(id="l01", spk=M, eng="ltx", refs=["guy"],
      text="Video calls, group chats, instant messages. On paper, nobody has ever been less alone. In practice, a lot of evenings look like this.",
      kf="The man from the reference sitting alone at a small kitchen table at night, eating instant noodles straight from the pot, his "
         "phone lying face up beside him glowing softly. Exactly one person.",
      mv="His phone lights up and buzzes; he glances at it, slowly turns it face down, and carries on eating his noodles. " + P1),
 dict(id="l02", spk=M, eng="still", mv="out", sfx="city at night, distant traffic, a window sliding shut",
      text="So is modern society actually making us lonelier? It's one of those questions where everyone already knows the answer. They just don't agree on what it is.",
      kf="A tall simple apartment building at dusk with dozens of lit windows, and in each window a single person on their own doing "
         "something different: reading, cooking, watching television, watering a plant, staring at a phone."),
 dict(id="l03", spk=M, eng="still", mv="in", env=True, sfx="park at dusk, wind in the leaves, a distant dog",
      text="So let's look at the case that it is, the case that it isn't, and what actually seems to help. But first, what do we even mean by lonely?",
      kf="A quiet empty park bench under a single glowing street lamp at dusk, autumn leaves on the path, a city skyline in the distance. "
         "No people."),
 dict(id="l04", spk=M, eng="still", mv="right", sfx="quiet room, a clock ticking",
      text="Loneliness isn't the same as being alone. The World Health Organization describes it as the painful gap between the social connections you want and the ones you actually have.",
      kf="A simple flat illustration of a person standing on one cliff edge looking across a wide gap at a warm glowing cliff on the "
         "other side where a small group of friends sit around a campfire. Simple flat style."),
 dict(id="l05", spk=M, eng="still", mv="left", sfx="wedding reception chatter, cutlery, a lake lapping",
      text="Which means you can feel lonely at a wedding with two hundred guests, and perfectly content on your own in a cabin. Being alone is a situation. Loneliness is a feeling.",
      kf="A simple split scene: on the left, a woman in a party dress sitting alone at the end of a long crowded wedding table, everyone "
         "around her turned away chatting; on the right, a bearded man sitting happily alone on a wooden jetty by a lake cabin with a "
         "fishing rod and a flask of tea."),
 # --- how big is the problem
 dict(id="l06", spk=M, eng="card", card=dict(big="1 IN 2", small="US ADULTS REPORT LONELINESS (2023)", bg="#2E3A5C", accent="#F2B95A"),
      sfx="quiet office hum, a page turning",
      text="In 2023, the US Surgeon General, Vivek Murthy, issued an official advisory warning of an epidemic of loneliness and isolation. Roughly half of American adults said they'd experienced loneliness."),
 dict(id="l07", spk=M, eng="still", mv="in", sfx="press room, cameras clicking, murmuring",
      text="Surgeons General usually issue warnings about things like smoking. This one was about not having enough people to talk to. It pointed out that loneliness is more widespread than smoking, diabetes or obesity.",
      kf="A doctor in a white coat standing at a podium with a microphone, giving a very serious press conference to a small group of "
         "journalists holding notepads, cameras flashing. Simple flat style."),
 dict(id="l07b", spk=M, eng="still", mv="in", sfx="dark kitchen at night, a fridge humming",
      text="Murthy compares loneliness to hunger or thirst. A signal from your body that something you need is missing. Which also makes it a lot less embarrassing. Nobody thinks being hungry is a character flaw.",
      kf="A man in pyjamas standing in a dark kitchen at night, lit by the light of the open fridge, peering inside at empty shelves that "
         "hold only a single small glowing red heart. Exactly one person."),
 dict(id="l08", spk=M, eng="card", card=dict(big="15 A DAY", small="CIGARETTES: A SIMILAR RISK OF EARLY DEATH", bg="#4A3C5A", accent="#F2B95A"),
      sfx="quiet room, a lighter clicking far away",
      text="Then it made the comparison that got quoted everywhere. Lacking social connection, it said, carries a risk of early death similar to smoking up to fifteen cigarettes a day."),
 dict(id="l09", spk=M, eng="still", mv="out", env=True, sfx="quiet study, a clock ticking",
      text="That figure comes from a big review of a hundred and forty-eight studies. People with stronger social ties had about a fifty percent better chance of survival over the course of the studies. It's a rough comparison, not an exact exchange rate. But it isn't small.",
      kf="A simple old-fashioned brass balance scale on a cream background, one side holding a small pile of cigarettes and the other side "
         "holding a single empty armchair, the scale perfectly level. No people."),
 dict(id="l10", spk=M, eng="card", card=dict(big="1 IN 6", small="PEOPLE WORLDWIDE AFFECTED BY LONELINESS (WHO)", bg="#2E3A5C", accent="#C9B6E4"),
      sfx="busy international street, many voices",
      text="And it isn't just an American thing. In 2025, a World Health Organization commission estimated that one in six people worldwide is affected by loneliness."),
 dict(id="l11", spk=M, eng="card", card=dict(big="871,000", small="DEATHS A YEAR LINKED TO LONELINESS (WHO)", bg="#3C4A6B", accent="#F2B95A"),
      sfx="quiet hospital corridor, a distant monitor beeping",
      text="It linked loneliness to an estimated eight hundred and seventy-one thousand deaths a year. That's about a hundred every hour."),
 dict(id="l12", spk=M, eng="still", mv="in", sfx="grand old office, rain on tall windows, a clock ticking",
      text="Governments have noticed. In 2018, Britain gave one of its ministers responsibility for loneliness, carrying on work the MP Jo Cox had cared about deeply before she was killed. Most ministries deal with roads, taxes or hospitals. This one was handed a feeling.",
      kf="A grand old government office with tall windows, a single minister in a dark suit sitting at a huge empty wooden desk, looking "
         "down at one small red paper heart lying on the desk in front of her. Exactly one person."),
 dict(id="l13", spk=M, eng="still", mv="right", refs=["gran"], sfx="quiet living room, a clock ticking, rain outside",
      text="At the time, the government cited research suggesting more than nine million people in the UK always or often felt lonely. Around two hundred thousand older people hadn't had a conversation with a friend or relative in over a month.",
      kf="The old woman from the reference sitting in an armchair by a rainy window in a tidy living room, a cup of tea going cold beside "
         "her, looking at an old landline telephone on the side table. Exactly one person."),
 dict(id="l14", spk=M, eng="still", mv="out", sfx="Tokyo street at night, a train passing, light rain",
      text="In 2021, Japan followed with a minister of its own. During the pandemic, the number of suicides there had risen for the first time in eleven years.",
      kf="A quiet Tokyo side street at night in light rain, plain glowing round lanterns and softly lit house windows, a single person with an "
         "umbrella walking past. Exactly one person."),
 dict(id="l15", spk=M, eng="still", mv="in", env=True, sfx="city street at night, rain, a bus pulling away",
      text="So the problem is real, it's large, and it now has its own place in government. The harder question is whether modern life is what's causing it.",
      kf="A quiet modern city street at night in the rain, warm lit windows above closed shops, a single empty bus stop under a street "
         "lamp. No people."),
 # --- the case for yes
 dict(id="l16", spk=M, eng="card", card=dict(big="60 → 20", small="MINUTES A DAY WITH FRIENDS (US, 2003–2020)", bg="#2E3A5C", accent="#F2B95A"),
      sfx="quiet cafe, a few cups clinking",
      text="The case for yes starts with how we spend our time. In 2003, Americans spent about an hour a day with friends in person. By 2020, it was twenty minutes."),
 dict(id="l17", spk=M, eng="still", mv="right", refs=["guy"], sfx="quiet kitchen, a board game piece clacking",
      text="Over the same years, time spent alone went up by about twenty-four hours a month. That's like gaining an extra day every month, spent entirely in your own company.",
      kf="The man from the reference playing a board game against himself at his kitchen table, sitting on one side and leaning right over "
         "the board to make the move for the empty chair opposite, with great concentration. Exactly one person."),
 dict(id="l18", spk=M, eng="still", mv="in", refs=["teen"], sfx="quiet bedroom, distant playground, birds",
      text="To be fair, 2020 was a pandemic year. But the drop began long before lockdown, and it was steepest for fifteen to twenty-four year olds. Their time with friends fell by nearly seventy percent.",
      kf="The teenage girl from the reference sitting alone on her bedroom floor with her back against the bed, scrolling her phone, while "
         "through the window a sunny empty basketball court and playground sit unused. Exactly one person."),
 dict(id="l19", spk=M, eng="card", card=dict(big="13% → 29%", small="US HOUSEHOLDS OF ONE PERSON (1960 → 2022)", bg="#3C4A6B", accent="#C9B6E4"),
      sfx="quiet flat, a key turning in a lock",
      text="Households have shrunk too. In 1960, thirteen percent of American households were a single person. By 2022, it was twenty-nine percent."),
 dict(id="l20", spk=M, eng="still", mv="left", refs=["gran"], sfx="cosy living room, a cat purring, a television murmuring",
      text="Living alone isn't the same as being lonely. Plenty of people choose it and love it. But in studies of older adults, those who live alone do tend to report more loneliness.",
      kf="The old woman from the reference sitting in a cosy armchair in her tidy living room, holding a television remote control high "
         "above her head like a trophy, looking very pleased, a cat asleep on her lap. Exactly one person."),
 dict(id="l21", spk=M, eng="still", mv="in", env=True, sfx="bowling alley, pins crashing, a ball rolling",
      text="None of this is a new worry. Back in 1995, the political scientist Robert Putnam noticed something strange about bowling.",
      kf="A retro American bowling alley with shiny wooden lanes, rows of white pins and colourful bowling balls on a rack, warm lights. "
         "No people."),
 dict(id="l22", spk=M, eng="card", card=dict(big="-40%", small="LEAGUE BOWLING IN THE US (1980–1993)", bg="#4A3C5A", accent="#F2B95A"),
      sfx="bowling alley, a single ball rolling, pins falling",
      text="Between 1980 and 1993, the number of Americans who went bowling rose by about ten percent. But bowling in organised leagues fell by forty percent."),
 dict(id="l23", spk=M, eng="still", mv="right", sfx="empty bowling alley, one ball rolling, echo",
      text="People were still bowling. They just weren't doing it in teams, with the same faces every week, the kind of group where somebody notices if you don't turn up. He later turned it into a book called Bowling Alone.",
      kf="A single man in a bright bowling shirt bowling alone in a long empty bowling alley, with a whole row of empty team chairs and "
         "an untouched scoreboard area behind him. Exactly one person."),
 dict(id="l24", spk=M, eng="still", mv="out", sfx="small community hall, teacups, quiet chatter",
      text="His argument was that Americans were drifting away from clubs, churches, unions and neighbourhood groups. The places where you used to see the same people without having to arrange anything.",
      kf="A small town community hall with a long table where three elderly people sit at a club meeting with tea and biscuits, "
         "surrounded by rows and rows of empty chairs."),
 dict(id="l25", spk=M, eng="ltx",
      text="And modern convenience keeps quietly removing the small encounters. Food, shopping, banking and films now arrive without anyone needing to say a word.",
      kf="A simple apartment corridor with a closed front door; a delivery rider in a helmet is placing a paper food bag on the doormat in "
         "front of the door. Exactly one person.",
      mv="The delivery rider sets the bag down and walks away out of frame; then the door opens a crack and a hand slowly reaches out and "
         "pulls the bag inside. Static camera."),
 ryan("l26", "The self-checkout talks to me. Mostly accusations.", "holding a shopping basket with a single loaf of bread in it, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then slowly lowers the basket."),
 dict(id="l27", spk=M, eng="still", mv="in", refs=["teen"], sfx="park, birds, distant traffic",
      text="Then there's the phone. In his 2024 bestseller The Anxious Generation, the social psychologist Jonathan Haidt argues that smartphones and social media rewired childhood, swapping time with friends for time on screens.",
      kf="Four teenagers, including the girl from the reference, sitting together on a park bench, each staring down at their own glowing "
         "phone, none of them looking at each other, a frisbee lying forgotten on the grass. Exactly four people."),
 dict(id="l28", spk=M, eng="still", mv="right", sfx="university lawn, students chatting, birds",
      text="And there's some experimental support. In a 2018 University of Pennsylvania study, students who cut their social media to about thirty minutes a day for three weeks reported less loneliness and depression than those who didn't.",
      kf="A university student sitting on a sunny lawn happily handing his phone to a friend for safekeeping, while two other students "
         "next to him chat and laugh. Exactly four people."),
 dict(id="l29", spk=M, eng="still", mv="in", refs=["guy"], sfx="quiet bedroom at night, a phone buzzing softly",
      text="Which makes a certain sense. Social media lets you watch your friends having a great time without you, in high definition, from bed.",
      kf="The man from the reference lying in bed at night in the dark, his face lit blue by his phone, which shows a tiny bright party "
         "scene with dancing figures and balloons. Exactly one person in the bed."),
 # --- the case for 'not so fast'
 dict(id="l30", spk=M, eng="still", mv="out", env=True, sfx="quiet study, a desk lamp buzzing, papers shuffling",
      text="So, case closed? Not quite. When researchers try to measure loneliness itself over time, rather than how we spend our time, the picture gets surprisingly murky.",
      kf="A detective's magnifying glass lying on a wooden desk on top of a messy pile of papers covered in simple coloured lines and bars, "
         "a desk lamp glowing. No people."),
 dict(id="l31", spk=M, eng="still", mv="right", sfx="quiet library, a page turning",
      text="A 2021 analysis combined studies of young adults from 1976 to 2019. Loneliness did go up. Slightly. The lead researcher described the increase as relatively small.",
      kf="A very long staircase made of simple blocks stretching into the distance, where each step is only a tiny bit higher than the "
         "last, and a small hiker standing on it with hands on hips, looking unimpressed at the gentle slope. Exactly one person."),
 dict(id="l32", spk=M, eng="still", mv="in", refs=["gran"], sfx="busy cafe, laughter, cups clinking",
      text="Another study of older Americans found loneliness barely changed between 2005 and 2016. And people born more recently were, if anything, a little less lonely than those born earlier.",
      kf="The old woman from the reference laughing at a cafe table with two other elderly friends, cups of tea and slices of cake between "
         "them. Exactly three people."),
 dict(id="l33", spk=M, eng="card", card=dict(big="24% vs 11%", small="FEEL LONELY: POORER VS RICHER COUNTRIES (WHO)", bg="#2E3A5C", accent="#F2B95A"),
      sfx="quiet countryside, wind, a distant rooster",
      text="The WHO's own numbers complicate things too. About twenty-four percent of people in low-income countries say they feel lonely. In high-income countries, it's around eleven."),
 dict(id="l34", spk=M, eng="still", mv="left", sfx="dusty road at sunset, crickets",
      text="If wealthy, gadget-filled modern life were the main cause, you'd expect that the other way round. The WHO suggests poverty can limit the time and places people have to meet.",
      kf="A simple split scene: on the left, a tired farm worker walking home alone along a long dusty road at sunset; on the right, a "
         "bright modern apartment where a woman on a sofa laughs while video-calling friends on a laptop. Exactly two people."),
 dict(id="l35", spk=M, eng="still", mv="in", env=True, sfx="old study, a candle flickering, a quill scratching",
      text="And the past wasn't one long village party. The historian Fay Bound Alberti argues that loneliness, as we use the word now, is a fairly modern idea. Before about 1800, she says, the language for it barely existed.",
      kf="A cosy old eighteenth-century study with a feather quill, an inkwell and a big open old book with blank pages on a wooden desk, "
         "lit by candlelight. No people."),
 dict(id="l36", spk=M, eng="still", mv="right", sfx="medieval village, chickens, a cart rolling",
      text="People in the past certainly felt alone. And a tight-knit village is very sociable, right up until you fall out with half of it.",
      kf="A medieval village street where a lone villager carrying a basket of eggs walks past a group of six other villagers who all turn "
         "their backs on him with their arms folded."),
 dict(id="l37", spk=M, eng="card", card=dict(big="0.4%", small="OF TEEN WELLBEING LINKED TO TECH USE (OXFORD)", bg="#3C4A6B", accent="#C9B6E4"),
      sfx="quiet lab, computer fans humming",
      text="The phone debate is far from settled either. In 2019, Oxford researchers analysed data on more than three hundred and fifty thousand young people. Technology use explained at most zero point four percent of the variation in their wellbeing."),
 dict(id="l38", spk=M, eng="still", mv="in", env=True, sfx="quiet kitchen, a fork on a plate",
      text="To put that in context, they compared it with other habits in the same surveys. Regularly eating potatoes had almost the same association. Wearing glasses was worse.",
      kf="A single plain baked potato on a white plate, a pair of round glasses and a smartphone, all lined up neatly side by side on a "
         "table under a bright spotlight like suspects in a police line-up. No people."),
 ryan("l39", "Nobody's writing a bestseller about potatoes.", "holding a baked potato on a fork, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then looks down at the potato thoughtfully."),
 dict(id="l40", spk=M, eng="still", mv="out", env=True, sfx="quiet room, a clock ticking",
      text="When Haidt's book came out, the psychologist Candice Odgers reviewed it in the journal Nature. She argued most of the evidence is correlational. Maybe phones make people unhappy. Or maybe unhappy people spend more time on their phones.",
      kf="Two big simple curved arrows chasing each other in a circle on a cream background, one arrow pointing from a glowing smartphone "
         "to a small grey rain cloud, the other pointing from the rain cloud back to the smartphone. No people."),
 dict(id="l41", spk=M, eng="still", mv="right", sfx="quiet library, two keyboards typing fast",
      text="Haidt replied that experimental studies back him up, and that his critics haven't offered a better explanation for when the decline began. The argument continues. Mostly, it has to be said, online.",
      kf="Two academics in tweed jackets sitting at two separate desks back to back in a library, each typing furiously on a laptop, steam "
         "rising from their coffee mugs. Exactly two people."),
 dict(id="l42", spk=M, eng="still", mv="in", refs=["gran"], sfx="cosy living room, children giggling through a speaker",
      text="And phones connect people too. A grandmother can video call grandchildren on the other side of the world. A teenager who feels like the only one of their kind in a small town can find people who get them.",
      kf="The old woman from the reference in her armchair holding a tablet at arm's length, beaming and waving at two small children "
         "waving back on the screen. Exactly one person in the room."),
 # --- what matters
 dict(id="l43", spk=M, eng="still", mv="out", env=True, sfx="quiet living room at night, a kettle clicking off",
      text="So the honest answer on the trend is this. Probably somewhat lonelier, for some groups, but less dramatically than the headlines suggest. What nobody really disputes is how much connection matters.",
      kf="A cosy living room at night with two mugs of tea steaming on a coffee table and two armchairs turned towards each other, a lamp "
         "glowing warmly. No people."),
 dict(id="l44", spk=M, eng="still", mv="right", sfx="1930s university courtyard, footsteps, birds",
      text="The Harvard Study of Adult Development has followed the same people since 1938. It began with Harvard students, including a young John F. Kennedy, and later took in hundreds of boys from some of Boston's poorest neighbourhoods.",
      kf="A 1930s university courtyard with red-brick buildings and ivy, a queue of young men in tweed jackets and ties lining up outside "
         "a doctor's office, one of them having his height measured by a researcher in a white coat."),
 dict(id="l45", spk=M, eng="ltx",
      text="Its director, Robert Waldinger, says the clearest lesson is that good relationships keep us happier and healthier.",
      kf="Two elderly men in cardigans sitting side by side on a park bench laughing together, feeding pigeons, autumn trees behind them. "
         "Exactly two people.",
      mv="The two old men laugh together and one gently nudges the other with his elbow; a pigeon hops closer. Static camera. Exactly two "
         "people; they keep the same faces and clothes."),
 dict(id="l46", spk=M, eng="still", mv="in", sfx="park, birds, friends laughing",
      text="The men most satisfied with their relationships at fifty were the healthiest at eighty. Their cholesterol in middle age was a worse predictor of how they'd age.",
      kf="A cheerful elderly man in a cardigan walking briskly through a sunny park with a group of laughing friends, while far behind them "
         "a big wobbly yellow blob sits alone on a bench, looking ignored."),
 dict(id="l47", spk=M, eng="still", mv="out", refs=["guy"], sfx="quiet flat, a phone keyboard tapping",
      text="Which is oddly good news. You can't choose your genes. You can reply to a message.",
      kf="The man from the reference sitting on his sofa smiling as he types a reply on his phone, a mug of tea beside him, warm lamp "
         "light. Exactly one person."),
 # --- what helps
 dict(id="l48", spk=M, eng="card", card=dict(big="200 HOURS", small="TO BECOME CLOSE FRIENDS (HALL, 2018)", bg="#4A3C5A", accent="#F2B95A"),
      sfx="busy cafe, chatter, a coffee machine",
      text="The catch is that friendship takes time. A 2018 study by Jeffrey Hall estimated it takes about fifty hours together to go from acquaintance to casual friend, ninety to become friends, and over two hundred to become close friends."),
 ryan("l49", "That explains a lot about my thirties.", "with arms folded, looking at camera with a thoughtful flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then gives a slow small nod."),
 dict(id="l50", spk=M, eng="still", mv="right", sfx="cafe, cups clinking, pages flipping",
      text="School and university hand you those hours for free. After that, you mostly have to build them in on purpose. Which is harder when every adult you know is busy until roughly March.",
      kf="Two friends at a cafe table each holding up a huge paper wall calendar packed with colourful blocks, squinting at them across "
         "the table, trying to find a free day. Exactly two people."),
 dict(id="l51", spk=M, eng="still", mv="in", sfx="commuter train, rails clacking, a quiet announcement chime",
      text="The encouraging part is that we're bad at predicting how connection will go. In a 2014 study, commuters on trains into Chicago were asked to talk to a stranger. They expected it to be worse than sitting quietly. They actually enjoyed their journey more.",
      kf="A busy commuter train carriage where two strangers in work clothes sit next to each other chatting and smiling, while everyone "
         "else in the carriage stares silently ahead or down at their phones."),
 ryan("l52", "I'm still not talking to people on trains.", "with big headphones around his neck, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then slowly puts the headphones on."),
 dict(id="l53", spk=M, eng="still", mv="left", sfx="quiet street, footsteps, a door closing",
      text="Another study found that after chatting with someone new, people consistently underestimate how much the other person liked them. The researchers called it the liking gap. Your inner critic, it turns out, is a poor judge of character.",
      kf="Two people walking away from each other on a pavement after a chat, each with a small thought bubble above their head: the "
         "woman's bubble holds a big glowing heart, the man's bubble holds a tiny wilted flower. Exactly two people."),
 dict(id="l54", spk=M, eng="still", mv="in", sfx="supermarket, a till beeping slowly, friendly chatter",
      text="Some places are building small conversations back in on purpose. In 2019, the Dutch supermarket chain Jumbo introduced chat checkouts. Slower tills, for anyone who'd rather have a proper natter than rush.",
      kf="A bright supermarket checkout where an elderly man and a friendly cashier are deep in happy conversation, while two more "
         "elderly shoppers in the queue behind wait contentedly, leaning on their trolleys and joining in. Exactly four people."),
 dict(id="l55", spk=M, eng="still", mv="right", refs=["gran", "guy"], sfx="allotment, birds, a trowel in soil",
      text="And the official advice is refreshingly unglamorous. Murthy suggests about fifteen minutes a day reaching out to someone. The advisory adds: join a group that meets regularly, help other people, and don't check your phone during meals with friends.",
      kf="The old woman from the first reference and the young man from the second reference kneeling together at a community allotment, "
         "planting seedlings in a raised bed and laughing. Exactly two people."),
 dict(id="l56", spk=M, eng="still", mv="out", sfx="bowling alley, a strike, cheering",
      text="Which, if you think about it, is roughly a description of a bowling league.",
      kf="A cheerful bowling alley where a mixed team of young and old people in matching bowling shirts celebrate a strike together with "
         "high fives."),
 # --- verdict
 dict(id="l57", spk=M, eng="still", mv="in", env=True, sfx="park at dusk, wind in the leaves",
      text="So, is modern society making us more lonely?",
      kf="A quiet empty park bench under a single glowing street lamp at dusk, autumn leaves on the path, a city skyline in the distance. "
         "No people."),
 dict(id="l58", spk=M, eng="still", mv="out", sfx="city at night, distant traffic",
      text="Partly. We spend much less time with friends in person, more of us live alone, and a lot of the small everyday encounters have been designed out of our lives. That part is real.",
      kf="A tall simple apartment building at dusk with dozens of lit windows, and in each window a single person on their own doing "
         "something different: reading, cooking, watching television, watering a plant, staring at a phone."),
 dict(id="l59", spk=M, eng="still", mv="right", env=True, sfx="distant thunder, light rain on a roof",
      text="But the evidence that loneliness itself has exploded is weaker than the headlines suggest. Poorer countries report more of it than rich ones, and the case against phones is still being argued.",
      kf="A small calm sunny town under a clear sky, with one huge dramatic thundercloud hovering over it that is raining only on a single "
         "small garden shed. No people."),
 dict(id="l60", spk=M, eng="still", mv="in", refs=["guy", "gran"], sfx="apartment corridor, a knock on a door, a door opening",
      text="Maybe the fairest version is this. Modern life doesn't force us to be lonely. It just no longer forces us not to be. Connection used to come built in. Now it's something you have to choose.",
      kf="The young man from the first reference standing in an apartment corridor knocking on his neighbour's door, which is opened by the "
         "old woman from the second reference, smiling and holding a plate of biscuits. Exactly two people."),
 dict(id="l61", spk=M, eng="ltx", refs=["guy", "gran"],
      text="So reply to that message. Tell us in the comments who you're going to call. And subscribe. We'll keep you company.",
      kf="The young man from the first reference and the old woman from the second reference sitting side by side on a cosy sofa with mugs "
         "of tea, both turning to look at camera. Exactly two people.",
      mv="Both turn to look at camera; the old woman raises her mug in a small toast and the young man gives a little wave. " + P1),
]
THUMB = dict(text="LONELIER|THAN EVER?", refs=["guy"],
             kf="The man from the reference sitting alone on a sofa at night, buried up to his chest in a huge pile of glowing phones, laptops "
                "and old telephones, looking at camera with a sad, puzzled face, while a carrier pigeon sits on his head. Deep navy "
                "background with warm amber light. Exactly one person.")
TAIL = 2.4
