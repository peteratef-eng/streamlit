from __future__ import annotations

import streamlit as st

from portfolio.content.projects import PROJECTS
from ui.components import project_card

st.title("Projects")

projects = sorted(PROJECTS, key=lambda item: item.get("sort_order", 999))
if len(projects) == 1:
    project_card(projects[0], actions=True, featured=True)
else:
    for row_start in range(0, len(projects), 2):
        columns = st.columns(2)
        for column, (index, project) in zip(columns, enumerate(projects[row_start : row_start + 2], start=row_start + 1)):
            with column:
                project_card(project, actions=True, index=index)
