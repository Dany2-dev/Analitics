import numpy as np

GOAL_X = 105
GOAL_Y = 34

def euclidean_distance(df):
    return np.sqrt((df["x"] - GOAL_X) ** 2 + (df["y"] - GOAL_Y) ** 2)

def compute_xg(df, a=0.45, b=0.02, k=18):
    d = euclidean_distance(df)
    return np.exp(-d / k) * a + b

def xg_model(df, a=0.45, b=0.02, k=18):
    shots = df[
        df["evento_raw"]
        .str.contains("tiro|gol|remate", case=False, na=False)
    ].copy()

    if shots.empty:
        return shots

    shots["distance"] = euclidean_distance(shots)
    shots["xG"] = compute_xg(shots, a, b, k)
    shots["xG"] = shots["xG"].clip(0, 1)

    return shots

def total_xg(df):
    if df.empty or "xG" not in df.columns:
        return 0.0
    return round(df["xG"].sum(), 2)
