from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
from ui.components import _sidebar_page_link
from portfolio.content.experience import EXPERIENCE

ROOT = Path(__file__).resolve().parents[1]

class NavigationAndControlStylesTest(unittest.TestCase):
    def test_active_navigation_does_not_emit_an_empty_markdown_row(self):
        page = {'route': '/experience', 'path': 'views/experience.py', 'label': 'Experience'}
        with patch('ui.components.st') as streamlit:
            streamlit.container.return_value = MagicMock()
            _sidebar_page_link(page, True, 'portfolio')
            streamlit.markdown.assert_not_called()
            streamlit.container.assert_called_once_with(key='sidebar_portfolio_experience_active')
            streamlit.page_link.assert_called_once_with('views/experience.py', label='Experience', use_container_width=True)

    def test_legacy_buttons_and_native_form_submit_have_explicit_contrast(self):
        css = (ROOT / 'ui/portfolio.css').read_text()
        self.assertIn('a:not(.pa-button):not(.portfolio-button):not(.contact-card-action)', css)
        self.assertIn('a.portfolio-button-primary { background: #78E1CD !important; color: #0F172A !important;', css)
        self.assertIn('button[kind="primaryFormSubmit"] *', css)
        for state in (':hover', ':focus-visible', ':active'):
            self.assertIn('[data-testid="stPageLink"] a' + state, css)

    def test_digicust_role_title(self):
        self.assertEqual(EXPERIENCE[0]['role'], 'Data Integration Engineer')

if __name__ == '__main__':
    unittest.main()
