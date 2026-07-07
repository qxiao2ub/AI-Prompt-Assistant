# Yashvi AI Prompt Assistant

A GitHub-ready Streamlit web app based on the uploaded Colab notebook `070726_Yashvi_AI_Assistant_Tool_App.ipynb`.

The app demonstrates an AI-based assistant tool that learns from approved user writing examples and predicts useful next phrases for emails, notes, reports, and online searches. It is designed as a portfolio project for Yashvi and can be deployed from GitHub to Streamlit Community Cloud.

---

## Live app goal

After uploading this repository to GitHub, deploy it with:

```bash
streamlit run app.py
```

For Streamlit Community Cloud, choose:

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`

No API keys are required.

---

## What this project includes

```text
yashvi_ai_prompt_assistant_streamlit_github/
├── app.py                                      # Main Streamlit app entrypoint
├── requirements.txt                           # Python dependencies for Streamlit Cloud
├── README.md                                  # Detailed project instructions
├── LICENSE                                    # Portfolio copyright notice template
├── .gitignore                                 # Files to exclude from GitHub
├── .streamlit/
│   └── config.toml                            # Streamlit theme/settings
├── data/
│   └── sample_user_history.csv                # Demo writing history
├── src/
│   ├── __init__.py
│   └── assistant_engine.py                    # Core ML + feedback ranking logic
├── notebooks/
│   └── 070726_Yashvi_AI_Assistant_Tool_App.ipynb
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── STREAMLIT_DEPLOYMENT_GUIDE.md
│   ├── GITHUB_UPLOAD_GUIDE.md
│   ├── PRIVACY_AND_SAFETY.md
│   └── IOS_ROADMAP.md
└── tests/
    └── test_engine.py                         # Basic smoke test for the core engine
