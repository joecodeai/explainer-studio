# Ryan Figures It Out — The Foolproof Plan to Call In Sick for GTA 6
### v3 FINAL: targeted edit of v2 + voice & performance direction

> **How to read the tags.** Every line has a small `voice` tag. That tag *is* the instruction the TTS receives, so delivery gets decided here, on paper, instead of by re-rendering.
>
> - **Ryan** (Qwen "Ryan" voice): the tag picks a written acting direction from `library/voices/benny/delivery.json`, listed in Part 2.
> - **Maya and Dana** (Chatterbox voices): the tag sets expressiveness and pitch movement, from `studio/tts_cb.py` STYLE.
> - **⏸ 0.8** means a written-in silence of 0.8 s after the line (`pause_after`).
> - **"..."** inside a line is a deliberate in-line beat (~0.6 s).
> - *Italic brackets* are for the animation and the director. The TTS never reads them.
>
> The voices themselves stay locked: Ryan is the Qwen "Ryan" preset and Maya is Chatterbox option C. Only the delivery changes.

---

## PART 1 — EDITORIAL

### 1. Remaining issues in v2
1. **Scene 2 timeline clash.** Dana says Ryan presents at ten. Later the ten o'clock is a team sync, and the client presentation is at two. The deck deadline is also never stated plainly. Dana's "slightly too long" look made her suspicious for no reason.
2. **Scene 4 "direction of travel."** It's a constructed joke. Nobody says it.
3. **Scene 7 reads like a news segment.** It packs three facts, two Maya punchlines and a closing button into one short scene.
4. **The download clock doesn't add up.** At 9:20 the download says 7 hours remaining, yet it's "ready to play" at 10:00.
5. **The ending risks feeling one beat over-engineered.** The HR decline arrives as a brand-new mechanism in the last ten seconds.
6. **The reel spends its best surprise.** Showing the whole team chat gives away the episode's main reveal.
7. **Some lines are written, not spoken:**
   - "There's never one fewer thing."
   - "At least someone's getting paid to suffer." It's slightly confusing, and silence does more.
   - "What do I tell people?" Who would she tell?

### 2. Changes, and why
| # | Change | Why |
|---|---|---|
| 1 | **Scene 2 rebuilt.** Dana: "Deck tonight? Client's at two." Ryan: "It's… coming together." | States the deadline plainly. Ryan's evasion sets up the Monday-dated file. Dana is busy, not suspicious. The Dana GTA pre-load plant stays. |
| 2 | **Scene 4.** "Direction of travel" becomes "I know. Dana went to Sydney last year." He writes *Australia (Dana?)* under RISKS. | Real paranoid logic, not a constructed line. The silence after it does the joke. Three options compared in §3. |
| 3 | **Scene 7 cut by ~40%.** The survey joke is now a look, not a line. Maya's "So the economy will be fine" is gone. | Every fact survives. The scene now has one punchline: "Shame. I liked being a threat to the economy." |
| 4 | **The download now finishes at 4:21 pm**, mid-meeting, after a short time-lapse in Scene 12. | The timeline now holds: at 9:20 it says 7 h left, so it's ready at about 4:20. It also lands the "ready to play" payoff when he's most trapped, not at 10 am. |
| 5 | **The ending keeps the HR decline, now planted.** Dana's email says *"Acting Team Lead (effective today, **until further notice**)"*. | The decline becomes the consequence of something we already saw, not a new device (§4). |
| 6 | **Reel:** the hook is the two-file desktop, and it ends on the *Acting Team Lead* email and Ryan's face. The team chat stays out. | The reel teases what happened without explaining it, and the episode keeps its reveal. |
| 7 | **Small trims:** "There's never one fewer thing" cut. "At least someone's getting paid to suffer" replaced by silence. "What do I tell people?" becomes "Take the duvet off first." | Each one is less written. Maya's new line is practical, not a correction, so it's funnier and more in character. |

