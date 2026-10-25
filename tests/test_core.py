import json, os, shutil, subprocess, sys, tempfile
import numpy as np, pytest
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
from chennai_wind.data import generate_synthetic_daily
from chennai_wind.arma_numpy import arma_forecast
MODEL = os.path.join(ROOT, "demo", "model.json")


def test_synthetic_daily_shape():
    df = generate_synthetic_daily()
    assert len(df) == 1096 and (df.wind_speed > 0).all()


@pytest.mark.skipif(shutil.which("node") is None or not os.path.exists(MODEL), reason="needs node and demo/model.json")
def test_js_and_python_forecasts_match():
    m = json.load(open(MODEL)); v = m["values"]
    cases = [{"hist": v[:n], "h": h} for n, h in ((400, 30), (800, 10), (m["fit_until"], 60))]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cases, f)
    js = json.loads(subprocess.run(["node", os.path.join(ROOT, "demo", "cli.js"), MODEL, f.name],
                                   capture_output=True, text=True, check=True).stdout)
    for c, j in zip(cases, js):
        assert np.allclose(j, arma_forecast(m["const"], m["ar"], m["ma"], c["hist"], c["h"]), atol=1e-6)
