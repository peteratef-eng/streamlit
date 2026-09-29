from __future__ import annotations

import re

import streamlit as st


_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
_WHITESPACE_RE = re.compile(r"\s+")
_PUNCTUATION_RE = re.compile(r"\s*([{};,>])\s*")


def _minify_css(css: str) -> str:
    css = _COMMENT_RE.sub("", css)
    css = _WHITESPACE_RE.sub(" ", css)
    return _PUNCTUATION_RE.sub(r"\1", css).strip()


@st.cache_resource(show_spinner=False)
def _global_styles_html(theme_items: tuple[tuple[str, str], ...]) -> str:
    return _build_global_styles(dict(theme_items))


def inject_global_styles(theme: dict[str, str]) -> None:
    st.markdown(_global_styles_html(tuple(sorted(theme.items()))), unsafe_allow_html=True)


def _build_global_styles(theme: dict[str, str]) -> str:
    css = (
        f"""
        <style>
        :root {{
            color-scheme: {theme["mode"]};
            --bg: {theme["background"]};
            --sidebar: {theme["sidebar"]};
            --surface: {theme["surface"]};
            --surface-2: {theme["surface_secondary"]};
            --surface-elevated: {theme["surface_elevated"]};
            --text: {theme["primary_text"]};
            --text-2: {theme["secondary_text"]};
            --muted: {theme["muted_text"]};
            --border: {theme["border"]};
            --accent: {theme["accent"]};
            --accent-hover: {theme["accent_hover"]};
            --accent-bright: {theme["bright_accent"]};
            --input-bg: {theme["input_bg"]};
            --input-text: {theme["input_text"]};
            --on-accent: {theme["on_accent"]};
            --tag-bg: {theme["tag_bg"]};
            --tag-text: {theme["tag_text"]};
            --positive: {theme["positive"]};
            --warning: {theme["warning"]};
            --negative: {theme["negative"]};
            --shadow: {theme["shadow"]};
            --shadow-accent: {theme["shadow_accent"]};
            --hover: {theme["hover"]};
            --disabled: {theme["disabled"]};
            --color-navy: #0f172a;
            --color-blue: #b45309;
            --color-blue-dark: #92400e;
            --color-cyan: #1e3a5f;
            --color-green: #10b981;
            --color-background: #f6f8fc;
            --color-surface: #ffffff;
            --color-text-muted: #52637a;
            --color-border: #d8e2ef;
            --color-border-blue: rgba(180, 83, 9, 0.24);
            --font: "Source Sans Pro", "Source Sans 3", "Source Sans", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --data-navy: #0F172A;
            --data-blue: #B45309;
            --data-blue-dark: #92400E;
            --data-cyan: #1E3A5F;
            --data-cyan-soft: rgba(30, 58, 95, 0.12);
            --data-indigo: #4F46E5;
            --data-green: #10B981;
            --data-green-soft: rgba(16, 185, 129, 0.10);
            --data-amber: #F59E0B;
            --data-amber-soft: rgba(245, 158, 11, 0.10);
            --data-red: #B91C1C;
            --data-surface: #FFFFFF;
            --data-background: #F8FAFC;
            --data-background-blue: #EFF6FF;
            --data-border: #CBD5E1;
            --data-border-soft: rgba(148, 163, 184, 0.28);
            --data-text: #0F172A;
            --data-text-secondary: #64748B;
        }}

        html, body, .stApp {{
            background: var(--bg);
            color: var(--text);
        }}
        .stApp, .block-container, [data-testid="stSidebar"], [data-testid="stSidebar"] * {{
            box-sizing: border-box;
        }}
        .material-icons,
        .material-icons-round,
        .material-icons-rounded,
        .material-symbols-outlined,
        .material-symbols-rounded,
        .material-symbols-sharp,
        [class*="material-icons"],
        [class*="material-symbols"] {{
            font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
            font-weight: normal !important;
            font-style: normal !important;
            font-size: 1.25rem;
            line-height: 1;
            letter-spacing: normal !important;
            text-transform: none !important;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            font-feature-settings: "liga";
            -webkit-font-feature-settings: "liga";
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }}

        header[data-testid="stHeader"] {{
            background: var(--bg);
            color: var(--text);
            border-bottom: 1px solid transparent;
        }}

        .block-container {{
            max-width: 1220px;
            padding: .35rem 1.35rem 2.5rem;
        }}

        h1, h2, h3, h4 {{
            color: var(--text);
            font-family: var(--font);
            letter-spacing: 0;
            line-height: 1.15;
        }}
        h1 {{ font-size: clamp(2rem, 3.8vw, 3.35rem); font-weight: 700; }}
        h2 {{ font-size: clamp(1.65rem, 2.6vw, 2rem); font-weight: 650; margin-top: 1.4rem; }}
        h3 {{ font-size: 1.2rem; font-weight: 650; }}
        p, li {{
            color: var(--text-2);
            font-size: 1rem;
            line-height: 1.65;
            font-family: var(--font);
        }}
        a {{
            color: var(--accent);
            font-weight: 500;
            text-decoration: none;
        }}
        a:hover {{
            color: var(--accent-hover);
            text-decoration: underline;
        }}
        a:focus-visible {{
            outline: 3px solid color-mix(in srgb, var(--accent) 34%, transparent);
            outline-offset: 3px;
            border-radius: 6px;
        }}
        [data-testid="stHeadingWithActionElements"] a,
        h1 a, h2 a, h3 a {{
            opacity: 0;
            transition: opacity 140ms ease;
        }}
        [data-testid="stHeadingWithActionElements"]:hover a,
        [data-testid="stHeadingWithActionElements"]:focus-within a,
        h1:hover a, h2:hover a, h3:hover a {{
            opacity: 1;
        }}

        [data-testid="stSidebar"] {{
            background: var(--sidebar);
            border-right: 1px solid var(--border);
            overflow-x: clip;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding: .85rem .9rem 1.1rem;
            max-width: 100%;
            min-width: 0;
        }}
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {{
            color: var(--text-2);
            font-family: var(--font);
        }}
        [data-testid="stSidebarNav"] a {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
            border-radius: 8px;
            color: var(--text-2);
            font-weight: 500;
            padding: .42rem .55rem;
            margin: .02rem 0;
            transition: background-color 180ms ease, border-color 180ms ease, color 180ms ease;
        }}
        [data-testid="stSidebarNav"] {{
            margin-top: .2rem;
        }}
        [data-testid="stSidebarNav"] ul {{
            gap: .08rem;
        }}
        [data-testid="stSidebarNav"] [role="heading"],
        [data-testid="stSidebarNav"] summary,
        [data-testid="stSidebarNav"] p {{
            color: var(--text);
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .04em;
            text-transform: uppercase;
            margin: .75rem 0 .25rem;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: var(--hover);
            color: var(--text);
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: var(--tag-bg);
            color: var(--tag-text);
            border: 1px solid var(--border);
        }}
        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: .75rem;
            border: 1px solid var(--border);
            background: var(--surface);
            border-radius: 8px;
            padding: .65rem .7rem;
            margin: .15rem 0 .65rem;
            box-shadow: var(--shadow);
            width: 100%;
            max-width: 100%;
            min-width: 0;
            transform-origin: center;
            transition:
                transform 240ms ease,
                border-color 240ms ease,
                background-color 240ms ease,
                box-shadow 240ms ease;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .sidebar-brand:hover,
            .sidebar-brand:focus-within {{
                transform: translateY(-3px);
                border-color: rgba(180, 83, 9, 0.45);
                background-color: rgba(239, 246, 255, 0.75);
                box-shadow: 0 14px 30px rgba(180, 83, 9, 0.14);
                position: relative;
                z-index: 2;
            }}
        }}
        .sidebar-brand > div:last-child {{
            min-width: 0;
        }}
        .brand-icon, .dataset-icon, .kpi-icon {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--tag-bg);
            color: var(--tag-text);
            font-weight: 700;
            flex: 0 0 auto;
        }}
        .brand-photo {{
            width: 42px;
            height: 42px;
            border-radius: 8px;
            flex: 0 0 42px;
            object-fit: cover;
            object-position: center top;
            display: block;
        }}
        .brand-title {{ color: var(--text); font-weight: 700; line-height: 1.15; }}
        .brand-subtitle {{ color: var(--muted); font-size: .82rem; margin-top: .12rem; }}
        .sidebar-profile-divider {{
            height: 1px;
            margin: 1rem 0 .85rem;
            background: rgba(148, 163, 184, .28);
        }}
        .sidebar-profile-card {{
            margin-top: 0;
            margin-bottom: .65rem;
        }}
        .sidebar-links {{
            margin: 0 0 .65rem;
            color: var(--muted);
            font-size: .84rem;
        }}
        .sidebar-social-links {{
            display: block;
        }}
        .sidebar-links a {{
            color: var(--accent-bright);
            text-decoration: none;
            font-weight: 500;
            transition: color 180ms ease, opacity 180ms ease;
        }}
        .sidebar-divider {{
            height: 1px;
            width: 100%;
            background: rgba(148, 163, 184, .28);
            margin: .75rem 0;
        }}
        .sidebar-section-expander {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
            box-sizing: border-box;
            margin: 0;
        }}
        .sidebar-portfolio {{
            width: 100%;
            max-width: 100%;
            margin: .25rem 0 0;
        }}
        .sidebar-projects {{
            width: 100%;
            max-width: 100%;
            margin: 0 0 .5rem;
        }}
        .sidebar-projects-expander {{
            width: 100%;
            max-width: 100%;
            margin: 0;
        }}
        .sidebar-section-toggle {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
            min-height: 44px;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 14px;
            border: 0;
            border-radius: 10px;
            color: var(--text);
            background: transparent;
            font-family: inherit;
            font-size: .75rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            cursor: pointer;
            list-style: none;
            user-select: none;
            transition:
                background-color 180ms ease,
                color 180ms ease;
        }}
        .sidebar-section-toggle::-webkit-details-marker,
        .sidebar-project-summary::-webkit-details-marker {{
            display: none;
        }}
        .sidebar-section-toggle::marker,
        .sidebar-project-summary::marker {{
            content: "";
        }}
        .sidebar-section-toggle:hover,
        .sidebar-section-toggle:focus-visible {{
            background: rgba(239, 246, 255, .72);
            outline: none;
        }}
        .sidebar-section-toggle:focus-visible,
        .sidebar-project-summary:focus-visible {{
            box-shadow: 0 0 0 3px rgba(180, 83, 9, .16);
        }}
        .sidebar-expander-chevron,
        .sidebar-project-chevron {{
            width: 16px;
            height: 16px;
            flex: 0 0 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--data-blue);
            transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1);
            transform-origin: center;
        }}
        .sidebar-expander-chevron svg,
        .sidebar-project-chevron svg {{
            width: 14px;
            height: 14px;
            fill: none;
            stroke: currentColor;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .sidebar-section-expander[open] > .sidebar-section-toggle .sidebar-expander-chevron,
        .sidebar-project-expander[open] > .sidebar-project-summary .sidebar-project-chevron {{
            transform: rotate(180deg);
        }}
        .sidebar-section-content {{
            display: grid;
            grid-template-rows: 0fr;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            opacity: 0;
            transition:
                grid-template-rows 220ms ease,
                opacity 160ms ease;
        }}
        .sidebar-section-expander[open] > .sidebar-section-content {{
            grid-template-rows: 1fr;
            opacity: 1;
        }}
        .sidebar-section-content-inner {{
            min-height: 0;
            overflow: hidden;
        }}
        .sidebar-portfolio-content {{
            margin-top: .5rem;
        }}
        .sidebar-projects-content {{
            width: 100%;
            max-width: 100%;
            margin-top: .5rem;
        }}
        .sidebar-portfolio-links {{
            display: flex;
            flex-direction: column;
            gap: .08rem;
            padding: .35rem 0 .25rem .85rem;
            border-left: 1px solid rgba(180, 83, 9, .20);
        }}
        .sidebar-portfolio-link {{
            display: flex;
            align-items: center;
            min-height: 2.05rem;
            padding: .38rem .5rem;
            border-radius: 8px;
            color: var(--text-2);
            font-size: .84rem;
            font-weight: 600;
            line-height: 1.2;
            text-decoration: none;
            transition:
                background-color 180ms ease,
                color 180ms ease;
        }}
        .sidebar-portfolio-link:hover,
        .sidebar-portfolio-link:focus-visible {{
            color: var(--data-blue);
            background: rgba(239, 246, 255, .82);
            outline: none;
            text-decoration: none;
        }}
        .sidebar-portfolio-link:focus-visible {{
            box-shadow: 0 0 0 3px rgba(180, 83, 9, .14);
        }}
        .sidebar-portfolio-link-active {{
            color: var(--data-blue);
            background: rgba(180, 83, 9, .09);
            font-weight: 700;
        }}
        .sidebar-project-expander {{
            width: 100%;
            max-width: 100%;
            min-width: 0;
        }}
        .sidebar-project-summary {{
            cursor: pointer;
            list-style: none;
            user-select: none;
        }}
        .sidebar-project-card {{
            position: relative;
            width: 100%;
            min-height: 92px;
            padding: .75rem 2rem .75rem .75rem;
            border: 1px solid rgba(180, 83, 9, .18);
            border-radius: 11px;
            background:
                radial-gradient(circle at 85% 15%, rgba(30, 58, 95, .09), transparent 38%),
                linear-gradient(145deg, rgba(255, 255, 255, .96), rgba(239, 246, 255, .86));
            box-shadow: 0 8px 20px rgba(15, 23, 42, .06);
            overflow: hidden;
            transition:
                transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
                border-color 220ms ease,
                box-shadow 220ms ease;
        }}
        .sidebar-project-chevron {{
            position: absolute;
            top: .78rem;
            right: .68rem;
        }}
        .sidebar-project-card-active {{
            border-color: rgba(180, 83, 9, .34);
            background:
                radial-gradient(circle at 85% 15%, rgba(30, 58, 95, .12), transparent 38%),
                rgba(239, 246, 255, .92);
        }}
        .sidebar-project-expander.is-active > .sidebar-project-summary {{
            border-color: rgba(180, 83, 9, .42);
            background:
                radial-gradient(circle at 85% 15%, rgba(30, 58, 95, .11), transparent 38%),
                rgba(239, 246, 255, .94);
        }}
        .sidebar-project-card-header {{
            display: flex;
            align-items: center;
            gap: .62rem;
            min-width: 0;
        }}
        .sidebar-project-icon {{
            width: 30px;
            height: 30px;
            flex: 0 0 30px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 9px;
            color: var(--data-blue);
            background: rgba(180, 83, 9, .10);
            border: 1px solid rgba(180, 83, 9, .16);
        }}
        .sidebar-project-icon svg {{
            width: 17px;
            height: 17px;
            fill: none;
            stroke: currentColor;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .sidebar-project-copy {{
            min-width: 0;
            padding-right: .7rem;
        }}
        .sidebar-project-name {{
            color: var(--text);
            font-size: .86rem;
            font-weight: 800;
            line-height: 1.16;
            overflow-wrap: anywhere;
        }}
        .sidebar-project-type {{
            color: var(--muted);
            font-size: .7rem;
            font-weight: 650;
            line-height: 1.2;
            margin-top: .18rem;
        }}
        .sidebar-project-links {{
            position: relative;
            display: flex;
            flex-direction: column;
            gap: .08rem;
            margin: .25rem 0 .15rem .8rem;
            padding: .35rem 0 .25rem .85rem;
            border-left: 1px solid rgba(180, 83, 9, .20);
        }}
        .sidebar-project-expander[open] > .sidebar-project-links {{
            animation: sidebar-project-content-in 220ms cubic-bezier(0.22, 1, 0.36, 1) both;
        }}
        @keyframes sidebar-project-content-in {{
            from {{
                opacity: 0;
                transform: translateY(-4px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .sidebar-project-link {{
            position: relative;
            display: flex;
            align-items: center;
            min-height: 2.05rem;
            padding: .38rem .5rem;
            border-radius: 8px;
            color: var(--text-2);
            font-size: .82rem;
            font-weight: 600;
            line-height: 1.2;
            text-decoration: none;
            transition:
                background-color 180ms ease,
                color 180ms ease,
                border-color 180ms ease;
        }}
        .sidebar-project-link::before {{
            content: "";
            position: absolute;
            left: -.98rem;
            top: 50%;
            width: 6px;
            height: 6px;
            border-radius: 999px;
            background: rgba(180, 83, 9, .26);
            transform: translateY(-50%);
        }}
        .sidebar-project-link:hover,
        .sidebar-project-link:focus-visible {{
            color: var(--data-blue);
            background: rgba(239, 246, 255, .82);
            text-decoration: none;
        }}
        .sidebar-project-link:hover::before,
        .sidebar-project-link:focus-visible::before {{
            background: var(--data-blue);
        }}
        .sidebar-project-link-active {{
            color: var(--data-blue);
            background: rgba(180, 83, 9, .09);
            font-weight: 700;
        }}
        .sidebar-project-link-active::before {{
            background: #b45309;
            box-shadow: 0 0 0 3px rgba(180, 83, 9, .12);
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] {{
            width: 100%;
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] a {{
            display: flex;
            align-items: center;
            min-height: 2.05rem;
            padding: .38rem .5rem;
            border-radius: 8px;
            color: var(--text-2);
            font-size: .84rem;
            font-weight: 600;
            line-height: 1.2;
            text-decoration: none;
            transition:
                background-color 180ms ease,
                color 180ms ease;
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] a {{
            position: relative;
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] a::before {{
            content: "";
            position: absolute;
            left: -.98rem;
            top: 50%;
            width: 6px;
            height: 6px;
            border-radius: 999px;
            background: rgba(180, 83, 9, .26);
            transform: translateY(-50%);
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:focus-visible {{
            color: var(--data-blue);
            background: rgba(239, 246, 255, .82);
            outline: none;
            text-decoration: none;
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover::before,
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:focus-visible::before {{
            background: var(--data-blue);
        }}
        .sidebar-project-mini-lineage {{
            position: relative;
            display: grid;
            grid-template-columns: 10px minmax(0, 1fr) 10px minmax(0, 1fr) 10px;
            align-items: center;
            gap: .25rem;
            height: 22px;
            margin-top: .62rem;
            opacity: .82;
            pointer-events: none;
        }}
        .sidebar-mini-stage {{
            position: relative;
            z-index: 3;
            width: 10px;
            height: 10px;
            border-radius: 4px;
            background: rgba(255, 255, 255, .95);
            border: 1px solid rgba(180, 83, 9, .26);
        }}
        .sidebar-mini-mart {{
            border-color: rgba(30, 58, 95, .35);
            background: rgba(236, 254, 255, .95);
        }}
        .sidebar-mini-track {{
            position: relative;
            z-index: 1;
            height: 2px;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(180, 83, 9, .24), rgba(30, 58, 95, .26));
        }}
        .sidebar-mini-packet {{
            position: absolute;
            z-index: 2;
            left: 3px;
            top: 50%;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: #b45309;
            box-shadow:
                0 0 0 3px rgba(180, 83, 9, .10),
                0 0 7px rgba(180, 83, 9, .26);
            transform: translate3d(0, -50%, 0);
            animation: sidebar-mini-packet-flow 4s linear infinite;
            pointer-events: none;
        }}
        @keyframes sidebar-mini-packet-flow {{
            0% {{ left: 3px; opacity: 0; background: #b45309; }}
            8% {{ opacity: 1; }}
            72% {{ opacity: 1; background: #b45309; }}
            88% {{ opacity: 1; background: #1e3a5f; }}
            96%, 100% {{ left: calc(100% - 8px); opacity: 0; background: #1e3a5f; }}
        }}
        .sidebar-projects-expander:not([open]) .sidebar-mini-packet {{
            animation-play-state: paused;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .sidebar-project-card:hover,
            .sidebar-project-card:focus-within {{
                transform: translateY(-2px);
                border-color: rgba(180, 83, 9, .38);
                box-shadow: 0 10px 24px rgba(180, 83, 9, .10);
            }}
        }}

        .page-header {{
            position: relative;
            margin: .15rem 0 1rem;
            max-width: 900px;
        }}
        .page-header-overview::after,
        .page-header-dashboard::after {{
            content: "";
            position: absolute;
            right: .2rem;
            top: .35rem;
            width: 6.5rem;
            height: 3.6rem;
            opacity: .045;
            pointer-events: none;
            background:
                radial-gradient(circle, var(--data-blue) 0 2px, transparent 3px),
                linear-gradient(90deg, transparent 48%, var(--data-cyan) 49% 51%, transparent 52%);
            background-size: 1.7rem 1.7rem, 100% 100%;
        }}
        .page-header-home,
        .page-header-overview {{
            margin-top: 1rem;
        }}
        .page-header-home .product-kicker {{
            color: var(--accent-hover);
            border-color: color-mix(in srgb, var(--accent) 35%, transparent);
            font-size: .96rem;
            font-weight: 700;
            padding: .5rem .875rem;
            white-space: normal;
        }}
        .page-header-overview {{
            margin-top: 1.55rem;
        }}
        .page-header-overview .product-kicker {{
            margin-bottom: .8rem;
        }}
        .product-kicker {{
            display: inline-flex;
            align-items: center;
            min-height: 1.9rem;
            line-height: 1.2;
            color: var(--tag-text);
            background: var(--tag-bg);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: .34rem .58rem;
            font-weight: 600;
            font-size: .82rem;
            margin-bottom: .6rem;
        }}
        .product-title {{
            color: var(--text);
            font-size: clamp(1.95rem, 4vw, 3.25rem);
            line-height: 1.1;
            font-weight: 700;
            margin: 0;
        }}
        .product-subtitle {{
            color: var(--text-2);
            max-width: 780px;
            line-height: 1.65;
            margin-top: .7rem;
            font-size: 1rem;
            font-weight: 400;
        }}

        .portfolio-hero {{
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(210px, .48fr);
            align-items: start;
            column-gap: clamp(1.1rem, 2vw, 1.65rem);
            row-gap: .55rem;
            height: auto;
            min-height: 0;
            padding: 0;
            overflow: visible;
        }}
        .data-command-hero {{
            position: relative;
            isolation: isolate;
            padding: clamp(.9rem, 1.55vw, 1.18rem);
            height: auto;
            min-height: 0;
            margin: .2rem 0 .85rem;
            border: 1px solid rgba(180, 83, 9, .14);
            border-radius: 18px;
            background:
                radial-gradient(circle at 78% 52%, rgba(180, 83, 9, .11), transparent 31%),
                radial-gradient(circle at 26% 30%, rgba(30, 58, 95, .075), transparent 28%),
                linear-gradient(145deg, rgba(255, 255, 255, .96), rgba(248, 250, 252, .90));
            box-shadow: 0 14px 34px rgba(15, 23, 42, .065);
            overflow: hidden;
        }}
        .data-blueprint-grid {{
            position: absolute;
            inset: 0;
            z-index: -3;
            opacity: .34;
            background-image:
                linear-gradient(rgba(180, 83, 9, .045) 1px, transparent 1px),
                linear-gradient(90deg, rgba(180, 83, 9, .045) 1px, transparent 1px),
                linear-gradient(rgba(15, 23, 42, .035) 1px, transparent 1px);
            background-size: 34px 34px;
            mask-image: linear-gradient(135deg, rgba(0, 0, 0, .76), transparent 78%);
        }}
        .data-background-path {{
            display: none;
        }}
        .data-background-particle {{
            display: none;
        }}
        .data-background-particle-1 {{
            left: 10%;
            bottom: 18%;
        }}
        .data-background-particle-2 {{
            right: 18%;
            top: 24%;
            animation-delay: 4.4s;
        }}
        @keyframes data-background-particle-flow {{
            0%, 12% {{ opacity: 0; transform: translate3d(0, 0, 0); }}
            18%, 60% {{ opacity: .75; }}
            84%, 100% {{ opacity: 0; transform: translate3d(78px, -34px, 0); }}
        }}
        .hero-copy {{
            min-width: 0;
            display: flex;
            flex-direction: column;
            grid-column: 1;
            grid-row: 1;
        }}
        .hero-kicker,
        .hero-copy h1,
        .hero-copy > p,
        .hero-value-rotator,
        .hero-actions,
        .hero-skill-section,
        .hero-profile-card {{
            animation: home-entrance-rise 520ms ease-out both;
        }}
        .hero-kicker {{ animation-delay: 40ms; }}
        .hero-copy h1 {{ animation-delay: 120ms; }}
        .hero-copy > p {{ animation-delay: 200ms; }}
        .hero-value-rotator {{ animation-delay: 280ms; }}
        .hero-actions {{ animation-delay: 360ms; }}
        .hero-profile-card {{ animation-delay: 440ms; }}
        .hero-skill-section {{ animation-delay: 520ms; }}
        @keyframes home-entrance-rise {{
            from {{ opacity: 0; transform: translateY(.65rem); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes home-skill-node-enter {{
            from {{ opacity: 0; transform: translateX(-.45rem); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        .portfolio-hero-spacer {{
            height: .5rem;
        }}
        .hero-kicker,
        .section-eyebrow {{
            color: var(--accent);
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: 0;
        }}
        .portfolio-hero h1 {{
            color: var(--text);
            font-size: clamp(2.6rem, 4.1vw, 3.18rem);
            line-height: 1.02;
            font-weight: 750;
            letter-spacing: 0;
            max-width: 560px;
            margin: .65rem 0 0;
        }}
        .portfolio-hero p,
        .contact-cta p {{
            color: var(--text-2);
            max-width: 680px;
            font-size: 1rem;
            line-height: 1.58;
            margin: .75rem 0 0;
        }}
        .hero-description {{
            max-width: 680px;
            margin-top: .68rem;
            line-height: 1.52;
        }}
        .hero-value-rotator {{
            position: relative;
            width: min(100%, 31rem);
            min-height: 1.55rem;
            margin-top: .45rem;
            border-left: 3px solid rgba(180, 83, 9, .42);
            padding: .22rem .58rem;
            color: var(--accent);
            font-size: .84rem;
            font-weight: 800;
            letter-spacing: .01em;
            overflow: hidden;
        }}
        .hero-value-line {{
            position: absolute;
            inset: .25rem auto auto .68rem;
            opacity: 0;
            transform: translateY(.55rem);
            animation: hero-value-rotate 16s ease-in-out infinite;
        }}
        .hero-value-line-1 {{ animation-delay: 0s; }}
        .hero-value-line-2 {{ animation-delay: 4s; }}
        .hero-value-line-3 {{ animation-delay: 8s; }}
        .hero-value-line-4 {{ animation-delay: 12s; }}
        @keyframes hero-value-rotate {{
            0%, 5% {{ opacity: 0; transform: translateY(.55rem); }}
            10%, 21% {{ opacity: 1; transform: translateY(0); }}
            26%, 100% {{ opacity: 0; transform: translateY(-.45rem); }}
        }}
        .hero-actions,
        .contact-cta-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: .7rem;
            margin-top: .78rem;
        }}
        .portfolio-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.65rem;
            padding: .7rem 1rem;
            border-radius: 10px;
            border: 1px solid rgba(180, 83, 9, .22);
            background: var(--surface);
            color: var(--data-blue);
            font-weight: 700;
            font-size: .82rem;
            line-height: 1.15;
            text-decoration: none;
            transition: background-color 180ms ease, border-color 180ms ease, color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
        }}
        .portfolio-button:hover {{
            border-color: var(--accent);
            background: var(--hover);
            color: var(--accent);
            text-decoration: none;
        }}
        .portfolio-button-primary {{
            background: var(--data-blue);
            border-color: var(--data-blue);
            color: var(--on-accent) !important;
            box-shadow: var(--shadow-accent);
        }}
        .portfolio-button-primary:hover {{
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            color: var(--on-accent) !important;
        }}
        .portfolio-button-quiet {{
            background: transparent;
        }}
        .hero-primary-action {{
            gap: .42rem;
        }}
        .hero-primary-action span {{
            display: inline-block;
            transform: translateX(0);
            transition: transform 180ms ease;
        }}
        .hero-stack {{
            display: flex;
            flex-wrap: wrap;
            gap: .35rem;
            margin-top: 1.15rem;
        }}
        .hero-skill-section {{
            grid-column: 1 / -1;
            grid-row: 2;
            margin-top: 0;
            width: 100%;
        }}
        .hero-skill-label {{
            margin-bottom: .36rem;
            color: var(--text-2);
            font-size: .68rem;
            font-weight: 750;
            letter-spacing: .11em;
            text-transform: uppercase;
        }}
        .hero-skill-pipeline {{
            position: relative;
            isolation: isolate;
            z-index: 5;
            display: grid;
            grid-template-columns: repeat(6, minmax(104px, 128px));
            justify-content: center;
            align-items: center;
            gap: .85rem;
            width: 100%;
            padding-top: 2.05rem;
            margin-top: 0;
            overflow: visible;
            container-type: inline-size;
        }}
        .core-workflow-orchestrator {{
            position: absolute;
            z-index: 4;
            top: 0;
            left: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 0;
            height: 1.65rem;
            padding: .22rem .55rem;
            border: 1px solid rgba(180, 83, 9, .20);
            border-radius: 999px;
            background: rgba(239, 246, 255, .92);
            box-shadow: 0 4px 10px rgba(180, 83, 9, .045);
            color: var(--data-blue);
            transform: translateX(-50%);
            overflow: hidden;
            pointer-events: none;
        }}
        .core-workflow-orchestrator-label {{
            display: inline-flex;
            align-items: baseline;
            gap: .32rem;
            white-space: nowrap;
        }}
        .core-workflow-orchestrator-label strong {{
            font-size: .6rem;
            font-weight: 850;
            letter-spacing: .04em;
        }}
        .core-workflow-orchestrator-label small {{
            color: var(--text-2);
            font-size: .58rem;
            font-weight: 750;
        }}
        .core-workflow-orchestration-line {{
            position: absolute;
            z-index: 2;
            top: 1.65rem;
            left: 50%;
            width: 2px;
            height: .48rem;
            border-radius: 999px;
            background: rgba(180, 83, 9, .28);
            transform: translateX(-50%);
            pointer-events: none;
        }}
        @property --hero-glow {{
            syntax: '<number>';
            inherits: true;
            initial-value: 0;
        }}
        .hero-flow-svg {{
            position: absolute;
            left: 4%;
            right: 4%;
            top: calc(2.05rem + 19px);
            z-index: 1;
            width: 92%;
            height: 40px;
            overflow: visible;
            pointer-events: none;
        }}
        .hero-flow-svg-tablet,
        .hero-flow-svg-mobile {{
            display: none;
        }}
        .hero-flow-base {{
            fill: none;
            stroke: var(--border);
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            vector-effect: non-scaling-stroke;
        }}
        .hero-flow-energy {{
            fill: none;
            stroke: var(--data-cyan);
            stroke-width: 2.6;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-dasharray: 18 82;
            vector-effect: non-scaling-stroke;
            filter: drop-shadow(0 0 4px color-mix(in srgb, var(--data-cyan) 65%, transparent));
        }}
        .hero-flow-dot {{
            fill: var(--data-cyan);
            stroke: var(--surface);
            stroke-width: .8;
            filter: drop-shadow(0 0 5px color-mix(in srgb, var(--data-cyan) 80%, transparent));
        }}
        .hero-skill-node {{
            position: relative;
            z-index: 3;
            min-width: 0;
            min-height: 76px;
            height: 76px;
            display: grid;
            grid-template-columns: auto minmax(0, 1fr);
            align-items: center;
            gap: .46rem;
            padding: .58rem .62rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--surface);
            box-shadow: 0 5px 12px rgba(15, 23, 42, .05);
            color: var(--text);
            text-align: left;
            text-decoration: none;
            cursor: pointer;
            transform-origin: center;
            transition: border-color .16s ease, box-shadow .16s ease, transform .16s ease;
            animation: home-skill-node-enter 420ms ease-out both;
            --hero-glow: 0;
        }}
        .hero-skill-node::before {{
            content: "";
            position: absolute;
            inset: -3px;
            z-index: -1;
            border-radius: 15px;
            border: 2px solid var(--data-blue);
            box-shadow:
                0 0 0 4px color-mix(in srgb, var(--data-blue) 16%, transparent),
                0 0 20px color-mix(in srgb, var(--data-blue) 45%, transparent);
            opacity: var(--hero-glow);
            pointer-events: none;
        }}
        .hero-skill-node-6::before {{
            border-color: var(--data-green);
            box-shadow:
                0 0 0 4px color-mix(in srgb, var(--data-green) 18%, transparent),
                0 0 20px color-mix(in srgb, var(--data-green) 50%, transparent);
        }}
        .hero-skill-icon {{
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--muted);
            box-shadow: 0 0 0 2px color-mix(in srgb, var(--muted) 12%, transparent);
        }}
        .hero-skill-node-content {{
            position: relative;
            z-index: 5;
            display: grid;
            gap: .22rem;
            min-width: 0;
        }}
        .core-workflow-stage {{
            color: var(--text-2);
            font-size: .52rem;
            font-weight: 850;
            letter-spacing: .08em;
            line-height: 1;
            text-transform: uppercase;
        }}
        .core-workflow-tool {{
            color: var(--text);
            font-size: .74rem;
            font-weight: 850;
            line-height: 1.15;
            overflow-wrap: normal;
        }}
        .hero-skill-tooltip {{
            position: absolute;
            left: 50%;
            bottom: calc(100% + 10px);
            z-index: 20;
            width: max-content;
            max-width: 200px;
            padding: .5rem .65rem;
            border-radius: 10px;
            background: var(--text);
            color: var(--surface);
            font-size: .68rem;
            font-weight: 600;
            line-height: 1.4;
            text-align: left;
            opacity: 0;
            transform: translate(-50%, 4px);
            transition: opacity .16s ease, transform .16s ease;
            pointer-events: none;
            box-shadow: 0 12px 26px rgba(15, 23, 42, .2);
        }}
        .hero-skill-tooltip::after {{
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: var(--text);
        }}
        .hero-skill-node:focus-visible {{
            border-color: var(--accent);
            outline: 2px solid var(--accent);
            outline-offset: 2px;
            box-shadow: 0 10px 22px color-mix(in srgb, var(--accent) 16%, transparent);
        }}
        .hero-skill-node:focus-visible .hero-skill-tooltip {{
            opacity: 1;
            transform: translate(-50%, 0);
        }}
        .hero-skill-node-1 {{ animation-delay: 120ms; }}
        .hero-skill-node-2 {{ animation-delay: 170ms; }}
        .hero-skill-node-3 {{ animation-delay: 220ms; }}
        .hero-skill-node-4 {{ animation-delay: 270ms; }}
        .hero-skill-node-5 {{ animation-delay: 320ms; }}
        .hero-skill-node-6 {{ animation-delay: 370ms; }}
        .hero-skill-node-1 {{ animation-name: home-skill-node-enter, hero-node-pulse-1; }}
        .hero-skill-node-2 {{ animation-name: home-skill-node-enter, hero-node-pulse-2; }}
        .hero-skill-node-3 {{ animation-name: home-skill-node-enter, hero-node-pulse-3; }}
        .hero-skill-node-4 {{ animation-name: home-skill-node-enter, hero-node-pulse-4; }}
        .hero-skill-node-5 {{ animation-name: home-skill-node-enter, hero-node-pulse-5; }}
        .hero-skill-node-6 {{ animation-name: home-skill-node-enter, hero-node-pulse-6; }}
        .hero-skill-node-1,
        .hero-skill-node-2,
        .hero-skill-node-3,
        .hero-skill-node-4,
        .hero-skill-node-5,
        .hero-skill-node-6 {{
            animation-duration: 420ms, 7s;
            animation-timing-function: ease-out, ease-in-out;
            animation-iteration-count: 1, infinite;
            animation-fill-mode: both, none;
        }}
        @keyframes hero-node-pulse-1 {{
            0%, 8%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            2% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-2 {{
            0%, 9%, 25%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            17% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-3 {{
            0%, 26%, 42%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            34% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-4 {{
            0%, 43%, 59%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            51% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-5 {{
            0%, 60%, 76%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            68% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-6 {{
            0%, 77%, 93%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            85% {{ transform: scale(1.07); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-1 {{
            0%, 8%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            2% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-2 {{
            0%, 10.5%, 26.5%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            18.5% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-3 {{
            0%, 29%, 45%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            37% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-4 {{
            0%, 40%, 56%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            48% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-5 {{
            0%, 58.5%, 74.5%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            66.5% {{ transform: scale(1.05); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        @keyframes hero-node-pulse-tablet-6 {{
            0%, 77%, 93%, 100% {{ transform: scale(1); --hero-glow: 0; }}
            85% {{ transform: scale(1.07); --hero-glow: 1; animation-timing-function: cubic-bezier(.34, 1.56, .64, 1); }}
        }}
        .hero-photo-shell {{
            justify-self: center;
            width: min(100%, 360px);
            aspect-ratio: 1;
            border-radius: 34px;
            padding: 1rem;
            background:
                radial-gradient(circle at 72% 18%, rgba(180, 83, 9, .2), transparent 36%),
                linear-gradient(145deg, rgba(239, 246, 255, .95), rgba(255, 255, 255, .5));
            border: 1px solid rgba(180, 83, 9, .18);
            box-shadow: 0 22px 44px rgba(180, 83, 9, .14);
            overflow: hidden;
        }}
        .hero-photo {{
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
            object-position: center top;
            border-radius: 26px;
            box-shadow: var(--shadow);
        }}
        .hero-photo-fallback {{
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--tag-bg);
            color: var(--tag-text);
            font-size: 3rem;
            font-weight: 800;
        }}
        .st-key-home_profile_photo_shell,
        .st-key-home_profile_info_card {{
            width: min(100%, 360px);
            margin-left: auto;
            margin-right: auto;
            overflow: visible;
        }}
        .st-key-home_profile_photo_shell {{
            margin-top: 1rem;
            transform: none;
            animation: none;
        }}
        .st-key-home_profile_info_card {{
            margin-top: .75rem;
        }}
        .st-key-home_profile_photo_shell [data-testid="stImage"] {{
            margin: 0 auto;
            transform: none;
            animation: none;
        }}
        .st-key-home_profile_photo_shell img {{
            display: block;
            width: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            object-position: center top;
            border-radius: 18px;
            border: 1px solid rgba(180, 83, 9, .18);
            box-shadow: 0 18px 38px rgba(180, 83, 9, .12);
            transform: none;
            animation: none;
        }}
        .st-key-home_profile_photo_shell:hover,
        .st-key-home_profile_photo_shell:focus-within,
        .st-key-home_profile_photo_shell:hover img,
        .st-key-home_profile_photo_shell [data-testid="stImage"]:hover img {{
            transform: none;
        }}
        .home-profile-info-card {{
            padding: 1rem 1rem 1.05rem;
            border: 1px solid rgba(180, 83, 9, .22);
            border-radius: 18px;
            background:
                radial-gradient(circle at 72% 12%, rgba(180, 83, 9, .14), transparent 34%),
                linear-gradient(145deg, rgba(255, 255, 255, .96), rgba(248, 250, 252, .92));
            box-shadow: 0 18px 38px rgba(180, 83, 9, .12);
            overflow: hidden;
            transform-origin: center center;
            transition:
                transform 250ms cubic-bezier(0.22, 1, 0.36, 1),
                border-color 250ms ease,
                box-shadow 250ms ease;
        }}
        .home-profile-info-card {{
            text-align: center;
        }}
        .home-profile-info-name {{
            color: var(--text);
            font-size: 1.22rem;
            line-height: 1.2;
            font-weight: 800;
            transition: color 250ms ease;
        }}
        .home-profile-info-role {{
            color: var(--accent);
            font-size: .94rem;
            font-weight: 700;
            line-height: 1.35;
            margin-top: .18rem;
        }}
        .home-profile-info-status {{
            display: inline-flex;
            align-items: center;
            gap: .38rem;
            color: var(--tag-text);
            background: var(--tag-bg);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: .34rem .58rem;
            font-size: .78rem;
            font-weight: 700;
            margin-top: .7rem;
        }}
        .home-profile-info-status span {{
            width: .48rem;
            height: .48rem;
            border-radius: 999px;
            background: var(--positive);
            box-shadow: 0 0 0 3px color-mix(in srgb, var(--positive) 20%, transparent);
            transition: box-shadow 250ms ease;
        }}
        .hero-profile-card {{
            position: relative;
            justify-self: center;
            align-self: start;
            grid-column: 2;
            grid-row: 1;
            width: min(100%, 340px);
            height: fit-content;
            min-height: 0;
            padding: 0;
            border: 1px solid color-mix(in srgb, var(--border) 85%, var(--accent));
            border-radius: 20px;
            background: var(--surface);
            box-shadow:
                0 24px 48px -20px rgba(22, 33, 46, 0.22),
                0 2px 6px rgba(22, 33, 46, 0.05);
            overflow: hidden;
            transform: translateZ(0);
            transition:
                transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 240ms ease;
        }}
        .hero-profile-card::before {{
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 4px;
            z-index: 2;
            background: linear-gradient(90deg, var(--accent), var(--accent-bright));
        }}
        .hero-profile-card:hover {{
            transform: translateY(-3px);
            box-shadow:
                0 30px 56px -20px rgba(22, 33, 46, 0.28),
                0 2px 6px rgba(22, 33, 46, 0.05);
        }}
        .hero-profile-card:focus-within {{
            box-shadow: 0 0 0 3px rgba(180, 83, 9, 0.16);
        }}
        .hero-profile-media {{
            position: relative;
            background: transparent;
        }}
        .hero-profile-media::after {{
            content: "";
            position: absolute;
            inset: auto 0 0 0;
            height: 38%;
            background: linear-gradient(180deg, transparent, rgba(22, 33, 46, .18));
            pointer-events: none;
        }}
        .hero-profile-image-wrap {{
            width: 100%;
            height: clamp(260px, 25vw, 300px);
            overflow: hidden;
            border: 0;
            border-radius: 0;
            background: var(--surface-2);
        }}
        .hero-profile-image {{
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 22%;
            border-radius: 0;
            border: 0;
            box-shadow: none;
            transform: none;
            animation: none;
        }}
        .hero-profile-identity {{
            display: flex;
            flex-direction: column;
            gap: .85rem;
            padding: 1.15rem 1.25rem 1.25rem;
            text-align: left;
            border-top: 0;
        }}
        .hero-profile-heading {{
            display: flex;
            flex-direction: column;
            gap: .25rem;
        }}
        .hero-profile-name {{
            margin: 0;
            color: var(--text);
            font-size: clamp(1.6rem, 2.2vw, 1.95rem);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -.01em;
            white-space: nowrap;
        }}
        .hero-profile-role {{
            margin: 0;
            color: var(--accent);
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
            line-height: 1.3;
        }}
        .hero-profile-meta {{
            display: flex;
            align-items: center;
            justify-content: flex-start;
            flex-wrap: wrap;
            gap: .42rem;
            margin: 0;
        }}
        .hero-profile-stack {{
            display: flex;
            flex-wrap: wrap;
            gap: .35rem;
            padding-top: .85rem;
            border-top: 1px solid var(--border);
        }}
        .hero-profile-stack span {{
            padding: 3px 9px;
            border-radius: 6px;
            background: var(--surface-2);
            color: var(--text-2);
            font-size: .75rem;
            font-weight: 650;
            line-height: 1.5;
        }}
        .hero-profile-links {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: .5rem;
        }}
        .hero-profile-links a {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 36px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface);
            color: var(--text) !important;
            font-size: .82rem;
            font-weight: 700;
            text-decoration: none !important;
            transition: border-color 160ms ease, background 160ms ease, color 160ms ease;
        }}
        .hero-profile-links a:hover {{
            border-color: var(--accent);
            background: var(--hover);
            color: var(--accent-hover) !important;
        }}
        .hero-profile-status {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            min-height: 28px;
            padding: 4px 10px;
            border: 1px solid color-mix(in srgb, var(--positive) 22%, transparent);
            border-radius: 999px;
            background: color-mix(in srgb, var(--positive) 10%, var(--tag-bg));
            color: color-mix(in srgb, var(--positive) 62%, var(--text));
            font-size: .78rem;
            font-weight: 650;
            line-height: 1;
            white-space: nowrap;
        }}
        .hero-profile-status-dot {{
            width: 8px;
            height: 8px;
            min-width: 8px;
            min-height: 8px;
            max-width: 8px;
            max-height: 8px;
            flex: 0 0 8px;
            aspect-ratio: 1 / 1;
            border-radius: 50%;
            background: var(--positive);
            box-shadow: 0 0 0 3px color-mix(in srgb, var(--positive) 14%, transparent);
        }}
        .hero-profile-location {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            min-height: 28px;
            padding: 4px 10px;
            border: 1px solid color-mix(in srgb, var(--border) 78%, var(--accent));
            border-radius: 999px;
            background: color-mix(in srgb, var(--surface-2) 84%, var(--tag-bg));
            color: var(--text-2);
            font-size: .78rem;
            font-weight: 600;
            line-height: 1;
            white-space: nowrap;
        }}
        .hero-profile-location-icon {{
            position: relative;
            width: 9px;
            height: 9px;
            flex: 0 0 9px;
            border: 1.6px solid currentColor;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
        }}
        .hero-profile-location-icon::after {{
            content: "";
            position: absolute;
            inset: 2px;
            border-radius: 999px;
            background: currentColor;
        }}
        .featured-project-card,
        .pipeline-step-card,
        .contact-cta {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
        }}
        .featured-project-card {{
            position: relative;
            display: grid;
            grid-template-columns: minmax(0, 42fr) minmax(0, 58fr);
            grid-auto-rows: max-content;
            gap: clamp(.9rem, 1.5vw, 1.25rem);
            align-items: start;
            height: auto;
            min-height: 0;
            padding: 1rem;
            margin: 1.1rem 0 1.45rem;
            overflow: visible;
        }}
        .featured-project-copy,
        .featured-preview,
        .featured-lineage-preview {{
            align-self: start;
            height: fit-content;
            min-height: 0;
        }}
        .featured-project-copy h2,
        .home-section h2,
        .contact-cta h2 {{
            color: var(--text);
            font-size: clamp(1.55rem, 3vw, 2.15rem);
            line-height: 1.12;
            margin: 0;
        }}
        .featured-project-copy p {{
            color: var(--text-2);
            line-height: 1.65;
            margin: .75rem 0 0;
        }}
        .featured-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: .5rem;
            margin-top: 1rem;
        }}
        .featured-meta span {{
            display: inline-flex;
            border: 1px solid var(--border);
            background: var(--tag-bg);
            color: var(--tag-text);
            border-radius: 999px;
            padding: .34rem .58rem;
            font-size: .82rem;
            font-weight: 600;
            line-height: 1.25;
        }}
        .featured-preview {{
            width: min(100%, 670px);
            justify-self: end;
            align-self: start;
            border: 1px solid var(--border);
            border-radius: 10px;
            background:
                radial-gradient(circle at 55% 45%, rgba(180, 83, 9, 0.10), transparent 48%),
                linear-gradient(145deg, rgba(255,255,255,0.98), rgba(239,246,255,0.88));
            overflow: hidden;
            min-height: 0;
        }}
        .featured-preview img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .featured-preview-fallback {{
            min-height: 230px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--muted);
            font-weight: 700;
        }}
        .featured-lineage-preview {{
            position: relative;
            box-sizing: border-box;
            width: 100%;
            max-width: 100%;
            min-height: 0;
            height: fit-content;
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 12px;
            border-radius: 14px;
            overflow: hidden;
            container-type: inline-size;
        }}
        .featured-lineage-header {{
            position: relative;
            z-index: 4;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .65rem;
            min-height: 20px;
            margin-bottom: 0;
        }}
        .featured-lineage-header span {{
            color: var(--data-blue);
            font-size: .69rem;
            font-weight: 850;
            letter-spacing: .09em;
            text-transform: uppercase;
        }}
        .featured-lineage-header small {{
            display: inline-flex;
            align-items: center;
            gap: .38rem;
            color: var(--muted);
            font-size: .64rem;
            font-weight: 700;
            white-space: nowrap;
        }}
        .featured-lineage-header small span {{
            width: .375rem;
            height: .375rem;
            border-radius: 999px;
            background: var(--data-green);
            box-shadow: 0 0 0 3px rgba(16, 185, 129, .10);
        }}
        .featured-lineage-canvas {{
            position: relative;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: start;
            gap: 10px;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            min-height: 0;
            height: auto;
            isolation: isolate;
            overflow: visible;
        }}
        .featured-lineage-stage-headings {{
            display: grid;
            grid-template-columns: minmax(104px, .9fr) minmax(126px, 1fr) minmax(152px, 1.18fr);
            gap: clamp(1rem, 2.8vw, 2rem);
            width: 100%;
            color: var(--muted);
            font-size: .58rem;
            font-weight: 850;
            letter-spacing: .09em;
            text-transform: uppercase;
            line-height: 1;
            padding: 0 .18rem;
        }}
        .featured-lineage-group {{
            box-sizing: border-box;
            width: 100%;
            height: auto;
            min-height: 0;
            padding: 10px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: linear-gradient(160deg, color-mix(in srgb, var(--surface) 70%, transparent), color-mix(in srgb, var(--surface) 45%, transparent));
        }}
        .featured-lineage-branch-title {{
            display: block;
            color: var(--data-blue);
            font-size: .62rem;
            font-weight: 850;
            letter-spacing: .085em;
            line-height: 1;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        .featured-lineage-graph {{
            position: relative;
            display: grid;
            grid-template-columns: minmax(104px, .9fr) minmax(126px, 1fr) minmax(152px, 1.18fr);
            align-items: center;
            gap: clamp(1rem, 2.8vw, 2rem);
            width: 100%;
            min-height: 0;
            overflow: visible;
        }}
        .featured-lineage-column {{
            position: relative;
            z-index: 2;
            display: grid;
            gap: 8px;
            min-width: 0;
        }}
        .featured-lineage-sources,
        .featured-lineage-intermediate {{
            align-content: center;
        }}
        .featured-lineage-marts {{
            grid-template-columns: minmax(0, 1fr);
            gap: 7px;
        }}
        .featured-lineage-marts-single {{
            grid-template-columns: minmax(0, 1fr);
            align-content: center;
        }}
        .featured-lineage-node {{
            position: relative;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            min-height: 42px;
            padding: 7px 9px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface);
            color: var(--text);
            box-shadow: 0 4px 10px rgba(15, 23, 42, .05);
            transition: transform .16s ease, box-shadow .16s ease;
            animation: featured-lineage-node-idle 8s ease-in-out infinite;
        }}
        .featured-lineage-node[data-tooltip]:hover,
        .featured-lineage-node[data-tooltip]:focus-visible {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(15, 23, 42, .1);
        }}
        .featured-lineage-model-name {{
            min-width: 0;
            color: var(--text);
            font-size: clamp(0.66rem, 0.18vw + 0.61rem, 0.75rem);
            font-weight: 750;
            line-height: 1.12;
            text-align: center;
            overflow-wrap: break-word;
            word-break: normal;
            hyphens: none;
        }}
        .featured-lineage-source-a,
        .featured-lineage-source-b {{
            animation-name: featured-lineage-source-activation;
        }}
        .featured-lineage-int {{
            overflow: hidden;
            animation-name: featured-lineage-int-activation;
        }}
        .featured-lineage-int::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(100deg, transparent 20%, rgba(180, 83, 9, .18) 48%, transparent 74%);
            opacity: 0;
            transform: translateX(-120%);
            animation: featured-lineage-int-shimmer 8s ease-in-out infinite;
            pointer-events: none;
        }}
        .featured-lineage-mart-1 {{ animation-name: featured-lineage-mart-activation-1; }}
        .featured-lineage-mart-2 {{ animation-name: featured-lineage-mart-activation-2; }}
        .featured-lineage-mart-3 {{ animation-name: featured-lineage-mart-activation-3; }}
        .featured-lineage-mart-4 {{ animation-name: featured-lineage-mart-activation-4; }}
        .featured-lineage-group-skill .featured-lineage-node,
        .featured-lineage-group-skill .featured-lineage-int::after,
        .featured-lineage-group-skill .featured-lineage-link,
        .featured-lineage-group-skill .featured-lineage-pulse {{
            animation-delay: 1s;
        }}
        .featured-lineage-node-source {{
            color: var(--muted);
            border-color: var(--border);
            background: var(--surface);
        }}
        .featured-lineage-node-intermediate {{
            color: var(--data-blue);
            border-color: color-mix(in srgb, var(--data-blue) 28%, transparent);
            background: color-mix(in srgb, var(--data-blue) 6%, var(--surface));
        }}
        .featured-lineage-node-mart {{
            color: color-mix(in srgb, var(--data-green) 70%, var(--text));
            border-color: color-mix(in srgb, var(--data-green) 26%, transparent);
            background: color-mix(in srgb, var(--data-green) 7%, var(--surface));
        }}
        .featured-lineage-node[data-tooltip] {{
            cursor: pointer;
        }}
        .featured-lineage-node[data-tooltip]::after {{
            content: attr(data-tooltip);
            position: absolute;
            left: 50%;
            top: calc(100% + 8px);
            z-index: 30;
            width: max-content;
            max-width: 180px;
            padding: .45rem .6rem;
            border-radius: 9px;
            background: var(--text);
            color: var(--surface);
            font-size: .64rem;
            font-weight: 600;
            line-height: 1.35;
            text-align: left;
            opacity: 0;
            transform: translate(-50%, -4px);
            transition: opacity .16s ease, transform .16s ease;
            pointer-events: none;
            box-shadow: 0 10px 22px rgba(15, 23, 42, .2);
        }}
        .featured-lineage-node[data-tooltip]:hover::after,
        .featured-lineage-node[data-tooltip]:focus-visible::after {{
            opacity: 1;
            transform: translate(-50%, 0);
        }}
        .featured-lineage-node[data-tooltip]:focus-visible {{
            outline: 2px solid var(--accent);
            outline-offset: 2px;
        }}
        .featured-lineage-links {{
            position: absolute;
            inset: 0;
            z-index: 1;
            width: 100%;
            height: 100%;
            overflow: visible;
            pointer-events: none;
        }}
        .featured-lineage-links marker path {{
            fill: rgba(180, 83, 9, .58);
        }}
        .featured-lineage-link {{
            fill: none;
            stroke: var(--border);
            stroke-width: 1.2;
            stroke-linecap: round;
            stroke-linejoin: round;
            marker-end: url(#featuredLineageArrow);
            vector-effect: non-scaling-stroke;
        }}
        .featured-lineage-energy {{
            fill: none;
            stroke: var(--data-cyan);
            stroke-width: 1.6;
            stroke-linecap: round;
            stroke-dasharray: 100;
            vector-effect: non-scaling-stroke;
            filter: drop-shadow(0 0 3px color-mix(in srgb, var(--data-cyan) 70%, transparent));
        }}
        .featured-lineage-energy-mart {{
            stroke: color-mix(in srgb, var(--data-cyan) 55%, var(--data-green) 45%);
        }}
        .featured-lineage-pulse {{
            fill: var(--data-cyan);
            stroke: #FFFFFF;
            stroke-width: .8;
            filter: drop-shadow(0 0 3px color-mix(in srgb, var(--data-cyan) 70%, transparent));
            opacity: 0;
            animation: featured-lineage-pulse-visibility 8s ease-in-out infinite;
        }}
        .featured-lineage-source-pulse {{
            fill: var(--data-cyan);
        }}
        .featured-lineage-merge-pulse {{
            fill: var(--data-cyan);
            animation-name: featured-lineage-merge-visibility;
        }}
        .featured-lineage-output-pulse,
        .featured-lineage-mart-pulse {{
            fill: var(--data-cyan);
            animation-name: featured-lineage-output-visibility;
        }}
        .featured-lineage-mart-pulse-1 {{ animation-delay: 0s; }}
        .featured-lineage-mart-pulse-2 {{ animation-delay: .12s; }}
        .featured-lineage-mart-pulse-3 {{ animation-delay: .24s; }}
        .featured-lineage-mart-pulse-4 {{ animation-delay: .36s; }}
        .featured-lineage-group-skill .featured-lineage-mart-pulse-1 {{
            animation-delay: 1s;
        }}
        .featured-lineage-group-skill .featured-lineage-mart-pulse-2 {{ animation-delay: 1.12s; }}
        .featured-lineage-group-skill .featured-lineage-mart-pulse-3 {{ animation-delay: 1.24s; }}
        .featured-lineage-group-skill .featured-lineage-mart-pulse-4 {{ animation-delay: 1.36s; }}
        @keyframes featured-lineage-source-activation {{
            0%, 7%, 25%, 100% {{ border-color: rgba(148, 163, 184, .34); box-shadow: 0 3px 8px rgba(15, 23, 42, .035); }}
            8%, 22% {{ border-color: rgba(180, 83, 9, .48); box-shadow: 0 0 0 3px rgba(180, 83, 9, .08); }}
        }}
        @keyframes featured-lineage-int-activation {{
            0%, 22%, 36%, 100% {{ border-color: rgba(180, 83, 9, .28); background: rgba(239, 246, 255, .96); box-shadow: 0 3px 8px rgba(15, 23, 42, .035); }}
            24%, 34% {{ border-color: rgba(180, 83, 9, .62); background: rgba(219, 234, 254, .98); box-shadow: 0 0 0 3px rgba(180, 83, 9, .11); }}
        }}
        @keyframes featured-lineage-int-shimmer {{
            0%, 23%, 35%, 100% {{ opacity: 0; transform: translateX(-120%); }}
            26% {{ opacity: .85; }}
            33% {{ opacity: 0; transform: translateX(120%); }}
        }}
        @keyframes featured-lineage-mart-activation-1 {{
            0%, 51%, 68%, 100% {{ border-color: color-mix(in srgb, var(--data-green) 26%, transparent); background: color-mix(in srgb, var(--data-green) 7%, var(--surface)); }}
            54%, 64% {{ border-color: color-mix(in srgb, var(--data-green) 64%, transparent); background: color-mix(in srgb, var(--data-green) 16%, var(--surface)); }}
        }}
        @keyframes featured-lineage-mart-activation-2 {{
            0%, 53%, 70%, 100% {{ border-color: color-mix(in srgb, var(--data-green) 26%, transparent); background: color-mix(in srgb, var(--data-green) 7%, var(--surface)); }}
            56%, 66% {{ border-color: color-mix(in srgb, var(--data-green) 64%, transparent); background: color-mix(in srgb, var(--data-green) 16%, var(--surface)); }}
        }}
        @keyframes featured-lineage-mart-activation-3 {{
            0%, 55%, 72%, 100% {{ border-color: color-mix(in srgb, var(--data-green) 26%, transparent); background: color-mix(in srgb, var(--data-green) 7%, var(--surface)); }}
            58%, 68% {{ border-color: color-mix(in srgb, var(--data-green) 64%, transparent); background: color-mix(in srgb, var(--data-green) 16%, var(--surface)); }}
        }}
        @keyframes featured-lineage-mart-activation-4 {{
            0%, 57%, 74%, 100% {{ border-color: color-mix(in srgb, var(--data-green) 26%, transparent); background: color-mix(in srgb, var(--data-green) 7%, var(--surface)); }}
            60%, 70% {{ border-color: color-mix(in srgb, var(--data-green) 64%, transparent); background: color-mix(in srgb, var(--data-green) 16%, var(--surface)); }}
        }}
        @keyframes featured-lineage-path-activation {{
            0%, 7%, 72%, 100% {{ opacity: .72; }}
            10%, 64% {{ opacity: 1; }}
        }}
        @keyframes featured-lineage-pulse-visibility {{
            0%, 7%, 25%, 100% {{ opacity: 0; }}
            9%, 22% {{ opacity: .95; }}
        }}
        @keyframes featured-lineage-merge-visibility {{
            0%, 22%, 33%, 100% {{ opacity: 0; }}
            24%, 31% {{ opacity: 1; }}
        }}
        @keyframes featured-lineage-output-visibility {{
            0%, 37%, 68%, 100% {{ opacity: 0; }}
            40%, 64% {{ opacity: .95; }}
        }}
        @container (max-width: 319px) {{
            .featured-lineage-canvas {{
                gap: 9px;
            }}
            .featured-lineage-stage-headings {{
                grid-template-columns: 1fr;
                gap: 5px;
            }}
            .featured-lineage-stage-headings span:not(:first-child) {{
                display: none;
            }}
            .featured-lineage-group {{
                padding: 9px;
            }}
            .featured-lineage-graph {{
                display: grid;
                grid-template-columns: 1fr;
                align-items: center;
                gap: 18px;
            }}
            .featured-lineage-column {{
                grid-template-columns: 1fr;
                gap: 7px;
            }}
            .featured-lineage-marts {{
                grid-template-columns: 1fr;
            }}
            .featured-lineage-links {{
                display: none;
            }}
            .featured-lineage-sources::after,
            .featured-lineage-intermediate::after {{
                content: "";
                justify-self: center;
                width: 2px;
                height: 14px;
                margin: 2px 0 -2px;
                border-radius: 999px;
                background: linear-gradient(180deg, rgba(180, 83, 9, .34), rgba(30, 58, 95, .38));
            }}
            .featured-lineage-sources::before,
            .featured-lineage-intermediate::before {{
                content: "";
                display: none;
            }}
            .featured-lineage-node {{
                min-height: 42px;
                padding: 6px 8px;
            }}
            .featured-lineage-model-name {{
                font-size: clamp(.66rem, 0.35vw + .58rem, .78rem);
            }}
        }}
        @container (max-width: 479px) {{
            .featured-lineage-header {{
                align-items: flex-start;
                flex-direction: column;
                gap: .15rem;
            }}
            .featured-lineage-canvas {{
                gap: .62rem;
            }}
            .featured-lineage-stage-headings,
            .featured-lineage-graph {{
                grid-template-columns: minmax(78px, .82fr) minmax(106px, 1fr) minmax(116px, 1.08fr);
                gap: .85rem;
            }}
            .featured-lineage-marts {{
                grid-template-columns: minmax(0, 1fr);
            }}
            .featured-lineage-group {{
                padding: .52rem;
            }}
            .featured-lineage-node {{
                min-height: 42px;
                padding: 7px 8px;
            }}
        }}
        .home-section {{
            margin: 1.55rem 0;
        }}
        .home-about-section {{
            margin-top: 2.25rem;
        }}
        .home-section-copy {{
            color: var(--text-2);
            max-width: 720px;
            line-height: 1.65;
            margin: .6rem 0 0;
        }}
        .home-about-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(0, .75fr);
            gap: .85rem;
            margin-top: 1rem;
            overflow: visible;
        }}
        .home-skills-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .7rem;
            margin-top: .8rem;
            overflow: visible;
        }}
        .home-about-card,
        .home-skill-card {{
            min-height: 126px;
        }}
        .home-skill-card {{
            border-top-width: 3px;
        }}
        .home-skill-card .section-title::before {{
            content: "";
            display: inline-block;
            width: .48rem;
            height: .48rem;
            border-radius: 999px;
            margin-right: .42rem;
            vertical-align: .06rem;
            background: var(--data-blue);
        }}
        .home-skill-card-1 {{
            border-top-color: rgba(180, 83, 9, .42);
        }}
        .home-skill-card-1 .section-title::before {{
            background: var(--data-blue);
        }}
        .home-skill-card-2 {{
            border-top-color: rgba(30, 58, 95, .42);
        }}
        .home-skill-card-2 .section-title::before {{
            background: var(--data-cyan);
        }}
        .home-skill-card-3 {{
            border-top-color: rgba(79, 70, 229, .42);
        }}
        .home-skill-card-3 .section-title::before {{
            background: var(--data-indigo);
        }}
        .home-skill-card-4 {{
            border-top-color: rgba(51, 65, 85, .34);
        }}
        .home-skill-card-4 .section-title::before {{
            background: #475569;
        }}
        .home-skill-badge-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: .38rem;
            margin-top: .58rem;
        }}
        .home-skill-badge {{
            display: inline-flex;
            align-items: center;
            max-width: 100%;
            border: 1px solid var(--border);
            background: var(--tag-bg);
            color: var(--tag-text);
            border-radius: 999px;
            padding: .36rem .58rem;
            font-size: .78rem;
            font-weight: 600;
            line-height: 1.25;
            overflow-wrap: anywhere;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .data-command-hero .portfolio-button:hover,
            .data-command-hero .portfolio-button:focus-visible {{
                transform: translateY(-2px);
                box-shadow: 0 10px 24px rgba(180, 83, 9, .13);
            }}
            .data-command-hero .portfolio-button-primary:hover span,
            .data-command-hero .portfolio-button-primary:focus-visible span {{
                transform: translateX(.18rem);
            }}
            .hero-skill-node:hover {{
                transform: translateY(-2px);
                border-color: var(--accent);
                box-shadow: 0 10px 22px color-mix(in srgb, var(--accent) 16%, transparent);
            }}
            .hero-skill-node:hover .hero-skill-tooltip {{
                opacity: 1;
                transform: translate(-50%, 0);
            }}
            .hero-profile-card:hover {{
                transform: translateY(-3px);
                border-color: rgba(180, 83, 9, 0.42);
                box-shadow: 0 20px 44px rgba(180, 83, 9, 0.15);
            }}
            .home-profile-info-card:hover,
            .home-profile-info-card:focus-within {{
                transform: translateY(-3px);
                border-color: rgba(180, 83, 9, 0.50);
                box-shadow: 0 18px 38px rgba(180, 83, 9, 0.17);
            }}
            .home-profile-info-card:hover .home-profile-info-name,
            .home-profile-info-card:focus-within .home-profile-info-name {{
                color: var(--accent);
            }}
            .home-profile-info-card:hover .home-profile-info-status span,
            .home-profile-info-card:focus-within .home-profile-info-status span {{
                box-shadow: 0 0 0 4px color-mix(in srgb, var(--positive) 24%, transparent), 0 0 14px color-mix(in srgb, var(--positive) 45%, transparent);
            }}
        }}
        .pipeline-step-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .85rem;
            margin-top: 1rem;
            overflow: visible;
        }}
        .pipeline-step-card {{
            padding: 1rem;
            min-height: 150px;
        }}
        .pipeline-step-name {{
            color: var(--text);
            font-size: 1rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: .45rem;
        }}
        .contact-cta {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            align-items: center;
            gap: 1.2rem;
            padding: 1.25rem;
            margin: 2rem 0 1rem;
        }}
        .home-contact-cta {{
            padding: .85rem 1rem;
            margin: 1.15rem 0 .5rem;
        }}
        .home-contact-cta p {{
            margin: 0;
            font-size: .98rem;
            line-height: 1.45;
        }}
        .home-contact-cta .contact-cta-actions {{
            margin-top: 0;
        }}
        .project-overview-header {{
            margin: .25rem 0 1.85rem;
            max-width: 920px;
        }}
        .project-overview-badges {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: .5rem;
            margin-bottom: 1rem;
        }}
        .project-verified-badge,
        .project-scale-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            min-height: 30px;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: .76rem;
            font-weight: 750;
            line-height: 1.1;
        }}
        .project-verified-badge {{
            border: 1px solid rgba(16, 185, 129, 0.24);
            background: rgba(16, 185, 129, 0.08);
            color: #047857;
        }}
        .project-verified-badge span {{
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #10B981;
        }}
        .project-scale-badge {{
            border: 1px solid rgba(180, 83, 9, 0.20);
            background: rgba(239, 246, 255, 0.82);
            color: var(--data-blue);
        }}
        .project-overview-header h1 {{
            color: var(--text);
            font-size: clamp(2rem, 5vw, 3.7rem);
            line-height: 1.02;
            font-weight: 760;
            margin: 0;
        }}
        .project-overview-header p {{
            color: var(--text-2);
            max-width: 760px;
            font-size: 1.02rem;
            line-height: 1.65;
            margin: 1.05rem 0 0;
        }}
        .project-tech-stack {{
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 1rem;
        }}
        .project-tech-pill {{
            display: inline-flex;
            align-items: center;
            padding: 5px 9px;
            border: 1px solid rgba(180, 83, 9, 0.16);
            border-radius: 999px;
            background: rgba(239, 246, 255, 0.68);
            color: var(--data-blue);
            font-size: .78rem;
            font-weight: 650;
            line-height: 1.15;
        }}
        .project-header-actions {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 12px;
            margin-top: 1rem;
        }}
        .project-header-secondary-action {{
            background: transparent;
        }}
        .project-evidence-compact {{
            display: inline-grid;
            grid-template-columns: repeat(2, auto);
            align-items: center;
            gap: 28px;
            margin-top: 1.5rem;
            padding: 12px 16px;
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.82);
        }}
        .project-evidence-item {{
            display: flex;
            align-items: baseline;
            gap: 7px;
            min-width: 0;
        }}
        .project-evidence-item strong {{
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.1;
        }}
        .project-evidence-item span {{
            color: var(--muted);
            font-size: .78rem;
            font-weight: 700;
            white-space: nowrap;
        }}
        .project-overview-architecture-link {{
            display: inline-flex;
            align-items: center;
            color: var(--data-blue);
            font-size: .9rem;
            font-weight: 750;
            text-decoration: none;
            width: fit-content;
            margin: .25rem 0 .95rem;
        }}
        .project-overview-architecture-link:hover {{
            color: var(--accent-hover);
            text-decoration: underline;
        }}
        .pipeline-info-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .75rem;
            align-items: stretch;
            margin-top: .85rem;
        }}
        .pipeline-info-grid .pipeline-card {{
            position: relative;
            height: auto;
            min-height: 0;
            margin: 0;
            padding: .9rem .95rem;
            border-top: 0;
            border-left: 3px solid rgba(180, 83, 9, .34);
        }}
        .pipeline-info-grid .pipeline-card::after {{
            content: "";
            position: absolute;
            right: -.53rem;
            top: 50%;
            width: .58rem;
            height: .58rem;
            opacity: .45;
            pointer-events: none;
            border-top: 2px solid rgba(180, 83, 9, .35);
            border-right: 2px solid rgba(180, 83, 9, .35);
            background: transparent;
            transform: translateY(-50%) rotate(45deg);
        }}
        .pipeline-info-grid .pipeline-card:last-child::after {{
            display: none;
        }}
        .pipeline-info-card-heading {{
            display: flex;
            align-items: center;
            gap: .55rem;
            margin-bottom: .5rem;
        }}
        .pipeline-info-icon {{
            display: grid;
            place-items: center;
            width: 1.8rem;
            height: 1.8rem;
            flex: 0 0 1.8rem;
            border-radius: 999px;
            color: var(--data-blue);
            background: rgba(239, 246, 255, .92);
            border: 1px solid rgba(180, 83, 9, .16);
            font-size: .72rem;
            font-weight: 850;
        }}
        .pipeline-info-card-heading small {{
            display: block;
            color: var(--data-blue);
            font-size: .6rem;
            font-weight: 850;
            letter-spacing: .09em;
            line-height: 1;
        }}
        .pipeline-info-card-heading strong {{
            display: block;
            margin-top: .18rem;
            color: var(--text);
            font-size: .92rem;
            line-height: 1.15;
        }}
        .pipeline-info-grid .section-copy {{
            font-size: .86rem;
            line-height: 1.48;
        }}
        .contact-resume-strip {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            align-items: center;
            gap: 1rem;
            height: auto;
            padding: .8rem 1rem;
            margin-top: 1rem;
            min-height: 0;
        }}
        .contact-hover-card.contact-resume-strip {{
            min-height: 0;
            height: auto;
        }}
        .contact-resume-strip .section-copy {{
            font-size: .88rem;
            line-height: 1.4;
        }}
        .contact-resume-strip .contact-card-action {{
            margin-top: 0;
            white-space: nowrap;
        }}

        .section-card, .dataset-card, .challenge-panel, .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
        }}
        .project-card, .timeline-card {{
            display: block;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
            padding: 1rem;
            margin: .7rem 0 1rem;
            text-decoration: none;
            color: var(--text);
            transition: background-color 180ms ease, border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
        }}
        .project-card {{
            min-height: 360px;
        }}
        .project-card-featured {{
            max-width: 860px;
            min-height: 0;
            margin-left: auto;
            margin-right: auto;
        }}
        .project-card:hover {{
            border-color: var(--accent);
            background: var(--surface-elevated);
            transform: translateY(-1px);
        }}
        .project-visual {{
            height: 118px;
            border-radius: 10px;
            border: 1px solid var(--border);
            background:
                linear-gradient(135deg, var(--tag-bg), transparent),
                repeating-linear-gradient(90deg, transparent 0 22px, color-mix(in srgb, var(--border) 70%, transparent) 22px 23px);
            color: var(--tag-text);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-bottom: .8rem;
        }}
        .project-pipeline-banner {{
            position: relative;
            align-items: stretch;
            justify-content: stretch;
            padding: .72rem .8rem;
            overflow: hidden;
            background:
                radial-gradient(circle at 50% 45%, rgba(180, 83, 9, 0.13), transparent 28%),
                linear-gradient(135deg, rgba(239, 246, 255, 0.98), rgba(255, 255, 255, 0.88)),
                repeating-linear-gradient(90deg, transparent 0 22px, rgba(147, 197, 253, 0.18) 22px 23px);
        }}
        .project-pipeline-track {{
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(4.5rem, 1fr) minmax(1rem, .5fr) minmax(4.9rem, 1fr) minmax(1rem, .5fr) minmax(5.4rem, 1.12fr) minmax(1rem, .5fr) minmax(4.9rem, 1fr) minmax(1rem, .5fr) minmax(4.8rem, 1fr);
            align-items: center;
            width: 100%;
            height: 100%;
            gap: .28rem;
        }}
        .project-pipeline-stage {{
            position: relative;
            z-index: 2;
            display: grid;
            justify-items: center;
            align-content: center;
            gap: .12rem;
            min-width: 0;
            min-height: 4.45rem;
            padding: .42rem .34rem;
            border: 1px solid rgba(180, 83, 9, 0.18);
            border-radius: 9px;
            background: rgba(255, 255, 255, 0.78);
            color: var(--text);
            opacity: .78;
            transform: none;
            animation: project-pipeline-stage-pulse 8s ease-in-out infinite;
            box-shadow: 0 5px 14px rgba(15, 23, 42, 0.06);
        }}
        .project-pipeline-stage-1 {{ animation-delay: 0s; }}
        .project-pipeline-stage-2 {{ animation-delay: 1.45s; }}
        .project-pipeline-stage-3 {{ animation-delay: 2.9s; }}
        .project-pipeline-stage-4 {{ animation-delay: 4.35s; }}
        .project-pipeline-stage-5 {{ animation-delay: 5.8s; }}
        .project-pipeline-icon {{
            width: 1.22rem;
            height: 1.22rem;
            fill: none;
            stroke: var(--accent);
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .project-pipeline-label {{
            max-width: 100%;
            color: var(--text);
            font-size: .68rem;
            font-weight: 800;
            line-height: 1.05;
            text-align: center;
            white-space: normal;
        }}
        .project-pipeline-detail {{
            max-width: 100%;
            color: var(--muted);
            font-size: .55rem;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: normal;
        }}
        .project-warehouse-stage {{
            min-height: 5rem;
            border-color: rgba(180, 83, 9, 0.32);
            background:
                radial-gradient(circle at 50% 36%, rgba(180, 83, 9, 0.18), transparent 55%),
                rgba(255, 255, 255, 0.86);
            animation-name: project-pipeline-warehouse-pulse;
        }}
        .project-warehouse-stage .project-pipeline-icon {{
            width: 1.42rem;
            height: 1.42rem;
        }}
        .project-pipeline-connector {{
            position: relative;
            height: 2px;
            min-width: 0;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(180, 83, 9, 0.18), rgba(180, 83, 9, 0.5));
            overflow: hidden;
        }}
        .project-pipeline-connector::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(180, 83, 9, 0.78), transparent);
            animation: project-pipeline-connector-flow 2.8s linear infinite;
        }}
        .project-pipeline-particle {{
            position: absolute;
            z-index: 1;
            top: 50%;
            left: 3.2%;
            width: .46rem;
            height: .46rem;
            border-radius: 999px;
            background: rgba(180, 83, 9, 0.92);
            box-shadow: 0 0 11px rgba(180, 83, 9, 0.42);
            transform: translate3d(0, -50%, 0);
            animation: project-pipeline-particle-flow 8s cubic-bezier(0.45, 0, 0.2, 1) infinite;
        }}
        .project-pipeline-particle-2 {{
            animation-delay: 2.65s;
            width: .38rem;
            height: .38rem;
            opacity: .82;
        }}
        .project-pipeline-particle-3 {{
            animation-delay: 5.25s;
            width: .34rem;
            height: .34rem;
            opacity: .72;
        }}
        @keyframes project-pipeline-particle-flow {{
            0% {{ left: 3.2%; opacity: 0; transform: translate3d(0, -50%, 0); }}
            7%, 82% {{ opacity: 1; }}
            95%, 100% {{ left: 96.8%; opacity: 0; transform: translate3d(-100%, -50%, 0); }}
        }}
        @keyframes project-pipeline-stage-pulse {{
            0%, 16%, 100% {{
                opacity: .78;
                transform: none;
                border-color: rgba(180, 83, 9, 0.18);
                box-shadow: 0 5px 14px rgba(15, 23, 42, 0.06);
            }}
            7%, 11% {{
                opacity: 1;
                transform: translateY(-2px);
                border-color: rgba(180, 83, 9, 0.50);
                box-shadow: 0 8px 22px rgba(180, 83, 9, 0.16);
            }}
        }}
        @keyframes project-pipeline-warehouse-pulse {{
            0%, 16%, 100% {{
                opacity: .82;
                transform: none;
                border-color: rgba(180, 83, 9, 0.32);
                box-shadow: 0 5px 14px rgba(15, 23, 42, 0.06);
            }}
            7%, 11% {{
                opacity: 1;
                transform: translateY(-2px);
                border-color: rgba(180, 83, 9, 0.56);
                box-shadow: 0 8px 24px rgba(180, 83, 9, 0.20);
            }}
        }}
        @keyframes project-pipeline-connector-flow {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(100%); }}
        }}
        @media (max-width: 680px) {{
            .project-pipeline-banner {{
                padding: .58rem .55rem;
            }}
            .project-pipeline-track {{
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: .18rem;
            }}
            .project-pipeline-stage {{
                min-height: 4rem;
                padding: .32rem .18rem;
                border-radius: 8px;
            }}
            .project-warehouse-stage {{
                min-height: 4.25rem;
            }}
            .project-pipeline-icon {{
                width: 1rem;
                height: 1rem;
            }}
            .project-warehouse-stage .project-pipeline-icon {{
                width: 1.14rem;
                height: 1.14rem;
            }}
            .project-pipeline-label {{
                font-size: .58rem;
            }}
            .project-pipeline-detail {{
                display: none;
            }}
            .project-pipeline-connector-1 {{
                position: absolute;
                z-index: 1;
                left: 8%;
                right: 8%;
                top: 50%;
                width: auto;
            }}
            .project-pipeline-connector-2,
            .project-pipeline-connector-3,
            .project-pipeline-connector-4 {{
                display: none;
            }}
            .project-pipeline-particle {{
                width: .34rem;
                height: .34rem;
                box-shadow: 0 0 7px rgba(180, 83, 9, 0.32);
            }}
            .project-card-featured .project-actions {{
                flex-direction: column;
            }}
            .project-card-featured .project-action {{
                width: 100%;
            }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .project-pipeline-stage,
            .project-warehouse-stage {{
                opacity: 1;
                transform: none;
                animation: none !important;
            }}
            .project-pipeline-connector::after,
            .project-pipeline-particle {{
                animation: none !important;
            }}
            .project-pipeline-particle {{
                display: none;
            }}
        }}
        .project-title {{
            color: var(--text);
            font-weight: 700;
            font-size: 1.12rem;
            line-height: 1.25;
            margin: .22rem 0 .42rem;
        }}
        .project-meta, .timeline-date {{
            color: var(--muted);
            font-weight: 600;
            font-size: .82rem;
            text-transform: uppercase;
            letter-spacing: .02em;
        }}
        .project-metric {{
            color: var(--accent-bright);
            font-weight: 700;
            margin: .65rem 0 .4rem;
        }}
        .project-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin-top: 1rem;
        }}
        .project-action {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.45rem;
            padding: .58rem .85rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            font-weight: 600;
            line-height: 1.15;
            white-space: nowrap;
            text-decoration: none;
            flex: 1 1 12rem;
        }}
        .project-action-primary {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--on-accent) !important;
            box-shadow: var(--shadow-accent);
        }}
        .timeline-card ul {{
            color: var(--text-2);
            margin-top: .55rem;
            padding-left: 1.2rem;
        }}
        .about-hover-card {{
            transform-origin: center;
            outline: none;
            overflow: visible;
            margin-top: .85rem;
            margin-bottom: 1.15rem;
            transition:
                transform 220ms ease,
                border-color 220ms ease,
                background-color 220ms ease,
                box-shadow 220ms ease;
        }}
        .experience-hover-card {{
            transform-origin: center;
            outline: none;
            overflow: visible;
            margin-top: .85rem;
            margin-bottom: 1.15rem;
            transition:
                transform 230ms cubic-bezier(0.22, 1, 0.36, 1),
                border-color 230ms ease,
                background-color 230ms ease,
                box-shadow 230ms ease;
        }}
        .about-hover-card .section-title {{
            transform-origin: left center;
            transition: color 220ms ease, font-size 220ms ease, transform 220ms ease;
        }}
        .experience-hover-card .project-title {{
            transform-origin: left center;
            transition: color 230ms ease;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .about-hover-card:hover,
            .about-hover-card:focus-within {{
                transform: translateY(-3px);
                border-color: rgba(180, 83, 9, 0.45);
                background-color: rgba(239, 246, 255, 0.65);
                box-shadow: 0 12px 28px rgba(180, 83, 9, 0.14);
                position: relative;
                z-index: 2;
            }}
            .experience-hover-card:hover,
            .experience-hover-card:focus-within {{
                transform: translateY(-4px);
                border-color: rgba(180, 83, 9, 0.38);
                background-color: rgba(239, 246, 255, 0.62);
                box-shadow: 0 14px 30px rgba(180, 83, 9, 0.13);
                position: relative;
                z-index: 2;
            }}
            .about-hover-card:hover .section-title,
            .about-hover-card:focus-within .section-title {{
                color: var(--accent);
                font-size: 1.12rem;
            }}
            .experience-hover-card:hover .project-title,
            .experience-hover-card:focus-within .project-title {{
                color: var(--accent);
            }}
        }}
        @media (hover: none), (pointer: coarse), (max-width: 760px) {{
            .about-hover-card,
            .experience-hover-card {{
                transform: none;
                transition: none;
            }}
            .about-hover-card:hover,
            .about-hover-card:focus-within,
            .experience-hover-card:hover,
            .experience-hover-card:focus-within {{
                transform: none;
                border-color: var(--border);
                background-color: var(--surface);
                box-shadow: var(--shadow);
            }}
            .about-hover-card:hover .section-title,
            .about-hover-card:focus-within .section-title,
            .experience-hover-card:hover .project-title,
            .experience-hover-card:focus-within .project-title {{
                color: var(--text);
                transform: none;
            }}
            .about-hover-card:hover .section-title,
            .about-hover-card:focus-within .section-title {{
                font-size: 1.08rem;
            }}
        }}
        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: var(--border);
            border-radius: 16px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }}
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] {{
            overflow-wrap: anywhere;
        }}
        .section-card {{
            padding: 1rem 1.05rem;
            margin: .7rem 0 1rem;
            min-height: 100px;
        }}
        .section-title {{
            font-size: 1.08rem;
            color: var(--text);
            font-weight: 600;
            margin-bottom: .32rem;
            line-height: 1.25;
        }}
        .section-copy, .muted {{
            color: var(--text-2);
            line-height: 1.62;
            font-size: .96rem;
        }}
        .dataset-card {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: .95rem 1rem;
            margin: 1rem 0;
        }}
        .dataset-metrics {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .85rem;
            width: 100%;
        }}
        .dataset-value {{ color: var(--text); font-size: 1.08rem; font-weight: 700; }}
        .dataset-label {{ color: var(--muted); font-size: .8rem; margin-top: .15rem; }}

        .challenge-panel {{
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            padding: 1rem;
            margin: .75rem 0 1.1rem;
        }}
        .challenge-chip, .meta-pill, .active-chip {{
            border: 1px solid var(--border);
            background: var(--tag-bg);
            color: var(--tag-text);
            border-radius: 999px;
            font-size: .82rem;
            font-weight: 500;
            transition: background-color 160ms ease, border-color 160ms ease, color 160ms ease;
        }}
        .challenge-chip {{ padding: .42rem .7rem; }}
        .skill-card {{
            overflow: visible;
            height: auto;
        }}
        .home-card,
        .skill-card,
        .pipeline-card {{
            transform-origin: center;
            will-change: transform;
            transition:
                transform 240ms ease,
                border-color 240ms ease,
                background-color 240ms ease,
                box-shadow 240ms ease;
        }}
        .home-card .section-title,
        .skill-card .section-title,
        .pipeline-card .section-title,
        .pipeline-card strong {{
            transition: color 240ms ease;
        }}
        .job-intelligence-hover-card,
        .data-quality-hover-card,
        .home-about-card,
        .home-skill-card,
        .featured-project-card,
        .pipeline-step-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
            transform-origin: center;
            overflow: visible;
            will-change: transform;
            transition:
                transform 250ms ease,
                border-color 250ms ease,
                background-color 250ms ease,
                box-shadow 250ms ease;
        }}
        .contact-hover-card {{
            display: flex;
            flex-direction: column;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
            transform-origin: center;
            overflow: visible;
            padding: 1rem;
            margin: .7rem 0 1rem;
            min-height: 210px;
            transition:
                transform 230ms cubic-bezier(0.22, 1, 0.36, 1),
                border-color 230ms ease,
                background-color 230ms ease,
                box-shadow 230ms ease;
        }}
        .data-quality-hover-card {{
            padding: 1rem;
            margin: .7rem 0 1rem;
        }}
        .quality-summary-panel,
        .quality-limitation-callout {{
            position: relative;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
            padding: 1rem;
            margin: .85rem 0 1rem;
        }}
        .quality-summary-grid {{
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .65rem;
            margin-top: .4rem;
        }}
        .quality-summary-panel::after {{
            content: "";
            position: absolute;
            right: 1rem;
            top: .85rem;
            width: 7rem;
            height: 4rem;
            opacity: .05;
            pointer-events: none;
            background:
                radial-gradient(circle, var(--data-green) 0 2px, transparent 3px),
                linear-gradient(90deg, transparent 47%, var(--data-green) 48% 52%, transparent 53%);
            background-size: 2rem 2rem, 100% 100%;
        }}
        .quality-summary-item {{
            min-width: 0;
            border: 1px solid rgba(180, 83, 9, .16);
            border-radius: 10px;
            background: rgba(239, 246, 255, .52);
            padding: .65rem .75rem;
        }}
        .quality-summary-item-1,
        .quality-summary-item-2,
        .quality-summary-item-3,
        .quality-summary-item-4,
        .quality-summary-item-6 {{
            border-color: rgba(16, 185, 129, .24);
            background: rgba(16, 185, 129, .06);
        }}
        .quality-summary-item-5 {{
            border-color: rgba(245, 158, 11, .28);
            background: var(--data-amber-soft);
        }}
        .quality-summary-item span {{
            display: block;
            color: var(--muted);
            font-size: .74rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: .035em;
            line-height: 1.2;
        }}
        .quality-summary-item strong {{
            display: block;
            color: var(--text);
            font-size: .92rem;
            line-height: 1.25;
            margin-top: .22rem;
        }}
        .quality-limitation-callout {{
            border-color: rgba(245, 158, 11, .38);
            border-left: 4px solid var(--data-amber);
            background:
                linear-gradient(135deg, rgba(245, 158, 11, .10), rgba(255, 255, 255, .94));
        }}
        .quality-limitation-callout .section-title::before {{
            content: "";
            display: inline-block;
            width: .52rem;
            height: .52rem;
            border-radius: 999px;
            margin-right: .42rem;
            background: var(--data-amber);
            box-shadow: 0 0 0 3px var(--data-amber-soft);
            vertical-align: .04rem;
        }}
        .quality-limitation-callout p {{
            color: var(--text-2);
            margin: .35rem 0 0;
            line-height: 1.45;
        }}
        .data-quality-detail {{
            padding: .15rem 0 .3rem;
            animation: data-quality-detail-in 220ms ease-out both;
        }}
        @keyframes data-quality-detail-in {{
            from {{ opacity: 0; transform: translateY(.25rem); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .job-intelligence-hover-card .section-title,
        .job-intelligence-hover-card strong,
        .data-quality-hover-card .section-title,
        .home-about-card .section-title,
        .home-skill-card .section-title,
        .featured-project-card h2,
        .pipeline-step-card .pipeline-step-name {{
            transition: color 250ms ease;
        }}
        .contact-hover-card .section-title {{
            transition: color 230ms ease;
        }}
        .contact-card-action {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.45rem;
            padding: .58rem .85rem;
            border-radius: 10px;
            border: 1px solid var(--accent);
            background: var(--accent);
            color: var(--on-accent) !important;
            font-weight: 600;
            line-height: 1.15;
            text-decoration: none;
            box-shadow: var(--shadow-accent);
            margin-top: auto;
        }}
        .contact-card-action-secondary {{
            background: transparent;
            color: var(--data-blue) !important;
            box-shadow: none;
            border-color: rgba(180, 83, 9, .24);
        }}
        .contact-card-action-secondary:hover,
        .contact-card-action-secondary:focus-visible {{
            background: rgba(239, 246, 255, .82);
            color: var(--data-blue-dark) !important;
            box-shadow: none;
        }}
        .quality-metric-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .7rem;
            margin: .8rem 0 .65rem;
        }}
        .quality-metric {{
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface-2);
            padding: .65rem .7rem;
        }}
        .quality-metric-label {{
            color: var(--muted);
            font-size: .78rem;
            line-height: 1.25;
        }}
        .quality-metric-value {{
            color: var(--text);
            font-size: 1.22rem;
            font-weight: 700;
            line-height: 1.2;
            margin-top: .22rem;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .home-card:hover,
            .home-card:focus-within,
            .skill-card:hover,
            .skill-card:focus-within,
            .pipeline-card:hover,
            .pipeline-card:focus-within {{
                transform: translateY(-3px);
                border-color: rgba(180, 83, 9, 0.30);
                background-color: rgba(239, 246, 255, 0.58);
                box-shadow: 0 14px 28px rgba(15, 23, 42, 0.09);
                position: relative;
                z-index: 2;
            }}
            .home-card:hover .section-title,
            .home-card:focus-within .section-title,
            .skill-card:hover .section-title,
            .skill-card:focus-within .section-title,
            .pipeline-card:hover .section-title,
            .pipeline-card:focus-within .section-title,
            .pipeline-card:hover strong,
            .pipeline-card:focus-within strong {{
                color: var(--accent);
            }}
            .job-intelligence-hover-card:hover,
            .job-intelligence-hover-card:focus-within,
            .data-quality-hover-card:hover,
            .data-quality-hover-card:focus-within,
            .home-about-card:hover,
            .home-about-card:focus-within,
            .home-skill-card:hover,
            .home-skill-card:focus-within,
            .featured-project-card:hover,
            .featured-project-card:focus-within,
            .pipeline-step-card:hover,
            .pipeline-step-card:focus-within {{
                transform: translateY(-4px);
                border-color: rgba(180, 83, 9, 0.30);
                background-color: rgba(239, 246, 255, 0.58);
                box-shadow: 0 14px 28px rgba(15, 23, 42, 0.09);
                position: relative;
                z-index: 2;
            }}
            .contact-hover-card:hover,
            .contact-hover-card:focus-within {{
                transform: translateY(-4px);
                border-color: rgba(180, 83, 9, 0.38);
                background-color: rgba(239, 246, 255, 0.62);
                box-shadow: 0 14px 30px rgba(180, 83, 9, 0.13);
                position: relative;
                z-index: 2;
            }}
            .contact-hover-card.contact-resume-strip:hover,
            .contact-hover-card.contact-resume-strip:focus-within {{
                transform: translateY(-2px);
                border-color: rgba(180, 83, 9, 0.38);
                background-color: rgba(239, 246, 255, 0.62);
                box-shadow: 0 12px 24px rgba(180, 83, 9, 0.11);
            }}
            .job-intelligence-hover-card:hover .section-title,
            .job-intelligence-hover-card:focus-within .section-title,
            .job-intelligence-hover-card:hover strong,
            .job-intelligence-hover-card:focus-within strong,
            .data-quality-hover-card:hover .section-title,
            .data-quality-hover-card:focus-within .section-title,
            .home-about-card:hover .section-title,
            .home-about-card:focus-within .section-title,
            .home-skill-card:hover .section-title,
            .home-skill-card:focus-within .section-title,
            .featured-project-card:hover h2,
            .featured-project-card:focus-within h2,
            .pipeline-step-card:hover .pipeline-step-name,
            .pipeline-step-card:focus-within .pipeline-step-name {{
                color: var(--accent);
            }}
            .contact-hover-card:hover .section-title,
            .contact-hover-card:focus-within .section-title {{
                color: var(--accent);
            }}
        }}
        @media (hover: none), (pointer: coarse), (max-width: 760px) {{
            .home-card,
            .skill-card,
            .pipeline-card,
            .job-intelligence-hover-card,
            .contact-hover-card,
            .data-quality-hover-card,
            .home-about-card,
            .home-skill-card,
            .featured-project-card,
            .pipeline-step-card {{
                transform: none;
                will-change: auto;
            }}
        }}
        .skill-chip-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: .55rem .5rem;
            align-items: flex-start;
            max-width: 100%;
            min-width: 0;
            overflow: visible;
        }}
        .skill-chip {{
            display: inline-flex;
            align-items: center;
            max-width: 100%;
            min-width: 0;
            white-space: normal;
            overflow-wrap: anywhere;
            line-height: 1.3;
            padding: .46rem .72rem;
        }}
        .meta-pill {{
            display: inline-flex;
            align-items: center;
            gap: .35rem;
            padding: .34rem .58rem;
            margin: .15rem .25rem .15rem 0;
        }}
        .active-filter-wrap {{ margin: .45rem 0 .9rem; }}
        .active-chip {{
            display: inline-block;
            max-width: 100%;
            padding: .28rem .55rem;
            margin: .12rem .18rem .12rem 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .st-key-dashboard_filter_panel {{
            display: block;
            padding: 1.25rem 1.3rem 1.1rem;
            margin: .85rem 0 .7rem;
            border: 1px solid color-mix(in srgb, var(--accent) 16%, var(--border));
            border-radius: 16px;
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 92%, var(--tag-bg)));
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.06);
        }}
        .market-filters-heading {{
            margin: 0 0 .9rem;
            line-height: 1.15;
        }}
        .st-key-market_basic_filters_grid [data-testid="stHorizontalBlock"] {{
            gap: clamp(.75rem, 1vw, 1rem);
        }}
        .st-key-market_basic_filters_grid [data-testid="stWidgetLabel"],
        .st-key-market_advanced_filters [data-testid="stWidgetLabel"] {{
            margin-bottom: .45rem;
        }}
        .st-key-market_advanced_filters {{
            margin-top: .7rem;
        }}
        .dashboard-results-status {{
            display: inline-flex;
            align-items: center;
            min-height: 2.35rem;
            color: var(--tag-text);
            background: var(--tag-bg);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: .42rem .75rem;
            font-size: .84rem;
            font-weight: 750;
            margin: .4rem 0 .75rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.045);
        }}
        .dashboard-primary-kpis {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .85rem;
            margin: .75rem 0 .75rem;
        }}
        .dashboard-primary-kpi {{
            min-width: 0;
            min-height: 116px;
            padding: 1.02rem 1.1rem;
            border: 1px solid var(--border);
            border-top: 3px solid var(--data-blue);
            border-radius: 16px;
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 94%, var(--data-blue)));
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.06);
            transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
        }}
        .dashboard-primary-kpi:hover {{
            transform: translateY(-2px);
            border-color: color-mix(in srgb, var(--data-blue) 45%, var(--border));
            box-shadow: 0 18px 38px rgba(15, 23, 42, 0.09);
        }}
        .dashboard-primary-kpi-2 {{
            border-top-color: var(--data-cyan);
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 94%, var(--data-cyan)));
        }}
        .dashboard-primary-kpi-2:hover {{
            border-color: color-mix(in srgb, var(--data-cyan) 45%, var(--border));
        }}
        .dashboard-primary-kpi-3 {{
            border-top-color: #64748B;
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 94%, #64748B));
        }}
        .dashboard-primary-kpi-3:hover {{
            border-color: color-mix(in srgb, #64748B 45%, var(--border));
        }}
        .dashboard-primary-kpi-4 {{
            border-top-color: var(--data-green);
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 94%, var(--data-green)));
        }}
        .dashboard-primary-kpi-4:hover {{
            border-color: color-mix(in srgb, var(--data-green) 45%, var(--border));
        }}
        .dashboard-kpi-label {{
            color: var(--muted);
            font-size: .78rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: .035em;
        }}
        .dashboard-kpi-value {{
            color: var(--text);
            font-size: clamp(1.35rem, 2.8vw, 1.85rem);
            font-weight: 850;
            line-height: 1.1;
            margin-top: .34rem;
            overflow-wrap: anywhere;
        }}
        .dashboard-kpi-note {{
            color: var(--muted);
            font-size: .76rem;
            line-height: 1.3;
            margin-top: .38rem;
        }}
        .dashboard-metadata-strip {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin: 0 0 1.2rem;
            padding: .72rem .95rem;
            border: 1px solid color-mix(in srgb, var(--accent) 18%, transparent);
            border-radius: 14px;
            background: linear-gradient(120deg, color-mix(in srgb, var(--accent) 7%, var(--surface)), color-mix(in srgb, var(--accent) 3%, var(--surface)));
        }}
        .dashboard-meta-item {{
            min-width: 0;
            padding: .15rem .85rem;
            border-left: 1px solid color-mix(in srgb, var(--accent) 18%, transparent);
            border-top: 3px solid transparent;
        }}
        .dashboard-meta-item-1 {{
            border-top-color: var(--data-indigo);
        }}
        .dashboard-meta-item-2 {{
            border-top-color: var(--data-amber);
        }}
        .dashboard-meta-item:first-child {{
            border-left: 0;
            padding-left: 0;
        }}
        .dashboard-meta-item span {{
            display: block;
            color: var(--muted);
            font-size: .72rem;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: .035em;
        }}
        .dashboard-meta-item strong {{
            display: block;
            color: var(--text);
            font-size: .94rem;
            line-height: 1.2;
            margin-top: .18rem;
            overflow-wrap: anywhere;
        }}
        .dashboard-methodology {{
            color: var(--text-2);
            font-size: .9rem;
            line-height: 1.55;
        }}
        .dashboard-methodology p {{
            margin: .35rem 0;
        }}
        .dashboard-methodology strong {{
            color: var(--text);
        }}
        .dashboard-compact-footer {{
            color: var(--muted);
            border-top: 1px solid var(--border);
            margin-top: 1.6rem;
            padding-top: .75rem;
            font-size: .82rem;
        }}
        .dashboard-compact-footer a {{
            color: var(--accent);
            font-weight: 750;
            text-decoration: none;
        }}
        .salary-coverage-note {{
            display: block;
            margin: .35rem 0 .85rem;
            padding: .55rem .8rem;
            border: 1px solid color-mix(in srgb, var(--warning) 30%, transparent);
            border-left: 3px solid var(--warning);
            border-radius: 8px;
            background: color-mix(in srgb, var(--warning) 8%, var(--surface));
            color: var(--text-2);
            font-size: .82rem;
            line-height: 1.45;
        }}
        .salary-coverage-note strong {{
            color: var(--text);
        }}
        .kpi-card {{
            min-height: 132px;
            padding: .95rem 1rem;
            transition: border-color .14s ease, background .14s ease, transform .14s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-1px);
            border-color: var(--accent);
            background: var(--surface-elevated);
        }}
        .kpi-icon {{
            width: 31px;
            height: 31px;
            margin-bottom: .55rem;
        }}
        .kpi-label {{
            font-size: .82rem;
            color: var(--muted);
            margin-bottom: .22rem;
            font-weight: 500;
        }}
        .kpi-value {{
            font-size: clamp(1.24rem, 2.8vw, 1.7rem);
            font-weight: 700;
            color: var(--text);
            overflow-wrap: anywhere;
            line-height: 1.2;
        }}
        .kpi-note {{
            color: var(--muted);
            font-size: .76rem;
            margin-top: .35rem;
            line-height: 1.35;
        }}

        .pipeline-architecture-shell {{
            position: relative;
            margin: .55rem 0 1.65rem;
        }}
        .pipeline-architecture-viewport {{
            position: relative;
            overflow-x: auto;
            overflow-y: hidden;
            padding: .35rem .15rem .55rem;
            scrollbar-width: thin;
            mask-image: linear-gradient(90deg, transparent 0, #000 1.2rem, #000 calc(100% - 1.2rem), transparent 100%);
        }}
        .pipeline.pipeline-architecture {{
            position: relative;
            isolation: isolate;
            display: block;
            min-width: 1180px;
            margin: 0;
            overflow: visible;
            container-type: inline-size;
        }}
        .pipeline-orchestration-band {{
            position: relative;
            display: grid;
            grid-template-columns: minmax(280px, .9fr) minmax(0, 1.1fr);
            align-items: center;
            gap: 1rem;
            min-height: 78px;
            padding: .82rem 1rem;
            margin: 0 0 .72rem;
            border: 1px solid rgba(180, 83, 9, .16);
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(239, 246, 255, .94), rgba(255, 255, 255, .96));
            box-shadow: 0 5px 14px rgba(15, 23, 42, .04);
        }}
        .pipeline-orchestration-main {{
            display: flex;
            align-items: center;
            gap: .72rem;
            min-width: 0;
        }}
        .pipeline-orchestration-icon {{
            display: grid;
            place-items: center;
            width: 2.2rem;
            height: 2.2rem;
            flex: 0 0 2.2rem;
            border-radius: 11px;
            color: var(--data-blue);
            background: rgba(219, 234, 254, .84);
            border: 1px solid rgba(180, 83, 9, .18);
        }}
        .pipeline-orchestration-icon svg {{
            width: 1.25rem;
            height: 1.25rem;
            fill: none;
            stroke: currentColor;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .pipeline-orchestration-main small {{
            display: block;
            color: var(--data-blue);
            font-size: .62rem;
            font-weight: 850;
            letter-spacing: .09em;
            line-height: 1;
        }}
        .pipeline-orchestration-main strong {{
            display: block;
            margin-top: .2rem;
            color: var(--text);
            font-size: 1rem;
            line-height: 1.15;
        }}
        .pipeline-orchestration-main em {{
            display: block;
            margin-top: .16rem;
            color: var(--text-2);
            font-size: .78rem;
            font-style: normal;
            font-weight: 600;
            line-height: 1.25;
        }}
        .pipeline-orchestration-status {{
            display: flex;
            justify-content: flex-end;
            flex-wrap: wrap;
            gap: .42rem;
            min-width: 0;
        }}
        .pipeline-orchestration-status span {{
            display: inline-flex;
            align-items: center;
            min-height: 1.65rem;
            padding: .28rem .52rem;
            border-radius: 999px;
            border: 1px solid rgba(180, 83, 9, .14);
            background: rgba(255, 255, 255, .78);
            color: var(--text-2);
            font-size: .7rem;
            font-weight: 750;
            white-space: nowrap;
        }}
        .pipeline-airflow-stem {{
            position: absolute;
            bottom: -.72rem;
            height: .72rem;
            width: 0;
            border-left: 1px dashed rgba(180, 83, 9, .34);
            pointer-events: none;
        }}
        .pipeline-airflow-stem-2 {{ left: calc((100% / 6) * 1.5); }}
        .pipeline-airflow-stem-4 {{ left: calc((100% / 6) * 3.5); }}
        .pipeline-airflow-stem-5 {{ left: calc((100% / 6) * 4.5); }}
        .pipeline-airflow-stem-6 {{ left: calc((100% / 6) * 5.5); }}
        .pipeline-stage-grid {{
            display: grid;
            grid-template-columns: repeat(6, minmax(175px, 1fr));
            gap: 12px;
        }}
        .pipeline-architecture-card {{
            position: relative;
            z-index: 2;
            display: grid;
            justify-items: start;
            align-content: start;
            min-height: 122px;
            padding: 14px 14px 13px;
            border: 1px solid rgba(148, 163, 184, .24);
            border-radius: 13px;
            background: rgba(255, 255, 255, .95);
            color: var(--text);
            text-align: left;
            box-shadow: 0 5px 14px rgba(15, 23, 42, .045);
            animation: pipeline-stage-pass 7s ease-in-out infinite;
        }}
        .pipeline-stage-icon {{
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            margin: 0 0 .45rem;
            border-radius: 10px;
            color: var(--data-blue);
            background: rgba(239, 246, 255, .96);
            border: 1px solid rgba(180, 83, 9, .18);
            transition: border-color 180ms ease, background-color 180ms ease;
        }}
        .pipeline-stage-icon svg {{
            width: 18px;
            height: 18px;
            fill: none;
            stroke: currentColor;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .pipeline-stage-number {{
            color: var(--data-blue);
            font-size: .62rem;
            font-weight: 850;
            letter-spacing: .09em;
            text-transform: uppercase;
            line-height: 1;
        }}
        .pipeline-stage-category {{
            display: block;
            margin-top: .16rem;
            color: var(--muted);
            font-size: .54rem;
            font-weight: 850;
            letter-spacing: .07em;
            line-height: 1.05;
        }}
        .pipeline-architecture-card strong {{
            display: block;
            margin-top: .32rem;
            color: var(--text);
            font-size: .88rem;
            font-weight: 800;
            line-height: 1.16;
        }}
        .pipeline-architecture-card small {{
            display: block;
            margin-top: .26rem;
            color: var(--muted);
            font-size: .72rem;
            font-weight: 600;
            line-height: 1.28;
        }}
        .pipeline-stage-status {{
            position: absolute;
            right: .65rem;
            top: .65rem;
            color: #0891B2;
            font-size: .58rem;
            font-weight: 850;
            opacity: 0;
            animation: pipeline-stage-status-pass 7s ease-in-out infinite;
        }}
        .pipeline-category-warehouse .pipeline-stage-icon,
        .pipeline-category-transform .pipeline-stage-icon {{
            color: #92400E;
            background: rgba(219, 234, 254, .92);
        }}
        .pipeline-category-validate .pipeline-stage-icon,
        .pipeline-category-serve .pipeline-stage-icon {{
            color: #0891B2;
            background: rgba(207, 250, 254, .62);
        }}
        .pipeline-stage-1 {{ animation-delay: 0s; }}
        .pipeline-stage-2 {{ animation-delay: 1.05s; }}
        .pipeline-stage-3 {{ animation-delay: 2.1s; }}
        .pipeline-stage-4 {{ animation-delay: 3.15s; }}
        .pipeline-stage-5 {{ animation-delay: 4.2s; }}
        .pipeline-stage-6 {{ animation-delay: 5.25s; }}
        .pipeline-stage-1 .pipeline-stage-status {{ animation-delay: 0s; }}
        .pipeline-stage-2 .pipeline-stage-status {{ animation-delay: 1.05s; }}
        .pipeline-stage-3 .pipeline-stage-status {{ animation-delay: 2.1s; }}
        .pipeline-stage-4 .pipeline-stage-status {{ animation-delay: 3.15s; }}
        .pipeline-stage-5 .pipeline-stage-status {{ animation-delay: 4.2s; }}
        .pipeline-stage-6 .pipeline-stage-status {{ animation-delay: 5.25s; }}
        .data-flow-lane {{
            height: 42px;
            margin-top: 16px;
            padding: 0 3px;
        }}
        .data-flow-svg {{
            display: block;
            width: 100%;
            height: 42px;
            overflow: visible;
        }}
        .data-flow-path {{
            fill: none;
            stroke: rgba(180, 83, 9, .30);
            stroke-width: 2;
            stroke-linecap: round;
        }}
        .data-flow-arrow-segments {{
            fill: none;
            stroke: url(#unused);
            stroke-width: 0;
            marker-end: url(#pipelineDataArrow);
        }}
        .data-flow-arrow-segments,
        .data-flow-stems {{
            stroke: rgba(180, 83, 9, .42);
            stroke-width: 1.4;
            fill: none;
            vector-effect: non-scaling-stroke;
        }}
        .data-flow-stems {{
            stroke-dasharray: 2 4;
            opacity: .74;
        }}
        .data-flow-svg marker path {{
            fill: rgba(30, 58, 95, .74);
        }}
        .data-packet,
        .pulse-trail,
        .data-flow-pulse {{
            transform-origin: center;
            transform-box: fill-box;
            transition: opacity .2s ease, fill .2s ease;
        }}
        .pulse-trail {{
            fill: #1e3a5f;
            stroke: none;
        }}
        .pulse-trail-1 {{
            opacity: .35;
        }}
        .pulse-trail-2 {{
            opacity: .15;
        }}
        .data-flow-pulse {{
            fill: #1e3a5f;
            stroke: #FFFFFF;
            stroke-width: 1;
            opacity: .96;
            filter: drop-shadow(0 0 4px rgba(30, 58, 95, .75));
        }}
        @keyframes pipeline-stage-pass {{
            0%, 86%, 100% {{ border-color: rgba(148, 163, 184, .24); background: rgba(255, 255, 255, .95); box-shadow: 0 5px 14px rgba(15, 23, 42, .045); }}
            5%, 13% {{ border-color: rgba(30, 58, 95, .54); background: rgba(239, 246, 255, .98); box-shadow: 0 0 0 3px rgba(30, 58, 95, .08); }}
        }}
        @keyframes pipeline-stage-status-pass {{
            0%, 4%, 15%, 100% {{ opacity: 0; }}
            6%, 12% {{ opacity: 1; }}
        }}
        .pipeline-architecture-card:hover,
        .pipeline-architecture-card:focus-within {{
            border-color: rgba(180, 83, 9, .48);
            box-shadow: 0 0 0 3px rgba(180, 83, 9, .08);
        }}
        .pipeline-architecture-card:hover .pipeline-stage-status,
        .pipeline-architecture-card:focus-within .pipeline-stage-status {{
            opacity: 1;
        }}

        .chart-card-heading {{
            background: linear-gradient(160deg, var(--surface), color-mix(in srgb, var(--surface) 95%, var(--tag-bg)));
            border: 1px solid var(--border);
            border-bottom: 0;
            border-radius: 14px 14px 0 0;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
            padding: .95rem 1.1rem .4rem;
            margin-top: .8rem;
        }}
        .st-key-market_dashboard_chart_job_title_demand,
        .st-key-market_dashboard_chart_company_activity,
        .st-key-market_dashboard_chart_salary_by_job_title,
        .st-key-market_dashboard_chart_salary_by_country,
        .st-key-market_dashboard_chart_remote_salary,
        .st-key-market_dashboard_chart_monthly_posting_trend,
        .st-key-market_dashboard_chart_monthly_growth,
        .st-key-market_dashboard_chart_technical_skill_demand,
        .st-key-market_dashboard_chart_high_salary_skills,
        .st-key-market_dashboard_chart_data_engineer_skill_demand {{
            opacity: 1;
            transform: none;
            transform-origin: center center;
            border: 1px solid transparent;
            border-radius: 14px;
            overflow: visible;
            transition:
                transform 220ms ease,
                border-color 220ms ease,
                box-shadow 220ms ease;
        }}
        .market-chart-reveal-ready {{
            opacity: 0 !important;
            transform: translate3d(-60px, 0, 0) !important;
            transition: none !important;
            will-change: opacity, transform;
        }}
        .market-chart-reveal-visible {{
            opacity: 1 !important;
            transform: translate3d(0, 0, 0) !important;
            transition:
                opacity 650ms ease-out,
                transform 650ms cubic-bezier(0.22, 1, 0.36, 1) !important;
            will-change: opacity, transform;
        }}
        .market-chart-reveal-complete {{
            opacity: 1 !important;
            transform: none;
            transition:
                transform 220ms ease,
                border-color 220ms ease,
                box-shadow 220ms ease;
            will-change: auto;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .market-chart-reveal-complete:hover {{
                transform: translate3d(0, -2px, 0);
                border-color: color-mix(in srgb, var(--accent) 40%, transparent);
                box-shadow: 0 14px 30px color-mix(in srgb, var(--accent) 14%, transparent);
                position: relative;
                z-index: 2;
            }}
        }}
        .insight {{
            color: var(--muted);
            border-left: 3px solid var(--accent);
            padding: .34rem .65rem;
            margin: -.08rem 0 1.05rem;
            font-size: .86rem;
            line-height: 1.45;
        }}
        .footer {{
            color: var(--muted);
            border-top: 1px solid var(--border);
            margin-top: 2rem;
            padding-top: 1rem;
            font-size: .86rem;
            line-height: 1.7;
        }}
        .footer a {{
            color: var(--accent-bright);
            text-decoration: none;
            font-weight: 500;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}

        .stButton button, .stLinkButton a, .stDownloadButton button {{
            min-height: 2.45rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            font-weight: 500;
            font-family: var(--font);
            box-shadow: none;
            transition: background-color 180ms ease, border-color 180ms ease, color 180ms ease, box-shadow 180ms ease;
        }}
        .stButton button * , .stLinkButton a *, .stDownloadButton button * {{
            color: inherit;
        }}
        .stLinkButton a[kind="primary"],
        [data-testid="stLinkButton"] a[kind="primary"],
        .stButton button[kind="primary"],
        .stDownloadButton button[kind="primary"] {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--on-accent) !important;
            box-shadow: var(--shadow-accent);
        }}
        .stButton button:hover, .stLinkButton a:hover, .stDownloadButton button:hover {{
            border-color: var(--accent);
            background: var(--hover);
            color: var(--text);
        }}
        .stLinkButton a[kind="primary"]:hover,
        [data-testid="stLinkButton"] a[kind="primary"]:hover,
        .stButton button[kind="primary"]:hover,
        .stDownloadButton button[kind="primary"]:hover {{
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            color: var(--on-accent) !important;
        }}
        .stButton button:focus, .stLinkButton a:focus,
        [data-baseweb="select"] > div:focus-within,
        input:focus, textarea:focus {{
            outline: 3px solid color-mix(in srgb, var(--accent) 34%, transparent);
            outline-offset: 2px;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--surface-2);
            color: var(--text);
        }}
        div[data-testid="stAlert"] * {{
            color: var(--text);
        }}

        [data-testid="stExpander"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
        }}
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary * {{
            color: var(--text);
            font-weight: 600;
        }}

        label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {{
            color: var(--text-2);
            font-family: var(--font);
            font-weight: 500;
        }}
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        [data-testid="stDateInput"] input,
        [data-testid="stTextInput"] input {{
            background: var(--input-bg);
            color: var(--input-text);
            border-color: var(--border);
            border-radius: 10px;
            min-height: 2.45rem;
            transition: border-color .14s ease, box-shadow .14s ease;
        }}
        [data-baseweb="select"]:hover > div,
        [data-testid="stDateInput"] input:hover {{
            border-color: color-mix(in srgb, var(--accent) 45%, var(--border));
        }}
        [data-baseweb="popover"] {{
            border-radius: 10px !important;
            box-shadow: 0 14px 32px rgba(15, 23, 42, .14) !important;
        }}
        [data-baseweb="menu"] li[role="option"]:hover {{
            background: var(--tag-bg) !important;
        }}
        [data-baseweb="select"] span,
        [data-baseweb="select"] input,
        [data-baseweb="input"] input,
        [data-testid="stDateInput"] input {{
            color: var(--input-text);
        }}
        [data-baseweb="tag"] {{
            background: var(--tag-bg);
            border: 1px solid var(--border);
            color: var(--tag-text);
            border-radius: 999px;
            max-width: 100%;
        }}
        [data-baseweb="tag"] span {{
            color: var(--tag-text);
            font-size: .78rem;
        }}
        [data-baseweb="select"] [role="combobox"] {{
            max-height: 92px;
            overflow-y: auto;
            align-items: flex-start;
            padding-top: .25rem;
            padding-bottom: .25rem;
        }}
        .st-key-dashboard_filter_panel [data-baseweb="select"] > div:focus-within {{
            outline: 0 !important;
            border-color: rgba(180, 83, 9, 0.70) !important;
            box-shadow: 0 0 0 3px rgba(180, 83, 9, 0.12) !important;
        }}
        .st-key-dashboard_filter_panel [data-baseweb="select"] input,
        .st-key-dashboard_filter_panel [data-baseweb="select"] input:focus,
        .st-key-dashboard_filter_panel [data-baseweb="select"] input:focus-visible {{
            border: 0 !important;
            outline: 0 !important;
            box-shadow: none !important;
            background: transparent !important;
            border-radius: 0 !important;
        }}
        [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {{
            background: var(--surface-elevated);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 10px;
            box-shadow: var(--shadow);
            z-index: 999999;
            max-height: 280px;
            overflow-y: auto;
        }}
        [role="option"], [data-baseweb="menu"] li {{
            color: var(--text);
            background: var(--surface-elevated);
            font-family: var(--font);
        }}
        [role="option"]:hover,
        [role="option"][aria-selected="true"],
        [data-baseweb="menu"] li:hover {{
            background: var(--hover);
            color: var(--text);
        }}
        [data-baseweb="popover"] div {{
            color: var(--text-2);
        }}
        input::placeholder {{
            color: var(--muted);
            opacity: 1;
        }}
        [data-testid="stSlider"] * {{
            color: var(--text-2);
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}
        .filter-title {{
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0 0 .7rem;
        }}
        @media (max-width: 1100px) {{
            .portfolio-hero {{
                grid-template-columns: minmax(0, 1.35fr) minmax(230px, .65fr);
                column-gap: clamp(1.25rem, 2.5vw, 2rem);
            }}
            .portfolio-hero h1 {{
                font-size: clamp(2.7rem, 4.6vw, 3.55rem);
            }}
            .hero-profile-card {{
                width: min(100%, 270px);
            }}
            .hero-profile-name {{
                font-size: 1.42rem;
            }}
            .hero-skill-section {{
                width: 100%;
            }}
            .featured-project-card {{
                grid-template-columns: 1fr;
            }}
            .featured-preview,
            .featured-lineage-preview {{
                width: 100%;
                justify-self: stretch;
            }}
        }}
        @media (max-width: 1024px) {{
            .pipeline.pipeline-architecture {{
                min-width: 1180px;
            }}
            .featured-preview img {{ max-height: 320px; }}
            .featured-lineage-preview {{ min-height: 0; }}
            .st-key-market_basic_filters_grid [data-testid="stHorizontalBlock"] {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                column-gap: 1rem;
                row-gap: 1rem;
            }}
            .st-key-market_basic_filters_grid [data-testid="column"] {{
                width: 100% !important;
            }}
            .hero-skill-pipeline {{
                grid-template-columns: repeat(3, minmax(108px, 136px));
                grid-template-rows: auto auto;
                justify-content: center;
                gap: .78rem 1rem;
                padding-top: 2.05rem;
            }}
            .core-workflow-orchestrator {{
                top: 0;
            }}
            .hero-skill-node-1 {{ grid-column: 1; grid-row: 1; }}
            .hero-skill-node-2 {{ grid-column: 2; grid-row: 1; }}
            .hero-skill-node-3 {{ grid-column: 3; grid-row: 1; }}
            .hero-skill-node-4 {{ grid-column: 3; grid-row: 2; }}
            .hero-skill-node-5 {{ grid-column: 2; grid-row: 2; }}
            .hero-skill-node-6 {{ grid-column: 1; grid-row: 2; }}
            .hero-flow-svg-desktop {{
                display: none;
            }}
            .hero-flow-svg-tablet {{
                display: block;
                left: calc(50% - 220px);
                right: calc(50% - 220px);
                top: calc(2.05rem + 38px);
                width: 440px;
                height: 88px;
            }}
            .hero-skill-node-1 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-1; }}
            .hero-skill-node-2 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-2; }}
            .hero-skill-node-3 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-3; }}
            .hero-skill-node-4 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-4; }}
            .hero-skill-node-5 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-5; }}
            .hero-skill-node-6 {{ animation-name: home-skill-node-enter, hero-node-pulse-tablet-6; }}
            .dashboard-primary-kpis,
            .dashboard-metadata-strip {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
            .quality-summary-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
            .pipeline-info-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
            .pipeline-info-grid .pipeline-card:last-child {{
                grid-column: 1 / -1;
            }}
            .dashboard-meta-item-1,
            .dashboard-meta-item-3 {{
                border-left: 0;
                padding-left: 0;
            }}
        }}
        @media (max-width: 760px) {{
            .project-card-featured {{ max-width: 100%; }}
            .portfolio-hero {{
                grid-template-columns: 1fr;
                row-gap: 1rem;
            }}
            .data-command-hero {{
                padding: .9rem;
                border-radius: 16px;
                background:
                    radial-gradient(circle at 50% 12%, rgba(180, 83, 9, .10), transparent 32%),
                    linear-gradient(145deg, rgba(255, 255, 255, .98), rgba(248, 250, 252, .94));
            }}
            .data-blueprint-grid {{
                opacity: .28;
                background-size: 28px 28px;
            }}
            .hero-value-rotator {{
                width: 100%;
            }}
            .hero-copy,
            .hero-profile-card,
            .hero-skill-section {{
                grid-column: 1;
                grid-row: auto;
            }}
            .portfolio-hero h1 {{
                font-size: clamp(2.35rem, 12vw, 3rem);
                margin-top: .8rem;
                max-width: 100%;
            }}
            .hero-description {{
                margin-top: .8rem;
            }}
            .hero-actions {{
                margin-top: .9rem;
            }}
            .hero-profile-card {{
                width: min(100%, 300px);
                margin: 0 auto;
                transform: none;
            }}
            .hero-profile-identity {{
                text-align: center;
            }}
            .hero-profile-meta,
            .hero-profile-stack {{
                justify-content: center;
            }}
            .hero-skill-section {{
                width: 100%;
                margin-top: 0;
            }}
            .hero-skill-pipeline {{
                grid-template-columns: minmax(0, 1fr);
                grid-template-rows: none;
                justify-content: stretch;
                gap: .5rem;
                padding-top: 2.35rem;
            }}
            .core-workflow-orchestrator {{
                left: 0;
                width: 100%;
                min-width: 0;
                justify-content: center;
                transform: none;
            }}
            .core-workflow-orchestrator-label {{
                gap: .32rem;
            }}
            .hero-skill-node-1,
            .hero-skill-node-2,
            .hero-skill-node-3,
            .hero-skill-node-4,
            .hero-skill-node-5,
            .hero-skill-node-6 {{
                grid-column: 1;
                grid-row: auto;
            }}
            .hero-skill-node {{
                min-height: 58px;
                height: 58px;
                width: 100%;
            }}
            .hero-flow-svg-desktop,
            .hero-flow-svg-tablet {{
                display: none;
            }}
            .hero-flow-svg-mobile {{
                display: block;
                left: 1.08rem;
                right: auto;
                top: calc(2.35rem + 29px);
                width: 20px;
                height: 330px;
            }}
            .hero-skill-node-1 {{ animation-name: home-skill-node-enter, hero-node-pulse-1; }}
            .hero-skill-node-2 {{ animation-name: home-skill-node-enter, hero-node-pulse-2; }}
            .hero-skill-node-3 {{ animation-name: home-skill-node-enter, hero-node-pulse-3; }}
            .hero-skill-node-4 {{ animation-name: home-skill-node-enter, hero-node-pulse-4; }}
            .hero-skill-node-5 {{ animation-name: home-skill-node-enter, hero-node-pulse-5; }}
            .hero-skill-node-6 {{ animation-name: home-skill-node-enter, hero-node-pulse-6; }}
            .hero-photo-shell {{
                order: -1;
                width: min(100%, 300px);
            }}
            .st-key-home_profile_photo_shell,
            .st-key-home_profile_info_card {{
                width: min(100%, 300px);
                transform: none;
            }}
            .home-profile-info-card {{
                transform: none;
            }}
            .home-about-grid,
            .home-skills-grid,
            .pipeline-step-grid,
            .pipeline-info-grid {{
                grid-template-columns: 1fr;
            }}
            .featured-lineage-preview {{
                padding: .58rem;
            }}
            .project-overview-header {{
                margin-bottom: 1.45rem;
            }}
            .project-header-actions {{
                gap: .65rem;
            }}
            .project-header-actions .portfolio-button {{
                flex: 1 1 13rem;
            }}
            .project-evidence-compact {{
                display: grid;
                grid-template-columns: 1fr;
                gap: .6rem;
                width: 100%;
            }}
            .project-evidence-item {{
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
            }}
            .contact-cta {{
                grid-template-columns: 1fr;
            }}
            .contact-cta-actions {{
                width: 100%;
            }}
            .contact-cta-actions .portfolio-button,
            .hero-actions .portfolio-button {{
                flex: 1 1 13rem;
            }}
            .contact-resume-strip {{
                grid-template-columns: 1fr;
            }}
            .contact-resume-strip .contact-card-action {{
                width: 100%;
            }}
            .st-key-dashboard_filter_panel {{
                padding: 1.05rem 1rem .95rem;
            }}
            .market-filters-heading {{
                margin-bottom: .9rem;
            }}
            .st-key-market_basic_filters_grid [data-testid="stHorizontalBlock"] {{
                grid-template-columns: 1fr;
                row-gap: .9rem;
            }}
            .dashboard-primary-kpis,
            .dashboard-metadata-strip {{
                grid-template-columns: 1fr;
            }}
            .quality-summary-grid {{
                grid-template-columns: 1fr;
            }}
            .dashboard-meta-item {{
                border-left: 0;
                border-top: 1px solid color-mix(in srgb, var(--accent) 14%, transparent);
                padding: .55rem 0;
            }}
            .dashboard-meta-item:first-child {{
                border-top: 0;
                padding-top: .15rem;
            }}
            .dashboard-results-status {{
                width: 100%;
                justify-content: center;
                border-radius: 12px;
            }}
            .st-key-market_dashboard_chart_job_title_demand,
            .st-key-market_dashboard_chart_company_activity,
            .st-key-market_dashboard_chart_salary_by_job_title,
            .st-key-market_dashboard_chart_salary_by_country,
            .st-key-market_dashboard_chart_remote_salary,
            .st-key-market_dashboard_chart_monthly_posting_trend,
            .st-key-market_dashboard_chart_monthly_growth,
            .st-key-market_dashboard_chart_technical_skill_demand,
            .st-key-market_dashboard_chart_high_salary_skills,
            .st-key-market_dashboard_chart_data_engineer_skill_demand {{
                animation: none !important;
                opacity: 1 !important;
                translate: 0 0 !important;
                transform: none !important;
            }}
        }}
        @media (max-width: 860px) {{
            .dataset-metrics {{ grid-template-columns: 1fr; }}
            .quality-metric-grid {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 560px) {{
            .block-container {{ padding: .35rem 1rem 2.5rem; }}
            .pipeline-architecture-viewport {{
                overflow-x: visible;
                padding: .25rem 0 .45rem;
                mask-image: none;
            }}
            .pipeline.pipeline-architecture {{
                min-width: 0;
            }}
            .pipeline-orchestration-band {{
                grid-template-columns: 1fr;
                gap: .6rem;
                min-height: 0;
                padding: .75rem;
            }}
            .pipeline-orchestration-status {{
                justify-content: flex-start;
            }}
            .pipeline-airflow-stem {{
                display: none;
            }}
            .pipeline-stage-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: .62rem;
                padding-left: 2.4rem;
            }}
            .pipeline-architecture-card {{
                min-height: 96px;
                justify-items: start;
                text-align: left;
                padding: .78rem .85rem;
            }}
            .pipeline-stage-icon {{
                position: absolute;
                left: -2.42rem;
                top: .85rem;
            }}
            .data-flow-lane {{
                position: absolute;
                left: 1.05rem;
                top: calc(110px + 1rem);
                bottom: .85rem;
                width: 32px;
                height: auto;
                margin: 0;
                padding: 0;
                pointer-events: none;
            }}
            .data-flow-svg {{
                width: 32px;
                height: 100%;
            }}
            .data-flow-path {{
                d: path("M16 8 V560");
            }}
            .data-flow-arrow-segments {{
                d: path("M16 8 V118 M16 118 V228 M16 228 V338 M16 338 V448 M16 448 V560");
            }}
            .data-flow-stems {{
                display: none;
            }}
            .section-card {{ padding: 1rem; }}
            .kpi-card {{ min-height: 118px; }}
        }}
        @media (hover: none), (pointer: coarse) {{
            .hero-skill-node:hover {{
                transform: none;
                border-color: var(--border);
                box-shadow: 0 8px 18px rgba(15, 23, 42, .05);
            }}
            .hero-skill-node:hover .hero-skill-tooltip {{
                opacity: 0;
                transform: translate(-50%, 4px);
            }}
            .hero-profile-card,
            .hero-profile-card:hover {{
                transform: none;
                border-color: rgba(180, 83, 9, .28);
                box-shadow: 0 12px 30px rgba(15, 23, 42, .10);
            }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                transition-duration: 0.01ms !important;
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
            }}
            .about-hover-card:hover,
            .about-hover-card:focus-within,
            .experience-hover-card:hover,
            .experience-hover-card:focus-within,
            .sidebar-project-card,
            .sidebar-project-card:hover,
            .sidebar-project-card:focus-within,
            .sidebar-section-content,
            .sidebar-projects-content,
            .sidebar-portfolio-content,
            .sidebar-project-links,
            .sidebar-expander-chevron,
            .sidebar-project-chevron,
            .sidebar-mini-packet,
            .st-key-home_profile_photo_shell,
            .st-key-home_profile_photo_shell img,
            .st-key-home_profile_info_card,
            .home-profile-info-card,
            .home-profile-info-card:hover,
            .home-profile-info-card:focus-within,
            .hero-profile-card,
            .hero-profile-card:hover,
            .hero-skill-node,
            .hero-skill-node:hover,
            .data-flow-pulse,
            .data-quality-detail,
            .sidebar-brand:hover,
            .sidebar-brand:focus-within,
            .home-card:hover,
            .home-card:focus-within,
            .skill-card:hover,
            .skill-card:focus-within,
            .pipeline-card:hover,
            .pipeline-card:focus-within,
            .job-intelligence-hover-card:hover,
            .job-intelligence-hover-card:focus-within,
            .contact-hover-card:hover,
            .contact-hover-card:focus-within,
            .data-quality-hover-card:hover,
            .data-quality-hover-card:focus-within,
            .home-about-card:hover,
            .home-about-card:focus-within,
            .home-skill-card:hover,
            .home-skill-card:focus-within,
            .featured-project-card:hover,
            .featured-project-card:focus-within,
            .pipeline-step-card:hover,
            .pipeline-step-card:focus-within,
            .st-key-market_dashboard_chart_job_title_demand,
            .st-key-market_dashboard_chart_company_activity,
            .st-key-market_dashboard_chart_salary_by_job_title,
            .st-key-market_dashboard_chart_salary_by_country,
            .st-key-market_dashboard_chart_remote_salary,
            .st-key-market_dashboard_chart_monthly_posting_trend,
            .st-key-market_dashboard_chart_monthly_growth,
            .st-key-market_dashboard_chart_technical_skill_demand,
            .st-key-market_dashboard_chart_high_salary_skills,
            .st-key-market_dashboard_chart_data_engineer_skill_demand,
            .market-chart-reveal-ready,
            .market-chart-reveal-visible,
            .market-chart-reveal-complete {{
                transform: none;
                animation: none !important;
                transition: none !important;
                opacity: 1 !important;
                translate: 0 0 !important;
                scale: 1 !important;
            }}
            .home-profile-info-card,
            .st-key-home_profile_photo_shell,
            .st-key-home_profile_info_card {{
                opacity: 1 !important;
            }}
            .data-background-particle {{
                display: none;
            }}
            .hero-value-rotator {{
                overflow: visible;
            }}
            .hero-value-line {{
                display: none;
                position: static;
                opacity: 1;
                transform: none;
            }}
            .hero-value-line-1 {{
                display: inline;
            }}
            .hero-profile-card,
            .hero-profile-card:hover,
            .hero-profile-status-dot,
            .hero-skill-node,
            .featured-lineage-pulse {{
                animation: none !important;
                transition: none !important;
                transform: none !important;
                opacity: 1 !important;
            }}
            .hero-skill-node::before {{
                opacity: 0 !important;
            }}
            .hero-flow-motion,
            .featured-lineage-pulse,
            .featured-lineage-energy {{
                display: none;
            }}
            .sidebar-mini-packet {{
                display: none;
            }}
            .data-flow-pulse {{
                opacity: .75 !important;
            }}
        }}
        </style>
        """
    )
    return _minify_css(css)
