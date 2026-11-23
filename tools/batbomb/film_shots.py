"""Shot list for the full bat-bomb film (16:9). Lines come from scripts/BATBOMB_STAGE2_NARRATION.md by (section, index).

Each entry: dict(
  id, line=(sec, idx) or None, beat=seconds (silent shot) , w=share of the line's time (when a line has several shots),
  eng='h3'|'ltx'|'reuse'|'card', refs=[...], kf=keyframe prompt, mv=motion prompt, sfx=natural foley (H3/card shots),
  reuse=path of an already-approved clip, n=number of people (H3 people rule))
Character look-locks are inserted with {ADAMS}, {FIESER}... so every prompt describes the same person the same way.
"""
LOCK = {
 "ADAMS": "the dentist Doc Adams from the reference (short, round-bellied, balding with a neat grey fringe, round wire-rimmed glasses, rosy cheeks, brown three-piece wool suit, small red bow tie, brown fedora)",
 "FIESER": "the chemist Fieser from the reference (tall, lean, neat dark-brown hair combed back, clean-shaven narrow face, white knee-length lab coat over grey waistcoat and dark tie)",
 "RANCHER": "the old rancher from the reference (white bushy moustache, white stubble, battered tan cowboy hat, faded blue work shirt, brown suspenders, denim jeans)",
 "FDR": "the president from the reference (dignified stylised Franklin Roosevelt: broad face, strong jaw, grey hair swept back, rimless pince-nez glasses, dark grey double-breasted suit)",
 "RYAN": "the young man Ryan from the reference (thick curly dark brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap)",
 "EPLER": "the Army officer Epler from the reference (lieutenant colonel, stern square-jawed man in his forties, khaki 1943 US Army officer uniform with tie, garrison cap, clipboard)",
 "COUFFER": "the teenage bat scientist Jack Couffer from the reference (lanky 17-year-old, messy light-brown hair, freckles, rolled-up white shirt sleeves, khaki trousers, canvas satchel)",
 "COMMANDER": "the base commander from the reference (full colonel, broad-shouldered red-faced man in his fifties, grey moustache, khaki 1943 US Army uniform, peaked officer's cap)",
 "DEHAVEN": "the Marine general from the reference (lean grey-haired man in his fifties, sharp features, 1943 US Marine Corps green service uniform with a general's stars)",
 "KING": "the admiral from the reference (stern lean bald-headed man in his sixties, thin lips, 1944 US Navy dark blue uniform with many gold sleeve stripes)",
 "ELEANOR": "the First Lady from the reference (dignified stylised Eleanor Roosevelt in her forties, warm smile, wavy brown hair, 1930s cloche hat, long coat)",
 "BAT": "the small hero bat from the reference (grey-brown fur, tan chest, big rounded pink-brown ears, big worried dark eyes)",
}
RYAN_SET = "standing in his small cosy modern apartment living room with a sofa, shelves and warm lamp light, waist-up, looking at camera"

S = []
def add(id, eng, kf="", mv="", line=None, beat=None, w=1.0, refs=(), sfx="", n=0, reuse=None):
    S.append(dict(id=id, eng=eng, kf=kf, mv=mv, line=line, beat=beat, w=w, refs=list(refs), sfx=sfx, n=n, reuse=reuse))

T = "projects/batbomb-animtest/clips/"
# ---------------------------------------------------------------- 1 COLD OPEN
add("a01", "ltx", line=(1, 0), w=1, kf="Wide establishing shot of a brand-new 1943 US Army auxiliary airfield in the New Mexico desert at midday: fresh wooden control tower, barracks and hangars, a sandy airstrip. In the foreground an Army cameraman in khaki films with a 1940s film camera on a tripod toward a folding table where a man in a white lab coat works. Hard blue sky, distant mesas.",
    mv="The cameraman cranks the film camera, heat shimmer over the sand, a windsock flutters. Slow dolly forward toward the table.")
add("a02", "h3", line=(1, 0), w=1.2, refs=["fieser", "bat"], n=1, sfx="hot desert wind, film camera whirring, a small glass syringe click",
    kf="Medium shot, desert airfield in bright midday sun: {FIESER} at a folding wooden table, holding a large glass-and-steel syringe and injecting a tiny grey capsule clipped to the chest of {BAT} lying sleepy in his palm; a metal tray of crushed ice with five more sleeping bats wearing tiny capsules. New wooden control tower and hangars behind.",
    mv="He presses the plunger into the capsule on the sleepy bat's chest, lifts the syringe away and reaches for the next bat. Slow push in. The capsule stays clipped to the bat's chest.")
add("a03", "ltx", line=(1, 1), refs=["bat"], kf="Close shot of a metal tray of crushed ice on a folding table in hard desert sun: six small grey-brown bats like {BAT}, each with a tiny grey capsule clipped to its chest, blinking awake and opening their wings. Blurred new wooden airfield buildings behind.",
    mv="The bats blink awake in the hot sun, stretch their dark wings and one by one lift off the tray and flap away toward the buildings, keeping their capsules. The camera tilts up to follow them.")
add("a04", "ltx", beat=2.5, refs=["bat"], kf="Wide shot over a brand-new wooden desert airfield at midday: six small bats with tiny capsules flutter across the blue sky toward the barracks, tower and hangars. No people.",
    mv="The six bats flutter and swoop toward the buildings and dive under the eaves and into open windows. The camera pans with them. Only wind.")
