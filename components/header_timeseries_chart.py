import streamlit as st
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def render_header_timeseries_chart(df_historical):
    """Render a 48-hour transit trends timseries"""

    st.subheader("48 Hour Transit Trends")

    cutoff = df_historical['snapshot_timestamp'].max() - timedelta(days=3)
    chart_data = (
        df_historical
        .loc[df_historical['snapshot_timestamp'] >= cutoff, ['snapshot_timestamp', 'average_moving_speed', 'stopped_vehicles', 'active_buses']]
        .set_index('snapshot_timestamp')
        .sort_index()
    )

    chart_data['% of Active Vehicles Moving'] = ((chart_data['active_buses'] - chart_data['stopped_vehicles']) / chart_data['active_buses']) * 100

    chart_data = chart_data.rename(columns={
        'average_moving_speed': 'Moving Speed (km/h)'
    })

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=chart_data.index, y=chart_data['Moving Speed (km/h)'],
                  name='Average Moving Speed (km/h)', mode='lines', line=dict(color="#31d1e9", width=2)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=chart_data.index, y=chart_data['% of Active Vehicles Moving'],
                  name='% of Active Vehicles Moving', mode='lines', line=dict(color="#a724f9", width=2)),
        secondary_y=True,
    )

    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    fig.update_yaxes(ticksuffix=" km/h", secondary_y=False)
    fig.update_yaxes(ticksuffix="%", range=[0, 100], secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
