"""Color identity and perceptual distinction tests."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from project_colors import MIN_DELTA_E, MIN_HUE_GAP, assign_colors, oklab_distance, hue_gap


class ColorsTests(unittest.TestCase):
    def test_registered_colors_match_name_based_scheme(self):
        data = json.loads((ROOT / "registry/projects.json").read_text())
        projects = data["projects"]
        assigned = assign_colors([p["name"] for p in projects])
        self.assertEqual(set(assigned), {p["slug"] for p in projects})
        for project in projects:
            self.assertEqual(project["accent_color"], assigned[project["slug"]])

    def test_distinct_human_visible_identities(self):
        entries = json.loads((ROOT / "registry/projects.json").read_text())["projects"]
        for i, a in enumerate(entries):
            for b in entries[i+1:]:
                self.assertGreaterEqual(oklab_distance(a["accent_color"], b["accent_color"]), MIN_DELTA_E - .001)
                self.assertGreaterEqual(hue_gap(a["accent_color"], b["accent_color"]), MIN_HUE_GAP - .001)

    def test_name_order_is_stable_and_legacy_colors_remain_fixed(self):
        names = ["Chromalect", "Nomos", "Urbarium", "Architectarium", "Stratlas", "Viewsource"]
        expected = assign_colors(names)
        self.assertEqual(assign_colors(reversed(names)), expected)
        self.assertEqual(expected["architectarium"], "#B9905D")
        self.assertEqual(expected["stratlas"], "#6B9DC4")
        self.assertEqual(expected["chromalect"], "#B97CD3")
        self.assertEqual(expected["nomos"], "#18B381")
        self.assertEqual(expected["urbarium"], "#E07081")
        self.assertEqual(expected["viewsource"], "#05D6E6")
        self.assertEqual(len(set(expected.values())), len(names))


if __name__ == "__main__":
    unittest.main()
