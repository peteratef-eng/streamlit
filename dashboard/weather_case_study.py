from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go

from ui.theme import current_theme

# Code/README-derived constants from weather-forecast-data-platform at 32c2b1f.
CITIES = ("Cairo", "Alexandria")
FORECAST_DAYS = 14
HOURLY_VARIABLES = 5
RETRIES = 2
RETRY_DELAY_MINUTES = 5


def configured_scope() -> pd.DataFrame:
    """Expected hourly records per city, not observed ingestion output."""
    return pd.DataFrame({"city": CITIES, "expected_rows": [FORECAST_DAYS * 24] * len(CITIES)})


def local_day_completeness() -> pd.DataFrame:
    """Deterministic timestamp-only example; no weather measurements are generated.

    A fixed UTC start makes this reproducible and illustrates the staging model's
    Africa/Cairo conversion and the daily mart's hours_count aggregation.
    """
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    counts: dict[str, int] = {}
    for hour in range(FORECAST_DAYS * 24):
        day = (start + timedelta(hours=hour)).astimezone(ZoneInfo("Africa/Cairo")).date().isoformat()
        counts[day] = counts.get(day, 0) + 1
    return pd.DataFrame({"local_day": list(counts), "hours_count": list(counts.values())})


def chart_style(figure: go.Figure, *, height: int = 285) -> go.Figure:
    theme = current_theme()
    figure.update_layout(
        template="plotly_dark",
        hoverlabel={"bgcolor": theme["surface"], "font_color": theme["primary_text"]},
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Source Sans Pro, Arial, sans-serif", "size": 13, "color": theme["secondary_text"]},
        margin={"l": 12, "r": 14, "t": 22, "b": 16},
        showlegend=False,
        dragmode=False,
    )
    figure.update_xaxes(showgrid=False, zeroline=False, fixedrange=True)
    figure.update_yaxes(gridcolor=theme["chart_grid"], zeroline=False, fixedrange=True)
    return figure


def scope_chart() -> go.Figure:
    scope = configured_scope()
    figure = go.Figure(go.Bar(
        x=scope["expected_rows"], y=scope["city"], orientation="h",
        marker_color=["#78E1CD", "#82B5F5"], text=scope["expected_rows"],
        textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x} expected hourly rows<extra></extra>",
    ))
    figure.update_xaxes(title="Expected hourly rows", range=[0, 400])
    return chart_style(figure, height=230)


def completeness_chart() -> go.Figure:
    sample = local_day_completeness()
    colors = ["#78E1CD" if count != 24 else "#82B5F5" for count in sample["hours_count"]]
    figure = go.Figure(go.Bar(
        x=list(range(1, len(sample) + 1)), y=sample["hours_count"], marker_color=colors,
        customdata=sample["local_day"],
        hovertemplate="%{customdata}: %{y} hours<extra></extra>",
    ))
    figure.add_hline(y=24, line_dash="dot", line_color="#93A8C4")
    figure.update_xaxes(title="Local day (Cairo)", dtick=2)
    figure.update_yaxes(title="Hourly timestamps", range=[0, 27], dtick=6)
    return chart_style(figure)
