"""Download a PUBLIC Chennai-like daily wind series from NASA POWER (WS10M,
10 m wind speed, m/s) near NIWE Pallikaranai (12.94 N, 80.21 E), 2015-2017.
This is reanalysis data, not the NIWE 45 m mast data used in the paper.
Output: data/nasa_power_chennai_daily.csv (git-ignored)."""
import os, json, urllib.request
import pandas as pd

url = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=WS10M"
       "&community=RE&longitude=80.21&latitude=12.94&start=20150101&end=20171231&format=JSON")
d = json.load(urllib.request.urlopen(url, timeout=60))["properties"]["parameter"]["WS10M"]
df = pd.DataFrame({"date": pd.to_datetime(list(d.keys())), "wind_speed": list(d.values())})
df.loc[df.wind_speed < 0, "wind_speed"] = None  # -999 = missing
os.makedirs("data", exist_ok=True)
df.to_csv("data/nasa_power_chennai_daily.csv", index=False)
print("wrote data/nasa_power_chennai_daily.csv; set data.csv in configs/default.yaml to use it")
