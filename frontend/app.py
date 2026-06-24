"""
Cybersecurity Intrusion Blindspot
Home — landing page and primary entry point.
"""

import streamlit as st

from utils.nav import render_sidebar
from utils.theme import inject_theme

st.set_page_config(
    page_title="Cybersecurity Intrusion Blindspot",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
render_sidebar()

st.markdown('<div class="home-landing">', unsafe_allow_html=True)

SHIELD_SVG = """
<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M12 2L4 5.5V11.5C4 16.5 7.5 20.5 12 22C16.5 20.5 20 16.5 20 11.5V5.5L12 2Z"
        stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>
  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="1.75"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

CTA_STYLE = (
    "display:inline-flex;align-items:center;justify-content:center;"
    "width:280px;height:60px;font-size:0.95rem;font-weight:700;"
    "background:#6b1414;border:1px solid #4a1a1a;border-radius:10px;"
    "color:#f5f5f5;text-decoration:none;box-sizing:border-box;"
    "font-family:Inter,sans-serif;letter-spacing:0.06em;text-transform:uppercase;"
)

st.markdown(
    f"""
    <section class="hero-landing">
        <div class="hero-grid"></div>
        <div class="hero-scanline"></div>
        <div class="hero-inner">
            <div class="hero-icon">{SHIELD_SVG}</div>
            <p class="hero-eyebrow">Cybersecurity Intrusion Blindspot</p>
            <h1 class="hero-title">Network Intrusion<br>Detection System</h1>
            <p class="hero-description">
                Detect malicious network traffic using advanced threat classification
                and real-time traffic analysis.
            </p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-label">Accuracy</div>
                    <div class="hero-stat-value">96.65%</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Attack Recall</div>
                    <div class="hero-stat-value">60%</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Network Flows</div>
                    <div class="hero-stat-value">10,000</div>
                </div>
            </div>
            <div class="hero-cta-wrapper">
                <a href="/analysis" class="hero-cta-btn" style="{CTA_STYLE}">Start Analysis</a>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
