import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

st.set_page_config(
    page_title="HR Employee Attrition Analytics",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    h1 {
        text-align: center;
    }

    .stMetric {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
# Load trained ML model
model = joblib.load("attrition_model.pkl")

st.title("📊 HR Employee Attrition Analytics")
st.caption("Employee Attrition Analysis & HR Insights Dashboard")
st.divider()

# ---------------- FILTERS ----------------

st.sidebar.header("🔎 Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

overtime = st.sidebar.selectbox(
    "OverTime",
    ["All"] + sorted(df["OverTime"].unique().tolist())
)

filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]

if gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender]

if overtime != "All":
    filtered_df = filtered_df[filtered_df["OverTime"] == overtime]

# ---------------- KPI CARDS ----------------

total = len(filtered_df)
left = (filtered_df["Attrition"] == "Yes").sum()
stayed = (filtered_df["Attrition"] == "No").sum()

rate = (left / total * 100) if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Total Employees", total)
c2.metric("❌ Employees Left", left)
c3.metric("✅ Employees Stayed", stayed)
c4.metric("📈 Attrition Rate", f"{rate:.2f}%")

st.divider()

# ---------------- ATTRITION ----------------

c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Attrition Distribution")

    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x="Attrition", ax=ax)
    ax.set_xlabel("Attrition")
    ax.set_ylabel("Employees")
    st.pyplot(fig)

with c2:
    st.subheader("🏢 Department-wise Attrition")

    fig, ax = plt.subplots()
    sns.countplot(
        data=filtered_df,
        x="Department",
        hue="Attrition",
        ax=ax
    )
    ax.set_xlabel("Department")
    ax.set_ylabel("Employees")
    st.pyplot(fig)

# ---------------- OVERTIME + SATISFACTION ----------------

c1, c2 = st.columns(2)

with c1:
    st.subheader("⏰ Overtime vs Attrition")

    fig, ax = plt.subplots()
    sns.countplot(
        data=filtered_df,
        x="OverTime",
        hue="Attrition",
        ax=ax
    )
    ax.set_xlabel("Overtime")
    ax.set_ylabel("Employees")
    st.pyplot(fig)

with c2:
    st.subheader("⭐ Job Satisfaction vs Attrition")

    fig, ax = plt.subplots()
    sns.countplot(
        data=filtered_df,
        x="JobSatisfaction",
        hue="Attrition",
        ax=ax
    )
    ax.set_xlabel("Job Satisfaction")
    ax.set_ylabel("Employees")
    st.pyplot(fig)

# ---------------- JOB ROLE + SALARY ----------------

c1, c2 = st.columns(2)

with c1:
    st.subheader("👔 Job Role-wise Attrition")

    role_data = pd.crosstab(
        filtered_df["JobRole"],
        filtered_df["Attrition"]
    )

    st.bar_chart(role_data)

with c2:
    st.subheader("💰 Monthly Income vs Attrition")

    fig, ax = plt.subplots()
    sns.boxplot(
        data=filtered_df,
        x="Attrition",
        y="MonthlyIncome",
        ax=ax
    )
    ax.set_xlabel("Attrition")
    ax.set_ylabel("Monthly Income")
    st.pyplot(fig)

# ---------------- HR RECOMMENDATIONS ----------------

st.divider()

st.subheader("💡 HR Recommendations")

st.info("""
• Reduce excessive overtime and improve work-life balance.

• Identify departments and job roles with higher attrition.

• Improve employee satisfaction and engagement.

• Review compensation and salary levels.

• Provide better career growth and promotion opportunities.

• Regularly monitor employee attrition trends.
""")



# ---------------- KEY INSIGHTS ----------------

st.divider()

st.subheader("📌 Key Insights")

overall_attrition = (df["Attrition"] == "Yes").mean() * 100

overtime_attrition = (
    df[df["OverTime"] == "Yes"]["Attrition"]
    .eq("Yes")
    .mean() * 100
)

st.write(f"• Overall employee attrition rate is **{overall_attrition:.2f}%**.")

