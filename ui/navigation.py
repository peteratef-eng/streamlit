from __future__ import annotations

from typing import Any

import streamlit as st


PORTFOLIO_PAGES = [
    {"label": "Home", "path": "views/home.py", "route": "/", "url_path": "", "default": True, "sidebar": True},
    {"label": "About Me", "path": "views/about.py", "route": "/about", "url_path": "about", "sidebar": False},
    {"label": "Experience", "path": "views/experience.py", "route": "/experience", "url_path": "experience", "sidebar": True},
    {"label": "Skills", "path": "views/skills.py", "route": "/skills", "url_path": "skills", "sidebar": False},
    {"label": "Projects", "path": "views/projects.py", "route": "/projects", "url_path": "projects", "sidebar": False},
    {"label": "Contact", "path": "views/contact.py", "route": "/contact", "url_path": "contact", "sidebar": True},
]

SIDEBAR_PROJECTS = [
    {
        "name": "Job Market Intelligence",
        "type": "Data Engineering Project",
        "pages": [
            {"label": "Overview", "path": "views/project_overview.py", "route": "/project_overview", "url_path": "project_overview"},
            {"label": "Market Dashboard", "path": "views/market_dashboard.py", "route": "/market_dashboard", "url_path": "market_dashboard"},
            {"label": "Data Pipeline", "path": "views/data_pipeline.py", "route": "/data_pipeline", "url_path": "data_pipeline"},
            {"label": "Data Quality", "path": "views/data_quality.py", "route": "/data_quality", "url_path": "data_quality"},
        ],
    },
    {
        "name": "E-Commerce Sales Analysis",
        "type": "Data Analysis Project",
        "pages": [
            {"label": "Dashboard", "path": "views/ecommerce_dashboard.py", "route": "/ecommerce_dashboard", "url_path": "ecommerce_dashboard"},
        ],
    },
]


def route_from_page(page: Any) -> str:
    url_path = getattr(page, "url_path", "") or ""
    return f"/{url_path.strip('/')}" if url_path else "/"


def route_href(route: str) -> str:
    route_path = route.strip("/")
    return "./" if not route_path else f"./{route_path}"


def portfolio_navigation() -> st.navigation:
    project_pages = [
        st.Page(page["path"], title=page["label"], url_path=page["url_path"], visibility="hidden")
        for project in SIDEBAR_PROJECTS
        for page in project["pages"]
    ]
    return st.navigation(
        {
            "PORTFOLIO": [
                st.Page(
                    page["path"],
                    title=page["label"],
                    url_path=page["url_path"],
                    default=bool(page.get("default")),
                    visibility="hidden",
                )
                for page in PORTFOLIO_PAGES
            ],
            "PROJECTS": project_pages,
        },
        position="hidden",
    )
