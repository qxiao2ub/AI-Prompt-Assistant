# Yashvi AI Prompt Assistant

A GitHub-ready Streamlit prototype based on the attached Colab notebook `070726_Yashvi_AI_Assistant_Tool_App.ipynb`.

This app demonstrates an AI-based prompt assistant that learns from previous user writing examples and suggests likely next phrases for email, notes, reports, and online search prompts.

## Important fix in this version

The previous Streamlit deployment failed with this error:

```text
ModuleNotFoundError: No module named 'src'
```

That happened because `app.py` imported:

```python
from src.assistant_engine import BanditRanker, SuggestionEngine, clean_history_df
```

If the `src/` folder is not uploaded to GitHub, or Streamlit does not see the folder in the deployed repository, the app crashes before it opens.

This fixed version removes that dependency from the running app. The root `app.py` is now self-contained, so Streamlit can run it directly from GitHub without needing to import `src`.

## Repository structure

```text
.
|-- app.py                              # Main Streamlit app; use this as the Streamlit entry point
|-- requirements.txt                    # Python packages needed by Streamlit
|-- runtime.txt                         # Python runtime hint for hosted deployment
|-- README.md                           # Main documentation
|-- data/
|   `-- sample_user_history.csv          # Demo writing history data
|-- notebooks/
|   `-- 070726_Yashvi_AI_Assistant_Tool_App.ipynb
|-- docs/
|   |-- GITHUB_UPLOAD_GUIDE.md
|   |-- STREAMLIT_DEPLOYMENT_GUIDE.md
|   |-- PROJECT_OVERVIEW.md
|   `-- PRIVACY_AND_SAFETY.md
|-- .streamlit/
|   `-- config.toml
|-- src/
|   |-- __init__.py
|   `-- assistant_engine.py              # Optional placeholder for future modular refactor
|-- tests/
|   `-- test_static_checks.py
|-- .gitignore
`-- LICENSE
```

## What the app does

The prototype includes four AI/ML-style components:

1. **N-gram next-phrase prediction**
   - Learns which words often follow recent words in the user's previous writing.
   - Produces a lightweight next phrase or sentence continuation.

2. **Local TF-IDF personalization**
   - Finds prior writing examples that are similar to the current prompt.
   - Suggests a continuation based on the user's own writing style.
   - Implemented directly in `app.py` to avoid heavy package dependencies.

3. **Context-aware suggestions**
   - Uses different fallback suggestions for email, search, note, report, and general writing.

4. **Reinforcement-learning-style feedback ranking**
   - Lets the user accept or reject suggestions.
   - Accepted suggestion sources rank higher in the current session.
   - This is a small bandit-style feedback loop suitable for a portfolio prototype.

## Quick local run

From the project folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## How to upload to GitHub

1. Download and unzip this project.
2. Create a new GitHub repository, for example:
   - `ai-prompt-assistant`
   - `yashvi-ai-prompt-assistant`
3. Upload the extracted files and folders to the repository.
4. Confirm that the repository root contains these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `data/sample_user_history.csv`
5. Commit the files.

Do not upload only the ZIP file to GitHub. GitHub and Streamlit need the extracted project files.

## How to deploy on Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Create a new app.
3. Select your GitHub repository.
4. Set the main file path to:

```text
app.py
```

5. Deploy the app.

The main file path should be exactly `app.py` if the file is in the root of the repository.

## CSV upload format

The app can run with its built-in sample data. You can also upload a CSV with your own writing examples.

Required column:

```text
user_input
```

Optional column:

```text
context
```

Allowed or suggested context values:

```text
email, search, note, report, general
```

Example:

```csv
context,user_input
email,"Dear team, thank you for the update. I will review the document and send comments by Friday."
search,"best way to deploy a Streamlit app from a GitHub repository"
note,"The assistant should learn from user-approved examples and keep the user in control."
```

## How to use the app

1. Choose a writing context in the dropdown.
2. Type a phrase, sentence, or paragraph.
3. Click **Generate suggestions**.
4. Review the suggested continuations.
5. Click **Accept** or **Reject** to update the session feedback ranker.
6. Optionally download the session profile JSON or session CSV.

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'src'`

This fixed version should not produce that error because `app.py` no longer imports from `src`.

If you still see the error, GitHub or Streamlit is probably running the old `app.py`. Fix it by doing the following:

1. Replace the old GitHub files with the files from this ZIP.
2. Confirm that the deployed `app.py` does not contain this line:

```python
from src.assistant_engine import ...
```

3. In Streamlit Cloud, reboot or redeploy the app.

### Error: Streamlit cannot find `app.py`

Make sure the Streamlit app entry point is:

```text
app.py
```

Also make sure `app.py` is at the root of the GitHub repository, not hidden inside another folder.

### Error reading CSV

Make sure your CSV contains a column named exactly:

```text
user_input
```

The optional context column should be named exactly:

```text
context
```

## Privacy and safety notes

This prototype is designed as a privacy-first demo:

- No external AI API is called.
- No API key is needed.
- No database is used.
- Session text stays in the active Streamlit session unless the user downloads it.
- The sample data is fictional demo data.

For a production typing assistant, browser extension, or iOS keyboard, additional privacy, consent, security, and data-retention controls would be required.

## Portfolio explanation

This project is useful for a student portfolio because it shows:

- Product thinking
- Data preprocessing
- Lightweight machine learning
- Personalization
- Feedback-based ranking
- Streamlit web app development
- GitHub project organization
- Documentation and deployment readiness

## Future improvements

Possible next steps:

- Add user login and encrypted storage.
- Add a browser extension prototype.
- Add an iOS keyboard extension proof of concept.
- Add transformer-based next-text generation with a small open-source model.
- Add an evaluation dashboard for accepted/rejected suggestions.
- Add stronger privacy controls and user data deletion tools.

## License and copyright note

This repository includes an MIT-style license file for portfolio demonstration. The copyright notice can be changed to Yashvi's full legal name if desired.

Copyright (c) 2026 Yashvi
