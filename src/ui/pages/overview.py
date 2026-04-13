"""
overview.py — Overview / Stats page.

KPI cards, health score gauge, busy users, response times.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analytics.stats import fetch_stats, busy_users, conversation_health_score
from src.preprocess.parser import compute_response_times
from src.visualization.charts import (
    plot_health_gauge,
    plot_busy_users_bar,
    plot_response_time_bar,
)


def _kpi_card(icon: str, label: str, value: str, sub: str = "") -> str:
    return f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """


def render(option: str, df: pd.DataFrame, response_times: pd.Series) -> None:
    # ── KPI Strip ──────────────────────────────────────────────────────────────
    stats = fetch_stats(option, df)

    st.markdown('<p class="section-heading">📊 Key Metrics</p>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        ("💬", "Messages",     f"{stats['total_messages']:,}",  ""),
        ("📝", "Words",        f"{stats['total_words']:,}",      ""),
        ("🖼",  "Media",        f"{stats['media_shared']:,}",    ""),
        ("🔗", "Links",        f"{stats['links_shared']:,}",     ""),
        ("📅", "Active Days",  f"{stats['active_days']:,}",      ""),
        ("📈", "Avg / Day",    f"{stats['avg_per_day']}",        "messages"),
    ]
    for col, (icon, label, value, sub) in zip(
        [c1, c2, c3, c4, c5, c6], cards
    ):
        with col:
            st.markdown(_kpi_card(icon, label, value, sub), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Health Score & Response Times ──────────────────────────────────────────
    col_g, col_r = st.columns([1, 1])

    with col_g:
        st.markdown(
            '<p class="section-heading">💚 Conversation Health</p>',
            unsafe_allow_html=True,
        )
        score = conversation_health_score(df)
        badge_class = (
            "health-good" if score >= 70 else
            "health-average" if score >= 40 else
            "health-poor"
        )
        label = "Thriving" if score >= 70 else ("Moderate" if score >= 40 else "Needs Work")
        st.markdown(
            f'<span class="health-badge {badge_class}">{label} — {score}/100</span>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            plot_health_gauge(score),
            width='stretch',
            config={"displayModeBar": False},
        )

    with col_r:
        st.markdown(
            '<p class="section-heading">⏱ Response Times</p>',
            unsafe_allow_html=True,
        )
        if response_times is not None and not response_times.empty:
            rt = response_times
            if option != "Overall" and option in rt.index:
                rt = rt[[option]]
            elif option != "Overall":
                st.info("No response data available for this user.")
                rt = pd.Series(dtype=float)
            if not rt.empty:
                st.plotly_chart(
                    plot_response_time_bar(rt),
                    width='stretch',
                    config={"displayModeBar": False},
                )
        else:
            st.info("Response time data unavailable for single-participant chats.")

    # ── Busiest Users (Overall only) ───────────────────────────────────────────
    if option == "Overall":
        st.markdown(
            '<p class="section-heading">🏆 Most Active Users</p>',
            unsafe_allow_html=True,
        )
        top_series, pct_df = busy_users(df)
        col_b, col_t = st.columns([3, 2])
        with col_b:
            st.plotly_chart(
                plot_busy_users_bar(top_series),
                width='stretch',
                config={"displayModeBar": False},
            )
        with col_t:
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(
                pct_df.rename(columns={"Percent": "Share (%)"}),
                width='stretch',
                hide_index=True,
            )
