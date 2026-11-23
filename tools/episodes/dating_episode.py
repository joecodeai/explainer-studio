"""Builds script.json for 'Why Ryan Keeps Getting Ghosted (The Algorithm Knows)' — a Ryan & Maya show episode about dating apps.

Facts used (all in research.json):
- Pew Research Center (Feb 2023, survey Jul 2022): 30% of US adults have used a dating site/app; 53% of under-30s; about 1 in 10
  partnered adults met their current partner through one; 53% of users describe the experience as positive, 46% negative.
- Rosenfeld, Thomas & Hausen (PNAS 2019): meeting online became the most common way US couples meet.
- Tinder once ranked users with an Elo score borrowed from chess; Tinder said in 2019 it no longer relies on it (HDSR, Sharabi 2022).
- Hinge says its recommendations use the Gale-Shapley "stable matching" algorithm (1962); Shapley and Roth won the 2012 Nobel
  Memorial Prize in economics for this line of work (HDSR 2022).
- Dating algorithms learn from behaviour: who you like and who likes you back (collaborative filtering, HDSR 2022).
- Iyengar & Lepper (2000) jam study: a display of 24 jams drew more shoppers, but only 3% bought; with 6 jams, 30% bought.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from yen_episode import L, cast, stage, card, hero, chart, mp
from studio import script

N, R, M, Z = "narrator", "benny", "maya", "zoe"
RM, RZ = cast(R, M), cast(R, Z)

SCENES = [
 # cold open: Ryan swiping right on everyone
 stage("flat", RM, [
   L(R, "Right. Right. Right. Right. Right.", "excited", act="the young man on the left sits forward, swiping fast on his phone with his thumb, totally focused",
     react="the woman on the right watches him, slowly lowering her coffee cup, mouth closed"),
   L(M, "Ryan. Are you even looking at them?", "sarcastic"),
   L(R, "No time. It's a numbers game, Maya. Two hundred right swipes today. Zero matches. But statistically, it's coming.", "confident",
     pause=0.7, react="the woman on the right stares at him in silence, one eyebrow rising, mouth closed"),
   L(M, "Statistically... you might be the reason.", "sarcastic", "closeup")], tr="cut"),
 card("Ryan Figures It Out", [L(N, "He thinks dating apps are a numbers game. They're not. They're watching.", "neutral")], tr="wipe"),
 # act 1: is it just him?
 stage("flat", RM, [
   L(R, "Okay, but how does this affect me? Is it just me? Is everyone this unlucky?", "worried"),
   L(M, "You're not alone. You're just very... dedicated.", "sarcastic"),
   L(R, "Thank you.", "happy", pause=0.5),
   L(M, "That wasn't a compliment.", "sarcastic", "closeup")]),
 chart({"mode": "stats", "title": "Online dating in the US (Pew Research, 2023)", "items": [
        {"value": "30%", "label": "of US adults have used a dating site or app"},
        {"value": "53%", "label": "of adults under 30 have"},
        {"value": "1 in 10", "label": "partnered adults met their partner on one"}]},
       [L(N, "According to Pew Research, three in ten American adults have used a dating site or app, and more than half of people under thirty. About one in ten partnered adults met their partner that way.", "neutral", "detail")]),
 stage("flat", RM, [
   L(R, "One in ten! So it works.", "excited"),
   L(M, "For some people. Users are split almost down the middle: fifty-three percent say it's been positive, forty-six percent say negative.", "neutral"),
   L(R, "So it's a coin flip.", "confused"),
   L(M, "A coin flip... where the coin is also judging you.", "sarcastic", "closeup", pause=0.6)]),
 # act 2: the algorithm
 hero("A cosy neighbourhood coffee shop in the afternoon, warm light through big windows, a few empty tables, steam rising from cups",
      [L(N, "The next day, Maya took Ryan for coffee. And a lesson.", "neutral")]),
 stage("coffee_shop", RM, [
   L(M, "Here's the thing. The app isn't just showing you random people. It's learning from everything you do.", "neutral",
     act="the woman on the right leans in and explains, tapping the table lightly"),
   L(R, "Like what?", "confused"),
   L(M, "Who you like. Who likes you back. And you just told it you like... everyone.", "sarcastic"),
   L(R, "I'm open-minded.", "confident", pause=0.6),
   L(M, "You're a spam account with hair.", "sarcastic", "closeup")]),
 stage("coffee_shop", RM, [
   L(M, "Tinder used to rank people with something called an Elo score.", "neutral"),
   L(R, "Elo? Like the band?", "confused"),
   L(M, "Like chess. The same system that ranks chess players.", "neutral"),
   L(R, "So if a really popular person swipes right on me... that's like beating a grandmaster?", "surprised"),
   L(M, "Exactly. Tinder says it doesn't rely on that score anymore. But the idea stuck.", "neutral")]),
 chart({"mode": "timeline", "title": "How the apps rank you", "items": [
        {"value": "Elo", "label": "chess-style score Tinder once used; it says it retired it in 2019"},
        {"value": "Gale-Shapley", "label": "1962 'stable matching' maths Hinge says it uses"},
        {"value": "2012", "label": "Nobel prize in economics for stable matching (Shapley and Roth)"}]},
       [L(N, "Hinge says it uses something else: the Gale-Shapley algorithm, a piece of maths from 1962 for making stable matches. The work behind it won a Nobel prize in economics in 2012.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "A Nobel prize? For dating?", "surprised", "closeup"),
   L(M, "For matching. Medical students with hospitals. Kidney donors with patients. And now... you.", "neutral"),
   L(R, "So a Nobel prize winner is personally trying to find me a girlfriend.", "excited"),
   L(M, "And he's struggling.", "sarcastic", "closeup", pause=0.7)]),
 stage("coffee_shop", RM, [
   L(M, "Stable means nobody would rather swap. You get matched with someone who'd also pick you back.", "neutral",
     act="the woman on the right explains, moving two sugar packets together on the table"),
   L(R, "So if I like everyone...", "thinking" if False else "confused"),
   L(M, "...the app learns nothing useful about you. You become noise.", "neutral"),
   L(R, "I've been noise. For three months.", "sad", pause=0.6, act="the young man on the left slowly lowers his head onto his hand")]),
 # act 3: choice overload in the jam aisle
 hero("A colourful supermarket aisle with a long tasting table covered in rows of jam jars of every colour, bright friendly light",
      [L(N, "Maya had one more lesson. It involved jam.", "sarcastic")]),
 stage("grocery_aisle", RM, [
   L(R, "Why are we in the jam aisle?", "confused"),
   L(M, "Because of a famous experiment. One table had twenty-four jams. Another had six.", "neutral",
     act="the woman on the right gestures along the shelves of jam jars"),
   L(R, "Twenty-four. Obviously. More jam, more joy.", "confident"),
   L(M, "More people stopped at the big table. But only three percent bought anything.", "neutral"),
   L(R, "And the small table?", "curious" if False else "confused"),
   L(M, "Thirty percent.", "sarcastic", "closeup", pause=0.7, react="the young man on the left blinks slowly at the jars, mouth closed")]),
 chart({"mode": "stats", "title": "The jam study (Iyengar & Lepper, 2000)", "items": [
        {"value": "24 jams", "label": "more shoppers stopped, but 3% bought"},
        {"value": "6 jams", "label": "fewer stopped, but 30% bought"}]},
       [L(N, "Psychologists call it choice overload. With too many options, people often choose nothing at all. Endless profiles can work the same way.", "neutral", "detail")]),
 stage("grocery_aisle", RM, [
   L(R, "So two hundred swipes a day is... twenty-four jams.", "thinking" if False else "confused"),
   L(M, "Two hundred jams, Ryan.", "sarcastic"),
   L(R, "That's a lot of jam.", "sad", "closeup", pause=0.6),
   L(M, "Fewer swipes. More attention. Actually read the profile.", "neutral"),
   L(R, "Read. The profile. Okay. Okay, I can do that.", "confident")]),
 # act 4: fixing his profile
 stage("flat", RM, [
   L(M, "Now. Your photos.", "neutral", act="the woman on the right holds out her hand for his phone"),
   L(R, "They're great! That one's me holding a fish.", "excited", act="the young man on the left proudly shows her his phone"),
   L(M, "Ryan, every man on this app is holding a fish.", "sarcastic", "closeup"),
   L(R, "...It was a very big fish.", "sad", pause=0.6),
   L(M, "Pick one clear photo where you're smiling. And write something that someone can actually reply to.", "neutral")]),
 stage("flat", RM, [
   L(R, "Okay. New bio: I make an excellent instant ramen, and I'm looking for someone to argue with about the best flavour.", "confident"),
   L(M, "...That's actually good.", "surprised", "closeup", pause=0.6),
   L(R, "I know things.", "confident", "closeup"),
   L(M, "You know one thing.", "sarcastic")]),
 card("One Week Later", [L(N, "One week later. Fewer swipes. Better photo. And for the first time... a match.", "happy")], tr="wipe"),
 # act 5: the date
 stage("cafe_date", RZ, [
   L(Z, "So, you're the ramen guy?", "happy", act="the young woman on the right smiles and sits down across from him"),
   L(R, "I am the ramen guy. Ask me anything.", "confident"),
   L(Z, "Best flavour?", "happy"),
   L(R, "Spicy miso. Not up for debate.", "confident", pause=0.5),
   L(Z, "Okay... I'm going to debate it.", "happy", "closeup")]),
 stage("cafe_date", RZ, [
   L(R, "Can I be honest? I used to swipe right on everyone.", "nervous" if False else "worried"),
   L(Z, "Everyone?", "surprised"),
   L(R, "Two hundred a day. My friend Maya said I was noise.", "sad"),
   L(Z, "I like that you read my profile. You asked about my dog.", "happy"),
   L(R, "He looked like a very good boy.", "happy", "closeup", pause=0.5)]),
 # ending
 stage("flat", RM, [
   L(R, "Maya. She wants a second date.", "excited"),
   L(M, "See? Fewer jams.", "happy"),
   L(R, "Fewer jams. More ramen.", "confident"),
   L(M, "That's not the lesson.", "sarcastic", "closeup"),
   L(R, "It's a lesson.", "confident", pause=0.6)]),
 stage("flat", RM, [
   L(R, "Okay, real question. What's the worst dating profile line you've ever seen? Comments. Go.", "excited", "closeup"),
   L(M, "Please don't say 'holding a fish'.", "sarcastic"),
   L(R, "Wait. She just texted. 'Have you ever been to a wedding?'", "surprised", act="the young man on the left looks down at his buzzing phone"),
   L(R, "Maya... what do I wear to a wedding?", "worried", pause=0.8),
   L(M, "...Next week, Ryan.", "sarcastic", "closeup")]),
 card("See You Next Time", [L(N, "Thanks for watching. Subscribe, because Ryan's dating life is just getting started.", "happy")], tr="fade"),
]

ENVS = [
 {"id": "flat", "prompt": "Ryan's small cosy city apartment living room: a comfy sofa against the back wall, a goldfish bowl on a side table, plants, a lamp, warm evening light", "ambience": "quiet apartment hum, distant traffic"},
 {"id": "coffee_shop", "prompt": "a bright neighbourhood coffee shop: counter and espresso machine along the back wall, pendant lights, small tables at the far edges, big window with soft daylight", "ambience": "light cafe chatter, espresso machine hiss"},
 {"id": "grocery_aisle", "prompt": "a bright friendly supermarket aisle: long shelves of colourful jam jars along the back, a small tasting table at the far left edge, clean floor", "ambience": "supermarket murmur, soft background music, trolley wheels"},
 {"id": "cafe_date", "prompt": "a charming small cafe in the evening: warm string lights, a few small round tables at the far edges, plants, a window with city lights", "ambience": "soft cafe chatter, clinking cups, gentle music"},
]
CHARS = [
 {"id": "zoe", "name": "Zoe", "role": "", "real_person": False, "tag": "the young woman with short curly hair in the mustard cardigan",
  "look": "a friendly, confident young woman in her mid twenties with fair skin, short curly auburn hair, freckles, warm smile, mustard yellow cardigan over a white top, dark jeans, small silver earrings",
  "voice": "A friendly young woman in her mid-twenties with a bright, playful, slightly husky voice, warm and quick-witted, casual neutral American accent."},
]
OUTFITS = {("flat", R): "home", ("cafe_date", R): "date_night", ("coffee_shop", M): "smart_casual", ("flat", M): "evening"}


def build(proj, scenes=SCENES, title="Why Ryan Keeps Getting Ghosted (The Algorithm Knows)"):
    sh = script.load_show()
    research = json.load(open(os.path.join(proj, "research.json")))
    scenes = json.loads(json.dumps(scenes))
    for s in scenes:                                   # outfits by place: home lounge at home, best effort on the date
        for c in s.get("cast", []):
            o = OUTFITS.get((s.get("environment"), c["char"]))
            if o: c["outfit"] = o
    d = {"title": title, "thumbnail_text": "200 SWIPES. 0 MATCHES", "description":
         "Ryan swipes right on everyone and can't work out why nobody matches. Maya explains how dating apps really decide who you see — "
         "Tinder's old chess-style Elo score, Hinge's Nobel-prize 'stable matching' maths, and why too many choices make people choose nothing.",
         "characters": [{k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person")} for c in sh["cast"]] + CHARS,
         "environments": ENVS, "scenes": scenes, "sources": [s["url"] for s in research["sources"]], "show": sh["name"]}
    d = script.apply_show(script.validate(d), sh)
    for c in d["characters"]:
        f = next((x for x in sh["cast"] if x["id"] == c["id"]), None) or next((x for x in CHARS if x["id"] == c["id"]), None)
        if f and f.get("tag"): c["tag"] = f["tag"]
    probs = [p for p in d["_problems"] if "environment as the previous" not in p]
    words = sum(len(s["narration"].split()) for s in d["scenes"])
    json.dump({k: v for k, v in d.items() if not k.startswith("_")}, open(os.path.join(proj, "script.json"), "w"), indent=1, ensure_ascii=False)
    return probs, words, len(d["scenes"])


if __name__ == "__main__":
    print(build(sys.argv[1]))
