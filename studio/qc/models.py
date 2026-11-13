"""Lazy-loaded local inspection models (GPU when available, CPU fallback). Call free() to release VRAM.

  ocr(img)              Florence-2-large OCR with boxes  -> [(text, (x0,y0,x1,y1))]
  detect(img, query)    GroundingDINO zero-shot boxes    -> [(score, label, (x0,y0,x1,y1))]
  segment(img, boxes)   SAM 2.1 masks for box prompts    -> [bool HxW]
  embed(imgs)           SigLIP2 image embeddings (L2-normalised) -> np.ndarray
  asr(wav_or_array)     faster-whisper small.en          -> [(word, start, end)]
"""
import gc, os
import numpy as np
from PIL import Image

_M = {}
DEV = "cuda" if os.environ.get("QC_CPU") != "1" else "cpu"
try:
    import torch
    if not torch.cuda.is_available(): DEV = "cpu"
except Exception:
    DEV = "cpu"


def _rgb(img):
    if isinstance(img, str): img = Image.open(img)
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255)); bg.paste(img, mask=img.split()[-1]); return bg
    return img.convert("RGB")


def free(*names):
    for k in list(_M):
        if not names or k in names: del _M[k]
    gc.collect()
    try:
        import torch; torch.cuda.empty_cache()
    except Exception: pass


# ---------------------------------------------------------------- OCR
def ocr(img):
    import torch
    from transformers import AutoProcessor, Florence2ForConditionalGeneration
    if "florence" not in _M:
        mid = "florence-community/Florence-2-large"
        _M["florence"] = (AutoProcessor.from_pretrained(mid),
                          Florence2ForConditionalGeneration.from_pretrained(mid, torch_dtype=torch.float16 if DEV == "cuda" else torch.float32).to(DEV).eval())
    proc, model = _M["florence"]
    im = _rgb(img)
    x = proc(text="<OCR_WITH_REGION>", images=im, return_tensors="pt").to(DEV, model.dtype)
    with torch.no_grad():
        ids = model.generate(input_ids=x["input_ids"], pixel_values=x["pixel_values"], max_new_tokens=512, num_beams=3, do_sample=False)
    txt = proc.batch_decode(ids, skip_special_tokens=False)[0]
    r = proc.post_process_generation(txt, task="<OCR_WITH_REGION>", image_size=im.size)["<OCR_WITH_REGION>"]
    out = []
    for t, q in zip(r.get("labels", []), r.get("quad_boxes", [])):
        t = t.replace("</s>", "").replace("<s>", "").strip()
        if t:
            xs, ys = q[0::2], q[1::2]
            out.append((t, (min(xs), min(ys), max(xs), max(ys))))
    return out


# ---------------------------------------------------------------- detection
def detect(img, query, th=0.3):
    import torch
    from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
    if "gdino" not in _M:
        mid = "IDEA-Research/grounding-dino-base"
        _M["gdino"] = (AutoProcessor.from_pretrained(mid), AutoModelForZeroShotObjectDetection.from_pretrained(mid).to(DEV).eval())
    proc, model = _M["gdino"]
    im = _rgb(img)
    x = proc(images=im, text=query, return_tensors="pt").to(DEV)
    with torch.no_grad(): o = model(**x)
    r = proc.post_process_grounded_object_detection(o, x.input_ids, threshold=th, text_threshold=th, target_sizes=[im.size[::-1]])[0]
    labels = r.get("text_labels", r.get("labels"))
    return sorted([(float(s), str(l), tuple(float(v) for v in b)) for s, l, b in zip(r["scores"], labels, r["boxes"])], reverse=True)


# ---------------------------------------------------------------- segmentation
def segment(img, boxes):
    import torch
    from transformers import Sam2Model, Sam2Processor
    if not boxes: return []
    if "sam" not in _M:
        mid = "facebook/sam2.1-hiera-large"
        _M["sam"] = (Sam2Processor.from_pretrained(mid), Sam2Model.from_pretrained(mid).to(DEV).eval())
    proc, model = _M["sam"]
    im = _rgb(img)
    x = proc(images=im, input_boxes=[[list(b) for b in boxes]], return_tensors="pt").to(DEV)
    with torch.no_grad(): o = model(**x, multimask_output=False)
    m = proc.post_process_masks(o.pred_masks.cpu(), x["original_sizes"])[0]
    return [np.asarray(mm[0] > 0) for mm in m]


# ---------------------------------------------------------------- embeddings
def embed(imgs):
    import torch
    from transformers import AutoModel, AutoProcessor
    if "siglip" not in _M:
        mid = "google/siglip2-base-patch16-256"
        _M["siglip"] = (AutoProcessor.from_pretrained(mid), AutoModel.from_pretrained(mid).to(DEV).eval())
    proc, model = _M["siglip"]
    x = proc(images=[_rgb(i) for i in imgs], return_tensors="pt").to(DEV)
    with torch.no_grad(): e = model.get_image_features(**x)
    e = e / e.norm(dim=-1, keepdim=True)
    return e.float().cpu().numpy()


# ---------------------------------------------------------------- speech
def asr(audio, sr=None, prompt=None):
    """audio: path or float32 mono array (any sr). Returns (text, [(word, start, end)])."""
    import soundfile as sf, torch, torchaudio
    from faster_whisper import WhisperModel
    if "whisper" not in _M:
        _M["whisper"] = WhisperModel("small.en", device=DEV, compute_type="float16" if DEV == "cuda" else "int8")
    if isinstance(audio, str):
        audio, sr = sf.read(audio, dtype="float32")
    if audio.ndim > 1: audio = audio.mean(1)
    if sr != 16000:
        audio = torchaudio.functional.resample(torch.from_numpy(np.ascontiguousarray(audio)), sr, 16000).numpy()
    segs, _ = _M["whisper"].transcribe(audio, beam_size=5, word_timestamps=True, initial_prompt=prompt)
    words = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or [])]
    return " ".join(w[0] for w in words), words
