"""The St Kilda mailboats (1877-2020). Sources: National Trust for Scotland, "St Kilda mailboat's epic journey" (29 Aug 2020) and NTS
St Kilda history pages; John Sands, Chambers's Journal (1877); The Times, 30 Aug 1930 (evacuation)."""
ERA = "Scottish Hebridean island period detail, wild North Atlantic light, stone cottages, tweed and wool clothing"
M, R = "maya", "benny"
CHARS = {}
SHOTS = [
 dict(id="k01", spk=M, text="In 2020, four children on a beach in Arctic Norway found a tiny wooden boat. Inside were postcards, still dry.",
      eng="ltx",
      kf="Vertical shot on a pebbly Arctic Norwegian beach under a pale summer sky with snowy mountains behind: three children and a small "
         "girl in colourful modern rain jackets crouch around a small hand-carved wooden toy boat with a little hatch open, one child holding "
         "up a dry postcard in wonder. Exactly four people, all children.",
      mv="The child carefully lifts the postcard out of the little boat's hatch, the others lean in amazed and look at each other. "
         "Gentle waves wash the pebbles behind them. Exactly four children; everyone keeps the same face and jacket."),
 dict(id="k02", spk=M, text="They had been sent by the ocean, from an island off Scotland more than a thousand miles away.", eng="ltx", env=True,
      kf="Vertical close shot of a tiny empty toy-sized hand-carved wooden boat, only as long as a forearm, with a little stick mast, tied to an "
         "inflated pale sheepskin float, bobbing alone on a huge dark rolling North Atlantic wave under a stormy grey sky, spray flying. "
         "The little boat is empty: nobody is in it, it is far too small for a person.",
      mv="The tiny boat climbs the face of the huge wave, tips over the crest and slides down the other side, the sheepskin float bobbing, "
         "spray blowing off the wave tops. The camera rises and falls with the swell. No people."),
 dict(id="k03", spk=M, text="This is St Kilda. For most of the year, no ship could reach it.", eng="ltx", env=True,
      kf="Vertical shot of the remote island of St Kilda rising from a stormy North Atlantic: enormous green-topped sea cliffs hundreds of metres "
         "high, a curved bay with one row of small stone cottages, thousands of seabirds wheeling, huge waves smashing white against the rocks.",
      mv="Huge waves crash against the foot of the cliffs and burst into white spray, clouds of seabirds swirl, mist drifts over the cliff "
         "tops. Slow aerial push in toward the bay. No people."),
 dict(id="k04", spk=M, text="In 1877, a journalist stuck there with nine shipwrecked sailors threw a message into the sea, tied to a lifebuoy.",
      eng="ltx",
      kf="Vertical shot on wet black rocks at the edge of the sea on St Kilda in winter: a bearded Victorian journalist in a long dark wool "
         "overcoat and flat cap holds a round white ship's lifebuoy with a small oilcloth packet tied to it, ready to throw it into the grey "
         "waves, while two weary shipwrecked sailors in worn pea coats watch behind him. Exactly three people.",
      mv="The journalist swings the lifebuoy back and hurls it out into the sea, it lands in the grey waves and is carried away, the "
         "sailors watch it go hopefully. Wind whips their coats. Exactly three people; everyone keeps the same face and clothes."),
 dict(id="k05", spk=M, text="Nine days later, it washed up in Orkney. A ship came to rescue them.", eng="ltx", env=True,
      kf="Vertical shot of a calm sandy beach in Orkney at sunrise, the round white lifebuoy with its oilcloth packet lying washed up at the "
         "waterline, seaweed around it, low green hills and a small stone farmhouse in the distance.",
      mv="A gentle wave washes up around the lifebuoy and slides back, the morning light grows warmer, a seabird lands nearby. Slow push in. No people."),
 dict(id="k06", spk=R, tag="disbelief", text="Nine days. My parcels take longer than that.", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical waist-up shot of the young man from the reference (thick curly dark brown hair, burnt-orange open hoodie over white t-shirt, "
         "black crossbody strap) standing in a small cosy modern apartment living room holding a small cardboard parcel, looking at camera "
         "with a sceptical raised eyebrow. Exactly one person.",
      mv="The young man speaks to camera in disbelief, lifts the small parcel and gestures at it, then a slow unimpressed blink. Locked-off "
         "camera, waist-up. Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="k07", spk=M, text="In 1885, a storm ruined the island's food. A fourteen-year-old boy carved five little boats, and sent them out asking for help.",
      eng="ltx",
      kf="Vertical shot on a grey St Kilda shore at dawn after a storm: a fourteen-year-old island boy in a rough wool jersey and cap kneels at "
         "the water's edge, setting a small hand-carved wooden boat with a sheepskin float into the surf, four more little boats lined up on "
         "the rocks beside him. Exactly one person.",
      mv="The boy gently pushes the little boat out into the waves, it bobs and drifts away, he picks up the next one and watches the first "
         "sail out to sea. Exactly one person; he keeps the same face and clothes."),
 dict(id="k08", spk=M, text="One of them reached the Isle of Lewis. The newspapers picked up the story, and a relief boat came.", eng="ltx",
      kf="Vertical shot of a small Victorian steam relief boat with a tall funnel arriving in a St Kilda bay under clearing skies, a group "
         "of islanders in wool clothing waving from the stone landing, the boy among them. Exactly six people.",
      mv="The steamer chugs into the bay trailing smoke, the islanders wave their caps and arms in relief, the boy jumps up and down. "
         "Exactly six people; everyone keeps the same face and clothes."),
 dict(id="k09", spk=M, text="After that, it became the island's mail. A carved boat, a sheepskin float, the letters sealed in a tin, launched when the wind blew from the northwest.",
      eng="ltx",
      kf="One single continuous image, not a collage, no panels: vertical close-up of weathered hands of an island man placing a folded letter into a small tin, then into the hollow of a small "
         "hand-carved wooden boat tied to an inflated sheepskin float, on a stone wall by the sea, a knife and wood shavings beside it. Hands only.",
      mv="The hands press the tin into the boat's hollow, slide a little wooden lid shut over it and tie the sheepskin float tight. Wind "
         "ruffles the grass behind. Hands only, no faces."),
 dict(id="k10", spk=M, text="About two out of every three were found, in Scotland or in Norway.", eng="ltx", env=True,
      kf="Vertical shot looking out from the St Kilda cliffs over a vast North Atlantic at golden hour, several tiny wooden mailboats with "
         "sheepskin floats scattered far apart on the long rolling swells, heading toward the horizon.",
      mv="The tiny boats ride the long golden swells away toward the horizon, sunlight glittering on the water, seabirds gliding past. "
         "Slow drift forward. No people."),
 dict(id="k11", spk=M, tag="sombre", text="In 1930, the last thirty-six islanders left St Kilda for good.", eng="ltx",
      kf="Vertical shot from the deck of a grey 1930 naval ship leaving St Kilda: in the foreground a few island families in wool clothing "
         "stand at the rail looking back, the island's cliffs and the row of stone cottages shrinking behind them in the morning haze. Exactly four people.",
      mv="The ship pulls away, the island slowly recedes into the haze, the islanders stand still at the rail, one woman pulls her shawl "
         "tighter. Exactly four people; everyone keeps the same face and clothes."),
 dict(id="k12", spk=M, text="Eighty years later, the National Trust for Scotland launched one more mailboat, with seven postcards.", eng="ltx",
      kf="Vertical shot on the St Kilda shore in 2010 on a bright windy day: a woman ranger in a modern green waterproof jacket crouches at the "
         "water's edge holding a small hand-carved wooden mailboat with a float, ready to set it on the waves. Exactly one person.",
      mv="The ranger sets the little boat on the water and lets it go, it bobs out to sea on the waves, she stands and watches it go. "
         "Exactly one person; she keeps the same face and jacket."),
 dict(id="k13", spk=M, tag="dry", text="It drifted for ten years, all the way to that beach in Norway. And the postcards got delivered. Subscribe for more.",
      eng="ltx", env=True,
      kf="Vertical shot of a small red rectangular Norwegian letterbox on a wooden post beside a red wooden house in Arctic Norway on a bright summer evening, a little "
         "hand-carved wooden mailboat with a sheepskin float resting on top of the letterbox, snowy mountains and a calm sea behind.",
      mv="The evening light glows, a breeze sways the grass, gentle waves lap the shore in the background, seabirds glide past. "
         "Slow push in to the little boat. No people."),
]
TAIL = 3.0
