import pandas as pd

def pass_network(df):
    # Requisitos mínimos
    if not {"player", "player_to", "x", "y", "x2", "y2"}.issubset(df.columns):
        return None, None

    # Solo eventos con destino válido
    pases = df[
        df["x2"].notna() &
        df["y2"].notna() &
        (df["x2"] != 0) &
        (df["y2"] != 0)
    ].copy()

    if pases.empty:
        return None, None

    # Posición media por jugador (origen del pase)
    posiciones = (
        pases.groupby("player")[["x", "y"]]
        .mean()
        .reset_index()
    )

    # Conteo de pases entre jugadores
    enlaces = (
        pases.groupby(["player", "player_to"])
        .size()
        .reset_index(name="total")
    )

    return posiciones, enlaces