add("a05", "ltx", line=(1, 2), refs=[], kf="A long brand-new 1943 wooden army barracks on a sandy desert airfield in midday sun, orange flames bursting out of its windows and eaves, thick black smoke rising into a clear blue sky. The scene is completely deserted: no humans, no figures anywhere.",
    mv="Flames burst out through the windows and climb the wooden walls, black smoke billows, embers fly. Nobody appears at any window or door. Slow push in.")
add("a06", "reuse", line=(1, 2), reuse=T + "t3_tower_ltx_s11.mp4")
add("a07", "ltx", line=(1, 2), kf="Wide shot of a desert airfield: a row of new wooden office buildings and a curved-roof hangar, the nearest office already burning and fire just catching on the hangar roof, black smoke columns. The scene is completely deserted: no humans, no figures anywhere.",
    mv="One after another the office building and then the hangar burst into flame, smoke columns rising in sequence. The camera slowly pans along the row.")
add("a08", "ltx", line=(1, 3), kf="A closed chain-link gate of a 1943 desert airfield, locked with a padlock and chain. A young US Army military policeman in khaki uniform and white helmet stands behind it with arms folded. Outside the gate two red 1940s fire engines with firemen wait. Black smoke rises behind the fence. Exactly three visible people.",
    mv="The gate stays shut and locked and never opens. The guard keeps his arms folded and slowly shakes his head. The firemen throw up their hands. Smoke rolls across the sky. Locked-off camera.")
add("a09", "ltx", beat=1.5, kf="Close shot of a heavy padlock and chain on a chain-link gate, red fire engine bumpers and idling headlights blurred behind it, black smoke in the sky.",
    mv="The padlock sways slightly, the fire engines idle and shudder, smoke drifts. Locked-off.")
add("a10", "ltx", line=(1, 4), kf="Wide shot at golden hour: a single tall column of black smoke rises from a distant desert airfield into an orange sky, empty desert road in the foreground. The scene is completely deserted: no humans, no figures anywhere.",
    mv="The smoke column drifts and widens slowly as the light fades. Very slow push in.")
add("a11", "card", beat=4.0, kf="SIX BATS BURNED DOWN A US AIR BASE", sfx="a single match strike in a quiet room")

# ---------------------------------------------------------------- 2 THE DENTIST
add("b01", "h3", line=(2, 0), refs=["adams"], n=2, sfx="small 1930s dental office, ticking clock, a distant drill whine",
    kf="Medium shot inside a small-town 1930s dental office: {ADAMS} in a white dentist's coat over his suit and bow tie leans over a seated patient (an ordinary man in a dental chair, back to camera), holding a little mirror, grinning. Brass lamp, cabinet of instruments.",
    mv="He peers into the patient's mouth, nods cheerfully and says something friendly. Locked-off camera.")
add("b02", "ltx", line=(2, 1), w=1.2, kf="Wide shot, 1930s countryside airstrip: a small single-engine mail plane swoops low over a field toward two poles with a mail sack hung on a rope between them; a long hook trails below the plane.",
    mv="The plane swoops in low, its trailing hook snags the rope and snatches the mail sack into the air without landing, then climbs away. The camera pans with it.")
add("b03", "h3", line=(2, 1), refs=["adams", "eleanor"], n=2, sfx="small plane engine droning, wind rushing",
    kf="Medium shot in the open two-seat cockpit of a 1930s small plane in flight: {ADAMS} in flying goggles at the controls, and behind him {ELEANOR} holding her hat and smiling, blue sky and clouds around.",
    mv="He grins and points proudly over the side; she laughs and holds her hat in the wind. Gentle camera bob with the plane.")
add("b04", "ltx", line=(2, 2), kf="Wide shot at dusk in the New Mexico desert: a battered 1930s dark sedan drives along a dirt road toward rocky hills, dust trailing, orange sunset.",
    mv="The car drives along the road kicking up dust; the camera tracks alongside slowly.")
add("b05", "ltx", line=(2, 2), kf="Wide shot at dusk: a huge dark cave mouth in a rocky New Mexico hillside, the first bats beginning to stream out into a violet sky, a small crowd of 1940s tourists watching from stone seats in silhouette.",
    mv="More and more bats pour out of the cave and spiral upward; the silhouetted watchers turn their heads to follow. Slow crane up.")
add("b06", "reuse", beat=4.0, reuse=T + "t1_batflight_ltx_s11.mp4")
add("b07", "h3", line=(2, 3), refs=["adams"], n=1, sfx="car interior, crackling 1940s radio static and an indistinct announcer, engine ticking",
    kf="Close-up inside a parked 1930s car at night: {ADAMS} leans toward the glowing dashboard radio, listening; dim green dial light on his face.",
    mv="His cheerful expression slowly falls into shock as he listens. Locked-off camera.")
add("b08", "h3", line=(2, 4), refs=["adams"], n=1, sfx="desert at dusk, crickets, a distant roar of wings",
    kf="Medium shot at dusk: {ADAMS} stands beside his parked car on a desert road, looking up at a sky full of streaming bats.",
    mv="He stares up at the bats, then a slow, delighted smile spreads across his face as an idea arrives. Slow push in.")
add("b09", "h3", line=(2, 5), refs=["adams"], n=1, sfx="desert at night, crickets, pencil scratching on paper",
    kf="Medium shot at night: {ADAMS} leans on the hood of his car under a starry sky with bats crossing the moon, scribbling eagerly in a small notebook with a pencil. He is completely alone: exactly one person in the image.",
    mv="He scribbles fast, taps the pencil on the notebook, looks up at the bats and scribbles again, grinning. Locked-off.")

