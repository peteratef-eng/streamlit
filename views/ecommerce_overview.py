from __future__ import annotations

import html
import streamlit as st

from portfolio.content.projects import PROJECTS
from ui.components import section_card
from ui.navigation import route_href
from ui.theme import current_theme


theme = current_theme()

project = next(item for item in PROJECTS if item["slug"] == "ecommerce-sales-analysis")
ecommerce_dashboard_href = route_href("/ecommerce_dashboard")

analysis_tools = ["Python", "Pandas", "NumPy", "Matplotlib", "Jupyter"]
tech_markup = "".join(f'<span class="project-tech-pill">{html.escape(tool)}</span>' for tool in analysis_tools)

st.markdown(
    f"""
    <section class="project-overview-header">
        <div class="project-overview-badges">
            <span class="project-verified-badge"><span aria-hidden="true"></span>Data Analysis Project</span>
            <span class="project-scale-badge">541K+ Transactions Analyzed</span>
        </div>
        <h1>E-Commerce Sales Analysis</h1>
        <p>Exploratory analysis of 541,909 UK online-retail invoice lines with Python and Pandas &mdash; cleaning, reconciling, and analyzing net sales, products, and customer value.</p>
        <div class="project-tech-stack">{tech_markup}</div>
        <div class="project-header-actions">
            <a class="portfolio-button portfolio-button-primary" href="{ecommerce_dashboard_href}" target="_self">Explore Dashboard</a>
            <a class="portfolio-button project-header-secondary-action" href="{html.escape(project["repository_url"])}" rel="noreferrer">View on GitHub</a>
        </div>
        <div class="project-evidence-compact" aria-label="Project evidence">
            <div class="project-evidence-item">
                <strong>541,909</strong>
                <span>Transactions Analyzed</span>
            </div>
            <div class="project-evidence-item">
                <strong>&pound;9.75M</strong>
                <span>Net Sales</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

problem_solution = [
    (
        "The Problem",
        "Raw e-commerce transaction data is noisy: duplicate rows, cancellations and returns, missing customer "
        "identifiers, and non-product line items (postage, fees, manual adjustments) can distort revenue and "
        "product rankings if they are not identified before analysis.",
    ),
    (
        "The Approach",
        "Clean and reconcile a full year of UK retail transactions into gross and net sales datasets, then answer "
        "core business questions: real net revenue, top markets, top products, and the most valuable customers.",
    ),
]
problem_cols = st.columns(2)
for col, (title, body) in zip(problem_cols, problem_solution):
    with col:
        section_card(title, body, class_name="job-intelligence-hover-card")

section_card(
    "Dataset",
    "UCI Online Retail Dataset (via Kaggle) — 541,909 invoice lines from a UK-based online retailer, "
    "covering December 2010 to December 2011, in GBP. Each row is a single product line within an invoice, "
    "so one invoice can span multiple rows.",
    class_name="job-intelligence-hover-card",
)

approach_steps = [
    "Loaded the raw CSV (ISO-8859-1 encoding) and inspected structure, dtypes, and missing values.",
    "Assessed data quality: Description missing in 0.27% of rows, CustomerID missing in 24.93%, and 5,268 exact "
    "duplicate rows identified.",
    "Removed exact duplicates; kept rows with a missing CustomerID for overall, product, and country analysis, "
    "and excluded them only from customer-level analysis.",
    "Split the cleaned data into a gross sales dataset (positive quantities and prices only) and a net sales "
    "dataset (cancellations and returns retained so they reduce revenue).",
    "Excluded non-product stock codes (postage, manual adjustments, and accounting entries) from product-level "
    "rankings.",
    "Aggregated the net data into monthly, country, product, and customer summary tables, then exported them "
    "as the analysis result files.",
]
approach_markup = "".join(f"<li>{html.escape(step)}</li>" for step in approach_steps)
st.markdown(
    f"""
    <div class="section-card timeline-card job-intelligence-hover-card" tabindex="0">
        <div class="section-title">Approach</div>
        <ul>{approach_markup}</ul>
    </div>
    """,
    unsafe_allow_html=True,
)

case_sections = [
    (
        "Key Findings",
        "Net sales were approximately £9.75M after cancellations and returns reduced gross sales "
        "(~£10.64M) by about 8.4%. The United Kingdom accounted for approximately 84% of net sales. "
        "The top-performing product by net sales was REGENCY CAKESTAND 3 TIER (~£164,459).",
    ),
    (
        "Limitations",
        "The dataset covers a single UK-based retailer over one year, so findings may not generalize. The final "
        "month (December 2011) is partial — the data ends on December 9, 2011. Approximately 25% of "
        "transactions have no linked CustomerID and are excluded from customer-level analysis.",
    ),
]

case_cols = st.columns(2)
for col, (title, body) in zip(case_cols, case_sections):
    with col:
        section_card(title, body, class_name="job-intelligence-hover-card")
