import os, sys
from . import run

proj = os.path.abspath(sys.argv[1]); fix = "--no-fix" not in sys.argv


def rebuild(p):
    from .. import pipeline
    topic = open(os.path.join(p, "TOPIC")).read().strip()
    pipeline.make_video(topic, approve=True, run_qc=False, review=False)


ok, sc, F = run(proj, fix=fix, rebuild=rebuild)
print("PASS" if ok else "FAIL", sc)
