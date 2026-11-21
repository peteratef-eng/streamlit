from __future__ import annotations

import html
import streamlit as st

from dashboard.data_loader import load_dashboard_metadata
from ui.components import pipeline_visual

st.title("Data Pipeline")
pipeline_visual()

metadata = load_dashboard_metadata()
source_rows = metadata.get("source_job_postings_rows")
sample_rows = metadata.get("sample_job_postings_rows")
skills_rows = metadata.get("sample_job_skills_rows")

pipeline_info = [
    (
        "INPUTS",
        "Source data",
        (
            f"{source_rows:,} verified source postings. Four relational source tables feed the pipeline."
            if source_rows
            else "Verified source postings from four relational source tables feed the pipeline."
        ),
    ),
    (
        "PROCESSING",
        "Engineering workflow",
        (
            f"{sample_rows:,}-posting hosted sample with {skills_rows:,} job-skill relationships. The hosted sample is prepared directly from raw CSVs with Python/Pandas, not exported from dbt marts."
            if sample_rows and skills_rows
            else "The hosted sample is prepared directly from raw CSVs with Python/Pandas, not exported from dbt marts."
        ),
    ),
    (
        "OUTPUTS",
        "Analytics delivery",
        "The Streamlit dashboard reads sample CSVs. The separate PostgreSQL/dbt warehouse workflow builds analytics marts for SQL analysis.",
    ),
]
pipeline_info_markup = "".join(
    (
        f'<div class="section-card pipeline-card pipeline-info-card-{index}" tabindex="0">'
        '<div class="pipeline-info-card-heading">'
        f'<span class="pipeline-info-icon" aria-hidden="true">{index}</span>'
        '<span>'
        f'<small>{html.escape(title)}</small>'
        f'<strong>{html.escape(label)}</strong>'
        '</span>'
        '</div>'
        f'<div class="section-copy">{html.escape(body)}</div>'
        '</div>'
    )
    for index, (title, label, body) in enumerate(pipeline_info, start=1)
)
st.markdown(f'<section class="pipeline-info-grid">{pipeline_info_markup}</section>', unsafe_allow_html=True)


st.subheader("Two separate data paths")
st.markdown("**Warehouse project:** PostgreSQL and dbt build staging, intermediate and mart models for SQL analysis. Airflow orchestration is a planned next step for Job Market, not an implemented DAG.")
st.code("Raw source data -> PostgreSQL -> dbt staging -> intermediate -> marts -> SQL analysis", language="text")
st.markdown("**Hosted dashboard:** the sample preparation script reads raw CSVs directly and writes dashboard CSVs plus metadata. The dashboard loader reads those files; it does not query PostgreSQL or read dbt mart exports.")
st.code("Raw CSVs -> scripts/prepare_dashboard_data.py -> data/dashboard/*.csv + metadata.json\n         -> dashboard/data_loader.py -> Pandas filters -> Streamlit / Plotly", language="text")
st.info("The dbt marts and hosted dashboard are not connected by an export step. The Weather project has its own implemented Airflow DAG, shown in its separate case study.")
