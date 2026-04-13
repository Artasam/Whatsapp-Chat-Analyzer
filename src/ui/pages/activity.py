"""
activity.py — Activity maps page.

Week/month bars, heatmap, and the 3-D activity landscape.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analytics.activity import (
    week_activity_map,
    month_activity_map,
    activity_heatmap,
    build_3d_activity_data,
)
from src.visualization.charts import (
    plot_week_activity,
    plot_month_activity,
    plot_heatmap,
    plot_3d_activity,
)


def render(option: str, df: pd.DataFrame) -> None:

    # ── Bar Charts ─────────────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">📊 Activity Maps</p>', unsafe_allow_html=True)

    col_w, col_m = st.columns(2)
    with col_w:
        week_data = week_activity_map(option, df)
        st.plotly_chart(plot_week_activity(week_data), width='stretch')
    with col_m:
        month_data = month_activity_map(option, df)
        st.plotly_chart(plot_month_activity(month_data), width='stretch')

    # ── Heatmap ────────────────────────────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🗓 Weekly Activity Heatmap (Weekday × Hour Period)</p>',
        unsafe_allow_html=True,
    )
    pivot = activity_heatmap(option, df)
    if not pivot.empty:
        st.plotly_chart(plot_heatmap(pivot), width='stretch')
    else:
        st.info("Not enough data to render the heatmap.")

    # ── 3-D Activity Landscape ─────────────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🌐 3-D Activity Landscape (Weekday × Hour × Messages)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="glass-card" style="padding:8px 12px; font-size:0.82rem; color:var(--muted);">'
        "💡 Drag to rotate the 3-D landscape · Each bubble = (weekday, hour) pair sized by volume"
        "</div>",
        unsafe_allow_html=True,
    )
    df_3d = build_3d_activity_data(option, df)
    fig_3d = plot_3d_activity(df_3d, title="3-D Activity Landscape · Weekday × Hour × Messages")
    st.plotly_chart(fig_3d, width='stretch')
