"""Automated tests for datasets, ML pipelines, leak-freedom, and Streamlit UI."""

from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest

from data import (
    PREDEFINED_NETWORK_SCENARIOS,
    PREDEFINED_SAMPLE_EMAILS,
    generate_network_dataset,
    generate_phishing_dataset,
)
from models import (
    FEATURE_COLUMNS,
    predict_email,
    predict_network_activity,
    train_intrusion_model,
    train_phishing_model,
)


def test_phishing_dataset_size_and_balance():
    df = generate_phishing_dataset(seed=42)
    assert len(df) >= 100
    assert set(df["label"].unique()) == {"Legitimate", "Phishing"}
    assert df["text"].nunique() == len(df)


def test_network_dataset_size_and_features():
    df = generate_network_dataset(n_samples=600, seed=42)
    assert len(df) >= 500
    for col in FEATURE_COLUMNS + ["label"]:
        assert col in df.columns
    assert set(df["label"].unique()) == {0, 1}
    assert set(df["unusual_port"].unique()).issubset({0, 1})


def test_phishing_model_both_vectorizers_and_validation():
    df = generate_phishing_dataset(seed=42)
    for vec_type in ("TF-IDF", "CountVectorizer"):
        art = train_phishing_model(df, vectorizer_type=vec_type, seed=42)
        assert art.train_size + art.test_size == len(df)
        assert 0.5 <= art.accuracy <= 1.0
        assert art.confusion_mat.shape == (2, 2)

        phish_sample = PREDEFINED_SAMPLE_EMAILS["Phishing: Urgent Account Verification"]
        res_phish = predict_email(art, phish_sample)
        assert res_phish.is_valid
        assert res_phish.predicted_label == "Potential Phishing"
        assert pytest.approx(res_phish.legitimate_score + res_phish.phishing_score, abs=1e-6) == 1.0

        legit_sample = PREDEFINED_SAMPLE_EMAILS["Legitimate: Team Workshop Update"]
        res_legit = predict_email(art, legit_sample)
        assert res_legit.is_valid
        assert res_legit.predicted_label == "Legitimate"

        # Invalid/empty & out-of-vocab inputs handled gracefully
        assert not predict_email(art, "   ").is_valid
        assert not predict_email(art, "12345 !!!").is_valid
        oov = predict_email(art, "xyzzy qwerty blargle")
        assert oov.is_valid
        assert oov.matched_token_count == 0


def test_intrusion_model_metrics_scenarios_and_validation():
    df = generate_network_dataset(n_samples=600, seed=42)
    art = train_intrusion_model(df, seed=42)
    assert art.train_size + art.test_size == len(df)
    assert 0.7 <= art.accuracy <= 1.0
    assert art.confusion_mat.shape == (2, 2)
    assert pytest.approx(sum(art.feature_importances.values()), abs=1e-6) == 1.0

    sc1 = PREDEFINED_NETWORK_SCENARIOS["SCENARIO 1 – NORMAL ACTIVITY"]
    r1 = predict_network_activity(
        art, sc1["failed_logins"], sc1["connection_count"], sc1["data_sent_mb"], sc1["unusual_port"]
    )
    assert r1.is_valid and r1.predicted_class == 0

    sc2 = PREDEFINED_NETWORK_SCENARIOS["SCENARIO 2 – SUSPICIOUS ACTIVITY"]
    r2 = predict_network_activity(
        art, sc2["failed_logins"], sc2["connection_count"], sc2["data_sent_mb"], sc2["unusual_port"]
    )
    assert r2.is_valid and r2.predicted_class == 1

    # Invalid inputs rejected gracefully
    bad1 = predict_network_activity(art, -1, 10, 20.0, 0)
    bad2 = predict_network_activity(art, 1, 10, 20.0, 5)
    assert not bad1.is_valid
    assert not bad2.is_valid


def test_streamlit_app_navigation_and_interactions():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    assert not at.exception

    # Navigate to Project 01 via Home Start Challenge button
    start_p1 = next(b for b in at.button if b.key == "start_p1")
    start_p1.click().run()
    assert not at.exception

    # Click Legitimate sample button and ANALYZE EMAIL
    legit_btn = next(b for b in at.button if b.key == "sample_email_0")
    legit_btn.click().run()
    assert not at.exception
    analyze_btn = next(b for b in at.button if b.key == "btn_analyze_email")
    analyze_btn.click().run()
    assert not at.exception

    # Navigate to Project 02 via sidebar radio
    nav = next(r for r in at.sidebar.radio if r.key == "sidebar_nav_radio")
    nav.set_value("Project 02: Network Intrusion Detector").run()
    assert not at.exception

    # Click Scenario 2 and ANALYZE NETWORK ACTIVITY
    sc2_btn = next(b for b in at.button if b.key == "net_sc_1")
    sc2_btn.click().run()
    net_btn = next(b for b in at.button if b.key == "btn_analyze_net")
    net_btn.click().run()
    assert not at.exception

    # Navigate to Comparison and Quiz pages
    nav = next(r for r in at.sidebar.radio if r.key == "sidebar_nav_radio")
    nav.set_value("Comparison: Two Cyber Problems").run()
    assert not at.exception

    nav = next(r for r in at.sidebar.radio if r.key == "sidebar_nav_radio")
    nav.set_value("Final Knowledge Check (Quiz)").run()
    assert not at.exception

    # Answer all 5 quiz questions correctly and submit
    for q_idx in range(1, 6):
        q_radio = next(r for r in at.radio if r.key == f"quiz_q{q_idx}")
        q_radio.set_value(1 if q_idx < 5 else 0)
    submit_btn = at.button[0]
    submit_btn.click().run()
    assert not at.exception
