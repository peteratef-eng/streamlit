from __future__ import annotations

import unittest
from pathlib import Path

from dashboard.weather_case_study import (
    configured_scope,
    local_day_completeness,
    scope_chart,
    completeness_chart,
)

ROOT = Path(__file__).resolve().parents[1]


class WeatherCaseStudyTest(unittest.TestCase):
    def test_scope_is_expected_response_not_observed_data(self) -> None:
        scope = configured_scope()
        self.assertEqual(set(scope['city']), {'Cairo', 'Alexandria'})
        self.assertEqual(scope['expected_rows'].tolist(), [336, 336])
        self.assertEqual(int(scope['expected_rows'].sum()), 672)

    def test_local_example_preserves_all_timestamps(self) -> None:
        example = local_day_completeness()
        self.assertEqual(int(example['hours_count'].sum()), 336)
        self.assertEqual(len(example), 15)
        self.assertEqual(example.iloc[0].to_dict(), {'local_day': '2026-01-01', 'hours_count': 22})
        self.assertEqual(example.iloc[-1].to_dict(), {'local_day': '2026-01-15', 'hours_count': 2})
        self.assertTrue(example.iloc[1:-1]['hours_count'].eq(24).all())
        self.assertTrue(example.equals(local_day_completeness()))

    def test_charts_match_their_disclosed_inputs(self) -> None:
        scope = scope_chart()
        self.assertEqual(list(scope.data[0].x), [336, 336])
        completeness = completeness_chart()
        self.assertEqual(list(completeness.data[0].y), local_day_completeness()['hours_count'].tolist())
        self.assertEqual(completeness.layout.shapes[0].y0, 24)
        self.assertTrue(scope.layout.xaxis.fixedrange)

    def test_evidence_is_local_and_present(self) -> None:
        for filename in ('dag.png', 'dbt-lineage.png', 'failure-run.png', 'pipeline-flow.gif', 'pipeline-flow-still.png'):
            with self.subTest(filename=filename):
                self.assertGreater((ROOT / 'assets/projects/weather' / filename).stat().st_size, 0)

    def test_page_labels_static_and_documented_evidence(self) -> None:
        view = (ROOT / 'views/weather_pipeline.py').read_text()
        self.assertIn('not a live monitor', view)
        self.assertIn('not independently verified current infrastructure', view)
        self.assertIn('No weather measurements are simulated', view)
        self.assertIn('Next improvements, not completed features', view)
        self.assertIn('Conceptual animation, not live telemetry', view)
        self.assertIn('Play conceptual pipeline animation', view)
        self.assertNotIn('requests.get', view)
        self.assertNotIn('read_sql', view)


if __name__ == '__main__':
    unittest.main()
