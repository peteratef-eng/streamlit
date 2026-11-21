from __future__ import annotations


def apply_chart_theme(fig, theme: dict[str, str]):
    fig.update_layout(
        template="plotly_dark" if theme["mode"] == "dark" else "plotly_white",
        paper_bgcolor=theme["chart_bg"],
        plot_bgcolor=theme["chart_bg"],
        font=dict(family="Inter, Segoe UI, Arial", size=13, color=theme["secondary_text"]),
        title=dict(text=""),
        margin=dict(l=90, r=80, t=14, b=58),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["secondary_text"]),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(
            bgcolor=theme["surface_elevated"],
            bordercolor=theme["border"],
            font=dict(color=theme["primary_text"], family="Inter, Segoe UI, Arial"),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=theme["chart_grid"],
        zeroline=False,
        linecolor=theme["border"],
        tickfont=dict(color=theme["secondary_text"]),
        title_font=dict(color=theme["muted_text"], size=13),
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor=theme["border"],
        tickfont=dict(color=theme["secondary_text"]),
        title_font=dict(color=theme["muted_text"], size=13),
    )
    return fig
