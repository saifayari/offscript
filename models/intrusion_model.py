"""Network Intrusion Detector ML pipeline using scikit-learn Random Forest.

Demonstrates a leak-free supervised tabular classification workflow:
    1. Synthetic network telemetry records (600 records)
    2. Feature/label separation
    3. Stratified train/test split
    4. Random Forest classifier training
    5. Held-out test evaluation + feature importance
    6. Interactive inference with counterfactual feature influence explanations
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = ["failed_logins", "connection_count", "data_sent_mb", "unusual_port"]

FEATURE_LABELS = {
    "failed_logins": "Failed Login Attempts",
    "connection_count": "Connection Count",
    "data_sent_mb": "Data Sent (MB)",
    "unusual_port": "Unusual Port (0/1)",
}


@dataclass
class IntrusionModelArtifacts:
    """Container for trained Random Forest intrusion detector and test evaluation."""

    model: RandomForestClassifier
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion_mat: np.ndarray
    feature_importances: dict[str, float]
    normal_baseline: dict[str, float]
    suspicious_baseline: dict[str, float]
    train_size: int
    test_size: int
    test_df: pd.DataFrame


@dataclass
class IntrusionPredictionResult:
    """Prediction output and model-driven feature influence breakdown."""

    is_valid: bool
    error_message: str | None
    predicted_label: str | None
    predicted_class: int | None
    normal_score: float
    suspicious_score: float
    feature_contributions: list[dict[str, float | str]]
    explanation: str


def train_intrusion_model(
    df: pd.DataFrame, seed: int = 42
) -> IntrusionModelArtifacts:
    """Train and evaluate a Random Forest classifier on synthetic network records."""
    X = df[FEATURE_COLUMNS].copy()
    y = df["label"].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=seed
    )

    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_leaf=2,
        random_state=seed,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label=1, zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label=1, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label=1, zero_division=0))
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

    importances = {
        col: float(imp) for col, imp in zip(FEATURE_COLUMNS, rf.feature_importances_)
    }

    # Compute training-set medians per class strictly from X_train (no test leakage)
    normal_mask = y_train == 0
    susp_mask = y_train == 1
    normal_baseline = {
        col: float(X_train.loc[normal_mask, col].median()) for col in FEATURE_COLUMNS
    }
    suspicious_baseline = {
        col: float(X_train.loc[susp_mask, col].median()) for col in FEATURE_COLUMNS
    }

    test_df = X_test.copy()
    test_df["actual"] = np.where(y_test.values == 1, "Suspicious", "Normal")
    test_df["predicted"] = np.where(y_pred == 1, "Suspicious", "Normal")
    test_df["correct"] = y_test.values == y_pred

    return IntrusionModelArtifacts(
        model=rf,
        accuracy=acc,
        precision=prec,
        recall=rec,
        f1=f1,
        confusion_mat=cm,
        feature_importances=importances,
        normal_baseline=normal_baseline,
        suspicious_baseline=suspicious_baseline,
        train_size=len(X_train),
        test_size=len(X_test),
        test_df=test_df,
    )


def predict_network_activity(
    artifacts: IntrusionModelArtifacts,
    failed_logins: int,
    connection_count: int,
    data_sent_mb: float,
    unusual_port: int,
) -> IntrusionPredictionResult:
    """Validate network telemetry inputs, run Random Forest inference, and explain drivers."""
    try:
        fl = int(failed_logins)
        cc = int(connection_count)
        ds = float(data_sent_mb)
        up = int(unusual_port)
    except (TypeError, ValueError):
        return IntrusionPredictionResult(
            is_valid=False,
            error_message="All network traffic inputs must be valid numbers.",
            predicted_label=None,
            predicted_class=None,
            normal_score=0.0,
            suspicious_score=0.0,
            feature_contributions=[],
            explanation="",
        )

    if fl < 0 or fl > 500 or cc < 0 or cc > 10000 or ds < 0 or ds > 100000 or up not in (0, 1):
        return IntrusionPredictionResult(
            is_valid=False,
            error_message=(
                "Input values are outside valid bounds: failed_logins (0-500), "
                "connection_count (0-10000), data_sent_mb (0-100000), unusual_port (0 or 1)."
            ),
            predicted_label=None,
            predicted_class=None,
            normal_score=0.0,
            suspicious_score=0.0,
            feature_contributions=[],
            explanation="",
        )

    sample = {
        "failed_logins": fl,
        "connection_count": cc,
        "data_sent_mb": ds,
        "unusual_port": up,
    }
    input_df = pd.DataFrame([sample], columns=FEATURE_COLUMNS)
    probs = artifacts.model.predict_proba(input_df)[0]
    classes = list(artifacts.model.classes_)
    norm_idx = classes.index(0)
    susp_idx = classes.index(1)

    normal_score = float(probs[norm_idx])
    suspicious_score = float(probs[susp_idx])
    pred_class = 1 if suspicious_score >= 0.5 else 0
    pred_label = "Potentially Suspicious Activity" if pred_class == 1 else "Normal Activity"

    # Measure authentic local sensitivity of the trained Random Forest to each feature:
    # replace one feature at a time with the training Normal-class median and measure delta P(Suspicious)
    contributions: list[dict[str, float | str]] = []
    for col in FEATURE_COLUMNS:
        cf_sample = dict(sample)
        cf_sample[col] = artifacts.normal_baseline[col]
        cf_df = pd.DataFrame([cf_sample], columns=FEATURE_COLUMNS)
        cf_susp = float(artifacts.model.predict_proba(cf_df)[0][susp_idx])
        delta_susp = suspicious_score - cf_susp
        contributions.append(
            {
                "feature": col,
                "label": FEATURE_LABELS[col],
                "user_value": float(sample[col]),
                "normal_median": float(artifacts.normal_baseline[col]),
                "delta_suspicious": delta_susp,
                "global_importance": float(artifacts.feature_importances[col]),
                "abs_delta": abs(delta_susp),
            }
        )

    contributions.sort(key=lambda item: float(item["abs_delta"]), reverse=True)

    # Build a grounded explanation from the actual Random Forest drivers
    top_push_susp = [c for c in contributions if float(c["delta_suspicious"]) > 0.03]
    if pred_class == 1:
        if top_push_susp:
            drivers = ", ".join(
                f"{c['label']} ({c['user_value']:.0f})" if c["feature"] != "data_sent_mb" else f"{c['label']} ({c['user_value']:.1f} MB)"
                for c in top_push_susp[:3]
            )
            explanation = (
                f"The Random Forest ensemble scored this activity as Potentially Suspicious ({suspicious_score:.1%}). "
                f"Changing {drivers} away from typical normal values caused the strongest upward shift in the suspicious score."
            )
        else:
            explanation = (
                f"The Random Forest ensemble scored this activity as Potentially Suspicious ({suspicious_score:.1%}) "
                "based on the combined interaction across all four network indicators."
            )
    else:
        explanation = (
            f"The Random Forest ensemble classified this traffic as Normal Activity ({normal_score:.1%}). "
            "The combination of failed logins, connection volume, outbound data, and port status aligns closely "
            "with normal baseline patterns learned during training."
        )

    return IntrusionPredictionResult(
        is_valid=True,
        error_message=None,
        predicted_label=pred_label,
        predicted_class=pred_class,
        normal_score=normal_score,
        suspicious_score=suspicious_score,
        feature_contributions=contributions,
        explanation=explanation,
    )
