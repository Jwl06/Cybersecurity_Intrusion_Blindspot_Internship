"""Shared cybersecurity-themed styling and reusable UI helpers."""

import html
import math

import streamlit as st

CYBER_COLORS = {
    "bg_dark": "#0A0A0A",
    "bg_card": "#111111",
    "bg_elevated": "#1A1A1A",
    "border": "#2A2A2A",
    "border_glow": "#FF3B3B",
    "accent": "#FF3B3B",
    "accent_dark": "#B30000",
    "text_primary": "#FFFFFF",
    "text_muted": "#B0B0B0",
    "text_dim": "#6B6B6B",
    "danger": "#FF3B3B",
    "warning": "#FF8C00",
    "success": "#00C853",
}

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "#111111",
    "font": {"color": "#B0B0B0", "family": "Inter, sans-serif", "size": 12},
    "margin": {"l": 0, "r": 0, "t": 10, "b": 0},
    "coloraxis_showscale": False,
    "xaxis": {
        "title": "",
        "showgrid": True,
        "gridcolor": "rgba(255, 255, 255, 0.12)",
        "gridwidth": 1,
        "zerolinecolor": "#3A3A3A",
        "linecolor": "#4A4A4A",
        "tickcolor": "#8A8A8A",
    },
    "yaxis": {
        "title": "",
        "showgrid": True,
        "gridcolor": "rgba(255, 255, 255, 0.12)",
        "gridwidth": 1,
        "zerolinecolor": "#3A3A3A",
        "linecolor": "#4A4A4A",
        "tickcolor": "#8A8A8A",
    },
}


