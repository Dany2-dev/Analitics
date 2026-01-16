import streamlit as st
import os
from auth import check_auth
from teams import team_selector, load_team_logos

st.set_option("client.toolbarMode", "minimal")

st.set_page_config(layout="wide", page_title="DataStrike | Sports Analytics")

# =========================
# SESSION STATE BASE
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "team" not in st.session_state:
    st.session_state.team = None

if "team_logo" not in st.session_state:
    st.session_state.team_logo = None

if "page" not in st.session_state:
    st.session_state.page = "team_select"

# =========================
# LOGIN (UNA SOLA VEZ)
# =========================
if not st.session_state.authenticated:
    check_auth()
# =========================
# SALTAR SELECTOR SI YA HAY EQUIPO
# =========================
if (
    st.session_state.page == "team_select"
    and st.session_state.team is None
    and "last_team" in st.session_state
):
    logo = f"G8/{st.session_state.last_team}.png"
    if os.path.exists(logo):
        st.session_state.team = st.session_state.last_team
        st.session_state.team_logo = logo
        st.session_state.page = "dashboard"
        st.rerun()

# 🔥 precarga logos (optimización real)
load_team_logos()

# =========================
# SELECTOR DE EQUIPO
# =========================
if st.session_state.page == "team_select":

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0c1220, #05070a 70%);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin-top:40px;">
            <h1 style="font-size:3.5rem; font-weight:900;">
                ⚡ DATASTRIKE
            </h1>
            <p style="color:#9fa3b3; font-size:1.2rem;">
                Selecciona tu equipo
            </p>
        </div>
    """, unsafe_allow_html=True)

    team_selector()
    st.stop()

# =========================
# DASHBOARD (SIGUE TU CÓDIGO)
# =========================

# =========================================
# LEER QUERY PARAMS (CLICK EN ESCUDO)
# =========================================
params = st.query_params

if "team" in params:
    team = params["team"].replace("%20", " ")
    logo = f"G8/{team}.png"

    if os.path.exists(logo):
        st.session_state.team = team
        st.session_state.team_logo = logo
        st.session_state.page = "dashboard"  # 🔥
        st.query_params.clear()
        st.rerun()

# =========================================
# PANTALLA A: SELECCIÓN DE EQUIPO (AISLADA)
# =========================================
if st.session_state.page == "team_select":

    # fondo específico solo para esta pantalla
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0c1220, #05070a 70%);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin-top:40px;">
            <h1 style="font-size:3.5rem; font-weight:900; letter-spacing:-2px;">
                ⚡ DATASTRIKE
            </h1>
            <p style="color:#9fa3b3; font-size:1.2rem; margin-top:10px;">
                Selecciona tu equipo
            </p>
        </div>
    """, unsafe_allow_html=True)

    team_selector()
    st.stop()

# =========================================
# PANTALLA B: DASHBOARD (A PARTIR DE AQUÍ)
# =========================================


# =========================================
# 3. IMPORTS DE ANALÍTICA (DESPUÉS DEL LOGIN)
# =========================================
from data.loader import load_data
from data.validator import validate
from data.enrich import enrich

from analytics.carriles import perdidas_por_carril
from analytics.jugadores import perdidas_por_jugador
from analytics.kpis import porcentaje_perdidas, kpis_por_periodo
from analytics.zonas import perdidas_zona_carril_periodo
from analytics.efectividad import ganados_vs_perdidos
from analytics.pases import pases_progresivos

from visuals.bars import bar_chart
from visuals.pitch import pitch_map
from visuals.heatmap import heatmap_zona_carril
from visuals.compare import barras_ganados_perdidos
from visuals.heatmap_pitch import heatmap_pitch
from visuals.pases_progresivos import barras_pases_progresivos

from utils.pdf_export import export_dashboard_pdf
from analytics.xg_model import xg_model, total_xg

