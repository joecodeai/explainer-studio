"""Minimal ComfyUI HTTP client: start server, queue API-format workflows, collect outputs, free VRAM."""
import json, os, shutil, subprocess, time, uuid
import requests
from . import config as C

_proc = None


def up():
    try:
        return requests.get(f"{C.COMFY_URL}/system_stats", timeout=3).ok
    except Exception:
        return False


def start():
    global _proc
    if up():
        return
    log = open(os.path.join(C.ROOT, "logs", "comfyui.log"), "a")
    env = dict(os.environ, PYTHONNOUSERSITE="1")
    _proc = subprocess.Popen([os.path.join(C.COMFY_DIR, ".venv", "bin", "python"), "main.py", "--listen", "127.0.0.1",
                              "--port", C.COMFY_URL.rsplit(":", 1)[1], "--disable-auto-launch"],
                             cwd=C.COMFY_DIR, stdout=log, stderr=log, env=env)
    for _ in range(180):
        if up():
            return
        time.sleep(1)
    raise RuntimeError("ComfyUI did not start; see logs/comfyui.log")


def free():
    if up():
        requests.post(f"{C.COMFY_URL}/free", json={"unload_models": True, "free_memory": True}, timeout=30)


def upload(path):
    start()  # a resumed run can upload before any run() call, so make sure the server is up
    with open(path, "rb") as f:
        r = requests.post(f"{C.COMFY_URL}/upload/image", files={"image": (os.path.basename(path), f)}, data={"overwrite": "true"})
    r.raise_for_status()
    return r.json()["name"]


def run(workflow, out_dir, prefix, timeout=3600):
    """Queue workflow, wait, copy every output file to out_dir/prefix_N.ext. Returns list of paths."""
    start()
    cid = str(uuid.uuid4())
    r = requests.post(f"{C.COMFY_URL}/prompt", json={"prompt": workflow, "client_id": cid})
    if not r.ok:
        raise RuntimeError(f"ComfyUI rejected workflow: {r.text[:1500]}")
    pid = r.json()["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = requests.get(f"{C.COMFY_URL}/history/{pid}").json()
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI error: {json.dumps(st.get('messages', []))[:1500]}")
            outs = []
            os.makedirs(out_dir, exist_ok=True)
            for node in h[pid]["outputs"].values():
                for key in ("images", "gifs", "videos", "audio"):
                    for it in node.get(key, []):
                        src = os.path.join(C.COMFY_DIR, it.get("type", "output"), it.get("subfolder", ""), it["filename"])
                        dst = os.path.join(out_dir, f"{prefix}_{len(outs)}{os.path.splitext(it['filename'])[1]}")
                        shutil.copy(src, dst); outs.append(dst)
            return outs
        time.sleep(1)
    raise TimeoutError("ComfyUI job timed out")


def nodes():
    return requests.get(f"{C.COMFY_URL}/object_info").json()
