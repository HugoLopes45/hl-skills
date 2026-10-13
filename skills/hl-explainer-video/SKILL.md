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

First line: the MP4 path and its duration. Then a table: beat, start time, what it shows. Then the paths of the script, scene source, audio, and captions; the checks run with results; and what was not checked.
