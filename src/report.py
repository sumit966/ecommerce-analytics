"""Generate charts and a Markdown report."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

from analyze import (
    compute_kpis, monthly_revenue, revenue_by_category,
    revenue_by_country, top_customers, business_insights
)

sns.set_theme(style="darkgrid")


def save_charts(df, customer_summary, rfm, output_dir: str = "reports"):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Monthly revenue trend
    mr = monthly_revenue(df)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(mr["month"], mr["revenue"], marker="o", color="#3b82f6")
    ax.set_title("Monthly Revenue Trend")
    ax.set_xlabel("Month"); ax.set_ylabel("Revenue ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/monthly_revenue.png", dpi=100)
    plt.close()

    # 2. Category revenue
    cat = revenue_by_category(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=cat, x="revenue", y="category", ax=ax, palette="Blues_r")
    ax.set_title("Revenue by Category")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/revenue_by_category.png", dpi=100)
    plt.close()

    # 3. RFM segment distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    seg_counts = rfm["rfm_segment"].value_counts()
    ax.pie(seg_counts.values, labels=seg_counts.index, autopct="%1.1f%%", colors=sns.color_palette("Set2"))
    ax.set_title("RFM Customer Segments")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/rfm_segments.png", dpi=100)
    plt.close()

    # 4. Country revenue
    country = revenue_by_country(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=country, x="revenue", y="country", ax=ax, palette="Greens_r")
    ax.set_title("Revenue by Country")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/revenue_by_country.png", dpi=100)
    plt.close()

    print(f"[OK] Saved charts to {output_dir}/")


def generate_markdown_report(df, customer_summary, rfm, output_path: str = "reports/report.md"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    kpis = compute_kpis(df)
    insights = business_insights(df, customer_summary, rfm)
    top_cust = top_customers(customer_summary, 10)
    cat = revenue_by_category(df)
    country = revenue_by_country(df)

    lines = []
    lines.append("# E-commerce Sales & Customer Analytics Report\n")
    lines.append(f"Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("## Key Performance Indicators\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    for k, v in kpis.items():
        lines.append(f"| {k.replace('_', ' ').title()} | {v} |")

    lines.append("\n## Business Insights\n")
    for i, insight in enumerate(insights, 1):
        lines.append(f"{i}. {insight}\n")

    lines.append("\n## Top 10 Customers\n")
    lines.append(top_cust.to_markdown(index=False))

    lines.append("\n\n## Revenue by Category\n")
    lines.append(cat.to_markdown(index=False))

    lines.append("\n\n## Revenue by Country\n")
    lines.append(country.to_markdown(index=False))

    lines.append("\n\n## RFM Segment Summary\n")
    rfm_summary = rfm.groupby("rfm_segment").agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        total_revenue=("monetary", "sum"),
    ).round(2).reset_index()
    lines.append(rfm_summary.to_markdown(index=False))

    lines.append("\n\n## Charts\n")
    lines.append("![Monthly Revenue](monthly_revenue.png)\n")
    lines.append("![Revenue by Category](revenue_by_category.png)\n")
    lines.append("![RFM Segments](rfm_segments.png)\n")
    lines.append("![Revenue by Country](revenue_by_country.png)\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Saved report to {output_path}")


if __name__ == "__main__":
    df = pd.read_csv("data/transactions_clean.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    customer_summary = pd.read_csv("data/customer_summary.csv")
    rfm = pd.read_csv("data/rfm.csv")

    save_charts(df, customer_summary, rfm)
    generate_markdown_report(df, customer_summary, rfm)
