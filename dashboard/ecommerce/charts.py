from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ui.chart_theme import apply_chart_theme


def _style(fig, theme: dict[str, str]):
    fig.update_layout(
        legend_title_text="",
        modebar_remove=[
            "zoom",
            "pan",
            "select",
            "lasso2d",
            "zoomIn",
            "zoomOut",
            "autoScale",
            "resetScale",
        ],
    )
    return apply_chart_theme(fig, theme)


def bar(df: pd.DataFrame, x: str, y: str, label: str, theme: dict[str, str], *, value_prefix: str = ""):
    plot_df = df.sort_values(y, ascending=True)
    fig = px.bar(
        plot_df,
        x=y,
        y=x,
        orientation="h",
        labels={x: "", y: label},
        color_discrete_sequence=theme["palette"],
        text=y,
        height=min(560, max(380, 90 + len(plot_df) * 40)),
    )
    text_template = f"{value_prefix}%{{text:,.0f}}"
    fig.update_traces(
        texttemplate=text_template,
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=f"<b>%{{y}}</b><br>{label}: {value_prefix}%{{x:,.0f}}<extra></extra>",
    )
    fig = _style(fig, theme)
    fig.update_xaxes(tickprefix=value_prefix)
    fig.update_layout(margin=dict(l=220, r=110, t=14, b=58))
    return fig


def monthly_net_sales_trend(df: pd.DataFrame, theme: dict[str, str]):
    complete = df[~df["is_partial"]]
    partial = df[df["is_partial"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["period"],
            y=df["TotalPrice"],
            mode="lines",
            line=dict(color=theme["accent"], width=3),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=complete["period"],
            y=complete["TotalPrice"],
            mode="markers",
            name="Complete month",
            marker=dict(color=theme["accent"], size=9),
            hovertemplate="%{x|%b %Y}<br>Net sales: £%{y:,.0f}<extra></extra>",
        )
    )
    if not partial.empty:
        fig.add_trace(
            go.Scatter(
                x=partial["period"],
                y=partial["TotalPrice"],
                mode="markers",
                name="Partial month (data ends Dec 9)",
                marker=dict(color=theme["muted_text"], size=11, symbol="diamond-open", line=dict(width=2)),
                hovertemplate="%{x|%b %Y}<br>Net sales: £%{y:,.0f} (partial month)<extra></extra>",
            )
        )
    fig = _style(fig, theme)
    fig.update_layout(height=460, margin=dict(l=90, r=45, t=14, b=68))
    fig.update_yaxes(tickprefix="£")
    return fig