# ---------------------------------------------------------------- 3 THE LETTER
add("c01", "h3", line=(3, 0), refs=["adams"], n=1, sfx="vintage typewriter keys clacking and a carriage return bell, clock ticking",
    kf="Medium shot inside a cosy 1942 home study at night: {ADAMS} sits at a wooden desk typing a letter on a black 1940s typewriter, a green-shaded desk lamp glowing, a framed photo of a cave on the wall.",
    mv="He types eagerly, pauses with a bright idea, pushes the carriage return and keeps typing. Gentle push in.")
add("c02", "ltx", line=(3, 0), kf="Wide shot of the White House in snowy January 1942 at dusk, warm lit windows, bare trees, a mail van at the gate.",
    mv="Snow falls gently, the mail van drives in through the gate, lights flicker on in the windows. Slow push in.")
add("c03", "ltx", line=(3, 1), refs=["bat"], kf="Inside a vast dark cave: a beam of golden heavenly light falls from a hole in the ceiling onto thousands of small bats hanging from the rock, as if chosen for a destiny. Dust motes glow in the beam.",
    mv="The golden light slowly intensifies, the bats stir and blink in the beam, dust motes swirl. Slow reverent crane down.")
add("c04", "ltx", line=(3, 2), w=1, kf="Night at a cave mouth in the desert: men with lanterns hold long-handled nets as bats stream out; wooden crates stacked nearby.",
    mv="The men sweep the nets through the stream of bats, lanterns swinging. Handheld feel, slow pan.")
add("c05", "ltx", line=(3, 2), w=1, refs=["bat"], kf="Extreme close-up: a small sleepy grey-brown bat like {BAT} in a gloved palm, a tiny grey cylindrical capsule clipped to its chest.",
    mv="The bat blinks sleepily, its ears twitch, the gloved fingers adjust the capsule clip gently. Shallow focus.")
add("c06", "ltx", line=(3, 2), w=1, kf="Before dawn over the sea: a WWII bomber silhouette flies over dark water toward a distant dark coastline, a faint glow on the horizon. The scene is completely deserted: no humans, no figures anywhere.",
    mv="The bomber flies steadily toward the coast, propellers spinning, clouds drifting past. Slow tracking shot.")
add("c07", "ltx", line=(3, 2), w=1.2, refs=["bat"], kf="Dawn close-up under the wooden eaves of an old timber roof (no people anywhere): several small bats with tiny capsules tuck themselves into the dark gaps between the wooden rafters.",
    mv="The bats crawl deeper into the dark gaps and fold their wings; dawn light slowly creeps across the wood. Very slow push in.")
add("c08", "h3", line=(3, 3), refs=["fdr"], n=1, sfx="fountain pen scratching on paper, paper rustle, quiet large office",
    kf="Medium shot in a 1942 presidential office: {FDR} sits at a large wooden desk reading a typed letter, a fountain pen in his hand, flags and tall windows behind.",
    mv="He reads the letter, raises one eyebrow, then writes a short note on a small card with his fountain pen and sets it on the letter. Locked-off camera.")
add("c09", "h3", line=(3, 4), refs=["ryan", "ryan_face"], n=1, kf="Medium waist-up shot: {RYAN} " + RYAN_SET + ", sceptical raised eyebrow.",
    mv="He speaks to camera in disbelief, eyebrows raised, a small open-palm gesture, then a slow blink. Locked-off camera.")
add("c10", "ltx", line=(3, 5), kf="Close-up on a polished wooden presidential desk: a small cream note card lies on top of a typed letter next to a fountain pen, warm lamp light. The scene is completely deserted: no humans, no figures anywhere.",
    mv="Lamp light flickers softly, the pen rolls a little, a hand slides the card into an envelope. Slow push in.")

add("c11", "ltx", line=(3, 6), kf="Dawn at Pearl Harbor, December 1941: damaged grey battleships half-sunk and smoking in the harbour, oil on the water, hills behind. No people visible. The scene is completely deserted: no humans, no figures anywhere.",
    mv="Smoke drifts slowly from the wrecked ships, oil shimmers on the water. Very slow, solemn pan.")
add("c12", "ltx", line=(3, 6), kf="A 1942 US airfield on the California coast at sunset: a single WWII bomber parked at the edge of the runway facing an endless empty Pacific Ocean. The scene is completely deserted: no humans, no figures anywhere.",
    mv="Waves roll in endlessly, the bomber sits still, the sun sinks into the vast empty ocean. Slow push in toward the horizon.")
add("c13", "ltx", line=(3, 6), refs=["bat"], kf="Close-up: a gloved hand holds a tiny grey firebomb capsule next to a small sleepy bat like {BAT} in the other palm, warm lamp light.",
    mv="The hand turns the tiny capsule in the light; the bat blinks sleepily. Shallow focus, slow push in.")

# ---------------------------------------------------------------- 4 BUILDING A BAT AIR FORCE
add("d01", "h3", line=(4, 0), refs=["adams", "couffer"], n=2, sfx="outdoor museum steps, birds, distant 1940s traffic",
    kf="Medium shot on the steps of a 1940s natural history museum in Los Angeles: {ADAMS} shakes hands enthusiastically with {COUFFER}, who looks thrilled.",
    mv="They shake hands vigorously; Adams claps the boy on the shoulder and laughs. Locked-off.")
