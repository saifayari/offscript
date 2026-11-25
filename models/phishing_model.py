"""Phishing Email Detector ML pipeline using scikit-learn Multinomial Naive Bayes.

Demonstrates a leak-free supervised text classification workflow:
    1. Labeled email dataset
    2. Train/test split BEFORE fitting vectorizer
    3. Text preprocessing & numerical vectorization (TF-IDF or CountVectorizer)
    4. Multinomial Naive Bayes classifier training
    5. Held-out test evaluation
    6. Live inference with authentic token log-odds explanations
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


@dataclass
class PhishingModelArtifacts:
    """Container for trained phishing classifier and held-out test metrics."""

    pipeline: Pipeline
    vectorizer_type: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion_mat: np.ndarray
    train_size: int
    test_size: int
    vocab_size: int
    top_phishing_terms: list[tuple[str, float]]
    top_legit_terms: list[tuple[str, float]]
    test_df: pd.DataFrame


@dataclass
class PhishingPredictionResult:
    """Prediction output and authentic per-token explanations for one email."""

    is_valid: bool
    error_message: str | None
    predicted_label: str | None
    legitimate_score: float
    phishing_score: float
    matched_token_count: int
    influencing_tokens: list[dict[str, float | str]]
    explanation: str


def preprocess_email_text(raw_text: str) -> str:
    """Normalize whitespace and strip control artifacts while keeping educational readability."""
    if not isinstance(raw_text, str):
        return ""
    cleaned = re.sub(r"\s+", " ", raw_text).strip()
    return cleaned


def train_phishing_model(
    df: pd.DataFrame,
    vectorizer_type: Literal["TF-IDF", "CountVectorizer"] = "TF-IDF",
    seed: int = 42,
) -> PhishingModelArtifacts:
    """Train and evaluate a Multinomial Naive Bayes phishing detector without data leakage."""
    X = df["text"].apply(preprocess_email_text)
    y = df["label"]

    # Split BEFORE fitting vectorizer so test vocabulary never leaks into training statistics
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=seed
    )

    if vectorizer_type == "CountVectorizer":
        vectorizer = CountVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_-]{1,}\b",
        )
    else:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_-]{1,}\b",
        )

    pipeline = Pipeline(
        [
            ("vectorizer", vectorizer),
            ("classifier", MultinomialNB(alpha=1.0)),
        ]
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label="Phishing", zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label="Phishing", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label="Phishing", zero_division=0))
    cm = confusion_matrix(y_test, y_pred, labels=["Legitimate", "Phishing"])

    vec = pipeline.named_steps["vectorizer"]
    clf: MultinomialNB = pipeline.named_steps["classifier"]
    feature_names = vec.get_feature_names_out()
    classes = list(clf.classes_)
    phish_idx = classes.index("Phishing")
    legit_idx = classes.index("Legitimate")

    # Log-likelihood ratio learned by Multinomial Naive Bayes
    log_odds = clf.feature_log_prob_[phish_idx] - clf.feature_log_prob_[legit_idx]
    sorted_idx = np.argsort(log_odds)

    top_legit = [(str(feature_names[i]), float(-log_odds[i])) for i in sorted_idx[:10]]
    top_phish = [(str(feature_names[i]), float(log_odds[i])) for i in sorted_idx[-10:][::-1]]

    test_df = pd.DataFrame(
        {
            "email_preview": [t[:95] + ("..." if len(t) > 95 else "") for t in X_test],
            "actual_label": y_test.values,
            "predicted_label": y_pred,
            "correct": y_test.values == y_pred,
        }
    )

    return PhishingModelArtifacts(
        pipeline=pipeline,
        vectorizer_type=vectorizer_type,
        accuracy=acc,
        precision=prec,
        recall=rec,
        f1=f1,
        confusion_mat=cm,
        train_size=len(X_train),
        test_size=len(X_test),
        vocab_size=len(feature_names),
        top_phishing_terms=top_phish,
        top_legit_terms=top_legit,
        test_df=test_df,
    )


def predict_email(
    artifacts: PhishingModelArtifacts, raw_email_text: str
) -> PhishingPredictionResult:
    """Classify an input email and extract token-level log-odds influence from the trained model."""
    cleaned = preprocess_email_text(raw_email_text)
    if not cleaned:
        return PhishingPredictionResult(
            is_valid=False,
            error_message="Please enter or select an email before analyzing.",
            predicted_label=None,
            legitimate_score=0.0,
            phishing_score=0.0,
            matched_token_count=0,
            influencing_tokens=[],
            explanation="",
        )

    alpha_chars = sum(1 for ch in cleaned if ch.isalpha())
    if alpha_chars < 3:
        return PhishingPredictionResult(
            is_valid=False,
            error_message="Please enter meaningful email text (at least a few words) so the text model can extract features.",
            predicted_label=None,
            legitimate_score=0.0,
            phishing_score=0.0,
            matched_token_count=0,
            influencing_tokens=[],
            explanation="",
        )

    vec = artifacts.pipeline.named_steps["vectorizer"]
    clf: MultinomialNB = artifacts.pipeline.named_steps["classifier"]

    x_vec = vec.transform([cleaned])
    probs = clf.predict_proba(x_vec)[0]
    classes = list(clf.classes_)
    legit_idx = classes.index("Legitimate")
    phish_idx = classes.index("Phishing")

    legit_score = float(probs[legit_idx])
    phish_score = float(probs[phish_idx])
    predicted_label = "Potential Phishing" if phish_score >= 0.5 else "Legitimate"

    # Extract per-token contributions from MultinomialNB parameters
    feature_names = vec.get_feature_names_out()
    log_odds_all = clf.feature_log_prob_[phish_idx] - clf.feature_log_prob_[legit_idx]
    nonzero_cols = x_vec.nonzero()[1]

    token_impacts: list[dict[str, float | str]] = []
    for col in nonzero_cols:
        weight = float(x_vec[0, col])
        contrib = float(weight * log_odds_all[col])
        token_impacts.append(
            {
                "term": str(feature_names[col]),
                "contribution": contrib,
                "direction": "Phishing" if contrib > 0 else "Legitimate",
                "abs_impact": abs(contrib),
            }
        )

    token_impacts.sort(key=lambda item: float(item["abs_impact"]), reverse=True)
    top_tokens = token_impacts[:10]

    if len(nonzero_cols) == 0:
        explanation = (
            "None of the words in this input appeared in the training vocabulary, so the model "
            "fell back purely to the baseline class balance in the training dataset. This shows "
            "why Machine Learning models struggle with completely unfamiliar wording."
        )
    else:
        phish_words = [str(t["term"]) for t in top_tokens if float(t["contribution"]) > 0][:4]
        legit_words = [str(t["term"]) for t in top_tokens if float(t["contribution"]) < 0][:4]
        if predicted_label == "Potential Phishing":
            clue_text = ", ".join(f"'{w}'" for w in phish_words) if phish_words else "the overall word pattern"
            explanation = (
                f"The Naive Bayes classifier scored this email higher for Phishing ({phish_score:.1%}) "
                f"because terms such as {clue_text} appeared much more frequently in synthetic phishing "
                "training examples than in legitimate emails."
            )
        else:
            clue_text = ", ".join(f"'{w}'" for w in legit_words) if legit_words else "the overall word pattern"
            explanation = (
                f"The Naive Bayes classifier scored this email higher for Legitimate ({legit_score:.1%}) "
                f"because words like {clue_text} matched normal workplace/university patterns seen during training."
            )

    return PhishingPredictionResult(
        is_valid=True,
        error_message=None,
        predicted_label=predicted_label,
        legitimate_score=legit_score,
        phishing_score=phish_score,
        matched_token_count=int(len(nonzero_cols)),
        influencing_tokens=top_tokens,
        explanation=explanation,
    )
