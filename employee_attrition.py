import pandas as pd

# Load dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

print("DATASET LOADED SUCCESSFULLY!")
print("Number of rows and columns:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())
# -------------------------------
# BASIC ATTRITION ANALYSIS
# -------------------------------

print("\n===== BASIC ANALYSIS =====")

# Total employees
total_employees = len(df)

# Employees who left
employees_left = (df["Attrition"] == "Yes").sum()

# Employees who stayed
employees_stayed = (df["Attrition"] == "No").sum()

# Attrition rate
attrition_rate = (employees_left / total_employees) * 100

print("Total Employees:", total_employees)
print("Employees Left:", employees_left)
print("Employees Stayed:", employees_stayed)
print("Attrition Rate:", round(attrition_rate, 2), "%")

# Attrition distribution
print("\nAttrition Distribution:")
print(df["Attrition"].value_counts())
# -------------------------------
# DEPARTMENT-WISE ATTRITION
# -------------------------------

print("\n===== DEPARTMENT-WISE ATTRITION =====")

department_attrition = pd.crosstab(
    df["Department"],
    df["Attrition"],
    normalize="index"
) * 100

print(department_attrition.round(2))
# -------------------------------
# KEY FACTORS AFFECTING ATTRITION
# -------------------------------

print("\n===== OVERTIME VS ATTRITION =====")
overtime_attrition = pd.crosstab(
    df["OverTime"],
    df["Attrition"],
    normalize="index"
) * 100
print(overtime_attrition.round(2))


print("\n===== JOB SATISFACTION VS ATTRITION =====")
satisfaction_attrition = pd.crosstab(
    df["JobSatisfaction"],
    df["Attrition"],
    normalize="index"
) * 100
print(satisfaction_attrition.round(2))


print("\n===== SALARY VS ATTRITION =====")
salary_attrition = df.groupby("Attrition")["MonthlyIncome"].mean()
print(salary_attrition.round(2))
# -------------------------------
# DATA VISUALIZATION
# -------------------------------

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Attrition Count
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="Attrition")
plt.title("Employee Attrition Distribution")
plt.xlabel("Attrition")
plt.ylabel("Number of Employees")



# 2. Department-wise Attrition
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Department", hue="Attrition")
plt.title("Department-wise Employee Attrition")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.xticks(rotation=20)
plt.show()


# 3. Overtime vs Attrition
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="OverTime", hue="Attrition")
plt.title("Overtime vs Employee Attrition")
plt.xlabel("Overtime")
plt.ylabel("Number of Employees")
plt.show()


# 4. Job Satisfaction vs Attrition
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x="JobSatisfaction", hue="Attrition")
plt.title("Job Satisfaction vs Employee Attrition")
plt.xlabel("Job Satisfaction Level")
plt.ylabel("Number of Employees")
plt.show()


# 5. Monthly Income vs Attrition
plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="Attrition", y="MonthlyIncome")
plt.title("Monthly Income vs Employee Attrition")
plt.xlabel("Attrition")
plt.ylabel("Monthly Income")
plt.show()
# -------------------------------
# HR INSIGHTS
# -------------------------------

print("\n===== HR INSIGHTS =====")

# Overtime impact
overtime_rate = pd.crosstab(
    df["OverTime"],
    df["Attrition"],
    normalize="index"
) * 100

print("\nAttrition by Overtime:")
print(overtime_rate["Yes"].round(2))

# Job role attrition
role_rate = pd.crosstab(
    df["JobRole"],
    df["Attrition"],
    normalize="index"
) * 100

print("\nAttrition by Job Role:")
print(role_rate["Yes"].sort_values(ascending=False).round(2))

# Business recommendations
print("\n===== HR RECOMMENDATIONS =====")
print("1. Reduce excessive overtime to improve employee retention.")
print("2. Focus on departments and job roles with high attrition.")
print("3. Improve employee satisfaction and work-life balance.")
print("4. Review compensation for employees with higher attrition risk.")
print("5. Provide better career growth and promotion opportunities.")
# -------------------------------
# FINAL SUMMARY
# -------------------------------

print("\n====================================")
print("     HR EMPLOYEE ATTRITION ANALYTICS")
print("====================================")

print("Total Employees:", total_employees)
print("Employees Left:", employees_left)
print("Employees Stayed:", employees_stayed)
print("Overall Attrition Rate:", round(attrition_rate, 2), "%")

print("\nKey Areas Analysed:")
print("- Department")
print("- Overtime")
print("- Job Satisfaction")
print("- Monthly Income")
print("- Job Role")

print("\nProject Status: COMPLETED")