add("d02", "ltx", line=(4, 0), w=1.2, kf="Wide shot: an odd group of five 1940s men posing beside a battered dark sedan on a desert road: a bookish scientist with glasses, a lanky teenage boy, a weathered lobster fisherman in a cable-knit sweater, a sharp-suited tough guy in a fedora, and a short round cheerful man in a brown suit and bow tie in the middle.",
    mv="They hold the pose awkwardly; the tough guy checks his watch, the fisherman scratches his beard, the round man beams. Slow push in.")
add("d03", "h3", line=(4, 1), refs=["adams"], n=1, sfx="desert wind, car door creak",
    kf="Medium close-up: {ADAMS} beside his car on a desert road, beaming and gesturing proudly at his team off-screen.",
    mv="He gestures proudly, chuckles and gives a thumbs-up. Locked-off camera.")
add("d04", "ltx", line=(4, 2), kf="Wide aerial shot of a battered dark 1930s sedan driving along an empty desert highway through the American Southwest, mesas and long shadows.",
    mv="The car drives along the winding road; the camera follows from above. Late afternoon light.")
add("d05", "ltx", line=(4, 2), kf="Inside a dark abandoned mine tunnel: three 1940s men with flashlights and a lantern peer up at bats hanging from the rocky ceiling.",
    mv="The flashlight beams sweep the ceiling, the bats shift and flutter, the men duck. Slow push in.")
add("d06", "ltx", line=(4, 2), kf="Wide shot at dusk over the Texas hill country: a dark ribbon of millions of bats unrolls out of a cave in a hillside across a pink sky, a tiny parked car and figures far below.",
    mv="The bat ribbon flows and twists endlessly across the sky; the camera slowly cranes up.")
add("d07", "ltx", beat=3.0, kf="Extreme wide shot: an endless river of bats crosses an orange-and-violet Texas sky above rolling hills, the setting sun behind.",
    mv="The river of bats keeps flowing across the sky like smoke. Very slow pan. Only the roar of wings.")
add("d08", "ltx", line=(4, 3), refs=["bat"], kf="Close-up in a 1940s laboratory: a small grey-brown bat like {BAT} sits on the pan of a brass balance scale, a tiny weight on the other pan.",
    mv="The scale wobbles and settles as the bat shifts its feet and looks around. Shallow focus.")
add("d09", "h3", line=(4, 3), refs=["fieser"], n=1, sfx="laboratory glassware clinking, a bubbling flask",
    kf="Medium shot in a 1942 Harvard chemistry laboratory: {FIESER} at a lab bench crowded with flasks and glass tubing, pouring a thick amber jelly from a beaker.",
    mv="He pours carefully, watches the jelly settle, then sets the beaker down with a satisfied nod. Locked-off.")
add("d10", "ltx", line=(4, 4), kf="Extreme close-up cutaway of a tiny firebomb timer: a thin steel wire held taut by a spring-loaded firing pin inside a small transparent capsule, a drop of blue-green liquid on the wire.",
    mv="The liquid slowly eats into the wire, the wire thins and snaps, the firing pin springs forward and a small spark flares. Macro focus.")
add("d11", "h3", line=(4, 4), refs=["fieser"], n=1, sfx="quiet laboratory, a soft click",
    kf="Close-up: {FIESER} holds a tiny grey cylindrical capsule up to the lab window light between finger and thumb, examining it.",
    mv="He turns the capsule slowly in the light, eyes narrowing with satisfaction. Locked-off.")
add("d12", "ltx", line=(4, 5), kf="Inside a 1940s toy factory: workers at a long bench assemble tiny clockwork timers next to boxes of colourful metal construction-set pieces.",
    mv="Hands assemble the little timers; a conveyor carries the finished ones along. Slow pan.")
add("d13", "ltx", line=(4, 5), kf="Inside a 1940s sheet-metal workshop: workers rivet a five-foot olive-drab steel bomb casing on a stand, sparks flying.",
    mv="Rivet guns hammer, sparks fly, a worker turns the casing. Slow push in.")
add("d14", "h3", line=(4, 6), refs=["ryan", "ryan_face"], n=1, kf="Medium waist-up shot: {RYAN} " + RYAN_SET + ", deadpan.",
    mv="He counts on his fingers deadpan as he talks to camera. Locked-off camera.")
add("d15", "ltx", line=(4, 7), kf="Exterior of an old red-brick Harvard university building with ivy and white columns in winter sun, students crossing the yard.",
    mv="Students walk across the yard, a flag stirs in the breeze. Slow tilt up.")
add("d16", "ltx", line=(4, 8), w=1, refs=["bat"], kf="Cutaway view inside a five-foot steel bomb casing: stacked round trays like egg cartons, each niche holding a small sleeping bat with a tiny capsule.",
    mv="The camera glides slowly down past tray after tray of sleeping bats; frost glitters. Smooth vertical move.")
add("d17", "ltx", line=(4, 8), w=1, kf="High above the desert: a WWII bomber releases a five-foot olive-drab casing which falls away; a white parachute begins to deploy.",
    mv="The casing drops from the bomb bay and tumbles, then the parachute snaps open and swings it upright. The camera follows.")
add("d18", "ltx", line=(4, 8), w=1, refs=["bat"], kf="A five-foot olive-drab steel casing hangs under a white parachute against a pale blue sky, its sides falling open as a cloud of small bats spills out. Desert far below.",
    mv="The sides fall away and hundreds of bats pour out and scatter in every direction, wings flickering. The camera drifts down with the casing.")
add("d19", "ltx", line=(4, 8), w=1, refs=["bat"], kf="Inside the dark rafters of an empty wooden attic: small bats with tiny capsules hanging between the beams, a thin wire on one capsule glinting.",
    mv="The bats settle and fold their wings; on one capsule the wire slowly dissolves and a tiny glow begins. Slow push in.")

