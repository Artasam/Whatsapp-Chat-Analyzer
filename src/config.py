"""
config.py — Global constants, theme tokens, and path configuration.
"""
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT            = Path(__file__).parent.parent
STOPWORDS_PATH  = ROOT / "stop_hinglish.txt"

# ── Plotly / Chart Theme ───────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"

THEME = {
    "bg":       "#0a0a14",
    "surface":  "rgba(255,255,255,0.06)",
    "border":   "rgba(124,58,237,0.35)",
    "primary":  "#7c3aed",
    "secondary":"#06b6d4",
    "accent":   "#f59e0b",
    "success":  "#10b981",
    "danger":   "#ef4444",
    "text":     "#f1f5f9",
    "muted":    "#94a3b8",
}

# Ordered color palette used across all charts
PALETTE = [
    "#7c3aed", "#06b6d4", "#f59e0b", "#10b981", "#ef4444",
    "#8b5cf6", "#0ea5e9", "#fbbf24", "#34d399", "#f87171",
    "#a78bfa", "#38bdf8", "#fcd34d", "#6ee7b7", "#fca5a5",
]

# ── WhatsApp message noise strings ─────────────────────────────────────────────
NOISE_MESSAGES = {
    "<Media omitted>\n",
    "Waiting for this message\n",
    "<this edited>\n",
    "null\n",
    "This message was deleted\n",
}

APP_NAME    = "WhatsApp Chat Analyzer"
APP_VERSION = "2026.1.0"
