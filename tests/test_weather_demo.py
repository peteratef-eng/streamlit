from __future__ import annotations
import unittest
from datetime import date
from pathlib import Path
from dashboard.weather_demo import sample_daily_mart, filter_sample, temperature_chart, precipitation_chart
from ui.navigation import SIDEBAR_PROJECTS
from ui.project_cards import project_card_html
from portfolio.content.projects import PROJECTS

class WeatherDemoTest(unittest.TestCase):
    def test_sample_is_deterministic_at_city_day_grain(self):
        data=sample_daily_mart()
        self.assertTrue(data.equals(sample_daily_mart()))
        self.assertEqual(len(data),30)
        self.assertFalse(data.duplicated(['city','day']).any())
        self.assertTrue((data.min_temp <= data.avg_temp).all())
        self.assertTrue((data.avg_temp <= data.max_temp).all())
        self.assertEqual(set(data.hours_count),{2,22,24})
        self.assertTrue(data.total_precipitation.ge(0).all())

    def test_filters_include_boundaries_and_empty_city_selection(self):
        data=sample_daily_mart()
        sample=filter_sample(data,['Cairo'],date(2026,1,1),date(2026,1,5))
        self.assertEqual(len(sample),5)
        self.assertEqual(len(filter_sample(data,['Cairo'],date(2026,1,1),date(2026,1,5),True)),4)
        self.assertTrue(filter_sample(data,[],date(2026,1,1),date(2026,1,15)).empty)

    def test_charts_follow_selected_city(self):
        selected=sample_daily_mart().query('city == "Cairo"')
        temperature=temperature_chart(selected)
        self.assertEqual(len(temperature.data),3)
        self.assertEqual(list(temperature.data[-1].y),selected.avg_temp.tolist())
        rain=precipitation_chart(selected)
        self.assertEqual(len(rain.data),1)
        self.assertEqual(list(rain.data[0].y),selected.total_precipitation.tolist())

    def test_dashboard_route_and_card_are_honest(self):
        weather=next(p for p in PROJECTS if p['slug']=='weather-forecast-data-platform')
        self.assertTrue(any(p['route']=='/weather_dashboard' for p in SIDEBAR_PROJECTS[0]['pages']))
        self.assertIn('Explore Dashboard (sample)',project_card_html(weather))
        source=(Path(__file__).resolve().parents[1]/'views/weather_dashboard.py').read_text()
        self.assertIn('All values below are synthetic',source)
        self.assertNotIn('requests.get',source)
        self.assertNotIn('read_sql',source)

if __name__=='__main__':
    unittest.main()
