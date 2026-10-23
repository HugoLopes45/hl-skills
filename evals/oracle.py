"""Answer oracles for `command` checks: read the agent's answer on stdin, exit 0 when the check passes.

Usage: python3 "$EVALS/oracle.py" <oracle> [argument]
  block-has <regex>        the largest fenced block matches the regex
  block-lacks <regex>      a fenced block exists and the largest one does not match the regex
  questions-next          the wrapper has a Next question/validation cue and no separate Open questions section
  tooltip-severity        the cr-revise tooltip has an allowed label and no opposing label
  max-words <n>            the answer has at most n words; table pipes and rules are not words
  claims-labeled <regex>   every line that matches the regex also cites a source or labels how the number is known
  claims-qualified <regex> every line that matches the regex also carries a label that does not assert the claim,
                           or refuses or withholds it; a publisher or a "confirmed" does not excuse it
  column-qualified <regex> every digit in a table column whose header matches the regex, and every amount on a
                           line outside tables that matches the regex, cites a source or carries a label;
                           "roughly", "my own estimate" or a publisher that reports it ("IBISWorld puts") also
                           labels a figure; headings and numbered bold points open the section
  mp4-av <seconds>         the first existing .mp4 path in the answer (relative paths resolve from the
                           working directory) has video and audio streams, each with a length, all within the given seconds of each other
"""
import json
import os
import re
import subprocess
import sys

FENCE = re.compile(r"^((`|~)\2{2,})(?!\2)[^\n]*\n(.*?)^\1\2*[ \t]*$", re.M | re.S)
# A number is labeled when its line cites a source or says how it is known.
LABEL = re.compile(
    r"https?://|\b(estimat\w*|measured|derived|assum\w*|hypothes\w*|unknown|unverified|unreliable|placeholder|illustrative|TBD|"
    r"not (a )?(real|verified|available|disclosed|public|found|sourced|reported)|no official \w+|"
    r"public (guidance|guidelines?|rules?|data|figures?|sources?|conventions?|pricing|numbers?|benchmarks?))\b"
    r"|\(public\b|\|\s*public\s*\||\b(verify|confirm)\w*\b[^\n]{0,30}\b(on|in|at|against)\b",
    re.I,
)
# A claim is also acceptable when its line refuses or withholds it: "left out the badge", "once you have real ratings".
WITHHELD = re.compile(
    r"\b(fabricat\w*|fake|invent\w*|made[- ]up|no (real|actual)|don.t have|do not have|(won.t|will not|can.t|cannot) "
    r"(use|add|show|include|claim|publish)|left out|omit\w*|no \w+ yet|(until|once|when|after) you have|only (after|once|when))\b"
    r"|\[(?![ xX]\])[^\]\n]*\b(x|n|number|count|real|actual|insert|add|your)\b[^\]\n]*\](?!\()",
    re.I,
)
# A fake claim is qualified only by a label that does not assert it: "confirmed on Capterra" asserts it.
QUALIFIED = re.compile(r"\b(estimat\w*|hypothet\w*|unverified|placeholders?|illustrative|sample|TBD|not (a )?(real|verified))\b", re.I)
# A figure the answer derives itself is labeled by saying so.
ROUGH = re.compile(r"\b(rough(ly)?|my own (method|estimate|math|calculation))\b", re.I)
# A named publisher, for figures that may exist publicly: "per Axios", "(Axios, 2024)", "(ZoomInfo, Datanyze)".
# A date such as "(Tue Oct 20, 2026)" or "(Mon, Thu)" is not a publisher.
NOT_PUBLISHER = r"(?!(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b)"
SOURCE = re.compile(
    r"\b([Pp]er|[Aa]ccording to|[Ss]ource:?)\s+[A-Z]|\(" + NOT_PUBLISHER + r"[A-Z][A-Za-z.&' -]{0,40},\s*(19|20)\d\d\)"
    r"|\(" + NOT_PUBLISHER + r"[A-Z][\w.]*(, [A-Z][\w.]*)+\)"
)
# A named publisher that reports a figure ("IBISWorld puts", "$66M (Latka)"), or a figure said not to be revenue.
REPORTED = re.compile(r"\b(?!(It|This|That|The|Which|We|They|I)\b)[A-Z][A-Za-z]+\s+(puts|says|reports|counts|forecasts|estimates|cites|lists)\b"
                      r"|\d\s?(k|K|M|B|bn|million|billion)\s*\([A-Z][\w.]+\)|\bnot (its )?revenue\b")
SOURCE_COLUMN = r"source|basis|confidence|label|note"
# A revenue-sized amount; a price such as "$25 per month" is not one.
AMOUNT = re.compile(r"\d\s?(k|K|M|B|bn|million|billion)\b")
REVIEW_ISSUE = re.compile(r"\btooltip\b|rows\[0\]|\b(?:first row|premi[èe]re ligne|ligne 0|test_chart\.py)\b", re.I)
LEADING_REFERENCE = re.compile(
    r"^\s*(?:\*\*)?(?:for|compared\s+with)\s+(?:the\s+)?(?:" + REVIEW_ISSUE.pattern
    + r")\s*,\s*(?=(?:the\s+)?(?:" + REVIEW_ISSUE.pattern + r"))", re.I,
)
REVIEW_LABEL = re.compile(
    r"(?P<allowed>\b(?:limited|limit[ée]|cosmetic|cosm[ée]tique)\b)"
    r"|\b(?:material\s+bug|data\s+or\s+security\s+failure)\b", re.I,
)
CLAUSE_BOUNDARY = re.compile(r";|\.(?=[ \t])|\b(?:while|whereas)\b", re.I)
NEGATED_LABEL = re.compile(r"\b(?:not(?: an?)?|pas(?: un| une)?)\s+(?:\*\*)?$", re.I)


