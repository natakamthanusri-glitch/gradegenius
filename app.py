import streamlit as st
import pandas as pd
from datetime import date, timedelta
import html

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GradeGenius",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
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
    margin-bottom: 18px;
}
.gg-purple {
    background: #E3D7FA;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
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

# ---------------- SUBJECT LIST ----------------
SUBJECTS = {
    "2nd Year": {
        "Semester 1": [
            "OOPS", "DS", "DBMS", "DW", "DMS", "AI"
        ],
        "Semester 2": [
            "Java Programming", "Operating Systems",
            "Computer Networks", "Software Engineering",
            "Web Technologies", "Algorithms"
        ]
    },
    "3rd Year": {
        "Semester 1": [
            "Artificial Intelligence", "Machine Learning",
            "Computer Networks", "Web Technologies",
            "Theory of Computation", "Data Mining"
        ],
        "Semester 2": [
            "Cloud Computing", "Cyber Security",
            "Big Data Analytics", "Compiler Design",
            "Distributed Systems", "Elective"
        ]
    },
    "4th Year": {
        "Semester 1": [
            "Deep Learning", "Big Data Analytics",
            "Project Work", "Internet of Things",
            "Professional Elective", "Open Elective"
        ],
        "Semester 2": [
            "Major Project", "Internship",
            "Technical Seminar", "Professional Ethics",
            "Open Elective", "Elective"
        ]
    }
}

# ---------------- SESSION DATA ----------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "course": "B.Tech",
        "year": "2nd Year",
        "semester": "Semester 1",
        "attendance": 75,
        "study_hours": 3
    }

if "subject_data" not in st.session_state:
    st.session_state.subject_data = {}

if "study_plan" not in st.session_state:
    st.session_state.study_plan = []

# ---------------- HELPER FUNCTIONS ----------------
def get_subject_key(year, semester, subject):
    return f"{year}_{semester}_{subject}"

def get_subject_data(year, semester, subject):
    key = get_subject_key(year, semester, subject)

    if key not in st.session_state.subject_data:
        st.session_state.subject_data[key] = {
            "marks": 0.0,
            "attendance": 75.0,
            "study_hours": 1.0,
            "assignments_done": 0,
            "assignments_total": 5,
            "topics_done": 0,
            "topics_total": 10
        }

    return st.session_state.subject_data[key]

def current_subjects():
    profile = st.session_state.profile
    return SUBJECTS[profile["year"]][profile["semester"]]

def calculate_average(subjects, year, semester):
    if not subjects:
        return 0

    marks = [
        get_subject_data(year, semester, subject)["marks"]
        for subject in subjects
    ]

    return round(sum(marks) / len(marks), 1)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("# 🎓 GradeGenius")
st.sidebar.caption("Your personal academic companion")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "My Subjects",
        "Study Planner",
        "What-if Simulator",
        "Progress & Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Daily Reminder")
st.sidebar.info("Small steps every day lead to big results.")

profile = st.session_state.profile
year = profile["year"]
semester = profile["semester"]
subjects = current_subjects()

