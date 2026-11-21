from __future__ import annotations

import streamlit as st

from ui.analytics import initialize_analytics
from ui.components import sidebar_bottom
from ui.navigation import portfolio_navigation, route_from_page
from ui.styles import inject_global_styles
from ui.theme import current_theme


st.set_page_config(
    page_title="Peter Atef | Data Engineer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "Job Market Intelligence | Data Engineering Portfolio",
    },
)

theme = current_theme()
inject_global_styles(theme)
initialize_analytics()

navigation = portfolio_navigation()
sidebar_bottom(route_from_page(navigation))
navigation.run()
