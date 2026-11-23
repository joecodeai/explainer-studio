"""'Ryan Thinks Robert Pattinson Is Coming for His Job' — Ryan & Maya, trending 2026-11-18. Written to library/HUMOR_GUIDE.md.

Facts (sources in research.json):
- Amazon MGM Studios confirmed Robert Pattinson as the next James Bond on Mon Nov 16 2026. Statement: "to be entrusted with 007 is the
  honour of a lifetime". Seventh actor to play Bond in the official films; untitled 26th official film; directed by Denis Villeneuve,
  written by Steven Knight (Peaky Blinders); produced by David Heyman and Amy Pascal. Pattinson is 40. (Variety, ABC, BBC, India Today)
- Memes: if you have a job it's only because he hasn't wanted it yet; Batman AND Bond ("I'm both"); "while you worried about AI taking
  jobs, Pattinson took them"; a 2008 Twilight scene: "Gambling, tuxedos and Bond, James Bond." (India Today, LinkedIn News)
- His run: Harry Potter and the Goblet of Fire (2005), Twilight (2008-), films with Cronenberg, Eggers, Lynne Ramsay; The Batman (2022);
  Nolan's The Odyssey (2026); The Batman II due 2028. (India Today)
- Final screen tests: three parts — stunts, camera presence, dialogue; finalists reportedly incl. Callum Turner, Jack Lowden, Josh
  O'Connor; memes also named Nicholas Hoult. (BBC citing Hollywood Reporter)
- Money: Amazon bought MGM for $8.5bn in 2021 (incl. Bond distribution rights); in 2025 took full creative control from Barbara Broccoli
  and Michael G. Wilson for more than $1bn; Skyfall (2012) made $1.1bn worldwide; BBC: a household name "widely seen as a safe pair of
  hands". (BBC, India Today)
- History: Ian Fleming thought Connery an "overgrown stuntman", appalled at the uncouth 31-year-old; Lazenby was found through a Fry's
  Chocolate Cream advert and played Bond once; Roger Moore was 57 in his last Bond film; Timothy Dalton turned it down at 24 or 25,
  thinking Bond should be 35-40; Daniel Craig's run ended with No Time to Die (2021). (Wikipedia: Portrayal of James Bond in film)
- Economics: Sherwin Rosen, "The Economics of Superstars" (American Economic Review, 1981): small differences in talent become large
  differences in earnings when one performer can serve a huge market. Arthur De Vany & David Walls: no amount of star power makes a
  hit; William Goldman (1983): "Nobody knows anything." (JSTOR/AER, De Vany & Walls)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from yen_episode import L, cast, stage, card, chart
from studio import script

N, R, M, D = "narrator", "benny", "maya", "dana"
RM, RD = cast(R, M), cast(R, D)

SCENES = [
 # ---------------------------------------------------------------- cold open
 stage("ryan_flat", RM, [
   L(R, "Maya. I need you to check my CV before Robert Pattinson sees it.", "worried",
     act="the young man on the left hunches over a laptop on the sofa, typing fast",
     react="the woman on the right stands holding a coffee mug, one eyebrow raised, mouth closed"),
   L(M, "Why would Robert Pattinson read your CV?", "confused"),
   L(R, "He's Batman. Since Monday, he's also James Bond. He is clearly working his way down a list.", "confident"),
   L(M, "And you think you're on the list.", "sarcastic", "closeup"),
   L(R, "I work in operations. Nobody knows what that is. That's exactly the kind of job you take when nobody's looking.", "worried", pause=0.7,
     react="the woman on the right slowly lowers her mug, mouth closed"),
   L(M, "So your fear is that a movie star secretly wants your spreadsheets.", "sarcastic"),
   L(R, "Everybody wants my spreadsheets.", "confident", "closeup")]),
 card("Ryan Figures It Out", [L(N, "On Monday, Robert Pattinson was named the next James Bond. By Tuesday, the internet had decided he was coming for everyone else's job too.", "neutral")], tr="wipe"),
 stage("ryan_flat", RM, [
   L(R, "Okay, but how does this affect me? The memes say if you have a job, it's only because he hasn't wanted it yet.", "worried"),
   L(M, "Those are jokes, Ryan.", "neutral"),
   L(R, "So were the AI ones. Now my calendar writes my emails.", "worried"),
   L(M, "And they're better than yours.", "sarcastic", "closeup", pause=0.5),
   L(R, "Fair. It doesn't start every single one with 'sorry for the late reply'.", "sad"),
   L(M, "Fine. Let's find out what actually happened, why one actor keeps getting every big role, and whether your spreadsheets are safe.", "neutral")]),
 # ---------------------------------------------------------------- act 1: what happened
 card("The New 007", [L(N, "First, the facts. Here's what was actually announced.", "neutral")]),
 chart({"mode": "stats", "title": "The next James Bond (announced Nov 16)", "items": [
        {"value": "7th", "label": "actor to play Bond in the official films"},
        {"value": "26th", "label": "official Bond film, title not announced yet"},
        {"value": "Villeneuve", "label": "director (Dune), script by Steven Knight (Peaky Blinders)"}]},
       [L(N, "Amazon MGM confirmed Pattinson as the seventh actor to play Bond in the official films. The twenty-sixth film will be directed by Denis Villeneuve, who made Dune, and written by Steven Knight, who created Peaky Blinders. Pattinson called it the honour of a lifetime.", "neutral", "detail")]),
 stage("ryan_flat", RM, [
   L(R, "Seven people in sixty-four years. That's not a job. That's a line of succession.", "surprised"),
   L(M, "With one difference. Royals don't have to audition.", "sarcastic"),
   L(R, "How do you even audition to be Bond? Do they push you out of a plane and see if you land in a tuxedo?", "confused"),
   L(M, "Close. The final screen tests reportedly had three parts. Stunts, camera presence, and dialogue.", "neutral"),
   L(R, "So. Can you fall, can you be looked at, and can you talk.", "confident"),
   L(M, "You'd pass one of the three.", "sarcastic", "closeup", pause=0.6,
     react="the young man on the left perks up hopefully, mouth closed"),
   L(R, "...Which one?", "confused"),
   L(M, "You fall beautifully.", "sarcastic", "closeup")]),
 # ---------------------------------------------------------------- act 2: every Bond is hated first
 card("Every Bond Gets Hated First", [L(N, "Before the memes, a little history. Because Bond fans have never liked a new Bond. Not once.", "neutral")]),
 chart({"mode": "stats", "title": "First reactions, 1962 to now", "items": [
        {"value": "\"Overgrown stuntman\"", "label": "Ian Fleming on Sean Connery, 31, the first film Bond"},
        {"value": "A chocolate advert", "label": "where producers found George Lazenby, who played Bond once"},
        {"value": "57", "label": "Roger Moore's age in his last Bond film"}]},
       [L(N, "Ian Fleming, who wrote the books, thought Sean Connery was an overgrown stuntman. George Lazenby was spotted in a chocolate advert, played Bond once, and left. Roger Moore kept going until he was fifty-seven. And Timothy Dalton turned the role down in his twenties, because he thought Bond should be at least thirty-five.", "neutral", "detail")]),
 stage("ryan_flat", RM, [
   L(R, "So the first Bond was hated by the guy who invented Bond.", "surprised"),
   L(M, "Bond fans have been furious since 1962. It's the most reliable part of the franchise.", "sarcastic"),
   L(R, "And one guy got the job from a chocolate advert.", "excited"),
   L(M, "Don't.", "sarcastic", "closeup", pause=0.5),
   L(R, "I was just going to ask if they're still hiring from adverts.", "confident",
     act="the young man on the left subtly straightens his posture, as if posing for a camera"),
   L(M, "You were in one advert. For a mattress. You were asleep.", "sarcastic"),
   L(R, "Method acting.", "confident", "closeup")]),
 # ---------------------------------------------------------------- act 3: follow the money
 card("Follow the Money", [L(N, "So why him? Why not one of the younger actors who reached the final tests? Follow the money.", "neutral")]),
 chart({"mode": "stats", "title": "What Bond is worth", "items": [
        {"value": "$8.5bn", "label": "Amazon's price for MGM, 2021 (incl. Bond rights)"},
        {"value": "$1bn+", "label": "paid in 2025 for full creative control of Bond"},
        {"value": "$1.1bn", "label": "what Skyfall made worldwide in 2012"}]},
       [L(N, "Amazon paid eight and a half billion dollars for MGM in 2021, Bond included. Then, last year, more than a billion more to take full creative control from the family that had run Bond for decades. One good Bond film, like Skyfall, can make over a billion dollars. With that much on the table, the BBC put it simply: they chose a household name, widely seen as a safe pair of hands.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "Nine and a half billion dollars, and the safe choice is the guy from Twilight.", "confused",
     act="the young man on the left stares at his phone in disbelief, holding a takeaway cup",
     react="the woman on the right sips her coffee, unbothered, mouth closed"),
   L(M, "He's also been Batman, worked with Christopher Nolan, and survived Twilight fans. That's basically military training.", "sarcastic"),
   L(R, "Twilight fans say they predicted this. There's a scene where someone says Bond, James Bond.", "excited"),
   L(M, "You got your blackout news from The Simpsons and your casting news from Twilight.", "sarcastic", "closeup", pause=0.5),
   L(R, "I get my news from the classics.", "confident", "closeup")]),
 chart({"mode": "stats", "title": "The long way to 007", "items": [
        {"value": "2005", "label": "Harry Potter and the Goblet of Fire"},
        {"value": "2008", "label": "Twilight, then years of small films with Cronenberg, Eggers, Lynne Ramsay"},
        {"value": "2022 - 2026", "label": "The Batman, Nolan's The Odyssey, now Bond"}]},
       [L(N, "His route matters. He got famous young, with Harry Potter and then Twilight. Then, instead of chasing blockbusters, he spent years in small, strange films with directors like David Cronenberg and Robert Eggers. Only after that came The Batman, Christopher Nolan's The Odyssey, and now Bond.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "Vampire, Batman, Bond. That's not a career. That's a character arc.", "surprised"),
   L(M, "In between, he spent years in odd little films most people never saw. On purpose.", "neutral"),
   L(R, "Why would anyone hide from the money?", "confused"),
   L(M, "Because it made the best directors trust him. Reputation compounds, Ryan. Like interest, but for being taken seriously.", "neutral"),
   L(R, "So my reputation has been compounding too.", "confident"),
   L(M, "Your reputation is mostly the mattress advert.", "sarcastic", "closeup", pause=0.6),
   L(R, "...Still compounding.", "confident", "closeup")]),
 # ---------------------------------------------------------------- act 4: the economics of superstars
 card("The Economics of Superstars", [L(N, "Here's the part the memes miss. An economist explained this exact situation in 1981.", "neutral")]),
 chart({"mode": "stats", "title": "Sherwin Rosen, \"The Economics of Superstars\" (1981)", "items": [
        {"value": "1 performance", "label": "can reach millions of people at once"},
        {"value": "Small talent gap", "label": "turns into a huge pay gap"},
        {"value": "Winner takes most", "label": "buyers want the best, not the cheapest"}]},
       [L(N, "Sherwin Rosen called it the economics of superstars. In some jobs, one performance can reach millions of people at once. A film is made once and watched everywhere. So a studio doesn't want the tenth-best actor at a discount. It wants the best one it can get, at almost any price. Tiny differences in talent become enormous differences in pay.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "So he's not stealing jobs. All the big jobs are the same job.", "surprised"),
   L(M, "Exactly. There's one Bond. Not ten Bonds who each get a tenth of the money.", "neutral"),
   L(R, "Ten cheaper Bonds sounds like a great deal to me.", "confident"),
   L(M, "Ten cheaper Bonds is a stag party.", "sarcastic", "closeup")]),
 stage("coffee_shop", RM, [
   L(M, "And here's the twist. Stars don't actually guarantee hits.", "neutral"),
   L(R, "Then why pay them?", "confused"),
   L(M, "Economists Arthur De Vany and David Walls studied box office results and found no amount of star power makes a movie a hit. The screenwriter William Goldman summed up Hollywood in three words. Nobody knows anything.", "neutral"),
   L(R, "So nobody knows anything, and they still picked him.", "confused"),
   L(M, "When nobody knows anything, you pick the person whose choice you can explain to your boss.", "sarcastic", "closeup", pause=0.6,
     react="the young man on the left slowly nods, impressed, mouth closed"),
   L(R, "That's the most honest thing anyone has ever said about my office.", "surprised")]),
 # ---------------------------------------------------------------- act 5: does this affect Ryan?
 card("Is Ryan's Job Safe?", [L(N, "Which brings us back to the real question. Ryan's spreadsheets.", "sarcastic")]),
 stage("office", RD, [
   L(R, "Dana. Quick one. Is my job safe from Robert Pattinson?", "worried",
     act="the young man on the left leans on the edge of a desk, trying to look casual",
     react="the woman on the right looks up slowly from her monitor, expressionless, mouth closed"),
   L(D, "Ryan, you've worked here three years. I still don't know what your job is.", "neutral"),
   L(R, "That's my security strategy.", "confident", "closeup", pause=0.6),
   L(D, "Then you're the safest person in this building.", "sarcastic"),
   L(R, "...I'm going to take that as a compliment.", "confused"),
   L(D, "Please do. It's quieter.", "neutral", "closeup")]),
 chart({"mode": "stats", "title": "Superstar job vs. normal job", "items": [
        {"value": "Millions at once", "label": "how many people one actor's work can reach"},
        {"value": "One room at a time", "label": "how many a normal job usually serves"},
        {"value": "Closer together", "label": "pay in normal jobs, because nobody can be everywhere"}]},
       [L(N, "Most jobs don't scale like a film. An actor can be in a million cinemas at once. An accountant, a nurse, or an operations guy can only be in one room at a time. So pay sits much closer together, and one star can't take everyone's job.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(M, "He can be in a million cinemas at once, Ryan. He cannot be in your Tuesday meeting.", "neutral"),
   L(R, "Thank goodness. Tuesday is when we discuss the printer.", "happy"),
   L(M, "But you can borrow his trick. He spent years doing strange, small films before the big ones came. Be the obvious choice for one specific thing.", "neutral"),
   L(R, "So I need to be the Robert Pattinson of operations.", "excited"),
   L(M, "Start smaller. Be the Robert Pattinson of the printer.", "sarcastic", "closeup"),
   L(R, "I fixed it twice this month.", "confident"),
   L(M, "See? That's a franchise.", "happy", "closeup")]),
 stage("coffee_shop", RM, [
   L(M, "And every job interview is a screen test. Stunts: can you do the work. Camera presence: how you come across. Dialogue: can you explain what you do.", "neutral"),
   L(R, "I fail dialogue.", "sad"),
   L(M, "Because nobody can explain operations.", "sarcastic"),
   L(R, "Nobody can explain operations.", "confident", "closeup", pause=0.5,
     act="the young man on the left nods with complete conviction"),
   L(M, "That was supposed to worry you.", "sarcastic", "closeup")]),
 # ---------------------------------------------------------------- act 6: Ryan applies the lesson (80% right)
 card("Friday. Performance Review.", [L(N, "Friday. Ryan's performance review. He prepared.", "sarcastic")], tr="wipe"),
 stage("office", RD, [
   L(D, "Ryan. Why are you wearing a tuxedo?", "confused",
     act="the woman on the right stares at him over her glasses",
     react="the young man on the left adjusts an imaginary cufflink with great seriousness, mouth closed"),
   L(R, "Every review is a screen test. I'm dressing for the role I want.", "confident"),
   L(D, "The role you want is your current role.", "sarcastic", "closeup"),
   L(R, "With a slightly better title.", "confident"),
   L(D, "Your numbers are fine, Ryan.", "neutral"),
   L(R, "Fine is how every Bond starts. Then everyone sees the second film.", "confident", "closeup", pause=0.6),
   L(D, "...Sit down, Ryan.", "sarcastic", "closeup")]),
 stage("coffee_shop", RM, [
   L(R, "Okay, real question for everyone watching. If Robert Pattinson took your job, what would he be worse at than you? Comments. Be honest.", "excited", "closeup"),
   L(M, "He'd be worse at the printer.", "sarcastic"),
   L(R, "Nobody is worse at the printer than Robert Pattinson.", "confident", "closeup")]),
 card("See You Next Time", [L(N, "Nobody stole anyone's job. Some markets crown one winner, most don't, and Ryan still has his spreadsheets. Subscribe. He's going to need the support.", "happy")], tr="fade"),
]

ENVS = [
 {"id": "ryan_flat", "prompt": "Ryan's small cosy city apartment living room in the evening: a sofa with a laptop on it, a bookshelf and a framed poster on the back wall, a television on the side wall, a floor lamp with warm light", "ambience": "quiet apartment hum, distant traffic"},
 {"id": "coffee_shop", "prompt": "a bright neighbourhood coffee shop: counter and espresso machine along the back wall, pendant lights, small tables at the far edges, big window with soft daylight", "ambience": "light cafe chatter, espresso machine hiss"},
 {"id": "office", "prompt": "a bright open-plan office: rows of desks with monitors along the back wall, a large office printer at the far left edge, plants, a whiteboard, big windows with daylight", "ambience": "office murmur, keyboard typing, distant printer"},
]
CHARS = [
 {"id": "dana", "name": "Dana", "role": "Ryan's team lead", "real_person": False, "tag": "the team lead with short dark hair and glasses",
  "look": "a composed, sharp woman in her early forties with fair skin, short neat dark hair, rectangular glasses, a navy blazer over a white blouse, a lanyard with an ID badge",
  "voice": "A composed woman in her early forties, dry and deadpan, low-to-mid pitch, unhurried, neutral American accent, very understated."},
]


def dress(scenes):
    for s in scenes:
        for c in s.get("cast", []):
            if s.get("environment") == "ryan_flat":
                c["outfit"] = "home" if c["char"] == R else "evening"
            elif s.get("environment") == "office" and c["char"] == R:
                c["outfit"] = "office"
    for s in scenes:                     # the review scene: the tuxedo-ish formal suit
        if s.get("kind") == "stage" and any("tuxedo" in l["text"].lower() for l in s["lines"]):
            for c in s["cast"]:
                if c["char"] == R: c["outfit"] = "formal"
    return scenes


TITLE = "Ryan Thinks Robert Pattinson Is Coming for His Job"
DESC = ("Robert Pattinson is the new James Bond, and the internet thinks he's coming for everyone's job, Ryan's included. Maya explains how "
        "Bond is really cast, what Amazon paid for 007, and the economics of superstars: why one actor gets every big role, why stars don't "
        "guarantee hits, and why your job is probably safe.")


def build(proj, scenes=SCENES, title=TITLE, desc=DESC):
    sh = script.load_show()
    research = json.load(open(os.path.join(proj, "research.json")))
    scenes = dress(json.loads(json.dumps(scenes)))
    d = {"title": title, "thumbnail_text": "HE TOOK BOND", "description": desc,
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


# ---------------------------------------------------------------- the 45-second reel (its own short project, rendered first)
REEL_SCENES = [
 stage("ryan_flat", RM, [
   L(R, "Maya. I need you to check my CV before Robert Pattinson sees it.", "worried",
     act="the young man on the left hunches over a laptop on the sofa, typing fast",
     react="the woman on the right stands holding a coffee mug, one eyebrow raised, mouth closed"),
   L(M, "Why would Robert Pattinson read your CV?", "confused"),
   L(R, "He's Batman. Since Monday, he's also James Bond. He is clearly working his way down a list.", "confident"),
   L(M, "So your fear is that a movie star secretly wants your spreadsheets.", "sarcastic", "closeup"),
   L(R, "Everybody wants my spreadsheets.", "confident", "closeup")]),
 chart({"mode": "stats", "title": "Why one actor gets every big role", "items": [
        {"value": "$8.5bn", "label": "what Amazon paid for MGM, Bond included"},
        {"value": "1 film", "label": "reaches millions of people at once"},
        {"value": "1981", "label": "Sherwin Rosen: the economics of superstars"}]},
       [L(N, "Economists saw this coming in 1981. When one performance reaches millions, studios want the best they can get, at almost any price.", "neutral", "detail")]),
 stage("coffee_shop", RM, [
   L(R, "Ten cheaper Bonds sounds like a great deal to me.", "confident"),
   L(M, "Ten cheaper Bonds is a stag party.", "sarcastic", "closeup"),
   L(R, "So is my job safe?", "worried"),
   L(M, "He can be in a million cinemas at once, Ryan. He cannot be in your Tuesday meeting.", "neutral", "closeup")]),
 card("Full Episode on YouTube", [L(N, "The full story is on our YouTube channel. Link in bio.", "happy")], tr="fade"),
]
REEL_TITLE = "Robert Pattinson Is Taking All the Jobs?"


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "episode"
    if which == "reel":
        print(build(sys.argv[1], REEL_SCENES, REEL_TITLE, DESC))
    else:
        print(build(sys.argv[1]))
