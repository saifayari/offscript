# Cybersecurity Machine Learning Lab

An interactive educational web application designed for a **2-hour Intro to AI workshop**. Students and beginners explore how **supervised Machine Learning** helps identify cyber threats through two hands-on projects:

1. **Project 01 — Phishing Email Detector** (`TF-IDF` / `CountVectorizer` + `MultinomialNB`)
2. **Project 02 — Network Intrusion Detector** (`RandomForestClassifier` on tabular telemetry)

> **Classroom Disclaimer:** This application uses **100% synthetic educational datasets** generated locally with reproducible seeds (`seed=42`). It does not collect real emails, credentials, or live network traffic, does not open external links or perform real network scans, and is **not** a production cybersecurity product.

---

## Project Structure

```text
├── app.py                      # Main Streamlit entry point and navigation
├── requirements.txt            # Python dependencies
├── README.md                   # Setup and launch instructions
├── data/
│   ├── __init__.py
│   └── datasets.py             # Synthetic phishing (120) & network (600) generators
├── models/
│   ├── __init__.py
│   ├── phishing_model.py       # Leak-free TF-IDF/Count + MultinomialNB pipeline
│   └── intrusion_model.py      # Leak-free RandomForestClassifier pipeline
├── education/
│   ├── __init__.py
│   └── content.py              # Pipeline steps, glossary terms, comparison & quiz
├── ui/
│   ├── __init__.py
│   ├── theme.py                # Dark cybersecurity theme CSS
│   └── components.py           # Plotly charts, SVGs, token highlighter & widgets
├── views/
│   ├── __init__.py
│   ├── home.py                 # Landing page & project cards
│   ├── phishing_lab.py         # Project 01 interactive lab & evaluation
│   ├── intrusion_lab.py        # Project 02 simulator, scenarios & evaluation
│   └── comparison_and_quiz.py  # Side-by-side comparison & 5-question quiz
└── tests/
    └── test_cyber_ml_lab.py    # Automated ML & Streamlit UI tests
```

---

## Installation & Setup (Beginner Friendly)

### 1. Prerequisites
- Python **3.10 or newer** installed (`python --version`)

### 2. Optional: Create a Virtual Environment
```bash
python -m venv .venv
```
Activate it:
- **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
- **macOS / Linux:** `source .venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
```bash
streamlit run app.py
```
Your browser will open automatically at `http://localhost:8501`.

---

## Running Automated Tests
Verify the datasets, leak-free train/test evaluation, edge-case input handling, and Streamlit UI flows:
```bash
pytest -v tests/test_cyber_ml_lab.py
```
