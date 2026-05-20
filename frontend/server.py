import csv
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_skill(skill, alias_mapping):
    normalized = skill.strip().lower()
    return alias_mapping.get(normalized, normalized)


def load_resumes():
    resumes = load_csv(DATA_DIR / "resumes.csv")
    alias_mapping = load_json(DATA_DIR / "skill_aliases.json")

    normalized = []
    for resume in resumes:
        skills = [normalize_skill(s, alias_mapping)
                  for s in resume["skills"].split(",") if s.strip()]
        filtered = []
        for skill in skills:
            if skill not in filtered:
                filtered.append(skill)
        normalized.append({
            "id": resume["id"],
            "name": resume["name"],
            "skills": filtered,
        })

    return normalized


def load_jobs():
    jobs = load_csv(DATA_DIR / "job_descriptions.csv")

    job_list = []
    for job in jobs:
        required = [s.strip() for s in job["required_skills"].split(",") if s.strip()]
        preferred = [s.strip() for s in job["preferred_skills"].split(",") if s.strip()]

        job_list.append({
            "id": job["id"],
            "company": job["company"],
            "role": job["role"],
            "required_skills": required,
            "preferred_skills": preferred,
        })

    return job_list


def build_results():
    resumes = load_resumes()
    jobs = load_jobs()
    results = []

    for job in jobs:
        required = set(job["required_skills"])
        preferred = set(job["preferred_skills"])
        all_skills = required | preferred

        rankings = []
        for resume in resumes:
            matched_required = len(required & set(resume["skills"]))
            matched_preferred = len(preferred & set(resume["skills"]))
            required_score = matched_required / len(required) if required else 0
            preferred_score = matched_preferred / len(preferred) if preferred else 0
            score = round((required_score * 0.7 + preferred_score * 0.3) * 100, 2)
            matched_skills = [skill for skill in resume["skills"] if skill in all_skills]

            rankings.append({
                "name": resume["name"],
                "score": score,
                "matched_skills": matched_skills,
            })

        rankings.sort(key=lambda item: (-item["score"], item["name"]))
        results.append({
            "jd_id": job["id"],
            "company": job["company"],
            "role": job["role"],
            "top_candidates": rankings[:3],
        })

    return {
        "job_descriptions": jobs,
        "results": results,
    }


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/match":
            payload = build_results()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            super().do_GET()


def run_server():
    os.chdir(BASE_DIR)
    server_address = ("", 8000)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print("Serving frontend and API at http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
