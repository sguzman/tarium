#!/usr/bin/env python3
"""Assemble a minimal static GitHub Pages artifact using only approved source files."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"
FILES = ("index.html", "styles.css", "app.js", "favicon.svg")


def build():
    data = json.loads((ROOT / "registry/projects.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 2 or not isinstance(data.get("projects"), list):
        raise ValueError("Invalid public project registry")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in FILES:
        shutil.copyfile(SOURCE / name, OUTPUT / name)
    (OUTPUT / "data").mkdir()
    (OUTPUT / "data" / "projects.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built static Tarium site: {len(data['projects'])} project(s), {len(FILES) + 2} published files")


if __name__ == "__main__":
    build()
