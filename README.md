# Student-Data-Analysis
Track grades, attendance, and engagement to flag at-risk students early. Interactive charts and filters help educators identify struggling learners and take timely action. Visual trends reveal patterns, while alerts highlight critical risks. Optimized for quick, data-driven interventions.

Overview
The Student Performance Analytics Dashboard is a data-driven web application designed to help educators, academic advisors, and administrators identify at-risk students early by analyzing key academic metrics. Built with Python and Streamlit, this dashboard provides actionable insights through interactive visualizations, automated risk detection, and customizable filters.

Key Objectives
✅ Early Intervention – Detect struggling students before they fall behind
✅ Performance Tracking – Monitor grades, attendance, and engagement trends
✅ Data-Backed Decisions – Support academic interventions with real-time analytics
✅ User-Friendly Interface – Accessible to both technical and non-technical users

Features
1. At-Risk Student Detection
Automated Alerts: Flags students with declining grades, low attendance, or poor engagement

Risk Scoring: Calculates risk probability based on customizable thresholds

Priority Ranking: Highlights students needing immediate attention

2. Interactive Visualizations
📊 Grade Distribution – Histograms & box plots showing class performance
📈 Trend Analysis – Tracks student progress over time
🔥 Heatmaps – Correlates attendance, grades, and LMS logins
📉 Comparative Charts – Top vs. struggling student benchmarks

3. Customizable Filters
Department/Semester – Drill down by academic programs

Risk Level – Filter by low/medium/high-risk students

Time Period – Analyze weekly, monthly, or term-wise trends

4. Exportable Reports
Generate PDF/Excel reports for faculty meetings

Save visualizations for presentations

Export student lists for targeted interventions

Technical Details
Data Requirements
The dashboard accepts CSV/Excel files with:

Student IDs, Names

Course Grades (e.g., Midterm, Final Exam)

Attendance Records (% or session counts)

LMS Login Frequency (optional)

Tech Stack
Backend: Python (Pandas, NumPy, Scikit-learn for risk modeling)

Frontend: Streamlit (Interactive UI)

Visualization: Plotly, Matplotlib, Seaborn

Deployment: Docker, Streamlit Cloud (or on-premise servers)