def inject_theme() -> None:
    """Inject global CSS for a red-black SOC dashboard aesthetic."""
    c = CYBER_COLORS
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

            /* ── Base app shell ─────────────────────────────────────────── */
            .stApp {{
                background-color: {c["bg_dark"]};
                background-image:
                    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(179, 0, 0, 0.07) 0%, transparent 55%),
                    linear-gradient(rgba(255, 59, 59, 0.12) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 59, 59, 0.12) 1px, transparent 1px),
                    linear-gradient(rgba(255, 59, 59, 0.06) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 59, 59, 0.06) 1px, transparent 1px);
                background-size:
                    100% 100%,
                    72px 72px,
                    72px 72px,
                    18px 18px,
                    18px 18px;
                background-position: center top, center center, center center, center center, center center;
                background-attachment: fixed;
                color: {c["text_primary"]};
            }}

            [data-testid="stAppViewContainer"] {{
                background: transparent;
            }}

            [data-testid="stMain"] {{
                background: transparent;
            }}

            .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1400px;
            }}

            /* ── Sidebar ────────────────────────────────────────────────── */
            [data-testid="stSidebarNav"] {{
                display: none;
            }}

            [data-testid="stSidebar"] {{
                background:
                    linear-gradient(180deg, rgba(255, 59, 59, 0.04) 0%, transparent 28%),
                    linear-gradient(180deg, #0D0D0D 0%, {c["bg_card"]} 100%);
                border-right: 1px solid {c["border"]};
                box-shadow: inset -1px 0 0 rgba(255, 59, 59, 0.06);
                min-width: 252px !important;
                max-width: 252px !important;
            }}

            [data-testid="stSidebar"] > div:first-child {{
                background: transparent;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                padding: 1.35rem 1rem 1.25rem;
            }}

            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                gap: 0.35rem;
            }}

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] .stCaption {{
                color: {c["text_muted"]} !important;
            }}

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {{
                color: {c["text_primary"]} !important;
            }}

            .sidebar-brand-block {{
                display: flex;
                align-items: flex-start;
                gap: 0.85rem;
                margin-bottom: 1.1rem;
            }}

            .sidebar-brand-icon {{
                flex-shrink: 0;
                width: 2.5rem;
                height: 2.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                color: {c["accent"]};
                background: rgba(255, 59, 59, 0.08);
                border: 1px solid rgba(255, 59, 59, 0.28);
                border-radius: 10px;
                box-shadow:
                    0 0 18px rgba(255, 59, 59, 0.14),
                    inset 0 1px 0 rgba(255, 255, 255, 0.04);
            }}

            .sidebar-brand-icon svg {{
                width: 1.35rem;
                height: 1.35rem;
            }}

            .sidebar-brand-copy {{
                display: flex;
                flex-direction: column;
                gap: 0.2rem;
                min-width: 0;
            }}

            .sidebar-brand-eyebrow {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: {c["text_dim"]};
                line-height: 1.3;
            }}

            .sidebar-brand-title {{
                font-family: 'Inter', sans-serif;
                font-size: 0.95rem;
                font-weight: 700;
                letter-spacing: -0.01em;
                line-height: 1.35;
                color: {c["text_primary"]};
            }}

            .sidebar-brand-rule {{
                height: 1px;
                margin-bottom: 1.35rem;
                background: linear-gradient(
                    90deg,
                    rgba(255, 59, 59, 0.45) 0%,
                    rgba(255, 59, 59, 0.08) 55%,
                    transparent 100%
                );
            }}

            .sidebar-nav-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.64rem;
                font-weight: 600;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                color: {c["text_dim"]} !important;
                margin: 0 0 0.65rem 0.15rem !important;
                padding: 0;
            }}

            [data-testid="stSidebar"] .stPageLink {{
                margin-bottom: 0.35rem;
            }}

            [data-testid="stSidebar"] .stPageLink a {{
                font-family: 'Inter', sans-serif !important;
                font-size: 0.9rem !important;
                font-weight: 500 !important;
                letter-spacing: 0.01em;
                color: {c["text_muted"]} !important;
                text-decoration: none !important;
                padding: 0.72rem 0.9rem !important;
                border-radius: 8px;
                border: 1px solid transparent;
                display: flex !important;
                align-items: center;
                gap: 0.7rem;
                line-height: 1.2;
                transition:
                    color 0.22s ease,
                    background 0.22s ease,
                    border-color 0.22s ease,
                    box-shadow 0.22s ease,
                    transform 0.22s ease;
            }}

            [data-testid="stSidebar"] .stPageLink a span[data-testid="stIconMaterial"],
            [data-testid="stSidebar"] .stPageLink a > span:first-child {{
                color: inherit !important;
                font-size: 1.05rem !important;
                opacity: 0.82;
                flex-shrink: 0;
                transition: opacity 0.22s ease, color 0.22s ease;
            }}

            [data-testid="stSidebar"] .stPageLink a:hover {{
                color: {c["text_primary"]} !important;
                background: rgba(255, 59, 59, 0.06);
                border-color: rgba(255, 59, 59, 0.18);
                transform: translateX(3px);
            }}

            [data-testid="stSidebar"] .stPageLink a:hover span[data-testid="stIconMaterial"],
            [data-testid="stSidebar"] .stPageLink a:hover > span:first-child {{
                opacity: 1;
                color: {c["accent"]} !important;
            }}

            [data-testid="stSidebar"] .stPageLink a[aria-current="page"] {{
                color: {c["accent"]} !important;
                background: rgba(255, 59, 59, 0.1);
                border-color: rgba(255, 59, 59, 0.35);
                border-left: 2px solid {c["accent"]};
                padding-left: calc(0.9rem - 1px) !important;
                box-shadow:
                    0 0 14px rgba(255, 59, 59, 0.22),
                    inset 0 0 0 1px rgba(255, 59, 59, 0.08);
            }}

            [data-testid="stSidebar"] .stPageLink a[aria-current="page"] span[data-testid="stIconMaterial"],
            [data-testid="stSidebar"] .stPageLink a[aria-current="page"] > span:first-child {{
                opacity: 1;
                color: {c["accent"]} !important;
            }}

            .sidebar-footer {{
                display: flex;
                align-items: center;
                gap: 0.55rem;
                margin-top: auto;
                padding: 0.85rem 0.75rem 0;
                border-top: 1px solid {c["border"]};
            }}

            .sidebar-status-indicator {{
                width: 0.45rem;
                height: 0.45rem;
                border-radius: 50%;
                background: {c["success"]};
                box-shadow: 0 0 8px rgba(0, 200, 83, 0.55);
                flex-shrink: 0;
            }}

            .sidebar-status-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c["text_dim"]};
            }}

            [data-testid="stSidebar"] hr {{
                margin: 0.65rem 0 !important;
            }}

            /* ── Typography ─────────────────────────────────────────────── */
            h1, h2, h3, h4, h5 {{
                font-family: 'Inter', sans-serif !important;
                color: {c["text_primary"]} !important;
                letter-spacing: -0.02em;
            }}

            p, li, span, label, .stMarkdown {{
                font-family: 'Inter', sans-serif;
                color: {c["text_muted"]};
            }}

            code {{
                font-family: 'JetBrains Mono', monospace !important;
                background: {c["bg_elevated"]} !important;
                color: {c["accent"]} !important;
                border: 1px solid {c["border"]};
                border-radius: 4px;
                padding: 0.1rem 0.35rem;
            }}

            /* ── SOC status bar ─────────────────────────────────────────── */
            .soc-status-bar {{
                display: flex;
                align-items: center;
                gap: 1.25rem;
                flex-wrap: wrap;
                background: {c["bg_card"]};
                border: 1px solid {c["border"]};
                border-left: 3px solid {c["accent"]};
                border-radius: 8px;
                padding: 0.65rem 1.25rem;
                margin-bottom: 1.25rem;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }}

            .soc-status-bar .soc-item {{
                color: {c["text_muted"]};
            }}

            .soc-status-bar .soc-item strong {{
                color: {c["text_primary"]};
            }}

            .soc-pulse {{
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: {c["success"]};
                box-shadow: 0 0 8px {c["success"]};
                animation: soc-pulse 2s ease-in-out infinite;
                margin-right: 0.4rem;
                vertical-align: middle;
            }}

            @keyframes soc-pulse {{
                0%, 100% {{ opacity: 1; box-shadow: 0 0 8px {c["success"]}; }}
                50% {{ opacity: 0.5; box-shadow: 0 0 4px {c["success"]}; }}
            }}

            /* ── Page headers ───────────────────────────────────────────── */
            .cyber-header {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: {c["accent"]};
                margin-bottom: 0.35rem;
            }}

            .cyber-title {{
                font-family: 'Inter', sans-serif;
                font-size: 1.75rem;
                font-weight: 700;
                color: {c["text_primary"]};
                margin: 0 0 0.4rem 0;
                line-height: 1.2;
            }}

            .cyber-subtitle {{
                color: {c["text_muted"]};
                font-size: 0.9rem;
                margin-bottom: 1.25rem;
                line-height: 1.6;
            }}

            .section-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c["accent"]};
                margin-bottom: 0.75rem;
                padding-bottom: 0.4rem;
                border-bottom: 1px solid {c["border"]};
            }}

            /* ── KPI / metric cards with glow ───────────────────────────── */
            div[data-testid="stMetric"] {{
                background: linear-gradient(145deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 1rem 1.25rem;
                box-shadow: 0 0 0 1px rgba(255, 59, 59, 0.08),
                            0 4px 20px rgba(0, 0, 0, 0.4);
                transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
            }}

            div[data-testid="stMetric"]:hover {{
                border-color: rgba(255, 59, 59, 0.55);
                box-shadow: 0 0 16px rgba(255, 59, 59, 0.18),
                            0 0 32px rgba(255, 59, 59, 0.06),
                            0 4px 20px rgba(0, 0, 0, 0.5);
                transform: translateY(-1px);
            }}

            [data-testid="stMetricLabel"] {{
                font-family: 'JetBrains Mono', monospace !important;
                color: {c["text_muted"]} !important;
                text-transform: uppercase;
                font-size: 0.68rem !important;
                letter-spacing: 0.08em;
            }}

            [data-testid="stMetricValue"] {{
                font-family: 'JetBrains Mono', monospace !important;
                color: {c["accent"]} !important;
                font-weight: 600 !important;
            }}

            [data-testid="stMetricDelta"] {{
                font-family: 'JetBrains Mono', monospace !important;
            }}

            /* ── Bordered containers (panel cards) ────────────────────── */
            [data-testid="stVerticalBlockBorderWrapper"] {{
                background: {c["bg_card"]};
                border: 1px solid {c["border"]} !important;
                border-radius: 10px;
                padding: 0.25rem;
                box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }}

            [data-testid="stVerticalBlockBorderWrapper"]:hover {{
                border-color: rgba(255, 59, 59, 0.3) !important;
                box-shadow: 0 0 12px rgba(255, 59, 59, 0.08),
                            0 4px 24px rgba(0, 0, 0, 0.4);
            }}

            /* ── Custom HTML cards ──────────────────────────────────────── */
            .cyber-card {{
                background: linear-gradient(160deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 1.1rem 1.35rem;
                margin-bottom: 0.85rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
            }}

            .cyber-card:hover {{
                border-color: rgba(255, 59, 59, 0.45);
                box-shadow: 0 0 14px rgba(255, 59, 59, 0.12),
                            0 4px 24px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }}

            .cyber-card-accent {{
                border-left: 3px solid {c["accent"]};
            }}

            .cyber-card-danger {{
                border-left: 3px solid {c["danger"]};
            }}

            .cyber-card-warning {{
                border-left: 3px solid {c["warning"]};
            }}

            .cyber-card-success {{
                border-left: 3px solid {c["success"]};
            }}

            .cyber-card-info {{
                border-left: 3px solid {c["accent_dark"]};
            }}

            .cyber-card h4 {{
                font-size: 0.9rem !important;
                margin: 0 0 0.45rem 0 !important;
                color: {c["text_primary"]} !important;
                font-weight: 600 !important;
            }}

            .cyber-card p {{
                color: {c["text_muted"]};
                font-size: 0.82rem;
                margin: 0 0 0.6rem 0;
                line-height: 1.55;
            }}

            /* ── KPI highlight card (HTML) ──────────────────────────────── */
            .kpi-card {{
                background: {c["bg_card"]};
                border: 1px solid rgba(255, 59, 59, 0.35);
                border-radius: 10px;
                padding: 1.1rem 1.25rem;
                text-align: center;
                box-shadow: 0 0 20px rgba(255, 59, 59, 0.1),
                            inset 0 1px 0 rgba(255, 255, 255, 0.03);
                transition: box-shadow 0.25s ease, transform 0.2s ease;
            }}

            .kpi-card:hover {{
                box-shadow: 0 0 28px rgba(255, 59, 59, 0.22),
                            inset 0 1px 0 rgba(255, 255, 255, 0.05);
                transform: translateY(-2px);
            }}

            .kpi-card .kpi-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.35rem;
            }}

            .kpi-card .kpi-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.6rem;
                font-weight: 700;
                color: {c["accent"]};
                line-height: 1.1;
            }}

            .kpi-card .kpi-delta {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                margin-top: 0.3rem;
            }}

            .kpi-delta-up {{ color: {c["success"]}; }}
            .kpi-delta-down {{ color: {c["danger"]}; }}
            .kpi-delta-neutral {{ color: {c["text_dim"]}; }}

            /* ── Badges ─────────────────────────────────────────────────── */
            .cyber-badge {{
                display: inline-block;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                font-weight: 600;
                padding: 0.18rem 0.5rem;
                border-radius: 4px;
                letter-spacing: 0.05em;
            }}

            .badge-secure {{
                background: rgba(0, 200, 83, 0.12);
                color: {c["success"]};
                border: 1px solid rgba(0, 200, 83, 0.35);
            }}

            .badge-alert {{
                background: rgba(255, 59, 59, 0.12);
                color: {c["danger"]};
                border: 1px solid rgba(255, 59, 59, 0.4);
            }}

            .badge-warning {{
                background: rgba(255, 140, 0, 0.12);
                color: {c["warning"]};
                border: 1px solid rgba(255, 140, 0, 0.35);
            }}

            .badge-pending {{
                background: rgba(179, 0, 0, 0.15);
                color: #E04040;
                border: 1px solid rgba(179, 0, 0, 0.4);
            }}

            /* ── Buttons ────────────────────────────────────────────────── */
            .stButton > button {{
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                border-radius: 8px;
                letter-spacing: 0.03em;
                transition: box-shadow 0.2s ease, transform 0.15s ease;
            }}

            .stButton > button[kind="primary"] {{
                background: linear-gradient(135deg, {c["accent"]} 0%, {c["accent_dark"]} 100%);
                color: {c["text_primary"]};
                border: 1px solid {c["accent_dark"]};
            }}

            .stButton > button[kind="primary"]:hover {{
                box-shadow: 0 0 22px rgba(255, 59, 59, 0.4);
                border-color: {c["accent"]};
            }}

            .stButton > button[kind="secondary"] {{
                background: {c["bg_elevated"]};
                color: {c["text_primary"]};
                border: 1px solid {c["border"]};
            }}

            .stButton > button[kind="secondary"]:hover {{
                border-color: rgba(255, 59, 59, 0.4);
                box-shadow: 0 0 12px rgba(255, 59, 59, 0.1);
            }}

            /* ── Forms & inputs ─────────────────────────────────────────── */
            div[data-testid="stForm"] {{
                background: {c["bg_elevated"]};
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 1.25rem;
            }}

            .stTextInput input, .stNumberInput input, .stSelectbox > div > div,
            .stMultiSelect > div > div, .stTextArea textarea {{
                background: {c["bg_card"]} !important;
                color: {c["text_primary"]} !important;
                border-color: {c["border"]} !important;
            }}

            .stSlider [data-baseweb="slider"] div {{
                color: {c["accent"]} !important;
            }}

            /* ── Alerts ─────────────────────────────────────────────────── */
            [data-testid="stAlert"] {{
                background: {c["bg_elevated"]};
                border-radius: 8px;
                border: 1px solid {c["border"]};
            }}

            .stAlert p {{
                color: {c["text_muted"]} !important;
            }}

            /* ── Progress bars ──────────────────────────────────────────── */
            .stProgress > div > div {{
                background: {c["bg_elevated"]};
            }}

            .stProgress > div > div > div {{
                background: linear-gradient(90deg, {c["accent_dark"]}, {c["accent"]});
            }}

            /* ── Expanders ──────────────────────────────────────────────── */
            [data-testid="stExpander"] {{
                background: {c["bg_card"]};
                border: 1px solid {c["border"]};
                border-radius: 8px;
            }}

            [data-testid="stExpander"] summary {{
                color: {c["text_primary"]} !important;
            }}

            /* ── Page links ─────────────────────────────────────────────── */
            .stPageLink a {{
                font-family: 'JetBrains Mono', monospace;
                color: {c["accent"]} !important;
                font-size: 0.82rem;
            }}

            /* ── Dividers ───────────────────────────────────────────────── */
            hr {{
                border-color: {c["border"]} !important;
                opacity: 0.6;
            }}

            /* ── Dataframes ─────────────────────────────────────────────── */
            [data-testid="stDataFrame"] {{
                border: 1px solid {c["border"]};
                border-radius: 8px;
            }}

            /* ── Risk scale indicators ──────────────────────────────────── */
            .risk-scale {{
                display: flex;
                gap: 0.5rem;
                margin-top: 0.5rem;
            }}

            .risk-level {{
                flex: 1;
                text-align: center;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.04em;
                padding: 0.45rem 0.25rem;
                border-radius: 6px;
                border: 1px solid {c["border"]};
                background: {c["bg_card"]};
            }}

            .risk-low {{ color: {c["success"]}; border-color: rgba(0, 200, 83, 0.3); }}
            .risk-medium {{ color: {c["warning"]}; border-color: rgba(255, 140, 0, 0.3); }}
            .risk-high {{ color: #FF6B35; border-color: rgba(255, 107, 53, 0.3); }}
            .risk-critical {{ color: {c["danger"]}; border-color: rgba(255, 59, 59, 0.4); }}

            /* ── Console nav tiles ──────────────────────────────────────── */
            .nav-tile {{
                display: block;
                background: {c["bg_card"]};
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 1.25rem;
                text-decoration: none;
                transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
                height: 100%;
            }}

            .nav-tile:hover {{
                border-color: rgba(255, 59, 59, 0.5);
                box-shadow: 0 0 20px rgba(255, 59, 59, 0.15);
                transform: translateY(-2px);
            }}

            .nav-tile .nav-tile-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["accent"]};
                margin-bottom: 0.4rem;
            }}

            .nav-tile .nav-tile-title {{
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                font-weight: 600;
                color: {c["text_primary"]};
                margin-bottom: 0.35rem;
            }}

            .nav-tile .nav-tile-desc {{
                font-size: 0.8rem;
                color: {c["text_muted"]};
                line-height: 1.5;
                margin: 0;
            }}

            /* ── Landing page (home hero) ─────────────────────────────── */
            html {{
                scroll-behavior: smooth;
            }}

            .home-landing [data-testid="stMain"] > div:first-child {{
                padding-top: 0;
            }}

            .home-landing .block-container {{
                max-width: 100%;
                padding: 0;
            }}

            .home-landing [data-testid="stMarkdownContainer"]:has(.hero-landing) {{
                padding: 0;
                margin: 0;
                max-width: none;
            }}

            .home-landing [data-testid="stHtml"] {{
                padding: 0;
                margin: 0;
                max-width: none;
            }}

            .home-landing [data-testid="stHtml"] iframe {{
                border: none;
            }}

            .hero-landing {{
                position: relative;
                min-height: 92vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                padding: 2rem 1.5rem 3rem;
                width: 100%;
            }}

            .hero-landing::before {{
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(ellipse 55% 45% at 50% 50%, rgba(255, 59, 59, 0.08) 0%, transparent 70%);
                pointer-events: none;
                z-index: 0;
            }}

            .hero-grid {{
                position: absolute;
                inset: 0;
                background-image:
                    linear-gradient(rgba(255, 59, 59, 0.09) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 59, 59, 0.09) 1px, transparent 1px),
                    linear-gradient(rgba(255, 59, 59, 0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 59, 59, 0.04) 1px, transparent 1px);
                background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
                animation: hero-grid-drift 28s linear infinite;
                mask-image: radial-gradient(ellipse 75% 70% at 50% 50%, black 20%, transparent 78%);
                -webkit-mask-image: radial-gradient(ellipse 75% 70% at 50% 50%, black 20%, transparent 78%);
                pointer-events: none;
                z-index: 0;
            }}

            @keyframes hero-grid-drift {{
                0% {{ background-position: 0 0, 0 0, 0 0, 0 0; }}
                100% {{ background-position: 80px 80px, 80px 80px, 20px 20px, 20px 20px; }}
            }}

            .hero-scanline {{
                position: absolute;
                inset: 0;
                background: linear-gradient(
                    180deg,
                    transparent 0%,
                    rgba(255, 59, 59, 0.03) 48%,
                    rgba(255, 59, 59, 0.06) 50%,
                    rgba(255, 59, 59, 0.03) 52%,
                    transparent 100%
                );
                background-size: 100% 220px;
                animation: hero-scan 9s linear infinite;
                pointer-events: none;
                z-index: 0;
                opacity: 0.55;
            }}

            @keyframes hero-scan {{
                0% {{ background-position: 0 -220px; }}
                100% {{ background-position: 0 100vh; }}
            }}

            .hero-inner {{
                position: relative;
                z-index: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                max-width: 900px;
                width: 100%;
                margin: 0 auto;
                gap: 1.35rem;
                text-align: center;
            }}

            .hero-inner::before {{
                content: "";
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                max-width: 900px;
                height: 115%;
                background:
                    radial-gradient(ellipse 75% 58% at 50% 48%, rgba(255, 59, 59, 0.16) 0%, transparent 62%),
                    radial-gradient(ellipse 45% 32% at 50% 88%, rgba(179, 0, 0, 0.22) 0%, transparent 55%);
                pointer-events: none;
                z-index: -1;
            }}

            .hero-icon {{
                display: flex;
                flex-shrink: 0;
                align-items: center;
                justify-content: center;
                width: 56px;
                height: 56px;
                margin: 0;
                color: {c["accent"]};
                border-radius: 14px;
                background: linear-gradient(145deg, rgba(255, 59, 59, 0.18) 0%, rgba(17, 17, 17, 0.9) 100%);
                border: 1px solid rgba(255, 59, 59, 0.45);
                box-shadow: 0 0 28px rgba(255, 59, 59, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.06);
                animation: hero-icon-glow 3.5s ease-in-out infinite;
            }}

            @keyframes hero-icon-glow {{
                0%, 100% {{ box-shadow: 0 0 28px rgba(255, 59, 59, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.06); }}
                50% {{ box-shadow: 0 0 42px rgba(255, 59, 59, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.08); }}
            }}

            .hero-icon svg {{
                width: 28px;
                height: 28px;
                fill: none;
                stroke: {c["accent"]};
                stroke-width: 1.75;
                filter: drop-shadow(0 0 6px rgba(255, 59, 59, 0.55));
            }}

            .hero-eyebrow {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                font-weight: 600;
                letter-spacing: 0.22em;
                text-transform: uppercase;
                color: {c["accent"]};
                margin: 0;
                text-shadow: 0 0 18px rgba(255, 59, 59, 0.35);
            }}

            .hero-title {{
                font-family: 'Inter', sans-serif;
                font-size: clamp(2.4rem, 5.5vw, 4rem);
                font-weight: 800;
                line-height: 1.08;
                letter-spacing: -0.03em;
                color: {c["text_primary"]};
                margin: 0;
                text-shadow: 0 0 40px rgba(255, 59, 59, 0.12);
            }}

            .hero-tagline {{
                font-family: 'Inter', sans-serif;
                font-size: clamp(1.05rem, 2.2vw, 1.35rem);
                font-weight: 600;
                color: {c["text_primary"]};
                margin: 0 0 1rem 0;
                opacity: 0.92;
            }}

            .hero-description {{
                font-family: 'Inter', sans-serif;
                font-size: clamp(0.95rem, 1.8vw, 1.08rem);
                line-height: 1.7;
                color: {c["text_muted"]};
                max-width: 600px;
                width: 100%;
                margin: 0;
                text-align: center;
            }}

            .hero-actions {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 0.85rem;
                margin: 0;
                width: 100%;
            }}

            .hero-btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 180px;
                padding: 0.82rem 1.65rem;
                border-radius: 10px;
                font-family: 'Inter', sans-serif;
                font-size: 0.92rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                text-decoration: none;
                transition: transform 0.2s ease, box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease;
                cursor: pointer;
            }}

            .hero-btn-primary {{
                background: linear-gradient(135deg, {c["accent"]} 0%, {c["accent_dark"]} 100%);
                color: {c["text_primary"]};
                border: 1px solid {c["accent_dark"]};
                box-shadow: 0 0 24px rgba(255, 59, 59, 0.25);
            }}

            .hero-btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 0 36px rgba(255, 59, 59, 0.45);
                border-color: {c["accent"]};
                color: {c["text_primary"]};
            }}

            .hero-btn-secondary {{
                background: rgba(26, 26, 26, 0.85);
                color: {c["text_primary"]};
                border: 1px solid {c["border"]};
                backdrop-filter: blur(8px);
            }}

            .hero-btn-secondary:hover {{
                transform: translateY(-2px);
                border-color: rgba(255, 59, 59, 0.5);
                box-shadow: 0 0 22px rgba(255, 59, 59, 0.14);
                color: {c["text_primary"]};
            }}

            .hero-stats {{
                display: flex;
                flex-direction: row;
                flex-wrap: wrap;
                align-items: stretch;
                justify-content: center;
                gap: 1rem;
                width: 100%;
                max-width: 720px;
                margin: 0;
            }}

            @media (max-width: 640px) {{
                .hero-stats {{
                    flex-direction: column;
                    align-items: center;
                    max-width: 280px;
                }}
            }}

            .hero-stat {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                flex: 1 1 0;
                min-width: 140px;
                max-width: 220px;
                background: linear-gradient(160deg, rgba(17, 17, 17, 0.92) 0%, rgba(26, 26, 26, 0.88) 100%);
                border: 1px solid rgba(255, 59, 59, 0.22);
                border-radius: 12px;
                padding: 1.15rem 1rem;
                transition: transform 0.2s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            }}

            @media (max-width: 640px) {{
                .hero-stat {{
                    width: 100%;
                    max-width: none;
                }}
            }}

            .hero-stat:hover {{
                transform: translateY(-3px);
                border-color: rgba(255, 59, 59, 0.55);
                box-shadow: 0 0 28px rgba(255, 59, 59, 0.18);
            }}

            .hero-stat-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.45rem;
            }}

            .hero-stat-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: clamp(1.35rem, 3vw, 1.75rem);
                font-weight: 700;
                color: {c["accent"]};
                text-shadow: 0 0 16px rgba(255, 59, 59, 0.25);
            }}

            .landing-section {{
                scroll-margin-top: 1.5rem;
                max-width: 1100px;
                margin: 0 auto;
                padding: 2.5rem 1.5rem 3rem;
            }}

            .landing-section-header {{
                text-align: center;
                margin-bottom: 1.75rem;
            }}

            .landing-section-header h2 {{
                font-family: 'Inter', sans-serif !important;
                font-size: 1.65rem !important;
                font-weight: 700 !important;
                margin: 0 0 0.5rem 0 !important;
            }}

            .landing-section-header p {{
                color: {c["text_muted"]};
                font-size: 0.95rem;
                margin: 0;
            }}

            .landing-panel {{
                background: linear-gradient(160deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 14px;
                padding: 1.75rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }}

            .landing-panel:hover {{
                border-color: rgba(255, 59, 59, 0.35);
                box-shadow: 0 0 24px rgba(255, 59, 59, 0.1), 0 8px 32px rgba(0, 0, 0, 0.4);
            }}

            /* ── Home primary CTA (Start Analysis) ────────────────────── */
            .hero-cta-wrapper {{
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin-top: 2.75rem;
                margin-bottom: 2.5rem;
                padding: 0 1rem;
            }}

            .hero-landing .hero-cta-wrapper a,
            .hero-landing a.hero-cta-btn,
            a.hero-cta-btn {{
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 280px !important;
                height: 60px !important;
                min-height: 60px !important;
                max-width: 280px !important;
                padding: 0 1.25rem !important;
                box-sizing: border-box !important;
                border-radius: 10px !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.95rem !important;
                font-weight: 700 !important;
                letter-spacing: 0.06em !important;
                text-transform: uppercase !important;
                color: #f5f5f5 !important;
                background: #6b1414 !important;
                border: 1px solid #4a1a1a !important;
                text-decoration: none !important;
                box-shadow:
                    0 0 16px rgba(107, 20, 20, 0.2),
                    0 0 32px rgba(107, 20, 20, 0.08),
                    0 6px 20px rgba(0, 0, 0, 0.5);
                transition:
                    transform 0.25s ease,
                    box-shadow 0.3s ease,
                    background 0.25s ease,
                    border-color 0.25s ease;
                cursor: pointer;
                animation: hero-cta-glow 2.8s ease-in-out infinite;
            }}

            @media (max-width: 400px) {{
                .hero-landing .hero-cta-wrapper a,
                .hero-landing a.hero-cta-btn,
                a.hero-cta-btn {{
                    width: min(280px, calc(100vw - 3rem)) !important;
                    max-width: min(280px, calc(100vw - 3rem)) !important;
                }}
            }}

            @keyframes hero-cta-glow {{
                0%, 100% {{
                    box-shadow:
                        0 0 16px rgba(92, 18, 18, 0.2),
                        0 0 32px rgba(92, 18, 18, 0.08),
                        0 6px 20px rgba(0, 0, 0, 0.5);
                }}
                50% {{
                    box-shadow:
                        0 0 22px rgba(92, 18, 18, 0.26),
                        0 0 40px rgba(92, 18, 18, 0.12),
                        0 6px 20px rgba(0, 0, 0, 0.5);
                }}
            }}

            .hero-landing .hero-cta-wrapper a:hover,
            .hero-landing a.hero-cta-btn:hover,
            a.hero-cta-btn:hover {{
                transform: translateY(-3px);
                background: #551010 !important;
                border-color: #3d1414 !important;
                box-shadow:
                    0 0 24px rgba(85, 16, 16, 0.28),
                    0 0 44px rgba(85, 16, 16, 0.14),
                    0 10px 28px rgba(0, 0, 0, 0.58);
                color: #ffffff !important;
                animation: none;
            }}

            .hero-landing .hero-cta-wrapper a:active,
            .hero-landing a.hero-cta-btn:active,
            a.hero-cta-btn:active {{
                transform: translateY(-1px);
            }}

            /* ── Workflow pipeline ─────────────────────────────────────── */
            .workflow-section {{
                max-width: 520px;
                margin: 0 auto;
                padding: 2rem 1.5rem 4rem;
                text-align: center;
            }}

            .workflow-heading {{
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 0.68rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: {c["accent"]} !important;
                margin: 0 0 1.5rem 0 !important;
            }}

            .workflow-pipeline {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.5rem;
            }}

            .workflow-step {{
                width: 100%;
                max-width: 320px;
                background: linear-gradient(160deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 0.85rem 1.25rem;
                font-family: 'Inter', sans-serif;
                font-size: 0.92rem;
                font-weight: 600;
                color: {c["text_primary"]};
            }}

            .workflow-step-final {{
                border-color: rgba(255, 59, 59, 0.45);
                box-shadow: 0 0 20px rgba(255, 59, 59, 0.12);
            }}

            .workflow-arrow {{
                font-size: 1.1rem;
                color: {c["accent"]};
                line-height: 1;
                opacity: 0.7;
            }}

            /* ── Prediction result panel ───────────────────────────────── */
            .prediction-panel {{
                border-radius: 10px;
                padding: 1.35rem;
                margin-top: 0.25rem;
            }}

            .prediction-panel-attack {{
                background: linear-gradient(160deg, rgba(255, 59, 59, 0.14) 0%, {c["bg_elevated"]} 100%);
                border: 1px solid rgba(255, 59, 59, 0.45);
                box-shadow: 0 0 32px rgba(255, 59, 59, 0.18);
            }}

            .prediction-panel-normal {{
                background: linear-gradient(160deg, rgba(0, 200, 83, 0.08) 0%, {c["bg_elevated"]} 100%);
                border: 1px solid rgba(0, 200, 83, 0.35);
                box-shadow: 0 0 24px rgba(0, 200, 83, 0.08);
            }}

            .prediction-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.35rem;
            }}

            .prediction-value {{
                font-family: 'Inter', sans-serif;
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: -0.02em;
                margin-bottom: 1.25rem;
                line-height: 1.1;
            }}

            .prediction-value-attack {{
                color: {c["danger"]};
                text-shadow: 0 0 24px rgba(255, 59, 59, 0.35);
            }}

            .prediction-value-normal {{
                color: {c["success"]};
            }}

            .prediction-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.75rem;
                margin-bottom: 1.25rem;
            }}

            .prediction-metric {{
                background: rgba(0, 0, 0, 0.25);
                border: 1px solid {c["border"]};
                border-radius: 8px;
                padding: 0.75rem 0.85rem;
            }}

            .prediction-metric-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.3rem;
            }}

            .prediction-metric-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.15rem;
                font-weight: 700;
                color: {c["text_primary"]};
            }}

            .prediction-risk-critical {{ color: {c["danger"]}; }}
            .prediction-risk-high {{ color: #FF6B35; }}
            .prediction-risk-medium {{ color: {c["warning"]}; }}
            .prediction-risk-low {{ color: {c["success"]}; }}
            .prediction-risk-minimal {{ color: {c["text_muted"]}; }}

            .prediction-action {{
                background: {c["bg_card"]};
                border: 1px solid {c["border"]};
                border-left: 3px solid {c["accent"]};
                border-radius: 8px;
                padding: 0.85rem 1rem;
            }}

            .prediction-action-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["accent"]};
                margin-bottom: 0.4rem;
            }}

            .prediction-action-text {{
                font-family: 'Inter', sans-serif;
                font-size: 0.88rem;
                color: {c["text_muted"]};
                line-height: 1.55;
                margin: 0;
            }}

            .prediction-placeholder {{
                text-align: center;
                padding: 2.5rem 1.25rem;
            }}

            .prediction-placeholder-title {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.72rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c["text_dim"]};
                margin: 0 0 0.65rem 0;
            }}

            .prediction-placeholder-text {{
                font-size: 0.88rem;
                color: {c["text_dim"]};
                line-height: 1.6;
                margin: 0;
                max-width: 320px;
                margin-left: auto;
                margin-right: auto;
            }}

            /* ── Analysis dashboard components ─────────────────────────── */
            .analysis-result-extras {{
                display: grid;
                grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
                gap: 0.85rem;
                margin-top: 0.85rem;
            }}

            .risk-gauge-panel {{
                background: linear-gradient(160deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 0.85rem 0.75rem 0.7rem;
                text-align: center;
            }}

            .risk-gauge-title {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.35rem;
            }}

            .risk-gauge-svg {{
                width: 100%;
                max-width: 168px;
                height: auto;
                display: block;
                margin: 0 auto;
            }}

            .risk-gauge-track {{
                fill: none;
                stroke: {c["border"]};
                stroke-width: 10;
                stroke-linecap: round;
            }}

            .risk-gauge-fill {{
                fill: none;
                stroke-width: 10;
                stroke-linecap: round;
                transition: stroke-dashoffset 0.6s ease;
            }}

            .risk-gauge-fill-critical {{ stroke: {c["danger"]}; filter: drop-shadow(0 0 6px rgba(255, 59, 59, 0.55)); }}
            .risk-gauge-fill-high {{ stroke: #FF6B35; filter: drop-shadow(0 0 5px rgba(255, 107, 53, 0.45)); }}
            .risk-gauge-fill-medium {{ stroke: {c["warning"]}; }}
            .risk-gauge-fill-low {{ stroke: {c["success"]}; }}
            .risk-gauge-fill-minimal {{ stroke: {c["text_dim"]}; }}

            .risk-gauge-needle {{
                fill: {c["text_primary"]};
                filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.35));
            }}

            .risk-gauge-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.35rem;
                font-weight: 700;
                color: {c["text_primary"]};
                margin-top: -0.15rem;
                line-height: 1.1;
            }}

            .risk-gauge-label {{
                font-family: 'Inter', sans-serif;
                font-size: 0.78rem;
                font-weight: 600;
                margin-top: 0.2rem;
            }}

            .risk-gauge-label-critical {{ color: {c["danger"]}; }}
            .risk-gauge-label-high {{ color: #FF6B35; }}
            .risk-gauge-label-medium {{ color: {c["warning"]}; }}
            .risk-gauge-label-low {{ color: {c["success"]}; }}
            .risk-gauge-label-minimal {{ color: {c["text_muted"]}; }}

            .attack-type-panel {{
                background: linear-gradient(160deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 0.85rem 1rem;
            }}

            .attack-type-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.5rem;
                margin-bottom: 0.55rem;
            }}

            .attack-type-title {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["text_muted"]};
            }}

            .attack-type-name {{
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                font-weight: 700;
                color: {c["text_primary"]};
                margin-bottom: 0.4rem;
                line-height: 1.25;
            }}

            .attack-type-desc {{
                font-size: 0.8rem;
                color: {c["text_muted"]};
                line-height: 1.5;
                margin: 0 0 0.55rem 0;
            }}

            .attack-type-indicators {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.35rem;
            }}

            .attack-indicator {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.58rem;
                font-weight: 500;
                letter-spacing: 0.04em;
                padding: 0.2rem 0.45rem;
                border-radius: 4px;
                background: rgba(255, 59, 59, 0.1);
                color: {c["accent"]};
                border: 1px solid rgba(255, 59, 59, 0.28);
            }}

            .attack-indicator-safe {{
                background: rgba(0, 200, 83, 0.08);
                color: {c["success"]};
                border-color: rgba(0, 200, 83, 0.28);
            }}

            .threat-stats-grid {{
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.85rem;
            }}

            .threat-stat-card {{
                background: linear-gradient(145deg, {c["bg_card"]} 0%, {c["bg_elevated"]} 100%);
                border: 1px solid {c["border"]};
                border-radius: 10px;
                padding: 0.95rem 1.1rem;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.28);
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }}

            .threat-stat-card:hover {{
                border-color: rgba(255, 59, 59, 0.4);
                box-shadow: 0 0 14px rgba(255, 59, 59, 0.1);
            }}

            .threat-stat-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.62rem;
                font-weight: 600;
                letter-spacing: 0.09em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                margin-bottom: 0.35rem;
            }}

            .threat-stat-value {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.45rem;
                font-weight: 700;
                color: {c["accent"]};
                line-height: 1.1;
            }}

            .threat-stat-value-danger {{ color: {c["danger"]}; }}
            .threat-stat-value-success {{ color: {c["success"]}; }}

            .threat-stat-sub {{
                font-size: 0.72rem;
                color: {c["text_dim"]};
                margin-top: 0.3rem;
            }}

            .analysis-history-wrap {{
                overflow-x: auto;
                margin-top: 0.25rem;
            }}

            .analysis-history-table {{
                width: 100%;
                border-collapse: collapse;
                font-family: 'Inter', sans-serif;
                font-size: 0.82rem;
                min-width: 1080px;
            }}

            .analysis-history-table thead th {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: {c["text_muted"]};
                text-align: left;
                padding: 0.65rem 0.85rem;
                border-bottom: 1px solid {c["border"]};
                background: {c["bg_elevated"]};
            }}

            .analysis-history-table tbody td {{
                padding: 0.62rem 0.85rem;
                color: {c["text_muted"]};
                border-bottom: 1px solid rgba(42, 42, 42, 0.65);
                vertical-align: middle;
            }}

            .analysis-history-table tbody tr:hover td {{
                background: rgba(255, 59, 59, 0.04);
                color: {c["text_primary"]};
            }}

            .analysis-history-table tbody tr:last-child td {{
                border-bottom: none;
            }}

            .history-pred-attack {{
                color: {c["danger"]};
                font-weight: 600;
            }}

            .history-pred-normal {{
                color: {c["success"]};
                font-weight: 600;
            }}

            .history-risk-critical {{ color: {c["danger"]}; }}
            .history-risk-high {{ color: #FF6B35; }}
            .history-risk-medium {{ color: {c["warning"]}; }}
            .history-risk-low {{ color: {c["success"]}; }}
            .history-risk-minimal {{ color: {c["text_dim"]}; }}

            .history-ua {{
                max-width: 220px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .history-volume {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.74rem;
                white-space: nowrap;
            }}

            .history-internal-yes {{
                color: {c["warning"]};
                font-weight: 600;
            }}

            .history-internal-no {{
                color: {c["text_dim"]};
            }}

            .analysis-history-empty {{
                text-align: center;
                padding: 1.75rem 1rem;
                color: {c["text_dim"]};
                font-size: 0.85rem;
            }}

            @media (max-width: 1100px) {{
                .threat-stats-grid {{
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }}
            }}

            @media (max-width: 768px) {{
                .analysis-result-extras {{
                    grid-template-columns: 1fr;
                }}

                .threat-stats-grid {{
                    grid-template-columns: 1fr 1fr;
                }}
            }}

            @media (max-width: 480px) {{
                .threat-stats-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def soc_status_bar(
    console: str = "SOC-01",
    posture: str = "MONITORING",
    threats: str = "0 ACTIVE",
    model: str = "STANDBY",
) -> None:
    """Render a compact SOC operations status strip."""
    st.markdown(
        f"""
        <div class="soc-status-bar">
            <span class="soc-item"><span class="soc-pulse"></span><strong>{console}</strong> · LIVE</span>
            <span class="soc-item">Posture: <strong>{posture}</strong></span>
            <span class="soc-item">Threats: <strong style="color:#FF3B3B;">{threats}</strong></span>
            <span class="soc-item">Model: <strong>{model}</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", badge: str = "") -> None:
    """Render a consistent page header."""
    if badge:
        st.markdown(f'<p class="cyber-header">{badge}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="cyber-title">{title}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="cyber-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def cyber_card(title: str, body: str, variant: str = "accent") -> None:
    """Render a themed info card."""
    st.markdown(
        f"""
        <div class="cyber-card cyber-card-{variant}">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", delta_type: str = "neutral") -> None:
    """Render a glowing KPI card with optional delta indicator."""
    delta_html = ""
    if delta:
        delta_html = f'<div class="kpi-delta kpi-delta-{delta_type}">{delta}</div>'
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_divider(label: str) -> None:
    """Render a labeled section divider."""
    st.markdown(f'<p class="section-label">{label}</p>', unsafe_allow_html=True)


def plotly_soc_layout(fig, height: int = 380, xaxis_title: str = "", yaxis_title: str = ""):
    """Apply dark SOC styling to a Plotly figure."""
    layout = {**PLOTLY_LAYOUT, "height": height}
    if xaxis_title:
        layout["xaxis"] = {**PLOTLY_LAYOUT["xaxis"], "title": xaxis_title}
    if yaxis_title:
        layout["yaxis"] = {**PLOTLY_LAYOUT["yaxis"], "title": yaxis_title}
    return fig.update_layout(**layout)


def prediction_panel(
    prediction: str,
    confidence: float,
    risk: str,
    risk_variant: str,
    action: str,
    variant: str = "normal",
) -> None:
    """Render a prominent threat classification result panel."""
    value_class = "prediction-value-attack" if variant == "attack" else "prediction-value-normal"
    panel_class = f"prediction-panel prediction-panel-{variant}"
    st.markdown(
        f"""
        <div class="{panel_class}">
            <div class="prediction-label">Classification</div>
            <div class="prediction-value {value_class}">{prediction}</div>
            <div class="prediction-metrics">
                <div class="prediction-metric">
                    <div class="prediction-metric-label">Confidence</div>
                    <div class="prediction-metric-value">{confidence:.1%}</div>
                </div>
                <div class="prediction-metric">
                    <div class="prediction-metric-label">Risk Level</div>
                    <div class="prediction-metric-value prediction-risk-{risk_variant}">{risk}</div>
                </div>
            </div>
            <div class="prediction-action">
                <div class="prediction-action-label">Recommended Action</div>
                <p class="prediction-action-text">{action}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_gauge(score: float, risk: str, risk_variant: str) -> None:
    """Render a semicircular threat risk gauge (score 0.0–1.0)."""
    clamped = max(0.0, min(1.0, score))
    arc_length = 157.08
    dash_offset = arc_length * (1.0 - clamped)
    angle = -90 + (clamped * 180)
    needle_x = 100 + 58 * math.cos(math.radians(angle))
    needle_y = 100 + 58 * math.sin(math.radians(angle))
    st.markdown(
        f"""
        <div class="risk-gauge-panel">
            <div class="risk-gauge-title">Threat Risk Meter</div>
            <svg viewBox="0 0 200 115" class="risk-gauge-svg" aria-hidden="true">
                <path class="risk-gauge-track"
                      d="M 30 100 A 70 70 0 0 1 170 100" />
                <path class="risk-gauge-fill risk-gauge-fill-{risk_variant}"
                      d="M 30 100 A 70 70 0 0 1 170 100"
                      stroke-dasharray="{arc_length:.2f}"
                      stroke-dashoffset="{dash_offset:.2f}" />
                <circle class="risk-gauge-needle" cx="{needle_x:.1f}" cy="{needle_y:.1f}" r="5" />
            </svg>
            <div class="risk-gauge-value">{clamped:.0%}</div>
            <div class="risk-gauge-label risk-gauge-label-{risk_variant}">{risk} Risk</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def attack_type_panel(
    attack_type: str,
    description: str,
    indicators: list[str],
    *,
    is_threat: bool = True,
) -> None:
    """Render inferred attack type details and behavioral indicators."""
    badge_class = "badge-alert" if is_threat else "badge-secure"
    badge_text = "Threat" if is_threat else "Clear"
    indicator_items = "".join(
        f'<span class="attack-indicator{"" if is_threat else " attack-indicator-safe"}">{item}</span>'
        for item in indicators
    )
    st.markdown(
        f"""
        <div class="attack-type-panel">
            <div class="attack-type-header">
                <span class="attack-type-title">Attack Type Analysis</span>
                <span class="cyber-badge {badge_class}">{badge_text}</span>
            </div>
            <div class="attack-type-name">{attack_type}</div>
            <p class="attack-type-desc">{description}</p>
            <div class="attack-type-indicators">{indicator_items}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def threat_statistics_row(
    total_scans: int,
    threats_detected: int,
    clean_traffic: int,
    avg_threat_score: float,
) -> None:
    """Render a four-column threat statistics summary."""
    st.markdown(
        f"""
        <div class="threat-stats-grid">
            <div class="threat-stat-card">
                <div class="threat-stat-label">Total Scans</div>
                <div class="threat-stat-value">{total_scans}</div>
                <div class="threat-stat-sub">Session analyses</div>
            </div>
            <div class="threat-stat-card">
                <div class="threat-stat-label">Threats Detected</div>
                <div class="threat-stat-value threat-stat-value-danger">{threats_detected}</div>
                <div class="threat-stat-sub">Attack classifications</div>
            </div>
            <div class="threat-stat-card">
                <div class="threat-stat-label">Clean Traffic</div>
                <div class="threat-stat-value threat-stat-value-success">{clean_traffic}</div>
                <div class="threat-stat-sub">Normal classifications</div>
            </div>
            <div class="threat-stat-card">
                <div class="threat-stat-label">Avg Threat Score</div>
                <div class="threat-stat-value">{avg_threat_score:.0%}</div>
                <div class="threat-stat-sub">Mean attack probability</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def analysis_history_table(entries: list[dict]) -> None:
    """Render a styled recent-analysis history table."""
    if not entries:
        st.markdown(
            '<div class="analysis-history-empty">No analyses recorded yet. Run a prediction to populate history.</div>',
            unsafe_allow_html=True,
        )
        return

    rows = []
    for entry in entries:
        pred_class = "history-pred-attack" if entry["prediction"] == "Attack" else "history-pred-normal"
        volume = entry.get("volume")
        if not volume:
            sent = entry.get("bytes_sent", 0)
            recv = entry.get("bytes_received", 0)
            volume = f"{int(sent):,} / {int(recv):,}"

        ua_short = entry.get("user_agent_short") or entry.get("user_agent", "—")
        confidence = entry.get("confidence", entry.get("score", 0.0))
        internal = entry.get("internal", False)
        internal_label = "Yes" if internal else "No"
        internal_class = "history-internal-yes" if internal else "history-internal-no"

        ua_full = html.escape(entry.get("user_agent", ua_short))
        ua_short_safe = html.escape(ua_short)
        attack_type = html.escape(str(entry["attack_type"]))
        rows.append(
            f"""
            <tr>
                <td>{entry["time"]}</td>
                <td>{entry["protocol"]}</td>
                <td>{entry["ports"]}</td>
                <td class="history-volume">{volume}</td>
                <td class="history-ua" title="{ua_full}">{ua_short_safe}</td>
                <td class="{internal_class}">{internal_label}</td>
                <td class="{pred_class}">{entry["prediction"]}</td>
                <td>{confidence:.0%}</td>
                <td class="history-risk-{entry["risk_variant"]}">{entry["risk"]}</td>
                <td>{attack_type}</td>
                <td>{entry["score"]:.0%}</td>
            </tr>
            """
        )

    table_html = f"""
        <div class="analysis-history-wrap">
            <table class="analysis-history-table">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Protocol</th>
                        <th>Ports</th>
                        <th>Bytes (S/R)</th>
                        <th>User Agent</th>
                        <th>Internal</th>
                        <th>Result</th>
                        <th>Confidence</th>
                        <th>Risk</th>
                        <th>Attack Type</th>
                        <th>Threat Score</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        """

    st.html(table_html)
