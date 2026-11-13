#!/usr/bin/env python3
"""Local AI explainer-video studio.

  ./make_video "topic or news URL" --minutes 6            # research + script, then stops for your review
  ./make_video "topic or news URL" --approve              # produce the video (resumes; cached stages are skipped)
  ./make_video "topic or news URL" --approve --rerender s07 s12   # re-render only those scenes
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import pipeline

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("topic")
ap.add_argument("--minutes", type=float, default=6)
ap.add_argument("--approve", action="store_true", help="script reviewed: produce the video")
ap.add_argument("--rerender", nargs="*", help="scene ids to force re-render")
a = ap.parse_args()
pipeline.make_video(a.topic, a.minutes, a.approve, a.rerender)
