import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf
from skills import (
    extract_skills,
    find_missing_skills,
    recommend_job_roles
)
from matcher import calculate_match_score
resume_text = ""
resume_skills = []
job_description = ""


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Resume Analyzer & Job Matcher")

st.write(
    "Analyze your resume, compare it with a job description, "
    "discover missing skills, and get suitable job role recommendations."
)

st.divider()


# ============================================================
# SIDEBAR - RESUME UPLOAD
# ============================================================

st.sidebar.header("📄 Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    st.success("Resume uploaded successfully!")

    with st.expander("View Extracted Resume Text"):
        st.text_area("Resume Text", text, height=300)


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="Paste the required job description..."
)




# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is None:

    st.info("📂 Please upload a PDF resume from the sidebar.")

else:

    # --------------------------------------------------------
    # EXTRACT RESUME TEXT
    # --------------------------------------------------------

    try:
        text = extract_text_from_pdf(uploaded_file)

        if not text or not text.strip():
            st.error("❌ Could not extract text from the PDF.")
            st.stop()

    except Exception as e:
        st.error(f"❌ Error while reading the resume: {e}")
        st.stop()


    st.success("✅ Resume uploaded successfully!")


    # --------------------------------------------------------
    # EXTRACT RESUME SKILLS
    # --------------------------------------------------------

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # YE LINE MISSING HAI AAPKE CODE ME - Isko add karo
    from skills import SKILLS_LIST
    resume_skills = [skill for skill in SKILLS_LIST if skill.lower() in resume_text.lower()]

    if not resume_skills:
        st.warning("⚠️ No skills detected in your resume.")


    # ========================================================
    # RESUME SKILLS
    # ========================================================

    st.subheader("🛠️ Skills Found")

    if resume_skills:

        skill_columns = st.columns(3)

        for index, skill in enumerate(resume_skills):

            with skill_columns[index % 3]:
                st.success(skill)

    else:

        st.warning("⚠️ No skills detected in your resume.")


    st.divider()

if job_description:
    st.subheader("📊 Resume vs Job Description")

match_score, matched_skills = calculate_match_score(
    resume_skills,
    job_description
)

st.metric(
        "Resume Match Score",
        f"{match_score}%"
    )

st.progress(int(match_score))
st.write("### ✅ Matched Skills")

if matched_skills:
        st.write(", ".join(matched_skills))
else:
        st.warning("No matching skills found.")



    # ========================================================
    # JOB ROLE RECOMMENDATIONS
    # ========================================================

st.subheader("💼 Recommended Job Roles")

try:

        recommendations = recommend_job_roles(resume_skills)

        if recommendations:

            for recommendation in recommendations[:3]:

                role = recommendation["role"]
                score = recommendation["score"]

                st.write(f"### {role}")

                st.progress(
                    min(int(score), 100),
                    text=f"{score}% skill match"
                )

        else:

            st.info("No suitable job roles found.")

except Exception as e:

        st.error(
            f"❌ Error generating job recommendations: {e}"
        )


st.divider()


    # ========================================================
    # JOB DESCRIPTION ANALYSIS
    # ========================================================

if job_description.strip():

        # ----------------------------------------------------
        # CALCULATE MATCH SCORE
        # ----------------------------------------------------

        try:

            match_score = calculate_match_score(
                resume_skills,
                job_description
            )

        except Exception as e:

            st.error(
                f"❌ Error calculating match score: {e}"
            )

            match_score = 0


        # ----------------------------------------------------
        # EXTRACT JOB SKILLS
        # ----------------------------------------------------

        job_skills = extract_skills(job_description)


        # ----------------------------------------------------
        # FIND MISSING SKILLS
        # ----------------------------------------------------

        missing_skills = find_missing_skills(
            resume_skills,
            job_skills
        )


        # ====================================================
        # KPI CARDS
        # ====================================================

        st.subheader("📊 Job Match Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Match Score",
                f"{match_score}%"
            )

        with col2:

            st.metric(
                "🛠️ Skills Found",
                len(resume_skills)
            )

        with col3:

            st.metric(
                "❌ Missing Skills",
                len(missing_skills)
            )


        st.divider()


        # ====================================================
        # MATCH SCORE
        # ====================================================

        st.subheader("🎯 Overall Resume Match")

        st.progress
        min(int(match_score[0] if isinstance(match_score, tuple) else match_score), 100),
        

        # ====================================================
        # MATCH SUMMARY
        # ====================================================

        st.subheader("📋 Resume Analysis Summary")

        match_score = float(match_score[0]) if isinstance(match_score, tuple) else float(match_score)

        if match_score >= 80:

            st.success(
                "Your resume has a strong match with this job description."
            )

        elif match_score >= 60:

            st.warning(
                "Your resume has a moderate match. "
                "Consider improving the missing skills."
            )

        else:

            st.error(
                "Your resume has a low match. "
                "Several skills may need improvement."
            )


        st.divider()


        # ====================================================
        # SKILLS COMPARISON
        # ====================================================

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # RESUME SKILLS
        # ----------------------------------------------------

        with col1:

            st.subheader("🛠️ Resume Skills")

            if resume_skills:

                for skill in resume_skills:
                    st.success(skill)

            else:

                st.warning(
                    "No skills detected in your resume."
                )


        # ----------------------------------------------------
        # MISSING SKILLS
        # ----------------------------------------------------

        with col2:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.error(skill)

            else:

                st.success(
                    "🎉 No major missing skills found!"
                )


        st.divider()


        # ====================================================
        # SKILLS TO LEARN
        # ====================================================

        st.subheader("📚 Recommended Skills to Learn")

        if missing_skills:

            for skill in missing_skills:

                st.info(
                    f"📖 Learn: {skill}"
                )

        else:

            st.success(
                "🎉 Your resume contains all detected required skills!"
            )


        st.divider()


        # ====================================================
        # JOB ROLE SKILL MATCH CHART
        # ====================================================

        if recommendations:

            st.subheader("📊 Job Role Skill Match")

            chart_data = pd.DataFrame({
                "Job Role": [
                    recommendation["role"]
                    for recommendation in recommendations[:5]
                ],
                "Match Score": [
                    recommendation["score"]
                    for recommendation in recommendations[:5]
                ]
            })

            st.bar_chart(
                chart_data.set_index("Job Role")
            )


        st.divider()


        # ====================================================
        # JOB MATCHING ANALYSIS
        # ====================================================

        st.subheader("🎯 Job Matching Analysis")

        if match_score >= 75:

            st.success(
                "🎉 Strong match with this job!"
            )

        elif match_score >= 50:

            st.warning(
                "👍 Moderate match with this job."
            )

        else:

            st.error(
                "⚠️ Low match with this job."
            )


else:

        
        # NO JOB DESCRIPTION

        st.info(
            "💼 Paste a job description above to compare "
            "your resume with the job."
        )















