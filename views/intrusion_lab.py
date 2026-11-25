"""Project 02: Network Intrusion Detector interactive educational view."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data import PREDEFINED_NETWORK_SCENARIOS
from education import INTRUSION_PIPELINE_STEPS, METRIC_EXPLANATIONS
from models import FEATURE_LABELS, IntrusionModelArtifacts, predict_network_activity
from ui import (
    plot_confusion_matrix,
    plot_feature_importance,
    plot_local_feature_contributions,
    plot_network_scatter,
    plot_probability_bars,
    render_glossary_section,
    render_learning_pipeline,
)


def render_intrusion_lab(
    df_network: pd.DataFrame,
    artifacts: IntrusionModelArtifacts,
) -> None:
    """Render the complete Project 02 Network Intrusion Detector lab."""
    st.markdown(
        """
        <div class="cyber-hero">
          <span class="cyber-badge">PROJECT 02 · TABULAR CLASSIFICATION</span>
          <h1 style="font-size:36px; margin:10px 0 6px 0;">NETWORK INTRUSION DETECTOR</h1>
          <p style="font-size:16px; color:#CBD5E1; margin:0;">
            Learn how a <strong>Random Forest</strong> model separates normal network behavior from potentially suspicious activity.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Scenario
    st.markdown("### Educational Scenario")
    st.markdown(
        """
        <div class="scenario-box">
          <strong>Your Mission:</strong> "You are a cybersecurity analyst responsible for monitoring a company's network.
          Your mission is to train a Machine Learning model that distinguishes normal network activity from potentially suspicious activity."
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_learning_pipeline(
        "Here, numeric network telemetry indicators replace text words—allowing a Random Forest of 150 decision trees to learn boundary patterns."
    )

    # A. Dataset Explanation
    st.markdown("### A. Synthetic Network Traffic Dataset (600 Records)")
    st.warning(
        "Classroom Simplification Notice: These 4 indicators are simplified synthetic educational signals—not definitive proof of an intrusion "
        "and not a live network scanner. Notice in the scatter plot below that Normal and Suspicious sessions overlap naturally."
    )

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Network Records", len(df_network))
    s2.metric("Normal Sessions (0)", int((df_network["label"] == 0).sum()))
    s3.metric("Suspicious Sessions (1)", int((df_network["label"] == 1).sum()))
    s4.metric("Train / Test Split", "75% / 25% (450 / 150)")

    d_col1, d_col2 = st.columns([1.2, 0.8], gap="medium")
    with d_col1:
        user_pt = st.session_state.get("intrusion_last_point")
        st.plotly_chart(plot_network_scatter(df_network, user_point=user_pt), use_container_width=True)
    with d_col2:
        st.markdown("#### Feature Guide")
        st.markdown(
            """
            - **`failed_logins`**: Number of failed login attempts in the window.
            - **`connection_count`**: Total connections opened during the window.
            - **`data_sent_mb`**: Outgoing data volume (MB) transferred.
            - **`unusual_port`**: Whether a non-standard port was observed (`0` = Standard, `1` = Unusual).
            - **Target `label`**: `0` = Normal, `1` = Suspicious.
            """
        )
        with st.expander("Preview Sample Network Records (first 12 rows)"):
            st.table(df_network.head(12))

    # B. Machine Learning Pipeline
    st.markdown("### B. Machine Learning Pipeline (Random Forest)")
    pipe_cols = st.columns(7)
    for col, step in zip(pipe_cols, INTRUSION_PIPELINE_STEPS):
        with col:
            st.markdown(
                f"""
                <div class="pipe-node" style="padding:11px; height:100%;">
                  <div class="cyber-badge" style="font-size:10px; padding:2px 7px;">STEP {step['step']}</div>
                  <div style="font-weight:700; color:#F8FAFC; font-size:12.5px; margin:7px 0 4px 0;">{step['title']}</div>
                  <div style="font-size:11.5px; color:#94A3B8; line-height:1.38;">{step['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # C & E. Interactive Simulator + 3 Predefined Scenarios
    st.markdown("### C. Interactive Network Traffic Simulator")
    st.write("Load one of the three workshop challenge scenarios or adjust the sliders manually, then click **ANALYZE NETWORK ACTIVITY**.")

    # Initialize defaults from Scenario 3 (Mixed) or Scenario 1
    if "sim_failed" not in st.session_state:
        init_sc = PREDEFINED_NETWORK_SCENARIOS["SCENARIO 1 – NORMAL ACTIVITY"]
        st.session_state.sim_failed = int(init_sc["failed_logins"])
        st.session_state.sim_conn = int(init_sc["connection_count"])
        st.session_state.sim_data = float(init_sc["data_sent_mb"])
        st.session_state.sim_port = int(init_sc["unusual_port"])
        st.session_state.sim_scenario_note = str(init_sc["description"])

    def _apply_network_scenario(sc_vals: dict[str, int | float | str]) -> None:
        st.session_state.sim_failed = int(sc_vals["failed_logins"])
        st.session_state.sim_conn = int(sc_vals["connection_count"])
        st.session_state.sim_data = float(sc_vals["data_sent_mb"])
        st.session_state.sim_port = int(sc_vals["unusual_port"])
        st.session_state.sim_scenario_note = str(sc_vals["description"])
        st.session_state.intrusion_last_res = None

    sc_cols = st.columns(3)
    for idx, (sc_name, sc_vals) in enumerate(PREDEFINED_NETWORK_SCENARIOS.items()):
        with sc_cols[idx]:
            st.button(
                sc_name,
                key=f"net_sc_{idx}",
                use_container_width=True,
                on_click=_apply_network_scenario,
                args=(sc_vals,),
            )

    if st.session_state.get("sim_scenario_note"):
        st.caption(f"Loaded preset context: {st.session_state.sim_scenario_note}")

    in_c1, in_c2, in_c3, in_c4 = st.columns(4)
    with in_c1:
        failed_logins = st.slider("Failed Login Attempts", min_value=0, max_value=30, key="sim_failed")
    with in_c2:
        connection_count = st.slider("Number of Connections", min_value=1, max_value=260, key="sim_conn")
    with in_c3:
        data_sent_mb = st.slider("Data Sent (MB)", min_value=0.0, max_value=650.0, step=0.5, key="sim_data")
    with in_c4:
        port_choice = st.selectbox(
            "Unusual Port Indicator",
            options=[0, 1],
            format_func=lambda v: "0 — Standard Port" if v == 0 else "1 — Unusual Port Observed",
            key="sim_port",
        )

    analyze_net = st.button("ANALYZE NETWORK ACTIVITY", key="btn_analyze_net", type="primary")
    if analyze_net or "intrusion_last_res" not in st.session_state or st.session_state.intrusion_last_res is None:
        res = predict_network_activity(
            artifacts,
            failed_logins=failed_logins,
            connection_count=connection_count,
            data_sent_mb=data_sent_mb,
            unusual_port=port_choice,
        )
        st.session_state.intrusion_last_res = res
        st.session_state.intrusion_last_point = (failed_logins, connection_count, data_sent_mb, port_choice)

    res = st.session_state.intrusion_last_res
    if st.session_state.get("intrusion_last_point") != (failed_logins, connection_count, data_sent_mb, port_choice):
        st.caption("Parameters adjusted — click **ANALYZE NETWORK ACTIVITY** to run the Random Forest model on these values.")
    if res is not None:
        if not res.is_valid:
            st.error(res.error_message)
        else:
            is_susp = res.predicted_class == 1
            banner_cls = "result-banner-alert" if is_susp else "result-banner-safe"
            badge_cls = "badge-red" if is_susp else "badge-green"
            st.markdown(
                f"""
                <div class="{banner_cls}">
                  <span class="cyber-badge {badge_cls}">RANDOM FOREST OUTPUT</span>
                  <h2 style="margin:8px 0 4px 0; font-size:26px;">{res.predicted_label.upper()}</h2>
                  <p style="margin:6px 0 0 0; color:#F1F5F9; font-size:15px; line-height:1.5;">
                    {res.explanation}
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(
                "Note: Scores shown below are the Random Forest tree-vote fractions (model class scores) on simplified synthetic data, "
                "not guaranteed intrusion probabilities."
            )

            p_col1, p_col2 = st.columns([0.95, 1.05], gap="medium")
            with p_col1:
                st.plotly_chart(
                    plot_probability_bars(
                        ["Normal (0)", "Suspicious (1)"],
                        [res.normal_score, res.suspicious_score],
                        ["#10B981", "#F43F5E"],
                        "Model Class Scores (Estimated)",
                    ),
                    use_container_width=True,
                )
            with p_col2:
                st.plotly_chart(
                    plot_local_feature_contributions(res.feature_contributions),
                    use_container_width=True,
                )

    # D. Model Evaluation Dashboard
    st.markdown("### D. Model Evaluation Dashboard (150 Unseen Test Records)")
    em1, em2, em3, em4 = st.columns(4)
    em1.metric("Accuracy", f"{artifacts.accuracy:.1%}")
    em2.metric("Precision (Suspicious)", f"{artifacts.precision:.1%}")
    em3.metric("Recall (Suspicious)", f"{artifacts.recall:.1%}")
    em4.metric("F1-Score", f"{artifacts.f1:.1%}")

    ev1, ev2 = st.columns(2, gap="large")
    with ev1:
        st.plotly_chart(
            plot_confusion_matrix(
                artifacts.confusion_mat,
                ["Normal (0)", "Suspicious (1)"],
                "Confusion Matrix (150 Unseen Network Sessions)",
            ),
            use_container_width=True,
        )
    with ev2:
        st.plotly_chart(
            plot_feature_importance(artifacts.feature_importances, FEATURE_LABELS),
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="cyber-card">
          <h4 style="margin:0 0 8px 0; color:#38BDF8;">Why False Positives &amp; False Negatives Matter in Cybersecurity</h4>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div style="background:#09101E; padding:14px; border-radius:10px; border-left:4px solid #F59E0B;">
              <strong style="color:#FBBF24;">False Positive (False Alarm)</strong>
              <p style="font-size:13.5px; color:#CBD5E1; margin:6px 0 0 0;">
                Flagging a normal employee backup or developer tool as an attack wastes analyst time (<em>alert fatigue</em>)
                and can accidentally lock out legitimate users.
              </p>
            </div>
            <div style="background:#09101E; padding:14px; border-radius:10px; border-left:4px solid #F43F5E;">
              <strong style="color:#FB7185;">False Negative (Missed Threat)</strong>
              <p style="font-size:13.5px; color:#CBD5E1; margin:6px 0 0 0;">
                Allowing stealthy suspicious activity to pass labeled as Normal means a real intrusion could go unnoticed.
              </p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Metric Definitions & Sample Held-Out Test Predictions"):
        for k, v in METRIC_EXPLANATIONS.items():
            st.markdown(f"- **{k}:** {v}")
        st.table(artifacts.test_df.head(12))

    # E. Experiment Challenge Discussion
    st.markdown("### E. Experiment Challenge: Explore Gray-Area Traffic")
    st.markdown(
        """
        <div class="cyber-card">
          <span class="cyber-badge badge-amber">WORKSHOP REFLECTION</span>
          <p style="color:#E2E8F0; font-size:15px; margin-top:10px;">
            Click <strong>SCENARIO 3 – MIXED ACTIVITY</strong> above and slowly nudge one slider at a time
            (for example, raise <code>failed_logins</code> from <code>2</code> to <code>4</code> or toggle <code>unusual_port</code> to <code>1</code>).
          </p>
          <ul style="color:#CBD5E1; font-size:14px; line-height:1.6;">
            <li><strong>Which features influenced the prediction most?</strong> Check the counterfactual chart right under the result banner.</li>
            <li><strong>Can normal activity look suspicious?</strong> Yes—software updates, big cloud backups, or forgotten passwords overlap with attack patterns!</li>
            <li><strong>Can malicious activity look normal?</strong> Yes—slow, low-volume attacks can blend inside normal thresholds.</li>
            <li><strong>Why can't we blindly trust an ML model?</strong> ML sees numbers, not business context—analysts confirm <em>why</em> traffic happened.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_glossary_section()
