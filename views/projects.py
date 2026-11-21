from __future__ import annotations

import streamlit as st

from portfolio.content.projects import PROJECTS
from ui.components import project_card

st.markdown('<section class="mn-project-index"><h1>Selected work.</h1></section>', unsafe_allow_html=True)

projects = sorted(PROJECTS, key=lambda item: item.get("sort_order", 999))
weather = next((project for project in projects if project["slug"] == "weather-forecast-data-platform"), None)
if weather:
    project_card(weather, actions=True, featured=True, index=1)
remaining = [project for project in projects if project is not weather]
for row_start in range(0, len(remaining), 2):
    columns = st.columns(2)
    for column, (index, project) in zip(columns, enumerate(remaining[row_start : row_start + 2], start=row_start + 2)):
        with column:
            project_card(project, actions=True, index=index)
