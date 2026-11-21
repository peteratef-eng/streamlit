"""Synthetic daily-mart demonstration. Never used as pipeline output."""
from __future__ import annotations

from datetime import date, timedelta
import math

import pandas as pd
import plotly.graph_objects as go

from dashboard.weather_case_study import chart_style

SAMPLE_NOTICE = "Sample data for demonstration. Live pipeline output is not published."
CITY_COLORS = {"Cairo": "#B45309", "Alexandria": "#1E3A5F"}


def sample_daily_mart() -> pd.DataFrame:
    """Fixed synthetic values shaped like mart_weather_daily, not API forecasts.

    Jan 1-15, 2026 is an arbitrary demonstration window. Deterministic waves
    illustrate filters and charts, not climate, accuracy, or real conditions.
    """
    rows = []
    for city_index, city in enumerate(CITY_COLORS):
        for day_index in range(15):
            avg = round(17 - city_index * 2 + 2 * math.sin(day_index * .6 + city_index), 2)
            rain = round((1.2 + city_index * 1.7) if day_index in (3, 7, 8, 12) else 0, 2)
            humidity = round(55 + city_index * 12 + 8 * math.sin(day_index * .4), 2)
            wind = round(13 + city_index * 4 + 3 * math.cos(day_index * .5), 2)
            rows.append({
                "city": city, "day": date(2026, 1, 1) + timedelta(days=day_index),
                "hours_count": 22 if day_index == 0 else 2 if day_index == 14 else 24,
                "avg_temp": avg, "min_temp": round(avg - 4, 2), "max_temp": round(avg + 5, 2),
                "total_precipitation": rain,
                "avg_humidity": humidity, "min_humidity": round(humidity - 10, 2), "max_humidity": round(humidity + 10, 2),
                "avg_wind_speed": wind, "min_wind_speed": round(wind - 4, 2), "max_wind_speed": round(wind + 5, 2),
                "avg_cloud_cover": round(30 + 20 * (1 + math.sin(day_index * .5 + city_index)), 2),
            })
    return pd.DataFrame(rows)


def filter_sample(data: pd.DataFrame, cities: list[str], start: date, end: date, full_days: bool = False) -> pd.DataFrame:
    mask = data['city'].isin(cities) & data['day'].between(start, end)
    if full_days:
        mask &= data['hours_count'].eq(24)
    return data.loc[mask].copy()


def temperature_chart(data: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    for city, color in CITY_COLORS.items():
        subset = data.loc[data['city'].eq(city)]
        if subset.empty:
            continue
        figure.add_trace(go.Scatter(x=subset['day'], y=subset['min_temp'], mode='lines', line={'width':0}, legendgroup=city, showlegend=False, hoverinfo='skip'))
        figure.add_trace(go.Scatter(x=subset['day'], y=subset['max_temp'], mode='lines', line={'width':0}, fill='tonexty', fillcolor='rgba(180,83,9,0.10)' if city=='Cairo' else 'rgba(30,58,95,0.10)', legendgroup=city, showlegend=False, hoverinfo='skip'))
        figure.add_trace(go.Scatter(x=subset['day'], y=subset['avg_temp'], mode='lines+markers', name=city, line={'color':color,'width':3}, marker={'size':5}, legendgroup=city, customdata=subset[['min_temp','max_temp','hours_count']].values, hovertemplate=city+' · %{x}<br>Avg %{y:.1f} °C<br>Min %{customdata[0]:.1f} / max %{customdata[1]:.1f} °C<br>Coverage %{customdata[2]} hours<extra>Sample</extra>'))
    chart_style(figure, height=340)
    figure.update_layout(showlegend=True, legend={'orientation':'h','y':1.16,'x':0}, hovermode='x unified')
    figure.update_yaxes(title='Temperature (°C)')
    figure.update_xaxes(tickformat='%d %b', nticks=5)
    return figure


def precipitation_chart(data: pd.DataFrame) -> go.Figure:
    figure=go.Figure()
    for city, color in CITY_COLORS.items():
        subset=data.loc[data['city'].eq(city)]
        if not subset.empty:
            figure.add_trace(go.Bar(x=subset['day'],y=subset['total_precipitation'], name=city, marker_color=color, hovertemplate=city+' · %{x}<br>%{y:.1f} mm<extra>Sample</extra>'))
    chart_style(figure, height=300)
    figure.update_layout(barmode='group', showlegend=True, legend={'orientation':'h','y':1.16,'x':0})
    figure.update_yaxes(title='Precipitation (mm)',rangemode='tozero')
    figure.update_xaxes(tickformat='%d %b',nticks=5)
    return figure
