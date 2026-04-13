"""
stats.py — Core statistics and KPI computation.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from urlextract import URLExtract

from src.config import NOISE_MESSAGES

_extractor = URLExtract()


def fetch_stats(option: str, df: pd.DataFrame) -> dict:
    """Return a dict of top-level KPI values for the selected user."""
    data = df if option == "Overall" else df[df["users"] == option]

    num_messages = len(data)

    words: list[str] = []
    for msg in data["messages"]:
        words.extend(str(msg).split())

    media_count = int(data["messages"].str.contains(
        "<Media omitted>", na=False
    ).sum())

    links: list[str] = []
    for msg in data["messages"]:
        links.extend(_extractor.find_urls(str(msg)))

    # Unique days active
    active_days = data["only_dates"].nunique()

    # Average messages per active day
    avg_per_day = round(num_messages / active_days, 1) if active_days else 0

    return {
        "total_messages": num_messages,
        "total_words":    len(words),
        "media_shared":   media_count,
        "links_shared":   len(links),
        "active_days":    active_days,
        "avg_per_day":    avg_per_day,
    }


def busy_users(df: pd.DataFrame, top_n: int = 10) -> tuple[pd.Series, pd.DataFrame]:
    """Top-N users by message count + percentage table."""
    counts = df["users"].value_counts()
    top    = counts.head(top_n)
    pct_df = (
        round((counts / len(df)) * 100, 2)
        .reset_index()
        .rename(columns={"users": "Name", "count": "Percent"})
        .head(top_n)
    )
    return top, pct_df


def conversation_health_score(df: pd.DataFrame) -> int:
    """
    Composite 0-100 conversation health score.

    Components
    ----------
    • Participation diversity  (Gini coefficient of message distribution) → 40 pts
    • Average message richness (mean word count)                          → 30 pts
    • Activity consistency     (fraction of span days that are active)    → 30 pts
    """
    real = df[df["users"] != "group_notification"]
    if real.empty:
        return 0

    # ── Diversity ──────────────────────────────────────────────────────────────
    counts = real["users"].value_counts(normalize=True).values
    counts_sorted = np.sort(counts)
    n = len(counts_sorted)
    gini = (
        (2 * np.sum((np.arange(1, n + 1) * counts_sorted))) / (n * counts_sorted.sum()) - (n + 1) / n
        if counts_sorted.sum() > 0 else 1
    )
    diversity_score = max(0.0, (1 - abs(gini))) * 40

    # ── Richness ───────────────────────────────────────────────────────────────
    clean = real[~real["messages"].isin(NOISE_MESSAGES)]
    avg_words = clean["messages"].str.split().str.len().mean() if not clean.empty else 0
    richness_score = min(avg_words / 15 * 30, 30)

    # ── Consistency ────────────────────────────────────────────────────────────
    if df["only_dates"].nunique() >= 2:
        date_range = (pd.to_datetime(df["only_dates"].max()) -
                      pd.to_datetime(df["only_dates"].min())).days + 1
        consistency_score = min(df["only_dates"].nunique() / date_range * 30, 30)
    else:
        consistency_score = 15

    return min(int(diversity_score + richness_score + consistency_score), 100)
