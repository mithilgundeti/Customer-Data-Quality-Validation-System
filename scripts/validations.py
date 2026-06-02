import pandas as pd
from datetime import datetime

# =================================================
# LOAD DATA
# =================================================

df = pd.read_csv(
    "data/customer_data.csv",
    sep="\t"
)

print("=" * 60)
print("DATA QUALITY VALIDATION SYSTEM")
print("=" * 60)

total_records = len(df)

# =================================================
# 1. MISSING VALUES
# =================================================

missing_income = df["Income"].isnull().sum()

# =================================================
# 2. DUPLICATE CUSTOMER IDS
# =================================================

duplicate_ids = df["ID"].duplicated().sum()

# =================================================
# 3. INVALID BIRTH YEARS
# =================================================

invalid_birth_years = df[
    (df["Year_Birth"] < 1900) |
    (df["Year_Birth"] > datetime.now().year)
].shape[0]

# =================================================
# 4. INVALID INCOME
# =================================================

invalid_income = df[
    df["Income"] < 0
].shape[0]

# =================================================
# 5. DATE VALIDATION
# =================================================

df["Dt_Customer"] = pd.to_datetime(
    df["Dt_Customer"],
    format="%d-%m-%Y"
)

future_dates = df[
    df["Dt_Customer"] > pd.Timestamp.today()
].shape[0]

# =================================================
# 6. NEGATIVE SPENDING VALUES
# =================================================

spending_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

negative_spending = 0

for col in spending_columns:
    negative_spending += (
        df[col] < 0
    ).sum()

# =================================================
# 7. NEGATIVE PURCHASE COUNTS
# =================================================

purchase_columns = [
    "NumDealsPurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

negative_purchases = 0

for col in purchase_columns:
    negative_purchases += (
        df[col] < 0
    ).sum()

# =================================================
# 8. INVALID BINARY FLAGS
# =================================================

binary_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Complain",
    "Response"
]

invalid_binary_values = 0

for col in binary_columns:
    invalid_binary_values += (
        ~df[col].isin([0, 1])
    ).sum()

# =================================================
# 9. AGE OUTLIERS
# =================================================

current_year = datetime.now().year

df["Age"] = current_year - df["Year_Birth"]

age_outliers = df[
    (df["Age"] < 18) |
    (df["Age"] > 100)
].shape[0]

# =================================================
# 10. INCOME OUTLIERS (IQR METHOD)
# =================================================

income_data = df["Income"].dropna()

Q1 = income_data.quantile(0.25)
Q3 = income_data.quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - (1.5 * IQR)
upper_bound = Q3 + (1.5 * IQR)

income_outliers = df[
    (df["Income"] < lower_bound) |
    (df["Income"] > upper_bound)
].shape[0]

# =================================================
# DATA QUALITY SCORE
# =================================================

total_errors = (
    missing_income +
    duplicate_ids +
    invalid_birth_years +
    invalid_income +
    future_dates +
    negative_spending +
    negative_purchases +
    invalid_binary_values +
    age_outliers
)

quality_score = (
    (1 - (total_errors / total_records))
    * 100
)

# =================================================
# RESULTS
# =================================================

print("\nVALIDATION RESULTS")
print("=" * 60)

print(f"Total Records: {total_records}")
print(f"Missing Income: {missing_income}")
print(f"Duplicate Customer IDs: {duplicate_ids}")
print(f"Invalid Birth Years: {invalid_birth_years}")
print(f"Invalid Income Values: {invalid_income}")
print(f"Future Registration Dates: {future_dates}")
print(f"Negative Spending Values: {negative_spending}")
print(f"Negative Purchase Counts: {negative_purchases}")
print(f"Invalid Binary Values: {invalid_binary_values}")
print(f"Age Outliers: {age_outliers}")
print(f"Income Outliers: {income_outliers}")

print("\nDATA QUALITY SCORE")
print("=" * 60)

print(f"Total Validation Errors: {total_errors}")
print(f"Quality Score: {quality_score:.2f}%")

# =================================================
# EXPORT SUMMARY
# =================================================

summary = pd.DataFrame({
    "Validation_Check": [
        "Missing Income",
        "Duplicate IDs",
        "Invalid Birth Years",
        "Invalid Income",
        "Future Dates",
        "Negative Spending",
        "Negative Purchases",
        "Invalid Binary Values",
        "Age Outliers",
        "Income Outliers"
    ],
    "Count": [
        missing_income,
        duplicate_ids,
        invalid_birth_years,
        invalid_income,
        future_dates,
        negative_spending,
        negative_purchases,
        invalid_binary_values,
        age_outliers,
        income_outliers
    ]
})

summary.to_csv(
    "outputs/validation_summary.csv",
    index=False
)

print("\nValidation summary exported successfully.")