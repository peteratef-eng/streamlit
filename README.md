# Job Market Data Engineering Project

## Project Overview

This project analyzes job market data for data-related roles using SQL and a layered data engineering workflow.

The goal is to transform raw job posting data into clean, reliable, and business-ready analytics models that can be used to answer questions about job demand, skills, remote work trends, salary trends, and company hiring activity.

This project is structured like a real data engineering workflow, starting from raw tables, then building staging models, intermediate models, analytics marts, quality checks, and final business insights.

---

## Dataset

The project uses a job market dataset containing:

* 1.6M+ job postings
* 215K+ companies
* 700K+ job-skill relationships

The dataset includes job titles, salaries, locations, companies, skills, and remote work information.

---

## Business Questions

This project answers questions such as:

* What are the most demanded skills for Data Engineer roles?
* Which companies have the highest hiring activity?
* How is the job market changing month over month?
* Are remote Data Engineer roles increasing or decreasing over time?
* How do salaries change across roles and remote statuses?
* Which companies have the highest share of remote job postings?

---

## Project Structure

```text
job_market_dbt/
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── tests/
├── macros/
├── analyses/
├── snapshots/
└── dbt_project.yml
```

---

## Data Flow

Raw CSV Files
↓
PostgreSQL Raw Tables
↓
dbt Staging Models
↓
dbt Intermediate Models
↓
dbt Analytics Marts
↓
Business Insights

---
### Folder Description

* `staging/`: Cleans and standardizes raw source tables.
* `intermediate/`: Joins cleaned staging models into reusable enriched datasets.
* `marts/`: Contains business-ready analytics models.
* `quality_checks/`: Validates row counts, nulls, duplicates, orphan keys, and calculation logic.
* `insights/`: Stores SQL queries used to generate README insights.

---

## SQL Architecture

The SQL workflow is organized into three main layers:

### 1. Staging Layer

The staging layer cleans and standardizes raw source tables while preserving the original row-level structure.

Models:

* `stg_job_postings`
* `stg_companies`
* `stg_skills`
* `stg_job_skills`

Examples of transformations in this layer:

* Standardizing text values using `LOWER()` and `TRIM()`
* Handling null and blank values using `COALESCE()` and `NULLIF()`
* Creating cleaned fields such as `clean_job_title`, `clean_job_location`, and `clean_company_name`
* Creating business-friendly classifications such as `remote_status` and `salary_category`
* Creating `posted_month` using `DATE_TRUNC()`

---

### 2. Intermediate Layer

The intermediate layer joins cleaned staging models and prepares reusable enriched datasets.

Models:

* `int_job_postings_enriched`
* `int_job_skills_enriched`

Examples:

* `int_job_postings_enriched` combines job postings with cleaned company names.
* `int_job_skills_enriched` combines job-skill relationships with cleaned skill names and skill types.

These models reduce repeated joins and create reliable building blocks for analytics marts.

---

### 3. Mart Layer

The mart layer contains business-ready analytics models used to generate insights.

Models:

* `mart_skill_demand_by_role`
* `mart_remote_work_trends`
* `mart_salary_trends`
* `mart_company_leaderboard`
* `mart_monthly_job_trends`

Each mart is designed around a specific business question.

---

## Analytics Marts

### `mart_skill_demand_by_role`

Analyzes the most demanded skills for each job role.

Main metrics:

* `job_title_short`
* `clean_skill_name`
* `clean_skill_type`
* `demand_count`

---

### `mart_remote_work_trends`

Analyzes remote, onsite, and unknown job status trends by month and role.

Main metrics:

* `posted_month`
* `job_title_short`
* `remote_status`
* `total_jobs`
* `monthly_role_total`
* `remote_status_percentage`

---

### `mart_salary_trends`

Analyzes salary trends by month, role, and remote status.

Main metrics:

* `posted_month`
* `job_title_short`
* `remote_status`
* `total_salary_jobs`
* `avg_salary`
* `min_salary`
* `max_salary`
* `previous_month_avg_salary`
* `salary_difference`
* `salary_growth_percentage`

---

### `mart_company_leaderboard`

Ranks companies by hiring activity and remote job share.

