"""The Great Stink, London, summer 1858. FLAT 2D STYLE PILOT (simple, fast).
Sources: UK Parliament, "The Great Stink" (parliament.uk living heritage); Science Museum, "Joseph Bazalgette and London's sewers";
Hansard 1858 (Metropolis Local Management Amendment Act, passed in 18 days); Stephen Halliday, "The Great Stink of London" (1999)."""
ERA = "Victorian London 1858"
M, R = "maya", "benny"
STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with "
         "very subtle gradients, no outlines, no texture, no clutter. Soft attractive palette of muted teal, warm cream, dusty coral, mustard "
         "yellow and murky olive green. Simple cute characters with round heads, small dot eyes, minimal facial features, simple bodies, "
         "consistent proportions. Clean simple background with only a few large shapes. Victorian London 1858 setting. "
         "Absolutely no text, letters, numbers or logos anywhere.")
ENV_STYLE = ("Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours with "
             "very subtle gradients, no outlines, no texture, no clutter. Soft attractive palette of muted teal, warm cream, dusty coral, mustard "
             "yellow and murky olive green. Clean simple background with only a few large shapes. "
             "Show only what the description names. There are NO characters of any kind: no people, no babies, no children, no mascots, "
             "no creatures, no cute figures, no faces. Absolutely no text, letters, numbers or logos anywhere.")
LOOK = ("Simple flat 2D vector explainer animation, smooth gentle motion, static background, shapes keep their exact form and colours, "
        "minimal movement, no morphing, no camera shake.")
