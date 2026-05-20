COMMON_CERTIFICATIONS = {
    "python": ["Microsoft Python Developer", "Certified Python Programmer"],
    "machine_learning": ["AWS ML Specialty", "TensorFlow Developer Certificate"],
    "data_analysis": ["Google Data Analytics", "IBM Data Analyst"],
    "nlp": ["Coursera NLP Specialization", "DeepLearning.AI NLP"],
    "sql": ["Microsoft SQL Server", "Oracle SQL"],
}

COMMON_ACTION_VERBS = [
    "orchestrated",
    "accelerated",
    "transformed",
    "delivered",
    "designed",
    "optimized",
    "streamlined",
]


def recommend_certifications(skills):
    certifications = []
    for skill in skills:
        for key, recommendations in COMMON_CERTIFICATIONS.items():
            if key in skill:
                certifications.extend(recommendations)
    return sorted(set(certifications))


def action_verb_suggestions():
    return COMMON_ACTION_VERBS[:6]


def build_suggestions(missing_skills, resume_text, jd_keywords):
    return {
        "missing_skills": missing_skills,
        "recommended_certifications": recommend_certifications(missing_skills),
        "strong_action_verbs": action_verb_suggestions(),
        "more_relevant_keywords": [k for k in jd_keywords if k not in resume_text.lower()][:8],
    }
