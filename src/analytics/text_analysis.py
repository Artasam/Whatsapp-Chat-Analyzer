"""
text_analysis.py — Word cloud, common-word, and emoji analysis.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd
from wordcloud import WordCloud

try:
    import emoji as emoji_lib
    _EMOJI_DATA = emoji_lib.EMOJI_DATA
except ImportError:
    _EMOJI_DATA = {}

from src.config import STOPWORDS_PATH, NOISE_MESSAGES, THEME


def _load_stopwords() -> set[str]:
    path = Path(STOPWORDS_PATH)
    if path.exists():
        return set(path.read_text(encoding="utf-8").split())
    return set()


def generate_wordcloud(option: str, df: pd.DataFrame) -> "WordCloud":
    data = df if option == "Overall" else df[df["users"] == option]
    data = data[~data["messages"].isin(NOISE_MESSAGES)]
    text = data["messages"].str.cat(sep=" ").strip()
    if not text:
        raise ValueError("Not enough text to build a word cloud.")

    stop = _load_stopwords()
    wc = WordCloud(
        width=900,
        height=500,
        min_font_size=10,
        background_color=None,
        mode="RGBA",
        colormap="plasma",
        stopwords=stop,
        max_words=200,
        prefer_horizontal=0.85,
    )
    return wc.generate(text)


def most_common_words(option: str, df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    stop = _load_stopwords()
    data = df if option == "Overall" else df[df["users"] == option]
    data = data[data["users"] != "group_notification"]
    data = data[~data["messages"].isin(NOISE_MESSAGES)]

    words: list[str] = []
    for msg in data["messages"]:
        for word in str(msg).lower().split():
            if word.isalpha() and word not in stop and len(word) > 2:
                words.append(word)

    if not words:
        raise ValueError("No meaningful words found.")

    common = Counter(words).most_common(top_n)
    return pd.DataFrame(common, columns=["word", "count"])


def emoji_count(option: str, df: pd.DataFrame) -> pd.DataFrame:
    data = df if option == "Overall" else df[df["users"] == option]
    emojis: list[str] = []
    for msg in data["messages"]:
        emojis.extend([ch for ch in str(msg) if ch in _EMOJI_DATA])

    if not emojis:
        return pd.DataFrame(columns=["emoji", "count"])

    counts = Counter(emojis).most_common()
    return pd.DataFrame(counts, columns=["emoji", "count"])
