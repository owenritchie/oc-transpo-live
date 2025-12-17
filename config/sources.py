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
        conn.isolation_level
    except (psycopg2.OperationalError, psycopg2.InterfaceError):
        # Connection is dead, clear cache and reconnect
        st.cache_resource.clear()
        conn = init_connection()
    return conn

@st.cache_data(ttl=600)
def get_active_transit_data():
    conn = get_connection()
    query = "SELECT * FROM public.fct_active_vehicles"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl=600)
def get_historical_transit_data():
    conn = get_connection()
    query = "SELECT * FROM public.oc_historical_snapshots"
    return pd.read_sql_query(query, conn)