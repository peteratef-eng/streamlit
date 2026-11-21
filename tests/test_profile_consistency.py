from pathlib import Path
import unittest
from portfolio.content.profile import PROFILE
from portfolio.content.experience import EXPERIENCE

ROOT = Path(__file__).resolve().parents[1]

class ProfileConsistencyTest(unittest.TestCase):
    def test_confirmed_title_and_dates(self):
        self.assertEqual(PROFILE["title"], "Data Engineer")
        role = next(x for x in EXPERIENCE if x["role"] == "Data Integration Engineer")
        self.assertEqual(role["end_date"], "May 2026")
        self.assertIn("Open to Data Engineer opportunities", PROFILE["availability"])

    def test_active_copy_has_no_old_title(self):
        for name in ("app.py", "ui/components.py", "dashboard/components.py", "views/home.py", "views/about.py", "views/contact.py", "portfolio/content/profile.py"):
            text = (ROOT / name).read_text()
            self.assertNotIn("Junior Data Engineer", text, name)
            self.assertNotIn("Junior%20Data%20Engineer", text, name)
