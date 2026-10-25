// ARMA(p,q) with mean (statsmodels ARIMA(p,0,q) parameterisation): conditional residuals + static forecast.
(function (root) {
  function forecast(m, hist, h) {
    const mu = m.const, ar = m.ar, ma = m.ma, z = hist.map(v => v - mu), e = new Array(z.length).fill(0);
    for (let t = 0; t < z.length; t++) {
      let f = 0; ar.forEach((a, i) => { if (t - i - 1 >= 0) f += a * z[t - i - 1]; });
      ma.forEach((b, j) => { if (t - j - 1 >= 0) f += b * e[t - j - 1]; });
      e[t] = z[t] - f;
    }
    const zz = z.slice(), ee = e.slice(), out = [];
    for (let k = 0; k < h; k++) {
      const t = zz.length; let f = 0;
      ar.forEach((a, i) => { f += a * zz[t - i - 1]; });
      ma.forEach((b, j) => { f += b * (ee[t - j - 1] || 0); });
      zz.push(f); ee.push(0); out.push(f + mu);
    }
    return out;
  }
  const api = { forecast };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.ARMA = api;
})(typeof self !== "undefined" ? self : this);
