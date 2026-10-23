---
name: hl-explainer-video
description: "Make a short narrated explainer video on one topic, in the style of animated math explainers: a beat-by-beat script, animated scenes, narration from a local voice or a provider the user supplies, captions, and one MP4. Use only when the user explicitly asks for a video explainer. Experimental: behavior and inputs may change in any release."
---
# Explainer Video

Input: `[topic] [--length <minutes>] [--voice local|<provider>]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Deliver the video and its supporting artifacts. Report actual media checks and narration limits, not the render log; keep unchecked viewing or listening explicit.

Defaults: length under 3 minutes; voice local. No topic: ask. Work in a new permitted temporary directory; never write into the repository unless the user names a path.

## 1. Script

State the one question the video answers and the audience. Take facts from the repository or checked sources. Mark unchecked factual claims unverified and invented teaching examples illustrative. Never invent evidence or quotes.

Write the beats as a table: beat, narration, visual, estimated seconds. One idea per beat. Narration: plain words and short, complete sentences. Visuals follow the explainer method: start from one concrete example with real numbers, build up, transform shapes instead of cutting, keep one idea on screen.

## 2. Tools

Check what is installed before writing commands: `ffmpeg -version`, `ffprobe -version`, and `manim --version`. Do not install or download a tool just to check its version. Check the installed version's documentation before using an API you have not seen work.

For offline rendering, disable automatic version lookups before rendering. Verify the installed option; Manim 0.22 uses `--silent` on the render command.

Local voice, first usable and permitted: the platform's speech command (`say -o <file>.aiff` on macOS), `piper`, `espeak-ng`. None usable: produce captions only and say so, unless narration is required; then stop. A denied invocation is not missing software; do not bypass its denial.

A provider voice (for example ElevenLabs) only when the user asks for it and has put the key in an environment variable. Read the key only from that variable; never print, log, or write it to a file. Use the provider's current documentation for the request. Paid usage needs the user's approval of the estimated cost first.

Name only tools confirmed missing, including ffprobe; distinguish tools not checked or denied. Offer an install command only after checking permitted documentation for the target environment; otherwise label it unverified. Ask before installing.

## 3. Narration first

With narration, generate one audio file per beat. Measure each with `ffprobe -v error -show_entries format=duration -of csv=p=0 <file>`. Each narrated beat's scene lasts its audio duration; the script estimates do not set timing. With captions only, use the script's estimated beat lengths and label them estimated.

## 4. Scenes

Write one Manim scene per beat, or one scene that waits per measured duration. A beat's wait is its planned duration minus its animation run time; shorten animations that exceed it.

Render at low quality first (`-ql`). Verify the preview's stream, duration, and one frame per beat before a final render (`-qh`). A denied required check: immediately report `Stopped` with the exact observed error and partial artifacts, then end tool use. Missing preview verification: stop before the final render. Take each rendered file's path from Manim's log or a confirmed filesystem entry, not a guessed path. Run every render and encode in the foreground, never as a background job, and wait for it to finish before the next step. If the host limits command time, raise the limit or render one scene per command so each finishes within it.

## 5. Assemble

Use new output paths and `ffmpeg -n` to preserve existing files. Join the beats in order. With narration, mux: `ffmpeg -n -i <video> -i <narration> -c:v copy -c:a aac -shortest <out>.mp4`. With captions only, keep the video without an audio stream. Write an `.srt` from the script and the actual assembled beat timings.

## 6. Check

- `ffprobe` shows a video stream. With narration, it also shows an audio stream; their durations differ by under 0.5 seconds. With captions only, verify the video duration and caption timing; no audio stream is required.
- Extract one frame per beat (`ffmpeg -n -ss <t> -i <out>.mp4 -frames:v 1 <beat>.png`) and look at each: no clipped or overlapping text, the visual matches the narration.
- Verify caption intervals are ordered, non-overlapping, within the final video duration, and cover every beat.
- Watching the whole video with sound is the user's check; never claim you did it.

## Output

Reader: someone who asked for a short video and will watch or share it, without having seen the script. The decision: use the video, or supply what is missing.

- Line 1, bold: one plain sentence that gives the result the viewer learns, in the user's words, not the file name. Never starts with a label.
- Under line 1, plain sentences: the narration source, or "The video has no narration: <observed reason>.", and "I have not watched or listened to the video."
- Body, as numbered points:
  1. **The video shows the steps in this order.** A beat is one scene and its narration or caption. A `text` block with one line per beat, `start - end  what the viewer sees`, times in seconds.
  2. **The media checks show <result>.** Maintain and report a verification ledger: full command, directory, actual execution count, observed result. Distinct arguments mean distinct entries, including preview and final probes. Copy commands verbatim from tool inputs; keep long commands in blocks keyed to ledger entries, not program-name shorthand. Then state coverage and limitations. Result words: `ran`, `ran, nothing to check`, `skipped: <reason>`, `failed: <reason>`. Include tool versions only when they explain compatibility or failure.
  3. Failed render only: **The render stopped at <step>.** Then its error line, quoted exactly.
- `Verdict: <label>` on its own line just before `**Next:**`, one fixed label:
  - `Ready`: the narrated MP4 is written and the checks passed.
  - `Ready, captions only`: narration is optional, no usable permitted narration was produced, and the video and caption checks passed.
  - `Failed`: a render or encode step failed.
  - `Stopped`: input or a tool is missing. See the stopped cases.
- `**Next:**` owns every viewer action, question, prerequisite, and unblock route once: watch the MP4 with sound before sharing (check captions and visuals for a captions-only video); for a failed step, the fix.
- `**Changed:**` list only artifacts actually written, including the MP4 path only when it exists. Report partial artifacts when stopped; do not list absent audio, scenes, or media. Say the repository is untouched only when verified.

Stopped cases: a bold line 1 in plain words, then `Verdict: Stopped`, then `**Next:**` with up to 2 numbered ways out, the default first, listed nowhere else:
- No topic: `**I need a topic before I can make the video.**`
  1. Name the topic and length, for example `a 20-second video on compound interest` (default).
- Paid voice without a key or cost approval: `**I can't use the paid voice until access is available and its cost is approved.**`
  1. Use the local voice (default).
  2. Add the key to your environment and approve the estimated cost, then tell me.
- Missing or unavailable required tools: line 1 names only the tools that block this run and the observed reason.
  1. Approve installation of confirmed missing tools using checked instructions, or resolve the reported permission blocker (default).
  2. Supply the missing tools or permitted documentation, then send the request again.

Reader rules: define each term once at first use: beat (one scene and its narration or caption), caption (text and timings in the `.srt` file), Manim (the Python animation library), ffmpeg (the tool that joins video and sound), ffprobe (reads media lengths). Give every length as seconds with its unit: `20.0 s`. Never say you watched or listened to the video.

Output skeleton: replace placeholders with evidence. Repeat the ledger entry and command block for every executed check.

````markdown
**The video shows <one result the viewer learns>.**
The video has no narration: <observed reason>. I have not watched or listened to the video.

1. **The video shows the steps in this order.**
   ```text
   <start> - <end> s   <what the viewer sees>
   ```

2. **The media checks show <observed result>.**

   | Entry | Directory | Executions | Observed result |
   |---|---|---|---|
   | C1 | `<actual working directory>` | <actual count> | <actual output and status> |

   C1 command:
   ```sh
   <verbatim command from its tool input>
   ```

   Coverage and limitations: <what was checked and what remains unknown>.

Verdict: <label justified by the observed checks>

**Next:**
1. Watch `<existing MP4 path>` with its captions before sharing it.

**Changed:** <only artifacts actually written, or none>.
````
