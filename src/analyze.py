"""Compute analytics KPIs, trends, and segments."""
import pandas as pd
import numpy as np


def compute_kpis(df: pd.DataFrame) -> dict:
    total_revenue = float(df["revenue"].sum())
    total_orders = int(df["transaction_id"].nunique())
    total_customers = int(df["customer_id"].nunique())
    aov = float(total_revenue / total_orders)
    repeat_rate = float(
        (df.groupby("customer_id")["transaction_id"].count() > 1).mean() * 100
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_order_value": round(aov, 2),
        "repeat_purchase_rate_pct": round(repeat_rate, 2),
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month")
        .agg(revenue=("revenue", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values("month")
    )


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")
        .agg(revenue=("revenue", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )


def revenue_by_country(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("country")
        .agg(revenue=("revenue", "sum"), orders=("transaction_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )


def top_customers(customer_summary: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        customer_summary
        .sort_values("total_revenue", ascending=False)
        .head(n)[["customer_id", "country", "segment", "total_orders", "total_revenue", "avg_order_value"]]
    )


def business_insights(df: pd.DataFrame, customer_summary: pd.DataFrame, rfm: pd.DataFrame) -> list:
    insights = []
    kpis = compute_kpis(df)

    insights.append(
        f"Total revenue is ${kpis['total_revenue']:,.2f} from "
        f"{kpis['total_orders']:,} orders by {kpis['total_customers']:,} unique customers."
    )
    insights.append(
        f"Average order value is ${kpis['avg_order_value']:.2f}; "
        f"{kpis['repeat_purchase_rate_pct']}% of customers are repeat buyers."
    )

    top_cat = revenue_by_category(df).iloc[0]
    insights.append(
        f"Top category is {top_cat['category']} with "
        f"${top_cat['revenue']:,.2f} ({top_cat['revenue']/kpis['total_revenue']*100:.1f}% of revenue)."
    )

    top_country = revenue_by_country(df).iloc[0]
    insights.append(
        f"Top market is {top_country['country']} with "
        f"${top_country['revenue']:,.2f} ({top_country['revenue']/kpis['total_revenue']*100:.1f}% of revenue)."
    )

    champions = rfm[rfm["rfm_segment"] == "Champions"]
    insights.append(
        f"{len(champions)} customers are in the 'Champions' RFM segment — "
        f"they generate ${champions['monetary'].sum():,.2f} ({champions['monetary'].sum()/kpis['total_revenue']*100:.1f}% of revenue)."
    )

    at_risk = rfm[rfm["rfm_segment"] == "At Risk"]
    insights.append(
        f"{len(at_risk)} customers are 'At Risk' (high value, low recency) — "
        f"target them with win-back campaigns."
    )

    return insights


if __name__ == "__main__":
    df = pd.read_csv("data/transactions_clean.csv")
    customer_summary = pd.read_csv("data/customer_summary.csv")
    rfm = pd.read_csv("data/rfm.csv")

    print("=== KPIs ===")
    for k, v in compute_kpis(df).items():
        print(f"  {k}: {v}")

    print("\n=== Business Insights ===")
    for i, insight in enumerate(business_insights(df, customer_summary, rfm), 1):
        print(f"  {i}. {insight}")
