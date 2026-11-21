from __future__ import annotations

import unittest
from pathlib import Path

from portfolio.content.projects import PROJECTS
from ui.navigation import SIDEBAR_PROJECTS, route_href

ROOT = Path(__file__).resolve().parents[1]


class PortfolioProjectNavigationTest(unittest.TestCase):
    def test_weather_is_first_featured_project(self) -> None:
        featured = sorted(
            (project for project in PROJECTS if project.get("featured")),
            key=lambda project: project.get("sort_order", 999),
        )
        self.assertEqual(featured[0]["slug"], "weather-forecast-data-platform")

    def test_weather_case_study_route_is_registered(self) -> None:
        weather = next(project for project in PROJECTS if project["slug"] == "weather-forecast-data-platform")
        page = SIDEBAR_PROJECTS[0]["pages"][0]
        self.assertEqual(page["path"], weather["case_study_page"])
        self.assertEqual(page["route"], weather["demo_url"])
        self.assertEqual(route_href(page["route"]), "./weather_pipeline")
        self.assertTrue((ROOT / page["path"]).is_file())
        self.assertEqual(weather["demo_label"], "View Case Study")
        self.assertEqual(weather["case_study_route"], "")

    def test_job_market_selection_does_not_depend_on_order(self) -> None:
        for name in ("about", "project_overview"):
            with self.subTest(view=name):
                source = (ROOT / "views" / f"{name}.py").read_text()
                self.assertNotIn("PROJECTS[0]", source)
                self.assertIn('item["slug"] == "job-market-intelligence"', source)
        project = next(item for item in reversed(PROJECTS) if item["slug"] == "job-market-intelligence")
        self.assertTrue(project["repository_url"].endswith("/job-market-data-engineering"))

    def test_routes_are_unique_and_views_exist(self) -> None:
        pages = [page for project in SIDEBAR_PROJECTS for page in project["pages"]]
        routes = [page["url_path"] for page in pages]
        self.assertEqual(len(routes), len(set(routes)))
        for page in pages:
            with self.subTest(page=page["path"]):
                self.assertTrue((ROOT / page["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
