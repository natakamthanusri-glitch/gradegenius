import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import StringIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GradeGenius",
    page_icon="🎓",
    layout="wide"
)

# ---------------- DESIGN ----------------
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

# ---------------- SUBJECTS ----------------
SUBJECTS = {
    "2nd Year": {
        "Semester 1": [
            "Mathematics", "Data Structures",
            "Digital Logic Design", "Python Programming",
            "Computer Organization"
        ],
        "Semester 2": [
            "Java Programming", "DBMS",
            "Operating Systems", "Computer Networks",
            "Design and Analysis of Algorithms"
        ]
    },
    "3rd Year": {
        "Semester 1": [
            "Artificial Intelligence", "Machine Learning",
            "Software Engineering", "Web Technologies",
            "Theory of Computation"
        ],
        "Semester 2": [
            "Cloud Computing", "Cyber Security",
            "Data Mining", "Compiler Design",
            "Distributed Systems"
        ]
    },
    "4th Year": {
        "Semester 1": [
            "Deep Learning", "Big Data Analytics",
            "Project Work", "Internet of Things",
            "Professional Elective"
        ],
        "Semester 2": [
            "Major Project", "Internship",
            "Professional Ethics", "Technical Seminar",
            "Open Elective"
        ]
    }
}

# ---------------- SESSION STATE ----------------
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "marks" not in st.session_state:
    st.session_state.marks = {}

if "progress" not in st.session_state:
    st.session_state.progress = {}

if "planner" not in st.session_state:
    st.session_state.planner = None

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("# 🎓 GradeGenius")
st.sidebar.caption("Your personal academic companion")
st.sidebar.markdown("---")

year = st.sidebar.selectbox(
    "Select your year",
    ["2nd Year", "3rd Year", "4th Year"]
)

semester = st.sidebar.selectbox(
    "Select semester",
    ["Semester 1", "Semester 2"]
)

student_name = st.sidebar.text_input(
    "Student name",
    value=st.session_state.student_name,
    placeholder="Enter your name"
)
st.session_state.student_name = student_name

attendance = st.sidebar.slider(
    "Attendance (%)", 0, 100, 80
)

daily_hours = st.sidebar.slider(
    "Available daily study hours",
    1, 12, 3
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "My Subjects",
        "Study Planner",
        "What-if Simulator",
        "Progress & Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Daily reminder")
st.sidebar.info("Small steps every day lead to big results.")

subjects = SUBJECTS[year][semester]

# Create marks and progress entries for selected subjects
for subject in subjects:
    mark_key = f"{year}_{semester}_{subject}_mark"
    progress_key = f"{year}_{semester}_{subject}_progress"

    if mark_key not in st.session_state.marks:
        st.session_state.marks[mark_key] = 0

    if progress_key not in st.session_state.progress:
        st.session_state.progress[progress_key] = {
            "total": 10,
            "completed": 0
        }

# Get marks for selected semester
scores = [
    st.session_state.marks[f"{year}_{semester}_{s}_mark"]
    for s in subjects
]

average = round(sum(scores) / len(scores), 1) if scores else 0

performance_estimate = round(
    0.70 * average
    + 0.20 * attendance
    + 0.10 * min(daily_hours * 10, 100),
    1
)

# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.title("🎓 GradeGenius")
    st.header("Your learning journey ✨")
    st.write("Predict. Plan. Perform.")

    st.markdown(
        f"""
        <div class="gg-pink">
        <h3>Welcome, {student_name.strip() or "Student"}! 👋</h3>
        <p>Selected academic year: <b>{year}</b></p>
        <p>Selected semester: <b>{semester}</b></p>
        <p>Manage your subjects, create a study plan,
        and track your academic progress.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Your Academic Snapshot")

    col1, col2, col3 = st.columns(3)
    col1.metric("Subject Average", f"{average}%")
    col2.metric("Attendance", f"{attendance}%")
    col3.metric("Daily Study", f"{daily_hours} hours")

    st.metric(
        "Illustrative Performance Estimate",
        f"{performance_estimate}%"
    )

    st.caption(
        "This is a simple rule-based estimate, not a validated "
        "machine-learning prediction or guaranteed exam result."
    )

    category = (
        "Excellent" if performance_estimate >= 85
        else "Good" if performance_estimate >= 70
        else "Keep Practising"
    )

    st.markdown(
        f"""
        <div class="gg-card">
        <h3>🎯 Current status: {category}</h3>
        <p>Enter your marks in My Subjects to update this overview.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📚 Subject-wise Marks")

    chart_df = pd.DataFrame({
        "Subject": subjects,
        "Marks (%)": scores
    }).set_index("Subject")

    st.bar_chart(chart_df)

    if scores:
        weakest_index = scores.index(min(scores))
        weakest_subject = subjects[weakest_index]

        st.info(
            f"💡 Suggested focus: **{weakest_subject}**. "
            "Try revising one topic and solving practice questions."
        )

# ---------------- MY SUBJECTS ----------------
elif page == "My Subjects":
    st.title("📚 My Subjects")
    st.write(f"Subjects for **{year} — {semester}**")

    st.info(
        "These are sample subject lists. You can change the marks "
        "and adapt the subjects to match your college syllabus."
    )

    for subject in subjects:
        key = f"{year}_{semester}_{subject}_mark"

        with st.container(border=True):
            st.subheader(subject)
            st.slider(
                f"{subject} marks (%)",
                min_value=0,
                max_value=100,
                value=st.session_state.marks[key],
                key=f"slider_{key}"
            )
            st.session_state.marks[key] = st.session_state[
                f"slider_{key}"
            ]
            st.progress(st.session_state.marks[key] / 100)

    updated_scores = [
        st.session_state.marks[f"{year}_{semester}_{s}_mark"]
        for s in subjects
    ]

    updated_average = round(
        sum(updated_scores) / len(updated_scores), 1
    )

    st.markdown("---")
    st.metric("Current Subject Average", f"{updated_average}%")

    marks_df = pd.DataFrame({
        "Year": [year] * len(subjects),
        "Semester": [semester] * len(subjects),
        "Subject": subjects,
        "Marks (%)": updated_scores
    })

    st.download_button(
        "⬇️ Download Subject Marks",
        data=marks_df.to_csv(index=False),
        file_name="gradegenius_subject_marks.csv",
        mime="text/csv"
    )

# ---------------- STUDY PLANNER ----------------
elif page == "Study Planner":
    st.title("🗓️ Personalized Study Planner")
    st.write("Create a study timetable for your upcoming exam.")

    st.markdown(
        f'<div class="gg-purple"><b>{year} — {semester}</b>'
        f'<br>Available subjects: {len(subjects)}</div>',
        unsafe_allow_html=True
    )

    exam_date = st.date_input(
        "Your exam date",
        value=date.today() + timedelta(days=7),
        min_value=date.today()
    )

    hours = st.slider(
        "Hours available per day",
        min_value=1,
        max_value=12,
        value=daily_hours
    )

    chosen_subjects = st.multiselect(
        "Choose subjects to study",
        options=subjects,
        default=subjects
    )

    if st.button("✨ Generate My Study Plan", use_container_width=True):
        days_left = (exam_date - date.today()).days

        if not chosen_subjects:
            st.error("Please select at least one subject.")
        elif days_left < 1:
            st.error("Choose an exam date after today.")
        else:
            schedule = []

            for day_number in range(days_left):
                study_date = date.today() + timedelta(
                    days=day_number
                )

                subject = chosen_subjects[
                    day_number % len(chosen_subjects)
                ]

                schedule.append({
                    "Date": study_date.strftime("%d-%m-%Y"),
                    "Day": study_date.strftime("%A"),
                    "Subject": subject,
                    "Study Hours": hours,
                    "Suggested Task": (
                        "Revise concepts and make notes"
                        if day_number % 2 == 0
                        else "Solve practice questions and review mistakes"
                    )
                })

            st.session_state.planner = schedule

    if st.session_state.planner:
        plan_df = pd.DataFrame(st.session_state.planner)

        st.subheader("📅 Your Generated Timetable")
        st.dataframe(
            plan_df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Your plan has {len(plan_df)} study days. "
            "Remember to take breaks and adjust it to your routine."
        )

        st.download_button(
            "⬇️ Download Study Plan",
            data=plan_df.to_csv(index=False),
            file_name="gradegenius_study_plan.csv",
            mime="text/csv"
        )

# ---------------- WHAT-IF SIMULATOR ----------------
elif page == "What-if Simulator":
    st.title("🧪 What-if Simulator")
    st.write(
        "Try different study habits and compare an illustrative score."
    )

    current_marks = st.slider(
        "Current marks (%)",
        0, 100, int(average)
    )

    current_attendance = st.slider(
        "Expected attendance (%)",
        0, 100, attendance
    )

    current_study_hours = st.slider(
        "Current daily study hours",
        0.0, 12.0, float(daily_hours), 0.5
    )

    extra_hours = st.slider(
        "Additional daily study hours",
        0.0, 5.0, 1.0, 0.5
    )

    days_available = st.slider(
        "Days available until exam",
        1, 120, 14
    )

    before_score = round(
        0.70 * current_marks
        + 0.20 * attendance
        + 0.10 * min(current_study_hours * 10, 100),
        1
    )

    proposed_hours = min(
        12, current_study_hours + extra_hours
    )

    after_score = round(
        0.70 * current_marks
        + 0.20 * current_attendance
        + 0.10 * min(proposed_hours * 10, 100),
        1
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Scenario", f"{before_score}%")
    col2.metric("Proposed Scenario", f"{after_score}%")
    col3.metric(
        "Difference",
        f"{after_score - before_score:+.1f}%"
    )

    st.write(
        f"With {proposed_hours} study hours per day for "
        f"{days_available} days, your planned extra study time "
        f"is {extra_hours * days_available:.1f} hours."
    )

    comparison_df = pd.DataFrame({
        "Scenario": ["Current", "Proposed"],
        "Illustrative Score": [before_score, after_score]
    }).set_index("Scenario")

    st.bar_chart(comparison_df)

    st.caption(
        "These figures are illustrative calculations, not a reliable "
        "prediction of actual marks. Real results depend on many factors."
    )

# ---------------- PROGRESS & REPORT ----------------
elif page == "Progress & Report":
    st.title("📈 Progress & Report")
    st.write(f"Track topic completion for {year} — {semester}.")

    st.info(
        "Enter the number of topics in each subject and how many "
        "you have completed. Your progress summary updates automatically."
    )

    report_rows = []

    for subject in subjects:
        progress_key = f"{year}_{semester}_{subject}_progress"
        saved = st.session_state.progress[progress_key]

        st.markdown(f"### 📘 {subject}")

        col1, col2 = st.columns(2)

        with col1:
            total = st.number_input(
                f"Total topics — {subject}",
                min_value=1,
                max_value=500,
                value=int(saved["total"]),
                key=f"total_{year}_{semester}_{subject}"
            )

        with col2:
            completed = st.number_input(
                f"Completed topics — {subject}",
                min_value=0,
                max_value=int(total),
                value=min(int(saved["completed"]), int(total)),
                key=f"completed_{year}_{semester}_{subject}"
            )

        completed = min(completed, total)

        st.session_state.progress[progress_key] = {
            "total": int(total),
            "completed": int(completed)
        }

        percent = round(completed / total * 100, 1)

        st.progress(percent / 100)
        st.caption(f"Completed: {completed}/{total} topics ({percent}%)")

        report_rows.append({
            "Year": year,
            "Semester": semester,
            "Subject": subject,
            "Marks (%)": st.session_state.marks[
                f"{year}_{semester}_{subject}_mark"
            ],
            "Total Topics": total,
            "Completed Topics": completed,
            "Progress (%)": percent
        })

    report_df = pd.DataFrame(report_rows)

    total_topics = int(report_df["Total Topics"].sum())
    completed_topics = int(report_df["Completed Topics"].sum())

    overall_progress = round(
        completed_topics / total_topics * 100, 1
    ) if total_topics else 0

    st.markdown("---")
    st.subheader("🎯 Overall Progress")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Topics", total_topics)
    col2.metric("Completed Topics", completed_topics)
    col3.metric("Overall Completion", f"{overall_progress}%")

    st.progress(overall_progress / 100)

    st.subheader("📊 Subject-wise Progress")
    progress_chart = report_df[
        ["Subject", "Progress (%)"]
    ].set_index("Subject")

    st.bar_chart(progress_chart)

    st.subheader("📄 Your Progress Report")
    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True
    )

    csv_report = report_df.to_csv(index=False)

    st.download_button(
        "⬇️ Download Progress Report (CSV)",
        data=csv_report,
        file_name="gradegenius_progress_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "Progress is kept in the current Streamlit session. "
        "It is not permanently saved to a database."
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "🎓 GradeGenius • Plan your learning, track your progress, "
    "and build better study habits."
)
