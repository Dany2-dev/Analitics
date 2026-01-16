import streamlit as st

@st.cache_data(show_spinner=False)
def pases_progresivos(df, umbral=8):
    if not {"x", "x2"}.issubset(df.columns):
        return df.iloc[0:0]

    pases = df[df["x2"].notna() & (df["x2"] > df["x"] + umbral)].copy()
    pases["ganancia"] = pases["x2"] - pases["x"]

    return pases
