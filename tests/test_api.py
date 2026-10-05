"""Tests for E-commerce Analytics API."""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()


def test_kpis_when_loaded():
    r = client.get("/kpis")
    if r.status_code == 503:
        return  # data not generated
    assert r.status_code == 200
    body = r.json()
    assert "total_revenue" in body


def test_monthly_revenue():
    r = client.get("/revenue/monthly")
    if r.status_code == 503:
        return
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_insights():
    r = client.get("/insights")
    if r.status_code == 503:
        return
    assert r.status_code == 200
    assert "insights" in r.json()
