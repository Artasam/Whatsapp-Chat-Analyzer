"""
charts.py — All Plotly chart builders (2-D + 3-D).

Each function returns a go.Figure ready for st.plotly_chart().
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.config import THEME, PALETTE
from src.visualization.themes import apply_3d_style, color_scale_purple_cyan


# ────────────────────────────────────────────────────────────────────────────────
# 3-D Charts
# ────────────────────────────────────────────────────────────────────────────────

def plot_3d_timeline(df_3d: pd.DataFrame, title: str = "3-D Message Timeline") -> go.Figure:
    """
    Scatter3d: X = day index, Y = hour (0-23), Z = message count.
    Colour-mapped by count to give a heatmap-like feel in 3-D.
    """
    if df_3d.empty:
        return _empty_figure(title)

    fig = go.Figure(
        go.Scatter3d(
            x=df_3d["date_idx"],
            y=df_3d["hour"],
            z=df_3d["count"],
            mode="markers",
            marker=dict(
                size=df_3d["count"].clip(upper=50) / 5 + 3,
                color=df_3d["count"],
                colorscale=color_scale_purple_cyan(),
                opacity=0.85,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Messages",
                        font=dict(color=THEME["text"]),
                    ),
                    tickfont=dict(color=THEME["muted"]),
                ),
            ),
            text=[
                f"Day +{di}<br>Hour: {h}:00<br>Messages: {c}"
                for di, h, c in zip(df_3d["date_idx"], df_3d["hour"], df_3d["count"])
            ],
            hoverinfo="text",
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=THEME["text"])),
        scene=dict(
            xaxis_title="Day Index",
            yaxis_title="Hour of Day",
            zaxis_title="Messages",
        ),
        height=520,
    )
    return apply_3d_style(fig)


def plot_3d_activity(df_3d: pd.DataFrame, title: str = "3-D Activity Landscape") -> go.Figure:
    """
    Scatter3d activity surface: X = weekday (0-6), Y = hour, Z = count.
    Surface interpolated via Mesh3d for a landscape effect.
    """
    if df_3d.empty:
        return _empty_figure(title)

    _DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    fig = go.Figure()

    # Bubble layer
    fig.add_trace(
        go.Scatter3d(
            x=df_3d["day_idx"],
            y=df_3d["hour"],
            z=df_3d["count"],
            mode="markers",
            marker=dict(
                size=df_3d["count"].clip(upper=80) / 5 + 4,
                color=df_3d["count"],
                colorscale="Plasma",
                opacity=0.80,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Messages",
                        font=dict(color=THEME["text"]),
                    ),
                    tickfont=dict(color=THEME["muted"]),
                ),
            ),
            text=[
                f"{_DAYS[int(di)]} — {h}:00<br>{c} messages"
                for di, h, c in zip(df_3d["day_idx"], df_3d["hour"], df_3d["count"])
            ],
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=THEME["text"])),
        scene=dict(
            xaxis=dict(
                title="Weekday",
                tickvals=list(range(7)),
                ticktext=_DAYS,
            ),
            yaxis_title="Hour of Day",
            zaxis_title="Messages",
        ),
        height=520,
    )
    return apply_3d_style(fig)


def plot_sentiment_3d(df_tl: pd.DataFrame, title: str = "Sentiment Trajectory") -> go.Figure:
    """
    3-D line: X = message index, Y = user char-code, Z = rolling sentiment score.
    One trace per user, coloured by label.
    """
    if df_tl.empty:
        return _empty_figure(title)

    fig = go.Figure()
    users = df_tl["users"].unique()

    for i, user in enumerate(users):
        sub = df_tl[df_tl["users"] == user].reset_index(drop=True)
        fig.add_trace(
            go.Scatter3d(
                x=list(range(len(sub))),
                y=[i] * len(sub),
                z=sub["rolling_score"].tolist(),
                mode="lines+markers",
                name=user,
                line=dict(color=PALETTE[i % len(PALETTE)], width=4),
                marker=dict(size=3, color=PALETTE[i % len(PALETTE)]),
                hovertemplate=f"<b>{user}</b><br>Sentiment: %{{z:.3f}}<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=THEME["text"])),
        scene=dict(
            xaxis_title="Message Index",
            yaxis=dict(
                title="User",
                tickvals=list(range(len(users))),
                ticktext=list(users),
            ),
            zaxis_title="Sentiment Score",
            zaxis=dict(range=[-1, 1]),
        ),
        height=520,
        showlegend=True,
    )
    return apply_3d_style(fig)


# ────────────────────────────────────────────────────────────────────────────────
# 2-D Interactive Charts
# ────────────────────────────────────────────────────────────────────────────────

def plot_monthly_timeline(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=df["time"],
            y=df["messages"],
            mode="lines+markers",
            line=dict(color=THEME["primary"], width=2.5, shape="spline"),
            marker=dict(size=6, color=THEME["secondary"]),
            fill="tozeroy",
            fillcolor="rgba(124,58,237,0.12)",
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Monthly Message Volume",
        xaxis=dict(tickangle=-45),
        height=350,
    )
    return fig


def plot_daily_timeline(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=df["only_dates"],
            y=df["messages"],
            mode="lines",
            line=dict(color=THEME["success"], width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.10)",
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Daily Message Volume",
        xaxis=dict(
            rangeslider=dict(visible=True, bgcolor="rgba(255,255,255,0.05)"),
            type="date",
        ),
        height=380,
    )
    return fig


def plot_hourly_bar(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=df["hour"],
            y=df["messages"],
            marker=dict(
                color=df["messages"],
                colorscale="Plasma",
                showscale=False,
            ),
            hovertemplate="Hour %{x}:00<br>Messages: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Messages by Hour of Day",
        xaxis_title="Hour",
        yaxis_title="Messages",
        height=300,
    )
    return fig


def plot_busy_users_bar(series: pd.Series) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=series.values,
            y=series.index,
            orientation="h",
            marker=dict(
                color=PALETTE[:len(series)],
                opacity=0.9,
            ),
            hovertemplate="<b>%{y}</b><br>Messages: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Most Active Users",
        xaxis_title="Messages",
        yaxis=dict(autorange="reversed"),
        height=max(300, len(series) * 40),
    )
    return fig


def plot_week_activity(series: pd.Series) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=series.index,
            y=series.values,
            marker=dict(color=PALETTE[0], opacity=0.9),
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
        )
    )
    fig.update_layout(title="Busiest Day of Week", height=300)
    return fig


def plot_month_activity(series: pd.Series) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=series.index,
            y=series.values,
            marker=dict(color=PALETTE[1], opacity=0.9),
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Busiest Month",
        xaxis=dict(tickangle=-45),
        height=300,
    )
    return fig


def plot_heatmap(pivot: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale="Plasma",
            hovertemplate="<b>%{y}</b> — Period %{x}<br>Messages: %{z}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Weekly Activity Heatmap",
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        height=320,
    )
    return fig


def plot_common_words(df: pd.DataFrame) -> go.Figure:
    df_sorted = df.sort_values("count")
    fig = go.Figure(
        go.Bar(
            x=df_sorted["count"],
            y=df_sorted["word"],
            orientation="h",
            marker=dict(
                color=df_sorted["count"],
                colorscale="Viridis",
                showscale=False,
            ),
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Top 20 Most Common Words",
        xaxis_title="Frequency",
        height=500,
    )
    return fig


def plot_emoji_donut(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    top = df.head(top_n) if len(df) >= top_n else df
    fig = go.Figure(
        go.Pie(
            labels=top["emoji"].tolist(),
            values=top["count"].tolist(),
            hole=0.55,
            marker=dict(colors=PALETTE[:len(top)]),
            textfont=dict(size=16),
            hovertemplate="<b>%{label}</b><br>%{value} uses (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        title="Top Emoji Distribution",
        height=380,
        legend=dict(orientation="v"),
    )
    return fig


def plot_sentiment_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar coloured by sentiment score."""
    color_map = df["avg_score"].apply(
        lambda s: THEME["success"] if s >= 0.05 else (THEME["danger"] if s <= -0.05 else PALETTE[4])
    ).tolist()
    fig = go.Figure(
        go.Bar(
            x=df["avg_score"],
            y=df["users"],
            orientation="h",
            marker=dict(color=color_map, opacity=0.85),
            text=df["label"].tolist(),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_dash="dash", line_color=THEME["muted"], line_width=1)
    fig.update_layout(
        title="Per-User Sentiment Scores",
        xaxis=dict(range=[-1, 1], title="Compound Score"),
        yaxis=dict(autorange="reversed"),
        height=max(300, len(df) * 40),
    )
    return fig


def plot_health_gauge(score: int) -> go.Figure:
    color = (
        THEME["success"] if score >= 70 else
        THEME["accent"]  if score >= 40 else
        THEME["danger"]
    )
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={"reference": 70, "increasing": {"color": THEME["success"]}},
            title={"text": "Conversation Health Score", "font": {"color": THEME["text"]}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": THEME["muted"]},
                "bar":  {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 40],   "color": "rgba(239,68,68,0.15)"},
                    {"range": [40, 70],  "color": "rgba(245,158,11,0.15)"},
                    {"range": [70, 100], "color": "rgba(16,185,129,0.15)"},
                ],
                "threshold": {
                    "line":  {"color": THEME["text"], "width": 2},
                    "thickness": 0.75,
                    "value": 70,
                },
            },
        )
    )
    fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)")
    return fig


def plot_response_time_bar(series: pd.Series) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=series.values,
            y=series.index,
            orientation="h",
            marker=dict(color=PALETTE[2], opacity=0.85),
            hovertemplate="<b>%{y}</b><br>Avg response: %{x:.1f} min<extra></extra>",
        )
    )
    fig.update_layout(
        title="Average Response Time (minutes)",
        xaxis_title="Minutes",
        yaxis=dict(autorange="reversed"),
        height=max(280, len(series) * 40),
    )
    return fig


# ── Helpers ────────────────────────────────────────────────────────────────────

def _empty_figure(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(
            text="Not enough data to render this chart.",
            showarrow=False,
            font=dict(color=THEME["muted"], size=14),
        )],
        height=400,
    )
    return fig
