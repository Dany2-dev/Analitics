import plotly.graph_objects as go

PITCH_LENGTH = 105
PITCH_WIDTH = 68

def pitch_xg(df):
    # =========================
    # ESCALAR COORDENADAS
    # =========================
    x = df["x"] * (PITCH_LENGTH / 100)
    y = df["y"] * (PITCH_WIDTH / 100)

    fig = go.Figure()

    # =========================
    # CANCHA (COPIA DE pitch_map)
    # =========================
    line_style = dict(color="rgba(255, 255, 255, 0.3)", width=2)

    shapes = [
        dict(type="rect", x0=0, y0=0, x1=105, y1=68,
             line=line_style, fillcolor="rgba(255,255,255,0.02)"),

        dict(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=line_style),

        dict(type="circle", x0=43.15, y0=24.15, x1=61.85, y1=42.85,
             line=line_style),

        dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line=line_style),
        dict(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line=line_style),

        dict(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16, line=line_style),
        dict(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16, line=line_style),
    ]

    # =========================
    # TIROS CON xG (EN VEZ DE EVENTOS)
    # =========================
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(
            size=8+df["xG"] * 80,
            color=df["xG"],
            colorscale="YlOrRd",
            opacity=0.9,
            line=dict(width=1.5, color="rgba(255,255,255,0.6)"),
            showscale=True,
            colorbar=dict(title="xG")
        ),
        hovertemplate="xG: %{marker.color:.2f}<extra></extra>",
        name="Shots (xG)"
    ))

    # =========================
    # LAYOUT FINAL
    # =========================
    fig.update_layout(
        shapes=shapes,

        xaxis=dict(range=[0, 105], visible=False, fixedrange=True),
        yaxis=dict(range=[0, 68], visible=False, fixedrange=True,
                   scaleanchor="x", scaleratio=1),

        height=600,
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    return fig
