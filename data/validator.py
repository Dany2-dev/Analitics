REQUIRED = ["player", "event", "x", "y"]

def validate(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