# ---------------------------------------------------------------- 5 TEST ONE: THE PARTY
add("e01", "ltx", line=(5, 0), kf="Wide establishing shot of a 1943 military airfield on a vast white dry lakebed in the California desert: a B-25 bomber parked, hangars, distant mountains, morning.",
    mv="Heat shimmer, a jeep crosses the field, the windsock flutters. Slow pan.")
add("e02", "h3", line=(5, 0), refs=["fieser"], n=3, sfx="propeller winding down, wind, footsteps on gravel",
    kf="Medium shot: {FIESER} in a suit and overcoat carrying a briefcase steps down from a small military transport plane, followed by two US Army officers in khaki.",
    mv="They walk forward from the plane toward camera, Fieser looking focused. Camera slowly backs away.")
add("e03", "h3", line=(5, 1), refs=["adams", "fieser"], n=6, sfx="dinner party: glasses clinking, laughter, murmured conversation, an old gramophone playing a 1940s dance tune in the room",
    kf="Wide shot of a warm 1943 California living room dinner party: {ADAMS} beams and raises a glass at the head of a table with four guests (two ladies in 1940s dresses and two men in suits), a gramophone on a cabinet; {FIESER} in an overcoat stands frozen in the doorway, horrified.",
    mv="The guests laugh and clink glasses, Adams waves Fieser in cheerfully, Fieser's jaw drops. Locked-off camera.")
add("e04", "h3", line=(5, 2), refs=["ryan", "ryan_face"], n=1, kf="Medium waist-up shot: {RYAN} " + RYAN_SET + ", awkward expression.",
    mv="He speaks to camera, slightly baffled, with an awkward half-smile and a small shrug. Locked-off camera.")
add("e05", "ltx", line=(5, 3), kf="Close-up at a 1940s dinner table: two ladies' hands in gloves clink champagne coupes over candles and a roast, warm light.",
    mv="The glasses clink, candle flames flicker, laughter-shake of the hands. Shallow focus.")
add("e06", "h3", line=(5, 4), refs=["adams"], n=1, sfx="quiet room, a few bats squeaking inside a small cage",
    kf="Medium shot: {ADAMS} holds up a small wire cage containing only a handful of bats, smiling apologetically and shrugging.",
    mv="He shrugs sheepishly, lifts the little cage a bit higher and tilts his head as if explaining. Locked-off.")
add("e07", "ltx", line=(5, 5), kf="Wide shot: an olive-drab WWII B-25 bomber flies low over the New Mexico desert at afternoon, mountains behind.",
    mv="The bomber roars past, propellers spinning; the camera pans to follow.")
add("e08", "ltx", beat=2.5, kf="Dusk at a desert airstrip: a B-25 bomber lands with its bomb bay open showing stacked wooden crates inside.",
    mv="The bomber touches down and rolls, the crates in the bomb bay rattle and shake. Camera tracks alongside.")
add("e09", "ltx", line=(5, 6), kf="Night: the open back of a 1940s refrigerated army truck lit by a work lamp, men in shirtsleeves stacking blocks of ice wrapped in towels around wooden crates, electric fans set up.",
    mv="The men heave ice blocks into place, the fans start spinning, cold mist drifts out. Slow push in.")
add("e10", "ltx", line=(5, 7), w=1, kf="Mid-air above a white dry lakebed: a cardboard bomb casing tumbles from a bomber and comes apart in the wind, pieces flying.",
    mv="The cardboard casing bursts apart in the airstream, pieces fluttering away. The camera falls with it.")
add("e11", "ltx", line=(5, 7), w=1, kf="Inside the open side hatch of a B-25 in flight: two 1940s men in shirtsleeves lean out holding small bats in their hands above the white desert far below.",
    mv="They toss the little bats out of the hatch one after another into the rushing air. Wind buffets their clothes.")
add("e12", "reuse", line=(5, 7), w=1, reuse=T + "t4_jeep_ltx_s11.mp4")
add("e13", "ltx", line=(5, 8), kf="Wide shot of a pale blue sky over the white lakebed: tiny dark specks falling straight down far away, a B-25 climbing higher in the distance.",
    mv="The specks drop straight down out of frame, the bomber climbs away. Locked-off, quiet.")
add("e14", "h3", line=(5, 9), refs=["fieser"], n=1, sfx="desert wind, a jeep engine idling, dust",
    kf="Medium shot: {FIESER} sits on the bumper of an army jeep on the white lakebed, overcoat dusty, rubbing his forehead wearily.",
    mv="He rubs his forehead, exhales and stares at the ground, then looks up at the sky. Locked-off.")
add("e15", "ltx", beat=1.5, kf="Two army jeeps stopped on a white dry lakebed, dust drifting across them, men standing still beside them, wide and quiet.",
    mv="Dust drifts slowly across the scene; nobody moves. Locked-off.")

# ---------------------------------------------------------------- 6 TEST TWO: IT WORKS
add("f01", "ltx", line=(6, 0), kf="Wide establishing shot of a brand-new 1943 auxiliary airfield in the New Mexico desert: fresh wooden control tower, barracks, offices and hangars, nobody around, rocky hills with cave openings behind.",
    mv="A windsock flutters, tumbleweed rolls across the empty airstrip. Slow pan.")
