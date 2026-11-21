from pathlib import Path

import streamlit as st

from portfolio.content.projects import PROJECTS

project = next(
    item for item in PROJECTS
    if item["slug"] == "weather-forecast-data-platform"
)

st.title(project["title"])
st.write(project["short_description"])
st.caption("Case study of the repository implementation, not a live pipeline-status monitor.")
st.link_button("View source on GitHub", project["repository_url"])

col1, col2 = st.columns(2)
col1.metric("Configured cities", "2")
col2.metric("Forecast horizon", "14 days")
st.caption("Expected response size: 336 hourly rows per city for a full 14-day forecast.")

st.subheader("Architecture")
st.code(
    "Open-Meteo API -> raw JSON -> PostgreSQL upsert\n"
    "                            -> dbt staging -> daily mart -> dbt tests\n"
    "Airflow: run_main_py -> run_dbt_run -> run_dbt_test",
    language="text",
)

image_path = Path(__file__).resolve().parents[1] / "assets/projects/weather-pipeline.png"
if image_path.exists():
    st.image(str(image_path), caption="Weather pipeline DAG")

st.subheader("Engineering decisions")
for item in [
    "Upsert on (city, time) refreshes revised forecasts without creating duplicate keys.",
    "Raw API JSON is saved before unit validation and database loading.",
    "Request timeouts and Airflow retries make transient API failures visible and retryable.",
    "UTC source timestamps are kept, with Africa/Cairo conversion in dbt staging.",
    "The daily mart exposes hours_count so partial days are visible.",
]:
    st.write(f"- {item}")

st.subheader("Deployment and failure testing")
st.write(
    "The repository documents Docker Compose on AWS EC2, scheduled instance start/stop, "
    "and a deliberate database-outage test of the failure email callback. "
    "See the README for screenshots and deployment details."
)

st.subheader("Next improvements")
st.write(
    "Ingestion unit tests and CI, ingestion timestamps and freshness checks, "
    "air-quality ingestion, and raw JSON storage in S3."
)
