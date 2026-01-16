import streamlit as st

@st.cache_data(show_spinner=False)
def porcentaje_perdidas(df):
    total = len(df)
    if total == 0:
        return 0.0
    return round((df["event"].eq("perdida").sum() / total) * 100, 1)

@st.cache_data(show_spinner=False)
def kpis_por_periodo(df):
    res = {}
    for p in ("1T", "2T"):
        d = df[df["periodo"] == p]
        total = len(d)
        perdidas = d["event"].eq("perdida").sum()

        res[p] = {
            "total": total,
            "perdidas": perdidas,
            "pct_perdidas": round((perdidas / total * 100), 1) if total else 0
        }
    return res
