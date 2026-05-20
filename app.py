import os
import re
import json
import uuid
import sqlite3
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash,
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from analyzer import parser, scorer, ml_model, suggestions, utils
from database.db_utils import (
    init_db,
    get_db_connection,
    create_user,
    get_user_by_username,
    save_analysis,
    fetch_analysis,
    fetch_analyses,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-please")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()
SKILL_DB = utils.load_skill_database(os.path.join(BASE_DIR, "data", "skill_aliases.json"))
RANKING_MODEL = ml_model.load_or_train_model(
    os.path.join(BASE_DIR, "data", "sample_training.csv")
)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    token = uuid.uuid4().hex
    output_name = f"{token}.{extension}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], output_name)
    file_storage.save(save_path)
    return save_path


@app.context_processor
def inject_user():
    return {
        "authenticated": "user_id" in session,
        "username": session.get("username", ""),
    }


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    records = fetch_analyses(user_id=session["user_id"])
    return render_template("dashboard.html", records=records)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Enter both username and password.", "warning")
            return redirect(url_for("signup"))
        if get_user_by_username(username) is not None:
            flash("This username is already taken.", "danger")
            return redirect(url_for("signup"))

        password_hash = generate_password_hash(password)
        user_id = create_user(username, password_hash)
        session["user_id"] = user_id
        session["username"] = username
        flash("Welcome! Your account is ready.", "success")
        return redirect(url_for("index"))

    if "user_id" in session:
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = get_user_by_username(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("index"))
        flash("Invalid username or password.", "danger")
        return redirect(url_for("login"))

    if "user_id" in session:
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "resume" not in request.files:
        return jsonify({"success": False, "message": "No resume file was submitted."}), 400

    resume_file = request.files["resume"]
    jd_text = request.form.get("jd_text", "").strip()
    candidate_name = request.form.get("candidate_name", "Anonymous Candidate").strip()
    jd_file = request.files.get("jd_file")

    if not resume_file or resume_file.filename == "":
        return jsonify({"success": False, "message": "Resume file is required."}), 400

    if not allowed_file(resume_file.filename):
        return jsonify({"success": False, "message": "Resume file type must be PDF, DOCX or TXT."}), 400

    if jd_file and jd_file.filename != "" and allowed_file(jd_file.filename):
        jd_path = save_uploaded_file(jd_file)
        jd_text = parser.parse_job_description(file_path=jd_path)
    elif not jd_text:
        return jsonify({"success": False, "message": "Please paste a job description or upload a JD file."}), 400

    resume_path = save_uploaded_file(resume_file)
    resume_text = parser.parse_resume(resume_path)
    jd_text = parser.parse_job_description(text=jd_text)

    extracted_resume = scorer.build_resume_profile(resume_text, SKILL_DB)
    extracted_jd = scorer.build_job_profile(jd_text, SKILL_DB)
    results = scorer.analyze_resume(
        resume_text=resume_text,
        jd_text=jd_text,
        resume_profile=extracted_resume,
        jd_profile=extracted_jd,
    )

    analysis_id = save_analysis(
        user_id=session.get("user_id"),
        candidate_name=candidate_name or "Anonymous Candidate",
        resume_text=resume_text,
        jd_text=jd_text,
        overall_score=results["overall_score"],
        fit_level=results["fit_level"],
        features=results["features"],
        suggestions=results["suggestions"],
        details=results["details"],
    )

    return jsonify({"success": True, "analysis_id": analysis_id, "redirect": url_for("results", analysis_id=analysis_id)})


@app.route("/api/compare", methods=["POST"])
def api_compare():
    jd_text = request.form.get("jd_text", "").strip()
    candidate_names = request.form.getlist("candidate_name")
    if not candidate_names:
        candidate_names_text = request.form.get("candidate_names", "").strip()
        candidate_names = [name.strip() for name in candidate_names_text.split(",") if name.strip()]

    if not jd_text:
        return jsonify({"success": False, "message": "A job description is required for comparison."}), 400

    resume_files = request.files.getlist("resumes")
    if not resume_files:
        return jsonify({"success": False, "message": "Please upload one or more resumes."}), 400

    jd_text = parser.parse_job_description(text=jd_text)
    jd_profile = scorer.build_job_profile(jd_text, SKILL_DB)
    comparison = []

    for index, resume_file in enumerate(resume_files):
        if not resume_file or resume_file.filename == "" or not allowed_file(resume_file.filename):
            continue
        resume_path = save_uploaded_file(resume_file)
        resume_text = parser.parse_resume(resume_path)
        resume_profile = scorer.build_resume_profile(resume_text, SKILL_DB)
        results = scorer.analyze_resume(
            resume_text=resume_text,
            jd_text=jd_text,
            resume_profile=resume_profile,
            jd_profile=jd_profile,
        )
        comparison.append(
            {
                "candidate": candidate_names[index] if index < len(candidate_names) and candidate_names[index].strip() else f"Candidate {index + 1}",
                "overall_score": results["overall_score"],
                "fit_level": results["fit_level"],
                "skill_match": results["features"]["skill_match"],
                "semantic_similarity": results["features"]["semantic_similarity"],
            }
        )

    comparison.sort(key=lambda row: row["overall_score"], reverse=True)
    return jsonify({"success": True, "comparison": comparison})


@app.route("/results/<int:analysis_id>")
def results(analysis_id):
    record = fetch_analysis(analysis_id)
    if not record:
        flash("Analysis result not found.", "danger")
        return redirect(url_for("index"))

    record_data = {
        "id": record["id"],
        "candidate_name": record["candidate_name"],
        "created_at": record["created_at"],
        "overall_score": record["overall_score"],
        "fit_level": record["fit_level"],
        "features": json.loads(record["features_json"]),
        "suggestions": json.loads(record["suggestions_json"]),
        "details": json.loads(record["details_json"]),
    }
    return render_template("results.html", record=record_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
