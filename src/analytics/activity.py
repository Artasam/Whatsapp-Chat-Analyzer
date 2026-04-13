"""
activity.py — Activity-map and heatmap computation.
"""
from __future__ import annotations

import pandas as pd

_WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def week_activity_map(option: str, df: pd.DataFrame) -> pd.Series:
    data = df if option == "Overall" else df[df["users"] == option]
    counts = data["weekday_name"].value_counts()
    return counts.reindex(_WEEKDAY_ORDER, fill_value=0)


def month_activity_map(option: str, df: pd.DataFrame) -> pd.Series:
    _MONTH_ORDER = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    data = df if option == "Overall" else df[df["users"] == option]
    counts = data["month"].value_counts()
    return counts.reindex(_MONTH_ORDER, fill_value=0).dropna()


def activity_heatmap(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: weekday × period → message count."""
    data = df if option == "Overall" else df[df["users"] == option]
    heatmap = data.pivot_table(
        index="weekday_name",
        columns="period",
        values="messages",
        aggfunc="count",
    ).fillna(0)
    # Reorder rows
    heatmap = heatmap.reindex(
        [d for d in _WEEKDAY_ORDER if d in heatmap.index]
    )
    return heatmap


def build_3d_activity_data(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Return long-form DataFrame for 3-D activity bar chart:
    weekday_idx × hour × message_count.
    """
    data = df if option == "Overall" else df[df["users"] == option]
    grouped = (
        data.groupby(["weekday_name", "hour"])
        .size()
        .reset_index(name="count")
    )
    day_map = {d: i for i, d in enumerate(_WEEKDAY_ORDER)}
    grouped["day_idx"] = grouped["weekday_name"].map(day_map)
    return grouped