Main metrics:

* `company_id`
* `clean_company_name`
* `total_jobs`
* `remote_jobs`
* `onsite_jobs`
* `known_salary_jobs`
* `avg_salary`
* `remote_percentage`

---

### `mart_monthly_job_trends`

Analyzes month-over-month job market changes.

Main metrics:

* `posted_month`
* `total_jobs`
* `previous_month_jobs`
* `job_difference`
* `job_growth_percentage`

---

## Data Quality Checks

Quality checks were created to validate the reliability of the SQL models.

The checks include:

* Row count comparisons between staging, intermediate, and mart models
* Missing values in key columns
* Duplicate job IDs
* Duplicate job-skill relationships
* Orphan keys between job postings, companies, and skills
* Null checks after joins
* Percentage calculation checks
* Month-over-month growth calculation checks
* Grain validation, such as one row per month in monthly trend marts

Examples of data quality checks:

* Ensuring staging row counts match raw source row counts
* Ensuring `job_id` does not contain duplicates
* Ensuring every `skill_id` in the job-skill bridge exists in the skills table
* Ensuring every `job_id` in the job-skill bridge exists in the job postings table
* Ensuring mart percentage calculations are logically valid

---

## Key Insights

### 1. Data Engineer Skills Demand

SQL and Python are the most demanded skills for Data Engineer roles, appearing in 233,132 and 224,102 job postings respectively.

Cloud platforms such as AWS and Azure are also highly demanded, followed by big data tools including Spark, Databricks, Snowflake, Scala, and Kafka.

This suggests that Data Engineer roles require a strong combination of SQL, Python, cloud platforms, and distributed data processing tools.

Top Data Engineer skills:

```text
1. SQL         233,132 job postings
2. Python      224,102 job postings
3. AWS         130,205 job postings
4. Azure       128,822 job postings
5. Spark       106,904 job postings
6. Java         69,657 job postings
7. Databricks   63,012 job postings
8. Snowflake    60,379 job postings
9. Scala        57,079 job postings
10. Kafka       56,410 job postings
```

---

### 2. Top Hiring Companies

The company leaderboard shows that `bebee careers` has the highest number of job postings with 32,224 listings, followed by `emprego`, `dice`, `capital one`, `amazon`, and `listopro`.

However, some of the top entities appear to be job boards or aggregators rather than direct hiring companies. This is an important dataset limitation when interpreting company-level hiring activity.

Examples:

```text
bebee careers       32,224 job postings
emprego              6,669 job postings
dice                 6,568 job postings
capital one          6,332 job postings
amazon               6,204 job postings
listopro             5,109 job postings
```

Some platforms also show a high remote job percentage, such as:

```text
upwork      90.62% remote
listopro    87.00% remote
dice        52.83% remote
```

This should be interpreted carefully because some of these entities may represent job boards or platforms rather than direct employers.

---

### 3. Monthly Job Market Growth

The monthly job market showed strong volatility across the dataset period.

Job postings dropped sharply from January to February 2023 by 29.82%, followed by several recovery months such as June 2023 (+18.26%) and August 2023 (+18.00%).

The largest declines appeared around September and October 2024, with job postings falling by more than 36% month over month. December 2024 and January 2025 showed a major rebound, growing by 147.60% and 98.29% respectively.

This suggests that job posting activity may be affected by seasonality, market changes, or source collection patterns.

---

### 4. Remote Work Trend for Data Engineer Roles

Data Engineer postings were mostly onsite across the dataset.

In 2023, remote Data Engineer roles generally represented around 9% to 15% of monthly postings, reaching 15.00% in October 2023.

In 2025, the remote share declined significantly, with remote postings dropping to around 3%–5% of monthly Data Engineer postings.

Examples:

```text
February 2025: 3.39% remote
June 2025:     4.24% remote
```

This indicates that Data Engineer roles in this dataset became more onsite-heavy over time, although this may also reflect changes in data source coverage or job posting classification.

---

## Limitations

