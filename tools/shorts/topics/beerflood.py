"""The London Beer Flood, 17 October 1814. Sources: The Times, 19 Oct 1814 (inquest report); Martyn Cornell, "Beer: The Story of
the Pint" (2003) and zythophile.co.uk on the myths; Historic England / Dominion Theatre site history."""
ERA = "gritty early 19th-century Regency London period detail, soot-stained brick, gas-less candlelit streets, 1814 clothing"
M, R = "maya", "benny"
CHARS = {}
SHOTS = [
 dict(id="b01", spk=M, text="In 1814, a street in London was hit by a wave of beer.", eng="ltx", env=True,
      kf="Vertical shot looking down a narrow 1814 London slum street of soot-stained brick houses at dusk: a fast rushing flood of dark "
         "brown liquid beer, waist-deep, pouring down the street toward camera like a river in flood, glossy dark brown water with only a thin tan froth "
         "on its surface, splashing up the walls, barrel staves and a broken cart floating in it.",
      mv="The dark brown river of beer rushes down the street toward camera, rising and splashing up the brick walls and doorways, the "
         "floating barrel staves and cart spin past. Glossy liquid motion like flood water. Wide shot, slow camera retreat. No people."),
 dict(id="b02", spk=M, text="At the Horse Shoe Brewery on Tottenham Court Road, a giant wooden vat of dark porter stood more than twenty feet tall.",
      eng="ltx", env=True,
      kf="Vertical low-angle shot inside a vast dim 1814 brewery storehouse: an enormous round wooden vat more than twenty feet tall, bound with "
         "thick iron hoops, towering up into the shadows of the roof beams, wooden ladders against it, smaller vats behind, shafts of dusty light.",
      mv="Slow tilt up the towering wooden vat from its base to its top, dust drifting in the light shafts, a faint creak of wood. No people."),
 dict(id="b03", spk=M, text="That afternoon, one of the iron hoops holding it together slipped off. A clerk was told not to worry about it.",
      eng="ltx",
      kf="Vertical medium shot in the dim 1814 brewery storehouse: a young clerk in a brown tailcoat, waistcoat and cravat holding a ledger looks up "
         "with concern at a heavy iron hoop that has slipped down the side of the giant wooden vat, while an older foreman in a leather apron "
         "waves a hand dismissively beside him. Exactly two people.",
      mv="The clerk points worriedly up at the slipped iron hoop, the foreman glances at it, shrugs and waves his hand as if to say it is nothing, "
         "and the clerk lowers his ledger uncertainly. Exactly two people; both keep the same face and clothes."),
 dict(id="b04", spk=M, text="About an hour later, the vat burst.", eng="ltx", env=True,
      kf="Vertical close shot of the side of the giant iron-hooped wooden vat in the dim 1814 brewery, its planks bulging outward, thin jets of "
         "dark beer spraying from the cracks between the staves.",
      mv="The wooden staves bulge, the jets of beer spray harder, then the planks burst apart and a massive torrent of dark foaming beer "
         "explodes out toward camera. No people."),
 dict(id="b05", spk=M, text="It smashed open the vats around it, and more than a million litres of beer tore through the brewery's back wall.",
      eng="ltx", env=True,
      kf="Vertical shot from outside of a tall soot-stained brick brewery back wall in 1814 London, the wall bursting outward as a colossal torrent "
         "of dark foaming beer breaks through it, bricks and timber flying. The beer is a LIQUID: dark brown porter like a flood of dark muddy-brown water with creamy tan foam on top, glossy, wet, splashing like a river in flood (not hay, not straw, not fibres).",
      mv="The brick wall collapses outward, a colossal flood of dark foaming beer pours through the gap and surges forward, bricks tumbling "
         "and splashing into it. Slow push back. No people."),
 dict(id="b06", spk=M, text="A wave of beer around fifteen feet high poured into the slum of St Giles.", eng="ltx", env=True,
      kf="Vertical high-angle shot over crooked crowded rooftops of the St Giles slum in 1814 London at dusk, a river of dark foaming beer "
         "flooding through its narrow alleys and yards, washing over carts and fences.",
      mv="The dark foaming flood races through the narrow alleys, swirling around corners, rising up the walls of the houses, debris spinning "
         "on the surface. Slow aerial drift. No people."),
 dict(id="b07", spk=M, text="Whole families there lived in cellars. The beer poured straight in.", eng="ltx", env=True,
      kf="Vertical shot inside a poor 1814 London cellar room lit by one candle: a straw mattress, a small table, a wooden stool, clay pots, "
         "and dark beer pouring down the narrow stone steps from the street above.",
      mv="Dark foaming beer pours down the steps and spreads across the cellar floor, rising fast, the stool tips and floats, the candle "
         "flickers. No people."),
 dict(id="b08", spk=M, tag="sombre", text="Eight people died. Some were mourners at a little boy's wake. One was a fourteen-year-old barmaid, buried when a wall came down.",
      eng="ltx", env=True,
      kf="Vertical quiet shot of a damp 1814 London street at dawn after the flood: a collapsed brick wall, scattered barrel staves, a small "
         "wooden chair on its side, puddles of dark beer reflecting the grey sky, a single extinguished candle on a windowsill.",
      mv="Very slow push in, drops of beer drip from the broken bricks, a thin wisp of mist drifts across the puddles. Silent and still. No people."),
 dict(id="b09", spk=R, tag="disbelief", text="Okay. I thought this was going to be a funny one.", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical waist-up shot of the young man from the reference (thick curly dark brown hair, burnt-orange open hoodie over white t-shirt, "
         "black crossbody strap) standing in a small cosy modern apartment living room, looking at camera, serious and a little taken aback. Exactly one person.",
      mv="The young man speaks quietly to camera, his face falls, he rubs the back of his neck awkwardly. Locked-off camera, waist-up. "
         "Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="b10", spk=M, text="You might have heard that crowds rushed out to drink it. The newspapers of the time don't say that. They describe neighbours digging through the rubble for survivors.",
      eng="ltx",
      kf="Vertical shot of a ruined 1814 London street at night lit by lanterns: a line of working-class men and women in period clothes "
         "lifting bricks and timber from a collapsed house, passing them hand to hand, ankle-deep in dark beer. Exactly five people.",
      mv="The neighbours lift bricks and pass them along the line, one man holds up a lantern and peers into the rubble, a woman calls out. "
         "Exactly five people; everyone keeps the same face and clothes."),
 dict(id="b11", spk=M, text="At the inquest, the jury called it an act of God. The brewery paid nothing, and even got the tax on its lost beer refunded.",
      eng="ltx",
      kf="Vertical shot of a cramped 1814 London inquest room: a row of jurymen in dark tailcoats on a wooden bench, a coroner in a white wig "
         "at a high desk, and a portly brewery owner in a fine coat and top hat looking relieved. Exactly six people.",
      mv="The coroner taps his desk and nods, the jurymen nod together, the portly brewery owner exhales and smugly adjusts his top hat. "
         "Exactly six people; everyone keeps the same face and clothes."),
 dict(id="b12", spk=M, tag="dry", text="The brewery kept going for another hundred years. Today, a theatre stands on the spot. Subscribe for more.",
      eng="ltx", env=True,
      kf="Vertical shot of a grand 1930s-style London theatre facade at night on a busy modern street corner, warm marquee lights glowing, "
         "rain-wet pavement reflecting the lights, a red double-decker bus passing.",
      mv="The marquee lights shimmer and chase, reflections ripple on the wet pavement, the red bus stays small in the far background and drives "
         "away from camera. Slow crane up the facade. Nothing comes close to the camera. No people in focus."),
]
TAIL = 2.6
