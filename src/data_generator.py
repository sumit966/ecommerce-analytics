"""Generate synthetic e-commerce transaction data."""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


COUNTRIES = ["USA", "UK", "India", "Germany", "Canada", "Australia"]
CATEGORIES = ["Electronics", "Books", "Clothing", "Home", "Sports"]
SEGMENTS = ["New", "Returning", "VIP"]


def generate_transactions(n_customers: int = 2000,
                          n_transactions: int = 50000,
                          days: int = 365,
                          seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    customers = pd.DataFrame({
        "customer_id": [f"C{str(i).zfill(5)}" for i in range(1, n_customers + 1)],
        "country": np.random.choice(COUNTRIES, n_customers, p=[0.35, 0.20, 0.20, 0.10, 0.08, 0.07]),
        "signup_date": [
            datetime(2023, 1, 1) + timedelta(days=int(np.random.randint(0, 365)))
            for _ in range(n_customers)
        ],
    })

    # Customer behavior weights (Pareto-like)
    weights = np.random.pareto(1.5, n_customers) + 1
    weights = weights / weights.sum()

    start_date = datetime(2024, 1, 1)
    customer_ids = np.random.choice(customers["customer_id"], size=n_transactions, p=weights)
    dates = [start_date + timedelta(days=int(np.random.randint(0, days))) for _ in range(n_transactions)]

    unit_prices = {
        "Electronics": (50, 1500),
        "Books": (10, 50),
        "Clothing": (15, 200),
        "Home": (20, 500),
        "Sports": (25, 300),
    }

    categories = np.random.choice(CATEGORIES, n_transactions, p=[0.30, 0.20, 0.25, 0.15, 0.10])

    prices = []
    quantities = []
    for cat in categories:
        lo, hi = unit_prices[cat]
        prices.append(round(np.random.uniform(lo, hi), 2))
        # Pareto-ish quantity distribution
        quantities.append(int(np.random.choice([1, 1, 1, 2, 2, 3, 5], p=[0.35, 0.25, 0.15, 0.10, 0.07, 0.05, 0.03])))

    df = pd.DataFrame({
        "transaction_id": [f"T{str(i).zfill(7)}" for i in range(1, n_transactions + 1)],
        "customer_id": customer_ids,
        "transaction_date": dates,
        "category": categories,
        "quantity": quantities,
        "unit_price": prices,
    })
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)

    # Add customer country/segment via merge
    df = df.merge(customers[["customer_id", "country", "signup_date"]], on="customer_id", how="left")

    # Segment based on customer behavior
    customer_stats = df.groupby("customer_id").agg(
        n_orders=("transaction_id", "count"),
        total_spend=("revenue", "sum"),
    ).reset_index()

    def segment(row):
        if row["n_orders"] >= 20 and row["total_spend"] >= 5000:
            return "VIP"
        if row["n_orders"] >= 5:
            return "Returning"
        return "New"

    customer_stats["segment"] = customer_stats.apply(segment, axis=1)
    df = df.merge(customer_stats[["customer_id", "segment"]], on="customer_id", how="left")

    return df.sort_values("transaction_date").reset_index(drop=True)


def save_dataset(output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)
    df = generate_transactions()
    path = f"{output_dir}/transactions.csv"
    df.to_csv(path, index=False)
    print(f"[OK] Generated {len(df)} transactions -> {path}")
    return df


if __name__ == "__main__":
    df = save_dataset()
    print(f"\nDate range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"Total revenue: ${df['revenue'].sum():,.2f}")
    print(f"Unique customers: {df['customer_id'].nunique()}")
    print(f"\nSample:")
    print(df.head())
