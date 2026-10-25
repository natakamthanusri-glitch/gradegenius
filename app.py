import streamlit as st
import pandas as pd

# =====================================================
# GRADEGENIUS - STUDENT ACADEMIC & CAREER GUIDANCE APP
# =====================================================

st.set_page_config(
    page_title="GradeGenius | Learn & Grow",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- THEME --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F3EDFF 0%, #FFF1F6 55%, #F9F5FF 100%);
    color: #382B50;
}
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}
[data-testid="stSidebar"] {
    background: #EAE0FA;
    border-right: 1px solid #DCCBF4;
}
h1, h2, h3 {
    color: #493566 !important;
}
.gg-card {
    background: #FFFCFF;
    border: 1px solid #E5D8F5;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 15px;
}
.gg-hero {
    background: linear-gradient(115deg, #E3D6FA, #FCE1EB);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 20px;
}
.gg-small {
    color: #786985;
    font-size: 0.92rem;
}
div.stButton > button,
div.stFormSubmitButton > button {
    background: #8666CF;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 42px;
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #6D4DB8;
    color: white;
    border: 0;
}
[data-testid="stMetric"] {
    background: #FFFCFF;
    border: 1px solid #E5D8F5;
    border-radius: 16px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SUBJECT INFORMATION --------------------

SUBJECTS = {
    "DBMS": {
        "full": "Database Management Systems",
        "roles": "Backend Developer, Database Developer, Data Engineer",
        "uses": "Websites and applications store customer profiles, "
                "orders, payments and other information in databases.",
        "skills": "SQL, joins, keys, normalization, database design",
        "project": "Student Records Management System",
        "tasks": [
            "Revise tables, primary keys and foreign keys.",
            "Practice SQL SELECT, WHERE and ORDER BY.",
            "Solve SQL INSERT, UPDATE and DELETE exercises.",
            "Practice joins using two related tables.",
            "Learn normalization with simple examples.",
            "Build a small student database.",
            "Review queries and explain what each one does."
        ]
    },
    "DMS": {
        "full": "Discrete Mathematical Structures",
        "roles": "Software Engineer, Algorithm Developer",
        "uses": "Logic, sets, relations, graphs and counting techniques "
                "support algorithms, software reasoning and computing.",
        "skills": "Propositional logic, sets, relations, graphs, counting",
        "project": "Campus Route Planner using graphs",
        "tasks": [
            "Revise propositions and logical operators.",
            "Practice truth tables.",
            "Solve set and relation problems.",
            "Practice permutations and combinations.",
            "Learn graph representations.",
            "Solve application-based problems.",
            "Review mistakes and explain the reasoning."
        ]
    },
    "OOPS": {
        "full": "Object-Oriented Programming",
        "roles": "Java Developer, Application Developer, Backend Developer",
        "uses": "Classes, objects and reusable components help developers "
                "organize and maintain large software applications.",
        "skills": "Classes, objects, inheritance, polymorphism, abstraction",
        "project": "Student Management Application",
        "tasks": [
            "Revise classes and objects.",
            "Write constructors and methods.",
            "Practice encapsulation.",
            "Implement inheritance.",
            "Practice polymorphism.",
            "Build a small object-oriented application.",
            "Test your code and review the design."
        ]
    },
    "DS": {
        "full": "Data Structures",
        "roles": "Software Engineer, Backend Developer, Systems Developer",
        "uses": "Data structures support efficient searching, scheduling, "
                "data processing and memory organization.",
        "skills": "Arrays, linked lists, stacks, queues, trees, sorting",
        "project": "Task Manager using a queue",
        "tasks": [
            "Revise arrays and their operations.",
            "Practice linked-list insertion.",
            "Practice linked-list deletion.",
            "Implement stacks and queues.",
            "Trace sorting algorithms.",
            "Solve beginner coding problems.",
            "Review time complexity and mistakes."
        ]
    },
    "AI": {
        "full": "Artificial Intelligence",
        "roles": "AI Engineer, Machine Learning Engineer, AI Application Developer",
        "uses": "AI supports prediction, recommendations, intelligent "
                "assistants, image recognition and automation.",
        "skills": "Python, data preparation, algorithms, model evaluation",
        "project": "Beginner Student Performance Analyzer",
        "tasks": [
            "Revise AI fundamentals and terminology.",
            "Practice Python basics.",
            "Learn data preparation.",
            "Explore search and reasoning algorithms.",
            "Understand training and testing data.",
            "Build a small beginner AI project.",
            "Review results and identify model limitations."
        ]
    },
    "DLD": {
        "full": "Digital Logic Design",
        "roles": "Embedded Systems Engineer, Digital Design Engineer, FPGA Engineer",
        "uses": "Digital logic underlies processors, controllers, "
                "electronic devices and computer hardware.",
        "skills": "Logic gates, Boolean algebra, truth tables, adders",
        "project": "Binary Adder/Subtractor Simulator",
        "tasks": [
            "Revise AND, OR and NOT gates.",
            "Practice logic-gate truth tables.",
            "Simplify Boolean expressions.",
            "Study combinational circuits.",
            "Practice half adders and full adders.",
            "Study binary addition and subtraction.",
            "Draw and verify circuit diagrams."
        ]
    },
    "DW": {
        "full": "Data Warehousing",
        "roles": "Data Analyst, BI Developer, Data Engineer",
        "uses": "Organizations combine data from different sources "
                "for reports, dashboards and business decisions.",
        "skills": "ETL, SQL, fact tables, dimension tables, star schemas",
        "project": "Academic Performance Analytics Dashboard",
        "tasks": [
            "Revise data warehouse fundamentals.",
            "Compare OLTP and OLAP.",
            "Learn fact and dimension tables.",
            "Draw a simple star schema.",
            "Understand ETL steps.",
            "Explore a reporting dataset.",
            "Create a simple analytics dashboard."
        ]
    }
}

# -------------------- SESSION DATA --------------------

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "year": "B.Tech 1st Year",
        "goal": "Software Development"
    }

if "subject_data" not in st.session_state:
    st.session_state.subject_data = {
        subject: {
            "marks": 60,
            "attendance": 80,
            "hours": 5.0,
            "assignments": 70
        }
        for subject in SUBJECTS
    }

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "planner_checks" not in st.session_state:
    st.session_state.planner_checks = {}

# -------------------- HELPER FUNCTIONS --------------------

def estimate_score(values):
    """
    Transparent illustrative score, NOT a trained ML prediction.
    Inputs are normalized to a 0-100 scale.
    """
    study_score = min(values["hours"] / 20 * 100, 100)
    return round(
        0.55 * values["marks"]
        + 0.15 * values["attendance"]
        + 0.15 * study_score
        + 0.15 * values["assignments"],
        1
    )


def progress_label(score):
    if score >= 85:
        return "Strong progress 🌟"
    elif score >= 70:
        return "Good progress 🌷"
    elif score >= 50:
        return "Building your skills 🌱"
    return "A fresh opportunity to practice 💜"


def encouragement(score):
    if score >= 85:
        return (
            "You're building a strong foundation. Keep practicing "
            "and try a project that challenges you."
        )
    elif score >= 70:
        return (
            "Your effort is moving you forward. Practice a few "
            "real-world problems to strengthen your skills."
        )
    elif score >= 50:
        return (
            "You're learning step by step. Focus on one concept "
            "at a time, practice regularly and review mistakes."
        )
    return (
        "Every learner starts somewhere. This result identifies "
        "topics to revisit; it does not define your ability or future. "
        "Begin with the basics and ask for help when needed."
    )


# -------------------- SIDEBAR --------------------

st.sidebar.markdown("# 🎓 GradeGenius")
st.sidebar.caption("Learn at your pace. Grow with purpose.")

page = st.sidebar.radio(
    "YOUR LEARNING SPACE",
    [
        "🏠 Home",
        "👤 Student Profile",
        "📊 Performance Dashboard",
        "💼 Career Connections",
        "📅 Study Planner",
        "🔮 What-if Simulator",
        "📄 Progress Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌷 Daily reminder")
st.sidebar.info(
    "Your marks describe a moment in your learning journey, "
    "not your potential."
)
st.sidebar.caption("7 subjects • Career insights • Study planning")

# =====================================================
# HOME
# =====================================================

if page == "🏠 Home":
    name = st.session_state.profile["name"]
    greeting = f"Welcome back, {name}!" if name else "Welcome to GradeGenius!"

    st.markdown(
        f"""
        <div class="gg-hero">
            <h1>{greeting} 🌷</h1>
            <h3>Understand your progress. Discover your potential.</h3>
            <p>Turn academic learning into practical skills for your future.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Subjects", "7")
    c2.metric("Career connections", "7")
    c3.metric("Your focus", "Steady growth")

    st.markdown("## Your learning journey")
    a, b = st.columns(2)

    with a:
        st.markdown(
            """
            <div class="gg-card">
            <h3>📊 Understand your progress</h3>
            Enter your subject marks, attendance, study time and
            assignment completion to review your current learning.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="gg-card">
            <h3>💼 Connect learning to careers</h3>
            Discover how your subjects connect to software,
            data, AI and hardware-related roles.
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            """
            <div class="gg-card">
            <h3>📅 Build a practical routine</h3>
            Follow a manageable seven-day study plan and track
            the tasks you complete.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="gg-card">
            <h3>🌱 Focus on improvement</h3>
            Find the next topic to practice without treating
            a single score as a measure of your potential.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Getting started: complete Student Profile, then enter "
        "your subject details in Performance Dashboard."
    )

# =====================================================
# STUDENT PROFILE
# =====================================================

elif page == "👤 Student Profile":
    st.header("Your Student Profile 🌷")
    st.write("Set up your profile and choose a career interest.")

    current = st.session_state.profile

    years = [
        "B.Tech 1st Year",
        "B.Tech 2nd Year",
        "B.Tech 3rd Year",
        "B.Tech 4th Year"
    ]
    goals = [
        "Software Development",
        "AI and Machine Learning",
        "Data Engineering and Analytics",
        "Embedded Systems",
        "Exploring careers"
    ]

    with st.form("profile_form"):
        name = st.text_input("Your name", value=current["name"])
        year = st.selectbox(
            "Academic year",
            years,
            index=years.index(current["year"])
        )
        goal = st.selectbox(
            "Career interest",
            goals,
            index=goals.index(current["goal"])
        )

        save_profile = st.form_submit_button("Save Profile")

    if save_profile:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            st.session_state.profile = {
                "name": name.strip(),
                "year": year,
                "goal": goal
            }
            st.success("Your profile has been saved for this session!")

    st.markdown("### Your profile summary")
    st.write("**Name:**", st.session_state.profile["name"] or "Not entered")
    st.write("**Year:**", st.session_state.profile["year"])
    st.write("**Career interest:**", st.session_state.profile["goal"])

# =====================================================
# PERFORMANCE DASHBOARD
# =====================================================

elif page == "📊 Performance Dashboard":
    st.header("Your Academic Dashboard 🌷")
    st.write(
        "Enter your current values for each subject. "
        "Use real academic records wherever possible."
    )

    with st.form("subject_inputs"):
        updated = {}

        for subject, info in SUBJECTS.items():
            st.markdown(f"### {subject} — {info['full']}")
            old = st.session_state.subject_data[subject]

            left, right = st.columns(2)

            with left:
                marks = st.number_input(
                    f"{subject}: Marks (%)",
                    min_value=0,
                    max_value=100,
                    value=int(old["marks"]),
                    key=f"marks_{subject}"
                )
                attendance = st.number_input(
                    f"{subject}: Attendance (%)",
                    min_value=0,
                    max_value=100,
                    value=int(old["attendance"]),
                    key=f"attendance_{subject}"
                )

            with right:
                hours = st.number_input(
                    f"{subject}: Study hours per week",
                    min_value=0.0,
                    max_value=60.0,
                    value=float(old["hours"]),
                    step=0.5,
                    key=f"hours_{subject}"
                )
                assignments = st.number_input(
                    f"{subject}: Assignment completion (%)",
                    min_value=0,
                    max_value=100,
                    value=int(old["assignments"]),
                    key=f"assignments_{subject}"
                )

            updated[subject] = {
                "marks": marks,
                "attendance": attendance,
                "hours": hours,
                "assignments": assignments
            }

        analyze = st.form_submit_button(
            "✨ Analyze My Learning",
            use_container_width=True
        )

    if analyze:
        st.session_state.subject_data = updated
        st.session_state.analyzed = True

    if st.session_state.analyzed:
        data = st.session_state.subject_data
        scores = {
            subject: estimate_score(values)
            for subject, values in data.items()
        }

        average = sum(scores.values()) / len(scores)

        st.markdown("## Your learning snapshot")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average indicative score", f"{average:.1f}/100")
        col2.metric("Subjects tracked", "7")
        col3.metric(
            "Study time per week",
            f"{sum(v['hours'] for v in data.values()):.1f} hrs"
        )

        st.caption(
            "These are illustrative rule-based scores, not trained "
            "machine-learning predictions or guaranteed exam marks."
        )

        rows = []
        for subject, score in scores.items():
            rows.append({
                "Subject": subject,
                "Current marks (%)": data[subject]["marks"],
                "Indicative score": score,
                "Learning insight": progress_label(score)
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("## Subject comparison")
        chart_df = pd.DataFrame({
            "Indicative score": scores
        })
        st.bar_chart(chart_df)

        st.markdown("## Your next steps 💜")

        for subject, score in scores.items():
            info = SUBJECTS[subject]
            values = data[subject]

            with st.expander(
                f"{subject} — {progress_label(score)}"
            ):
                st.write(encouragement(score))
                st.write(f"**Career connection:** {info['roles']}")
                st.write(f"**Industry application:** {info['uses']}")
                st.write(f"**Skills to practice:** {info['skills']}")
                st.write(f"**Suggested project:** {info['project']}")

                if values["marks"] < 50:
                    st.write(
                        "**Suggested starting point:** Revisit one "
                        "fundamental concept and solve a few beginner "
                        "questions before moving to harder topics."
                    )
                elif values["marks"] < 75:
                    st.write(
                        "**Suggested next step:** Practice problems "
                        "and apply one concept in a small project."
                    )
                else:
                    st.write(
                        "**Suggested next step:** Challenge yourself "
                        "with a practical project or more advanced problems."
                    )

                st.progress(int(max(0, min(100, score))))

    else:
        st.info(
            "Enter your subject details and click Analyze My Learning "
            "to view the dashboard."
        )

# =====================================================
# CAREER CONNECTIONS
# =====================================================

elif page == "💼 Career Connections":
    st.header("From Subjects to Software Careers 💼")
    st.write(
        "Explore real-world applications and beginner projects "
        "connected to your subjects."
    )

    selected = st.selectbox(
        "Choose a subject",
        list(SUBJECTS.keys())
    )
    info = SUBJECTS[selected]
    values = st.session_state.subject_data[selected]

    st.markdown(
        f"""
        <div class="gg-hero">
            <h2>{selected}: {info['full']}</h2>
            <p>{info['uses']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💻 Related job roles")
    st.write(info["roles"])

    st.markdown("### 🧠 Skills to build")
    st.write(info["skills"])

    st.markdown("### 🛠️ Beginner project idea")
    st.write(info["project"])

    st.markdown("### 🌱 How to get started")
    st.write(
        "Choose one skill, learn the fundamentals, practice it regularly, and build a small project."