* Salary data is missing for a large portion of job postings, so salary analysis only reflects postings with available salary values.
* Some company names appear to represent job boards, platforms, or aggregators rather than direct hiring companies.
* Remote status is derived from job location values and may not fully capture hybrid roles.
* Large month-over-month changes may reflect source collection patterns, seasonality, or changes in data coverage.
* The analysis is based on the available dataset and may not represent the entire global job market.

---

## Tools Used

* SQL
* PostgreSQL
* dbt
* DuckDB / MotherDuck
* Python
* VS Code
* Git & GitHub

---

## Skills Demonstrated

This project demonstrates:

* SQL data cleaning
* Data quality validation
* CTEs
* Window functions
* Aggregations
* Joins
* Staging models
* Intermediate models
* Analytics marts
* Data modeling
* dbt model development
* dbt testing
* Data lineage
* Data documentation
* Business insight generation
* Git-based project organization

---

## dbt Implementation

The project was migrated into dbt and organized using a layered architecture:

* Staging Layer
* Intermediate Layer
* Mart Layer

dbt was used for:

* Model dependency management using ref()
* Data quality testing
* Documentation generation
* Data lineage visualization

Implemented Tests:

* not_null
* unique

Results:

* 11 dbt models built successfully
* 11/11 tests passed

All models and tests executed successfully.

---

## Project Screenshots

### dbt Lineage Graph

![dbt Lineage](images/dbt_lineage.png)

### dbt Run Results

![dbt Run](images/dbt_run.png)

### dbt Test Results

![dbt Test](images/dbt_test.png)

The lineage graph and test results demonstrate successful model execution, dependency management, and data quality validation using dbt.

---

## Next Steps

Future improvements include:

* Building a Python ETL pipeline
* Extracting data from public APIs
* Loading raw data into PostgreSQL
* Building incremental dbt models
* Scheduling workflows with Airflow
* Containerizing the pipeline using Docker
* Creating Power BI dashboards
* Deploying the pipeline to a cloud environment

---

## Resume Highlights

* Built a layered SQL analytics project using PostgreSQL and dbt.
* Developed staging, intermediate, and mart models following modern data engineering practices.
* Implemented data quality checks and dbt tests for data validation.
* Generated business insights from 1.6M+ job postings and 7.1M+ job-skill relationships
* Created project documentation, lineage visualization, and analytics marts using dbt.

---

## Live Demo

Hosted dashboard URL: `https://app-6py432aqcozmvm4vm477rp.streamlit.app/`

The portfolio is hosted on Streamlit Community Cloud. The optional Fly.io configuration below is a deployment template, not the live hosting setup.

---

## Streamlit Dashboard

This repository now includes a recruiter-friendly Streamlit application with portfolio pages and project case studies:

The portfolio uses anonymous Google Analytics 4 usage analytics to understand page visits and safe aggregate interactions. It does not send filter selections, search values, salary selections, company selections, email addresses, or form content.

* `app.py`: app entry point, shared layout, analytics, and navigation.
* `views/`: portfolio pages and project views, including the Weather pipeline case study.
* `views/market_dashboard.py`: interactive dashboard with KPI cards, filters, Plotly charts, and plain-English chart explanations.

Dashboard features include:

* Total postings, companies, countries, skills, average salary, median salary, remote share, and salary coverage.
* Filters for job title, country, skill, company, remote status, salary range, and posted date range.
* Charts for job-title demand, skill demand, top hiring companies, salary by title, salary by country, remote versus on-site salary, monthly posting trends, monthly growth, high-salary skills, and Data Engineer skill demand.
* Graceful handling for missing data files, missing salaries, null values, empty filter results, and data-loading errors.

---

## Dashboard Screenshots

Add screenshots after deployment or local review:

* `images/dashboard_overview.png`: first viewport of the Project Overview page.
* `images/dashboard_filters_kpis.png`: sidebar filters with KPI cards.
* `images/dashboard_skill_salary_trends.png`: skill demand, salary, and monthly trend charts.
* `images/dashboard_mobile.png`: narrow-screen layout.

---

## Local Installation

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the `python` launcher is not available on Windows, use the existing virtual environment interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Environment Variables

Copy `.env.example` to `.env` for local development:

```powershell
Copy-Item .env.example .env
```

Variables:

