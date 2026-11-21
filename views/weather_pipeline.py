from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from dashboard.weather_case_study import configured_scope, local_day_completeness, scope_chart, completeness_chart

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/peteratef-eng/weather-forecast-data-platform"
COMMIT = "32c2b1f"


def markup(value: str) -> None:
    st.markdown("\n".join(line.strip() for line in value.splitlines()), unsafe_allow_html=True)


def heading(number: str, title: str, detail: str) -> None:
    markup(f'<section class="wx-section-head"><p class="pa-eyebrow">{number}</p><h2>{html.escape(title)}</h2><p>{html.escape(detail)}</p></section>')


def cards(items: list[tuple[str, str, str]], class_name: str = "") -> None:
    body = "".join(
        f'<article class="wx-card"><span class="wx-card-label">{html.escape(label)}</span><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></article>'
        for label, title, body in items
    )
    markup(f'<div class="wx-card-grid {class_name}">{body}</div>')


markup(f'''
<section class="wx-hero">
    <p class="pa-eyebrow">FEATURED CASE STUDY / DATA ENGINEERING</p>
    <h1>Weather Forecast<br>Data Platform<span>.</span></h1>
    <p class="wx-hero-lead">A daily forecast pipeline, built to rerun safely and fail visibly.</p>
    <p class="wx-hero-copy">Open-Meteo forecasts for Cairo and Alexandria, preserved as raw JSON, validated before loading, and modeled into Cairo-local daily marts.</p>
    <div class="pa-tags"><span>Python</span><span>PostgreSQL</span><span>dbt</span><span>Apache Airflow</span><span>Docker Compose</span><span>AWS EC2</span></div>
    <div class="pa-hero-actions"><a class="pa-button pa-button-copper" href="{REPOSITORY}" target="_blank" rel="noopener noreferrer">Explore source code ↗</a><a class="pa-button pa-button-outline" href="./weather_dashboard" target="_self">Explore Dashboard (sample) ↗</a><a class="pa-button pa-button-outline" href="#pipeline" target="_self">Follow the pipeline ↓</a></div>
</section>
<div class="wx-evidence-note"><strong>Repository case study, not a live monitor.</strong> Code and screenshots are from commit {COMMIT}. AWS deployment and experiment outcomes below are documented in the project README, not independently verified current infrastructure.</div>
<div class="wx-metrics">
    <div><span>CONFIGURED SCOPE</span><strong>2 cities</strong><p>Cairo + Alexandria</p></div>
    <div><span>REQUESTED HORIZON</span><strong>14 days</strong><p>Hourly forecasts per city</p></div>
    <div><span>TABLE GRAIN</span><strong>city × hour</strong><p>Unique key for safe upserts</p></div>
    <div><span>AIRFLOW SCHEDULE</span><strong>@daily</strong><p>3 sequential tasks</p></div>
</div>
<div id="pipeline"></div>
''')
heading("01 / THE DATA PATH", "One forecast, every layer.", "Airflow orchestrates the workflow. The ingestion script stores the raw response before validation and database writes.")
# Local static assets only; toggling playback does not contact the source systems.
play_animation = st.toggle("Play conceptual pipeline animation", value=True, key="weather_pipeline_animation")
with st.container(key="weather_pipeline_figure"):
    st.image(
        str(ROOT / "assets/projects/weather" / ("pipeline-flow.gif" if play_animation else "pipeline-flow-still.png")),
        caption="Conceptual animation, not live telemetry. Arrows show data movement; Airflow orchestrates the tasks inside Docker on the README-documented EC2 host.",
        use_container_width=True,
    )
steps = [
    ("01", "Fetch", "Open-Meteo API", "Five hourly variables, 14-day horizon, 30-second request timeout."),
    ("02", "Preserve", "Timestamped raw JSON", "Keep the API response in data/raw before checking units or loading."),
    ("03", "Validate", "Units before writes", "Temperature, precipitation, humidity, wind and cloud-cover units must match."),
    ("04", "Load", "PostgreSQL upsert", "ON CONFLICT (city, time) DO UPDATE refreshes revised forecast values."),
    ("05", "Model", "dbt staging → daily mart", "Keep UTC traceability; group metrics by Africa/Cairo calendar day."),
    ("06", "Test", "Schema + grain checks", "Not-null tests and a singular city/day uniqueness test."),
]
markup('<div class="wx-pipeline">' + ''.join(f'<article><span class="wx-step-number">{number} / {label}</span><h3>{title}</h3><p>{detail}</p></article>' for number, label, title, detail in steps) + '</div>')
st.caption("Implementation sources: src/main.py; weather_dbt/models/stg_weather_hourly.sql; mart_weather_daily.sql; schema.yml; tests/assert_mart_unique_city_day.sql.")