add("f02", "h3", line=(6, 1), refs=["commander"], n=1, sfx="desert wind, flag rope clinking on a pole",
    kf="Medium shot: {COMMANDER} stands proudly in front of the new control tower with hands on hips.",
    mv="He looks up at his tower proudly, then sighs and gives a grudging nod. Locked-off.")
add("f03", "h3", line=(6, 1), refs=["epler", "commander"], n=2, sfx="desert wind, gate rattle",
    kf="Medium shot at the airfield gate: {EPLER} holds up a hand to stop {COMMANDER}, who stands outside the gate looking offended.",
    mv="Epler politely but firmly holds up his hand and shakes his head; the commander's face reddens. Locked-off.")
add("f04", "ltx", line=(6, 2), kf="Close shot under the wing of a B-25 on a desert airstrip: a five-foot olive-drab steel bomb casing hangs on the bomb rack, ground crew checking it.",
    mv="A crewman pats the casing and steps back, the propellers start turning. Slow push in.")
add("f05", "ltx", beat=3.0, refs=["bat"], kf="Wide shot over the New Mexico desert: a white parachute blooms above a falling steel casing, its sides beginning to open.",
    mv="The parachute snaps open, the casing sways, its sides fall away and a cloud of small bats spills out and scatters on the breeze.")
add("f06", "h3", line=(6, 3), refs=["couffer"], n=1, sfx="desert wind, a soft rush of wings far above",
    kf="Medium shot: {COUFFER} stands in the desert scrub shading his eyes, looking up at tiny specks fluttering across the sky.",
    mv="He tracks the specks across the sky with wide excited eyes and points. Locked-off.")
add("f07", "ltx", line=(6, 3), kf="Wide shot: two army jeeps race across rough desert scrub toward a weathered ranch house and red barn, dust plumes behind.",
    mv="The jeeps bounce over the rough ground toward the ranch house; the camera pans with them.")
add("f08", "h3", line=(6, 4), refs=["rancher"], n=1, sfx="porch boards creaking, a screen door, desert wind",
    kf="Medium shot on a shaded wooden ranch porch: {RANCHER} squints out at the yard with a dry, amused look.",
    mv="He squints, raises one bushy eyebrow and gives a slow dry half-smile. Locked-off camera.")
add("f09", "h3", line=(6, 5), refs=["rancher"], n=1, sfx="porch boards creaking, wind",
    kf="Medium close-up on the ranch porch: {RANCHER} places a hand on his heart solemnly.",
    mv="He nods slowly and solemnly with his hand on his heart, eyes steady. Locked-off.")
add("f10", "reuse", line=(6, 6), reuse=T + "t5_rancher_h3_s12.mp4")
add("f11", "reuse", beat=2.0, reuse=T + "t5_rancher_ltx_s12.mp4")
add("f12", "ltx", line=(6, 7), refs=["bat"], kf="Close-up of {BAT} tucked between porch ceiling boards, a tiny grey capsule on its chest, looking down with big eyes.",
    mv="The bat blinks and gives a tiny shrug of its wings. Locked-off.")

# ---------------------------------------------------------------- 7 THE FIRE
add("g01", "h3", line=(7, 0), refs=["adams"], n=1, sfx="desert wind, distant voices",
    kf="Medium shot on the new airfield: {ADAMS} holds up one finger eagerly, asking for one more test.",
    mv="He wags one finger, grins hopefully and nods. Locked-off.")
add("g02", "ltx", line=(7, 0), kf="Medium shot: a US Army Signal Corps cameraman in khaki behind a 1940s film camera on a tripod, a photographer with a press camera beside him, on a desert airfield.",
    mv="The cameraman starts cranking, the photographer raises his camera and snaps. Slow push in.")
add("g03", "reuse", line=(7, 1), reuse=T + "t2_fieser_h3_s12.mp4")
add("g04", "ltx", line=(7, 2), refs=["bat"], kf="Close shot: a metal tray of crushed ice in harsh desert sun, six small bats with tiny capsules waking up, the sun glaring.",
    mv="The bats wake suddenly in the heat and burst up off the tray into the sky. The camera tilts up after them.")
add("g05", "ltx", beat=2.0, refs=["bat"], kf="Wide shot: six small bats fly over the brand-new wooden barracks, tower and hangars of a desert airfield under a blue sky.",
    mv="The bats swoop down and vanish under the eaves and into open windows. The camera pans after them.")
add("g06", "ltx", line=(7, 3), kf="Medium shot of a new wooden barracks window on a desert airfield, quiet, then flames suddenly burst out of it. No people.",
    mv="A flicker of light inside, then flames burst out of the window and race up the wall. Locked-off.")
add("g07", "reuse", beat=3.0, reuse=T + "t3_tower_ltx_s11.mp4")
add("g08", "ltx", line=(7, 4), kf="Wide shot of a desert airfield: new wooden office buildings and a large curved-roof hangar burning one after another, black smoke columns rising. No people.",
    mv="The fire jumps from the offices to the hangar, the hangar roof catches and flames roll along it. Slow pan.")
add("g09", "ltx", line=(7, 4), kf="Close shot: an empty brass fire-hose reel and a red fire bucket hanging uselessly on a wooden wall, the glow of fire flickering on them.",
    mv="Firelight flickers across the empty hose reel; ash drifts past. Locked-off.")
add("g10", "h3", line=(7, 5), refs=["commander"], n=1, sfx="distant fire roar, sirens approaching",
    kf="Medium shot outside a chain-link fence: {COMMANDER} stares in alarm at black smoke rising over his airfield.",
    mv="His eyes widen, he takes off his cap and grips it, aghast. Locked-off.")
