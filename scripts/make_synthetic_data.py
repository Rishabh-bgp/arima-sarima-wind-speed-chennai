"""Regenerate data/synthetic/synthetic_chennai_daily.csv (SYNTHETIC data, not NIWE measurements)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from chennai_wind.data import generate_synthetic_daily
os.makedirs("data/synthetic", exist_ok=True)
generate_synthetic_daily().to_csv("data/synthetic/synthetic_chennai_daily.csv", index=False)
print("wrote data/synthetic/synthetic_chennai_daily.csv")
