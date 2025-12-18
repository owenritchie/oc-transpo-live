import streamlit as st
import plotly.graph_objects as go

def render_active_vehicles_gauge(df_active):
    """Gauge to show percentage of moving vehicles vs active vehicles"""

    # Metrics
    total_vehicles = len(df_active)
    active_vehicles = len(df_active[df_active['speed'] > 0])
    active_percentage = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0

    # Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=active_percentage,
        title={'text': f"Current Moving Vehicles: {active_vehicles} / {total_vehicles}<br>({active_percentage:.1f}%)", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#31d1e9"}
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=80, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
