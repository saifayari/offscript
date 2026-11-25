"""Cybersecurity Machine Learning Lab — Main Streamlit Application.

Educational workshop application demonstrating supervised Machine Learning
for Phishing Email Detection and Network Intrusion Detection using synthetic data.

Run locally with:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from data import generate_network_dataset, generate_phishing_dataset
from models import train_intrusion_model, train_phishing_model
from ui import inject_cyber_theme
from views import (
    render_comparison_page,
    render_home_page,
    render_intrusion_lab,
    render_phishing_lab,
    render_quiz_page,
)

PAGES = [
    "Home — Cybersecurity ML Lab",
    "Project 01: Phishing Email Detector",
    "Project 02: Network Intrusion Detector",
    "Comparison: Two Cyber Problems",
    "Final Knowledge Check (Quiz)",
]


@st.cache_data(show_spinner=False)
def load_datasets():
    """Load deterministic synthetic classroom datasets."""
    return generate_phishing_dataset(seed=42), generate_network_dataset(n_samples=600, seed=42)


@st.cache_resource(show_spinner=False)
def load_trained_models():
    """Train scikit-learn models once per session without data leakage."""
    df_phish, df_net = load_datasets()
    phish_tfidf = train_phishing_model(df_phish, vectorizer_type="TF-IDF", seed=42)
    phish_count = train_phishing_model(df_phish, vectorizer_type="CountVectorizer", seed=42)
    intrusion_rf = train_intrusion_model(df_net, seed=42)
    return phish_tfidf, phish_count, intrusion_rf


def navigate_to(page_name: str) -> None:
    """Queue navigation to a target workshop module before the next rerun."""
    if page_name in PAGES:
        st.session_state.pending_page = page_name
        st.session_state.current_page = page_name


def _on_sidebar_change() -> None:
    """Synchronize current_page when user clicks a sidebar module."""
    st.session_state.current_page = st.session_state.sidebar_nav_radio


def main() -> None:
    """Configure Streamlit app, load models, and route active workshop page."""
    st.set_page_config(
        page_title="Cybersecurity ML Lab | Intro to AI Workshop",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_cyber_theme()

    if "pending_page" in st.session_state:
        target = st.session_state.pop("pending_page")
        st.session_state.current_page = target
        st.session_state.sidebar_nav_radio = target

    if "current_page" not in st.session_state:
        st.session_state.current_page = PAGES[0]
    if "sidebar_nav_radio" not in st.session_state:
        st.session_state.sidebar_nav_radio = st.session_state.current_page

    df_phish, df_net = load_datasets()
    phish_tfidf, phish_count, intrusion_rf = load_trained_models()

    # Sidebar Navigation & Workshop Status
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 6px 0 14px 0;">
              <span class="cyber-badge">INTRO TO AI WORKSHOP</span>
              <h2 style="font-size:22px; margin:8px 0 2px 0;">Cybersecurity ML Lab</h2>
              <div style="font-size:12.5px; color:#94A3B8;">Interactive Educational Sandbox</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.radio(
            "Navigate Lab Modules:",
            options=PAGES,
            key="sidebar_nav_radio",
            on_change=_on_sidebar_change,
        )

        st.markdown("---")
        st.markdown("**Live Model Summary**")
        st.caption(
            f"• Phishing NB (TF-IDF): **{phish_tfidf.accuracy:.1%}** test accuracy\n"
            f"• Intrusion RF: **{intrusion_rf.accuracy:.1%}** test accuracy"
        )
        st.markdown(
            """
            <div class="classroom-disclaimer">
              <strong>Classroom Demonstration Only:</strong><br>
              Uses 100% synthetic data. Does not collect real emails, inspect live credentials,
              scan networks, or act as a production security product.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Route Active Page
    page = st.session_state.current_page
    if page == PAGES[0]:
        render_home_page(navigate_to)
    elif page == PAGES[1]:
        render_phishing_lab(df_phish, phish_tfidf, phish_count)
    elif page == PAGES[2]:
        render_intrusion_lab(df_net, intrusion_rf)
    elif page == PAGES[3]:
        render_comparison_page()
    elif page == PAGES[4]:
        render_quiz_page()


if __name__ == "__main__":
    main()
