"""ARIMA vs SARIMA on daily wind speed. Usage: python train.py [--config configs/default.yaml]"""
import os, sys, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import numpy as np, pandas as pd, yaml
from chennai_wind.data import load_series
from chennai_wind.models import adf_test, acf_pacf, aic_search_arima, fit_forecast


def metrics(y, p):
    e = y - p
    mse = float(np.mean(e ** 2))
    m = np.abs(y) >= 0.1
    return {"MSE": mse, "RMSE": mse ** 0.5, "MAE": float(np.mean(np.abs(e))),
            "MAPE": float(np.mean(np.abs(e[m] / y[m])) * 100),
            "R2": float(1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--out", default="results")
    ap.add_argument("--quick", action="store_true", help="skip AIC search (smoke test)")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    s = load_series(cfg)
    print(f"{len(s)} daily observations {s.index[0].date()} .. {s.index[-1].date()}")
    out = {"adf": adf_test(s.values), "acf_pacf": acf_pacf(s.values)}
    print("ADF:", {k: v for k, v in out["adf"].items() if k != "critical_values"})
    ao, so = tuple(cfg["arima_order"]), (tuple(cfg["sarima_order"]), tuple(cfg["sarima_seasonal_order"]))
    rows, preds = [], {}
    for test in cfg["tests"]:
        n = test["last_n_days"] if "last_n_days" in test else int(round(len(s) * (1 - test["train_frac"])))
        tr, te = s.iloc[:-n], s.iloc[-n:]
        if cfg.get("aic_search") and not a.quick:
            o, aic = aic_search_arima(tr.values)
            print(f"[{test['name']}] AIC-best ARIMA order = {o} (AIC {aic:.1f}); paper uses {ao}")
            out.setdefault("aic_best_order", {})[test["name"]] = o
        pa, _ = fit_forecast(tr.values, n, "arima", ao)
        ps, _ = fit_forecast(tr.values, n, "sarima", *so)
        for name, p in (("ARIMA%s" % (ao,), pa), ("SARIMA%s%s" % so, ps)):
            r = {"test": test["name"], "n_test": n, "model": name, **metrics(te.values, p)}
            rows.append(r)
            preds[f"{test['name']}|{name}"] = pd.Series(p, index=te.index)
    df = pd.DataFrame(rows)
    os.makedirs(a.out, exist_ok=True)
    df.to_csv(f"{a.out}/metrics.csv", index=False)
    pd.DataFrame(preds).join(s.rename("actual")).dropna(how="all", subset=list(preds)).to_csv(f"{a.out}/predictions.csv")
    json.dump(out, open(f"{a.out}/details.json", "w"), indent=2, default=str)
    print(df.to_string(index=False))
    for t in df.test.unique():
        d = df[df.test == t].sort_values("RMSE")
        print(f"[{t}] lower RMSE: {d.iloc[0].model}")


if __name__ == "__main__":
    main()