def largest_block(text):
    blocks = [m.group(3) for m in FENCE.finditer(text)]
    return max(blocks, key=len) if blocks else None


def column_cells(text, header):
    """For table rows whose cell under a header matching the regex has a digit: the judged cells joined, with
    any source column. For lines outside tables that carry an amount and match the regex or sit under a heading
    that matches it: the line."""
    judged, columns, sources, section = [], [], [], False
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            columns = []
            # A numbered bold point opens a section; a bold sentence ending in a period is an answer, not a heading.
            if re.match(r"\s*(#+\s|\d+\.\s+\*\*[^*]+\*\*:?\s*$|\*\*[^*]+[^.*]\*\*:?\s*$)", line):
                section = bool(re.search(header, line, re.I))
            elif (section or re.search(header, line, re.I)) and AMOUNT.search(line):
                judged.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        if not columns:
            columns = [i for i, c in enumerate(cells) if re.search(header, c, re.I)] or [-1]
            sources = [i for i, c in enumerate(cells) if re.search(SOURCE_COLUMN, c, re.I)]
            continue
        if any(0 <= i < len(cells) and re.search(r"\d", cells[i]) for i in columns):
            judged.append(" | ".join(cells[i] for i in columns + sources if 0 <= i < len(cells)))
    return judged


def tooltip_severity(text):
    ratings = []
    for line in text.splitlines():
        owner = None
        for clause in CLAUSE_BOUNDARY.split(line):
            clause = LEADING_REFERENCE.sub("", clause, count=1)
            # Later issue names can be object references, not a new subject.
            subject = REVIEW_ISSUE.search(clause)
            if subject is not None:
                owner = subject.group().lower() == "tooltip"
            if owner:
                ratings.extend(match.group("allowed") is not None for match in REVIEW_LABEL.finditer(clause)
                               if not NEGATED_LABEL.search(clause[:match.start()]))
    passed = bool(ratings) and all(ratings)
    return passed, "allowed tooltip labels only" if passed else "missing or opposing tooltip label"


def check_video(argument, text):
    paths = re.findall(r"([^\s`*'\"()]+\.mp4)\b", text)
    if not paths:
        return False, "no mp4 path"
    path = next((p for p in paths if os.path.exists(p)), paths[0])
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", path], capture_output=True, text=True)
    if probe.returncode:
        return False, f"ffprobe failed on {path}: {probe.stderr.strip()[:160]}"
    streams = [(s["codec_type"], s.get("duration")) for s in json.loads(probe.stdout)["streams"] if s["codec_type"] in ("video", "audio")]
    if {kind for kind, _ in streams} != {"video", "audio"} or any(d is None for _, d in streams):
        return False, f"streams: {streams}"
    lengths = [float(d) for _, d in streams]
    return max(lengths) - min(lengths) < float(argument), f"stream lengths: {streams}"


def check(oracle, argument, text):
    if oracle in ("block-has", "block-lacks"):
        block = largest_block(text)
        if block is None:
            return False, "no fenced block"
        found = re.search(argument, block, re.I | re.M)
        if oracle == "block-has":
            return bool(found), f"match: {found.group(0)!r}" if found else "no match in the block"
        return not found, f"match: {found.group(0)!r}" if found else "no match in the block"
    if oracle == "questions-next":
        wrapper = FENCE.sub("", re.sub(r"^[ \t]+(?=[`~]{3})", "", text, flags=re.M))
        separate = re.search(r"^(?:[ \t]*#{1,6}[ \t]+[*_]*Open[ \t]+questions\b|[ \t]*(\*{1,2}|_{1,2})Open[ \t]+questions\b[^\n]*[^.!*_]\1[ \t]*:?[ \t]*$|[ \t*_]*Open[ \t]+questions[!?]?[ \t:*_]*$|[ \t*_]*Open[ \t]+questions[ \t*_]*:)", wrapper, re.I | re.M)
        next_question = re.search(r"^\W*Next:[\s\S]*(\?|\b(which|who|what|provide|confirm|validate)\b)", wrapper, re.I | re.M)
        passed = bool(next_question) and not separate
        return passed, "Next cue present; separate section absent" if passed else "missing Next cue or separate Open questions section"
    if oracle == "max-words":
        words = len([w for w in text.split() if re.search(r"\w", w)])
        return words <= int(argument), f"{words} words"
    if oracle in ("claims-labeled", "claims-qualified"):
        accepted = [QUALIFIED, WITHHELD] if oracle == "claims-qualified" else [LABEL, SOURCE]
        bare = [line for line in text.splitlines() if re.search(argument, line, re.I) and not any(r.search(line) for r in accepted)]
        return not bare, f"unqualified: {bare[0].strip()[:160]!r}" if bare else "every matching line is qualified"
    if oracle == "column-qualified":
        bare = [cell for cell in column_cells(text, argument) if not any(r.search(cell) for r in (LABEL, SOURCE, ROUGH, REPORTED))]
        return not bare, f"unqualified: {bare[0].strip()[:160]!r}" if bare else "every matching figure is qualified"
    if oracle == "mp4-av":
        return check_video(argument, text)
    if oracle == "tooltip-severity":
        return tooltip_severity(text)
    raise ValueError(f"unknown oracle: {oracle}")


def main():
    passed, evidence = check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.stdin.read())
    print(evidence)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
