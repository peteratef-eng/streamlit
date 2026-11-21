from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

from portfolio.content.profile import PROFILE, SPECIALTIES
from portfolio.content.projects import PROJECTS
from ui.project_cards import project_card_html

ROOT = Path(__file__).resolve().parents[1]


def asset_data_uri(path_value: str, mime_type: str) -> str:
    path = Path(path_value)
    if not path.is_file():
        return ""
    return f"data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def escape(value: str) -> str:
    return html.escape(value, quote=True)


photo = asset_data_uri(str(ROOT / "assets/profile/peter-atef-hero.jpg"), "image/jpeg")
resume = asset_data_uri(str(ROOT / PROFILE["resume_path"]), "application/pdf")
resume_href = resume or escape(PROFILE["resume_path"])
resume_attr = ' download="Peter_Atef_Resume_2026.pdf"' if resume else ""
portrait = f'<img src="{photo}" alt="Peter Atef" width="72" height="72">' if photo else '<span class="mn-monogram">PA</span>'
projects = sorted((project for project in PROJECTS if project.get("featured")), key=lambda project: project.get("sort_order", 999))
project_markup = "".join(project_card_html(project, index=index) for index, project in enumerate(projects, 1))
stack = "".join(f"<span>{escape(item)}</span>" for item in SPECIALTIES)

markup = f'''
<div class="mn-home">
<aside class="mn-identity">
    <a class="mn-person" href="./" target="_self">{portrait}<span>DATA ENGINEERING<br>PORTFOLIO / 2026</span></a>
    <h1>Peter Atef<span>.</span></h1>
    <p class="mn-role">Junior Data Engineer</p>
    <p class="mn-statement">Reliable pipelines.<br> Data you can trust.</p>
    <p class="mn-intro">Python, SQL and a quality-first approach to turning raw records into useful models.</p>
    <nav class="mn-jumps" aria-label="Home sections">
        <a href="#selected-work" target="_self"><span>01</span> Selected work</a>
        <a href="#background" target="_self"><span>02</span> Background</a>
        <a href="#contact" target="_self"><span>03</span> Get in touch</a>
    </nav>
    <a class="mn-resume" href="{resume_href}"{resume_attr}>Download resume <span aria-hidden="true">↗</span></a>
    <div class="mn-socials"><a href="{escape(PROFILE['github_url'])}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="{escape(PROFILE['linkedin_url'])}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a></div>
    <p class="mn-location">{escape(PROFILE['location'])} <span>·</span> Open to opportunities</p>
</aside>
<main class="mn-content">
    <section class="mn-opening"><p class="mn-eyebrow">BUILD / VALIDATE / EXPLAIN</p><p>{escape(PROFILE['hero_subtitle'])}</p><p class="mn-opening-secondary">{escape(PROFILE['hero_subtitle_secondary'])}</p></section>
    <section id="selected-work" class="mn-work"><div class="mn-section-label"><span>01 / SELECTED WORK</span><span>3 PROJECTS</span></div>{project_markup}</section>
    <section id="background" class="mn-background"><div class="mn-section-label"><span>02 / BACKGROUND</span></div><h2>Quality first.<br>Then the pipeline.</h2><p>{escape(PROFILE['bio'])}</p><div class="mn-stack">{stack}</div><div class="mn-focus"><span>CURRENT FOCUS</span><p>{escape(PROFILE['current_focus_status'])}</p></div></section>
    <section id="contact" class="mn-contact"><p class="mn-eyebrow">03 / GET IN TOUCH</p><h2>Let's build something<br>that holds up.</h2><p>{escape(PROFILE['availability'])}</p><a class="mn-contact-link" href="./contact" target="_self">Start a conversation <span aria-hidden="true">↗</span></a></section>
    <footer class="mn-footer"><span>Peter Atef / Data portfolio</span><span>Built with Python & Streamlit</span></footer>
</main>
</div>
'''
st.markdown("\n".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)
