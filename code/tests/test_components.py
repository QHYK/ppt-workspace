"""Focused checks for reusable drawing and build entry points."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from code.lib import Deck, flowchart, framework, gantt, relationship, timeline
from code.themes import DEFAULT


class ComponentTests(unittest.TestCase):
    def setUp(self):
        self.deck = Deck(DEFAULT, icon_dir=ROOT / "assets" / "icons")
        self.slide = self.deck.ppt.slides.add_slide(self.deck.ppt.slide_layouts[6])

    def test_theme_and_editable_components(self):
        """Components draw native objects and accept data without brand content."""
        variant = DEFAULT.override(colors={"dark": "123456"}, layout={"left": 0.8})
        self.assertEqual(variant.colors["dark"], "123456")
        self.assertEqual(variant.colors["green"], DEFAULT.colors["green"])
        self.assertEqual(DEFAULT.layout["left"], 0.55)
        self.deck.card(self.slide, 0.5, 0.5, 2.5, 2, title="A", body="B", number="01")
        self.assertEqual(str(self.slide.shapes[0].fill.fore_color.rgb), DEFAULT.colors["white"])
        self.assertEqual(str(self.slide.shapes[0].line.color.rgb), DEFAULT.colors["border"])
        framework(self.deck, self.slide, tiers=["A"], branches=[("B", "C")], x=3, y=0.5, width=3)
        flowchart(self.deck, self.slide, steps=[("A", "B")], x=6.2, y=0.5, width=2.5, height=2)
        timeline(self.deck, self.slide, milestones=[("Q1", "A", "B")], x=0.5, y=3, width=2.5, height=2)
        gantt(self.deck, self.slide, periods=["Q1", "Q2"], rows=[("Work", 0, 1, "green", "")], x=3, y=3, label_width=1, width=2)
        relationship(self.deck, self.slide, center="A", satellites=[("B", "C")], x=6, y=3, width=3, height=2)
        self.assertGreater(len(self.slide.shapes), 20)
        with tempfile.TemporaryDirectory() as tmp:
            output = self.deck.save(Path(tmp) / "components.pptx")
            self.assertEqual(len(Presentation(output).slides), 1)

    def test_missing_icon_fails_loudly(self):
        """An absent asset must not silently disappear from a slide."""
        with self.assertRaises(FileNotFoundError):
            self.deck.icon(self.slide, "missing-icon", 0, 0)

    def test_relationship_node_limit(self):
        """Unsupported diagrams fail with a clear boundary error."""
        with self.assertRaises(ValueError):
            relationship(self.deck, self.slide, center="A", satellites=[("B", "C")] * 5, x=0, y=0, width=3, height=2)


class BuildTests(unittest.TestCase):
    def test_showcase_regenerates_without_local_projects(self):
        """The public example builds from shared code and assets alone."""
        script = ROOT / "slides/example/build.py"
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "showcase.pptx"
            subprocess.run(
                [sys.executable, str(script), "--output", str(output)],
                check=True, cwd=ROOT, capture_output=True,
            )
            self.assertEqual(len(Presentation(output).slides), 11)


if __name__ == "__main__":
    unittest.main()
