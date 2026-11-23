"""The Great Stink, v3: written to the user's 2026-11-23 humour guide (library/HUMOR_GUIDE.md).
This story's comedic personality: an unimpressed friend noticing whose problems Parliament considers urgent. Understatement, plain
facts with the joke left to the visual, one comparison, one callback-free twist; no announced punchlines, no list formula.
Verified: 200-250 tons of lime used near the sewer outfalls (Halliday 2013 via Wikipedia "Great Stink"); The Times leader: Parliament
"all but compelled to legislate ... by the force of sheer stench" (RMG "Dickens and the Great Stink"); curtains soaked in chloride of lime;
Disraeli leaving a committee room with a handkerchief to his nose (The Times, 1858); Metropolis Local Management Amendment Act passed in
18 days; Bazalgette ~1,100 miles of street sewers, pipes oversized; London ~2.8 m (1861) vs ~9 m today; overflows still happen (Tideway Tunnel)."""
from topics.greatstink2 import STYLE, ENV_STYLE, LOOK, LTX_WH, H3_REF_KF, CHARS, GAP, TEMPO, VOICE_REF
ERA = "Victorian London 1858"
M, R = "maya", "benny"
V2 = "projects/short-greatstink2/keyframes"
REUSE_KF = {"t01": f"{V2}/s01.png", "t02": f"{V2}/s05.png", "t05": f"{V2}/s07.png", "t06": f"{V2}/s08.png", "t08": f"{V2}/s09.png",
            "t09": f"{V2}/s10.png", "t12": f"{V2}/s12.png", "t13": f"{V2}/s13.png", "t14": f"{V2}/s14.png", "t15": f"{V2}/s15.png", "t16": f"{V2}/s16.png"}
SHOTS = [
 dict(id="t01", spk=M, text="By 1858, London had been using the River Thames as a toilet for decades. Nobody important seemed to mind.", eng="ltx", env=True,
      kf="(reused)", mv="The huge green stink cloud slowly swells and bulges over the city, the little birds flap away as fast as they can, "
                       "the river ripples. Static camera."),
 dict(id="t02", spk=M, text="The same river, incidentally, supplied a lot of the city's drinking water.", eng="ltx",
      kf="(reused)", mv="Greenish water pours from the pump spout into her jug, she looks into the jug, then slowly turns to look at camera, "
                       "completely unimpressed. Static camera. Exactly one person; she keeps the same face and dress."),
 dict(id="t03", spk=M, text="Thousands of people were dying of cholera. Parliament decided the sensible thing to do was keep scheduling meetings about it.",
      eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference fast asleep in a big green leather armchair, head "
         "tipped back, mouth open, top hat slipping over his eyes, a towering wobbly stack of paper reports on a small table beside him, "
         "a simple panelled room. Exactly one person.",
      mv="He snores peacefully, his chest rising and falling, the top hat slowly slides further down over his face, the tall stack of "
         "reports leans and wobbles. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t04", spk=M, text="The summer of 1858 arrived, temperatures soared, and the Thames started producing a smell bad enough to get its own name. The Great Stink.", eng="card",
      card=dict(big="1858", small="THE GREAT STINK", bg="#3C5A50", accent="#F2C14E"), sfx="hot summer day, flies buzzing, river water lapping"),
 dict(id="t05", spk=M, text="Parliament had recently moved into a beautiful new building. Unfortunately, they had also built it next to the Thames. With windows.", eng="ltx", env=True,
      kf="(reused)", mv="The grinning green stink cloud creeps slowly along the river toward Parliament and stretches a wispy arm up toward "
                       "its windows. Static camera."),
 dict(id="t06", spk=M, text="They soaked the curtains in chemicals.", eng="ltx", refs=["mp"],
      kf="(reused)", mv="The green stink lines drift through the curtain as if it isn't there, the curtain slowly droops, the man watches "
                       "it and sighs into his handkerchief. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t07", spk=M, text="Then workers spread hundreds of tons of lime along the riverbanks. Which was essentially putting deodorant on a corpse.",
      eng="ltx",
      kf="Vertical flat illustration: a simple Victorian workman character with a round head, dot eyes, flat cap, rolled sleeves and brown "
         "waistcoat, shovelling white powdery lime from a wooden wheelbarrow onto the muddy brown riverbank, while a huge lumpy green stink "
         "cloud hangs over the murky olive-green river behind him. Exactly one person.",
      mv="He shovels a scoop of white lime onto the mud, a little white puff rises, the big green stink cloud behind him barely wobbles. "
         "He stops, looks at it, and wipes his brow. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t08", spk=M, text="At one point, future Prime Minister Benjamin Disraeli was seen leaving a committee room in a hurry, handkerchief pressed to his face.",
      eng="ltx", refs=["disraeli"],
      kf="(reused)", mv="He hurries forward out of the doorway, handkerchief pressed to his nose, papers flapping, the green stink lines "
                       "trailing after him. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t09", spk=M, text="At the time, most doctors believed disease spread through foul air. So to the politicians breathing it every day, the smell now looked like a threat to them personally.",
      eng="ltx", refs=["mp"],
      kf="(reused)", mv="The green smell cloud drifts closer, the man leans back in alarm, his top hat lifts slightly off his head. "
                       "Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t10", spk=R, tag="deadpan", text="Oh. So now it's urgent.", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, arms folded, standing in a simple flat "
         "cosy living room with a teal wall and a plant, looking at camera with a flat, unimpressed expression. Exactly one person.",
      mv="The young man speaks to camera flatly, unimpressed, arms folded, then a slow blink and a tiny shake of the head. Static camera, "
         "waist-up. Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="t11", spk=M, text="A sewer plan that had been put off for years was approved in eighteen days.", eng="card",
      card=dict(big="18", small="DAYS", bg="#2E4A62", accent="#F2A65A"), sfx="quiet old hall, paper rustling, a wooden gavel knock"),
 dict(id="t12", spk=M, text="The Times summed it up quite nicely. Parliament had been forced to act by the force of sheer stench.", eng="ltx", refs=["mp"],
      kf="(reused)", mv="He signs and stamps the papers very fast, sheet after sheet flying onto a growing pile, the clothes peg on his nose "
                       "wobbling. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="t13", spk=M, text="The engineer, Joseph Bazalgette, built over a thousand miles of sewers, and made the pipes far wider than his maths said he needed. Just in case.",
      eng="ltx", refs=["bazalgette"],
      kf="(reused)", mv="He looks up at the enormous pipe, nods with satisfaction and pats the brickwork with one hand. Static camera. "
                       "Exactly one person; he keeps the same face and clothes."),
 dict(id="t14", spk=M, text="London's population has more than tripled since. Those oversized pipes turned out to be a pretty good investment.", eng="ltx", env=True,
      kf="(reused)", mv="The water flows steadily along the tunnel floor with small ripples. The street above stays completely still: the "
                       "red bus stays parked exactly where it is and keeps its shape. Static camera."),
 dict(id="t15", spk=M, text="And the part nobody saw coming? Cholera doesn't spread through bad air. It spreads through dirty water.", eng="ltx", env=True,
      kf="(reused)", mv="The water droplet wobbles gently, the two little germ shapes drift and bounce slowly inside it. Static camera."),
 dict(id="t16", spk=M, text="So Parliament built the sewers to get rid of a smell, and ended up helping to protect London's drinking water. The city's last major cholera outbreak came in 1866. Subscribe for more.", eng="ltx", env=True,
      kf="(reused)", mv="The river sparkles gently, the birds glide across the sky, the sunset glow shifts softly. Static camera."),
]
TAIL = 2.4
