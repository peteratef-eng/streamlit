from __future__ import annotations

import html

import streamlit as st

from portfolio.content.profile import PROFILE
from ui.styles import inject_global_styles


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


def app_header(kicker: str, title: str, subtitle: str, location: str) -> dict[str, str]:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="product-kicker">{html.escape(kicker)}</div>
            <h1 class="product-title">{html.escape(title)}</h1>
            <div class="product-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return {}


def section_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{html.escape(title)}</div>
            <div class="section-copy">{html.escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_grid(values: dict[str, str]) -> None:
    cols = st.columns(4)
    for index, (label, value) in enumerate(values.items()):
        icon = KPI_ICONS.get(label, "*")
        with cols[index % 4]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{html.escape(icon)}</div>
                    <div class="kpi-label">{html.escape(label)}</div>
                    <div class="kpi-value">{html.escape(value)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def pipeline_visual() -> None:
    steps = [
        ("01", "Raw CSVs"),
        ("02", "Python / Pandas"),
        ("03", "PostgreSQL"),
        ("04", "dbt Models"),
        ("05", "Analytics Marts"),
        ("06", "Streamlit Dashboard"),
    ]
    markup = "".join(
        f'<div class="pipeline-step"><span>{number}</span>{html.escape(label)}</div>'
        for number, label in steps
    )
    st.markdown(f'<div class="pipeline">{markup}</div>', unsafe_allow_html=True)


def insight(text: str) -> None:
    st.markdown(f'<div class="insight">{html.escape(text)}</div>', unsafe_allow_html=True)


def active_filter_chips(
    filters: dict[str, list[str] | tuple[float, float] | tuple[object, object] | None],
) -> None:
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
        st.markdown(
            '<div class="active-filter-wrap"><span class="active-chip">No active filters</span></div>',
            unsafe_allow_html=True,
        )
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
        f'<div class="footer">Peter &mdash; Data Engineer<br>{html.escape(PROFILE["availability"])}<br>{links_markup}</div>',
        unsafe_allow_html=True,
    )


__all__ = [
    "active_filter_chips",
    "app_header",
    "footer",
    "inject_global_styles",
    "insight",
    "kpi_grid",
    "pipeline_visual",
    "section_card",
]
