from __future__ import annotations

import base64
import html
from pathlib import Path
from textwrap import dedent
from urllib.parse import urlparse

import streamlit as st

from portfolio.content.profile import PROFILE
from ui.navigation import PORTFOLIO_PAGES, SIDEBAR_PROJECTS, route_href


SIDEBAR_PORTFOLIO_LINKS = [page for page in PORTFOLIO_PAGES if page.get("sidebar")]

KPI_ICONS = {
    "Total postings": "JP",
    "Companies": "CO",
    "Countries": "GL",
    "Skills": "SK",
    "Avg salary": "$",
    "Median salary": "MD",
    "Remote share": "RM",
    "Salary coverage": "%",
}

FOOTER_EMAIL_URL = PROFILE["mailto_url"]
PROFILE_PHOTO_PATH = Path(__file__).resolve().parents[1] / "assets" / "profile" / "peter.jpg"


def _route_slug(route: str) -> str:
    return "home" if route == "/" else route.strip("/").replace("_", "-").replace("/", "-")


def _normalize_route(route: str | None) -> str:
    if not route:
        return "/"
    parsed_path = urlparse(route).path or "/"
    normalized = "/" + parsed_path.strip("/")
    return "/" if normalized == "/" else normalized


def _current_path(active_route: str | None = None) -> str:
    if active_route is not None:
        return _normalize_route(active_route)

    try:
        context_url = st.context.url
    except Exception:
        return "/"

    if not context_url:
        return "/"

    return _normalize_route(context_url)


