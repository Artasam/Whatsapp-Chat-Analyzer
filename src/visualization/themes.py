"""
themes.py — Plotly layout defaults and color utilities.
"""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

from src.config import THEME, PALETTE, PLOTLY_TEMPLATE

# ── Register a custom Plotly template ─────────────────────────────────────────
_base_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=THEME["text"], family="Inter, Segoe UI, sans-serif", size=13),
    title_font=dict(size=18, color=THEME["text"]),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor=THEME["border"],
        borderwidth=1,
    ),
    colorway=PALETTE,
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(
        bgcolor="rgba(15,15,30,0.95)",
        bordercolor=THEME["primary"],
        font_color=THEME["text"],
        font_size=13,
    ),
)

pio.templates["wca_dark"] = go.layout.Template(layout=_base_layout)
pio.templates.default = f"{PLOTLY_TEMPLATE}+wca_dark"


def apply_3d_style(fig: go.Figure) -> go.Figure:
    """Apply consistent glass-dark styling to a 3-D figure."""
    fig.update_layout(
        scene=dict(
            bgcolor="rgba(10,10,20,0.0)",
            xaxis=dict(
                gridcolor="rgba(124,58,237,0.2)",
                backgroundcolor="rgba(0,0,0,0)",
                showbackground=True,
                zerolinecolor=THEME["primary"],
                tickfont=dict(color=THEME["muted"]),
            ),
            yaxis=dict(
                gridcolor="rgba(6,182,212,0.2)",
                backgroundcolor="rgba(0,0,0,0)",
                showbackground=True,
                zerolinecolor=THEME["secondary"],
                tickfont=dict(color=THEME["muted"]),
            ),
            zaxis=dict(
                gridcolor="rgba(245,158,11,0.2)",
                backgroundcolor="rgba(0,0,0,0)",
                showbackground=True,
                zerolinecolor=THEME["accent"],
                tickfont=dict(color=THEME["muted"]),
            ),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def color_scale_purple_cyan() -> list[list]:
    return [
        [0.0, THEME["primary"]],
        [0.5, THEME["secondary"]],
        [1.0, THEME["accent"]],
    ]
