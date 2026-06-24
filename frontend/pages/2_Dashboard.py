"""Dashboard — supporting analytics for model performance and dataset overview."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data import CONFUSION_MATRIX, DATASET_STATS, FEATURE_IMPORTANCE, MODEL_METRICS
from utils.nav import render_sidebar
from utils.theme import inject_theme, plotly_soc_layout, section_divider

inject_theme()
render_sidebar()

st.markdown('<p class="cyber-header">Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="cyber-title">Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="cyber-subtitle">Model evaluation metrics and dataset statistics.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    section_divider("Model Metrics")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Accuracy", f"{MODEL_METRICS['accuracy']:.2%}")
    metric_cols[1].metric("Attack Precision", f"{MODEL_METRICS['precision']:.0%}")
    metric_cols[2].metric("Attack Recall", f"{MODEL_METRICS['recall']:.0%}")
    metric_cols[3].metric("Attack F1 Score", f"{MODEL_METRICS['f1_score']:.0%}")

chart_col, matrix_col = st.columns(2, gap="large")

with chart_col:
    with st.container(border=True):
        section_divider("Feature Importance")
        fig = px.bar(
            FEATURE_IMPORTANCE,
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            color_continuous_scale=["#1A1A1A", "#B30000", "#FF3B3B"],
        )
        fig = plotly_soc_layout(fig, height=340, xaxis_title="Importance")
        fig.update_traces(marker_line_width=0)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with matrix_col:
    with st.container(border=True):
        section_divider("Confusion Matrix")
        cm_fig = go.Figure(
            data=go.Heatmap(
                z=CONFUSION_MATRIX.values,
                x=CONFUSION_MATRIX.columns.tolist(),
                y=CONFUSION_MATRIX.index.tolist(),
                colorscale=[[0, "#1A1A1A"], [0.5, "#B30000"], [1, "#FF3B3B"]],
                showscale=True,
                text=CONFUSION_MATRIX.values,
                texttemplate="%{text}",
                textfont={"size": 14, "color": "#FFFFFF"},
            )
        )
        cm_fig = plotly_soc_layout(cm_fig, height=340)
        st.plotly_chart(cm_fig, use_container_width=True)

with st.container(border=True):
    section_divider("Dataset Statistics")
    stats_cols = st.columns(4)
    stats_cols[0].metric("Total Flows", f"{DATASET_STATS['total_flows']:,}")
    stats_cols[1].metric("Normal Flows", f"{DATASET_STATS['normal_flows']:,}")
    stats_cols[2].metric("Attack Flows", f"{DATASET_STATS['attack_flows']:,}")
    stats_cols[3].metric("Features", DATASET_STATS["features"])
