"""Fit ARIMA(3,0,2) on the synthetic daily CSV (all but the last 120 days) and export
parameters + data to demo/model.json for the in-browser demo."""
import json, os, sys, warnings
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
warnings.filterwarnings("ignore")
df = pd.read_csv(os.path.join(ROOT, "data", "synthetic", "synthetic_chennai_daily.csv"), parse_dates=["date"])
s = df.set_index("date")["wind_speed"]
fit = ARIMA(s.values[:-120], order=(3, 0, 2)).fit()
p = dict(zip(fit.model.param_names, fit.params))
m = {"const": float(p["const"]), "ar": [float(p[f"ar.L{i}"]) for i in range(1, 4)], "ma": [float(p[f"ma.L{i}"]) for i in range(1, 3)],
     "dates": [d.strftime("%Y-%m-%d") for d in s.index], "values": s.round(3).tolist(), "fit_until": len(s) - 120,
     "note": "ARIMA(3,0,2) fitted on SYNTHETIC daily data (2015-2017). Not NIWE data; not the paper's results."}
os.makedirs(os.path.join(ROOT, "demo"), exist_ok=True)
json.dump(m, open(os.path.join(ROOT, "demo", "model.json"), "w"))
print({k: m[k] for k in ("const", "ar", "ma")})
