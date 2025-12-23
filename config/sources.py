import streamlit as st
import psycopg2
import pandas as pd

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets['postgres'])

def get_connection():
    """Get a connection, reconnecting if necessary"""
    conn = init_connection()
    try:
        # Test if connection is alive
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
    except Exception:
        # Connection is dead, clear cache and reconnect
        st.cache_resource.clear()
        conn = init_connection()
    return conn

@st.cache_data(ttl=1800)
def get_active_transit_data():
    conn = get_connection()
    query = "SELECT * FROM public.fct_active_vehicles"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl=7200)
def get_historical_transit_data():
    conn = get_connection()
    query = "SELECT * FROM public.oc_historical_snapshots"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl=3600)
def get_historical_weather_data():
    conn = get_connection()
    query = "SELECT * FROM public.fct_current_weather"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl=None)
def get_route_stops_data():
    conn = get_connection()
    query = "SELECT stop_id, stop_name, stop_sequence, route_id, stop_code, stop_lat, stop_lon FROM public.dim_stops"
    return pd.read_sql_query(query, conn)
