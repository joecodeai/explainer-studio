"""Builds script.json for 'Ryan Became a Millionaire in Japan (He Didn't)' (hand-written show episode)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from studio import script

N = "narrator"
def L(spk, text, emo="neutral", shot="two_shot", pause=None, act=None, react=None):
    d = {"speaker": spk, "text": text, "emotion": emo, "shot": shot}
    if pause: d["pause_after"] = pause
    if act: d["act"] = act
    if react: d["react"] = react
    return d
def cast(a, b=None): return [{"char": a, "position": "left"}] + ([{"char": b, "position": "right"}] if b else [])
def stage(env, c, lines, tr="cut", music="comedic", beats=(), sfx=()): return {"kind": "stage", "environment": env, "cast": c, "lines": lines, "transition": tr, "music": music, "beats": list(beats), "sfx": list(sfx)}
def card(t, lines, tr="slide", music="upbeat"): return {"kind": "title_card", "title_text": t, "lines": lines, "transition": tr, "music": music}
def hero(p, lines, tr="fade", music="upbeat", beats=()): return {"kind": "hero", "hero_prompt": p, "lines": lines, "transition": tr, "music": music, "beats": list(beats)}
def chart(ch, lines, tr="zoom", music="upbeat", beats=()): return {"kind": "chart", "chart": ch, "lines": lines, "transition": tr, "music": music, "beats": list(beats)}
def mp(m, lines, tr="zoom", music="upbeat", beats=()): return {"kind": "map", "map": m, "lines": lines, "transition": tr, "music": music, "beats": list(beats)}
BM, BC, BK = cast("benny", "maya"), cast("benny", "exchange_clerk"), cast("benny", "ramen_chef")
B, M, CL, CH = "benny", "maya", "exchange_clerk", "ramen_chef"
PL = [{"name": "Washington", "lat": 38.9, "lon": -77.04}, {"name": "Tokyo", "lat": 35.68, "lon": 139.69}]

SCENES = [
 # cold open
 stage("airport_exchange", BC, [
   L(B, "Hi! Hello. Konnichiwa! I'd like to change one thousand dollars, please.", "excited",
     act="the young man on the left slides a few dollar bills across the counter, beaming",
     react="the clerk in the navy uniform on the right smiles politely, mouth closed"),
   L(CL, "Of course. After our fee... that's one hundred and fifty-six thousand yen.", "neutral", pause=0.9,
     act="the clerk in the navy uniform on the right counts a thick stack of banknotes and pushes it toward him",
     react="the young man on the left stares at the stack, his smile slowly freezing, eyes widening, mouth closed"),
   L(B, "...How many thousand?", "surprised", "closeup"),
   L(CL, "One hundred and fifty-six thousand, sir.", "happy")], tr="cut"),
 stage("airport_exchange", BM, [
   L(B, "Maya. Maya! Are you sitting down?", "excited", act="the young man on the left rushes to the woman, clutching a thick stack of banknotes"),
   L(M, "I'm standing, Ryan. We're in an airport.", "sarcastic", "closeup"),
   L(B, "I'm a millionaire.", "excited", "closeup", pause=0.8, react="the woman on the right just looks at him, one eyebrow slowly rising, mouth closed"),
   L(M, "You're a hundred-and-fifty-six-thousand-aire.", "sarcastic", "closeup"),
   L(B, "Okay, but that's so close.", "happy", pause=0.6)]),
 card("Ryan Figures It Out", [L(N, "He's not a millionaire. But he's about to find out why Japan feels so cheap right now.", "neutral")], tr="wipe"),
 # act 1
 hero("A cosy little Tokyo ramen shop entrance on a narrow street at midday, a fabric curtain hanging at the door, steam drifting out, warm light, a few people walking by",
      [L(N, "Day one. First stop: lunch.", "neutral")], tr="fade"),
 stage("ramen_shop", BM, [
   L(M, "You order at the machine. Pick a button, pay, and give the ticket to the chef.", "neutral", act="the woman on the right points toward the side, explaining patiently"),
   L(B, "Which one's the most expensive?", "excited"),
   L(M, "Why is that your first question?", "sarcastic", "closeup"),
   L(B, "Because I'm rich now, Maya. The special. Fifteen hundred yen. Three of them.", "confident", act="the young man on the left proudly presses a button three times with one finger"),
   L(M, "Three?", "confused", "closeup"),
   L(B, "One for you, one for me... and one for confidence.", "confident", "closeup", pause=0.8,
     react="the woman on the right closes her eyes for a moment, holding back a smile, mouth closed")]),
 stage("ramen_shop", BK, [
   L(CH, "Three specials. Enjoy.", "happy", act="the chef in the white headband on the right sets steaming bowls on the counter and smiles"),
   L(B, "Thank you so much. This is for you.", "happy", act="the young man on the left slides a few coins across the counter toward the chef"),
   L(CH, "Ah, no, no. Thank you, but no.", "surprised", act="the chef on the right gently slides the coins back with a polite little bow"),
   L(B, "No, please. I insist.", "confident", act="the young man on the left slides the coins back again, smiling"),
   L(CH, "Really. It's okay.", "happy", pause=0.7, act="the chef on the right slides the coins back once more, still smiling, and bows",
     react="the young man on the left freezes, confused, mouth closed")]),
 stage("ramen_shop", BM, [
   L(B, "Maya, he won't take my money.", "confused"),
   L(M, "You don't tip in Japan. Good service is just... the service. He's not being modest, Ryan. He's being polite.", "neutral"),
   L(B, "So I just insulted a man... with coins.", "worried", "closeup", pause=0.5),
   L(M, "Very politely, though.", "sarcastic", "closeup")]),
 stage("ramen_shop", BM, [
   L(B, "Okay. Fifteen hundred yen for this bowl. In real money, that's...", "thinking" if False else "confused", act="the young man on the left looks down at his phone, doing maths"),
   L(M, "About nine dollars and forty cents.", "neutral"),
   L(B, "Nine forty? For this? Back home, I'd pay twice that. At least.", "surprised", "closeup"),
   L(M, "Because right now, one dollar buys you almost a hundred and sixty yen.", "neutral")]),
 mp({"label": "Your dollar buys more yen", "countries": ["United States", "Japan"], "places": PL, "routes": []},
    [L(N, "This month, the dollar climbed as high as a hundred and fifty-nine point nine four yen, its strongest against the yen in more than two months. Traders treat one-sixty as a line in the sand.", "neutral", "wide")],
    beats=[{"at_word": "climbed", "type": "number", "text": "¥159.94 per $1"}]),
 stage("ramen_shop", BM, [
   L(B, "So Japan is on sale.", "excited"),
   L(M, "For you.", "sarcastic", "closeup"),
   L(B, "For me. Specifically.", "confident"),
   L(M, "For anyone holding dollars. And a lot of people noticed.", "neutral")]),
 chart({"mode": "stats", "title": "Visitors to Japan", "items": [
        {"value": "42.7 million", "label": "foreign visitors in 2025, a record"},
        {"value": "¥9.5 trillion", "label": "spent by visitors in 2025, a record"},
        {"value": "¥7.06 trillion", "label": "spent Jan–Sep 2026, another record"}]},
       [L(N, "Last year, a record forty-two point seven million foreign visitors came to Japan, and spent a record nine and a half trillion yen. This year, they'd already spent over seven trillion by September.", "neutral", "detail")]),
 stage("ramen_shop", BM, [
   L(B, "So I'm part of a trend.", "happy"),
   L(M, "You're part of a statistic.", "sarcastic", "closeup"),
   L(B, "A record-breaking statistic.", "confident", "closeup", pause=0.6)]),
 # act 2
 card("Why So Cheap?", [L(N, "Which raises the question Ryan has been avoiding. Why is the yen so cheap?", "neutral")]),
 hero("A quiet Tokyo side street at night, a brightly lit convenience store glowing warmly, a row of vending machines, light rain reflections on the pavement",
      [L(N, "That night, outside a convenience store, Ryan came up with a theory.", "neutral")]),
 stage("konbini_street", BM, [
   L(B, "I figured it out. Their money is too pretty. So they printed too much of it.", "confident", act="the young man on the left holds up a banknote, explaining proudly"),
   L(M, "That's not it.", "sarcastic", "closeup"),
   L(B, "Maya, it has art on it. Who wouldn't print more of that?", "confused"),
   L(M, "Okay. Hold these.", "neutral", act="the woman on the right hands him two paper coffee cups")]),
 stage("konbini_street", BM, [
   L(M, "This cup is America. This one is Japan. Your money goes wherever it earns more interest.", "neutral", act="the woman on the right taps one cup, then the other"),
   L(B, "And America pays more.", "confused", act="the young man on the left holds two coffee cups and looks from one to the other"),
   L(M, "A lot more. America's central bank rate is around four percent. Japan's is one and a quarter.", "neutral"),
   L(B, "Four... versus one and a quarter.", "confused", pause=0.5, act="the young man on the left weighs the two cups in his hands, frowning"),
   L(M, "If you were money, which cup would you jump into?", "sarcastic", "closeup"),
   L(B, "The four one. Obviously.", "confident", "closeup", pause=0.5),
   L(M, "That's exactly what money does. And the four might go even higher.", "neutral"),
   L(B, "Why would it go higher?", "surprised", "closeup")]),
 chart({"mode": "stats", "title": "US inflation surprise", "items": [
        {"value": "0.4%", "label": "US price rise in October (forecast 0.3%)"},
        {"value": "100%", "label": "market odds of a December Fed rate hike (CME FedWatch)"}]},
       [L(N, "America only started raising rates again in September, its first hike in more than three years. Then US prices rose zero point four percent in October, hotter than the zero point three that was expected. Markets now see a one hundred percent chance that the Federal Reserve raises rates in December.", "neutral", "detail")]),
 mp({"label": "Money chases higher rates", "countries": ["United States", "Japan"], "places": PL,
     "routes": [{"from": "Tokyo", "to": "Washington", "via": [], "label": "money", "icon": "money", "blocked": False}]},
    [L(N, "So money flows toward the higher rates, and the dollar index hit a nineteen-month high.", "neutral", "wide")],
    beats=[{"at_word": "nineteen-month", "type": "label", "text": "19-MONTH HIGH"}]),
 stage("konbini_street", BM, [
   L(B, "So money goes where it's treated best.", "thinking" if False else "confident"),
   L(M, "Like you, and the bank that gave you a free pen.", "sarcastic"),
   L(B, "It was a really good pen.", "confident", "closeup", pause=0.6),
   L(M, "I know. You've shown me. Twice.", "sarcastic", "closeup")]),
 # act 3
 card("Tokyo Strikes Back", [L(N, "Japan, meanwhile, was not enjoying the sale.", "sarcastic")]),
 stage("hotel_room", BM, [
   L(B, "Maya. The guy on TV looks upset.", "worried", act="the young man on the left points toward the side of the room, worried"),
   L(M, "That's Atsushi Mimura. He's Japan's top currency official.", "neutral")]),
 hero("A Japanese government ministry building in Tokyo at dusk, office windows glowing, a tense calm mood, dramatic sky",
      [L(N, "This week, he warned that the yen was moving too fast, and said it was too early to forget what happened this summer.", "worried")],
      music="tense", beats=[{"at_word": "fast", "type": "keyword", "text": "TOO FAST"}]),
 stage("hotel_room", BM, [
   L(B, "Why say it's too fast? Why not just say stop?", "confused"),
   L(M, "Because Tokyo has a script. First, they say the moves are too rapid. Then they say they're watching closely. Then... they act.", "neutral"),
   L(B, "So it's like my mom counting to three.", "confused", "closeup"),
   L(M, "Exactly like your mom. With trillions of yen.", "sarcastic", "closeup", pause=0.5)], music="tense"),
 stage("hotel_room", BM, [
   L(M, "And it kind of works. Right after he spoke, the yen bounced back a little.", "neutral"),
   L(B, "He just talked, and it moved?", "surprised", "closeup"),
   L(M, "It's called verbal intervention.", "neutral"),
   L(B, "I do that. With my plants.", "confident", "closeup", pause=0.7, react="the woman on the right stares at him, then slowly shakes her head, mouth closed")]),
 stage("hotel_room", BM, [
   L(B, "Okay. So what happened this summer?", "surprised"),
   L(M, "Twice this year, the yen getting close to one-sixty came right before the real thing. Japan fought back. The government sold dollars and bought yen. A lot of yen.", "neutral"),
   L(B, "By itself?", "confused"),
   L(M, "Not always. One of those operations was done together with the United States.", "neutral"),
   L(B, "America helped? That's nice.", "happy"),
   L(M, "Very neighbourly.", "sarcastic", "closeup"),
   L(B, "So how much is a lot?", "confused")], music="tense"),
 chart({"mode": "stats", "title": "Japan defending the yen, summer 2026", "items": [
        {"value": "¥15.4 trillion", "label": "spent on July 30, July 31 and August 3"},
        {"value": "¥7.98 trillion", "label": "on July 30 alone, a one-day record"},
        {"value": "¥27 trillion+", "label": "total this year (old record: about ¥15 trillion, 2024)"}]},
       [L(N, "Over three days, fifteen point four trillion yen. July thirtieth alone was almost eight trillion, a one-day record. That pushed this year's total past twenty-seven trillion. The old record, set in 2024, was about fifteen.", "neutral", "detail")], music="tense"),
 stage("hotel_room", BM, [
   L(B, "Twenty-seven trillion?", "surprised", "closeup", pause=0.5),
   L(M, "And within a month, the yen slid back toward one-sixty anyway.", "neutral"),
   L(B, "They spent twenty-seven trillion, and it just... came back?", "confused"),
   L(M, "Markets don't send thank-you notes.", "sarcastic", "closeup")], music="tense"),
 stage("hotel_room", BM, [
   L(B, "Wait. If they do it again, my sale ends.", "worried"),
   L(M, "Maybe. For a while. Nobody knows when. Not even Tokyo.", "neutral"),
   L(B, "Then I have to spend everything. Tonight.", "excited", "closeup"),
   L(M, "Ryan. That is not the lesson.", "sarcastic", "closeup"),
   L(B, "It's a lesson.", "confident", pause=0.5, act="the young man on the left grabs his jacket and turns to leave")]),
 hero("A colourful Tokyo souvenir shop at night packed with shelves of small lucky cat figurines, one gigantic golden lucky cat statue in the middle with its paw raised",
      [L(N, "He did not spend everything. He spent most of it. On one thing.", "sarcastic")], beats=[{"at_word": "thing", "type": "keyword", "text": "ONE THING"}]),
 stage("souvenir_shop", BM, [
   L(B, "Maya. Meet Lucky.", "happy", act="the young man on the left proudly gestures at something big beside him, grinning"),
   L(M, "Ryan. That cat is taller than you.", "surprised", "closeup"),
   L(B, "It waves. All the time. That's luck, Maya.", "confident"),
   L(M, "That's a battery.", "sarcastic", "closeup", pause=0.6)]),
 stage("hotel_room", BM, [
   L(B, "He fits. Mostly.", "happy", act="the young man on the left gestures proudly toward the window"),
   L(M, "He's blocking the window, Ryan.", "sarcastic"),
   L(B, "He's protecting us.", "confident"),
   L(M, "From what?", "confused", "closeup"),
   L(B, "Bad luck. And... sunlight.", "confident", "closeup", pause=0.6)]),
 # act 4
 card("The Other Side", [L(N, "The next day, Ryan went back to the ramen shop. This time, he listened.", "neutral")], music="sad"),
 stage("ramen_shop", BK, [
   L(B, "Can I ask you something? Is the cheap yen good for you?", "neutral"),
   L(CH, "For tourists, maybe. For me, everything from overseas costs more. Fuel. Flour. Even some of the pork.", "worried",
     act="the chef in the white headband on the right sighs gently and explains, wiping the counter"),
   L(B, "Oh.", "worried", "closeup", pause=0.6)], music="sad"),
 chart({"mode": "stats", "title": "The other side of a weak yen", "items": [
        {"value": "7.1%", "label": "rise in Japan's wholesale prices, October"},
        {"value": "Q3", "label": "Japan's economy shrank, first drop in four quarters"},
        {"value": "8% → 1%", "label": "food tax cut being debated by lawmakers"}]},
       [L(N, "A weak yen makes imported fuel, food and raw materials more expensive. Japan's wholesale prices rose seven point one percent in October. The economy shrank last quarter, its first drop in four quarters. Lawmakers are even debating cutting the tax on food from eight percent to one.", "neutral", "detail")], music="sad"),
 stage("ramen_shop", BM, [
   L(B, "So my sale... is his price rise.", "sad"),
   L(M, "...Yeah. That's exactly it.", "surprised", pause=0.6),
   L(B, "And if Japan raises interest rates, money comes back, and the yen gets stronger. My sale ends. But his flour gets cheaper.", "thinking" if False else "confident"),
   L(M, "Ryan. That's actually right.", "surprised", "closeup", pause=0.7, react="the young man on the left slowly breaks into a proud smile, mouth closed"),
   L(B, "I know things.", "confident", "closeup"),
   L(B, "So is anyone in Japan winning?", "confused"),
   L(M, "Some exporters. Companies that sell abroad earn dollars, and those dollars turn into more yen back home.", "neutral"),
   L(B, "So they're like me at the airport.", "happy"),
   L(M, "Except their millions are real.", "sarcastic", "closeup")], music="upbeat"),
 chart({"mode": "timeline", "title": "What to watch", "items": [
        {"value": "Dec 9", "label": "US Fed decides: markets price a hike at 100%"},
        {"value": "Dec 17–18", "label": "Bank of Japan meets: some expect 1.25% → 1.5%"}]},
       [L(N, "So, what to watch. On December ninth, the Federal Reserve decides whether the gap gets wider. On December seventeenth and eighteenth, the Bank of Japan meets, and some analysts expect it to raise its rate from one and a quarter to one and a half percent. That gap is what decides where the yen goes next.", "neutral", "detail")]),
 # ending
 card("Going Home", [L(N, "Five days later.", "neutral")], tr="wipe"),
 stage("airport_exchange", BC, [
   L(B, "Hi again! I'd like to change my yen back to dollars, please.", "happy", act="the young man on the left places a few coins on the counter"),
   L(CL, "Of course. How much?", "neutral"),
   L(B, "Four hundred yen. I also have a cat, but I'm keeping him.", "confident", pause=0.6, react="the clerk on the right blinks politely, mouth closed"),
   L(CL, "That's about two dollars, sir.", "neutral")]),
 stage("airport_exchange", BM, [
   L(B, "I was a millionaire for five days.", "sad"),
   L(M, "A hundred-and-fifty-six-thousand-aire.", "sarcastic", "closeup"),
   L(B, "Still so close.", "happy", "closeup", pause=0.6),
   L(M, "And you learned something.", "neutral"),
   L(B, "I did. Weak yen, cheap Japan, expensive flour for the chef. And never buy a cat that's taller than you.", "confident")]),
 stage("airport_exchange", BM, [
   L(B, "Okay, real question. What would you buy first with a hundred and fifty-six thousand yen? Tell me in the comments. I need ideas for next time.", "excited", "closeup"),
   L(M, "There's no next time.", "sarcastic", "closeup"),
   L(B, "Wait. Why is my phone buzzing?", "confused", act="the young man on the left looks down at his buzzing phone"),
   L(B, "Maya... what's a foreign transaction fee?", "worried", pause=0.8),
   L(M, "...Next week, Ryan.", "sarcastic", "closeup")]),
 card("See You Next Time", [L(N, "Thanks for watching. Subscribe, because Ryan's credit card statement is on its way.", "happy")], tr="fade"),
]

ENVS = [
 {"id": "airport_exchange", "prompt": "a bright modern Tokyo airport arrivals hall with a currency exchange counter along the back, glass partitions, travellers' luggage trolleys at the far edges, soft daylight", "ambience": "airport hall murmur, distant announcements"},
 {"id": "ramen_shop", "prompt": "a cosy small Tokyo ramen shop interior: wooden counter along the back wall, steam rising from big pots, paper lanterns, a ticket vending machine at the far left edge, warm light", "ambience": "ramen shop bustle, broth bubbling, quiet slurping"},
 {"id": "konbini_street", "prompt": "a quiet Tokyo street at night outside a brightly lit convenience store, vending machines at the far edges, wet pavement reflecting warm lights", "ambience": "quiet city night, distant traffic, light rain"},
 {"id": "hotel_room", "prompt": "a compact neat Tokyo hotel room at night: bed along the back wall, a TV glowing on the side wall, city lights through the window, warm lamp light", "ambience": "quiet hotel room hum, faint TV"},
 {"id": "souvenir_shop", "prompt": "a colourful Tokyo souvenir shop at night: shelves of lucky cat figurines and toys along the back wall, a giant golden lucky cat statue at the far right edge, warm bright light", "ambience": "shop chatter, soft chimes"},
]
CHARS = [
 {"id": "exchange_clerk", "name": "Clerk", "role": "", "real_person": False, "tag": "the clerk in the navy uniform",
  "look": "a polite young Japanese woman in her twenties, neat dark hair in a bun, navy blue airline-style uniform with a white blouse and small scarf, friendly professional smile",
  "voice": "A polite young Japanese woman in her twenties, soft, clear and professional, gentle Japanese accent in English, calm and friendly."},
 {"id": "ramen_chef", "name": "Chef", "role": "Ramen chef", "real_person": False, "tag": "the chef in the white headband",
  "look": "a kind Japanese man in his fifties, short greying hair, white headband, dark navy cook's jacket, white apron, warm crinkly-eyed smile",
  "voice": "A kind Japanese man in his fifties, warm, gentle and slightly gravelly, Japanese accent in English, calm unhurried pace."},
]

# outfits by story day: day 1 = signature outfits; that night = "night"; the last days = "home"
NIGHT_ENVS, HOME_FROM = {"konbini_street", "hotel_room", "souvenir_shop"}, "The Other Side"

def dress(scenes):
    home = False
    for s in scenes:
        if s.get("kind") == "title_card" and s.get("title_text") == HOME_FROM: home = True
        for c in s.get("cast", []):
            if c["char"] in ("benny", "maya"):
                o = ({"benny": "luckycat", "maya": "denim"}[c["char"]] if home else ("evening" if s.get("environment") in NIGHT_ENVS else None))
                if o: c["outfit"] = o
    return scenes

def build(proj, scenes=SCENES, title="Ryan Became a Millionaire in Japan (He Didn't)"):
    sh = script.load_show()
    scenes = dress(json.loads(json.dumps(scenes)))
    research = json.load(open(os.path.join(proj, "research.json")))
    d = {"title": title, "thumbnail_text": "I'M RICH?", "description":
         "Ryan changes $1,000 at a Tokyo airport and thinks he's a millionaire. Maya walks him through why the yen is so cheap, why Japan "
         "spent a record ¥27 trillion defending it, and who pays the price for his ramen discount.",
         "characters": [{"id": c["id"], "name": c["name"], "look": c["look"], "voice": c["voice"], "role": c.get("role", ""), "real_person": False} for c in sh["cast"]] + CHARS,
         "environments": ENVS, "scenes": json.loads(json.dumps(scenes)), "sources": [s["url"] for s in research["sources"]], "show": sh["name"]}
    d = script.apply_show(script.validate(d), sh)
    for c in d["characters"]:                                  # keep the guests' short tags (validate drops unknown fields? keep explicitly)
        g = next((x for x in CHARS if x["id"] == c["id"]), None)
        if g: c["tag"] = g["tag"]
        f = next((x for x in sh["cast"] if x["id"] == c["id"]), None)
        if f and f.get("tag"): c["tag"] = f["tag"]
    probs = [p for p in d["_problems"] if "environment as the previous" not in p]
    words = sum(len(s["narration"].split()) for s in d["scenes"])
    json.dump({k: v for k, v in d.items() if not k.startswith("_")}, open(os.path.join(proj, "script.json"), "w"), indent=1, ensure_ascii=False)
    return probs, words, len(d["scenes"])

if __name__ == "__main__":
    print(build(sys.argv[1]))
