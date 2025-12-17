def calculate_metrics(df_historical):
    """Calculate key metrics from historical data."""

    df_sorted = df_historical.sort_values('snapshot_timestamp', ascending=False)

    active_transit_count = df_sorted['active_buses'].iloc[0]
    last_transit_count = df_sorted['active_buses'].iloc[1] if len(df_sorted) > 1 else active_transit_count
    change_transit_count = active_transit_count - last_transit_count

    active_route_count = df_sorted['active_routes'].iloc[0]
    last_route_count = df_sorted['active_routes'].iloc[1] if len(df_sorted) > 1 else active_route_count
    change_route_count = active_route_count - last_route_count

    moving_average_speed = df_sorted['average_moving_speed'].iloc[0]
    last_average_moving_speed = df_sorted['average_moving_speed'].iloc[1] if len(df_sorted) > 1 else moving_average_speed
    change_active_speed = ((moving_average_speed - last_average_moving_speed) / last_average_moving_speed) * 100 if last_average_moving_speed != 0 else 0

    last_updated = df_sorted['snapshot_timestamp'].iloc[0]
    last_updated_str = last_updated.strftime("%Y-%m-%d %I:%M %p")

    prev_updated = df_sorted['snapshot_timestamp'].iloc[1] if len(df_sorted) > 1 else last_updated
    prev_updated_str = prev_updated.strftime("%I:%M %p")

    return {
        'active_transit_count': active_transit_count,
        'change_transit_count': change_transit_count,
        'active_route_count': active_route_count,
        'change_route_count': change_route_count,
        'moving_average_speed': moving_average_speed,
        'change_active_speed': change_active_speed,
        'last_updated_str': last_updated_str,
        'prev_updated_str': prev_updated_str
    }
