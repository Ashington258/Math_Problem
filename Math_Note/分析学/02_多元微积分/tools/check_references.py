"""Check chapter references in the working tree or a Git revision.

python tools/check_references.py
python tools/check_references.py --git-ref HEAD
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                   cwd=ROOT, text=True).strip())
PREFIX = ROOT.relative_to(REPO).as_posix() + "/"


def links(text):
    # Ignore examples in fenced code and inline code.
    text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    pattern = r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|(?:[^()\s]|\([^()]*\))+)\s*\)"
    for match in re.finditer(pattern, text):
        yield match.group(1).strip("<>"), text.count("\n", 0, match.start()) + 1
    for match in re.finditer(r"(?m)^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", text):
        yield match.group(1).strip("<>"), text.count("\n", 0, match.start()) + 1


def inspect(git_ref=None):
    tracked = set(subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "-z", git_ref or "HEAD"],
        cwd=REPO).decode("utf-8").split("\0"))
    if git_ref:
        names = sorted(p for p in tracked if p.startswith(PREFIX) and p.endswith(".md"))
    else:
        names = sorted(p.relative_to(REPO).as_posix() for p in ROOT.rglob("*.md"))
    broken, nonportable, pending_external = [], [], set()
    edges = defaultdict(set)
    for name in names:
        if git_ref:
            text = subprocess.check_output(["git", "show", f"{git_ref}:{name}"],
                                           cwd=REPO).decode("utf-8-sig")
        else:
            text = (REPO / name).read_text(encoding="utf-8-sig")
        for raw, line in links(text):
            if raw.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            if "\\" in raw or re.match(r"^(?:[A-Za-z]:|file:|/)", raw):
                nonportable.append([name, line, raw])
                continue
            target = unquote(urlsplit(raw).path)
            if not target:
                continue
            absolute = (REPO / name).parent.joinpath(target).resolve()
            try:
                relative = absolute.relative_to(REPO).as_posix()
            except ValueError:
                broken.append([name, line, raw])
                continue
            exists = relative in tracked if git_ref else absolute.exists()
            if git_ref and not exists:
                exists = any(p.startswith(relative.rstrip("/") + "/") for p in tracked)
            if not exists:
                broken.append([name, line, raw])
            if relative.endswith(".md"):
                edges[name].add(relative)
            if not git_ref and not relative.startswith(PREFIX) and relative not in tracked:
                pending_external.add(relative)
    entry = PREFIX + "README.md"
    reached, queue = {entry}, deque([entry])
    while queue:
        current = queue.popleft()
        # An automatically generated index must not hide missing chapter entries.
        if current == PREFIX + "关系图谱.md":
            continue
        for target in edges[current]:
            if target.startswith(PREFIX) and target not in reached:
                reached.add(target)
                queue.append(target)
    return {
        "mode": git_ref or "working-tree",
        "markdown_files": len(names),
        "reference_edges": sum(len(v) for v in edges.values()),
        "broken": broken,
        "nonportable": nonportable,
        "unreachable": [p for p in names if p not in reached],
        "pending_external_dependencies": sorted(pending_external),
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--git-ref")
    args = parser.parse_args()
    report = inspect(args.git_ref)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report["broken"] or report["nonportable"] or report["unreachable"]))
