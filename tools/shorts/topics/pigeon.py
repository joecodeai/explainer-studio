"""Project Pigeon (1940-1953). Sources: B. F. Skinner, "Pigeons in a Pelican", American Psychologist 15 (1960);
Smithsonian National Museum of American History (Project Pigeon nose cone); Navy Project ORCON 1948-1953."""
ERA = "warm 1940s American period detail"
M, R = "maya", "benny"
CHARS = {
 "skinner": "the psychologist B. F. Skinner in 1943, stylised and respectful: slim man in his late thirties, long thoughtful face, "
            "dark hair receding and neatly combed back, high forehead, sleeves rolled up, white shirt, dark tie, brown waistcoat.",
 "pigeon": "a plump grey rock pigeon, the hero of the story: blue-grey feathers, iridescent green and purple neck, two black wing bars, "
           "bright orange eyes, pink feet, alert curious expression, cartoon-expressive but anatomically a real pigeon.",
}
SHOTS = [
 dict(id="p01", spk=M, text="In 1943, America's most secret missile guidance system was three pigeons.", eng="ltx", refs=["pigeon"],
      kf="Vertical cutaway view inside the cone-shaped nose of a 1940s olive-drab glide missile: exactly THREE small padded compartments in ONE single row side by side, "
         "nothing above or below them, each holding one grey pigeon like the reference in a little cloth jacket, each pigeon facing its own small glowing round screen "
         "showing a tiny ship on the sea. Exactly three pigeons in total, no more. Warm brass fittings, wires, rivets.",
      mv="The three pigeons blink, tilt their heads and peck at their glowing screens in turn, small brass parts twitch with every peck, "
         "the image of the ship on the screens drifts. Slow push in."),
 dict(id="p02", spk=M, text="It started on a train in 1940. A psychologist called B. F. Skinner watched a flock of birds flying alongside him.",
      eng="ltx", refs=["skinner"],
      kf="Vertical shot inside a 1940s railway passenger carriage: the psychologist from the reference sits by the window in profile, "
         "looking out in fascination at a flock of birds flying in formation beside the train over golden autumn farmland. Exactly one person.",
      mv="Outside the window the flock of birds glides and wheels in formation beside the moving train, the landscape streams past. "
         "The man leans closer to the glass, his eyes following the birds. Exactly one person; he keeps the same face and clothes."),
 dict(id="p03", spk=M, text="Birds have amazing eyesight, he thought. Could one of them steer a bomb?", eng="ltx", refs=["skinner"],
      kf="Vertical close-up of the psychologist from the reference in a train seat at golden hour, a sudden idea lighting up his face, "
         "one finger raised, the reflection of flying birds in the window glass. Exactly one person.",
      mv="The man's eyes widen, a slow smile spreads as the idea lands, he taps his finger on his chin and glances back at the window. "
         "Gentle push in. Exactly one person; he keeps the same face."),
 dict(id="p04", spk=M, text="So he trained pigeons to peck at a picture of a target. Every good peck earned a few grains of food.",
      eng="ltx", refs=["pigeon"],
      kf="Vertical shot in a 1940s wooden laboratory: the grey pigeon from the reference stands on a workbench in front of a small upright "
         "card printed with a simple silhouette of a warship, a little metal tray of grain beside it, a lamp lighting the scene.",
      mv="The pigeon pecks sharply at the warship picture, then bobs its head down and eats grain from the little tray, then pecks at the "
         "picture again, quick and precise. Locked-off camera."),
 dict(id="p05", spk=M, text="Then he built a missile around them. A lens in the nose showed the bird the view ahead, and its pecks steered the missile.",
      eng="ltx", refs=["pigeon"],
      kf="Vertical side-profile close-up inside a 1940s missile nose compartment: the grey pigeon from the reference seen from the side, "
         "beak close to a glowing round glass screen on the left that shows a warship on the ocean seen from the air, brass levers and wires around the screen. "
         "Both wings folded neatly against its body.",
      mv="The pigeon pecks at the ship on the glowing screen with quick head bobs, its wings stay folded, each peck nudges the brass levers "
         "and the view on the screen swings until the ship is centred and grows larger. Locked-off camera. The pigeon stays a normal pigeon."),
 dict(id="p06", spk=M, text="In case one pigeon got distracted, there were three of them. They voted.", eng="ltx", refs=["pigeon"],
      kf="Vertical shot of three grey pigeons like the reference side by side in a row of small padded compartments, each in front of its own "
         "glowing round screen showing the same ship, 1940s brass and rivets.",
      mv="Two pigeons peck at the ship on their screens while the middle pigeon looks around distracted, then it notices the others and "
         "quickly pecks too. Locked-off camera, comic timing."),
 dict(id="p07", spk=R, tag="disbelief", text="So the missile was run by a committee. Of pigeons.", eng="h3", refs=["ryan", "ryan_face"],
      kf="Vertical waist-up shot of the young man from the reference (thick curly dark brown hair, burnt-orange open hoodie over white t-shirt, "
         "black crossbody strap) standing in a small cosy modern apartment living room, looking at camera with a sceptical raised eyebrow. Exactly one person.",
      mv="The young man speaks to camera in disbelief, eyebrows raised, a small open-palm gesture, then a slow blink. Locked-off camera, waist-up. "
         "Exactly one person; he keeps the same face, hair and hoodie."),
 dict(id="p08", spk=M, text="The flour company General Mills gave him the top floor of a mill in Minneapolis to train them. Then the government put in twenty-five thousand dollars.",
      eng="ltx", refs=["skinner", "pigeon"],
      kf="Vertical shot on the sunlit top floor of a 1940s brick flour mill: the psychologist from the reference kneels beside a row of wooden "
         "training boxes, holding a grey pigeon like the reference gently in both hands, flour sacks stacked behind, sunbeams through tall windows. Exactly one person.",
      mv="The man gently places the pigeon into a training box, it hops in and starts pecking, he smiles and makes a note. Dust floats in the "
         "sunbeams. Exactly one person; he keeps the same face and clothes."),
 dict(id="p09", spk=M, text="At the big demonstration in Washington, the pigeon tracked its target perfectly. The scientists watching still couldn't take it seriously.",
      eng="ltx", refs=["skinner"],
      kf="Vertical shot of a 1940s wood-panelled meeting room: the psychologist from the reference stands proudly beside a small wooden box with a "
         "glowing round window on a table, while three older scientists in dark suits lean in and stare at it with doubtful, amused faces. Exactly four people.",
      mv="Inside the box's glowing window a pigeon pecks steadily, the psychologist gestures at it proudly, the three scientists exchange "
         "sceptical glances and one smirks and shakes his head. Exactly four people; everyone keeps the same face."),
 dict(id="p10", spk=M, text="In 1944, Project Pigeon was cancelled.", eng="ltx", refs=["skinner", "pigeon"],
      kf="Vertical shot of the psychologist from the reference alone in the empty top-floor mill room at dusk, sitting on a crate, a grey pigeon "
         "like the reference perched on his knee, empty training boxes around them, last orange light through the windows. Exactly one person.",
      mv="The man sighs and slowly strokes the pigeon's back, the pigeon tilts its head and looks up at him. Dust drifts in the fading light. "
         "Exactly one person; he keeps the same face."),
 dict(id="p11", spk=M, text="Then, in 1948, the Navy brought the pigeons back, and kept them until 1953, when electronic guidance finally won.",
      eng="ltx", env=True,
      kf="Vertical shot of a 1950s US Navy laboratory: a row of grey electronic consoles with glowing vacuum tubes, dials and green radar "
         "screens, and on a bench beside them a small empty wooden pigeon training box with its door open.",
      mv="The radar screens sweep, vacuum tubes glow and flicker, dials twitch. A single grey feather drifts down past the empty box. "
         "Slow push in. No people."),
 dict(id="p12", spk=M, text="Skinner kept some of his birds. Years later, he tested them again. They still went straight for the target.",
      eng="ltx", refs=["skinner", "pigeon"],
      kf="Vertical shot of an older version of the psychologist from the reference, now with grey hair, in a 1950s study, crouching to watch "
         "a grey pigeon like the reference in front of a small glowing screen showing a ship. Exactly one person.",
      mv="The pigeon instantly pecks at the ship on the screen, again and again, precise. The older man's face breaks into a delighted grin. "
         "Exactly one person; he keeps the same face."),
 dict(id="p13", spk=M, tag="dry", text="Subscribe for more.", eng="ltx", refs=["pigeon"],
      kf="Vertical shot on the roof edge of a 1940s brick flour mill at sunset over Minneapolis, the grey hero pigeon from the reference "
         "perched on the ledge looking back over its shoulder at camera, the river and city behind.",
      mv="The pigeon bobs its head, blinks at camera, then spreads its wings and launches off the ledge, flying away into the sunset sky. "
         "The camera holds, then slowly tilts up to follow."),
]
TAIL = 3.4
