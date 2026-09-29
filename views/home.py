from __future__ import annotations

import base64
import html
from pathlib import Path
from textwrap import dedent
from html.parser import HTMLParser

import streamlit as st

from dashboard.data_loader import load_dashboard_metadata
from portfolio.content.profile import PROFILE
from portfolio.content.projects import PROJECTS
from portfolio.content.skills import SKILL_GROUPS
from ui.navigation import route_href
from ui.theme import current_theme


theme = current_theme()

ROOT = Path(__file__).resolve().parents[1]
HERO_PHOTO_PATH = ROOT / "assets" / "profile" / "peter-atef-hero.jpg"
RESUME_PATH = ROOT / PROFILE["resume_path"]


@st.cache_data(show_spinner=False)
def asset_data_uri(path_value: str, mime_type: str) -> str:
    path = Path(path_value)
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def format_int(value: int | str | None) -> str:
    return f"{value:,}" if isinstance(value, int) else html.escape(str(value or "Verified"))


class _MarkupStructureValidator(HTMLParser):
    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1] != tag:
            expected = self.stack[-1] if self.stack else "none"
            raise ValueError(f"Unexpected closing tag </{tag}>; expected </{expected}>.")
        self.stack.pop()


def validate_html_fragment(markup: str, *, expected_start: str, expected_end: str) -> None:
    if markup != markup.strip():
        raise ValueError("HTML fragment contains leading or trailing whitespace.")
    if not markup.startswith(expected_start) or not markup.endswith(expected_end):
        raise ValueError("HTML fragment does not start and end with the expected wrapper.")
    if "```" in markup or "&lt;" in markup:
        raise ValueError("HTML fragment contains Markdown fences or escaped HTML.")
    parser = _MarkupStructureValidator()
    parser.feed(markup)
    parser.close()
    if parser.stack:
        raise ValueError(f"Unclosed HTML tags: {parser.stack}.")


def collapse_html_fragment(markup: str) -> str:
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


project = PROJECTS[0]
metadata = load_dashboard_metadata()
source_rows = metadata.get("source_job_postings_rows")

resume_href = asset_data_uri(str(RESUME_PATH), "application/pdf")
resume_attr = ' download="Peter_Atef_Resume_2026.pdf"' if resume_href else ""
resume_link = resume_href or html.escape(PROFILE["resume_path"])
contact_href = route_href("/contact")
market_dashboard_href = route_href("/market_dashboard")
project_overview_href = route_href("/project_overview")
tech_stack = " - ".join(project["technologies"][:6])
hero_photo_src = asset_data_uri(str(HERO_PHOTO_PATH), "image/jpeg")
hero_photo_markup = (
    f'<img class="hero-profile-image" src="{hero_photo_src}" alt="Portrait of Peter Atef, Junior Data Engineer">'
    if hero_photo_src
    else '<div class="hero-photo-fallback" aria-label="Peter Atef portrait">PA</div>'
)


st.markdown(
    f"""
    <section class="portfolio-hero data-command-hero">
        <div class="data-blueprint-grid" aria-hidden="true"></div>
        <div class="data-background-path data-background-path-1" aria-hidden="true"></div>
        <div class="data-background-path data-background-path-2" aria-hidden="true"></div>
        <span class="data-background-particle data-background-particle-1" aria-hidden="true"></span>
        <span class="data-background-particle data-background-particle-2" aria-hidden="true"></span>
        <div class="hero-copy">
            <div class="hero-kicker">Hi, I'm Peter Atef</div>
            <h1>Junior Data Engineer</h1>
            <p class="hero-description">I build reliable data pipelines and transform raw, messy data into analytics-ready insights using Python, SQL, PostgreSQL, and dbt.</p>
            <div class="hero-value-rotator" aria-hidden="true">
                <span class="hero-value-line hero-value-line-1">Building Reliable Pipelines</span>
                <span class="hero-value-line hero-value-line-2">Transforming Messy Data</span>
                <span class="hero-value-line hero-value-line-3">Validating Trusted Models</span>
                <span class="hero-value-line hero-value-line-4">Delivering Analytics-Ready Insights</span>
            </div>
            <span class="hero-value-accessible-summary sr-only">Building reliable pipelines, transforming messy data, validating trusted models, and delivering analytics-ready insights.</span>
            <div class="hero-actions">
                <a class="portfolio-button portfolio-button-primary hero-primary-action" href="{project_overview_href}" target="_self">EXPLORE MY PROJECT<span aria-hidden="true">-&gt;</span></a>
                <a class="portfolio-button" href="{resume_link}"{resume_attr}>DOWNLOAD RESUME</a>
                <a class="portfolio-button portfolio-button-quiet" href="{contact_href}" target="_self">CONTACT ME</a>
            </div>
        </div>
        <article class="hero-profile-card">
            <div class="hero-profile-media">
                <div class="hero-profile-image-wrap">
                    {hero_photo_markup}
                </div>
            </div>
            <div class="hero-profile-identity hero-profile-info">
                <div class="hero-profile-heading">
                    <h2 class="hero-profile-name">Peter Atef</h2>
                    <p class="hero-profile-role">Junior Data Engineer</p>
                </div>
                <div class="hero-profile-meta">
                    <span class="hero-profile-status">
                        <span class="hero-profile-status-dot" aria-hidden="true"></span>
                        Open to opportunities
                    </span>
                    <span class="hero-profile-location">
                        {html.escape(PROFILE["location"])}
                    </span>
                </div>
            </div>
        </article>
    </section>
    """,
    unsafe_allow_html=True,
)

