import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Constants
SUBJECTS = [
    "Mathematics", "Programming", "Statistics", "Database", "Algorithms",
    "Literature", "History", "Economics", "Psychology", "Chemistry",
    "Physics", "Biology", "Business", "Arts", "Languages"
]

# Set page config
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("student_performance.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Department filter
depts = sorted(df["Department"].unique())
selected_depts = st.sidebar.multiselect(
    "Select Departments", 
    depts, 
    default=depts
)

# Semester filter
semesters = sorted(df["Semester"].unique())
selected_semesters = st.sidebar.multiselect(
    "Select Semesters", 
    semesters, 
    default=semesters
)

# Risk status filter
risk_filter = st.sidebar.radio(
    "Risk Status",
    ["All Students", "At Risk Only", "Not At Risk"]
)

# Apply filters
filtered_df = df[
    (df["Department"].isin(selected_depts)) &
    (df["Semester"].isin(selected_semesters))
]

if risk_filter == "At Risk Only":
    filtered_df = filtered_df[filtered_df["At_Risk"]]
elif risk_filter == "Not At Risk":
    filtered_df = filtered_df[~filtered_df["At_Risk"]]

# Main dashboard
st.title("📚 Student Performance Analytics Dashboard")
st.markdown("""
Analyze academic performance and attendance patterns to identify at-risk students.
""")

# KPI cards
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(filtered_df))
col2.metric("At Risk Students", f"{filtered_df['At_Risk'].sum()} ({filtered_df['At_Risk'].mean()*100:.1f}%)")
col3.metric("Average Mark", f"{filtered_df['Semester_Average'].mean():.1f}")
col4.metric("Average Attendance", f"{filtered_df['Attendance_Perc'].mean():.1f}%")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "📈 Performance Trends", 
    "📅 Attendance Analysis", 
    "🔍 Student Explorer"
])

with tab1:
    st.subheader("Performance Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            filtered_df, 
            x="Semester_Average",
            nbins=20,
            title="Distribution of Semester Averages",
            color_discrete_sequence=["#636EFA"]
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        risk_by_dept = filtered_df.groupby("Department")["At_Risk"].mean().reset_index()
        fig = px.bar(
            risk_by_dept,
            x="Department",
            y="At_Risk",
            title="% At Risk Students by Department",
            labels={"At_Risk": "% At Risk"},
            color="Department"
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Performance vs Attendance")
    fig = px.scatter(
        filtered_df,
        x="Attendance_Perc",
        y="Semester_Average",
        color="At_Risk",
        title="Academic Performance vs Attendance",
        hover_name="Student_ID",
        hover_data=["First_Name", "Last_Name", "Department"],
        color_discrete_map={True: "#EF553B", False: "#636EFA"}
    )
    fig.update_layout(legend_title_text="At Risk")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sem_avg = filtered_df.groupby("Semester")["Semester_Average"].mean().reset_index()
        fig = px.line(
            sem_avg,
            x="Semester",
            y="Semester_Average",
            title="Average Performance by Semester",
            markers=True
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        subject_cols = [col for col in filtered_df.columns if col in SUBJECTS]
        subject_means = filtered_df[subject_cols].mean().reset_index()
        subject_means.columns = ["Subject", "Average"]
        subject_means = subject_means.sort_values("Average", ascending=False)
        
        fig = px.bar(
            subject_means,
            x="Subject",
            y="Average",
            title="Average Performance by Subject",
            color="Subject"
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Performance by Student Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(
            filtered_df,
            x="Financial_Aid",
            y="Semester_Average",
            title="Performance by Financial Aid Status",
            points="all"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            filtered_df,
            x="International",
            y="Semester_Average",
            title="Performance by International Status",
            points="all"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Attendance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            filtered_df,
            x="Attendance_Perc",
            nbins=20,
            title="Attendance Distribution",
            color_discrete_sequence=["#00CC96"]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            filtered_df,
            x="Department",
            y="Attendance_Perc",
            title="Attendance by Department",
            color="Department"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Attendance Trends Over Time")
    attend_trend = filtered_df.groupby(["Academic_Year", "Semester"])["Attendance_Perc"].mean().reset_index()
    attend_trend["Period"] = attend_trend["Academic_Year"] + " - Sem " + attend_trend["Semester"].astype(str)
    
    fig = px.line(
        attend_trend,
        x="Period",
        y="Attendance_Perc",
        title="Average Attendance Over Time",
        markers=True
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Student Performance Explorer")
    
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_id = st.text_input("Search by Student ID")
    with search_col2:
        search_name = st.text_input("Search by Name")
    
    if search_id:
        filtered_df = filtered_df[filtered_df["Student_ID"].str.contains(search_id, case=False)]
    if search_name:
        name_filter = (filtered_df["First_Name"].str.contains(search_name, case=False)) | \
                     (filtered_df["Last_Name"].str.contains(search_name, case=False))
        filtered_df = filtered_df[name_filter]
    
    st.dataframe(
        filtered_df.sort_values("Semester_Average", ascending=False),
        column_order=["Student_ID", "First_Name", "Last_Name", "Department", 
                    "Semester", "Semester_Average", "Attendance_Perc", "At_Risk"],
        hide_index=True,
        height=600,
        use_container_width=True
    )
    
    if not filtered_df.empty:
        selected_id = st.selectbox(
            "Select a student for detailed view",
            filtered_df["Student_ID"].unique()
        )
        
        student_data = filtered_df[filtered_df["Student_ID"] == selected_id]
        student_name = f"{student_data.iloc[0]['First_Name']} {student_data.iloc[0]['Last_Name']}"
        
        st.subheader(f"Academic History for {student_name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                student_data,
                x="Semester",
                y="Semester_Average",
                title="Performance Trend",
                markers=True
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                student_data,
                x="Semester",
                y="Attendance_Perc",
                title="Attendance Trend",
                markers=True,
                color_discrete_sequence=["#00CC96"]
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Subject Performance")
        subject_data = student_data.melt(
            id_vars=["Student_ID", "Semester"],
            value_vars=[col for col in student_data.columns if col in SUBJECTS],
            var_name="Subject",
            value_name="Mark"
        ).dropna()
        
        if not subject_data.empty:
            fig = px.bar(
                subject_data,
                x="Subject",
                y="Mark",
                color="Semester",
                barmode="group",
                title="Marks by Subject",
                facet_col="Semester",
                facet_col_wrap=2
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)