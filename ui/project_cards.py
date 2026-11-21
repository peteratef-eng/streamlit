from __future__ import annotations

import html

from ui.navigation import route_href


PREVIEW_STAGES = {
    "weather-forecast-data-platform": ("Open-Meteo API", "PostgreSQL", "dbt marts"),
    "job-market-intelligence": ("Raw data", "PostgreSQL", "dbt marts"),
    "ecommerce-sales-analysis": ("Raw CSV", "Pandas", "Result tables"),
}
PREVIEW_NOTES = {
    "weather-forecast-data-platform": "Airflow: ingest → model → test",
    "job-market-intelligence": "Warehouse path · separate CSV dashboard",
    "ecommerce-sales-analysis": "Data quality before aggregation",
}


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
        secondary = f'<a class="pa-text-link" href="{html.escape(href, quote=True)}" target="_self">Dashboard ↗</a>'
    repository = project.get("repository_url", "")
    source = (
        f'<a class="pa-text-link" href="{html.escape(repository, quote=True)}" target="_blank" rel="noopener noreferrer">Source code ↗</a>'
        if repository else ""
    )
    classes = "pa-project pa-project-compact" if compact else "pa-project"
    return (
        f'<article class="{classes}">'
        '<div class="pa-project-map">'
        f'<div class="pa-map-top"><span>IMPLEMENTATION MAP</span><span>{index:02}</span></div>'
        f'<div class="pa-map-flow">{nodes}</div>'
        f'<p class="pa-map-note">{html.escape(PREVIEW_NOTES.get(slug, "Project workflow"))}</p>'
        '</div><div class="pa-project-body">'
        f'<div class="pa-project-category">{html.escape(project.get("category", ""))}<span>{html.escape(project.get("status", ""))}</span></div>'
        f'<h2 class="pa-project-title">{html.escape(project["title"])}</h2>'
        f'<p class="pa-project-description">{html.escape(project["short_description"])}</p>'
        f'<p class="pa-project-metric">{html.escape(project.get("key_metric", ""))}</p>'
        f'<div class="pa-tags">{tags}</div>'
        f'<div class="pa-project-actions"><a class="pa-button pa-button-ink" href="{html.escape(primary_url, quote=True)}" target="_self">{primary_label} <span aria-hidden="true">↗</span></a>{secondary}{source}</div>'
        '</div></article>'
    )