add("g11", "ltx", line=(7, 5), kf="Three red 1940s fire engines race along a dusty desert road toward a column of black smoke, firemen holding on.",
    mv="The fire engines race past the camera, dust and gravel flying. Camera pans with them.")
add("g12", "ltx", line=(7, 5), kf="A closed chain-link airfield gate locked with a padlock and chain; a military policeman with arms folded behind it; three red fire engines stopped outside; smoke behind.",
    mv="The gate stays shut and never opens; the guard shakes his head; the firemen gesture angrily. Locked-off.")
add("g13", "h3", line=(7, 6), refs=["epler", "commander"], n=2, sfx="smoke, crackling embers, wind",
    kf="Medium shot in front of smoking ruins: {EPLER} politely asks {COMMANDER}, who stares back speechless, soot on his face.",
    mv="Epler gestures politely toward the ruins; the commander's jaw drops slowly. Locked-off.")
add("g14", "ltx", line=(7, 6), kf="A yellow 1940s bulldozer parked on a desert airfield in front of smoking charred ruins of wooden buildings.",
    mv="Smoke drifts past the bulldozer, its engine coughs to life with a puff of exhaust. Slow push in.")
add("g15", "ltx", line=(7, 7), kf="A dark green 1940s US Army staff car with a general's flag on the fender, parked beside a burning building, flames reflecting on its paint.",
    mv="Flames lick toward the car, its paint blistering, smoke curling over the hood. Slow push in.")
add("g16", "ltx", line=(7, 7), kf="Close-up of a 1940s army typewriter on a desk with a blank sheet of paper in it, an officer's hand pulling the finished page out.",
    mv="The hand pulls the page out of the typewriter with a ratchet and lays it on a pile. Shallow focus.")
add("g17", "h3", beat=4.0, refs=["ryan", "ryan_face"], n=1, kf="Medium waist-up shot: {RYAN} " + RYAN_SET + ", completely blank stare.",
    mv="He stares silently at camera without speaking, completely still except one slow blink. Locked-off camera.")
add("g18", "ltx", line=(7, 8), kf="Wide shot of the smoking charred ruins of a small desert airfield at sunset, only the blackened lattice frame of the control tower still standing. No people.",
    mv="Thin smoke rises from the ruins, embers glow, the sunset light fades. Slow pan.")
add("g19", "ltx", line=(7, 9), kf="Close-up of an army office desk: an officer's hands close a thick file folder and drop it into a drawer.",
    mv="The hands close the folder firmly and slide the drawer shut. Locked-off.")

add("g20", "ltx", line=(7, 10), refs=["bat"], kf="Close-up in the dark gap under the eaves of a new wooden building: a small bat with a tiny capsule crawls deeper into the warm dark wood.",
    mv="The bat squeezes into the dark gap and settles, folding its wings. Slow push in.")
add("g21", "ltx", line=(7, 10), refs=["bat"], kf="Wide shot over a desert landscape: small bats scattering in every direction across the sky from a single point, like a burst of confetti.",
    mv="The bats fly off in all directions at once, impossible to follow. The camera tries to pan after one, then gives up.")

# ---------------------------------------------------------------- 8 SECOND LIFE, AND THE END
add("h01", "h3", line=(8, 0), refs=["dehaven"], n=1, sfx="desert wind, distant crackle of fire",
    kf="Medium shot: {DEHAVEN} stands among observers on a desert airfield, watching black smoke rise, intrigued.",
    mv="He narrows his eyes thoughtfully, then a slow impressed nod. Locked-off.")
add("h02", "ltx", line=(8, 0), kf="Close-up in a 1943 office: a US Navy officer's hand passes a thick file folder stamped with a blank red mark across a desk to a Marine officer's hand.",
    mv="The folder slides across the desk from one hand to the other. Shallow focus.")
add("h03", "ltx", line=(8, 1), kf="Dusk at a cave entrance in the Texas hills: two US Marines with rifles stand guard beside a wire-mesh screen fitted over the cave mouth.",
    mv="The Marines stand still, bats flutter behind the mesh, the light fades. Slow push in.")
add("h04", "h3", line=(8, 1), refs=["adams"], n=1, sfx="quiet office, a briefcase clasp clicking shut",
    kf="Medium shot in a bare office: {ADAMS} packs papers into his worn leather briefcase, his smile gone.",
    mv="He slowly puts the last papers in, closes the briefcase, sighs. Locked-off.")
add("h05", "ltx", line=(8, 2), kf="Wide shot of the snowy Utah desert in December: a row of full-size replica wooden houses with tiled roofs and a replica brick block, built as a test village, grey winter sky. No people.",
    mv="Snow flurries blow across the empty test village. Slow pan.")
add("h06", "ltx", beat=2.5, kf="Close shot under the wooden eaves of a replica test house in winter: small fires starting in the gaps under the roof, no people.",
    mv="Small flames flicker up inside the eaves and grow, smoke curling out. Locked-off.")
add("h07", "ltx", line=(8, 3), kf="Medium shot: a US Army inspector in a winter coat with a clipboard examines scorched rafters inside a replica wooden house.",
    mv="He runs a gloved finger along the charred wood and writes on his clipboard, nodding. Slow push in.")
add("h08", "ltx", line=(8, 3), kf="Inside a 1944 factory warehouse: long rows of olive-drab steel bomb casings and stacked crates ready for production.",
    mv="Workers wheel another casing into the row; the camera dollies slowly along the rows.")
