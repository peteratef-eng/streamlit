from pathlib import Path
import unittest
import pandas as pd
from dashboard.transformations import top_counts
from ui.theme import current_theme
from dashboard.weather_case_study import scope_chart
from dashboard.weather_demo import sample_daily_mart, temperature_chart

ROOT = Path(__file__).resolve().parents[1]

class SitewideMidnightTests(unittest.TestCase):
    def test_theme_and_charts_are_dark(self):
        theme = current_theme()
        self.assertEqual(theme['mode'], 'dark')
        self.assertEqual(theme['background'], '#0F172A')
        for figure in (scope_chart(), temperature_chart(sample_daily_mart())):
            self.assertEqual(figure.layout.font.color, theme['secondary_text'])
            self.assertEqual(figure.layout.template.layout.paper_bgcolor, 'rgb(17,17,17)')

    def test_css_is_not_cached_without_its_source(self):
        source = (ROOT / 'ui/styles.py').read_text()
        self.assertNotIn('@st.cache_resource', source)

    def test_categorical_counts_allow_missing_label(self):
        frame = pd.DataFrame({'role': pd.Categorical(['Engineer', None, 'Engineer'])})
        result = top_counts(frame, 'role')
        self.assertEqual(dict(zip(result['role'], result['postings'])), {'Engineer': 2, 'Unknown': 1})
        self.assertEqual(str(frame['role'].dtype), 'category')

if __name__ == '__main__':
    unittest.main()
