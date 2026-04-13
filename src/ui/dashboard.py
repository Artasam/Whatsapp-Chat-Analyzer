"""
dashboard.py — Master dashboard renderer.

Assembles the 5 tab-pages and routes state to each.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.ui.pages import overview, timelines, activity, content, sentiment


_TABS = [
    ("📊", "Overview"),
    ("📅", "Timelines"),
    ("🗓", "Activity"),
    ("🔤", "Content"),
    ("🧠", "Sentiment"),
]


def render_dashboard(state: dict) -> None:
    df             = state["data"]
    option         = state["option"]
    response_times = state["response_times"]

    user_label = option if option != "Overall" else "All Participants"

    # ── Title row — split into two separate markdown calls (Streamlit-safe) ──────

    st.markdown(
        f'<h1 style="font-size:1.9rem;font-weight:800;color:#a78bfa;margin:0 0 4px 0;'
        f'line-height:1.2;">💬 WhatsApp Chat Analyzer</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="color:#94a3b8;font-size:0.9rem;font-weight:500;margin-bottom:12px;">'
        f'Analysing: <b style="color:#a78bfa">{user_label}</b>'
        f'&nbsp;·&nbsp; {len(df):,} messages'
        f'&nbsp;·&nbsp; {df["only_dates"].min()} → {df["only_dates"].max()}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(124,58,237,0.25);margin:4px 0 18px 0;">',
        unsafe_allow_html=True,
    )

    tab_labels = [f"{icon} {name}" for icon, name in _TABS]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        overview.render(option, df, response_times)

    with tabs[1]:
        timelines.render(option, df)

    with tabs[2]:
        activity.render(option, df)

    with tabs[3]:
        content.render(option, df)

    with tabs[4]:
        sentiment.render(option, df)


def render_landing() -> None:
    """Hero landing screen shown before any file is uploaded."""

    # ── Hero header ──────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="text-align:center;padding:52px 20px 4px;font-size:4.8rem;'
        'filter:drop-shadow(0 0 22px rgba(124,58,237,0.85));">💬</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h1 style="text-align:center;font-size:2.6rem;font-weight:800;'
        'color:#a78bfa;margin:8px 0 16px;">WhatsApp Chat Analyzer</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="text-align:center;font-size:1.05rem;color:#94a3b8;'
        'max-width:560px;margin:0 auto 32px;line-height:1.75;">'
        'Upload your WhatsApp chat export and unlock deep insights — '
        'interactive 3-D visualisations, AI sentiment analysis, and '
        'beautiful analytics dashboards.</p>',
        unsafe_allow_html=True,
    )

    # ── Feature chips via st.columns (avoids Streamlit HTML sanitiser) ────────
    _FEATURES = [
        ("🌐", "3-D Timelines"),
        ("🧠", "VADER Sentiment"),
        ("🗓", "Activity Heatmaps"),
        ("☁️", "Word Clouds"),
        ("😀", "Emoji Analytics"),
        ("⏱️", "Response Times"),
        ("💚", "Health Score"),
        ("📥", "CSV Export"),
    ]
    _CHIP = (
        "background:rgba(255,255,255,0.06);"
        "border:1px solid rgba(124,58,237,0.32);"
        "border-radius:12px;padding:13px 18px;"
        "font-size:0.83rem;font-weight:500;"
        "color:#f1f5f9;text-align:center;margin-bottom:10px;"
    )
    cols = st.columns(4)
    for i, (icon, label) in enumerate(_FEATURES):
        with cols[i % 4]:
            st.markdown(
                f'<div style="{_CHIP}">{icon}&nbsp; {label}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Instructions card (centre-column, inline styles only) ─────────────────
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.06);
                border:1px solid rgba(124,58,237,0.30);
                border-radius:16px;padding:24px 28px;text-align:center;">
                <b style="font-size:1rem;color:#f1f5f9;">
                    How to export your WhatsApp chat
                </b>
                <ol style="text-align:left;margin-top:12px;color:#94a3b8;
                           line-height:2;font-size:0.88rem;">
                    <li>Open the chat in WhatsApp</li>
                    <li>Tap ⋮ → <b>More</b> → <b>Export chat</b></li>
                    <li>Select <b>Without Media</b></li>
                    <li>Save the <code>.txt</code> file and upload it ↑</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )
