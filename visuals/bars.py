import plotly.express as px

def bar_chart(df, x, y, title):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        template="plotly_dark"
    )

    fig.update_traces(
        marker_color="#FF4B4B" if "pérdidas" in title.lower() else "#00CC96",
        marker_line_width=0,
        opacity=0.9,
        hovertemplate="<b>%{x}</b><br>%{y} eventos<extra></extra>"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_size=18,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        bargap=0.3
    )

    return fig
