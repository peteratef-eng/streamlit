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
    }
]
