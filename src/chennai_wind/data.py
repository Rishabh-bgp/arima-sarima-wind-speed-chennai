import os
import numpy as np
import pandas as pd


def generate_synthetic_daily(start="2015-01-01", end="2017-12-31", seed=42):
    """Synthetic Chennai-like DAILY mean wind speed (m/s), 2015-2017.
    Assumed shape: SW-monsoon maximum (Jun-Aug), NE-monsoon secondary peak
    (Nov-Dec), calmer Mar-Apr / Oct; AR(1) noise. Constants are assumptions."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range(start, end, freq="D")
    doy = idx.dayofyear.values
    seas = 1.3 * np.exp(-((doy - 190) / 45.0) ** 2) + 0.6 * np.exp(-((doy - 340) / 25.0) ** 2)
    noise = np.zeros(len(idx))
    e = rng.normal(0, 0.55, len(idx))
    for t in range(1, len(idx)):
        noise[t] = 0.6 * noise[t - 1] + e[t]
    ws = np.clip(3.0 + seas + noise, 0.2, None)
    return pd.DataFrame({"date": idx, "wind_speed": np.round(ws, 3)})


def load_daily_csv(path, date_col="date", wind_col="wind_speed"):
    df = pd.read_csv(path)
    s = pd.Series(pd.to_numeric(df[wind_col], errors="coerce").values,
                  index=pd.to_datetime(df[date_col]), name="wind_speed").sort_index()
    s = s.asfreq("D")
    return s.interpolate(limit_direction="both")


def load_series(cfg):
    p = cfg["data"].get("csv")
    if p and os.path.exists(p):
        print("Loaded", p)
        return load_daily_csv(p, cfg["data"].get("date_col", "date"), cfg["data"].get("wind_col", "wind_speed"))
    print("[warn] data file not found -> generating synthetic daily series")
    df = generate_synthetic_daily(seed=cfg.get("seed", 42))
    return df.set_index("date")["wind_speed"].asfreq("D")
