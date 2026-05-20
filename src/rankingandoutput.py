import ast

from utils import (
    load_csv,
    cosine_similarity
)


# =====================================================
# RANK CANDIDATES
# =====================================================

def rank_candidates():

    resumes = load_csv(
        "../data/intermediate_results/deduplicated_resumes.csv"
    )

    jobs = load_csv(
        "../data/job_descriptions.csv"
    )

    tfidf_vectors = load_csv(
        "../data/intermediate_results/resumetfidfvectors.csv"
    )

    binary_vectors = load_csv(
        "../data/intermediate_results/binary_vectors.csv"
    )

    for job_index, job in enumerate(jobs):

        jd_vector = ast.literal_eval(
            binary_vectors[job_index]["vector"]
        )

        rankings = []

        for resume_index, resume in enumerate(resumes):

            resume_vector = ast.literal_eval(
                tfidf_vectors[resume_index]["vector"]
            )

            similarity = cosine_similarity(
                resume_vector,
                jd_vector
            )

            rankings.append({
                "name": resume["name"],
                "score": round(similarity * 100, 2)
            })

        # Sorting Rules
        rankings.sort(
            key=lambda x: (
                -x["score"],
                x["name"]
            )
        )

        top_3 = rankings[:3]

        print()
        print(
            f"{job['id']} — "
            f"{job['company']} "
            f"({job['role']})"
        )

        for index, candidate in enumerate(top_3):

            print(
                f"{index + 1}. "
                f"{candidate['name']} "
                f"({candidate['score']})"
            )