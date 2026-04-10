import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Attendance Insight Generator", layout="wide")

# ----------- 3D WEBSITE STYLE CSS -----------

st.markdown("""
<style>

.big-title{
    text-align:center;
    font-size:120px;
    font-weight:900;
    color:#1f3c88;
    text-shadow:3px 3px 8px rgba(0,0,0,0.3);
}

.page-title{
    text-align:center;
    font-size:90px;
    font-weight:900;
    color:#2c3e50;
    text-shadow:2px 2px 6px rgba(0,0,0,0.25);
}

.card{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.15);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-10px);
    box-shadow:0px 15px 35px rgba(0,0,0,0.35);
}

</style>
""", unsafe_allow_html=True)

# ----------- SIDEBAR MENU -----------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Upload Data", "Attendance Analysis", "Graph Visualization", "AI Insights"]
)

# ----------- HOME PAGE -----------

if page == "Home":

    st.markdown('<p class="big-title">Smart Attendance Insight Generator</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>Upload Data</h3>
        Upload student attendance CSV data for analysis.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>Attendance Analysis</h3>
        System calculates attendance percentage automatically.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>Graph Dashboard</h3>
        Visualize attendance patterns with graphs.
        </div>
        """, unsafe_allow_html=True)

# ----------- UPLOAD DATA -----------

elif page == "Upload Data":

    st.markdown('<p class="page-title">Upload Attendance Data</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state["data"] = df

        st.subheader("Attendance Data")
        st.write(df)

# ----------- ATTENDANCE ANALYSIS -----------

elif page == "Attendance Analysis":

    st.markdown('<p class="page-title">Attendance Analysis</p>', unsafe_allow_html=True)

    if "data" in st.session_state:

        df = st.session_state["data"]

        df["Attendance_Percentage"] = (df["Classes_Attended"] / df["Total_Classes"]) * 100

        st.write(df)

    else:
        st.warning("Please upload data first.")

# ----------- GRAPH VISUALIZATION -----------

elif page == "Graph Visualization":

    st.markdown('<p class="page-title">Attendance Graph Visualization</p>', unsafe_allow_html=True)

    if "data" in st.session_state:

        df = st.session_state["data"]

        df["Attendance_Percentage"] = (df["Classes_Attended"] / df["Total_Classes"]) * 100

        st.subheader("Bar Chart")

        fig, ax = plt.subplots()
        ax.bar(df["Name"], df["Attendance_Percentage"])
        ax.set_ylabel("Attendance Percentage")
        ax.set_title("Student Attendance")

        ax.tick_params(axis='x', labelsize=7)

        st.pyplot(fig)

        st.subheader("Pie Chart (Attendance Distribution)")

        def risk_level(percent):
            if percent >= 75:
                return "Safe"
            elif percent >= 60:
                return "Warning"
            else:
                return "High Risk"

        df["Risk_Level"] = df["Attendance_Percentage"].apply(risk_level)

        risk_counts = df["Risk_Level"].value_counts()

        fig2, ax2 = plt.subplots()

        ax2.pie(
            risk_counts,
            labels=risk_counts.index,
            autopct='%1.1f%%'
        )

        ax2.set_title("Attendance Risk Distribution")

        st.pyplot(fig2)

    else:
        st.warning("Please upload data first.")

# ----------- AI INSIGHTS -----------

elif page == "AI Insights":

    st.markdown('<p class="page-title">AI Generated Insights</p>', unsafe_allow_html=True)

    if "data" in st.session_state:

        df = st.session_state["data"]

        df["Attendance_Percentage"] = (df["Classes_Attended"] / df["Total_Classes"]) * 100

        def risk_level(percent):
            if percent >= 75:
                return "Safe"
            elif percent >= 60:
                return "Warning"
            else:
                return "High Risk"

        df["Risk_Level"] = df["Attendance_Percentage"].apply(risk_level)

        st.subheader("Warning Messages")

        for index, row in df.iterrows():

            if row["Risk_Level"] == "High Risk":
                st.error(f" Dear {row['Name']}, your attendance is {row['Attendance_Percentage']:.2f}%.")

            elif row["Risk_Level"] == "Warning":
                st.warning(f" Dear {row['Name']}, your attendance is close to shortage ({row['Attendance_Percentage']:.2f}%).")

            else:
                st.success(f" {row['Name']} has good attendance ({row['Attendance_Percentage']:.2f}%).")

        st.subheader("Overall Insights")

        avg = df["Attendance_Percentage"].mean()
        high_risk = len(df[df["Risk_Level"]=="High Risk"])
        warning = len(df[df["Risk_Level"]=="Warning"])

        st.write(f"Average Class Attendance: {avg:.2f}%")
        st.write(f"Students at High Risk: {high_risk}")
        st.write(f"Students Near Attendance Shortage: {warning}")

    else:
        st.warning("Please upload data first.")