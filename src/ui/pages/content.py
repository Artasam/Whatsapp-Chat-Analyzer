"""
content.py — Text & Emoji analysis page.

Word cloud, top-20 words bar, emoji donut chart.
"""
from __future__ import annotations

import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.analytics.text_analysis import (
    generate_wordcloud,
    most_common_words,
    emoji_count,
)
from src.visualization.charts import plot_common_words, plot_emoji_donut


def render(option: str, df: pd.DataFrame) -> None:

    # ── Word Cloud ─────────────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">☁ Word Cloud</p>', unsafe_allow_html=True)
    try:
        wc = generate_wordcloud(option, df)
        fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        fig_wc.patch.set_facecolor("none")
        ax_wc.set_facecolor("none")
        st.pyplot(fig_wc)
        plt.close(fig_wc)

        # Download button for the word cloud image
        buf = io.BytesIO()
        wc.to_image().save(buf, format="PNG")
        st.download_button(
            "⬇ Download Word Cloud",
            data=buf.getvalue(),
            file_name="wordcloud.png",
            mime="image/png",
        )
    except ValueError as e:
        st.warning(str(e))

    # ── Most Common Words ──────────────────────────────────────────────────────
    st.markdown(
        '<p class="section-heading">🔤 Top 20 Most Common Words</p>',
        unsafe_allow_html=True,
    )
    try:
        df_words = most_common_words(option, df)
        st.plotly_chart(plot_common_words(df_words), width='stretch')
    except ValueError as e:
        st.warning(str(e))

    # ── Emoji Analysis ─────────────────────────────────────────────────────────
    st.markdown('<p class="section-heading">😀 Emoji Usage</p>', unsafe_allow_html=True)
    df_emoji = emoji_count(option, df)

    if df_emoji.empty:
        st.info("No emojis found in the selected messages.")
    else:
        col_e1, col_e2 = st.columns([2, 3])
        with col_e1:
            st.dataframe(
                df_emoji.head(20).rename(columns={"emoji": "Emoji", "count": "Count"}),
                width='stretch',
                hide_index=True,
            )
        with col_e2:
            st.plotly_chart(
                plot_emoji_donut(df_emoji),
                width='stretch',
                config={"displayModeBar": False},
            )