heading("02 / SCALE & TIME", "What the configuration means.", "Engineering visuals derived from repository settings and timestamp transformations. These are not measured production volumes or observed weather charts.")
st.subheader("Expected response size by city")
st.caption("Calculated from src/main.py: 14 forecast days × 24 hourly timestamps = 336 rows per city, or 672 across two cities for a full response. This is not the retained database row count.")
st.plotly_chart(scope_chart(), use_container_width=True, config={"displayModeBar": False}, key="weather_expected_scope")
markup('<div class="wx-chart-summary"><strong>336 expected rows / city</strong><span>672 total expected hourly records · 5 weather variables</span></div>')

st.subheader("Why a local day is not always 24 rows")
st.caption("Reproducible timestamp-only example: 336 consecutive UTC hours starting 1 Jan 2026 00:00 UTC, converted with Africa/Cairo, then grouped by local day using the mart logic. No weather measurements are simulated.")
st.plotly_chart(completeness_chart(), use_container_width=True, config={"displayModeBar": False}, key="weather_local_completeness")
example = local_day_completeness()
first_hours = int(example.iloc[0]["hours_count"])
last_hours = int(example.iloc[-1]["hours_count"])
markup(f'<div class="wx-chart-summary"><strong>First day: {first_hours} hours · last day: {last_hours} hours</strong><span>Interior days: 24 hours in this January example. DST transitions can produce 23- or 25-hour local days.</span></div>')
st.write("The mart exposes hours_count instead of silently dropping partial days. Temperature averages from a short overnight slice should not be compared with a full day as if coverage were equal.")
with st.expander("Inspect the exact chart inputs and derivation"):
    st.write("Expected per-response scope, calculated from the configured horizon:")
    st.dataframe(configured_scope(), hide_index=True, use_container_width=True)
    st.write("Timestamp-only local-day example, one city. Source logic: stg_weather_hourly.sql and mart_weather_daily.sql.")
    st.dataframe(example, hide_index=True, use_container_width=True)
    st.caption("No API, PostgreSQL, Airflow, or AWS connection is made by this page. A real weather trend needs a committed, dated mart export; none is included in this repository snapshot.")

heading("03 / ORCHESTRATION", "Three tasks. No silent success.", "The implemented DAG runs ingestion first, then dbt models, then tests. A failed upstream task prevents downstream work from pretending the run succeeded.")
cards([
    ("TASK 01", "run_main_py", "Runs python src/main.py. Each city is attempted; collected city failures raise at the end so the task turns red."),
    ("TASK 02", "run_dbt_run", "Runs dbt run inside weather_dbt after successful ingestion."),
    ("TASK 03", "run_dbt_test", "Runs dbt test after model execution, including the mart grain check."),
])
markup('<div class="wx-retry-band"><strong>2 retries</strong><span>5-minute retry delay</span><span>catchup=False</span><span>Failure callback: SmtpNotifier</span></div>')
st.caption("Source: airflow/dags/weather_pipeline_dag.py. Two retries allow up to three attempts, not a guarantee of successful recovery.")
with st.expander("Repository evidence: Airflow DAG and dbt lineage"):
    st.image(str(ROOT / "assets/projects/weather/dag.png"), caption="Cropped repository DAG screenshot. Historical success state, not current run status.", use_container_width=True)
    st.image(str(ROOT / "assets/projects/weather/dbt-lineage.png"), caption="Repository dbt lineage: raw hourly source → staging → daily mart → grain test.", use_container_width=True)

