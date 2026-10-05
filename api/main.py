"""FastAPI service exposing e-commerce analytics endpoints."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from analyze import (
    compute_kpis, monthly_revenue, revenue_by_category,
    revenue_by_country, top_customers, business_insights
)


app = FastAPI(
    title="E-commerce Analytics API",
    description="Analytics on synthetic e-commerce transactions with RFM segmentation and cohort retention",
    version="1.0.0",
)

STATE = {"df": None, "customer_summary": None, "rfm": None}


def _load():
    if STATE["df"] is None:
        try:
            df = pd.read_csv("data/transactions_clean.csv")
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
            STATE["df"] = df
            STATE["customer_summary"] = pd.read_csv("data/customer_summary.csv")
            STATE["rfm"] = pd.read_csv("data/rfm.csv")
            print("[OK] Loaded analytics data")
        except FileNotFoundError:
            print("[WARN] Data not found. Run the pipeline first.")


@app.on_event("startup")
def startup():
    _load()


@app.get("/")
def root():
    return {"message": "E-commerce Analytics API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy", "data_loaded": STATE["df"] is not None}


@app.get("/kpis")
def kpis():
    if STATE["df"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return compute_kpis(STATE["df"])


@app.get("/revenue/monthly")
def monthly():
    if STATE["df"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return monthly_revenue(STATE["df"]).to_dict(orient="records")


@app.get("/revenue/category")
def category():
    if STATE["df"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return revenue_by_category(STATE["df"]).to_dict(orient="records")


@app.get("/revenue/country")
def country():
    if STATE["df"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return revenue_by_country(STATE["df"]).to_dict(orient="records")


@app.get("/customers/top")
def top(n: int = 10):
    if STATE["customer_summary"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return top_customers(STATE["customer_summary"], n).to_dict(orient="records")


@app.get("/insights")
def insights():
    if STATE["df"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return {"insights": business_insights(STATE["df"], STATE["customer_summary"], STATE["rfm"])}


@app.get("/rfm/segments")
def rfm_segments():
    if STATE["rfm"] is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    grouped = STATE["rfm"].groupby("rfm_segment").agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        total_revenue=("monetary", "sum"),
    ).round(2).reset_index()
    return grouped.to_dict(orient="records")
