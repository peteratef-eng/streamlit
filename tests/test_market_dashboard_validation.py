from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from dashboard.data_loader import filter_jobs, load_dashboard_data, skills_for_jobs
from dashboard.transformations import (
    high_salary_skills,
    kpi_values,
    monthly_trends,
    remote_salary,
    salary_by_dimension,
    top_counts,
    top_skills,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "dashboard"


def expected_kpis(jobs: pd.DataFrame, skills: pd.DataFrame) -> dict[str, str]:
    salary = jobs["salary_year_avg"].dropna()
    remote_pct = jobs["remote_status"].eq("Remote").sum() / len(jobs) * 100 if len(jobs) else None
    return {
        "Total postings": format_number(len(jobs)),
        "Companies": format_number(jobs["company_id"].nunique()),
        "Countries": format_number(jobs["job_country"].dropna().nunique()),
        "Skills": format_number(skills["clean_skill_name"].dropna().nunique()),
        "Avg salary": format_currency(salary.mean() if not salary.empty else None),
        "Median salary": format_currency(salary.median() if not salary.empty else None),
        "Remote share": f"{remote_pct:.1f}%" if remote_pct is not None else "N/A",
        "Salary coverage": f"{len(salary) / len(jobs) * 100:.1f}%" if len(jobs) else "N/A",
    }


def format_number(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def format_currency(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"${float(value):,.0f}"


def expected_top_counts(df: pd.DataFrame, column: str, limit: int = 15) -> pd.DataFrame:
    if df.empty or column not in df:
        return pd.DataFrame(columns=[column, "postings"])
    return (
        df[column]
        .astype("object")
        .fillna("Unknown")
        .value_counts()
        .head(limit)
        .rename_axis(column)
        .reset_index(name="postings")
    )


def expected_top_skills(skills: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
    if skills.empty:
        return pd.DataFrame(columns=["clean_skill_name", "clean_skill_type", "postings"])
    return (
        skills.dropna(subset=["clean_skill_name"])
        .groupby(["clean_skill_name", "clean_skill_type"], dropna=False)["job_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index(name="postings")
    )


def expected_salary_by_dimension(jobs: pd.DataFrame, column: str, limit: int = 15) -> pd.DataFrame:
    salary_jobs = jobs.dropna(subset=["salary_year_avg"])
    if salary_jobs.empty:
        return pd.DataFrame(columns=[column, "avg_salary", "median_salary", "salary_jobs"])
    return (
        salary_jobs.groupby(column, dropna=False)
        .agg(
            avg_salary=("salary_year_avg", "mean"),
            median_salary=("salary_year_avg", "median"),
            salary_jobs=("job_id", "nunique"),
        )
        .query("salary_jobs >= 3")
        .sort_values("avg_salary", ascending=False)
        .head(limit)
        .reset_index()
    )


def expected_monthly_trends(jobs: pd.DataFrame) -> pd.DataFrame:
    if jobs.empty:
        return pd.DataFrame(columns=["posted_month", "total_jobs", "previous_month_jobs", "job_growth_percentage"])
    monthly = (
        jobs.dropna(subset=["posted_month"])
        .groupby("posted_month")["job_id"]
        .nunique()
        .sort_index()
        .reset_index(name="total_jobs")
    )
    monthly["previous_month_jobs"] = monthly["total_jobs"].shift(1)
    monthly["job_growth_percentage"] = (
        (monthly["total_jobs"] - monthly["previous_month_jobs"])
        / monthly["previous_month_jobs"]
        * 100
    )
    return monthly


def expected_remote_salary(jobs: pd.DataFrame) -> pd.DataFrame:
    salary_jobs = jobs.dropna(subset=["salary_year_avg"])
    if salary_jobs.empty:
        return pd.DataFrame(columns=["remote_status", "avg_salary", "salary_jobs"])
    return (
        salary_jobs.groupby("remote_status", dropna=False)
        .agg(avg_salary=("salary_year_avg", "mean"), salary_jobs=("job_id", "nunique"))
        .reset_index()
    )


def expected_high_salary_skills(jobs: pd.DataFrame, skills: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
    salary_jobs = jobs.dropna(subset=["salary_year_avg"])[["job_id", "salary_year_avg"]]
    if salary_jobs.empty or skills.empty:
        return pd.DataFrame(columns=["clean_skill_name", "avg_salary", "salary_jobs"])
    merged = skills.merge(salary_jobs, on="job_id", how="inner")
    return (
        merged.groupby("clean_skill_name", dropna=False)
        .agg(avg_salary=("salary_year_avg", "mean"), salary_jobs=("job_id", "nunique"))
        .query("salary_jobs >= 3")
        .sort_values("avg_salary", ascending=False)
        .head(limit)
        .reset_index()
    )


class MarketDashboardValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.jobs, cls.skills, cls.metadata = load_dashboard_data(str(DATA_DIR))
        cls.skill_options = sorted(cls.skills["clean_skill_name"].dropna().unique())
        cls.company_options = (
            cls.jobs["clean_company_name"].dropna().value_counts().head(250).index.sort_values().tolist()
        )

    def apply_filters(self, **overrides: object) -> tuple[pd.DataFrame, pd.DataFrame]:
        params = {
            "job_titles": [],
            "countries": [],
            "companies": [],
            "skills_filter": [],
            "remote_statuses": [],
            "salary_range": None,
            "date_range": None,
        }
        params.update(overrides)
        filtered_jobs = filter_jobs(self.jobs, self.skills, **params)
        return filtered_jobs, skills_for_jobs(self.skills, filtered_jobs)

    def assert_frame_matches(self, actual: pd.DataFrame, expected: pd.DataFrame, message: str) -> None:
        assert_frame_equal(actual.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False, atol=1e-9, rtol=1e-9)

    def test_dataset_integrity_hard_invariants(self) -> None:
        self.assertEqual(len(self.jobs), 150_000, "hosted jobs sample row count changed")
        self.assertEqual(len(self.skills), 667_829, "hosted skills sample row count changed")
        self.assertEqual(self.metadata.get("sample_job_postings_rows"), 150_000)
        self.assertEqual(self.metadata.get("source_job_postings_rows"), 1_615_930)
        self.assertEqual(self.jobs["job_id"].isna().sum(), 0, "jobs contain missing job_id values")
        self.assertEqual(self.skills["job_id"].isna().sum(), 0, "skills contain missing job_id values")
        self.assertEqual(self.jobs["job_id"].duplicated().sum(), 0, "jobs contain duplicate job_id values")
        orphan_rows = (~self.skills["job_id"].isin(self.jobs["job_id"])).sum()
        self.assertEqual(orphan_rows, 0, "skills contain orphan job_id values")
        duplicate_relationships = self.skills.duplicated(["job_id", "clean_skill_name"]).sum()
        self.assertEqual(duplicate_relationships, 0, "skills contain duplicate (job_id, clean_skill_name) relationships")

    def test_kpis_match_independent_calculations_for_filter_scenarios(self) -> None:
        scenarios = self.filter_scenarios()
        for name, params in scenarios.items():
            with self.subTest(name=name):
                filtered_jobs, filtered_skills = self.apply_filters(**params)
                self.assertEqual(kpi_values(filtered_jobs, filtered_skills), expected_kpis(filtered_jobs, filtered_skills))

    def test_filters_match_independent_job_id_sets(self) -> None:
        scenarios = self.filter_scenarios()
        for name, params in scenarios.items():
            with self.subTest(name=name):
                actual_jobs, _ = self.apply_filters(**params)
                expected_ids = self.expected_filter_job_ids(**params)
                self.assertEqual(set(actual_jobs["job_id"].dropna()), expected_ids, f"filter mismatch for {name}")
                self.assertEqual(len(actual_jobs), len(expected_ids), f"matching-record count mismatch for {name}")

    def test_chart_tables_match_independent_calculations(self) -> None:
        scenarios = {
            "no_filters": {},
            "one_job_title": {"job_titles": ["Data Engineer"]},
            "country_and_skill": {"countries": ["United States"], "skills_filter": ["python"]},
            "company_and_work_mode": {"companies": [self.company_options[0]], "remote_statuses": ["Remote"]},
            "several_filters": {
                "job_titles": ["Data Analyst", "Data Engineer"],
                "countries": ["United States", "India"],
                "skills_filter": ["python", "sql"],
                "remote_statuses": ["Remote", "Onsite"],
            },
        }
        for name, params in scenarios.items():
            with self.subTest(name=name):
                jobs, skills = self.apply_filters(**params)
                self.assert_all_chart_tables_match(jobs, skills)

    def test_empty_filter_result_handling(self) -> None:
        jobs, skills = self.apply_filters(job_titles=["not a real job title"])
        self.assertTrue(jobs.empty)
        self.assertTrue(skills.empty)
        self.assertEqual(kpi_values(jobs, skills)["Total postings"], "0")
        self.assert_all_chart_tables_match(jobs, skills)

    def assert_all_chart_tables_match(self, jobs: pd.DataFrame, skills: pd.DataFrame) -> None:
        self.assert_frame_matches(top_counts(jobs, "job_title_short"), expected_top_counts(jobs, "job_title_short"), "job title demand")
        self.assert_frame_matches(top_skills(skills), expected_top_skills(skills), "technical skill demand")
        self.assert_frame_matches(top_counts(jobs, "clean_company_name"), expected_top_counts(jobs, "clean_company_name"), "company activity")
        self.assert_frame_matches(salary_by_dimension(jobs, "job_title_short"), expected_salary_by_dimension(jobs, "job_title_short"), "salary by job title")
        self.assert_frame_matches(salary_by_dimension(jobs, "job_country"), expected_salary_by_dimension(jobs, "job_country"), "salary by country")
        self.assert_frame_matches(remote_salary(jobs), expected_remote_salary(jobs), "remote salary")
        self.assert_frame_matches(monthly_trends(jobs), expected_monthly_trends(jobs), "monthly trends")
        self.assert_frame_matches(high_salary_skills(jobs, skills), expected_high_salary_skills(jobs, skills), "high salary skills")
        data_engineer_jobs = jobs[jobs["job_title_short"].eq("Data Engineer")]
        data_engineer_skills = skills_for_jobs(skills, data_engineer_jobs)
        self.assert_frame_matches(top_skills(data_engineer_skills), expected_top_skills(data_engineer_skills), "data engineer skill demand")

    def expected_filter_job_ids(
        self,
        *,
        job_titles: list[str] | None = None,
        countries: list[str] | None = None,
        companies: list[str] | None = None,
        skills_filter: list[str] | None = None,
        remote_statuses: list[str] | None = None,
        salary_range: tuple[float, float] | None = None,
        date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
    ) -> set[int]:
        expected = set(self.jobs["job_id"].dropna())
        if job_titles:
            expected &= set(self.jobs.loc[self.jobs["job_title_short"].isin(job_titles), "job_id"].dropna())
        if countries:
            expected &= set(self.jobs.loc[self.jobs["job_country"].isin(countries), "job_id"].dropna())
        if companies:
            expected &= set(self.jobs.loc[self.jobs["clean_company_name"].isin(companies), "job_id"].dropna())
        if remote_statuses:
            expected &= set(self.jobs.loc[self.jobs["remote_status"].isin(remote_statuses), "job_id"].dropna())
        if salary_range is not None:
            low, high = salary_range
            salary = self.jobs["salary_year_avg"]
            expected &= set(self.jobs.loc[salary.isna() | salary.between(low, high), "job_id"].dropna())
        if date_range is not None:
            start, end = date_range
            mask = self.jobs["job_posted_date"].between(pd.Timestamp(start), pd.Timestamp(end))
            expected &= set(self.jobs.loc[mask, "job_id"].dropna())
        if skills_filter:
            expected &= set(self.skills.loc[self.skills["clean_skill_name"].isin(skills_filter), "job_id"].dropna())
        return expected

    def filter_scenarios(self) -> dict[str, dict[str, object]]:
        salary_values = self.jobs["salary_year_avg"].dropna()
        salary_mid = float(salary_values.median())
        date_start = pd.Timestamp("2024-01-01")
        date_end = pd.Timestamp("2024-02-01")
        few_record_company = self.jobs["clean_company_name"].value_counts().loc[lambda s: s <= 2].index[0]
        return {
            "no_active_filters": {},
            "one_job_title": {"job_titles": ["Data Engineer"]},
            "multiple_job_titles": {"job_titles": ["Data Analyst", "Data Scientist"]},
            "one_country": {"countries": ["United States"]},
            "one_skill": {"skills_filter": ["python"]},
            "multiple_skills": {"skills_filter": ["python", "sql"]},
            "one_company": {"companies": [self.company_options[0]]},
            "multiple_companies": {"companies": self.company_options[:2]},
            "remote_only": {"remote_statuses": ["Remote"]},
            "onsite_only": {"remote_statuses": ["Onsite"]},
            "combined_work_modes": {"remote_statuses": ["Remote", "Onsite"]},
            "narrow_salary_range": {"salary_range": (salary_mid, salary_mid + 10_000)},
            "narrow_date_range": {"date_range": (date_start, date_end)},
            "job_title_plus_country": {"job_titles": ["Data Engineer"], "countries": ["United States"]},
            "skill_plus_work_mode": {"skills_filter": ["python"], "remote_statuses": ["Remote"]},
            "several_filters": {
                "job_titles": ["Data Analyst", "Data Engineer"],
                "countries": ["United States", "India"],
                "skills_filter": ["python", "sql"],
                "remote_statuses": ["Remote", "Onsite"],
                "salary_range": (salary_mid, salary_mid + 25_000),
                "date_range": (pd.Timestamp("2024-01-01"), pd.Timestamp("2025-01-01")),
            },
            "very_few_records": {"companies": [few_record_company]},
            "zero_records": {"job_titles": ["not a real job title"]},
            "reset_filters": {},
        }


if __name__ == "__main__":
    unittest.main()
