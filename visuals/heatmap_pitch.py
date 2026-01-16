import plotly.graph_objects as go

PITCH_LENGTH = 105
PITCH_WIDTH = 68


def heatmap_pitch(df, title="Heatmap de eventos"):
    # Escalar coordenadas
    x = df["x"] * (PITCH_LENGTH / 100)
    y = df["y"] * (PITCH_WIDTH / 100)

    fig = go.Figure()

    # =========================
    # HEATMAP
    # =========================
    fig.add_trace(go.Histogram2dContour(
        x=x,
        y=y,
        colorscale=[
            [0.0, "rgba(0,0,0,0)"],   # 👈 transparente total
            [0.2, "#FFE066"],
            [0.4, "#FDB833"],
            [0.6, "#F57328"],
            [0.8, "#D7263D"],
            [1.0, "#3A0F2E"]
        ],
        contours=dict(
            showlines=False,
            coloring="fill"
        ),
        ncontours=20,
        showscale=False,
        zmin=1,
        opacity=0.85
    ))



    # =========================
    # CANCHA
    # =========================
    shapes = [
        dict(type="rect", x0=0, y0=0, x1=105, y1=68,
             fillcolor="#2e7d32", layer="below", line_width=0),

        dict(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line_color="white"),
        dict(type="circle", x0=43.15, y0=24.15, x1=61.85, y1=42.85, line_color="white"),

        dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line_color="white"),
        dict(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line_color="white"),
    ]

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

        margin=dict(l=0, r=0, t=30, b=0),
        title=title,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )


    return fig
