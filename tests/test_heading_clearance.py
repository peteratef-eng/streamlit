"""Guard the top clearance below Streamlit's fixed application header."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class HeadingClearanceTest(unittest.TestCase):
    def test_shared_layout_reserves_toolbar_clearance(self):
        styles = (ROOT / "ui/styles.py").read_text()
        self.assertIn("padding: 4.5rem 1.35rem 2.5rem;", styles)
        self.assertNotIn("padding: .35rem 1.35rem 2.5rem;", styles)
        self.assertIn("padding: 4.5rem 1rem 2.5rem;", styles)
        self.assertNotIn("padding: .35rem 1rem 2.5rem;", styles)

    def test_home_overrides_keep_the_same_clearance(self):
        css = (ROOT / "ui/portfolio.css").read_text()
        import re
        overrides = re.findall(r'\.stApp:has\(\.mn-home\) \[data-testid="stMainBlockContainer"\] \{([^}]+)\}', css)
        self.assertEqual(len(overrides), 2)
        for rule in overrides:
            self.assertIn("padding-top: 4.5rem;", rule)

    def test_heading_permalink_controls_are_hidden_without_hiding_content_links(self):
        styles = (ROOT / "ui/styles.py").read_text()
        self.assertIn('[data-testid="stHeadingWithActionElements"] a.anchor-link', styles)
        self.assertIn('display: none !important;', styles)
        self.assertNotIn('h1:hover a, h2:hover a, h3:hover a', styles)
