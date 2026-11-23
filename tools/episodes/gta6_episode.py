"""'Ryan's Foolproof Plan to Call In Sick for GTA 6' - built from scripts/GTA6_SICK_DAY_SCRIPT_v3_FINAL.md (user-approved direction).

  python tools/episodes/gta6_episode.py projects/<slug> reel      # native 9:16 reel (~50 s)
  python tools/episodes/gta6_episode.py projects/<slug> episode   # YouTube episode (~8.5 min)

Every line carries a performance tag ("voice"): Ryan -> library/voices/benny/delivery.json, Maya -> library/voices/maya/delivery.json
(Qwen VoiceDesign 'I'), Dana -> qwen_design, Tom -> Qwen preset Aiden. pause_after = written-in silence BETWEEN lines only.
Facts and sources: research.json (written by build()).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from studio import script

N, R, M, D, T = "narrator", "benny", "maya", "dana", "tom"
SERIOUS = {"deadpan", "rationalising", "research", "formal", "fake_ill", "dry", "distracted", "professional"}
EMO = {"deadpan": "neutral", "rationalising": "confident", "research": "confident", "earnest": "excited", "fake_ill": "sad", "formal": "neutral",
       "awkward": "worried", "under_breath": "neutral", "defeated": "sad", "deflated": "sad", "dry": "sarcastic", "curious": "confused",
       "distracted": "neutral", "amused": "happy", "tired": "neutral", "narration": "neutral", "professional": "neutral", "concerned": "worried"}


def L(spk, text, voice, shot="two_shot", pause=None, act=None, react=None, off=False):
    d = {"speaker": spk, "text": text, "voice": voice, "emotion": EMO.get(voice, "neutral"), "shot": shot}
    if pause: d["pause_after"] = pause
    if act: d["act"] = act
    elif voice in SERIOUS: d["act"] = "speaks seriously with a calm, neutral face, no smile"
    if react: d["react"] = react
    if off: d["offscreen"] = True
    return d


def cast(*ids, outfits=None):
    pos = ["left", "right"]
    return [{"char": c, "position": pos[i] if len(ids) > 1 else "center", **({"outfit": outfits[i]} if outfits and outfits[i] else {})}
            for i, c in enumerate(ids)]


def stage(env, c, lines, tr="cut", music="comedic", hold=None, action=None, top=None):
    s = {"kind": "stage", "environment": env, "cast": c, "lines": lines, "transition": tr, "music": music, "beats": [], "sfx": []}
    if hold: s["hold"] = hold
    if action: s["action"] = action
    if top: s["top_text"] = top
    return s


def screen(spec, lines=(), hold=None, tr="cut", music="comedic", top=None):
    s = {"kind": "screen", "environment": "", "cast": [], "screen": spec, "lines": list(lines), "transition": tr, "music": music,
         "beats": [], "sfx": []}
    if hold: s["hold"] = hold
    if top: s["top_text"] = top
    return s


def card(lines_text, vo=(), hold=3.0, tr="fade", music="comedic", dark=True):
    return screen({"type": "card", "lines": lines_text, "dark": dark}, vo, hold=hold, tr=tr, music=music)


# wardrobe
HOME = cast(R, M, outfits=["home", "home"])
R_HOME = cast(R, outfits=["home"])
R_OFFICE = cast(R, outfits=["office"])
RD_OFFICE = cast(R, D, outfits=["office", None])
RM_MORNING = cast(R, M, outfits=["home", "pyjamas"])
RM_EVENING = cast(R, M, outfits=["office", "pyjamas"])
FILES = [{"name": "Q4_Client_Deck_v2.pptx", "meta": "Last edited Monday"}, {"name": "WHY_THURSDAY.pptx", "meta": "Last edited 2 minutes ago"}]

ENVS = [
 {"id": "flat_evening", "prompt": "a small cosy city apartment in the evening: an open-plan living room with a sofa on the right, a small kitchen table with two chairs on the left, a bookshelf and a framed poster on the back wall, warm floor-lamp light, dark blue window", "ambience": "quiet apartment hum, distant traffic"},
 {"id": "bedroom_night", "prompt": "a small bedroom at night with the lights off: a double bed with a grey duvet, a bedside table, curtains closed, dim blue moonlight, a soft glow from the hallway door on the far left", "ambience": "quiet night room tone"},
 {"id": "bedroom_morning", "prompt": "the same small bedroom very early in the morning: a double bed with a rumpled grey duvet, a bedside table with a neat box of tissues and a full glass of water carefully arranged on it, curtains half open, cool pale-blue dawn light", "ambience": "quiet early morning room tone, a bird outside"},
 {"id": "kitchen_morning", "prompt": "the same apartment's kitchen and living area on a weekday morning: a small kitchen table with a closed laptop and a coffee mug, kitchen counter along the back wall, a sofa and coffee table at the far right edge, bright soft daylight from a window", "ambience": "quiet morning apartment, a kettle clicking off"},
 {"id": "office_busy", "prompt": "a bright open-plan office in the afternoon: rows of desks with monitors along the back wall, a team lead's desk with two monitors and a headset, plants, a whiteboard, big windows with daylight", "ambience": "office murmur, keyboard typing, distant printer"},
 {"id": "office_lift", "prompt": "an office lift lobby: brushed steel lift doors on the back wall, a potted plant, glass doors at the far right edge opening onto an open-plan office, cool even daylight, completely empty", "ambience": "quiet building hum"},
 {"id": "office_empty", "prompt": "the same bright open-plan office completely empty on a weekday morning: rows of empty desks with chairs pushed in, monitors switched off, one monitor showing a simple screensaver of coloured shapes, a printer with a small green light, plants, big windows with daylight, no people", "ambience": "very quiet empty office, air conditioning hum"},
 {"id": "meeting_room", "prompt": "a glass-walled office meeting room: one long table for twelve with empty chairs, a laptop at the near end, a blank wall screen, through the glass an empty open-plan office, daylight", "ambience": "quiet meeting room, air conditioning hum"},
 {"id": "flat_tv", "prompt": "the same cosy apartment living room in the evening: a sofa facing a television on the far right wall with a colourful car chase on screen, a coffee table with snack bowls and a game controller, warm lamp light", "ambience": "television car chase, quiet apartment"},
]
CHARS = [
 {"id": D, "name": "Dana", "role": "Ryan's team lead", "real_person": False, "tag": "the team lead with short dark hair and glasses",
  "look": "a composed, sharp woman in her early forties with fair skin, short neat dark hair, rectangular glasses, a navy blazer over a white blouse, a lanyard with an ID badge",
  "voice": "A composed woman in her early forties, low-to-mid pitch, efficient and pleasant, neutral American accent.",
  "tts": {"engine": "qwen_clone", "model": "models/Qwen3-TTS-12Hz-1.7B-Base", "base_direction": "",    # locked 2026-11-21 (was qwen_design)
          "ref_audio": "library/voices/dana/ref_locked.wav", "ref_text": "library/voices/dana/ref_locked.txt"}},
 {"id": T, "name": "Tom", "role": "", "real_person": False, "tag": False, "look": "a man in his thirties", "voice": "a man in his thirties",
  "tts": {"engine": "qwen_clone", "model": "models/Qwen3-TTS-12Hz-1.7B-Base", "base_direction": "",    # locked 2026-11-21 (was preset Aiden)
          "ref_audio": "library/voices/tom/ref_locked.wav", "ref_text": "library/voices/tom/ref_locked.txt"}},
]

SOURCES = [
 {"title": "Rockstar Games Newswire: GTA VI release date (19 November 2026) and apology for the delays", "url": "https://www.rockstargames.com/newswire"},
 {"title": "The Guardian, 15 Nov 2026: 'Ten years, thousands of staff and a billion dollars' (GTA VI, GTA flu, 900,000 survey, $1bn claim)", "url": "https://www.theguardian.com/games"},
 {"title": "Take-Two Interactive: GTA V sales and $1bn record; GTA VI pricing", "url": "https://www.take2games.com/ir"},
 {"title": "Sensor Tower: GTA VI pre-launch sales estimate", "url": "https://sensortower.com/blog"},
 {"title": "Fair Work Ombudsman (Australia): notice and evidence for sick and carer's leave", "url": "https://www.fairwork.gov.au/leave/sick-and-carers-leave/notice-and-medical-certificates"},
 {"title": "GOV.UK: Taking sick leave (self-certification up to 7 days)", "url": "https://www.gov.uk/taking-sick-leave"},
 {"title": "US Department of Labor: Sick leave", "url": "https://www.dol.gov/general/topic/workhours/sickleave"},
 {"title": "IGN / The Guardian: Dragon Quest release days moved to weekends in Japan", "url": "https://www.ign.com"},
]

# ====================================================================== REEL (native 9:16, ~50 s)
REEL = [
 screen({"type": "desktop", "files": FILES, "open": {"index": 1, "at": 2.3}}, hold=3.2,
        top=[{"text": "GTA 6 is out tomorrow. Ryan has prepared.", "at": 0.2}]),
 stage("flat_evening", HOME, [
   L(R, "I've been looking into taking tomorrow off.", "rationalising"),
   L(M, "You have annual leave.", "distracted", react="keeps reading the book, mouth closed"),
   L(R, "Yes. But that's for holidays.", "rationalising", pause=0.5),
   L(M, "And tomorrow?", "curious"),
   L(R, "Is a medical situation.", "deadpan"),
   L(M, "You're not ill.", "dry"),
   L(R, "Not yet. There's still time.", "deadpan", pause=0.9,
     react="slowly lowers her book and looks at him, mouth closed")]),
 stage("bedroom_morning", R_HOME, [
   L(R, "Hi, Dana. I'm feeling a little under the weather.", "fake_ill", act="holds a phone to his ear and speaks carefully, trying to sound unwell"),
   L(D, "Oh no. Rest up.", "concerned", off=True),
   L(D, "Could you just send the deck before you log off?", "professional", off=True, pause=0.3)], top=[{"text": "6:01 AM", "at": 0}]),
 screen({"type": "desktop", "files": FILES[:1]}, [L(R, "Of course.", "formal"), L(D, "And the revised budget.", "professional")]),
 stage("bedroom_morning", R_HOME, [
   L(R, "Naturally.", "formal", act="holds a phone to his ear, eyes closed for a moment"),
   L(D, "And the client notes?", "professional", off=True),
   L(R, "I'm beginning to regret being such a good employee.", "under_breath", act="mutters to himself, looking away from the phone"),
   L(D, "Sorry?", "professional", off=True),
   L(R, "Fever. I'm delirious.", "fake_ill", act="gives one small cough and speaks into the phone, trying to sound ill")]),
 stage("office_lift", R_OFFICE, [], hold=2.6,
       action="stands just outside the open lift doors, slowly looking around at the silent, empty office, mouth closed"),
 screen({"type": "email", "emails": [{"from": "HR System", "subject": "Acting Team Lead (effective today, until further notice)", "at": 0.4}]}, hold=2.4),
 stage("office_empty", R_OFFICE, [], hold=1.8, action="stands completely still at an empty desk, blinks once, mouth closed"),
 card([{"text": "He called in sick at 6:02.", "at": 0.2}, {"text": "By ten, he was running the office.", "at": 1.6, "color": "#ffd166"},
       {"text": "Ryan Figures It Out · link in bio", "at": 3.6, "size": 40}],
      [L(N, "It gets worse. Full episode's on YouTube.", "narration")], hold=5.5),
]

# ====================================================================== YOUTUBE EPISODE (~8.5 min)
EPISODE = [
 # ---------------------------------------------------------------- 1 the business plan
 stage("flat_evening", HOME, [
   L(R, "I've been looking into taking tomorrow off.", "rationalising", act="sits at the table typing on a laptop, completely businesslike",
     react="keeps reading her book, mouth closed"),
   L(M, "You have annual leave.", "distracted"),
   L(R, "Yes. But that's for holidays.", "rationalising", pause=0.6),
   L(M, "And tomorrow?", "curious"),
   L(R, "Is a medical situation.", "deadpan"),
   L(M, "You're not ill.", "dry"),
   L(R, "Not yet. There's still time.", "deadpan", pause=1.2, react="slowly lowers her book and looks at him, mouth closed"),
   L(M, "You're planning to develop a medical condition.", "curious"),
   L(R, "I'm exploring my options.", "rationalising", pause=0.8, react="watches him a moment longer, then lifts the book again, mouth closed"),
   L(M, "Let me know what you come down with.", "dry")], top=[{"text": "Wednesday, 7:38 PM", "at": 0, "until": 3}]),
 card([{"text": "GRAND THEFT AUTO VI", "at": 0.1, "size": 80}, {"text": "Out Thursday, 19 November", "at": 0.6, "size": 54},
       {"text": "The first new GTA in thirteen years", "at": 1.2, "size": 44, "color": "#ffd166"},
       {"text": "RYAN FIGURES IT OUT", "at": 2.6, "size": 64}], hold=4.4, music="upbeat"),
 # ---------------------------------------------------------------- 2 earlier that day
 stage("office_busy", RD_OFFICE, [
   L(R, "Got a minute?", "awkward", act="holds a coffee mug, trying to look casual",
     react="keeps typing fast on her keyboard, eyes on the screen, mouth closed"),
   L(D, "About one.", "professional", act="keeps typing, eyes on her screen"),
   L(R, "Tomorrow, everyone's in? As far as you know?", "awkward"),
   L(D, "As far as I know. Why?", "professional"),
   L(R, "No reason. Planning ahead.", "awkward", pause=0.5),
   L(D, "Good. Then I'll have the deck tonight? Client's at two.", "professional"),
   L(R, "The deck. Yes.", "awkward", pause=0.4),
   L(D, "How's it looking?", "professional", act="glances up at him briefly"),
   L(R, "It's coming together.", "formal", act="gives a careful, evasive smile"),
   L(D, "Great. Tonight, then.", "professional", act="goes straight back to typing")], top=[{"text": "Earlier that day", "at": 0, "until": 2.5}]),
 screen({"type": "game", "title": "GRAND THEFT AUTO VI", "sub": "PRE-LOAD COMPLETE"}, hold=1.6,
        top=[{"text": "Dana's second monitor", "at": 0}]),
 # ---------------------------------------------------------------- 3 the business case
 screen({"type": "desktop", "files": FILES, "open": {"index": 1, "at": 2.4}}, hold=3.2, top=[{"text": "8:05 PM", "at": 0}]),
 stage("flat_evening", HOME, [L(R, "Context.", "rationalising", act="turns the laptop toward her",
                                react="looks up from her book, mouth closed, she did not ask for this")]),
 screen({"type": "slide", "title": "13 YEARS", "sub": "since the last new GTA"}, [
   L(R, "The last one came out in 2013. I was fifteen.", "earnest")]),
 stage("flat_evening", HOME, [
   L(M, "And you've been waiting since.", "dry"),
   L(R, "I've been patient since.", "deadpan")]),
 screen({"type": "slide", "title": "~230 MILLION", "sub": "copies of GTA V. Third best-selling game ever.", "source": "Take-Two"}, [
   L(R, "Two hundred and thirty million copies. Take-Two says it made a billion dollars faster than any entertainment product in history. Any. Films. Albums. Anything.", "earnest")]),
 screen({"type": "slide", "title": "$1BN+", "sub": "in GTA VI pre-orders, before anyone has played it", "source": "Sensor Tower estimate"}, [
   L(R, "The new one's done over a billion in pre-orders. Before anyone's even played it.", "earnest")]),
 stage("flat_evening", HOME, [
   L(M, "Including you.", "dry"),
   L(R, "Including me.", "deadpan", pause=0.5)]),
 screen({"type": "slide", "kicker": "The Guardian", "title": "“Ten years, thousands of staff and a billion dollars”", "source": "The Guardian, 15 November"}, [
   L(R, "Ten years. Thousands of people. A billion dollars.", "rationalising")]),
 stage("flat_evening", HOME, [
   L(M, "And you want one Thursday.", "dry"),
   L(R, "When you put it like that, it's the least I can do.", "rationalising", pause=1.0,
     react="looks at the laptop for a long moment, says nothing, mouth closed"),
   L(M, "How much was it?", "curious"),
   L(R, "Seventy-nine ninety-nine. The last one was sixty, in 2013. That's about eighty-five in today's money. So technically, I've saved money.", "research"),
   L(M, "You bought the ninety-nine ninety-nine one.", "dry"),
   L(R, "I saved on the standard edition. And reinvested.", "deadpan")]),
 # ---------------------------------------------------------------- 4 risk assessment
 stage("flat_evening", HOME, [
   L(R, "Problem.", "research", react="keeps reading her book, mouth closed"),
   L(R, "Australia's Fair Work Ombudsman says an employer can ask for evidence. Even for one day off sick.", "research"),
   L(M, "We don't live in Australia.", "distracted"),
   L(R, "I know. Dana went to Sydney last year.", "rationalising", pause=1.4,
     react="waits for the rest of the argument, there isn't any, mouth closed")], top=[{"text": "9:15 PM", "at": 0, "until": 2.5}]),
 screen({"type": "notepad", "columns": ["RISKS", "STRENGTHS"], "items": [{"text": "Australia (Dana?)", "col": 0, "at": 0.3}]}, [
   L(R, "And I don't have evidence. Because I'm well. That's the whole problem with being well.", "deflated", pause=0.6)]),
 stage("flat_evening", HOME, [
   L(R, "On the other hand. In April, the head of Take-Two, the company that makes it, joked that a lot of people would be calling in sick on the nineteenth.", "research"),
   L(M, "The man selling you the game.", "dry"),
   L(R, "He's acknowledged the condition.", "rationalising"),
   L(M, "He's also got your eighty dollars.", "dry"),
   L(R, "That's between me and capitalism.", "deadpan")]),
 screen({"type": "notepad", "columns": ["RISKS", "STRENGTHS"], "items": [{"text": "Australia (Dana?)", "col": 0},
         {"text": "Industry-recognised condition", "col": 0, "at": 0.3, "moveTo": 1, "moveAt": 1.8}]}, hold=3.4),
 # ---------------------------------------------------------------- 5 the delays
 screen({"type": "notepad", "paper": "white", "columns": ["PLAN"], "items": [
         {"text": "Autumn 2025 — book flu", "col": 0, "at": 0.2, "strike": True}, {"text": "26 May 2026 — book flu", "col": 0, "at": 0.9, "strike": True}]}, hold=3.0),
 stage("flat_evening", HOME, [
   L(M, "You've done this before.", "curious", act="holds up an old notepad page"),
   L(R, "Twice.", "deadpan"),
   L(M, "Book flu.", "curious"),
   L(R, "It was meant to come out last autumn. Then they moved it to May. Then November. Every time, I had a plan.", "rationalising"),
   L(M, "And every time—", "curious"),
   L(R, "Rockstar apologised. Very gracious about it. Sorry for adding additional time.", "rationalising", pause=0.8),
   L(R, "When you think about it, the game called in sick. Twice.", "deadpan"),
   L(M, "And nobody asked it for evidence.", "dry"),
   L(R, "Nobody asked it for evidence.", "under_breath", act="says it quietly to himself, with real feeling")]),
 # ---------------------------------------------------------------- 6 the paperwork
 stage("flat_evening", HOME, [
   L(M, "Have you printed the internet?", "curious", act="holds a mug of tea, looking at the papers on the table"),
   L(R, "You can't highlight a website.", "deadpan", act="highlights a printed page without looking up"),
   L(R, "In the UK you can self-certify for up to seven days. No fit note.", "research"),
   L(M, "Seven days.", "dry"),
   L(R, "I only need one. I'm not greedy.", "deadpan"),
   L(M, "And America?", "curious"),
   L(R, "No national law. Most private-sector workers don't get paid sick days unless their state or their employer gives them. So it depends where you live, and who you work for.", "research"),
   L(R, "Which is why I've read this.", "rationalising", act="taps a thick staff handbook covered in coloured sticky tabs"),
   L(M, "You've read the staff handbook.", "curious"),
   L(R, "Twice.", "deadpan"),
   L(M, "How long did that take?", "curious"),
   L(R, "About three hours.", "deadpan", pause=2.0, act="checks his watch and answers like a timesheet",
     react="nods slowly, sips her tea and says nothing, mouth closed")], top=[{"text": "11:48 PM", "at": 0, "until": 2.5}]),
 # ---------------------------------------------------------------- 7 the epidemic
 stage("flat_evening", HOME, [
   L(R, "When the last one came out in 2013, so many people went off sick it got a name. GTA flu.", "research", act="scrolls on his phone, energised"),
   L(M, "Catchy.", "dry"),
   L(R, "A survey says nine hundred thousand Brits are going to pretend to be sick tomorrow.", "research"),
   L(M, "How many people did they ask?", "curious"),
   L(R, "A thousand.", "deadpan", pause=1.2, react="just looks at him, mouth closed"),
   L(R, "There's also a figure saying it'll cost the American economy a billion dollars.", "research"),
   L(M, "Says who?", "curious"),
   L(R, "One article. Spanish TV, last summer. The Guardian calls the maths back-of-the-napkin.", "research", pause=0.8),
   L(R, "Shame. I liked being a threat to the economy.", "deflated")]),
 # ---------------------------------------------------------------- 8 precedent
 stage("bedroom_night", HOME, [
   L(R, "In Japan, in the nineties, Dragon Quest had so many kids skipping school and adults calling in sick that they moved the releases to Saturdays.", "research",
     act="lies in bed, face lit by his phone", react="stands in the doorway brushing her teeth, mouth closed"),
   L(M, "Mm.", "distracted"),
   L(R, "A whole country rearranged itself around a game.", "earnest"),
   L(M, "Or they rearranged the game around the country.", "dry", pause=1.0),
   L(R, "Rockstar didn't do that.", "rationalising"),
   L(M, "Rockstar picked a Thursday.", "dry"),
   L(R, "It's a test.", "deadpan"),
   L(M, "Goodnight, Ryan.", "tired")], top=[{"text": "Midnight", "at": 0, "until": 2.5}]),
 screen({"type": "phone", "clock": "00:04", "date": "Thursday 19 November", "alarm": {"time": "6:00", "label": "CALL DANA (sound ill)"}}, hold=2.6),
 # ---------------------------------------------------------------- 9 the call
 screen({"type": "download", "title": "GTA VI", "steps": [{"at": 0, "pct": 3, "remain": "11 hrs remaining"}]}, hold=2.0, top=[{"text": "Thursday, 6:01 AM", "at": 0}]),
 stage("bedroom_morning", R_HOME, [
   L(R, "Hi, Dana. It's Ryan.", "fake_ill", act="sits up and holds a phone to his ear, clears his throat"),
   L(D, "Ryan. Hi.", "professional", off=True),
   L(R, "Just wanted to let you know I'm feeling a little under the weather.", "fake_ill"),
   L(D, "Oh no. What is it?", "concerned", off=True),
   L(R, "Flu, I think. Headache. Fatigue. Very sudden.", "fake_ill"),
   L(D, "Right. Rest up. Anything urgent you need to hand over?", "concerned", off=True),
   L(R, "Nothing that can't wait.", "fake_ill", act="glances sideways at something off-screen, then back"),
   L(D, "Great. Actually, could you just send the deck over before you log off? I'll take the client through it at two.", "professional", off=True)]),
 screen({"type": "desktop", "files": FILES[:1]}, hold=1.8),
 stage("bedroom_morning", R_HOME, [
   L(R, "Of course.", "formal", act="closes his eyes for a moment, phone to his ear"),
   L(D, "And the revised budget.", "professional", off=True),
   L(R, "Naturally.", "formal"),
   L(D, "And the client notes. And if you could update the tracker, that'd be amazing.", "professional", off=True),
   L(R, "I'm beginning to regret being such a good employee.", "under_breath", act="mutters to himself, looking away from the phone"),
   L(D, "Sorry?", "professional", off=True),
   L(R, "Fever. I'm delirious.", "fake_ill", act="gives one small cough and speaks into the phone"),
   L(D, "Feel better.", "concerned", off=True, pause=1.2)]),
 # ---------------------------------------------------------------- 10 working from bed
 stage("kitchen_morning", RM_MORNING, [
   L(M, "How's the flu?", "amused", act="wanders past slowly holding a coffee, in no hurry at all",
     react="types fast on a laptop, wrapped in a duvet, mouth closed"),
   L(R, "Productive.", "defeated", act="keeps typing without looking up"),
   L(R, "Thanks, Ryan. One more thing.", "under_breath", pause=0.6, act="reads a message off the laptop flatly")], top=[{"text": "9:20 AM", "at": 0, "until": 2.5}]),
 screen({"type": "download", "title": "GTA VI", "steps": [{"at": 0, "pct": 14, "remain": "6 hrs remaining"}, {"at": 1.6, "pct": 14.1, "remain": "7 hrs remaining"}]}, hold=3.2),
 stage("kitchen_morning", RM_MORNING, [
   L(R, "It went up.", "deadpan"),
   L(M, "What did?", "curious"),
   L(R, "The time. I've been ill all morning, and it's further away than when I started.", "defeated")]),
 screen({"type": "chat", "title": "Dana", "messages": [{"who": "Dana", "time": "9:22", "text": "Can you dial into the 10? Camera on if you're up to it :)", "at": 0.2}]}, hold=2.6),
 stage("kitchen_morning", RM_MORNING, [
   L(R, "If I dial in, I have to be ill. For an hour. On camera.", "rationalising", pause=1.5),
   L(R, "It'd be less work to go in.", "deadpan", act="arrives at the conclusion quietly"),
   L(M, "Take the duvet off first.", "dry", act="sips her coffee"),
 ]),
 stage("kitchen_morning", cast(M, outfits=["pyjamas"]), [], hold=3.0, action="puts her feet up on the coffee table, picks up the TV remote and settles in, relaxed and smiling slightly",
       top=[{"text": "9:24 AM. Thursday.", "at": 0.3}]),
 # ---------------------------------------------------------------- 11 the reality
 stage("office_lift", R_OFFICE, [], hold=3.0, action="steps out of the open lift doors and stops, looking at the silent, empty office, mouth closed",
       top=[{"text": "9:58 AM", "at": 0, "until": 2}], music="none"),
 stage("office_empty", R_OFFICE, [], hold=2.6, action="sits down slowly at an empty desk and does nothing for two seconds, mouth closed", music="none"),
 screen({"type": "chat", "title": "Team chat", "focusAt": 4.4, "messages": [
   {"who": "Ryan", "time": "6:02", "text": "Feeling under the weather today, will be mostly offline.", "highlight": True},
   {"who": "Dana", "time": "7:02", "text": "Not feeling great. Taking a sick day.", "at": 0.8},
   {"who": "Priya", "time": "7:15", "text": "Same, sorry all.", "at": 1.6},
   {"who": "Tom", "time": "7:31", "text": "Woke up with a fever.", "at": 2.4},
   {"who": "Leo", "time": "7:48", "text": "Working from home today, might be patchy.", "at": 3.2}]}, hold=5.6, music="none"),
 stage("office_empty", R_OFFICE, [L(R, "Interesting.", "deadpan", pause=1.0, act="says it almost without emotion")], music="none"),
 screen({"type": "email", "emails": [
   {"from": "Dana", "subject": "Quick favour", "at": 0.2, "body": "Ryan, just saw you badged in, so glad you're feeling better! Since you're the only one in, could you chair the 10am and take the client at 2? Thanks for stepping up."},
   {"from": "HR System", "subject": "Acting Team Lead (effective today, until further notice)", "at": 4.0}]}, hold=6.0),
 stage("office_empty", R_OFFICE, [L(R, "I've accidentally been promoted by the flu.", "under_breath", pause=0.8, act="looks around the empty office, then quietly says it to the screen")]),
 screen({"type": "calendar", "day": "Thursday 19 November", "events": [
   {"time": "10:00", "title": "Team Sync", "note": "You are the host"}, {"time": "11:00", "title": "Budget review"}, {"time": "12:00", "title": "Vendor call"},
   {"time": "13:00", "title": "Tracker update (due)"}, {"time": "14:00", "title": "CLIENT PRESENTATION — Q4 deck", "hot": True},
   {"time": "15:00", "title": "Ops stand-up"}, {"time": "16:30", "title": "Client follow-up", "note": "You are the host"}]}, hold=3.2),
 screen({"type": "phone", "clock": "10:00", "thread": {"who": "Maya", "messages": [{"text": "How's your day off?", "at": 0.2},
         {"mine": True, "text": "Apparently, I'm the only person in the country who isn't sick.", "at": 1.4}], "typing": {"at": 5.0, "end": 6.4}}}, hold=7.2),
 # ---------------------------------------------------------------- 12 the 10 am meeting
 stage("meeting_room", R_OFFICE, [L(R, "Morning, everyone. Thanks for joining.", "formal", pause=1.0, act="sits alone at the end of a long table, speaking to a laptop")]),
 screen({"type": "call", "title": "Team Sync", "tiles": [{"name": "Dana"}, {"name": "Priya"}, {"name": "Tom"}, {"name": "Leo"}],
         "events": [{"at": 0.3, "kind": "thumbs", "who": "Priya"}, {"at": 3.2, "kind": "away", "who": "Priya"}, {"at": 4.6, "kind": "talk", "who": "Tom", "dur": 1.8}]},
        [L(R, "Let's go round with updates. Priya?", "formal", pause=1.2), L(R, "Tom?", "formal"),
         L(T, "Yeah, nothing from me, mate.", "distracted")], hold=7.0),
 stage("meeting_room", R_OFFICE, [L(R, "Thanks, Tom. Get well soon.", "deadpan", act="says it with complete sincerity")]),
 screen({"type": "call", "title": "Team Sync", "tiles": [{"name": "Dana"}, {"name": "Priya", "state": "away"}, {"name": "Tom"}, {"name": "Leo"}],
         "events": [{"at": 0.8, "kind": "present", "who": "Dana", "dur": 0.6, "text": "GRAND THEFT AUTO VI"}, {"at": 1.4, "kind": "stopped", "who": "Dana"}]}, hold=3.4),
 stage("meeting_room", R_OFFICE, [L(R, "Lovely. Let's take the rest of the agenda offline.", "deadpan", act="looks straight into the webcam with a perfectly neutral face")],
       hold=4.0),
 screen({"type": "phone", "clock": "16:21", "notes": [{"app": "Library", "title": "GTA VI is ready to play", "text": "", "at": 0.6},
         {"app": "Calendar", "title": "Client follow-up — 4:30 PM", "text": "You are the host", "at": 1.8}]}, hold=4.2,
        top=[{"text": "4:21 PM", "at": 0}]),
 # ---------------------------------------------------------------- 13 the annual leave
 stage("flat_tv", RM_EVENING, [
   L(R, "You're playing it.", "defeated", act="stands in the doorway, tie loose, holding a stack of printed slides",
     react="sits relaxed on the sofa with a game controller, eyes on the TV, mouth closed"),
   L(M, "Mm.", "distracted"),
   L(R, "You're not at work.", "curious"),
   L(M, "I'm on annual leave.", "distracted", pause=1.0),
   L(R, "Since when?", "curious"),
   L(M, "September. I booked it the day they announced the date.", "dry", pause=1.0),
   L(R, "It wasn't sick leave.", "deadpan"),
   L(M, "No. That's for when you're ill.", "dry", pause=1.0, react="passes him the second controller without looking away from the screen, mouth closed"),
   L(R, "How do you—", "defeated"),
   L(M, "There's a form.", "dry")], top=[{"text": "Evening", "at": 0, "until": 2}]),
 screen({"type": "form", "title": "HR Portal — Annual leave", "fields": [{"label": "Dates", "value": "Fri 20 November", "at": 0.4},
         {"label": "Reason for leave", "value": "Holiday", "at": 1.8}], "submitAt": 3.0,
         "result": {"at": 3.5, "text": "Request declined.\nYou are the only available cover for: Acting Team Lead."}}, hold=6.0),
 stage("flat_tv", RM_EVENING, [
   L(R, "I think I'm coming down with something.", "under_breath", pause=0.5, act="says it very quietly, staring at his phone"),
   L(M, "There's still time.", "deadpan", act="keeps playing, eyes on the TV, no smile")], hold=4.0),
 card([{"text": "RYAN FIGURES IT OUT", "at": 0.2, "size": 64}],
      [L(N, "Ryan Figures It Out. If you're watching this at work today, get well soon.", "narration")], hold=5.0, tr="fade"),
]

TITLE = "Ryan's Foolproof Plan to Call In Sick for GTA 6"
REEL_TITLE = "He Called In Sick for GTA 6. It Went Badly."
DESC = ("GTA 6 is out on Thursday 19 November, the first new GTA in thirteen years. Ryan doesn't want to waste annual leave on it, so he "
        "builds a business case for calling in sick instead: sick-note rules, GTA flu, a dubious billion-dollar statistic and a game "
        "that got delayed twice. Then he makes the call.")


def build(proj, which="episode"):
    os.makedirs(proj, exist_ok=True)
    sh = script.load_show()
    json.dump({"topic": TITLE, "sources": SOURCES}, open(os.path.join(proj, "research.json"), "w"), indent=1)
    scenes = json.loads(json.dumps(REEL if which == "reel" else EPISODE))
    d = {"title": REEL_TITLE if which == "reel" else TITLE, "thumbnail_text": "CALLING IN SICK", "description": DESC,
         "characters": [{k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person")} for c in sh["cast"]] +
                       [{k: c[k] for k in ("id", "name", "look", "voice", "role", "real_person", "tts")} for c in CHARS],
         "environments": ENVS, "scenes": scenes, "sources": [s["url"] for s in SOURCES], "show": sh["name"],
         "format": "vertical" if which == "reel" else "landscape", "no_outro": True}
    d = script.apply_show(script.validate(d), sh)
    for c in d["characters"]:
        f = next((x for x in sh["cast"] if x["id"] == c["id"]), None) or next((x for x in CHARS if x["id"] == c["id"]), None)
        if f and f.get("tag"): c["tag"] = f["tag"]
        if f and f.get("tts"): c["tts"] = f["tts"]
    for s, src in zip(d["scenes"], scenes):          # fields validate() does not know about
        for k in ("screen", "hold", "action", "top_text"):
            if k in src: s[k] = src[k]
    d["format"], d["no_outro"] = ("vertical" if which == "reel" else "landscape"), True
    probs = [p for p in d["_problems"] if "environment as the previous" not in p]
    json.dump({k: v for k, v in d.items() if not k.startswith("_")}, open(os.path.join(proj, "script.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(proj, "TOPIC"), "w").write((REEL_TITLE if which == "reel" else TITLE) if False else os.path.basename(proj).replace("-", " "))
    open(os.path.join(proj, "NO_REEL"), "w").write("reel is its own native-vertical project\n")
    words = sum(len(l["text"].split()) for s in d["scenes"] for l in s["lines"])
    return probs, words, len(d["scenes"])


if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "episode"))
