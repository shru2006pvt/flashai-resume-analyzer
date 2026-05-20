import math
from sentence_transformers import SentenceTransformer, util
from analyzer.utils import (
    extract_skills,
    extract_sections,
    extract_years_of_experience,
    find_degree_keywords,
    detect_buzzwords,
    build_keyword_frequency,
)
from analyzer.ml_model import predict_fit_level
from analyzer.suggestions import build_suggestions

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

PROJECT_KEYWORDS = [
    "project",
    "built",
    "developed",
    "launched",
    "implemented",
    "designed",
    "optimized",
    "deployed",
]

EDUCATION_KEYWORDS = [
    "bachelor",
    "master",
    "mba",
    "phd",
    "associate",
    "degree",
    "diploma",
    "certificate",
]


def compute_embedding(text):
    if not text:
        return None
    return MODEL.encode(text, convert_to_tensor=True)


def semantic_similarity(resume_text, jd_text):
    if not resume_text or not jd_text:
        return 0.0
    resume_embedding = compute_embedding(resume_text)
    jd_embedding = compute_embedding(jd_text)
    similarity = util.pytorch_cos_sim(resume_embedding, jd_embedding).item()
    return max(0.0, min(1.0, similarity))


def normalize_score(value):
    return round(max(0.0, min(1.0, value)), 3)


def skill_match_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0
    matched = set(resume_skills) & set(jd_skills)
    return normalize_score(len(matched) / len(set(jd_skills)))


def experience_score(resume_text):
    years = extract_years_of_experience(resume_text)
    score = min(years / 10.0, 1.0)
    return normalize_score(score)


def education_score(resume_text):
    lower = resume_text.lower()
    found = [word for word in EDUCATION_KEYWORDS if word in lower]
    score = min(len(found) * 0.2, 1.0)
    if find_degree_keywords(resume_text):
        score = max(score, 0.8)
    return normalize_score(score)


def project_score(resume_text):
    lower = resume_text.lower()
    found = [word for word in PROJECT_KEYWORDS if word in lower]
    score = min(len(found) * 0.18, 1.0)
    return normalize_score(score)


def ats_score(resume_text):
    sections = extract_sections(resume_text)
    required_sections = {"experience", "education", "skills", "projects"}
    match_count = len(required_sections & set(sections.keys()))
    score = normalize_score((match_count / len(required_sections)) * 1.0)
    if not resume_text.strip():
        return 0.0
    return max(score, 0.35)


def build_resume_profile(resume_text, skill_database):
    return {
        "text": resume_text,
        "skills": extract_skills(resume_text, skill_database),
        "sections": extract_sections(resume_text),
        "years_experience": extract_years_of_experience(resume_text),
        "degree_keywords": find_degree_keywords(resume_text),
    }


def build_job_profile(jd_text, skill_database):
    return {
        "text": jd_text,
        "skills": extract_skills(jd_text, skill_database),
        "sections": extract_sections(jd_text),
        "keywords": build_keyword_frequency(jd_text, top_n=12),
    }


def analyze_resume(resume_text, jd_text, resume_profile, jd_profile):
    semantic = semantic_similarity(resume_text, jd_text)
    skill_match = skill_match_score(resume_profile["skills"], jd_profile["skills"])
    experience = experience_score(resume_text)
    education = education_score(resume_text)
    projects = project_score(resume_text)
    ats = ats_score(resume_text)

    overall_score = normalize_score(
        (semantic * 0.34)
        + (skill_match * 0.28)
        + (experience * 0.14)
        + (education * 0.11)
        + (projects * 0.08)
        + (ats * 0.05)
    ) * 100

    fit_level = predict_fit_level(
        {
            "semantic_similarity": semantic,
            "skill_match": skill_match,
            "experience": experience,
            "education": education,
            "project": projects,
            "ats": ats,
        }
    )

    missing_skills = sorted(set(jd_profile["skills"]) - set(resume_profile["skills"]))
    suggestions = build_suggestions(missing_skills, resume_text, jd_profile["keywords"])

    return {
        "overall_score": round(overall_score, 1),
        "fit_level": fit_level,
        "features": {
            "semantic_similarity": round(semantic, 3),
            "skill_match": round(skill_match, 3),
            "experience": round(experience, 3),
            "education": round(education, 3),
            "project": round(projects, 3),
            "ats": round(ats, 3),
            "matched_skills": sorted(set(resume_profile["skills"]) & set(jd_profile["skills"])),
            "missing_skills": missing_skills,
            "job_keywords": jd_profile["keywords"],
        },
        "suggestions": suggestions,
        "details": {
            "resume_skill_count": len(resume_profile["skills"]),
            "job_skill_count": len(jd_profile["skills"]),
            "years_experience": resume_profile["years_experience"],
            "degree_keywords": resume_profile["degree_keywords"],
            "resume_sections": list(resume_profile["sections"].keys()),
        },
    }
