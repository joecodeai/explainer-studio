"""Instagram/Shorts version of a finished short video: 1080x1920, the 16:9 video (side edges trimmed) centred over a blurred fill of
itself, a headline at the top (the video already carries its captions), plus INSTAGRAM_REEL.txt. Seconds, no LLM.

  python tools/make_vertical.py projects/<slug> "Headline text" "Caption text..." "#tag1 #tag2 ..."
"""
import json, os, subprocess, sys


def main(proj, headline, caption, tags):
    name = os.path.basename(proj.rstrip("/"))
    src, srt = os.path.join(proj, f"{name}.mp4"), os.path.join(proj, "subtitles.srt")
    out = os.path.join(proj, f"{name}_vertical.mp4")
    head = headline.replace("'", "’").replace(":", "\\:")
    style = ("FontName=DejaVu Sans,Bold=1,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,"
             "Shadow=0,Alignment=2,MarginV=70")
    words = head.split(); rows = [(head, 330)]
    if len(head) > 24:                             # two lines: split at the space closest to the middle
        cut = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(head) / 2))
        rows = [(" ".join(words[:cut]), 260), (" ".join(words[cut:]), 345)]
    vf = ("[0:v]split[a][b];"
          "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.12[bg];"
          "[b]scale=-2:910,crop=1080:910[fg];"          # bigger picture: trim the empty side edges (both characters + captions stay)
          "[bg][fg]overlay=0:(H-h)/2[v];[v]"
          + ",".join(f"drawtext=text='{t}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=64:fontcolor=white:"
                     f"borderw=4:bordercolor=black:x=(w-text_w)/2:y={y}" for t, y in rows) + "[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", vf, "-map", "[out]", "-map", "0:a",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                               capture_output=True, text=True).stdout.strip() or 0)
    open(os.path.join(proj, "INSTAGRAM_REEL.txt"), "w").write(
        f"=== VIDEO ===\n{os.path.basename(out)}  ({dur:.0f} s, 1080x1920)\n\n=== CAPTION ===\n{caption}\n\n{tags}\n\n"
        "=== SETTINGS ===\nCover: pick the frame with Ryan's reaction in the first scene\nShare to feed: yes\n"
        "Audio: original (already mixed)\nFull episode: post it on YouTube first, so 'link in bio' points somewhere\n")
    print(out, f"{dur:.1f}s")


if __name__ == "__main__":
    main(*sys.argv[1:5])
