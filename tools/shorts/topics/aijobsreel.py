"""Reel / Short for the AI-and-jobs debate video: the whole argument in ~75 s, native 9:16. Same facts and sources as topics/aijobs.py."""
from topics.aijobs import STYLE, ENV_STYLE, LOOK, CHARS, VOICE_REF, H3_REF_KF, P1
FOLDER = "Should AI Replace Workers"            # VIDEOS/<FOLDER>/...
ERA = "modern"
M, R = "maya", "benny"
GAP, TEMPO = 0.15, 1.10
LTX_WH = (512, 896)
SHOTS = [
 dict(id="q01", spk=M, eng="still", mv="in", sfx="quiet office, a tape measure clicking", refs=["worker", "robot"],
      text="If a robot could do your job for half the price, should your boss hire it? Before you answer, the robot is already measuring your desk.",
      kf="The woman from the first reference sitting at her office desk with her headset on, frozen mid-typing with wide alarmed eyes, while "
         "the robot from the second reference cheerfully measures the width of her desk with a long yellow tape measure. Exactly two characters.",
      mv_ltx="The woman keeps typing, then slowly turns her head to look at the robot behind her; the robot gives a small polite wave. " + P1),
 dict(id="q02", spk=M, eng="card", card=dict(big="40%", small="OF JOBS EXPOSED TO AI (IMF)", bg="#2E4A62", accent="#F2C14E"),
      sfx="quiet office hum",
      text="The IMF says about forty percent of jobs worldwide are exposed to AI. Exposed, not replaced. AI can do part of the job."),
 dict(id="q03", spk=M, eng="still", mv="in", sfx="old textile mill, looms clattering",
      text="The case for: power looms automated almost all the work of weaving cloth, and weaving jobs still grew, because cheap cloth meant people bought far more of it.",
      kf="A bright Victorian textile mill hall with long rows of big iron power looms and many simple weavers in aprons working at them, "
         "sunlight through tall windows."),
 dict(id="q04", spk=M, eng="still", mv="in", refs=["weaver"], sfx="quiet cottage, a fire crackling",
      text="The case against: the hand-loom weavers they replaced saw their pay collapse. The economy won. They didn't.",
      kf="The man from the reference sitting at a small cottage table counting a tiny pile of coins, looking worried, an empty plate in front "
         "of him. Exactly one person."),
 dict(id="q05", spk=M, eng="still", mv="in", refs=["robot"], sfx="phone line, muffled hold music, a frustrated sigh",
      text="Then there's Klarna. It said its AI assistant did the work of seven hundred agents, let its workforce shrink by a third, then admitted quality suffered and brought humans back.",
      kf="The robot from the reference wearing a headset at a call-centre desk, its screen face showing two confused dot eyes, a long tangled "
         "phone cord wrapped around its arms. Exactly one robot, no people."),
 dict(id="q06", spk=R, tag="deadpan", eng="h3", refs=["ryan", "ryan_face"],
      text="So the robots are coming. Slowly. And over budget.",
      kf="Vertical flat 2D vector illustration of the young man from the reference redrawn in a simple flat explainer style: thick curly dark "
         "brown hair, burnt-orange open hoodie over a white t-shirt, black crossbody strap, waist-up, standing in a simple flat cosy living "
         "room with a teal wall and a plant, holding a coffee mug, looking at camera with a flat expression. Exactly one person.",
      mv="The young man speaks flatly to camera, then takes a slow sip from the mug. Static camera, waist-up. Exactly one person; he keeps the "
         "same face, hair and hoodie."),
 dict(id="q07", spk=M, eng="card", card=dict(big="23%", small="WORTH AUTOMATING TODAY (MIT)", bg="#3C5A50", accent="#F2C14E"),
      sfx="quiet lab, computer fans humming",
      text="And often it isn't even cheaper. MIT found only about a quarter of the wages paid for visual tasks would be worth automating at today's prices."),
 dict(id="q08", spk=M, eng="still", mv="in", sfx="call centre, calm voices",
      text="The best results so far come from AI helping people. In one study, support agents with an AI assistant solved fourteen percent more problems per hour.",
      kf="A woman with a headset at her desk, with a tiny friendly robot sitting on her shoulder whispering into her ear, while she smiles "
         "and types confidently. Exactly one person."),
 dict(id="q09", spk=M, eng="ltx",
      text="So maybe the real question isn't whether it's cheaper. It's who pays the difference, and who keeps it. The full debate is on our channel.",
      kf="A simple big golden coin balanced on its edge on a wooden table between a robot's hand coming from the left and a person's hand "
         "coming from the right, both reaching for it, plain teal background.",
      mv="Both hands slowly reach towards the coin, the coin wobbles slightly on its edge. Static camera."),
]
THUMB = dict(text="CHEAPER|THAN YOU?", refs=["worker", "robot"],
             kf="Vertical: the woman from the first reference with her headset, shocked with her mouth wide open and hands on her cheeks, "
                "while the robot from the second reference sits smugly in her office chair wearing her headset and holding her coffee mug. "
                "Bright teal background. Exactly two characters.")
TAIL = 2.4
