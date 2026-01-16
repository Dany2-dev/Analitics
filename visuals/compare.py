import plotly.express as px

def barras_ganados_perdidos(df, title):
    fig = px.bar(
        df, x="event", y="total", color="color",
        text=df["pct"].apply(lambda x: f"{x:.1f}%"), # Usamos 'pct' de forma segura
        color_discrete_map="identity",
        title=title,
        template="plotly_dark"
    )
    
    fig.update_traces(
        textposition='outside',
        marker_line_width=0,
        width=0.4 # Barras más delgadas y elegantes
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="", yaxis_title="Total",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig