from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

from portfolio.content.profile import PROFILE


def resume_data_uri(path_value: str) -> str:
    resume_file = Path(path_value)
    if not resume_file.exists():
        return ""
    encoded = base64.b64encode(resume_file.read_bytes()).decode("ascii")
    return f"data:application/pdf;base64,{encoded}"

st.title("Let's Build Something Reliable")
st.markdown("I'm open to Junior Data Engineer opportunities where I can build dependable pipelines, improve data quality, and make analytics easier for teams.")

badge_cols = st.columns([0.28, 0.22, 0.5])
with badge_cols[0]:
    st.caption("Available for opportunities")
with badge_cols[1]:
    st.caption(f"Based in {PROFILE['location']}")

send_email_url = PROFILE["mailto_url"]
linkedin_url = PROFILE.get("linkedin_url", "")
github_url = PROFILE.get("github_url", "")

cards = st.columns(3)
with cards[0]:
    st.markdown(
        f"""
        <div class="contact-hover-card" tabindex="0">
            <div class="section-title">Email</div>
            <p>{html.escape(PROFILE["email"])}</p>
            <a class="contact-card-action" href="{html.escape(send_email_url)}">Send Email</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with cards[1]:
    linkedin_action = (
        f'<a class="contact-card-action contact-card-action-secondary" href="{html.escape(linkedin_url)}" rel="noreferrer">View LinkedIn</a>'
        if linkedin_url.startswith("https://")
        else ""
    )
    st.markdown(
        f"""
        <div class="contact-hover-card" tabindex="0">
            <div class="section-title">LinkedIn</div>
            <p>peter-atef-eng</p>
            {linkedin_action}
        </div>
        """,
        unsafe_allow_html=True,
    )

with cards[2]:
    github_action = (
        f'<a class="contact-card-action contact-card-action-secondary" href="{html.escape(github_url)}" rel="noreferrer">View GitHub</a>'
        if github_url.startswith("https://")
        else ""
    )
    st.markdown(
        f"""
        <div class="contact-hover-card" tabindex="0">
            <div class="section-title">GitHub</div>
            <p>peteratef-eng</p>
            {github_action}
        </div>
        """,
        unsafe_allow_html=True,
    )

encoded_resume = resume_data_uri(PROFILE["resume_path"])
if encoded_resume:
    st.markdown(
        f"""
        <div class="contact-hover-card contact-resume-strip" tabindex="0">
            <div>
                <div class="section-title">Want the full overview?</div>
                <div class="section-copy">Download my resume for experience, skills, and project details.</div>
            </div>
            <a class="contact-card-action" href="{encoded_resume}" download="Peter_Atef_Resume_2026.pdf">Download Resume</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
