from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def contrast(a, b):
    def luminance(color):
        channels = [int(color[i:i+2],16)/255 for i in (1,3,5)]
        linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c,w in zip(linear,(.2126,.7152,.0722)))
    low,high = sorted((luminance(a),luminance(b)))
    return (high+.05)/(low+.05)

class MidnightContrastTests(unittest.TestCase):
    def test_button_variants_have_separate_foregrounds(self):
        css = (ROOT/'ui/portfolio.css').read_text()
        self.assertIn('a.pa-button-outline { background: #142036 !important; color: #DCE9F7 !important;',css)
        self.assertIn('a.pa-button-copper { background: #78E1CD !important; color: #0F172A !important;',css)
        self.assertNotIn('a.pa-button:not(.pa-button-secondary):not(.pa-project-actions .pa-button)',css)
        for fg,bg in [('#DCE9F7','#142036'),('#0F172A','#78E1CD'),('#B2C2D8','#0F172A')]:
            self.assertGreater(contrast(fg,bg),4.5)