```

---

## Product concept

The **Yashvi AI Prompt Assistant** is a prototype of an assistant tool that can support users while they type emails, notes, reports, and search queries.

The goal is to save time and reduce interruption by suggesting likely next phrases based on prior writing patterns. The prototype uses lightweight machine learning methods so it can run quickly on a free Streamlit deployment.

### Main user flow

1. User chooses a writing context such as `email`, `search`, `note`, `report`, or `general`.
2. User starts typing a sentence or paragraph.
3. The app generates suggested next phrases.
4. User can accept or reject suggestions.
5. The feedback ranker adjusts which suggestion sources are shown first.
6. User can download a session profile JSON or CSV.

---

## AI / ML techniques demonstrated

### 1. Machine learning: n-gram prediction

The app includes a simple n-gram model that learns word and phrase transitions from the writing history.

Example:

```text
Input: Dear team, thank you
Possible continuation: for the updates
```

This is a transparent baseline model. It is easy to explain in a student portfolio because it learns from previous text without requiring a paid model API.

### 2. Personalization: TF-IDF similarity search

The app uses TF-IDF vectorization and cosine similarity to find previous writing examples that are similar to the current prompt. This gives the assistant a simple personalization signal.

### 3. Reinforcement-learning-style feedback

The app includes a lightweight multi-armed bandit-style ranker. Each suggestion source is treated like an arm:

- `ml_ngram`
- `similarity`
- `template`

When the user accepts a suggestion, that source receives a reward. When the user rejects a suggestion, it receives more exposure without a reward. Over time, accepted sources rank higher.

### 4. Deep learning roadmap

The original notebook includes an optional TensorFlow/Keras section for a tiny sequence model. The Streamlit app does **not** include TensorFlow by default because it would make the web deployment heavier. See `docs/PROJECT_OVERVIEW.md` and the notebook for the deep-learning extension idea.

---

## Local setup

### 1. Install Python

Recommended: Python 3.10, 3.11, or 3.12.

### 2. Create a virtual environment

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

---

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload all files from this project folder to the repository root.
3. Commit the files to the `main` branch.
4. Go to Streamlit Community Cloud.
5. Select **Create app**.
6. Choose your GitHub repo.
7. Set the main file path to:

```text
app.py
```

8. Click **Deploy**.

The app should build from `requirements.txt` and launch as a public Streamlit app.

---

## CSV data format

The app works with the included sample file:

```text
data/sample_user_history.csv
```

You can upload your own writing history CSV from the app sidebar.

Required column:

| Column | Required | Meaning |
|---|---:|---|
| `user_input` | Yes | A sentence, paragraph, email snippet, note, or search query |

Optional column:

| Column | Required | Meaning |
|---|---:|---|
| `context` | No | Writing type such as `email`, `search`, `note`, `report`, or `general` |

Example:

```csv
context,user_input
email,"Dear team, thank you for the updates. I reviewed the draft and added comments."
search,"best way to deploy a Streamlit app from GitHub"
note,"The assistant should learn from approved writing examples."
```

---

## How to customize the app

### Change default examples

Edit:

```text
data/sample_user_history.csv
```

or edit the built-in examples in:

```text
src/assistant_engine.py
```

### Change templates

Open:

```text
src/assistant_engine.py
```

Then update the `TEMPLATES` dictionary.

### Change the app title or UI copy

Open:

```text
app.py
```

Then update:

```python
APP_NAME = "Yashvi AI Prompt Assistant"
```

### Add a larger model later

Possible upgrades:

- Keras GRU/LSTM next-token model
- Transformer-based local model
- User-specific model fine-tuning
- Browser extension
- iOS keyboard extension
- Secure account-based storage
- Encrypted on-device profile

---

## Privacy-first design

This prototype is intentionally privacy-conscious:

- No external API calls
- No paid model keys
- No database storage
- No background tracking
- No automatic collection from email, keyboard, browser, or search history
- User can upload a CSV manually
- User can download their session profile

For a real production assistant, add:

- Clear opt-in consent
- Data deletion controls
- Local encryption
- Sensitive-data filters
- Security review
- Model evaluation
- Bias and safety testing
- App Store / platform privacy disclosures

---

## Important limitations

This is a working portfolio prototype, not a production keyboard assistant.

It does **not**:

- Read the user's real email inbox
- Read browser searches automatically
- Act as a native iOS keyboard
- Train a large neural network in the Streamlit app
- Store user data permanently
- Register copyright automatically

A production iOS assistant would require native Swift/SwiftUI development, keyboard-extension architecture, Apple privacy disclosures, security review, and App Store submission.

---

## Suggested GitHub repository description

```text
A Streamlit AI writing assistant prototype that learns from approved writing examples and suggests next phrases using n-gram ML, TF-IDF personalization, and reinforcement-learning-style feedback ranking.
```

Suggested topics:

```text
streamlit, machine-learning, ai-assistant, nlp, portfolio-project, python, scikit-learn, personalization
```

---

## Portfolio summary for Yashvi

This project demonstrates how an AI assistant can support writing productivity by learning from user-approved examples and generating next-phrase suggestions. The app combines transparent machine learning, similarity-based personalization, and feedback optimization in a Streamlit interface that can be deployed publicly from GitHub.

---

## Troubleshooting

### Streamlit Cloud says it cannot find dependencies

Make sure `requirements.txt` is in the repository root and includes:

```text
streamlit
pandas
numpy
scikit-learn
```

### The app cannot find `src.assistant_engine`

Make sure the `src/` folder is uploaded to the same repository root as `app.py`.

### The app has no suggestions

Use a longer prompt or upload a CSV with more writing examples.

### Uploaded CSV fails

Check that the CSV has a column named exactly:

```text
user_input
```

The optional context column should be named:

```text
context
```

---

## Copyright note

This repository includes a portfolio copyright notice template in `LICENSE`. Replace `Yashvi` with the full legal name if desired.

This project file does not register copyright by itself. For formal registration, follow the official process in your jurisdiction.
