
def calculate_match_score(resume_skills, job_description):
    if not resume_skills or not job_description.strip():
        return 0, []

    job_text = job_description.lower()
    matched_skills = []

    for skill in resume_skills:
        if skill.lower() in job_text:
            matched_skills.append(skill)

    if len(resume_skills) == 0:
        return 0, []

    match_score = round(
        len(matched_skills) / len(resume_skills) * 100
    )

    return match_score, matched_skills