about_cards = [
    (
        "Professional Story",
        "After working across AI, NLP, data annotation leadership, quality assurance, and integration workflows, I moved deeper into Data Engineering. I enjoy building reliable pipelines, cleaning messy data, validating outputs, and turning raw records into analytics-ready models that teams can trust.",
    ),
    (
        "Current Focus",
        "I am targeting Junior Data Engineer opportunities where I can build dependable pipelines, improve data quality, and create models that make analysis easier for teams.",
    ),
]
about_markup = "".join(
    (
        '<div class="section-card home-about-card" tabindex="0">'
        f'<div class="section-title">{html.escape(title)}</div>'
        f'<div class="section-copy">{html.escape(body)}</div>'
        '</div>'
    )
    for title, body in about_cards
)
st.markdown(
    f"""
    <section class="home-section home-about-section">
        <div class="section-eyebrow">Professional Profile</div>
        <h2>About Me</h2>
        <div class="home-about-grid">{about_markup}</div>
    </section>
    """,
    unsafe_allow_html=True,
)

skills_markup = "".join(
    (
        f'<div class="section-card home-skill-card home-skill-card-{index}" tabindex="0">'
        f'<div class="section-title">{html.escape(title)}</div>'
        '<div class="home-skill-badge-wrap">'
        + "".join(f'<span class="home-skill-badge">{html.escape(skill)}</span>' for skill in skills)
        + '</div>'
        '</div>'
    )
    for index, (title, skills) in enumerate(SKILL_GROUPS.items(), start=1)
)
st.markdown(
    f"""
    <section class="home-section home-skills-section">
        <div class="section-eyebrow">Workflow Skills</div>
        <h2>Skills</h2>
        <p class="home-section-copy">Grouped by the data engineering workflow areas demonstrated across my project and professional background.</p>
        <div class="home-skills-grid">{skills_markup}</div>
    </section>
    """,
    unsafe_allow_html=True,
)

repository_button = (
    f'<a class="portfolio-button" href="{html.escape(project["repository_url"])}" rel="noopener noreferrer">VIEW ON GITHUB</a>'
    if project.get("repository_url")
    else ""
)
cover_src = asset_data_uri(str(ROOT / project["cover_image"]), "image/png") if project.get("cover_image") else ""
preview_markup = (
    f'<img src="{cover_src}" alt="dbt lineage graph: staging models feed intermediate models and analytics marts" loading="lazy">'
    if cover_src
    else '<div class="featured-preview-fallback">Project preview</div>'
)

featured_project_markup = (
    dedent(
        f"""
        <section class="featured-project-card" tabindex="0">
            <div class="featured-project-copy">
                <div class="section-eyebrow">Featured Project</div>
                <h2>{html.escape(project["title"])}</h2>
                <p>{html.escape(project["case_study_sections"]["Business problem"])}</p>
                <p>{html.escape(project["case_study_sections"]["Project summary"])}</p>
                <div class="featured-meta">
                    <span>{html.escape(tech_stack)}</span>
                    <span>{format_int(source_rows)} source postings</span>
                </div>
                <div class="hero-actions">
                    <a class="portfolio-button portfolio-button-primary" href="{market_dashboard_href}" target="_self">VIEW LIVE PROJECT</a>
                    {repository_button}
                </div>
            </div>
            <div class="featured-preview">
        """
    ).strip()
    + "\n"
    + preview_markup
    + "\n"
    + dedent(
        """
            </div>
        </section>
        """
    ).strip()
)
featured_project_markup = collapse_html_fragment(featured_project_markup)
validate_html_fragment(
    featured_project_markup,
    expected_start='<section class="featured-project-card"',
    expected_end="</section>",
)
st.markdown(featured_project_markup, unsafe_allow_html=True)

st.markdown(
    f"""
    <section class="contact-cta home-contact-cta">
        <div>
            <p>Open to Junior Data Engineer opportunities.</p>
        </div>
        <div class="contact-cta-actions">
            <a class="portfolio-button portfolio-button-primary" href="{contact_href}" target="_self">CONTACT ME</a>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)
