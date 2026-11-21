from __future__ import annotations

import streamlit as st

from dashboard.weather_demo import SAMPLE_NOTICE, sample_daily_mart, filter_sample, temperature_chart, precipitation_chart

st.markdown('''<section class="wx-section-head"><p class="pa-eyebrow">WEATHER / INTERACTIVE DEMO</p><h1>Explore the daily mart.</h1><p>Temperature ranges, rainy city-days and coverage, with the same city/day grain as the weather project.</p></section>''', unsafe_allow_html=True)
st.warning(SAMPLE_NOTICE)
st.caption("All values below are synthetic, fixed examples, not historical weather, current forecasts or measured pipeline output. Dates are an arbitrary demonstration window in Cairo-local calendar time.")
st.page_link("views/weather_pipeline.py", label="Back to the pipeline case study", icon="↩️")
data = sample_daily_mart()
with st.container(border=True):
    cities = st.multiselect("Cities", ["Cairo", "Alexandria"], default=["Cairo", "Alexandria"])
    dates = st.date_input("Cairo-local date range (sample)", value=(data['day'].min(), data['day'].max()), min_value=data['day'].min(), max_value=data['day'].max(), format="DD/MM/YYYY")
    full_days = st.checkbox("Only 24-hour sample city-days", value=False)
    st.caption("Boundary city-days deliberately have 22 or 2 hours to demonstrate partial coverage. This filter keeps exactly 24 hours; it is not a general rule for DST days.")
if not isinstance(dates, (list,tuple)) or len(dates) != 2:
    st.info("Choose both a start and end date.")
    st.stop()
filtered = filter_sample(data, cities, dates[0], dates[1], full_days)
if filtered.empty:
    st.info("No sample city-days match these filters. Select a city or widen the date range.")
    st.stop()
mean = filtered['avg_temp'].mean()
rainy = int(filtered['total_precipitation'].gt(0).sum())
partial = int(filtered['hours_count'].ne(24).sum())
st.markdown(f'''<div class="wx-metrics"><div><span>SAMPLE CITY-DAYS</span><strong>{len(filtered)}</strong><p>City × local calendar day</p></div><div><span>MEAN DAILY AVG</span><strong>{mean:.1f} °C</strong><p>Unweighted across selection</p></div><div><span>RAINY CITY-DAYS</span><strong>{rainy}</strong><p>Precipitation greater than 0 mm</p></div><div><span>PARTIAL CITY-DAYS</span><strong>{partial}</strong><p>Not 24 hours in this sample</p></div></div>''', unsafe_allow_html=True)
st.subheader("Sample temperature trend")
st.caption("Line = daily average. Shaded band = daily minimum to maximum. Hover to inspect min/max and hours_count. Partial-day averages do not have the same coverage as full days.")
st.plotly_chart(temperature_chart(filtered), use_container_width=True, config={"displayModeBar":False})
st.subheader("Sample precipitation by day")
st.caption("Daily totals in millimeters. These are invented demonstration values, not observed rainfall. Rainy city-days count each city separately.")
st.plotly_chart(precipitation_chart(filtered), use_container_width=True, config={"displayModeBar":False})
with st.expander("Inspect sample daily-mart rows and download CSV"):
    st.caption("Synthetic fields follow the repository mart column names. A future real export should carry its source, extraction time and forecast run date; replacing this sample is not a live database connection.")
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    st.download_button("Download filtered SAMPLE CSV", data=filtered.to_csv(index=False), file_name="weather_SAMPLE_daily_mart.csv", mime="text/csv")
st.markdown('<div class="wx-evidence-note"><strong>Demo only.</strong> The real project implements ingestion, models and orchestration. This portfolio dashboard is a separate sample-data interface. It does not query Open-Meteo, PostgreSQL, Airflow or AWS.</div>',unsafe_allow_html=True)
