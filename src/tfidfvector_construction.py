import math
from collections import defaultdict

from utils import (
    load_csv,
    load_vocabulary,
    save_csv
)


# =====================================================
# DOCUMENT FREQUENCY
# =====================================================

def compute_document_frequency(resume_skill_lists):

    df = defaultdict(int)

    for skills in resume_skill_lists:

        unique_skills = set(skills)

        for skill in unique_skills:
            df[skill] += 1

    return df


# =====================================================
# COMPUTE TF-IDF VECTORS
# =====================================================

def compute_tfidf_vectors():

    resumes = load_csv(
        "../data/intermediate_results/deduplicated_resumes.csv"
    )

    vocabulary = load_vocabulary(
        "../data/vocabulary.txt"
    )

    resume_skill_lists = []

    for resume in resumes:

        skills = resume["skills"].split(",")

        resume_skill_lists.append(skills)

    df = compute_document_frequency(
        resume_skill_lists
    )

    rows = []

    for index, skills in enumerate(resume_skill_lists):

        vector = []

        total_unique_skills = len(skills)

        for vocab_skill in vocabulary:

            if vocab_skill in skills:

                tf = 1 / total_unique_skills

                idf = math.log(
                    10 / df[vocab_skill]
                )

                tfidf = round(tf * idf, 4)

            else:
                tfidf = 0

            vector.append(tfidf)

        rows.append({
            "resume_id": resumes[index]["id"],
            "vector": vector
        })

    save_csv(
        "../data/intermediate_results/resumetfidfvectors.csv",
        ["resume_id", "vector"],
        rows
    )

    print("TF-IDF vectors created.")