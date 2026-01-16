def perdidas_por_zona(df):
    return (
        df[df["event"] == "perdida"]
        .groupby(["zona", "carril"])
        .size()
        .reset_index(name="total")
    )
def perdidas_zona_carril_periodo(df, periodo):
    return (
        df[(df["event"] == "perdida") & (df["periodo"] == periodo)]
        .groupby(["zona", "carril"])
        .size()
        .reset_index(name="total")
    )
