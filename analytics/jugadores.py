import streamlit as st

@st.cache_data(show_spinner=False)
def perdidas_por_jugador(df, top=10):
    data = (
        df[df["event"] == "perdida"]
        .groupby("player", as_index=False)
        .size()
        .rename(columns={"size": "total"})
    )

    return (
        data.sort_values("total", ascending=False)
        .head(top)
        .rename(columns={"player": "Jugador", "total": "Pérdidas"})
    )
