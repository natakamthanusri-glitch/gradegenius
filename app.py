import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="Student Study Planner",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Student Study Companion")
st.write(
    "A smart study planner for 2nd, 3rd and 4th year students"
)

# Sidebar
st.sidebar.header("Student Details")

year = st.sidebar.selectbox(
    "Select Year",
    ["2nd Year", "3rd Year", "4th Year"]
)

semester = st.sidebar.selectbox(
    "Select Semester",
    ["Semester 1", "Semester 2"]
)

student = st.sidebar.text_input("Student Name")

# Subjects based on year
subjects_data = {
    "2nd Year": [
        "Data Structures",
        "Object Oriented Programming",
        "DBMS",
        "Operating Systems",
        "Discrete Mathematics"
    ],
    "3rd Year": [
        "Computer Networks",
        "Design and Analysis of Algorithms",
        "Software Engineering",
        "Theory of Computation",
        "Web Technologies"
    ],
    "4th Year": [
        "Artificial Intelligence",
        "Machine Learning",
        "Cloud Computing",
        "Cyber Security",
        "Project Work"
    ]
}

subjects = subjects_data[year]

st.sidebar.write("Selected:", year, "-", semester)

# Navigation
dashboard, planner, simulator, report = st.tabs([
    "🏠 Dashboard",
    "📅 Study Planner",
    "🔮 What-If Simulator",
    "📊 Progress Report"
])

# Store progress during the current session
progress_key = f"progress_{year}_{semester}"

if progress_key not in st.session_state:
    st.session_state[progress_key] = {
        subject: {"total": 5, "completed": 0}
        for subject in subjects
    }

progress = st.session_state[progress_key]

for subject in subjects:
    if subject not in progress:
        progress[subject] = {"total": 5, "completed": 0}

# DASHBOARD
with dashboard:
    if student.strip():
        st.subheader(f"Welcome, {student}!")
    else:
        st.subheader("Welcome, Student!")

    st.write(f"Year: **{year}**")
    st.write(f"Semester: **{semester}**")

    total_topics = sum(
        item["total"] for item in progress.values()
    )

    completed_topics = sum(
        item["completed"] for item in progress.values()
    )

    remaining = total_topics - completed_topics

    percentage = (
        completed_topics / total_topics * 100
        if total_topics else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Subjects", len(subjects))
    c2.metric("Completed Topics", completed_topics)
    c3.metric("Overall Progress", f"{percentage:.1f}%")

    st.progress(int(percentage))
    st.write("### Your Subjects")

    for subject in subjects:
        st.write("📘", subject)

# STUDY PLANNER
with planner:
    st.subheader("📅 Personal Study Planner")

    st.write(
        "Create a daily study schedule for your selected subjects."
    )

    hours = st.number_input(
        "Daily Study Hours",
        min_value=1,
        max_value=16,
        value=3
    )

    start_date = st.date_input(
        "Start Date",
        value=date.today()
    )

    exam_date = st.date_input(
        "Exam Date",
        value=date.today() + timedelta(days=7),
        min_value=date.today()
    )

    selected_subjects = st.multiselect(
        "Choose Subjects",
        subjects,
        default=subjects
    )

    if st.button("Generate Study Plan"):
        if not selected_subjects:
            st.warning("Please select at least one subject.")

        elif exam_date < start_date:
            st.error("Exam date must be after the start date.")

        else:
            days = (exam_date - start_date).days + 1
            rows = []

            for i in range(days):
                study_date = start_date + timedelta(days=i)
                subject = selected_subjects[
                    i % len(selected_subjects)
                ]

                rows.append({
                    "Date": study_date.strftime("%d-%m-%Y"),
                    "Day": study_date.strftime("%A"),
                    "Subject": subject,
                    "Study Hours": hours,
                    "Task": "Learn topics, revise notes and practise questions"
                })

            plan_df = pd.DataFrame(rows)

            st.success("Study plan generated successfully!")
            st.dataframe(plan_df, use_container_width=True)

            st.download_button(
                "Download Study Plan",
                data=plan_df.to_csv(index=False),
                file_name="study_plan.csv",
                mime="text/csv"
            )

# WHAT-IF SIMULATOR
with simulator:
    st.subheader("🔮 What-If Simulator")

    st.write(
        "See how changing your daily study hours affects "
        "your total preparation time."
    )

    current_hours = st.slider(
        "Current Study Hours Per Day",
        1, 12, 2
    )

    new_hours = st.slider(
        "What if you study this many hours per day?",
        1, 12, 4
    )

    days_left = st.number_input(
        "Days Until Exam",
        min_value=1,
        max_value=365,
        value=14
    )

    current_total = current_hours * days_left
    new_total = new_hours * days_left
    difference = new_total - current_total

    c1, c2, c3 = st.columns(3)

    c1.metric("Current Total Hours", current_total)
    c2.metric("New Total Hours", new_total)
    c3.metric("Change in Hours", f"{difference:+}")

    if difference > 0:
        st.success(
            f"You gain {difference} extra study hours before your exam!"
        )
    elif difference < 0:
        st.warning(
            f"You have {abs(difference)} fewer study hours."
        )
    else:
        st.info("Your total study time remains the same.")

    st.caption(
        "This is a study-time estimate, not a prediction of exam marks."
    )

# PROGRESS REPORT
with report:
    st.subheader("📊 Progress Report")

    st.write(
        "Update completed topics for each subject "
        "to track your preparation."
    )

    report_rows = []

    for subject in subjects:
        st.markdown(f"### {subject}")

        total = st.number_input(
            f"Total Topics - {subject}",
            min_value=1,
            max_value=500,
            value=int(progress[subject]["total"]),
            key=f"total_{year}_{semester}_{subject}"
        )

        completed = st.number_input(
            f"Completed Topics - {subject}",
            min_value=0,
            max_value=int(total),
            value=min(
                int(progress[subject]["completed"]),
                int(total)
            ),
            key=f"completed_{year}_{semester}_{subject}"
        )

        progress[subject] = {
            "total": int(total),
            "completed": int(completed)
        }

        percent = completed / total * 100

        st.progress(int(percent))
        st.write(f"Progress: {percent:.1f}%")

        report_rows.append({
            "Subject": subject,
            "Completed": completed,
            "Remaining": total - completed,
            "Progress (%)": round(percent, 1)
        })

    df = pd.DataFrame(report_rows)

    total_completed = int(df["Completed"].sum())
    total_remaining = int(df["Remaining"].sum())
    total_all = total_completed + total_remaining

    overall = (
        total_completed / total_all * 100
        if total_all else 0
    )

    st.divider()
    st.subheader("Overall Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric("Completed", total_completed)
    c2.metric("Remaining", total_remaining)
    c3.metric("Progress", f"{overall:.1f}%")

    st.bar_chart(
        df.set_index("Subject")[["Completed", "Remaining"]]
    )

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Progress Report",
        data=df.to_csv(index=False),
        file_name="progress_report.csv",
        mime="text/csv"
    )

st.divider()
st.caption(
    "Student Study Companion | Plan Smart • Study Better • Track Progress"
)
