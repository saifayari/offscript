"""Real scikit-learn Machine Learning pipelines for Cybersecurity ML Lab."""

from .intrusion_model import (
    FEATURE_COLUMNS,
    FEATURE_LABELS,
    IntrusionModelArtifacts,
    IntrusionPredictionResult,
    predict_network_activity,
    train_intrusion_model,
)
from .phishing_model import (
    PhishingModelArtifacts,
    PhishingPredictionResult,
    predict_email,
    preprocess_email_text,
    train_phishing_model,
)

__all__ = [
    "PhishingModelArtifacts",
    "PhishingPredictionResult",
    "preprocess_email_text",
    "train_phishing_model",
    "predict_email",
    "FEATURE_COLUMNS",
    "FEATURE_LABELS",
    "IntrusionModelArtifacts",
    "IntrusionPredictionResult",
    "train_intrusion_model",
    "predict_network_activity",
]
