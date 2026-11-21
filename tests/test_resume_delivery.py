"""The two download controls read the current resume, not cached old bytes."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ResumeDeliveryTest(unittest.TestCase):
    def test_resume_matches_supplied_file(self):
        data = (ROOT / "assets/resume/Peter Resume 2026.pdf").read_bytes()
        self.assertTrue(data.startswith(b"%PDF-"))
        self.assertEqual(hashlib.sha256(data).hexdigest(), "152b46516de3cbd97f9fe8bedbe5d07ebcb50baa09b056e694c8ac98c2643c39")

    def test_resume_helpers_are_not_cached_by_path_only(self):
        for name in ("home", "contact"):
            source = (ROOT / f"views/{name}.py").read_text()
            self.assertNotIn("@st.cache_data", source)
            self.assertIn('PROFILE["resume_path"]', source)
            self.assertIn('download="Peter_Atef_Resume_2026.pdf"', source)