add("h09", "h3", line=(8, 4), refs=["king"], n=1, sfx="quiet office, a rubber stamp thump",
    kf="Medium shot in a 1944 Navy office: {KING} at his desk reads a memo, frowning.",
    mv="He reads, frowns deeper, then stamps the memo firmly and pushes it away. Locked-off.")
add("h10", "ltx", line=(8, 4), kf="Close-up of a rubber stamp slamming down onto a typed document on a desk.",
    mv="The stamp slams down and lifts away; papers flutter. Locked-off.")
add("h11", "ltx", line=(8, 4), kf="Inside a dim warehouse: workers pull canvas tarpaulins over rows of olive-drab steel bomb casings.",
    mv="The tarps billow and settle over the casings, dust rising in the light. Slow pan.")
add("h12", "h3", line=(8, 5), refs=["ryan", "ryan_face"], n=1, kf="Medium waist-up shot: {RYAN} " + RYAN_SET + ", deflated.",
    mv="He speaks to camera, deflated, shoulders dropping, arms spread in disbelief. Locked-off camera.")
add("h13", "ltx", line=(8, 6), kf="Dusk at a desert cave mouth: an old brass pocket watch lies open on a rock in the foreground as the first bats stream out of the cave exactly on time.",
    mv="The watch's second hand ticks, the bats pour out right on cue. Rack focus from the watch to the bats.")
add("h17", "ltx", line=(8, 7), kf="Close-up of a wooden desk: three old books and typed reports lie open side by side with old black-and-white photos of bats and a burnt airfield between them, a magnifying glass on top, warm lamp light. No readable text.",
    mv="A hand slides the magnifying glass from one report to another; lamp light flickers. Slow overhead push in.")
add("h18", "ltx", line=(8, 7), kf="Close-up: a thick file folder passes from a hand in a khaki Army sleeve, to a hand in a dark blue Navy sleeve with gold stripes, to a hand in a green Marine sleeve, across a desk.",
    mv="The folder is handed along from the khaki sleeve to the navy sleeve to the green sleeve. Smooth lateral move.")
add("h19", "ltx", line=(8, 7), kf="Close-up of a large 1940s office wall clock, its second hand moving, a calendar beside it.",
    mv="The second hand sweeps, then the clock hands spin forward fast as calendar pages flip. Locked-off.")
add("h14", "h3", line=(8, 8), refs=["adams"], n=1, sfx="echoing government corridor, footsteps",
    kf="Medium shot in a long 1944 Washington government corridor: {ADAMS} walks toward camera carrying his briefcase, looking baffled.",
    mv="He walks slowly toward camera, scratching his head, briefcase swinging. Camera backs away.")
add("h15", "ltx", line=(8, 9), kf="Night: a remote mesa top with a cluster of plain wartime laboratory buildings and lit windows, searchlights, mountains behind.",
    mv="The lights glow, a searchlight sweeps slowly, clouds drift across the stars. Very slow push in.")
add("h16", "h3", line=(8, 10), refs=["adams"], n=1, sfx="quiet room, briefcase clasp, paper rustle",
    kf="Medium close-up: {ADAMS} opens his worn leather briefcase and lifts out a folded letter, smiling fondly at it.",
    mv="He opens the letter, reads it and his cheerful grin returns. Locked-off.")

# ---------------------------------------------------------------- 9 AFTERMATH
add("i01", "ltx", line=(9, 0), kf="Darkness filled with drifting orange embers floating slowly upward, nothing else visible.",
    mv="The embers drift and slowly fade. Very slow, quiet, respectful.")
add("i02", "ltx", beat=3.0, kf="Near-total darkness with the last few faint embers.",
    mv="The last embers fade to black.")
add("i03", "ltx", line=(9, 1), kf="A 1944 train station platform: a group of men in hats and coats shake hands and part ways, steam from a locomotive.",
    mv="They shake hands and walk off in different directions; steam billows. Slow pan.")
add("i04", "h3", line=(9, 1), refs=["couffer"], n=1, sfx="seaside wind, waves, seagulls, a film camera running",
    kf="Medium shot on a 1970s beach: an older Jack Couffer (now a grown man in his late forties, same face shape as the reference, light-brown hair greying, safari shirt) behind a professional film camera on a tripod, filming seagulls.",
    mv="He films the seagulls, adjusts the lens and smiles. Locked-off.")
add("i05", "ltx", line=(9, 2), kf="Wide shot: a small 1940s single-engine plane flies low over the Arizona desert, a stream of small pellets pouring from a hopper under it.",
    mv="The plane flies along scattering pellets in a long stream. Camera tracks alongside.")
add("i06", "ltx", line=(9, 2), kf="Close-up of dry cracked desert soil where small seed pellets land and scatter; a few tiny green shoots nearby.",
    mv="Pellets patter onto the soil, then time-lapse green grass shoots sprout up. Shallow focus.")
add("i07", "h3", line=(9, 3), refs=["adams"], n=1, sfx="small plane engine, wind, birdsong far below",
    kf="Medium shot in the open cockpit of a small plane over the desert: {ADAMS} in flying goggles looks down over the side, smiling contentedly.",
    mv="He looks down at the green below and smiles warmly. Gentle camera bob with the plane.")
add("i08", "ltx", beat=4.0, refs=["bat"], kf="Dusk at a huge desert cave: {BAT} hangs at the cave mouth looking back at camera while a river of millions of bats spirals up into an orange and violet sunset sky.",
    mv="The bat blinks, turns and drops off the rock and flies out to join the swirling river of bats. The camera holds, then slowly cranes up and fades.")
