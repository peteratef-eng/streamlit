from __future__ import annotations

import html

from ui.navigation import route_href


PREVIEW_STAGES = {
    "weather-forecast-data-platform": ("Open-Meteo API", "Python ELT", "PostgreSQL"),
    "job-market-intelligence": ("Raw data", "PostgreSQL", "dbt marts"),
    "ecommerce-sales-analysis": ("Raw CSV", "Pandas", "Result tables"),
}
PREVIEW_NOTES = {
    "weather-forecast-data-platform": "Airflow orchestrates Python ELT + dbt models/tests",
    "job-market-intelligence": "Warehouse path · separate CSV dashboard",
    "ecommerce-sales-analysis": "Data quality before aggregation",
}


def tool_icon(name: str) -> str:
    paths = {
        "api": '<path d="M7 16H6a4 4 0 0 1-.4-8A6 6 0 0 1 17 6a5 5 0 0 1 1 10h-1"/><path d="m9 13-3 3 3 3m6-6 3 3-3 3m-3-7-1 9"/>',
        "python": '<path d="M6 11V6q0-3 6-3t6 3v5H9q-4 0-4 4v3H3V11z"/><path d="M18 13v5q0 3-6 3t-6-3v-5h9q4 0 4-4V6h2v7z"/><circle cx="10" cy="6" r=".8"/><circle cx="14" cy="18" r=".8"/>',
        "postgres": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
        "airflow": '<path d="M12 12 6 3Q1 4 4 9Zm0 0 9-6q3 5-3 7Zm0 0 6 9q-5 3-7-3Zm0 0-9 6q-3-5 3-7Z"/>',
        "docker": '<path d="M3 13h17q-1 8-9 8-7 0-8-8Zm17 0q3-1 2-4M5 9h4v4H5zm5 0h4v4h-4zm5 0h4v4h-4zM10 4h4v4h-4z"/>',
        "dbt": '<path d="m4 4 16 16M4 20 20 4M8 8h8v8H8z"/>',
        "aws": '<path d="M5 14H4a4 4 0 0 1 0-8 6 6 0 0 1 11-2 5 5 0 1 1 4 10M4 19q8 5 16-1m-4 0h4v4"/>',
    }
    return f'<svg class="wxa-icon wxa-icon-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def weather_architecture_html() -> str:
    """A schematic, not live telemetry. Tool names remain visible at phone width."""
    return (
        '<section class="wxa" aria-label="Weather project architecture">'
        '<div class="wxa-heading"><span>WEATHER / ARCHITECTURE</span><span>IMPLEMENTED IN CODE</span></div>'
        '<div class="wxa-orchestrator">'
        f'<div class="wxa-tool">{tool_icon("airflow")}<div><strong>Apache Airflow</strong><span>Workflow orchestration</span></div></div>'
        '<div class="wxa-tasks"><span>Python</span><b>→</b><span>dbt run</span><b>→</b><span>dbt test</span></div>'
        '</div><div class="wxa-control"><span>Schedules and retries the workflow</span></div>'
        '<div class="wxa-data-path" aria-label="Open-Meteo API to Python ELT to PostgreSQL">'
        f'<div class="wxa-node wxa-source">{tool_icon("api")}<div><small>01 / EXTRACT FROM</small><strong>Open-Meteo API</strong><span>Hourly forecast JSON</span></div></div>'
        '<span class="wxa-arrow" aria-hidden="true">→</span>'
        f'<div class="wxa-node wxa-python">{tool_icon("python")}<div><small>02 / INGEST WITH</small><strong>Python ELT</strong><span>Save raw JSON · validate units<br>Upsert city-hour records</span></div></div>'
        '<span class="wxa-arrow" aria-hidden="true">→</span>'
        f'<div class="wxa-node wxa-database">{tool_icon("postgres")}<div><small>03 / LOAD INTO</small><strong>PostgreSQL</strong><span>Hourly records</span>'
        f'<div class="wxa-dbt">{tool_icon("dbt")}<span><b>dbt models + tests</b><br>Staging → daily marts</span></div></div></div>'
        '</div><div class="wxa-runtime">'
        f'<div>{tool_icon("docker")}<span><strong>Docker Compose</strong><small>Container runtime</small></span></div>'
        f'<div>{tool_icon("aws")}<span><strong>AWS EC2</strong><small>README-documented deployment</small></span></div>'
        '</div><p class="wxa-note">Architecture schematic, not live telemetry. dbt runs in PostgreSQL. AWS deployment is not independently verified.</p>'
        '</section>'
    )