LTX_WH = (512, 896)          # half-size render, upscaled to 1080x1920 in the mix
H3_REF_KF = True             # Ryan's flat-style keyframe is his reference (keeps the flat look)
CHARS = {
 "bazalgette": "Joseph Bazalgette, Victorian engineer, as a simple flat vector character: small and slim, big bushy dark mutton-chop "
               "sideburns joined to a thick moustache, bald dome, dark navy frock coat, cream shirt, small round head, dot eyes.",
 "mp": "a Victorian Member of Parliament as a simple flat vector character: plump, tall black top hat, grey sideburns, dark green frock "
       "coat, white cravat, small round head, dot eyes, holding a white handkerchief.",
}
SHOTS = [
 dict(id="g01", spk=M, text="In the summer of 1858, London smelled so bad that the newspapers gave it a name. The Great Stink.", eng="ltx", env=True,
      kf="Vertical flat illustration: the River Thames in London on a hot summer day, the river a murky olive-green, the Houses of Parliament "
         "and its clock tower as simple flat shapes on the bank, a big round yellow sun, and wavy green stink lines rising from the water.",
      mv="The wavy green stink lines rise and wobble gently up from the river, small ripples move on the water, the sun pulses softly. "
         "Static camera."),
 dict(id="g02", spk=M, text="A heatwave had hit the city, and the River Thames was basically an open sewer.", eng="card",
      card=dict(big="1858", small="HEATWAVE", bg="#3C5A50", accent="#F2C14E"), sfx="hot summer day, flies buzzing, river water lapping"),
 dict(id="g03", spk=M, text="London had just fallen in love with the flushing toilet. And almost all of it ended up in the river.", eng="ltx", env=True,
      kf="Vertical flat illustration of a simple Victorian bathroom: a white toilet with a tall wall-mounted cistern and a hanging pull chain, "
         "soft cream wall with teal tiles, clean and minimal.",
      mv="The pull chain swings gently, water swirls around in the toilet bowl and drains away. Static camera."),
 dict(id="g04", spk=M, text="Which was also where a lot of Londoners got their drinking water.", eng="ltx",
      kf="Vertical flat illustration: a simple Victorian woman character with a round head, dot eyes, brown hair in a bun, long dusty-coral dress "
         "and cream apron, standing beside a green iron street water pump on the riverbank, holding a jug under the spout. Exactly one person.",
      mv="Greenish water pours from the pump spout into her jug, she looks into the jug and pulls a doubtful face. Static camera. "
         "Exactly one person; she keeps the same face and dress."),
 dict(id="g05", spk=R, tag="disbelief", text="Please tell me they fixed that part first.", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, looking at camera with a worried raised eyebrow. Exactly one person.",
      mv="The young man speaks to camera, worried, one hand raised in a small pleading gesture, then a slow blink. Static camera, waist-up. "
         "Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="g06", spk=M, text="Right beside the river stood the brand new Houses of Parliament. The smell came in through every window.", eng="ltx", env=True,
      kf="Vertical flat illustration: the Gothic Houses of Parliament as simple flat cream shapes with rows of tall windows, beside the murky "
         "olive-green river, wavy green stink clouds drifting from the water toward the windows, soft teal sky.",
      mv="The wavy green stink clouds drift slowly from the river toward the building and curl in through the windows. Static camera."),
 dict(id="g07", spk=M, text="Staff hung curtains soaked in chemicals over the windows to block it out. It did not work.", eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference stands inside a simple flat panelled committee room "
         "next to a tall window covered by a damp cream curtain, pressing his white handkerchief to his nose, wavy green stink lines "
         "seeping around the curtain. Exactly one person.",
      mv="The green stink lines seep around the curtain, the man's eyes water, he presses the handkerchief harder to his nose and leans away. "
         "Static camera. Exactly one person; he keeps the same face and clothes."),
 dict(id="g08", spk=M, text="Back then, doctors believed bad smells caused diseases like cholera. So the politicians thought the air itself could kill them.",
      eng="ltx", refs=["mp"],
      kf="Vertical flat illustration: the plump Member of Parliament from the reference stands alone in a simple flat corridor, wide-eyed with "
         "fear, while a big cartoon green smell cloud with a gloomy face floats toward him. Exactly one person.",
      mv="The green smell cloud drifts closer, the man leans back in alarm, his top hat lifts slightly off his head. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="g09", spk=M, text="Suddenly, a sewer plan they had put off for years was approved in just eighteen days.", eng="card",
      card=dict(big="18", small="DAYS", bg="#2E4A62", accent="#F2A65A"), sfx="quiet old hall, paper rustling, a wooden gavel knock"),
 dict(id="g10", spk=M, text="Engineer Joseph Bazalgette built more than a thousand miles of sewers under London.", eng="ltx", refs=["bazalgette"],
      kf="Vertical flat illustration: the engineer from the reference (big bushy sideburns, navy frock coat) stands at a simple wooden drafting "
         "table unrolling a big blue blueprint of tunnel lines, a soft cream background. Exactly one person.",
      mv="He unrolls the blueprint, looks it over, nods with satisfaction and taps it with one finger. Static camera. "
         "Exactly one person; he keeps the same face and clothes."),
 dict(id="g11", spk=M, text="He even made the pipes bigger than they needed to be, just in case. Much of his system is still working today.", eng="ltx", env=True,
      kf="Vertical flat illustration of a cross-section of a huge round brick sewer tunnel under a London street, warm orange brick ring, "
         "a stream of water flowing along its floor, the street above with a simple lamp post.",
      mv="The water flows steadily along the tunnel floor, small ripples move, a soft light glows from the lamp above. Static camera."),
 dict(id="g12", spk=M, text="And here's the twist. Cholera actually spreads through dirty water, not bad smells.", eng="ltx", env=True,
      kf="Vertical flat illustration: a big clear water droplet on a soft teal background with a few small cartoon germ shapes inside it, "
         "simple and clean.",
      mv="The water droplet wobbles gently, the little germ shapes drift and bounce slowly inside it. Static camera."),
 dict(id="g13", spk=M, tag="dry", text="So by fixing a smell, London accidentally beat cholera too. Subscribe for more.", eng="ltx", env=True,
      kf="Vertical flat illustration: modern London at sunset, the clean blue River Thames, the clock tower and a few simple modern buildings "
         "as flat shapes, a warm orange sky, a few birds.",
      mv="The river sparkles gently, the birds glide across the sky, the sunset glow shifts softly. Static camera."),
]
TAIL = 2.6
