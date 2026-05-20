from data_preprocessing import (
    preprocess_resumes
)

from tfidfvector_construction import (
    compute_tfidf_vectors
)

from similarity_calculation import (
    compute_binary_vectors
)

from rankingandoutput import (
    rank_candidates
)


# =====================================================
# MAIN PIPELINE
# =====================================================

def main():

    print("=" * 50)
    print("FLASHAI RESUME ANALYZER")
    print("=" * 50)

    # Step 1
    preprocess_resumes()

    # Step 2
    compute_tfidf_vectors()

    # Step 3
    compute_binary_vectors()

    # Step 4
    rank_candidates()


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":
    main()