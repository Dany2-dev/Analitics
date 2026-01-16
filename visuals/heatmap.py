import plotly.express as px

def heatmap_zona_carril(df, titulo):
    fig = px.density_heatmap(
        df,
        x="carril",
        y="zona",
        z="total",
        color_continuous_scale="Reds",
        title=titulo
    )

    fig.update_layout(
        height=450,
        autosize=True,
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Pérdidas",
            thickness=12
        )
    )

    fig.update_xaxes(
        fixedrange=True,
        title=""
    )

    fig.update_yaxes(
        fixedrange=True,
        title=""
    )

    return fig
