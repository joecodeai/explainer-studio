"""Paths, model names and channel-wide style. Everything persistent lives under LIBRARY."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMFY_DIR = os.path.join(ROOT, "ComfyUI")
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")
LLM_URL = os.environ.get("LLM_URL", "http://127.0.0.1:1234/v1")       # LM Studio OpenAI-compatible server
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3.6-35b-a3b")
LMS = os.path.expanduser("~/.lmstudio/bin/lms")
LMSTUDIO_APP = os.environ.get("LMSTUDIO_APP", os.path.expanduser("~/Downloads/LM-Studio-0.4.16-2-x64.AppImage"))
NODE = os.path.join(ROOT, "bin", "node", "bin")
RHUBARB = next((os.path.join(ROOT, "bin", d, "rhubarb") for d in sorted(os.listdir(os.path.join(ROOT, "bin")))
                if d.lower().startswith("rhubarb")), "rhubarb") if os.path.isdir(os.path.join(ROOT, "bin")) else "rhubarb"
REMOTION = os.path.join(ROOT, "remotion")
PROJECTS = os.path.join(ROOT, "projects")
LIBRARY = os.path.join(ROOT, "library")
CHAR_LIB = os.path.join(LIBRARY, "characters_news")   # 2026-11-12 newsroom style; old cartoon set stays in library/characters
VOICE_LIB = os.path.join(LIBRARY, "voices")
SOUND_LIB = os.path.join(LIBRARY, "sounds")
BG_LIB = os.path.join(LIBRARY, "backgrounds_news")
TTS_DESIGN = os.path.join(ROOT, "models", "Qwen3-TTS-12Hz-1.7B-VoiceDesign")
TTS_BASE = os.path.join(ROOT, "models", "Qwen3-TTS-12Hz-1.7B-Base")

W, H, FPS = 1920, 1080, 30

# Channel name for the on-screen bug (top right); "" = no bug
BRAND = os.environ.get("EXPLAINER_BRAND", "")

# Channel look — one style string reused for every generated asset (consistency across videos)
ART_STYLE = ("clean modern editorial vector illustration, like a serious news explainer or magazine infographic, "
             "realistic adult proportions (normal-sized head, not chibi, not a caricature), calm composed expression, "
             "muted sophisticated colour palette (navy, slate, charcoal, warm grey, off-white, a touch of brick red), "
             "subtle flat shading, thin clean dark outlines, simple but detailed face with visible eyes and a clear mouth")
CHAR_SUFFIX = ("full body character standing, facing the viewer, MOUTH CLOSED (small simple closed mouth line), isolated on a transparent background, "
               "no text, no shadow, no ground")
BG_STYLE = ("clean modern editorial vector illustration background, like a serious news explainer, realistic perspective, "
            "muted sophisticated palette (navy, slate, warm grey, off-white, soft daylight), subtle depth, no people, no text, wide 16:9 composition, "
            "plenty of empty space in the lower middle for characters: open clear floor across the whole foreground, "
            "furniture and props only along the back wall and the far left/right edges, nothing in the lower centre, eye-level camera, "
            "absolutely no text, letters or writing on any sign, board, screen or paper")

# Narrator: designed once, then cloned from the saved reference so every video sounds the same
NARRATOR = {
    "name": "narrator",
    "design": ("A witty, warm male narrator in his thirties with a clear neutral English accent, conversational and fast-paced, "
               "dry humour, energetic but not shouty, like a popular history explainer YouTuber."),
    "language": "English",
}

POSES = ["neutral", "talk", "point", "arms_up", "shrug", "facepalm", "angry", "thinking", "happy", "surprised", "worried",
         "side_talk", "side_listen"]
for d in (PROJECTS, CHAR_LIB, VOICE_LIB, SOUND_LIB, BG_LIB):
    os.makedirs(d, exist_ok=True)