* `DATABASE_URL`: optional PostgreSQL connection string for the broader data engineering project.
* `DASHBOARD_DATA_DIR`: dashboard dataset folder. Defaults to `data/dashboard`.
* `STREAMLIT_SERVER_PORT`: local Streamlit port. Defaults to `8501`.

Do not commit `.env` or real credentials.

---

## Hosted Demo Dataset

The full raw CSV dataset is too large for many free hosting environments, so the dashboard uses an optimized deployment dataset generated from the real source CSVs.

Generate or refresh it with:

```powershell
.\.venv\Scripts\python.exe scripts\prepare_dashboard_data.py --sample-size 150000
```

This creates:

* `data/dashboard/jobs_sample.csv`
* `data/dashboard/job_skills_sample.csv`
* `data/dashboard/metadata.json`

The current generated dataset contains 150,000 sampled job postings and 667,829 matching job-skill relationships from 1,615,930 source job postings. The script uses a reproducible random sample and joins the sampled postings to matching company and skill data.

---

## Run the Dashboard

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Then open:

```text
http://localhost:8501
```

---

## Application Architecture

```text
app.py
views/
  home.py
  weather_pipeline.py
  project_overview.py
  market_dashboard.py
  data_pipeline.py
ui/
  navigation.py
portfolio/content/
  projects.py
dashboard/
  data_loader.py
  transformations.py
  charts.py
  components.py
scripts/
  prepare_dashboard_data.py
.streamlit/
  config.toml
data/dashboard/
  jobs_sample.csv
  job_skills_sample.csv
  metadata.json
```

The Streamlit app is intentionally separate from the existing dbt and SQL workflow. It reads optimized dashboard CSVs, caches data loading, applies filters in Pandas, and renders interactive Plotly charts.

---

## Docker

Build the image:

```powershell
docker build -t job-market-dashboard .
```

Run the container:

```powershell
docker run --rm -p 8501:8501 --env DASHBOARD_DATA_DIR=data/dashboard job-market-dashboard
```

Open:

```text
http://localhost:8501
```

---

## Fly.io Deployment

`fly.toml` is configured with a placeholder app name:

```text
job-market-data-engineering-dashboard
```

Replace it with a globally unique Fly.io app name before deployment.

Suggested deployment flow:

```powershell
fly auth login
fly apps create YOUR_UNIQUE_APP_NAME
```

Update `fly.toml`:

```toml
app = "YOUR_UNIQUE_APP_NAME"
```

Deploy:

```powershell
fly deploy
```

Check status:

```powershell
fly status
fly open
```

Required placeholder to replace:

* `fly.toml` `app`: use your own globally unique Fly.io app name.
* README Live Demo URL: replace after deployment.

---

## Current Dashboard Limitations

* Hosted charts use the optimized sample dataset, not every raw row.
* Salary metrics only include postings with non-null yearly salary values.
* Company rankings may include job boards or aggregators.
* Remote status is inferred from source fields and may not fully capture hybrid roles.
* Docker build and Fly.io deployment require Docker/Fly CLI availability on the local machine.

---

## Portfolio Hub

The Streamlit project now works as a personal Data Engineering portfolio with the Job Market Intelligence project as the first featured case study.

Navigation groups:

* Portfolio: Home, About Me, Experience, Skills, Projects, Contact
* Featured Projects: Job Market Intelligence, Market Dashboard, Data Pipeline, Data Quality

Editable portfolio content is centralized in:

```text
portfolio/content/profile.py
portfolio/content/experience.py
portfolio/content/skills.py
portfolio/content/projects.py
```

Resume asset:

```text
assets/resume/Peter Resume 2026.pdf
```

## Add a Future Project

To add another project without redesigning the portfolio:

1. Add a new dictionary entry in `portfolio/content/projects.py`.
2. Fill in `slug`, `title`, descriptions, category, year, status, technologies, key metric, links, and case-study sections.
3. Add optional images under an assets folder if needed.
4. Link to a separate deployment through `demo_url` when the project runs outside this repository.
5. Create a dedicated view only when the project needs a custom case study beyond the shared fields.

The portfolio hub can link to independent deployments, so future projects can use different repositories, hosting targets, or technology stacks.
