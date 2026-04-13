"""
sidebar.py — Sidebar rendering and state management.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.preprocess.parser import preprocess, compute_response_times


def render_sidebar() -> dict:
    """
    Render the sidebar and return a state dict:
      { data, option, response_times, raw_bytes }
    """

    # ── Branding ───────────────────────────────────────────────────────────────
    st.sidebar.markdown(
        """
        <div class="sidebar-logo">
            <span class="logo-icon">💬</span>
            <div class="logo-text">WhatsApp<br>Chat Analyzer</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── File Upload ────────────────────────────────────────────────────────────
    st.sidebar.markdown("### 📂 Upload Chat Export")
    uploaded = st.sidebar.file_uploader(
        "Select a WhatsApp .txt file",
        type=["txt"],
        accept_multiple_files=False,
        help="Export from WhatsApp: Chat → Export Chat → Without Media",
    )

    if uploaded is None:
        return {"data": None, "option": "Overall", "response_times": None}

    # ── Parse ──────────────────────────────────────────────────────────────────
    raw_bytes = uploaded.read()
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw_text = raw_bytes.decode("latin-1")

    with st.sidebar:
        with st.spinner("Parsing chat…"):
            try:
                df = preprocess(raw_text)
            except ValueError as exc:
                st.error(str(exc))
                return {"data": None, "option": "Overall", "response_times": None}

    response_times = compute_response_times(df)

    # ── User Selector ──────────────────────────────────────────────────────────
    st.sidebar.markdown("### 👤 Filter by User")
    users = [u for u in df["users"].unique().tolist() if u != "group_notification"]
    users.sort()
    users.insert(0, "Overall")
    option = st.sidebar.selectbox("Analyse as", users, index=0)

    # ── File info ──────────────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="font-size:0.78rem; color:var(--muted, #94a3b8); line-height:1.8;">
            📄 <b>{uploaded.name}</b><br>
            💬 {len(df):,} messages<br>
            👥 {df['users'].nunique() - 1} participants<br>
            📅 {df['only_dates'].min()} → {df['only_dates'].max()}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Download Raw Data ──────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="⬇ Export Parsed Data (CSV)",
        data=csv_bytes,
        file_name="wca_parsed.csv",
        mime="text/csv",
    )

    st.sidebar.markdown(
        "<div style='font-size:0.7rem;color:var(--muted,#94a3b8);text-align:center;"
        "margin-top:20px;'>WCA 2026 · Powered by Plotly + VADER</div>",
        unsafe_allow_html=True,
    )

    return {
        "data":           df,
        "option":         option,
        "response_times": response_times,
    }
