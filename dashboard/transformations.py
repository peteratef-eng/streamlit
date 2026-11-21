from __future__ import annotations

import pandas as pd


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


def kpi_values(jobs: pd.DataFrame, skills: pd.DataFrame) -> dict[str, str]:
    salary = jobs["salary_year_avg"].dropna()
    remote_pct = (
        (jobs["remote_status"].eq("Remote").sum() / len(jobs) * 100) if len(jobs) else None
    )
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


def salary_coverage(jobs: pd.DataFrame) -> tuple[str, int, int]:
    total_postings = len(jobs)
    salary_records = int(jobs["salary_year_avg"].notna().sum()) if "salary_year_avg" in jobs else 0
    coverage = f"{salary_records / total_postings * 100:.1f}%" if total_postings else "N/A"
    return coverage, salary_records, total_postings


def top_counts(df: pd.DataFrame, column: str, limit: int = 15) -> pd.DataFrame:
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


def top_skills(skills: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
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


def salary_by_dimension(jobs: pd.DataFrame, column: str, limit: int = 15) -> pd.DataFrame:
    salary_jobs = jobs.dropna(subset=["salary_year_avg"])
    if salary_jobs.empty:
        return pd.DataFrame(columns=[column, "avg_salary", "median_salary", "salary_jobs"])
    grouped = (
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
    return grouped


def monthly_trends(jobs: pd.DataFrame) -> pd.DataFrame:
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


def remote_salary(jobs: pd.DataFrame) -> pd.DataFrame:
    salary_jobs = jobs.dropna(subset=["salary_year_avg"])
    if salary_jobs.empty:
        return pd.DataFrame(columns=["remote_status", "avg_salary", "salary_jobs"])
    return (
        salary_jobs.groupby("remote_status", dropna=False)
        .agg(avg_salary=("salary_year_avg", "mean"), salary_jobs=("job_id", "nunique"))
        .reset_index()
    )


def high_salary_skills(jobs: pd.DataFrame, skills: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
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
