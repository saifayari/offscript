"""Reusable Plotly visualizations, SVG cards, and educational widgets."""

from __future__ import annotations

import html
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from education import CORE_PIPELINE_STAGES, GLOSSARY_TERMS


def render_phishing_svg() -> str:
    """Return a clean dark-cyber SVG illustration for Project 01."""
    return (
        '<svg width="100%" height="135" viewBox="0 0 360 135" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="360" height="135" rx="14" fill="#091122"/>'
        '<rect x="34" y="28" width="160" height="82" rx="12" fill="#111D38" stroke="#1769FF" stroke-width="2"/>'
        '<path d="M36 33 L114 78 L192 33" stroke="#20C5E8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="192" cy="40" r="14" fill="#F43F5E"/>'
        '<text x="192" y="45" fill="#FFFFFF" font-size="15" font-weight="800" text-anchor="middle" font-family="Inter">!</text>'
        '<path d="M214 68 H246" stroke="#20C5E8" stroke-width="2.5" stroke-dasharray="4 4"/>'
        '<rect x="252" y="28" width="76" height="36" rx="9" fill="rgba(16,185,129,0.16)" stroke="#10B981" stroke-width="1.8"/>'
        '<text x="290" y="50" fill="#34D399" font-size="11" font-weight="700" text-anchor="middle" font-family="Inter">SAFE</text>'
        '<rect x="252" y="74" width="76" height="36" rx="9" fill="rgba(244,63,94,0.18)" stroke="#F43F5E" stroke-width="1.8"/>'
        '<text x="290" y="96" fill="#FB7185" font-size="11" font-weight="700" text-anchor="middle" font-family="Inter">PHISH</text>'
        '</svg>'
    )


def render_intrusion_svg() -> str:
    """Return a clean dark-cyber SVG illustration for Project 02."""
    return (
        '<svg width="100%" height="135" viewBox="0 0 360 135" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="360" height="135" rx="14" fill="#091122"/>'
        '<path d="M24 98 L72 88 L112 94 L154 78 L188 32 L218 86 L264 76 L332 84" stroke="#20C5E8" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="188" cy="32" r="9" fill="#F43F5E" stroke="#FFE4E6" stroke-width="2"/>'
        '<rect x="206" y="20" width="112" height="24" rx="8" fill="rgba(244,63,94,0.22)" stroke="#F43F5E" stroke-width="1.4"/>'
        '<text x="262" y="36" fill="#FB7185" font-size="10.5" font-weight="700" text-anchor="middle" font-family="JetBrains Mono">ANOMALY SPIKE</text>'
        '<circle cx="72" cy="88" r="4.5" fill="#1769FF"/>'
        '<circle cx="154" cy="78" r="4.5" fill="#1769FF"/>'
        '<circle cx="264" cy="76" r="4.5" fill="#10B981"/>'
        '<text x="28" y="120" fill="#94A3B8" font-size="10" font-family="JetBrains Mono">failed_logins · connections · data_mb · port</text>'
        '</svg>'
    )


