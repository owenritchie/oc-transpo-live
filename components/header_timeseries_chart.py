import streamlit as st
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def render_header_timeseries_chart(df_historical,df_weather):
    """Render a 48-hour transit trends timseries"""

    col_title, col_checkbox = st.columns([4, 1])
    with col_title:
        st.subheader("72 Hour Transit Trends")
    with col_checkbox:
        show_weather = st.checkbox("Show Weather", value=False, key="weather_toggle")

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

    # prep weather data
    weather_data = df_weather[df_weather['snapshot_timestamp'] >= cutoff].copy()
    weather_data = weather_data.sort_values('snapshot_timestamp')

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


    if show_weather:
        # color mapping for weather conditions
        weather_colors = {
            'Clear sky': 'rgba(255, 255, 150, 0.3)',
            'Partly cloudy': 'rgba(200, 200, 200, 0.3)',
            'Fog': 'rgba(150, 150, 150, 0.4)',
            'Drizzle': 'rgba(173, 216, 230, 0.3)',
            'Rain': 'rgba(100, 149, 237, 0.4)',
            'Freezing Rain': 'rgba(147, 112, 219, 0.4)',
            'Snow': 'rgba(240, 248, 255, 0.5)',
            'Thunderstorm': 'rgba(75, 0, 130, 0.4)'
        }

        added_to_legend = set()

        for i in range(len(weather_data) - 1):
            start_time = weather_data['snapshot_timestamp'].iloc[i]
            end_time = weather_data['snapshot_timestamp'].iloc[i + 1]
            precipitation = weather_data['precipitation_mm'].iloc[i]
            weather_desc = weather_data['weather_description'].iloc[i]

            if precipitation > 0:
                color = weather_colors.get(weather_desc, 'rgba(173, 216, 230, 0.3)')
                show_in_legend = weather_desc not in added_to_legend

                fig.add_vrect(
                    x0=start_time, x1=end_time,
                    fillcolor=color,
                    layer="below", line_width=0
                )

                if show_in_legend:
                    fig.add_trace(
                        go.Scatter(
                            x=[None], y=[None],
                            mode='markers',
                            marker=dict(size=10, color=color, symbol='square'),
                            name=weather_desc,
                            showlegend=True
                        ),
                        secondary_y=False
                    )
                    added_to_legend.add(weather_desc)

    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    fig.update_yaxes(ticksuffix=" km/h", secondary_y=False)
    fig.update_yaxes(ticksuffix="%", range=[0, 100], secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
