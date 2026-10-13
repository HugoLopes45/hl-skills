---
name: hl-explainer-video
description: "Make a short narrated explainer video on one topic, in the style of animated math explainers: a beat-by-beat script, animated scenes, narration from a local voice or a provider the user supplies, captions, and one MP4. Use only when the user explicitly asks for a video explainer. Experimental: behavior and inputs may change in any release."
---
# Explainer Video

Input: `[topic] [--length <minutes>] [--voice local|<provider>]`

Defaults: length under 3 minutes; voice local. No topic: ask. Work in a new temporary directory; never write into the repository unless the user names a path.

## 1. Script

State the one question the video answers and the audience. Take facts from the repository or cited sources; label the rest assumption. Never invent numbers or quotes.

Write the beats as a table: beat, narration, visual, estimated seconds. One idea per beat. Narration: plain words, sentences up to 20 words. Visuals follow the explainer method: start from one concrete example with real numbers, build up, transform shapes instead of cutting, keep one idea on screen.

## 2. Tools

Check what is installed before writing commands: `ffmpeg -version`, `ffprobe -version`, and `manim --version` (or `uvx --from manim manim --version` when `uv` exists). Check the installed version's documentation before using an API you have not seen work.

Local voice, first found: the platform's speech command (`say -o <file>.aiff` on macOS), `piper`, `espeak-ng`. None: produce the video with captions only and say so.

A provider voice (for example ElevenLabs) only when the user asks for it and has put the key in an environment variable. Read the key only from that variable; never print, log, or write it to a file. Use the provider's current documentation for the request. Paid usage needs the user's approval of the estimated cost first.

Missing Manim or ffmpeg: name it and its documented install command; ask before installing.

## 3. Narration first

Generate one audio file per beat. Measure each with `ffprobe -v error -show_entries format=duration -of csv=p=0 <file>`. Each beat's scene lasts its audio duration; the script estimates do not set timing.

## 4. Scenes

Write one Manim scene per beat, or one scene that waits per measured duration. A beat's wait is its audio duration minus its animation run time; audio shorter than the animation: shorten the animation. Render at low quality first (`-ql`) and check frames before a final render (`-qh`). Take each rendered file's path from Manim's log, not a guessed path. Run every render and encode in the foreground, never as a background job, and wait for it to finish before the next step. If the host limits command time, raise the limit or render one scene per command so each finishes within it.

## 5. Assemble

Join the beats in order, then mux: `ffmpeg -i <video> -i <narration> -c:v copy -c:a aac -shortest <out>.mp4`. Write an `.srt` caption file from the narration and the measured durations.

## 6. Check

- `ffprobe` shows a video and an audio stream; their durations differ by under 0.5 seconds.
- Extract one frame per beat (`ffmpeg -ss <t> -i <out>.mp4 -frames:v 1 <beat>.png`) and look at each: no clipped or overlapping text, the visual matches the narration.
- Watching the whole video with sound is the user's check; never claim you did it.

## Output

Reader: someone who asked for a short video and will watch or share it, without having seen the script. The decision: use the video, or supply what is missing.

- Line 1, bold: one plain sentence that gives the result the viewer learns, in the user's words, not the file name. Under 100 characters. Never starts with a label.
- Under line 1, plain sentences: the narration source ("The narration uses the local voice." or "The video has no narration: no speech tool was found."), and "I have not watched or listened to the video; check it with sound before you share it."
- Body, as numbered points:
  1. **The video shows the steps in this order.** A beat is one scene and its narration. A `text` block with one line per beat, `start - end  what the viewer sees`, times in seconds.
  2. **The checks ran, and their results are below.** A table, up to 5 checks: check, result, detail. Result words: `ran`, `ran, nothing to check`, `skipped: <reason>`, `failed: <reason>`. Keep each cell to a few words.
  3. Failed render only: **The render stopped at <step>.** Then its error line, quoted exactly.
- `Verdict: <word>` on its own line just before `**Next:**`, one fixed word:
  - `Ready`: the MP4 is written and the checks passed.
  - `Ready, captions only`: no speech tool was found, so the video has no narration.
  - `Failed`: a render or encode step failed.
  - `Stopped`: input or a tool is missing. See the stopped cases.
- `**Next:**` the steps a person takes now: watch the MP4 with sound; for a failed step, the fix.
- `**Changed:**` the temp directory, which holds the script, scene file, audio, captions, and MP4, and the MP4 path. The repository is not touched.

Stopped cases: a bold line 1 in plain words, then `Verdict: Stopped`, then `**Next:**` with up to 2 numbered ways out, the default first, listed nowhere else:
- No topic: `**I need a topic before I can make the video. What should it explain, and how long?**`
  1. Name the topic and length, for example `a 20-second video on compound interest` (default).
- Paid voice without a key or cost approval: `**I can't make the paid voice yet: no API key is set, and the cost needs your approval.**`
  1. Use the local voice (default).
  2. Add the key to your environment and approve the estimated cost, then tell me.
- Missing Manim or ffmpeg: `**I need two tools before I can make the video: Manim and ffmpeg.**`
  1. Approve the install; the documented command runs (default).
  2. Install both yourself, then send the request again.

Reader rules: define each term once at first use: beat (one scene and its narration), caption (the `.srt` on-screen text file), Manim (the Python animation library), ffmpeg (the tool that joins video and sound), ffprobe (reads media lengths). Give every length as seconds with its unit: `20.0 s`. Never say you watched or listened to the video.

The example below fixes the shape, not the content.

````markdown
**The video is done. It shows that interest earns interest, so each year adds more.**
The narration uses the local voice. I have not watched or listened to the video; check it with sound before you share it.

1. **The video shows one year of growth per beat, with real numbers.**
   ```text
   0.0 - 6.0 s    $1,000 at 5% a year: $50 earned in year one
   6.0 - 13.0 s   year two earns 5% of $1,050: $52.50
   13.0 - 20.0 s  after three years: $1,157.63
   ```

2. **The checks ran, and both lengths match.**
   | Check | Result | Detail |
   |---|---|---|
   | Video and audio lengths match | ran | video 20.0 s, audio 20.0 s |
   | One frame per beat | ran | 3 frames, no clipped text |

Verdict: Ready

**Next:**
1. Watch `/tmp/explainer-4c1e/compound-interest.mp4` with sound.

**Changed:** `/tmp/explainer-4c1e/` holds the script, scene file, audio, captions, and MP4 `compound-interest.mp4`. The repository is not touched.
````
