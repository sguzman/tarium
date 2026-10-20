#!/usr/bin/env python3
"""Conservative detector for obvious secrets and raw private-context artifacts.

This is not a privacy certification. Human/agent provenance review is mandatory.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_PATHS = (
    re.compile(r"(^|/)\.env($|\.)", re.I),
    re.compile(r"\.(?:pem|p12|pfx|key|sqlite|sqlite3|db|eml)$", re.I),
    re.compile(r"(^|/)(?:id_rsa|id_ed25519|credentials\.json)$", re.I),
)
CHECKS = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("credential token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|AKIA[0-9A-Z]{16})\b")),
    ("raw chat delimiter", re.compile(r"<\|(?:im_start|im_end)\|>|\[im_start\]|<<< BEGIN OF CONVERSATION >>>")),
    ("raw role-tagged transcript", re.compile(r"(?m)^\s*(?:USER|ASSISTANT|SYSTEM|DEVELOPER):\s+\S")),
    ("internal context serialization", re.compile(r"model_editable_context|<MemoryCite\s*/>|sandbox:/mnt/data/")),
    ("merge conflict", re.compile(r"(?m)^(?:<{7}|>{7}) ")),
]
SKIP_CONTENT = {"scripts/publication_guard.py"}  # Contains the signatures it checks.


def main():
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    paths = [p.decode("utf-8") for p in result.stdout.split(b"\0") if p]
    failures = []
    for name in paths:
        if any(pattern.search(name) for pattern in BLOCKED_PATHS):
            failures.append(f"{name}: prohibited sensitive-file type")
        if name in SKIP_CONTENT:
            continue
        path = ROOT / name
        if not path.is_file():
            failures.append(f"{name}: tracked file missing")
            continue
        data = path.read_bytes()
        if b"\0" in data[:4096]:
            continue  # Binary content still requires separate provenance inspection.
        content = data.decode("utf-8", errors="replace")
        for label, pattern in CHECKS:
            if pattern.search(content):
                failures.append(f"{name}: potential {label}")
    for failure in failures:
        print(f"BLOCKED: {failure}", file=sys.stderr)
    if failures:
        sys.exit(1)
    print(f"Public-content signature checks passed for {len(paths)} tracked files.")
    print("Warning: this does not prove that prose, history, images, or derived content is free of private information.")


if __name__ == "__main__":
    main()
