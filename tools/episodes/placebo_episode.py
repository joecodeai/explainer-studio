"""'This Button Has Done Nothing Since 1990' - Ryan & Maya. Script + sources: scripts/PLACEBO_BUTTONS_SCRIPT.md (user-approved).

  python tools/episodes/placebo_episode.py projects/<slug> reel      # native 9:16 reel (~45 s)
  python tools/episodes/placebo_episode.py projects/<slug> episode   # YouTube episode

Facts (all sourced in research.json): ADA 3-second minimum door time + Otis quote (Nexstar 2024); NYT 2004 2,500 of 3,250 NYC walk
buttons 'mechanical placebos'; TfL via BBC: ~2,500 junction crossings, no effect by day, works 00:00-07:00; ACHR News 2003: 51 of 70
contractors installed dummy thermostats; Langer 1975 $8.67 vs $1.96; Buell & Norton 2011 labor illusion; Kaptchuk 2010 59% vs 35%.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gta6_episode import L, cast, stage, screen, card, CHARS as GTA_CHARS, N, R, M, D
from studio import script

CHARS = [c for c in GTA_CHARS if c["id"] == D]
OFFICE_RM = cast(R, M, outfits=["office", None])
HOME = cast(R, M, outfits=["home", "home"])
R_OFFICE = cast(R, outfits=["office"])
D_ONLY = cast(D)
RD = cast(R, D, outfits=["office", None])

ENVS = [
 {"id": "lift", "prompt": "inside a small modern office lift: brushed steel walls, a steel handrail, a small round-button panel on the far right wall, soft white ceiling light, closed steel doors at the back", "ambience": "quiet lift hum"},
 {"id": "lift_lobby", "prompt": "an office lift lobby in the morning: two brushed steel lift doors on the back wall with a small call-button panel between them, a potted plant at the far left edge, polished floor, cool daylight", "ambience": "quiet building lobby"},
 {"id": "crossing", "prompt": "a city pavement at a pedestrian crossing in the morning: a traffic-light pole with a yellow push-button box at the far right edge, a striped crossing and a road behind, brick buildings and a few trees, soft daylight, no cars close by", "ambience": "city street, distant traffic, birds"},
 {"id": "office", "prompt": "a bright open-plan office: rows of desks with monitors along the back wall, a small white wall thermostat on a pillar at the far right edge, plants, big windows with daylight", "ambience": "office murmur, keyboard typing"},
 {"id": "flat_evening", "prompt": "a small cosy city apartment in the evening: an open-plan living room with a sofa on the right, a small kitchen table with two chairs on the left, a bookshelf and a framed poster on the back wall, warm floor-lamp light, dark blue window", "ambience": "quiet apartment hum, distant traffic"},
]
SOURCES = [
 {"title": "Nexstar / Fox 8 (26 Oct 2024): Does the elevator's 'door close' button actually do anything? (ADA 3-second minimum; Otis statement)", "url": "https://fox8.com/news/nexstar-media-wire/does-the-elevators-door-close-button-actually-do-anything/"},
 {"title": "New York Times (27 Feb 2004): For Exercise in New York Futility, Push Button", "url": "https://www.nytimes.com/2004/02/27/nyregion/for-exercise-in-new-york-futility-push-button.html"},
 {"title": "BBC News Magazine: Does pressing the pedestrian crossing button actually do anything? (Transport for London)", "url": "https://www.bbc.com/news/magazine-23869955"},
 {"title": "ACHR News (27 Mar 2003): Placebo Stats (51 of 70 contractors installed dummy thermostats)", "url": "https://www.achrnews.com/articles/92414-placebo-stats"},
 {"title": "Langer (1975), The Illusion of Control, J. Personality and Social Psychology (review in Addiction, PMC)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9292938/"},
 {"title": "Buell & Norton (2011), The Labor Illusion, Management Science (Harvard Business School)", "url": "https://www.hbs.edu/ris/Publication%20Files/Norton_Michael_The%20labor%20illusion%20How%20operational_f4269b70-3732-4fc4-8113-72d0c47533e0.pdf"},
 {"title": "Kaptchuk et al. (2010), Placebos without Deception, PLoS ONE", "url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0015591"},
 {"title": "Waber, Shiv, Carmon & Ariely (2008), Commercial features of placebo and therapeutic efficacy, JAMA (85% vs 61%)", "url": "https://www.gsb.stanford.edu/insights/behavioral-impact-higher-price"},
 {"title": "European Commission (2019): sound-emitting device obligatory in all new e-cars as of 1 July 2021", "url": "https://single-market-economy.ec.europa.eu/news/electric-and-hybrid-cars-new-rules-noise-emitting-protect-vulnerable-road-users-2019-07-03_en"},
 {"title": "CNET: BMW M5 generates fake engine noise using stereo (Active Sound Design)", "url": "https://www.cnet.com/roadshow/auto-tech/bmw-m5-generates-fake-engine-noise-using-stereo/"},
 {"title": "Library of Congress (2008): Shutter Sound of Cell Phone Cameras - Japan does not regulate it (industry practice)", "url": "https://tile.loc.gov/storage-services/service/ll/llglrd/2019669583/2019669583.pdf"},
]

LIFT_PANEL = lambda presses, cap=None: {"type": "panel", "style": "lift", "buttons": [{"label": "OPEN"}, {"label": "CLOSE", "hot": True}], "presses": presses, **({"caption": cap} if cap else {})}
JAB = [0.15, 0.4, 0.62, 0.85, 1.05, 1.3, 1.5, 1.72, 1.95, 2.2, 2.45]

# ====================================================================== REEL (native 9:16, ~45 s)
REEL = [
 screen(LIFT_PANEL(JAB), [L(R, "Every second counts.", "rationalising")], hold=2.8,
        top=[{"text": "This button has done nothing since 1990.", "at": 0}]),
 stage("lift", OFFICE_RM, [
   L(M, "That button doesn't do anything.", "dry"),
   L(R, "It does for me.", "deadpan", pause=0.9, act="keeps pressing a button off to the side without looking"),
   L(R, "See?", "rationalising"),
   L(M, "They were closing anyway.", "dry"),
   L(R, "Because I asked.", "deadpan")]),
 screen({"type": "panel", "style": "crossing", "buttons": [{"label": "PUSH", "hot": True}], "presses": [0.3, 0.7, 1.1, 1.5],
         "caption": "NYC, 2004: 2,500 of 3,250 crossing buttons were placebos"},
        [L(M, "In London, during the day, the button has no effect. It works between midnight and seven a.m.", "dry")]),
 stage("crossing", OFFICE_RM, [L(R, "So I'm only in charge between midnight and seven.", "deflated", act="checks his watch, then looks at the crossing button")]),
 stage("office", R_OFFICE, [], hold=1.8, action="turns a small wall thermostat dial down without stopping, then walks on"),
 screen({"type": "panel", "style": "thermostat", "reading": [{"at": 0, "text": "23°"}, {"at": 0.4, "text": "19°"}]}, hold=1.1, tr="cut"),
 stage("office", D_ONLY, [], hold=1.8, action="turns a small wall thermostat dial back up without stopping, then walks on"),
 screen({"type": "panel", "style": "thermostat", "reading": [{"at": 0, "text": "19°"}, {"at": 0.4, "text": "23°"}]}, hold=1.1, tr="cut"),
 card([{"text": "51 of 70 heating contractors admitted installing dummy thermostats.", "at": 0, "size": 56},
       {"text": "ACHR News, 2003", "at": 0.8, "size": 34, "color": "#9aa8c6"}], hold=2.8, tr="cut"),
 stage("office", RD, [], hold=3.4, action="the young man on the left slowly pulls the small thermostat off the wall and stares at the bare wall behind it; the woman on the right stops and stares too, both mouths closed"),
 card([{"text": "Which button do YOU still press?", "at": 0}, {"text": "Ryan Figures It Out · link in bio", "at": 1.6, "size": 40}],
      [L(N, "The full episode's on YouTube. Press the link. That one works.", "narration")], hold=4.6),
]

# ====================================================================== EPISODE
EPISODE = [
 # ---------------------------------------------------------------- 1 cold open
 screen(LIFT_PANEL(JAB), [L(R, "Every second counts.", "rationalising")], hold=2.8),
 stage("lift", OFFICE_RM, [
   L(M, "That button doesn't do anything.", "dry", react="keeps pressing a button off to the side, eyes on the doors, mouth closed"),
   L(R, "It does for me.", "deadpan", pause=1.0, act="keeps pressing a button off to the side without looking"),
   L(R, "See?", "rationalising"),
   L(M, "They were closing anyway.", "dry"),
   L(R, "Because I asked.", "deadpan")], top=[{"text": "8:47 AM", "at": 0, "until": 2.5}]),
 card([{"text": "THIS BUTTON HAS DONE NOTHING SINCE 1990", "at": 0, "size": 66}, {"text": "RYAN FIGURES IT OUT", "at": 1.6, "size": 44, "color": "#ffd166"}],
      hold=3.4, music="comedic"),
 # ---------------------------------------------------------------- 2 the law of the lift
 stage("lift", OFFICE_RM, [
   L(M, "In America, since the disability law of 1990, the doors have to stay open at least three seconds. The close button isn't allowed to make that shorter.", "dry"),
   L(R, "And after three seconds?", "curious"),
   L(M, "Otis, the lift company, says whether the button actually closes the door sooner is up to the building owner.", "dry"),
   L(R, "So it might work.", "rationalising"),
   L(M, "It might.", "dry", pause=0.8)]),
 screen(LIFT_PANEL([0.6]), hold=1.6),
 # ---------------------------------------------------------------- 3 the crossing
 screen({"type": "panel", "style": "crossing", "buttons": [{"label": "PUSH", "hot": True}], "presses": [0.2, 0.45, 0.7, 0.95, 1.2, 1.45, 1.7]},
        [L(R, "This one works. It says wait. It's talking to me.", "earnest")]),
 stage("crossing", OFFICE_RM, [
   L(M, "In 2004, the New York Times found that more than two thousand five hundred of New York's three thousand two hundred and fifty crossing buttons were, quote, mechanical placebos.", "dry",
     react="presses the crossing button again, mouth closed")]),
 card([{"text": "2,500 of 3,250", "at": 0, "size": 110, "color": "#ffd166"}, {"text": "New York crossing buttons were \"mechanical placebos\"", "at": 0.5, "size": 46},
       {"text": "The New York Times, 2004", "at": 0.9, "size": 32, "color": "#9aa8c6"}], hold=3.0, tr="cut"),
 stage("crossing", OFFICE_RM, [
   L(R, "We're not in New York.", "deadpan"),
   L(M, "London has about two and a half thousand crossings at junctions. Transport for London says during the day, the button has no effect.", "dry"),
   L(R, "None?", "curious"),
   L(M, "It works between midnight and seven a.m.", "dry", pause=0.8, react="looks at the button, then at his watch, mouth closed"),
   L(R, "So I'm only in charge between midnight and seven.", "deflated", pause=1.0)], top=[{"text": "8:52 AM", "at": 0, "until": 2.5}]),
 # ---------------------------------------------------------------- 4 the thermostat war
 stage("office", R_OFFICE, [], hold=2.0, action="turns a small wall thermostat dial down as he walks past, without stopping"),
 screen({"type": "panel", "style": "thermostat", "reading": [{"at": 0, "text": "23°"}, {"at": 0.5, "text": "19°"}]}, hold=1.4, tr="cut"),
 stage("office", D_ONLY, [], hold=2.0, action="turns the same small wall thermostat dial back up as she walks past, without stopping"),
 screen({"type": "panel", "style": "thermostat", "reading": [{"at": 0, "text": "19°"}, {"at": 0.5, "text": "23°"}]}, hold=1.4, tr="cut"),
 screen({"type": "notepad", "paper": "white", "columns": ["RYAN", "DANA"], "items": [{"text": "214", "col": 0, "at": 0.2}, {"text": "211", "col": 1, "at": 0.6}]}, hold=2.4,
        top=[{"text": "THE THERMOSTAT WAR", "at": 0}]),
 stage("office", R_OFFICE, [
   L(M, "How's the office?", "dry", off=True),
   L(R, "Winning. I've kept this floor at nineteen degrees since March.", "rationalising", act="talks on his phone, quietly proud"),
   L(M, "Is it nineteen degrees?", "dry", off=True, pause=1.2, react="looks around the office, mouth closed"),
   L(R, "It's a slow war.", "deadpan"),
   L(M, "In 2003, a heating and air-con trade paper asked contractors if they'd ever installed dummy thermostats. Fifty-one out of seventy said yes.", "dry", off=True, pause=1.0)]),
 stage("office", RD, [], hold=4.0, action="the young man on the left slowly pulls the small thermostat off the wall and stares at the bare wall behind it; the woman on the right walks up, stops and stares at it too; both mouths closed"),
 stage("office", RD, [], hold=3.6, action="in silence the young man on the left presses the thermostat back onto the wall, then they both walk away in opposite directions, mouths closed"),
 card([{"text": "RYAN 214 · DANA 211", "at": 0, "size": 70}, {"text": "WAR SUSPENDED", "at": 0.8, "size": 54, "color": "#ffd166"}], hold=2.6, tr="cut"),
 # ---------------------------------------------------------------- 5 why we fall for it
 screen({"type": "notepad", "columns": ["BUTTONS I TRUSTED"], "items": [{"text": "Lift: close door", "col": 0, "at": 0.2, "strike": True},
         {"text": "Crossing", "col": 0, "at": 0.8, "strike": True}, {"text": "Thermostat", "col": 0, "at": 1.4, "strike": True}]}, hold=3.2,
        top=[{"text": "That evening", "at": 0, "until": 2}]),
 stage("flat_evening", HOME, [
   L(R, "Why would anyone build a button that does nothing?", "defeated"),
   L(M, "Because pressing it feels like doing something.", "curious"),
   L(R, "Pressing it is doing something.", "deadpan"),
   L(M, "In 1975, a psychologist called Ellen Langer ran a lottery in an office. Some people picked their own ticket. Others were just handed one.", "dry"),
   L(R, "Same odds?", "curious"),
   L(M, "Same odds. When she offered to buy the tickets back, the people who'd picked their own asked for eight dollars sixty-seven. The others asked for one ninety-six.", "dry"),
   L(R, "Because they chose it.", "deadpan"),
   L(M, "She called it the illusion of control.", "dry", pause=0.8)]),
 screen({"type": "spinner", "text": "Searching 400 airlines for your best price…", "sub": "Please wait"},
        [L(R, "This app takes ages. That's how I know it's working hard.", "research")]),
 stage("flat_evening", HOME, [
   L(M, "Harvard tested that. People preferred a website that made them wait and showed its work, over one that gave the same results instantly.", "dry"),
   L(R, "So I like being made to wait.", "deflated"),
   L(M, "If someone's watching you do it.", "dry", pause=1.0, react="stares at his phone, betrayed, mouth closed")]),
 # ---------------------------------------------------------------- 5b fake sounds
 stage("flat_evening", HOME, [
   L(R, "Dinner.", "rationalising", act="holds up his phone to take a photo of his plate"),
   L(M, "Your phone doesn't have a shutter. That click is a recording.", "dry"),
   L(R, "Then why does it click?", "curious"),
   L(M, "So you know it worked.", "dry"),
   L(R, "It's a placebo noise.", "deadpan"),
   L(M, "In Japan you can't turn it off. It isn't even a law. The phone industry just agreed on it.", "dry", pause=0.8),
   L(R, "Who else is lying to me?", "deflated")]),
 card([{"text": "BMW M5", "at": 0, "size": 90}, {"text": "engine sound played through the car's speakers", "at": 0.5, "size": 46},
       {"text": "\"Active Sound Design\" (CNET)", "at": 0.9, "size": 32, "color": "#9aa8c6"}], hold=2.8, tr="cut"),
 stage("flat_evening", HOME, [
   L(M, "Some BMWs play engine noise through the speakers, so the car sounds the way you expect it to.", "dry"),
   L(R, "And electric cars?", "curious"),
   L(M, "Too quiet. Since July 2021, every new electric car in the EU has to make a noise at low speed, so people on the pavement hear it coming.", "dry"),
   L(R, "So the quiet car has to pretend to be loud, and the loud car is pretending to be louder.", "deadpan"),
   L(M, "Mm.", "distracted", pause=0.8),
   L(R, "I don't trust anything that clicks.", "deflated")]),
 # ---------------------------------------------------------------- 6 Ryan stops pressing
 stage("lift_lobby", R_OFFICE, [], hold=3.4, action="stands in front of the closed lift doors with his arms folded, completely still, pressing nothing",
       top=[{"text": "8:51 AM", "at": 0, "until": 1.7}, {"text": "8:55 AM", "at": 1.7}]),
 stage("lift_lobby", RD, [
   L(D, "Morning.", "professional", act="presses the lift call button as she arrives"),
   L(R, "I don't press buttons any more. They're placebos.", "rationalising"),
   L(D, "That one calls the lift, Ryan.", "professional", pause=1.5)]),
 stage("lift_lobby", R_OFFICE, [], hold=2.4, action="stands alone in front of the lift doors, which have just closed, mouth closed"),
 stage("lift_lobby", R_OFFICE, [L(R, "That one works.", "under_breath", act="says it very quietly to himself")]),
 screen({"type": "panel", "style": "lift", "buttons": [{"label": "CALL", "hot": True}], "presses": [0.5]}, hold=1.6),
 # ---------------------------------------------------------------- 7a the expensive painkiller
 stage("flat_evening", HOME, [
   L(R, "Headache. I'm getting the expensive ones. The cheap ones don't work on me.", "rationalising", act="rubs his temple, holding a small box of pills"),
   L(M, "In 2008, researchers gave people a fake painkiller. They told half of them it cost two dollars fifty a pill, and the other half that it cost ten cents.", "dry"),
   L(R, "And?", "curious"),
   L(M, "Eighty-five percent of the expensive group said the pain went down. Sixty-one percent of the cheap group.", "dry"),
   L(R, "Expensive works.", "rationalising"),
   L(M, "They were both sugar.", "deadpan", pause=1.0),
   L(R, "So I'm paying extra for the box.", "deflated")]),
 # ---------------------------------------------------------------- 7 the button that works
 screen({"type": "panel", "style": "red", "buttons": [{"label": "DOES NOTHING", "hot": True}], "presses": []}, hold=2.0),
 stage("flat_evening", HOME, [
   L(M, "This one was free.", "dry"),
   L(R, "What does it do?", "curious"),
   L(M, "It says on it.", "dry", pause=1.0)]),
 screen({"type": "panel", "style": "red", "buttons": [{"label": "DOES NOTHING", "hot": True}], "presses": [0.6]}, hold=1.8),
 stage("flat_evening", HOME, [
   L(R, "That helped.", "deflated", act="his shoulders drop slightly, he says it quietly"),
   L(M, "In 2010, Harvard doctors gave patients sugar pills and told them, honestly, they were sugar pills. Fifty-nine percent of them reported their symptoms got better, compared with thirty-five percent who got nothing.", "dry"),
   L(R, "Even though they knew?", "curious"),
   L(M, "Even though they knew.", "dry", pause=1.0)]),
 # ---------------------------------------------------------------- 8 the last crossing
 stage("crossing", OFFICE_RM, [], hold=3.2, action="the young man on the left stands with his hands in his pockets, calm, not pressing anything; the woman on the right glances at him"),
 screen({"type": "panel", "style": "crossing", "buttons": [{"label": "PUSH", "hot": True}], "presses": [0.5, 0.9]}, hold=1.6),
 stage("crossing", OFFICE_RM, [
   L(M, "It's a placebo.", "deadpan", pause=0.6, act="meets his look with a perfectly straight face",
     react="stares at her, mouth closed"),
   L(M, "It still works.", "deadpan", pause=1.2)]),
 card([{"text": "RYAN 21 · MAYA 2", "at": 0, "size": 70}, {"text": "Which button do you still press?", "at": 1.2, "size": 44, "color": "#ffd166"}],
      [L(N, "Ryan Figures It Out. Which button do you still press? Tell us. We won't tell the button.", "narration")], hold=5.0, tr="fade"),
]

TITLE = "This Button Has Done Nothing Since 1990"
REEL_TITLE = "This Button Has Done Nothing Since 1990"
DESC = ("You press 'close door' in the lift, the button at the crossing and the office thermostat. Most of them do nothing. Ryan finds out "
        "why: the 1990 lift law, New York's 2,500 placebo crossing buttons, London's daytime crossings, the dummy thermostats contractors "
        "admit to, the click your phone fakes, the noise electric cars must make, the illusion of control, and the sugar pills "
        "that work even when you know.")


def build(proj, which="episode"):
    os.makedirs(proj, exist_ok=True)
    sh = script.load_show()
    json.dump({"topic": TITLE, "sources": SOURCES}, open(os.path.join(proj, "research.json"), "w"), indent=1)
    scenes = json.loads(json.dumps(REEL if which == "reel" else EPISODE))
    d = {"title": REEL_TITLE if which == "reel" else TITLE, "thumbnail_text": "DOES NOTHING", "description": DESC,
         "characters": [{k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person")} for c in sh["cast"]] +
                       [{k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person", "tts")} for c in CHARS],
         "environments": ENVS, "scenes": scenes, "sources": [s["url"] for s in SOURCES], "show": sh["name"],
         "format": "vertical" if which == "reel" else "landscape", "no_outro": True}
    d = script.apply_show(script.validate(d), sh)
    for c in d["characters"]:
        f = next((x for x in sh["cast"] if x["id"] == c["id"]), None) or next((x for x in CHARS if x["id"] == c["id"]), None)
        if f and f.get("tag"): c["tag"] = f["tag"]
        if f and f.get("tts"): c["tts"] = f["tts"]
    for s, src in zip(d["scenes"], scenes):
        for k in ("screen", "hold", "action", "top_text"):
            if k in src: s[k] = src[k]
    d["format"], d["no_outro"] = ("vertical" if which == "reel" else "landscape"), True
    probs = [p for p in d["_problems"] if "environment as the previous" not in p]
    json.dump({k: v for k, v in d.items() if not k.startswith("_")}, open(os.path.join(proj, "script.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(proj, "TOPIC"), "w").write(os.path.basename(proj).replace("-", " "))
    open(os.path.join(proj, "NO_REEL"), "w").write("reel is its own native-vertical project\n")
    words = sum(len(l["text"].split()) for s in d["scenes"] for l in s["lines"])
    return probs, words, len(d["scenes"]), len(scenes)


if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "episode"))
