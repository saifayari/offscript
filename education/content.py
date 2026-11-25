"""Structured educational explanations, glossary, pipelines, and quiz content."""

from __future__ import annotations

CORE_PIPELINE_STAGES: list[dict[str, str]] = [
    {
        "step": "01",
        "title": "DATA",
        "summary": "Examples used to teach the model.",
        "detail": "Clean, labeled historical records (emails or network traffic logs) that show what normal and suspicious cases look like.",
        "color": "#1769FF",
    },
    {
        "step": "02",
        "title": "TRAINING",
        "summary": "The algorithm learns statistical patterns from labeled examples.",
        "detail": "During training, the algorithm adjusts mathematical probabilities or decision trees using ONLY the training split.",
        "color": "#20C5E8",
    },
    {
        "step": "03",
        "title": "MODEL",
        "summary": "The trained representation used to make predictions.",
        "detail": "A compact mathematical engine (such as learned word weights or an ensemble of decision trees) saved after training.",
        "color": "#8067FF",
    },
    {
        "step": "04",
        "title": "PREDICTION",
        "summary": "The model applies what it learned to new data.",
        "detail": "Given an unseen email or network session, the model outputs a predicted label and estimated class scores.",
        "color": "#10B981",
    },
]

GLOSSARY_TERMS: dict[str, str] = {
    "Supervised Learning": (
        "A type of Machine Learning where a model learns from examples that already have the correct "
        "answer (label) attached—like emails tagged 'Legitimate' or 'Phishing'."
    ),
    "Features": (
        "The measurable inputs given to an ML model—for example, word frequencies in an email or "
        "failed login counts and megabytes sent on a network."
    ),
    "Labels": (
        "The target category or answer we want the model to predict (such as Phishing vs. Legitimate, "
        "or Suspicious vs. Normal)."
    ),
    "Training Data": (
        "The portion of the dataset used to teach the algorithm patterns. Typically 70–80% of the records."
    ),
    "Testing Data": (
        "A separate, unseen portion of the dataset held back during training so we can fairly measure "
        "how well the model generalizes to new inputs."
    ),
    "Classification": (
        "A supervised ML task where the goal is to assign an input into discrete categories "
        "(for example, classifying an email as Legitimate or Phishing)."
    ),
    "Overfitting": (
        "When a model memorizes the training examples (including random noise) instead of learning general "
        "patterns—resulting in high training scores but poor performance on real unseen data."
    ),
    "False Positives": (
        "False alarms: the model flags benign activity as a threat (e.g., blocking a real university email "
        "or flagging a legitimate developer backup as an intrusion)."
    ),
    "False Negatives": (
        "Missed threats: a genuine phishing email or malicious network activity slips through classified "
        "as safe/normal."
    ),
}

METRIC_EXPLANATIONS: dict[str, str] = {
    "Accuracy": "Overall percentage of unseen test examples the model classified correctly.",
    "Precision": "Out of everything the model flagged as a threat, what share was actually a threat? (Low precision = many false alarms.)",
    "Recall": "Out of all real threats in the test set, what share did the model catch? (Low recall = dangerous missed attacks.)",
    "F1-score": "A balanced single score combining Precision and Recall—especially helpful when classes are uneven.",
    "Confusion Matrix": "A 2×2 grid comparing actual labels vs. predicted labels so you can see True Positives, True Negatives, False Positives, and False Negatives.",
}

PHISHING_PIPELINE_STEPS: list[dict[str, str]] = [
    {"step": "1", "title": "Collect Labeled Email Data", "desc": "Gather synthetic examples labeled Legitimate or Phishing."},
    {"step": "2", "title": "Preprocess Text", "desc": "Normalize whitespace, lowercase words, and remove common filler stop-words."},
    {"step": "3", "title": "Numerical Features (TF-IDF / Count)", "desc": "Convert words and 2-word phrases into numeric frequency vectors."},
    {"step": "4", "title": "Train Multinomial Naive Bayes", "desc": "Learn how strongly each word correlates with Phishing vs. Legitimate emails."},
    {"step": "5", "title": "Evaluate on Unseen Test Split", "desc": "Score Accuracy, Precision, Recall, F1, and the Confusion Matrix on held-out emails."},
    {"step": "6", "title": "Predict & Explain New Email", "desc": "Classify a new email and highlight the exact tokens driving the score."},
]

