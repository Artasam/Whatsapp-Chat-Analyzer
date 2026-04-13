"""
timeline.py — Message timeline aggregations.
"""
from __future__ import annotations

import pandas as pd


def monthly_timeline(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """Messages grouped by Year-Month."""
    data = df if option == "Overall" else df[df["users"] == option]
    tl = (
        data.groupby(["year", "month_num", "month"])
        .size()
        .reset_index(name="messages")
    )
    tl["time"] = tl["month"] + "-" + tl["year"].astype(str)
    return tl


def daily_timeline(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """Messages grouped by calendar date."""
    data = df if option == "Overall" else df[df["users"] == option]
    daily = data.groupby("only_dates").size().reset_index(name="messages")
    return daily


def hourly_distribution(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """Message count for each hour 0-23."""
    data = df if option == "Overall" else df[df["users"] == option]
    hourly = (
        data.groupby("hour")
        .size()
        .reindex(range(24), fill_value=0)
        .reset_index(name="messages")
    )
    return hourly


def build_3d_timeline_data(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a DataFrame for a 3-D scatter: date_index × hour × message_count.
    Each row = one (date, hour) bucket.
    """
    data = df if option == "Overall" else df[df["users"] == option]
    grouped = (
        data.groupby(["only_dates", "hour"])
        .size()
        .reset_index(name="count")
    )
    grouped["date_ordinal"] = pd.to_datetime(
        grouped["only_dates"]
    ).map(pd.Timestamp.toordinal)
    # Normalise to 0-based index for nicer 3-D display
    if not grouped.empty:
        grouped["date_idx"] = grouped["date_ordinal"] - grouped["date_ordinal"].min()
    else:
        grouped["date_idx"] = []
    return grouped
