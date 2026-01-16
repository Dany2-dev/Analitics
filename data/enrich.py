def normalizar_evento(nombre):
    n = str(nombre).lower()

    if "incompleto" in n or "perdido" in n:
        return "perdida"

    if "completo" in n or "ganado" in n:
        return "ganado"

    return "otro"


def carril(x):
    if x < 33:
        return "Izquierdo"
    if x < 66:
        return "Central"
    return "Derecho"


def zona(y):
    if y < 33:
        return "Defensiva"
    if y < 66:
        return "Creación"
    return "Finalización"


def enrich(df):
    df["evento_raw"] = df["event"]
    df["event"] = df["event"].apply(normalizar_evento)
    df["carril"] = df["x"].apply(carril)
    df["zona"] = df["y"].apply(zona)
    return df
