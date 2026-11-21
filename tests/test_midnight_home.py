from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class MidnightHomeTest(unittest.TestCase):
    def test_home_has_readable_sections_and_personal_identity(self):
        source=(ROOT/'views/home.py').read_text()
        for text in ('mn-identity','Junior Data Engineer','selected-work','background','contact','Download resume','PROFILE[\'bio\']'):
            with self.subTest(text=text): self.assertIn(text,source)
        self.assertNotIn('st.columns',source)
        self.assertNotIn('st.components',source)

    def test_theme_is_scoped_and_motion_respects_preferences(self):
        css=(ROOT/'ui/portfolio.css').read_text()
        self.assertIn('.stApp:has(.mn-home)',css)
        self.assertIn('.stApp:has(.mn-project-index)',css)
        self.assertIn('prefers-reduced-motion: reduce',css)
        self.assertIn(':focus-visible',css)
        self.assertIn('grid-template-columns: minmax(0,1fr)',css)

if __name__=='__main__':unittest.main()
