import streamlit as st
from config.sources import get_active_transit_data, get_historical_transit_data
from utils.metrics import calculate_metrics
from components.header_callouts import render_header_callouts
from components.header_timeseries_chart import render_header_timeseries_chart
from components.live_transit_map import render_live_transit_map
from components.weekly_timeseries_trends import render_transit_details
from components.active_vehicles_gauge import render_active_vehicles_gauge
from components.daily_summary_table import render_daily_summary_table
from components.slowest_travel_times import render_slowest_travel_times

st.set_page_config(
    page_title="OC Transpo Active Transit",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.sidebar.markdown("### Navigation")
page = st.sidebar.radio("", ["Dashboard", "About"], label_visibility="collapsed")

if page == "About":
    st.title("About This Report")

    st.markdown("""
    ## Overview
    This dashboard provides real-time and historical analytics for OC Transpo's bus fleet in Ottawa, Canada.

    ## Features
    Currently, I have created the following pages, which are accessible via tabs.
    - ** ✅Live Map**: View current bus locations and speeds across the city
    - ** ✅ Transit Details**: Analyze transit performance with metrics, trends, and historical data
    - ** 🚧 Route Details**: Coming soon - Route-specific performance analysis
    - ** 🚧 Forecasts**: Coming soon - Predictive analytics for transit patterns

    ## Data Sources
    Data is collected from OC Transpo's real-time vehicle position feeds using Python, and stored in a Neon PostgreSQL database. The data is then transformed using dbt with a medallion architecture, and visualized in Streamlit. The end-to-end ELT process is completely automated using GitHub Actions. Real-time data refreshes occur every hour (due to free storage limits & CU-hrs constraints).
    """)

else:
    st.title("OC Transpo Transit Report")

    try:
        df_active = get_active_transit_data()
        df_historical = get_historical_transit_data()

        metrics = calculate_metrics(df_historical)

        left_callouts, right_timeseries = st.columns([1, 4])

        with left_callouts:
            render_header_callouts(metrics)

        with right_timeseries:
            render_header_timeseries_chart(df_historical)

        st.divider()

        tab_live_map, tab_transit_details, tab_route_details, tab_forecasts = st.tabs([
            "Live Map", "Transit Details", "Route Details", "Forecasts"
        ])

        with tab_live_map:
            render_live_transit_map(df_active)

        with tab_transit_details:
            col1, col2 = st.columns(2)
            with col1:
                render_active_vehicles_gauge(df_active)
            with col2:
                render_slowest_travel_times(df_historical)
            st.divider()
            render_transit_details(df_historical)
            st.divider()
            render_daily_summary_table(df_historical)

        with tab_route_details:
            st.info("Coming Soon - Route-specific mapping and comparisons")

        with tab_forecasts:
            st.info("Coming Soon - Predictive forecasts including traffic speed volume forecasting, taking into account time, weather etc.")

    except Exception as e:
        st.error(f"Database connection error: {e}")

st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; padding: 20px;'>Made by <a href='https://www.linkedin.com/in/owenritchie2004/' target='_blank' style='color: #0077b5; text-decoration: none;'>Owen Ritchie</a></div>",
    unsafe_allow_html=True
)
