"""Shared sidebar navigation for the application."""

import streamlit as st

SHIELD_ICON = """
<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M12 2L4 5.5V11.5C4 16.5 7.5 20.5 12 22C16.5 20.5 20 16.5 20 11.5V5.5L12 2Z"
        stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="1.5"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

BRAND_HTML = f"""
<div class="sidebar-brand-block">
  <div class="sidebar-brand-icon">{SHIELD_ICON}</div>
  <div class="sidebar-brand-copy">
    <span class="sidebar-brand-eyebrow">Security Operations</span>
    <span class="sidebar-brand-title">Cyber Intrusion Blindspot</span>
  </div>
</div>
<div class="sidebar-brand-rule"></div>
"""


def render_sidebar() -> None:
    """Render the SOC-style sidebar with branded header and navigation."""
    with st.sidebar:
        st.markdown(BRAND_HTML, unsafe_allow_html=True)
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link("pages/analysis.py", label="Analysis", icon=":material/manage_search:")
        st.page_link("pages/2_Dashboard.py", label="Dashboard", icon=":material/bar_chart:")
        st.markdown(
            """
            <div class="sidebar-footer">
              <span class="sidebar-status-indicator" aria-hidden="true"></span>
              <span class="sidebar-status-label">Monitoring Active</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
