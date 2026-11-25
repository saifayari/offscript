"""Synthetic educational datasets for Cybersecurity ML Lab."""

from .datasets import (
    PREDEFINED_NETWORK_SCENARIOS,
    PREDEFINED_SAMPLE_EMAILS,
    generate_network_dataset,
    generate_phishing_dataset,
)

__all__ = [
    "generate_phishing_dataset",
    "generate_network_dataset",
    "PREDEFINED_SAMPLE_EMAILS",
    "PREDEFINED_NETWORK_SCENARIOS",
]