from visuals.gauges import gauge
from visuals.pitch_xg import pitch_xg
from visuals.gauges import animated_gauge

# =========================================
# 4. FUNCIONES DE APOYO
# =========================================
@st.cache_data(show_spinner=False)
def load_and_prepare(file):
    df = load_data(file)
    df.columns = df.columns.str.strip().str.lower()
    validate(df)
    return enrich(df)

def load_css(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 1. CARGA DE CSS
load_css("styles/main.css")

# 2. HEADER PRINCIPAL (Solo uno)
st.markdown("""
    <div class="main-header-wrapper">
        <h1 class="main-title">DataStrike</h1>
        <div class="main-subtitle-container">
            <div class="subtitle-accent"></div>
            <p class="main-subtitle">By Daniel Vidales</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.team is not None:
    st.image(st.session_state.team_logo, width=90)
    st.markdown(f"### {st.session_state.team}")


# 3. SISTEMA DE GUARDADO Y CARGA
if not os.path.exists("storage"):
    os.makedirs("storage")

safe_email = st.session_state.user.replace("@", "_").replace(".", "_")
user_save_path = f"storage/last_data_{safe_email}.csv"

# Usamos una key única para evitar el error de DuplicateElementId
file = st.file_uploader(
    "Cargar CSV / Excel", 
    type=["csv", "xlsx"], 
    key="uploader_principal"
)

if file:
    with open(user_save_path, "wb") as f:
        f.write(file.getbuffer())
    df = load_and_prepare(file)
elif os.path.exists(user_save_path):
    st.info(f"Sesión activa: {st.session_state.user}")
    df = load_and_prepare(user_save_path)
else:
    st.warning("No hay datos cargados. Sube un archivo para comenzar.")
    st.stop()


# =========================
# UI HELPERS
# =========================
def kpi_card(label, value, icon="📊", status="neutral"):
    color_class = {"good": "kpi-green", "bad": "kpi-red", "warn": "kpi-yellow"}.get(status, "")
    st.markdown(f"""
        <div class="kpi-card {color_class}">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="font-size:28px;">{icon}</div>
                <div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def section(title, subtitle=None):
    if not title:
        return  # evita secciones vacías

    sub = f"<div class='section-subtitle'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"""
        <div class="section">
            <div style="border-left:3px solid #00CC96; padding-left:15px;">
                <div class="section-title">{title}</div>
                {sub}
            </div>
    """, unsafe_allow_html=True)


def end_section():
    st.markdown("</div>", unsafe_allow_html=True)

def kpi_delta(label, v1, v2, suffix=""):
    delta = v2 - v1
    st.metric(label, f"{v2:.1f}{suffix}", delta=f"{delta:+.1f}{suffix}")

# =========================
# HEADER PRINCIPAL
# =========================


# =========================
# CARGA DE ARCHIVO
# =========================

if not file:
    st.info("Carga un archivo para comenzar")
    st.stop()

df = load_and_prepare(file)

# =========================
# FILTROS
# =========================
# =========================
# SIDEBAR TÁCTICO (CORREGIDO)
# =========================
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding-bottom:1px;'>
            <h1 style='color:#00CC96; font-size:100px; margin:0;'>⚡</h1>
            <p style='color:#8a8d97; font-size:17px; letter-spacing:2px;'>ANALISTA: {st.session_state.user}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### CONFIGURACIÓN")
    
    # Añadimos keys únicas para evitar duplicados
    mostrar_heatmap = st.checkbox("🛰️ Heatmap en cancha", value=False, key="chk_heatmap")
    mostrar_pases_prog = st.checkbox("📈 Pases Progresivos", key="chk_pases")
    
    st.markdown("---")
    
    # Filtros organizados con Keys Únicas
# ... código anterior (header, carga de archivo, etc.)

with st.sidebar:
    st.markdown("### CONFIGURACIÓN TÁCTICA")
    
    with st.expander("FILTRO TEMPORAL", expanded=True):
        periodos = st.multiselect(
            "Seleccionar Periodo", 
            options=sorted(df["periodo"].unique()), 
            default=sorted(df["periodo"].unique()),
            key="ms_periodo"
        )
    
    with st.expander(" FILTRO DE JUGADORES", expanded=True):
        jugadores = st.multiselect(
            "Seleccionar Jugador", 
            options=sorted(df["player"].unique()),
            key="ms_jugadores"
        )
    
    with st.expander(" ACCIONES", expanded=False):
        eventos = st.multiselect(
            "Resultado", 
            options=sorted(df["event"].unique()),
            key="ms_eventos"
        )
        tipos_evento = st.multiselect(
            "Tipo de acción", 
            options=sorted(df["evento_raw"].dropna().unique()),
            key="ms_tipos"
        )
if st.button("🔄 Cambiar equipo"):
    st.session_state.team = None
    st.session_state.team_logo = None
    st.session_state.page = "team_select"
    st.rerun()


st.markdown("---")

if st.button(" CERRAR SESIÓN", key="btn_logout"):
    st.session_state.authenticated = False
    st.rerun()

# --- NOTA: AQUÍ TERMINA EL SIDEBAR (CUIDA LA INDENTACIÓN) ---

# Aplicación de filtros al DataFrame (Fuera del 'with')
df_ctx = df.copy()
if periodos: 
    df_ctx = df_ctx[df_ctx["periodo"].isin(periodos)]
if jugadores: 
    df_ctx = df_ctx[df_ctx["player"].isin(jugadores)]
if eventos: 
    df_ctx = df_ctx[df_ctx["event"].isin(eventos)]
if tipos_evento: 
    df_ctx = df_ctx[df_ctx["evento_raw"].isin(tipos_evento)]


# =========================
# xG CONTROLADO POR SELECCIÓN DEL USUARIO
# =========================
eventos_xg = {"tiro", "gol", "remate"}

# 👉 detectar selección REAL del usuario sobre evento_raw
hay_xg = bool(tipos_evento) and any(
    e.lower() in eventos_xg for e in tipos_evento
)

# 👉 inicializar siempre
df_xg = df_ctx.iloc[0:0]
xg_total = 0

gauge_container = st.empty()

if hay_xg:
    df_xg = xg_model(df_ctx)
    xg_total = total_xg(df_xg)

animated_gauge(
    container=gauge_container,
    start=0,
    end=xg_total,
    titulo="xG Total",
    max_val=1,
    steps=25,
    delay=0.015
)




# ... continuar con los KPIs y Gráficos usando df_ctx
# KPIs
# =========================
k1, k2, k3, k4 = st.columns(4)
with k1: kpi_card("Eventos", len(df_ctx), "📋", "good")
with k2: kpi_card("Pérdidas", (df_ctx["event"] == "perdida").sum(), "❌", "bad")
with k3: kpi_card("% Pérdidas", f"{porcentaje_perdidas(df_ctx)}%", "📉", "warn")
with k4:
    kpi_card("xG Total", total_xg(df_xg), "⚽", "good")

st.divider()

# =========================
# CARRILES + MAPA
# =========================
section("Distribución y localización", "Pérdidas por carril y eventos")
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_chart(perdidas_por_carril(df_ctx), "carril", "total", "Pérdidas por sector"), 
        use_container_width=True,
         config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
         
    )
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.plotly_chart(heatmap_pitch(df_ctx) if mostrar_heatmap else pitch_map(df_ctx), use_container_width=True, config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    })
end_section()

st.divider()

# =========================
# RANKING JUGADORES
# =========================
section("Rendimiento individual", "Pérdidas por jugador")
st.plotly_chart(
    bar_chart(
        perdidas_por_jugador(df_ctx),
        "Jugador",
        "Pérdidas",
        "Pérdidas por jugador"
    ),
    use_container_width=True,
     config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
)


end_section()

st.divider()

# =========================
# KPIs 1T vs 2T
# =========================
st.subheader("KPIs comparativos: 1T vs 2T")
kpis = kpis_por_periodo(df_ctx)
a, b, c = st.columns(3)
with a: kpi_delta("Eventos", kpis["1T"]["total"], kpis["2T"]["total"])
with b: kpi_delta("Pérdidas", kpis["1T"]["perdidas"], kpis["2T"]["perdidas"])
with c: kpi_delta("% Pérdidas", kpis["1T"]["pct_perdidas"], kpis["2T"]["pct_perdidas"], "%")

st.divider()

# =========================
# EFECTIVIDAD
# =========================
section("Efectividad", "Ganados vs Perdidos por periodo")

g1, g2 = st.columns(2)

with g1:
    st.plotly_chart(
        barras_ganados_perdidos(
            ganados_vs_perdidos(df_ctx, "1T"),
            "Ganados vs Perdidos – 1T"
        ),
        use_container_width=True, config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
    )

with g2:
    st.plotly_chart(
        barras_ganados_perdidos(
            ganados_vs_perdidos(df_ctx, "2T"),
            "Ganados vs Perdidos – 2T"
        ),
        use_container_width=True,
         config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
    )

end_section()

st.divider()

# =========================
# MAPA DE CALOR POR PERIODO
# =========================
section("Mapa de calor de pérdidas", "Comparación espacial 1T vs 2T")

h1, h2 = st.columns(2)

df_1t = perdidas_zona_carril_periodo(df_ctx, "1T")
df_2t = perdidas_zona_carril_periodo(df_ctx, "2T")

with h1:
    st.caption("Primer Tiempo (1T)")
    if not df_1t.empty:
        st.plotly_chart(
            heatmap_zona_carril(df_1t, "Pérdidas 1T"),
            use_container_width=True,
             config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
        )
    else:
        st.info("Sin pérdidas en 1T")

with h2:
    st.caption("Segundo Tiempo (2T)")
    if not df_2t.empty:
        st.plotly_chart(
            heatmap_zona_carril(df_2t, "Pérdidas 2T"),
            use_container_width=True,
             config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": True
    }
        )
    else:
        st.info("Sin pérdidas en 2T")

end_section()

st.divider()


# =========================
# PASES PROGRESIVOS
# =========================
if mostrar_pases_prog:
    st.divider()
    st.subheader("Análisis de pases progresivos")
    df_prog = pases_progresivos(df_ctx)
    if df_prog.empty:
        st.info("No hay pases progresivos con los filtros actuales")
    else:
        st.plotly_chart(barras_pases_progresivos(df_prog), use_container_width=True, config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": False
    })

st.divider()
st.subheader("Exportar reporte")

if st.button("📄 Exportar PDF"):
    export_dashboard_pdf(
        filename="DataStrike_Reporte.pdf",
        title="DataStrike – Reporte de Análisis",
        kpis={
            "Eventos totales": len(df_ctx),
            "Pérdidas": (df_ctx["event"] == "perdida").sum(),
            "% Pérdidas": f"{porcentaje_perdidas(df_ctx)}%"
        },
        figures=[
            bar_chart(
                perdidas_por_carril(df_ctx),
                "carril",
                "total",
                "Pérdidas por carril"
            ),
            pitch_map(df_ctx)
        ]
    )

    with open("DataStrike_Reporte.pdf", "rb") as f:
        st.download_button(
            "⬇️ Descargar PDF",
            f,
            file_name="DataStrike_Reporte.pdf",
            mime="application/pdf"
        )
st.divider()
section("Expected Goals (xG)", "Modelo exponencial por distancia")

if df_xg.empty:
    st.info("No hay tiros en los filtros actuales")
else:
    st.plotly_chart(pitch_xg(df_xg), use_container_width=True, config={
        "displayModeBar": False,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": False
    })

end_section()

