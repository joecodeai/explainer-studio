"""Local LLM (Qwen3.6 via LM Studio). Loads on demand, unloads to free VRAM for image/video models."""
import json, os, re, subprocess, time
import requests
from . import config as C


def _lms(*args, check=False):
    return subprocess.run([C.LMS, *args], capture_output=True, text=True, check=check)


def loaded():
    try:
        return [m["id"] for m in requests.get(f"{C.LLM_URL}/models", timeout=5).json()["data"]]
    except Exception:
        return []


def ensure_loaded():
    if "Server: ON" not in _lms("status").stdout:
        if os.path.exists(C.LMSTUDIO_APP):        # headless LM Studio service
            subprocess.Popen([C.LMSTUDIO_APP, "--run-as-service"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            for _ in range(60):
                time.sleep(2)
                if "Server: ON" in _lms("status").stdout: break
        _lms("server", "start")
    out = _lms("ps").stdout
    if C.LLM_MODEL not in out:
        _lms("unload", "--all")
        r = _lms("load", C.LLM_MODEL, "--gpu", "max", "--context-length", "32768", "-y")
        if r.returncode != 0:
            raise RuntimeError(f"lms load failed: {r.stderr or r.stdout}")


def unload():
    _lms("unload", "--all")


def chat(messages, schema=None, temperature=0.7, max_tokens=12000, retries=3):
    """Returns text, or a parsed dict when `schema` (JSON-schema) is given. Validates & retries on bad JSON."""
    ensure_loaded()
    body = {"model": C.LLM_MODEL, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if schema:
        # Free-form JSON + our own validation: grammar-constrained decoding is CPU-bound and ~10x slower on big schemas.
        body["chat_template_kwargs"] = {"enable_thinking": False}      # (ignored by some LM Studio builds -> /no_think below)
        body["messages"] = messages = messages[:-1] + [{"role": messages[-1]["role"], "content": messages[-1]["content"] +
            "\n\nRespond with ONLY one JSON object (no markdown fences, no commentary) that matches this JSON schema:\n" + json.dumps(schema) + " /no_think"}]
    last = None
    for _ in range(retries):
        r = requests.post(f"{C.LLM_URL}/chat/completions", json=body, timeout=1800)
        r.raise_for_status()
        ch = r.json()["choices"][0]; msg_ = ch["message"]
        txt = msg_.get("content") or ""
        if not txt.strip():
            if ch.get("finish_reason") == "length":       # model spent the budget thinking: retry with more room
                body["max_tokens"] = min(32000, int(body["max_tokens"] * 2)); continue
            txt = msg_.get("reasoning_content") or ""
        txt = re.sub(r"<think>.*?</think>", "", txt, flags=re.S).strip()
        if not schema:
            return txt
        try:
            i = txt.find("{")
            out, _ = json.JSONDecoder().raw_decode(txt[i:] if i >= 0 else txt)   # first complete object; ignore trailing text
            missing = [k for k in schema.get("required", []) if k not in out]
            if missing:
                raise ValueError(f"missing keys {missing}")
            return out
        except Exception as e:
            last = e
            body["messages"] = messages + [{"role": "assistant", "content": txt[:2000]},
                                           {"role": "user", "content": f"That was not valid JSON ({e}). Reply with ONLY the JSON object."}]
    raise RuntimeError(f"LLM returned invalid JSON: {last}")
