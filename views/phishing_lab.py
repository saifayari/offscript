"""Project 01: Phishing Email Detector interactive educational view."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from data import PREDEFINED_SAMPLE_EMAILS
from education import METRIC_EXPLANATIONS, PHISHING_PIPELINE_STEPS
from models import PhishingModelArtifacts, predict_email
from ui import (
    highlight_email_tokens,
    plot_confusion_matrix,
    plot_probability_bars,
    plot_token_influences,
    render_glossary_section,
    render_learning_pipeline,
)


def render_phishing_lab(
    df_emails: pd.DataFrame,
    artifacts_tfidf: PhishingModelArtifacts,
    artifacts_count: PhishingModelArtifacts,
) -> None:
    """Render the complete Project 01 Phishing Email Detector lab."""
    st.markdown(
        """
        <div class="cyber-hero">
          <span class="cyber-badge">PROJECT 01 · TEXT CLASSIFICATION</span>
          <h1 style="font-size:36px; margin:10px 0 6px 0;">PHISHING EMAIL DETECTOR</h1>
          <p style="font-size:16px; color:#CBD5E1; margin:0;">
            Learn how supervised Machine Learning classifies text into <strong>Legitimate</strong> or <strong>Phishing</strong>.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # A. Introduction & Scenario
    st.markdown("### A. Scenario & Educational Objective")
    st.markdown(
        """
        <div class="scenario-box">
          <strong>Your Mission:</strong> "You are a cybersecurity analyst. Your company receives hundreds of emails every day.
          Your mission is to train an ML model that can distinguish legitimate emails from phishing attempts."
          <br><br>
          <strong>Why it matters:</strong> Phishing emails attempt to manipulate users into revealing sensitive information
          (like passwords or bank details) or clicking malicious links. In <strong>supervised learning</strong>, we show
          an algorithm labeled historical examples so it learns which words and phrasing patterns signal phishing versus everyday communication.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Visual ML Learning Flow")
    render_learning_pipeline(
        "For text classification, raw email wording becomes numerical word vectors before Multinomial Naive Bayes learns patterns."
    )

    # B. Synthetic Dataset Explorer
    st.markdown("### B. Synthetic Labeled Email Dataset")
    st.info(
        "Classroom Data Notice: All 120 emails below are 100% synthetic educational examples created specifically for this workshop. "
        "Links shown in brackets (such as `[verify-account-link]`) are harmless text placeholders—no real emails or live URLs are used."
    )

    c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
    c_stat1.metric("Total Synthetic Emails", len(df_emails))
    c_stat2.metric("Legitimate Emails", int((df_emails["label"] == "Legitimate").sum()))
    c_stat3.metric("Phishing Examples", int((df_emails["label"] == "Phishing").sum()))
    c_stat4.metric("Train / Test Split", "75% / 25% (90 / 30)")

    with st.expander("Explore the Synthetic Email Dataset (120 labeled records)"):
        filter_lbl = st.radio(
            "Filter dataset preview:",
            ["All", "Legitimate", "Phishing"],
            horizontal=True,
            key="phish_ds_filter",
        )
        view_df = df_emails if filter_lbl == "All" else df_emails[df_emails["label"] == filter_lbl]
        st.caption(f"Showing first 15 of {len(view_df)} matching synthetic emails:")
        st.table(view_df[["id", "label", "category", "subject", "body"]].head(15))

    # C. Machine Learning Pipeline
    st.markdown("### C. Machine Learning Pipeline (Scikit-Learn)")
    vec_choice = st.radio(
        "Choose feature extraction method to inspect live:",
        ["TF-IDF (Term Frequency - Inverse Document Frequency)", "CountVectorizer (Raw Word Counts)"],
        horizontal=True,
        key="phish_vec_choice",
    )
    artifacts = artifacts_tfidf if vec_choice.startswith("TF-IDF") else artifacts_count

    pipe_cols = st.columns(6)
    for col, step in zip(pipe_cols, PHISHING_PIPELINE_STEPS):
        with col:
            st.markdown(
                f"""
                <div class="pipe-node" style="padding:12px; height:100%;">
                  <div class="cyber-badge" style="font-size:10px; padding:2px 8px;">STEP {step['step']}</div>
                  <div style="font-weight:700; color:#F8FAFC; font-size:13.5px; margin:8px 0 4px 0;">{step['title']}</div>
                  <div style="font-size:12px; color:#94A3B8; line-height:1.4;">{step['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander(f"Peek inside the trained {artifacts.vectorizer_type} + Multinomial Naive Bayes model ({artifacts.vocab_size} learned features)"):
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown("**Top Terms Associated with Phishing (Training Set Only)**")
            st.table(
                pd.DataFrame(artifacts.top_phishing_terms, columns=["Word / Phrase", "Phishing Log-Odds Strength"])
            )
        with t_col2:
            st.markdown("**Top Terms Associated with Legitimate Emails (Training Set Only)**")
            st.table(
                pd.DataFrame(artifacts.top_legit_terms, columns=["Word / Phrase", "Legitimate Log-Odds Strength"])
            )

    # D. Interactive Email Testing
    st.markdown("### D. Interactive Email Tester")
    st.write("Choose a predefined sample email or write/edit your own text, then click **ANALYZE EMAIL**.")

    if "phish_input_text" not in st.session_state:
        st.session_state.phish_input_text = PREDEFINED_SAMPLE_EMAILS["Phishing: Urgent Account Verification"]

    def _apply_sample_email(body: str) -> None:
        st.session_state.phish_input_text = body
        st.session_state.phish_last_result = None

    sample_cols = st.columns(len(PREDEFINED_SAMPLE_EMAILS))
    for idx, (sample_name, sample_body) in enumerate(PREDEFINED_SAMPLE_EMAILS.items()):
        with sample_cols[idx]:
            short_lbl = sample_name.split(": ", 1)[-1]
            st.button(
                short_lbl,
                key=f"sample_email_{idx}",
                use_container_width=True,
                on_click=_apply_sample_email,
                args=(sample_body,),
            )

    user_email = st.text_area(
        "Email content to inspect:",
        key="phish_input_text",
        height=155,
        placeholder="Paste or type an email subject and body here...",
    )

    analyze_clicked = st.button("ANALYZE EMAIL", key="btn_analyze_email", type="primary")
    vec_changed = st.session_state.get("phish_last_vec") != artifacts.vectorizer_type
    if analyze_clicked or vec_changed or st.session_state.get("phish_last_result") is None:
        st.session_state.phish_last_result = (user_email, predict_email(artifacts, user_email))
        st.session_state.phish_last_vec = artifacts.vectorizer_type

    if st.session_state.phish_last_result is not None:
        analyzed_text, res = st.session_state.phish_last_result
        if analyzed_text != user_email:
            st.caption("Email text edited — click **ANALYZE EMAIL** to re-score your updated message.")
        if not res.is_valid:
            st.warning(res.error_message)
        else:
            is_phish = res.predicted_label == "Potential Phishing"
            banner_cls = "result-banner-alert" if is_phish else "result-banner-safe"
            badge_cls = "badge-red" if is_phish else "badge-green"
            title_txt = "POTENTIAL PHISHING" if is_phish else "LEGITIMATE EMAIL"

            st.markdown(
                f"""
                <div class="{banner_cls}">
                  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                    <div>
                      <span class="cyber-badge {badge_cls}">MODEL PREDICTION</span>
                      <h2 style="margin:8px 0 4px 0; font-size:26px;">{title_txt}</h2>
                    </div>
                    <div style="text-align:right; font-family:'JetBrains Mono',monospace;">
                      <div style="font-size:13px; color:#CBD5E1;">Matched Known Vocabulary Terms: <strong>{res.matched_token_count}</strong></div>
                    </div>
                  </div>
                  <p style="margin:8px 0 0 0; color:#F1F5F9; font-size:15px; line-height:1.5;">
                    {html.escape(res.explanation)}
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                "Note: Percentages below are **model scores** produced by Multinomial Naive Bayes on this synthetic dataset—"
                "they are not guaranteed real-world risk probabilities."
            )

            r_col1, r_col2 = st.columns([1.0, 1.2], gap="medium")
            with r_col1:
                fig_prob = plot_probability_bars(
                    ["Legitimate", "Potential Phishing"],
                    [res.legitimate_score, res.phishing_score],
                    ["#10B981", "#F43F5E"],
                    "Model Class Scores (Estimated)",
                )
                st.plotly_chart(fig_prob, use_container_width=True)

                st.markdown("**Highlighted Influencing Words in Your Email**")
                st.markdown(
                    "<span style='font-size:12.5px; color:#94A3B8;'>Red underline = pushed toward Phishing · Green underline = pushed toward Legitimate</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(highlight_email_tokens(analyzed_text, res.influencing_tokens), unsafe_allow_html=True)

            with r_col2:
                fig_tok = plot_token_influences(res.influencing_tokens)
                st.plotly_chart(fig_tok, use_container_width=True)

    # E. Model Evaluation
    st.markdown("### E. Model Evaluation (Strictly Held-Out Test Split)")
    st.write(
        f"These metrics come from testing the trained model on **{artifacts.test_size} unseen emails** "
        f"never shown during training (**{artifacts.train_size} training emails**)."
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{artifacts.accuracy:.1%}")
    m2.metric("Precision (Phishing)", f"{artifacts.precision:.1%}")
    m3.metric("Recall (Phishing)", f"{artifacts.recall:.1%}")
    m4.metric("F1-Score", f"{artifacts.f1:.1%}")

    ev_col1, ev_col2 = st.columns([1.0, 1.1], gap="large")
    with ev_col1:
        st.plotly_chart(
            plot_confusion_matrix(
                artifacts.confusion_mat,
                ["Legitimate", "Phishing"],
                "Confusion Matrix (30 Unseen Test Emails)",
            ),
            use_container_width=True,
        )
    with ev_col2:
        st.markdown("#### What Do These Metrics Mean?")
        for metric_name, metric_desc in METRIC_EXPLANATIONS.items():
            st.markdown(f"- **{metric_name}:** {metric_desc}")

    with st.expander("Inspect Real Held-Out Test Predictions (See where the model succeeded or made mistakes)"):
        st.table(artifacts.test_df.head(15))

    # F. Experiment Challenge
    st.markdown("### F. Experiment Challenge: CAN YOU FOOL THE MODEL?")
    st.markdown(
        """
        <div class="cyber-card">
          <span class="cyber-badge badge-amber">HANDS-ON CHALLENGE</span>
          <h3 style="margin:10px 0 8px 0;">CAN YOU FOOL THE MODEL?</h3>
          <ol style="color:#E2E8F0; font-size:15px; line-height:1.65;">
            <li><strong>Test a normal business email:</strong> Try adding a word like <code>urgent</code> or <code>password</code> to a harmless campus reminder.</li>
            <li><strong>Test a phishing-style email:</strong> Try removing obvious buzzwords like <code>prize</code> or <code>click immediately</code> while still asking politely for login details.</li>
            <li><strong>Rewrite an email</strong> and watch how the model score and highlighted words shift in real time.</li>
          </ol>
          <div style="margin-top:12px; padding:14px; border-radius:10px; background:#09101E; border:1px solid rgba(32,197,232,0.2);">
            <strong style="color:#38BDF8;">Discussion Questions for the Room:</strong>
            <ul style="color:#CBD5E1; font-size:14px; margin:6px 0 0 0;">
              <li>Does the model actually <em>understand</em> the meaning of the email, or is it counting learned word statistics?</li>
              <li>Can it make mistakes (False Positives on urgent legitimate notes, or False Negatives on polite disguised lures)?</li>
              <li>Why is human verification still essential alongside automated ML filters?</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_glossary_section()
