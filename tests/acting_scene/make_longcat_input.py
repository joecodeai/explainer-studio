import json, math, sys
T = sys.argv[1]
sc = json.load(open(f"{T}/scene.json"))["beats"]; tl = json.load(open(f"{T}/timeline.json"))
FPS, NF, NC = 25, 93, 13
dur = tl["duration"]; n_frames = int(dur * FPS); n_seg = 1 + max(0, math.ceil((n_frames - NF) / (NF - NC)))
BASE = ("Static camera, medium two-shot in a cosy Japanese ramen shop. A young man with curly dark hair in an orange hoodie (left) and a young "
        "woman with long wavy dark hair in an olive green jacket (right) stand facing each other and talk; they look at each other, natural "
        "eye contact. Polished 2D anime-style animated series, expressive faces, natural subtle acting, natural hand gestures, the listener "
        "reacts with facial expressions and keeps her or his mouth closed. ")
segs = []
for k in range(n_seg):
    t0 = (k * (NF - NC) + (NC if k else 0)) / FPS; t1 = (k * (NF - NC) + NF) / FPS
    ov = []
    for b, e in zip(sc, tl["timeline"]):
        o = min(t1, e["end"] + 0.3) - max(t0, e["start"])
        if o > 0: ov.append((e["start"], o + (5 if b.get("silent") else 0), b))   # a silent acting beat always gets its segment
    if not ov: ov = [(0, 1, sc[-1])]
    ov = sorted(sorted(ov, key=lambda x: -x[1])[:2], key=lambda x: x[0])          # the two beats that fill this segment, in order
    segs.append(BASE + " Then ".join(f"{b['act']}; {b['react']}" for _, _, b in ov) + ".")
NEG = ("photorealistic, live action, 3D render, blurred details, subtitles, text, watermark, worst quality, low quality, JPEG artifacts, ugly, "
       "extra fingers, poorly drawn hands, poorly drawn faces, deformed, disfigured, misshapen limbs, fused fingers, still picture, frozen, "
       "both people talking at the same time, camera zoom, camera shake, messy background, three legs, many people in the background")
inp = {"prompt": segs[0], "segment_prompts": segs, "negative_prompt": NEG, "cond_image": f"{T}/cond.png",
       "cond_audio": {"person1": f"{T}/track_benny.wav", "person2": f"{T}/track_maya.wav"}, "audio_type": "para",
       "bbox": {"person1": [40, 200, 768, 600], "person2": [50, 680, 768, 1000]}}
json.dump(inp, open(f"{T}/longcat_input.json", "w"), indent=1)
print("segments", n_seg, "frames", n_frames); [print(i, s[len(BASE):][:150]) for i, s in enumerate(segs)]