st.write(
    f"• Employees working overtime have an attrition rate of "
    f"**{overtime_attrition:.2f}%**."
)

st.write(
    "• HR should focus on employee satisfaction, workload, "
    "compensation and career growth to reduce employee attrition."
)

st.divider()

st.subheader("🎯 Business Objective")

st.write(
    "The objective of this project is to analyze employee attrition "
    "patterns and identify important factors that may contribute "
    "to employee turnover."
)


# ---------------- WHAT-IF ANALYSIS ----------------

st.divider()

st.subheader("🔮 What-If Employee Attrition Analysis")
st.write("Change employee conditions to explore the historical attrition rate for similar employees.")

col1, col2 = st.columns(2)

with col1:
    whatif_overtime = st.selectbox(
        "Overtime",
        ["All", "Yes", "No"],
        key="whatif_overtime"
    )

    whatif_satisfaction = st.slider(
        "Job Satisfaction",
        min_value=1,
        max_value=4,
        value=3,
        key="whatif_satisfaction"
    )

with col2:
    whatif_joblevel = st.slider(
        "Job Level",
        min_value=1,
        max_value=5,
        value=2,
        key="whatif_joblevel"
    )

    whatif_years = st.slider(
        "Years at Company",
        min_value=0,
        max_value=int(df["YearsAtCompany"].max()),
        value=3,
        key="whatif_years"
    )

whatif_df = df.copy()

if whatif_overtime != "All":
    whatif_df = whatif_df[whatif_df["OverTime"] == whatif_overtime]

whatif_df = whatif_df[
    (whatif_df["JobSatisfaction"] == whatif_satisfaction) &
    (whatif_df["JobLevel"] == whatif_joblevel) &
    (whatif_df["YearsAtCompany"] == whatif_years)
]

if len(whatif_df) > 0:
    whatif_rate = (whatif_df["Attrition"] == "Yes").mean() * 100

    st.metric(
        "Historical Attrition Rate for Selected Conditions",
        f"{whatif_rate:.2f}%"
    )

    st.write(f"Employees matching these conditions: **{len(whatif_df)}**")

else:
    st.warning("No employees found with these exact conditions.")
    # ---------------- FUTURE ML PREDICTION ----------------

st.divider()

st.subheader("🤖 Future Employee Attrition Prediction")

st.write(
    "Explore the predicted attrition risk by changing employee conditions."
)

col1, col2 = st.columns(2)

with col1:

    prediction_overtime = st.selectbox(
        "⏰ Overtime",
        ["Yes", "No"],
        key="prediction_overtime"
    )

    prediction_satisfaction = st.slider(
        "⭐ Job Satisfaction",
        min_value=1,
        max_value=4,
        value=3,
        key="prediction_satisfaction"
    )

with col2:

    prediction_joblevel = st.slider(
        "📈 Job Level",
        min_value=1,
        max_value=5,
        value=2,
        key="prediction_joblevel"
    )

    prediction_years = st.slider(
        "🏢 Years at Company",
        min_value=0,
        max_value=int(df["YearsAtCompany"].max()),
        value=3,
        key="prediction_years"
    )


# Create a baseline employee using the most common value
# for every column
prediction_data = (
    df.drop(columns=["Attrition"])
    .mode()
    .iloc[0]
    .to_dict()
)

# Change selected conditions
prediction_data["OverTime"] = prediction_overtime
prediction_data["JobSatisfaction"] = prediction_satisfaction
prediction_data["JobLevel"] = prediction_joblevel
prediction_data["YearsAtCompany"] = prediction_years


# Convert into DataFrame
prediction_df = pd.DataFrame([prediction_data])


# Make prediction
prediction = model.predict(prediction_df)[0]

prediction_probability = model.predict_proba(prediction_df)[0]

# Find probability of Yes
yes_index = list(model.classes_).index("Yes")

attrition_probability = prediction_probability[yes_index] * 100


# Display result
st.metric(
    "🔮 Predicted Attrition Probability",
    f"{attrition_probability:.2f}%"
)


if attrition_probability >= 50:

    st.error(
        "🚨 High Attrition Risk"
    )

