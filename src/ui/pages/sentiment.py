"""
sentiment.py — Sentiment analysis page (VADER-powered, fully offline).

Per-user sentiment bar, rolling sentiment timeline, 3-D sentiment trajectory.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analytics.sentiment import (
    analyze_sentiment,
    sentiment_timeline,
    vader_available,
)
from src.visualization.charts import plot_sentiment_bar, plot_sentiment_3d
import plotly.express as px
from src.config import THEME, PALETTE


def render(option: str, df: pd.DataFrame) -> None:

    # ── VADER availability warning ─────────────────────────────────────────────
    if not vader_available():
        st.error(
            "⚠ **VADER Sentiment library not installed.**\n\n"
            "Run: `pip install vaderSentiment` then restart the app."
        )
        return

    # ── Per-User Sentiment Bar Chart ───────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🧠 Per-User Sentiment Analysis</p>',
        unsafe_allow_html=True,
    )

    try:
        sent_df = analyze_sentiment(option, df)
    except Exception as e:
        st.error(f"Could not compute sentiment: {e}")
        return

    if sent_df.empty:
        st.info("Not enough messages to compute sentiment.")
        return

    col_s, col_t = st.columns([3, 2])
    with col_s:
        st.plotly_chart(
            plot_sentiment_bar(sent_df),
            width='stretch',
            config={"displayModeBar": False},
        )
    with col_t:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            sent_df.rename(columns={
                "users":         "User",
                "avg_score":     "Score",
                "label":         "Sentiment",
                "message_count": "Messages",
            }),
            width='stretch',
            hide_index=True,
        )

    # ── Rolling Sentiment Timeline (2-D) ──────────────────────────────────────
    st.markdown(
        '<p class="section-heading">📈 Rolling Sentiment Over Time</p>',
        unsafe_allow_html=True,
    )

    try:
        tl_df = sentiment_timeline(option, df, window=30)
        if not tl_df.empty:
            if option == "Overall":
                # Show all users as separate lines
                fig_tl = px.line(
                    tl_df,
                    x="date",
                    y="rolling_score",
                    color="users",
                    title="Rolling Sentiment (30-msg window)",
                    labels={"rolling_score": "Sentiment", "date": "Date", "users": "User"},
                    color_discrete_sequence=PALETTE,
                )
            else:
                fig_tl = px.area(
                    tl_df,
                    x="date",
                    y="rolling_score",
                    title=f"Rolling Sentiment — {option}",
                    labels={"rolling_score": "Sentiment", "date": "Date"},
                    color_discrete_sequence=[THEME["primary"]],
                )
            fig_tl.add_hline(
                y=0,
                line_dash="dash",
                line_color=THEME["muted"],
                annotation_text="Neutral",
                annotation_font_color=THEME["muted"],
            )
            fig_tl.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=350,
            )
            st.plotly_chart(fig_tl, width='stretch')
        else:
            st.info("Not enough data for sentiment timeline.")
    except Exception as e:
        st.warning(f"Timeline error: {e}")

    # ── 3-D Sentiment Trajectory ───────────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🌐 3-D Sentiment Trajectory</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="glass-card" style="padding:8px 12px; font-size:0.82rem; color:var(--muted);">'
        "💡 Each line is a user's sentiment journey over messages — rotate to explore patterns"
        "</div>",
        unsafe_allow_html=True,
    )

    # Limit to top-6 users for readability
    top_users = (
        df[df["users"] != "group_notification"]["users"]
        .value_counts()
        .head(6)
        .index.tolist()
    )
    tl_top = sentiment_timeline("Overall", df, window=20)
    tl_top = tl_top[tl_top["users"].isin(top_users)]

    fig_3d = plot_sentiment_3d(tl_top, title="3-D Sentiment Trajectory · Message → User → Score")
    st.plotly_chart(fig_3d, width='stretch')

    # ── Legend / Interpretation ────────────────────────────────────────────────
    st.markdown(
        """
        <div class="glass-card" style="margin-top:12px;">
            <b style="color:var(--text)">How to read VADER scores</b><br><br>
            <span class="sentiment-positive">● ≥ +0.05 → Positive</span> &nbsp;|&nbsp;
            <span class="sentiment-negative">● ≤ −0.05 → Negative</span> &nbsp;|&nbsp;
            <span class="sentiment-neutral">● Between → Neutral</span><br>
            <span style="color:var(--muted);font-size:0.8rem;margin-top:6px;display:block;">
            VADER is optimised for social media text and emoji-rich messages.
            Scores reflect the overall tone, not individual message meaning.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