INTRUSION_PIPELINE_STEPS: list[dict[str, str]] = [
    {"step": "1", "title": "Collect Network Traffic Data", "desc": "Gather 600 synthetic network telemetry records with 4 behavioral indicators."},
    {"step": "2", "title": "Prepare & Inspect Dataset", "desc": "Check ranges, class distribution, and realistic overlap between classes."},
    {"step": "3", "title": "Separate Features & Labels", "desc": "Split X (4 numeric columns) from target y (0 = Normal, 1 = Suspicious)."},
    {"step": "4", "title": "Split Train & Test Sets", "desc": "Hold out 25% of records in a stratified test split to prevent leakage."},
    {"step": "5", "title": "Train Random Forest Classifier", "desc": "Build an ensemble of 150 decision trees voting together on traffic patterns."},
    {"step": "6", "title": "Evaluate & Inspect Importance", "desc": "Check Accuracy, Precision, Recall, F1, Confusion Matrix, and top indicators."},
    {"step": "7", "title": "Predict New Network Activity", "desc": "Test live scenarios and see which inputs shifted the model's score."},
]

PROJECT_COMPARISON_ROWS: list[dict[str, str]] = [
    {"Element": "Data", "Phishing Detection": "Text (email subject & body)", "Intrusion Detection": "Numerical network features"},
    {"Element": "Feature Extraction", "Phishing Detection": "TF-IDF / CountVectorizer word vectors", "Intrusion Detection": "Direct numeric telemetry columns"},
    {"Element": "Algorithm", "Phishing Detection": "Multinomial Naive Bayes", "Intrusion Detection": "Random Forest Classifier"},
    {"Element": "Task", "Phishing Detection": "Text classification", "Intrusion Detection": "Tabular classification"},
    {"Element": "Output", "Phishing Detection": "Legitimate / Potential Phishing", "Intrusion Detection": "Normal / Potentially Suspicious"},
]

QUIZ_QUESTIONS: list[dict[str, object]] = [
    {
        "id": "q1",
        "question": "1. What is supervised learning?",
        "options": [
            "Training a model using unlabeled random numbers with no expected answers.",
            "Training a model on labeled examples where the correct output is already known.",
            "Hardcoding manual IF/ELSE security rules written by a human analyst.",
            "Scanning live internet routers automatically without human permission.",
        ],
        "correct_index": 1,
        "explanation": (
            "In supervised learning, every training example includes an input (features) AND a known "
            "correct answer (label), allowing the algorithm to learn patterns that generalize to new data."
        ),
    },
    {
        "id": "q2",
        "question": "2. Why do we split a dataset into training data and testing data?",
        "options": [
            "To make the spreadsheet file smaller so Python opens faster.",
            "To evaluate whether the model generalizes to unseen data instead of memorizing training examples.",
            "Because scikit-learn cannot run unless half the dataset is deleted.",
            "To allow the test labels to be used during training for higher accuracy.",
        ],
        "correct_index": 1,
        "explanation": (
            "Evaluating a model on the same examples it trained on hides overfitting. Testing data acts as a "
            "fair exam using unseen examples."
        ),
    },
    {
        "id": "q3",
        "question": "3. In cybersecurity, what is a False Positive?",
        "options": [
            "A real phishing email or cyberattack that the model completely misses.",
            "Benign, legitimate activity mistakenly flagged as suspicious or malicious.",
            "A network packet arriving on port 443.",
            "A model achieving 100% accuracy on synthetic classroom data.",
        ],
        "correct_index": 1,
        "explanation": (
            "A False Positive is a false alarm—flagging safe emails or normal user activity as threats. "
            "Too many false positives overwhelm analysts (alert fatigue)."
        ),
    },
    {
        "id": "q4",
        "question": "4. Which Machine Learning algorithm did we use for Phishing Email Detection?",
        "options": [
            "K-Means Clustering",
            "Multinomial Naive Bayes",
            "Linear Regression",
            "Reinforcement Q-Learning",
        ],
        "correct_index": 1,
        "explanation": (
            "We converted text into word-frequency vectors (TF-IDF or CountVectorizer) and trained a "
            "Multinomial Naive Bayes classifier, which works naturally with word counts and text probabilities."
        ),
    },
    {
        "id": "q5",
        "question": "5. Why should analysts never blindly trust an ML security prediction?",
        "options": [
            "Because ML models learn statistical patterns from past data—they do not truly 'understand' intent and can make mistakes on disguised or unusual cases.",
            "Because scikit-learn generates completely random guesses on every run.",
            "Because phishing emails never contain text.",
            "Because accuracy above 80% means false negatives are impossible.",
        ],
        "correct_index": 0,
        "explanation": (
            "ML models rely on statistical patterns in their training data. Attackers can disguise phrasing "
            "(False Negatives) and legitimate urgency can trigger false alarms (False Positives), so human "
            "critical thinking remains essential."
        ),
    },
]
