"""The Great Stink, v2: faster, funnier (user, 2026-11-23: "voice sounds so AI and so slow... no comedic stuff. make the reel a lot better").
Humour per library/HUMOR_GUIDE.md: dry observations, deadpan, visual gags; facts unchanged.
Sources: UK Parliament "The Great Stink"; The Times, July 1858 (Disraeli leaving a committee room, handkerchief to his nose);
Science Museum on Bazalgette (1,100+ miles of street sewers, pipes oversized "just in case"); 1861 census (London ~2.8 million)."""
from topics.greatstink import STYLE, ENV_STYLE, LOOK, LTX_WH, H3_REF_KF, CHARS as _C
ERA = "Victorian London 1858"
M, R = "maya", "benny"
GAP = 0.15                   # snappier: short breath between lines
TEMPO = 1.10                 # user picked C (2026-11-23): lively lock + 10%
VOICE_REF = {"maya": {"ref_audio": "library/voices/maya/ref_lively.wav", "ref_text": "library/voices/maya/ref_lively.txt"}}
CHARS = dict(_C, disraeli=("Benjamin Disraeli in 1858 as a simple flat vector character: slim, pale, a single dark curl of black hair on his "
                           "forehead, small black goatee, dark plum frock coat, grey waistcoat, small round head, dot eyes."))
