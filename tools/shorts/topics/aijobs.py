"""Should AI replace human workers if it is cheaper? Efficiency vs employment. 10-minute LANDSCAPE debate explainer (fast flat pipeline).
Comedic personality: a calm, fair referee. It takes both sides seriously and finds the comedy in corporate euphemism, in confident
predictions, and in the gap between 'exposed' and 'replaced'. It never mocks workers who lose jobs.
Sources: IMF blog, Georgieva 14 Jan 2024 (~40% of global employment exposed, ~60% in advanced economies, about half may benefit);
Goldman Sachs Mar 2023 (equivalent of 300 m full-time jobs exposed); WEF Future of Jobs 2025 (170 m created, 92 m displaced, net 78 m by 2030);
Bessen, IMF F&D Mar 2015 (power looms automated 98% of weaving labour yet weaving jobs grew and wages rose; ATMs: tellers per urban branch
20 -> 13 1988-2004, branches +43%, teller jobs did not decrease); Brynjolfsson, Li, Raymond, NBER w31161 / QJE 2025 (+14% issues resolved/hour,
+34% novices, minimal for experienced); Svanberg, Thompson et al., MIT 2024 (only 23% of wages paid for vision tasks attractive to automate at
today's costs); Klarna (Customer Experience Dive 2025; Fast Company Jan 2026: hiring paused, 5,500 -> 3,400 staff, chatbot 'work of 700 agents',
later returned to humans for customer service); Luddites 1811-16 and the Frame Breaking Act 1812 (capital offence); Bill Gates robot-tax idea
(Quartz, Feb 2017); Finland basic income experiment 2017-18 (2,000 unemployed people, EUR 560/month; better wellbeing, small employment effect)."""
from topics.wwc2035 import VOICE_REF, H3_REF_KF
FOLDER = "Should AI Replace Workers"            # VIDEOS/<FOLDER>/...
ERA = "modern"
M, R = "maya", "benny"
LANDSCAPE = True
GAP, TEMPO = 0.2, 1.10
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
         "subtle gradients, no outlines, no texture, no clutter. Friendly palette of teal, warm cream, coral, navy and mustard yellow. "
         "Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, consistent proportions. Clean simple "
         "background with only a few large shapes. Absolutely no text, letters, numbers, logos or badges anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with very "
             "subtle gradients, no outlines, no texture, no clutter. Friendly palette of teal, warm cream, coral, navy and mustard yellow. "
             "Show only what the description names. There are NO characters of any kind: no people, no robots, no faces, no figures. "
             "Absolutely no text, letters, numbers, logos or badges anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
CHARS = {
 "worker": "a modern office worker as a simple flat vector character: young woman, short wavy brown hair, round glasses, mustard-yellow "
           "cardigan over a white shirt, navy trousers, a small black headset, small round head, dot eyes.",
 "robot": "a friendly office robot as a simple flat vector character: boxy white body, rounded square head with a dark teal screen face showing "
          "two simple glowing dot eyes, thin grey arms, a small navy tie, short legs.",
 "boss": "a company manager as a simple flat vector character: middle-aged man, neat grey hair, navy suit, coral tie, holding a coffee mug, "
         "small round head, dot eyes, confident smile.",
 "weaver": "an 1811 English cloth worker as a simple flat vector character: man with messy dark hair and sideburns, brown waistcoat, rolled "
           "white sleeves, grey trousers, leather apron, small round head, dot eyes.",
}
P1 = "Static camera. Characters keep the same faces and clothes."
RY = ("Flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark brown hair, "
      "burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living room with a teal "
      "wall and a plant, ")
