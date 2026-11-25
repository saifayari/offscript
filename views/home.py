"""Landing page view for Cybersecurity ML Lab."""

from __future__ import annotations

from typing import Callable

import streamlit as st

from ui import (
    render_glossary_section,
    render_intrusion_svg,
    render_learning_pipeline,
    render_phishing_svg,
)


def render_home_page(navigate_to: Callable[[str], None]) -> None:
    """Render the attractive Home Page introducing both ML cybersecurity labs."""
    st.markdown(
        """
        <div class="cyber-hero">
          <span class="cyber-badge">2-HOUR INTRO TO AI · INTERACTIVE WORKSHOP LAB</span>
          <h1 style="font-size:44px; margin:12px 0 6px 0;">CYBERSECURITY <span style="color:#20C5E8;">ML LAB</span></h1>
          <p style="font-size:19px; color:#CBD5E1; margin-bottom:14px;">
            Discover how Machine Learning helps identify cyber threats.
          </p>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <span class="cyber-badge badge-green">Real Scikit-Learn Models</span>
            <span class="cyber-badge">Synthetic Classroom Data Only</span>
            <span class="cyber-badge">Zero Coding Required</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two Large Project Cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            f"""<div class="cyber-card" style="min-height:425px; display:flex; flex-direction:column; justify-content:space-between;">
<div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
<span class="cyber-badge">PROJECT 01</span>
<span class="cyber-badge badge-green">Difficulty: Beginner Friendly</span>
</div>
{render_phishing_svg()}
<h2 style="font-size:23px; margin:14px 0 6px 0;">PHISHING EMAIL DETECTOR</h2>
<p style="color:#CBD5E1; font-size:15px; line-height:1.5; margin-bottom:10px;">
Train a Machine Learning model to identify suspicious emails.
</p>
</div>
<p style="color:#94A3B8; font-size:13.5px; line-height:1.5; margin:0;">
Turn email text into numerical word features with <strong>TF-IDF / CountVectorizer</strong> and train a
<strong>Multinomial Naive Bayes</strong> classifier to distinguish legitimate messages from phishing attempts.
</p>
</div>""",
            unsafe_allow_html=True,
        )
        if st.button("Start Challenge → Project 01", key="start_p1", type="primary", use_container_width=True):
            navigate_to("Project 01: Phishing Email Detector")
            st.rerun()

    with col2:
        st.markdown(
            f"""<div class="cyber-card" style="min-height:425px; display:flex; flex-direction:column; justify-content:space-between;">
<div>
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
<span class="cyber-badge">PROJECT 02</span>
<span class="cyber-badge badge-amber">Difficulty: Intermediate Lab</span>
</div>
{render_intrusion_svg()}
<h2 style="font-size:23px; margin:14px 0 6px 0;">NETWORK INTRUSION DETECTOR</h2>
<p style="color:#CBD5E1; font-size:15px; line-height:1.5; margin-bottom:10px;">
Train a Machine Learning model to identify potentially suspicious network activity.
</p>
</div>
<p style="color:#94A3B8; font-size:13.5px; line-height:1.5; margin:0;">
Analyze numeric telemetry (failed logins, connections, data sent, unusual ports) using a
<strong>Random Forest Classifier</strong> and test gray-area traffic scenarios live.
</p>
</div>""",
            unsafe_allow_html=True,
        )
        if st.button("Start Challenge → Project 02", key="start_p2", type="primary", use_container_width=True):
            navigate_to("Project 02: Network Intrusion Detector")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Educational Cards
    c_ml, c_sup, c_learn = st.columns(3, gap="medium")
    with c_ml:
        st.markdown(
            """
            <div class="cyber-card" style="height:100%;">
              <span class="cyber-badge">FOUNDATION</span>
              <h3 style="font-size:19px; margin:10px 0 8px 0;">What is Machine Learning?</h3>
              <p style="font-size:14px; color:#CBD5E1; line-height:1.55;">
                Instead of a human writing rigid <code>IF/ELSE</code> rules for every possible attack,
                Machine Learning lets a computer <strong>learn statistical patterns directly from examples</strong>
                and apply them to brand-new situations.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_sup:
        st.markdown(
            """
            <div class="cyber-card" style="height:100%;">
              <span class="cyber-badge">CORE PARADIGM</span>
              <h3 style="font-size:19px; margin:10px 0 8px 0;">What is Supervised Learning?</h3>
              <p style="font-size:14px; color:#CBD5E1; line-height:1.55;">
                In supervised learning, we teach the algorithm using <strong>labeled examples</strong>—data
                where the correct answer (<em>Phishing vs. Legitimate</em> or <em>Suspicious vs. Normal</em>)
                is already known during training.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_learn:
        st.markdown(
            """
            <div class="cyber-card" style="height:100%;">
              <span class="cyber-badge badge-green">WORKSHOP OUTCOMES</span>
              <h3 style="font-size:19px; margin:10px 0 8px 0;">What Will You Learn?</h3>
              <ul style="font-size:13.8px; color:#CBD5E1; line-height:1.55; padding-left:18px; margin:0;">
                <li>How text &amp; numeric security data become ML features</li>
                <li>Why train/test splits prevent false confidence</li>
                <li>How to read Accuracy, Precision, Recall &amp; Confusion Matrices</li>
                <li>Where ML models fail—and why humans remain essential</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### How Every Supervised ML Project Works")
    render_learning_pipeline(
        "Both labs follow this exact 4-stage learning flow using real scikit-learn models on safe synthetic classroom data."
    )
    render_glossary_section()
