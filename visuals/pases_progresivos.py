import plotly.graph_objects as go

def barras_pases_progresivos(df):
    data = (
        df.groupby("player")
        .size()
        .reset_index(name="total")
        .sort_values("total", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x=data["total"],
        y=data["player"],
        orientation="h",
        marker_color="#00CC96"
    ))

    fig.update_layout(
        title="Pases progresivos por jugador",
        xaxis_title="Cantidad",
        yaxis_title="Jugador",
        height=400,
        margin=dict(l=100, r=20, t=40, b=20)
    )

    return fig
