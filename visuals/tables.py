import plotly.express as px

def heat_table(df):
    return px.density_heatmap(
        df, x="carril", y="zona", z="total", color_continuous_scale="Reds"
    )
