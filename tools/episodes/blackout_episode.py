"""Builds script.json for 'Ryan Prepared for the 90-Day Blackout (It Was a 1-Minute Test)' — Ryan & Maya, trending news 2026-11-17.

Facts (all in research.json):
- FEMA + FCC nationwide Emergency Alert System test, Tue Nov 17 2026, 2:20 p.m. ET; announced by the FCC Sept 16; FEMA must test
  nationwide at least once every three years; last test Oct 4 2023; TV/radio/cable/satellite, about one minute; message in English and
  Spanish: "This is only a test. No action is required by the public."; no cellphone (WEA) alerts this time; backup date Dec 3. (Snopes,
  Nacionale citing FCC DA-26-989)
- Rumour sources: a Simpsons episode "It's a Blunderful Life" (aired Nov 19 2023) with a blackout starting Nov 17, "six days before
  Thanksgiving" — true for 2023 (Thanksgiving Nov 23), not 2026 (Thanksgiving Nov 26); viral X post around Nov 1. (Snopes, Nacionale)
- Pentagon FORTRESS America, unveiled by Defense Secretary Pete Hegseth Sept 30: every military department and defense agency able to
  operate independently for at least 90 days (water, electricity, fuel, communications); five pillars. (WBBJ/Gray News)
- Real outages days before: Microsoft Outlook outage Nov 12; nationwide aircraft ground stop Nov 13 (telecom failure); bank software
  outages Nov 16. (Snopes)
- "33 countries" = a Newsweek map of governments giving stockpiling advice; UK "Be Ready", Brazil Civil Defense: ~3 days of water/food. (Nacionale)
- Grid: Lower 48 run on three main interconnections (Eastern, Western, Texas/ERCOT); the US has never had a nationwide blackout;
  2003 (Aug 14) ~50 million people, a line in northern Ohio sagged into trees and tripped without the utility realising; 1965 >30 million;
  Texas Feb 2021 >4.5 million. (Nacionale)
- CDC/FEMA prep: 1 gallon of water per person per day for at least 3 days; nonperishable food for 3 days; flashlights instead of
  candles; never run a generator indoors, keep it at least 20 feet from windows, doors and vents; fridge ~4 hours closed, full freezer
  ~48 hours, half-full ~24 hours. (Nacionale citing CDC/FEMA)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from yen_episode import L, cast, stage, card, hero, chart, mp
from studio import script

N, R, M, H = "narrator", "benny", "maya", "store_clerk"
RM, RH = cast(R, M), cast(R, H)

SCENES = [
 # ---------------------------------------------------------------- cold open: the night before
 stage("flat_supplies", RM, [
   L(R, "Maya. Don't panic. But the power goes out tomorrow. For ninety days.", "worried",
     act="the young man on the left wears a headlamp and stands among stacks of supplies, speaking seriously",
     react="the woman on the right stops in the doorway, staring at the boxes, mouth closed"),
   L(M, "Ryan, why are there forty candles on your sofa?", "confused"),
   L(R, "Because the grid goes down at two-twenty tomorrow afternoon. I have the date. I have the time.", "confident"),
   L(M, "Who told you that?", "sarcastic", "closeup"),
   L(R, "The internet. And... The Simpsons.", "confident", pause=0.8,
     react="the woman on the right closes her eyes for a moment, mouth closed"),
   L(M, "So... nobody.", "sarcastic", "closeup")], tr="cut"),
 card("Ryan Figures It Out", [L(N, "There is no ninety-day blackout. But there is a very real reason Ryan's phone was full of them.", "neutral")], tr="wipe"),
 stage("flat_supplies", RM, [
   L(R, "Okay, but how does this affect me? Because I spent four hundred dollars on beans.", "worried"),
   L(M, "How many beans?", "confused"),
   L(R, "Two hundred cans.", "confident", pause=0.6),
   L(M, "And a can opener?", "sarcastic", "closeup"),
   L(R, "...I'll be right back.", "worried", pause=0.6, act="the young man on the left freezes, then slowly looks toward the door")]),
 # ---------------------------------------------------------------- act 1: where the rumour came from
 card("Where It Came From", [L(N, "So where did this come from? Maya found four ingredients, all stirred into one very scary soup.", "neutral")]),
 stage("flat_supplies", RM, [
   L(M, "Ingredient one. A real test. Tomorrow at two-twenty Eastern, FEMA and the FCC test the national Emergency Alert System.", "neutral",
     act="the woman on the right scrolls on her phone, then holds it up for him"),
   L(R, "A test of what? The blackout?", "surprised"),
   L(M, "The beeping. You know, the loud tone before a storm warning. TV and radio, for about a minute.", "neutral"),
   L(R, "A minute. Not ninety days?", "confused"),
   L(M, "The message literally says: This is only a test. No action is required.", "sarcastic", "closeup", pause=0.6,
     react="the young man on the left glances at his stack of beans, mouth closed")]),
 chart({"mode": "stats", "title": "The real thing on November 17", "items": [
        {"value": "2:20 PM ET", "label": "national Emergency Alert System test (FEMA + FCC)"},
        {"value": "~1 minute", "label": "on TV, radio, cable and satellite"},
        {"value": "Dec 3", "label": "backup date if it has to be moved"}]},
       [L(N, "The FCC announced it back in September. By law, FEMA has to test the system nationwide at least once every three years. The last one was in October 2023. And this time, it won't even buzz your phone.", "neutral", "detail")]),
 stage("flat_supplies", RM, [
   L(M, "Ingredient two. The Simpsons.", "neutral"),
   L(R, "They predict everything, Maya. Everything.", "confident"),
   L(M, "The episode aired in 2023. Lisa opens a diary on November seventeenth, six days before Thanksgiving.", "neutral"),
   L(R, "See? Six days before Thanksgiving!", "excited"),
   L(M, "Thanksgiving this year is on the twenty-sixth. Six days before is the twentieth.", "sarcastic", "closeup", pause=0.7,
     react="the young man on the left slowly counts on his fingers, mouth closed"),
   L(R, "So the Simpsons got... 2023 right.", "confused")]),
 stage("flat_supplies", RM, [
   L(M, "Ingredient three. The Pentagon.", "neutral"),
   L(R, "Now we're talking.", "excited"),
   L(M, "In September, the Defense Secretary announced a plan called FORTRESS America. Military bases should be able to run on their own for at least ninety days.", "neutral"),
   L(R, "NINETY DAYS. There it is.", "surprised", "closeup"),
   L(M, "To keep running during a problem, Ryan. Water, power, fuel, communications. It's a backup plan. Not a date when the problem starts.", "neutral")]),
 chart({"mode": "stats", "title": "FORTRESS America (Pentagon, Sept 30)", "items": [
        {"value": "90 days", "label": "military departments operating on their own"},
        {"value": "5 pillars", "label": "energy, supply chain, reserves, bases & cyber, space"},
        {"value": "0", "label": "blackouts announced"}]},
       [L(N, "It's about resilience: energy independence, supply chains, a strategic reserve, hardening bases against cyberattacks, and space. Nowhere does it announce a blackout.", "neutral", "detail")]),
 stage("flat_supplies", RM, [
   L(M, "Ingredient four. Bad timing. Outlook went down on the twelfth. Flights were grounded nationwide on the thirteenth. Bank apps broke on the sixteenth.", "neutral"),
   L(R, "Three things broke in five days! That's a pattern!", "excited"),
   L(M, "That's... technology.", "sarcastic", "closeup", pause=0.6),
   L(R, "And the map! Thirty-three countries are telling people to stockpile!", "worried"),
   L(M, "That's a map of countries that give normal advice, like keeping three days of water. The UK does it. Brazil does it. It's not a countdown.", "neutral")]),
 stage("flat_supplies", RM, [
   L(R, "But why did it feel so real? Everyone was posting it.", "confused"),
   L(M, "Because it had everything a good rumour needs. A date. A time. A scary number. And a few real things breaking right before it.", "neutral"),
   L(R, "And The Simpsons.", "confident"),
   L(M, "And The Simpsons. Think about it, though. If someone really planned to switch off a whole country, would they post the date online first?", "sarcastic"),
   L(R, "...That would be very polite of them.", "confused", "closeup", pause=0.7,
     react="the woman on the right nods slowly, holding back a smile, mouth closed"),
   L(M, "Very polite. And if it were the government, they'd tell you through the alert system. The one they're testing tomorrow.", "neutral")]),
 stage("flat_supplies", RM, [
   L(R, "Okay, what is the alert system even for?", "curious" if False else "confused"),
   L(M, "Real emergencies. Tornadoes, floods, missing children. It's the loud beep that interrupts your show.", "neutral"),
   L(R, "So tomorrow's beep is the system checking that the beep still works.", "thinking" if False else "confused"),
   L(M, "Exactly. It's a fire drill. For beeps.", "sarcastic", "closeup", pause=0.6),
   L(R, "I've been panicking about a fire drill.", "sad", "closeup")]),
 # ---------------------------------------------------------------- act 2: how the grid really works
 hero("A night view over an American city with glowing windows and long lines of high-voltage power towers stretching to the horizon, calm and steady",
      [L(N, "Next morning, Ryan had one last question. Could the whole country actually go dark at once?", "neutral")]),
 stage("coffee_shop", RM, [
   L(R, "Be honest. Could it all go off at the same time? One big switch?", "worried"),
   L(M, "There isn't one big switch. The Lower 48 states run on three main grids.", "neutral",
     act="the woman on the right draws three shapes on a napkin with her finger"),
   L(R, "Three? I thought it was one giant extension cord.", "confused"),
   L(M, "East, West, and Texas runs its own.", "neutral"),
   L(R, "Of course Texas runs its own.", "sarcastic", "closeup", pause=0.5)]),
 mp({"label": "Three US power grids", "countries": ["United States"],
     "places": [{"name": "Eastern Interconnection", "lat": 38.5, "lon": -82.0}, {"name": "Western Interconnection", "lat": 40.0, "lon": -114.0},
                {"name": "Texas (ERCOT)", "lat": 31.0, "lon": -99.0}], "routes": []},
    [L(N, "The Eastern grid, the Western grid, and Texas, run by a council called ERCOT. They're run largely apart, and the United States has never had a blackout across the whole country at once.", "neutral", "wide")]),
 chart({"mode": "timeline", "title": "The biggest real US blackouts", "items": [
        {"value": "1965", "label": "30+ million people: one faulty relay in Ontario"},
        {"value": "2003", "label": "about 50 million: a power line in Ohio sagged into trees"},
        {"value": "2021", "label": "4.5+ million Texans: a winter storm froze plants and gas"}]},
       [L(N, "Big blackouts do happen. In 2003, about fifty million people lost power after one line in northern Ohio sagged into some trees and nobody noticed in time. But they come from a cause on the grid. Not from a date on the internet.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "The biggest blackout in history started with... a tree?", "surprised", "closeup"),
   L(M, "A tree, and a warning that nobody saw.", "neutral"),
   L(R, "So the real threat is trees.", "confident", pause=0.6),
   L(M, "The real threat is you with forty candles.", "sarcastic", "closeup")]),
 stage("coffee_shop", RM, [
   L(R, "How do I not fall for this next time?", "worried"),
   L(M, "Three quick checks. One: who is actually saying it? A real agency, or a video with dramatic music?", "neutral",
     act="the woman on the right counts on her fingers, calm and clear"),
   L(R, "Dramatic music. Very dramatic.", "sad"),
   L(M, "Two: is there an official announcement? The alert test had one, from the FCC, back in September. The blackout had none.", "neutral"),
   L(R, "And three?", "confused"),
   L(M, "Three: does the maths even work? Six days before Thanksgiving isn't the seventeenth this year.", "sarcastic", "closeup", pause=0.6),
   L(R, "So The Simpsons failed the maths test.", "confident"),
   L(M, "The Simpsons passed. You failed it.", "sarcastic", "closeup", pause=0.6)]),
 # ---------------------------------------------------------------- act 3: preparing the right way
 stage("hardware_store", RH, [
   L(R, "Hi. I need your biggest generator. It's going in my living room.", "confident",
     act="the young man on the left points proudly at a big generator on display"),
   L(H, "In your... living room?", "surprised"),
   L(R, "Right next to the sofa. Cosy.", "happy"),
   L(H, "Please don't. Never run a generator indoors. Not even with the windows open. At least twenty feet from any door or window.", "worried",
     act="the store clerk on the right holds up both hands, alarmed but kind"),
   L(R, "...Twenty feet. My flat is twenty feet.", "worried", pause=0.6)]),
 stage("hardware_store", RH, [
   L(H, "Can I ask what you're preparing for?", "neutral", act="the store clerk on the right leans on the counter, curious"),
   L(R, "The ninety-day blackout. The Simpsons predicted it.", "confident"),
   L(H, "Ah. You're the fourth one today.", "sarcastic", "closeup", pause=0.6,
     react="the young man on the left blinks, slowly realising, mouth closed"),
   L(R, "...What did the other three buy?", "confused"),
   L(H, "Flashlights, batteries, and water. The sensible stuff.", "neutral"),
   L(R, "Okay. I'll take a flashlight. And... a can opener.", "sad", "closeup")]),
 chart({"mode": "stats", "title": "If the power really does go out (CDC & FEMA)", "items": [
        {"value": "1 gallon", "label": "of water per person per day, for at least 3 days"},
        {"value": "20 feet", "label": "generator away from windows, doors and vents — never indoors"},
        {"value": "4 hours", "label": "fridge food stays safe with the door closed"}]},
       [L(N, "Here's what actually helps. Water: one gallon per person per day, for at least three days. Generators: never indoors, at least twenty feet from windows and doors. And keep the fridge shut. Food stays safe for about four hours, and a full freezer for about two days.", "neutral", "detail")]),
 stage("flat_supplies", RM, [
   L(M, "And swap the candles for flashlights. Candles are how a blackout becomes a fire.", "neutral"),
   L(R, "So I should keep... some of this?", "confused"),
   L(M, "Some. Three days. Not ninety. And not two hundred cans of beans.", "sarcastic"),
   L(R, "I'm keeping the beans.", "confident", "closeup", pause=0.5),
   L(M, "You don't have a can opener.", "sarcastic", "closeup")]),
 # ---------------------------------------------------------------- act 4: 2:20 PM
 card("2:20 PM", [L(N, "Tuesday afternoon. Two-nineteen.", "neutral")], tr="wipe"),
 stage("flat_supplies", RM, [
   L(R, "One minute. If the lights go out, I'm saying I told you so.", "worried",
     act="the young man on the left grips a flashlight, staring at the television",
     react="the woman on the right sips her coffee calmly, mouth closed"),
   L(M, "If the lights go out, it's because you plugged in the generator.", "sarcastic", pause=0.8),
   L(R, "Here it comes...", "worried", "closeup", pause=1.0, react="the woman on the right glances at the television, eyebrows raised, mouth closed"),
   L(M, "This is only a test. No action is required by the public.", "sarcastic", "closeup", pause=0.8,
     react="the young man on the left slowly lowers the flashlight, mouth closed"),
   L(R, "...The lights are still on.", "surprised")]),
 stage("flat_supplies", RM, [
   L(R, "My phone didn't even buzz.", "confused"),
   L(M, "They're not testing phones this time.", "neutral"),
   L(R, "So I prepared for the end of the world... and it was a one-minute beep.", "sad", "closeup", pause=0.6),
   L(M, "Honestly? I charged my power bank last night. Just in case.", "happy",
     act="the woman on the right admits it with a small embarrassed smile"),
   L(R, "Maya! You believed it!", "excited", "closeup"),
   L(M, "I believed in being ready for a storm. That's different.", "confident")]),
 stage("flat_supplies", RM, [
   L(R, "So being a little bit ready is smart. Just not two-hundred-cans-of-beans ready.", "confident"),
   L(M, "...That's actually right.", "surprised", "closeup", pause=0.6),
   L(R, "I know things.", "confident", "closeup"),
   L(M, "What are you doing with the beans?", "confused"),
   L(R, "Food bank. They're getting a very prepared donation.", "happy")]),
 stage("flat_supplies", RM, [
   L(R, "Okay, real question. What's the weirdest thing you bought for an end of the world that never came? Comments. I need to feel less alone.", "excited", "closeup"),
   L(M, "Nothing beats forty candles.", "sarcastic"),
   L(R, "Wait. Grand Theft Auto Six comes out on Thursday?", "surprised", act="the young man on the left looks down at his phone, eyes wide"),
   L(R, "Maya... how do I call in sick?", "worried", pause=0.8),
   L(M, "...Next week, Ryan.", "sarcastic", "closeup")]),
 card("See You Next Time", [L(N, "Thanks for watching. Subscribe, and check before you panic. Ryan clearly didn't.", "happy")], tr="fade"),
]

ENVS = [
 {"id": "flat_supplies", "prompt": "Ryan's small cosy city apartment living room crowded with survival supplies: stacks of canned food and water bottles along the back wall, boxes of candles, a hand-crank radio, a television on the side wall, a sofa, warm lamp light", "ambience": "quiet apartment hum, distant traffic"},
 {"id": "coffee_shop", "prompt": "a bright neighbourhood coffee shop: counter and espresso machine along the back wall, pendant lights, small tables at the far edges, big window with soft daylight", "ambience": "light cafe chatter, espresso machine hiss"},
 {"id": "hardware_store", "prompt": "a bright American hardware store aisle: shelves of tools, flashlights and batteries along the back wall, a large portable generator on display at the far right edge, clean floor", "ambience": "store murmur, beeping scanner, soft background music"},
]
CHARS = [
 {"id": "store_clerk", "name": "Clerk", "role": "Hardware store", "real_person": False, "tag": "the store clerk in the red apron",
  "look": "a kind, sensible man in his forties with fair skin, short greying beard, glasses, red work apron over a grey t-shirt, name badge",
  "voice": "A kind, calm man in his forties, warm and steady, friendly neutral American accent, patient and a little concerned."},
]
OUTFITS = {}   # day 1 (night): evening; day 2: signature


def dress(scenes):
    day2 = False
    for s in scenes:
        if s.get("kind") == "hero": day2 = True
        for c in s.get("cast", []):
            if c["char"] in (R, M):
                if not day2: c["outfit"] = "home" if c["char"] == R else "evening"
    return scenes


def build(proj, scenes=SCENES, title="Ryan Prepared for the 90-Day Blackout (It Was a 1-Minute Test)"):
    sh = script.load_show()
    research = json.load(open(os.path.join(proj, "research.json")))
    scenes = dress(json.loads(json.dumps(scenes)))
    d = {"title": title, "thumbnail_text": "90-DAY BLACKOUT?", "description":
         "Ryan believed the viral November 17 '90-day blackout' rumour and bought 40 candles and 200 cans of beans. Maya traces the rumour to "
         "its four ingredients — a one-minute Emergency Alert System test, a Simpsons episode, the Pentagon's FORTRESS plan and a week of "
         "outages — explains how the US power grid really works, and what preparing for a real outage actually looks like.",
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


REEL = [0, 2, 4, 6, 18]          # cold open, beans/can opener, the real test, the Simpsons maths, the generator


if __name__ == "__main__":
    print(build(sys.argv[1]))
