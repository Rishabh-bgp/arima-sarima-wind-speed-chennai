<a href="https://rishabh-bgp.github.io/arima-sarima-wind-speed-chennai/"><img src="docs/img/banner.png" width="100%" alt="Banner: ARIMA and SARIMA Wind Speed Forecasting for Chennai, India, with a red seal stamp and a Bagua trigram"></a>

# ARIMA and SARIMA Wind Speed Forecasting for Chennai, India (Python, statsmodels)

[![Live demo](https://img.shields.io/badge/Live%20demo-GitHub%20Pages-B3121B)](https://rishabh-bgp.github.io/arima-sarima-wind-speed-chennai/) [![CI](https://github.com/Rishabh-bgp/arima-sarima-wind-speed-chennai/actions/workflows/ci.yml/badge.svg)](https://github.com/Rishabh-bgp/arima-sarima-wind-speed-chennai/actions/workflows/ci.yml) [![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-D4A64A)](https://colab.research.google.com/github/Rishabh-bgp/arima-sarima-wind-speed-chennai/blob/main/notebooks/walkthrough.ipynb) [![License: MIT](https://img.shields.io/badge/License-MIT-D4A64A.svg)](LICENSE) ![Python 3.12](https://img.shields.io/badge/python-3.12-111214) ![Data: synthetic](https://img.shields.io/badge/data-synthetic-111214)

**ARIMA and SARIMA for Chennai** is the reference implementation of my paper on ARIMA and SARIMA forecasting of daily wind speed in Chennai, India. The paper proposes modeling **daily wind speed in Chennai** (NIWE met mast, Pallikaranai, 2015–2017) with classical time-series models. It checks stationarity with the ADF test, identifies orders from ACF/PACF and AIC, and compares **ARIMA(3,0,2)** with **SARIMA(0,1,2)(0,1,2,4)** using MSE and RMSE on two test sets. It concludes that ARIMA is more accurate.

<a href="https://rishabh-bgp.github.io/arima-sarima-wind-speed-chennai/"><img src="docs/img/demo.png" width="100%" alt="Screenshot of the Daoist-style live demo for arima-sarima-wind-speed-chennai: red and gold page with the 坎 (Kǎn, water) trigram, a forecast chart on synthetic data compared with persistence, and input sliders"></a>

**Live demo:** https://rishabh-bgp.github.io/arima-sarima-wind-speed-chennai/ (runs entirely in your browser on synthetic data)

**About the demo design.** The page uses a Daoist, Chinese-ink style: crimson, charcoal and navy with gold accents, brush-style headings in the Ma Shan Zheng font, and charts drawn in gold, red and ink. Each repository has its own trigram. This one is **坎 ☵ (Kǎn, Water)**. 坎 (Kǎn) is water: flowing and returning to its level. It fits coastal Chennai and ARIMA's mean-reverting forecasts. The red seal stamp (印) carries the initials RA, the faint taiji and the row of eight Bagua trigrams stand for balance and change, and the vertical motto 上善若水 means "The highest good is like water". The design is purely decorative. Everything is computed by the model shown, on synthetic data.

## What this repository implements

- Daily mean wind speed series (the paper: NIWE met mast, 45 m, Pallikaranai, Chennai, 2015–2017).
- **Augmented Dickey-Fuller** stationarity test (autolag = AIC), **ACF / PACF** values for order identification, and an optional **AIC grid search** for the ARIMA order.
- **ARIMA(3, 0, 2)** and **SARIMA(0, 1, 2)(0, 1, 2, 4)** exactly as reported, fitted with `statsmodels` (`ARIMA`, `SARIMAX`) and forecast statically over the test period, as in the paper's code listing.
- **Two tests**, mirroring the paper's "Test 1 / Test 2": `test1_last30days` (last 30 days held out, as in the code listing) and `test2_80_20` (80:20 split described in the text, done chronologically here).
- Metrics: **MSE and RMSE** (the paper's metrics) plus MAE, MAPE and R2.

## 架構 · Architecture

```
daily series -> ADF test -> ACF/PACF + AIC -> ARIMA(3,0,2) | SARIMA(0,1,2)(0,1,2,4) -> static forecast over the test window -> MSE / RMSE
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python train.py --quick      # fast check (skips the AIC search)
python train.py              # both tests + AIC order search
python -m pytest -q          # tests (incl. JS-vs-Python demo check; needs Node.js)
```

Outputs: `results/metrics.csv`, `results/predictions.csv`, `results/details.json` (ADF, ACF/PACF, AIC-best order).

## Notebook

[![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-D4A64A)](https://colab.research.google.com/github/Rishabh-bgp/arima-sarima-wind-speed-chennai/blob/main/notebooks/walkthrough.ipynb)

[`notebooks/walkthrough.ipynb`](notebooks/walkthrough.ipynb) is a beginner-friendly, self-contained version of the code, with explanations in plain words. It runs in Colab or in Anaconda Jupyter on Windows, macOS or Linux:

1. Load the synthetic daily CSV (local file, else download from GitHub, else generate it).
2. Plot the series.
3. Run the ADF stationarity test.
4. Hold out the last 30 days.
5. Fit ARIMA(3,0,2) and SARIMA(0,1,2)(0,1,2,4).
6. Compare MSE, RMSE, MAE, MAPE and R² with a persistence baseline.
7. Plot the forecasts.

## 數據 · Data

**The original NIWE dataset used in the paper is not publicly available** and is not, and will never be, included here.

- `data/synthetic/synthetic_chennai_daily.csv` is a **SYNTHETIC** daily wind speed series (2015–2017) generated by `scripts/make_synthetic_data.py` (seed 42). It is committed only so the code runs out of the box. It is not measured data.
- `python scripts/fetch_nasa_power.py` downloads a **public** Chennai-like alternative: NASA POWER daily 10 m wind speed (WS10M) at 12.94 N, 80.21 E for 2015–2017 (reanalysis, not the 45 m NIWE mast). It is saved to `data/nasa_power_chennai_daily.csv`.
- To use your own data, put a CSV with columns `date,wind_speed` under `data/` and point `data.csv` in `configs/default.yaml` at it. Everything in `data/` except the committed synthetic CSV is git-ignored.

## 結果 · Results (honest, synthetic data)

These are the real numbers from `python train.py --quick` on the **synthetic** daily CSV. They are **not** the paper's results.

| Test | Model | MSE | RMSE | MAE | MAPE (%) | R² |
|---|---|---:|---:|---:|---:|---:|
| test1_last30days | ARIMA(3, 0, 2) | 0.5228 | 0.7231 | 0.5959 | 18.25 | 0.018 |
| test1_last30days | SARIMA(0, 1, 2)(0, 1, 2, 4) | 0.7176 | 0.8471 | 0.6873 | 23.06 | -0.348 |
| test2_80_20 | ARIMA(3, 0, 2) | 0.9952 | 0.9976 | 0.7885 | 21.38 | -0.448 |
| test2_80_20 | SARIMA(0, 1, 2)(0, 1, 2, 4) | 1.4935 | 1.2221 | 1.0012 | 26.08 | -1.173 |

On this synthetic series ARIMA(3,0,2) beats SARIMA in both tests, as in the paper, but both have R² near or below zero. That means a multi-day static forecast is barely better than predicting the mean. The live demo also shows a **persistence** baseline (every future day = the last observed day). For example, from 2 Sep 2017 over 30 days: ARIMA RMSE 0.606 vs persistence 1.011. The notebook prints persistence for the last-30-days test.

## Reference implementation note

> **Reference implementation.** This repository is a reference implementation of my own paper (cited below), rebuilt in Python and run on synthetic data because the original NIWE met-mast data cannot be redistributed. Results from this code will differ from the numbers published in the paper, and this repository does not claim to reproduce them.

### Assumptions and deviations from the paper

- The paper's text says the 80:20 split was done "randomly"; for time series this would leak future data, so it is done **chronologically** here.
- The paper's listing uses the last 30 days as the test set; it is not stated which of "Test 1 / Test 2" this was, so both splits are provided.
- The paper does not state the two test datasets precisely, nor the 45 m vs 10 m height; NASA POWER is only a stand-in.
- Synthetic generator constants (monsoon peaks, noise) are assumptions.
- Unlike the deep-learning repositories, the models here are not switched to predicting the change from the last reading, because the paper specifies the exact orders. SARIMA(0,1,2)(0,1,2,4) already works on differenced data (d = 1), while ARIMA(3,0,2) models the level.

## Citation

R. Aryan and Manimozhi I, "Modeling and forecasting of wind speed using ARIMA and SARIMA models: An empirical study of Chennai city," *Int. J. Res. Adv. Comput. Sci. Eng. (IJRACSE)*, vol. 12, no. 1, pp. 23–45, May 2026. [Online]. Available: https://gnpublication.org/index.php/cse

## License

MIT License, © 2026 Rishabh Aryan. See [`LICENSE`](LICENSE).

## M.Tech Thesis Work in AI and Data Science, IIIT Bhagalpur

*An Investigation into Advanced Techniques for Wind Speed Forecasting with Applications to Renewable Energy Grid Integration*

This repository is part of my M.Tech thesis work.

**1. Quantum and hybrid quantum ML**

- 08 ☰ [hybrid-vqc-wind-speed-forecasting](https://github.com/Rishabh-bgp/hybrid-vqc-wind-speed-forecasting) · [live demo](https://rishabh-bgp.github.io/hybrid-vqc-wind-speed-forecasting/)
- 10 ☵ [cbma-tn-vqc-wind-green-hydrogen](https://github.com/Rishabh-bgp/cbma-tn-vqc-wind-green-hydrogen) · [live demo](https://rishabh-bgp.github.io/cbma-tn-vqc-wind-green-hydrogen/)
- 12 ☶ [hcq-lstm-clqgwo-wind-forecasting](https://github.com/Rishabh-bgp/hcq-lstm-clqgwo-wind-forecasting) · [live demo](https://rishabh-bgp.github.io/hcq-lstm-clqgwo-wind-forecasting/)

**2. Metaheuristic-optimized hybrids**

- 04 ☷ [geoai-hybrid-ga-pso-anfis-wind-forecasting](https://github.com/Rishabh-bgp/geoai-hybrid-ga-pso-anfis-wind-forecasting) · [live demo](https://rishabh-bgp.github.io/geoai-hybrid-ga-pso-anfis-wind-forecasting/)

**3. Deep learning with attention and gating**

- 01 ☴ [cnn-bilstm-attention-synthetic-scada](https://github.com/Rishabh-bgp/cnn-bilstm-attention-synthetic-scada) · [live demo](https://rishabh-bgp.github.io/cnn-bilstm-attention-synthetic-scada/)
- 02 ☳ [cnn-bilstm-attention-real-scada](https://github.com/Rishabh-bgp/cnn-bilstm-attention-real-scada) · [live demo](https://rishabh-bgp.github.io/cnn-bilstm-attention-real-scada/)
- 03 ☰ [cnn-bilstm-attention-benchmarking-indian-scada](https://github.com/Rishabh-bgp/cnn-bilstm-attention-benchmarking-indian-scada) · [live demo](https://rishabh-bgp.github.io/cnn-bilstm-attention-benchmarking-indian-scada/)
- 05 ☲ [xai-shap-lime-cnn-bilstm-attention-wind](https://github.com/Rishabh-bgp/xai-shap-lime-cnn-bilstm-attention-wind) · [live demo](https://rishabh-bgp.github.io/xai-shap-lime-cnn-bilstm-attention-wind/)
- 06 ☲ [wind-forecasting-mathematical-formulations-validation](https://github.com/Rishabh-bgp/wind-forecasting-mathematical-formulations-validation) · [live demo](https://rishabh-bgp.github.io/wind-forecasting-mathematical-formulations-validation/)
- 09+13 ☵ [wuweidl-daoist-gated-wind-forecasting](https://github.com/Rishabh-bgp/wuweidl-daoist-gated-wind-forecasting) · [live demo](https://rishabh-bgp.github.io/wuweidl-daoist-gated-wind-forecasting/)
- 16 ☴ [rso-net-wind-grid-stabilization](https://github.com/Rishabh-bgp/rso-net-wind-grid-stabilization) · [live demo](https://rishabh-bgp.github.io/rso-net-wind-grid-stabilization/)

**4. IoT, automation and multi-agent systems**

- 14 ☳ [iot-n8n-wind-turbine-predictive-maintenance](https://github.com/Rishabh-bgp/iot-n8n-wind-turbine-predictive-maintenance) · [live demo](https://rishabh-bgp.github.io/iot-n8n-wind-turbine-predictive-maintenance/)
- 15 ☱ [multi-agent-turbine-fleet-chief-of-staff](https://github.com/Rishabh-bgp/multi-agent-turbine-fleet-chief-of-staff) · [live demo](https://rishabh-bgp.github.io/multi-agent-turbine-fleet-chief-of-staff/)

**5. Statistical time-series models**

- 07 ☵ [arima-sarima-wind-speed-chennai](https://github.com/Rishabh-bgp/arima-sarima-wind-speed-chennai) · [live demo](https://rishabh-bgp.github.io/arima-sarima-wind-speed-chennai/)

## Other repositories by Rishabh Aryan

- [100-days-of-python](https://github.com/Rishabh-bgp/100-days-of-python)
- [Agentic-Engineering-Ebook](https://github.com/Rishabh-bgp/Agentic-Engineering-Ebook)
- [Brain-Computer-Interfaces-and-Cognitive-Computing-An-Introduction](https://github.com/Rishabh-bgp/Brain-Computer-Interfaces-and-Cognitive-Computing-An-Introduction)
- [Chronic-Kidney-Disease-Stage-Identification-in-HIV-Infected-Patients-Using-Supervised-ML](https://github.com/Rishabh-bgp/Chronic-Kidney-Disease-Stage-Identification-in-HIV-Infected-Patients-Using-Supervised-ML)
- [IIT-ROPAR-GENAI-FOUNDATIONS](https://github.com/Rishabh-bgp/IIT-ROPAR-GENAI-FOUNDATIONS)
- [Meeting-of-Machines-Consumer-Agents-Seller-Agents-and-Hidden-Fulfilment-Risk-in-Online-Retail](https://github.com/Rishabh-bgp/Meeting-of-Machines-Consumer-Agents-Seller-Agents-and-Hidden-Fulfilment-Risk-in-Online-Retail)
- [NIELIT-DATA-SCIENCE](https://github.com/Rishabh-bgp/NIELIT-DATA-SCIENCE)
- [NIELIT-MACHINE-LEARNING-PROJECTS](https://github.com/Rishabh-bgp/NIELIT-MACHINE-LEARNING-PROJECTS)
- [NIELIT-PYTHON-](https://github.com/Rishabh-bgp/NIELIT-PYTHON-)
- [Predicting-Hot-Events-in-the-Early-Period-through-Bayesian-Model-for-Social-Networks](https://github.com/Rishabh-bgp/Predicting-Hot-Events-in-the-Early-Period-through-Bayesian-Model-for-Social-Networks)
- [beed-ml-study](https://github.com/Rishabh-bgp/beed-ml-study)
- [boston-house-price-prediction](https://github.com/Rishabh-bgp/boston-house-price-prediction)
- [building-a-virtual-cell-in-python](https://github.com/Rishabh-bgp/building-a-virtual-cell-in-python)
- [california-house-price-prediction](https://github.com/Rishabh-bgp/california-house-price-prediction)
- [cobratate](https://github.com/Rishabh-bgp/cobratate)
- [coda-synth](https://github.com/Rishabh-bgp/coda-synth)
- [iris-classification](https://github.com/Rishabh-bgp/iris-classification)
- [kbc-game](https://github.com/Rishabh-bgp/kbc-game)
- [knn-classifier](https://github.com/Rishabh-bgp/knn-classifier)
- [linear-regression-model-](https://github.com/Rishabh-bgp/linear-regression-model-)
- [logistic-regression](https://github.com/Rishabh-bgp/logistic-regression)
- [logistics-website-capstone](https://github.com/Rishabh-bgp/logistics-website-capstone)
- [lovelight-leap](https://github.com/Rishabh-bgp/lovelight-leap)
- [machine-learning-part-1](https://github.com/Rishabh-bgp/machine-learning-part-1)
- [morocco-city-aware-load-forecasting](https://github.com/Rishabh-bgp/morocco-city-aware-load-forecasting)
- [pan-cancer-classification](https://github.com/Rishabh-bgp/pan-cancer-classification)
- [prediction-as-power](https://github.com/Rishabh-bgp/prediction-as-power)
- [real-estate-valuation-taiwan](https://github.com/Rishabh-bgp/real-estate-valuation-taiwan)
- [snakes-and-ladders](https://github.com/Rishabh-bgp/snakes-and-ladders)
- [spam-scan](https://github.com/Rishabh-bgp/spam-scan)
- [vedic-math-hybrid-kt](https://github.com/Rishabh-bgp/vedic-math-hybrid-kt)
- [wind-turbine-power-model](https://github.com/Rishabh-bgp/wind-turbine-power-model)
- [zoo-website-capstone](https://github.com/Rishabh-bgp/zoo-website-capstone)
