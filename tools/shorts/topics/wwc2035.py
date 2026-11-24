"""FIFA and the 2035 Women's World Cup: the future of women's football. 10-minute LANDSCAPE video (fast flat pipeline).
Comedic personality: a calm narrator quietly amazed at how long the people in charge took to notice something obvious; the jokes aim at
institutions (the FA, FIFA), never at the players. Mostly plain facts; the future section stays honest, not cheerleading.
Sources: The FA, "UK to host FIFA Women's World Cup 2035" (23 Nov 2026: 48 teams, 104 matches, 39 days, 22 venues in 16 cities, 4.5 m tickets,
3.5 bn TV, legacy aims, 'parks and playgrounds'); AP 23 Nov 2026 (only valid bid, 2031 US/Mexico/Costa Rica/Jamaica, 2027 Brazil, 1991 12 teams);
Wikipedia "Dick, Kerr Ladies F.C." (1917 Preston munitions works team, beat factory men, Alfred Frankland, 53,000 at Goodison 26 Dec 1920,
FA resolution 5 Dec 1921 "quite unsuitable for females and should not be encouraged", receipts/expenses complaint, lifted 1971, 755 games 682 wins);
Wikipedia "1991 FIFA Women's World Cup" (80-minute matches, M&M's Cup name, USA 2-1 Norway, 63,000); FIFA "Women's World Cup 2023 Impact"
(USD 110 m prize money, defined amount per player, average salary USD 16,825, 1,978,274 attendance); Wikipedia "2035 FIFA Women's World Cup"
(Man Utd interest in unbuilt 100,000-seat stadium, FA prefers Wembley)."""
ERA = "football"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
VOICE_REF = {"maya": {"ref_audio": "library/voices/maya/ref_lively.wav", "ref_text": "library/voices/maya/ref_lively.txt"}}
H3_REF_KF = True
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Bright friendly palette of grass green, navy, coral, warm cream and mustard yellow. "
         "Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. Clean simple "
         "background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Bright friendly palette of grass green, navy, coral, warm cream and mustard yellow. "
             "Show only what the description names. There are NO characters of any kind: no people, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "dkl": "a 1920 English women's footballer as a simple flat vector character: young woman, short dark bobbed hair under a small black-and-white "
        "striped cap, black-and-white vertically striped long-sleeved jersey, dark knee-length shorts, long dark socks, brown leather boots, "
        "small round head, dot eyes.",
 "fa": "a 1921 football official as a simple flat vector character: elderly stout man, grey walrus moustache, bald head, dark three-piece suit "
       "with a pocket watch chain, stiff white collar, small round head, dot eyes, stern expression.",
 "girl": "a modern ten-year-old girl as a simple flat vector character: curly black hair in two puffs, bright orange t-shirt, navy shorts, "
         "white socks, trainers, small round head, dot eyes, big grin.",
}
P1 = "Exactly one person; she keeps the same face and clothes. Static camera."
SHOTS = [
 # --- cold open
 dict(id="w01", spk=M, eng="ltx", env=True,
      text="On the twenty-third of November 2026, FIFA confirmed who will host the 2035 Women's World Cup. England, Scotland, Wales and Northern Ireland.",
      kf="A shiny golden football trophy cup on a navy podium under a spotlight, a simple soft green outline map of Great Britain and "
         "Ireland glowing behind it, colourful confetti in the air.",
      mv="Golden confetti drifts down slowly, the flags wave gently, the trophy gleams. Static camera."),
 dict(id="w02", spk=M, eng="still", mv="in", sfx="large conference hall, polite applause, murmuring",
      text="Theirs was the only valid bid, so it wasn't the tensest vote FIFA has ever held.",
      kf="A huge formal conference hall with rows of identical delegates as simple round-headed figures in dark suits, all holding up green voting "
         "cards, one delegate at the front yawning. Wide shot."),
 dict(id="w03", spk=M, eng="still", env=True, mv="right", sfx="quiet library room tone, a clock ticking",
      text="It's a big moment for the country that wrote football's first rulebook. It's also slightly awkward, because that same country once kept women off its football pitches for fifty years.",
      kf="An old leather-bound rulebook lying open on a wooden desk beside a football and an old ink pen, a dusty window behind, warm light."
         " No people."),
 dict(id="w03b", spk=M, eng="still", mv="in", sfx="old pub, quiet chatter, a clock ticking",
      text="England has hosted a men's World Cup exactly once, in 1966, and won it. People here still bring it up. This will be the first time any of the four nations has hosted the women's tournament.",
      kf="A cosy old pub corner: an elderly man in a flat cap proudly pointing at a small faded framed photo of a football team on the wall, "
         "while the young barman behind the counter rolls his eyes. Simple flat style."),
 dict(id="w04", spk=M, eng="card", card=dict(big="1917", small="PRESTON, ENGLAND", bg="#2E4A62", accent="#F2C14E"),
      sfx="old factory machinery hum in the distance",
      text="So how do you get from that to hosting the biggest tournament in women's sport? It starts in a factory in Preston."),
 # --- Dick, Kerr Ladies
 dict(id="w05", spk=M, eng="ltx",
      text="In 1917, Britain was at war, and the Dick, Kerr and Company works was full of women making ammunition.",
      kf="A simple flat factory floor in 1917: a row of women workers in khaki overalls and headscarves at long workbenches, filling and stacking "
         "brass artillery shells, big round windows, warm light. Simple round-headed figures.",
      mv="The workers stack the shells steadily along the bench, a conveyor belt moves slowly. Static camera."),
 dict(id="w06", spk=M, eng="still", mv="in", sfx="factory yard, distant machinery, birds",
      text="The bosses believed a bit of organised sport would keep morale up and production high. So football was, technically, an efficiency measure.",
      kf="A plump factory manager in a grey suit at a desk, looking at a simple upward line graph on a board next to a leather football, nodding. "
         "Exactly one person."),
 dict(id="w07", spk=M, eng="ltx", refs=["dkl"],
      text="During their lunch and tea breaks, the women started kicking a ball around the factory yard.",
      kf="The woman from the reference, wearing khaki overalls instead of her kit, kicking an old leather football across a cobbled factory yard, "
         "red brick walls and a tall chimney behind. Exactly one person.",
      mv="She dribbles the ball forward and kicks it, the ball rolls away, she runs after it smiling. " + P1),
 dict(id="w08", spk=M, eng="still", mv="left", sfx="factory yard, a few people catching their breath, birds",
      text="Then they played the men of the factory. And beat them.",
      kf="A cobbled factory yard: four men in work clothes and flat caps sitting exhausted on the ground, red-faced and out of breath, while in the "
         "background a group of women in overalls walk away cheerfully carrying a leather football."),
 dict(id="w09", spk=M, eng="still", mv="in", sfx="quiet office, papers shuffling",
      text="After that, they formed a proper team, managed by an office worker called Alfred Frankland. They were called the Dick, Kerr Ladies.",
      kf="A team photo in flat style: eleven women in identical black-and-white striped jerseys and caps in two rows, a thin man in a suit and "
         "bowler hat standing proudly at the side, a grass field."),
 dict(id="w10", spk=M, eng="ltx",
      text="They played charity matches to raise money for wounded soldiers. And people came to watch. A lot of people.",
      kf="A 1920 football stadium seen from the pitch, wooden stands packed with a huge crowd of tiny simple round-headed spectators in flat caps "
         "and hats, a green pitch in front.",
      mv="The crowd sways and cheers, hats waving in the air, small flags flutter. Static camera."),
 dict(id="w10b", spk=M, eng="still", mv="right", refs=["dkl"], sfx="old stadium crowd cheering",
      text="In 1920 they played a touring team from France, in what's now seen as the first women's international match. They won two nil, in front of twenty-five thousand people.",
      kf="The footballer from the reference shaking hands with a smiling French footballer in a plain blue jersey before a match on a green pitch, "
         "a packed old wooden stand behind them. Exactly two people."),
 dict(id="w11", spk=M, eng="card", card=dict(big="53,000", small="BOXING DAY 1920", bg="#3C5A50", accent="#F2C14E"),
      sfx="huge football crowd roaring in an old stadium",
      text="On Boxing Day 1920, they played at Goodison Park in Liverpool in front of fifty-three thousand people."),
 dict(id="w12", spk=M, eng="still", mv="out", sfx="small football ground, a handful of fans clapping, wind",
      text="That's a crowd most men's clubs would have been delighted with. Plenty of them still would.",
      kf="A tiny modern football ground with one small stand holding only six scattered fans, one of them holding a thermos, a grey drizzly sky."),
 dict(id="w13", spk=M, eng="still", mv="right", refs=["dkl"], sfx="football pitch, ball being kicked, crowd in distance",
      text="They also had stars, like Lily Parr, a tall winger from St Helens with a famously powerful shot.",
      kf="The footballer from the reference, drawn tall, striking a leather ball with a huge powerful kick on a green pitch, motion lines behind "
         "the ball. Exactly one person."),
 dict(id="w14", spk=M, eng="card", card=dict(big="682", small="WINS FROM 755 GAMES", bg="#2E4A62", accent="#F2A65A"),
      sfx="old stadium crowd applause",
      text="Over the years, the team played seven hundred and fifty-five games and won six hundred and eighty-two of them. That sort of record usually gets a manager a statue."),
 # --- the ban
 dict(id="w14b", spk=M, eng="still", env=True, mv="out", sfx="quiet afternoon, wind, distant traffic",
      text="And they kept that up from 1917 all the way to 1965. Which is impressive for any team. It's especially impressive given what happened next.",
      kf="A simple calendar on a wall with its pages blowing away in a long stream through an open window, a leather football on the windowsill. "
         "No people."),
 dict(id="w15", spk=M, eng="still", mv="in", refs=["fa"], sfx="quiet wood-panelled room, clock ticking, a cough",
      text="The Football Association was watching all of this closely. And on the fifth of December 1921, it made a decision.",
      kf="The man from the reference sitting at the head of a long polished table in a dark wood-panelled committee room, fingers steepled, "
         "staring seriously. Exactly one person."),
 dict(id="w16", spk=M, eng="card", card=dict(big="1921", small="\"QUITE UNSUITABLE FOR FEMALES\"", bg="#5A3C3C", accent="#F2C14E"),
      sfx="quiet old room, paper rustling, a pen scratching",
      text="It announced that football was, quote, quite unsuitable for females, and should not be encouraged."),
 dict(id="w17", spk=M, eng="still", mv="left", refs=["fa"], sfx="empty stadium, wind, a gate creaking",
      text="Clubs were told not to let women use their grounds. So women weren't banned from football exactly. Just from everywhere worth playing it.",
      kf="The man from the reference standing in front of the closed iron gates of a big football stadium, swinging a large padlock shut, "
         "looking pleased. Exactly one person."),
 dict(id="w18", spk=M, eng="still", mv="in", refs=["fa"], sfx="quiet office, an adding machine clicking",
      text="The FA also complained that too much of the charity money was going on expenses. A fair question. Although the usual answer to that is an accountant, not a ban.",
      kf="The man from the reference peering through a magnifying glass at a tiny ledger book on a desk, a small pile of coins beside it. "
         "Exactly one person."),
 dict(id="w19", spk=M, eng="still", mv="out", sfx="big stadium crowd, distant cheering",
      text="Many historians think the real problem was simpler. Women's football had become very popular. Possibly more popular than the men in charge were comfortable with.",
      kf="A long queue of simple round-headed fans in 1920s coats and hats stretching around the outside of a football stadium and off into the "
         "distance."),
 dict(id="w20", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So they were banned for selling too many tickets.",
      kf="Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
         "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, arms folded, standing in a simple flat cosy living room "
         "with a teal wall and a plant, looking at camera with a flat, unimpressed expression. Exactly one person.",
      mv="The young man speaks to camera flatly, unimpressed, arms folded, then raises one eyebrow. Static camera, waist-up. Exactly one person; "
         "he keeps the same face, hair and hoodie."),
 dict(id="w21", spk=M, eng="still", mv="right", sfx="open field, cows mooing in the distance, wind", refs=["dkl"],
      text="The Dick, Kerr Ladies kept going anyway, on rugby grounds and open fields, and even toured the United States, playing against men's teams.",
      kf="The footballer from the reference dribbling a ball on a bumpy open field with tall goalposts shaped like a rugby H in the background, "
         "cows watching from behind a fence. Exactly one person.",
      mv_ltx="She dribbles the ball across the bumpy field, the cows turn their heads to follow her. " + P1),
 dict(id="w22", spk=M, eng="still", env=True, mv="out", sfx="wind across an empty field, distant crows",
      text="But without proper grounds, the women's game in England shrank for decades.",
      kf="An empty overgrown grass field at dusk with one small rusty goal frame and a single deflated leather football in the long grass."),
 dict(id="w23", spk=M, eng="card", card=dict(big="1971", small="BAN LIFTED", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet office, a rubber stamp thump",
      text="The FA finally lifted the ban in 1971. By then, a lot of the women it had banned were drawing their pensions."),
 # --- FIFA catches up
 dict(id="w23b", spk=M, eng="still", mv="right", sfx="quiet office, rain on the window",
      text="And England wasn't unusual. West Germany's football association banned the women's game in 1955, and only changed its mind in 1970.",
      kf="A grumpy official in a grey suit firmly closing a big wooden door marked only by a football-shaped brass knocker, while a women's "
         "football bounces sadly off the step. Exactly one person."),
 dict(id="w23c", spk=M, eng="still", mv="in", sfx="tropical city street, distant traffic, birds",
      text="In Brazil, a 1941 law barred women from sports considered incompatible with, quote, the conditions of their nature. Football was on the list until 1979.",
      kf="A sunny Brazilian beach with a football lying alone on the sand next to a stern little no-entry style barrier made of a wooden plank, "
         "palm trees and a blue sea behind. No people."),
 dict(id="w23d", spk=M, eng="still", mv="out", sfx="quiet empty stadium, wind",
      text="So several of today's big football nations spent decades actively stopping women from playing. And then, for a while, wondered why the women's game was behind.",
      kf="A running track race: one young woman athlete in a blue vest sprinting far ahead near the finish line, and at the start line a "
         "second young woman athlete in a red vest standing with her ankles tied together by a thick rope, looking down at the rope, unimpressed. "
         "Exactly two people, both with normal round human heads."),
 dict(id="w24", spk=M, eng="still", env=True, mv="in", sfx="quiet grand office, clock ticking",
      text="Meanwhile FIFA, the body that runs world football, got through most of the twentieth century without a Women's World Cup at all.",
      kf="A grand empty office with a huge desk, a globe, and a calendar on the wall with its pages flying off in a long stream, golden light."),
 dict(id="w25", spk=M, eng="ltx",
      text="The first one finally arrived in 1991, in China, with twelve teams.",
      kf="A big modern stadium at night in southern China seen from the stands, bright floodlights, a packed crowd of simple round-headed "
         "spectators, fireworks bursting in the sky above.",
      mv="Fireworks burst and sparkle in the sky, the crowd waves, the floodlights glow. Static camera."),
 dict(id="w25b", spk=M, eng="still", mv="in", sfx="big stadium crowd cheering, a goal roar",
      text="The very first goal was scored by Ma Li of China, in a four nil win over Norway, and more than half a million people came to watch the tournament.",
      kf="A woman footballer in a plain red kit celebrating a goal with both arms raised, the ball in the back of the net behind her, a big crowd. "
         "Exactly one person."),
 dict(id="w26", spk=M, eng="still", mv="right", sfx="stadium crowd, a referee whistle",
      text="The matches lasted eighty minutes instead of the usual ninety. Just in case ninety turned out to be too much.",
      kf="A referee in black holding up a big round stopwatch, looking at it anxiously on a green pitch. Exactly one person."),
 dict(id="w26b", spk=M, eng="still", mv="in", sfx="changing room, lockers closing",
      text="Some teams also reported struggling to find decent kit in the right size. The first world championship of women's football, played partly in shirts designed for someone else.",
      kf="A woman footballer in a changing room wearing an enormous baggy football shirt that reaches down to her knees, sleeves dangling past "
         "her hands, looking down at it flatly. Exactly one person."),
 dict(id="w27", spk=M, eng="card", card=dict(big="1991", small="\"...FOR THE M&M'S CUP\"", bg="#2E4A62", accent="#F2A65A"),
      sfx="stadium crowd murmuring",
      text="And FIFA still wasn't ready to call it a World Cup. Its official name was the First FIFA World Championship for Women's Football for the M and M's Cup."),
 dict(id="w28", spk=M, eng="still", mv="out", refs=["fa"], sfx="a long scroll unrolling, paper rustling",
      text="Which is a lot of words to avoid saying World Cup.",
      kf="A smartly dressed official holding the top of an absurdly long blank paper scroll that unrolls down a grand staircase and across the "
         "floor. Exactly one person."),
 dict(id="w29", spk=M, eng="still", mv="in", sfx="huge stadium crowd cheering",
      text="The United States won it, beating Norway two one in the final in front of sixty-three thousand people.",
      kf="Women footballers in plain white kits jumping and hugging in celebration on a green pitch under floodlights, confetti, a packed stand."),
 # --- growth
 dict(id="w29b", spk=M, eng="still", mv="right", sfx="stadium crowd, chanting",
      text="The United States went on to host the tournament in 1999 and 2003, and have won it four times. For a while, women's football and the American team were almost the same thing.",
      kf="A trophy cabinet with four shiny golden football trophies in a row on glass shelves, one empty space at the end with a small spotlight. "
         "No people."),
 dict(id="w29c", spk=M, eng="still", mv="out", sfx="quiet office, a fax machine beeping",
      text="Back in England, things moved more slowly. The Women's Super League only started in 2011, and its teams didn't go fully professional until 2018.",
      kf="A snail with a tiny football on its back crawling slowly across a long green football pitch, a stadium in the background. No people."),
 dict(id="w30", spk=M, eng="ltx",
      text="Fast forward to 2023, in Australia and New Zealand. Thirty-two teams, and almost two million people through the gates.",
      kf="A modern stadium by a harbour at sunset with a curved white roof, a packed colourful crowd of simple round-headed fans in the stands.",
      mv="The crowd waves scarves and flags, the sunset sky glows and the sea sparkles. Static camera."),
 dict(id="w30b", spk=M, eng="still", mv="in", sfx="stadium crowd cheering, drums",
      text="The average crowd was nearly thirty-one thousand, and the stadiums were about eighty-seven percent full. That's not a niche sport. That's a sport with a parking problem.",
      kf="A packed stadium car park seen from above, rows and rows of small colourful cars bumper to bumper, a long queue of cars at the exit. "
         "No people."),
 dict(id="w31", spk=M, eng="card", card=dict(big="$110M", small="PRIZE MONEY, 2023", bg="#3C5A50", accent="#F2C14E"),
      sfx="stadium crowd applause",
      text="FIFA paid out a hundred and ten million dollars in prize money, and for the first time, every player was guaranteed a share."),
 dict(id="w31b", spk=M, eng="card", card=dict(big="$499M", small="FIFA SPENT IN 2023", bg="#2E4A62", accent="#F2C14E"),
      sfx="stadium crowd applause",
      text="Overall, FIFA's spending on the 2023 tournament jumped from a hundred and fifty-five million dollars in 2019 to four hundred and ninety-nine million. The money each team got to prepare doubled too."),
 dict(id="w32", spk=M, eng="still", env=True, mv="left", sfx="quiet changing room, a shower dripping",
      text="That mattered, because FIFA's own report put the average professional women's footballer's salary at under seventeen thousand dollars a year.",
      kf="A plain changing room with a wooden bench, a single pair of worn football boots, and a small empty piggy bank on the bench."),
 dict(id="w33", spk=M, eng="still", mv="in", sfx="stadium crowd far away, a phone notification ding",
      text="So for some players, one month at a World Cup paid more than a whole year at their club.",
      kf="A woman footballer in a plain green kit sitting on a bench staring at a phone in her hand with wide surprised eyes. Exactly one person."),
 dict(id="w34", spk=M, eng="still", env=True, mv="right", sfx="quiet room tone, a calculator clicking",
      text="For comparison, the men's World Cup in Qatar the year before paid out four hundred and forty million.",
      kf="A simple old-fashioned balance scale: one small stack of gold coins on one side, and a much taller stack of gold coins on the other side, "
         "the scale tipped heavily, plain cream background."),
 dict(id="w35", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So. A quarter.",
      kf="Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
         "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
         "wall and a plant, holding a small calculator, looking at camera with a flat expression. Exactly one person.",
      mv="The young man looks up from the calculator to camera and speaks flatly, then slowly puts the calculator down. Static camera, waist-up. "
         "Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="w36", spk=M, eng="still", mv="out", sfx="stadium crowd, a single big groan",
      text="Spain won that final, beating England one nil in Sydney.",
      kf="Women footballers in plain red kits celebrating and hugging on a pitch while in the foreground one player in a plain white kit sits on the "
         "grass, head in her hands."),
 dict(id="w37", spk=M, eng="still", mv="in", sfx="enormous stadium crowd singing",
      text="But England were already European champions. They'd won Euro 2022 at Wembley, in front of more than eighty-seven thousand people, the biggest crowd in the history of the Euros, men's or women's.",
      kf="A huge modern stadium with a tall white arch over it, packed with a giant crowd, a team in plain white kits lifting a silver trophy on "
         "the pitch, fireworks."),
 dict(id="w37b", spk=M, eng="still", mv="right", sfx="enormous stadium crowd erupting",
      text="They beat Germany two one after extra time. For an English crowd, there aren't many better ways to win a final.",
      kf="A huge crowd in a stadium leaping out of their seats in celebration, scarves and arms flying, popcorn spilling everywhere."),
 dict(id="w38", spk=M, eng="still", mv="right", sfx="stadium crowd cheering",
      text="Then in 2025, they won the Euros again.",
      kf="A team of women footballers in plain white kits lifting a silver trophy again, looking cheerful but slightly used to it, one player "
         "checking her watch, confetti."),
 dict(id="w38b", spk=M, eng="still", mv="in", sfx="stadium crowd tense silence, then a roar",
      text="That one was against Spain, on penalties. The same Spain that had beaten them in the World Cup final two years earlier.",
      kf="A goalkeeper in a plain green kit diving full stretch to save a penalty, the ball heading for her gloves, a packed stand behind."
         " Exactly one person."),
 dict(id="w38c", spk=M, eng="still", mv="out", sfx="huge stadium crowd singing",
      text="Club football is growing too. In 2022, more than ninety-one thousand people watched Barcelona play Wolfsburg at the Camp Nou, a world record for a women's match.",
      kf="An enormous stadium bowl packed to the very top with a sea of tiny colourful dots of fans, seen from high above at dusk, floodlights on, a small green pitch far below."),
 dict(id="w39", spk=M, eng="still", env=True, mv="in", sfx="quiet office, papers being stamped",
      text="So the UK's bid for 2035 wasn't exactly a leap of faith.",
      kf="A thick bid document folder with a shiny gold football on its cover lying on a desk next to two silver trophies, warm desk lamp light. "
         "No people."),
 # --- 2035
 dict(id="w40", spk=M, eng="card", card=dict(big="48", small="TEAMS IN 2035", bg="#2E4A62", accent="#F2C14E"),
      sfx="stadium crowd rumble",
      text="So what will 2035 actually look like? It's big. Forty-eight teams, a hundred and four matches, over thirty-nine days."),
 dict(id="w41", spk=M, eng="still", mv="out", sfx="football crowd in distance, wind",
      text="That's sixteen more teams than in 2023, so a lot more countries get a real shot at qualifying.",
      kf="A big simple flat world map in soft colours with lots of small football icons popping up across every continent. No people."),
 dict(id="w42", spk=M, eng="still", mv="in", sfx="gentle wind, seagulls",
      text="The bid proposes twenty-two stadiums in sixteen cities. Sixteen in England, three in Wales, two in Scotland and one in Northern Ireland.",
      kf="A simple flat map of Great Britain and Northern Ireland in green on a soft blue sea, dotted with small round stadium icons spread across "
         "the land. No people."),
 dict(id="w42b", spk=M, eng="still", mv="right", sfx="football crowd singing far away",
      text="The bid is called All Together, and that's the idea. One tournament across four nations, which between them have a long history of not agreeing about football.",
      kf="Four simple round-headed football fans in red, white, blue and green scarves standing in a row on a terrace, arms around each other's "
         "shoulders, each one looking slightly uncomfortable about it."),
 dict(id="w43", spk=M, eng="still", env=True, mv="right", sfx="building site, distant machinery, birds",
      text="Where the final goes hasn't been decided. Wembley is the obvious choice. Manchester United would like to host it in a hundred-thousand-seat stadium they haven't built yet.",
      kf="An empty muddy building site with a single small sign post, a lonely yellow digger and one traffic cone, under a grey sky. No people."),
 dict(id="w44", spk=M, eng="card", card=dict(big="4.5M", small="TICKETS EXPECTED", bg="#3C5A50", accent="#F2A65A"),
      sfx="huge stadium crowd cheering",
      text="The organisers expect around four and a half million tickets to be sold, and a global TV audience of three and a half billion."),
 dict(id="w45", spk=M, eng="still", mv="out", sfx="busy train station, announcements muffled, footsteps",
      text="They also point out that sixty-three million people live within two hours of a proposed venue. Which, in Britain, depends heavily on the trains.",
      kf="A crowded train station platform full of football fans in colourful scarves, all staring up at a departures board showing only "
         "blank red panels, a train nowhere in sight."),
 dict(id="w46", spk=M, eng="still", mv="left", sfx="tropical city ambience, distant samba drums",
      text="Before that, there are two more World Cups. Brazil hosts in 2027, the first in South America. Then 2031 goes to the United States, together with Mexico, Costa Rica and Jamaica.",
      kf="A simple flat map of the Americas with a glowing golden trophy icon over Brazil and another over North America, soft blue ocean. "
         "No people."),
 # --- the future
 dict(id="w47", spk=M, eng="still", mv="in", sfx="empty stadium after a match, wind, a sweeping broom",
      text="But a tournament only lasts a few weeks. The real question is what happens to the game in the years around it.",
      kf="An empty stadium after a match at night, one cleaner sweeping confetti off the pitch under a single floodlight. Exactly one person."),
 dict(id="w48", spk=M, eng="still", mv="right", sfx="local football pitch, kids playing, whistle",
      text="The four football associations have promised three things. More girls playing. More coaches, referees and leaders. And more investment, from grassroots all the way to the top.",
      kf="A sunny local pitch: a young woman coach with a whistle and clipboard, a referee in black, and a group of girls in bright bibs "
         "doing a passing drill between cones."),
 dict(id="w49", spk=M, eng="still", env=True, mv="out", sfx="empty stadium, wind, a lone bird",
      text="Every host promises a legacy. The test is whether any of it is still there after the stadiums are swept up.",
      kf="A tidy empty stadium in daylight with a perfect green pitch and rows of empty seats, a single forgotten scarf on one seat. No people."),
 dict(id="w49b", spk=M, eng="still", mv="in", sfx="quiet office, rain on the window",
      text="The associations say they now have eight and a half years to make it happen, on facilities, coaching, refereeing, and the pathway that takes a girl from her first game to a professional contract.",
      kf="A long winding path across green hills from a tiny local pitch with a single goal in the foreground to a huge bright stadium far away "
         "on the horizon. No people."),
 dict(id="w49c", spk=M, eng="still", mv="right", sfx="city park, kids playing, birds",
      text="There is some evidence it works. After the 2023 tournament, more New Zealanders said women's sport was exciting, and viewing of women's sport there rose by twenty-nine percent in a year.",
      kf="A family on a sofa in a cosy living room watching a women's football match on a television, the father leaning forward excitedly, "
         "a dog watching too."),
 dict(id="w50", spk=M, eng="still", mv="in", sfx="quiet room tone, a clock ticking",
      text="Because the gaps are still real. Prize money is still a fraction of the men's. And many players outside the top leagues still have second jobs.",
      kf="A woman in a plain football kit with a supermarket apron over it, stacking tins on a shop shelf, a football under her arm. "
         "Exactly one person."),
 dict(id="w51", spk=M, eng="still", mv="in", sfx="sunny park, kids playing in the distance, birds", refs=["girl"],
      text="And here's the nice part. Most of the players who'll star in 2035 aren't professionals yet. They're kids, in a park somewhere.",
      kf="The girl from the reference in a sunny park, about to kick a football towards a goal made of two piled-up jumpers on the grass, "
         "trees behind. Exactly one person.",
      mv_ltx="The girl runs up and kicks the ball between the two jumpers, then throws her arms up in celebration. " + P1),
 dict(id="w52", spk=M, eng="still", mv="right", refs=["girl"], sfx="park, kids shouting, birds",
      text="Probably arguing about whether that one went in.",
      kf="The girl from the reference standing next to a goal made of two piled-up jumpers on park grass, pointing firmly at the gap between them "
         "with a determined face, the ball just past one jumper. Exactly one person."),
 dict(id="w53", spk=M, eng="still", mv="in", refs=["girl"], sfx="park, distant kids playing, birds",
      text="A ten-year-old girl today will be nineteen in 2035. Right about the age to make a World Cup squad.",
      kf="The girl from the reference sitting on park grass with her football, looking up dreamily at a big glowing stadium silhouette on the "
         "horizon. Exactly one person."),
 # --- bookend
 dict(id="w54", spk=M, eng="still", mv="out", refs=["fa"], sfx="quiet wood-panelled room, clock ticking",
      text="So in 1921, the people in charge of English football said women's football should not be encouraged.",
      kf="The man from the reference sitting alone at the head of a long polished table in a dark wood-panelled committee room, looking stern. "
         "Exactly one person."),
 dict(id="w55", spk=M, eng="ltx",
      text="In 2035, they'll be hosting the whole world for it.",
      kf="A huge modern stadium at night with a tall white arch over it, packed with a giant crowd waving flags of many colours, bright floodlights, "
         "fireworks above.",
      mv="Fireworks burst over the stadium, the crowd waves flags, the floodlights sparkle. Static camera."),
 dict(id="w56", spk=M, eng="still", mv="out", sfx="huge stadium crowd cheering, fading",
      text="It took a hundred and fourteen years. But as changes of heart go, it's a fairly thorough one. Subscribe for more.",
      kf="A golden football trophy cup on a green pitch in the evening sun, with the long shadow of a 1920s footballer in a striped cap stretching "
         "across the grass beside it. No people visible."),
]
TAIL = 2.4
