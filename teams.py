import os
import time
import streamlit as st

TEAMS_DIR = "G8"

# =========================
# CARGA CACHEADA DE LOGOS
# =========================
@st.cache_data(show_spinner=False)
def load_team_logos():
    equipos = sorted(
        f for f in os.listdir(TEAMS_DIR)
        if f.lower().endswith(".png")
    )

    return [
        (equipo.replace(".png", ""), f"{TEAMS_DIR}/{equipo}")
        for equipo in equipos
    ]

# =========================
# SELECTOR DE EQUIPO
# =========================
def team_selector():

    teams = load_team_logos()

    st.markdown("## Selecciona tu equipo")

    cols = st.columns(8)

    # 🔥 Skeletons primero
    for i in range(len(teams)):
        with cols[i % 8]:
            st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)

    # pequeña pausa visual
    time.sleep(0.15)

    cols = st.columns(8)

    for i, (nombre, logo) in enumerate(teams):
        with cols[i % 8]:
            st.markdown(
                f'<div class="team-tile" style="animation-delay:{i*0.04}s">',
                unsafe_allow_html=True
            )

            if st.button("", key=f"team_{nombre}"):
                st.session_state.team = nombre
                st.session_state.team_logo = logo
                st.session_state.page = "dashboard"
                st.session_state.last_team = nombre
                st.rerun()

            st.image(logo, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)
