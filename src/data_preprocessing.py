from utils import (
    load_csv,
    load_json,
    save_csv
)


# =====================================================
# NORMALIZE SKILLS
# =====================================================

def normalize_skills(raw_skill_text, alias_mapping):

    raw_skill_text = raw_skill_text.lower()

    split_skills = raw_skill_text.split(",")

    normalized = []

    for skill in split_skills:

        skill = skill.strip()

        # Match aliases
        if skill in alias_mapping:
            normalized.append(
                alias_mapping[skill]
            )

    # Deduplicate
    unique_skills = []

    for skill in normalized:

        if skill not in unique_skills:
            unique_skills.append(skill)

    return unique_skills


# =====================================================
# PREPROCESS RESUMES
# =====================================================

def preprocess_resumes():

    resumes = load_csv(
        "../data/resumes.csv"
    )

    alias_mapping = load_json(
        "../data/skill_aliases.json"
    )

    normalized_rows = []

    deduplicated_rows = []

    for resume in resumes:

        normalized_skills = normalize_skills(
            resume["skills"],
            alias_mapping
        )

        normalized_rows.append({
            "id": resume["id"],
            "name": resume["name"],
            "skills": ",".join(normalized_skills)
        })

        deduplicated_rows.append({
            "id": resume["id"],
            "name": resume["name"],
            "skills": ",".join(normalized_skills)
        })

    save_csv(
        "../data/intermediate_results/normalized_resumes.csv",
        ["id", "name", "skills"],
        normalized_rows
    )

    save_csv(
        "../data/intermediate_results/deduplicated_resumes.csv",
        ["id", "name", "skills"],
        deduplicated_rows
    )

    print("Resume preprocessing completed.")