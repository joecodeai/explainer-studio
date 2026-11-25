"""Voice sample for the hustle-culture script review (current voices: Maya lively lock +10%, Ryan lock)."""
from topics.wwc2035 import VOICE_REF
ERA = "modern"; M, R = "maya", "benny"; GAP, TEMPO = 0.4, 1.10; LANDSCAPE = True
L = [(M, "Somewhere right now, a man is standing next to a very clean car, telling you to wake up at four in the morning so you can be rich like him."),
     (M, "And if you watch until the end, he'll tell you exactly how he made his money. It was selling you this video."),
     (R, "He's not wrong. I'm still watching."),
     (M, "A year later, Jack Ma, the founder of Alibaba, said China's nine-nine-six schedule was a huge blessing. That's nine in the morning to nine at night, six days a week. A blessing in the same way a second mortgage is a fun surprise."),
     (R, "Seventy-two hours a week. I've had weeks like that. They're called holidays with my family."),
     (M, "That sounds great. Until you see the median, which is the person exactly in the middle. Two hundred dollars a month."),
     (R, "So the typical side hustle is a slightly nicer coffee budget."),
     (R, "So if you get up at four, you're basically tipsy by bedtime."),
     (M, "It's called survivorship bias. And it's the entire business model of the success video. You only ever hear from the guy who made it. Nobody films the morning routine of the guy whose dropshipping store sold three phone cases."),
     (R, "Passive income. Active losing."),
     (M, "The evidence is fairly boring. Work hard on things that matter. Rest on purpose. Sleep is not for the weak. Sleep is for people who'd like to still be productive on Thursday.")]
SHOTS = [dict(id=f"v{i:02d}", spk=s, tag="deadpan" if s == R else "narration", text=t, eng="still", kf="-") for i, (s, t) in enumerate(L)]
TAIL = 1.0
