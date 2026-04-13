"""
sentiment.py — VADER-based sentiment analysis (fully offline).

Returns per-user polarity scores and a rolling sentiment timeline.
"""
from __future__ import annotations

import pandas as pd

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _analyzer = SentimentIntensityAnalyzer()
    _VADER_AVAILABLE = True
except ImportError:
    _VADER_AVAILABLE = False

from src.config import NOISE_MESSAGES


def _score(text: str) -> float:
    """Return VADER compound score in [-1, 1]."""
    if not _VADER_AVAILABLE:
        return 0.0
    return _analyzer.polarity_scores(str(text))["compound"]


def _label(score: float) -> str:
    if score >= 0.05:
        return "Positive 😊"
    if score <= -0.05:
        return "Negative 😞"
    return "Neutral 😐"


def analyze_sentiment(option: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Per-user average sentiment.

    Returns DataFrame with columns: user, avg_score, label, message_count
    """
    data = df if option == "Overall" else df[df["users"] == option]
    data = data[
        (data["users"] != "group_notification") &
        (~data["messages"].isin(NOISE_MESSAGES))
    ].copy()

    data["score"] = data["messages"].apply(_score)

    result = (
        data.groupby("users")
        .agg(
            avg_score=("score", "mean"),
            message_count=("score", "count"),
        )
        .reset_index()
    )
    result["avg_score"] = result["avg_score"].round(4)
    result["label"] = result["avg_score"].apply(_label)
    result = result.sort_values("avg_score", ascending=False).reset_index(drop=True)
    return result


def sentiment_timeline(option: str, df: pd.DataFrame, window: int = 50) -> pd.DataFrame:
    """
    Rolling-window sentiment over time for charting.

    Returns DataFrame: date, rolling_score
    """
    data = df if option == "Overall" else df[df["users"] == option]
    data = data[
        (data["users"] != "group_notification") &
        (~data["messages"].isin(NOISE_MESSAGES))
    ].copy().sort_values("date")

    data["score"] = data["messages"].apply(_score)
    data["rolling_score"] = data["score"].rolling(window=window, min_periods=1).mean()
    return data[["date", "rolling_score", "users"]].reset_index(drop=True)


def vader_available() -> bool:
    return _VADER_AVAILABLE
