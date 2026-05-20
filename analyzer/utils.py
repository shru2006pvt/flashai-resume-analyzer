import json
import os
import re
from pathlib import Path
from collections import Counter

COMMON_BuzzWORDS = [
    "synergy",
    "passionate",
    "results-driven",
    "team player",
    "detail-oriented",
    "problem solver",
    "go-getter",
    "strategic thinker",
    "self-starter",
]

DEGREE_KEYWORDS = [
    "bachelor",
    "master",
    "mba",
    "phd",
    "associate",
    "diploma",
    "certification",
]

SECTION_HEADERS = [
    "experience",
    "education",
    "skills",
    "projects",
    "certifications",
    "summary",
    "objective",
    "professional experience",
    "technical skills",
]


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[\t\u200b]+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def load_skill_database(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r", encoding="utf-8") as handle:
        mapped_skills = json.load(handle)
    skills = set()
    for alias, normalized in mapped_skills.items():
        skills.add(normalized.lower())
        skills.add(alias.lower())
    return sorted(skills, key=lambda value: len(value), reverse=True)


def extract_sections(text):
    lower = text.lower()
    sections = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    current_title = "summary"
    current_lines = []

    for line in lines:
        header = line.lower().strip(" :")
        if header in SECTION_HEADERS:
            sections[current_title] = "\n".join(current_lines).strip()
            current_title = header
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_title] = "\n".join(current_lines).strip()

    return sections


def find_degree_keywords(text):
    lower = text.lower()
    found = [word for word in DEGREE_KEYWORDS if word in lower]
    return sorted(set(found))


def extract_years_of_experience(text):
    patterns = [r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", r"(\d+)\s*[-–]\s*(\d+)\s*years"]
    years = 0.0
    for pattern in patterns:
        for match in re.findall(pattern, text.lower()):
            if isinstance(match, tuple):
                values = [float(value) for value in match if value]
                years = max(years, max(values, default=0.0))
            else:
                years = max(years, float(match))
    if years == 0.0:
        if "seasoned" in text.lower() or "senior" in text.lower():
            years = 5.0
    return round(years, 1)


def extract_skills(text, skill_database):
    normalized = text.lower()
    detected = set()
    for phrase in skill_database:
        if phrase in normalized:
            detected.add(phrase)
    return sorted(detected)


def detect_buzzwords(text):
    lower = text.lower()
    found = [buzzword for buzzword in COMMON_BuzzWORDS if buzzword in lower]
    return sorted(set(found))


def build_keyword_frequency(text, top_n=8):
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())
    words = [word for word in cleaned.split() if len(word) > 3]
    counter = Counter(words)
    return [word for word, _ in counter.most_common(top_n)]
