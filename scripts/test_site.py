#!/usr/bin/env python3
"""No-network tests for the deployable registry-driven landing page."""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import build


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()

    def test_export_matches_authoritative_registry(self):
        source = json.loads((ROOT / "registry/projects.json").read_text())
        published = json.loads((ROOT / "_site/data/projects.json").read_text())
        self.assertEqual(source, published)
        self.assertEqual(len(published["projects"]), 1)
        self.assertEqual(published["projects"][0]["slug"], "architectarium")

    def test_static_assets_and_relative_paths(self):
        output = ROOT / "_site"
        html = (output / "index.html").read_text()
        for path in ("./app.js", "./styles.css", "./favicon.svg", "./data/projects.json"):
            if path != "./data/projects.json":
                self.assertIn(path, html)
            self.assertTrue((output / path).is_file())
        self.assertIn('id="project-list"', html)
        self.assertIn('id="project-count"', html)
        self.assertIn('id="orbit-projects"', html)
        self.assertIn('aria-label="Orbiting links to Tarium projects"', html)

    def test_catalog_is_not_hardcoded_in_site(self):
        for name in ("index.html", "styles.css", "app.js"):
            raw = (ROOT / "site" / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("architectarium", raw)
        app = (ROOT / "site/app.js").read_text()
        self.assertIn('fetch("./data/projects.json"', app)
        self.assertIn("textContent", app)
        self.assertNotIn("innerHTML", app)
        self.assertIn("makeOrbit(project, index)", app)
        self.assertIn("projectDestination(project)", app)
        self.assertIn('orbitHost.replaceChildren(', app)

    def test_registry_links_and_colors(self):
        entries = json.loads((ROOT / "_site/data/projects.json").read_text())["projects"]
        for entry in entries:
            self.assertRegex(entry["repository"], r"^https://github\.com/[\w-]+/[\w.-]+$")
            self.assertRegex(entry["accent_color"], r"^#[0-9A-Fa-f]{6}$")
            self.assertTrue(entry["ontology_path"].startswith("ontology/"))


if __name__ == "__main__":
    unittest.main()
