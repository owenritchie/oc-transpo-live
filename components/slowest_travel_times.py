import streamlit as st
from datetime import timedelta

def render_slowest_travel_times(df_historical):
    """Render top 5 slowest moving speed times in the last week"""
    st.subheader("Top 5 Slowest Travel Times (Last Week)")

    cutoff = df_historical['snapshot_timestamp'].max() - timedelta(days=7)

    slowest_times = (
        df_historical[df_historical['snapshot_timestamp'] >= cutoff]
        .nsmallest(5, 'average_moving_speed')[['snapshot_timestamp', 'average_moving_speed']]
        .round(1)
        .rename(columns={
            'snapshot_timestamp': 'Time',
            'average_moving_speed': 'Avg Moving Speed (km/h)'
        })
    )

    slowest_times['Time'] = slowest_times['Time'].dt.strftime('%Y-%m-%d %H:%M')

    st.dataframe(
        slowest_times.style.background_gradient(cmap='Reds_r', axis=0, subset=['Avg Moving Speed (km/h)'], low=0.05, high=0.3),
        use_container_width=True,
        hide_index=True
    )
