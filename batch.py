#!/usr/bin/env python3
"""Batch production.
  ./batch scripts topics.txt     # research + script + local fact-check for every topic (stops before production)
  ./batch produce                # produce every project that has an APPROVED file and no final video yet (or is outdated)
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import pipeline, factcheck, config as C

def scripts(path, limit=None):
    done = 0
    for topic in [t.strip() for t in open(path) if t.strip() and not t.startswith("#")]:
        proj = pipeline.project_dir(topic)
        open(f"{proj}/TOPIC", "w").write(topic)
        if os.path.exists(f"{proj}/FACTCHECK.md"): continue
        t0 = time.time()
        try:
            pipeline.stage_script(proj, topic, float(os.environ.get("MINUTES", 6)))
            flags = factcheck.run(proj)
            pipeline.log(proj, f"BATCH script ready in {(time.time() - t0) / 60:.0f} min, {len(flags)} fact-check flag(s)")
            print("READY", proj, flush=True)
        except Exception as e:
            pipeline.log(proj, f"BATCH script FAILED: {e}")
        done += 1
        if limit and done >= limit: return

def produce():
    from studio import progress
    todo = [os.path.join(C.PROJECTS, d) for d in sorted(os.listdir(C.PROJECTS), key=lambda x: os.path.getmtime(os.path.join(C.PROJECTS, x)))
            if os.path.exists(os.path.join(C.PROJECTS, d, "APPROVED")) and not os.path.exists(os.path.join(C.PROJECTS, d, "DONE"))]
    progress.batch_start(todo)
    for proj in todo:
        try:
            topic = open(f"{proj}/TOPIC").read().strip()
            pipeline.make_video(topic, approve=True); open(f"{proj}/DONE", "w").write(time.ctime())
        except Exception as e:
            pipeline.log(proj, f"BATCH produce FAILED: {e}")

if __name__ == "__main__":
    if sys.argv[1] == "scripts": scripts(sys.argv[2])
    elif sys.argv[1] == "next": scripts(sys.argv[2], limit=1)      # one topic only
    elif sys.argv[1] == "redo":      # re-produce finished projects with the current pipeline + QC:  ./batch redo <project_dir>...
        from studio import progress
        projs = [os.path.join(C.PROJECTS, os.path.basename(p.rstrip("/"))) for p in sys.argv[2:]]
        progress.batch_start(projs)
        for proj in projs:
            try:
                pipeline.make_video(open(f"{proj}/TOPIC").read().strip(), approve=True)
                open(f"{proj}/DONE", "w").write(time.ctime())
            except Exception as e:
                pipeline.log(proj, f"BATCH redo FAILED: {e}"); progress.stage(proj, "done")
    else: produce()