RYM = "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."
def ryan(id_, text, pose, mv): return dict(id=id_, spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"], text=text, kf=RY + pose, mv=mv + " " + RYM)
SHOTS = [
 # --- hook
 dict(id="a00", spk=M, eng="still", mv="in", refs=["worker", "robot"], sfx="quiet office, a tape measure clicking",
      text="If a robot could do your job for half the price, should your boss hire it? Before you answer, the robot is already measuring your desk.",
      kf="The woman from the first reference sitting at her office desk with her headset on, frozen mid-typing with wide alarmed eyes, while "
         "the robot from the second reference cheerfully measures the width of her desk with a long yellow tape measure. Exactly two characters."),
 dict(id="a01", spk=M, eng="ltx", refs=["worker", "robot"],
      text="Right now, in a lot of companies, someone is asking a very simple question. If a machine can do this job for less, why are we paying a person?",
      kf="A simple open-plan office: the woman from the first reference typing at her desk with her headset on, while the robot from the second "
         "reference stands politely right behind her chair, peering over her shoulder at the screen. Exactly two characters.",
      mv="The woman keeps typing, then slowly turns her head to look at the robot behind her; the robot gives a small polite wave. " + P1),
 dict(id="a02", spk=M, eng="still", mv="in", sfx="quiet office, keyboards clicking, air conditioning hum",
      text="It sounds like a maths problem. Cost of a human, minus cost of a machine. Keep the difference.",
      kf="A big simple old-fashioned balance scale on a cream background: on one side a small smiling robot, on the other side a person in a "
         "cardigan, the scale tipping towards the robot side."),
 dict(id="a03", spk=M, eng="still", mv="right", sfx="crowded debate hall murmuring",
      text="But it's really one of the biggest arguments of our time. On one side, efficiency. On the other, employment. So let's do what nobody online does, and actually hear both sides.",
      kf="A simple debate stage with two empty wooden podiums facing each other, one painted teal and one painted coral, a spotlight on each, "
         "a red curtain behind. No people."),
 ryan("a04", "Bold choice for the internet.", "arms folded, raising one eyebrow at camera. Exactly one person.",
      "The young man speaks to camera flatly, arms folded, one eyebrow raised, then gives a tiny shrug."),
 # --- how big is this
 dict(id="a05", spk=M, eng="card", card=dict(big="40%", small="OF JOBS EXPOSED TO AI", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet office hum",
      text="First, how big is this? In 2024, the International Monetary Fund estimated that almost forty percent of jobs worldwide are exposed to AI."),
 dict(id="a06", spk=M, eng="still", mv="in", sfx="busy city street, distant traffic",
      text="In rich countries, it's about sixty percent. Goldman Sachs put it another way: the equivalent of three hundred million full-time jobs.",
      kf="A busy city street seen from above with hundreds of tiny simple commuters walking, about six in every ten of them softly glowing teal."),
 dict(id="a07", spk=M, eng="still", mv="out", refs=["worker"], sfx="small office, a printer whirring",
      text="Those numbers sound terrifying, and they're often reported that way. But exposed doesn't mean replaced. It means AI can do some part of the job.",
      kf="The woman from the reference at her desk, looking calmly at a small glowing robot hand that is helpfully stapling papers for her. "
         "Exactly one person."),
 dict(id="a08", spk=M, eng="still", mv="left", sfx="quiet office, a coffee machine gurgling",
      text="The IMF actually thinks about half of the exposed jobs could benefit, with AI doing the boring bits and the person doing more of the rest.",
      kf="A woman with a headset leaning back happily with a mug of coffee while a small friendly robot sorts a tall pile of paper forms "
         "into neat stacks on her desk."),
 dict(id="a09", spk=M, eng="still", mv="in", sfx="quiet office, keyboards clicking",
      text="The other half is where the argument starts.",
      kf="A woman with a headset at her desk staring flatly at a small friendly robot that is now sitting in her chair wearing her headset."),
 # --- the case for: efficiency
 dict(id="a10", spk=M, eng="card", card=dict(big="98%", small="OF WEAVING LABOUR AUTOMATED", bg="#3C5A50", accent="#F2C14E"),
      sfx="old textile mill, looms clattering",
      text="Let's start with the case for efficiency, and it has history on its side. In the nineteenth century, power looms automated about ninety-eight percent of the work needed to weave a yard of cloth."),
 dict(id="a11", spk=M, eng="still", mv="right", sfx="old textile mill, looms clattering",
      text="You'd expect weaving jobs to vanish. Instead, the number of factory weavers grew.",
      kf="A bright Victorian textile mill hall with long rows of big iron power looms and many simple weavers in aprons working at them, "
         "sunlight through tall windows.",
      mv_ltx="The looms shuttle back and forth rhythmically, the workers move along the rows tending them. Static camera."),
 dict(id="a12", spk=M, eng="still", mv="right", sfx="busy Victorian market street, chatter",
      text="Cheaper cloth meant cheaper clothes. Cheaper clothes meant people bought a lot more of them. And a lot more cloth needed a lot more weavers.",
      kf="A Victorian market stall overflowing with colourful rolls of cloth and clothes, a queue of simple shoppers in bonnets and top hats "
         "stretching along the street."),
 dict(id="a13", spk=M, eng="still", mv="in", sfx="old mill, distant looms",
      text="By the late eighteen hundreds, factory weavers' wages were rising faster than most other workers'.",
      kf="A weaver in a leather apron proudly holding up a small cloth money bag next to a power loom, a simple upward arrow made of cloth "
         "ribbon behind him. Exactly one person."),
 dict(id="a14", spk=M, eng="still", mv="out", sfx="bank lobby, quiet chatter, a door opening",
      text="A more recent example. When cash machines spread across America, everyone assumed bank tellers were finished.",
      kf="A simple modern bank street corner with a cash machine in the wall and a little bank tellers' counter visible through the window."
         " No people."),
 dict(id="a15", spk=M, eng="card", card=dict(big="20 → 13", small="TELLERS PER BRANCH", bg="#2E4A62", accent="#F2A65A"),
      sfx="bank lobby, coins, quiet chatter",
      text="And the machines did cut the number of tellers a city branch needed, from about twenty to thirteen between 1988 and 2004."),
 dict(id="a16", spk=M, eng="still", mv="left", sfx="busy city street, traffic, a bank door chime",
      text="But running a branch got cheaper, so banks opened a lot more of them. Urban branches went up by forty-three percent, and the number of teller jobs didn't fall.",
      kf="A long city street lined with lots of identical small bank branches side by side, one after another into the distance. No people."),
 dict(id="a17", spk=M, eng="still", mv="in", sfx="bank lobby, friendly conversation",
      text="The job just changed. Less counting cash, more talking to customers and selling them things. Which, depending on your view of banks, is either progress or a warning.",
      kf="A bank teller in a neat waistcoat leaning eagerly across the counter towards a nervous customer, holding out a glossy brochure with "
         "a big smile. Exactly two people."),
 dict(id="a17b", spk=M, eng="still", mv="out", sfx="quiet bank, a phone notification ding",
      text="In fairness to the pessimists, teller numbers have been falling in recent years, as banking moved onto phones. The cash machine didn't kill the job. The app is having a better go.",
      kf="An empty quiet bank counter with a single tired teller resting her chin on her hand, while outside the window lots of people walk "
         "past staring at their phones. Exactly one person behind the counter."),
 dict(id="a18", spk=M, eng="card", card=dict(big="+14%", small="MORE PROBLEMS SOLVED PER HOUR", bg="#3C5A50", accent="#F2C14E"),
      sfx="call centre, phones ringing softly, keyboards",
      text="And there's evidence from AI itself. A study of more than five thousand customer support agents found that an AI assistant helped them solve about fourteen percent more problems per hour."),
 dict(id="a19", spk=M, eng="still", mv="right", refs=["worker"], sfx="call centre, soft voices, keyboards",
      text="The biggest gains went to the newest, least experienced workers. They improved by about a third. The experts barely changed, mostly because they already knew the answers.",
      kf="The woman from the reference at a call-centre desk with her headset, confidently helping a caller, a little robot on her monitor "
         "giving her a thumbs-up. Exactly one person."),
 dict(id="a20", spk=M, eng="card", card=dict(big="+78M", small="NET NEW JOBS BY 2030 (WEF)", bg="#2E4A62", accent="#F2C14E"),
      sfx="busy office, cheerful chatter",
      text="And the World Economic Forum expects technology and other trends to create a hundred and seventy million jobs by 2030, while displacing ninety-two million. A net gain of seventy-eight million."),
 dict(id="a21", spk=M, eng="still", mv="in", refs=["boss"], sfx="office, a pen clicking",
      text="So the efficiency case goes like this. Cheaper work means cheaper products, more demand, new kinds of jobs, and over time, everyone's money goes further.",
      kf="The man from the reference standing confidently next to a simple whiteboard drawing of a circle of arrows linking a coin, a shopping "
         "bag and a small factory, pointing at it with his coffee mug. Exactly one person."),
 dict(id="a21b", spk=M, eng="still", mv="left", sfx="busy town square, chatter",
      text="Economists even have a name for the fear on the other side. The lump of labour fallacy. The idea that there's a fixed amount of work in the world, so every task a machine does is one less for us.",
      kf="A giant lumpy clay blob labelled with nothing, sitting in a town square, with a crowd of small simple people each trying to pull off "
         "a piece of it."),
 dict(id="a21c", spk=M, eng="still", mv="in", sfx="busy office, chatter",
      text="Historically, that's been wrong. Two hundred years ago, most people worked on farms. Now very few do, and we didn't run out of jobs. We invented app developers, yoga teachers and people who review headphones on the internet.",
      kf="A simple split scene: on the left, a big field full of farm workers with hoes; on the right, a modern street with a yoga studio, a "
         "laptop cafe and a person filming themselves holding headphones."),
 dict(id="a22", spk=M, eng="still", mv="out", sfx="quiet office, a clock ticking",
      text="It's a strong argument. It's also the argument that has made almost every country on Earth richer than it was two hundred years ago.",
      kf="A simple illustrated timeline along a long green hill, from a tiny thatched cottage on the left to a bright modern city on the right, "
         "under a sunny sky. No people."),
 # --- the case against: employment
 dict(id="a22b", spk=M, eng="still", mv="in", sfx="cobbled street at dawn, a tapping on glass",
      text="Supporters also point out that some jobs are worth losing. In Victorian Britain, you could be paid to be a knocker-up, walking the streets before dawn, tapping on windows with a long stick to wake people for work.",
      kf="A Victorian street before dawn, a man in a flat cap and long coat tapping on an upstairs window with a very long wooden pole, "
         "gas lamps glowing. Exactly one person."),
 dict(id="a22c", spk=M, eng="still", mv="right", sfx="cobbled street at dawn, birds",
      text="Then alarm clocks got cheap. Nobody campaigned to save the knocker-ups. Most of them presumably got a lie-in.",
      kf="The same man in a flat cap asleep in a small bed with a nightcap on, his long wooden pole leaning in the corner, a ticking alarm "
         "clock on the bedside table. Exactly one person."),
 dict(id="a22d", spk=M, eng="still", mv="out", sfx="old telephone exchange, plugs clicking, quiet voices",
      text="For decades, telephone operator was one of the most common jobs for young women in America, plugging cables into switchboards all day. Then the network learned to connect calls by itself, and those women moved into other work.",
      kf="A long row of simple women telephone operators in 1940s dresses and headsets sitting at a huge wall switchboard full of cables and "
         "sockets."),
 dict(id="a22e", spk=M, eng="still", mv="in", sfx="quiet factory, a heavy machine humming",
      text="And machines are often best at the work that's dangerous, dull or bad for your back. That's a real benefit, and it's easy to forget once it's normal.",
      kf="A friendly robot arm lifting a heavy steel beam in a bright factory while a worker in a hard hat stands safely behind a yellow line "
         "with a clipboard, giving a thumbs up. Exactly one person."),
 dict(id="a23", spk=M, eng="still", mv="in", sfx="quiet empty room, wind outside",
      text="Now the other side. And the first thing it would point out is that 'over time' is doing a lot of work in that sentence.",
      kf="A simple wall clock on a cream wall with its hands spinning in a blur, small motion lines around it. No people."),
 dict(id="a24", spk=M, eng="ltx", refs=["weaver"],
      text="In 1811, cloth workers in Nottinghamshire started breaking into workshops at night and smashing knitting frames.",
      kf="The man from the reference inside a small wooden workshop at night, brightly lit by a warm lantern hanging above him so everything "
         "is clearly visible, raising a big wooden hammer over a large iron knitting frame machine. Exactly one person.",
      mv="He swings the hammer down onto the frame, a few wooden splinters fly, he looks over his shoulder at the window. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="a25", spk=M, eng="still", mv="right", refs=["weaver"], sfx="night, wind, a dog barking far away",
      text="They called themselves Luddites, after a leader called Ned Ludd, who probably never existed. Which is a very efficient way to run a movement.",
      kf="The man from the reference and two other workers in waistcoats huddled around a candle at night, looking at a crude charcoal drawing "
         "of a shadowy figure pinned to a wooden wall. Exactly three people."),
 dict(id="a26", spk=M, eng="still", mv="in", refs=["weaver"], sfx="quiet cottage, a fire crackling",
      text="Today, Luddite means someone who hates technology. But most of them didn't hate machines. They hated machines being used to cut their wages and replace skilled workers with cheaper ones.",
      kf="The man from the reference sitting at a small cottage table counting a tiny pile of coins, looking worried, an empty plate in front "
         "of him. Exactly one person."),
 dict(id="a27", spk=M, eng="card", card=dict(big="1812", small="FRAME BREAKING ACT", bg="#5A3C3C", accent="#F2C14E"),
      sfx="old courtroom, a gavel knock, murmuring",
      text="The government's response was to make breaking a machine punishable by death. Which settled the debate, though not in a way anyone would call a debate."),
 dict(id="a28", spk=M, eng="still", mv="out", sfx="rain on a cottage window, a fire crackling",
      text="And here's the uncomfortable part of the weaving story. The factory weavers did well. The hand-loom weavers they replaced mostly didn't. Their pay collapsed, and a lot of them never recovered.",
      kf="A small dark cottage room with an old wooden hand loom standing unused and covered in cobwebs, rain on the window. No people."),
 dict(id="a29", spk=M, eng="still", mv="in", sfx="busy street, distant traffic",
      text="The economy as a whole got richer. The specific people who lost out were not the people who gained.",
      kf="A simple illustration of a road splitting in two: on the bright sunny branch, a crowd of cheerful people walking towards a city; "
         "on the dark rainy branch, a few tired people walking away with bags."),
 ryan("a30", "So, good news for the economy. Less good for Dave.", "standing with his arms folded, looking at camera with a flat unimpressed expression. Exactly one person.",
      "The young man speaks flatly to camera, arms folded, then tilts his head slightly to one side."),
 dict(id="a31", spk=M, eng="still", mv="right", sfx="crowded train station, footsteps",
      text="That's the problem with net numbers. A net gain of seventy-eight million still means ninety-two million people whose jobs disappear. They're real people, and the new jobs may be in different places, needing different skills.",
      kf="A big crowd of simple people in work clothes standing on one side of a wide river, looking across at a shiny new city on "
         "the far bank, with no bridge between them. No signs, no flags, no writing."),
 dict(id="a32", spk=M, eng="still", mv="in", sfx="call centre, quiet, a single phone ringing",
      text="And some argue AI is different from looms and cash machines. Those replaced hands. AI is aimed at the thinking parts of jobs, writing, analysing, advising. The kinds of work people moved into the last time.",
      kf="A friendly robot at an office desk wearing reading glasses, writing in a notebook with one hand and typing with the other, a stack of "
         "neat reports beside it."),
 # --- Klarna
 dict(id="a32b", spk=M, eng="still", mv="right", sfx="city at night, distant traffic",
      text="There's also the question of where the savings go. The IMF warned that in most scenarios, AI is likely to make inequality worse, because the gains flow to the people who own the technology and the workers who can use it best.",
      kf="A tall shiny skyscraper with a glowing penthouse at the top, gold coins floating upwards into it from the dark streets below. "
         "No people."),
 dict(id="a32c", spk=M, eng="still", mv="in", sfx="quiet kitchen, a clock ticking",
      text="And a job isn't only a pay cheque. For a lot of people it's routine, identity, and the reason to get up in the morning. A spreadsheet doesn't have a column for that.",
      kf="A man in a work uniform sitting alone at a kitchen table early in the morning, an untouched lunchbox in front of him, looking at the "
         "door. Exactly one person."),
 dict(id="a33", spk=M, eng="still", mv="left", refs=["boss"], sfx="modern office, applause from a small crowd",
      text="We also have a real-world test. The Swedish payments company Klarna stopped hiring for over a year and announced that its AI assistant was doing the work of seven hundred customer service agents.",
      kf="The man from the reference on a small stage, proudly presenting a glowing robot with a sweeping arm gesture, confetti falling. "
         "Exactly one person and one robot."),
 dict(id="a34", spk=M, eng="card", card=dict(big="5,500 → 3,400", small="KLARNA STAFF", bg="#2E4A62", accent="#F2A65A"),
      sfx="quiet office, a door closing",
      text="Its workforce fell from around fifty-five hundred to thirty-four hundred, mostly by not replacing people who left."),
 dict(id="a35", spk=M, eng="still", mv="in", refs=["robot"], sfx="phone line, hold music muffled, a frustrated sigh",
      text="Then the company admitted it had focused too much on cost. Quality had suffered. Customers, it turned out, sometimes wanted a human.",
      kf="The robot from the reference wearing a headset at a call-centre desk, its screen face showing two confused dot eyes, a long tangled "
         "phone cord wrapped around its arms. Exactly one robot, no people."),
 dict(id="a36", spk=M, eng="still", mv="right", refs=["worker"], sfx="office, phones, friendly voices",
      text="So Klarna started bringing people back to customer service, with AI handling the simple questions and humans handling the complicated ones.",
      kf="The woman from the reference back at her call-centre desk with her headset, smiling, the little robot at the next desk handing her "
         "a cup of tea. Exactly one person and one robot."),
 dict(id="a37", spk=M, eng="still", mv="out", sfx="quiet office, keyboards",
      text="Which, if you remember, is roughly what the call centre study found in the first place.",
      kf="A woman with a headset and a small friendly robot sitting side by side at one shared desk, both typing calmly."),
 # --- is it even cheaper?
 dict(id="a37b", spk=M, eng="still", mv="right", sfx="call centre, calm voices",
      text="That study also found something easy to miss. The AI mostly spread the know-how of the best workers to everyone else. It worked less like a replacement, and more like having your most experienced colleague whispering in your ear.",
      kf="A woman with a headset at her desk, with a tiny friendly robot sitting on her shoulder whispering into her ear, while she smiles "
         "and types confidently. Exactly one person."),
 dict(id="a38", spk=M, eng="still", mv="in", sfx="quiet office, a calculator clicking",
      text="Which raises the question in the title. If it is cheaper. Because often, it isn't, yet.",
      kf="A very long paper receipt unrolling off a desk and across the floor, next to a small expensive-looking robot box with a bow on it. "
         "No people."),
 dict(id="a39", spk=M, eng="card", card=dict(big="23%", small="WORTH AUTOMATING TODAY (MIT)", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet lab, computer fans humming",
      text="Researchers at MIT looked at jobs involving visual tasks, like inspecting products. At today's prices, only about twenty-three percent of the wages paid for those tasks would be worth automating."),
 dict(id="a40", spk=M, eng="still", mv="left", sfx="small bakery, an oven door, a bell",
      text="For most businesses, building, installing and maintaining the system costs more than just paying the person. Especially in a small firm, where one person checks the bread and also answers the phone.",
      kf="A small cosy bakery with a cheerful baker inspecting a loaf of bread while holding a phone to her ear, flour on her apron. "
         "Exactly one person."),
 dict(id="a41", spk=M, eng="still", mv="in", sfx="quiet office, a clock ticking",
      text="Costs fall over time, of course. But it means the takeover is likely to be slower and patchier than the headlines suggest.",
      kf="A friendly robot standing on a ladder, slowly changing a single light bulb in a huge office ceiling full of light bulbs, only one "
         "bulb lit so far."),
 # --- cheaper for whom?
 ryan("a41b", "So the robots are coming. Slowly. And over budget.", "holding a coffee mug, looking at camera with a flat expression. Exactly one person.",
      "The young man speaks flatly to camera, then takes a slow sip from the mug."),
 dict(id="a42", spk=M, eng="still", mv="out", sfx="busy city, distant traffic",
      text="There's also a subtler problem with the word cheaper. Cheaper for whom?",
      kf="A big simple pie chart floating over a city skyline, one slice glowing gold and the rest grey. No people."),
 dict(id="a43", spk=M, eng="still", mv="right", sfx="government office, quiet, papers shuffling",
      text="When a company swaps workers for software, it saves money. But if those workers end up claiming benefits, retraining, or out of work for years, a lot of that cost lands on everyone else.",
      kf="A company building with a happy coin pouring out of its chimney, while next door a government building receives a long queue of "
         "tired people and a growing pile of paperwork."),
 dict(id="a44", spk=M, eng="still", mv="in", refs=["boss"], sfx="office, a coffee cup set down",
      text="Economists have a word for costs you cause but don't pay. It's an externality. Most people have a shorter word for it.",
      kf="The man from the reference sweeping a small pile of crumbs under a large rug with a broom, whistling innocently. Exactly one person."),
 # --- what could be done
 dict(id="a45", spk=M, eng="still", mv="left", sfx="classroom, chalk on a board, quiet voices",
      text="So what are the options? The most popular one is retraining. Help workers move into the new jobs before the old ones disappear.",
      kf="A simple bright classroom with adult learners of different ages at desks, one older man in a hi-vis vest concentrating hard on a "
         "laptop, a teacher pointing at a whiteboard of simple shapes."),
 dict(id="a46", spk=M, eng="still", mv="in", sfx="classroom, quiet",
      text="It sounds obvious, but it's hard to do well. Fifty-year-olds don't retrain as fast as a press release does.",
      kf="An older man in a hi-vis vest at a classroom desk, staring at a laptop with a confused face, a single pencil behind his ear. "
         "Exactly one person."),
 dict(id="a47", spk=M, eng="card", card=dict(big="ROBOT TAX?", small="BILL GATES, 2017", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet office hum",
      text="Another idea, suggested by Bill Gates in 2017, is a tax on robots. If a machine replaces a worker, the company pays something like the tax that worker would have paid."),
 dict(id="a48", spk=M, eng="still", mv="right", refs=["robot"], sfx="office, a calculator beeping",
      text="Critics say that would slow down useful technology. And nobody can quite agree on what counts as a robot.",
      kf="The robot from the reference standing next to a toaster, a dishwasher and a laptop, all lined up in a row like suspects at a police "
         "line-up. Exactly one robot, no people."),
 dict(id="a49", spk=M, eng="card", card=dict(big="€560", small="A MONTH, NO STRINGS (FINLAND)", bg="#3C5A50", accent="#F2A65A"),
      sfx="quiet Nordic town, wind, a bicycle bell",
      text="Then there's basic income. In 2017 and 2018, Finland gave two thousand unemployed people five hundred and sixty euros a month, whether or not they found work."),
 dict(id="a50", spk=M, eng="still", mv="in", sfx="quiet home, a kettle boiling",
      text="They reported better wellbeing and less stress. The effect on employment was small. Which supporters and critics both took as proof they were right.",
      kf="A calm man reading a book in a cosy Finnish living room with a cup of tea and a sleeping cat, snow falling outside the window. "
         "Exactly one person."),
 ryan("a51", "Classic.", "holding a mug, looking at camera with a tired, knowing expression. Exactly one person.",
      "The young man takes a small sip from the mug, then speaks the single word flatly to camera."),
 # --- verdict
 dict(id="a52", spk=M, eng="still", mv="out", sfx="crowded debate hall, murmuring",
      text="So, should AI replace human workers if it's cheaper?",
      kf="A simple debate stage with two empty wooden podiums facing each other, one painted teal and one painted coral, a spotlight on each, "
         "a red curtain behind. No people."),
 dict(id="a53", spk=M, eng="still", mv="in", sfx="quiet office, a clock ticking",
      text="History says new technology usually creates more jobs than it destroys, eventually. It also says eventually can be a whole working life, and that the gains rarely reach the people who paid for them.",
      kf="An old man and a young woman sitting on a park bench, the old man in a leather apron holding an old shuttle, the young woman holding "
         "a laptop, both looking towards a sunset over a city. Exactly two people."),
 dict(id="a54", spk=M, eng="still", mv="right", sfx="office, keyboards, a phone ringing",
      text="The evidence so far suggests the best results come from AI helping people, not simply replacing them. And that a company's spreadsheet doesn't always show the full bill.",
      kf="A woman with a headset and a friendly robot high-fiving over a shared desk, a happy customer on a video call on the screen between them."),
 dict(id="a55", spk=M, eng="still", mv="in", sfx="busy city street, people talking",
      text="So maybe the better question isn't whether AI should replace workers if it's cheaper. It's who pays the difference, and who gets to keep it.",
      kf="A simple big golden coin balanced on its edge on a table between a robot's hand and a person's hand, both reaching for it."),
 dict(id="a56", spk=M, eng="ltx", refs=["worker", "robot"],
      text="Tell us in the comments which side you're on. And subscribe, while the person editing these videos still has a job.",
      kf="The woman from the first reference and the robot from the second reference sitting side by side at a desk, both turning to look at "
         "camera, the robot holding a cup of coffee. Exactly two characters.",
      mv="The woman and the robot both turn to look at camera; the robot slowly sips its coffee and the woman raises an eyebrow. " + P1),
]
THUMB = dict(text="CHEAPER|THAN YOU?", refs=["worker", "robot"],
             kf="The woman from the first reference with her headset, shocked with her mouth wide open and hands on her cheeks, while the "
                "robot from the second reference sits smugly in her office chair wearing her headset and holding her coffee mug, a big pile "
                "of gold coins on the desk. Bright teal background. Exactly two characters.")
TAIL = 2.4
