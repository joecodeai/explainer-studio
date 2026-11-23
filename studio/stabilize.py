"""Lock the camera on generated conversation shots.

LTX tends to creep the camera in during a shot, and chaining shots (each starting from the last frame of the previous one)
compounds it. We track the background against the scene's reference still (ORB features + RANSAC similarity transform),
warp every frame back into the reference framing (anything the zoomed frame no longer shows is filled from the reference
still), then crop a fixed window. Result: a steady medium two-shot whatever the model did, and a "re-widened" last frame to
start the next shot from, so drift can never accumulate.
"""
import subprocess
import numpy as np
import cv2


def _track(ref_gray, frame_gray, orb, ref_kp, ref_des):
    kp, des = orb.detectAndCompute(frame_gray, None)
    if des is None or ref_des is None or len(kp) < 12: return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    mt = sorted(bf.match(ref_des, des), key=lambda m: m.distance)[:400]
    if len(mt) < 12: return None
    src = np.float32([ref_kp[m.queryIdx].pt for m in mt]); dst = np.float32([kp[m.trainIdx].pt for m in mt])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=3000)
    if M is None or inl is None or inl.sum() < 10: return None
    return M                                      # ref -> frame


def _read(path):
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 24; frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    return frames, fps


def stabilize(video, ref_png, out, crop, size=(1920, 1080), smooth=5):
    """video: LTX shot; ref_png: the scene's reference still (same size as the video frames);
    crop: (x, y, w, h) window in reference coordinates for the final framing. Writes `out` (no audio) and returns
    (out, rewidened_last_frame_png)."""
    frames, fps = _read(video)
    if not frames: raise RuntimeError(f"no frames in {video}")
    H, W = frames[0].shape[:2]
    ref = cv2.resize(cv2.imread(ref_png), (W, H))
    orb = cv2.ORB_create(3000)
    rg = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY); rkp, rdes = orb.detectAndCompute(rg, None)
    Ms, last = [], np.float32([[1, 0, 0], [0, 1, 0]])
    for f in frames:
        M = _track(rg, cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), orb, rkp, rdes)
        last = M if M is not None else last; Ms.append(last)
    # smooth the transform over time (no jitter from per-frame estimation noise)
    A = np.array(Ms); k = max(1, smooth)
    pad = np.concatenate([A[:1].repeat(k, 0), A, A[-1:].repeat(k, 0)])
    A = np.array([pad[i:i + 2 * k + 1].mean(0) for i in range(len(Ms))])
    x, y, w, h = crop
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{size[0]}x{size[1]}",
                             "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", out], stdin=subprocess.PIPE)
    lastw = None
    for f, M in zip(frames, A):
        inv = cv2.invertAffineTransform(M)                       # frame -> ref
        # outside what the model still shows: stretch the frame's own edge (pasting the reference still there left a visible seam)
        full = cv2.warpAffine(f, inv, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        lastw = full
        win = full[y:y + h, x:x + w]
        proc.stdin.write(cv2.resize(win, size, interpolation=cv2.INTER_CUBIC).tobytes())
    proc.stdin.close(); proc.wait()
    last_png = out.rsplit(".", 1)[0] + "_last.png"
    cv2.imwrite(last_png, lastw)
    return out, last_png


def scale_of(M):
    return float(np.sqrt(abs(np.linalg.det(M[:, :2]))))