heading("04 / DEPLOYMENT", "A batch job does not need an always-on server.", "Documented deployment: Docker Compose on AWS EC2, with EventBridge Scheduler starting and stopping the instance around the daily DAG.")
cards([
    ("RUNTIME", "Docker Compose", "Airflow API server, scheduler, DAG processor and triggerer. LocalExecutor coordinates tasks; a custom Airflow image pins dbt-core and dbt-postgres."),
    ("ISOLATION", "Two PostgreSQL services", "Airflow metadata and weather data use separate PostgreSQL 16 services and persistent volumes. The project is mounted into Airflow containers."),
    ("DOCUMENTED HOST", "EC2 in Frankfurt", "The README describes Amazon Linux 2023 and m7i-flex.large, upgraded after the 1 GB host ran out of memory. This is deployment history, not a live account check."),
])
markup('''<div class="wx-schedule">
<div><span>23:45 UTC</span><strong>Start instance</strong><p>EventBridge starts EC2; containers auto-restart.</p></div>
<div><span>00:00 UTC</span><strong>Run the DAG</strong><p>Ingest → dbt run → dbt test.</p></div>
<div><span>00:30 UTC</span><strong>Stop instance</strong><p>EventBridge stops EC2.</p></div>
</div>''')
markup('<div class="wx-evidence-note"><strong>Documented operating window: 45 minutes / day.</strong> This is the intended schedule, not a measured run duration or billing result. Stopping EC2 is not proof that all AWS charges stop. The fixed stop time also needs enough room for delayed runs and retries.</div>')
st.write("The README describes a limited IAM scheduler role, restricted Airflow/SSH network access, and an AWS Budget alert. The Compose file is based on a development template; this case study does not certify production hardening or the current security configuration.")
st.caption("Sources: airflow/docker-compose.yaml; airflow/Dockerfile; README sections Deployment and Challenges & Debugging.")

heading("05 / BREAK IT ON PURPOSE", "A failure should reach a person.", "The README documents an intentional database-outage experiment, with screenshots of the failed tasks and the notification email.")
cards([
    ("INJECT", "Stop the weather database", "The documented experiment stopped the weather PostgreSQL container, then manually triggered the DAG."),
    ("OBSERVE", "Fail after the third attempt", "Ingestion failed across the allowed attempts. Downstream dbt tasks were marked upstream_failed instead of running on a failed load."),
    ("NOTIFY & RECOVER", "Alert, then restore", "The README records the final-failure email, a database restart and a subsequent successful run. SMTP credentials belong in the Airflow Connection, not the portfolio."),
])
with st.expander("Repository evidence: failed run"):
    st.image(str(ROOT / "assets/projects/weather/failure-run.png"), caption="Repository screenshot: ingestion failed at try 3; dbt run and dbt test show Upstream Failed. Historical test, not a current incident.", use_container_width=True)
st.write("One debugging lesson in the README: SSL on port 465 and STARTTLS were enabled together, so the alert did not arrive at first. The callback error was found in task logs; after correcting the SMTP configuration, the failure experiment was repeated. A red task alone does not prove notifications work.")

heading("06 / MODEL & TRADE-OFFS", "Design for revised forecasts, not append-only history.", "The current implementation refreshes forecasts at the city/hour grain. It does not retain every forecast revision as a separate historical snapshot.")
cards([
    ("RAW TABLE", "weather_hourly", "One city per UTC hour. The unique (city, time) constraint supports idempotent updates; raw API JSON stays on local disk."),
    ("STAGING VIEW", "stg_weather_hourly", "Keeps weather_time_utc and derives Cairo-local weather_time with PostgreSQL AT TIME ZONE."),
    ("DAILY VIEW", "mart_weather_daily", "Groups by city and local day. Aggregates temperature, precipitation, humidity, wind and cloud cover, with hours_count for coverage."),
])
markup('''<div class="wx-next"><h3>Next improvements, not completed features</h3><p>Ingestion unit tests and CI · freshness checks · config-driven cities · S3 raw storage · air-quality ingestion · automated EC2 deployment · a dashboard backed by a dated daily-mart export.</p></div>''')
markup(f'<footer class="wx-footer"><span>Case study source: {COMMIT} · static repository evidence</span><a href="{REPOSITORY}" target="_blank" rel="noopener noreferrer">Read implementation and README ↗</a></footer>')
