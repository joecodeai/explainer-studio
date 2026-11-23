"""Build H3 bake-off inputs from the yen acting scene: beat-shot keyframes, audio slices, H3-format prompts."""
import json, subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SC = ROOT / "tests/acting_scene"
OUT = Path(__file__).parent / "in"
OUT.mkdir(exist_ok=True)
tl = json.load(open(SC / "timeline.json"))["timeline"]
acts = json.load(open(SC / "scene.json"))["beats"]

RYAN = ("<Subject 1> is the young man in <Picture 1>, whose face and hair follow <Picture 2> exactly: tousled curly dark-brown hair, "
        "warm brown eyes, fair skin with a warm peachy undertone, a burnt-orange zip hoodie over a plain white T-shirt, a thin dark crossbody strap.")
MAYA = ("<Subject 2> is the young woman in <Picture 1>, whose face and hair follow <Picture 3> exactly: long wavy dark-brown hair, warm brown eyes, "
        "fair skin with a warm peachy undertone, small gold hoop earrings, an olive-green shirt jacket over a cream top.")
NOREF = "Do not carry over the white backgrounds, the crossed-arm poses or any lettering of <Picture 2> and <Picture 3>."
STYLE = ("2D hand-drawn anime cartoon exactly matching <Picture 1>: clean ink line art, flat cel shading, warm lantern light inside a small "
         "Japanese ramen shop with cloth noren curtains and steaming pots behind the counter. Expressions are subtle and natural, never exaggerated.")
VOICE = {"benny": "<Subject 1> (S1), in a lively, warm young male voice,", "maya": "<Subject 2> (S2), in a calm, dry, warm female voice,"}
SUBJ = {"benny": "<Subject 1>", "maya": "<Subject 2>"}

# beat shots: (id, setup, line indices, start, end)
SHOTS = [("b1", "two_mc", [0, 1], 0.0, 9.29), ("b2", "two_mc", [2, 3], 9.29, 20.05),
         ("b3", "single_L", [4, 5], 20.05, 26.70), ("b4", "two_mc", [6, 7], 26.70, 34.29)]


def keyframes():
    c = Image.open(SC / "cond.png").convert("RGB")
    c.crop((145, 40, 1135, 590)).resize((864, 480), Image.LANCZOS).save(OUT / "kf_two_mc.png")
    c.crop((150, 30, 790, 386)).resize((864, 480), Image.LANCZOS).save(OUT / "kf_single_L.png")
    sheet = Image.open(ROOT / "library/show_refs/benny_maya_sheet.png").convert("RGB")
    sheet.crop((215, 0, 470, 505)).save(OUT / "ref_ryan.png")
    sheet.crop((205, 512, 465, 1024)).save(OUT / "ref_maya.png")


def prompt(setup, lines, t0):
    single = setup == "single_L"
    parts = [f"For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.", "",
             "subject_definitions:", RYAN, MAYA, NOREF, "", "integrated_multimodal_description:", STYLE]
    frame = ("[Shot 1] Medium close-up on <Subject 1> on the left, <Subject 2> partly visible at the right edge."
             if single else "[Shot 1] Medium two-shot, <Subject 1> on the left facing right, <Subject 2> on the right facing left.")
    parts.append(frame + " The camera holds a static shot with no zoom and no movement for the whole clip.")
    for i in lines:
        b, t = acts[i], tl[i]
        at = f"At 00:{t['start'] - t0:06.3f}, " if t["start"] - t0 > 0.2 else ""
        other = "maya" if b["spk"] == "benny" else "benny"
        if t.get("silent"):
            parts.append(f"{at}{b['act'].replace('the woman on the right', SUBJ['maya']).replace('the young man on the left', SUBJ['benny'])}, "
                         f"saying nothing, her lips completely closed. Meanwhile {b['react'].replace('the young man on the left', SUBJ['benny'])}.")
            continue
        act = b["act"].replace("the young man on the left", "").replace("the woman on the right", "").strip()
        parts.append(f"{at}{VOICE[b['spk']]} {act}, and says: <d>[English] {b['text']}</d> "
                     f"While {SUBJ[b['spk']]} speaks, {SUBJ[other]}'s lips remain completely closed: "
                     f"{b['react'].replace('the woman on the right', '').replace('the young man on the left', '').strip()}.")
    parts += ["", "overall_soundscape:", "Quiet ramen-shop room tone with a faint simmer of broth; no other voices.", "",
              "non_diegetic_music:", "N/A"]
    return "\n".join(parts)


def main():
    keyframes()
    for sid, setup, lines, t0, t1 in SHOTS:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SC / "mix.wav"), "-ss", f"{t0}", "-to", f"{t1}",
                        "-ar", "32000", "-ac", "2", str(OUT / f"{sid}.wav")], check=True)
        (OUT / f"{sid}.txt").write_text(prompt(setup, lines, t0))
        (OUT / f"{sid}.json").write_text(json.dumps({"setup": setup, "seconds": round(t1 - t0, 2),
                                                     "keyframe": str(OUT / f"kf_{setup}.png")}))
    print((OUT / "b2.txt").read_text())


main()
