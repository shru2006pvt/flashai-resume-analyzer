import csv
import json
import math


# =====================================================
# LOAD CSV
# =====================================================

def load_csv(filepath):

    rows = []

    with open(filepath, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


# =====================================================
# SAVE CSV
# =====================================================

def save_csv(filepath, fieldnames, rows):

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


# =====================================================
# LOAD JSON
# =====================================================

def load_json(filepath):

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# =====================================================
# LOAD VOCABULARY
# =====================================================

def load_vocabulary(filepath):

    vocabulary = []

    with open(filepath, "r", encoding="utf-8") as file:

        for line in file:
            vocabulary.append(line.strip())

    return vocabulary


# =====================================================
# COSINE SIMILARITY
# =====================================================

def cosine_similarity(vector_a, vector_b):

    dot_product = 0
    magnitude_a = 0
    magnitude_b = 0

    for i in range(len(vector_a)):

        dot_product += vector_a[i] * vector_b[i]

        magnitude_a += vector_a[i] ** 2
        magnitude_b += vector_b[i] ** 2

    magnitude_a = math.sqrt(magnitude_a)
    magnitude_b = math.sqrt(magnitude_b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)