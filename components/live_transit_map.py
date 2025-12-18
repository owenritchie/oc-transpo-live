import streamlit as st
import plotly.graph_objects as go

def render_live_transit_map(df_active, df_routes=None):
    """Render live vehicle locations on a map"""

    left_map, right_search = st.columns([4, 1])

    df_map = df_active.dropna(subset=['latitude', 'longitude'])

    with right_search:
        if len(df_map) > 0:
            st.subheader("Filters")

            df_map['route_display'] = df_map['route_id'].astype(str).str.replace('-0', '')
            unique_routes = sorted(
                df_map['route_display'].unique(),
                key=lambda x: (int(x) if x.isdigit() else float('inf'), x)
            )
            selected_route = st.selectbox("Select Route", ['All Routes'] + unique_routes, index=0, key="route_select")
            df_map_filtered = df_map if selected_route == 'All Routes' else df_map[df_map['route_display'] == selected_route]

            all_vehicles = ['All Vehicles'] + df_map_filtered['vehicle_id'].astype(str).tolist()
            selected_vehicle = st.selectbox("Select Vehicle", all_vehicles, index=0, key="vehicle_select")

            show_stops = st.checkbox("Show Route Stops", value=False, key="show_route_stops")

            st.divider()

            df_metrics = df_map_filtered if selected_vehicle == 'All Vehicles' else df_map_filtered[df_map_filtered['vehicle_id'].astype(str) == selected_vehicle]

            total_vehicles = len(df_metrics)
            stopped_count = len(df_metrics[df_metrics['speed'] == 0])
            moving_count = total_vehicles - stopped_count
            avg_moving_speed = df_metrics[df_metrics['speed'] > 0]['speed'].mean() if moving_count > 0 else 0

            st.metric("Total Vehicles", total_vehicles)
            st.metric("Moving Vehicles", moving_count)
            st.metric("Stopped Vehicles", stopped_count)
            st.metric("Avg Moving Speed", f"{avg_moving_speed:.1f} km/h")

    with left_map:
        st.subheader("Last Updated Vehicle Locations")

        if len(df_map) > 0:
            df_display = df_map_filtered

            if selected_vehicle == 'All Vehicles':
                center_lat = df_display['latitude'].mean()
                center_lon = df_display['longitude'].mean()
                zoom_level = 11
            else:
                vehicle_data = df_display[df_display['vehicle_id'].astype(str) == selected_vehicle].iloc[0]
                center_lat = vehicle_data['latitude']
                center_lon = vehicle_data['longitude']
                zoom_level = 15

            fig_map = go.Figure()

            # Add vehicle markers
            fig_map.add_trace(go.Scattermapbox(
                lat=df_display['latitude'],
                lon=df_display['longitude'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=df_display['speed'],
                    colorscale=[[0, 'rgb(220, 20, 60)'], [0.5, 'rgb(255, 215, 0)'], [1, 'rgb(50, 205, 50)']],
                    cmin=0,
                    cmax=60,
                    showscale=True,
                    colorbar=dict(title="Speed<br>(km/h)")
                ),
                text=df_display.apply(lambda row: f"Vehicle: {row['vehicle_id']}<br>Speed: {row['speed']:.1f} km/h<br>Route: {row.get('route_id', 'N/A')}", axis=1),
                hoverinfo='text',
                name='Vehicles'
            ))

            # Add route stops
            if show_stops and df_routes is not None and len(df_routes) > 0:
                # Filter route stops based on selected route
                if selected_route != 'All Routes':
                    df_stops = df_routes[df_routes['route_id'] == selected_route]
                else:
                    df_stops = df_routes

                if len(df_stops) > 0:
                    fig_map.add_trace(go.Scattermapbox(
                        lat=df_stops['stop_lat'],
                        lon=df_stops['stop_lon'],
                        mode='markers',
                        marker=dict(
                            size=6,
                            color='rgba(255, 255, 255, 0.7)',
                            symbol='circle'
                        ),
                        text=df_stops.apply(lambda row: f"Stop: {row['stop_name']}<br>Stop ID: {row['stop_id']}<br>Route: {row['route_id']}", axis=1),
                        hoverinfo='text',
                        name='Stops'
                    ))

            fig_map.update_layout(
                mapbox_style="carto-darkmatter",
                mapbox=dict(
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=zoom_level
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=600
            )

            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No vehicle location data available")
