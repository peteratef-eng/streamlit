from __future__ import annotations

import streamlit as st

from dashboard.data_loader import load_dashboard_metadata
from portfolio.content.profile import PROFILE
from portfolio.content.projects import PROJECTS
from ui.components import section_card

st.title("About Me")
metadata = load_dashboard_metadata()
project = next(item for item in PROJECTS if item["slug"] == "job-market-intelligence")

cols = st.columns(2)
with cols[0]:
    section_card("Professional Story", PROFILE["bio"], class_name="about-hover-card")
with cols[1]:
    section_card(
        "Current Focus",
        "I am targeting Data Engineer opportunities where I can build dependable pipelines, improve data quality, and create models that make analysis easier for teams.",
        class_name="about-hover-card",
    )

cols = st.columns(2)
with cols[0]:
    section_card(
        "Background",
        "My experience includes data annotation leadership, quality assurance, structured dataset preparation, API integrations, automation, and cross-functional data workflows.",
        class_name="about-hover-card",
    )
with cols[1]:
    evidence = []
    source_rows = metadata.get("source_job_postings_rows")
    sample_rows = metadata.get("sample_job_postings_rows")
    if source_rows:
        evidence.append(f"{source_rows:,} source postings")
    if sample_rows:
        evidence.append(f"{sample_rows:,} hosted sample postings")
    evidence.append(", ".join(project["technologies"][:6]))
    section_card("Project Evidence", " | ".join(evidence), class_name="about-hover-card")
