"""UI theme, Plotly visualizations, and educational components."""

from .components import (
    highlight_email_tokens,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_local_feature_contributions,
    plot_network_scatter,
    plot_probability_bars,
    plot_token_influences,
    render_glossary_section,
    render_intrusion_svg,
    render_learning_pipeline,
    render_phishing_svg,
)
from .theme import inject_cyber_theme

__all__ = [
    "inject_cyber_theme",
    "render_phishing_svg",
    "render_intrusion_svg",
    "render_learning_pipeline",
    "render_glossary_section",
    "plot_confusion_matrix",
    "plot_probability_bars",
    "plot_token_influences",
    "plot_feature_importance",
    "plot_local_feature_contributions",
    "plot_network_scatter",
    "highlight_email_tokens",
]
