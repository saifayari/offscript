"""Comparison Page and Interactive 5-Question Knowledge Check Quiz."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from education import PROJECT_COMPARISON_ROWS, QUIZ_QUESTIONS
from ui import render_glossary_section, render_learning_pipeline


def render_comparison_page() -> None:
    """Compare Project 01 (Phishing Detection) and Project 02 (Intrusion Detection)."""
    st.markdown(
        """
        <div class="cyber-hero">
          <span class="cyber-badge">COMPARISON · TWO CYBERSECURITY PROBLEMS</span>
          <h1 style="font-size:36px; margin:10px 0 6px 0;">PHISHING VS. INTRUSION DETECTION</h1>
          <p style="font-size:16px; color:#CBD5E1; margin:0;">
            Two very different cybersecurity data types—solved with the same core supervised Machine Learning workflow.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Side-by-Side Architecture Comparison")
    comp_df = pd.DataFrame(PROJECT_COMPARISON_ROWS)
    st.table(comp_df.set_index("Element"))

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            """
            <div class="cyber-card" style="border-top:4px solid #1769FF;">
              <span class="cyber-badge">TEXT SUPERVISED LEARNING</span>
              <h3 style="margin:10px 0 8px 0;">Why Naive Bayes for Phishing?</h3>
              <p style="color:#CBD5E1; font-size:14.5px; line-height:1.55;">
                Emails are unstructured text. Converting them with <strong>TF-IDF / CountVectorizer</strong> creates
                over a thousand word features. <strong>Multinomial Naive Bayes</strong> learns rapidly from high-dimensional
                word counts and transparently shows which words pushed the decision.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="cyber-card" style="border-top:4px solid #20C5E8;">
              <span class="cyber-badge">TABULAR SUPERVISED LEARNING</span>
              <h3 style="margin:10px 0 8px 0;">Why Random Forest for Network Traffic?</h3>
              <p style="color:#CBD5E1; font-size:14.5px; line-height:1.55;">
                Network telemetry consists of structured numbers (logins, connections, megabytes, ports).
                A <strong>Random Forest</strong> combines 150 decision trees that capture non-linear combinations
                (such as moderate logins <em>plus</em> unusual ports) much better than single threshold rules.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### The Shared Supervised Learning Blueprint")
    st.info(
        "Key Takeaway: Both projects are examples of **Supervised Machine Learning**! Even though one reads English words "
        "and the other reads numeric network counters, both require labeled training data, leak-free train/test splitting, "
        "metric evaluation, and human judgment."
    )
    render_learning_pipeline(
        "Once you master DATA → TRAINING → MODEL → PREDICTION, you can apply Machine Learning across almost any domain."
    )
    render_glossary_section()


def render_quiz_page() -> None:
    """Render the interactive 5-question workshop knowledge check."""
    st.markdown(
        """
        <div class="cyber-hero">
          <span class="cyber-badge badge-green">FINAL KNOWLEDGE CHECK</span>
          <h1 style="font-size:36px; margin:10px 0 6px 0;">CYBERSECURITY ML QUIZ</h1>
          <p style="font-size:16px; color:#CBD5E1; margin:0;">
            Test what you learned across both workshops in 5 quick questions.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("workshop_quiz_form"):
        answers: dict[str, int | None] = {}
        for q in QUIZ_QUESTIONS:
            qid = str(q["id"])
            options = list(q["options"])
            choice = st.radio(
                str(q["question"]),
                options=list(range(len(options))),
                format_func=lambda idx, opts=options: opts[idx],
                index=None,
                key=f"quiz_{qid}",
            )
            answers[qid] = choice
            st.markdown("---")

        submitted = st.form_submit_button("CHECK MY ANSWERS", type="primary", use_container_width=True)

    if submitted:
        unanswered = [q["id"] for q in QUIZ_QUESTIONS if answers[str(q["id"])] is None]
        if unanswered:
            st.warning("Please select an answer for all 5 questions before submitting.")
            return

        score = 0
        for q in QUIZ_QUESTIONS:
            qid = str(q["id"])
            if answers[qid] == int(q["correct_index"]):
                score += 1

        pct = int(round((score / len(QUIZ_QUESTIONS)) * 100))
        banner_cls = "result-banner-safe" if score >= 4 else "cyber-card"
        st.markdown(
            f"""
            <div class="{banner_cls}" style="margin: 14px 0 20px 0;">
              <span class="cyber-badge badge-green">QUIZ RESULT</span>
              <h2 style="margin:8px 0 4px 0;">Your Score: {score} / {len(QUIZ_QUESTIONS)} ({pct}%)</h2>
              <p style="margin:0; color:#E2E8F0; font-size:15px;">
                {"Outstanding work—you nailed the fundamentals of supervised ML in cybersecurity!" if score >= 4 else "Great effort! Review the detailed explanations below to lock in each concept."}
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for q in QUIZ_QUESTIONS:
            qid = str(q["id"])
            user_idx = int(answers[qid])
            correct_idx = int(q["correct_index"])
            opts = list(q["options"])
            is_right = user_idx == correct_idx

            if is_right:
                st.success(f"✓ {q['question']} — Correct! ({opts[correct_idx]})")
            else:
                st.error(
                    f"✕ {q['question']} — Your answer: '{opts[user_idx]}' | Correct answer: '{opts[correct_idx]}'"
                )
            st.caption(f"Explanation: {q['explanation']}")
