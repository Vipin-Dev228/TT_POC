import requests
from pathlib import Path
from rapidfuzz import fuzz

from mogo_util import fetch_candidates


def extract_jd_data(
    file_path: str,
    url: str = "https://tt-parsing.pharynxai.in/extract_jd_data",
    timeout: int = 60,
) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("rb") as f:
        files = {"jd_files": (path.name, f, "application/pdf")}
        response = requests.post(url, files=files, timeout=timeout)

    response.raise_for_status()

    try:
        return response.json()

    except requests.exceptions.JSONDecodeError as e:
        raise ValueError(
            f"Non-JSON response (status {response.status_code}): {response.text[:200]}"
        ) from e


def fuzzy_match(jd_skills, candidate_skills, threshold=80):

    matched_skills = []
    total_score = 0

    for jd_skill in jd_skills:
        best_match = None
        best_score = 0

        for cand_skill in candidate_skills:
            score = fuzz.ratio(jd_skill.lower(), cand_skill.lower())

            if score > best_score:
                best_score = score
                best_match = cand_skill

        if best_score >= threshold:
            matched_skills.append(
                {
                    "jd_skill": jd_skill,
                    "candidate_skill": best_match,
                    "score": best_score,
                }
            )
            total_score += best_score

    overall_score = round(total_score / len(jd_skills), 2) if jd_skills else 0

    return overall_score, matched_skills


def top_n_candidates(jd_path: str, n=5):
    jd_data = extract_jd_data(jd_path)
    bucket = jd_data.get("data")[0].get("bucket")
    job_title = jd_data.get("data")[0].get("Job Title")
    primary_skills = jd_data.get("data")[0].get("Primary Skills")

    # Step 1: Fetch candidates from Mongo
    candidates = fetch_candidates(bucket, job_title)

    # Step 2: Calculate fuzzy match score for each candidate
    for candidate in candidates:
        score, matched = fuzzy_match(primary_skills, candidate.get("primarySkills"))
        candidate["score"] = score
        candidate["matched_skills"] = matched

    # Step 3: Sort candidates by score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    return candidates[:n]


if __name__ == "__main__":
    print(
        top_n_candidates(
            "/home/vipin/OFFICE/POC/AI_Candidate_finder/uploads/19d291480ef5cdf4/soft_eng_jd_20260303162035166978.pdf"
        )
    )

    # jd = ["Python", "Machine Learning", "Docker", "FastAPI", "Django", "Flask", "aws"]
    # candidate = [
    #     "pyhton",
    #     "docker",
    #     "fastapi",
    #     "n8n",
    #     "mongodb",
    #     "aws",
    #     "azure",
    #     "gcp",
    #     "kubernetes",
    # ]

    # score, matched = fuzzy_match(jd, candidate)

    # print(score)
    # print(matched)
