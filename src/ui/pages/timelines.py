"""
timelines.py — Timeline visualizations page.

Monthly area, daily area (with range slider), hourly bar, 3D timeline scatter.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analytics.timeline import (
    monthly_timeline,
    daily_timeline,
    hourly_distribution,
    build_3d_timeline_data,
)
from src.visualization.charts import (
    plot_monthly_timeline,
    plot_daily_timeline,
    plot_hourly_bar,
    plot_3d_timeline,
)


def render(option: str, df: pd.DataFrame) -> None:

    # ── Monthly ────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">📅 Monthly Message Volume</p>', unsafe_allow_html=True)
    mt = monthly_timeline(option, df)
    if not mt.empty:
        st.plotly_chart(plot_monthly_timeline(mt), width='stretch')
    else:
        st.info("Not enough data for monthly timeline.")

    # ── Daily ──────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">📆 Daily Message Volume</p>', unsafe_allow_html=True)
    dt = daily_timeline(option, df)
    if not dt.empty:
        st.plotly_chart(plot_daily_timeline(dt), width='stretch')
    else:
        st.info("Not enough data for daily timeline.")

    # ── Hourly Distribution ────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">🕐 Messages by Hour of Day</p>', unsafe_allow_html=True)
    hd = hourly_distribution(option, df)
    st.plotly_chart(plot_hourly_bar(hd), width='stretch')

    # ── 3-D Timeline ──────────────────────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🌐 3-D Message Scatter (Day × Hour × Count)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="glass-card" style="padding:8px 12px; font-size:0.82rem; color:var(--muted);">'
        "💡 Rotate the 3-D chart by dragging · Scroll to zoom · Double-click to reset"
        "</div>",
        unsafe_allow_html=True,
    )
    df_3d = build_3d_timeline_data(option, df)
    fig_3d = plot_3d_timeline(df_3d, title="3-D Message Timeline · Day Index × Hour × Count")
    st.plotly_chart(fig_3d, width='stretch')
