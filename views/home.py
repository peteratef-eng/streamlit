from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

from portfolio.content.profile import PROFILE, SPECIALTIES
from portfolio.content.projects import PROJECTS
from ui.navigation import route_href
from ui.project_cards import project_card_html

ROOT = Path(__file__).resolve().parents[1]


@st.cache_data(show_spinner=False)
def asset_data_uri(path_value: str, mime_type: str) -> str:
    path = Path(path_value)
    if not path.is_file():
        return ""
    return f"data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def render_html(markup: str) -> None:
    """Keep HTML out of Markdown code blocks without changing its text content."""
    st.markdown("\n".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


photo = asset_data_uri(str(ROOT / "assets/profile/peter-atef-hero.jpg"), "image/jpeg")
resume = asset_data_uri(str(ROOT / PROFILE["resume_path"]), "application/pdf")
resume_href = resume or html.escape(PROFILE["resume_path"], quote=True)
resume_attr = ' download="Peter_Atef_Resume_2026.pdf"' if resume else ""
contact_href = route_href("/contact")
weather_href = route_href("/weather_pipeline")
portrait = (
    f'<img src="{photo}" alt="Peter Atef" width="400" height="400">'
    if photo else '<span class="pa-portrait-fallback">PA</span>'
)
stack = "".join(f"<span>{html.escape(item)}</span>" for item in SPECIALTIES[:5])

render_html(f'''
<section class="pa-hero">
    <div class="pa-hero-copy">
        <p class="pa-eyebrow"><span></span> PETER ATEF / DATA PORTFOLIO</p>
        <h1>Junior<br>Data Engineer<span class="pa-heading-dot">.</span></h1>
        <p class="pa-hero-lead">{html.escape(PROFILE["hero_subtitle"])}</p>
        <p class="pa-hero-context">{html.escape(PROFILE["hero_subtitle_secondary"])}</p>
        <div class="pa-hero-actions">
            <a class="pa-button pa-button-copper pa-hero-primary" href="{weather_href}" target="_self">Explore my work <span aria-hidden="true">↗</span></a>
            <a class="pa-button pa-button-outline" href="{resume_href}"{resume_attr}>Download resume <span aria-hidden="true">↓</span></a>
        </div>
        <div class="pa-hero-stack"><span>CORE STACK</span><div>{stack}</div></div>
    </div>
    <aside class="pa-profile-card" aria-label="Peter Atef profile">
        <div class="pa-portrait">{portrait}<span class="pa-photo-caption">BASED IN {html.escape(PROFILE["location"].upper())}</span></div>
        <div class="pa-profile-info">
            <p class="pa-availability"><span></span>Open to opportunities</p>
            <h2>{html.escape(PROFILE["full_name"])}</h2>
            <p>{html.escape(PROFILE["title"])}</p>
            <div class="pa-profile-links">
                <a href="{html.escape(PROFILE["github_url"], quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
                <a href="{html.escape(PROFILE["linkedin_url"], quote=True)}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
                <a href="{contact_href}" target="_self">Contact ↗</a>
            </div>
        </div>
    </aside>
</section>
<div class="pa-focus"><span class="pa-focus-label">CURRENT FOCUS</span><p>{html.escape(PROFILE["current_focus_status"])}</p></div>
<section class="pa-section-heading">
    <div><p class="pa-eyebrow">01 / SELECTED WORK</p><h2>From raw data to useful models.</h2></div>
    <p>Implementation, decisions, and source code.</p>
</section>
''')

projects = sorted((project for project in PROJECTS if project.get("featured")), key=lambda project: project.get("sort_order", 999))
for index, project in enumerate(projects, 1):
    st.markdown(project_card_html(project, index=index), unsafe_allow_html=True)

specialties = "".join(f"<span>{html.escape(item)}</span>" for item in SPECIALTIES)
render_html(f'''
<section class="pa-about">
    <div><p class="pa-eyebrow">02 / BACKGROUND</p><h2>Quality first.<br> Then the pipeline.</h2></div>
    <div class="pa-about-copy"><p>{html.escape(PROFILE["bio"])}</p><div class="pa-tags">{specialties}</div></div>
</section>
<section class="pa-contact">
    <div><p class="pa-eyebrow">LET'S TALK</p><h2>Open to Junior Data Engineer opportunities.</h2></div>
    <a class="pa-button pa-button-ink" href="{contact_href}" target="_self">Get in touch <span aria-hidden="true">↗</span></a>
</section>
<footer class="pa-footer"><span>{html.escape(PROFILE["full_name"])} / Data portfolio</span><a href="{html.escape(PROFILE["github_url"], quote=True)}" target="_blank" rel="noopener noreferrer">Built with Python & Streamlit ↗</a></footer>
''')
