from __future__ import annotations

import unittest

from portfolio.content.projects import PROJECTS
from ui.project_cards import project_card_html


class ProjectCardTest(unittest.TestCase):
    def test_weather_is_case_study_not_live_demo(self) -> None:
        weather = next(project for project in PROJECTS if project["slug"] == "weather-forecast-data-platform")
        markup = project_card_html(weather)
        self.assertIn('href="./weather_pipeline"', markup)
        self.assertIn("View case study", markup)
        self.assertNotIn("Live Demo", markup)
        self.assertIn('class="wxa-orchestrator"', markup)
        self.assertIn("Apache Airflow", markup)
        self.assertIn("Workflow orchestration", markup)
        flow = markup[markup.index('class="wxa-data-path"'):]
        stages = [flow.index(label) for label in ("Open-Meteo API", "Python ELT", "PostgreSQL")]
        self.assertEqual(stages, sorted(stages))
        for tool in ("Python ELT", "PostgreSQL", "dbt", "Apache Airflow", "Docker Compose", "AWS EC2"):
            self.assertIn(tool, markup)
        self.assertIn("README-documented deployment", markup)
        self.assertIn("not independently verified", markup)
        self.assertIn("not live telemetry", markup)
        self.assertLess(markup.index('class="wxa-orchestrator"'), markup.index('class="wxa-data-path"'))
        self.assertIn(weather["repository_url"], markup)

    def test_job_market_map_does_not_imply_dbt_dashboard_feed(self) -> None:
        job = next(project for project in PROJECTS if project["slug"] == "job-market-intelligence")
        markup = project_card_html(job)
        self.assertIn("separate CSV dashboard", markup)
        self.assertIn('href="./project_overview"', markup)
        self.assertIn('href="./market_dashboard"', markup)
        self.assertNotIn("Airflow", markup)

    def test_text_and_link_attributes_are_escaped(self) -> None:
        project = {"title": '<script>alert("x")</script>', "short_description": "A & B", "demo_url": '/test?x="quote"'}
        markup = project_card_html(project)
        self.assertNotIn("<script>", markup)
        self.assertIn("&lt;script&gt;", markup)
        self.assertIn("A &amp; B", markup)
        self.assertIn("&quot;quote&quot;", markup)

    def test_all_projects_render_compact_and_full(self) -> None:
        for project in PROJECTS:
            for compact in (False, True):
                with self.subTest(slug=project["slug"], compact=compact):
                    markup = project_card_html(project, compact=compact)
                    self.assertTrue(markup.startswith('<article class="pa-project'))
                    self.assertTrue(markup.endswith("</article>"))
                    self.assertIn("Source code", markup)
                    self.assertNotIn("Project preview", markup)
                    self.assertNotIn(">DATA<", markup)


if __name__ == "__main__":
    unittest.main()