def render_learning_pipeline(project_note: str) -> None:
    """Render the core DATA -> TRAINING -> MODEL -> PREDICTION educational strip."""
    cols = st.columns(4)
    for col, stage in zip(cols, CORE_PIPELINE_STAGES):
        with col:
            st.markdown(
                f"""
                <div class="pipe-node" style="border-top: 4px solid {stage['color']}; height: 100%;">
                  <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700; color:{stage['color']};">STAGE {stage['step']}</div>
                  <div style="font-family:'Poppins',sans-serif; font-size:19px; font-weight:700; color:#F8FAFC; margin:4px 0;">{stage['title']}</div>
                  <div style="font-size:13.5px; font-weight:600; color:#E2E8F0; margin-bottom:6px;">{stage['summary']}</div>
                  <div style="font-size:12.5px; color:#94A3B8; line-height:1.45;">{stage['detail']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.caption(project_note)


def render_glossary_section() -> None:
    """Render expandable glossary definitions for ML & cybersecurity fundamentals."""
    with st.expander("Beginner ML & Cybersecurity Glossary (Click to explore 9 key terms)"):
        cols = st.columns(3)
        for idx, (term, desc) in enumerate(GLOSSARY_TERMS.items()):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div style="background:#0A1221; border:1px solid rgba(32,197,232,0.16); border-radius:12px; padding:14px; margin-bottom:10px;">
                      <div style="font-family:'Poppins',sans-serif; font-weight:700; color:#38BDF8; font-size:14.5px; margin-bottom:5px;">{html.escape(term)}</div>
                      <div style="font-size:13px; color:#CBD5E1; line-height:1.45;">{html.escape(desc)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def plot_confusion_matrix(
    cm: np.ndarray, labels: list[str], title: str = "Held-Out Test Confusion Matrix"
) -> go.Figure:
    """Create an annotated dark-theme Plotly confusion matrix."""
    z = cm
    annotations = []
    cell_roles = [["True Negative", "False Positive"], ["False Negative", "True Positive"]]
    for i in range(2):
        for j in range(2):
            annotations.append(
                dict(
                    x=labels[j],
                    y=labels[i],
                    text=f"<b>{z[i, j]}</b><br><span style='font-size:11px'>{cell_roles[i][j]}</span>",
                    showarrow=False,
                    font=dict(color="#F8FAFC", size=14),
                )
            )

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels,
            y=labels,
            colorscale=[[0.0, "#0F1D36"], [0.5, "#1769FF"], [1.0, "#20C5E8"]],
            showscale=False,
            hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#F8FAFC")),
        xaxis=dict(title="Predicted Label", color="#CBD5E1", side="bottom"),
        yaxis=dict(title="Actual Label", color="#CBD5E1", autorange="reversed"),
        annotations=annotations,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
    )
    return fig


def plot_probability_bars(
    class_names: list[str], scores: list[float], colors: list[str], title: str
) -> go.Figure:
    """Render horizontal model score bar chart (labeled clearly as model scores)."""
    fig = go.Figure(
        go.Bar(
            x=[round(s * 100, 1) for s in scores],
            y=class_names,
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{s:.1%}" for s in scores],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=14),
            hovertemplate="%{y}: %{x:.1f}% model score<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#F8FAFC")),
        xaxis=dict(title="Model Score (%)", range=[0, 108], color="#94A3B8", gridcolor="rgba(148,163,184,0.15)"),
        yaxis=dict(color="#F8FAFC"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=20, t=46, b=30),
        height=210,
    )
    return fig


def plot_token_influences(tokens: list[dict[str, float | str]]) -> go.Figure:
    """Plot top token log-odds contributions from the trained Naive Bayes model."""
    if not tokens:
        fig = go.Figure()
        fig.update_layout(
            title="No matching vocabulary tokens found in input",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
        )
        return fig

    ordered = list(reversed(tokens[:8]))
    terms = [str(t["term"]) for t in ordered]
    vals = [float(t["contribution"]) for t in ordered]
    colors = ["#F43F5E" if v > 0 else "#10B981" for v in vals]

    fig = go.Figure(
        go.Bar(
            x=vals,
            y=terms,
            orientation="h",
            marker=dict(color=colors),
            hovertemplate="Token: %{y}<br>Log-odds weight: %{x:+.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Words Influencing This Model Score (← Legitimate | Phishing →)", font=dict(size=14, color="#F8FAFC")),
        xaxis=dict(title="Naive Bayes Contribution", color="#94A3B8", zeroline=True, zerolinecolor="#64748B", gridcolor="rgba(148,163,184,0.12)"),
        yaxis=dict(color="#F8FAFC"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=20, t=46, b=30),
        height=290,
    )
    return fig


def plot_feature_importance(importances: dict[str, float], label_map: dict[str, str]) -> go.Figure:
    """Render Random Forest feature importance bar chart."""
    items = sorted(importances.items(), key=lambda kv: kv[1])
    labels = [label_map.get(k, k) for k, _ in items]
    vals = [v * 100 for _, v in items]

    fig = go.Figure(
        go.Bar(
            x=vals,
            y=labels,
            orientation="h",
            marker=dict(color=["#8067FF", "#1769FF", "#20C5E8", "#38BDF8"][: len(vals)]),
            text=[f"{v:.1f}%" for v in vals],
            textposition="auto",
        )
    )
    fig.update_layout(
        title=dict(text="Random Forest Feature Importance (Global)", font=dict(size=16, color="#F8FAFC")),
        xaxis=dict(title="Relative Importance (%)", range=[0, max(vals) * 1.2 + 5], color="#94A3B8", gridcolor="rgba(148,163,184,0.15)"),
        yaxis=dict(color="#F8FAFC"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=30),
        height=320,
    )
    return fig


def plot_local_feature_contributions(contributions: list[dict[str, float | str]]) -> go.Figure:
    """Plot per-prediction Random Forest counterfactual feature shifts."""
    ordered = list(reversed(contributions))
    labels = [str(c["label"]) for c in ordered]
    raw_deltas = [float(c["delta_suspicious"]) * 100 for c in ordered]
    deltas = [0.0 if abs(d) < 0.05 else d for d in raw_deltas]
    colors = ["#F43F5E" if d > 0 else ("#10B981" if d < 0 else "#64748B") for d in deltas]
    max_abs = max([abs(d) for d in deltas] + [10.0]) * 1.2

    fig = go.Figure(
        go.Bar(
            x=deltas,
            y=labels,
            orientation="h",
            marker=dict(color=colors),
            text=[f"{d:+.1f} pts" if d != 0 else "0.0 pts" for d in deltas],
            textposition="auto",
        )
    )
    fig.update_layout(
        title=dict(text="How Each Input Shifted the Suspicious Score vs. Normal Baseline", font=dict(size=14, color="#F8FAFC")),
        xaxis=dict(
            title="Score Shift (percentage points)",
            range=[-max_abs, max_abs],
            color="#94A3B8",
            zeroline=True,
            zerolinecolor="#64748B",
            gridcolor="rgba(148,163,184,0.12)",
        ),
        yaxis=dict(color="#F8FAFC"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=20, t=46, b=30),
        height=270,
    )
    return fig


def plot_network_scatter(
    df: pd.DataFrame,
    user_point: tuple[int, int, float, int] | None = None,
) -> go.Figure:
    """Visualize network traffic overlap and optional live simulated session."""
    norm = df[df["label"] == 0]
    susp = df[df["label"] == 1]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=norm["connection_count"],
            y=norm["data_sent_mb"],
            mode="markers",
            name="Normal (0)",
            marker=dict(color="#10B981", size=7, opacity=0.65),
            customdata=norm[["failed_logins", "unusual_port"]],
            hovertemplate="Normal<br>Connections: %{x}<br>Data Sent: %{y} MB<br>Failed Logins: %{customdata[0]}<br>Unusual Port: %{customdata[1]}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=susp["connection_count"],
            y=susp["data_sent_mb"],
            mode="markers",
            name="Suspicious (1)",
            marker=dict(color="#F43F5E", size=7, opacity=0.68, symbol="diamond"),
            customdata=susp[["failed_logins", "unusual_port"]],
            hovertemplate="Suspicious<br>Connections: %{x}<br>Data Sent: %{y} MB<br>Failed Logins: %{customdata[0]}<br>Unusual Port: %{customdata[1]}<extra></extra>",
        )
    )

    if user_point is not None:
        fl, cc, ds, up = user_point
        fig.add_trace(
            go.Scatter(
                x=[cc],
                y=[ds],
                mode="markers+text",
                name="Your Simulated Session",
                text=["YOU"],
                textposition="top center",
                textfont=dict(color="#38BDF8", size=12),
                marker=dict(color="#38BDF8", size=16, symbol="star", line=dict(color="#FFFFFF", width=1.5)),
            )
        )

    fig.update_layout(
        title=dict(text="Dataset Distribution: Connections vs. Data Sent (Showing Natural Overlap)", font=dict(size=15, color="#F8FAFC")),
        xaxis=dict(title="Connection Count", color="#94A3B8", gridcolor="rgba(148,163,184,0.12)"),
        yaxis=dict(title="Data Sent (MB)", color="#94A3B8", gridcolor="rgba(148,163,184,0.12)"),
        legend=dict(font=dict(color="#E2E8F0"), orientation="h", yanchor="bottom", y=1.02, x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=65, b=30),
        height=360,
    )
    return fig


def highlight_email_tokens(raw_text: str, influencing_tokens: list[dict[str, float | str]]) -> str:
    """Safely escape user email text and highlight single-word influencing tokens."""
    escaped = html.escape(raw_text)
    word_map: dict[str, str] = {}
    for item in influencing_tokens:
        term = str(item["term"])
        if " " in term:
            continue
        cls = "tok-phish" if str(item["direction"]) == "Phishing" else "tok-legit"
        word_map[term.lower()] = cls

    if not word_map:
        return f'<div class="token-preview-box">{escaped}</div>'

    # Sort longest words first to prevent partial word replacement
    terms_sorted = sorted(word_map.keys(), key=len, reverse=True)
    pattern = re.compile(r"\b(" + "|".join(re.escape(t) for t in terms_sorted) + r")\b", re.IGNORECASE)

    def _repl(match: re.Match[str]) -> str:
        w = match.group(0)
        cls = word_map.get(w.lower(), "")
        return f'<span class="{cls}">{w}</span>' if cls else w

    highlighted = pattern.sub(_repl, escaped)
    return f'<div class="token-preview-box">{highlighted}</div>'
