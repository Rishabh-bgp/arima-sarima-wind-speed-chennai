"""Plain-numpy ARMA recursion (same algorithm as demo/arma.js), used for the JS/Python check."""
import numpy as np


def arma_forecast(const, ar, ma, hist, h):
    z = np.asarray(hist, float) - const
    e = np.zeros(len(z))
    for t in range(len(z)):
        f = sum(a * z[t - i - 1] for i, a in enumerate(ar) if t - i - 1 >= 0)
        f += sum(b * e[t - j - 1] for j, b in enumerate(ma) if t - j - 1 >= 0)
        e[t] = z[t] - f
    z, e, out = list(z), list(e), []
    for _ in range(h):
        t = len(z)
        f = sum(a * z[t - i - 1] for i, a in enumerate(ar)) + sum(b * e[t - j - 1] for j, b in enumerate(ma))
        z.append(f); e.append(0.0); out.append(f + const)
    return np.array(out)
