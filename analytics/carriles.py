import streamlit as st

@st.cache_data(show_spinner=False)
def perdidas_por_carril(df):
    return (
        df[df["event"] == "perdida"]
        .groupby("carril", as_index=False)
        .size()
        .rename(columns={"size": "total"})
    )
