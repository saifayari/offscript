"""Custom dark cybersecurity CSS theme for the Streamlit workshop platform."""

import streamlit as st


def inject_cyber_theme() -> None:
    """Inject modern dark navy/black theme with subtle blue & cyan accents."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Poppins:wght@600;700;800&display=swap');

        :root {
            --bg-main: #060A13;
            --bg-card: #0D1526;
            --bg-card-2: #111C33;
            --border-subtle: rgba(32, 197, 232, 0.18);
            --accent-blue: #1769FF;
            --accent-cyan: #20C5E8;
            --accent-violet: #8067FF;
            --text-main: #F1F5F9;
            --text-muted: #94A3B8;
            --ok-green: #10B981;
            --warn-red: #F43F5E;
            --warn-amber: #F59E0B;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 12% 10%, #0C1830 0%, #060A13 55%, #04070E 100%) !important;
            color: var(--text-main);
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(6, 10, 19, 0.78) !important;
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #091020 0%, #060A13 100%) !important;
            border-right: 1px solid rgba(32, 197, 232, 0.15);
        }

        h1, h2, h3, h4 {
            font-family: 'Poppins', 'Segoe UI', system-ui, sans-serif !important;
            letter-spacing: -0.015em;
            color: #F8FAFC !important;
        }

        .block-container {
            padding-top: 3.4rem !important;
            padding-bottom: 3rem !important;
            max-width: 1280px !important;
        }

        @keyframes fadeSlideIn {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .cyber-hero {
            background: linear-gradient(135deg, rgba(23, 105, 255, 0.14) 0%, rgba(13, 21, 38, 0.94) 55%, rgba(32, 197, 232, 0.10) 100%);
            border: 1px solid rgba(32, 197, 232, 0.25);
            border-radius: 18px;
            padding: 26px 30px;
            margin-bottom: 20px;
            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
            animation: fadeSlideIn 0.35s ease-out;
        }

        .cyber-card {
            background: linear-gradient(160deg, rgba(17, 28, 51, 0.92) 0%, rgba(11, 18, 34, 0.96) 100%);
            border: 1px solid rgba(32, 197, 232, 0.18);
            border-radius: 16px;
            padding: 22px 24px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
            transition: transform 0.2s ease, border-color 0.2s ease;
            animation: fadeSlideIn 0.35s ease-out;
        }
        .cyber-card:hover {
            border-color: rgba(32, 197, 232, 0.45);
        }

        .cyber-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            background: rgba(32, 197, 232, 0.14);
            color: #5CE1FF;
            border: 1px solid rgba(32, 197, 232, 0.32);
        }

        .badge-green {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border-color: rgba(16, 185, 129, 0.35);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border-color: rgba(245, 158, 11, 0.35);
        }
        .badge-red {
            background: rgba(244, 63, 94, 0.16);
            color: #FB7185;
            border-color: rgba(244, 63, 94, 0.38);
        }

        .scenario-box {
            background: rgba(23, 105, 255, 0.09);
            border: 1px solid rgba(23, 105, 255, 0.28);
            border-left: 5px solid #20C5E8;
            border-radius: 12px;
            padding: 16px 20px;
            margin: 10px 0 18px 0;
            color: #E2E8F0;
            font-size: 15.5px;
            line-height: 1.55;
        }

        .pipeline-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin: 12px 0 18px 0;
        }
        @media (max-width: 900px) {
            .pipeline-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .pipe-node {
            background: rgba(13, 21, 38, 0.95);
            border: 1px solid rgba(32, 197, 232, 0.2);
            border-radius: 14px;
            padding: 16px;
        }

        .result-banner-safe {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(6, 78, 59, 0.28));
            border: 1.5px solid #10B981;
            border-radius: 14px;
            padding: 18px 22px;
            animation: fadeSlideIn 0.28s ease-out;
        }
        .result-banner-alert {
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.20), rgba(127, 29, 29, 0.26));
            border: 1.5px solid #F43F5E;
            border-radius: 14px;
            padding: 18px 22px;
            animation: fadeSlideIn 0.28s ease-out;
        }

        .token-preview-box {
            background: #09101E;
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 12px;
            padding: 16px 18px;
            line-height: 1.75;
            font-size: 15px;
            color: #E2E8F0;
            white-space: pre-wrap;
        }
        .tok-phish {
            background: rgba(244, 63, 94, 0.28);
            border-bottom: 2px solid #FB7185;
            color: #FFE4E6;
            padding: 1px 5px;
            border-radius: 5px;
            font-weight: 600;
        }
        .tok-legit {
            background: rgba(16, 185, 129, 0.24);
            border-bottom: 2px solid #34D399;
            color: #D1FAE5;
            padding: 1px 5px;
            border-radius: 5px;
            font-weight: 600;
        }

        /* Streamlit Button Polish */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #1769FF 0%, #20C5E8 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(23, 105, 255, 0.35) !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(32, 197, 232, 0.4) !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background: rgba(13, 21, 38, 0.92);
            border: 1px solid rgba(32, 197, 232, 0.18);
            padding: 14px 16px;
            border-radius: 14px;
        }
        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-family: 'Poppins', sans-serif !important;
        }

        .classroom-disclaimer {
            font-size: 12.5px;
            color: #94A3B8;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 10px;
            padding: 10px 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
