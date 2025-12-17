import streamlit as st
from datetime import timedelta

def render_daily_summary_table(df_historical):
    """Render daily transit summary table for the last 7 days"""
    st.subheader("Daily Transit Summary (Last 7 Days)")

    agg_type = st.selectbox("Aggregation", ["Mean", "Min", "Max"], index=0).lower()

    cutoff = df_historical['snapshot_timestamp'].max() - timedelta(days=7)

    daily_summary = (
        df_historical[df_historical['snapshot_timestamp'] >= cutoff]
        .set_index('snapshot_timestamp')
        .resample('D')
        .agg({
            'active_buses': agg_type,
            'average_moving_speed': agg_type,
            'stopped_vehicles': agg_type,
            'fast_vehicles': agg_type
        })
        .round(1)
        .sort_index(ascending=False)
        .rename(columns={
            'active_buses': 'Active Buses',
            'average_moving_speed': 'Average Moving Speed',
            'stopped_vehicles': 'Stopped Vehicles',
            'fast_vehicles': '# of Fast Vehicles (50km/h+)'
        })
    )

    daily_summary.index = daily_summary.index.strftime('%Y-%m-%d')

    st.dataframe(
        daily_summary.style.background_gradient(cmap='Blues', axis=0, low=0.05, high=0.3),
        use_container_width=True
    )
