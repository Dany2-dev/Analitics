import plotly.graph_objects as go

PITCH_LENGTH = 105
PITCH_WIDTH = 68

def pitch_map(df):
    # =========================
    # ESCALAR COORDENADAS
    # =========================
    x1 = df["x"] * (PITCH_LENGTH / 100)
    y1 = df["y"] * (PITCH_WIDTH / 100)

    fig = go.Figure()

    # =========================
    # CANCHA (SHAPES) - MEJORADOS
    # =========================
    # Usamos un blanco con transparencia para un look minimalista
    line_style = dict(color="rgba(255, 255, 255, 0.3)", width=2)
    
    shapes = [
        # Perímetro externo (Sustituye al rectángulo verde)
        dict(type="rect", x0=0, y0=0, x1=105, y1=68, line=line_style, fillcolor="rgba(255,255,255,0.02)"),

        # Línea de medio campo
        dict(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=line_style),
        
        # Círculo central
        dict(type="circle", x0=43.15, y0=24.15, x1=61.85, y1=42.85, line=line_style),

        # Áreas grandes
        dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line=line_style),
        dict(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line=line_style),

        # Áreas chicas
        dict(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16, line=line_style),
        dict(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16, line=line_style),
    ]

    # =========================
    # EVENTOS (PUNTOS CON GLOW)
    # =========================
    fig.add_trace(go.Scatter(
        x=x1, y=y1,
        mode="markers",
        marker=dict(
            size=12,
            color=df["event"].map({"ganado": "#00CC96", "perdida": "#FF4B4B"}).fillna("#31333F"),
            line=dict(width=1.5, color="rgba(255,255,255,0.5)"),
            opacity=1
        ),
        text=df["player"].astype(str) + "<br>" + df["evento_raw"].astype(str),
        hoverinfo="text",
        name="Eventos"
    ))

    # =========================
    # PASES (LÓGICA DE FLECHAS)
    # =========================
    if {"x2", "y2"}.issubset(df.columns):
        pases = df[df["x2"].notna() & (df["x2"] != 0)]
        for _, r in pases.iterrows():
            fig.add_annotation(
                x=r["x2"] * (PITCH_LENGTH / 100),
                y=r["y2"] * (PITCH_WIDTH / 100),
                ax=r["x"] * (PITCH_LENGTH / 100),
                ay=r["y"] * (PITCH_WIDTH / 100),
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
                arrowcolor="#00CC96" if r["event"] == "ganado" else "#FF4B4B",
                opacity=0.6
            )

    # =========================
    # LAYOUT FINAL (TRANSPARENTE)
    # =========================
    fig.update_layout(
        shapes=shapes,

        xaxis=dict(
            range=[0, 105],
            visible=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[0, 68],
            visible=False,
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1
        ),

        height=600,
        autosize=True,

        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True
    )


    return fig
