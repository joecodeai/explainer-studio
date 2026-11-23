"""IndexTTS-2.5 worker (run inside engines/index-tts with `uv run`): Maya's own reference voice + per-line tone.
  uv run python ../../tools/maya_index_gen.py <jobs.json>
jobs: [{text, ref, out, emo_text?, emo_vector?, emo_alpha?, seed?}]
"""
import json, os, sys, random
import numpy as np, torch

sys.path.insert(0, os.getcwd())
from indextts.infer_v2_5 import IndexTTS2


def main(path):
    jobs = json.load(open(path))
    need_text = any(j.get("emo_text") for j in jobs)
    tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints", use_bf16=True, use_qwen_emo=need_text)
    for j in jobs:
        s = int(j.get("seed", 1234)); torch.manual_seed(s); random.seed(s); np.random.seed(s)
        kw = {}
        if j.get("emo_text"): kw.update(use_emo_text=True, emo_text=j["emo_text"], emo_alpha=j.get("emo_alpha", 0.6))
        elif j.get("emo_vector"): kw.update(emo_vector=j["emo_vector"], emo_alpha=j.get("emo_alpha", 1.0))
        tts.infer(spk_audio_prompt=j["ref"], text=j["text"], output_path=j["out"], lang="EN", verbose=False, text_normalization=False, **kw)
        print("idx", os.path.basename(j["out"]), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