def project_card_html(project: dict, *, index: int = 1, compact: bool = False) -> str:
    """Render an escaped project card, with an implementation map, not live telemetry."""
    slug = project.get("slug", "")
    stages = PREVIEW_STAGES.get(slug, tuple(project.get("technologies", [])[:3]))
    nodes = '<span class="pa-map-arrow" aria-hidden="true">↓</span>'.join(
        f'<span class="pa-map-node"><span>{number:02}</span>{html.escape(label)}</span>'
        for number, label in enumerate(stages, 1)
    )
    tags = "".join(f'<span>{html.escape(item)}</span>' for item in project.get("technologies", [])[:6])
    demo_url = project.get("demo_url") or "/market_dashboard"
    case_url = project.get("case_study_route") or demo_url
    primary_url = route_href(case_url) if case_url.startswith("/") else case_url
    primary_label = "View case study" if project.get("case_study_route") or project.get("demo_label") else "Explore dashboard"
    secondary = ""
    if demo_url != case_url:
        href = route_href(demo_url) if demo_url.startswith("/") else demo_url
        secondary_label = 'Explore Dashboard (sample)' if slug == 'weather-forecast-data-platform' else 'Dashboard'
        secondary = f'<a class="pa-text-link" href="{html.escape(href, quote=True)}" target="_self">{secondary_label} ↗</a>'
    repository = project.get("repository_url", "")
    source = (
        f'<a class="pa-text-link" href="{html.escape(repository, quote=True)}" target="_blank" rel="noopener noreferrer">Source code ↗</a>'
        if repository else ""
    )
    classes = "pa-project pa-project-compact" if compact else "pa-project"
    if slug == "weather-forecast-data-platform":
        classes += " pa-project-weather"
        map_markup = weather_architecture_html()
    else:
        map_markup = (
            '<div class="pa-project-map">'
            f'<div class="pa-map-top"><span>IMPLEMENTATION MAP</span><span>{index:02}</span></div>'
            f'<div class="pa-map-flow">{nodes}</div>'
            f'<p class="pa-map-note">{html.escape(PREVIEW_NOTES.get(slug, "Project workflow"))}</p></div>'
        )
    intro = (
        f'<div class="pa-project-category">{html.escape(project.get("category", ""))}<span>{html.escape(project.get("status", ""))}</span></div>'
        f'<h2 class="pa-project-title">{html.escape(project["title"])}</h2>'
        f'<p class="pa-project-description">{html.escape(project.get("short_description", ""))}</p>'
    )
    details = (
        f'<p class="pa-project-metric">{html.escape(project.get("key_metric", ""))}</p>'
        f'<div class="pa-tags">{tags}</div>'
        f'<div class="pa-project-actions"><a class="pa-button pa-button-ink" href="{html.escape(primary_url, quote=True)}" target="_self">{primary_label} <span aria-hidden="true">↗</span></a>{secondary}{source}</div>'
    )
    if slug == "weather-forecast-data-platform":
        return (
            f'<article class="{classes}"><div class="pa-project-body wxa-intro">{intro}</div>'
            f'{map_markup}<div class="pa-project-body wxa-details">{details}</div></article>'
        )
    return f'<article class="{classes}">{map_markup}<div class="pa-project-body">{intro}{details}</div></article>'
