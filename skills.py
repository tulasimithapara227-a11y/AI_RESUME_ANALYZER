import re

SKILLS_LIST = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "nlp",
    "opencv",
    "git",
    "github",
    "streamlit",
    "flask",
    "django",
    "aws",
    "docker"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_LIST:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

def find_missing_skills(resume_skills, job_description):

    if isinstance(job_description, list):
        job_description = " ".join(job_description)

    job_text = job_description.lower()

    required_skills = []

    for skill in SKILLS_LIST:
        if skill.lower() in job_text:
            required_skills.append(skill)

    missing_skills = []

    for skill in required_skills:
        if skill.lower() not in [s.lower() for s in resume_skills]:
            missing_skills.append(skill)

    return missing_skills

JOB_ROLES = {
    "Data Analyst": [
        "python",
        "pandas",
        "numpy",
        "sql",
        "data analysis",
        "matplotlib"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "scikit-learn",
        "statistics"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "numpy"
    ],

    "Python Developer": [
        "python",
        "django",
        "flask",
        "sql",
        "git"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "python",
        "django"
    ]
}


def recommend_job_roles(resume_skills):

    recommendations = []

    for role, required_skills in JOB_ROLES.items():

        matched_skills = []

        for skill in required_skills:
            if skill in resume_skills:
                matched_skills.append(skill)

        score = (len(matched_skills) / len(required_skills)) * 100

        recommendations.append(
            {
                "role": role,
                "score": round(score, 2)
            }
        )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations