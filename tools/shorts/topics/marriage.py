"""Is marriage becoming obsolete? 10-minute LANDSCAPE explainer (fast flat pipeline).
Comedic personality: a warm, slightly cynical wedding guest who has seen it all. Dry about weddings, money and history's very
unromantic idea of marriage; never mocks single people, married people or anyone's choices. Balanced: both cases, honest verdict.
Sources: Pew/TIME 2010 'The Decline of Marriage and Rise of New Families' (39% say marriage is becoming obsolete; 28% in TIME's 1978 poll;
51% of adults married in 2010 vs 72% in 1960); Pew 2023 (25% of 40-year-olds never married in 2021, record; 16% in 1910; 6% in 1980);
US Census MS-2 (median age at first marriage ~30 men / ~28 women now vs ~23 / ~20 in 1960); OECD Family Database SF3.1 (crude marriage rates
7-10 per 1,000 in 1970, about 5-7 by 1995, lower since); Pew 2019 (59% of 18-44s have cohabited vs 50% ever married; married adults more
satisfied and trusting); CDC NCHS (about 4 in 10 US births outside marriage); The Knot 2026 Real Weddings Study (average 2025 wedding $34,200,
median $24,000); NCFMR/BGSU (refined divorce rate 14.2 per 1,000 married women in 2024, peak ~22.6 in 1980); Pew Feb 2024 (69% of
never-married 18-34s want to marry someday); Statistics Korea via Bloomberg/UPI (191,690 marriages in 2022, 222,412 in 2024 (+14.8%), rose
again in 2025); S. Coontz, 'Marriage, a History' (2005: love-based marriage is historically recent); A. Cherlin ('capstone' marriage);
Married Women's Property Acts 1870 and 1882 (UK); US Equal Credit Opportunity Act 1974; same-sex marriage: Netherlands 2001, US 2015."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Is Marriage Becoming Obsolete"
ERA = "modern"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Warm romantic palette of blush pink, cream, sage green, navy and gold. "
         "Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. Clean simple "
         "background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Warm romantic palette of blush pink, cream, sage green, navy and gold. "
             "Show only what the description names. There are NO characters of any kind: no people, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "her": "a modern woman in her late twenties as a simple flat vector character: long dark wavy hair, sage-green jumper, light blue jeans, "
        "white trainers, small round head, dot eyes, warm smile.",
 "him": "a modern man in his early thirties as a simple flat vector character: short ginger hair, neat short beard, navy shirt with rolled "
        "sleeves, beige chinos, brown shoes, small round head, dot eyes.",
 "lady": "an 1840s English wife as a simple flat vector character: young woman with her hair in a neat bun, long dusty-pink Victorian dress "
         "with a high collar, small round head, dot eyes, polite resigned expression.",
}
P1 = "Static camera. Characters keep the same faces and clothes."
RY = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
      "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
      "wall and a plant, ")
RYM = "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."
def ryan(id_, text, pose, mv): return dict(id=id_, spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"], text=text, kf=RY + pose, mv=mv + " " + RYM)
SHOTS = [
 # --- hook
 dict(id="m00", spk=M, eng="still", mv="in", refs=["her", "him"], sfx="small wedding chapel, organ fading, a camera shutter",
      text="Four in ten Americans say marriage is becoming obsolete. And yet, every weekend, people still spend the price of a car on a single afternoon to do it. So which is it?",
      kf="The woman from the first reference in a white wedding dress and the man from the second reference in a navy suit standing at a "
         "flower-covered wedding arch, smiling, while behind them a shiny red family car sits on the altar with a giant gold price tag "
         "dangling from it. Exactly two people."),
 dict(id="m01", spk=M, eng="card", card=dict(big="28% → 39%", small="SAY MARRIAGE IS OBSOLETE", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet room, a page turning",
      text="When TIME magazine first asked Americans in 1978, twenty-eight percent said marriage was becoming obsolete. By 2010, Pew found it was thirty-nine."),
 dict(id="m02", spk=M, eng="still", mv="right", sfx="busy cafe, chatter, cups clinking",
      text="That's a lot of people calling something obsolete while still attending its parties.",
      kf="A big wedding reception in a garden: lots of simple round-headed guests dancing, eating cake and raising glasses under fairy lights."),
 dict(id="m02b", spk=M, eng="still", env=True, mv="out", sfx="old office, a fax machine screeching",
      text="Obsolete is also a strong word. Fax machines are obsolete. Floppy disks are obsolete. Nobody is spending thirty thousand dollars to celebrate their floppy disk.",
      kf="A dusty museum display case containing a fax machine, a floppy disk and a rotary telephone under little spotlights, and next to it an "
         "empty case with a small velvet stand where a wedding ring might go. No people."),
 ryan("m03", "To be fair, the cake is excellent.", "holding a small plate with a slice of wedding cake, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then takes a bite of the cake."),
 # --- the numbers
 dict(id="m03b", spk=M, eng="still", env=True, mv="in", sfx="quiet room, a page turning",
      text="So let's look at what's actually happening to marriage, what it used to be for, the case that it's dying, the case that it isn't, and what it might turn into.",
      kf="A simple flat illustration of a winding road with four signposts shaped like hearts, rings, a broken heart and a question mark, "
         "leading towards a distant chapel on a hill. No people."),
 dict(id="m04", spk=M, eng="card", card=dict(big="72% → 51%", small="US ADULTS WHO ARE MARRIED", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet office, a calculator clicking",
      text="Let's start with the numbers. In 1960, seventy-two percent of American adults were married. By 2010, it was barely half."),
 dict(id="m05", spk=M, eng="still", env=True, mv="out", sfx="quiet suburban street, birds",
      text="And it isn't only America. Across rich countries, marriage rates have been falling for decades. In 1970, most had seven to ten weddings a year for every thousand people. By the mid-nineties, it was five to seven, and it's dropped further since.",
      kf="A simple flat illustration of a row of wedding chapels along a street, the first ones busy and decorated with flowers, getting "
         "emptier and plainer further along the row. No people."),
 dict(id="m06", spk=M, eng="card", card=dict(big="25%", small="OF 40-YEAR-OLDS NEVER MARRIED", bg="#2E4A62", accent="#F2A65A"),
      sfx="quiet room tone, a clock ticking",
      text="By 2021, a record twenty-five percent of American forty-year-olds had never been married. In 1980 it was six percent."),
 dict(id="m07", spk=M, eng="still", mv="in", refs=["her"], sfx="quiet flat, a kettle boiling, rain on the window",
      text="The previous record was in 1910, at sixteen percent. So today's forty-year-olds have beaten a record set by people who had to get around on horses.",
      kf="The woman from the reference relaxing on a sofa with a book and a cup of tea, while outside the window a man in a 1910 suit rides "
         "past on a horse, tipping his hat. Exactly two people."),
 dict(id="m08", spk=M, eng="still", mv="right", refs=["her", "him"], sfx="quiet street, distant traffic",
      text="People are also marrying later. In 1960, the typical American got married at about twenty-three if you were a man, and twenty if you were a woman. Today it's around thirty and twenty-eight.",
      kf="The woman from the first reference and the man from the second reference sitting on a park bench holding hands, with a small "
         "wedding ring box on the bench between them, a big old clock tower behind them. Exactly two people."),
 dict(id="m09", spk=M, eng="still", mv="in", refs=["her", "him"], sfx="small flat, pans sizzling, soft music from next door",
      text="And a lot of couples simply live together instead. Among Americans aged eighteen to forty-four, more have lived with an unmarried partner than have ever been married. Fifty-nine percent, against fifty.",
      kf="The woman from the first reference and the man from the second reference in a small cosy kitchen cooking dinner together, laughing, "
         "two mugs and a plant on the counter. Exactly two people."),
 dict(id="m09b", spk=M, eng="still", mv="right", sfx="quiet Swedish street, a bicycle bell",
      text="In Sweden, living together unmarried is so normal that there's a law covering it, and an everyday word for your partner: sambo. In France, a civil partnership called the PACS, created in 1999, has become almost as popular as marriage.",
      kf="A cosy Scandinavian flat with a couple's two pairs of boots by the door, two bicycles, and a simple wooden table set for two, snow "
         "outside the window. No people."),
 dict(id="m09c", spk=M, eng="still", mv="in", sfx="quiet flat, a single cup set down",
      text="More people are also living completely alone. About twenty-nine percent of American households are now just one person, a record.",
      kf="A tall apartment building at night with many windows lit, and in each lit window a single person doing their own thing: reading, "
         "cooking, playing guitar, watching television."),
 dict(id="m10", spk=M, eng="still", mv="out", sfx="quiet nursery, a baby's mobile chiming",
      text="About four in ten American babies are now born to parents who aren't married. Fifty years ago, that would have caused a scandal. Today it barely causes a raised eyebrow, except possibly from grandma.",
      kf="A cosy nursery with a crib and a mobile of little stars, a framed family photo of two smiling parents and a baby on the wall, and an "
         "old grandmother in the doorway raising one eyebrow. Exactly one person visible in the room."),
 # --- history
 dict(id="m10b", spk=M, eng="still", env=True, mv="right", sfx="quiet countryside, a church bell",
      text="But before we decide marriage is dying, we should ask what it was supposed to be in the first place. Because it has changed shape many times before.",
      kf="A simple flat illustration of a single wedding ring sitting on a shelf next to an hourglass and a very old dusty book. No people."),
 dict(id="m11", spk=M, eng="still", env=True, mv="in", sfx="medieval hall, a fire crackling, a lute far away",
      text="To understand why this is happening, it helps to know what marriage used to be for. And for most of history, the answer was not love.",
      kf="A medieval stone hall with a long wooden table and a heart-shaped wax seal on a rolled parchment contract, candles burning. No people."),
 dict(id="m12", spk=M, eng="ltx",
      text="Marriage was about property, alliances and labour. Families married their children to join farms, merge fortunes or make peace.",
      kf="A medieval castle courtyard where two noble families in rich robes face each other, the two fathers shaking hands over a table "
         "piled with coins and land deeds, while a young bride and groom stand behind them looking at each other awkwardly.",
      mv="The two fathers shake hands firmly and nod, the bride and groom glance at each other and then away. Static camera."),
 dict(id="m12b", spk=M, eng="still", mv="right", sfx="busy Indian family home, chatter, a pressure cooker whistle",
      text="And that's still true for a lot of the world. In India, for example, most marriages are still arranged by families, and many couples say they're perfectly happy with that.",
      kf="A lively Indian living room where two families sit on sofas facing each other drinking tea and chatting, a young man and young woman "
         "in the middle glancing shyly at each other."),
 dict(id="m13", spk=M, eng="still", mv="right", sfx="medieval hall, quiet murmuring",
      text="Love was nice if it happened, but it wasn't the point. In many places, marrying purely for love was seen as reckless. A bit like quitting your job to become a poet.",
      kf="A young medieval man in a tunic dramatically reading a poem from a scroll to a balcony, while two worried parents watch from a "
         "doorway shaking their heads. Exactly three people."),
 dict(id="m14", spk=M, eng="still", mv="in", sfx="quiet study, a fire crackling",
      text="The historian Stephanie Coontz argues that the idea of marrying mainly for love only really took hold in the last couple of centuries. Which, in the history of marriage, is basically last week.",
      kf="A simple long timeline painted along a wall, mostly grey stone and grey figures, with only the very last tiny section at the end "
         "glowing pink with little hearts. No people."),
 dict(id="m14b", spk=M, eng="still", mv="out", sfx="village green, birds, distant church bell",
      text="For centuries in Europe, a couple could marry just by exchanging promises, without a priest or any witnesses. Which caused exactly the arguments you'd imagine, usually involving one person insisting it had happened and the other insisting it hadn't.",
      kf="A medieval village green: a young woman pointing firmly at a young man who is shrugging innocently, while a crowd of villagers "
         "watches the argument with great interest."),
 dict(id="m14c", spk=M, eng="still", mv="in", sfx="old church, an organ note, murmuring",
      text="In 1563, the Catholic Church's Council of Trent decided that was enough, and required a priest and witnesses for a valid marriage.",
      kf="A grand old church interior with rows of serious bishops in tall hats seated at long tables, one standing up and raising a finger "
         "firmly."),
 dict(id="m14d", spk=M, eng="card", card=dict(big="1857", small="BEFORE THIS: DIVORCE BY ACT OF PARLIAMENT", bg="#2E4A62", accent="#F2A65A"),
      sfx="old parliament chamber, murmuring, a gavel",
      text="Getting out was even harder. In England, before 1857, a divorce usually needed its own Act of Parliament. Only a few hundred were ever granted, almost all to wealthy men."),
 dict(id="m14e", spk=M, eng="still", mv="in", sfx="1960s office, a typewriter",
      text="In 1969, California became the first American state to allow no-fault divorce, where nobody has to prove the other person did something wrong.",
      kf="A 1960s government office with a smiling official stamping a document, while a relieved couple in 1960s clothes shake hands politely "
         "across the desk. Exactly three people."),
 dict(id="m14f", spk=M, eng="still", mv="out", sfx="quiet English office, rain outside, a pen scratching",
      text="England only got there in 2022. Before that, couples who wanted a quick divorce usually had to blame each other in writing. Which is a very British way to end a relationship: politely, on paperwork.",
      kf="A rainy English office where a man and a woman sit at separate desks, each writing a very long list on paper with great "
         "concentration, a teapot between them. Exactly two people."),
 dict(id="m15", spk=M, eng="still", mv="out", refs=["lady"], sfx="Victorian parlour, a clock ticking",
      text="And for women, marriage could mean disappearing legally. Under English common law, a wife's legal identity was folded into her husband's. Her property and her earnings became his.",
      kf="The woman from the reference sitting very straight in a Victorian parlour chair, slowly fading and becoming transparent, while a "
         "large framed portrait of a stern moustached husband looms on the wall behind her. Exactly one person."),
 dict(id="m16", spk=M, eng="card", card=dict(big="1870 & 1882", small="MARRIED WOMEN'S PROPERTY ACTS", bg="#5A3C3C", accent="#F2C14E"),
      sfx="old courtroom, a gavel knock",
      text="In Britain, it took the Married Women's Property Acts of 1870 and 1882 to start letting wives keep their own money and property."),
 dict(id="m17", spk=M, eng="still", mv="right", refs=["her"], sfx="bank lobby, quiet chatter",
      text="And in the United States, it wasn't until 1974 that a law stopped lenders discriminating against women on the basis of sex or marital status, which had made it hard for many women to get credit without a husband.",
      kf="The woman from the reference standing confidently at a bank counter, holding up a shiny new bank card, while a 1970s bank clerk with "
         "big glasses looks at it in surprise. Exactly two people."),
 ryan("m18", "1974. That's practically yesterday.", "with arms folded, looking at camera with raised eyebrows. Exactly one person.",
      "The young man speaks flatly to camera, eyebrows raised, then slowly shakes his head."),
 dict(id="m19", spk=M, eng="still", mv="in", sfx="quiet room tone",
      text="So for a long time, marriage wasn't really optional. It was how you got money, status, legal protection, and a respectable place in society. For a lot of women, it was the only option on the menu.",
      kf="A restaurant menu card on a table showing only one single dish, a wedding cake, with a lonely fork beside it. No people."),
 # --- the case: becoming obsolete
 dict(id="m20", spk=M, eng="still", mv="right", refs=["her"], sfx="busy modern office, keyboards",
      text="Now take those reasons away one by one. Women can work, own property, borrow money and live alone. Living together without a ring is normal. Having children outside marriage is normal.",
      kf="The woman from the reference striding confidently out of a modern office building with a laptop bag and house keys in her hand, "
         "city behind her. Exactly one person."),
 dict(id="m21", spk=M, eng="ltx", env=True,
      text="That's the heart of the obsolete argument. Marriage used to be a necessity. Most of the things that made it necessary have gone.",
      kf="A large heart-shaped pink balloon floating on a cream background, slightly saggy. No people.",
      mv="The heart-shaped balloon slowly deflates, wrinkles and sags down towards the floor. Static camera."),
 dict(id="m22", spk=M, eng="card", card=dict(big="$34,200", small="AVERAGE US WEDDING (2025)", bg="#3C5A50", accent="#F2A65A"),
      sfx="busy wedding venue, champagne pop, chatter",
      text="Then there's the cost. The average American wedding in 2025 cost thirty-four thousand two hundred dollars, according to The Knot. Even the median was twenty-four thousand."),
 dict(id="m22b", spk=M, eng="still", mv="right", sfx="Victorian church, bells, crowd cheering",
      text="And some of the most traditional parts of a wedding are newer than you'd think. White wedding dresses became fashionable after Queen Victoria wore one in 1840. Before that, brides usually just wore their best dress, whatever colour it was.",
      kf="A young Queen Victoria in a white lace wedding gown and veil walking down an aisle, while a crowd of Victorian ladies in colourful "
         "dresses stare at her and take notes."),
 dict(id="m22c", spk=M, eng="still", mv="in", sfx="jewellery shop, a little bell, soft music",
      text="And the idea that an engagement ring has to be a diamond owes a lot to a 1947 advertising slogan for the diamond company De Beers. A Diamond Is Forever. It worked so well that people now think it's a tradition.",
      kf="A sparkling diamond ring on a velvet cushion in a jewellery shop window, with a 1940s advertising executive in a suit standing "
         "proudly next to it, arms folded. Exactly one person."),
 dict(id="m23", spk=M, eng="still", mv="out", refs=["her", "him"], sfx="quiet flat, a calculator beeping",
      text="So a lot of couples wait. Not because they don't want to marry, but because they want to do it properly, with a house, stable jobs, and enough savings that the reception doesn't come with a payment plan.",
      kf="The woman from the first reference and the man from the second reference sitting at a kitchen table covered in bills and a laptop, "
         "looking at a tiny piggy bank with a wedding ring on top of it. Exactly two people."),
 dict(id="m24", spk=M, eng="still", env=True, mv="right", sfx="soft wind, distant church bells",
      text="The sociologist Andrew Cherlin calls this capstone marriage. It used to be the foundation you built a life on. Now, for many people, it's the last brick you put on top once everything else is finished.",
      kf="A small house being built from big blocks, completely finished, with a single shiny heart-shaped brick being lowered onto the very "
         "top of the roof by a little crane. No people."),
 dict(id="m25", spk=M, eng="still", mv="in", sfx="busy city, distant traffic",
      text="And researchers have noticed a divide. In America, marriage has become more common among people with more education and money, and less common among those with less. Some worry it's turning into a luxury good.",
      kf="A shiny wedding chapel on a hill behind a velvet rope with a bouncer, and a long line of ordinary people below looking up at it. "
         "Simple flat style."),
 # --- the case: not obsolete
 dict(id="m26", spk=M, eng="still", mv="out", sfx="quiet room, a pen clicking",
      text="So is marriage on its way out? Well, here's the other side. And it has some surprisingly good numbers.",
      kf="A simple old balance scale on a cream background, one side holding a pair of gold wedding rings and the other side holding a house "
         "key, the scale perfectly level. No people."),
 dict(id="m27", spk=M, eng="card", card=dict(big="69%", small="OF NEVER-MARRIED 18-34s WANT TO MARRY", bg="#2E4A62", accent="#F2C14E"),
      sfx="busy cafe, chatter",
      text="Pew found that sixty-nine percent of never-married Americans aged eighteen to thirty-four say they want to get married someday."),
 dict(id="m28", spk=M, eng="still", mv="right", refs=["him"], sfx="park, birds, distant children",
      text="So most young people aren't rejecting marriage. They're postponing it. Which is a very different thing, even if your mum can't tell the difference.",
      kf="The man from the reference on a video call on his phone in a park, smiling politely, while on the phone screen an older woman is "
         "holding up a bridal magazine hopefully. Exactly one person in the park."),
 dict(id="m29", spk=M, eng="card", card=dict(big="22.6 → 14.2", small="DIVORCES PER 1,000 MARRIED WOMEN", bg="#3C5A50", accent="#F2A65A"),
      sfx="quiet office, a clock ticking",
      text="Divorce is falling too. In 1980, about twenty-three in every thousand married American women divorced each year. By 2024, it was about fourteen."),
 dict(id="m30", spk=M, eng="still", mv="in", refs=["her", "him"], sfx="quiet home, a fire crackling",
      text="The famous idea that half of all marriages end in divorce is out of date. People who marry later, and more carefully, tend to stay married.",
      kf="An older version of the couple from the references, both with grey hair, sitting close together on a sofa doing a crossword, "
         "sharing a blanket. Exactly two people."),
 dict(id="m31", spk=M, eng="still", mv="out", refs=["her", "him"], sfx="quiet flat, soft evening ambience",
      text="Pew also found that married adults are, on average, more satisfied with their relationships and more trusting of their partners than people who live together without marrying. Though that may partly be because the happiest couples are the ones who marry.",
      kf="The woman from the first reference and the man from the second reference sitting on their sofa, with a little pink heart floating "
         "above them, sharing a bowl of popcorn. Exactly two people."),
 dict(id="m31b", spk=M, eng="still", mv="in", sfx="solicitor's office, a clock ticking",
      text="Marriage also still matters legally. In England, lots of people believe in something called common-law marriage, the idea that living together long enough gives you the same rights as a married couple.",
      kf="A couple sitting confidently in a solicitor's office, while the solicitor behind the desk winces and slowly slides a thick legal book "
         "towards them. Exactly three people."),
 dict(id="m31c", spk=M, eng="still", mv="right", sfx="quiet office, a book closing",
      text="It doesn't exist. Couples who split up or lose a partner after decades together can find they have far fewer rights than they assumed. Which is a terrible time to find out.",
      kf="A sad empty sofa in a living room with only half of the furniture left, packing boxes by the door, a single potted plant. No people."),
 dict(id="m32", spk=M, eng="still", mv="right", sfx="crowd cheering, confetti cannons",
      text="And if marriage were truly obsolete, it would be strange for so many people to have fought for the right to do it. The Netherlands legalised same-sex marriage in 2001. The United States did it nationwide in 2015.",
      kf="Two grooms in suits kissing under a shower of confetti on town hall steps, with a cheering crowd of friends around them."),
 dict(id="m33", spk=M, eng="still", mv="in", sfx="Seoul street, traffic, a wedding hall bell",
      text="Even in South Korea, where marriage had been falling for years, it bounced back. Marriages rose almost fifteen percent in 2024, the biggest jump on record, and rose again in 2025.",
      kf="A modern Korean wedding hall at sunset decorated with flowers, with a long queue of happy couples in wedding clothes waiting outside "
         "the door."),
 ryan("m34", "Turns out, love is not dead. Just running late.", "with his hands in his hoodie pockets, looking at camera with a small flat smile. Exactly one person.",
      "The young man speaks flatly to camera, then gives a tiny shrug."),
 # --- verdict
 dict(id="m35", spk=M, eng="still", mv="out", sfx="quiet chapel, birds outside",
      text="So, is marriage becoming obsolete?",
      kf="An empty, peaceful wedding chapel with sunlight streaming through the windows onto rows of wooden pews and a flower arch. No people."),
 dict(id="m36", spk=M, eng="still", env=True, mv="in", sfx="quiet room tone",
      text="Not exactly. What's becoming obsolete is marriage as a requirement. The idea that you have to marry to be an adult, to be respectable, to have money, or to raise a family.",
      kf="A rusty old iron chain and padlock lying broken open on the floor next to a pair of shiny gold wedding rings. No people."),
 dict(id="m36b", spk=M, eng="still", mv="right", sfx="courtroom steps, cameras clicking, cheering",
      text="It's also becoming more flexible. In 2019, Britain opened civil partnerships to opposite-sex couples, after one couple who wanted the legal protection without the traditional baggage took their case all the way to the Supreme Court.",
      kf="A smiling couple in smart clothes holding hands on the steps of a grand court building, waving to a small crowd of photographers. "
         "Exactly two people in front."),
 dict(id="m36c", spk=M, eng="still", mv="in", sfx="quiet cafe, cups clinking",
      text="So the future may look less like one fixed template, and more like a menu. Marriage, partnership, living together, living apart. With the same question underneath all of them: who do you actually want to build a life with?",
      kf="A friendly cafe menu board illustrated with simple pictures: two rings, a key, a little house and two separate houses side by side, "
         "with a small heart drawn at the top. No people, no writing."),
 dict(id="m37", spk=M, eng="still", mv="right", refs=["her", "him"], sfx="park, birds, soft wind",
      text="What's left is marriage as a choice. Fewer people make it, and they make it later. But the ones who do seem to mean it more.",
      kf="The woman from the first reference and the man from the second reference walking hand in hand along a path in a sunny park, "
         "talking and smiling. Exactly two people."),
 ryan("m37b", "So, not dead. Just pickier.", "holding a mug, looking at camera with a small knowing smile. Exactly one person.",
      "The young man speaks flatly to camera, then takes a small sip from the mug."),
 dict(id="m38", spk=M, eng="still", mv="in", sfx="quiet room, a page turning",
      text="In a way, it's gone back to what the old romantics wanted all along. Marrying for love, instead of for land, money or a functioning bank account.",
      kf="A medieval poet with a lute and the modern couple from the references sitting together on a bench, the poet looking very pleased "
         "with himself. Exactly three people."),
 dict(id="m39", spk=M, eng="ltx", refs=["her", "him"],
      text="Tell us in the comments: is marriage still worth it? And subscribe. It's a lot cheaper than a wedding.",
      kf="The woman from the first reference and the man from the second reference sitting side by side on a sofa, both turning to look at "
         "camera, the man holding a tiny ring box. Exactly two people.",
      mv="Both turn to look at camera; the woman raises one eyebrow and the man slowly hides the ring box behind his back. " + P1),
]
THUMB = dict(text="IS MARRIAGE|DYING?", refs=["her", "him"],
             kf="The woman from the first reference in a white wedding dress and the man from the second reference in a navy suit both "
                "staring in shock at a giant wedding cake that is leaning and cracking, a huge gold price tag hanging from the cake. Soft pink "
                "background. Exactly two people.")
TAIL = 2.4
