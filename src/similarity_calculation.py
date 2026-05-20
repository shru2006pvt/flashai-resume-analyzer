from utils import (
    load_csv,
    load_vocabulary,
    save_csv
)


# =====================================================
# BUILD BINARY JD VECTOR
# =====================================================

def build_jd_vector(jd_skills, vocabulary):

    vector = []

    for vocab_skill in vocabulary:

        if vocab_skill in jd_skills:
            vector.append(1)
        else:
            vector.append(0)

    return vector


# =====================================================
# COMPUTE BINARY VECTORS
# =====================================================

def compute_binary_vectors():

    jobs = load_csv(
        "../data/job_descriptions.csv"
    )

    vocabulary = load_vocabulary(
        "../data/vocabulary.txt"
    )

    rows = []

    for job in jobs:

        required_skills = (
            job["required_skills"].split(",")
        )

        preferred_skills = (
            job["preferred_skills"].split(",")
        )

        all_skills = (
            required_skills +
            preferred_skills
        )

        vector = build_jd_vector(
            all_skills,
            vocabulary
        )

        rows.append({
            "job_id": job["id"],
            "vector": vector
        })

    save_csv(
        "../data/intermediate_results/binary_vectors.csv",
        ["job_id", "vector"],
        rows
    )

    print("Binary vectors created.")