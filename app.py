import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GradeGenius",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #EAE4F8;
    color: #30264B;
}
[data-testid="stSidebar"] {
    background: #FFFDF8;
}
.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}
.gg-card {
    background: #FFFDF8;
    border: 1px solid #E5DAF6;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 15px;
}
.gg-pink {
    background: #FBE6EE;
    border-radius: 18px;
    padding: 22px;
}
.gg-purple {
    background: #E3D7FA;
    border-radius: 18px;
    padding: 22px;
}
h1, h2, h3 {
    color: #30264B !important;
}
.stButton > button {
    background: #8B6CE8;
    color: white;
    border-radius: 12px;
    border: none;
    min-height: 42px;
}
.stButton > button:hover {
    background: #7050CE;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 🎓 GradeGenius")
st.sidebar.caption("Your personal academic companion")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "My Subjects", "Study Planner",
     "What-if Simulator", "Progress & Report"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Your daily reminder")
st.sidebar.info("Small steps every day lead to big results.")

if "results" not in st.session_state:
    st.session_state.results = None

if page == "Overview":
    st.markdown("# Your learning journey ✨")
    st.write("Predict. Plan. Perform.")
    st.write(
        "Understand your academic performance and "
        "build a personalized study routine."
    )

    st.markdown('<div class="gg-pink">', unsafe_allow_html=True)
    st.subheader("📊 Your Academic Snapshot")
    st.write("Enter your current academic details to get started.")
    with st.form("student_form"):
        name = st.text_input("Student name")
        course = st.selectbox(
            "Course",
            ["B.Tech", "B.Sc", "BCA", "Other"]
        )
        attendance = st.slider(
            "Attendance (%)", 0, 100, 80
        )
        study_hours = st.slider(
            "Daily study hours", 0.0, 12.0, 3.0, 0.5
        )
        previous_marks = st.slider(
            "Previous overall marks (%)", 0, 100, 65
        )

        st.markdown("#### Subject-wise marks")
        math = st.slider("Mathematics", 0, 100, 70)
        programming = st.slider("Programming", 0, 100, 75)
        data_science = st.slider("Data Science", 0, 100, 65)

        submitted = st.form_submit_button(
            "✨ Analyze My Performance",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            subject_avg = (
                math + programming + data_science
            ) / 3

            estimate = (
                0.50 * subject_avg
                + 0.25 * previous_marks
                + 0.15 * attendance
                + 0.10 * min(study_hours * 10, 100)
            )
            estimate = round(max(0, min(100, estimate)), 1)

            st.session_state.results = {
                "name": name,
                "course": course,
                "attendance": attendance,
                "study_hours": study_hours,
                "previous_marks": previous_marks,
                "Mathematics": math,
                "Programming": programming,
                "Data Science": data_science,
                "estimate": estimate
            }

    result = st.session_state.results

    if result:
        st.markdown("## Hello, " + result["name"] + "! 👋")
        a, b, c = st.columns(3)
        a.metric("Performance estimate", f'{result["estimate"]}%')
        b.metric("Attendance", f'{result["attendance"]}%')
        c.metric("Daily study", f'{result["study_hours"]} hrs')

        st.caption(
            "Demo estimate based on a simple weighted rule, "
            "not a trained machine-learning prediction."
        )

        category = (
            "Excellent" if result["estimate"] >= 85
            else "Good" if result["estimate"] >= 70
            else "Needs Improvement"
        )
        st.markdown(
            f'<div class="gg-card"><h3>🎯 {category}</h3>'
            f'<p>Estimated score: {result["estimate"]}%</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader("📚 Subject Progress")
        subjects = ["Mathematics", "Programming", "Data Science"]
        scores = [result[s] for s in subjects]
        chart_df = pd.DataFrame({
            "Subject": subjects,
            "Marks": scores
        }).set_index("Subject")
        st.bar_chart(chart_df)

        weakest = min(subjects, key=lambda s: result[s])
        st.markdown("### 💡 Your personalized next step")
        st.info(
            f"Focus more on **{weakest}**. "
            "Try a 30-minute revision session and solve "
            "five practice questions."
        )

elif page == "My Subjects":
    st.title("📚 My Subjects")
    st.write("Track your marks and identify subjects to improve.")
    subjects = {
        "Mathematics": 70,
        "Programming": 75,
        "Data Science": 65
    }
    for subject, score in subjects.items():
        st.markdown(f"**{subject} — {score}%**")
        st.progress(score / 100)

elif page == "Study Planner":
    st.title("🗓️ Personalized Study Planner")
    st.write("A simple starter plan you can adapt to your routine.")
    plan = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"],
        "Study plan": [
            "Mathematics revision",
            "Programming practice",
            "Data Science concepts",
            "Mathematics problem solving",
            "Programming mini-project",
            "Revise weak topics",
            "Weekly review and rest"
        ],
        "Duration": ["45 min", "60 min", "45 min",
                     "45 min", "60 min", "60 min", "30 min"]
    })
    st.dataframe(plan, use_container_width=True, hide_index=True)

elif page == "What-if Simulator":
    st.title("🧪 What-if Simulator")
    st.write("Explore how different study habits change the demo estimate.")
    current = st.slider("Current marks (%)", 0, 100, 65)
    extra = st.slider("Additional daily study time (hours)", 0.0, 5.0, 1.0)
    attendance_change = st.slider("Expected attendance (%)", 0, 100, 85)
    simulated = min(
        100, round(0.65 * current
                   + 0.20 * attendance_change
                   + 0.15 * min(extra * 20, 100), 1)
    )
    st.metric("Illustrative scenario score", f"{simulated}%")
    st.caption("This is a rule-based scenario, not a validated ML forecast.")

elif page == "Progress & Report":
    st.title("📈 Progress & Report")
    result = st.session_state.results
    if result:
        st.write("Student:", result["name"])
        st.write("Course:", result["course"])
        st.write("Demo performance estimate:", result["estimate"])
        report = pd.DataFrame([result]).to_csv(index=False)
        st.download_button(
            "Download progress report (CSV)",
            data=report,
            file_name="gradegenius_report.csv",
            mime="text/csv"
        )
    else:
        st.info("Submit your profile in Overview first to see your report.")

st.markdown("---")
st.caption("GradeGenius • Academic insights for your learning journey")
