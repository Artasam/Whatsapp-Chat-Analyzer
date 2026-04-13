"""
app.py — WhatsApp Chat Analyzer 2026
Slim entry point: page config → CSS injection → sidebar → dashboard.
"""
import warnings
warnings.filterwarnings("ignore")

import sys
from pathlib import Path

# ── Ensure the project root is on sys.path so `src` resolves correctly ─────────
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

# ── Page must be the very first Streamlit call ─────────────────────────────────
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help":    None,
        "Report a bug": None,
        "About": "**WhatsApp Chat Analyzer 2026** · Built with Streamlit + Plotly",
    },
)

# ── Inject glassmorphism CSS ───────────────────────────────────────────────────
_css_path = ROOT / "src" / "ui" / "styles" / "main.css"
if _css_path.exists():
    st.markdown(
        f"<style>{_css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

# ── Register Plotly dark template (must happen after imports) ──────────────────
import src.visualization.themes  # noqa: F401  (side-effect: registers template)

# ── UI modules ────────────────────────────────────────────────────────────────
from src.ui.sidebar   import render_sidebar
from src.ui.dashboard import render_dashboard, render_landing

# ── Main flow ─────────────────────────────────────────────────────────────────
state = render_sidebar()

if state["data"] is not None:
    render_dashboard(state)
else:
    render_landing()