def _sidebar_page_link(page: dict[str, object], active: bool, group: str) -> None:
    route = str(page["route"])
    key = f"sidebar_{group}_{_route_slug(route)}"
    if active:
        st.markdown(
            f"""
            <style>
            .st-key-{key} [data-testid="stPageLink"] a {{
                color: var(--data-blue) !important;
                background: rgba(37, 99, 235, .09) !important;
                font-weight: 700 !important;
            }}
            .st-key-{key} [data-testid="stPageLink"] a::before {{
                background: #2563eb !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, .12) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    with st.container(key=key):
        st.page_link(str(page["path"]), label=str(page["label"]), use_container_width=True)


@st.cache_data(show_spinner=False)
def _profile_photo_markup() -> str:
    if not PROFILE_PHOTO_PATH.exists():
        return '<div class="brand-icon">P</div>'

    encoded_photo = base64.b64encode(PROFILE_PHOTO_PATH.read_bytes()).decode("ascii")
    return (
        '<img class="brand-photo" '
        'src="data:image/jpeg;base64,'
        f'{encoded_photo}" '
        'alt="Peter profile photo">'
    )


def sidebar_brand() -> None:
    profile_photo = _profile_photo_markup()
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand sidebar-profile-card">
            {profile_photo}
            <div>
                <div class="brand-title">{html.escape(PROFILE["full_name"])}</div>
                <div class="brand-subtitle">Junior Data Engineer</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_projects(active_route: str | None = None) -> None:
    current_path = _current_path(active_route)
    project_routes = {
        page["route"]
        for project in SIDEBAR_PROJECTS
        for page in project["pages"]
    }
    projects_open = current_path in project_routes
    st.sidebar.markdown(
        '<section class="sidebar-projects native-sidebar-projects">',
        unsafe_allow_html=True,
    )
    with st.sidebar.expander("PROJECTS", expanded=projects_open):
        for project in SIDEBAR_PROJECTS:
            project_open = any(page["route"] == current_path for page in project["pages"])
            project_active_class = " is-active" if project_open else ""
            st.markdown(
                '<div class="sidebar-project-expander'
                f'{project_active_class}">'
                '<div class="sidebar-project-summary sidebar-project-card">'
                '<div class="sidebar-project-card-header">'
                '<span class="sidebar-project-icon" aria-hidden="true">'
                '<svg viewBox="0 0 24 24" focusable="false">'
                '<path d="M6 7c0-1.7 12-1.7 12 0v10c0 1.7-12 1.7-12 0V7z"></path>'
                '<path d="M6 7c0 1.7 12 1.7 12 0"></path>'
                '<path d="M6 12c0 1.7 12 1.7 12 0"></path>'
                '</svg>'
                '</span>'
                '<div class="sidebar-project-copy">'
                f'<div class="sidebar-project-name">{html.escape(project["name"])}</div>'
                f'<div class="sidebar-project-type">{html.escape(project["type"])}</div>'
                '</div>'
                '</div>'
                '<div class="sidebar-project-mini-lineage" aria-hidden="true">'
                '<span class="sidebar-mini-stage sidebar-mini-source"></span>'
                '<span class="sidebar-mini-track"></span>'
                '<span class="sidebar-mini-stage sidebar-mini-model"></span>'
                '<span class="sidebar-mini-track"></span>'
                '<span class="sidebar-mini-stage sidebar-mini-mart"></span>'
                '<span class="sidebar-mini-packet"></span>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<nav class="sidebar-project-links native-sidebar-links">', unsafe_allow_html=True)
            for page in project["pages"]:
                page_active = page["route"] == current_path
                _sidebar_page_link(page, page_active, "project")
            st.markdown('</nav>', unsafe_allow_html=True)
    st.sidebar.markdown('</section>', unsafe_allow_html=True)


def sidebar_portfolio(active_route: str | None = None) -> None:
    current_path = _current_path(active_route)
    portfolio_routes = {link["route"] for link in SIDEBAR_PORTFOLIO_LINKS}
    portfolio_open = current_path in portfolio_routes
    st.sidebar.markdown(
        '<section class="sidebar-portfolio native-sidebar-portfolio">',
        unsafe_allow_html=True,
    )
    with st.sidebar.expander("PORTFOLIO", expanded=portfolio_open):
        for link in SIDEBAR_PORTFOLIO_LINKS:
            _sidebar_page_link(link, link["route"] == current_path, "portfolio")
    st.sidebar.markdown('</section>', unsafe_allow_html=True)


def app_header(kicker: str, title: str, subtitle: str, location: str) -> dict[str, str]:
    st.markdown(
        f"""
        <div class="page-header page-header-{html.escape(location)}">
            <div class="product-kicker">{html.escape(kicker)}</div>
            <h1 class="product-title">{html.escape(title)}</h1>
            <div class="product-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return {}


def sidebar_bottom(active_route: str | None = None) -> None:
    sidebar_portfolio(active_route)
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    sidebar_projects(active_route)
    st.sidebar.markdown('<div class="sidebar-profile-divider"></div>', unsafe_allow_html=True)
    sidebar_brand()
    links = []
    if PROFILE.get("github_url"):
        links.append(f'<a href="{html.escape(PROFILE["github_url"])}" rel="noreferrer">GitHub</a>')
    if PROFILE.get("linkedin_url"):
        links.append(f'<a href="{html.escape(PROFILE["linkedin_url"])}" rel="noreferrer">LinkedIn</a>')
    links_markup = " | ".join(links)
    st.sidebar.markdown(
        f"""
        <nav class="sidebar-links sidebar-social-links">{links_markup}</nav>
        """,
        unsafe_allow_html=True,
    )


def section_card(title: str, body: str, class_name: str = "") -> None:
    classes = " ".join(["section-card", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    st.markdown(
        f"""
        <div class="{html.escape(classes)}"{tabindex}>
            <div class="section-title">{html.escape(title)}</div>
            <div class="section-copy">{html.escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_grid(values: dict[str, str]) -> None:
    notes = {
        "Total postings": "Filtered posting count",
        "Companies": "Distinct organizations",
        "Countries": "Distinct job countries",
        "Skills": "Distinct technical skills",
        "Avg salary": "Yearly salary records only",
        "Median salary": "Yearly salary records only",
        "Remote share": "Remote status classification",
        "Salary coverage": "Postings with salary data",
    }
    cols = st.columns(4)
    for index, (label, value) in enumerate(values.items()):
        icon = KPI_ICONS.get(label, "*")
        note = notes.get(label, "")
        if value == "N/A" and label in {"Avg salary", "Median salary"}:
            note = "No yearly salary records for this selection"
        with cols[index % 4]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{html.escape(icon)}</div>
                    <div class="kpi-label">{html.escape(label)}</div>
                    <div class="kpi-value">{html.escape(value)}</div>
                    <div class="kpi-note">{html.escape(note)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def pipeline_visual(class_name: str = "") -> None:
    steps = [
        ("01", "DATA SOURCES", "Raw CSV Files", "Source tables", "source", "M5 4h10l2 2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4z M9 12h6 M9 16h6"),
        ("02", "INGEST & PREPARE", "Python / Pandas", "Load, clean, sample", "process", "M8 9l-4 3 4 3 M16 9l4 3-4 3 M14 5l-4 14"),
        ("03", "DATA WAREHOUSE", "PostgreSQL", "Relational storage", "warehouse", "M5 7c0-2 3.1-4 7-4s7 2 7 4-3.1 4-7 4-7-2-7-4z M5 7v10c0 2 3.1 4 7 4s7-2 7-4V7 M5 12c0 2 3.1 4 7 4s7-2 7-4"),
        ("04", "TRANSFORM & MODEL", "dbt", "Staging -> marts", "transform", "M12 3l8 4-8 4-8-4 8-4z M4 12l8 4 8-4 M4 17l8 4 8-4"),
        ("05", "VALIDATE", "dbt Tests + SQL Checks", "Integrity checks", "validate", "M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6l7-3z M9 12l2 2 4-5"),
        ("06", "SERVE & EXPLORE", "Streamlit Dashboard", "Interactive insights", "serve", "M4 19V5h16v14H4z M8 15l3-3 2 2 3-5 M8 19v-2 M12 19v-3 M16 19v-6"),
    ]
    step_classes = " ".join(["pipeline-architecture-card", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    markup = "".join(
        (
            f'<div class="{html.escape(step_classes)} pipeline-stage-{index} pipeline-category-{html.escape(category)}"{tabindex}>'
            '<span class="pipeline-stage-icon" aria-hidden="true">'
            f'<svg viewBox="0 0 24 24" role="img" aria-label="{html.escape(label)} icon">'
            f'<path d="{path}"></path>'
            '</svg>'
            '</span>'
            f'<span class="pipeline-stage-number">{number}</span>'
            f'<span class="pipeline-stage-category">{html.escape(category_label)}</span>'
            f'<strong>{html.escape(label)}</strong>'
            f'<small>{html.escape(output)}</small>'
            '<span class="pipeline-stage-status">Processing</span>'
            '</div>'
        )
        for index, (number, category_label, label, output, category, path) in enumerate(steps, start=1)
    )
    st.markdown(
        (
            '<div class="pipeline-architecture-shell" aria-label="Data engineering architecture from source files to dashboard">'
            '<div class="pipeline-architecture-viewport">'
            '<div class="pipeline pipeline-architecture" role="list">'
            '<section class="pipeline-orchestration-band" aria-label="Apache Airflow orchestration layer">'
            '<div class="pipeline-orchestration-main">'
            '<span class="pipeline-orchestration-icon" aria-hidden="true">'
            '<svg viewBox="0 0 24 24"><path d="M4 7h5m6 0h5M9 7a3 3 0 1 0 6 0 3 3 0 0 0-6 0z M6 17h12M8 14l-2 3 2 3M16 14l2 3-2 3"></path></svg>'
            '</span>'
            '<span><small>ORCHESTRATION LAYER</small><strong>Apache Airflow</strong><em>Schedules and coordinates pipeline tasks</em></span>'
            '</div>'
            '<div class="pipeline-orchestration-status">'
            '<span>Scheduled DAG</span><span>Task dependencies</span><span>Monitoring &amp; retries</span>'
            '</div>'
            '<span class="pipeline-airflow-stem pipeline-airflow-stem-2" aria-hidden="true"></span>'
            '<span class="pipeline-airflow-stem pipeline-airflow-stem-4" aria-hidden="true"></span>'
            '<span class="pipeline-airflow-stem pipeline-airflow-stem-5" aria-hidden="true"></span>'
            '<span class="pipeline-airflow-stem pipeline-airflow-stem-6" aria-hidden="true"></span>'
            '</section>'
            '<div class="pipeline-stage-grid">'
            f'{markup}'
            '</div>'
            '<div class="data-flow-lane" aria-label="Data flows from source files to the Streamlit dashboard">'
            '<svg class="data-flow-svg" aria-hidden="true">'
            '<defs><marker id="pipelineDataArrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L8,4 L0,8 Z"></path></marker><filter id="pipelinePulseGlow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2" result="blur"></feGaussianBlur><feMerge><feMergeNode in="blur"></feMergeNode><feMergeNode in="SourceGraphic"></feMergeNode></feMerge></filter></defs>'
            '<path id="pipelineDataFlowPath" class="data-flow-path" d="M98 26 H1083"></path>'
            '<path class="data-flow-arrow-segments" d="M98 26 H296 M296 26 H493 M493 26 H690 M690 26 H886 M886 26 H1083"></path>'
            '<path class="data-flow-stems" d="M98 4 V26 M296 4 V26 M493 4 V26 M690 4 V26 M886 4 V26 M1083 4 V26"></path>'
            '<g class="data-packet">'
            '<circle class="pulse-trail pulse-trail-2" r="2.5" cx="0" cy="0"><animateMotion dur="7s" begin="0.18s" repeatCount="indefinite" calcMode="linear"><mpath href="#pipelineDataFlowPath"></mpath></animateMotion></circle>'
            '<circle class="pulse-trail pulse-trail-1" r="3.5" cx="0" cy="0"><animateMotion dur="7s" begin="0.09s" repeatCount="indefinite" calcMode="linear"><mpath href="#pipelineDataFlowPath"></mpath></animateMotion></circle>'
            '<circle class="data-flow-pulse" r="5" cx="0" cy="0" filter="url(#pipelinePulseGlow)"><animateMotion dur="7s" repeatCount="indefinite" calcMode="linear"><mpath href="#pipelineDataFlowPath"></mpath></animateMotion></circle>'
            '</g>'
            '</svg>'
            '</div>'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def insight(text: str) -> None:
    st.markdown(f'<div class="insight">{html.escape(text)}</div>', unsafe_allow_html=True)


def active_filter_chips(filters: dict[str, list[str] | tuple[float, float] | tuple[object, object] | None]) -> None:
    chips = []
    for label, value in filters.items():
        if value is None:
            continue
        if isinstance(value, list) and value:
            display = ", ".join(str(item) for item in value[:3])
            if len(value) > 3:
                display += f" +{len(value) - 3}"
            chips.append(f"{label}: {display}")
        elif isinstance(value, tuple):
            chips.append(f"{label}: active")
    if not chips:
        st.markdown('<div class="active-filter-wrap"><span class="active-chip">No active filters</span></div>', unsafe_allow_html=True)
        return
    markup = "".join(f'<span class="active-chip">{html.escape(chip)}</span>' for chip in chips)
    st.markdown(f'<div class="active-filter-wrap">{markup}</div>', unsafe_allow_html=True)


def footer() -> None:
    links = []
    if PROFILE.get("email"):
        links.append(f'<a href="{html.escape(FOOTER_EMAIL_URL)}">Email</a>')
    if PROFILE.get("linkedin_url"):
        links.append(f'<a href="{html.escape(PROFILE["linkedin_url"])}" rel="noreferrer">LinkedIn</a>')
    if PROFILE.get("github_url"):
        links.append(f'<a href="{html.escape(PROFILE["github_url"])}" rel="noreferrer">GitHub</a>')
    links_markup = " | ".join(links)
    st.markdown(
        f'<div class="footer">Peter &mdash; Junior Data Engineer<br>{html.escape(PROFILE["availability"])}<br>{links_markup}</div>',
        unsafe_allow_html=True,
    )


def metric_status_card(sample_rows: int, source_rows: int | str, class_name: str = "") -> None:
    source_value = f"{source_rows:,}" if isinstance(source_rows, int) else html.escape(str(source_rows))
    sample_value = f"{sample_rows:,}" if isinstance(sample_rows, int) else html.escape(str(sample_rows))
    classes = " ".join(["dataset-card", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    st.markdown(
        f"""
        <div class="{html.escape(classes)}"{tabindex}>
            <div class="dataset-icon">DB</div>
            <div class="dataset-metrics">
                <div>
                    <div class="dataset-value">{sample_value}</div>
                    <div class="dataset-label">hosted sample postings</div>
                </div>
                <div>
                    <div class="dataset-value">{source_value}</div>
                    <div class="dataset-label">source postings</div>
                </div>
                <div>
                    <div class="dataset-value">Verified</div>
                    <div class="dataset-label">real project data</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def purpose_cards(class_name: str = "") -> None:
    cards = [
        ("Understand Demand", "See which roles, companies, and markets show the strongest hiring activity."),
        ("Compare Salaries", "Review salary patterns across roles, countries, and remote-work status where salary data exists."),
        ("Track Skills", "Explore the technical skills most associated with job postings and Data Engineer demand."),
    ]
    columns = st.columns(3)
    for column, (title, body) in zip(columns, cards):
        with column:
            section_card(title, body, class_name=class_name)


def challenge_points(class_name: str = "") -> None:
    points = [
        "Inconsistent locations",
        "Missing salary values",
        "Duplicate relationships",
        "Aggregator companies",
        "Noisy job-posting records",
    ]
    markup = "".join(f'<span class="challenge-chip">{html.escape(point)}</span>' for point in points)
    classes = " ".join(["challenge-panel", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    st.markdown(f'<div class="{html.escape(classes)}"{tabindex}>{markup}</div>', unsafe_allow_html=True)


def chart_card(title: str, description: str):
    st.markdown(
        f"""
        <div class="chart-card-heading">
            <div class="section-title">{html.escape(title)}</div>
            <div class="section-copy">{html.escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_row(items: list[str]) -> None:
    markup = "".join(f'<span class="meta-pill">{html.escape(item)}</span>' for item in items)
    st.markdown(f"<div>{markup}</div>", unsafe_allow_html=True)


def _project_pipeline_visual() -> str:
    stages = [
        ("raw", "Raw Data", "Source", "M4 5h16v14H4z M7 9h10 M7 13h7"),
        ("etl", "Python ETL", "Pandas", "M12 3v18 M5 8h14 M5 16h14"),
        ("warehouse project-warehouse-stage", "PostgreSQL", "Warehouse", "M6 6c0-1.7 12-1.7 12 0v12c0 1.7-12 1.7-12 0V6z M6 6c0 1.7 12 1.7 12 0 M6 12c0 1.7 12 1.7 12 0"),
        ("marts", "dbt Marts", "Analytics", "M5 18V8l7-4 7 4v10 M9 18v-6h6v6"),
        ("dashboard", "Dashboard", "Streamlit", "M4 5h16v12H4z M8 21h8 M12 17v4"),
    ]
    stage_markup = []
    for index, (class_name, label, detail, icon_path) in enumerate(stages, start=1):
        stage_markup.append(
            f"""
            <div class="project-pipeline-stage project-pipeline-stage-{index} {class_name}">
                <svg class="project-pipeline-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="{icon_path}"></path>
                </svg>
                <span class="project-pipeline-label">{html.escape(label)}</span>
                <span class="project-pipeline-detail">{html.escape(detail)}</span>
            </div>
            """
        )
        if index < len(stages):
            stage_markup.append(f'<div class="project-pipeline-connector project-pipeline-connector-{index}" aria-hidden="true"></div>')

    particles = "".join(
        f'<span class="project-pipeline-particle project-pipeline-particle-{index}" aria-hidden="true"></span>'
        for index in range(1, 4)
    )
    return (
        '<div class="project-visual project-pipeline-banner" '
        'aria-label="Data pipeline from raw data through Python ETL, PostgreSQL, dbt marts, and dashboard">'
        '<div class="project-pipeline-track">'
        f'{particles}'
        f'{"".join(stage_markup)}'
        '</div>'
        '</div>'
    )


def project_card(project: dict, *, actions: bool = False, featured: bool = False) -> None:
    tech_markup = "".join(
        f'<span class="meta-pill">{html.escape(tech)}</span>' for tech in project.get("technologies", [])[:6]
    )
    action_markup = ""
    if actions:
        demo_url = project.get("demo_url") or "/market_dashboard"
        repository_url = project.get("repository_url", "")
        repository_link = (
            f'<a class="project-action" href="{html.escape(repository_url)}" rel="noopener noreferrer">GitHub Repository</a>'
            if repository_url
            else ""
        )
        case_study_route = project.get("case_study_route", "")
        case_study_link = (
            ""
            if not case_study_route or featured
            else f'<a class="project-action project-action-primary" href="{route_href(case_study_route)}" target="_self">View Case Study</a>'
        )
        demo_class = "project-action project-action-primary" if not case_study_link else "project-action"
        demo_target_attr = ' target="_self"' if demo_url.startswith("/") else ""
        demo_href = route_href(demo_url) if demo_url.startswith("/") else demo_url
        action_markup = (
            '<div class="project-actions">'
            f'{case_study_link}'
            f'<a class="{demo_class}" href="{html.escape(demo_href)}"{demo_target_attr}>Live Demo</a>'
            f'{repository_link}'
            '</div>'
        )
    card_class = "project-card project-card-featured" if featured else "project-card"
    visual_markup = (
        _project_pipeline_visual()
        if featured and project.get("slug") == "job-market-intelligence"
        else '<div class="project-visual">DATA</div>'
    )
    st.markdown(
        f"""
        <div class="{card_class}">
            {visual_markup}
            <div class="project-meta">{html.escape(project.get("category", ""))} | {html.escape(project.get("status", ""))}</div>
            <div class="project-title">{html.escape(project["title"])}</div>
            <div class="section-copy">{html.escape(project["short_description"])}</div>
            <div class="project-metric">{html.escape(project.get("key_metric", ""))}</div>
            <div>{tech_markup}</div>
            {action_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _experience_card_html(entry: dict, class_name: str = "") -> str:
    responsibilities = "".join(
        f"<li>{html.escape(item)}</li>" for item in entry.get("responsibilities", [])
    )
    technologies = "".join(
        f'<span class="meta-pill">{html.escape(item)}</span>' for item in entry.get("technologies", [])
    )
    classes = " ".join(["timeline-card", "experience-card", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    summary = (
        f'<div class="section-copy">{html.escape(entry["summary"])}</div>'
        if entry.get("summary")
        else ""
    )
    return dedent(
        f"""
        <article class="{html.escape(classes)}"{tabindex}>
        <div class="timeline-date">{html.escape(entry["start_date"])} - {html.escape(entry["end_date"])}</div>
        <div class="project-title">{html.escape(entry["role"])}</div>
        <div class="project-meta">{html.escape(entry["company"])} | {html.escape(entry.get("location", ""))}</div>
        {summary}
        <ul class="experience-list">{responsibilities}</ul>
        <div class="experience-tags">{technologies}</div>
        </article>
        """
    ).strip()


def render_experience_card(entry: dict, class_name: str = "") -> None:
    st.markdown(
        _experience_card_html(entry, class_name=class_name),
        unsafe_allow_html=True,
    )


def timeline_entry(entry: dict, class_name: str = "") -> None:
    render_experience_card(entry, class_name=class_name)


def skill_group_card(title: str, skills: list[str], class_name: str = "") -> None:
    skills_markup = "".join(
        f'<span class="challenge-chip skill-chip">{html.escape(skill)}</span>' for skill in skills
    )
    classes = " ".join(["section-card", "skill-card", class_name]).strip()
    tabindex = ' tabindex="0"' if class_name else ""
    st.markdown(
        f"""
        <div class="{html.escape(classes)}"{tabindex}>
            <div class="section-title">{html.escape(title)}</div>
            <div class="skill-chip-wrap">{skills_markup}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
