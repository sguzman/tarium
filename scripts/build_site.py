#!/usr/bin/env python3
"""Assemble a minimal static GitHub Pages artifact using only approved source files."""

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"
FILES = ("index.html", "styles.css", "app.js", "theme.js", "favicon.svg")


def build():
    data = json.loads((ROOT / "registry/projects.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 2 or not isinstance(data.get("projects"), list):
        raise ValueError("Invalid public project registry")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in FILES:
        shutil.copyfile(SOURCE / name, OUTPUT / name)
    # Version assets by their contents so a fresh page never loads stale CSS or JS
    # from an earlier GitHub Pages deployment.
    html = (OUTPUT / "index.html").read_text(encoding="utf-8")
    for name in ("styles.css", "app.js", "theme.js"):
        digest = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()[:12]
        old = f'./{name}"'
        if html.count(old) != 1:
            raise ValueError(f"Expected exactly one asset reference for {name}")
        html = html.replace(old, f'./{name}?v={digest}"')
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    (OUTPUT / "data").mkdir()
    (OUTPUT / "data" / "projects.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built static Tarium site: {len(data['projects'])} project(s), {len(FILES) + 2} published files")


if __name__ == "__main__":
    build()
