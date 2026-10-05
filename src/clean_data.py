"""Clean and model the raw transactions into one analysis-ready table."""
import pandas as pd
import numpy as np


def clean_and_model(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Type conversions
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Handle missing values
    df["segment"] = df["segment"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    # Remove duplicates
    df = df.drop_duplicates(subset=["transaction_id"])

    # Remove negative/zero revenue
    df = df[df["revenue"] > 0]

    # Add derived columns
    df["year"] = df["transaction_date"].dt.year
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["transaction_date"].dt.strftime("%b")
    df["day_of_week"] = df["transaction_date"].dt.day_name()
    df["quarter"] = df["transaction_date"].dt.to_period("Q").astype(str)

    return df


def build_customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One row per customer with aggregates."""
    today = df["transaction_date"].max() + pd.Timedelta(days=1)

    summary = df.groupby("customer_id").agg(
        first_purchase=("transaction_date", "min"),
        last_purchase=("transaction_date", "max"),
        total_orders=("transaction_id", "count"),
        total_revenue=("revenue", "sum"),
        avg_order_value=("revenue", "mean"),
        unique_categories=("category", "nunique"),
        country=("country", "first"),
        segment=("segment", "first"),
    ).reset_index()

    summary["recency_days"] = (today - summary["last_purchase"]).dt.days
    summary["tenure_days"] = (summary["last_purchase"] - summary["first_purchase"]).dt.days

    return summary


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """RFM segmentation: Recency, Frequency, Monetary."""
    today = df["transaction_date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_id").agg(
        recency=("transaction_date", lambda x: (today - x.max()).days),
        frequency=("transaction_id", "count"),
        monetary=("revenue", "sum"),
    ).reset_index()

    # Score 1-5
    rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)

    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

    def segment(score):
        if score >= 13:
            return "Champions"
        if score >= 10:
            return "Loyal"
        if score >= 7:
            return "Potential"
        if score >= 5:
            return "At Risk"
        return "Lost"

    rfm["rfm_segment"] = rfm["rfm_score"].apply(segment)
    return rfm


def build_cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly cohort retention matrix."""
    df = df.copy()
    df["order_month"] = df["transaction_date"].dt.to_period("M")

    first_purchase = df.groupby("customer_id")["order_month"].min().rename("cohort_month")
    df = df.merge(first_purchase, on="customer_id")

    df["cohort_index"] = (df["order_month"] - df["cohort_month"]).apply(lambda x: x.n)

    cohort_data = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

    # Retention %
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0) * 100

    return retention.round(2)


if __name__ == "__main__":
    df = pd.read_csv("data/transactions.csv")
    df = clean_and_model(df)

    customer_summary = build_customer_summary(df)
    rfm = build_rfm(df)
    retention = build_cohort_retention(df)

    df.to_csv("data/transactions_clean.csv", index=False)
    customer_summary.to_csv("data/customer_summary.csv", index=False)
    rfm.to_csv("data/rfm.csv", index=False)
    retention.to_csv("data/cohort_retention.csv")

    print(f"[OK] Cleaned {len(df)} transactions")
    print(f"[OK] Customer summary: {len(customer_summary)} customers")
    print(f"[OK] RFM segments:")
    print(rfm["rfm_segment"].value_counts())
