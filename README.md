# Resume AI Analyzer

A full-stack AI-powered resume analyzer and job matching web application built with Flask, Python, and modern web UI.

## Features

- Upload PDF/DOCX/TXT resumes
- Paste or upload job descriptions
- Semantic similarity scoring with sentence-transformers
- Skill extraction and missing skill detection
- Experience, education, project, and ATS scoring
- Recruiter dashboard with saved candidate reports
- Basic login/signup authentication
- Responsive frontend and AJAX-powered analysis

## Project Structure

- `app.py` — Flask application entry point
- `requirements.txt` — Python dependencies
- `analyzer/` — parsing, scoring, ML, and suggestion logic
- `database/` — SQLite helper and persistence layer
- `templates/` — Flask HTML templates
- `static/` — CSS and JavaScript assets
- `uploads/` — saved upload files
- `data/` — sample dataset and skill alias map

## Setup Instructions

1. Create a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

4. Run the app:

```bash
python app.py
```

5. Open a browser at `http://127.0.0.1:5000`

## Notes

- Uploaded files are stored in the `uploads/` directory.
- Analysis records are saved in `database/app.db`.
- The app uses a small sample dataset for training a simple ranking model.
- For production, set `SECRET_KEY` via environment variable.