### 3. Scene 4: three alternatives
**A.** RYAN: "No. But it's the direction of travel." *(v2, cut: it's a policy-paper phrase, so it sounds written)*

**B.** MAYA: "We don't live in Australia." / RYAN: "Not yet." *(cut: it spends the "Not yet" callback, which the ending needs fresh)*

**C. ✅ CHOSEN.** MAYA: "We don't live in Australia." / RYAN: "I know." *(beat)* "Dana went to Sydney last year." *Maya waits for the rest of the argument. There isn't any. He writes it under RISKS.*

C is how an anxious, intelligent person actually reasons: one weak link, held with total sincerity. The joke is the gap where an explanation should be, so silence lands it and nobody has to say anything.

### 4. Ending A vs B
- **A — the HR decline:** Ryan files annual leave. It's auto-declined because he's the only cover. "I think I'm coming down with something." / "There's still time."
- **B — understated:** he takes the controller and they sit. RYAN: "I should've just booked it." MAYA: "Mm."

**A wins, with the plant.**
- **B states the moral.** "I should've just booked it" is the lesson said out loud, which is what the show rules out.
- **A closes the loop.** The episode's argument started at "annual leave is for holidays". A ends with him finally using annual leave properly and the office refusing it. Every step of the story produced that refusal: he went in, so he became cover, so he can't leave.
- **A pays off the first scene.** He reaches for the sick-day logic again, and Maya hands his own opening line back to him.
- **A no longer feels like an extra punchline**, because the email in Scene 11 says "until further notice". The audience half-expects the decline before it arrives.
- **Two trims keep it lean:** Ryan doesn't speak while filling in the form, and the decline appears with no sound effect. A soft notification tick only.

---

## PART 2 — VOICE & PERFORMANCE BIBLE

**The one rule:** don't perform the joke; perform the character's intention.
- Ryan genuinely believes he has a plan.
- Maya genuinely can't believe how much effort he's putting into it.
- Dana genuinely has work to get done.

Only the audience gets to find it ridiculous.

### RYAN — earnest rationaliser
- **Base voice:** mid-range, calm and conversational. He takes himself seriously.
- **He never pauses for a laugh**, and never smirks or puts weight on the funny word.
- **His ridiculous lines get the same voice as his ordinary ones.** That flatness is the joke.

| Tag | When | What it sounds like |
|---|---|---|
| `rationalising` | Defending the plan | Calm and slightly deliberate. He chooses words carefully and is genuinely convinced. A touch defensive, never smug. |
| `deadpan` | Absurd statement as plain fact | Flat, even pitch, sincere, natural pace. No emphasis anywhere. |
| `earnest` | Genuine GTA enthusiasm | A little quicker and brighter. Adult excitement, not a kid's. |
| `research` | Reading out a finding | Focused and quick. A small lift on the detail that helps his case. |
| `awkward` | Fishing (Scene 2) | A small hesitation, slightly too casual, a little stilted. No stammer, no laugh. |
| `formal` | To Dana | Polite and restrained, consciously managing his voice. |
| `fake_ill` | The call | An amateur trying to sound unwell: a little rough, a little too careful. Never a cartoon cough. |
| `under_breath` | Talking to himself | Lower volume, dry and conversational. Not a whisper. |
| `defeated` | The office onward | Low energy, quietly resigned. No outrage. |
| `deflated` | Small private disappointments | Soft, almost sincere, a man who liked his idea. |

### MAYA — the person who already knows
- **Base voice:** calm, a little lower-energy than Ryan, measured and warm underneath.
- **She isn't annoyed with him.** She's mildly entertained, and later quietly amazed.
- **Many of her best moments are no line at all:** a look, a page turned, a sip of tea.

| Tag | Kind | What it sounds like |
|---|---|---|
| `dry` | Dry acknowledgement | Treats the absurd as ordinary. Flat but warm, as if she's heard this argument before. |
| `curious` | Genuine question | Real curiosity with a pinch of disbelief, a slightly slower pace. She's processing, not mocking. |
| `amused` | Quietly amused | A small smile you can hear, not see. Rare. |
| `deadpan` | The final callback | No smile and no change in volume, almost indifferent. If she smiles, it dies. |
| `distracted` | Half-engaged | She's reading, brushing her teeth or playing. Half her attention is elsewhere, and you can hear it. |

**Her arc:** affectionate disbelief in Scenes 1–3, fewer words and more looks in Scenes 4–8, and complete relaxation in Scene 13. She doesn't gloat. Her lack of surprise is the victory.

### DANA — a reasonable manager with bad timing
- **Base voice:** professional, efficient, friendly enough and a little distracted (she's typing). Never sarcastic.
- **Each request lands as a small, normal addition.** No escalating pauses. The joke is the pile-up, and she has no idea it's a joke.

| Tag | What it sounds like |
|---|---|
| `professional` | Brisk and pleasant, mid-task. |
| `concerned` | Brief, genuine sympathy, then straight back to business. |

### Humour delivery guide
| Type | Used for | Performance |
|---|---|---|
| **Deadpan** | Ridiculous things said seriously ("Is a medical situation.") | Minimal movement, steady pace, no pause after. Let the audience find it. |
| **Dry acknowledgement** | Maya treating madness as normal ("Let me know what you come down with.") | Conversational. A tiny weight change is enough. |
| **Repeat-back** | Maya echoing a fact to hear it ("You've read the staff handbook.") | Slower, with a micro-pause before the key noun. Genuine, not mocking. |
| **Awkward** | Ryan hiding his intent | A beat before replying, eyes away, slightly too casual. |
| **Under-the-breath** | Ryan's private comments | Quieter, to himself. Not for the room. |
| **Escalation** | The call and the working-from-bed scene | Pauses shorten, and Ryan's control slips gradually. Never panic. |
| **Silence** | Office arrival, Maya's looks, the decline | A held frame of 1.5–3 s. The cut comes *after* the audience gets it. |

**Timing rules:**
- **A short pause (0.3–0.6 s)** = Ryan searching for a justification.
- **A long pause (1–2 s)** = someone processing something absurd.
- **No pause after punchlines.** The next line or a cut carries on.
- **Overlap is allowed** where marked ("And every time—").

---

## PART 3 — THE YOUTUBE EPISODE (~8.5 min)

### SCENE 1 — THE BUSINESS PLAN
*Wednesday, 7:38 pm. Ryan's flat. Ryan at the kitchen table, laptop open. In the screen's corner, a countdown: **GTA VI — 14:22:07**. Maya on the sofa with a book, feet tucked under her.*
**Atmosphere:** quiet domestic evening. Ryan is calmly businesslike. Maya is half-reading.

- **RYAN** `rationalising` *(as if raising an agenda item)*: I've been looking into taking tomorrow off.
- **MAYA** `distracted` *(doesn't look up)*: You have annual leave.
- **RYAN** `rationalising` *(explaining a legitimate distinction; small breath before "But")*: Yes... But that's for holidays. ⏸ 0.6
*Maya turns a page.*
- **MAYA** `curious`: And tomorrow?
- **RYAN** `deadpan`: Is a medical situation.
- **MAYA** `dry`: You're not ill.
- **RYAN** `deadpan` *(keeps typing; no look up)*: Not yet... There's still time. ⏸ 1.2
*Maya lowers the book. Ryan doesn't notice.*
- **MAYA** `curious` *(slowly; repeating it to hear it)*: You're planning to develop a medical condition.
- **RYAN** `rationalising` *(professional, like a career decision)*: I'm exploring my options. ⏸ 0.8
*She watches him a moment longer, then lifts the book again.*
- **MAYA** `dry`: Let me know... what you come down with.

### TITLE CARD
*Music sting. **GRAND THEFT AUTO VI — OUT THURSDAY, 19 NOVEMBER.** / **The first new GTA in thirteen years.** → **RYAN FIGURES IT OUT***

### SCENE 2 — EARLIER THAT DAY
*Wednesday, 3:10 pm. The office. Dana types fast, headset round her neck. Ryan arrives holding a mug he clearly doesn't need.*
**Atmosphere:** busy afternoon. Ryan is fishing and Dana is mid-task. Play it straight: Dana suspects nothing.

- **RYAN** `awkward`: Got a minute?
- **DANA** `professional` *(eyes on screen, still typing)*: About one.
- **RYAN** `awkward` *(too casual)*: Tomorrow... everyone's in? As far as you know?
- **DANA** `professional`: As far as I know. Why?
- **RYAN** `awkward`: No reason. Planning... ahead. ⏸ 0.5
- **DANA** `professional`: Good. Then I'll have the deck tonight? Client's at two.
- **RYAN** `awkward` *(a beat too long before answering)*: The deck... Yes. ⏸ 0.4
- **DANA** `professional` *(brief glance up, purely practical)*: How's it looking?
- **RYAN** `formal` *(a careful, evasive smile)*: It's... coming together.
- **DANA** `professional` *(already back to typing)*: Great. Tonight, then.
*He leaves. Dana keeps typing. On her second monitor, unnoticed, a browser tab: **GTA VI — Pre-load complete.***

### SCENE 3 — THE BUSINESS CASE
*The flat, 8:05 pm. Close on Ryan's desktop: two files.*
`Q4_Client_Deck_v2.pptx — last edited Monday`
`WHY_THURSDAY.pptx — last edited 2 minutes ago`
*Hold for 2 s. Ryan turns the laptop toward Maya. She didn't ask for this.*
**Atmosphere:** Ryan presents with real enthusiasm. Maya is a polite, captive audience.

- **RYAN** `rationalising`: Context.
*Slide 1 — **13 YEARS.***
- **RYAN** `earnest`: The last one came out in 2013. I was fifteen.
- **MAYA** `dry`: And you've been waiting since.
- **RYAN** `deadpan` *(gentle correction, entirely sincere)*: I've been patient since.
*Slide 2 — **GTA V · ~230 MILLION COPIES · 3rd best-selling game ever.***
- **RYAN** `earnest`: Two hundred and thirty million copies. Take-Two says it made a billion dollars faster than any entertainment product in history... Any. Films. Albums. Anything.
*Slide 3 — **GTA VI · $1BN+ IN PRE-ORDERS** (Sensor Tower estimate)*
- **RYAN** `earnest`: The new one's done over a billion in pre-orders. Before anyone's even played it.
- **MAYA** `dry`: Including you.
- **RYAN** `deadpan` *(tiny pause; quietly owns it)*: ...Including me.
*Slide 4 — headline: **"Ten years, thousands of staff and a billion dollars" — The Guardian.***
- **RYAN** `rationalising` *(slower, letting the scale sink in)*: Ten years. Thousands of people. A billion dollars.
- **MAYA** `dry`: And you want one Thursday.
- **RYAN** `rationalising` *(a reasonable concession)*: When you put it like that, it's the least I can do. ⏸ 1.0
*Maya looks at the slide, then at the other file, the one last edited on Monday. She says nothing. Hold 1.5 s.*
- **MAYA** `curious`: How much was it?
- **RYAN** `research`: Seventy-nine ninety-nine. The last one was sixty, in 2013. That's about eighty-five in today's money. So technically, I've saved money.
- **MAYA** `dry` *(she's seen the receipt)*: You bought the ninety-nine ninety-nine one.
- **RYAN** `deadpan` *(zero hesitation)*: I saved on the standard edition. And reinvested.

### SCENE 4 — RISK ASSESSMENT
*9:15 pm. A notepad beside the laptop, headed in capitals: **RISKS.** One item so far.*
**Atmosphere:** Ryan in due-diligence mode. Maya has gone back to her book.

- **RYAN** `research`: Problem.
*Maya keeps reading.*
- **RYAN** `research`: Australia's Fair Work Ombudsman says an employer can ask for evidence. Even for one day off sick.
- **MAYA** `distracted`: We don't live in Australia.
- **RYAN** `rationalising`: I know... Dana went to Sydney last year. ⏸ 1.5
*Maya waits for the rest of the argument. There isn't any. Under RISKS he writes: **Australia (Dana?)***
- **RYAN** `deflated` *(quiet, genuinely put out)*: And I don't have evidence. Because I'm well... That's the whole problem with being well. ⏸ 0.6
*He scrolls. He brightens.*
- **RYAN** `research`: On the other hand. In April, the head of Take-Two, the company that makes it, joked that a lot of people would be calling in sick on the nineteenth.
- **MAYA** `dry`: The man selling you the game.
- **RYAN** `rationalising`: He's acknowledged the condition.
- **MAYA** `dry`: He's also got your eighty dollars.
- **RYAN** `deadpan` *(slightly lofty, closing the matter)*: That's between me and capitalism.
*On the notepad he writes **Industry-recognised condition**, then draws an arrow moving it to a new column headed **STRENGTHS**. No comment from anyone.*

### SCENE 5 — THE DELAYS
*Maya reaches over to slide the notepad out of his reach. Under it is an older page with two lines, both crossed out:*
~~**Autumn 2025 — book flu**~~
~~**26 May 2026 — book flu**~~
*She looks at it, then at him.*
**Atmosphere:** a small discovery. Ryan isn't embarrassed. He's a veteran.

- **MAYA** `curious`: You've done this before.
- **RYAN** `deadpan`: Twice.
- **MAYA** `curious` *(reading it aloud, slowly)*: "Book flu."
- **RYAN** `rationalising`: It was meant to come out last autumn. Then they moved it to May. Then November. Every time, I had a plan.
- **MAYA** `curious`: And every time—
- **RYAN** `rationalising` *(cuts in; strangely respectful)*: Rockstar apologised. Very gracious about it. "Sorry for adding additional time." ⏸ 0.8
- **RYAN** `deadpan` *(an observation he's proud of, but doesn't sell)*: When you think about it, the game called in sick. Twice.
- **MAYA** `dry`: And nobody asked it for evidence.
- **RYAN** `under_breath` *(quietly, with real feeling; to himself)*: Nobody asked it for evidence.

### SCENE 6 — THE PAPERWORK
*11:48 pm. Maya comes back from the kitchen with tea. Ryan is at the table with printed pages, a highlighter, and the company staff handbook, bristling with coloured sticky tabs.*
**Atmosphere:** late-night legal prep. Maya is quietly astonished.

- **MAYA** `curious`: Have you printed the internet?
- **RYAN** `deadpan` *(not looking up)*: You can't highlight a website.
*He holds up a page.*
- **RYAN** `research`: In the UK you can self-certify for up to seven days. No fit note.
- **MAYA** `dry`: Seven days.
- **RYAN** `deadpan` *(modest)*: I only need one. I'm not greedy.
- **MAYA** `curious`: And America?
- **RYAN** `research`: No national law. Most private-sector workers don't get paid sick days unless their state or their employer gives them. So it depends where you live, and who you work for.
*He taps the handbook.*
- **RYAN** `rationalising`: Which is why I've read this.
- **MAYA** `curious` *(micro-pause before the noun; processing, not mocking)*: You've read the... staff handbook.
- **RYAN** `deadpan`: Twice.
- **MAYA** `curious`: How long did that take?
- **RYAN** `deadpan` *(checks his watch; answers like a timesheet)*: About three hours. ⏸ 2.0
*Maya nods slowly. Sips her tea. Says nothing. Goes back to the sofa.*

### SCENE 7 — THE EPIDEMIC
*The sofa. Ryan, energised, scrolls news on his phone. Maya half-watches TV.*
**Atmosphere:** quick and light. It should run under a minute.

- **RYAN** `research`: When the last one came out in 2013, so many people went off sick it got a name. GTA flu.
- **MAYA** `dry`: Catchy.
- **RYAN** `research`: A survey says nine hundred thousand Brits are going to pretend to be sick tomorrow.
- **MAYA** `curious`: How many people did they ask?
- **RYAN** `deadpan` *(scrolls; finds it)*: ...A thousand. ⏸ 1.2
*Maya just looks at him. No line needed.*
- **RYAN** `research`: There's also a figure saying it'll cost the American economy a billion dollars.
- **MAYA** `curious`: Says who?
- **RYAN** `research` *(reading; enthusiasm draining as he goes)*: One article. Spanish TV, last summer... The Guardian calls the maths "back-of-the-napkin." ⏸ 0.8
- **RYAN** `deflated` *(genuinely a little disappointed)*: Shame. I liked being a threat to the economy.

### SCENE 8 — PRECEDENT
*Midnight. Ryan's bedroom, lights off. Ryan in bed, face lit by his phone. Maya in the doorway, brushing her teeth.*
**Atmosphere:** sleepy and low-volume. One last argument before bed.

- **RYAN** `research` *(quietly; late-night voice)*: In Japan, in the nineties, Dragon Quest had so many kids skipping school and adults calling in sick that they moved the releases to Saturdays.
- **MAYA** `distracted` *(toothbrush in)*: Mm.
- **RYAN** `earnest`: A whole country rearranged itself around a game.
- **MAYA** `dry` *(takes the toothbrush out)*: Or they rearranged the game around the country. ⏸ 1.0
*Ryan thinks about this.*
- **RYAN** `rationalising`: Rockstar didn't do that.
- **MAYA** `dry`: Rockstar picked a Thursday.
- **RYAN** `deadpan`: It's a test.
- **MAYA** `distracted`: Goodnight, Ryan.
*She switches off the hall light. In the dark, his phone shows the alarm he's just set: **6:00 — CALL DANA (sound ill)***

### SCENE 9 — THE CALL
*Thursday, 6:01 am. Ryan sits up in bed in a hoodie, the duvet arranged around him. A box of tissues and a glass of water are set carefully on the bedside table, staged for a phone call nobody can see. The laptop beside him: **GTA VI — Downloading 3% · 11 hrs remaining.***
**Atmosphere:** a performance under pressure. Ryan's control slips line by line, and he never panics. Dana is just a normal manager on a normal morning.

- **RYAN** `fake_ill` *(clears throat first)*: Hi, Dana. It's Ryan.
- **DANA (V.O.)** `professional` *(keyboard clatter under her)*: Ryan. Hi.
- **RYAN** `fake_ill`: Just wanted to let you know I'm feeling a little under the weather.
- **DANA** `concerned`: Oh no. What is it?
- **RYAN** `fake_ill` *(listing symptoms he rehearsed)*: Flu, I think. Headache. Fatigue... Very sudden.
*The download ticks to 4%.*
- **DANA** `concerned`: Right. Rest up. Anything urgent you need to hand over?
*Ryan looks at the laptop.*
- **RYAN** `fake_ill`: Nothing that can't wait.
- **DANA** `professional` *(brightening; it's a small thing)*: Great. Actually, could you just send the deck over before you log off? I'll take the client through it at two.
*Ryan closes his eyes. Insert: **Q4_Client_Deck_v2 — last edited Monday.***
- **RYAN** `formal` *(the croak slips for a word)*: Of course.
- **DANA** `professional`: And the revised budget.
- **RYAN** `formal`: Naturally.
- **DANA** `professional` *(no extra weight; just the list)*: And the client notes. And if you could update the tracker, that'd be amazing.
*Slowly, Ryan pulls the laptop closer, minimises the download and opens a spreadsheet.*
- **RYAN** `under_breath` *(to himself, forgetting he's on the phone)*: I'm beginning to regret being such a good employee.
- **DANA** `professional`: Sorry?
- **RYAN** `fake_ill` *(snaps back into the croak; one small cough)*: Fever. I'm delirious.
- **DANA** `concerned`: Feel better.
*Click. Alone, Ryan opens Q4_Client_Deck_v2. It's half finished. Hold 1.5 s.*

### SCENE 10 — WORKING FROM BED
*Thursday, 9:20 am. Kitchen table. Ryan is wrapped in the duvet, typing fast. The work chat pings every few seconds. Maya wanders past in pyjamas and slippers, coffee in hand, in no hurry at all. The camera doesn't linger on her.*
**Atmosphere:** relatable work-from-sickbed drudgery. Ryan is tired. Maya is on holiday, though nobody says so.

- **MAYA** `amused` *(passing by)*: How's the flu?
- **RYAN** `defeated` *(not looking up)*: Productive.
*Ping.*
- **RYAN** `under_breath` *(reading)*: "Thanks, Ryan. One more thing." ⏸ 0.6
*He glances at the download window: **14% · 6 hrs remaining.** As he watches, it changes to **7 hrs remaining.***
- **RYAN** `deadpan` *(quiet disbelief)*: It went up.
- **MAYA** `curious`: What did?
- **RYAN** `defeated`: The time. I've been ill all morning, and it's further away than when I started.
*Ping. Dana: **"Can you dial into the 10? Camera on if you're up to it 🙂"** He reads it twice.*
- **RYAN** `rationalising` *(working it through, slowly)*: If I dial in, I have to be ill. For an hour. On camera. ⏸ 1.5
*Long pause. He looks at the deck, the budget, the chat, the download.*
- **RYAN** `deadpan` *(quiet; arriving at the truth for the wrong reason)*: It'd be less work to go in.
*He closes the laptop and stands, duvet still on his shoulders. Maya sips her coffee.*
- **MAYA** `dry` *(purely practical)*: Take the duvet off first.
*He looks down. Takes it off. Leaves. Maya puts her feet up on the coffee table, picks up the TV remote and settles in. On-screen clock: **9:24 — Thursday.***

### SCENE 11 — THE REALITY
*9:58 am. The office. The lift doors open on Ryan.*
*Silence: no music, just room tone. Rows of empty desks, chairs pushed in, one monitor running a screensaver, the printer blinking.*
*He walks to his desk slowly and sits. Two full seconds of nothing.*
**Atmosphere:** an eerie hush. Ryan barely speaks, and the screens tell the story.

*His phone buzzes. The team chat, in order:*
- **Ryan (6:02):** Feeling under the weather today, will be mostly offline.
- **Dana (7:02):** Not feeling great. Taking a sick day.
- **Priya (7:15):** Same, sorry all.
- **Tom (7:31):** Woke up with a fever.
- **Leo (7:48):** Working from home today, might be patchy.

*He reads the whole thing. Scrolls back to the top, to his own message, the first one. Beat.*
- **RYAN** `deadpan` *(almost emotionless)*: Interesting. ⏸ 1.0

*An email: **From: Dana · Subject: Quick favour.***
*"Ryan — just saw you badged in, so glad you're feeling better! Since you're the only one in, could you chair the 10am and take the client at 2? Thanks for stepping up."*
*A second email, immediately: **Subject: Acting Team Lead (effective today, until further notice)***
*Ryan looks at it, then around the empty office, then back.*
- **RYAN** `under_breath` *(quiet, almost to the email)*: I've accidentally been promoted by the flu. ⏸ 0.8

*He opens the calendar: **Nine meetings. Three deadlines. Client presentation — 2:00 pm.** It's the deck.*
*His phone buzzes. **MAYA:** How's your day off?*
*He types. We read it as he types it. No V.O.:*
**RYAN:** Apparently, I'm the only person in the country who isn't sick.
*Maya's typing dots appear. They stop. Nothing comes.*
*Calendar reminder: **Team Sync — starting now (you are the host).** He clicks Join. No line.*

### SCENE 12 — THE 10 AM MEETING
*A glass meeting room. Ryan alone at the end of a table for twelve. On the laptop, a video call of black tiles, cameras off: Dana, Priya, Tom, Leo.*
**Atmosphere:** Ryan runs a completely normal meeting. Everyone else is clearly doing something else. The comedy comes from his professionalism, not from the sound effects.

- **RYAN** `formal` *(standard meeting voice)*: Morning, everyone. Thanks for joining. ⏸ 1.0
*Silence. A thumbs-up reaction floats up from Priya's tile. Ryan nods at it.*
- **RYAN** `formal`: Let's go round with updates. Priya? ⏸ 1.2
*Priya's tile shows a small "Away" clock.*
- **RYAN** `formal`: Tom?
- **TOM** `distracted` *(muffled; unmutes)*: Yeah, nothing from me, mate.
*Behind his voice, faintly, an engine revving hard. His tile mutes.*
- **RYAN** `deadpan` *(utterly sincere)*: Thanks, Tom. Get well soon.
*Dana's tile switches to **"Dana is presenting."** For half a second the shared screen shows the GTA VI main menu. Then: **"Dana stopped sharing."***
*Ryan looks into his webcam. A long, perfectly neutral pause, about 2 s.*
- **RYAN** `deadpan`: Lovely. Let's take the rest of the agenda offline.
*He ends the call, sits back and looks out at forty empty desks.*
*Time-lapse: the light moves across the empty office. Clock: **2:00 pm** (Ryan presenting the deck alone to a client call) → **4:21 pm.***
*His phone buzzes: **GTA VI is ready to play.** Directly beneath it slides in: **Reminder: Client follow-up — 4:30 pm (you are the host).***
*He looks at both. He puts the phone face down.*

### SCENE 13 — THE ANNUAL LEAVE
*Evening. Ryan lets himself into the flat, tie loose, carrying the printed client presentation he delivered alone. The game fills the flat: a car chase. Maya is on the sofa, feet up, controller in hand, snacks laid out. GTA VI is on the TV. She's clearly been there for a while. Ryan stops in the doorway.*
**Atmosphere:** Maya is completely relaxed and Ryan is drained. Nobody gloats, and nobody explains.

- **RYAN** `defeated`: You're playing it.
- **MAYA** `distracted` *(eyes on the screen)*: Mm.
- **RYAN** `curious`: You're not at work.
- **MAYA** `distracted`: I'm on annual leave. ⏸ 1.0
- **RYAN** `curious` *(quiet)*: Since when?
- **MAYA** `dry` *(no triumph at all)*: September. I booked it the day they announced the date. ⏸ 1.0
*Ryan processes this.*
- **RYAN** `deadpan` *(checking the logic)*: It wasn't sick leave.
- **MAYA** `dry`: No. That's for when you're ill. ⏸ 1.0
*He sits down beside her, very slowly. Without looking away from the screen, she passes him the second controller. He doesn't take it. He takes out his phone and opens the HR portal.*
- **RYAN** `defeated` *(quiet)*: How do you—
- **MAYA** `dry` *(eyes on the game)*: There's a form.
*He fills it in. We read over his shoulder: Reason for leave: **Holiday.** Submit.*
*A soft notification tick, then: **"Request declined. You are the only available cover for: Acting Team Lead."** Hold 2 s.*
*Maya un-pauses the game. Sirens.*
- **RYAN** `under_breath` *(very quietly)*: I think I'm coming down with something. ⏸ 0.5
- **MAYA** `deadpan` *(no smile; no change in volume; she's been waiting all day to say it)*: There's still time.
*Cut to black.*

### END CARD
- **MAYA (V.O.)** `dry`: Ryan Figures It Out. If you're watching this at work today... get well soon.

---

## PART 4 — THE REEL (native 9:16, ~50 s)
*Natively vertical framing: tight singles, faces in the upper third, screens filling the frame. Burned-in captions throughout.*

**0:00–0:03 — HOOK (silent, readable)**
*A tight, full-frame shot of the laptop desktop:*
`Q4_Client_Deck_v2.pptx — last edited Monday`
`WHY_THURSDAY.pptx — last edited 2 minutes ago`
*The cursor double-clicks WHY_THURSDAY. Top caption: **GTA 6 is out tomorrow. Ryan has prepared.***

**0:03–0:17 — THE PLAN** *(alternating tight singles. Maya barely looks up.)*
- **RYAN** `rationalising`: I've been looking into taking tomorrow off.
- **MAYA** `distracted`: You have annual leave.
- **RYAN** `rationalising`: Yes... But that's for holidays.
- **MAYA** `curious`: And tomorrow?
- **RYAN** `deadpan`: Is a medical situation.
- **MAYA** `dry`: You're not ill.
*Hold on Ryan for one beat. He keeps typing.*
- **RYAN** `deadpan`: Not yet... There's still time. ⏸ 0.8
*Maya slowly lowers her book. Cut.*

**0:17–0:38 — THE CALL** *(caption: **6:01 AM**. Ryan sits up in bed; tissues and water arranged like a stage set. Laptop: **DOWNLOADING 3%**.)*
- **RYAN** `fake_ill`: Hi, Dana. I'm feeling a little under the weather.
- **DANA (V.O.)** `concerned`: Oh no. Rest up.
- **DANA** `professional`: Could you just send the deck before you log off?
*Insert: **last edited Monday.** Ryan closes his eyes.*
- **RYAN** `formal`: Of course.
- **DANA** `professional`: And the revised budget.
*Close on the laptop: his finger minimises the download.*
- **RYAN** `formal`: Naturally.
- **DANA** `professional`: And the client notes?
- **RYAN** `under_breath`: I'm beginning to regret being such a good employee.
- **DANA** `professional`: Sorry?
- **RYAN** `fake_ill`: Fever. I'm delirious.

**0:38–0:46 — IT BACKFIRES** *(no dialogue; room tone only)*
- The lift doors open. An empty office. Silence. Ryan, small in the frame. 2 s.
- Close on his phone. An email slides in: **Subject: Acting Team Lead (effective today, until further notice).**
- Push in on Ryan's face: completely still, blinking once. Freeze.

**0:46–0:52 — CLIFFHANGER + CTA**
- **On screen:** *He called in sick at 6:02.* → beat → *By ten, he was running the office.*
- **MAYA (V.O.)** `dry`: It gets worse. Full episode's on YouTube.
- *End frame: **Ryan Figures It Out** · link in bio.*

> Why it ends here: the reel shows that the plan backfired (the empty office and the email) but not *why*. The team chat, the meeting and Maya's leave stay in the episode.

---

## PART 5 — DIRECTOR'S NOTES

**Keeping it from going theatrical:**
1. **No reaction shots that "sell" a joke.** Maya's looks are neutral attention, not eye-rolls.
2. **Ryan never smiles at his own lines.** The voice tags steer every take away from a grin. In the episode builder, each `deadpan`, `rationalising` and `research` line gets the animation acting "speaks seriously with a neutral face, no smile".
3. **Cut after the audience gets it, not after the line.** Holds are written in (⏸). Respect them, and don't add more.
4. **Silence is a shot.** The empty office (Sc 11), Maya's nod (Sc 6), the decline (Sc 13) and the Monday file (Sc 3) are held frames, and each is part of the comedy.
5. **Sound effects stay naturalistic and quiet:**
   - the engine behind Tom;
   - the car chase on Maya's TV;
   - a soft notification tick.
   No stings on punchlines.

**The visual moments that matter most (build these screen inserts first):**
1. **The two-file desktop** (Sc 3, reel hook): the setup for everything.
2. **The download bar**, with the time remaining going *up* (Sc 10) and "ready to play" at 4:21 under the 4:30 reminder (Sc 12).
3. **The empty office**, then the team chat with Ryan's 6:02 message at the top (Sc 11).
4. **Dana's half-second GTA screen-share** (Sc 12).
5. **"Request declined. You are the only available cover"** (Sc 13).
6. **The notepad:** *Australia (Dana?)*, then the RISKS→STRENGTHS arrow, then the crossed-out "Book flu" page (Sc 4–5).
7. **The props:** tissues and water staged for a phone call (Sc 9), and Maya's pyjamas at 9:24 (Sc 10).

**Voice production notes:**
- **Tags are machine instructions.**
  - For Ryan, each tag picks a written direction in `library/voices/benny/delivery.json`. The new profiles are `deadpan`, `rationalising`, `earnest`, `research`, `fake_ill`, `formal`, `awkward`, `under_breath`, `defeated` and `deflated`.
  - For Maya, Dana and Tom, each tag sets Chatterbox expressiveness and pitch movement. The new styles are `deadpan`, `dry`, `amused`, `curious`, `distracted`, `professional`, `concerned` and `tired`.
  - Each line still gets 3–4 takes, and the one that best fits its tag is kept automatically.
- **Ryan's base direction changed** from "charismatic… lively" to "an understated workplace sitcom; he takes himself seriously and never performs a joke". His voice identity (the "Ryan" preset) is unchanged.
- **Accent:** the locked voices are American-accented. The British flavour comes from the writing and the understatement, not the accent.
- **Tom** uses an existing library voice with a muffled, call-quality filter. **Dana** uses the existing `dana` voice, which is already designed as dry, low-to-mid and unhurried.
- **Before the full render**, a 2-minute voice test of ~12 key lines (all the deadpan beats plus the call) confirms the tags work. Fixes then happen in the tags, not by re-rendering scenes.

**Fact check:** unchanged from v2. Every claim is still in the episode, and all remain sourced:
- release date and the 13 years;
- prices;
- GTA V sales and the $1bn record;
- Sensor Tower pre-orders;
- the Guardian headline;
- Zelnick's April joke;
- the Fair Work Ombudsman;
- GTA flu;
- the 900k-from-1,000 survey;
- the $1bn claim's single source and "back-of-the-napkin";
- Dragon Quest;
- $60 → ~$85;
- the delay dates and Rockstar's apology;
- UK self-certification;
- US sick pay.

*Wording change:* "pretend to be sick" stays as the survey's claim, and Ryan presents it as "a survey says".