elif attrition_probability >= 25:

    st.warning(
        "⚠️ Moderate Attrition Risk"
    )

else:

    st.success(
        "✅ Low Attrition Risk"
    )


st.write(
    f"Model Prediction: **{prediction}**"
)

st.caption(
    "💡 This result represents the model's estimated attrition risk "
    "for the selected employee conditions."
)
# ---------------- HIGH-RISK EMPLOYEE / SEGMENT ANALYSIS ----------------

st.divider()

st.subheader("🚨 High-Risk Employee / Segment Analysis")

st.write(
    "Identify employee groups with higher historical attrition rates."
)

# Create a copy
risk_df = df.copy()

# Convert Attrition into 0/1
risk_df["Attrition_Flag"] = (
    risk_df["Attrition"] == "Yes"
).astype(int)


# ---------- OVERTIME RISK ----------

st.markdown("### ⏰ Attrition Risk by Overtime")

overtime_risk = (
    risk_df.groupby("OverTime")["Attrition_Flag"]
    .agg(["mean", "count"])
    .reset_index()
)

overtime_risk["Attrition Rate"] = (
    overtime_risk["mean"] * 100
).round(2)

overtime_risk = overtime_risk.drop(columns=["mean"])

st.dataframe(
    overtime_risk,
    use_container_width=True
)


# ---------- DEPARTMENT RISK ----------

st.markdown("### 🏢 Attrition Risk by Department")

department_risk = (
    risk_df.groupby("Department")["Attrition_Flag"]
    .agg(["mean", "count"])
    .reset_index()
)

department_risk["Attrition Rate"] = (
    department_risk["mean"] * 100
).round(2)

department_risk = department_risk.drop(columns=["mean"])

st.dataframe(
    department_risk.sort_values(
        "Attrition Rate",
        ascending=False
    ),
    use_container_width=True
)


# ---------- JOB ROLE RISK ----------

st.markdown("### 💼 Attrition Risk by Job Role")

jobrole_risk = (
    risk_df.groupby("JobRole")["Attrition_Flag"]
    .agg(["mean", "count"])
    .reset_index()
)

jobrole_risk["Attrition Rate"] = (
    jobrole_risk["mean"] * 100
).round(2)

jobrole_risk = jobrole_risk.drop(columns=["mean"])

st.dataframe(
    jobrole_risk.sort_values(
        "Attrition Rate",
        ascending=False
    ),
    use_container_width=True
)


# ---------- JOB SATISFACTION RISK ----------

st.markdown("### ⭐ Attrition Risk by Job Satisfaction")

satisfaction_risk = (
    risk_df.groupby("JobSatisfaction")["Attrition_Flag"]
    .agg(["mean", "count"])
    .reset_index()
)

satisfaction_risk["Attrition Rate"] = (
    satisfaction_risk["mean"] * 100
).round(2)

satisfaction_risk = satisfaction_risk.drop(columns=["mean"])

st.dataframe(
    satisfaction_risk.sort_values(
        "Attrition Rate",
        ascending=False
    ),
    use_container_width=True
)


# ---------- HIGH-RISK SEGMENT ----------

st.markdown("### 🔴 High-Risk Segments")

# Combine important employee conditions
segment_risk = (
    risk_df.groupby(
        ["OverTime", "JobSatisfaction", "JobLevel"]
    )["Attrition_Flag"]
    .agg(["mean", "count"])
    .reset_index()
)

segment_risk["Attrition Rate"] = (
    segment_risk["mean"] * 100
).round(2)

segment_risk = segment_risk.drop(columns=["mean"])

# Keep only segments with at least 10 employees
segment_risk = segment_risk[
    segment_risk["count"] >= 10
]

segment_risk = segment_risk.sort_values(
    "Attrition Rate",
    ascending=False
)

st.dataframe(
    segment_risk.head(10),
    use_container_width=True
)

st.caption(
    "💡 High-risk segments are identified using historical attrition patterns. "
    "Segments with fewer than 10 employees are excluded to avoid unreliable results."
)