# ---------------- HOME PAGE ----------------
if page == "Home":
    st.title("🎓 GradeGenius")
    st.header("Welcome to your learning journey ✨")
    st.write("Predict. Plan. Perform.")

    st.markdown("""
    <div class="gg-pink">
        <h3>🏠 Student Home Page</h3>
        <p>Enter your details below to personalize your academic dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_details_form"):
        st.subheader("👤 Student Details")

        name = st.text_input(
            "Student Name",
            value=profile["name"],
            placeholder="Enter your full name"
        )

        course = st.selectbox(
            "Course",
            ["B.Tech", "B.Sc", "BCA", "Other"],
            index=["B.Tech", "B.Sc", "BCA", "Other"].index(
                profile["course"]
            )
        )

        year = st.selectbox(
            "Year",
            ["2nd Year", "3rd Year", "4th Year"],
            index=["2nd Year", "3rd Year", "4th Year"].index(
                profile["year"]
            )
        )

        semester = st.selectbox(
            "Semester",
            ["Semester 1", "Semester 2"],
            index=["Semester 1", "Semester 2"].index(
                profile["semester"]
            )
        )

        st.subheader("📅 General Academic Details")

        attendance = st.number_input(
            "Overall Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(profile["attendance"]),
            step=1.0
        )

        study_hours = st.number_input(
            "Available Daily Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=float(profile["study_hours"]),
            step=0.5
        )

        save_profile = st.form_submit_button(
            "💾 Save Student Details",
            use_container_width=True
        )

    if save_profile:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            st.session_state.profile = {
                "name": name.strip(),
                "course": course,
                "year": year,
                "semester": semester,
                "attendance": attendance,
                "study_hours": study_hours
            }

            st.success("Student details saved successfully!")
            st.rerun()

    profile = st.session_state.profile
    subjects = current_subjects()

    st.markdown("---")
    st.subheader("📊 Academic Overview")

    if profile["name"]:
        st.markdown(
            f"### Hello, {html.escape(profile['name'])}! 👋"
        )
    else:
        st.info("Save your student details to personalize this page.")

    st.write(
        f"**{profile['year']} — {profile['semester']}**"
    )

    average = calculate_average(
        subjects, profile["year"], profile["semester"]
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Subject Average", f"{average}%")
    col2.metric("Overall Attendance", f"{profile['attendance']}%")
    col3.metric("Daily Study Hours", f"{profile['study_hours']}")

    st.markdown("### 📚 Your Subjects")

    subject_rows = []

    for subject in subjects:
        data = get_subject_data(
            profile["year"], profile["semester"], subject
        )
        subject_rows.append({
            "Subject": subject,
            "Marks (%)": data["marks"],
            "Attendance (%)": data["attendance"],
            "Study Hours": data["study_hours"]
        })

    st.dataframe(
        pd.DataFrame(subject_rows),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Enter or update individual subject details in My Subjects."
    )

# ---------------- MY SUBJECTS ----------------
elif page == "My Subjects":
    st.title("📚 My Subjects")
    st.write(f"**{year} — {semester}**")

    st.info(
        "Type your marks and other details manually for every subject. "
        "Your entries update the current session's dashboard and reports."
    )

    for subject in subjects:
        data = get_subject_data(year, semester, subject)

        with st.container(border=True):
            st.subheader(f"📘 {subject}")

            c1, c2 = st.columns(2)

            with c1:
                data["marks"] = st.number_input(
                    f"{subject} Marks (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(data["marks"]),
                    step=1.0,
                    key=f"marks_{year}_{semester}_{subject}"
                )

                data["attendance"] = st.number_input(
                    f"{subject} Attendance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(data["attendance"]),
                    step=1.0,
                    key=f"attendance_{year}_{semester}_{subject}"
                )

            with c2:
                data["study_hours"] = st.number_input(
                    f"Daily Study Hours for {subject}",
                    min_value=0.0,
                    max_value=24.0,
                    value=float(data["study_hours"]),
                    step=0.5,
                    key=f"hours_{year}_{semester}_{subject}"
                )

                data["assignments_total"] = st.number_input(
                    f"Total Assignments — {subject}",
                    min_value=0,
                    max_value=100,
                    value=int(data["assignments_total"]),
                    step=1,
                    key=f"total_assign_{year}_{semester}_{subject}"
                )

            data["assignments_done"] = st.number_input(
                f"Assignments Completed — {subject}",
                min_value=0,
                max_value=int(data["assignments_total"]),
                value=min(
                    int(data["assignments_done"]),
                    int(data["assignments_total"])
                ),
                step=1,
                key=f"done_assign_{year}_{semester}_{subject}"
            )

            c3, c4 = st.columns(2)

            with c3:
                data["topics_total"] = st.number_input(
                    f"Total Topics — {subject}",
                    min_value=1,
                    max_value=500,
                    value=int(data["topics_total"]),
                    step=1,
                    key=f"total_topics_{year}_{semester}_{subject}"
                )

            with c4:
                data["topics_done"] = st.number_input(
                    f"Topics Completed — {subject}",
                    min_value=0,
                    max_value=int(data["topics_total"]),
                    value=min(
                        int(data["topics_done"]),
                        int(data["topics_total"])
                    ),
                    step=1,
                    key=f"done_topics_{year}_{semester}_{subject}"
                )

            assignment_total = data["assignments_total"]
            assignment_done = min(
                data["assignments_done"], assignment_total
            )

            assignment_percent = (
                assignment_done / assignment_total * 100
                if assignment_total > 0 else 0
            )

            st.progress(assignment_percent / 100)
            st.caption(
                f"Assignments: {assignment_done}/{assignment_total} "
                f"({assignment_percent:.1f}%)"
            )

            topic_percent = (
                data["topics_done"] / data["topics_total"] * 100
            )

            st.progress(topic_percent / 100)
            st.caption(
                f"Topics: {data['topics_done']}/{data['topics_total']} "
                f"({topic_percent:.1f}%)"
            )

    st.markdown("---")

    average = calculate_average(subjects, year, semester)
    st.metric("Current Subject Average", f"{average}%")

    rows = []
    for subject in subjects:
        data = get_subject_data(year, semester, subject)
        rows.append({
            "Year": year,
            "Semester": semester,
            "Subject": subject,
            "Marks (%)": data["marks"],
            "Attendance (%)": data["attendance"],
            "Daily Study Hours": data["study_hours"],
            "Assignments Completed": data["assignments_done"],
            "Total Assignments": data["assignments_total"],
            "Topics Completed": data["topics_done"],
            "Total Topics": data["topics_total"]
        })

    st.download_button(
        "⬇️ Download Subject Details",
        data=pd.DataFrame(rows).to_csv(index=False),
        file_name="gradegenius_subjects.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------- STUDY PLANNER ----------------
elif page == "Study Planner":
    st.title("🗓️ Personalized Study Planner")
    st.write("Build a timetable based on your available time.")

    exam_date = st.date_input(
        "Exam Date",
        value=date.today() + timedelta(days=7),
        min_value=date.today()
    )

    hours_per_day = st.number_input(
        "Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=max(1, min(12, int(profile["study_hours"])))
    )

    selected_subjects = st.multiselect(
        "Select Subjects",
        options=subjects,
        default=subjects
    )

    if st.button("✨ Generate Study Plan", use_container_width=True):
        days = (exam_date - date.today()).days

        if days < 1:
            st.error("Choose an exam date after today.")
        elif not selected_subjects:
            st.error("Select at least one subject.")
        else:
            plan = []

            for i in range(days):
                study_date = date.today() + timedelta(days=i)
                subject = selected_subjects[i % len(selected_subjects)]

                task = (
                    "Revise concepts and prepare notes"
                    if i % 2 == 0
                    else "Solve practice questions and review mistakes"
                )

                plan.append({
                    "Date": study_date.strftime("%d-%m-%Y"),
                    "Day": study_date.strftime("%A"),
                    "Subject": subject,
                    "Study Hours": hours_per_day,
                    "Suggested Task": task
                })

            st.session_state.study_plan = plan

    if st.session_state.study_plan:
        plan_df = pd.DataFrame(st.session_state.study_plan)

        st.subheader("📅 Your Timetable")
        st.dataframe(
            plan_df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Timetable generated for {len(plan_df)} days."
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
        "Compare your current routine with a possible new study routine."
    )

    average = calculate_average(subjects, year, semester)

    current_marks = st.number_input(
        "Current Average Marks (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(average),
        step=1.0
    )

    new_attendance = st.number_input(
        "Expected Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(profile["attendance"]),
        step=1.0
    )

    current_hours = st.number_input(
        "Current Daily Study Hours",
        min_value=0.0,
        max_value=24.0,
        value=float(profile["study_hours"]),
        step=0.5
    )

    extra_hours = st.number_input(
        "Additional Daily Study Hours",
        min_value=0.0,
        max_value=12.0,
        value=1.0,
        step=0.5
    )

    days = st.number_input(
        "Days Until Exam",
        min_value=1,
        max_value=365,
        value=14
    )

    proposed_hours = min(24, current_hours + extra_hours)

    before = round(
        0.70 * current_marks
        + 0.20 * profile["attendance"]
        + 0.10 * min(current_hours * 10, 100),
        1
    )

    after = round(
        0.70 * current_marks
        + 0.20 * new_attendance
        + 0.10 * min(proposed_hours * 10, 100),
        1
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Scenario", f"{before}%")
    c2.metric("New Scenario", f"{after}%")
    c3.metric("Difference", f"{after - before:+.1f}%")

    st.write(
        f"Planned extra study time: **{extra_hours * days:.1f} hours** "
        f"over {days} days."
    )

    chart = pd.DataFrame({
        "Scenario": ["Current", "New"],
        "Illustrative Score (%)": [before, after]
    }).set_index("Scenario")

    st.bar_chart(chart)

    st.caption(
        "This is a simple illustrative calculation, not a guaranteed "
        "prediction of actual exam marks."
    )

# ---------------- PROGRESS & REPORT ----------------
elif page == "Progress & Report":
    st.title("📈 Progress & Report")
    st.write(f"**{year} — {semester}**")

    rows = []

    for subject in subjects:
        data = get_subject_data(year, semester, subject)

        topic_percent = (
            data["topics_done"] / data["topics_total"] * 100
            if data["topics_total"] > 0 else 0
        )

        assignment_percent = (
            data["assignments_done"] / data["assignments_total"] * 100
            if data["assignments_total"] > 0 else 0
        )

        rows.append({
            "Subject": subject,
            "Marks (%)": data["marks"],
            "Attendance (%)": data["attendance"],
            "Daily Study Hours": data["study_hours"],
            "Assignments Completed": data["assignments_done"],
            "Total Assignments": data["assignments_total"],
            "Assignment Progress (%)": round(assignment_percent, 1),
            "Topics Completed": data["topics_done"],
            "Total Topics": data["topics_total"],
            "Topic Progress (%)": round(topic_percent, 1)
        })

    report_df = pd.DataFrame(rows)

    total_topics = int(report_df["Total Topics"].sum())
    completed_topics = int(report_df["Topics Completed"].sum())

    overall_progress = (
        round(completed_topics / total_topics * 100, 1)
        if total_topics else 0
    )

    total_assignments = int(report_df["Total Assignments"].sum())
    completed_assignments = int(
        report_df["Assignments Completed"].sum()
    )

    assignment_progress = (
        round(completed_assignments / total_assignments * 100, 1)
        if total_assignments else 0
    )

    average = calculate_average(subjects, year, semester)

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Marks", f"{average}%")
    c2.metric("Topic Completion", f"{overall_progress}%")
    c3.metric("Assignment Completion", f"{assignment_progress}%")

    st.subheader("📚 Topic Progress by Subject")
    st.bar_chart(
        report_df.set_index("Subject")[["Topic Progress (%)"]]
    )

    st.subheader("📝 Assignment Progress by Subject")
    st.bar_chart(
        report_df.set_index("Subject")[["Assignment Progress (%)"]]
    )

    st.subheader("📋 Complete Progress Report")
    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True
    )

  st.download_button(
        "⬇️ Download Progress Report",
        data=report_df.to_csv(index=False),
        file_name="gradegenius_progress_report.csv",
        mime="text/csv",
        use_container_width=True
    )
