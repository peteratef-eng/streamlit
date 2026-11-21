from __future__ import annotations



DESIGN_SYSTEM = {
    "mode": "dark",
    "background": "#0F172A",
    "sidebar": "#111C30",
    "surface": "#142036",
    "surface_secondary": "#18283E",
    "surface_elevated": "#142036",
    "primary_text": "#E2E8F0",
    "secondary_text": "#B2C2D8",
    "muted_text": "#93A8C4",
    "border": "#2B405B",
    "accent": "#78E1CD",
    "accent_hover": "#A2F0DF",
    "bright_accent": "#82B5F5",
    "input_bg": "#142036",
    "input_text": "#E2E8F0",
    "on_accent": "#0F172A",
    "tag_bg": "#193B42",
    "tag_text": "#9EE9DC",
    "chart_bg": "rgba(255,255,255,0)",
    "chart_grid": "#293D55",
    "positive": "#6DD6B4",
    "warning": "#F4C775",
    "negative": "#FFA3A3",
    "shadow": "0 12px 28px rgba(0, 0, 0, 0.12)",
    "shadow_accent": "0 10px 24px rgba(120, 225, 205, 0.08)",
    "hover": "#193B42",
    "disabled": "#D4CDC0",
    "palette": ["#78E1CD", "#82B5F5", "#6DD6B4", "#93A8C4", "#A2F0DF", "#AD9FEA"],
}


def current_theme() -> dict[str, str]:
    return DESIGN_SYSTEM