SHOTS = [
 dict(id="s01", spk=M, text="In the summer of 1858, London smelled so bad that it got its own name. The Great Stink.", eng="ltx", env=True,
      kf="Vertical flat illustration: the London skyline with the Houses of Parliament and clock tower beside the murky olive-green River "
         "Thames, a single enormous lumpy green stink cloud hanging over the whole city, a few small birds flying away from it.",
      mv="The huge green stink cloud slowly swells and bulges over the city, the little birds flap away as fast as they can, the river "
         "ripples. Static camera."),
 dict(id="s02", spk=M, text="The recipe was simple. Nearly three million people, plus the hot new invention of the decade: the flushing toilet.", eng="ltx", env=True,
      kf="Vertical flat illustration: a single Victorian toilet with a tall wall-mounted cistern and pull chain, displayed on a round "
         "velvet pedestal under a bright spotlight like a luxury product launch, simple sparkle shapes around it, dark teal background.",
      mv="The spotlight glows, the little sparkle shapes twinkle around the toilet, the pull chain swings gently. Slow push in."),
 dict(id="s03", spk=M, text="And one river to flush it all into.", eng="ltx", env=True,
      kf="Vertical flat illustration, simple cross-section: a row of little Victorian terraced houses on a riverbank, each with a simple "
         "brown pipe running down underground and straight out into the murky olive-green river.",
      mv="Brown water gushes out of every pipe end into the river one after another, the river turns darker and ripples. Static camera."),
 dict(id="s04", spk=M, text="Then add a heatwave, and leave it to simmer.", eng="card",
      card=dict(big="1858", small="HEATWAVE", bg="#3C5A50", accent="#F2C14E"), sfx="hot summer day, flies buzzing, river water lapping"),
 dict(id="s05", spk=M, text="That same river was also where a lot of Londoners got their drinking water.", eng="ltx",
      kf="Vertical flat illustration: a simple Victorian woman character with a round head, dot eyes, brown hair in a bun, long dusty-coral dress "
         "and cream apron, standing beside a green iron street water pump on the riverbank, holding a jug under the spout. Exactly one person.",
      mv="Greenish water pours from the pump spout into her jug, she looks into the jug, then slowly turns to look at camera, unimpressed. "
         "Static camera. Exactly one person; she keeps the same face and dress."),
 dict(id="s06", spk=R, tag="disbelief", text="Hold on. The toilet and the tap were the same river?", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, holding a glass of water, staring at it in horror. Exactly one person.",
      mv="The young man looks from the glass of water to camera in disbelief and speaks, then slowly puts the glass down out of frame. "
         "Static camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="s07", spk=M, text="For years, nobody in charge did a thing. Then the smell reached the one building that mattered.", eng="ltx", env=True,
      kf="Vertical flat illustration: the Gothic Houses of Parliament as simple flat cream shapes on the riverbank, and a big lumpy green "
         "stink cloud with a sly cartoon grin creeping up the river toward it, soft teal sky.",
      mv="The grinning green stink cloud creeps slowly along the river toward Parliament and stretches a wispy arm up toward its windows. "
         "Static camera."),
 dict(id="s08", spk=M, tag="dry", text="Parliament sits right on the river. They soaked the curtains in chemicals. The curtains lost.", eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference stands beside a tall window covered by a damp cream "
         "curtain, holding his white handkerchief, wavy green stink lines seeping around the curtain edges. Exactly one person.",
      mv="The green stink lines push through, the curtain slowly droops and wilts, the man looks at the wilting curtain and sighs into his "
         "handkerchief. Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="s09", spk=M, text="Future Prime Minister Benjamin Disraeli was seen fleeing a committee room, with a handkerchief clamped to his nose.", eng="ltx", refs=["disraeli"],
      kf="Vertical flat illustration: the man from the reference (single black curl on his forehead, small goatee, plum frock coat) hurrying "
         "out through a tall wooden committee-room doorway into a simple corridor, papers under one arm, a white handkerchief clamped over "
         "his nose, green stink lines behind him. Exactly one person.",
      mv="He hurries forward out of the doorway, handkerchief pressed to his nose, papers flapping, the green stink lines trailing after him. "
         "Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="s10", spk=M, text="Doctors back then believed bad smells caused disease. So as far as Parliament knew, the air was trying to kill them personally.",
      eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference stands alone in a simple flat corridor, wide-eyed with "
         "fear, while a big cartoon green smell cloud with a gloomy face floats toward him. Exactly one person.",
      mv="The green smell cloud drifts closer, the man leans back in alarm, his top hat lifts slightly off his head. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="s11", spk=M, text="A sewer plan they had ignored for years suddenly passed in eighteen days.", eng="card",
      card=dict(big="18", small="DAYS", bg="#2E4A62", accent="#F2A65A"), sfx="quiet old hall, paper rustling, a wooden gavel knock"),
 dict(id="s12", spk=M, tag="dry", text="Nothing speeds up a government like a problem it can smell from its own desk.", eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference sits at a simple wooden desk with a wooden clothes "
         "peg clipped on his nose, quill in hand, stamping and signing a pile of papers, a green stink wisp curling near the window behind "
         "him. Exactly one person.",
      mv="He signs and stamps the papers very fast, sheet after sheet flying onto a growing pile, the clothes peg on his nose wobbling. "
         "Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="s13", spk=M, text="Engineer Joseph Bazalgette built over a thousand miles of sewers, and made the pipes far bigger than he needed. Just in case.",
      eng="ltx", refs=["bazalgette"],
      kf="Vertical flat illustration: the engineer from the reference (big bushy sideburns, navy frock coat) stands proudly next to the open "
         "end of an enormous round brick sewer pipe that towers over him, a soft cream background. Exactly one person.",
      mv="He looks up at the enormous pipe, nods with satisfaction and pats the brickwork with one hand. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="s14", spk=M, tag="dry", text="London's population has more than tripled since. Just in case turned out to be the whole plan.", eng="ltx", env=True,
      kf="Vertical flat illustration of a cross-section under a busy modern London street: a huge round warm-orange brick Victorian sewer "
         "tunnel with water flowing along its floor, modern buildings and a red double-decker bus on the street above.",
      mv="The water flows steadily along the tunnel floor, the bus above rolls slowly across the frame from left to right. Static camera."),
 dict(id="s15", spk=M, text="Here's the twist. Cholera doesn't spread through bad smells. It spreads through dirty water.", eng="ltx", env=True,
      kf="Vertical flat illustration: a big clear water droplet on a soft teal background with two small cartoon germ shapes inside it, "
         "simple and clean.",
      mv="The water droplet wobbles gently, the two little germ shapes drift and bounce slowly inside it. Static camera."),
 dict(id="s16", spk=M, tag="dry", text="So they beat cholera by accident. Wrong theory. Right sewer. Subscribe for more.", eng="ltx", env=True,
      kf="Vertical flat illustration: modern London at sunset, the clean blue River Thames, the clock tower and a few simple modern buildings "
         "as flat shapes, a warm orange sky, a few birds.",
      mv="The river sparkles gently, the birds glide across the sky, the sunset glow shifts softly. Static camera."),
]
TAIL = 2.4
