from __future__ import annotations

import html
import streamlit as st

from dashboard.data_loader import load_dashboard_metadata
from portfolio.content.projects import PROJECTS
from ui.components import section_card
from ui.navigation import route_href
from ui.theme import current_theme


theme = current_theme()

project = next(item for item in PROJECTS if item["slug"] == "job-market-intelligence")
data_pipeline_href = route_href("/data_pipeline")
market_dashboard_href = route_href("/market_dashboard")

metadata = {}
try:
    metadata = load_dashboard_metadata()
    source_rows = metadata.get("source_job_postings_rows", "1.6M+")
    sample_rows = metadata.get("sample_job_postings_rows", "Hosted sample")
    skill_rows = metadata.get("sample_job_skills_rows", "667,829")
except Exception:
    source_rows = "1.6M+"
    sample_rows = "Hosted sample"
    skill_rows = "667,829"
    st.warning("Dataset metadata unavailable. Generate the hosted sample data before sharing this portfolio.")

source_value = f"{source_rows:,}" if isinstance(source_rows, int) else html.escape(str(source_rows))
sample_value = f"{sample_rows:,}" if isinstance(sample_rows, int) else html.escape(str(sample_rows))
skill_rows_value = f"{skill_rows:,}" if isinstance(skill_rows, int) else html.escape(str(skill_rows))

tech_markup = "".join(
    f'<span class="project-tech-pill">{html.escape(technology)}</span>'
    for technology in project["technologies"][:6]
)

st.markdown(
    f"""
    <section class="project-overview-header">
        <div class="project-overview-badges">
            <span class="project-verified-badge"><span aria-hidden="true"></span>Verified Project</span>
            <span class="project-scale-badge">1.6M+ Job Postings</span>
        </div>
        <h1>Job Market Intelligence</h1>
        <p>Explore hiring demand, salaries, technical skills, remote-work patterns, and market trends across 1.6M+ job postings.</p>
        <div class="project-tech-stack">{tech_markup}</div>
        <div class="project-header-actions">
            <a class="portfolio-button portfolio-button-primary" href="{market_dashboard_href}" target="_self">Explore Dashboard</a>
            <a class="portfolio-button project-header-secondary-action" href="{html.escape(project["repository_url"])}" rel="noreferrer">View on GitHub</a>
        </div>
        <div class="project-evidence-compact" aria-label="Project evidence">
            <div class="project-evidence-item">
                <strong>{source_value}</strong>
                <span>Source Postings</span>
            </div>
            <div class="project-evidence-item">
                <strong>{sample_value}</strong>
                <span>Hosted Sample</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

problem_solution = [
    (
        "The Problem",
        "Job-market data is noisy and difficult to analyze because of inconsistent locations, missing salary values, duplicate relationships, aggregator companies, and unstructured posting records.",
    ),
    (
        "The Solution",
        "A validated Data Engineering pipeline prepares, stores, models, tests, and delivers analytics-ready job-market data through an interactive dashboard.",
    ),
]
problem_cols = st.columns(2)
for col, (title, body) in zip(problem_cols, problem_solution):
    with col:
        section_card(title, body, class_name="job-intelligence-hover-card")

st.markdown(
    f'<a class="project-overview-architecture-link" href="{data_pipeline_href}" target="_self">View technical architecture -&gt;</a>',
    unsafe_allow_html=True,
)

case_sections = [
    (
        "My Role",
        "Designed the project structure, SQL models, quality checks, documentation, and dashboard experience.",
    ),
    (
        "Key Features",
        "KPIs and filters for hiring demand, skill demand, salary analysis, company rankings, remote-work patterns, and monthly trends.",
    ),
    (
        "Key Results",
        f"{source_value} source postings processed, {sample_value} hosted sample postings, {skill_rows_value} job-skill rows, 241 distinct skills, and dashboard-ready analytical outputs.",
    ),
    (
        "Limitations",
        "Salary coverage is incomplete, company names may include aggregators, remote status is inferred from source fields, and the hosted dashboard uses a sample for deployment performance.",
    ),
]

for index in range(0, len(case_sections), 2):
    cols = st.columns(2)
    for col, (title, body) in zip(cols, case_sections[index : index + 2]):
        with col:
            section_card(title, body, class_name="job-intelligence-hover-card")
