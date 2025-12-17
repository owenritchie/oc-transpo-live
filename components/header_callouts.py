import streamlit as st

def render_header_callouts(metrics):
    """Render the metrics callout section"""

    st.metric(
        "Active Transit Vehicles",
        value=metrics['active_transit_count'],
        delta=f"{metrics['change_transit_count']} (since {metrics['prev_updated_str']})"
    )
    st.metric(
        "Active Routes Running",
        value=metrics['active_route_count'],
        delta=f"{metrics['change_route_count']} (since {metrics['prev_updated_str']})"
    )
    st.metric(
        "Average Moving Transit Speed",
        value=f"{metrics['moving_average_speed']:.1f} km/h",
        delta=f"{metrics['change_active_speed']:.1f}% (since {metrics['prev_updated_str']})"
    )
    st.caption(f"Last updated: {metrics['last_updated_str']}")
