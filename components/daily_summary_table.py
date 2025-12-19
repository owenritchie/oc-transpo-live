import streamlit as st
from datetime import timedelta

def render_daily_summary_table(df_historical):
    """Render daily transit summary table for the last 7 days"""
    st.subheader("Daily Transit Summary (Last 7 Days)")

    agg_type = st.selectbox("Aggregation", ["Mean", "Min", "Max"], index=0, key="daily_summary_agg").lower()

    cutoff = df_historical['snapshot_timestamp'].max() - timedelta(days=7)

    df_calc = df_historical[df_historical['snapshot_timestamp'] >= cutoff].copy()
    df_calc['stopped_pct'] = (df_calc['stopped_vehicles'] / df_calc['active_buses']) * 100
    df_calc['fast_pct'] = (df_calc['fast_vehicles'] / df_calc['active_buses']) * 100

    daily_summary = (
        df_calc
        .set_index('snapshot_timestamp')
        .resample('D')
        .agg({
            'active_buses': agg_type,
            'average_moving_speed': agg_type,
            'stopped_pct': agg_type,
            'fast_pct': agg_type
        })
        .sort_index(ascending=False)
    )

    # rename columns
    daily_summary = daily_summary[['active_buses', 'average_moving_speed', 'stopped_pct', 'fast_pct']].rename(columns={
        'active_buses': 'Active Buses',
        'average_moving_speed': 'Avg Moving Speed (km/h)',
        'stopped_pct': '% Stopped',
        'fast_pct': '% Fast (50km/h+)'
    })

    daily_summary.index = daily_summary.index.strftime('%Y-%m-%d')

    st.dataframe(
        daily_summary.style.background_gradient(cmap='Blues', axis=0, low=0.05, high=0.3).format({
            'Active Buses': '{:.1f}',
            'Avg Moving Speed (km/h)': '{:.1f} km/h',
            '% Stopped': '{:.1f}%',
            '% Fast (50km/h+)': '{:.1f}%'
        }),
        use_container_width=True
    )
