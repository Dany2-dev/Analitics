import streamlit as st

@st.cache_data(show_spinner=False)
def ganados_vs_perdidos(df, periodo=None):
    d = df if not periodo else df[df["periodo"] == periodo]

    res = (
        d[d["event"].isin(["ganado", "perdida"])]
        .groupby("event", as_index=False)
        .size()
        .rename(columns={"size": "total"})
    )

    total = res["total"].sum()
    res["pct"] = 0 if total == 0 else (res["total"] / total * 100)
    res["color"] = res["event"].map({"ganado": "#00CC96", "perdida": "#FF4B4B"})

    return res
