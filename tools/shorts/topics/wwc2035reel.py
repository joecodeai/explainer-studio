"""Reel / Short for the 2035 Women's World Cup video: the whole story in ~75 s, native 9:16. Same facts and sources as topics/wwc2035.py."""
from topics.wwc2035 import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
ERA = "football"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="r01", spk=M, eng="ltx", env=True,
      text="FIFA has just confirmed that the UK will host the 2035 Women's World Cup.",
      kf="A shiny golden football trophy cup on a navy podium under a spotlight, a simple soft green outline map of Great Britain and "
         "Ireland glowing behind it, colourful confetti in the air.",
      mv="Golden confetti drifts down slowly, the flags wave gently, the trophy gleams. Static camera."),
 dict(id="r02", spk=M, eng="still", mv="in", sfx="empty stadium, wind, a gate creaking", refs=["fa"],
      text="Which is a big moment for a country that once kept women off its football grounds. For fifty years.",
      kf="The man from the reference standing in front of the closed iron gates of a big football stadium, swinging a large padlock shut, "
         "looking pleased. Exactly one person."),
 dict(id="r03", spk=M, eng="ltx", refs=["dkl"],
      text="In 1917, women at a munitions factory in Preston started playing football on their lunch breaks. Then they beat the factory's men.",
      kf="The woman from the reference, wearing khaki overalls instead of her kit, kicking an old leather football across a cobbled factory yard, "
         "red brick walls and a tall chimney behind. Exactly one person.",
      mv="She dribbles the ball forward and kicks it, the ball rolls away, she runs after it smiling. " + P1),
 dict(id="r04", spk=M, eng="card", card=dict(big="53,000", small="BOXING DAY 1920", bg="#3C5A50", accent="#F2C14E"),
      sfx="huge football crowd roaring in an old stadium",
      text="By Boxing Day 1920, the Dick, Kerr Ladies were drawing fifty-three thousand people to Goodison Park."),
 dict(id="r05", spk=M, eng="still", mv="in", refs=["fa"], sfx="quiet wood-panelled room, clock ticking",
      text="A year later, the FA declared football quite unsuitable for females, and told its clubs not to let women use their grounds.",
      kf="The man from the reference sitting at the head of a long polished table in a dark wood-panelled committee room, fingers steepled, "
         "staring seriously. Exactly one person."),
 dict(id="r06", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So they were banned for selling too many tickets.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, arms folded, standing in a simple flat "
         "cosy living room with a teal wall and a plant, looking at camera with a flat, unimpressed expression. Exactly one person.",
      mv="The young man speaks to camera flatly, unimpressed, arms folded, then raises one eyebrow. Static camera, waist-up. Exactly one person; "
         "he keeps the same face, hair and hoodie."),
 dict(id="r07", spk=M, eng="card", card=dict(big="1971", small="BAN LIFTED", bg="#5A3C3C", accent="#F2C14E"),
      sfx="quiet office, a rubber stamp thump",
      text="The ban stayed until 1971."),
 dict(id="r08", spk=M, eng="still", mv="out", refs=["fa"], sfx="a long scroll unrolling, paper rustling",
      text="FIFA's first Women's World Cup came in 1991, with eighty-minute matches, and officially it wasn't even called a World Cup. It was the First FIFA World Championship for Women's Football for the M and M's Cup.",
      kf="A smartly dressed official holding the top of an absurdly long blank paper scroll that unrolls down a grand staircase and across the "
         "floor. Exactly one person."),
 dict(id="r09", spk=M, eng="still", sfx="big stadium crowd cheering by the sea",
      text="In 2023, almost two million people went to the World Cup. England are now two-time European champions.",
      kf="A modern stadium by a harbour at sunset with a curved white roof, every seat packed with a colourful crowd of tiny fans waving scarves, an empty green pitch in front. No ball, nobody on the pitch.",
      mv_ltx="The crowd waves scarves and flags, the sunset sky glows and the sea sparkles. Static camera."),
 dict(id="r10", spk=M, eng="card", card=dict(big="48", small="TEAMS IN 2035", bg="#2E4A62", accent="#F2C14E"),
      sfx="stadium crowd rumble",
      text="And 2035 will have forty-eight teams, a hundred and four matches, and around four and a half million tickets."),
 dict(id="r11", spk=M, eng="still", sfx="sunny park, kids playing in the distance, birds", refs=["girl"],
      text="Most of the players who'll star in it are kids right now, in a park somewhere.",
      kf="The girl from the reference in a sunny park, about to kick a football towards a goal made of two piled-up jumpers on the grass, "
         "trees behind. Exactly one person.",
      mv_ltx="The girl runs up and kicks the ball between the two jumpers, then throws her arms up in celebration. " + P1),
 dict(id="r12", spk=M, eng="ltx",
      text="In 1921, women's football should not be encouraged. In 2035, the whole world is coming to watch it. The full story is on our channel.",
      kf="A huge modern stadium at night with a tall white arch over it, packed with a giant crowd waving flags of many colours, bright floodlights, "
         "fireworks above, an empty green pitch. Nobody on the pitch.",
      mv="Fireworks burst over the stadium, the crowd waves flags, the floodlights sparkle. Static camera."),
]
TAIL = 2.4
