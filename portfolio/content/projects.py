from __future__ import annotations


PROJECTS = [
    {
        "slug": "job-market-intelligence",
        "title": "Job Market Intelligence",
        "short_description": (
            "End-to-end Data Engineering project processing more than 1.6 million job postings with "
            "Python, PostgreSQL, dbt, data-quality checks, and an interactive market dashboard."
        ),
        "full_description": (
            "A complete analytics workflow that transforms raw job posting data into cleaned staging "
            "models, enriched intermediate models, analytical marts, and recruiter-friendly insights."
        ),
        "category": "Data Engineering",
        "year": "2026",
        "status": "Featured",
        "featured": True,
        "technologies": ["Python", "Pandas", "PostgreSQL", "dbt", "SQL", "Streamlit", "Plotly", "Docker"],
        "key_metric": "1.6M+ job postings",
        "cover_image": "assets/projects/job-market-lineage.png",
        "demo_url": "",
        "repository_url": "https://github.com/peteratef-eng/job-market-data-engineering",
        "case_study_page": "views/project_overview.py",
        "case_study_route": "/project_overview",
        "dashboard_page": "views/market_dashboard.py",
        "sort_order": 1,
        "case_study_sections": {
            "Project summary": "Transforms raw job-market data into analytics-ready models and an interactive dashboard.",
            "Business problem": "Hiring data is noisy, incomplete, and difficult to interpret without cleaning, validation, and modeling.",
            "My role": "Designed the project structure, SQL models, quality checks, documentation, and dashboard experience.",
            "Dataset or source": "MotherDuck/DuckDB source tables for job postings, companies, skills, and job-skill relationships.",
            "Architecture": "Raw data, Python/Pandas processing, PostgreSQL, dbt staging and mart models, analytics, and dashboard.",
            "Data pipeline": "Source Data -> Python/Pandas -> PostgreSQL -> dbt Models -> Quality Checks -> Market Insights.",
            "Technologies": "Python, Pandas, PostgreSQL, DuckDB, MotherDuck, dbt, SQL, Streamlit, Plotly, Docker.",
            "Data-quality process": "Checks for row counts, null keys, duplicate IDs, orphan relationships, joins, percentages, and mart grain.",
            "Key features": "KPIs, filters, skill demand, salary analysis, company rankings, remote-work patterns, and monthly trends.",
            "Key results": "Business-ready analysis for demand, salaries, skills, hiring companies, remote work, and market movement.",
            "Challenges and solutions": "Handled missing salary data, aggregator companies, remote-status classification, and hosted sample constraints.",
            "Limitations": "Salary coverage is incomplete, company names may include aggregators, and remote status is inferred from source fields.",
        },
    },
    {
        "slug": "ecommerce-sales-analysis",
        "title": "E-Commerce Sales Analysis",
        "short_description": (
            "Exploratory analysis of 541,909 UK online-retail invoice lines with Python and Pandas, "
            "with most of the effort spent on data quality before trusting any aggregate."
        ),
        "full_description": (
            "Cleaned and reconciled a raw transactional export into gross and net sales datasets, "
            "then analyzed monthly trends, country revenue, product performance, and customer value "
            "in an interactive dashboard."
        ),
        "category": "Data Analysis",
        "year": "TODO",
        "status": "Completed",
        "featured": False,
        "technologies": ["Python", "Pandas", "NumPy", "Plotly", "Streamlit"],
        "key_metric": "541K+ transactions analyzed",
        "cover_image": "TODO",
        "demo_url": "/ecommerce_dashboard",
        "repository_url": "https://github.com/peteratef-eng/ecommerce-sales-analysis",
        "case_study_page": "",
        "dashboard_page": "views/ecommerce_dashboard.py",
        "sort_order": 2,
        "case_study_sections": {
            "Project summary": "Cleans and reconciles UK online-retail transactions into net sales, then analyzes trends, products, and customer value.",
            "Business problem": "Hiring data is noisy, incomplete, and hard to trust without cleaning, validation, and modeling.",
            "My role": "Performed the full analysis: data quality assessment, cleaning decisions, gross/net sales modeling, and visualization.",
            "Dataset or source": "UCI Online Retail Dataset (Kaggle) — 541,909 invoice lines, Dec 2010–Dec 2011, GBP.",
            "Architecture": "Raw CSV, Python/Pandas cleaning and aggregation, exported result tables, Streamlit dashboard.",
            "Data pipeline": "Raw Data -> Pandas Cleaning -> Gross/Net Sales Split -> Aggregated Result Tables -> Dashboard.",
            "Technologies": "Python, Pandas, NumPy, Matplotlib, Jupyter, Plotly, Streamlit.",
            "Data-quality process": "Checked missing values, exact duplicates, negative quantities/prices, zero prices, and non-product stock codes before trusting any aggregate.",
            "Key features": "KPIs, monthly net sales trend, country and product rankings, and customer value analysis.",
            "Key results": "Net sales ~£9.75M after ~8.4% lost to cancellations and returns; UK ~84% of net sales; identified the top product and top customers by spend and by average order value.",
            "Challenges and solutions": "Handled a best-selling product that was fully cancelled, non-product stock codes mixed into product data, and a partial final month.",
            "Limitations": "Customer-level totals exclude ~25% of transactions with no linked CustomerID; only aggregated result tables are shipped with the dashboard, not the raw 44MB source file.",
        },
    },
]
