import time
import plotly.graph_objects as go

def gauge(valor, titulo, max_val=5):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        title={"text": titulo},
        gauge={"axis": {"range": [0, max_val]}}
    ))

def animated_gauge(container, start, end, titulo, max_val=1, steps=30, delay=0.02):
    values = [
        start + (end - start) * i / steps
        for i in range(steps + 1)
    ]

    for i, v in enumerate(values):

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=v,
            number={"valueformat": ".2f"},
            title={"text": titulo},
            gauge={
                "axis": {"range": [0, max_val]},
                "bar": {"color": "#FF4B4B"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0
            }
        ))

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        container.plotly_chart(
            fig,
            use_container_width=True,
            key=f"gauge_frame_{i}"
        )


        time.sleep(delay)

