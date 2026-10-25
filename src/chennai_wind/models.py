import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, acf, pacf


def adf_test(s):
    r = adfuller(s, autolag="AIC")
    return {"adf_stat": r[0], "p_value": r[1], "lags": r[2], "n_obs": r[3],
            "critical_values": r[4], "stationary_at_5pct": r[1] < 0.05}


def acf_pacf(s, nlags=20):
    return {"acf": acf(s, nlags=nlags).tolist(), "pacf": pacf(s, nlags=nlags).tolist()}


def aic_search_arima(train, max_p=4, max_d=1, max_q=4):
    best = (np.inf, None)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for p in range(max_p + 1):
            for d in range(max_d + 1):
                for q in range(max_q + 1):
                    try:
                        a = ARIMA(train, order=(p, d, q)).fit().aic
                    except Exception:
                        continue
                    if a < best[0]:
                        best = (a, (p, d, q))
    return best[1], best[0]


def fit_forecast(train, n_test, kind, order, seasonal_order=None):
    """Static multi-step forecast over the test period, as in the paper's code
    (model.predict(start=len(train), end=len(train)+len(test)-1))."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if kind == "arima":
            res = ARIMA(train, order=order).fit()
        else:
            res = SARIMAX(train, order=order, seasonal_order=seasonal_order).fit(disp=False)
    fc = res.predict(start=len(train), end=len(train) + n_test - 1)
    return np.asarray(fc), res.aic
