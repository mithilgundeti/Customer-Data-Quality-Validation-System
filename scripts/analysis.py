import pandas as pd
from datetime import datetime

# ================================================
# LOAD DATA
# ================================================

df = pd.read_csv(
    "data/customer_data.csv",
    sep="\t"
)

df["Marital_Status"] = df["Marital_Status"].replace({
    "YOLO": "Other",
    "Absurd": "Other"
})

print("=" * 60)
print("CUSTOMER DATA ANALYSIS")
print("=" * 60)

# ================================================
# AGE CALCULATION
# ================================================

current_year = datetime.now().year

df["Age"] = current_year - df["Year_Birth"]

# ================================================
# EDUCATION DISTRIBUTION
# ================================================

education_distribution = (
    df["Education"]
    .value_counts()
    .reset_index()
)

education_distribution.columns = [
    "Education",
    "Count"
]

education_distribution.to_csv(
    "outputs/education_distribution.csv",
    index=False
)

# ================================================
# MARITAL STATUS DISTRIBUTION
# ================================================

marital_distribution = (
    df["Marital_Status"]
    .value_counts()
    .reset_index()
)

marital_distribution.columns = [
    "Marital_Status",
    "Count"
]

marital_distribution.to_csv(
    "outputs/marital_status_distribution.csv",
    index=False
)

# ================================================
# AGE GROUP DISTRIBUTION
# ================================================

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 45, 55, 65, 100, 150],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "66-100",
        "100+"
    ]
)

age_distribution = (
    df["Age_Group"]
    .value_counts()
    .reset_index()
)

age_distribution.columns = [
    "Age_Group",
    "Count"
]

age_distribution.to_csv(
    "outputs/age_group_distribution.csv",
    index=False
)

# ================================================
# INCOME DISTRIBUTION
# ================================================

income_summary = pd.DataFrame({
    "Metric": [
        "Average Income",
        "Median Income",
        "Maximum Income",
        "Minimum Income"
    ],
    "Value": [
        df["Income"].mean(),
        df["Income"].median(),
        df["Income"].max(),
        df["Income"].min()
    ]
})

income_summary.to_csv(
    "outputs/income_distribution.csv",
    index=False
)

# ================================================
# CAMPAIGN RESPONSE ANALYSIS
# ================================================

response_analysis = (
    df["Response"]
    .value_counts()
    .reset_index()
)

response_analysis.columns = [
    "Response",
    "Count"
]

response_analysis.to_csv(
    "outputs/campaign_response_analysis.csv",
    index=False
)

# ================================================
# CUSTOMER SPENDING
# ================================================

df["Total_Spending"] = (
    df["MntWines"] +
    df["MntFruits"] +
    df["MntMeatProducts"] +
    df["MntFishProducts"] +
    df["MntSweetProducts"] +
    df["MntGoldProds"]
)

spending_summary = pd.DataFrame({
    "Metric": [
        "Average Spending",
        "Median Spending",
        "Maximum Spending",
        "Minimum Spending"
    ],
    "Value": [
        df["Total_Spending"].mean(),
        df["Total_Spending"].median(),
        df["Total_Spending"].max(),
        df["Total_Spending"].min()
    ]
})

spending_summary.to_csv(
    "outputs/customer_spending_summary.csv",
    index=False
)

# ================================================
# CONSOLE SUMMARY
# ================================================

print("\nANALYSIS COMPLETE")
print("=" * 60)

print(f"Average Income: {df['Income'].mean():,.2f}")
print(f"Average Spending: {df['Total_Spending'].mean():,.2f}")
print(f"Response Rate: {(df['Response'].mean()*100):.2f}%")

# ================================================
# SPENDING BY PRODUCT CATEGORY
# ================================================

product_spending = pd.DataFrame({
    "Category": [
        "Wine",
        "Fruits",
        "Meat",
        "Fish",
        "Sweets",
        "Gold"
    ],
    "Amount": [
        df["MntWines"].sum(),
        df["MntFruits"].sum(),
        df["MntMeatProducts"].sum(),
        df["MntFishProducts"].sum(),
        df["MntSweetProducts"].sum(),
        df["MntGoldProds"].sum()
    ]
})

product_spending.to_csv(
    "outputs/product_spending_analysis.csv",
    index=False
)
# ================================================
# CAMPAIGN ACCEPTANCE ANALYSIS
# ================================================

campaign_analysis = pd.DataFrame({
    "Campaign": [
        "Campaign 1",
        "Campaign 2",
        "Campaign 3",
        "Campaign 4",
        "Campaign 5"
    ],
    "Accepted": [
        df["AcceptedCmp1"].sum(),
        df["AcceptedCmp2"].sum(),
        df["AcceptedCmp3"].sum(),
        df["AcceptedCmp4"].sum(),
        df["AcceptedCmp5"].sum()
    ]
})

campaign_analysis.to_csv(
    "outputs/campaign_acceptance_analysis.csv",
    index=False
)

print("\nOutput files exported successfully.")