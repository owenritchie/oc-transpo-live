import streamlit as st
from datetime import timedelta

def render_transit_details(df_historical):
    """Render 7 days of transit trends (timeseries)"""

    st.subheader("Weekly Transit Trends")

    cutoff = df_historical['snapshot_timestamp'].max() - timedelta(days=7)
    chart_data = (
        df_historical
        .loc[df_historical['snapshot_timestamp'] >= cutoff, ['snapshot_timestamp', 'average_moving_speed', 'stopped_vehicles', 'fast_vehicles', 'active_buses']]
        .set_index('snapshot_timestamp')
        .sort_index()
    )

    chart_data['% Stopped'] = (chart_data['stopped_vehicles'] / chart_data['active_buses']) * 100
    chart_data['% Fast'] = (chart_data['fast_vehicles'] / chart_data['active_buses']) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("% Stopped Vehicles", f"{chart_data['% Stopped'].iloc[-1]:.1f}%")
        st.line_chart(chart_data[['% Stopped']], color="#a724f9")

    with col2:
        st.metric("% Fast Vehicles (50km/h+)", f"{chart_data['% Fast'].iloc[-1]:.1f}%")
        st.line_chart(chart_data[['% Fast']], color="#f99624")

    with col3:
        st.metric("Average Moving Speed", f"{chart_data['average_moving_speed'].iloc[-1]:.1f} km/h")
        st.line_chart(chart_data[['average_moving_speed']], color="#31d1e9")
